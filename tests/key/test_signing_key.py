import os

from duniterpy.key import VerifyingKey, SigningKey, PublicKey
from duniterpy.key.scrypt_params import ScryptParams
import unittest

TEST_FILE_PATH = '/tmp/test_file.txt'


class TestSigningKey(unittest.TestCase):

    def tearDown(self) -> None:
        super(TestSigningKey, self)

        # remove test file from disk
        if os.path.exists(TEST_FILE_PATH):
            os.unlink(TEST_FILE_PATH)

    def test_decrypt_seal(self):
        sign_key = SigningKey.from_credentials("alice", "password", ScryptParams())
        public_key = PublicKey(sign_key.pubkey)

        message = "Hello world with utf-8 chars like éàè !"
        encrypted_message = public_key.encrypt_seal(bytes(message, 'utf-8'))
        decrypted_message = sign_key.decrypt_seal(encrypted_message)
        self.assertEqual(message, decrypted_message.decode('utf-8'))

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