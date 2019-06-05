import re
from typing import TypeVar, List, Type

from duniterpy.api.endpoint import endpoint, Endpoint
from .document import Document, MalformedDocumentError
from .block_uid import BlockUID
from ..constants import BLOCK_HASH_REGEX, PUBKEY_REGEX

# required to type hint cls in classmethod
PeerType = TypeVar("PeerType", bound="Peer")


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
    re_pubkey = re.compile(
        "PublicKey: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX)
    )
    re_block = re.compile(
        "Block: ([0-9]+-{block_hash_regex})\n".format(block_hash_regex=BLOCK_HASH_REGEX)
    )
    re_endpoints = re.compile("(Endpoints:)\n")

    fields_parsers = {
        **Document.fields_parsers,
        **{
            "Type": re_type,
            "Pubkey": re_pubkey,
            "Block": re_block,
            "Endpoints": re_endpoints,
        },
    }

    def __init__(
        self,
        version: int,
        currency: str,
        pubkey: str,
        block_uid: BlockUID,
        endpoints: List[Endpoint],
        signature: str,
    ) -> None:
        """
        Init Peer instance

        :param version: Version of the document
        :param currency: Name of the currency
        :param pubkey: Public key of the issuer
        :param block_uid: BlockUID instance timestamp
        :param endpoints: List of endpoints string
        :param signature: Signature of the document
        """
        super().__init__(version, currency, [signature])

        self.pubkey = pubkey
        self.blockUID = block_uid
        self.endpoints = endpoints

    @classmethod
    def from_signed_raw(cls: Type[PeerType], raw: str) -> PeerType:
        """
        Return a Peer instance from a signed raw format string

        :param raw: Signed raw format string
        :return:
        """
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

        data = Peer.re_signature.match(lines[n])
        if data is None:
            raise MalformedDocumentError("Peer")
        signature = data.group(1)

        return cls(version, currency, pubkey, block_uid, endpoints, signature)

    def raw(self) -> str:
        """
        Return a raw format string of the Peer document

        :return:
        """
        doc = """Version: {0}
Type: Peer
Currency: {1}
PublicKey: {2}
Block: {3}
Endpoints:
""".format(
            self.version, self.currency, self.pubkey, self.blockUID
        )

        for _endpoint in self.endpoints:
            doc += "{0}\n".format(_endpoint.inline())

        return doc
