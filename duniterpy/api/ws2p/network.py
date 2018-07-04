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
#

from duniterpy.api.client import API, logging, parse_response

logger = logging.getLogger("duniter/network")

URL_PATH = 'network'

WS2P_HEADS_SCHEMA = {
                    "type": "object",
                    "properties": {
                        "heads": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string"
                                    },
                                    "sig": {
                                        "type": "string",
                                    },
                                    "messageV2": {
                                        "type": "string"
                                    },
                                    "sigV2": {
                                        "type": "string",
                                    },
                                    "step": {
                                        "type": "number",
                                    },
                                },
                                "required": ["message", "sig"]
                            }
                        }
                    },
                    "required": ["heads"]
                }


async def heads(connection):
    """
    GET Certification data over a member

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)

    r = await client.requests_get('/ws2p/heads')
    return await parse_response(r, WS2P_HEADS_SCHEMA)
