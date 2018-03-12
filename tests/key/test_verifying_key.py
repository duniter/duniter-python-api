from duniterpy.key import VerifyingKey, SigningKey, ScryptParams
from duniterpy.documents import Peer
from duniterpy.documents.ws2p.heads import *
import unittest


class TestVerifyingKey(unittest.TestCase):
    def test_from_sign_to_verify(self):
        sign_key = SigningKey("saltsalt", "passwordpassword", ScryptParams(4096, 16, 1))
        verify_key = VerifyingKey(sign_key.pubkey)
        self.assertEqual(verify_key.vk, sign_key.vk)

    def test_peer_signature(self):
        signed_raw = """Version: 2
Type: Peer
Currency: test_net
PublicKey: 8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU
Block: 2086-00005D6FC6E22FB308D8815A565A01C66FFB7DC761D616DE0698F6322565F1D6
Endpoints:
BASIC_MERKLED_API testnet.duniter.inso.ovh 80
4aQ/sfqFAFUeYkkLdC2OfgXqTBjCIcMptpR/GIlGqbe4aFVJcy9NEVAFx7sHiLuAb+VNnec3XHHC+xOk3MLzDA==
"""""
        peer = Peer.from_signed_raw(signed_raw)
        pubkey = "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU"
        verifying_key = VerifyingKey(pubkey)
        self.assertTrue(verifying_key.verify_document(peer))

    def test_ws2p_headv0(self):
        headv0, _ = HeadV0.from_inline("WS2P:HEAD:3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj:"
                                    "54813-00000A24802B33B71A91B6E990038C145A4815A45C71E57B2F2EF393183C7E2C",
                                    "a1vAAM666kPsMCFTbkgkcCsqHf8nmXR+Lh3D3u+BaXzmArj7kwlItbdGUs4fc9QUG5Lp4TwPS7nhOM5t1Kt6CA==")

        verifying_key = VerifyingKey(headv0.pubkey)
        self.assertTrue(verifying_key.verify_ws2p_head(headv0))

    def test_ws2p_headv1(self):
        headv1, _ = HeadV1.from_inline("WS2POCAIC:HEAD:1:HbTqJ1Ts3RhJ8Rx4XkNyh1oSKmoZL1kY5U7t9mKTSjAB:"
                                       "102131-0000066028B991BDFE3FF6DBA84EF519F76B62EA3787BC29D9A05557675B1F16:1152e46e:"
                                       "duniter:1.6.21:1",
                                       "ZGpT8HG4uX5Hc96gqhzIkkELVjGQKDp2/L+7BTFG5ODxGYWd2VX/H+hdZRqf0iUWRNuhxlequ68kkwMaE6ymBw==")

        verifying_key = VerifyingKey(headv1.pubkey)
        self.assertTrue(verifying_key.verify_ws2p_head(headv1))

    def test_ws2p_headv2(self):
        headv2, _ = HeadV2.from_inline("WS2POCA:HEAD:2:D3krfq6J9AmfpKnS3gQVYoy7NzGCc61vokteTS8LJ4YH:"
                                       "99393-0000017256006BFA979565F1280488D5831DD66054069E46A3EDEB1AECDBBF13:cb36b021:"
                                       "duniter:1.6.21:1:20:19",
                                       "CgD1vaImPWZUCDFt5HDHUdjCTFcIwW5ndiCx6kXioFLZoz1a4WhCFYXvjI2N8+jEwQdWtf5+yNoHonqBSqirAQ==")

        verifying_key = VerifyingKey(headv2.pubkey)
        self.assertTrue(verifying_key.verify_ws2p_head(headv2))
