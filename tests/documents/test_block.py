'''
Created on 12 déc. 2014

@author: inso
'''
import unittest
from duniterpy.documents.block import Block, BlockUID

raw_block = """Version: 2
Type: Block
Currency: zeta_brouzouf
Number: 15
PoWMin: 4
Time: 1418083330
MedianTime: 1418080208
Issuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
PreviousHash: 0000E73C340601ACA1AD5AAA5B5E56B03E178EF8
PreviousIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
MembersCount: 4
Identities:
Joiners:
Actives:
Leavers:
Revoked:
Excluded:
Certifications:
Transactions:
InnerHash: DB30D958EE5CB75186972286ED3F4686B8A1C2CD
Nonce: 45079
42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r
"""

raw_block_with_tx = """Version: 2
Type: Block
Currency: meta_brouzouf
Number: 34436
PoWMin: 5
Time: 1443896211
MedianTime: 1443881811
Issuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
PreviousHash: 000002B06C990DEBD5C1D947289C2CF4F4396FB2
PreviousIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
MembersCount: 19
Identities:
Joiners:
Actives:
ATkjQPa4sn4LBF69jqEPzFtRdHYJs6MJQjvP8JdN7MtN:QTowsupV+uXrcomL44WCxbu3LQoJM2C2VPMet5Xg6gXGAHEtGRp47FfQLb2ok1+/588JiIHskCyazj3UOsmKDw==:34434-00000D21F80687248A8C02F16BB19A975B4F983D:34432-00000D21F80687248A8C02F16BB19A975B4F983D:urodelus
Leavers:
Revoked:
Excluded:
Certifications:
5ocqzyDMMWf1V8bsoNhWb1iNwax1e9M7VTUN6navs8of:ATkjQPa4sn4LBF69jqEPzFtRdHYJs6MJQjvP8JdN7MtN:0:6TuxRcARnpo13l3cXtgPTkjJlv8DZOUvsAzmZJMbjHZbbZfDQ6MJpH9DIuH0eyG3WGc0EX/046mbMGBrKKg9DQ==
ATkjQPa4sn4LBF69jqEPzFtRdHYJs6MJQjvP8JdN7MtN:2qwGeLWoPG7db72bKXPfJpAtj67FYDnPaJn2JB7tyXxJ:0:LusTbb7CgwrqqacDKjtldw60swwvDBH8wVUIJN4SWRb2pZPJSpDxgqaGyjC5P9i/DendfyQWc7cfzPDqSZmZAg==
Transactions:
TX:2:1:3:3:1:0:0
HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY
T:6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3:0
T:3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435:10
D:HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY:88
0:SIG(0)
1:SIG(0)
2:SIG(0)
30:2:SIG(BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g)
42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r
TX:2:3:6:6:3:1:0
HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY
CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp
9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB
T:6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3:2
T:3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435:8
D:HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY:46
T:A0D9B4CDC113ECE1145C5525873821398890AE842F4B318BD076095A23E70956:3
T:67F2045B5318777CC52CD38B424F3E40DDA823FA0364625F124BABE0030E7B5B:5
D:9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB:46
0:SIG(0)
1:XHX(7665798292)
2:SIG(0)
3:SIG(0) SIG(2)
4:SIG(0) SIG(1) SIG(2)
5:SIG(2)
120:2:SIG(BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g)
146:2:SIG(DSz4rgncXCytsUMW2JU2yhLquZECD2XpEkpP9gG5HyAx)
49:2:(SIG(6DyGr5LFtFmbaJYRvcs9WmBsr4cbJbJ1EV9zBbqG7A6i) OR XHX(3EB4702F2AC2FD3FA4FDC46A4FC05AE8CDEE1A85))
-----@@@----- (why not this comment?)
42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r
2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX
2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk
InnerHash: DB30D958EE5CB75186972286ED3F4686B8A1C2CD
Nonce: 581
nY/MsFU2luiohLmSiOOimL1RIqbriOBgc22ua03Z2dhxtSJxKZeGNGDvl1jaXgmEBRnXU87yXbZ7ioOS/AAVCA==
"""


