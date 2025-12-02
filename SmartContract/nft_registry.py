class NFTRegistry:
    def __init__(self):
        # nft_id -> {"owner": address, "metadata": {...}}
        self.store = {}

    def mint(self, nft_id: str, owner: str, metadata=None):
        if nft_id in self.store:
            # منع إعادة الإصدار لنفس المعرف
            return
        self.store[nft_id] = {"owner": owner, "metadata": metadata or {}}

    def transfer(self, nft_id: str, from_addr: str, to_addr: str):
        if nft_id not in self.store:
            return
        if self.store[nft_id]["owner"] != from_addr:
            return
        self.store[nft_id]["owner"] = to_addr

    def owner_of(self, nft_id: str):
        return self.store.get(nft_id, {}).get("owner")

    def all(self):
        return self.store
