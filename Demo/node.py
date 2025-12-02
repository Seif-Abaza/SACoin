import asyncio
import os
import sys
from typing import Dict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Blockchain.blockchain import Block, Blockchain
from Blockchain.transaction import Transaction
from Network.p2p import P2PNode, PeerInfo


class SACoinNode:
    def __init__(self, host="127.0.0.1", port=9001, seeds=None):
        self.bc = Blockchain(difficulty=3, mining_reward=50)
        self.p2p = P2PNode(host, port, self.on_message)
        self.seeds = seeds or []
        self.mempool = set()  # tx_id to prevent duplication

    async def start(self):
        await self.p2p.start()
        await self.bootstrap()
        # Update best_height regularly
        asyncio.create_task(self._height_updater())

    async def bootstrap(self):
        for h, p in self.seeds:
            await self.p2p.connect_to(h, p)

    async def _height_updater(self):
        while True:
            self.p2p.set_best_height(len(self.bc.chain) - 1)
            await asyncio.sleep(2)

    def on_message(self, msg: Dict, peer: PeerInfo):
        t = msg.get("type")
        if t == "hello":
            # Integrating the peer list and the experience of contacting them
            for p in msg.get("peers", []):
                asyncio.create_task(self.p2p.connect_to(p["host"], p["port"]))
        elif t == "tx":
            txd = msg.get("data")
            if not txd:
                return
            tx = Transaction(**txd)
            if tx.tx_id in self.mempool:
                return
            try:
                if not tx.is_valid():
                    return
                self.bc.add_transaction(tx)
                self.mempool.add(tx.tx_id)
                asyncio.create_task(
                    self.p2p.broadcast(
                        {"type": "tx", "data": tx.to_dict()}, exclude=peer
                    )
                )
                print(f"[Node] Received and broadcast a transaction: {tx.tx_id}")
            except Exception:
                pass
        elif t == "new_block":
            bd = msg.get("data")
            if not bd:
                return
            # Simple check: Recalculate the hash and link the chain
            block = self._block_from_dict(bd)
            if self._validate_and_attach(block):
                asyncio.create_task(
                    self.p2p.broadcast(
                        {"type": "new_block", "data": self._block_to_dict(block)},
                        exclude=peer,
                    )
                )
                print(f"[Node] Added a block from peer: {block.index}")

        elif t == "get_status":
            asyncio.create_task(
                self.p2p.send(
                    peer,
                    {
                        "type": "status",
                        "data": {
                            "best_height": len(self.bc.chain) - 1,
                            "peers": [p.to_dict() for p in self.p2p.peers],
                        },
                    },
                )
            )

    def _block_to_dict(self, b: Block):
        return {
            "index": b.index,
            "previous_hash": b.previous_hash,
            "timestamp": b.timestamp,
            "transactions": [tx.to_dict() for tx in b.transactions],
            "nonce": b.nonce,
            "hash": b.hash,
        }

    def _block_from_dict(self, d: Dict):
        txs = []
        for t in d["transactions"]:
            txs.append(Transaction(**t))
        b = Block(d["index"], d["previous_hash"], txs, d["timestamp"], d["nonce"])
        return b

    def _validate_and_attach(self, block: Block) -> bool:
        # Basic chain verification
        latest = self.bc.get_latest_block()
        if block.previous_hash != latest.hash:
            return False
        # Verify the retail
        if block.calculate_hash() != block.hash:
            return False
        # Difficulty Check
        if not block.hash.startswith("0" * self.bc.difficulty):
            return False
        # Transaction verification
        for tx in block.transactions:
            if not tx.is_valid():
                return False
        # Appending
        self.bc.chain.append(block)
        self.bc.apply_block_effects(block)
        return True

    async def mine(self, miner_address: str):
        # Mining pending transactions locally and then broadcasting the block
        self.bc.mine_pending_transactions(miner_address)
        new_block = self.bc.get_latest_block()
        await self.p2p.broadcast(
            {"type": "new_block", "data": self._block_to_dict(new_block)}
        )
        print(f"[Node] Broadcast Block: {new_block.index}")
