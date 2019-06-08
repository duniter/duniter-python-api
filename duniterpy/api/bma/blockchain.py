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
from typing import Union

from aiohttp import ClientResponse

from duniterpy.api.client import Client, RESPONSE_AIOHTTP

logger = logging.getLogger("duniter/blockchain")

MODULE = "blockchain"

BLOCK_SCHEMA = {
    "type": "object",
    "properties": {
        "version": {"type": "number"},
        "currency": {"type": "string"},
        "nonce": {"type": "number"},
        "number": {"type": "number"},
        "time": {"type": "number"},
        "medianTime": {"type": "number"},
        "dividend": {"type": ["number", "null"]},
        "monetaryMass": {"type": ["number", "null"]},
        "issuer": {"type": "string"},
        "previousHash": {"type": ["string", "null"]},
        "previousIssuer": {"type": ["string", "null"]},
        "membersCount": {"type": "number"},
        "hash": {"type": "string"},
        "inner_hash": {"type": "string"},
        "identities": {"type": "array", "items": {"type": "string"}},
        "joiners": {"type": "array", "items": {"type": "string"}},
        "leavers": {"type": "array", "items": {"type": "string"}},
        "revoked": {"type": "array", "items": {"type": "string"}},
        "excluded": {"type": "array", "items": {"type": "string"}},
        "certifications": {"type": "array", "items": {"type": "string"}},
        "transactions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "signatures": {"type": "array"},
                    "version": {"type": "number"},
                    "currency": {"type": "string"},
                    "issuers": {"type": "array", "items": {"type": "string"}},
                    "inputs": {"type": "array", "items": {"type": "string"}},
                    "unlocks": {"type": "array", "items": {"type": "string"}},
                    "outputs": {"type": "array", "item": {"type": "string"}},
                },
                "required": [
                    "signatures",
                    "version",
                    "currency",
                    "issuers",
                    "inputs",
                    "outputs",
                ],
            },
        },
        "signature": {"type": "string"},
    },
    "required": [
        "version",
        "currency",
        "nonce",
        "number",
        "time",
        "medianTime",
        "dividend",
        "monetaryMass",
        "issuer",
        "previousHash",
        "previousIssuer",
        "membersCount",
        "hash",
        "inner_hash",
        "identities",
        "joiners",
        "leavers",
        "excluded",
        "certifications",
        "transactions",
        "signature",
    ],
}

BLOCK_NUMBERS_SCHEMA = {
    "type": "object",
    "properties": {
        "result": {
            "type": "object",
            "properties": {"blocks": {"type": "array", "items": {"type": "number"}}},
            "required": ["blocks"],
        }
    },
    "required": ["result"],
}

PARAMETERS_SCHEMA = {
    "type": "object",
    "properties": {
        "currency": {"type": "string"},
        "c": {"type": "number"},
        "dt": {"type": "number"},
        "ud0": {"type": "number"},
        "sigPeriod": {"type": "number"},
        "sigStock": {"type": "number"},
        "sigWindow": {"type": "number"},
        "sigValidity": {"type": "number"},
        "sigQty": {"type": "number"},
        "sigReplay": {"type": "number"},
        "xpercent": {"type": "number"},
        "msValidity": {"type": "number"},
        "msPeriod": {"type": "number"},
        "stepMax": {"type": "number"},
        "medianTimeBlocks": {"type": "number"},
        "avgGenTime": {"type": "number"},
        "dtDiffEval": {"type": "number"},
        "percentRot": {"type": "number"},
        "udTime0": {"type": "number"},
        "udReevalTime0": {"type": "number"},
        "dtReeval": {"type": "number"},
    },
    "required": [
        "currency",
        "c",
        "dt",
        "ud0",
        "sigPeriod",
        "sigValidity",
        "sigQty",
        "xpercent",
        "sigStock",
        "sigWindow",
        "msValidity",
        "stepMax",
        "medianTimeBlocks",
        "avgGenTime",
        "dtDiffEval",
        "percentRot",
        "udTime0",
        "udReevalTime0",
        "dtReeval",
    ],
}

MEMBERSHIPS_SCHEMA = {
    "type": "object",
    "properties": {
        "pubkey": {"type": "string"},
        "uid": {"type": "string"},
        "sigDate": {"type": "string"},
        "memberships": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "version": {"type": "number"},
                    "currency": {"type": "string"},
                    "membership": {"type": "string"},
                    "blockNumber": {"type": "number"},
                    "written": {"type": ["number", "null"]},
                },
                "required": [
                    "version",
                    "currency",
                    "membership",
                    "blockNumber",
                    "blockHash",
                    "written",
                ],
            },
        },
    },
    "required": ["pubkey", "uid", "sigDate", "memberships"],
}

BLOCKS_SCHEMA = {"type": "array", "items": BLOCK_SCHEMA}

