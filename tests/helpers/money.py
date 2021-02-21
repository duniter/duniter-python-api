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
from operator import eq, ne, lt, ge
from duniterpy.helpers.money import output_available
from duniterpy.grammars.output import SIG, XHX, CLTV, CSV
from duniterpy.documents.transaction import OutputSource


class TestHelpersMoney(unittest.TestCase):
    def test_output_available(self):
        """
        Only tests for single condition without operators
        """
        # SIG
        pubkey = "GB8iMAzq1DNmFe3ZxFTBQkGhq4fszTg1gZvx3XCkZXYH"
        sig_condition = SIG.token(pubkey).compose()
        condition = OutputSource.condition_from_text(sig_condition)

        self.assertTrue(output_available(condition, eq, pubkey))
        self.assertFalse(output_available(condition, ne, pubkey))

        # XHX
        sha_hash = "309BC5E644F797F53E5A2065EAF38A173437F2E6"
        xhx_condition = XHX.token(sha_hash).compose()
        condition = OutputSource.condition_from_text(xhx_condition)

        self.assertTrue(output_available(condition, eq, sha_hash))
        self.assertFalse(output_available(condition, ne, sha_hash))

        # CSV
        time = 1654300
        csv_condition = CSV.token(time).compose()
        condition = OutputSource.condition_from_text(csv_condition)

        self.assertTrue(output_available(condition, ge, time))
        self.assertFalse(output_available(condition, lt, time))

        # CLTV
        timestamp = 2594024
        cltv_condition = CLTV.token(timestamp).compose()
        condition = OutputSource.condition_from_text(cltv_condition)

        self.assertTrue(output_available(condition, ge, timestamp))
        self.assertFalse(output_available(condition, lt, timestamp))
