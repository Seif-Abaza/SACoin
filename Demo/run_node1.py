import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from node import SACoinNode

from Blockchain.Wallet.wallet import Wallet


async def main():
    # Node 1 on port 9001
    node1 = SACoinNode(port=9001, seeds=[("127.0.0.1", 9001)])
    await node1.start()

    # Wallet Mining
    miner_wallet = Wallet()

    # Mining
    while True:
        await node1.mine(miner_wallet.public_hex)
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
