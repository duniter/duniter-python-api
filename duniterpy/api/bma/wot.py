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

logger = logging.getLogger("duniter/wot")

URL_PATH = 'wot'


CERTIFICATIONS_SCHEMA = {
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


MEMBERS_SCHEMA = {
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


REQUIREMENTS_SCHEMA = {
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

LOOKUP_SCHEMA = {
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

async def add(connection, identity):
    """
    POST identity document

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param duniterpy.documents.certification.Identity identity: Identity document
    :rtype: aiohttp.ClientResponse
    """
    client = API(connection, URL_PATH)

    r = await client.requests_post('/add', identity=identity)
    return r

async def certify(connection, cert):
    """
    POST certification document

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param duniterpy.documents.certification.Certification cert: Certification document
    :rtype: aiohttp.ClientResponse
    """
    client = API(connection, URL_PATH)

    r = await client.requests_post('/certify', cert=cert)
    return r

async def revoke(connection, revocation):
    """
    POST revocation document

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param duniterpy.documents.certification.Revocation revocation: Certification document
    :rtype: aiohttp.ClientResponse
    """
    client = API(connection, URL_PATH)

    r = await client.requests_post('/revoke', revocation=revocation)
    return r


async def lookup(connection, search):
    """
    GET UID/Public key data

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str search: UID or public key
    :rtype: dict
    """
    client = API(connection, URL_PATH)

    r = await client.requests_get('/lookup/%s' % search)
    return await parse_response(r, LOOKUP_SCHEMA)


async def certifiers_of(connection, search):
    """
    GET UID/Public key certifiers

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str search: UID or public key
    :rtype: dict
    """

    client = API(connection, URL_PATH)

    r = await client.requests_get('/certifiers-of/%s' % search)
    return await parse_response(r, CERTIFICATIONS_SCHEMA)

async def certified_by(connection, search):
    """
    GET identities certified by UID/Public key

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str search: UID or public key
    :rtype: dict
    """
    client = API(connection, URL_PATH)

    r = await client.requests_get('/certified-by/%s' % search)
    return await parse_response(r, CERTIFICATIONS_SCHEMA)

async def members(connection):
    """
    GET list of all current members of the Web of Trust

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """
    client = API(connection, URL_PATH)

    r = await client.requests_get('/members')
    return await parse_response(r, MEMBERS_SCHEMA)


async def requirements(connection, search):
    """
    GET list of requirements for a given UID/Public key

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str search: UID or public key
    :rtype: dict
    """
    client = API(connection, URL_PATH)

    r = await client.requests_get('/requirements/%s' % search)
    return await parse_response(r, REQUIREMENTS_SCHEMA)
