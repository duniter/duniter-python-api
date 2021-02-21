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
from duniterpy.documents.membership import Membership

membership_inline = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:\
dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==:\
0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:cgeek\n"

membership_raw = """Version: 2
Type: Membership
Currency: beta_brousouf
Issuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
Block: 0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709
Membership: IN
UserID: cgeek
CertTS: 0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709
dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==
"""


class TestMembership(unittest.TestCase):
    def test_frominline(self):
        membership = Membership.from_inline(2, "zeta_brousouf", "IN", membership_inline)
        self.assertEqual(
            membership.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
        )
        self.assertEqual(membership.membership_ts.number, 0)
        self.assertEqual(
            membership.membership_ts.sha_hash,
            "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709",
        )
        self.assertEqual(membership.identity_ts.number, 0)
        self.assertEqual(
            membership.identity_ts.sha_hash, "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709"
        )
        self.assertEqual(membership.uid, "cgeek")
        self.assertEqual(
            membership.signatures[0],
            "dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==",
        )
        self.assertEqual(membership.membership_type, "IN")

    def test_fromraw(self):
        membership = Membership.from_signed_raw(membership_raw)
        self.assertEqual(
            membership.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
        )
        self.assertEqual(membership.membership_ts.number, 0)
        self.assertEqual(
            membership.membership_ts.sha_hash,
            "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709",
        )
        self.assertEqual(membership.identity_ts.number, 0)
        self.assertEqual(
            membership.identity_ts.sha_hash, "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709"
        )
        self.assertEqual(membership.uid, "cgeek")
        self.assertEqual(
            membership.signatures[0],
            "dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==",
        )
        self.assertEqual(membership.membership_type, "IN")

    def test_fromraw_toraw(self):
        membership = Membership.from_signed_raw(membership_raw)
        rendered_membership = membership.signed_raw()
        from_rendered_membership = Membership.from_signed_raw(rendered_membership)
        self.assertEqual(
            from_rendered_membership.issuer,
            "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
        )
        self.assertEqual(from_rendered_membership.membership_ts.number, 0)
        self.assertEqual(
            from_rendered_membership.membership_ts.sha_hash,
            "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709",
        )
        self.assertEqual(membership.identity_ts.number, 0)
        self.assertEqual(
            membership.identity_ts.sha_hash, "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709"
        )
        self.assertEqual(from_rendered_membership.uid, "cgeek")
        self.assertEqual(
            from_rendered_membership.signatures[0],
            "dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==",
        )
        self.assertEqual(from_rendered_membership.membership_type, "IN")
