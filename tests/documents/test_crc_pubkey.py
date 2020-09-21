"""
Copyright  2014-2020 Vincent Texier <vit@free.fr>

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
from duniterpy.documents.crc_pubkey import CRCPubkey


class TestCRCPubkey(unittest.TestCase):
    def test_from_pubkey(self):
        crc_pubkey = CRCPubkey.from_pubkey(
            "J4c8CARmP9vAFNGtHRuzx14zvxojyRWHW2darguVqjtX"
        )
        self.assertEqual(crc_pubkey.crc, "KAv")
