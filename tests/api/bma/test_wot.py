import aiohttp
import unittest
import jsonschema
import json
from tests.api.webserver import WebFunctionalSetupMixin, web, asyncio
from duniterpy.documents import BMAEndpoint
from duniterpy.api.bma.wot import lookup, members, certified_by, certifiers_of, requirements, \
    REQUIREMENTS_SCHEMA, CERTIFICATIONS_SCHEMA, LOOKUP_SCHEMA, MEMBERS_SCHEMA


class Test_BMA_Wot(WebFunctionalSetupMixin, unittest.TestCase):
    def test_bma_wot_lookup(self):
        json_sample = {
  "partial": False,
  "results": [
            {
              "pubkey": "5cnvo5bmR8QbtyNVnkDXWq6n5My6oNLd1o6auJApGCsv",
              "uids": [
                {
                  "uid": "inso",
                  "meta": {
                    "timestamp": "0-E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"
                  },
                  "revoked": False,
                  "revoked_on": None,
                  "revocation_sig": None,
                  "self": "gTUSERA3IqEzMDvdpiFkTgBBFKwUl7M62e+VCzwyHJTrxvBSB+C+8ImoKsd7pYFAnZ+HL6cJ1p7jyVUIOZGqCw==",
                  "others": [
                    {
                      "pubkey": "Ds1z6Wd8hNTexBoo3LVG2oXLZN4dC9ZWxoWwnDbF1NEW",
                      "meta": {
                        "block_number": 0,
                        "block_hash": "000003D02B95D3296A4F06DBAC51775C4336A4DC09D0E958DC40033BE7E20F3D"
                      },
                      "uids": [
                        "Galuel"
                      ],
                      "isMember": True,
                      "wasMember": True,
                      "signature": "iK3TOdqrHhUbHNB3cPpmWd8sTL2hz0wiScZmXlRc8WhLg2et3xMjAHMuF+wuiM9/7R3daKZq5dOGF3drOuApAg=="
                    },
                    {
                      "pubkey": "7F6oyFQywURCACWZZGtG97Girh9EL1kg2WBwftEZxDoJ",
                      "meta": {
                        "block_number": 0,
                        "block_hash": "000003D02B95D3296A4F06DBAC51775C4336A4DC09D0E958DC40033BE7E20F3D"
                      },
                      "uids": [
                        "vit"
                      ],
                      "isMember": True,
                      "wasMember": True,
                      "signature": "eTdxT+2VikgYgdFENy/zmYxFyDDpBuGDBHedS7CzlEfYWU7iClZ9se06QdtzkFtiOtQ1BBkWPVMXxbqF8KSECw=="
                    },
                      ]
                },
              ],
              "signed": [
                    {
                      "uid": "yannlefranco",
                      "pubkey": "8SJZia3RJ36hp3wXy8AJXJj8z7yeLHCVaTtv2xSi2MBj",
                      "meta": {
                        "timestamp": "0-E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"
                      },
                      "cert_time": {
                        "block": 0
                      },
                      "isMember": True,
                      "wasMember": True,
                      "signature": "lYdOV3uLH3DQHzuODuaZXQnfPIKKF9AsT84b8pkmgU65trAojmTpuBgaYaPN0Yce+8dwtdHxby7h5pO0RWgRBw=="
                    },
                    {
                      "uid": "Galuel",
                      "pubkey": "Ds1z6Wd8hNTexBoo3LVG2oXLZN4dC9ZWxoWwnDbF1NEW",
                      "meta": {
                        "timestamp": "0-E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"
                      },
                      "cert_time": {
                        "block": 0
                      },
                      "isMember": True,
                      "wasMember": True,
                      "signature": "PcZUAleSeR38CbL5zfcdN2+ir+s11Y6oIl2iO4t80M4PXKXWHeqd0uYore0JibMBVnIhpLqcC8SpyVmZnfdaAQ=="
                    }
          ]
            },
            {
              "pubkey": "7hygreNPE4LJpQhB6zHqGsofKA2G3dDXQM2n6LkDBakB",
              "uids": [
                {
                  "uid": "Mymypinson",
                  "meta": {
                    "timestamp": "17524-00000C1533A49A4EC583B91148E2A38E91E39396BAD0C8D3A5B93338E905EF83"
                  },
                  "revoked": False,
                  "revoked_on": None,
                  "revocation_sig": None,
                  "self": "trkirggMe9HsnO4T2FV9h1NKzxiZncXB5D5znhuq3zDZaY3MTja2edWaJhO0KcFU4yZdQPudt8ltldYL0rk1Cg==",
                  "others": [
                    {
                      "pubkey": "zio4Jp8hnqkYmoz5FMYm1siCjGmjWzVUg27KMfDoefA",
                      "meta": {
                        "block_number": 19452,
                        "block_hash": "00000B96722EC36F4089D2490929931B3CF26994A8ED6708C6C71370D60AA25F"
                      },
                      "uids": [
                        "eliadem"
                      ],
                      "isMember": True,
                      "wasMember": True,
                      "signature": "GJJa4T9eOJf6oL+SYLGQDnD4K1TpC1492ItGa4+51imkJRXMTvvYmZguwbOuBn8GRISxlMqfgzbHzj5SFG0ODg=="
                    },
                    {
                      "pubkey": "5SwfQubSat5SunNafCsunEGTY93nVM4kLSsuprNqQb6S",
                      "meta": {
                        "block_number": 19452,
                        "block_hash": "00000B96722EC36F4089D2490929931B3CF26994A8ED6708C6C71370D60AA25F"
                      },
                      "uids": [
                        "Patrice_F"
                      ],
                      "isMember": True,
                      "wasMember": True,
                      "signature": "E2Km7x6L8/iiFuWVa+UHailM/AOsM/1COj9aQM7B0bDRMx6h+iSfOPxnUSXydiaeT1FPlNeLZOEKIcNmRk6gCA=="
                    },
                  ],
                }
              ],
                "signed": [
                    {
                      "uid": "Duarte",
                      "pubkey": "GRBPV3Y7PQnB9LaZhSGuS3BqBJbSHyibzYq65kTh1nQ4",
                      "meta": {
                        "timestamp": "20544-000008FFA0AABEA96759559DA426D92880EA35878C680479135A5C9A3FFA8BF9"
                      },
                      "cert_time": {
                        "block": 35202
                      },
                      "isMember": True,
                      "wasMember": True,
                      "signature": "regfnOZWIrA4Tkj+MU6PFwHcfm/8G+ygDlNGKUP7b5pLhBHGVVMIw3xh6PcLHSkUUmnxlTImuqGJg+ky6dl3CA=="
                    },
                    {
                      "uid": "NicolasCARRAT",
                      "pubkey": "44PxHAjt5L9vasbgruPeccs1kjhG3sdzP3ATRWvXSLop",
                      "meta": {
                        "timestamp": "21924-000007B75B75D8E6393F609BD42423776FAB90500BCAE7EAAC498BD8EC6DFABB"
                      },
                      "cert_time": {
                        "block": 36645
                      },
                      "isMember": True,
                      "wasMember": True,
                      "signature": "kC8hoeM2b0wiis5iaF4aHEzRUs0YQy7qJyPFD4rGtZ6II+EN5WbvmxQaN7PckoRUbbSFhNC4gMcnrClNdchBBQ=="
                    },
          ]
            }
          ]
    }
        jsonschema.validate(json_sample, LOOKUP_SCHEMA)

    def test_bma_wot_lookup_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, port, url = await self.create_server('GET', '/wot/lookup/pubkey', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                async with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await lookup(connection, 'pubkey')

        self.loop.run_until_complete(go())

    def test_bma_wot_members(self):
        json_sample = {
            "results": [
                {"pubkey": "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY", "uid": "cat"},
                {"pubkey": "9kNEiyseUNoPn3pmNUhWpvCCwPRgavsLu7YFKZuzzd1L", "uid": "tac"},
                {"pubkey": "9HJ9VXa9wc6EKC6NkCi8b5TKWBot68VhYDg7kDk5T8Cz", "uid": "toc"}
            ]
        }
        jsonschema.validate(MEMBERS_SCHEMA, json_sample)

    def test_bma_wot_members_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, port, url = await self.create_server('GET', '/wot/members', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                async with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await members(connection)

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
        jsonschema.validate(json_sample, CERTIFICATIONS_SCHEMA)
        jsonschema.validate(json_sample, CERTIFICATIONS_SCHEMA)

    def test_bma_wot_certifiers_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, port, url = await self.create_server('GET', '/wot/certifiers-of/pubkey', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                async with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await certifiers_of(connection, 'pubkey')

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
            _, port, url = await self.create_server('GET', '/wot/certifiers-of/pubkey', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                async with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await certifiers_of(connection, 'pubkey')

        self.loop.run_until_complete(go())

    def test_bma_wot_certified_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, port, url = await self.create_server('GET', '/wot/certified-by/pubkey', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                async with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await certified_by(connection, 'pubkey')

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
                    "revocation_sig": None,
                    "revoked": False,
                    "revoked_on": None,
                    "expired": False,
                    "isSentry": True,
                    "wasMember": True,
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
        jsonschema.validate(json_sample, REQUIREMENTS_SCHEMA)

