'''
Created on 12 déc. 2014

@author: inso
'''
import unittest
from ucoinpy.documents.membership import Membership

membership_inline = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:\
dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==:\
0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1416335620:cgeek\n"

membership_raw = """Version: 1
Type: Membership
Currency: beta_brousouf
Issuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
Block: 0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709
Membership: IN
UserID: cgeek
CertTS: 1416335620
dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==
"""


class Test_Membership(unittest.TestCase):
    def test_frominline(self):
        membership = Membership.from_inline(1, "zeta_brousouf", 'IN', membership_inline)
        self.assertEquals(membership.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEquals(membership.block_number, 0)
        self.assertEquals(membership.block_hash, "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709")
        self.assertEquals(membership.cert_ts, 1416335620)
        self.assertEquals(membership.uid, "cgeek")
        self.assertEquals(membership.signatures[0], "dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==")
        self.assertEquals(membership.membership_type, 'IN')

    def test_fromraw(self):
        membership = Membership.from_signed_raw(membership_raw)
        self.assertEquals(membership.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEquals(membership.block_number, 0)
        self.assertEquals(membership.block_hash, "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709")
        self.assertEquals(membership.cert_ts, 1416335620)
        self.assertEquals(membership.uid, "cgeek")
        self.assertEquals(membership.signatures[0], "dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==")
        self.assertEquals(membership.membership_type, 'IN')

    def test_fromraw_toraw(self):
        membership = Membership.from_signed_raw(membership_raw)
        rendered_membership = membership.signed_raw()
        from_rendered_membership = Membership.from_signed_raw(rendered_membership)
        self.assertEquals(from_rendered_membership.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEquals(from_rendered_membership.block_number, 0)
        self.assertEquals(from_rendered_membership.block_hash, "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709")
        self.assertEquals(from_rendered_membership.cert_ts, 1416335620)
        self.assertEquals(from_rendered_membership.uid, "cgeek")
        self.assertEquals(from_rendered_membership.signatures[0], "dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==")
        self.assertEquals(from_rendered_membership.membership_type, 'IN')