raw_block_zero = """Version: 2
Type: Block
Currency: zeta_brouzouf
Number: 0
PoWMin: 3
Time: 1418077277
MedianTime: 1418077277
Issuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
Parameters: 0.007376575:300:10:0:40:1209600:31536000:0:0.9:31536000:3:20:60:10:20:0.66
MembersCount: 4
Identities:
HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:h/H8tDIEbfA4yxMQcvfOXVDQhi1sUa9qYtPKrM59Bulv97ouwbAvAsEkC1Uyit1IOpeAV+CQQs4IaAyjE8F1Cw==:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:cgeek
8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:lAW4mCPqA3cnEubHAGpMXR0o8euEdDVeSLplRgdLPf8Bty7R7FqVqwoAlL/4q/7p3O57Cz9z3mvhRSNwt23qBw==:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:inso
RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS:Ah55O8cvdkGS4at6AGOKUjy+wrFwAq8iKRJ5xLIb6Xdi3M8WfGOUdMjwZA6GlSkdtlMgEhQPm+r2PMebxKrCBg==:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:vit
9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y:ZjlNz2k/7Y38xwzaVEtyteOD12ukRT+x8NBFVTrcZtUHSJdqt7ejBAC0ULu7eCTLlmJk0jS6cuJ3IeVTLfFRDg==:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:ManUtopiK
Joiners:
HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:cgeek
8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:43FEO5wwKzo79k+WmZsrUDsNNceStYkrweEntwYGoGn9+YNjyyCbMmKcEU38xzMV2M0ZMgjvlTK30/vWwrD5CQ==:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:inso
RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS:zPg1kgjVstsaKDBq3Re6Z84hlw0Ja2pjJEORmn7w5ifT6/e45BnEPJaqoVgImzSnytjOpzXN/rhAO4+UDJOUBQ==:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:vit
9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y:ox/t5um2bbFJfc6NdRDM8DniGxlRB5zmKuW7WK+MiDpE32GUhf/tDcyfBkIpwIFcaY0hqLYW1OQlgbm2qT6xAw==:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:ManUtopiK
Actives:
Leavers:
Revoked:
Excluded:
Certifications:
8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:TgmDuMxZdyutroj9jiLJA8tQp/389JIzDKuxW5+h7GIfjDu1ZbwI7HNm5rlUDhR2KreaV/QJjEaItT4Cf75rCQ==
RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:xvIlhFdTUwqWx7XIG980xatL0JULOj1Ex15Q9nDcDLVtyFXZZCp1ZeRewkGjkJoGyOFGCJ1iDSB/qFzsPtrsDQ==
9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:mNsbLvezg8Zx1NPfs2gdGwmCKtoVWbw64yEHZE7uPkDvF+iexk93O8IT06HKgo1VI5SennwDfh0qp3Ko1OB5BQ==
HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:wIdLq6EYKSLoVXcXoSMLciBPMvJvvP1t5cTCIrvPH4qvo/y02al6vFfQR+wUGwFtoXulUSr8C+U1FRHWfUTCBg==
RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:Gr4EHqCEt+uuLbGPdu1qT/YObkqVthVzmFWCBlKRnRUz3xUt828W25GRtvdVn8hlycvCX/05mMlWeRMBUI/LDA==
9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:qn/XNJjaGIwfnR+wGrDME6YviCQbG+ywsQWnETlAsL6q7o3k1UhpR5ZTVY9dvejLKuC+1mUEXVTmH+8Ib55DBA==
HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS:0:QLaYgLndAqRIk2uRAuxxhNUEQtSLpPqpfKvGBfClpQV0y7YTm1GnEoX9bY3DPhXU8GjUThngkFR0+M4Fx5R6DQ==
8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS:0:T+MkH18Eyddq5o93v2tSyBMd/RSkL/mcnE017t/t11QrMmFrXFZeufUhkVfRPi89kLSap4sLV/weEETXX8S7Aw==
9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y:RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS:0:mWARDngVFmw76JPmHRZHUOh1MFjddNyJ3OMPQHMERFdeev1hKQ3pEUY9lQc6BL524GjIOcvLWufo65Ie0XTDCQ==
8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y:0:4vLU/VUE5VxcMnvv4mtJs9bky45o2fddKZCnP0FVGZD3BHC20YMPabTZ2RWcNiCc97zig1Munqj2Ss5RQMBDBA==
RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS:9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y:0:90w2HrbdsKIc6YJq3Ksa4sSgjpYSMM05+UuowAlYjrk1ixHIyWyg5odyZPRwO50aiIyUsbikoOWsMc3G8ob/Cg==
HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y:0:28lv0p8EPHpVgAMiPvXvIe5lMvYJxwko2tv5bPO4voHRHSaDcTz5BR7Oe69S6wjANIEAMfebXiFMqZdj+mWRAA==
Transactions:
InnerHash: DB30D958EE5CB75186972286ED3F4686B8A1C2CD
Nonce: 2125
42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r
"""


