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

logger = logging.getLogger("ucoin/blockchain")


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
      "sigDelay": {
          "type": "number"
      },
      "sigValidity": {
          "type": "number"
      },
      "sigQty": {
          "type": "number"
      },
      "sigWoT": {
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
    }
    }
    def __get__(self, **kwargs):
        r = yield from self.requests_get('/parameters', **kwargs)
        return (yield from self.parse(r))


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
                "type": "number"
            },
            "memberships": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "version": {
                            "type": "string"
                        },
                        "currency": {
                            "type": "string"
                        },
                        "membership": {
                            "type": "string"
                        },
                        "blockNumber": {
                            "type": "number",
                        },
                        "blockHash": {
                            "type": "string"
                        }
                    },
                }
            }
        }
    }

    def __init__(self, connection_handler, search=None):
        super().__init__(connection_handler)
        self.search = search

    def __post__(self, **kwargs):
        assert 'membership' in kwargs

        r = yield from self.requests_post('/membership', **kwargs)
        return r

    def __get__(self, **kwargs):
        assert self.search is not None
        r = yield from self.requests_get('/memberships/%s' % self.search, **kwargs)
        return (yield from self.parse(r))


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
            "timestamp": {
                "type": "number"
            },
            "dividend": {
                "type": ["number", "null"]
            },
            "monetaryMass": {
                "type": "number"
            },
            "issuer": {
                "type": "string"
            },
            "previousHash": {
                "type": "string"
            },
            "previousIssuer": {
                "type": "string"
            },
            "membersCount": {
                "type": "number"
            },
            "hash": {
                "type": "string"
            },
            "identities": {
                "type": "array",
                "item": {
                    "type": "string"
                }
            },
            "joiners": {
                "type": "array",
                "item": {
                    "type": "string"
                }
            },
            "leavers": {
                "type": "array",
                "item": {
                    "type": "string"
                }
            },
            "excluded": {
                "type": "array",
                "item": {
                    "type": "string"
                }
            },
            "certifications": {
                "type": "array",
                "item": {
                    "type": "string"
                }
            },
            "transactions": {
                "type": "array",
                "item": {
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
                            "item": {
                                "type": "string"
                            }
                        },
                        "inputs": {
                            "type": "array",
                            "item": {
                                "type": "string"
                            }
                        },
                        "outputs": {
                            "type": "array",
                            "item": {
                                "type": "string"
                            }
                        }
                    }
                }
            },
            "signature": {
                "type": "string"
            }
        }
    }

    def __init__(self, connection_handler, number=None):
        """
        Use the number parameter in order to select a block number.

        Arguments:
        - `number`: block number to select
        """

        super(Block, self).__init__(connection_handler)

        self.number = number

    def __get__(self, **kwargs):
        assert self.number is not None
        r = yield from self.requests_get('/block/%d' % self.number, **kwargs)
        return (yield from self.parse(r))

    def __post__(self, **kwargs):
        assert 'block' in kwargs
        assert 'signature' in kwargs

        r = yield from self.requests_post('/block', **kwargs)
        return r


class Current(Blockchain):
    """GET, same as block/[number], but return last accepted block."""

    schema = Block.schema

    def __get__(self, **kwargs):
        r = yield from self.requests_get('/current', **kwargs)
        return (yield from self.parse(r))


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
        }
    }

    def __init__(self, connection_handler, fingerprint):
        """
        Use the number parameter in order to select a block number.

        Arguments:
        - `fingerprint`: member fingerprint
        """

        super(Hardship, self).__init__(connection_handler)

        self.fingerprint = fingerprint

    def __get__(self, **kwargs):
        assert self.fingerprint is not None
        r = yield from self.requests_get('/hardship/%s' % self.fingerprint.upper(), **kwargs)
        return (yield from self.parse(r))


class Newcomers(Blockchain):
    """GET, return block numbers containing newcomers."""

    schema = {
        "type": "object",
        "properties": {
            "block": {
                "type": "number"
            },
            "level": {
                "type": "number"
            }
        }
    }

    def __get__(self, **kwargs):
        r = yield from self.requests_get('/with/newcomers', **kwargs)
        return (yield from self.parse(r))


class Certifications(Blockchain):
    """GET, return block numbers containing certifications."""

    schema = Newcomers.schema

    def __get__(self, **kwargs):
        r = yield from self.requests_get('/with/certs', **kwargs)
        return (yield from self.parse(r))


class Joiners(Blockchain):
    """GET, return block numbers containing joiners."""

    schema = Newcomers.schema
    def __get__(self, **kwargs):
        r = yield from self.requests_get('/with/joiners', **kwargs)
        return (yield from self.parse(r))


class Actives(Blockchain):
    """GET, return block numbers containing actives."""

    schema = Newcomers.schema

    def __get__(self, **kwargs):
        r = yield from self.requests_get('/with/actives', **kwargs)
        return (yield from self.parse(r))


class Leavers(Blockchain):
    """GET, return block numbers containing leavers."""

    schema = Newcomers.schema

    def __get__(self, **kwargs):
        r = yield from self.requests_get('/with/leavers', **kwargs)
        return (yield from self.parse(r))


class Excluded(Blockchain):
    """GET, return block numbers containing excluded."""

    schema = Newcomers.schema

    def __get__(self, **kwargs):
        r = yield from self.requests_get('/with/excluded', **kwargs)
        return (yield from self.parse(r))


class UD(Blockchain):
    """GET, return block numbers containing universal dividend."""

    schema = Newcomers.schema

    def __get__(self, **kwargs):
        r = yield from self.requests_get('/with/ud', **kwargs)
        return (yield from r.json())


class TX(Blockchain):
    """GET, return block numbers containing transactions."""

    schema = Newcomers.schema

    def __get__(self, **kwargs):
        r = yield from self.requests_get('/with/tx', **kwargs)
        return (yield from r.json())
