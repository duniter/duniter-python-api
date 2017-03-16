'''
Created on 12 déc. 2014

@author: inso
'''
import unittest
import pypeg2
from duniterpy.grammars import output
from duniterpy.documents.transaction import Transaction, reduce_base, SimpleTransaction


compact_change = """TX:10:1:1:1:1:1:0
13410-000041DF0CCA173F09B5FBA48F619D4BC934F12ADF1D0B798639EB2149C4A8CC
D8BsQZN9hangHVuqwD6McfxM1xvGJ8DPuPYrswwnSif3
1500:1:T:0D0264F324BC4A23C4B2C696CD1907BD6E70FD1F409BB1D42E84847AA4C1E87C:0
0:SIG(0)
1500:1:(XHX(8AFC8DF633FC158F9DB4864ABED696C1AA0FE5D617A7B5F7AB8DE7CA2EFCD4CB) && SIG(36j6pCNzKDPo92m7UXJLFpgDbcLFAZBgThD2TCwTwGrd)) || (SIG(D8BsQZN9hangHVuqwD6McfxM1xvGJ8DPuPYrswwnSif3) && SIG(36j6pCNzKDPo92m7UXJLFpgDbcLFAZBgThD2TCwTwGrd))
META tic to toc
eNAZpJjhZaPKbx5pUvuDDM1j4XNWJ4ABK48ouTvimvg3ceIcoZUvgLHmXuSwk2bgxZaB5qSKP9H6T7qsBcLtBg==
"""


xhx_output = """Version: 10
Type: Transaction
Currency: gtest
Blockstamp: 13739-000087835A9B746C1A6E173DB13A2C3D23DBDE8B2C5E93565B644313FE3D179B
Locktime: 0
Issuers:
95ApcNEeoFnjUYPwh4fbGqKPDe5mCJysfJfezLngEZcu
Inputs:
250:1:T:7AEDF83C99071E040698ED6E1445BF02FADEF37DA380795684D5C9271C037D5A:0
Unlocks:
0:SIG(0)
Outputs:
250:1:(XHX(8FAA0ED653CA4D2C1156D511F0D0036F5168ABA4DAC2929676D279C8A2A12E36) && SIG(DCYELkvV1aAsxFv58SbfRerHy5giJwKA1i4ZKTTcVGZe)) || (SIG(95ApcNEeoFnjUYPwh4fbGqKPDe5mCJysfJfezLngEZcu) && SIG(DCYELkvV1aAsxFv58SbfRerHy5giJwKA1i4ZKTTcVGZe))
Comment: XHX for pubkey DCYELkvV1aAsxFv58SbfRerHy5giJwKA1i4ZKTTcVGZe
GXGephqTSJfb+8xsG/UMKRW0y+edL4RoMHM+OlgFq1aYOuaQ3/CtBKVSA01n2mkI7zwepeIABSjS94iVH4vZDg==
"""


tx_compact = """TX:2:3:6:6:3:1:0
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
49:2:(SIG(6DyGr5LFtFmbaJYRvcs9WmBsr4cbJbJ1EV9zBbqG7A6i) || XHX(8FAA0ED653CA4D2C1156D511F0D0036F5168ABA4DAC2929676D279C8A2A12E36))
-----@@@----- (why not this comment?)
42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r
2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX
2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk
"""


tx_compact_2 = """TX:2:1:1:1:2:0:0
GNPdPNwSJAYw7ixkDeibo3YpdELgLmrZ2Q86HF4cyg92
D:GNPdPNwSJAYw7ixkDeibo3YpdELgLmrZ2Q86HF4cyg92:471
0:SIG(0)
90:0:SIG(5zDvFjJB1PGDQNiExpfzL9c1tQGs6xPA8mf1phr3VoVi)
10:0:SIG(GNPdPNwSJAYw7ixkDeibo3YpdELgLmrZ2Q86HF4cyg92)
XDQeEMcJDd+XVGaFIZc8d4kKRJgsPuWAPVNG5UKNk8mDZx2oE1kTP/hbxiFx6yDouBELCswuf/X6POK9ES7JCA==
"""

