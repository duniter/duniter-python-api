# Authors:
# Caner Candan <caner@candan.fr>, http://caner.candan.fr
# Inso <insomniak.fr at gmail.com>
# vit
import json
import logging
from typing import Callable, Union, Any, Optional

import jsonschema
from aiohttp import ClientResponse, ClientSession, ClientWebSocketResponse
from aiohttp.client import _WSRequestContextManager
import duniterpy.api.endpoint as endpoint
from .errors import DuniterError

logger = logging.getLogger("duniter")

# Response type constants
RESPONSE_JSON = "json"
RESPONSE_TEXT = "text"
RESPONSE_AIOHTTP = "aiohttp"

# Connection type constants
CONNECTION_TYPE_AIOHTTP = 1

# jsonschema validator
ERROR_SCHEMA = {
    "type": "object",
    "properties": {"ucode": {"type": "number"}, "message": {"type": "string"}},
    "required": ["ucode", "message"],
}


def parse_text(text: str, schema: dict) -> Any:
    """
    Validate and parse the BMA answer from websocket

    :param text: the bma answer
    :param schema: dict for jsonschema
    :return: the json data
    """
    try:
        data = json.loads(text)
        jsonschema.validate(data, schema)
    except (TypeError, json.decoder.JSONDecodeError):
        raise jsonschema.ValidationError("Could not parse json")

    return data


def parse_error(text: str) -> Any:
    """
    Validate and parse the BMA answer from websocket

    :param text: the bma error
    :return: the json data
    """
    try:
        data = json.loads(text)
        jsonschema.validate(data, ERROR_SCHEMA)
    except (TypeError, json.decoder.JSONDecodeError) as e:
        raise jsonschema.ValidationError("Could not parse json : {0}".format(str(e)))

    return data


async def parse_response(response: ClientResponse, schema: dict) -> Any:
    """
    Validate and parse the BMA answer

    :param response: Response of aiohttp request
    :param schema: The expected response structure
    :return: the json data
    """
    try:
        data = await response.json()
        response.close()
        if schema is not None:
            jsonschema.validate(data, schema)
        return data
    except (TypeError, json.decoder.JSONDecodeError) as e:
        raise jsonschema.ValidationError("Could not parse json : {0}".format(str(e)))


class WSConnection:
    """
    From the documentation of the aiohttp_library, the web socket connection

      await ws_connection = session.ws_connect()

    should return a ClientWebSocketResponse object...

    https://docs.aiohttp.org/en/stable/client_quickstart.html#websockets

    In fact, aiohttp.session.ws_connect() returns a aiohttp.client._WSRequestContextManager instance.
    It must be used in a with statement to get the ClientWebSocketResponse instance from it (__aenter__).
    At the end of the with statement, aiohttp.client._WSRequestContextManager.__aexit__ is called
    and close the ClientWebSocketResponse in it.

      await with ws_connection as ws:
          await ws.receive_str()
    """

    def __init__(self, connection: _WSRequestContextManager) -> None:
        """
        Init WSConnection instance

        :param connection: Connection instance of the connection library
        """
        if not isinstance(connection, _WSRequestContextManager):
            raise Exception(
                BaseException(
                    "Only  aiohttp.client._WSRequestContextManager class supported"
                )
            )

        self.connection_type = CONNECTION_TYPE_AIOHTTP
        self._connection = connection  # type: _WSRequestContextManager
        self.connection = None  # type: Optional[ClientWebSocketResponse]

    async def send_str(self, data: str) -> None:
        """
        Send a data string to the web socket connection

        :param data: Data string
        :return:
        """
        if self.connection is None:
            raise Exception("Connection property is empty")

        await self.connection.send_str(data)
        return None

    async def receive_str(self, timeout: Optional[float] = None) -> str:
        """
        Wait for a data string from the web socket connection

        :param timeout: Timeout in seconds
        :return:
        """
        if self.connection is None:
            raise Exception("Connection property is empty")

        return await self.connection.receive_str(timeout=timeout)

    async def receive_json(self, timeout: Optional[float] = None) -> Any:
        """
        Wait for json data from the web socket connection

        :param timeout: Timeout in seconds
        :return:
        """
        if self.connection is None:
            raise Exception("Connection property is empty")

        return await self.connection.receive_json(timeout=timeout)

    async def init_connection(self):
        """
        Mandatory for aiohttp library in order to avoid the usage of the 'with' statement
        :return:
        """
        self.connection = await self._connection.__aenter__()

    async def close(self) -> None:
        """
        Close the web socket connection

        :return:
        """
        await self._connection.__aexit__(None, None, None)

        if self.connection is None:
            raise Exception("Connection property is empty")

        await self.connection.close()


