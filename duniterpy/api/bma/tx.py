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

logger = logging.getLogger("duniter/tx")

MODULE = "tx"

HISTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "currency": {"type": "string"},
        "pubkey": {"type": "string"},
        "history": {
            "type": "object",
            "properties": {
                "sent": {"$ref": "#/definitions/transaction_data"},
                "received": {"$ref": "#/definitions/transaction_data"},
                "sending": {"$ref": "#/definitions/transactioning_data"},
                "receiving": {"$ref": "#/definitions/transactioning_data"},
                "pending": {"$ref": "#/definitions/transactioning_data"},
            },
            "required": ["sent", "received", "sending", "receiving", "pending"],
        },
    },
    "definitions": {
        "transaction_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "version": {"type": "number"},
                    "issuers": {"type": "array", "items": {"type": "string"}},
                    "inputs": {"type": "array", "items": {"type": "string"}},
                    "outputs": {"type": "array", "items": {"type": "string"}},
                    "unlocks": {"type": "array", "items": {"type": "string"}},
                    "comment": {"type": "string"},
                    "signatures": {"type": "array", "items": {"type": "string"}},
                    "hash": {"type": "string"},
                    "block_number": {"type": "number"},
                    "time": {"type": "number"},
                },
                "required": [
                    "version",
                    "issuers",
                    "inputs",
                    "outputs",
                    "comment",
                    "signatures",
                    "hash",
                    "block_number",
                    "time",
                ],
            },
        },
        "transactioning_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "version": {"type": "number"},
                    "issuers": {"type": "array", "items": {"type": "string"}},
                    "inputs": {"type": "array", "items": {"type": "string"}},
                    "outputs": {"type": "array", "items": {"type": "string"}},
                    "unlocks": {"type": "array", "items": {"type": "string"}},
                    "comment": {"type": "string"},
                    "signatures": {"type": "array", "items": {"type": "string"}},
                    "hash": {"type": "string"},
                },
                "required": [
                    "version",
                    "issuers",
                    "inputs",
                    "outputs",
                    "comment",
                    "signatures",
                    "hash",
                ],
            },
        },
    },
    "required": ["currency", "pubkey", "history"],
}

SOURCES_SCHEMA = {
    "type": "object",
    "properties": {
        "currency": {"type": "string"},
        "pubkey": {"type": "string"},
        "sources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "noffset": {"type": "number"},
                    "identifier": {"type": "string"},
                    "amount": {"type": "number"},
                    "base": {"type": "number"},
                },
                "required": ["type", "noffset", "identifier", "amount", "base"],
            },
        },
    },
    "required": ["currency", "pubkey", "sources"],
}


async def history(client: Client, pubkey: str) -> dict:
    """
    Get transactions history of public key

    :param client: Client to connect to the api
    :param pubkey: Public key
    :return:
    """
    return await client.get(MODULE + "/history/%s" % pubkey, schema=HISTORY_SCHEMA)


async def process(client: Client, transaction_signed_raw: str) -> ClientResponse:
    """
    POST a transaction raw document

    :param client: Client to connect to the api
    :param transaction_signed_raw: Transaction signed raw document
    :return:
    """
    return await client.post(
        MODULE + "/process",
        {"transaction": transaction_signed_raw},
        rtype=RESPONSE_AIOHTTP,
    )


async def sources(client: Client, pubkey: str) -> dict:
    """
    GET transaction sources

    :param client: Client to connect to the api
    :param pubkey: Public key
    :return:
    """
    return await client.get(MODULE + "/sources/%s" % pubkey, schema=SOURCES_SCHEMA)


async def pending(client: Client, pubkey: str) -> dict:
    """
    GET pending transaction history for the given pubkey

    :param client: Client to connect to the api
    :param pubkey: Public key
    :return:
    """
    return await client.get(
        MODULE + "/history/%s/pending" % pubkey, schema=HISTORY_SCHEMA
    )


async def blocks(client: Client, pubkey: str, start: int, end: int) -> dict:
    """
    GET public key transactions history between start and end block number

    :param client: Client to connect to the api
    :param pubkey: Public key
    :param start: Start from block number
    :param end: End to block number
    :return:
    """
    return await client.get(
        MODULE + "/history/%s/blocks/%s/%s" % (pubkey, start, end),
        schema=HISTORY_SCHEMA,
    )


async def times(client: Client, pubkey: str, start: int, end: int) -> dict:
    """
    GET public key transactions history between start and end timestamp

    :param client: Client to connect to the api
    :param pubkey: Public key
    :param start: Start from timestamp
    :param end: End to timestamp
    :return:
    """
    return await client.get(
        MODULE + "/history/%s/times/%s/%s" % (pubkey, start, end), schema=HISTORY_SCHEMA
    )
