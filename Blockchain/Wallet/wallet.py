# The `Wallet` class in Python provides functionality for generating a cryptographic wallet with a
# signing key, verifying key, and methods for signing and verifying messages using the SECP256k1
# curve.
# Create By Seif Abaza <seif.abaza@yandex.com>


from ecdsa import SECP256k1, SigningKey, VerifyingKey


class Wallet:
    def __init__(self, signing_key: SigningKey = None):
        self.sk = signing_key or SigningKey.generate(curve=SECP256k1)
        self.vk = self.sk.verifying_key

    @property
    def private_hex(self):
        return self.sk.to_string().hex()

    @property
    def public_hex(self):
        return self.vk.to_string().hex()

    def sign(self, message: str) -> str:
        return self.sk.sign(message.encode()).hex()

    @staticmethod
    def verify(public_hex: str, signature_hex: str, message: str) -> bool:
        vk = VerifyingKey.from_string(bytes.fromhex(public_hex), curve=SECP256k1)
        try:
            return vk.verify(bytes.fromhex(signature_hex), message.encode())
        except:
            return False
