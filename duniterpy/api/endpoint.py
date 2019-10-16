import re
from typing import Any, Optional, TypeVar, Type, Dict

from aiohttp import ClientSession

import duniterpy.constants as constants
from ..documents import MalformedDocumentError


class ConnectionHandler:
    """Helper class used by other API classes to ease passing server connection information."""

    def __init__(
        self,
        http_scheme: str,
        ws_scheme: str,
        server: str,
        port: int,
        path: str,
        session: ClientSession,
        proxy: Optional[str] = None,
    ) -> None:
        """
        Init instance of connection handler

        :param http_scheme: Http scheme
        :param ws_scheme: Web socket scheme
        :param server: Server IP or domain name
        :param port: Port number
        :param port: Url path
        :param session: Session AIOHTTP
        :param proxy: Proxy (optional, default=None)
        """
        self.http_scheme = http_scheme
        self.ws_scheme = ws_scheme
        self.server = server
        self.port = port
        self.path = path
        self.proxy = proxy
        self.session = session

    def __str__(self) -> str:
        return "connection info: %s:%d" % (self.server, self.port)


# required to type hint cls in classmethod
EndpointType = TypeVar("EndpointType", bound="Endpoint")


class Endpoint:
    @classmethod
    def from_inline(cls: Type[EndpointType], inline: str) -> EndpointType:
        raise NotImplementedError("from_inline(..) is not implemented")

    def inline(self) -> str:
        raise NotImplementedError("inline() is not implemented")

    def conn_handler(
        self, session: ClientSession, proxy: str = None
    ) -> ConnectionHandler:
        raise NotImplementedError("conn_handler is not implemented")

    def __str__(self) -> str:
        raise NotImplementedError("__str__ is not implemented")

    def __eq__(self, other: Any) -> bool:
        return NotImplemented


# required to type hint cls in classmethod
UnknownEndpointType = TypeVar("UnknownEndpointType", bound="UnknownEndpoint")


class UnknownEndpoint(Endpoint):
    API = None

    def __init__(self, api: str, properties: list) -> None:
        self.api = api
        self.properties = properties

    @classmethod
    def from_inline(cls: Type[UnknownEndpointType], inline: str) -> UnknownEndpointType:
        """
        Return UnknownEndpoint instance from endpoint string

        :param inline: Endpoint string
        :return:
        """
        try:
            api = inline.split()[0]
            properties = inline.split()[1:]
            return cls(api, properties)
        except IndexError:
            raise MalformedDocumentError(inline)

    def inline(self) -> str:
        """
        Return endpoint string

        :return:
        """
        doc = self.api
        for p in self.properties:
            doc += " {0}".format(p)
        return doc

    def conn_handler(
        self, session: ClientSession, proxy: str = None
    ) -> ConnectionHandler:
        """
        Return connection handler from session

        :param session: AIOHTTP Session
        :param proxy: Proxy server
        :return:
        """
        return ConnectionHandler("", "", "", 0, "", ClientSession())

    def __str__(self) -> str:
        return "{0} {1}".format(
            self.api, " ".join(["{0}".format(p) for p in self.properties])
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UnknownEndpoint):
            return NotImplemented
        return self.api == other.api and self.properties == other.properties

    def __hash__(self) -> int:
        return hash((self.api, self.properties))


# required to type hint cls in classmethod
BMAEndpointType = TypeVar("BMAEndpointType", bound="BMAEndpoint")


