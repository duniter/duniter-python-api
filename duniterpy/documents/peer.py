import re
from typing import Generator

from ..api.bma import ConnectionHandler
from .document import Document, MalformedDocumentError
from . import BlockUID
from .constants import block_hash_regex, pubkey_regex, ipv4_regex, ipv6_regex, ws2pid_regex, host_regex, path_regex


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
            endpoints.append(endpoint(lines[n]))
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


def endpoint(value):
    if issubclass(type(value), Endpoint):
        return value
    elif isinstance(value, str):
        for api, cls in MANAGED_API.items():
            if value.startswith(api + " "):
                return cls.from_inline(value)
        return UnknownEndpoint.from_inline(value)
    else:
        raise TypeError("Cannot convert {0} to endpoint".format(value))


class Endpoint():
    @classmethod
    def from_inline(cls, inline):
        raise NotImplementedError("from_inline(..) is not implemented")

    def inline(self):
        raise NotImplementedError("inline() is not implemented")

    def __str__(self):
        raise NotImplementedError("__str__ is not implemented")

    def __eq__(self, other):
        raise NotImplementedError("__eq__ is not implemented")


class UnknownEndpoint(Endpoint):
    API = None

    def __init__(self, api, properties):
        self.api = api
        self.properties = properties

    @classmethod
    def from_inline(cls, inline):
        try:
            api = inline.split()[0]
            properties = inline.split()[1:]
            return cls(api, properties)
        except IndexError:
            raise MalformedDocumentError(inline)

    def inline(self):
        doc = self.api
        for p in self.properties:
            doc += " {0}".format(p)
        return doc

    def __str__(self):
        return "{0} {1}".format(self.api, ' '.join(["{0}".format(p) for p in self.properties]))

    def __eq__(self, other):
        if isinstance(other, UnknownEndpoint):
            return self.api == other.api and self.properties == other.properties
        else:
            return False

    def __hash__(self):
        return hash((self.api, self.properties))


class BMAEndpoint(Endpoint):
    API = "BASIC_MERKLED_API"
    re_inline = re.compile('^BASIC_MERKLED_API(?: ({host_regex}))?(?: ({ipv4_regex}))?(?: ({ipv6_regex}))?(?: ([0-9]+))$'.format(host_regex=host_regex,
                                                                                                                                 ipv4_regex=ipv4_regex,
                                                                                                                                 ipv6_regex=ipv6_regex))

    def __init__(self, server, ipv4, ipv6, port):
        self.server = server
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.port = port

    @classmethod
    def from_inline(cls, inline):
        m = BMAEndpoint.re_inline.match(inline)
        str_re = BMAEndpoint.re_inline.pattern
        if m is None:
            raise MalformedDocumentError(BMAEndpoint.API)
        server = m.group(1)
        ipv4 = m.group(2)
        ipv6 = m.group(3)
        port = int(m.group(4))
        return cls(server, ipv4, ipv6, port)

    def inline(self):
        return BMAEndpoint.API + "{DNS}{IPv4}{IPv6}{PORT}" \
                    .format(DNS=(" {0}".format(self.server) if self.server else ""),
                            IPv4=(" {0}".format(self.ipv4) if self.ipv4 else ""),
                            IPv6=(" {0}".format(self.ipv6) if self.ipv6 else ""),
                            PORT=(" {0}".format(self.port) if self.port else ""))

    def conn_handler(self, session=None, proxy=None):
        """
        Return connection handler instance for the endpoint

        :param aiohttp.ClientSession session: AIOHTTP client session instance
        :param str proxy: Proxy url
        :rtype: Generator[ConnectionHandler, None, None]
        """
        if self.server:
            yield ConnectionHandler("http", "ws", self.server, self.port, "", proxy, session)
        elif self.ipv6:
            yield ConnectionHandler("http", "ws", "[{0}]".format(self.ipv6), self.port, "", proxy, session)
        else:
            yield ConnectionHandler("http", "ws", self.ipv4, self.port, "", proxy, session)

    def __str__(self):
        return self.inline()

    def __eq__(self, other):
        if isinstance(other, BMAEndpoint):
            return self.server == other.server and self.ipv4 == other.ipv4 \
                    and self.ipv6 == other.ipv6 and self.port == other.port
        else:
            return False

    def __hash__(self):
        return hash((self.server, self.ipv4, self.ipv6, self.port))


class SecuredBMAEndpoint(BMAEndpoint):
    API = "BMAS"
    re_inline = re.compile('^BMAS(?: ({host_regex}))?(?: ({ipv4_regex}))?(?: ({ipv6_regex}))? ([0-9]+)(?: ({path_regex}))?$'.format(host_regex=host_regex,
                                                                                                                                   ipv4_regex=ipv4_regex,
                                                                                                                                   ipv6_regex=ipv6_regex,
                                                                                                                                   path_regex=path_regex))

    def __init__(self, server, ipv4, ipv6, port, path):
        super().__init__(server, ipv4, ipv6, port)
        self.path = path

    @classmethod
    def from_inline(cls, inline):
        m = SecuredBMAEndpoint.re_inline.match(inline)
        if m is None:
            raise MalformedDocumentError(SecuredBMAEndpoint.API)
        server = m.group(1)
        ipv4 = m.group(2)
        ipv6 = m.group(3)
        port = int(m.group(4))
        path = m.group(5)
        if not path:
            path = ""
        return cls(server, ipv4, ipv6, port, path)

    def inline(self):
        inlined = [str(info) for info in (self.server, self.ipv4, self.ipv6, self.port, self.path) if info]
        return SecuredBMAEndpoint.API + " " + " ".join(inlined)

    def conn_handler(self, session=None, proxy=None):
        """
        Return connection handler instance for the endpoint

        :param aiohttp.ClientSession session: AIOHTTP client session instance
        :param str proxy: Proxy url
        :rtype: Generator[ConnectionHandler, None, None]
        """
        if self.server:
            yield ConnectionHandler("https", "wss", self.server, self.port, self.path, proxy, session)
        elif self.ipv6:
            yield ConnectionHandler("https", "wss", "[{0}]".format(self.ipv6), self.port, self.path, proxy, session)
        else:
            yield ConnectionHandler("https", "wss", self.ipv4, self.port, self.path, proxy, session)


