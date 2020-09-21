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
            endpoint = BMAEndpoint(
                "test.com",
                "124.2.2.1",
                "2001:0db8:0000:85a3:0000:0000:ac1f:8001 ",
                9092,
            )
            session = aiohttp.ClientSession()
            api = API(endpoint.conn_handler(session))
            self.assertEqual(
                api.reverse_url("http", "/test/url"), "http://test.com:9092/test/url"
            )
            await session.close()

        self.loop.run_until_complete(go())

    def test_reverse_url_only_ipv4(self):
        async def go():
            endpoint = BMAEndpoint("", "124.2.2.1", "", 9092)
            session = aiohttp.ClientSession()

            api = API(endpoint.conn_handler(session))
            self.assertEqual(
                api.reverse_url("http", "/test/url"), "http://124.2.2.1:9092/test/url"
            )
            await session.close()

        self.loop.run_until_complete(go())

    def test_reverse_url_only_ipv6(self):
        async def go():
            endpoint = BMAEndpoint(
                "", "", "2001:0db8:0000:85a3:0000:0000:ac1f:8001", 9092
            )
            session = aiohttp.ClientSession()
            api = API(endpoint.conn_handler(session))
            self.assertEqual(
                api.reverse_url("http", "/test/url"),
                "http://[2001:0db8:0000:85a3:0000:0000:ac1f:8001]:9092/test/url",
            )
            await session.close()

        self.loop.run_until_complete(go())

    def test_parse_error(self):
        error = parse_error(
            """{
"ucode": 1005,
"message": "Document has unkown fields or wrong line ending format"
}"""
        )
        self.assertEqual(error["ucode"], 1005)
        self.assertEqual(
            error["message"], "Document has unkown fields or wrong line ending format"
        )
