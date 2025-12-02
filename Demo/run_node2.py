import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from node import SACoinNode

from Blockchain.transaction import Transaction
from Blockchain.Wallet.wallet import Wallet


async def main():
    # Node 2 on port 9002
    node2 = SACoinNode(port=9002, seeds=[("127.0.0.1", 9001)])
    await node2.start()

    # Wallets
    user_wallet = Wallet()
    miner_wallet = Wallet()

    # Make transaction
    tx = Transaction(
        sender=user_wallet.public_hex, recipient=miner_wallet.public_hex, amount=10
    )
    tx.sign_transaction(user_wallet)
    node2.bc.add_transaction(tx)

    # mining
    while True:
        await node2.mine(miner_wallet.public_hex)
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
