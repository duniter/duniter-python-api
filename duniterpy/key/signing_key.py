"""
duniter public and private keys

@author: inso, vtexier, Moul
"""
import re
from typing import Optional, Union, TypeVar, Type

import libnacl.sign
import pyaes
from libnacl.utils import load_key
from pylibscrypt import scrypt

from .scrypt_params import ScryptParams
from .base58 import Base58Encoder
from ..tools import (
    ensure_bytes,
    xor_bytes,
    convert_seedhex_to_seed,
    convert_seed_to_seedhex,
)

# required to type hint cls in classmethod
SigningKeyType = TypeVar("SigningKeyType", bound="SigningKey")


class SigningKey(libnacl.sign.Signer):
    def __init__(self, seed: bytes) -> None:
        """
        Init pubkey property

        :param str seed: Hexadecimal seed string
        """
        super().__init__(seed)
        self.pubkey = Base58Encoder.encode(self.vk)

    @classmethod
    def from_credentials(
        cls: Type[SigningKeyType],
        salt: Union[str, bytes],
        password: Union[str, bytes],
        scrypt_params: Optional[ScryptParams] = None,
    ) -> SigningKeyType:
        """
        Create a SigningKey object from credentials

        :param salt: Secret salt passphrase credential
        :param password: Secret password credential
        :param scrypt_params: ScryptParams instance
        """
        if scrypt_params is None:
            scrypt_params = ScryptParams()

        salt = ensure_bytes(salt)
        password = ensure_bytes(password)
        seed = scrypt(
            password,
            salt,
            scrypt_params.N,
            scrypt_params.r,
            scrypt_params.p,
            scrypt_params.seed_length,
        )

        return cls(seed)

    def save_seedhex_file(self, path: str) -> None:
        """
        Save hexadecimal seed file from seed

        :param path: Authentication file path
        """
        seedhex = convert_seed_to_seedhex(self.seed)
        with open(path, "w") as fh:
            fh.write(seedhex)

    @staticmethod
    def from_seedhex_file(path: str) -> SigningKeyType:
        """
        Return SigningKey instance from Seedhex file

        :param str path: Hexadecimal seed file path
        """
        with open(path, "r") as fh:
            seedhex = fh.read()
        return SigningKey.from_seedhex(seedhex)

    @classmethod
    def from_seedhex(cls: Type[SigningKeyType], seedhex: str) -> SigningKeyType:
        """
        Return SigningKey instance from Seedhex

        :param str seedhex: Hexadecimal seed string
        """
        regex_seedhex = re.compile("([0-9a-fA-F]{64})")
        match = re.search(regex_seedhex, seedhex)
        if not match:
            raise Exception("Error: Bad seed hexadecimal format")
        seedhex = match.groups()[0]
        seed = convert_seedhex_to_seed(seedhex)
        return cls(seed)

    def save_private_key(self, path: str) -> None:
        """
        Save authentication file

        :param path: Authentication file path
        """
        self.save(path)

    @staticmethod
    def from_private_key(path: str) -> SigningKeyType:
        """
        Read authentication file
        Add public key attribute

        :param path: Authentication file path
        """
        key = load_key(path)
        key.pubkey = Base58Encoder.encode(key.vk)
        return key

    def decrypt_seal(self, data: bytes) -> bytes:
        """
        Decrypt bytes data with a curve25519 version of the ed25519 key pair

        :param data: Encrypted data

        :return:
        """
        curve25519_public_key = libnacl.crypto_sign_ed25519_pk_to_curve25519(self.vk)
        curve25519_secret_key = libnacl.crypto_sign_ed25519_sk_to_curve25519(self.sk)
        return libnacl.crypto_box_seal_open(
            data, curve25519_public_key, curve25519_secret_key
        )

    @classmethod
    def from_pubsec_file(cls: Type[SigningKeyType], path: str) -> SigningKeyType:
        """
        Return SigningKey instance from Duniter WIF file

        :param path: Path to WIF file
        """
        with open(path, "r") as fh:
            pubsec_content = fh.read()

        # line patterns
        regex_pubkey = re.compile("pub: ([1-9A-HJ-NP-Za-km-z]{43,44})", re.MULTILINE)
        regex_signkey = re.compile("sec: ([1-9A-HJ-NP-Za-km-z]{87,90})", re.MULTILINE)

        # check public key field
        match = re.search(regex_pubkey, pubsec_content)
        if not match:
            raise Exception("Error: Bad format PubSec v1 file, missing public key")

        # check signkey field
        match = re.search(regex_signkey, pubsec_content)
        if not match:
            raise Exception("Error: Bad format PubSec v1 file, missing sec key")

        # capture signkey
        signkey_hex = match.groups()[0]

        # extract seed from signkey
        seed = bytes(Base58Encoder.decode(signkey_hex)[0:32])

        return cls(seed)

    def save_pubsec_file(self, path: str) -> None:
        """
        Save a Duniter PubSec file (PubSec) v1

        :param path: Path to file
        """
        # version
        version = 1

        # base58 encode keys
        base58_signing_key = Base58Encoder.encode(self.sk)
        base58_public_key = self.pubkey

        # save file
        with open(path, "w") as fh:
            fh.write(
                """Type: PubSec
Version: {version}
pub: {pubkey}
sec: {signkey}""".format(
                    version=version,
                    pubkey=base58_public_key,
                    signkey=base58_signing_key,
                )
            )

    @staticmethod
    def from_wif_or_ewif_file(
        path: str, password: Optional[str] = None
    ) -> SigningKeyType:
        """
        Return SigningKey instance from Duniter WIF or EWIF file

        :param path: Path to WIF of EWIF file
        :param password: Password needed for EWIF file
        """
        with open(path, "r") as fh:
            wif_content = fh.read()

        # check data field
        regex = re.compile("Data: ([1-9A-HJ-NP-Za-km-z]+)", re.MULTILINE)
        match = re.search(regex, wif_content)
        if not match:
            raise Exception("Error: Bad format WIF or EWIF v1 file")

        # capture hexa wif key
        wif_hex = match.groups()[0]
        return SigningKey.from_wif_or_ewif_hex(wif_hex, password)

    @staticmethod
    def from_wif_or_ewif_hex(
        wif_hex: str, password: Optional[str] = None
    ) -> SigningKeyType:
        """
        Return SigningKey instance from Duniter WIF or EWIF in hexadecimal format

        :param wif_hex: WIF or EWIF string in hexadecimal format
        :param password: Password of EWIF encrypted seed
        """
        wif_bytes = Base58Encoder.decode(wif_hex)

        fi = wif_bytes[0:1]

        if fi == b"\x01":
            result = SigningKey.from_wif_hex(wif_hex)
        elif fi == b"\x02" and password is not None:
            result = SigningKey.from_ewif_hex(wif_hex, password)
        else:
            raise Exception("Error: Bad format: not WIF nor EWIF")

        return result

    @staticmethod
    def from_wif_file(path: str) -> SigningKeyType:
        """
        Return SigningKey instance from Duniter WIF file

        :param path: Path to WIF file
        """
        with open(path, "r") as fh:
            wif_content = fh.read()

        # check data field
        regex = re.compile("Data: ([1-9A-HJ-NP-Za-km-z]+)", re.MULTILINE)
        match = re.search(regex, wif_content)
        if not match:
            raise Exception("Error: Bad format WIF v1 file")

        # capture hexa wif key
        wif_hex = match.groups()[0]
        return SigningKey.from_wif_hex(wif_hex)

    @classmethod
    def from_wif_hex(cls: Type[SigningKeyType], wif_hex: str) -> SigningKeyType:
        """
        Return SigningKey instance from Duniter WIF in hexadecimal format

        :param wif_hex: WIF string in hexadecimal format
        """
        wif_bytes = Base58Encoder.decode(wif_hex)
        if len(wif_bytes) != 35:
            raise Exception("Error: the size of WIF is invalid")

        # extract data
        checksum_from_wif = wif_bytes[-2:]
        fi = wif_bytes[0:1]
        seed = wif_bytes[1:-2]
        seed_fi = wif_bytes[0:-2]

        # check WIF format flag
        if fi != b"\x01":
            raise Exception("Error: bad format version, not WIF")

        # checksum control
        checksum = libnacl.crypto_hash_sha256(libnacl.crypto_hash_sha256(seed_fi))[0:2]
        if checksum_from_wif != checksum:
            raise Exception("Error: bad checksum of the WIF")

        return cls(seed)

    def save_wif_file(self, path: str) -> None:
        """
        Save a Wallet Import Format file (WIF) v1

        :param path: Path to file
        """
        # version
        version = 1

        # add format to seed (1=WIF,2=EWIF)
        seed_fi = b"\x01" + self.seed

        # calculate checksum
        sha256_v1 = libnacl.crypto_hash_sha256(seed_fi)
        sha256_v2 = libnacl.crypto_hash_sha256(sha256_v1)
        checksum = sha256_v2[0:2]

        # base58 encode key and checksum
        wif_key = Base58Encoder.encode(seed_fi + checksum)

        with open(path, "w") as fh:
            fh.write(
                """Type: WIF
Version: {version}
Data: {data}""".format(
                    version=version, data=wif_key
                )
            )

    @staticmethod
    def from_ewif_file(path: str, password: str) -> SigningKeyType:
        """
        Return SigningKey instance from Duniter EWIF file

        :param path: Path to EWIF file
        :param password: Password of the encrypted seed
        """
        with open(path, "r") as fh:
            wif_content = fh.read()

        # check data field
        regex = re.compile("Data: ([1-9A-HJ-NP-Za-km-z]+)", re.MULTILINE)
        match = re.search(regex, wif_content)
        if not match:
            raise Exception("Error: Bad format EWIF v1 file")

        # capture ewif key
        ewif_hex = match.groups()[0]
        return SigningKey.from_ewif_hex(ewif_hex, password)

    @classmethod
    def from_ewif_hex(
        cls: Type[SigningKeyType], ewif_hex: str, password: str
    ) -> SigningKeyType:
        """
        Return SigningKey instance from Duniter EWIF in hexadecimal format

        :param ewif_hex: EWIF string in hexadecimal format
        :param password: Password of the encrypted seed
        """
        ewif_bytes = Base58Encoder.decode(ewif_hex)
        if len(ewif_bytes) != 39:
            raise Exception("Error: the size of EWIF is invalid")

        # extract data
        fi = ewif_bytes[0:1]
        checksum_from_ewif = ewif_bytes[-2:]
        ewif_no_checksum = ewif_bytes[0:-2]
        salt = ewif_bytes[1:5]
        encryptedhalf1 = ewif_bytes[5:21]
        encryptedhalf2 = ewif_bytes[21:37]

        # check format flag
        if fi != b"\x02":
            raise Exception("Error: bad format version, not EWIF")

        # checksum control
        checksum = libnacl.crypto_hash_sha256(
            libnacl.crypto_hash_sha256(ewif_no_checksum)
        )[0:2]
        if checksum_from_ewif != checksum:
            raise Exception("Error: bad checksum of the EWIF")

        # SCRYPT
        password_bytes = password.encode("utf-8")
        scrypt_seed = scrypt(password_bytes, salt, 16384, 8, 8, 64)
        derivedhalf1 = scrypt_seed[0:32]
        derivedhalf2 = scrypt_seed[32:64]

        # AES
        aes = pyaes.AESModeOfOperationECB(derivedhalf2)
        decryptedhalf1 = aes.decrypt(encryptedhalf1)
        decryptedhalf2 = aes.decrypt(encryptedhalf2)

        # XOR
        seed1 = xor_bytes(decryptedhalf1, derivedhalf1[0:16])
        seed2 = xor_bytes(decryptedhalf2, derivedhalf1[16:32])
        seed = bytes(seed1 + seed2)

        # Password Control
        signer = SigningKey(seed)
        salt_from_seed = libnacl.crypto_hash_sha256(
            libnacl.crypto_hash_sha256(Base58Encoder.decode(signer.pubkey))
        )[0:4]
        if salt_from_seed != salt:
            raise Exception("Error: bad Password of EWIF address")

        return cls(seed)

    def save_ewif_file(self, path: str, password: str) -> None:
        """
        Save an Encrypted Wallet Import Format file (WIF v2)

        :param path: Path to file
        :param password:
        """
        # version
        version = 1

        # add version to seed
        salt = libnacl.crypto_hash_sha256(
            libnacl.crypto_hash_sha256(Base58Encoder.decode(self.pubkey))
        )[0:4]

        # SCRYPT
        password_bytes = password.encode("utf-8")
        scrypt_seed = scrypt(password_bytes, salt, 16384, 8, 8, 64)
        derivedhalf1 = scrypt_seed[0:32]
        derivedhalf2 = scrypt_seed[32:64]

        # XOR
        seed1_xor_derivedhalf1_1 = bytes(xor_bytes(self.seed[0:16], derivedhalf1[0:16]))
        seed2_xor_derivedhalf1_2 = bytes(
            xor_bytes(self.seed[16:32], derivedhalf1[16:32])
        )

        # AES
        aes = pyaes.AESModeOfOperationECB(derivedhalf2)
        encryptedhalf1 = aes.encrypt(seed1_xor_derivedhalf1_1)
        encryptedhalf2 = aes.encrypt(seed2_xor_derivedhalf1_2)

        # add format to final seed (1=WIF,2=EWIF)
        seed_bytes = b"\x02" + salt + encryptedhalf1 + encryptedhalf2

        # calculate checksum
        sha256_v1 = libnacl.crypto_hash_sha256(seed_bytes)
        sha256_v2 = libnacl.crypto_hash_sha256(sha256_v1)
        checksum = sha256_v2[0:2]

        # B58 encode final key string
        ewif_key = Base58Encoder.encode(seed_bytes + checksum)

        # save file
        with open(path, "w") as fh:
            fh.write(
                """Type: EWIF
Version: {version}
Data: {data}""".format(
                    version=version, data=ewif_key
                )
            )
