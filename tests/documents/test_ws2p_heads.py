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

from duniterpy.documents.ws2p.heads import HeadV0, HeadV1, HeadV2, BlockUID

headv1_clear = ""

headv1_tor = ""


class TestWS2PHeads(unittest.TestCase):
    def test_headv0(self):

        inline = "WS2P:HEAD:3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj:54813-00000A24802B33B71A91B6E990038C145A4815A45C71E57B2F2EF393183C7E2C"
        signature = "a1vAAM666kPsMCFTbkgkcCsqHf8nmXR+Lh3D3u+BaXzmArj7kwlItbdGUs4fc9QUG5Lp4TwPS7nhOM5t1Kt6CA=="

        headv0, _ = HeadV0.from_inline(inline, signature)

        self.assertEqual(headv0.api.public, "")
        self.assertEqual(headv0.api.private, "")
        self.assertEqual(headv0.head.version, 0)
        self.assertEqual(headv0.pubkey, "3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj")
        self.assertEqual(
            headv0.blockstamp,
            BlockUID.from_str(
                "54813-00000A24802B33B71A91B6E990038C145A4815A45C71E57B2F2EF393183C7E2C"
            ),
        )

        new_inline = headv0.inline()

        assert inline == new_inline

    def test_ws2p_headv1(self):
        inline = "WS2P:HEAD:1:HbTqJ1Ts3RhJ8Rx4XkNyh1oSKmoZL1kY5U7t9mKTSjAB:102131-0000066028B991BDFE3FF6DBA84EF519F76B62EA3787BC29D9A05557675B1F16:1152e46e:duniter:1.6.21-beta:1"
        signature = "ZGpT8HG4uX5Hc96gqhzIkkELVjGQKDp2/L+7BTFG5ODxGYWd2VX/H+hdZRqf0iUWRNuhxlequ68kkwMaE6ymBw=="
        headv1, _ = HeadV1.from_inline(inline, signature)

        self.assertEqual(headv1.head.version, 1)
        self.assertEqual(headv1.software, "duniter")
        self.assertEqual(headv1.software_version, "1.6.21-beta")
        self.assertEqual(headv1.pow_prefix, 1)

        new_inline = headv1.inline()

        assert inline == new_inline

    def test_ws2p_headv2(self):
        inline = "WS2POCA:HEAD:2:D3krfq6J9AmfpKnS3gQVYoy7NzGCc61vokteTS8LJ4YH:99393-0000017256006BFA979565F1280488D5831DD66054069E46A3EDEB1AECDBBF13:cb36b021:duniter:1.6.21:1:20:19"
        signature = "CgD1vaImPWZUCDFt5HDHUdjCTFcIwW5ndiCx6kXioFLZoz1a4WhCFYXvjI2N8+jEwQdWtf5+yNoHonqBSqirAQ=="
        headv2, _ = HeadV2.from_inline(inline, signature)
        self.assertEqual(headv2.api.public, "")
        self.assertEqual(headv2.api.private, "OCA")
        self.assertEqual(headv2.free_member_room, 20)
        self.assertEqual(headv2.free_mirror_room, 19)
        self.assertEqual(headv2.head.version, 2)

        new_inline = headv2.inline()

        assert inline == new_inline

        inline = "WS2POCAIC:HEAD:2:D3krfq6J9AmfpKnS3gQVYoy7NzGCc61vokteTS8LJ4YH:99393-0000017256006BFA979565F1280488D5831DD66054069E46A3EDEB1AECDBBF13:cb36b021:duniter:1.6.21:1:20:19"
        signature = "CgD1vaImPWZUCDFt5HDHUdjCTFcIwW5ndiCx6kXioFLZoz1a4WhCFYXvjI2N8+jEwQdWtf5+yNoHonqBSqirAQ=="

        headv2, _ = HeadV2.from_inline(inline, signature)
        self.assertEqual(headv2.api.public, "IC")
        self.assertEqual(headv2.api.private, "OCA")
        self.assertEqual(headv2.free_member_room, 20)
        self.assertEqual(headv2.free_mirror_room, 19)
        self.assertEqual(headv2.head.version, 2)

        new_inline = headv2.inline()

        assert inline == new_inline
