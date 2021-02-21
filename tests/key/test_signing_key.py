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

import os

from duniterpy.key import VerifyingKey, SigningKey, PublicKey
from duniterpy.key.scrypt_params import ScryptParams
import unittest

TEST_FILE_PATH = "/tmp/test_file.txt"


class TestSigningKey(unittest.TestCase):
    def tearDown(self) -> None:
        super()

        # remove test file from disk
        if os.path.exists(TEST_FILE_PATH):
            os.unlink(TEST_FILE_PATH)

    def test_decrypt_seal(self):
        sign_key = SigningKey.from_credentials("alice", "password", ScryptParams())
        public_key = PublicKey(sign_key.pubkey)

        message = "Hello world with utf-8 chars like éàè !"
        encrypted_message = public_key.encrypt_seal(bytes(message, "utf-8"))
        decrypted_message = sign_key.decrypt_seal(encrypted_message)
        self.assertEqual(message, decrypted_message.decode("utf-8"))

    def test_from_credentials(self):
        sign_key = SigningKey.from_credentials("alice", "password", ScryptParams())
        verify_key = VerifyingKey(sign_key.pubkey)
        self.assertEqual(verify_key.vk, sign_key.vk)

    def test_save_and_load_from_seedhex_file(self):
        sign_key_save = SigningKey.from_credentials("alice", "password", ScryptParams())
        sign_key_save.save_seedhex_file(TEST_FILE_PATH)

        sign_key_load = SigningKey.from_seedhex_file(TEST_FILE_PATH)
        self.assertEqual(sign_key_save.sk, sign_key_load.sk)

    def test_save_and_load_from_pubsec_file(self):
        sign_key_save = SigningKey.from_credentials("alice", "password", ScryptParams())
        sign_key_save.save_pubsec_file(TEST_FILE_PATH)

        sign_key_load = SigningKey.from_pubsec_file(TEST_FILE_PATH)
        self.assertEqual(sign_key_save.sk, sign_key_load.sk)

    def test_save_and_load_from_wif_file(self):
        sign_key_save = SigningKey.from_credentials("alice", "password", ScryptParams())
        sign_key_save.save_wif_file(TEST_FILE_PATH)

        sign_key_load = SigningKey.from_wif_file(TEST_FILE_PATH)
        self.assertEqual(sign_key_save.sk, sign_key_load.sk)

    def test_save_and_load_from_private_key_file(self):
        sign_key_save = SigningKey.from_credentials("alice", "password", ScryptParams())
        sign_key_save.save_private_key(TEST_FILE_PATH)

        sign_key_load = SigningKey.from_private_key(TEST_FILE_PATH)
        self.assertEqual(sign_key_save.sk, sign_key_load.sk)

    def test_save_and_load_from_ewif_file(self):
        sign_key_save = SigningKey.from_credentials("alice", "password", ScryptParams())
        sign_key_save.save_ewif_file(TEST_FILE_PATH, "password")

        sign_key_load = SigningKey.from_ewif_file(TEST_FILE_PATH, "password")
        self.assertEqual(sign_key_save.sk, sign_key_load.sk)

    def test_save_ewif_and_load_from_ewif_or_wif_file(self):
        sign_key_save = SigningKey.from_credentials("alice", "password", ScryptParams())
        sign_key_save.save_ewif_file(TEST_FILE_PATH, "password")

        sign_key_load = SigningKey.from_wif_or_ewif_file(TEST_FILE_PATH, "password")
        self.assertEqual(sign_key_save.sk, sign_key_load.sk)

    def test_save_wif_and_load_from_ewif_or_wif_file(self):
        sign_key_save = SigningKey.from_credentials("alice", "password", ScryptParams())
        sign_key_save.save_wif_file(TEST_FILE_PATH)

        sign_key_load = SigningKey.from_wif_or_ewif_file(TEST_FILE_PATH)
        self.assertEqual(sign_key_save.sk, sign_key_load.sk)

    def test_load_credentials_file(self):
        salt = password = "test"

        # create a dummy credentials file
        with open(TEST_FILE_PATH, "w") as fh:
            fh.write("{}\n{}\n".format(salt, password))

        # same key from credentials
        sign_key_test = SigningKey.from_credentials(salt, password)

        # test load file
        sign_key_load = SigningKey.from_credentials_file(TEST_FILE_PATH)
        self.assertEqual(sign_key_test.sk, sign_key_load.sk)
        self.assertEqual(sign_key_test.pubkey, sign_key_load.pubkey)
        self.assertEqual(sign_key_test.vk, sign_key_load.vk)

    def test_load_ssb_file(self):
        dummy_content = """
        # comments
        #
        #
        
        {
            "curve": "ed25519",
            "public": "dGVzdHRlc3R0ZXN0dGV0c3RldHN0dGV0c3RldGV0ZXRldHN0ZXR0c3RldHN0dGV0c3Q=.ed25519",
            "private": "dGVzdHRlc3R0ZXN0dGV0c3RldHN0dGV0c3RldGV0ZXRldHN0ZXR0c3RldHN0dGV0c3Q==.ed25519",
            "id": "@qJ8qVfXU2mIWG9WfKIRsd6GDscQlErzPHsxzHcyQMWQ=.ed25519"
        }
        
        #
        # comments
        """

        # create dummy .ssb/secret file
        with open(TEST_FILE_PATH, "w") as fh:
            fh.write(dummy_content)
        # test load file
        sign_key_load = SigningKey.from_credentials_file(TEST_FILE_PATH)
        self.assertEqual(
            sign_key_load.pubkey, "FAhCeyWq2Ni2xZS3hmYk5w95f8ELxNhUVvU5VB2LXy49"
        )
        self.assertEqual(
            sign_key_load.sk.hex(),
            "f2f7ae68635dba3455390a74ca0811e4c06142229bb58556aaa37d5598548c9ed27f4cb2bfadbaf45b61714b896d4639ab90db035aee746611cdd342bdaa8996",
        )
        self.assertEqual(
            sign_key_load.vk.hex(),
            "d27f4cb2bfadbaf45b61714b896d4639ab90db035aee746611cdd342bdaa8996",
        )
