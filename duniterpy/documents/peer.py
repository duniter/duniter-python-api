import re

from ..api.bma import ConnectionHandler
from .document import Document, MalformedDocumentError
from . import BlockUID
from .. import PROTOCOL_VERSION, MANAGED_API
from .constants import block_hash_regex, pubkey_regex

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

    def __init__(self, version, currency, pubkey, blockUID,
                 endpoints, signature):
        super().__init__(version, currency, [signature])

        self.pubkey = pubkey
        self.blockUID = blockUID
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

        blockUID = BlockUID.from_str(Peer.parse_field("Block", lines[n]))
        n += 1

        Peer.parse_field("Endpoints", lines[n])
        n += 1

        endpoints = []
        while not Peer.re_signature.match(lines[n]):
            endpoint = Endpoint.from_inline(lines[n])
            endpoints.append(endpoint)
            n += 1

        signature = Peer.re_signature.match(lines[n]).group(1)

        return cls(version, currency, pubkey, blockUID, endpoints, signature)

    def raw(self):
        doc = """Version: {0}
Type: Peer
Currency: {1}
PublicKey: {2}
Block: {3}
Endpoints:
""".format(self.version, self.currency, self.pubkey, self.blockUID)

        for endpoint in self.endpoints:
            doc += "{0}\n".format(endpoint.inline())

        return doc


class Endpoint:
    """
    Describing endpoints
    """

    @staticmethod
    def from_inline(inline):
        for api in MANAGED_API:
            if (inline.startswith(api)):
                if (api == "BASIC_MERKLED_API"):
                    return BMAEndpoint.from_inline(inline)
        return UnknownEndpoint.from_inline(inline)


class UnknownEndpoint(Endpoint):

    def __init__(self, api, properties):
        self.api = api
        self.properties = properties

    @classmethod
    def from_inline(cls, inline):
        api = inline.split()[0]
        properties = inline.split()[1:]
        return cls(api, properties)

    def inline(self):
        doc = self.api
        for p in self.properties:
            doc += " {0}".format(p)
        return doc


class BMAEndpoint(Endpoint):
    re_inline = re.compile('^BASIC_MERKLED_API(?: ([a-z0-9-_.]*(?:.[a-zA-Z])))?(?: ((?:[0-9.]{1,4}){4}))?(?: ((?:[0-9a-f:]{4,5}){4,8}))?(?: ([0-9]+))$')

    @classmethod
    def from_inline(cls, inline):
        m = BMAEndpoint.re_inline.match(inline)
        if m is None:
            raise MalformedDocumentError("BMAEndpoint")
        server = m.group(1)
        ipv4 = m.group(2)
        ipv6 = m.group(3)
        port = int(m.group(4))
        return cls(server, ipv4, ipv6, port)

    def __init__(self, server, ipv4, ipv6, port):
        self.server = server
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.port = port

    def inline(self):
        return "BASIC_MERKLED_API{DNS}{IPv4}{IPv6}{PORT}" \
                    .format(DNS=(" {0}".format(self.server) if self.server else ""),
                            IPv4=(" {0}".format(self.ipv4) if self.ipv4 else ""),
                            IPv6=(" {0}".format(self.ipv6) if self.ipv6 else ""),
                            PORT=(" {0}".format(self.port) if self.port else ""))

    def conn_handler(self):
        if self.server:
            return ConnectionHandler(self.server, self.port)
        elif self.ipv4:
            return ConnectionHandler(self.ipv4, self.port)
        else:
            return ConnectionHandler(self.ipv6, self.port)
