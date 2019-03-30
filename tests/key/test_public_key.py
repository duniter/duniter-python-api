from duniterpy.key import SigningKey, PublicKey
from duniterpy.key.scrypt_params import ScryptParams
import unittest


class TestPublicKey(unittest.TestCase):
    def test_encrypt_seal(self):
        sign_key = SigningKey.from_credentials("alice", "password", ScryptParams())
        public_key = PublicKey(sign_key.pubkey)

        message = "Hello world with utf-8 chars like éàè !"
        encrypted_message = public_key.encrypt_seal(bytes(message, 'utf-8'))
        decrypted_message = sign_key.decrypt_seal(encrypted_message)
        self.assertEqual(message, decrypted_message.decode('utf-8'))
