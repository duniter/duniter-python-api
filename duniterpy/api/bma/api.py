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


import aiohttp, json, logging, jsonschema
import warnings
from ..errors import DuniterError

logger = logging.getLogger("duniter")


class ConnectionHandler(object):
    """Helper class used by other API classes to ease passing server connection information."""

    def __init__(self, server, port, session=None):
        """
        Init instance of connection handler

        :param str server: Server IP or domaine name
        :param int port: Port
        :param aiohttp.ClientSession|None session: Session AIOHTTP
        """
        self.server = server
        self.port = port
        if session is None:
            self.session = aiohttp.ClientSession()
        else:
            self.session = session

    def __str__(self):
        return 'connection info: %s:%d' % (self.server, self.port)


class API(object):
    """APIRequest is a class used as an interface. The intermediate derivated classes are the modules and the leaf classes are the API requests."""

    schema = {}
    error_schema = {
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

        url = '{scheme}://{server}:{port}/{module}'.format(scheme=scheme,
                                                           server=server,
                                                           port=port,
                                                           module=self.module)
        return url + path

    def parse_text(self, text):
        """
        Validate and parse the BMA answer from websocket

        :param str text: the bma answer
        :return: the json data
        """
        try:
            data = json.loads(text)
            jsonschema.validate(data, self.schema)
            return data
        except (TypeError, json.decoder.JSONDecodeError):
            raise jsonschema.ValidationError("Could not parse json")

    def parse_error(self, text):
        """
        Validate and parse the BMA answer from websocket

        :param str text: the bma error
        :return: the json data
        """
        try:
            data = json.loads(text)
            jsonschema.validate(data, self.error_schema)
            return data
        except (TypeError, json.decoder.JSONDecodeError):
            raise jsonschema.ValidationError("Could not parse json")

    async def parse_response(self, response, schema=None):
        """
        Validate and parse the BMA answer

        :param aiohttp.ClientResponse response: Response of aiohttp request
        :param dict schema: The expected response structure
        :return: the json data
        """
        try:
            data = await response.json()
            if schema is not None:
                jsonschema.validate(data, schema)
            return data
        except (TypeError, json.decoder.JSONDecodeError):
            raise jsonschema.ValidationError("Could not parse json")

    async def requests_get(self, path, **kwargs):
        """
        Requests GET wrapper in order to use API parameters.

        :params str path: the request path
        """
        logging.debug("Request : {0}".format(self.reverse_url("http", path)))
        with aiohttp.Timeout(15):
            response = await self.connection_handler.session.get(self.reverse_url("http", path), params=kwargs,headers=self.headers)
            if response.status != 200:
                try:
                    error_data = self.parse_error(await response.text())
                    raise DuniterError(error_data)
                except TypeError:
                    raise ValueError('status code != 200 => %d (%s)' % (response.status, (await response.text())))

            return response

    async def requests_post(self, path, **kwargs):
        """
        Requests POST wrapper in order to use API parameters.

        :param str path: the request path
        """
        if 'self_' in kwargs:
            kwargs['self'] = kwargs.pop('self_')

        logging.debug("POST : {0}".format(kwargs))
        with aiohttp.Timeout(15):
            response = await self.connection_handler.session.post(
                self.reverse_url("http", path),
                data=kwargs,
                headers=self.headers
            )
            return response

    def connect_ws(self, session, path):
        """
        Connect to a websocket in order to use API parameters

        :param aiohttp.ClientSession session: the session of the connection
        :param str path: the url path
        :return:
        """
        url = self.reverse_url("ws", path)
        return session.ws_connect(url)
