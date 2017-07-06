import base58
import re
import hashlib
from .constants import pubkey_regex


class CRCPubkey:
    """
    Class to implement a crc on a pubkey
    """
    re_crc_pubkey = re.compile("({pubkey_regex}):([A-Za-z0-9]{{3}})".format(pubkey_regex=pubkey_regex))

    def __init__(self, pubkey, crc):
        """
        Creates a pubkey with a crc
        :param pubkey:
        """
        self.pubkey = pubkey
        self.crc = crc

    @classmethod
    def from_str(cls, str):
        data = CRCPubkey.re_crc_pubkey.match(str)
        pubkey = data.group(1)
        crc = data.group(2)
        return cls(pubkey, crc)

    @classmethod
    def from_pubkey(cls, pubkey):
        hash_root = hashlib.sha256()
        hash_root.update(base58.b58decode(pubkey))
        hash_squared = hashlib.sha256()
        hash_squared.update(hash_root.digest())
        b58_checksum = base58.b58encode(hash_squared.digest())

        crc = b58_checksum[:3]
        return cls(pubkey, crc)

    def is_valid(self):
        return CRCPubkey.from_pubkey(self.pubkey).crc == self.crc

    def __str__(self):
        return "{:}:{:}".format(self.pubkey, self.crc)