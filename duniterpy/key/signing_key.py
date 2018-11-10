"""
duniter public and private keys

@author: inso
"""
from typing import Optional, Union

import libnacl.sign
from pylibscrypt import scrypt

from .base58 import Base58Encoder
from ..helpers import ensure_bytes

SEED_LENGTH = 32  # Length of the key
crypto_sign_BYTES = 64


class ScryptParams:
    def __init__(self, n: int, r: int, p: int) -> None:
        """
        Init a ScryptParams instance with crypto parameters

        :param n: scrypt param N
        :param r: scrypt param r
        :param p: scrypt param p
        """
        self.N = n
        self.r = r
        self.p = p


class SigningKey(libnacl.sign.Signer):
    def __init__(self, salt: Union[str, bytes], password: Union[str, bytes],
                 scrypt_params: Optional[ScryptParams] = None) -> None:
        """
        Init a SigningKey object from credentials

        :param salt: Secret salt passphrase credential
        :param password: Secret password credential
        :param scrypt_params: ScryptParams instance
        """
        if scrypt_params is None:
            scrypt_params = ScryptParams(4096, 16, 1)

        salt = ensure_bytes(salt)
        password = ensure_bytes(password)
        seed = scrypt(password, salt,
                      scrypt_params.N, scrypt_params.r, scrypt_params.p,
                      SEED_LENGTH)

        super().__init__(seed)
        self.pubkey = Base58Encoder.encode(self.vk)

    def decrypt_seal(self, message: bytes) -> str:
        """
        Decrypt message with a curve25519 version of the ed25519 key pair

        :param message: Encrypted message

        :return:
        """
        curve25519_public_key = libnacl.crypto_sign_ed25519_pk_to_curve25519(self.vk)
        curve25519_secret_key = libnacl.crypto_sign_ed25519_sk_to_curve25519(self.sk)
        return libnacl.crypto_box_seal_open(message, curve25519_public_key, curve25519_secret_key).decode('utf-8')
