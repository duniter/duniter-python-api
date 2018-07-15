import re

from duniterpy.api.endpoint import endpoint
from .document import Document
from . import BlockUID
from ..constants import block_hash_regex, pubkey_regex


class Peer(Document):
    """
.. note:: A peer document is specified by the following format :

    | Version: VERSION
    | Type: Peer
    | Currency: CURRENCY_NAME
    | PublicKey: NODE_PUBLICKEY
    | Block: BLOCK
    | Endpoints:
    | END_POINT_1
    | END_POINT_2
    | END_POINT_3
    | [...]

    """

    re_type = re.compile("Type: (Peer)")
    re_pubkey = re.compile("PublicKey: ({pubkey_regex})\n".format(pubkey_regex=pubkey_regex))
    re_block = re.compile("Block: ([0-9]+-{block_hash_regex})\n".format(block_hash_regex=block_hash_regex))
    re_endpoints = re.compile("(Endpoints:)\n")

    fields_parsers = {**Document.fields_parsers, **{
        "Type": re_type,
        "Pubkey": re_pubkey,
        "Block": re_block,
        "Endpoints": re_endpoints
    }}

    def __init__(self, version, currency, pubkey, block_uid,
                 endpoints, signature):
        super().__init__(version, currency, [signature])

        self.pubkey = pubkey
        self.blockUID = block_uid
        self.endpoints = endpoints

    @classmethod
    def from_signed_raw(cls, raw):
        lines = raw.splitlines(True)
        n = 0

        version = int(Peer.parse_field("Version", lines[n]))
        n += 1

        Peer.parse_field("Type", lines[n])
        n += 1

        currency = Peer.parse_field("Currency", lines[n])
        n += 1

        pubkey = Peer.parse_field("Pubkey", lines[n])
        n += 1

        block_uid = BlockUID.from_str(Peer.parse_field("Block", lines[n]))
        n += 1

        Peer.parse_field("Endpoints", lines[n])
        n += 1

        endpoints = []
        while not Peer.re_signature.match(lines[n]):
            endpoints.append(endpoint(lines[n]))
            n += 1

        signature = Peer.re_signature.match(lines[n]).group(1)

        return cls(version, currency, pubkey, block_uid, endpoints, signature)

    def raw(self):
        doc = """Version: {0}
Type: Peer
Currency: {1}
PublicKey: {2}
Block: {3}
Endpoints:
""".format(self.version, self.currency, self.pubkey, self.blockUID)

        for _endpoint in self.endpoints:
            doc += "{0}\n".format(_endpoint.inline())

        return doc
