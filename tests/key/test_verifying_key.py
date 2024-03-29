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

from duniterpy.key import VerifyingKey, SigningKey
from duniterpy.key.scrypt_params import ScryptParams
from duniterpy.documents.peer import Peer
from duniterpy.documents.ws2p.heads import HeadV0, HeadV1, HeadV2
from duniterpy.documents import Block
from duniterpy.documents.transaction import Transaction
import unittest


class TestVerifyingKey(unittest.TestCase):
    def test_from_sign_to_verify(self):
        sign_key = SigningKey.from_credentials("alice", "password", ScryptParams())
        verify_key = VerifyingKey(sign_key.pubkey)
        self.assertEqual(verify_key.vk, sign_key.vk)

    def test_get_verified_data(self):
        sign_key = SigningKey.from_credentials("alice", "password", ScryptParams())

        message = "Hello world with utf-8 chars like éàè !"
        # Sign the message, the signed string is the message itself plus the
        # signature
        signed_message = sign_key.sign(bytes(message, "utf-8"))  # type: bytes

        # Verify the message!
        verifier = VerifyingKey(sign_key.pubkey)
        verified_message = verifier.get_verified_data(signed_message)
        self.assertEqual(message, verified_message.decode("utf-8"))

    def test_peer_signature(self):
        signed_raw = """Version: 2
Type: Peer
Currency: test_net
PublicKey: 8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU
Block: 2086-00005D6FC6E22FB308D8815A565A01C66FFB7DC761D616DE0698F6322565F1D6
Endpoints:
BASIC_MERKLED_API testnet.duniter.inso.ovh 80
4aQ/sfqFAFUeYkkLdC2OfgXqTBjCIcMptpR/GIlGqbe4aFVJcy9NEVAFx7sHiLuAb+VNnec3XHHC+xOk3MLzDA==
"""
        peer = Peer.from_signed_raw(signed_raw)
        pubkey = "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU"
        verifying_key = VerifyingKey(pubkey)
        self.assertTrue(verifying_key.verify_document(peer))

    def test_ws2p_headv0(self):
        headv0, _ = HeadV0.from_inline(
            "WS2P:HEAD:3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj:"
            "54813-00000A24802B33B71A91B6E990038C145A4815A45C71E57B2F2EF393183C7E2C",
            "a1vAAM666kPsMCFTbkgkcCsqHf8nmXR+Lh3D3u"
            "+BaXzmArj7kwlItbdGUs4fc9QUG5Lp4TwPS7nhOM5t1Kt6CA==",
        )

        verifying_key = VerifyingKey(headv0.pubkey)
        self.assertTrue(verifying_key.verify_ws2p_head(headv0))

    def test_ws2p_headv1(self):
        headv1, _ = HeadV1.from_inline(
            "WS2POCAIC:HEAD:1:HbTqJ1Ts3RhJ8Rx4XkNyh1oSKmoZL1kY5U7t9mKTSjAB:"
            "102131-0000066028B991BDFE3FF6DBA84EF519F76B62EA3787BC29D9A05557675B1F16"
            ":1152e46e:duniter:1.6.21:1",
            "ZGpT8HG4uX5Hc96gqhzIkkELVjGQKDp2/L+7BTFG5ODxGYWd2VX/H"
            "+hdZRqf0iUWRNuhxlequ68kkwMaE6ymBw==",
        )

        verifying_key = VerifyingKey(headv1.pubkey)
        self.assertTrue(verifying_key.verify_ws2p_head(headv1))

    def test_ws2p_headv2(self):
        headv2, _ = HeadV2.from_inline(
            "WS2POCA:HEAD:2:D3krfq6J9AmfpKnS3gQVYoy7NzGCc61vokteTS8LJ4YH:"
            "99393-0000017256006BFA979565F1280488D5831DD66054069E46A3EDEB1AECDBBF13"
            ":cb36b021:duniter:1.6.21:1:20:19",
            "CgD1vaImPWZUCDFt5HDHUdjCTFcIwW5ndiCx6kXioFLZoz1a4WhCFYXvjI2N8+jEwQdWtf5"
            "+yNoHonqBSqirAQ==",
        )

        verifying_key = VerifyingKey(headv2.pubkey)
        self.assertTrue(verifying_key.verify_ws2p_head(headv2))

    def test_block_document(self):
        block_document = """Version: 10
Type: Block
Currency: g1
Number: 15145
PoWMin: 80
Time: 1493684276
MedianTime: 1493681245
UnitBase: 0
Issuer: 6fFt4zdvtNyVcfJn7Y41mKLmMDizyK3nVeNW3qdDXzpc
IssuersFrame: 106
IssuersFrameVar: 0
DifferentIssuersCount: 21
PreviousHash: 00000A0CE0AE54F3F6B63383F386067160C477B5338FB93AF3AF0776A959AA32
PreviousIssuer: D9D2zaJoWYWveii1JRYLVK3J4Z7ZH3QczoKrnQeiM6mx
MembersCount: 98
Identities:
Joiners:
Actives:
Leavers:
Revoked:
Excluded:
Certifications:
Transactions:
InnerHash: AA01ABD5C6D3F99A189C0CF0E37768DA0F876526AF93FE150E92B135D4AD0D85
Nonce: 10300000099432
"""
        block_signature = "Uxa3L+/m/dWLex2xSh7Jv1beAn4f99BmoYAs7iX3Lr+t1l5jzJpd9m4iI1cHppIizCgbg6ztaiZedQ+Mp6KuDg=="
        block = Block.from_signed_raw(block_document + block_signature + "\n")
        verifying_key = VerifyingKey(block.issuer)
        self.assertTrue(verifying_key.verify_document(block))

    def test_transaction_document(self):
        transaction_document = """TX:10:1:6:6:2:1:0
278644-000004546FCB16F2851A8B6D1066219B0EBB3580C882850411618E35241719EA
8rYgYd64F2Y3Gfxwohjrc7K3zSNpDz79yNxRJorUwmse
1011:0:D:8rYgYd64F2Y3Gfxwohjrc7K3zSNpDz79yNxRJorUwmse:278052
1011:0:D:8rYgYd64F2Y3Gfxwohjrc7K3zSNpDz79yNxRJorUwmse:278333
1011:0:D:8rYgYd64F2Y3Gfxwohjrc7K3zSNpDz79yNxRJorUwmse:278609
1011:0:T:4116D06975AE613C96183390FC5A2BE2561F36C86F5CFE69EB23E3B517AA6F17:1
20330:0:T:56D8A0ACE3BC7E1173FF8BFB8A97A2F3353B6F3AEBCF4923C8BE2E81FDCC0685:1
11121:0:T:7CC29A8707D72936ED0EB9C618CEB3278DFAB4647B6639AA09620FA31EAD95D8:1
0:SIG(0)
1:SIG(0)
2:SIG(0)
3:SIG(0)
4:SIG(0)
5:SIG(0)
30000:0:SIG(2mKmto464oWCVsRgcYM6vpwsLsGk6MhMtrBKf7DTAU34)
5495:0:SIG(8rYgYd64F2Y3Gfxwohjrc7K3zSNpDz79yNxRJorUwmse)
Solde huile Millepertuis
rgjOmzFH5h+hkDbJLk1b88X7Z83HMgTa5rBckeMSdF/yZtItN3zMn09MphcXjffdrKcK+MebwoisLJqV+jXrDg==
"""
        tx = Transaction.from_compact("g1", transaction_document)
        verifying_key = VerifyingKey(tx.issuers[0])
        self.assertTrue(verifying_key.verify_document(tx))
