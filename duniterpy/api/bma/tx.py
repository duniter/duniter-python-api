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

logger = logging.getLogger("duniter/tx")

URL_PATH = 'tx'

HISTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "currency": {
            "type": "string"
        },
        "pubkey": {
            "type": "string"
        },
        "history": {
            "type": "object",
            "properties": {
                "sent": {
                    "$ref": "#/definitions/transaction_data"
                },
                "received": {
                    "$ref": "#/definitions/transaction_data"
                },
                "sending": {
                    "$ref": "#/definitions/transactioning_data"
                },
                "receiving": {
                    "$ref": "#/definitions/transactioning_data"
                },
            },
            "required": ["sent", "received", "sending", "receiving"]
        }
    },
    "definitions": {
        "transaction_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "version": {
                        "type": "number"
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
                    "outputs": {
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
                    "comment": {
                        "type": "string"
                    },
                    "signatures": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "hash": {
                        "type": "string"
                    },
                    "block_number": {
                        "type": "number"
                    },
                    "time": {
                        "type": "number"
                    }
                },
                "required": ["version", "issuers", "inputs", "outputs",
                             "comment", "signatures", "hash", "block_number", "time"]
            }
        },
        "transactioning_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "version": {
                        "type": "number"
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
                    "outputs": {
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
                    "comment": {
                        "type": "string"
                    },
                    "signatures": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "hash": {
                        "type": "string"
                    },
                },
                "required": ["version", "issuers", "inputs", "outputs",
                             "comment", "signatures", "hash"]
            }
        }
    },
    "required": ["currency", "pubkey", "history"]
}

SOURCES_SCHEMA = {
        "type": "object",
        "properties": {
            "currency": {
                "type": "string"
            },
            "pubkey": {
                "type": "string"
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string"
                        },
                        "noffset": {
                            "type": "number"
                        },
                        "identifier": {
                            "type": "string"
                        },
                        "amount": {
                            "type": "number"
                        },
                        "base": {
                            "type": "number"
                        }
                    },
                    "required": ["type", "noffset", "identifier", "amount", "base"]
                }
            }
        },
        "required": ["currency", "pubkey", "sources"]
    }

async def history(connection, pubkey):
    """
    Get transactions history of public key

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str pubkey: Public key
    :rtype: dict
    """

    client = API(connection, URL_PATH)

    r = await client.requests_get( '/history/%s' % pubkey)
    return await parse_response(r, HISTORY_SCHEMA)

async def process(connection, transaction):
    """
    POST a transaction

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param duniterpy.documents.Transaction transaction: Transaction document
    :rtype: aiohttp.ClientResponse
    """
    client = API(connection, URL_PATH)

    r = await client.requests_post('/process', transaction=transaction)
    return r


async def sources(connection, pubkey):
    """
    GET transaction sources

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str pubkey: Public key
    :rtype: dict
    """
    client = API(connection, URL_PATH)

    r = await client.requests_get( '/sources/%s' % pubkey)
    return await parse_response(r, SOURCES_SCHEMA)

async def blocks(connection, pubkey, start, end):
    """
    GET public key transactions history between start and end block number

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str pubkey: Public key
    :param int start: Start from block number
    :param int end: End to block number
    :return: dict
    """
    client = API(connection, URL_PATH)

    r = await client.requests_get('/history/%s/blocks/%s/%s' % (pubkey, start, end))
    return await parse_response(r, HISTORY_SCHEMA)

async def times(connection, pubkey, start, end):
    """
    GET public key transactions history between start and end timestamp

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str pubkey: Public key
    :param int start: Start from timestamp
    :param int end: End to timestamp
    :return: dict
    """
    client = API(connection, URL_PATH)

    r = await client.requests_get('/history/%s/times/%s/%s' % (pubkey, start, end))
    return await parse_response(r, HISTORY_SCHEMA)
