import asyncio
import json
import uuid
from typing import Callable, Dict, List, Optional


class PeerInfo:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def to_tuple(self):
        return (self.host, self.port)

    def to_dict(self):
        return {"host": self.host, "port": self.port}


class P2PNode:
    def __init__(
        self, host: str, port: int, on_message: Callable[[Dict, PeerInfo], None]
    ):
        self.host = host
        self.port = port
        self.node_id = str(uuid.uuid4())
        self.server: Optional[asyncio.AbstractServer] = None
        self.peers: List[PeerInfo] = []
        self.on_message = on_message
        self.best_height = 0
        # To prevent the same message from being rebroadcast
        self.seen_ids = set()

    def set_best_height(self, height: int):
        self.best_height = height

    async def start(self):
        self.server = await asyncio.start_server(self.handle_conn, self.host, self.port)
        print(f"[P2P] has started listening on {self.host}:{self.port}")

    async def connect_to(self, host: str, port: int):
        peer = PeerInfo(host, port)
        if any(p.to_tuple() == peer.to_tuple() for p in self.peers):
            return
        try:
            reader, writer = await asyncio.open_connection(host, port)
            self.peers.append(peer)
            await self.send_hello(writer)
            asyncio.create_task(self.read_loop(reader, peer))
            print(f"[P2P] Peer connection: {host}:{port}")
        except Exception as e:
            print(f"[P2P] Failed to connect to {host}:{port} - {e}")

    async def handle_conn(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        # Title of the next counterpart
        addr = writer.get_extra_info("peername")
        peer = PeerInfo(addr[0], addr[1])
        asyncio.create_task(self.read_loop(reader, peer))
        await self.send_hello(writer)

    async def read_loop(self, reader: asyncio.StreamReader, peer: PeerInfo):
        try:
            while True:
                line = await reader.readline()
                if not line:
                    break
                msg = json.loads(line.decode())
                msg_id = msg.get("id")
                if msg_id and msg_id in self.seen_ids:
                    continue
                if msg_id:
                    self.seen_ids.add(msg_id)
                self.on_message(msg, peer)
        except Exception as e:
            print(f"[P2P] Error reading from {peer.host}:{peer.port} - {e}")

    async def send(self, peer: PeerInfo, message: Dict):
        try:
            reader, writer = await asyncio.open_connection(peer.host, peer.port)
            message.setdefault("id", str(uuid.uuid4()))
            writer.write((json.dumps(message) + "\n").encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print(f"[P2P] Failed to send to {peer.host}:{peer.port} - {e}")

    async def broadcast(self, message: Dict, exclude: Optional[PeerInfo] = None):
        message.setdefault("id", str(uuid.uuid4()))
        for p in self.peers:
            if exclude and p.to_tuple() == exclude.to_tuple():
                continue
            try:
                reader, writer = await asyncio.open_connection(p.host, p.port)
                writer.write((json.dumps(message) + "\n").encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    async def send_hello(self, writer: asyncio.StreamWriter):
        hello = {
            "type": "hello",
            "node_id": self.node_id,
            "best_height": self.best_height,
            "peers": [p.to_dict() for p in self.peers],
            "id": str(uuid.uuid4()),
        }
        writer.write((json.dumps(hello) + "\n").encode())
        await writer.drain()
