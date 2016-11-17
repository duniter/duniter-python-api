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

from duniterpy.api.bma import API, logging
from duniterpy.api.bma.blockchain import BLOCK_SCHEMA

logger = logging.getLogger("duniter/ws")

URL_PATH = 'ws'


WS_BLOCk_SCHEMA = BLOCK_SCHEMA
WS_PEER_SCHEMA = {
    "type": "object",
    "properties": {
        "version": {
            "type": "number"
        },
        "currency": {
            "type": "string"
        },
        "pubkey": {
            "type": "string"
        },
        "endpoints": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "signature": {
            "type": "string"
        }
    },
    "required": ["version", "currency", "pubkey", "endpoints", "signature"]
}


def block(connection):
    """
    Connect to block websocket

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: aiohttp.ClientWebSocketResponse
    """
    client = API(connection, URL_PATH)
    return client.connect_ws('/block')


def peer(connection):
    """
    Connect to peer websocket

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: aiohttp.ClientWebSocketResponse
    """
    client = API(connection, URL_PATH)
    return client.connect_ws('/peer')
