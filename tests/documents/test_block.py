'''
Created on 12 déc. 2014

@author: inso
'''
import unittest
from duniterpy.documents.block import Block, BlockUID, block_uid

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


raw_block_zero = """Version: 10
Type: Block
Currency: zeta_brouzouf
Number: 0
PoWMin: 3
Time: 1418077277
MedianTime: 1418077277
UnitBase: 0
Issuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
IssuersFrame: 1
IssuersFrameVar: 0
DifferentIssuersCount: 0
Parameters: 0.0488:86400:1000:432000:100:5259600:63115200:5:5259600:5259600:0.8:31557600:5:24:300:12:0.67:1488970800:1490094000:15778800
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

raw_block_with_tx_v3 = """Version: 3
Type: Block
Currency: meta_brouzouf
Number: 34436
PoWMin: 5
Time: 1443896211
MedianTime: 1443881811
UnitBase: 3
Issuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
IssuersFrame: 43
IssuersFrameVar: 2
DifferentIssuersCount: 8
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
TX:3:1:3:3:1:0:0
32-DB30D958EE5CB75186972286ED3F4686B8A1C2CD
HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY
5:0:T:6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3:0
1:1:T:3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435:10
35:0:D:HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY:88
0:SIG(0)
1:SIG(0)
2:SIG(0)
30:2:SIG(BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g)
42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r
TX:3:3:6:6:3:1:0
3-DB30D958EE5CB75186972286ED3F4686B8A1C2CD
HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY
CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp
9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB
30:0:T:6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3:2
25:0:T:3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435:8
5:1:D:HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY:46
10:1:T:A0D9B4CDC113ECE1145C5525873821398890AE842F4B318BD076095A23E70956:3
60:0:T:67F2045B5318777CC52CD38B424F3E40DDA823FA0364625F124BABE0030E7B5B:5
50:0:D:9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB:46
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


raw_block_with_excluded = """Version: 3
Type: Block
Currency: test_net
Number: 33365
PoWMin: 76
Time: 1472075456
MedianTime: 1472072569
UnitBase: 3
Issuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk
IssuersFrame: 50
IssuersFrameVar: 0
DifferentIssuersCount: 9
PreviousHash: 0000338C775613399FA508A8F8B22EB60F525884730639E2A707299E373F43C0
PreviousIssuer: DesHja7gonANRJB7YUkfCgQpnDjgGeDXAeArdhcbXPmJ
MembersCount: 128
Identities:
Joiners:
Actives:
Leavers:
Revoked:
2VAxjr8QoJtSzhE7APno4AkR2RAQNySpNNvDzMgPotSF:DGXpXwnxIP+j6fyLeaa8Toys9TN/fzumIrAslzAf+Tv50PTIrzBkxjE5oHGtI4AvytApW14rFWgWljmbtrVDAw==
Excluded:
2VAxjr8QoJtSzhE7APno4AkR2RAQNySpNNvDzMgPotSF
Certifications:
Transactions:
TX:3:1:4:4:12:1:0
33363-000021C4B5BE2DA996F953DC09482F4FA2FA68774B1A38FAB03B2AAB4A08EBE0
TENGx7WtzFsTXwnbrPEvb6odX2WnqYcnnrjiiLvp1mS
5:0:T:D25272F1D778B52798B7A51CF0CE21F7C5812F841374508F4367872D4A47F0F7:0
6:1:T:D25272F1D778B52798B7A51CF0CE21F7C5812F841374508F4367872D4A47F0F7:1
7:2:T:D25272F1D778B52798B7A51CF0CE21F7C5812F841374508F4367872D4A47F0F7:2
2300962:3:T:D25272F1D778B52798B7A51CF0CE21F7C5812F841374508F4367872D4A47F0F7:10
0:SIG(0)
1:SIG(0)
2:SIG(0)
3:SIG(0)
5:0:SIG(TENGx7WtzFsTXwnbrPEvb6odX2WnqYcnnrjiiLvp1mS)
6:1:SIG(TENGx7WtzFsTXwnbrPEvb6odX2WnqYcnnrjiiLvp1mS)
7:2:SIG(TENGx7WtzFsTXwnbrPEvb6odX2WnqYcnnrjiiLvp1mS)
10000:3:SIG(5ocqzyDMMWf1V8bsoNhWb1iNwax1e9M7VTUN6navs8of)
13000:3:SIG(XeBpJwRLkF5J4mnwyEDriEcNB13iFpe1MAKR4mH3fzN)
8000:3:SIG(9bZEATXBGPUSsk8oAYi4KAChg3rHKwNt67hVdErbNGCW)
2250:3:SIG(J78bPUvLjxmjaEkdjxWLeENQtcfXm7iobqB49uT1Bgp3)
4750:3:SIG(HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk)
3000:3:SIG(6KXBjAFceD1gp8RBVZfy5YQyKFXG8GaX8tKaLAyPWHrj)
500:3:SIG(ACkHkjDj1SPUu8LhtSAWJLRLoWEXWFuzFPL65zFbe7Yb)
500:3:SIG(5bxtdmC7RGGJEmcdnJ3ut5zg7KdUH2pYZepSHbwNYs7z)
2258962:3:SIG(TENGx7WtzFsTXwnbrPEvb6odX2WnqYcnnrjiiLvp1mS)
REMU:30244:30411
Yo5waBymzDRd0AAMPH8dBj/GnSjtCJUn4EKWaze/4CaU39lf7JAysYmc6yoQGSnGUKZwKT0P0/FvJr9kzX6RBA==
InnerHash: EB2926354963AA21E99E4D304B7765811BA385C9A1976B9A5FACBBCB12F4C969
Nonce: 137387
GmgYhWrwCtsK7t2B/omPpxZ8EfJgv9UYzJIFo++Za+A0Mo70xRfZG7kywxbQTTxDk/V7r90P946N89vdVjv1Bg==
"""