tx_raw = """Version: 2
Type: Transaction
Currency: beta_brousouf
Locktime: 0
Issuers:
HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY
CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp
9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB
Inputs:
T:6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3:2
T:3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435:8
D:HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY:46
T:A0D9B4CDC113ECE1145C5525873821398890AE842F4B318BD076095A23E70956:3
T:67F2045B5318777CC52CD38B424F3E40DDA823FA0364625F124BABE0030E7B5B:5
D:9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB:46
Unlocks:
0:SIG(0)
1:XHX(7665798292)
2:SIG(0)
3:SIG(0) SIG(2)
4:SIG(0) SIG(1) SIG(2)
5:SIG(2)
Outputs:
120:2:SIG(BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g)
146:2:SIG(DSz4rgncXCytsUMW2JU2yhLquZECD2XpEkpP9gG5HyAx)
49:2:(SIG(6DyGr5LFtFmbaJYRvcs9WmBsr4cbJbJ1EV9zBbqG7A6i) || XHX(8FAA0ED653CA4D2C1156D511F0D0036F5168ABA4DAC2929676D279C8A2A12E36))
Comment: -----@@@----- (why not this comment?)
42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r
2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX
2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk
"""


tx_raw_v3 = """Version: 3
Type: Transaction
Currency: beta_brousouf
Blockstamp: 32-DB30D958EE5CB75186972286ED3F4686B8A1C2CD
Locktime: 0
Issuers:
HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY
CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp
9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB
Inputs:
30:0:T:6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3:2
25:0:T:3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435:8
5:1:D:HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY:46
10:1:T:A0D9B4CDC113ECE1145C5525873821398890AE842F4B318BD076095A23E70956:3
60:0:T:67F2045B5318777CC52CD38B424F3E40DDA823FA0364625F124BABE0030E7B5B:5
50:0:D:9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB:46
Unlocks:
0:SIG(0)
1:XHX(7665798292)
2:SIG(0)
3:SIG(0) SIG(2)
4:SIG(0) SIG(1) SIG(2)
5:SIG(2)
Outputs:
120:2:SIG(BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g)
146:2:SIG(DSz4rgncXCytsUMW2JU2yhLquZECD2XpEkpP9gG5HyAx)
49:2:(SIG(6DyGr5LFtFmbaJYRvcs9WmBsr4cbJbJ1EV9zBbqG7A6i) || XHX(8FAA0ED653CA4D2C1156D511F0D0036F5168ABA4DAC2929676D279C8A2A12E36))
Comment: -----@@@----- (why not this comment?)
42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r
2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX
2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk
"""