HARDSHIP_SCHEMA = {
    "type": "object",
    "properties": {"block": {"type": "number"}, "level": {"type": "number"}},
    "required": ["block", "level"],
}

DIFFICULTIES_SCHEMA = {
    "type": "object",
    "properties": {
        "block": {"type": "number"},
        "levels": {
            "type": "array",
            "items": [
                {
                    "type": "object",
                    "properties": {
                        "uid": {"type": "string"},
                        "level": {"type": "number"},
                    },
                    "required": ["uid", "level"],
                }
            ],
        },
    },
    "required": ["block", "levels"],
}

BRANCHES_SCHEMA = {"type": "object", "properties": {"blocks": BLOCKS_SCHEMA}}


async def parameters(client: Client) -> dict:
    """
    GET the blockchain parameters used by this node

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/parameters", schema=PARAMETERS_SCHEMA)


async def memberships(client: Client, search: str) -> dict:
    """
    GET list of Membership documents for UID/Public key

    :param client: Client to connect to the api
    :param search: UID/Public key
    :return:
    """
    return await client.get(
        MODULE + "/memberships/%s" % search, schema=MEMBERSHIPS_SCHEMA
    )


async def membership(client: Client, membership_signed_raw: str) -> ClientResponse:
    """
    POST a Membership document

    :param client: Client to connect to the api
    :param membership_signed_raw: Membership signed raw document
    :return:
    """
    return await client.post(
        MODULE + "/membership",
        {"membership": membership_signed_raw},
        rtype=RESPONSE_AIOHTTP,
    )


async def current(client: Client) -> dict:
    """
    GET the last accepted block

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/current", schema=BLOCK_SCHEMA)


async def block(
    client: Client, number: int = 0, block_raw: str = None, signature: str = None
) -> Union[dict, ClientResponse]:
    """
    GET/POST a block from/to the blockchain

    :param client: Client to connect to the api
    :param number: Block number to get
    :param block_raw: Block document to post
    :param signature: Signature of the block document issuer
    :return:
    """
    # POST block
    if block_raw is not None and signature is not None:
        return await client.post(
            MODULE + "/block",
            {"block": block_raw, "signature": signature},
            rtype=RESPONSE_AIOHTTP,
        )
    # GET block
    return await client.get(MODULE + "/block/%d" % number, schema=BLOCK_SCHEMA)


async def blocks(client: Client, count: int, start: int) -> list:
    """
    GET list of blocks from the blockchain

    :param client: Client to connect to the api
    :param count: Number of blocks
    :param start: First block number
    :return:
    """
    assert type(count) is int
    assert type(start) is int

    return await client.get(
        MODULE + "/blocks/%d/%d" % (count, start), schema=BLOCKS_SCHEMA
    )


async def hardship(client: Client, pubkey: str) -> dict:
    """
    GET hardship level for given member's public key for writing next block

    :param client: Client to connect to the api
    :param pubkey:  Public key of the member
    :return:
    """
    return await client.get(MODULE + "/hardship/%s" % pubkey, schema=HARDSHIP_SCHEMA)


async def difficulties(client: Client) -> dict:
    """
    GET difficulties levels for members into current window for writing next block

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/difficulties", schema=DIFFICULTIES_SCHEMA)


async def branches(client: Client) -> list:
    """
    GET current branches of the node (top block of each branch)

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/branches", schema=BRANCHES_SCHEMA)


async def newcomers(client: Client) -> dict:
    """
    GET the block numbers containing newcomers

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/with/newcomers", schema=BLOCK_NUMBERS_SCHEMA)


async def certifications(client: Client) -> dict:
    """
    GET the block numbers containing certifications

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/with/certs", schema=BLOCK_NUMBERS_SCHEMA)


async def joiners(client: Client) -> dict:
    """
    GET the block numbers containing joiners

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/with/joiners", schema=BLOCK_NUMBERS_SCHEMA)


async def actives(client: Client) -> dict:
    """
    GET the block numbers containing actives

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/with/actives", schema=BLOCK_NUMBERS_SCHEMA)


async def leavers(client: Client) -> dict:
    """
    GET the block numbers containing leavers

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/with/leavers", schema=BLOCK_NUMBERS_SCHEMA)


async def revoked(client: Client) -> dict:
    """
    GET the block numbers containing revoked members.

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/with/excluded", schema=BLOCK_NUMBERS_SCHEMA)


async def excluded(client: Client) -> dict:
    """
    GET the block numbers containing excluded

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/with/excluded", schema=BLOCK_NUMBERS_SCHEMA)


async def ud(client: Client) -> dict:
    """
    GET the block numbers containing universal dividend

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/with/ud", schema=BLOCK_NUMBERS_SCHEMA)


async def tx(client: Client) -> dict:
    """
    GET the block numbers containing transactions

    :param client: Client to connect to the api
    :return:
    """
    return await client.get(MODULE + "/with/tx", schema=BLOCK_NUMBERS_SCHEMA)