negative_issuers_frame_var = """Version: 3
Type: Block
Currency: test_net
Number: 34662
PoWMin: 78
Time: 1472499945
MedianTime: 1472496896
UnitBase: 3
Issuer: ATkjQPa4sn4LBF69jqEPzFtRdHYJs6MJQjvP8JdN7MtN
IssuersFrame: 65
IssuersFrameVar: 10
DifferentIssuersCount: 14
PreviousHash: 0000069B5B8B86220D5AAF7E4912FA06860FD72A3C9E2A00E0FE11EA0BDD977C
PreviousIssuer: E2uioubZeK5SDMoxkTkizRnhE8qDL24v5oUNNa1sQKMH
MembersCount: 129
Identities:
Joiners:
Actives:
Leavers:
Revoked:
Excluded:
Certifications:
Transactions:
TX:3:1:4:4:2:1:0
34660-00001EEB3FDCEB2F9F39F931ED8F6D419C4C64B4D3F7EA52C35FB6B07A085664
5ocqzyDMMWf1V8bsoNhWb1iNwax1e9M7VTUN6navs8of
765201:3:T:636150D38D565DA0B9717E93C2AD8D6270FA032BF963360ECFCDD55F44493F08:1
435871:3:D:5ocqzyDMMWf1V8bsoNhWb1iNwax1e9M7VTUN6navs8of:34596
5500:3:T:84BB2ADBB690F9204E1139DC4967F364847E68B910D6DA52CD71E09F59A4FB9A:5
5500:3:T:A47000FA1B1DE4E72EF18D77033E2B97D815C39A2D7F132418CB3BEDD1A55D6F:5
0:SIG(0)
1:SIG(0)
2:SIG(0)
3:SIG(0)
217935:3:SIG(BnSRjMjJ7gWy13asCRz9rQ6G5Njytdf3pvR1GMkJgtu6)
994137:3:SIG(5ocqzyDMMWf1V8bsoNhWb1iNwax1e9M7VTUN6navs8of)
tu peux maintenant supprimer les annonces dans cesium - nouveau bouton
PkCYSNLQaM1m6cRzgRTknrQ1BjvoyUYO5XRMNNYfjwUigg62guPd79QXZqmBIlUb5RPPI6EF1SMdArhaoYc7Cg==
InnerHash: 96C3CBEC2EF6C7AD768EC787EADEA41B0ADA80FBC611EED6976BBCEDA3D2D6CE
Nonce: 202829
WnJvw204wccmSBQK9UE2rCFw0EG34zf+b58n2KTLwSIhTpgmGsnr5ohkSyYZYcLEKjisLXKNCmMl7D1Q9bJiBQ==
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
        self.assertEqual(block.version, 10)
        self.assertEqual(block.currency, "zeta_brouzouf")
        self.assertEqual(block.noonce, 2125)
        self.assertEqual(block.number, 0)
        self.assertEqual(block.powmin, 3)
        self.assertEqual(block.time, 1418077277)
        self.assertEqual(block.mediantime, 1418077277)
        self.assertEqual(block.issuer, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(block.parameters, ("0.0488","86400","1000","432000","100","5259600","63115200","5","5259600",
                                            "5259600","0.8","31557600","5","24","300","12","0.67","1488970800",
                                            "1490094000", "15778800"))
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

        self.assertEqual(from_rendered_raw.version, 10)
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

    def test_raw_with_tx_v3(self):
        block = Block.from_signed_raw(raw_block_with_tx_v3)
        rendered_raw = block.signed_raw()
        from_rendered_raw = block.from_signed_raw(rendered_raw)

        self.assertEqual(from_rendered_raw.version, 3)
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

        self.assertEqual(block.signed_raw(), raw_block_with_tx_v3)

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

    def test_parse_with_excluded(self):
        block = Block.from_signed_raw(raw_block_with_excluded)
        rendered_raw = block.signed_raw()
        from_rendered_raw = block.from_signed_raw(rendered_raw)
        self.assertEqual(from_rendered_raw.signed_raw(), raw_block_with_excluded)

    def test_parse_negative_issuers_frame_var(self):
        block = Block.from_signed_raw(negative_issuers_frame_var)
        rendered_raw = block.signed_raw()
        from_rendered_raw = block.from_signed_raw(rendered_raw)
        self.assertEqual(from_rendered_raw.signed_raw(), negative_issuers_frame_var)

    def test_block_uid_converter(self):
        buid = block_uid("1345-0000338C775613399FA508A8F8B22EB60F525884730639E2A707299E373F43C0")
        self.assertEqual(buid.number, 1345)
        self.assertEqual(buid.sha_hash, "0000338C775613399FA508A8F8B22EB60F525884730639E2A707299E373F43C0")

    def test_block_uid_converter_error(self):
        with self.assertRaises(TypeError):
            buid = block_uid(1235654)

    def test_block_uid_no_convert(self):
        buid = block_uid(BlockUID(1345, "0000338C775613399FA508A8F8B22EB60F525884730639E2A707299E373F43C0"))
        self.assertEqual(buid.number, 1345)
        self.assertEqual(buid.sha_hash, "0000338C775613399FA508A8F8B22EB60F525884730639E2A707299E373F43C0")

    def test_block_uid_non_zero(self):
        buid = BlockUID(1345, "0000338C775613399FA508A8F8B22EB60F525884730639E2A707299E373F43C0")
        if not buid:
            self.fail("__nonzero__ comparison failed")
        elif BlockUID.empty():
            self.fail("Empty blockuid __nonzero__ comparison failed")

    def test_proof_of_work(self):
        block = """Version: 5
