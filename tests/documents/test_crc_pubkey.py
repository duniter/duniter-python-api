import unittest
from duniterpy.documents.crc_pubkey import CRCPubkey


class Test_CRCPubkey(unittest.TestCase):
    def test_from_pubkey(self):
        crc_pubkey = CRCPubkey.from_pubkey("J4c8CARmP9vAFNGtHRuzx14zvxojyRWHW2darguVqjtX")
        self.assertEqual(crc_pubkey.crc, "KAv")
