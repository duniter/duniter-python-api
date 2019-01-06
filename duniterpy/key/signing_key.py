"""
duniter public and private keys

@author: inso
"""
from re import compile, MULTILINE, search
from typing import Optional, Union, TypeVar, Type

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


# required to type hint cls in classmethod
SigningKeyType = TypeVar('SigningKeyType', bound='SigningKey')


class SigningKey(libnacl.sign.Signer):

    def __init__(self, seed: bytes) -> None:
        """
        Init pubkey property

        :param str seed: Hexadecimal seed string
        """
        super().__init__(seed)
        self.pubkey = Base58Encoder.encode(self.vk)

    @classmethod
    def from_credentials(cls: Type[SigningKeyType], salt: Union[str, bytes], password: Union[str, bytes],
                         scrypt_params: Optional[ScryptParams] = None) -> SigningKeyType:
        """
        Create a SigningKey object from credentials

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

        return cls(seed)

    def decrypt_seal(self, message: bytes) -> str:
        """
        Decrypt message with a curve25519 version of the ed25519 key pair

        :param message: Encrypted message

        :return:
        """
        curve25519_public_key = libnacl.crypto_sign_ed25519_pk_to_curve25519(self.vk)
        curve25519_secret_key = libnacl.crypto_sign_ed25519_sk_to_curve25519(self.sk)
        return libnacl.crypto_box_seal_open(message, curve25519_public_key, curve25519_secret_key).decode('utf-8')

    @classmethod
    def from_wif_file(cls: Type[SigningKeyType], path: str) -> SigningKeyType:
        """
        Return SigningKey instance from Duniter WIF v1 file

        :param path: Path to WIF file
        """
        with open(path, 'r') as fh:
            wif_content = fh.read()

        regex = compile('Data: ([1-9A-HJ-NP-Za-km-z]+)', MULTILINE)
        match = search(regex, wif_content)
        if not match:
            raise Exception('Error: Bad format WIF v1 file')

        wif_hex = match.groups()[0]
        wif_bytes = Base58Encoder.decode(wif_hex)
        if len(wif_bytes) != 35:
            raise Exception("Error: the size of WIF is invalid")

        checksum_from_wif = wif_bytes[-2:]
        fi = wif_bytes[0:1]
        seed = wif_bytes[1:-2]
        seed_fi = wif_bytes[0:-2]

        if fi != b"\x01":
            raise Exception("Error: bad WIF version")

        # checksum control
        checksum = libnacl.crypto_hash_sha256(libnacl.crypto_hash_sha256(seed_fi))[0:2]
        if checksum_from_wif != checksum:
            raise Exception("Error: bad checksum of the WIF")

        return cls(seed)

    def save_wif(self, path: str) -> None:
        """
        Save a Wallet Import Format file (v1)

        :param path: Path to file
        """
        # Cesium v1
        version = 1

        # add version to seed
        seed_fi = version.to_bytes(version, 'little') + self.seed

        # calculate checksum
        sha256_v1 = libnacl.crypto_hash_sha256(seed_fi)
        sha256_v2 = libnacl.crypto_hash_sha256(sha256_v1)
        checksum = sha256_v2[0:2]

        wif_key = Base58Encoder.encode(seed_fi + checksum)

        with open(path, 'w') as fh:
            fh.write(
                """Type: WIF
Version: {version}
Data: {data}""".format(version=1, data=wif_key)
            )
