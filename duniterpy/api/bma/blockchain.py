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

logger = logging.getLogger("duniter/blockchain")

URL_PATH = 'blockchain'

BLOCK_SCHEMA = {
    "type": "object",
    "properties": {
        "version": {
            "type": "number"
        },
        "currency": {
            "type": "string"
        },
        "nonce": {
            "type": "number"
        },
        "number": {
            "type": "number"
        },
        "time": {
            "type": "number"
        },
        "medianTime": {
            "type": "number"
        },
        "dividend": {
            "type": ["number", "null"]
        },
        "monetaryMass": {
            "type": ["number", "null"]
        },
        "issuer": {
            "type": "string"
        },
        "previousHash": {
            "type": ["string", "null"]
        },
        "previousIssuer": {
            "type": ["string", "null"]
        },
        "membersCount": {
            "type": "number"
        },
        "hash": {
            "type": "string"
        },
        "inner_hash": {
            "type": "string"
        },
        "identities": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "joiners": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "leavers": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "revoked": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "excluded": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "certifications": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "transactions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "signatures": {
                        "type": "array"
                    },
                    "version": {
                        "type": "number"
                    },
                    "currency": {
                        "type": "string"
                    },
                    "issuers": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "inputs": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "unlocks": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "outputs": {
                        "type": "array",
                        "item": {
                            "type": "string"
                        }
                    }
                },
                "required": ["signatures", "version", "currency", "issuers", "inputs", "outputs"]
            }
        },
        "signature": {
            "type": "string"
        },
    },
    "required": ["version", "currency", "nonce", "number", "time", "medianTime", "dividend", "monetaryMass",
                 "issuer", "previousHash", "previousIssuer", "membersCount", "hash", "inner_hash", "identities",
                 "joiners", "leavers", "excluded", "certifications", "transactions", "signature"]
}

BLOCK_NUMBERS_SCHEMA = {
    "type": "object",
    "properties": {
        "result": {
            "type": "object",
            "properties": {
                "blocks": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    }
                },
            },
            "required": ["blocks"]
        }
    },
    "required": ["result"]
}

PARAMETERS_SCHEMA = {
        "type": "object",
        "properties":
        {
              "currency": {
                  "type": "string"
              },
              "c": {
                  "type": "number"
              },
              "dt": {
                  "type": "number"
              },
              "ud0": {
                  "type": "number"
              },
              "sigPeriod": {
                  "type": "number"
              },
              "sigStock": {
                  "type": "number"
              },
              "sigWindow": {
                  "type": "number"
              },
              "sigValidity": {
                  "type": "number"
              },
              "sigQty": {
                  "type": "number"
              },
              "xpercent": {
                  "type": "number"
              },
              "msValidity": {
                  "type": "number"
              },
              "stepMax": {
                  "type": "number"
              },
              "medianTimeBlocks": {
                  "type": "number"
              },
              "avgGenTime": {
                  "type": "number"
              },
              "dtDiffEval": {
                  "type": "number"
              },
              "percentRot": {
                  "type": "number"
              },
              "udTime0": {
                  "type": "number"
              },
              "udReevalTime0": {
                  "type": "number"
              },
              "dtReeval": {
                  "type": "number"
              }
            },
        "required": ["currency", "c", "dt", "ud0","sigPeriod", "sigValidity", "sigQty", "xpercent", "sigStock",
                     "sigWindow", "msValidity","stepMax", "medianTimeBlocks",
                     "avgGenTime", "dtDiffEval", "percentRot", "udTime0", "udReevalTime0", "dtReeval"]
    }


MEMBERSHIPS_SCHEMA = {
        "type": "object",
        "properties":
        {
            "pubkey": {
                "type": "string"
            },
            "uid": {
                "type": "string",
            },
            "sigDate": {
                "type": "string"
            },
            "memberships": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "version": {
                            "type": "number"
                        },
                        "currency": {
                            "type": "string"
                        },
                        "membership": {
                            "type": "string"
                        },
                        "blockNumber": {
                            "type": "number"
                        },
                        "written": {
                            "type": ["number", "null"]
                        }
                    },
                    "required": ["version", "currency", "membership", "blockNumber", "blockHash", "written"]
                }
            }
        },
        "required": ["pubkey", "uid", "sigDate", "memberships"]
    }


