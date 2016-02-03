import unittest
from _ucoinpy_test.api.webserver import WebFunctionalSetupMixin
from ucoinpy.api.bma.ws import Block, Peer


class Test_BMA_Websocket(WebFunctionalSetupMixin, unittest.TestCase):

    def test_block_014(self):
        json_sample = """
{
"documentType":"block",
"version":1,
"currency":"meta_brouzouf",
"nonce":567093,
"number":49191,
"parameters":"",
"previousHash":"0000084665ABA60118B6D302C9A9BA4BCCA94852",
"previousIssuer":"HBSSmqZjT4UQKsCntTSmZbu7iRP14HYtifLE6mW1PsBD",
"issuer":"HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
"identities":[],"joiners":[],"actives":[],"leavers":[],"excluded":[],
"membersCount":18,
"certifications":[],
"transactions":[],
"powMin":5,
"medianTime":1454058545,
"time":1454072945,
"signature":"Bk2lo/MAVgEwCr7pEopMs9DdN3TylwPH45MZg80h/V5IsuYwcVmPOstty6Z8XXqFCSfiCuYPUS7NhxGHOcnxDw==",
"hash":"0000011D7A92E746F9B2D5B7035B98867F4A95A2",
"fork":false,
"monetaryMass":15431388469457603000,
"dividend":0,
"UDTime":1453979780,
"wrong":false
}
"""
        block = Block(None)
        block.parse_text(json_sample)

    def test_peer(self):
        json_sample = """{
  "version": 1,
  "currency": "beta_brouzouf",
  "pubkey": "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY",
  "endpoints": [
    "BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:0db8:0000:85a3:0000:0000:ac1f 9001",
    "BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:0db8:0000:85a3:0000:0000:ac1f 9002",
    "OTHER_PROTOCOL 88.77.66.55 9001"
    ],
  "signature": "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r"
}
"""
        peer = Peer(None)
        data = peer.parse_text(json_sample)
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["currency"], "beta_brouzouf")
        self.assertEqual(data["pubkey"], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(len(data["endpoints"]), 3)
        self.assertEqual(data["signature"], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")
