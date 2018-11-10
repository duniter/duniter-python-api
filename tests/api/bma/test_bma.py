import asyncio
import unittest

import aiohttp

from duniterpy.api.client import API, parse_error
from duniterpy.api.endpoint import BMAEndpoint


class TestBmaApi(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        try:
            self.loop.stop()
            self.loop.close()
        finally:
            asyncio.set_event_loop(None)

    def test_reverse_url_complete(self):
        async def go():
            endpoint = BMAEndpoint("test.com", "124.2.2.1", "2001:0db8:0000:85a3:0000:0000:ac1f:8001 ", 9092)
            session = aiohttp.ClientSession()
            api = API(endpoint.conn_handler(session), )
            self.assertEqual(api.reverse_url("http", "/test/url"), "http://test.com:9092/test/url")
            await session.close()

        self.loop.run_until_complete(go())

    def test_reverse_url_only_ipv4(self):
        async def go():
            endpoint = BMAEndpoint("", "124.2.2.1", "", 9092)
            session = aiohttp.ClientSession()

            api = API(endpoint.conn_handler(session), )
            self.assertEqual(api.reverse_url("http", "/test/url"), "http://124.2.2.1:9092/test/url")
            await session.close()

        self.loop.run_until_complete(go())

    def test_reverse_url_only_ipv6(self):
        async def go():
            endpoint = BMAEndpoint("", "", "2001:0db8:0000:85a3:0000:0000:ac1f:8001", 9092)
            session = aiohttp.ClientSession()
            api = API(endpoint.conn_handler(session), )
            self.assertEqual(api.reverse_url("http", "/test/url"),
                             "http://[2001:0db8:0000:85a3:0000:0000:ac1f:8001]:9092/test/url")
            await session.close()

        self.loop.run_until_complete(go())

    def test_parse_error(self):
        error = parse_error("""{
"ucode": 1005,
"message": "Document has unkown fields or wrong line ending format"
}""")
        self.assertEqual(error["ucode"], 1005)
        self.assertEqual(error["message"], "Document has unkown fields or wrong line ending format")
