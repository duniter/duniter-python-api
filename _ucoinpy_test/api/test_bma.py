import unittest
from ucoinpy.api.bma import API
from ucoinpy.documents.peer import BMAEndpoint


class Test_BMA_API(unittest.TestCase):

    def test_reverse_url_complete(self):
        endpoint = BMAEndpoint("test.com", "124.2.2.1", "2001:0db8:0000:85a3:0000:0000:ac1f:8001 ", 9092)
        api = API(endpoint.conn_handler(), "any")
        self.assertEqual(api.reverse_url("/test/url"), "http://test.com:9092/any/test/url")

    def test_reverse_url_only_ipv4(self):
        endpoint = BMAEndpoint(None, "124.2.2.1", None, 9092)
        api = API(endpoint.conn_handler(), "any")
        self.assertEqual(api.reverse_url("/test/url"), "http://124.2.2.1:9092/any/test/url")

    def test_reverse_url_only_ipv6(self):
        endpoint = BMAEndpoint(None, None, "2001:0db8:0000:85a3:0000:0000:ac1f:8001", 9092)
        api = API(endpoint.conn_handler(), "any")
        self.assertEqual(api.reverse_url("/test/url"), "http://2001:0db8:0000:85a3:0000:0000:ac1f:8001:9092/any/test/url")
