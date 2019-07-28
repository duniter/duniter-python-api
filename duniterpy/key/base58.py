from typing import Union

import base58

from ..tools import ensure_str, ensure_bytes


class Base58Encoder:
    @staticmethod
    def encode(data: Union[str, bytes]) -> str:
        """
        Return Base58 string from data

        :param data: Bytes or string data
        """
        return ensure_str(base58.b58encode(ensure_bytes(data)))

    @staticmethod
    def decode(data: str) -> bytes:
        """
        Decode Base58 string data and return bytes

        :param data: Base58 string
        """
        return base58.b58decode(data)
