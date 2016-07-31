"""
duniter public and private keys

@author: inso
"""

import libnacl.public
from pylibscrypt import scrypt
from .base58 import Base58Encoder
from .signing_key import _ensure_bytes


SEED_LENGTH = 32  # Length of the key
crypto_sign_BYTES = 64
SCRYPT_PARAMS = {'N': 4096,
                 'r': 16,
                 'p': 1
                 }


class SecretKey(libnacl.public.SecretKey):
    def __init__(self, salt, password):
        salt = _ensure_bytes(salt)
        password = _ensure_bytes(password)
        seed = scrypt(password, salt,
                    SCRYPT_PARAMS['N'], SCRYPT_PARAMS['r'], SCRYPT_PARAMS['p'],
                    SEED_LENGTH)

        super().__init__(seed)
        self.public_key = PublicKey(Base58Encoder.encode(self.pk))

    def encrypt(self, pubkey, noonce, text):
        text_bytes = _ensure_bytes(text)
        noonce_bytes = _ensure_bytes(noonce)
        recipient_pubkey = PublicKey(pubkey)
        crypt_bytes = libnacl.public.Box(self, recipient_pubkey).encrypt(text_bytes, noonce_bytes)
        return Base58Encoder.encode(crypt_bytes[24:])

    def decrypt(self, pubkey, noonce, text):
        sender_pubkey = PublicKey(pubkey)
        noonce_bytes = _ensure_bytes(noonce)
        encrypt_bytes = Base58Encoder.decode(text)
        decrypt_bytes = libnacl.public.Box(self, sender_pubkey).decrypt(encrypt_bytes, noonce_bytes)
        return decrypt_bytes.decode('utf-8')


class PublicKey(libnacl.public.PublicKey):
    def __init__(self, pubkey):
        key = Base58Encoder.decode(pubkey)
        super().__init__(key)

    def base58(self):
        return Base58Encoder.encode(self.pk)

