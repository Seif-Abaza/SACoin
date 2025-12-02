# The `SmartContract` class represents a smart contract with a name, condition function, action
# function, and the ability to execute based on conditions in a blockchain.
class SmartContract:
    def __init__(self, name, condition_fn, action_fn):
        self.name = name
        self.condition_fn = condition_fn  # blockchain -> bool
        self.action_fn = action_fn  # blockchain -> None
        self.active = True

    def try_execute(self, blockchain):
        if self.active and self.condition_fn(blockchain):
            self.action_fn(blockchain)
