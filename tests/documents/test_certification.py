'''
Created on 6 déc. 2014

@author: inso
'''

import unittest
from duniterpy.documents.certification import SelfCertification, Certification, Revokation
from duniterpy.documents import Block, BlockUID

selfcert_inlines = ["HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:\
h/H8tDIEbfA4yxMQcvfOXVDQhi1sUa9qYtPKrM59Bulv97ouwbAvAsEkC1Uyit1IOpeAV+CQQs4IaAyjE8F1Cw==:\
32-DB30D958EE5CB75186972286ED3F4686B8A1C2CD:lolcat\n", "RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS:\
Ah55O8cvdkGS4at6AGOKUjy+wrFwAq8iKRJ5xLIb6Xdi3M8WfGOUdMjwZA6GlSkdtlMgEhQPm+r2PMebxKrCBg==:\
36-1076F10A7397715D2BEE82579861999EA1F274AC:lolmouse\n" ]


cert_inlines = [
"8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:\
0:TgmDuMxZdyutroj9jiLJA8tQp/389JIzDKuxW5+h7GIfjDu1ZbwI7HNm5rlUDhR2KreaV/QJjEaItT4Cf75rCQ==\n",
"9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:12:\
qn/XNJjaGIwfnR+wGrDME6YviCQbG+ywsQWnETlAsL6q7o3k1UhpR5ZTVY9dvejLKuC+1mUEXVTmH+8Ib55DBA==\n"
]

revokation_inline = "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:\
TgmDuMxZdyutroj9jiLJA8tQp/389JIzDKuxW5+h7GIfjDu1ZbwI7HNm5rlUDhR2KreaV/QJjEaItT4Cf75rCQ==\n"


