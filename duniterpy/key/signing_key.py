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
        """
        Init a ScryptParams instance with crypto parameters

        :param int N: scrypt param N
        :param int r: scrypt param r
        :param int p: scrypt param p
        """
        self.N = N
        self.r = r
        self.p = p


def _ensure_bytes(data):
    """
    Convert data in bytes if data is a string

    :param data: Data
    :rtype bytes:
    """
    if isinstance(data, str):
        return bytes(data, 'utf-8')

    return data


class SigningKey(libnacl.sign.Signer):
    def __init__(self, salt, password, scrypt_params=None):
        """
        Init a SigningKey object from credentials

        :param str salt: Secret salt passphrase credential
        :param str password: Secret password credential
        :param ScryptParams scrypt_params: ScryptParams instance
        """
        if scrypt_params is None:
            scrypt_params = ScryptParams(4096, 16, 1)

        salt = _ensure_bytes(salt)
        password = _ensure_bytes(password)
        seed = scrypt(password, salt,
                      scrypt_params.N, scrypt_params.r, scrypt_params.p,
                      SEED_LENGTH)

        super().__init__(seed)
        self.pubkey = Base58Encoder.encode(self.vk)
