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
from duniterpy.documents.peer import Peer

logger = logging.getLogger("duniter/network")

MODULE = 'network'

PEERING_SCHEMA = {
        "type": "object",
        "properties": {
          "version": {
              "type": ["number", "string"]
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

PEERS_SCHEMA = schema = {
        "type": ["object"],
        "properties": {
            "depth": {
                "type": "number"
            },
            "nodesCount": {
                "type": "number"
            },
            "leavesCount": {
                "type": "number"
            },
            "root": {
                "type": "string"
            },
            "hash": {
                "type": "string"
            },
            "value": {
                "type": "object",
                "properties": {
                    "version": {
                        "type": "string"
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
        },
        "oneOf": [
            {
                "required": ["depth", "nodesCount", "leavesCount", "root"]
            },
            {
                "required": ["hash", "value"]
            }
        ]
    }


async def peering(client: Client) -> dict:
    """
    GET peering information about a peer

    :param client: Client to connect to the api
    :rtype: dict
    """
    return await client.get(MODULE + '/peering', schema=PEERING_SCHEMA)


async def peers(client: Client, leaves: bool = False, leaf: str = ""):
    """
    GET peering entries of every node inside the currency network

    :param client: Client to connect to the api
    :param leaves: True if leaves should be requested
    :param leaf: True if leaf should be requested
    :rtype: dict
    """
    if leaves is True:
        return await client.get(MODULE + '/peering/peers', {"leaves": "true"}, schema=PEERS_SCHEMA)
    else:
        return await client.get(MODULE + '/peering/peers', {"leaf": leaf}, schema=PEERS_SCHEMA)


# async def peer(client: Client, entry: Peer = None, signature: str = None) -> dict:
#     """
#     POST a Peer document with his signature
#
#     :param client: Client to connect to the api
#     :param entry: Peer document
#     :param signature: Signature of the document issuer
#     :rtype: dict
#     """
#
#     client = API(connection, MODULE)
#     r = await client.requests_post('/peering/peers', entry=entry, signature=signature)
#     return r
