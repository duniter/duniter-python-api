"""
Copyright  2014-2021 Vincent Texier <vit@free.fr>

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

from duniterpy.api.client import API, parse_error
from duniterpy.api.endpoint import BMAEndpoint, SecuredBMAEndpoint, GVAEndpoint


class TestBmaApi(unittest.TestCase):
    def test_reverse_url_complete(self):
        endpoint = BMAEndpoint(
            "test.com",
            "124.2.2.1",
            "2001:0db8:0000:85a3:0000:0000:ac1f:8001 ",
            9092,
        )
        api = API(endpoint.conn_handler())
        self.assertEqual(
            api.reverse_url("http", "/test/url"), "http://test.com:9092/test/url"
        )

    def test_reverse_url_complete_bmas(self):
        endpoint = SecuredBMAEndpoint(
            "test.com",
            "124.2.2.1",
            "2001:0db8:0000:85a3:0000:0000:ac1f:8001 ",
            9092,
            "api_path",
        )
        api = API(endpoint.conn_handler())
        self.assertEqual(
            api.reverse_url("http", "/test/url"),
            "http://test.com:9092/api_path/test/url",
        )

    def test_reverse_url_complete_gva(self):
        endpoint = GVAEndpoint(
            "S",
            "test.com",
            "124.2.2.1",
            "2001:0db8:0000:85a3:0000:0000:ac1f:8001 ",
            9092,
            "gva",
        )
        api = API(endpoint.conn_handler())
        self.assertEqual(api.reverse_url("https", ""), "https://test.com:9092/gva")

    def test_reverse_url_only_ipv4(self):
        endpoint = BMAEndpoint("", "124.2.2.1", "", 9092)

        api = API(endpoint.conn_handler())
        self.assertEqual(
            api.reverse_url("http", "/test/url"), "http://124.2.2.1:9092/test/url"
        )

    def test_reverse_url_only_ipv6(self):
        endpoint = BMAEndpoint("", "", "2001:0db8:0000:85a3:0000:0000:ac1f:8001", 9092)
        api = API(endpoint.conn_handler())
        self.assertEqual(
            api.reverse_url("http", "/test/url"),
            "http://[2001:0db8:0000:85a3:0000:0000:ac1f:8001]:9092/test/url",
        )

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