class Test_Certification(unittest.TestCase):

    def test_self_certification_from_inline(self):
        version = 2
        currency = "beta_brousouf"
        selfcert = SelfCertification.from_inline(version, currency, selfcert_inlines[0])
        self.assertEqual(selfcert.pubkey, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(selfcert.signatures[0], "h/H8tDIEbfA4yxMQcvfOXVDQhi1sUa9qYtPKrM59Bulv97ouwbAvAsEkC1Uyit1IOpeAV+CQQs4IaAyjE8F1Cw==")
        self.assertEqual(str(selfcert.timestamp), "32-DB30D958EE5CB75186972286ED3F4686B8A1C2CD")
        self.assertEqual(selfcert.uid, "lolcat")

        selfcert = SelfCertification.from_inline(version, currency, selfcert_inlines[1])
        self.assertEqual(selfcert.pubkey, "RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS")
        self.assertEqual(selfcert.signatures[0], "Ah55O8cvdkGS4at6AGOKUjy+wrFwAq8iKRJ5xLIb6Xdi3M8WfGOUdMjwZA6GlSkdtlMgEhQPm+r2PMebxKrCBg==")
        self.assertEqual(str(selfcert.timestamp), "36-1076F10A7397715D2BEE82579861999EA1F274AC")
        self.assertEqual(selfcert.uid, "lolmouse")

    def test_raw_self_certification(self):
        version = 2
        currency = "beta_brousouf"
        issuer = "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd"
        uid = "lolcat"
        timestamp = BlockUID(32, "DB30D958EE5CB75186972286ED3F4686B8A1C2CD")
        signature = "J3G9oM5AKYZNLAB5Wx499w61NuUoS57JVccTShUbGpCMjCqj9yXXqNq7dyZpDWA6BxipsiaMZhujMeBfCznzyci"

        selfcert = SelfCertification(version, currency, issuer, uid, timestamp, signature)

        result = """Version: 2
Type: Identity
Currency: beta_brousouf
Issuer: HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd
UniqueID: lolcat
Timestamp: 32-DB30D958EE5CB75186972286ED3F4686B8A1C2CD
J3G9oM5AKYZNLAB5Wx499w61NuUoS57JVccTShUbGpCMjCqj9yXXqNq7dyZpDWA6BxipsiaMZhujMeBfCznzyci
"""
        self.assertEqual(selfcert.signed_raw(), result)

    def test_certifications_from_inline(self):
        version = 2
        currency = "zeta_brousouf"
        cert = Certification.from_inline(version, currency, None, cert_inlines[0])
        self.assertEqual(cert.pubkey_from, "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU")
        self.assertEqual(cert.pubkey_to, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(cert.timestamp.number, 0)
        self.assertEqual(cert.timestamp.sha_hash, Block.Empty_Hash)
        self.assertEqual(cert.signatures[0], "TgmDuMxZdyutroj9jiLJA8tQp/389JIzDKuxW5+h7GIfjDu1ZbwI7HNm5rlUDhR2KreaV/QJjEaItT4Cf75rCQ==")

        cert = Certification.from_inline(version, currency, "DB30D958EE5CB75186972286ED3F4686B8A1C2CD", cert_inlines[1])
        self.assertEqual(cert.pubkey_from, "9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y")
        self.assertEqual(cert.pubkey_to, "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU")
        self.assertEqual(cert.timestamp.number, 12)
        self.assertEqual(cert.timestamp.sha_hash, "DB30D958EE5CB75186972286ED3F4686B8A1C2CD")
        self.assertEqual(cert.signatures[0], "qn/XNJjaGIwfnR+wGrDME6YviCQbG+ywsQWnETlAsL6q7o3k1UhpR5ZTVY9dvejLKuC+1mUEXVTmH+8Ib55DBA==")

    def test_certification_raw(self):
        version = 2
        currency = "beta_brousouf"
        pubkey_from = "DNann1Lh55eZMEDXeYt59bzHbA3NJR46DeQYCS2qQdLV"
        pubkey_to = "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd"
        timestamp = BlockUID(36, "1076F10A7397715D2BEE82579861999EA1F274AC")
        signature = "SoKwoa8PFfCDJWZ6dNCv7XstezHcc2BbKiJgVDXv82R5zYR83nis9dShLgWJ5w48noVUHimdngzYQneNYSMV3rk"
        selfcert = SelfCertification(version, currency, pubkey_to, "lolcat",
                                     BlockUID(32, "DB30D958EE5CB75186972286ED3F4686B8A1C2CD"),
                                     "J3G9oM5AKYZNLAB5Wx499w61NuUoS57JVccTShUbGpCMjCqj9yXXqNq7dyZpDWA6BxipsiaMZhujMeBfCznzyci")

        certification = Certification(version, currency, pubkey_from, pubkey_to, timestamp, signature)

        result = """Version: 2
Type: Certification
Currency: beta_brousouf
Issuer: DNann1Lh55eZMEDXeYt59bzHbA3NJR46DeQYCS2qQdLV
IdtyIssuer: HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd
IdtyUniqueID: lolcat
IdtyTimestamp: 32-DB30D958EE5CB75186972286ED3F4686B8A1C2CD
IdtySignature: J3G9oM5AKYZNLAB5Wx499w61NuUoS57JVccTShUbGpCMjCqj9yXXqNq7dyZpDWA6BxipsiaMZhujMeBfCznzyci
CertTimestamp: 36-1076F10A7397715D2BEE82579861999EA1F274AC
SoKwoa8PFfCDJWZ6dNCv7XstezHcc2BbKiJgVDXv82R5zYR83nis9dShLgWJ5w48noVUHimdngzYQneNYSMV3rk
"""
        self.assertEqual(certification.signed_raw(selfcert), result)



    def test_revokation_from_inline(self):
        version = 2
        currency = "zeta_brousouf"
        revokation = Revokation.from_inline(version, currency, revokation_inline)
        self.assertEqual(revokation.pubkey, "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU")
        self.assertEqual(revokation.signatures[0], "TgmDuMxZdyutroj9jiLJA8tQp/389JIzDKuxW5+h7GIfjDu1ZbwI7HNm5rlUDhR2KreaV/QJjEaItT4Cf75rCQ==")

    def test_revokation_raw(self):

        version = 2
        currency = "beta_brousouf"
        pubkey = "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd"
        signature = "SoKwoa8PFfCDJWZ6dNCv7XstezHcc2BbKiJgVDXv82R5zYR83nis9dShLgWJ5w48noVUHimdngzYQneNYSMV3rk"
        revokation = Revokation(version, currency, pubkey, signature)
        selfcert = SelfCertification(version, currency, pubkey, "lolcat",
                                     BlockUID(32, "DB30D958EE5CB75186972286ED3F4686B8A1C2CD"),
                                     "J3G9oM5AKYZNLAB5Wx499w61NuUoS57JVccTShUbGpCMjCqj9yXXqNq7dyZpDWA6BxipsiaMZhujMeBfCznzyci")

        result = """Version: 2
Type: Revocation
Currency: beta_brousouf
Issuer: HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd
IdtyUniqueID: lolcat
IdtyTimestamp: 32-DB30D958EE5CB75186972286ED3F4686B8A1C2CD
IdtySignature: J3G9oM5AKYZNLAB5Wx499w61NuUoS57JVccTShUbGpCMjCqj9yXXqNq7dyZpDWA6BxipsiaMZhujMeBfCznzyci
SoKwoa8PFfCDJWZ6dNCv7XstezHcc2BbKiJgVDXv82R5zYR83nis9dShLgWJ5w48noVUHimdngzYQneNYSMV3rk
"""
        self.assertEqual(revokation.signed_raw(selfcert), result)