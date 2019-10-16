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
# vit
import logging

from duniterpy.api.client import Client

logger = logging.getLogger("duniter/network")

MODULE = "network"

WS2P_HEADS_SCHEMA = {
    "type": "object",
    "properties": {
        "heads": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "sig": {"type": "string"},
                    "messageV2": {"type": "string"},
                    "sigV2": {"type": "string"},
                    "step": {"type": "number"},
                },
                "required": ["message", "sig"],
            },
        }
    },
    "required": ["heads"],
}


def heads(client: Client):
    """
    GET Certification data over a member

    :param client: Client to connect to the api
    :rtype: dict
    """
    return client.get(MODULE + "/ws2p/heads", schema=WS2P_HEADS_SCHEMA)


WS2P_CONNECT_MESSAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "auth": {"type": "string", "pattern": "^CONNECT$"},
        "challenge": {"type": "string"},
        "currency": {"type": "string"},
        "pub": {"type": "string"},
        "sig": {"type": "string"},
    },
    "required": ["auth", "challenge", "currency", "pub", "sig"],
}

WS2P_ACK_MESSAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "auth": {"type": "string", "pattern": "^ACK$"},
        "pub": {"type": "string"},
        "sig": {"type": "string"},
    },
    "required": ["auth", "pub", "sig"],
}

WS2P_OK_MESSAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "auth": {"type": "string", "pattern": "^OK$"},
        "sig": {"type": "string"},
    },
    "required": ["auth", "sig"],
}
