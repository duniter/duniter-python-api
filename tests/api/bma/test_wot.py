import aiohttp
import unittest
import jsonschema
import json
from tests.api.webserver import WebFunctionalSetupMixin, web, asyncio
from duniterpy.api.bma.wot import Lookup, Members, CertifiedBy, CertifiersOf, Requirements


class Test_BMA_Wot(WebFunctionalSetupMixin, unittest.TestCase):
    def test_bma_wot_lookup(self):
        json_sample = {
            "partial": False,
            "results": [
                {
                    "pubkey": "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY",
                    "uids": [
                        {
                            "uid": "udid2;c;TOCQUEVILLE;FRANCOIS-XAVIER-ROBE;1989-07-14;e+48.84+002.30;0;",
                            "meta": {
                                "timestamp": "44-76522E321B3380B058DB6D9E66121705EEA63610869A7C5B3E701CF6AF2D55A8"
                            },
                            "self": "J3G9oM5AKYZNLAB5Wx499w61NuUoS57JVccTShUbGpCMjCqj9yXXqNq7dyZpDWA6BxipsiaMZhujMeBfCznzyci",
                            "others": [
                                {
                                    "pubkey": "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB",
                                    "meta": {
                                        "timestamp": "44-76522E321B3380B058DB6D9E66121705EEA63610869A7C5B3E701CF6AF2D55A8"
                                    },
                                    "signature": "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r"
                                }
                            ]
                        }
                    ],
                    "signed": [
                        {
                            "uid": "snow",
                            "pubkey": "2P7y2UDiCcvsgSSt8sgHF3BPKS4m9waqKw4yXHCuP6CN",
                            "meta": {
                                "timestamp": "44-76522E321B3380B058DB6D9E66121705EEA63610869A7C5B3E701CF6AF2D55A8"
                            },
                            "signature": "Xbr7qhyGNCmLoVuuKnKIbrdmtCvb9VBIEY19izUNwA5nufsjNm8iEsBTwKWOo0lq5O1+AAPMnht8cm2JjMq8AQ=="
                        },
                        {
                            "uid": "snow",
                            "pubkey": "2P7y2UDiCcvsgSSt8sgHF3BPKS4m9waqKw4yXHCuP6CN",
                            "meta": {
                                "timestamp": "44-76522E321B3380B058DB6D9E66121705EEA63610869A7C5B3E701CF6AF2D55A8"
                            },
                            "signature": "HU9VPwC4EqPJwATPuyUJM7HLjfig5Ke1CKonL9Q78n5/uNSL2hkgE9Pxsor8CCJfkwCxh66NjGyqnGYqZnQMAg=="
                        },
                        {
                            "uid": "snow",
                            "pubkey": "7xapQvvxQ6367bs8DsskEf3nvQAgJv97Yu11aPbkCLQj",
                            "meta": {
                                "timestamp": "44-76522E321B3380B058DB6D9E66121705EEA63610869A7C5B3E701CF6AF2D55A8"
                            },
                            "signature": "6S3x3NwiHB2QqYEY79x4wCUYHcDctbazfxIyxejs38V1uRAl4DuC8R3HJUfD6wMSiWKPqbO+td+8ZMuIn0L8AA=="
                        },
                        {
                            "uid": "cat",
                            "pubkey": "CK2hBp25sYQhdBf9oFMGHyokkmYFfzSCmwio27jYWAN7",
                            "meta": {
                                "timestamp": "44-76522E321B3380B058DB6D9E66121705EEA63610869A7C5B3E701CF6AF2D55A8"
                            },
                            "signature": "AhgblSOdxUkLwpUN9Ec46St3JGaw2jPyDn/mLcR4j3EjKxUOwHBYqqkxcQdRz/6K4Qo/xMa941MgUp6NjNbKBA=="
                        }
                    ]
                }
            ]
        }
        jsonschema.validate(json_sample, Lookup.schema)

    def test_bma_wot_lookup_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/pubkey', handler)
            lookup = Lookup(None, "pubkey")
            lookup.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await lookup.get(session)

        self.loop.run_until_complete(go())

    def test_bma_wot_members(self):
        json_sample = {
            "results": [
                {"pubkey": "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY", "uid": "cat"},
                {"pubkey": "9kNEiyseUNoPn3pmNUhWpvCCwPRgavsLu7YFKZuzzd1L", "uid": "tac"},
                {"pubkey": "9HJ9VXa9wc6EKC6NkCi8b5TKWBot68VhYDg7kDk5T8Cz", "uid": "toc"}
            ]
        }
        jsonschema.validate(Members.schema, json_sample)

    def test_bma_wot_members_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            members = Members(None)
            members.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await members.get(session)

        self.loop.run_until_complete(go())

    def test_bma_wot_cert(self):
        json_sample = {
            "pubkey": "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY",
            "uid": "user identifier",
            "isMember": True,
            "certifications": [
                {
                    "pubkey": "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB",
                    "uid": "certifier uid",
                    "cert_time": {
                        "block": 88,
                        "medianTime": 1509991044
                    },
                    "sigDate": "80-D30978C9D6C5A348A8188603F039423D90E50DC5",
                    "written": {
                        "number": 872768,
                        "hash": "D30978C9D6C5A348A8188603F039423D90E50DC5"
                    },
                    "isMember": True,
                    "wasMember": True,
                    "signature": "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r"
                },
                {
                    "pubkey": "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB",
                    "uid": "certifier uid",
                    "sigDate": "80-D30978C9D6C5A348A8188603F039423D90E50DC5",
                    "cert_time": {
                        "block": 88,
                        "medianTime": 1509991044
                    },
                    "written": None,
                    "isMember": True,
                    "wasMember": False,
                    "signature": "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r"
                }
            ]
        }
        jsonschema.validate(json_sample, CertifiersOf.schema)
        jsonschema.validate(json_sample, CertifiedBy.schema)

    def test_bma_wot_certifiers_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/pubkey', handler)
            certsof = CertifiersOf(None, 'pubkey')
            certsof.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await certsof.get(session)

        self.loop.run_until_complete(go())

    def test_bma_wot_certifiers_inner_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=bytes(json.dumps({
                "pubkey": "7Aqw6Efa9EzE7gtsc8SveLLrM7gm6NEGoywSv4FJx6pZ",
                "uid": "john",
                "isMember": True,
                "certifications": [
                    {
                        "pubkey": "FADxcH5LmXGmGFgdixSes6nWnC4Vb4pRUBYT81zQRhjn",
                        "meta": {
                            "block_number": 38580
                        },
                        "uids": [
                            "doe"
                        ],
                        "isMember": True,
                        "wasMember": True,
                        "signature": "8XYmBdElqNkkl4AeFjJnC5oj/ujBrzH9FNgPZvK8Cicp8Du0PQa0yYFG95EQ46MJhdV0fUT2g5xyH8N3/OGhDA=="
                    },
                ]
            }), "utf-8"), content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/pubkey', handler)
            certsof = CertifiersOf(None, 'pubkey')
            certsof.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await certsof.get(session)

        self.loop.run_until_complete(go())

    def test_bma_wot_certified_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/pubkey', handler)
            certby = CertifiedBy(None, 'pubkey')
            certby.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await certby.get(session)

        self.loop.run_until_complete(go())

    def test_bma_wot_requirements(self):
        json_sample = {
            "identities": [
                {
                    "pubkey": "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU",
                    "uid": "inso",
                    "meta": {
                        "timestamp": "1470-46221DE81776D8382F6DE595105386ADEDD291BEC33D238C506F56EA3721B012"
                    },
                    "outdistanced": False,
                    "certifications": [
                        {
                            "from": "J78bPUvLjxmjaEkdjxWLeENQtcfXm7iobqB49uT1Bgp3",
                            "to": "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU",
                            "expiresIn": 30423649
                        },
                        {
                            "from": "9bZEATXBGPUSsk8oAYi4KAChg3rHKwNt67hVdErbNGCW",
                            "to": "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU",
                            "expiresIn": 30488510
                        },
                        {
                            "from": "HGYV5C16mrdvE9vpb1S9nMDHkVPsubBgANs9pSb6HWCV",
                            "to": "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU",
                            "expiresIn": 30505972
                        },
                        {
                            "from": "5ocqzyDMMWf1V8bsoNhWb1iNwax1e9M7VTUN6navs8of",
                            "to": "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU",
                            "expiresIn": 30923721
                        }
                    ],
                    "membershipPendingExpiresIn": 0,
                    "membershipExpiresIn": 14707940
                }
            ]
        }
        jsonschema.validate(Requirements.schema, json_sample)
