from duniterpy.key import VerifyingKey, SigningKey
from duniterpy.documents import Peer
import unittest


class Test_VerifyingKey(unittest.TestCase):
    def test_from_sign_to_verify(self):
        sign_key = SigningKey("saltsalt", "passwordpassword")
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
