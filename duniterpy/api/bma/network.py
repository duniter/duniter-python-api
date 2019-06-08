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

from aiohttp import ClientResponse

from duniterpy.api.client import Client, RESPONSE_AIOHTTP

logger = logging.getLogger("duniter/network")

MODULE = "network"

PEERING_SCHEMA = {
    "type": "object",
    "properties": {
        "version": {"type": ["number", "string"]},
        "currency": {"type": "string"},
        "pubkey": {"type": "string"},
        "endpoints": {"type": "array", "items": {"type": "string"}},
        "signature": {"type": "string"},
    },
    "required": ["version", "currency", "pubkey", "endpoints", "signature"],
}

PEERS_SCHEMA = schema = {
    "type": ["object"],
    "properties": {
        "depth": {"type": "number"},
        "nodesCount": {"type": "number"},
        "leavesCount": {"type": "number"},
        "root": {"type": "string"},
        "hash": {"type": "string"},
        "value": {
            "type": "object",
            "properties": {
                "version": {"type": "string"},
                "currency": {"type": "string"},
                "pubkey": {"type": "string"},
                "endpoints": {"type": "array", "items": {"type": "string"}},
                "signature": {"type": "string"},
            },
            "required": ["version", "currency", "pubkey", "endpoints", "signature"],
        },
    },
    "oneOf": [
        {"required": ["depth", "nodesCount", "leavesCount", "root"]},
        {"required": ["hash", "value"]},
    ],
}

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
                "required": ["messageV2", "sigV2", "step"],
            },
        }
    },
    "required": ["heads"],
}


async def peering(client: Client) -> dict:
    """
    GET peering information about a peer

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/peering", schema=PEERING_SCHEMA)


async def peers(client: Client, leaves: bool = False, leaf: str = "") -> dict:
    """
    GET peering entries of every node inside the currency network

    :param client: Client to connect to the api
    :param leaves: True if leaves should be requested
    :param leaf: True if leaf should be requested
    :return:
    """
    if leaves is True:
        response = await client.get(
            MODULE + "/peering/peers", {"leaves": "true"}, schema=PEERS_SCHEMA
        )
    else:
        response = await client.get(
            MODULE + "/peering/peers", {"leaf": leaf}, schema=PEERS_SCHEMA
        )
    return response


async def peer(client: Client, peer_signed_raw: str) -> ClientResponse:
    """
    POST a Peer signed raw document

    :param client: Client to connect to the api
    :param peer_signed_raw: Peer signed raw document
    :return:
    """
    return await client.post(
        MODULE + "/peering/peers", {"peer": peer_signed_raw}, rtype=RESPONSE_AIOHTTP
    )


async def ws2p_heads(client: Client) -> dict:
    """
    GET ws2p heads known by the node

    :param client: Client to connect to the api
    :rtype: dict
    """
    return await client.get(MODULE + "/ws2p/heads", schema=WS2P_HEADS_SCHEMA)
