import unittest
from duniterpy.api.bma import API, parse_error
from duniterpy.documents.peer import BMAEndpoint


class Test_BMA_API(unittest.TestCase):

    def test_reverse_url_complete(self):
        endpoint = BMAEndpoint("test.com", "124.2.2.1", "2001:0db8:0000:85a3:0000:0000:ac1f:8001 ", 9092)
        api = API(next(endpoint.conn_handler()), "any")
        self.assertEqual(api.reverse_url("http", "/test/url"), "http://test.com:9092/any/test/url")

    def test_reverse_url_only_ipv4(self):
        endpoint = BMAEndpoint(None, "124.2.2.1", None, 9092)
        api = API(next(endpoint.conn_handler()), "any")
        self.assertEqual(api.reverse_url("http", "/test/url"), "http://124.2.2.1:9092/any/test/url")

    def test_reverse_url_only_ipv6(self):
        endpoint = BMAEndpoint(None, None, "2001:0db8:0000:85a3:0000:0000:ac1f:8001", 9092)
        api = API(next(endpoint.conn_handler()), "any")
        self.assertEqual(api.reverse_url("http", "/test/url"), "http://[2001:0db8:0000:85a3:0000:0000:ac1f:8001]:9092/any/test/url")

    def test_parse_error(self):
        api = API(None, "any")
        error = parse_error("""{
"ucode": 1005,
"message": "Document has unkown fields or wrong line ending format"
}""")
        self.assertEqual(error["ucode"], 1005)
        self.assertEqual(error["message"], "Document has unkown fields or wrong line ending format")
