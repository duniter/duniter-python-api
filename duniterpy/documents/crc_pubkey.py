from typing import TypeVar, Type

import base58
import re
import hashlib
from ..constants import PUBKEY_REGEX
from ..tools import ensure_str

# required to type hint cls in classmethod
CRCPubkeyType = TypeVar("CRCPubkeyType", bound="CRCPubkey")


class CRCPubkey:
    """
    Class to implement a crc on a pubkey
    """

    re_crc_pubkey = re.compile(
        "({pubkey_regex}):([A-Za-z0-9]{{3}})".format(pubkey_regex=PUBKEY_REGEX)
    )

    def __init__(self, pubkey: str, crc: str) -> None:
        """
        Creates a pubkey with a crc

        :param pubkey: Public key
        :param crc: CRC
        """
        self.pubkey = pubkey
        self.crc = crc

    @classmethod
    def from_str(cls: Type[CRCPubkeyType], crc_pubkey: str) -> CRCPubkeyType:
        """
        Return CRCPubkey instance from CRC public key string

        :param crc_pubkey: CRC public key
        :return:
        """
        data = CRCPubkey.re_crc_pubkey.match(crc_pubkey)
        if data is None:
            raise Exception("Could not parse CRC public key {0}".format(crc_pubkey))
        pubkey = data.group(1)
        crc = data.group(2)
        return cls(pubkey, crc)

    @classmethod
    def from_pubkey(cls: Type[CRCPubkeyType], pubkey: str) -> CRCPubkeyType:
        """
        Return CRCPubkey instance from public key string

        :param pubkey: Public key
        :return:
        """
        hash_root = hashlib.sha256()
        hash_root.update(base58.b58decode(pubkey))
        hash_squared = hashlib.sha256()
        hash_squared.update(hash_root.digest())
        b58_checksum = ensure_str(base58.b58encode(hash_squared.digest()))

        crc = b58_checksum[:3]
        return cls(pubkey, crc)

    def is_valid(self) -> bool:
        """
        Return True if CRC is valid
        :return:
        """
        return CRCPubkey.from_pubkey(self.pubkey).crc == self.crc

    def __str__(self) -> str:
        """
        Return string representation of instance
        :return:
        """
        return "{:}:{:}".format(self.pubkey, self.crc)