Type: Block
Currency: test_net
Number: 60803
PoWMin: 80
Time: 1480979125
MedianTime: 1480975879
UnitBase: 7
Issuer: 9bZEATXBGPUSsk8oAYi4KAChg3rHKwNt67hVdErbNGCW
IssuersFrame: 120
IssuersFrameVar: 0
DifferentIssuersCount: 18
PreviousHash: 0000083FB6E3435ADCDF0F86B0A1BCA108B6B47D4B4BA61D0B4FDC21A262CF4C
PreviousIssuer: BnSRjMjJ7gWy13asCRz9rQ6G5Njytdf3pvR1GMkJgtu6
MembersCount: 187
Identities:
Joiners:
Actives:
Leavers:
Revoked:
Excluded:
Certifications:
Transactions:
InnerHash: 310F57575EA865EF47BFA236108B2B1CAEBFBF8EF70960E32E214E413E9C836B
Nonce: 10200000037440
AywstQpC0S5iaA/YQvbz2alpP6zTYG3tjkWpxy1jgeCo028Te2V327bBZbfDGDzsjxOrF4UVmEBiGsgbqhL9CA==
"""
        block_doc = Block.from_signed_raw(block)
        self.assertEqual(block_doc.proof_of_work(), "00000A84839226046082E2B1AD49664E382D98C845644945D133D4A90408813A")

if __name__ == '__main__':
    unittest.main()


