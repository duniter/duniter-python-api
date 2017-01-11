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

from duniterpy.api.bma import API, logging, parse_response

logger = logging.getLogger("duniter/network")

URL_PATH = 'network'

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

async def peering(connection):
    """
    GET peering information about a peer

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    r = await client.requests_get('/peering')
    return await parse_response(r, PEERING_SCHEMA)

async def peers(connection, leaves=False, leaf=""):
    """
    GET peering entries of every node inside the currency network

    :param bool leaves: True if leaves should be requested
    :param str leaf: True if leaf should be requested
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    # GET Peers
    if leaves:
        r = await client.requests_get('/peering/peers', leaves=leaves)
    else:
        r = await client.requests_get('/peering/peers', leaf=leaf)

    return await parse_response(r, PEERS_SCHEMA)

async def peer(connection, entry=None, signature=None):
    """
    GET peering entries of every node inside the currency network

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param duniterpy.documents.peer.Peer entry: Peer document
    :param str signature: Signature of the document issuer
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    r = await client.requests_post('/peering/peers', entry=entry, signature=signature)
    return r

# async def status(connection):
#     """
# NOT DOCUMENTED IN BMA API DOCUMENTATION
#     POST a network status document to this node in order notify of its status
#
#     :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
#     :param duniterpy.documents.peer.Peer entry: Peer document
#     :param str signature: Signature of the document issuer
#     :rtype: dict
#     """
#
#     async def __post__(self, session, **kwargs):
#         assert 'status' in kwargs
#         assert 'signature' in kwargs
#
#         r = await self.requests_post(session, '/status', **kwargs)
#         return r
