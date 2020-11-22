"""
Copyright  2014-2021 Vincent Texier <vit@free.fr>

DuniterPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DuniterPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
import logging
from typing import Callable, Union, Any, Optional, Dict
from urllib import request, parse

import jsonschema
from websocket import WebSocket
from aiohttp import ClientSession
from http.client import HTTPResponse

import duniterpy.api.endpoint as endpoint
from .errors import DuniterError

logger = logging.getLogger("duniter")

# Response type constants
RESPONSE_JSON = "json"
RESPONSE_TEXT = "text"
RESPONSE_AIOHTTP = "aiohttp"
RESPONSE_HTTP = "http"

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
    except (TypeError, json.decoder.JSONDecodeError) as e:
        raise jsonschema.ValidationError("Could not parse json") from e

    return data


def parse_error(text: str) -> dict:
    """
    Validate and parse the BMA answer from websocket

    :param text: the bma error
    :return: the json data
    """
    try:
        data = json.loads(text)
        jsonschema.validate(data, ERROR_SCHEMA)
    except (TypeError, json.decoder.JSONDecodeError) as e:
        raise jsonschema.ValidationError(
            "Could not parse json : {0}".format(str(e))
        ) from e

    return data


async def parse_response(response: str, schema: dict) -> Any:
    """
    Validate and parse the BMA answer

    :param response: Response of aiohttp request
    :param schema: The expected response structure
    :return: the json data
    """
    try:
        data = json.loads(response)
        if schema is not None:
            jsonschema.validate(data, schema)
        return data
    except (TypeError, json.decoder.JSONDecodeError) as exception:
        raise jsonschema.ValidationError(
            "Could not parse json : {0}".format(str(exception))
        ) from exception


class WSConnection:
    """
    Abstraction layer on websocket library
    """

    def __init__(self, connection: WebSocket) -> None:
        """
        Init WSConnection instance

        :param connection: Connection instance of the websocket library
        """
        self.connection = connection

    async def send_str(self, data: str) -> None:
        """
        Send a data string to the web socket connection

        :param data: Data string
        :return:
        """
        if self.connection is None:
            raise Exception("Connection property is empty")

        self.connection.send(data)
        return None

    async def receive_str(self, timeout: Optional[float] = None) -> str:
        """
        Wait for a data string from the web socket connection

        :param timeout: Timeout in seconds
        :return:
        """
        if self.connection is None:
            raise Exception("Connection property is empty")
        if timeout is not None:
            self.connection.settimeout(timeout)
        return self.connection.recv()

    async def receive_json(self, timeout: Optional[float] = None) -> Any:
        """
        Wait for json data from the web socket connection

        :param timeout: Timeout in seconds
        :return:
        """
        if self.connection is None:
            raise Exception("Connection property is empty")
        if timeout is not None:
            self.connection.settimeout(timeout)
        return json.loads(self.connection.recv())

    async def close(self) -> None:
        """
        Close the web socket connection

        :return:
        """
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
            url = "{scheme}://{server}:{port}".format(
                scheme=scheme, server=server, port=port
            )

        if len(path.strip()) > 0:
            return f"{url}/{path}"

        return url

    async def request_url(
        self,
        path: str,
        method: str = "GET",
        rtype: str = RESPONSE_JSON,
        schema: Optional[dict] = None,
        json_data: Optional[dict] = None,
        bma_errors: bool = False,
        **kwargs: Any,
    ) -> Any:
        """
        Requests wrapper in order to use API parameters.

        :param path: the request path
        :param method: Http method  'GET' or 'POST' (optional, default='GET')
        :param rtype: Response type (optional, default RESPONSE_JSON, can be RESPONSE_TEXT, RESPONSE_HTTP)
        :param schema: Json Schema to validate response (optional, default None)
        :param json_data: Json data as dict (optional, default None)
        :param bma_errors: Set it to True to handle Duniter Error Response (optional, default False)

        :return:
        """
        logging.debug(
            "Request : %s", self.reverse_url(self.connection_handler.http_scheme, path)
        )
        url = self.reverse_url(self.connection_handler.http_scheme, path)
        duniter_request = request.Request(url, method=method)

        if kwargs:
            # urlencoded http form content as bytes
            duniter_request.data = parse.urlencode(kwargs).encode("utf-8")
            logging.debug("%s : %s, data=%s", method, url, duniter_request.data)

        if json_data:
            # json content as bytes
            duniter_request.data = json.dumps(json_data).encode("utf-8")
            logging.debug("%s : %s, data=%s", method, url, duniter_request.data)

            # http header to send json body
            self.headers["Content-Type"] = "application/json"

        if self.headers:
            duniter_request.headers = self.headers

        if self.connection_handler.proxy:
            # proxy host
            duniter_request.set_proxy(
                self.connection_handler.proxy, self.connection_handler.http_scheme
            )

        response = request.urlopen(duniter_request, timeout=15)  # type: HTTPResponse

        if response.status != 200:
            content = response.read()
            if bma_errors:
                try:
                    error_data = parse_error(content)
                    raise DuniterError(error_data)
                except (TypeError, jsonschema.ValidationError) as exception:
                    raise ValueError(
                        "status code != 200 => %d (%s)" % (response.status, content)
                    ) from exception

            raise ValueError(
                "status code != 200 => %d (%s)" % (response.status, content)
            )

        # get response content
        content = response.read()
        response.close()

        # if schema supplied...
        if schema is not None:
            # validate response
            await parse_response(content, schema)

        # return the chosen type
        result = response  # type: Any
        if rtype == RESPONSE_TEXT:
            result = content
        elif rtype == RESPONSE_JSON:
            result = json.loads(content)

        return result

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

        ws = WebSocket()
        if self.connection_handler.proxy:
            proxy_split = ":".split(self.connection_handler.proxy)
            if len(proxy_split) == 2:
                host = proxy_split[0]
                port = proxy_split[1]
            else:
                host = self.connection_handler.proxy
                port = 80
            ws.connect(url, http_proxy_host=host, http_proxy_port=port)
        else:
            ws.connect(url)

        return WSConnection(ws)


class Client:
    """
    Main class to create an API client
    """

    def __init__(
        self,
        _endpoint: Union[str, endpoint.Endpoint],
        session: Optional[ClientSession] = None,
        proxy: Optional[str] = None,
    ) -> None:
        """
        Init Client instance

        :param _endpoint: Endpoint string in duniter format
        :param session: Aiohttp client session (optional, default None)
        :param proxy: Proxy server as hostname:port (optional, default None)
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
        params: Optional[dict] = None,
        rtype: str = RESPONSE_JSON,
        schema: Optional[dict] = None,
    ) -> Any:
        """
        GET request on endpoint host + url_path

        :param url_path: Url encoded path following the endpoint
        :param params: Url query string parameters dictionary (optional, default None)
        :param rtype: Response type (optional, default RESPONSE_JSON, can be RESPONSE_TEXT, RESPONSE_HTTP)
        :param schema: Json Schema to validate response (optional, default None)
        :return:
        """
        if params is None:
            params = dict()

        client = API(self.endpoint.conn_handler(self.session, self.proxy))

        # get response
        return await client.request_url(
            url_path, "GET", rtype, schema, bma_errors=True, **params
        )

    async def post(
        self,
        url_path: str,
        params: Optional[dict] = None,
        rtype: str = RESPONSE_JSON,
        schema: Optional[dict] = None,
    ) -> Any:
        """
        POST request on endpoint host + url_path

        :param url_path: Url encoded path following the endpoint
        :param params: Url query string parameters dictionary (optional, default None)
        :param rtype: Response type (optional, default RESPONSE_JSON, can be RESPONSE_TEXT, RESPONSE_HTTP)
        :param schema: Json Schema to validate response (optional, default None)
        :return:
        """
        if params is None:
            params = dict()

        client = API(self.endpoint.conn_handler(self.session, self.proxy))

        # get response
        return await client.request_url(
            url_path, "POST", rtype, schema, bma_errors=True, **params
        )

    async def query(
        self,
        query: str,
        variables: Optional[dict] = None,
        schema: Optional[dict] = None,
    ) -> Any:
        """
        GraphQL query or mutation request on endpoint

        :param query: GraphQL query string
        :param variables: Variables for the query (optional, default None)
        :param rtype: Response type (optional, default RESPONSE_JSON)
        :param schema: Json Schema to validate response (optional, default None)
        :return:
        """
        payload = {"query": query}  # type: Dict[str, Union[str, dict]]

        if variables is not None:
            payload["variables"] = variables

        client = API(self.endpoint.conn_handler(self.session, self.proxy))

        # get aiohttp response
        response = await client.request_url(
            "", "POST", rtype=RESPONSE_JSON, schema=schema, json_data=payload
        )

        # if schema supplied...
        if schema is not None:
            # validate response
            await parse_response(response, schema)

        return response

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
