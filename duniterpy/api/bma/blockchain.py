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

from duniterpy.api.bma import API, logging

logger = logging.getLogger("duniter/blockchain")


class Blockchain(API):
    def __init__(self, connection_handler, module='blockchain'):
        super(Blockchain, self).__init__(connection_handler, module)


class Parameters(Blockchain):
    """GET the blockchain parameters used by this node."""
    schema = {
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
              "blocksRot": {
                  "type": "number"
              },
              "percentRot": {
                  "type": "number"
              },
            },
        "required": ["currency", "c", "dt", "ud0","sigPeriod", "sigValidity", "sigQty", "xpercent", "sigStock",
                     "sigWindow", "msValidity","stepMax", "medianTimeBlocks",
                     "avgGenTime", "dtDiffEval", "blocksRot", "percentRot"]
    }

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/parameters', **kwargs)
        return (await self.parse_response(r))


class Membership(Blockchain):
    """GET/POST a Membership document."""
    schema = {
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

    def __init__(self, connection_handler, search=None):
        super().__init__(connection_handler)
        self.search = search

    async def __post__(self, session, **kwargs):
        assert 'membership' in kwargs

        r = await self.requests_post(session, '/membership', **kwargs)
        return r

    async def __get__(self, session, **kwargs):
        assert self.search is not None
        r = await self.requests_get(session, '/memberships/%s' % self.search, **kwargs)
        return (await self.parse_response(r))


class Block(Blockchain):
    """GET/POST a block from/to the blockchain."""

    schema = {
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

    def __init__(self, connection_handler, number=None):
        """
        Use the number parameter in order to select a block number.

        Arguments:
        - `number`: block number to select
        """

        super(Block, self).__init__(connection_handler)

        self.number = number

    async def __get__(self, session, **kwargs):
        assert self.number is not None
        r = await self.requests_get(session, '/block/%d' % self.number, **kwargs)
        return (await self.parse_response(r))

    async def __post__(self, session, **kwargs):
        assert 'block' in kwargs
        assert 'signature' in kwargs

        r = await self.requests_post(session, '/block', **kwargs)
        return r


class Current(Blockchain):
    """GET, same as block/[number], but return last accepted block."""

    schema = Block.schema

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/current', **kwargs)
        return (await self.parse_response(r))


class Hardship(Blockchain):
    """GET hardship level for given member's fingerprint for writing next block."""
    schema = {
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

    def __init__(self, connection_handler, fingerprint):
        """
        Use the number parameter in order to select a block number.

        Arguments:
        - `fingerprint`: member fingerprint
        """

        super(Hardship, self).__init__(connection_handler)

        self.fingerprint = fingerprint

    async def __get__(self, session, **kwargs):
        assert self.fingerprint is not None
        r = await self.requests_get(session, '/hardship/%s' % self.fingerprint.upper(), **kwargs)
        return (await self.parse_response(r))


class Newcomers(Blockchain):
    """GET, return block numbers containing newcomers."""

    schema = {
        "type": "object",
        "properties": {
            "result":{
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

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/with/newcomers', **kwargs)
        return await self.parse_response(r)


class Certifications(Blockchain):
    """GET, return block numbers containing certifications."""

    schema = Newcomers.schema

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/with/certs', **kwargs)
        return await self.parse_response(r)


class Joiners(Blockchain):
    """GET, return block numbers containing joiners."""

    schema = Newcomers.schema

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/with/joiners', **kwargs)
        return await self.parse_response(r)


class Actives(Blockchain):
    """GET, return block numbers containing actives."""

    schema = Newcomers.schema

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/with/actives', **kwargs)
        return await self.parse_response(r)


class Leavers(Blockchain):
    """GET, return block numbers containing leavers."""

    schema = Newcomers.schema

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/with/leavers', **kwargs)
        return await self.parse_response(r)


class Excluded(Blockchain):
    """GET, return block numbers containing excluded."""

    schema = Newcomers.schema

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/with/excluded', **kwargs)
        return await self.parse_response(r)


class UD(Blockchain):
    """GET, return block numbers containing universal dividend."""

    schema = Newcomers.schema

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/with/ud', **kwargs)
        return await self.parse_response(r)


class TX(Blockchain):
    """GET, return block numbers containing transactions."""

    schema = Newcomers.schema

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/with/tx', **kwargs)
        return await self.parse_response(r)
