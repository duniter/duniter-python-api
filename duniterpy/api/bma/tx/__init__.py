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

from .. import API, logging

logger = logging.getLogger("duniter/tx")


class Tx(API):
    def __init__(self, connection_handler, module='tx'):
        super(Tx, self).__init__(connection_handler, module)


class History(Tx):
    """Get transaction sources."""
    schema = {
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

    def __init__(self, conn_handler, pubkey, module='tx'):
        super(Tx, self).__init__(conn_handler, module)
        self.pubkey = pubkey

    async def __get__(self, session, **kwargs):
        assert self.pubkey is not None
        r = await self.requests_get(session, '/history/%s' % self.pubkey, **kwargs)
        return await self.parse_response(r)


class Process(Tx):
    """POST a transaction."""

    async def __post__(self, session, **kwargs):
        assert 'transaction' in kwargs

        r = await self.requests_post(session, '/process', **kwargs)
        return r


class Sources(Tx):
    """Get transaction sources."""
    schema = {
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

    def __init__(self, connection_handler, pubkey, module='tx'):
        super(Tx, self).__init__(connection_handler, module)
        self.pubkey = pubkey

    async def __get__(self, session, **kwargs):
        assert self.pubkey is not None
        r = await self.requests_get(session, '/sources/%s' % self.pubkey, **kwargs)
        return await self.parse_response(r)


from . import history
