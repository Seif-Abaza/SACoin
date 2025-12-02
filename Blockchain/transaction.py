# Make sure that __init__ accepts the following keys: sender, recipient, amount, tx_type, metadata, tx_id(optional), signature(optional)
# Create By Seif Abaza <seif.abaza@yandex.com>

import hashlib
import os
import sys
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Blockchain.Wallet.wallet import Wallet


class Transaction:
    def __init__(
        self,
        sender,
        recipient,
        amount=0,
        tx_type="Transfer",
        metadata=None,
        tx_id=None,
        signature=None,
    ):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.tx_type = tx_type
        self.metadata = metadata or {}
        self.tx_id = tx_id or str(uuid.uuid4())
        self.signature = signature

    def calculate_hash(self):
        base = f"{self.sender}{self.recipient}{self.amount}{self.tx_type}{self.metadata}{self.tx_id}"
        return hashlib.sha256(base.encode()).hexdigest()

    def sign_transaction(self, wallet: Wallet):
        if self.tx_type in ["Reward", "NFTMint"] and self.sender is None:
            # A formal transaction that does not require a signature
            return
        if wallet.public_hex != self.sender:
            raise Exception(
                "A signature cannot be obtained with a key that does not match the sender."
            )
        self.signature = wallet.sign(self.calculate_hash())

    def is_valid(self):
        if self.tx_type in ["Reward", "NFTMint"] and self.sender is None:
            return True
        if not self.signature or not self.sender:
            return False
        return Wallet.verify(self.sender, self.signature, self.calculate_hash())

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "tx_type": self.tx_type,
            "metadata": self.metadata,
            "tx_id": self.tx_id,
            "signature": self.signature,
        }
