import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from node import SACoinNode

from Blockchain.transaction import Transaction
from Blockchain.Wallet.wallet import Wallet


async def main():
    # Node 3 on port 9003
    node3 = SACoinNode(port=9003, seeds=[("127.0.0.1", 9001)])
    await node3.start()

    # Wallets
    user_wallet = Wallet()
    miner_wallet = Wallet()

    # Make transaction
    tx = Transaction(
        sender=user_wallet.public_hex, recipient=miner_wallet.public_hex, amount=15
    )
    tx.sign_transaction(user_wallet)
    node3.bc.add_transaction(tx)

    # mining
    while True:
        await node3.mine(miner_wallet.public_hex)
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
