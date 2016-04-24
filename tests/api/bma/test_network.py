import unittest
import jsonschema
from duniterpy.api.bma.network import Peering
from tests.api.webserver import WebFunctionalSetupMixin, web, asyncio
from duniterpy.api.bma.network.peering import Peers


class Test_BMA_Network(WebFunctionalSetupMixin, unittest.TestCase):

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
        jsonschema.validate(json_sample, Peering.schema)

    def test_peering_bad(self):
        async        def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async        def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            peering = Peering(None)
            peering.reverse_url = lambda path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                await peering.get()

    def test_peers_root(self):
        json_sample = {
          "depth": 3,
          "nodesCount": 6,
          "leavesCount": 5,
          "root": "114B6E61CB5BB93D862CA3C1DFA8B99E313E66E9"
        }
        jsonschema.validate(json_sample, Peers.schema)

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
        jsonschema.validate(json_sample, Peers.schema)

    def test_peers_bad(self):
        async        def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async        def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            peers = Peers(None)
            peers.reverse_url = lambda path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                await peers.get()