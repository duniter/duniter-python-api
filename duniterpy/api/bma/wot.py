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

logger = logging.getLogger("duniter/wot")


class WOT(API):
    def __init__(self, connection_handler, module='wot'):
        super(WOT, self).__init__(connection_handler, module)


class Add(WOT):
    """POST Identity data."""

    async def __post__(self, session, **kwargs):
        assert 'identity' in kwargs

        r = await self.requests_post(session, '/add', **kwargs)
        return r


class Certify(WOT):
    """POST Certification data."""

    async def __post__(self, session, **kwargs):
        assert 'cert' in kwargs

        r = await self.requests_post(session, '/certify', **kwargs)
        return r


class Revoke(WOT):
    """POST Public key data."""

    async def __post__(self, session, **kwargs):
        assert 'pubkey' in kwargs
        assert 'self_' in kwargs

        r = await self.requests_post(session, '/revoke', **kwargs)
        return r


class Lookup(WOT):
    """GET Public key data."""
    schema = {
        "type": "object",
        "definitions": {
            "meta_data": {
                "type": "object",
                "properties": {
                    "timestamp": {
                        "type": "string"
                    }
                }
            },
        },
        "properties": {
            "partial": {
                "type": "boolean"
            },
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "pubkey": {
                            "type": "string"
                        }
                    },
                    "uids": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "uid": {
                                    "type": "string"
                                },
                                "meta": {
                                    "$ref": "#/definitions/meta_data"
                                },
                                "self": {
                                    "type": "string",
                                },
                                "revokation_sig": {
                                    "type": "string"
                                },
                                "revoked": {
                                    "type": "boolean"
                                },
                                "others": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "pubkey": {
                                                "type": "string",
                                            },
                                            "meta": {
                                                "$ref": "#/definitions/meta_data"
                                            },
                                            "signature": {
                                                "type": "string"
                                            }
                                        }
                                    }
                                }
                            },
                            "required": ["uid", "meta", "self", "revokation_sig", "revoked", "others"]
                        }
                    },
                    "signed": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "uid": {
                                    "type": "string"
                                },
                                "pubkey": {
                                    "type": "string"
                                },
                                "meta": {
                                    "$ref": "#/definitions/meta_data"
                                },
                                "signature": {
                                    "type": "string"
                                },
                                "revokation_sig": {
                                    "type": "string"
                                },
                                "revoked": {
                                    "type": "boolean"
                                }
                            },
                            "required": ["uid", "pubkey", "meta", "revokation_sig", "revoked", "signature"]
                        }
                    },
                    "required": ["uids", "signed"]
                }
            }
        },
        "required": ["partial", "results"]
    }

    def __init__(self, connection_handler, search, module='wot'):
        super(WOT, self).__init__(connection_handler, module)

        self.search = search

    async def __get__(self, session, **kwargs):
        assert self.search is not None

        r = await self.requests_get(session, '/lookup/%s' % self.search, **kwargs)
        return await self.parse_response(r)


class CertifiersOf(WOT):
    """GET Certification data over a member."""

    schema = {
        "type": "object",
        "properties": {
            "pubkey": {
                "type": "string"
            },
            "uid": {
                "type": "string"
            },
            "isMember": {
                "type": "boolean"
            },
            "certifications": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "pubkey": {
                            "type": "string"
                        },
                        "uid": {
                            "type": "string"
                        },
                        "cert_time": {
                            "type": "object",
                            "properties": {
                                "block": {
                                    "type": "number"
                                },
                                "medianTime": {
                                    "type": "number"
                                }
                            },
                            "required": ["block", "medianTime"]
                        },
                        "sigDate": {
                            "type": "string"
                        },
                        "written": {
                            "oneOf": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "number": {
                                            "type": "number",
                                        },
                                        "hash": {
                                            "type": "string"
                                        }
                                    },
                                    "required": ["number", "hash"]
                                },
                                {
                                    "type": "null"
                                }
                            ]
                        },
                        "isMember": {
                            "type": "boolean"
                        },
                        "wasMember": {
                            "type": "boolean"
                        },
                        "signature": {
                            "type": "string"
                        }
                    },
                    "required": ["pubkey", "uid", "cert_time", "sigDate",
                                 "written", "wasMember", "isMember", "signature"]
                }
            }
        },
        "required": ["pubkey", "uid", "isMember", "certifications"]
    }

    def __init__(self, connection_handler, search, module='wot'):
        super(WOT, self).__init__(connection_handler, module)

        self.search = search

    async def __get__(self, session, **kwargs):
        assert self.search is not None

        r = await self.requests_get(session, '/certifiers-of/%s' % self.search, **kwargs)
        return await self.parse_response(r)


class CertifiedBy(WOT):
    """GET Certification data from a member."""

    schema = CertifiersOf.schema

    def __init__(self, connection_handler, search, module='wot'):
        super(WOT, self).__init__(connection_handler, module)

        self.search = search

    async def __get__(self, session, **kwargs):
        assert self.search is not None

        r = await self.requests_get(session, '/certified-by/%s' % self.search, **kwargs)
        return await self.parse_response(r)


class Members(WOT):
    """GET List all current members of the Web of Trust."""
    schema = {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "pubkey": {
                            "type": "string"
                        }
                    },
                    "required": ["pubkey"]
                }
            }
        },
        "required": ["results"]
    }

    def __init__(self, connection_handler, module='wot'):
        super(WOT, self).__init__(connection_handler, module)

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/members', **kwargs)
        return await self.parse_response(r)


class Requirements(WOT):
    """
    Get list of requirements for a given pubkey
    """
    schema = {
        "type": "object",
        "properties": {
            "identities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "pubkey": {
                            "type": "string"
                        },
                        "uid": {
                            "type": "string"
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string"
                                }
                            }
                        },
                        "outdistanced": {
                            "type": "boolean"
                        },
                        "certifications": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "from": {
                                        "type": "string"
                                    },
                                    "to": {
                                        "type": "string"
                                    },
                                    "expiresIn": {
                                        "type": "number"
                                    }
                                }
                            }
                        },
                        "membershipPendingExpiresIn": {
                            "type": "number"
                        },
                        "membershipExpiresIn": {
                            "type": "number"
                        }
                    }
                }
            }
        }
    }

    def __init__(self, connection_handler, search, module='wot'):
        super(WOT, self).__init__(connection_handler, module)

        self.search = search

    async def __get__(self, session, **kwargs):
        assert self.search is not None

        r = await self.requests_get(session, '/requirements/%s' % self.search, **kwargs)
        return await self.parse_response(r)
