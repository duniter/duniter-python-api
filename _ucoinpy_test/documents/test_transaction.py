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

tx_raw = ("Version: 1\n"
          "Type: Transaction\n"
          "Currency: beta_brousouf\n"
          "Issuers:\n"
          "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY\n"
          "Inputs:\n"
          "0:T:65:D717FEC1993554F8EAE4CEA88DE5FBB6887CFAE8:4\n"
          "0:T:77:F80993776FB55154A60B3E58910C942A347964AD:15\n"
          "0:D:88:F4A47E39BC2A20EE69DCD5CAB0A9EB3C92FD8F7B:11\n"
          "Outputs:\n"
          "BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g:30\n"
          "Comment: \n"
          "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r\n")


class Test_Transaction(unittest.TestCase):
    def test_fromcompact(self):
        tx = Transaction.from_compact("zeta_brousouf", tx_compact)
        self.assertEqual(tx.version, 1)
        self.assertEqual(tx.currency, "zeta_brousouf")
        self.assertEqual(len(tx.issuers), 1)
        self.assertEqual(len(tx.inputs), 3)
        self.assertEqual(len(tx.outputs), 1)

        self.assertEqual(tx.issuers[0], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")

        self.assertEqual(tx.inputs[0].index, 0)
        self.assertEqual(tx.inputs[0].source, 'T')
        self.assertEqual(tx.inputs[0].number, 65)
        self.assertEqual(tx.inputs[0].txhash, "D717FEC1993554F8EAE4CEA88DE5FBB6887CFAE8")
        self.assertEqual(tx.inputs[0].amount, 4)

        self.assertEqual(tx.inputs[1].index, 0)
        self.assertEqual(tx.inputs[1].source, 'T')
        self.assertEqual(tx.inputs[1].number, 77)
        self.assertEqual(tx.inputs[1].txhash, "F80993776FB55154A60B3E58910C942A347964AD")
        self.assertEqual(tx.inputs[1].amount, 15)

        self.assertEqual(tx.inputs[2].index, 0)
        self.assertEqual(tx.inputs[2].source, 'D')
        self.assertEqual(tx.inputs[2].number, 88)
        self.assertEqual(tx.inputs[2].txhash, "F4A47E39BC2A20EE69DCD5CAB0A9EB3C92FD8F7B")
        self.assertEqual(tx.inputs[2].amount, 11)

        self.assertEqual(tx.outputs[0].pubkey, "BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g")
        self.assertEqual(tx.outputs[0].amount, 30)

        self.assertEqual(tx.signatures[0], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")

    def test_fromraw(self):
        tx = Transaction.from_signed_raw(tx_raw)
        self.assertEqual(tx.version, 1)
        self.assertEqual(tx.currency, "beta_brousouf")
        self.assertEqual(len(tx.issuers), 1)
        self.assertEqual(len(tx.inputs), 3)
        self.assertEqual(len(tx.outputs), 1)

        self.assertEqual(tx.issuers[0], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")

        self.assertEqual(tx.inputs[0].index, 0)
        self.assertEqual(tx.inputs[0].source, 'T')
        self.assertEqual(tx.inputs[0].number, 65)
        self.assertEqual(tx.inputs[0].txhash, "D717FEC1993554F8EAE4CEA88DE5FBB6887CFAE8")
        self.assertEqual(tx.inputs[0].amount, 4)

        self.assertEqual(tx.inputs[1].index, 0)
        self.assertEqual(tx.inputs[1].source, 'T')
        self.assertEqual(tx.inputs[1].number, 77)
        self.assertEqual(tx.inputs[1].txhash, "F80993776FB55154A60B3E58910C942A347964AD")
        self.assertEqual(tx.inputs[1].amount, 15)

        self.assertEqual(tx.inputs[2].index, 0)
        self.assertEqual(tx.inputs[2].source, 'D')
        self.assertEqual(tx.inputs[2].number, 88)
        self.assertEqual(tx.inputs[2].txhash, "F4A47E39BC2A20EE69DCD5CAB0A9EB3C92FD8F7B")
        self.assertEqual(tx.inputs[2].amount, 11)

        self.assertEqual(tx.outputs[0].pubkey, "BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g")
        self.assertEqual(tx.outputs[0].amount, 30)

        self.assertEqual(tx.signatures[0], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")

    def test_fromraw_toraw(self):
        tx = Transaction.from_signed_raw(tx_raw)
        rendered_tx = tx.signed_raw()
        from_rendered_tx = Transaction.from_signed_raw(rendered_tx)

        self.assertEqual(from_rendered_tx.version, 1)
        self.assertEqual(len(from_rendered_tx.issuers), 1)
        self.assertEqual(len(from_rendered_tx.inputs), 3)
        self.assertEqual(len(from_rendered_tx.outputs), 1)

        self.assertEqual(from_rendered_tx.issuers[0], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")

        self.assertEqual(from_rendered_tx.inputs[0].index, 0)
        self.assertEqual(from_rendered_tx.inputs[0].source, 'T')
        self.assertEqual(from_rendered_tx.inputs[0].number, 65)
        self.assertEqual(from_rendered_tx.inputs[0].txhash, "D717FEC1993554F8EAE4CEA88DE5FBB6887CFAE8")
        self.assertEqual(from_rendered_tx.inputs[0].amount, 4)

        self.assertEqual(from_rendered_tx.inputs[1].index, 0)
        self.assertEqual(from_rendered_tx.inputs[1].source, 'T')
        self.assertEqual(from_rendered_tx.inputs[1].number, 77)
        self.assertEqual(from_rendered_tx.inputs[1].txhash, "F80993776FB55154A60B3E58910C942A347964AD")
        self.assertEqual(from_rendered_tx.inputs[1].amount, 15)

        self.assertEqual(from_rendered_tx.inputs[2].index, 0)
        self.assertEqual(from_rendered_tx.inputs[2].source, 'D')
        self.assertEqual(from_rendered_tx.inputs[2].number, 88)
        self.assertEqual(from_rendered_tx.inputs[2].txhash, "F4A47E39BC2A20EE69DCD5CAB0A9EB3C92FD8F7B")
        self.assertEqual(from_rendered_tx.inputs[2].amount, 11)

        self.assertEqual(from_rendered_tx.outputs[0].pubkey, "BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g")
        self.assertEqual(from_rendered_tx.outputs[0].amount, 30)

        self.assertEqual(from_rendered_tx.signatures[0], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")