class BMAEndpoint(Endpoint):
    API = "BASIC_MERKLED_API"
    re_inline = re.compile(
        "^BASIC_MERKLED_API(?: ({host_regex}))?(?: ({ipv4_regex}))?(?: ({ipv6_regex}))?(?: ([0-9]+))$".format(
            host_regex=constants.HOST_REGEX,
            ipv4_regex=constants.IPV4_REGEX,
            ipv6_regex=constants.IPV6_REGEX,
        )
    )

    def __init__(self, server: str, ipv4: str, ipv6: str, port: int) -> None:
        """
        Init BMAEndpoint instance

        :param server: IP or domain name
        :param ipv4: IP as IPv4 format
        :param ipv6: IP as IPv6 format
        :param port: Port number
        """
        self.server = server
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.port = port

    @classmethod
    def from_inline(cls: Type[BMAEndpointType], inline: str) -> BMAEndpointType:
        """
        Return BMAEndpoint instance from endpoint string

        :param inline: Endpoint string
        :return:
        """
        m = BMAEndpoint.re_inline.match(inline)
        if m is None:
            raise MalformedDocumentError(BMAEndpoint.API)
        server = m.group(1)
        ipv4 = m.group(2)
        ipv6 = m.group(3)
        port = int(m.group(4))
        return cls(server, ipv4, ipv6, port)

    def inline(self) -> str:
        """
        Return endpoint string

        :return:
        """
        return BMAEndpoint.API + "{DNS}{IPv4}{IPv6}{PORT}".format(
            DNS=(" {0}".format(self.server) if self.server else ""),
            IPv4=(" {0}".format(self.ipv4) if self.ipv4 else ""),
            IPv6=(" {0}".format(self.ipv6) if self.ipv6 else ""),
            PORT=(" {0}".format(self.port) if self.port else ""),
        )

    def conn_handler(
        self, session: ClientSession, proxy: str = None
    ) -> ConnectionHandler:
        """
        Return connection handler instance for the endpoint

        :param session: AIOHTTP client session instance
        :param proxy: Proxy url
        :return:
        """
        if self.server:
            conn_handler = ConnectionHandler(
                "http", "ws", self.server, self.port, "", session, proxy
            )
        elif self.ipv6:
            conn_handler = ConnectionHandler(
                "http", "ws", "[{0}]".format(self.ipv6), self.port, "", session, proxy
            )
        else:
            conn_handler = ConnectionHandler(
                "http", "ws", self.ipv4, self.port, "", session, proxy
            )

        return conn_handler

    def __str__(self) -> str:
        return self.inline()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BMAEndpoint):
            return NotImplemented
        return (
            self.server == other.server
            and self.ipv4 == other.ipv4
            and self.ipv6 == other.ipv6
            and self.port == other.port
        )

    def __hash__(self) -> int:
        return hash((self.server, self.ipv4, self.ipv6, self.port))


# required to type hint cls in classmethod
SecuredBMAEndpointType = TypeVar("SecuredBMAEndpointType", bound="SecuredBMAEndpoint")


class SecuredBMAEndpoint(BMAEndpoint):
    API = "BMAS"
    re_inline = re.compile(
        "^BMAS(?: ({host_regex}))?(?: ({ipv4_regex}))?(?: ({ipv6_regex}))? ([0-9]+)(?: ({path_regex}))?$".format(
            host_regex=constants.HOST_REGEX,
            ipv4_regex=constants.IPV4_REGEX,
            ipv6_regex=constants.IPV6_REGEX,
            path_regex=constants.PATH_REGEX,
        )
    )

    def __init__(self, server: str, ipv4: str, ipv6: str, port: int, path: str) -> None:
        """
        Init SecuredBMAEndpoint instance

        :param server: IP or domain name
        :param ipv4: IP as IPv4 format
        :param ipv6: IP as IPv6 format
        :param port: Port number
        :param path: Url path
        """
        super().__init__(server, ipv4, ipv6, port)
        self.path = path

    @classmethod
    def from_inline(
        cls: Type[SecuredBMAEndpointType], inline: str
    ) -> SecuredBMAEndpointType:
        """
        Return SecuredBMAEndpoint instance from endpoint string

        :param inline: Endpoint string
        :return:
        """
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

    def inline(self) -> str:
        """
        Return endpoint string

        :return:
        """
        inlined = [
            str(info)
            for info in (self.server, self.ipv4, self.ipv6, self.port, self.path)
            if info
        ]
        return SecuredBMAEndpoint.API + " " + " ".join(inlined)

    def conn_handler(
        self, session: ClientSession, proxy: str = None
    ) -> ConnectionHandler:
        """
        Return connection handler instance for the endpoint

        :param session: AIOHTTP client session instance
        :param proxy: Proxy url
        :return:
        """
        if self.server:
            conn_handler = ConnectionHandler(
                "https", "wss", self.server, self.port, self.path, session, proxy
            )
        elif self.ipv6:
            conn_handler = ConnectionHandler(
                "https",
                "wss",
                "[{0}]".format(self.ipv6),
                self.port,
                self.path,
                session,
                proxy,
            )
        else:
            conn_handler = ConnectionHandler(
                "https", "wss", self.ipv4, self.port, self.path, session, proxy
            )

        return conn_handler


# required to type hint cls in classmethod
WS2PEndpointType = TypeVar("WS2PEndpointType", bound="WS2PEndpoint")


