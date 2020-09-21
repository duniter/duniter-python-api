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

from duniterpy.key import SigningKey, PublicKey
from duniterpy.key.scrypt_params import ScryptParams
import unittest


class TestPublicKey(unittest.TestCase):
    def test_encrypt_seal(self):
        sign_key = SigningKey.from_credentials("alice", "password", ScryptParams())
        public_key = PublicKey(sign_key.pubkey)

        message = "Hello world with utf-8 chars like éàè !"
        encrypted_message = public_key.encrypt_seal(bytes(message, "utf-8"))
        decrypted_message = sign_key.decrypt_seal(encrypted_message)
        self.assertEqual(message, decrypted_message.decode("utf-8"))
