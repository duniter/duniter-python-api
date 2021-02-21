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

from duniterpy.key import SecretKey
import unittest


class TestEncryptionKey(unittest.TestCase):
    def test_from_bob_to_alice(self):
        bob_secret_key = SecretKey("bob", "password")
        alice_secret_key = SecretKey("alice", "password")
        text = "Relatively ciphered text"
        noonce = "00005D6FC6E22FB308D8815A565A01C66FFB7DC761D616DE0698F6322565F1D6"[:24]
        bob_to_alice = bob_secret_key.encrypt(
            alice_secret_key.public_key.base58(), noonce, text
        )
        alice_from_bob = alice_secret_key.decrypt(
            bob_secret_key.public_key.base58(), noonce, bob_to_alice
        )
        self.assertEqual(alice_from_bob, text)