raw_block_with_leavers = """Version: 2
Type: Block
Currency: meta_brouzouf
Number: 34895
PoWMin: 4
Time: 1444434128
MedianTime: 1444426438
Issuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
PreviousHash: 0000E88115ADDF79344372C0212928501E21622B
PreviousIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
MembersCount: 21
Identities:
Joiners:
Actives:
Leavers:
2sq8bBDQGK74f1eD3mAPQVgHCmFdijZr9nbv16FwbokX:4MsVEpiL5YXQ0w8KgkbeKR73Y/aSLtQS5HxPFoQJuG5pt+Zl0Q2dLCQfmfvePW4/ANLzcOGnZJH2Tgsw5inJDw==:34893-0000CC15C495623FFAF370D87A7E025FCF01D0AF:0-DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:smoul
Revoked:
Excluded:
Certifications:
Transactions:
InnerHash: DB30D958EE5CB75186972286ED3F4686B8A1C2CD
Nonce: 9906
5LZCFSnm5FkFihPBTpmsPyILEdvu8MXfJOp6OR4d1s+/e2jVWg4J6YSDfO2KBBPgubASyr2QwQuiBlYD2918Bw==
"""


class Test_Block(unittest.TestCase):
    def test_fromraw(self):
        block = Block.from_signed_raw(raw_block)
        self.assertEqual(block.version, 2)
        self.assertEqual(block.currency, "zeta_brouzouf")
        self.assertEqual(block.noonce, 45079)
        self.assertEqual(block.number, 15)
        self.assertEqual(block.powmin, 4)
        self.assertEqual(block.time, 1418083330)
        self.assertEqual(block.mediantime, 1418080208)
        self.assertEqual(block.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(block.prev_hash, "0000E73C340601ACA1AD5AAA5B5E56B03E178EF8")
        self.assertEqual(block.prev_issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(block.members_count, 4)
        self.assertEqual(block.identities, [])
        self.assertEqual(block.joiners, [])
        self.assertEqual(block.actives, [])
        self.assertEqual(block.leavers, [])
        self.assertEqual(block.excluded, [])
        self.assertEqual(block.certifications, [])
        self.assertEqual(block.transactions, [])

    def test_from_signed_raw_block_zero(self):
        block = Block.from_signed_raw(raw_block_zero)
        self.assertEqual(block.version, 2)
        self.assertEqual(block.currency, "zeta_brouzouf")
        self.assertEqual(block.noonce, 2125)
        self.assertEqual(block.number, 0)
        self.assertEqual(block.powmin, 3)
        self.assertEqual(block.time, 1418077277)
        self.assertEqual(block.mediantime, 1418077277)
        self.assertEqual(block.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(block.parameters, ("0.007376575",
                                            "300","10","0","40","1209600","31536000","0","0.9","31536000",
                                            "3","20","60","10","20","0.66"))
        self.assertEqual(block.members_count, 4)
        self.assertEqual(len(block.identities), 4)
        self.assertEqual(len(block.joiners), 4)
        self.assertEqual(block.actives, [])
        self.assertEqual(block.leavers, [])
        self.assertEqual(block.excluded, [])
        self.assertEqual(len(block.certifications), 12)
        self.assertEqual(block.transactions, [])

        self.assertEqual(block.signed_raw(), raw_block_zero)

    def test_toraw_fromsignedraw(self):
        block = Block.from_signed_raw(raw_block)
        rendered_raw = block.signed_raw()
        from_rendered_raw = Block.from_signed_raw(rendered_raw)

        self.assertEqual(from_rendered_raw.version, 2)
        self.assertEqual(from_rendered_raw.currency, "zeta_brouzouf")
        self.assertEqual(from_rendered_raw.noonce, 45079)
        self.assertEqual(from_rendered_raw.number, 15)
        self.assertEqual(from_rendered_raw.powmin, 4)
        self.assertEqual(from_rendered_raw.time, 1418083330)
        self.assertEqual(from_rendered_raw.mediantime, 1418080208)
        self.assertEqual(from_rendered_raw.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(from_rendered_raw.prev_hash, "0000E73C340601ACA1AD5AAA5B5E56B03E178EF8")
        self.assertEqual(from_rendered_raw.prev_issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(from_rendered_raw.members_count, 4)
        self.assertEqual(from_rendered_raw.identities, [])
        self.assertEqual(from_rendered_raw.joiners, [])
        self.assertEqual(from_rendered_raw.actives, [])
        self.assertEqual(from_rendered_raw.leavers, [])
        self.assertEqual(from_rendered_raw.excluded, [])
        self.assertEqual(from_rendered_raw.certifications, [])
        self.assertEqual(from_rendered_raw.transactions, [])

        self.assertEqual(block.signed_raw(), raw_block)

    def test_toraw_fromrawzero(self):
        block = Block.from_signed_raw(raw_block_zero)
        rendered_raw = block.signed_raw()
        from_rendered_raw = block.from_signed_raw(rendered_raw)

        self.assertEqual(from_rendered_raw.version, 2)
        self.assertEqual(from_rendered_raw.currency, "zeta_brouzouf")
        self.assertEqual(from_rendered_raw.noonce, 2125)
        self.assertEqual(from_rendered_raw.number, 0)
        self.assertEqual(from_rendered_raw.powmin, 3)
        self.assertEqual(from_rendered_raw.time, 1418077277)
        self.assertEqual(from_rendered_raw.mediantime, 1418077277)
        self.assertEqual(from_rendered_raw.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(from_rendered_raw.members_count, 4)
        self.assertEqual(len(from_rendered_raw.identities), 4)
        self.assertEqual(len(from_rendered_raw.joiners), 4)
        self.assertEqual(from_rendered_raw.actives, [])
        self.assertEqual(from_rendered_raw.leavers, [])
        self.assertEqual(from_rendered_raw.excluded, [])
        self.assertEqual(len(from_rendered_raw.certifications), 12)
        self.assertEqual(from_rendered_raw.transactions, [])

        self.assertEqual(block.signed_raw(), raw_block_zero)

    def test_raw_with_tx(self):
        block = Block.from_signed_raw(raw_block_with_tx)
        rendered_raw = block.signed_raw()
        from_rendered_raw = block.from_signed_raw(rendered_raw)

        self.assertEqual(from_rendered_raw.version, 2)
        self.assertEqual(from_rendered_raw.currency, "meta_brouzouf")
        self.assertEqual(from_rendered_raw.noonce, 581)
        self.assertEqual(from_rendered_raw.number, 34436)
        self.assertEqual(from_rendered_raw.powmin, 5)
        self.assertEqual(from_rendered_raw.time, 1443896211)
        self.assertEqual(from_rendered_raw.mediantime, 1443881811)
        self.assertEqual(from_rendered_raw.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(from_rendered_raw.parameters, None)
        self.assertEqual(from_rendered_raw.members_count, 19)
        self.assertEqual(from_rendered_raw.identities, [])
        self.assertEqual(from_rendered_raw.joiners, [])
        self.assertEqual(len(from_rendered_raw.actives), 1)
        self.assertEqual(from_rendered_raw.leavers, [])
        self.assertEqual(from_rendered_raw.excluded, [])
        self.assertEqual(len(from_rendered_raw.certifications), 2)
        self.assertEqual(len(from_rendered_raw.transactions), 2)

        self.assertEqual(block.signed_raw(), raw_block_with_tx)

    def test_raw_with_leavers(self):
        block = Block.from_signed_raw(raw_block_with_leavers)
        rendered_raw = block.signed_raw()
        from_rendered_raw = block.from_signed_raw(rendered_raw)
        self.assertEqual(from_rendered_raw.version, 2)
        self.assertEqual(from_rendered_raw.currency, "meta_brouzouf")
        self.assertEqual(from_rendered_raw.noonce, 9906)
        self.assertEqual(from_rendered_raw.number, 34895)
        self.assertEqual(from_rendered_raw.powmin, 4)
        self.assertEqual(from_rendered_raw.time, 1444434128)
        self.assertEqual(from_rendered_raw.mediantime, 1444426438)
        self.assertEqual(from_rendered_raw.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(from_rendered_raw.prev_hash, "0000E88115ADDF79344372C0212928501E21622B")
        self.assertEqual(from_rendered_raw.prev_issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(from_rendered_raw.parameters, None)
        self.assertEqual(from_rendered_raw.members_count, 21)
        self.assertEqual(from_rendered_raw.identities, [])
        self.assertEqual(from_rendered_raw.joiners, [])
        self.assertEqual(from_rendered_raw.actives, [])
        self.assertEqual(len(from_rendered_raw.leavers), 1)
        self.assertEqual(from_rendered_raw.excluded, [])
        self.assertEqual(from_rendered_raw.certifications, [])
        self.assertEqual(from_rendered_raw.transactions, [])

        self.assertEqual(block.signed_raw(), raw_block_with_leavers)

    def test_block_uid__compare(self):
        lower = BlockUID(10, "8101618234DBE5AAD529C13C8BE45E2F9BBE1150CD2FAA25095671F56C1DCDA5")
        higher = BlockUID(14, "E1C0AD728983D8A57335E52CF1064F1AFFD1D454173D8CEBD3ED8B4A72B48704")
        self.assertTrue(lower < higher)
        self.assertFalse(lower > higher)
        self.assertFalse(lower == higher)

if __name__ == '__main__':
    unittest.main()