class API:
    """
    API is a class used as an abstraction layer over the request library (AIOHTTP).
    """

    def __init__(
        self,
        connection_handler: endpoint.ConnectionHandler,
        headers: Optional[dict] = None,
    ) -> None:
        """
        Asks a module in order to create the url used then by derivated classes.

        :param connection_handler: Connection handler
        :param headers: Headers dictionary (optional, default None)
        """
        self.connection_handler = connection_handler
        self.headers = {} if headers is None else headers

    def reverse_url(self, scheme: str, path: str) -> str:
        """
        Reverses the url using scheme and path given in parameter.

        :param scheme: Scheme of the url
        :param path: Path of the url
        :return:
        """
        # remove starting slash in path if present
        path = path.lstrip("/")

        server, port = self.connection_handler.server, self.connection_handler.port
        if self.connection_handler.path:
            url = "{scheme}://{server}:{port}/{api_path}".format(
                scheme=scheme,
                server=server,
                port=port,
                api_path=self.connection_handler.path,
            )
        else:
            url = "{scheme}://{server}:{port}/".format(
                scheme=scheme, server=server, port=port
            )

        return url + path

    async def requests_get(self, path: str, **kwargs) -> ClientResponse:
        """
        Requests GET wrapper in order to use API parameters.

        :param path: the request path
        :return:
        """
        logging.debug(
            "Request : %s", self.reverse_url(self.connection_handler.http_scheme, path)
        )
        url = self.reverse_url(self.connection_handler.http_scheme, path)
        response = await self.connection_handler.session.get(
            url,
            params=kwargs,
            headers=self.headers,
            proxy=self.connection_handler.proxy,
            timeout=15,
        )
        if response.status != 200:
            try:
                error_data = parse_error(await response.text())
                raise DuniterError(error_data)
            except (TypeError, jsonschema.ValidationError):
                raise ValueError(
                    "status code != 200 => %d (%s)"
                    % (response.status, (await response.text()))
                )

        return response

    async def requests_post(self, path: str, **kwargs) -> ClientResponse:
        """
        Requests POST wrapper in order to use API parameters.

        :param path: the request path
        :return:
        """
        if "self_" in kwargs:
            kwargs["self"] = kwargs.pop("self_")

        logging.debug("POST : %s", kwargs)
        response = await self.connection_handler.session.post(
            self.reverse_url(self.connection_handler.http_scheme, path),
            data=kwargs,
            headers=self.headers,
            proxy=self.connection_handler.proxy,
            timeout=15,
        )
        return response

    async def connect_ws(self, path: str) -> WSConnection:
        """
        Connect to a websocket in order to use API parameters

        In reality, aiohttp.session.ws_connect returns a aiohttp.client._WSRequestContextManager instance.
        It must be used in a with statement to get the ClientWebSocketResponse instance from it (__aenter__).
        At the end of the with statement, aiohttp.client._WSRequestContextManager.__aexit__ is called
        and close the ClientWebSocketResponse in it.

        :param path: the url path
        :return:
        """
        url = self.reverse_url(self.connection_handler.ws_scheme, path)

        connection = WSConnection(
            self.connection_handler.session.ws_connect(
                url, proxy=self.connection_handler.proxy, autoclose=False
            )
        )

        # init aiohttp connection
        await connection.init_connection()

        return connection


class Client:
    """
    Main class to create an API client
    """

    def __init__(
        self,
        _endpoint: Union[str, endpoint.Endpoint],
        session: ClientSession = None,
        proxy: str = None,
    ) -> None:
        """
        Init Client instance

        :param _endpoint: Endpoint string in duniter format
        :param session: Aiohttp client session (optional, default None)
        :param proxy: Proxy server as hostname:port
        """
        if isinstance(_endpoint, str):
            # Endpoint Protocol detection
            self.endpoint = endpoint.endpoint(_endpoint)
        else:
            self.endpoint = _endpoint

        if isinstance(self.endpoint, endpoint.UnknownEndpoint):
            raise NotImplementedError(
                "{0} endpoint in not supported".format(self.endpoint.api)
            )

        # if no user session...
        if session is None:
            # open a session
            self.session = ClientSession()
        else:
            self.session = session
        self.proxy = proxy

    async def get(
        self,
        url_path: str,
        params: dict = None,
        rtype: str = RESPONSE_JSON,
        schema: dict = None,
    ) -> Any:
        """
        GET request on self.endpoint + url_path

        :param url_path: Url encoded path following the endpoint
        :param params: Url query string parameters dictionary
        :param rtype: Response type
        :param schema: Json Schema to validate response (optional, default None)
        :return:
        """
        if params is None:
            params = dict()

        client = API(self.endpoint.conn_handler(self.session, self.proxy))

        # get aiohttp response
        response = await client.requests_get(url_path, **params)

        # if schema supplied...
        if schema is not None:
            # validate response
            await parse_response(response, schema)

        # return the chosen type
        result = response  # type: Any
        if rtype == RESPONSE_TEXT:
            result = await response.text()
        elif rtype == RESPONSE_JSON:
            result = await response.json()

        return result

    async def post(
        self,
        url_path: str,
        params: dict = None,
        rtype: str = RESPONSE_JSON,
        schema: dict = None,
    ) -> Any:
        """
        POST request on self.endpoint + url_path

        :param url_path: Url encoded path following the endpoint
        :param params: Url query string parameters dictionary
        :param rtype: Response type
        :param schema: Json Schema to validate response (optional, default None)
        :return:
        """
        if params is None:
            params = dict()

        client = API(self.endpoint.conn_handler(self.session, self.proxy))

        # get aiohttp response
        response = await client.requests_post(url_path, **params)

        # if schema supplied...
        if schema is not None:
            # validate response
            await parse_response(response, schema)

        # return the chosen type
        result = response  # type: Any
        if rtype == RESPONSE_TEXT:
            result = await response.text()
        elif rtype == RESPONSE_JSON:
            result = await response.json()

        return result

    async def connect_ws(self, path: str = "") -> WSConnection:
        """
        Connect to a websocket in order to use API parameters

        :param path: the url path
        :return:
        """
        client = API(self.endpoint.conn_handler(self.session, self.proxy))
        return await client.connect_ws(path)

    async def close(self):
        """
        Close aiohttp session

        :return:
        """
        await self.session.close()

    def __call__(self, _function: Callable, *args: Any, **kwargs: Any) -> Any:
        """
        Call the _function given with the args given
        So we can call many packages wrapping the REST API

        :param _function: The function to call
        :param args: The parameters
        :param kwargs: The key/value parameters
        :return:
        """
        return _function(self, *args, **kwargs)