class Test_Transaction(unittest.TestCase):
    def test_fromcompact(self):
        tx = Transaction.from_compact("zeta_brousouf", tx_compact)
        self.assertEqual(tx.version, 2)
        self.assertEqual(tx.currency, "zeta_brousouf")
        self.assertEqual(len(tx.issuers), 3)
        self.assertEqual(len(tx.inputs), 6)
        self.assertEqual(len(tx.unlocks), 6)
        self.assertEqual(len(tx.outputs), 3)

        self.assertEqual(tx.issuers[0], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(tx.issuers[1], "CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp")
        self.assertEqual(tx.issuers[2], "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB")

        self.assertEqual(tx.inputs[0].source, 'T')
        self.assertEqual(tx.inputs[0].origin_id, "6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3")
        self.assertEqual(tx.inputs[0].index, 2)
        self.assertEqual(tx.inputs[1].source, 'T')
        self.assertEqual(tx.inputs[1].origin_id, "3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435")
        self.assertEqual(tx.inputs[1].index, 8)
        self.assertEqual(tx.inputs[2].source, 'D')
        self.assertEqual(tx.inputs[2].origin_id, "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(tx.inputs[2].index, 46)
        self.assertEqual(tx.inputs[3].source, 'T')
        self.assertEqual(tx.inputs[3].origin_id, "A0D9B4CDC113ECE1145C5525873821398890AE842F4B318BD076095A23E70956")
        self.assertEqual(tx.inputs[3].index, 3)
        self.assertEqual(tx.inputs[4].source, 'T')
        self.assertEqual(tx.inputs[4].origin_id, "67F2045B5318777CC52CD38B424F3E40DDA823FA0364625F124BABE0030E7B5B")
        self.assertEqual(tx.inputs[4].index, 5)
        self.assertEqual(tx.inputs[5].source, 'D')
        self.assertEqual(tx.inputs[5].origin_id, "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB")
        self.assertEqual(tx.inputs[5].index, 46)

        self.assertEqual(tx.unlocks[0].index, 0)
        self.assertEqual(str(tx.unlocks[0].parameters[0]), "SIG(0)")
        self.assertEqual(tx.unlocks[1].index, 1)
        self.assertEqual(str(tx.unlocks[1].parameters[0]), "XHX(7665798292)")
        self.assertEqual(tx.unlocks[2].index, 2)
        self.assertEqual(str(tx.unlocks[2].parameters[0]), "SIG(0)")
        self.assertEqual(tx.unlocks[3].index, 3)
        self.assertEqual(str(tx.unlocks[3].parameters[0]), "SIG(0)")
        self.assertEqual(str(tx.unlocks[3].parameters[1]), "SIG(2)")
        self.assertEqual(tx.unlocks[4].index, 4)
        self.assertEqual(str(tx.unlocks[4].parameters[0]), "SIG(0)")
        self.assertEqual(str(tx.unlocks[4].parameters[1]), "SIG(1)")
        self.assertEqual(str(tx.unlocks[4].parameters[2]), "SIG(2)")
        self.assertEqual(tx.unlocks[5].index, 5)
        self.assertEqual(str(tx.unlocks[5].parameters[0]), "SIG(2)")

        self.assertEqual(tx.outputs[0].amount, 120)
        self.assertEqual(tx.outputs[0].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[0].conditions, output.Condition), "SIG(BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g)")
        self.assertEqual(tx.outputs[1].amount, 146)
        self.assertEqual(tx.outputs[1].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[1].conditions, output.Condition), "SIG(DSz4rgncXCytsUMW2JU2yhLquZECD2XpEkpP9gG5HyAx)")
        self.assertEqual(tx.outputs[2].amount, 49)
        self.assertEqual(tx.outputs[2].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[2].conditions, output.Condition), "(SIG(6DyGr5LFtFmbaJYRvcs9WmBsr4cbJbJ1EV9zBbqG7A6i) || XHX(8FAA0ED653CA4D2C1156D511F0D0036F5168ABA4DAC2929676D279C8A2A12E36))")

        self.assertEqual(tx.comment, "-----@@@----- (why not this comment?)")

        self.assertEqual(tx.signatures[0], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")
        self.assertEqual(tx.signatures[1], "2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX")
        self.assertEqual(tx.signatures[2], "2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk")

    def test_fromcompact2(self):
        tx = Transaction.from_compact("zeta_brousouf", tx_compact_2)
        self.assertEqual(tx.version, 2)
        self.assertEqual(tx.currency, "zeta_brousouf")
        self.assertEqual(len(tx.issuers), 1)
        self.assertEqual(len(tx.inputs), 1)
        self.assertEqual(len(tx.unlocks), 1)
        self.assertEqual(len(tx.outputs), 2)

        self.assertEqual(tx.issuers[0], "GNPdPNwSJAYw7ixkDeibo3YpdELgLmrZ2Q86HF4cyg92")

        self.assertEqual(tx.inputs[0].source, 'D')
        self.assertEqual(tx.inputs[0].origin_id, "GNPdPNwSJAYw7ixkDeibo3YpdELgLmrZ2Q86HF4cyg92")
        self.assertEqual(tx.inputs[0].index, 471)

        self.assertEqual(tx.unlocks[0].index, 0)
        self.assertEqual(str(tx.unlocks[0].parameters[0]), "SIG(0)")

        self.assertEqual(tx.outputs[0].amount, 90)
        self.assertEqual(tx.outputs[0].base, 0)
        self.assertEqual(pypeg2.compose(tx.outputs[0].conditions, output.Condition), "SIG(5zDvFjJB1PGDQNiExpfzL9c1tQGs6xPA8mf1phr3VoVi)")
        self.assertEqual(type(tx.outputs[0].conditions.left), output.SIG)
        self.assertEqual(tx.outputs[1].amount, 10)
        self.assertEqual(tx.outputs[1].base, 0)
        self.assertEqual(pypeg2.compose(tx.outputs[1].conditions, output.Condition), "SIG(GNPdPNwSJAYw7ixkDeibo3YpdELgLmrZ2Q86HF4cyg92)")
        self.assertEqual(type(tx.outputs[1].conditions.left), output.SIG)
        self.assertEqual(tx.signatures[0], "XDQeEMcJDd+XVGaFIZc8d4kKRJgsPuWAPVNG5UKNk8mDZx2oE1kTP/hbxiFx6yDouBELCswuf/X6POK9ES7JCA==")

    def test_fromraw(self):
        tx = Transaction.from_signed_raw(tx_raw)
        self.assertEqual(tx.version, 2)
        self.assertEqual(tx.currency, "beta_brousouf")
        self.assertEqual(len(tx.issuers), 3)
        self.assertEqual(len(tx.inputs), 6)
        self.assertEqual(len(tx.unlocks), 6)
        self.assertEqual(len(tx.outputs), 3)

        self.assertEqual(tx.issuers[0], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(tx.issuers[1], "CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp")
        self.assertEqual(tx.issuers[2], "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB")

        self.assertEqual(tx.inputs[0].source, 'T')
        self.assertEqual(tx.inputs[0].origin_id, "6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3")
        self.assertEqual(tx.inputs[0].index, 2)
        self.assertEqual(tx.inputs[1].source, 'T')
        self.assertEqual(tx.inputs[1].origin_id, "3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435")
        self.assertEqual(tx.inputs[1].index, 8)
        self.assertEqual(tx.inputs[2].source, 'D')
        self.assertEqual(tx.inputs[2].origin_id, "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(tx.inputs[2].index, 46)
        self.assertEqual(tx.inputs[3].source, 'T')
        self.assertEqual(tx.inputs[3].origin_id, "A0D9B4CDC113ECE1145C5525873821398890AE842F4B318BD076095A23E70956")
        self.assertEqual(tx.inputs[3].index, 3)
        self.assertEqual(tx.inputs[4].source, 'T')
        self.assertEqual(tx.inputs[4].origin_id, "67F2045B5318777CC52CD38B424F3E40DDA823FA0364625F124BABE0030E7B5B")
        self.assertEqual(tx.inputs[4].index, 5)
        self.assertEqual(tx.inputs[5].source, 'D')
        self.assertEqual(tx.inputs[5].origin_id, "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB")
        self.assertEqual(tx.inputs[5].index, 46)

        self.assertEqual(tx.unlocks[0].index, 0)
        self.assertEqual(str(tx.unlocks[0].parameters[0]), "SIG(0)")
        self.assertEqual(tx.unlocks[1].index, 1)
        self.assertEqual(str(tx.unlocks[1].parameters[0]), "XHX(7665798292)")
        self.assertEqual(tx.unlocks[2].index, 2)
        self.assertEqual(str(tx.unlocks[2].parameters[0]), "SIG(0)")
        self.assertEqual(tx.unlocks[3].index, 3)
        self.assertEqual(str(tx.unlocks[3].parameters[0]), "SIG(0)")
        self.assertEqual(str(tx.unlocks[3].parameters[1]), "SIG(2)")
        self.assertEqual(tx.unlocks[4].index, 4)
        self.assertEqual(str(tx.unlocks[4].parameters[0]), "SIG(0)")
        self.assertEqual(str(tx.unlocks[4].parameters[1]), "SIG(1)")
        self.assertEqual(str(tx.unlocks[4].parameters[2]), "SIG(2)")
        self.assertEqual(tx.unlocks[5].index, 5)
        self.assertEqual(str(tx.unlocks[5].parameters[0]), "SIG(2)")

        self.assertEqual(tx.outputs[0].amount, 120)
        self.assertEqual(tx.outputs[0].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[0].conditions, output.Condition), "SIG(BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g)")
        self.assertEqual(tx.outputs[1].amount, 146)
        self.assertEqual(tx.outputs[1].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[1].conditions, output.Condition), "SIG(DSz4rgncXCytsUMW2JU2yhLquZECD2XpEkpP9gG5HyAx)")
        self.assertEqual(tx.outputs[2].amount, 49)
        self.assertEqual(tx.outputs[2].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[2].conditions, output.Condition), "(SIG(6DyGr5LFtFmbaJYRvcs9WmBsr4cbJbJ1EV9zBbqG7A6i) || XHX(8FAA0ED653CA4D2C1156D511F0D0036F5168ABA4DAC2929676D279C8A2A12E36))")

        self.assertEqual(tx.comment, "-----@@@----- (why not this comment?)")

        self.assertEqual(tx.signatures[0], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")
        self.assertEqual(tx.signatures[1], "2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX")
        self.assertEqual(tx.signatures[2], "2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk")

    def test_fromraw_toraw(self):
        tx = Transaction.from_signed_raw(tx_raw)
        rendered_tx = tx.signed_raw()
        from_rendered_tx = Transaction.from_signed_raw(rendered_tx)

        self.assertEqual(tx.version, 2)
        self.assertEqual(tx.currency, "beta_brousouf")
        self.assertEqual(len(tx.issuers), 3)
        self.assertEqual(len(tx.inputs), 6)
        self.assertEqual(len(tx.unlocks), 6)
        self.assertEqual(len(tx.outputs), 3)

        self.assertEqual(tx.issuers[0], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(tx.issuers[1], "CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp")
        self.assertEqual(tx.issuers[2], "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB")

        self.assertEqual(tx.inputs[0].source, 'T')
        self.assertEqual(tx.inputs[0].origin_id, "6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3")
        self.assertEqual(tx.inputs[0].index, 2)
        self.assertEqual(tx.inputs[1].source, 'T')
        self.assertEqual(tx.inputs[1].origin_id, "3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435")
        self.assertEqual(tx.inputs[1].index, 8)
        self.assertEqual(tx.inputs[2].source, 'D')
        self.assertEqual(tx.inputs[2].origin_id, "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(tx.inputs[2].index, 46)
        self.assertEqual(tx.inputs[3].source, 'T')
        self.assertEqual(tx.inputs[3].origin_id, "A0D9B4CDC113ECE1145C5525873821398890AE842F4B318BD076095A23E70956")
        self.assertEqual(tx.inputs[3].index, 3)
        self.assertEqual(tx.inputs[4].source, 'T')
        self.assertEqual(tx.inputs[4].origin_id, "67F2045B5318777CC52CD38B424F3E40DDA823FA0364625F124BABE0030E7B5B")
        self.assertEqual(tx.inputs[4].index, 5)
        self.assertEqual(tx.inputs[5].source, 'D')
        self.assertEqual(tx.inputs[5].origin_id, "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB")
        self.assertEqual(tx.inputs[5].index, 46)

        self.assertEqual(tx.unlocks[0].index, 0)
        self.assertEqual(str(tx.unlocks[0].parameters[0]), "SIG(0)")
        self.assertEqual(tx.unlocks[1].index, 1)
        self.assertEqual(str(tx.unlocks[1].parameters[0]), "XHX(7665798292)")
        self.assertEqual(tx.unlocks[2].index, 2)
        self.assertEqual(str(tx.unlocks[2].parameters[0]), "SIG(0)")
        self.assertEqual(tx.unlocks[3].index, 3)
        self.assertEqual(str(tx.unlocks[3].parameters[0]), "SIG(0)")
        self.assertEqual(str(tx.unlocks[3].parameters[1]), "SIG(2)")
        self.assertEqual(tx.unlocks[4].index, 4)
        self.assertEqual(str(tx.unlocks[4].parameters[0]), "SIG(0)")
        self.assertEqual(str(tx.unlocks[4].parameters[1]), "SIG(1)")
        self.assertEqual(str(tx.unlocks[4].parameters[2]), "SIG(2)")
        self.assertEqual(tx.unlocks[5].index, 5)
        self.assertEqual(str(tx.unlocks[5].parameters[0]), "SIG(2)")

        self.assertEqual(tx.outputs[0].amount, 120)
        self.assertEqual(tx.outputs[0].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[0].conditions, output.Condition), "SIG(BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g)")
        self.assertEqual(tx.outputs[1].amount, 146)
        self.assertEqual(tx.outputs[1].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[1].conditions, output.Condition), "SIG(DSz4rgncXCytsUMW2JU2yhLquZECD2XpEkpP9gG5HyAx)")
        self.assertEqual(tx.outputs[2].amount, 49)
        self.assertEqual(tx.outputs[2].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[2].conditions, output.Condition), "(SIG(6DyGr5LFtFmbaJYRvcs9WmBsr4cbJbJ1EV9zBbqG7A6i) || XHX(8FAA0ED653CA4D2C1156D511F0D0036F5168ABA4DAC2929676D279C8A2A12E36))")

        self.assertEqual(tx.comment, "-----@@@----- (why not this comment?)")

        self.assertEqual(tx.signatures[0], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")
        self.assertEqual(tx.signatures[1], "2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX")
        self.assertEqual(tx.signatures[2], "2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk")

    def test_fromraw_toraw_v3(self):
        tx = Transaction.from_signed_raw(tx_raw_v3)
        rendered_tx = tx.signed_raw()
        from_rendered_tx = Transaction.from_signed_raw(rendered_tx)

        self.assertEqual(tx.version, 3)
        self.assertEqual(tx.currency, "beta_brousouf")
        self.assertEqual(tx.blockstamp.number, 32)
        self.assertEqual(tx.blockstamp.sha_hash, "DB30D958EE5CB75186972286ED3F4686B8A1C2CD")
        self.assertEqual(len(tx.issuers), 3)
        self.assertEqual(len(tx.inputs), 6)
        self.assertEqual(len(tx.unlocks), 6)
        self.assertEqual(len(tx.outputs), 3)

        self.assertEqual(tx.issuers[0], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(tx.issuers[1], "CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp")
        self.assertEqual(tx.issuers[2], "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB")

        self.assertEqual(tx.inputs[0].source, 'T')
        self.assertEqual(tx.inputs[0].origin_id, "6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3")
        self.assertEqual(tx.inputs[0].index, 2)
        self.assertEqual(tx.inputs[1].source, 'T')
        self.assertEqual(tx.inputs[1].origin_id, "3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435")
        self.assertEqual(tx.inputs[1].index, 8)
        self.assertEqual(tx.inputs[2].source, 'D')
        self.assertEqual(tx.inputs[2].origin_id, "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(tx.inputs[2].index, 46)
        self.assertEqual(tx.inputs[3].source, 'T')
        self.assertEqual(tx.inputs[3].origin_id, "A0D9B4CDC113ECE1145C5525873821398890AE842F4B318BD076095A23E70956")
        self.assertEqual(tx.inputs[3].index, 3)
        self.assertEqual(tx.inputs[4].source, 'T')
        self.assertEqual(tx.inputs[4].origin_id, "67F2045B5318777CC52CD38B424F3E40DDA823FA0364625F124BABE0030E7B5B")
        self.assertEqual(tx.inputs[4].index, 5)
        self.assertEqual(tx.inputs[5].source, 'D')
        self.assertEqual(tx.inputs[5].origin_id, "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB")
        self.assertEqual(tx.inputs[5].index, 46)

        self.assertEqual(tx.unlocks[0].index, 0)
        self.assertEqual(str(tx.unlocks[0].parameters[0]), "SIG(0)")
        self.assertEqual(tx.unlocks[1].index, 1)
        self.assertEqual(str(tx.unlocks[1].parameters[0]), "XHX(7665798292)")
        self.assertEqual(tx.unlocks[2].index, 2)
        self.assertEqual(str(tx.unlocks[2].parameters[0]), "SIG(0)")
        self.assertEqual(tx.unlocks[3].index, 3)
        self.assertEqual(str(tx.unlocks[3].parameters[0]), "SIG(0)")
        self.assertEqual(str(tx.unlocks[3].parameters[1]), "SIG(2)")
        self.assertEqual(tx.unlocks[4].index, 4)
        self.assertEqual(str(tx.unlocks[4].parameters[0]), "SIG(0)")
        self.assertEqual(str(tx.unlocks[4].parameters[1]), "SIG(1)")
        self.assertEqual(str(tx.unlocks[4].parameters[2]), "SIG(2)")
        self.assertEqual(tx.unlocks[5].index, 5)
        self.assertEqual(str(tx.unlocks[5].parameters[0]), "SIG(2)")

        self.assertEqual(tx.outputs[0].amount, 120)
        self.assertEqual(tx.outputs[0].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[0].conditions, output.Condition), "SIG(BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g)")
        self.assertEqual(tx.outputs[1].amount, 146)
        self.assertEqual(tx.outputs[1].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[1].conditions, output.Condition), "SIG(DSz4rgncXCytsUMW2JU2yhLquZECD2XpEkpP9gG5HyAx)")
        self.assertEqual(tx.outputs[2].amount, 49)
        self.assertEqual(tx.outputs[2].base, 2)
        self.assertEqual(pypeg2.compose(tx.outputs[2].conditions, output.Condition), "(SIG(6DyGr5LFtFmbaJYRvcs9WmBsr4cbJbJ1EV9zBbqG7A6i) || XHX(8FAA0ED653CA4D2C1156D511F0D0036F5168ABA4DAC2929676D279C8A2A12E36))")

        self.assertEqual(tx.comment, "-----@@@----- (why not this comment?)")

        self.assertEqual(tx.signatures[0], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")
        self.assertEqual(tx.signatures[1], "2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX")
        self.assertEqual(tx.signatures[2], "2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk")

    def test_compact_change(self):
        tx = Transaction.from_compact("gtest", compact_change)
        rendered_tx = tx.signed_raw()
        from_rendered_tx = Transaction.from_signed_raw(rendered_tx)

    def test_reduce_base(self):
        amount = 1200
        base = 0
        computed = reduce_base(amount, base)
        self.assertEqual(computed[0], 12)
        self.assertEqual(computed[1], 2)

    def test_reduce_base_2(self):
        amount = 120
        base = 4
        computed = reduce_base(amount, base)
        self.assertEqual(computed[0], 12)
        self.assertEqual(computed[1], 5)

    def test_is_simple(self):
        tx = Transaction.from_compact("zeta_brousouf", tx_compact_2)
        self.assertTrue(SimpleTransaction.is_simple(tx))

        tx = Transaction.from_compact("zeta_brousouf", tx_compact)
        self.assertFalse(SimpleTransaction.is_simple(tx))
