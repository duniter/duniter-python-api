import base64
import logging
import re
from typing import Optional, TypeVar, Type, Union

from .identity import Identity
from .block_uid import BlockUID
from ..constants import (
    PUBKEY_REGEX,
    SIGNATURE_REGEX,
    BLOCK_ID_REGEX,
    BLOCK_UID_REGEX,
    UID_REGEX,
)
from .document import Document, MalformedDocumentError


# required to type hint cls in classmethod
CertificationType = TypeVar("CertificationType", bound="Certification")


class Certification(Document):
    """
    A document describing a certification.
    """

    re_inline = re.compile(
        "({certifier_regex}):({certified_regex}):({block_id_regex}):({signature_regex})\n".format(
            certifier_regex=PUBKEY_REGEX,
            certified_regex=PUBKEY_REGEX,
            block_id_regex=BLOCK_ID_REGEX,
            signature_regex=SIGNATURE_REGEX,
        )
    )
    re_timestamp = re.compile(
        "META:TS:({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX)
    )
    re_type = re.compile("Type: (Certification)")
    re_issuer = re.compile(
        "Issuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX)
    )
    re_idty_issuer = re.compile(
        "IdtyIssuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX)
    )
    re_idty_unique_id = re.compile(
        "IdtyUniqueID: ({uid_regex})\n".format(uid_regex=UID_REGEX)
    )
    re_idty_timestamp = re.compile(
        "IdtyTimestamp: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX)
    )
    re_idty_signature = re.compile(
        "IdtySignature: ({signature_regex})\n".format(signature_regex=SIGNATURE_REGEX)
    )
    re_cert_timestamp = re.compile(
        "CertTimestamp: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX)
    )

    fields_parsers = {
        **Document.fields_parsers,
        **{
            "Type": re_type,
            "Issuer": re_issuer,
            "CertTimestamp": re_cert_timestamp,
            "IdtyIssuer": re_idty_issuer,
            "IdtyUniqueID": re_idty_unique_id,
            "IdtySignature": re_idty_signature,
            "IdtyTimestamp": re_idty_timestamp,
        },
    }

    def __init__(
        self,
        version: int,
        currency: str,
        pubkey_from: str,
        identity: Union[Identity, str],
        timestamp: BlockUID,
        signature: str,
    ) -> None:
        """
        Constructor

        :param version: the UCP version
        :param currency: the currency of the blockchain
        :param pubkey_from: Pubkey of the certifier
        :param identity: Document instance of the certified identity or identity pubkey string
        :param timestamp: the blockuid
        :param signature: the signature of the document
        """
        super().__init__(version, currency, [signature])
        self.pubkey_from = pubkey_from
        self.identity = identity if isinstance(identity, Identity) else None
        self.pubkey_to = identity.pubkey if isinstance(identity, Identity) else identity
        self.timestamp = timestamp

    @classmethod
    def from_signed_raw(
        cls: Type[CertificationType], signed_raw: str
    ) -> CertificationType:
        """
        Return Certification instance from signed raw document

        :param signed_raw: Signed raw document
        :return:
        """
        n = 0
        lines = signed_raw.splitlines(True)

        version = int(Identity.parse_field("Version", lines[n]))
        n += 1

        Certification.parse_field("Type", lines[n])
        n += 1

        currency = Certification.parse_field("Currency", lines[n])
        n += 1

        pubkey_from = Certification.parse_field("Issuer", lines[n])
        n += 1

        identity_pubkey = Certification.parse_field("IdtyIssuer", lines[n])
        n += 1

        identity_uid = Certification.parse_field("IdtyUniqueID", lines[n])
        n += 1

        identity_timestamp = BlockUID.from_str(
            Certification.parse_field("IdtyTimestamp", lines[n])
        )
        n += 1

        identity_signature = Certification.parse_field("IdtySignature", lines[n])
        n += 1

        timestamp = BlockUID.from_str(
            Certification.parse_field("CertTimestamp", lines[n])
        )
        n += 1

        signature = Certification.parse_field("Signature", lines[n])

        identity = Identity(
            version,
            currency,
            identity_pubkey,
            identity_uid,
            identity_timestamp,
            identity_signature,
        )

        return cls(version, currency, pubkey_from, identity, timestamp, signature)

    @classmethod
    def from_inline(
        cls: Type[CertificationType],
        version: int,
        currency: str,
        blockhash: Optional[str],
        inline: str,
    ) -> CertificationType:
        """
        Return Certification instance from inline document

        Only self.pubkey_to is populated.
        You must populate self.identity with an Identity instance to use raw/sign/signed_raw methods

        :param version: Version of document
        :param currency: Name of the currency
        :param blockhash: Hash of the block
        :param inline: Inline document
        :return:
        """
        cert_data = Certification.re_inline.match(inline)
        if cert_data is None:
            raise MalformedDocumentError("Certification ({0})".format(inline))
        pubkey_from = cert_data.group(1)
        pubkey_to = cert_data.group(2)
        blockid = int(cert_data.group(3))
        if blockid == 0 or blockhash is None:
            timestamp = BlockUID.empty()
        else:
            timestamp = BlockUID(blockid, blockhash)

        signature = cert_data.group(4)
        return cls(version, currency, pubkey_from, pubkey_to, timestamp, signature)

    def raw(self) -> str:
        """
        Return a raw document of the certification
        """
        if not isinstance(self.identity, Identity):
            raise MalformedDocumentError(
                "Can not return full certification document created from inline"
            )

        return """Version: {version}
Type: Certification
Currency: {currency}
Issuer: {issuer}
IdtyIssuer: {certified_pubkey}
IdtyUniqueID: {certified_uid}
IdtyTimestamp: {certified_ts}
IdtySignature: {certified_signature}
CertTimestamp: {timestamp}
""".format(
            version=self.version,
            currency=self.currency,
            issuer=self.pubkey_from,
            certified_pubkey=self.identity.pubkey,
            certified_uid=self.identity.uid,
            certified_ts=self.identity.timestamp,
            certified_signature=self.identity.signatures[0],
            timestamp=self.timestamp,
        )

    def sign(self, keys: list) -> None:
        """
        Sign the current document with the keys for the certified Identity given

        Warning : current signatures will be replaced with the new ones.

        :param keys: List of libnacl key instances
        """
        if not isinstance(self.identity, Identity):
            raise MalformedDocumentError(
                "Can not return full certification document created from inline"
            )

        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(), "ascii")))
            logging.debug("Signature : \n%s", signing.decode("ascii"))
            self.signatures.append(signing.decode("ascii"))

    def signed_raw(self) -> str:
        """
        Return signed raw document of the certification for the certified Identity instance

        :return:
        """
        if not isinstance(self.identity, Identity):
            raise MalformedDocumentError(
                "Can not return full certification document created from inline"
            )

        raw = self.raw()
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw

    def inline(self) -> str:
        """
        Return inline document string

        :return:
        """
        return "{0}:{1}:{2}:{3}".format(
            self.pubkey_from, self.pubkey_to, self.timestamp.number, self.signatures[0]
        )
