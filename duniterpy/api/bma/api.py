#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
# Caner Candan <caner@candan.fr>, http://caner.candan.fr
# Inso <insomniak.fr at gmail.com>


import aiohttp
import json
import logging
import jsonschema
from ..errors import DuniterError

logger = logging.getLogger("duniter")

ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "ucode": {
            "type": "number"
        },
        "message": {
            "type": "string"
        }
    },
    "required": ["ucode", "message"]
}


class ConnectionHandler(object):
    """Helper class used by other API classes to ease passing server connection information."""

    def __init__(self, http_scheme, ws_scheme, server, port, path="", proxy=None, session=None):
        """
        Init instance of connection handler

        :param str server: Server IP or domaine name
        :param int port: Port
        :param aiohttp.ClientSession|None session: Session AIOHTTP
        """
        self.http_scheme = http_scheme
        self.ws_scheme = ws_scheme
        self.server = server
        self.proxy = proxy
        self.port = port
        self.session = session
        self.path = path

    def __str__(self):
        return 'connection info: %s:%d' % (self.server, self.port)


def parse_text(text, schema):
    """
    Validate and parse the BMA answer from websocket

    :param str text: the bma answer
    :return: the json data
    """
    try:
        data = json.loads(text)
        jsonschema.validate(data, schema)
        return data
    except (TypeError, json.decoder.JSONDecodeError):
        raise jsonschema.ValidationError("Could not parse json")


def parse_error(text):
    """
    Validate and parse the BMA answer from websocket

    :param str text: the bma error
    :return: the json data
    """
    try:
        data = json.loads(text)
        jsonschema.validate(data, ERROR_SCHEMA)
        return data
    except (TypeError, json.decoder.JSONDecodeError) as e:
        raise jsonschema.ValidationError("Could not parse json : {0}".format(str(e)))


async def parse_response(response, schema):
    """
    Validate and parse the BMA answer

    :param aiohttp.ClientResponse response: Response of aiohttp request
    :param dict schema: The expected response structure
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


class API(object):
    """APIRequest is a class used as an interface. The intermediate derivated classes are the modules and the leaf classes are the API requests."""

    schema = {}

    def __init__(self, connection_handler, module):
        """
        Asks a module in order to create the url used then by derivated classes.

        :param ConnectionHandler connection_handler: Connection handler
        :param str module: Module path
        """
        self.module = module
        self.connection_handler = connection_handler
        self.headers = {}

    def reverse_url(self, scheme, path):
        """
        Reverses the url using scheme and path given in parameter.

        :param str scheme: Scheme of the url
        :param str path: Path of the url
        :return: str
        """

        server, port = self.connection_handler.server, self.connection_handler.port
        if self.connection_handler.path:
            url = '{scheme}://{server}:{port}/{path}/{module}'.format(scheme=scheme,
                                                                  server=server,
                                                                  port=port,
                                                                  path=path,
                                                                  module=self.module)
        else:
            url = '{scheme}://{server}:{port}/{module}'.format(scheme=scheme,
                                                                  server=server,
                                                                  port=port,
                                                                  module=self.module)

        return url + path

    async def requests_get(self, path, **kwargs):
        """
        Requests GET wrapper in order to use API parameters.

        :param str path: the request path
        :rtype: aiohttp.ClientResponse
        """
        logging.debug("Request : {0}".format(self.reverse_url(self.connection_handler.http_scheme, path)))
        with aiohttp.Timeout(15):
            url = self.reverse_url(self.connection_handler.http_scheme, path)
            response = await self.connection_handler.session.get(url, params=kwargs, headers=self.headers,
                                                                 proxy=self.connection_handler.proxy)
            if response.status != 200:
                try:
                    error_data = parse_error(await response.text())
                    raise DuniterError(error_data)
                except (TypeError, jsonschema.ValidationError):
                    raise ValueError('status code != 200 => %d (%s)' % (response.status, (await response.text())))

            return response

    async def requests_post(self, path, **kwargs):
        """
        Requests POST wrapper in order to use API parameters.

        :param str path: the request path
        :rtype: aiohttp.ClientResponse
        """
        if 'self_' in kwargs:
            kwargs['self'] = kwargs.pop('self_')

        logging.debug("POST : {0}".format(kwargs))
        with aiohttp.Timeout(15):
            response = await self.connection_handler.session.post(
                self.reverse_url(self.connection_handler.http_scheme, path),
                data=kwargs,
                headers=self.headers,
                proxy=self.connection_handler.proxy
            )
            return response

    def connect_ws(self, path):
        """
        Connect to a websocket in order to use API parameters

        :param str path: the url path
        :rtype: aiohttp.ClientWebSocketResponse
        """
        url = self.reverse_url(self.connection_handler.ws_scheme, path)
        return self.connection_handler.session.ws_connect(url, proxy=self.connection_handler.proxy)
