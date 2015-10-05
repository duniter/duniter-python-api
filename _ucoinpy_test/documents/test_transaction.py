'''
Created on 12 déc. 2014

@author: inso
'''
import unittest
from ucoinpy.documents.transaction import Transaction


tx_compact = """TX:1:1:3:1:0
HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY
0:T:65:D717FEC1993554F8EAE4CEA88DE5FBB6887CFAE8:4
0:T:77:F80993776FB55154A60B3E58910C942A347964AD:15
0:D:88:F4A47E39BC2A20EE69DCD5CAB0A9EB3C92FD8F7B:11
BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g:30
42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r
"""

tx_raw = """Version: 1
Type: Transaction
Currency: beta_brousouf
Issuers:
HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY
Inputs:
0:T:65:D717FEC1993554F8EAE4CEA88DE5FBB6887CFAE8:4
0:T:77:F80993776FB55154A60B3E58910C942A347964AD:15
0:D:88:F4A47E39BC2A20EE69DCD5CAB0A9EB3C92FD8F7B:11
Outputs:
BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g:30
Comment:
42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r
"""


class Test_Transaction(unittest.TestCase):
    def test_fromcompact(self):
        tx = Transaction.from_compact("zeta_brousouf", tx_compact)
        self.assertEquals(tx.version, 1)
        self.assertEquals(tx.currency, "zeta_brousouf")
        self.assertEquals(len(tx.issuers), 1)
        self.assertEquals(len(tx.inputs), 3)
        self.assertEquals(len(tx.outputs), 1)

        self.assertEquals(tx.issuers[0], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")

        self.assertEquals(tx.inputs[0].index, 0)
        self.assertEquals(tx.inputs[0].source, 'T')
        self.assertEquals(tx.inputs[0].number, 65)
        self.assertEquals(tx.inputs[0].txhash, "D717FEC1993554F8EAE4CEA88DE5FBB6887CFAE8")
        self.assertEquals(tx.inputs[0].amount, 4)

        self.assertEquals(tx.inputs[1].index, 0)
        self.assertEquals(tx.inputs[1].source, 'T')
        self.assertEquals(tx.inputs[1].number, 77)
        self.assertEquals(tx.inputs[1].txhash, "F80993776FB55154A60B3E58910C942A347964AD")
        self.assertEquals(tx.inputs[1].amount, 15)

        self.assertEquals(tx.inputs[2].index, 0)
        self.assertEquals(tx.inputs[2].source, 'D')
        self.assertEquals(tx.inputs[2].number, 88)
        self.assertEquals(tx.inputs[2].txhash, "F4A47E39BC2A20EE69DCD5CAB0A9EB3C92FD8F7B")
        self.assertEquals(tx.inputs[2].amount, 11)

        self.assertEquals(tx.outputs[0].pubkey, "BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g")
        self.assertEquals(tx.outputs[0].amount, 30)

        self.assertEquals(tx.signatures[0], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")

    def test_fromraw(self):
        tx = Transaction.from_signed_raw(tx_raw)
        self.assertEquals(tx.version, 1)
        self.assertEquals(tx.currency, "beta_brousouf")
        self.assertEquals(len(tx.issuers), 1)
        self.assertEquals(len(tx.inputs), 3)
        self.assertEquals(len(tx.outputs), 1)

        self.assertEquals(tx.issuers[0], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")

        self.assertEquals(tx.inputs[0].index, 0)
        self.assertEquals(tx.inputs[0].source, 'T')
        self.assertEquals(tx.inputs[0].number, 65)
        self.assertEquals(tx.inputs[0].txhash, "D717FEC1993554F8EAE4CEA88DE5FBB6887CFAE8")
        self.assertEquals(tx.inputs[0].amount, 4)

        self.assertEquals(tx.inputs[1].index, 0)
        self.assertEquals(tx.inputs[1].source, 'T')
        self.assertEquals(tx.inputs[1].number, 77)
        self.assertEquals(tx.inputs[1].txhash, "F80993776FB55154A60B3E58910C942A347964AD")
        self.assertEquals(tx.inputs[1].amount, 15)

        self.assertEquals(tx.inputs[2].index, 0)
        self.assertEquals(tx.inputs[2].source, 'D')
        self.assertEquals(tx.inputs[2].number, 88)
        self.assertEquals(tx.inputs[2].txhash, "F4A47E39BC2A20EE69DCD5CAB0A9EB3C92FD8F7B")
        self.assertEquals(tx.inputs[2].amount, 11)

        self.assertEquals(tx.outputs[0].pubkey, "BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g")
        self.assertEquals(tx.outputs[0].amount, 30)

        self.assertEquals(tx.signatures[0], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")

    def test_fromraw_toraw(self):
        tx = Transaction.from_signed_raw(tx_raw)
        rendered_tx = tx.signed_raw()
        from_rendered_tx = Transaction.from_signed_raw(rendered_tx)

        self.assertEquals(from_rendered_tx.version, 1)
        self.assertEquals(len(from_rendered_tx.issuers), 1)
        self.assertEquals(len(from_rendered_tx.inputs), 3)
        self.assertEquals(len(from_rendered_tx.outputs), 1)

        self.assertEquals(from_rendered_tx.issuers[0], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")

        self.assertEquals(from_rendered_tx.inputs[0].index, 0)
        self.assertEquals(from_rendered_tx.inputs[0].source, 'T')
        self.assertEquals(from_rendered_tx.inputs[0].number, 65)
        self.assertEquals(from_rendered_tx.inputs[0].txhash, "D717FEC1993554F8EAE4CEA88DE5FBB6887CFAE8")
        self.assertEquals(from_rendered_tx.inputs[0].amount, 4)

        self.assertEquals(from_rendered_tx.inputs[1].index, 0)
        self.assertEquals(from_rendered_tx.inputs[1].source, 'T')
        self.assertEquals(from_rendered_tx.inputs[1].number, 77)
        self.assertEquals(from_rendered_tx.inputs[1].txhash, "F80993776FB55154A60B3E58910C942A347964AD")
        self.assertEquals(from_rendered_tx.inputs[1].amount, 15)

        self.assertEquals(from_rendered_tx.inputs[2].index, 0)
        self.assertEquals(from_rendered_tx.inputs[2].source, 'D')
        self.assertEquals(from_rendered_tx.inputs[2].number, 88)
        self.assertEquals(from_rendered_tx.inputs[2].txhash, "F4A47E39BC2A20EE69DCD5CAB0A9EB3C92FD8F7B")
        self.assertEquals(from_rendered_tx.inputs[2].amount, 11)

        self.assertEquals(from_rendered_tx.outputs[0].pubkey, "BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g")
        self.assertEquals(from_rendered_tx.outputs[0].amount, 30)

        self.assertEquals(from_rendered_tx.signatures[0], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")

