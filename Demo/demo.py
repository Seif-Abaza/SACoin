import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.Wallet.wallet import Wallet

if __name__ == "__main__":
    bc = Blockchain()

    # Creating a wallets
    user_wallet = Wallet()
    miner_wallet = Wallet()

    # Correct transaction
    tx1 = Transaction(
        sender=user_wallet.public_hex, recipient=miner_wallet.public_hex, amount=20
    )
    tx1.sign_transaction(user_wallet)  # Signing the transaction
    bc.add_transaction(tx1)

    # Transaction Mining
    bc.mine_pending_transactions(miner_wallet.public_hex)

    # Unsigned transaction (must fail)
    try:
        tx2 = Transaction(
            sender=user_wallet.public_hex, recipient=miner_wallet.public_hex, amount=10
        )
        bc.add_transaction(tx2)  # Unsigned
    except Exception as e:
        print("Transaction declined:", e)

    # Display Results
    print("User Balance:", bc.get_balance(user_wallet.public_hex))
    print("Miner Balance:", bc.get_balance(miner_wallet.public_hex))
    print("Is Chain Valid?", bc.is_chain_valid())