class WS2PEndpoint(Endpoint):
    API = "WS2P"
    re_inline = re.compile(
        "^WS2P ({ws2pid_regex}) ((?:{host_regex})|(?:{ipv4_regex})|(?:{ipv6_regex})) ([0-9]+)?(?: ({path_regex}))?$".format(
            ws2pid_regex=constants.WS2PID_REGEX,
            host_regex=constants.HOST_REGEX,
            ipv4_regex=constants.IPV4_REGEX,
            ipv6_regex=constants.IPV6_REGEX,
            path_regex=constants.PATH_REGEX,
        )
    )

    def __init__(self, ws2pid: str, server: str, port: int, path: str) -> None:
        self.ws2pid = ws2pid
        self.server = server
        self.port = port
        self.path = path

    @classmethod
    def from_inline(cls: Type[WS2PEndpointType], inline: str) -> WS2PEndpointType:
        """
        Return WS2PEndpoint instance from endpoint string

        :param inline: Endpoint string
        :return:
        """
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

    def inline(self) -> str:
        """
        Return endpoint string

        :return:
        """
        inlined = [
            str(info)
            for info in (self.ws2pid, self.server, self.port, self.path)
            if info
        ]
        return WS2PEndpoint.API + " " + " ".join(inlined)

    def conn_handler(
        self, session: ClientSession, proxy: str = None
    ) -> ConnectionHandler:
        """
        Return connection handler instance for the endpoint

        :param session: AIOHTTP client session instance
        :param proxy: Proxy url
        :return:
        """
        http_scheme = "http"
        websocket_scheme = "ws"
        if self.port == 443:
            http_scheme += "s"
            websocket_scheme += "s"
        return ConnectionHandler(
            http_scheme,
            websocket_scheme,
            self.server,
            self.port,
            self.path,
            session,
            proxy,
        )

    def __str__(self) -> str:
        return self.inline()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, WS2PEndpoint):
            return NotImplemented
        return (
            self.server == other.server
            and self.ws2pid == other.ws2pid
            and self.port == other.port
            and self.path == other.path
        )

    def __hash__(self) -> int:
        return hash((self.ws2pid, self.server, self.port, self.path))


# required to type hint cls in classmethod
ESCoreEndpointType = TypeVar("ESCoreEndpointType", bound="ESCoreEndpoint")


class ESCoreEndpoint(Endpoint):
    API = "ES_CORE_API"
    re_inline = re.compile(
        "^ES_CORE_API ((?:{host_regex})|(?:{ipv4_regex})) ([0-9]+)$".format(
            host_regex=constants.HOST_REGEX, ipv4_regex=constants.IPV4_REGEX
        )
    )

    def __init__(self, server: str, port: int) -> None:
        self.server = server
        self.port = port

    @classmethod
    def from_inline(cls: Type[ESCoreEndpointType], inline: str) -> ESCoreEndpointType:
        """
        Return ESCoreEndpoint instance from endpoint string

        :param inline: Endpoint string
        :return:
        """
        m = ESCoreEndpoint.re_inline.match(inline)
        if m is None:
            raise MalformedDocumentError(ESCoreEndpoint.API)
        server = m.group(1)
        port = int(m.group(2))
        return cls(server, port)

    def inline(self) -> str:
        """
        Return endpoint string

        :return:
        """
        inlined = [str(info) for info in (self.server, self.port) if info]
        return ESCoreEndpoint.API + " " + " ".join(inlined)

    def conn_handler(
        self, session: ClientSession, proxy: str = None
    ) -> ConnectionHandler:
        """
        Return connection handler instance for the endpoint

        :param session: AIOHTTP client session instance
        :param proxy: Proxy url
        :return:
        """
        return ConnectionHandler(
            "https", "wss", self.server, self.port, "", session, proxy
        )

    def __str__(self) -> str:
        return self.inline()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ESCoreEndpoint):
            return NotImplemented
        return self.server == other.server and self.port == other.port

    def __hash__(self) -> int:
        return hash((self.server, self.port))


# required to type hint cls in classmethod
ESUserEndpointType = TypeVar("ESUserEndpointType", bound="ESUserEndpoint")


