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
# vit
import logging

from duniterpy.api.bma.blockchain import BLOCK_SCHEMA
from duniterpy.api.client import Client, WSConnection

logger = logging.getLogger("duniter/ws")

MODULE = "ws"

WS_BLOCK_SCHEMA = BLOCK_SCHEMA

WS_PEER_SCHEMA = {
    "type": "object",
    "properties": {
        "version": {"type": "number"},
        "currency": {"type": "string"},
        "pubkey": {"type": "string"},
        "endpoints": {"type": "array", "items": {"type": "string"}},
        "signature": {"type": "string"},
    },
    "required": ["version", "currency", "pubkey", "endpoints", "signature"],
}


async def block(client: Client) -> WSConnection:
    """
    Connect to block websocket

    :param client: Client to connect to the api
    :return:
    """
    return await client.connect_ws(MODULE + "/block")


async def peer(client: Client) -> WSConnection:
    """
    Connect to peer websocket

    :param client: Client to connect to the api
    :return:
    """
    return await client.connect_ws(MODULE + "/peer")