class WS2PEndpoint(Endpoint):
    API = "WS2P"
    re_inline = re.compile('^WS2P ({ws2pid_regex}) ((?:{host_regex})|(?:{ipv4_regex})) ([0-9]+)?(?: ({path_regex}))?$'.format(ws2pid_regex=ws2pid_regex,
                                                                                                                 host_regex=host_regex,
                                                                                                                 ipv4_regex=ipv4_regex,
                                                                                                                 ipv6_regex=ipv6_regex,
                                                                                                                 path_regex=path_regex))

    def __init__(self, ws2pid, server, port, path):
        self.ws2pid = ws2pid
        self.server = server
        self.port = port
        self.path = path

    @classmethod
    def from_inline(cls, inline):
        m = WS2PEndpoint.re_inline.match(inline)
        if m is None:
            raise MalformedDocumentError(WS2PEndpoint.API)
        ws2pid = m.group(1)
        server = m.group(2)
        port = int(m.group(3))
        path = m.group(4)
        if not path:
            path = ""
        return cls(ws2pid, server, port, path)

    def inline(self):
        inlined = [str(info) for info in (self.ws2pid, self.server, self.port, self.path) if info]
        return WS2PEndpoint.API + " " + " ".join(inlined)

    def conn_handler(self, session=None, proxy=None):
        """
        Return connection handler instance for the endpoint

        :param aiohttp.ClientSession session: AIOHTTP client session instance
        :rtype: ConnectionHandler
        """
        yield ConnectionHandler("https", "wss", self.server, self.port, self.path, proxy, session)

    def __str__(self):
        return self.inline()

    def __eq__(self, other):
        if isinstance(other, WS2PEndpoint):
            return self.server == other.server and self.ws2pid == other.ws2pid \
                    and self.port == other.port and self.path == other.path
        else:
            return False

    def __hash__(self):
        return hash((self.ws2pid, self.server, self.port, self.path))


class ESUserEndpoint(Endpoint):
    API = "ES_USER_API"
    re_inline = re.compile('^ES_USER_API ((?:{host_regex})|(?:{ipv4_regex})) ([0-9]+)$'.format(ws2pid_regex=ws2pid_regex,
                                                                                             host_regex=host_regex,
                                                                                             ipv4_regex=ipv4_regex))

    def __init__(self, server, port):
        self.server = server
        self.port = port

    @classmethod
    def from_inline(cls, inline):
        m = ESUserEndpoint.re_inline.match(inline)
        if m is None:
            raise MalformedDocumentError(ESUserEndpoint.API)
        server = m.group(1)
        port = int(m.group(2))
        return cls(server, port)

    def inline(self):
        inlined = [str(info) for info in (self.server, self.port) if info]
        return ESUserEndpoint.API + " " + " ".join(inlined)

    def conn_handler(self, session=None, proxy=None):
        """
        Return connection handler instance for the endpoint

        :param aiohttp.ClientSession session: AIOHTTP client session instance
        :rtype: ConnectionHandler
        """
        yield ConnectionHandler("https", "wss", self.server, self.port, "", proxy, session)

    def __str__(self):
        return self.inline()

    def __eq__(self, other):
        if isinstance(other, ESUserEndpoint):
            return self.server == other.server and self.port == other.port
        else:
            return False

    def __hash__(self):
        return hash((self.server, self.port))


class ESSubscribtionEndpoint(Endpoint):
    API = "ES_SUBSCRIPTION_API"
    re_inline = re.compile('^ES_SUBSCRIPTION_API ((?:{host_regex})|(?:{ipv4_regex})) ([0-9]+)$'.format(ws2pid_regex=ws2pid_regex,
                                                                                                      host_regex=host_regex,
                                                                                                      ipv4_regex=ipv4_regex))

    def __init__(self, server, port):
        self.server = server
        self.port = port

    @classmethod
    def from_inline(cls, inline):
        m = ESSubscribtionEndpoint.re_inline.match(inline)
        if m is None:
            raise MalformedDocumentError(ESSubscribtionEndpoint.API)
        server = m.group(1)
        port = int(m.group(2))
        return cls(server, port)

    def inline(self):
        inlined = [str(info) for info in (self.server, self.port) if info]
        return ESSubscribtionEndpoint.API + " " + " ".join(inlined)

    def conn_handler(self, session=None, proxy=None):
        """
        Return connection handler instance for the endpoint

        :param aiohttp.ClientSession session: AIOHTTP client session instance
        :rtype: ConnectionHandler
        """
        yield ConnectionHandler("https", "wss", self.server, self.port, "", proxy, session)

    def __str__(self):
        return self.inline()

    def __eq__(self, other):
        if isinstance(other, ESSubscribtionEndpoint):
            return self.server == other.server and self.port == other.port
        else:
            return False

    def __hash__(self):
        return hash((ESSubscribtionEndpoint.API, self.server, self.port))



MANAGED_API={
    BMAEndpoint.API: BMAEndpoint,
    SecuredBMAEndpoint.API: SecuredBMAEndpoint,
    WS2PEndpoint.API: WS2PEndpoint,
    ESUserEndpoint.API: ESUserEndpoint,
    ESSubscribtionEndpoint.API: ESSubscribtionEndpoint
}
