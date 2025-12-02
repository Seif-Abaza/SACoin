#!/opt/conda/miniconda3/envs/sacoin/bin/python

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.Wallet.wallet import Wallet


def WalletTransactions(bc: Blockchain, sender: Wallet, receiver: Wallet, amount: int):
    tx1 = Transaction(
        sender=sender.public_hex, recipient=receiver.public_hex, amount=amount
    )
    tx1.sign_transaction(sender)  # Signing the transaction
    bc.add_transaction(tx1)
    # Transaction Mining
    return bc.mine_pending_transactions(receiver.public_hex)


def create_NFT(bc: Blockchain, Owner: Wallet, metadata: dict):
    nft_tx = Transaction(
        sender=None,
        recipient=Owner.public_hex,
        amount=0,
        tx_type="NFTMint",
        metadata=metadata,
    )
    bc.add_transaction(nft_tx)

    # NFT transaction mining
    bc.mine_pending_transactions(Owner.public_hex)


if __name__ == "__main__":
    # Creating a new blockchain
    bc = Blockchain(difficulty=3, mining_reward=50)

    # Creating Wallets

    # Normal User
    user_wallet = Wallet()

    # Miner Wallet ( Pool )
    miner_wallet = Wallet()

    # NFT Owner
    nft_owner_wallet = Wallet()

    print("🔑 User address:", user_wallet.public_hex)
    print("🔑 Miner's address:", miner_wallet.public_hex)
    print("🔑 NFT owner address:", nft_owner_wallet.public_hex)
    # Wallets balance
    print(f"User's Balance : ", bc.get_balance(user_wallet.public_hex))
    print(f"Miner's Balance : ", bc.get_balance(miner_wallet.public_hex))
    print(f"NFT's User Balance : ", bc.get_balance(nft_owner_wallet.public_hex))

    # Mining: The miner starts by mining an empty block (receiving a reward)
    bc.mine_pending_transactions(miner_wallet.public_hex)

    # Send and Receive: The user sends 25 coins to the miner
    WalletTransactions(bc, user_wallet, miner_wallet, 25)

    # Creating an NFT: Issuing a new digital asset for the third wallet
    create_NFT(
        bc=bc,
        Owner=nft_owner_wallet,
        metadata={"nft_id": "NFT-001", "name": "iPad 1234"},
    )
    # User Wallet
    create_NFT(
        bc=bc,
        Owner=user_wallet,
        metadata={"nft_id": "NFT-002", "name": "iPhone"},
    )
    # --- Show Results ---
    print("\n--- Show Results ---")
    print("User balance:", bc.get_balance(user_wallet.public_hex))
    print("Miner's balance:", bc.get_balance(miner_wallet.public_hex))
    print("NFT owner balance:", bc.get_balance(nft_owner_wallet.public_hex))
    print("Record NFTs:", bc.nft.all())

    # Get all blocks
    print("\n\nExplore")
    print("*" * 30)
    for block in bc.chain:
        print(f"\nblock {block.index}:")
        for tx in block.transactions:
            print(
                f"- Transaction type: {tx.tx_type}, Sender: {tx.sender}, Receiver: {tx.recipient}, Data: {tx.metadata}"
            )
        print(f"Hash: {block.hash}")