BLOCKS_SCHEMA = {
    "type": "array",
    "items": BLOCK_SCHEMA
}

HARDSHIP_SCHEMA = {
    "type": "object",
    "properties": {
        "block": {
            "type": "number"
        },
        "level": {
            "type": "number"
        }
    },
    "required": ["block", "level"]
}


async def parameters(connection):
    """
    GET the blockchain parameters used by this node

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """
    client = API(connection, URL_PATH)
    r = await client.requests_get('/parameters')
    return await parse_response(r, PARAMETERS_SCHEMA)

async def memberships(connection, search):
    """
    GET list of Membership documents for UID/Public key

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str search: UID/Public key
    :rtype: dict
    """
    client = API(connection, URL_PATH)

    r = await client.requests_get('/memberships/%s' % search)
    return await parse_response(r, MEMBERSHIPS_SCHEMA)

async def membership(connection, membership):
    """
    POST a Membership document

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str membership: Membership signed raw document
    :rtype: aiohttp.ClientResponse
    """
    client = API(connection, URL_PATH)

    return await client.requests_post('/membership', membership=membership)

async def block(connection, number=0, block=None, signature=None):
    """
    GET/POST a block from/to the blockchain

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param int number: Block number to get
    :param dict block: Block document to post
    :param str signature: Signature of the block document issuer
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    # POST block
    if block is not None and signature is not None:
        return await client.requests_post('/block', block=block, signature=signature)

    # GET block
    r = await client.requests_get('/block/%d' % number)
    data = await parse_response(r, BLOCK_SCHEMA)
    return data

async def current(connection):
    """
    GET, return last accepted block

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)

    r = await client.requests_get('/current')
    return await parse_response(r, BLOCK_SCHEMA)


async def blocks(connection, count, start):
    """
    GET list of blocks from the blockchain

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param int count: Number of blocks
    :param int start: First block number
    :rtype: list
    """

    client = API(connection, URL_PATH)
    assert type(count) is int
    assert type(start) is int
    r = await client.requests_get('/blocks/%d/%d' % (count, start))
    return await parse_response(r, BLOCKS_SCHEMA)

async def hardship(connection, pubkey):
    """
    GET hardship level for given member's public key for writing next block

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str pubkey:  Public key of the member
    :rtype: dict
    """
    client = API(connection, URL_PATH)
    r = await client.requests_get('/hardship/%s' % pubkey)
    return await parse_response(r, HARDSHIP_SCHEMA)

async def newcomers(connection):
    """
    GET, return block numbers containing newcomers

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    r = await client.requests_get('/with/newcomers')
    return await parse_response(r, BLOCK_NUMBERS_SCHEMA)

async def certifications(connection):
    """
    GET, return block numbers containing certifications

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    r = await client.requests_get('/with/certs')
    return await parse_response(r, BLOCK_NUMBERS_SCHEMA)

async def joiners(connection):
    """
    GET, return block numbers containing joiners

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    r = await client.requests_get('/with/joiners')
    return await parse_response(r, BLOCK_NUMBERS_SCHEMA)

async def actives(connection):
    """
    GET, return block numbers containing actives

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    r = await client.requests_get('/with/actives')
    return await parse_response(r, BLOCK_NUMBERS_SCHEMA)

async def leavers(connection):
    """
    GET, return block numbers containing leavers

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    r = await client.requests_get('/with/leavers')
    return await parse_response(r, BLOCK_NUMBERS_SCHEMA)

async def excluded(connection):
    """
    GET, return block numbers containing excluded

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    r = await client.requests_get('/with/excluded')
    return await parse_response(r, BLOCK_NUMBERS_SCHEMA)

async def ud(connection):
    """
    GET, return block numbers containing universal dividend

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """
    client = API(connection, URL_PATH)
    r = await client.requests_get('/with/ud')
    return await parse_response(r, BLOCK_NUMBERS_SCHEMA)

async def tx(connection):
    """
    GET, return block numbers containing transactions

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)
    r = await client.requests_get('/with/tx')
    return await parse_response(r, BLOCK_NUMBERS_SCHEMA)
