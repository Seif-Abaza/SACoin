import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from node import SACoinNode

from Blockchain.transaction import Transaction
from Blockchain.Wallet.wallet import Wallet


async def run():
    # Set up three contracts on different outlets
    node1 = SACoinNode(port=9005, seeds=[("127.0.0.1", 9002)])
    node2 = SACoinNode(port=9006, seeds=[])
    node3 = SACoinNode(port=9007, seeds=[])

    await asyncio.gather(node1.start(), node2.start(), node3.start())

    # Wallets
    w_user = Wallet()
    w_miner = Wallet()

    # Create, sign, and broadcast a transaction via node1
    tx = Transaction(sender=w_user.public_hex, recipient=w_miner.public_hex, amount=25)
    tx.sign_transaction(w_user)

    # Add the transaction to node1 (it will be broadcast automatically when mining or we can broadcast it manually)
    node1.bc.add_transaction(tx)

    # Mining on node2 then broadcasting the block
    await node2.mine(w_miner.public_hex)

    # Waiting for synchronization
    await asyncio.sleep(2)

    print("Chain height:")
    print(len(node1.bc.chain), len(node2.bc.chain), len(node3.bc.chain))


if __name__ == "__main__":
    asyncio.run(run())
