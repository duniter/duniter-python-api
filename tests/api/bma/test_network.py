import unittest

import aiohttp
import jsonschema

from duniterpy.documents import BMAEndpoint
from tests.api.webserver import WebFunctionalSetupMixin, web
from duniterpy.api.bma import network


class TestBMANetwork(WebFunctionalSetupMixin, unittest.TestCase):

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
          "signature": "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r"
        }
        jsonschema.validate(json_sample, network.PEERING_SCHEMA)

    def test_peering_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/network/peering', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await network.peering(connection)

        self.loop.run_until_complete(go())

    def test_peers_root(self):
        json_sample = {
          "depth": 3,
          "nodesCount": 6,
          "leavesCount": 5,
          "root": "114B6E61CB5BB93D862CA3C1DFA8B99E313E66E9"
        }
        jsonschema.validate(json_sample, network.PEERS_SCHEMA)

    def test_peers_leaf(self):
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
            "signature": "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r"
          }
        }
        jsonschema.validate(json_sample, network.PEERS_SCHEMA)

    def test_peers_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/network/peering/peers', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await network.peers(connection)

        self.loop.run_until_complete(go())
