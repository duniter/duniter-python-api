import base64
import re
from typing import Union, Type, TypeVar

from ..constants import PUBKEY_REGEX, SIGNATURE_REGEX, BLOCK_UID_REGEX
from .document import Document, MalformedDocumentError
from .identity import Identity

# required to type hint cls in classmethod
RevocationType = TypeVar("RevocationType", bound="Revocation")


class Revocation(Document):
    """
    A document describing a self-revocation.
    """

    re_inline = re.compile(
        "({pubkey_regex}):({signature_regex})\n".format(
            pubkey_regex=PUBKEY_REGEX, signature_regex=SIGNATURE_REGEX
        )
    )

    re_type = re.compile("Type: (Revocation)")
    re_issuer = re.compile(
        "Issuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX)
    )
    re_uniqueid = re.compile("IdtyUniqueID: ([^\n]+)\n")
    re_timestamp = re.compile(
        "IdtyTimestamp: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX)
    )
    re_idtysignature = re.compile(
        "IdtySignature: ({signature_regex})\n".format(signature_regex=SIGNATURE_REGEX)
    )

    fields_parsers = {
        **Document.fields_parsers,
        **{
            "Type": re_type,
            "Issuer": re_issuer,
            "IdtyUniqueID": re_uniqueid,
            "IdtyTimestamp": re_timestamp,
            "IdtySignature": re_idtysignature,
        },
    }

    def __init__(
        self,
        version: int,
        currency: str,
        identity: Union[Identity, str],
        signature: str,
    ) -> None:
        """
        Init Revocation instance

        :param version: Version number
        :param currency: Name of the currency
        :param identity: Identity instance or identity pubkey
        :param signature: Signature
        """
        super().__init__(version, currency, [signature])

        self.identity = identity if isinstance(identity, Identity) else None
        self.pubkey = identity.pubkey if isinstance(identity, Identity) else identity

    @classmethod
    def from_inline(
        cls: Type[RevocationType], version: int, currency: str, inline: str
    ) -> RevocationType:
        """
        Return Revocation document instance from inline string

        Only self.pubkey is populated.
        You must populate self.identity with an Identity instance to use raw/sign/signed_raw methods

        :param version: Version number
        :param currency: Name of the currency
        :param inline: Inline document

        :return:
        """
        cert_data = Revocation.re_inline.match(inline)
        if cert_data is None:
            raise MalformedDocumentError("Revokation")
        pubkey = cert_data.group(1)
        signature = cert_data.group(2)
        return cls(version, currency, pubkey, signature)

    @classmethod
    def from_signed_raw(cls: Type[RevocationType], signed_raw: str) -> RevocationType:
        """
        Return Revocation document instance from a signed raw string

        :param signed_raw: raw document file in duniter format
        :return:
        """
        lines = signed_raw.splitlines(True)
        n = 0

        version = int(Revocation.parse_field("Version", lines[n]))
        n += 1

        Revocation.parse_field("Type", lines[n])
        n += 1

        currency = Revocation.parse_field("Currency", lines[n])
        n += 1

        issuer = Revocation.parse_field("Issuer", lines[n])
        n += 1

        identity_uid = Revocation.parse_field("IdtyUniqueID", lines[n])
        n += 1

        identity_timestamp = Revocation.parse_field("IdtyTimestamp", lines[n])
        n += 1

        identity_signature = Revocation.parse_field("IdtySignature", lines[n])
        n += 1

        signature = Revocation.parse_field("Signature", lines[n])
        n += 1

        identity = Identity(
            version,
            currency,
            issuer,
            identity_uid,
            identity_timestamp,
            identity_signature,
        )

        return cls(version, currency, identity, signature)

    @staticmethod
    def extract_self_cert(signed_raw: str) -> Identity:
        """
        Return self-certified Identity instance from the signed raw Revocation document

        :param signed_raw: Signed raw document string
        :return:
        """
        lines = signed_raw.splitlines(True)
        n = 0

        version = int(Revocation.parse_field("Version", lines[n]))
        n += 1

        Revocation.parse_field("Type", lines[n])
        n += 1

        currency = Revocation.parse_field("Currency", lines[n])
        n += 1

        issuer = Revocation.parse_field("Issuer", lines[n])
        n += 1

        unique_id = Revocation.parse_field("IdtyUniqueID", lines[n])
        n += 1

        timestamp = Revocation.parse_field("IdtyTimestamp", lines[n])
        n += 1

        signature = Revocation.parse_field("IdtySignature", lines[n])
        n += 1

        return Identity(version, currency, issuer, unique_id, timestamp, signature)

    def inline(self) -> str:
        """
        Return inline document string

        :return:
        """
        return "{0}:{1}".format(self.pubkey, self.signatures[0])

    def raw(self) -> str:
        """
        Return Revocation raw document string

        :return:
        """
        if not isinstance(self.identity, Identity):
            raise MalformedDocumentError(
                "Can not return full revocation document created from inline"
            )

        return """Version: {version}
Type: Revocation
Currency: {currency}
Issuer: {pubkey}
IdtyUniqueID: {uid}
IdtyTimestamp: {timestamp}
IdtySignature: {signature}
""".format(
            version=self.version,
            currency=self.currency,
            pubkey=self.identity.pubkey,
            uid=self.identity.uid,
            timestamp=self.identity.timestamp,
            signature=self.identity.signatures[0],
        )

    def sign(self, keys: list) -> None:
        """
        Sign the current document.
        Warning : current signatures will be replaced with the new ones.

        :param keys: List of libnacl key instances
        :return:
        """
        if not isinstance(self.identity, Identity):
            raise MalformedDocumentError(
                "Can not return full revocation document created from inline"
            )

        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(), "ascii")))
            self.signatures.append(signing.decode("ascii"))

    def signed_raw(self) -> str:
        """
        Return Revocation signed raw document string

        :return:
        """
        if not isinstance(self.identity, Identity):
            raise MalformedDocumentError(
                "Can not return full revocation document created from inline"
            )

        raw = self.raw()
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw
