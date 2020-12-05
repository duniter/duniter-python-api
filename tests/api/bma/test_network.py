"""
Copyright  2014-2020 Vincent Texier <vit@free.fr>

DuniterPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DuniterPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest

import jsonschema
from jsonschema import ValidationError, SchemaError

from duniterpy.api.bma import network
from duniterpy.api.client import Client
from duniterpy.api.endpoint import BMAEndpoint
from tests.api.webserver import WebFunctionalSetupMixin, web


class TestBmaNetwork(WebFunctionalSetupMixin, unittest.TestCase):
    def test_peers(self):
        json_sample = {
            "peers": [
                {
                    "version": "1",
                    "currency": "beta_brouzouf",
                    "status": "UP",
                    "first_down": None,
                    "last_try": 1607180847,
                    "pubkey": "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY",
                    "block": "378529-00028D6F71E384565A1A106C1247E5F4B0392645A84EDB121173AC930540D552",
                    "signature": "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r",
                    "endpoints": [
                        "BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:0db8:0000:85a3:0000:0000:ac1f 9001",
                        "BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:0db8:0000:85a3:0000:0000:ac1f 9002",
                        "OTHER_PROTOCOL 88.77.66.55 9001",
                    ],
                }
            ]
        }

        try:
            jsonschema.validate(json_sample, network.PEERS_SCHEMA)
        except (SchemaError, ValidationError) as e:
            raise self.failureException from e

    def test_peering(self):
        json_sample = {
            "version": "1",
            "currency": "beta_brouzouf",
            "pubkey": "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY",
            "endpoints": [
                "BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:0db8:0000:85a3:0000:0000:ac1f 9001",
                "BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:0db8:0000:85a3:0000:0000:ac1f 9002",
                "OTHER_PROTOCOL 88.77.66.55 9001",
            ],
            "signature": "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r",
        }
        try:
            jsonschema.validate(json_sample, network.PEERING_SCHEMA)
        except (SchemaError, ValidationError) as e:
            raise self.failureException from e

    def test_peering_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b"{}", content_type="application/json")

        async def go():
            _, port, _ = await self.create_server("GET", "/network/peering", handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                client = Client(BMAEndpoint("127.0.0.1", "", "", port))
                await client(network.peering)
            await client.close()

        self.loop.run_until_complete(go())

    def test_peering_peers_root(self):
        json_sample = {
            "depth": 3,
            "nodesCount": 6,
            "leavesCount": 5,
            "root": "114B6E61CB5BB93D862CA3C1DFA8B99E313E66E9",
        }
        try:
            jsonschema.validate(json_sample, network.PEERING_PEERS_SCHEMA)
        except (SchemaError, ValidationError) as e:
            raise self.failureException from e

    def test_peering_peers_leaf(self):
        json_sample = {
            "hash": "2E69197FAB029D8669EF85E82457A1587CA0ED9C",
            "value": {
                "version": "1",
                "currency": "beta_brouzouf",
                "pubkey": "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY",
                "endpoints": [
                    "BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:0db8:0000:85a3:0000:0000:ac1f 9001",
                    "BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:0db8:0000:85a3:0000:0000:ac1f 9002",
                    "OTHER_PROTOCOL 88.77.66.55 9001",
                ],
                "signature": "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r",
            },
        }
        try:
            jsonschema.validate(json_sample, network.PEERING_PEERS_SCHEMA)
        except (SchemaError, ValidationError) as e:
            raise self.failureException from e

    def test_peering_peers_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b"{}", content_type="application/json")

        async def go():
            _, port, _ = await self.create_server(
                "GET", "/network/peering/peers", handler
            )
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                client = Client(BMAEndpoint("127.0.0.1", "", "", port))
                await client(network.peering_peers)
            await client.close()

        self.loop.run_until_complete(go())

    def test_ws2p_heads(self):
        json_sample = {
            "heads": [
                {
                    "messageV2": "WS2POCAIC:HEAD:2:238pNfpkNs4TdRgt6NnJ5Q72CDZbgNqm4cJo4nCP3BxC:367572"
                    "-000024399D612753E59D44415CFA61F3A663919110CD2EB8D30C93F49C61E07F:96675302:duniter"
                    ":1.7.10:1:0:0",
                    "message": "WS2POCAIC:HEAD:1:238pNfpkNs4TdRgt6NnJ5Q72CDZbgNqm4cJo4nCP3BxC:367572"
                    "-000024399D612753E59D44415CFA61F3A663919110CD2EB8D30C93F49C61E07F:96675302:duniter:1"
                    ".7.10:1",
                    "sigV2": "G1YQd5hgW6+bVGSZJgFzBjZyHgiIqzgUzHOVjcelbHJnwFtxl9XtqZiC5Ul0+Wv8im4IcOwgPypzFe/xUVJMBQ==",
                    "sig": "frlBj5ntC64H/iqNTqsB+igvEn2C9RD6fF2UOvZHWlzEqyaFy0YSRDyvZIyCTi/kPC+f1Xq2PKUItZvQdqPuAQ==",
                    "step": 0,
                },
                {
                    "messageV2": "WS2POTAIT:HEAD:2:CrznBiyq8G4RVUprH9jHmAw1n1iuzw8y9FdJbrESnaX7:378529"
                    "-00028D6F71E384565A1A106C1247E5F4B0392645A84EDB121173AC930540D552:3eaab4c7:duniter"
                    ":1.7.18:1:30:30",
                    "message": "WS2POTAIT:HEAD:1:CrznBiyq8G4RVUprH9jHmAw1n1iuzw8y9FdJbrESnaX7:378529"
                    "-00028D6F71E384565A1A106C1247E5F4B0392645A84EDB121173AC930540D552:3eaab4c7:duniter:1"
                    ".7.18:1",
                    "sigV2": "EIa5P8jJSdKR740/fLgu8u+7VFf6tiDs3xGKHxiM8nTVLjsZR8RoZtRGexqG0XIoPGpCty9rIduOu83knsorAA==",
                    "sig": "up5LLKm9DEXeiEAcMyPv9hignCx/rKlXSfcHVH1EZUOEMcNBiE4WzR4kSU8AA5cSpBYpZ7Uoo9y4ATmrLj3YDw==",
                    "step": 2,
                },
            ]
        }
        try:
            jsonschema.validate(json_sample, network.WS2P_HEADS_SCHEMA)
        except (SchemaError, ValidationError) as e:
            raise self.failureException from e

    def test_ws2p_heads_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b"{}", content_type="application/json")

        async def go():
            _, port, _ = await self.create_server("GET", "/network/ws2p/heads", handler)
            with self.assertRaises(jsonschema.ValidationError):
                client = Client(BMAEndpoint("127.0.0.1", "", "", port))
                await client(network.ws2p_heads)
            await client.close()

        self.loop.run_until_complete(go())
