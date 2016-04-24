import unittest
import jsonschema
import aiohttp
from duniterpy.api.bma.tx import History, Sources
from tests.api.webserver import WebFunctionalSetupMixin, web, asyncio
from duniterpy.api.bma.tx.history import Blocks


class Test_BMA_TX(WebFunctionalSetupMixin, unittest.TestCase):
    def test_bma_tx_history(self):
        json_sample = {
          "currency": "meta_brouzouf",
          "pubkey": "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
          "history": {
            "sent": [
              {
                "version": 1,
                "issuers": [
                  "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
                ],
                "inputs": [
                  "0:D:125:000A8362AE0C1B8045569CE07735DE4C18E81586:100"
                ],
                "outputs": [
                  "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:5",
                  "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:95"
                ],
                "comment": "Essai",
                "signatures": [
                  "8zzWSU+GNSNURnH1NKPT/TBoxngEc/0wcpPSbs7FqknGxud+94knvT+dpe99k6NwyB5RXvOVnKAr4p9/KEluCw=="
                ],
                "hash": "FC7BAC2D94AC9C16AFC5C0150C2C9E7FBB2E2A09",
                "block_number": 173,
                "time": 1421932545
              }
            ],
            "received": [
              {
                "version": 1,
                "issuers": [
                  "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU"
                ],
                "inputs": [
                  "0:D:125:000A8362AE0C1B8045569CE07735DE4C18E81586:100"
                ],
                "outputs": [
                  "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:7",
                  "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:93"
                ],
                "comment": "",
                "signatures": [
                  "1Mn8q3K7N+R4GZEpAUm+XSyty1Uu+BuOy5t7BIRqgZcKqiaxfhAUfDBOcuk2i4TJy1oA5Rntby8hDN+cUCpvDg=="
                ],
                "hash": "5FB3CB80A982E2BDFBB3EA94673A74763F58CB2A",
                "block_number": 207,
                "time": 1421955525
              },
              {
                "version": 1,
                "issuers": [
                  "J78bPUvLjxmjaEkdjxWLeENQtcfXm7iobqB49uT1Bgp3"
                ],
                "inputs": [
                  "0:T:15128:6A50FF82410387B239489CE38B34E0FDDE1697FE:10000"
                ],
                "outputs": [
                  "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:42",
                  "J78bPUvLjxmjaEkdjxWLeENQtcfXm7iobqB49uT1Bgp3:9958"
                ],
                "comment": "",
                "signatures": [
                  "XhBcCPizPiWdKeXWg1DX/FTQst6DppEjsYEtoAZNA0P11reXtgc9IduiIxNWzNjt/KvTw8APkSI8/Uf31QQVDA=="
                ],
                "hash": "ADE7D1C4002D6BC10013C34CE22733A55173BAD4",
                "block_number": 15778,
                "time": 1432314584
              }
            ],
            "sending": [
              {
                "version": 1,
                "issuers": [
                  "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
                ],
                "inputs": [
                  "0:D:8196:000022AD426FE727C707D847EC2168A64C577706:5872"
                ],
                "outputs": [
                  "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:5871"
                  "2sq8bBDQGK74f1eD3mAPQVgHCmFdijZr9nbv16FwbokX:1",
                ],
                "comment": "some comment",
                "signatures": [
                  "kLOAAy7/UldQk7zz4I7Jhv9ICuGYRx7upl8wH8RYL43MMF6+7MbPh3QRN1qNFGpAfa3XMWIQmbUWtjZKP6OfDA=="
                ],
                "hash": "BA41013F2CD38EDFFA9D38A275F8532DD906A2DE"
              }
            ],
            "receiving": [
             {
                "version": 1,
                "issuers": [
                  "2sq8bBDQGK74f1eD3mAPQVgHCmFdijZr9nbv16FwbokX"
                ],
                "inputs": [
                  "0:D:8196:000022AD426FE727C707D847EC2168A64C577706:4334"
                ],
                "outputs": [
                  "2sq8bBDQGK74f1eD3mAPQVgHCmFdijZr9nbv16FwbokX:1",
                  "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:4333"
                ],
                "comment": "some comment",
                "signatures": [
                  "DRiZinUEKrrLiJNogtydzwEbmETrvWiLNYXCiJsRekxTLyU5g4LjnwiLp/XlvmIekjJK5n/gullLWrHUBvFSAw=="
                ],
                "hash": "A0A511131CD0E837204A9441B3354918AC4CE671"
              }
            ]
          }
        }
        jsonschema.validate(json_sample, History.schema)
        jsonschema.validate(json_sample, Blocks.schema)

    def test_bma_tx_history_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/pubkey', handler)
            history = History(None, 'pubkey')
            history.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await history.get(session)

        self.loop.run_until_complete(go())

    def test_bma_tx_history_blocks_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/pubkey/0/100', handler)
            blocks = Blocks(None, 'pubkey', 0, 100)
            blocks.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await blocks.get(session)

        self.loop.run_until_complete(go())

    def test_bma_tx_sources(self):
        json_sample = {
          "currency": "meta_brouzouf",
          "pubkey": "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU",
          "sources": [
            {
              "pubkey": "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU",
              "type": "T",
              "noffset": 34444,
              "identifier": "6ACECB199D1B054B2633D0E42C066939B7F8EF1D",
              "amount": 1000000,
              "base": 1
            },
            {
              "pubkey": "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU",
              "type": "D",
              "noffset": 34989,
              "identifier": "0007CCC9755067008C28E791E6F2B0D4CBE9B894",
              "amount": 1730543585843,
              "base": 2
            }
          ]
        }
        jsonschema.validate(json_sample, Sources.schema)

    def test_bma_tx_sources_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/pubkey', handler)
            sources = Sources(None, 'pubkey')
            sources.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await sources.get(session)

        self.loop.run_until_complete(go())