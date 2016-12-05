"""
duniter public and private keys

@author: inso
"""

import libnacl.sign
from pylibscrypt import scrypt
from .base58 import Base58Encoder


SEED_LENGTH = 32  # Length of the key
crypto_sign_BYTES = 64

class ScryptParams:
    def __init__(self, N, r, p):
        self.N = N
        self.r = r
        self.p = p

def _ensure_bytes(data):
    if isinstance(data, str):
        return bytes(data, 'utf-8')

    return data


class SigningKey(libnacl.sign.Signer):
    def __init__(self, salt, password, scrypt_params):
        salt = _ensure_bytes(salt)
        password = _ensure_bytes(password)
        seed = scrypt(password, salt,
                      scrypt_params.N, scrypt_params.r, scrypt_params.p,
                      SEED_LENGTH)

        super().__init__(seed)
        self.pubkey = Base58Encoder.encode(self.vk)
