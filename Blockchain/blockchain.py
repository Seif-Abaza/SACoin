# This file contains blocks, mining, adding transactions, and executing contracts.
# Create By Seif Abaza <seif.abaza@yandex.com>

import hashlib
import os
import sys
import time
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Blockchain.transaction import Transaction
from SmartContract.nft_registry import NFTRegistry
from SmartContract.smart_contract import SmartContract


class Block:
    def __init__(
        self,
        index,
        previous_hash,
        transactions: List[Transaction],
        timestamp=None,
        nonce=0,
    ):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{[t.to_dict() for t in self.transactions]}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self, difficulty=3, mining_reward=50):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = mining_reward
        self.contracts: List[SmartContract] = []
        self.nft = NFTRegistry()

    def create_genesis_block(self):
        """
        The function creates a genesis block with specified attributes.
        :return: A genesis block is being returned.
        """
        return Block(0, "0", [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        """
        The `add_transaction` function adds a transaction to a list of pending transactions after
        checking if it is valid.

        :param transaction: The `add_transaction` method takes in a `Transaction` object as a parameter.
        This method checks if the transaction is valid by calling the `is_valid` method on the
        `Transaction` object. If the transaction is not valid, it raises an exception indicating that
        the transaction is either invalid or unsigned
        :type transaction: Transaction
        """
        if not transaction.is_valid():
            raise Exception("❌ The transaction is invalid or unsigned.")
        self.pending_transactions.append(transaction)

    def add_contract(self, contract: SmartContract):
        self.contracts.append(contract)

    def mine_pending_transactions(self, miner_address):
        # Reward the miner
        reward_tx = Transaction(
            sender=None,
            recipient=miner_address,
            amount=self.mining_reward,
            tx_type="Reward",
        )
        self.pending_transactions.append(reward_tx)

        # Mining a block
        new_block = Block(
            len(self.chain), self.get_latest_block().hash, self.pending_transactions
        )
        self.mine_block(new_block)
        self.chain.append(new_block)

        # Applying block effects (balances and NFT ownership)
        self.apply_block_effects(new_block)

        # Clear the transaction pool
        self.pending_transactions = []

        # Attempt to execute contracts after each block
        for contract in self.contracts:
            contract.try_execute(self)
        return new_block.calculate_hash()

    def mine_block(self, block: Block):
        while block.hash[: self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        print(f"✅ Block mined {block.index}: {block.hash}")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def apply_block_effects(self, block: Block):
        for tx in block.transactions:
            # Upgrade NFT Owner
            if tx.tx_type == "NFTMint":
                nft_id = tx.metadata.get("nft_id")
                self.nft.mint(nft_id, tx.recipient, tx.metadata)
            elif tx.tx_type == "NFTTransfer":
                nft_id = tx.metadata.get("nft_id")
                self.nft.transfer(nft_id, tx.sender, tx.recipient)

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.tx_type in ["Transfer", "Reward"]:
                    if tx.sender == address and tx.amount:
                        balance -= tx.amount
                    if tx.recipient == address and tx.amount:
                        balance += tx.amount
                elif tx.tx_type == "Burn":
                    if tx.sender == address and tx.amount:
                        balance -= tx.amount
        return balance
