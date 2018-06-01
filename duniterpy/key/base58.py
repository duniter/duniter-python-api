import base58
from ..helpers import ensure_str, ensure_bytes


class Base58Encoder(object):
    @staticmethod
    def encode(data):
        return ensure_str(base58.b58encode(ensure_bytes(data)))

    @staticmethod
    def decode(data):
        return base58.b58decode(data)
