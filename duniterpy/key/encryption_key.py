"""
duniter public and private keys

@author: inso
"""
from typing import Union

import libnacl.public
from pylibscrypt import scrypt

from .base58 import Base58Encoder
from ..helpers import ensure_bytes

SEED_LENGTH = 32  # Length of the key
crypto_sign_BYTES = 64
SCRYPT_PARAMS = {'N': 4096,
                 'r': 16,
                 'p': 1
                 }


class SecretKey(libnacl.public.SecretKey):
    """
    Raw Public Key Encryption Class
    """

    def __init__(self, salt: Union[str, bytes], password: Union[str, bytes]) -> None:
        """
        Create SecretKey key pair instance from salt and password credentials

        :param salt: Salt credential
        :param password: Password credential
        """
        salt = ensure_bytes(salt)
        password = ensure_bytes(password)
        seed = scrypt(password, salt,
                      SCRYPT_PARAMS['N'], SCRYPT_PARAMS['r'], SCRYPT_PARAMS['p'],
                      SEED_LENGTH)

        super().__init__(seed)
        self.public_key = PublicKey(Base58Encoder.encode(self.pk))

    def encrypt(self, pubkey: str, nonce: Union[str, bytes], text: Union[str, bytes]) -> str:
        """
        Encrypt message text with the public key of the recipient and a noonce

        The nonce must be a 24 character string (you can use libnacl.utils.rand_nonce() to get one)
        and unique for each encrypted message.

        Return base58 encoded encrypted message

        :param pubkey: Base58 encoded public key of the recipient
        :param nonce: Unique nonce
        :param text: Message to encrypt
        :return:
        """
        text_bytes = ensure_bytes(text)
        nonce_bytes = ensure_bytes(nonce)
        recipient_pubkey = PublicKey(pubkey)
        crypt_bytes = libnacl.public.Box(self, recipient_pubkey).encrypt(text_bytes, nonce_bytes)
        return Base58Encoder.encode(crypt_bytes[24:])

    def decrypt(self, pubkey: str, nonce: Union[str, bytes], text: str) -> str:
        """
        Decrypt encrypted message text with recipient public key and the unique nonce used by the sender.

        :param pubkey: Public key of the recipient
        :param nonce: Unique nonce used by the sender
        :param text: Encrypted message
        :return:
        """
        sender_pubkey = PublicKey(pubkey)
        nonce_bytes = ensure_bytes(nonce)
        encrypt_bytes = Base58Encoder.decode(text)
        decrypt_bytes = libnacl.public.Box(self, sender_pubkey).decrypt(encrypt_bytes, nonce_bytes)
        return decrypt_bytes.decode('utf-8')


class PublicKey(libnacl.public.PublicKey):
    def __init__(self, pubkey: str) -> None:
        """
        Create instance of libnacl ed25519 sign PublicKey from a base58 public key

        :param pubkey: Base58 public key
        """
        key = Base58Encoder.decode(pubkey)
        super().__init__(key)

    def base58(self) -> str:
        """
        Return a base58 encoded string of the public key
        """
        return Base58Encoder.encode(self.pk)

    def encrypt_seal(self, message: Union[str, bytes]) -> bytes:
        """
        Encrypt message with a curve25519 version of the ed25519 public key

        :param message: Message to encrypt
        """
        curve25519_public_key = libnacl.crypto_sign_ed25519_pk_to_curve25519(self.pk)
        return libnacl.crypto_box_seal(ensure_bytes(message), curve25519_public_key)