class ESUserEndpoint(Endpoint):
    API = "ES_USER_API"
    re_inline = re.compile(
        "^ES_USER_API ((?:{host_regex})|(?:{ipv4_regex})) ([0-9]+)$".format(
            host_regex=constants.HOST_REGEX, ipv4_regex=constants.IPV4_REGEX
        )
    )

    def __init__(self, server: str, port: int) -> None:
        self.server = server
        self.port = port

    @classmethod
    def from_inline(cls: Type[ESUserEndpointType], inline: str) -> ESUserEndpointType:
        """
        Return ESUserEndpoint instance from endpoint string

        :param inline: Endpoint string
        :return:
        """
        m = ESUserEndpoint.re_inline.match(inline)
        if m is None:
            raise MalformedDocumentError(ESUserEndpoint.API)
        server = m.group(1)
        port = int(m.group(2))
        return cls(server, port)

    def inline(self) -> str:
        """
        Return endpoint string

        :return:
        """
        inlined = [str(info) for info in (self.server, self.port) if info]
        return ESUserEndpoint.API + " " + " ".join(inlined)

    def conn_handler(
        self, session: ClientSession, proxy: str = None
    ) -> ConnectionHandler:
        """
        Return connection handler instance for the endpoint

        :param session: AIOHTTP client session instance
        :param proxy: Proxy url
        :return:
        """
        return ConnectionHandler(
            "https", "wss", self.server, self.port, "", session, proxy
        )

    def __str__(self) -> str:
        return self.inline()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ESUserEndpoint):
            return NotImplemented
        return self.server == other.server and self.port == other.port

    def __hash__(self) -> int:
        return hash((self.server, self.port))


# required to type hint cls in classmethod
ESSubscribtionEndpointType = TypeVar(
    "ESSubscribtionEndpointType", bound="ESSubscribtionEndpoint"
)


class ESSubscribtionEndpoint(Endpoint):
    API = "ES_SUBSCRIPTION_API"
    re_inline = re.compile(
        "^ES_SUBSCRIPTION_API ((?:{host_regex})|(?:{ipv4_regex})) ([0-9]+)$".format(
            host_regex=constants.HOST_REGEX, ipv4_regex=constants.IPV4_REGEX
        )
    )

    def __init__(self, server: str, port: int) -> None:
        self.server = server
        self.port = port

    @classmethod
    def from_inline(
        cls: Type[ESSubscribtionEndpointType], inline: str
    ) -> ESSubscribtionEndpointType:
        """
        Return ESSubscribtionEndpoint instance from endpoint string

        :param inline: Endpoint string
        :return:
        """
        m = ESSubscribtionEndpoint.re_inline.match(inline)
        if m is None:
            raise MalformedDocumentError(ESSubscribtionEndpoint.API)
        server = m.group(1)
        port = int(m.group(2))
        return cls(server, port)

    def inline(self) -> str:
        """
        Return endpoint string

        :return:
        """
        inlined = [str(info) for info in (self.server, self.port) if info]
        return ESSubscribtionEndpoint.API + " " + " ".join(inlined)

    def conn_handler(
        self, session: ClientSession, proxy: str = None
    ) -> ConnectionHandler:
        """
        Return connection handler instance for the endpoint

        :param session: AIOHTTP client session instance
        :param proxy: Proxy url
        :return:
        """
        return ConnectionHandler(
            "https", "wss", self.server, self.port, "", session, proxy
        )

    def __str__(self) -> str:
        return self.inline()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ESSubscribtionEndpoint):
            return NotImplemented
        return self.server == other.server and self.port == other.port

    def __hash__(self) -> int:
        return hash((ESSubscribtionEndpoint.API, self.server, self.port))


MANAGED_API = {
    BMAEndpoint.API: BMAEndpoint,
    SecuredBMAEndpoint.API: SecuredBMAEndpoint,
    WS2PEndpoint.API: WS2PEndpoint,
    ESCoreEndpoint.API: ESCoreEndpoint,
    ESUserEndpoint.API: ESUserEndpoint,
    ESSubscribtionEndpoint.API: ESSubscribtionEndpoint,
}  # type: Dict[str, Any]


def endpoint(value: Any) -> Any:
    """
    Convert an endpoint string to the corresponding Endpoint instance type

    :param value: Endpoint string or subclass
    :return:
    """
    result = UnknownEndpoint.from_inline(value)
    # if Endpoint instance...
    if issubclass(type(value), Endpoint):
        result = value
        # if str...
    elif isinstance(value, str):
        # find Endpoint instance
        for api, cls in MANAGED_API.items():
            if value.startswith(api + " "):
                result = cls.from_inline(value)
    else:
        raise TypeError("Cannot convert {0} to endpoint".format(value))

    return result
