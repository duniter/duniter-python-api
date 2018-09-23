import base64
import logging
import re
from typing import Optional, TypeVar, Type, List

from duniterpy.documents import BlockUID
from ..constants import PUBKEY_REGEX, SIGNATURE_REGEX, BLOCK_ID_REGEX, BLOCK_UID_REGEX, UID_REGEX
from .document import Document, MalformedDocumentError

# required to type hint cls in classmethod
IdentityType = TypeVar('IdentityType', bound='Identity')


class Identity(Document):
    """
    A document describing a self certification.
    """

    re_inline = re.compile("({pubkey_regex}):({signature_regex}):({block_uid_regex}):([^\n]+)\n"
                           .format(pubkey_regex=PUBKEY_REGEX,
                                   signature_regex=SIGNATURE_REGEX,
                                   block_uid_regex=BLOCK_UID_REGEX))
    re_type = re.compile("Type: (Identity)")
    re_issuer = re.compile("Issuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX))
    re_unique_id = re.compile("UniqueID: ({uid_regex})\n".format(uid_regex=UID_REGEX))
    re_uid = re.compile("UID:([^\n]+)\n")
    re_meta_ts = re.compile("META:TS:({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX))
    re_timestamp = re.compile("Timestamp: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX))

    fields_parsers = {**Document.fields_parsers, **{
        "Type": re_type,
        "UniqueID": re_unique_id,
        "Issuer": re_issuer,
        "Timestamp": re_timestamp
    }}

    def __init__(self, version: int, currency: str, pubkey: str, uid: str, ts: BlockUID,
                 signature: Optional[str]) -> None:
        """
        Create an identity document

        :param version: Version of the document
        :param currency: Name of the currency
        :param pubkey:  Public key of the account linked to the identity
        :param uid: Unique identifier
        :param ts: Block timestamp
        :param signature: Signature of the document
        """
        if signature:
            super().__init__(version, currency, [signature])
        else:
            super().__init__(version, currency, [])
        self.pubkey = pubkey
        self.timestamp = ts
        self.uid = uid

    @classmethod
    def from_inline(cls: Type[IdentityType], version: int, currency: str, inline: str) -> IdentityType:
        """
        Return Identity instance from inline Identity string
        :param version: Document version number
        :param currency: Name of the currency
        :param inline: Inline string of the Identity
        :return:
        """
        from .block import BlockUID

        selfcert_data = Identity.re_inline.match(inline)
        if selfcert_data is None:
            raise MalformedDocumentError("Inline self certification")
        pubkey = selfcert_data.group(1)
        signature = selfcert_data.group(2)
        ts = BlockUID.from_str(selfcert_data.group(3))
        uid = selfcert_data.group(4)

        return cls(version, currency, pubkey, uid, ts, signature)

    @classmethod
    def from_signed_raw(cls: Type[IdentityType], signed_raw: str) -> IdentityType:
        """
        Return Identity instance from a signed_raw string
        :param signed_raw: Signed raw document
        :return:
        """
        from .block import BlockUID

        n = 0
        lines = signed_raw.splitlines(True)

        version = int(Identity.parse_field("Version", lines[n]))
        n += 1

        Identity.parse_field("Type", lines[n])
        n += 1

        currency = Identity.parse_field("Currency", lines[n])
        n += 1

        pubkey = Identity.parse_field("Issuer", lines[n])
        n += 1

        uid = Identity.parse_field("UniqueID", lines[n])
        n += 1

        ts = BlockUID.from_str(Identity.parse_field("Timestamp", lines[n]))
        n += 1

        signature = Identity.parse_field("Signature", lines[n])

        return cls(version, currency, pubkey, uid, ts, signature)

    def raw(self) -> str:
        """
        Return a raw document of the Identity
        :return:
        """
        return """Version: {version}
Type: Identity
Currency: {currency}
Issuer: {pubkey}
UniqueID: {uid}
Timestamp: {timestamp}
""".format(version=self.version,
           currency=self.currency,
           pubkey=self.pubkey,
           uid=self.uid,
           timestamp=self.timestamp)

    def inline(self) -> str:
        """
        Return an inline string of the Identity
        :return:
        """
        return "{pubkey}:{signature}:{timestamp}:{uid}".format(
            pubkey=self.pubkey,
            signature=self.signatures[0],
            timestamp=self.timestamp,
            uid=self.uid)


# required to type hint cls in classmethod
CertificationType = TypeVar('CertificationType', bound='Certification')


class Certification(Document):
    """
    A document describing a certification.
    """

    re_inline = re.compile("({certifier_regex}):({certified_regex}):({block_id_regex}):({signature_regex})\n".format(
        certifier_regex=PUBKEY_REGEX,
        certified_regex=PUBKEY_REGEX,
        block_id_regex=BLOCK_ID_REGEX,
        signature_regex=SIGNATURE_REGEX
    ))
    re_timestamp = re.compile("META:TS:({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX))
    re_type = re.compile("Type: (Certification)")
    re_issuer = re.compile("Issuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX))
    re_idty_issuer = re.compile("IdtyIssuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX))
    re_idty_unique_id = re.compile("IdtyUniqueID: ({uid_regex})\n".format(uid_regex=UID_REGEX))
    re_idty_timestamp = re.compile("IdtyTimestamp: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX))
    re_idty_signature = re.compile("IdtySignature: ({signature_regex})\n".format(signature_regex=SIGNATURE_REGEX))
    re_cert_timestamp = re.compile("CertTimestamp: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX))

    fields_parsers = {**Document.fields_parsers, **{
        "Type": re_type,
        "Issuer": re_issuer,
        "CertTimestamp": re_cert_timestamp,
        "IdtyIssuer": re_idty_issuer,
        "IdtyUniqueID": re_idty_unique_id,
        "IdtySignature": re_idty_signature,
        "IdtyTimestamp": re_idty_timestamp
    }}

    def __init__(self, version: int, currency: str, pubkey_from: str, pubkey_to: str,
                 timestamp: BlockUID, signature: str) -> None:
        """
        Constructor

        :param version: the UCP version
        :param currency: the currency of the blockchain
        :param pubkey_from: Pubkey of the certifier
        :param pubkey_to: Pubkey of the certified
        :param timestamp: the blockuid
        :param signature: the signature of the document
        """
        super().__init__(version, currency, [signature])
        self.pubkey_from = pubkey_from
        self.pubkey_to = pubkey_to
        self.timestamp = timestamp

    @classmethod
    def from_signed_raw(cls: Type[CertificationType], signed_raw: str) -> CertificationType:
        """
        Return Certification instance from signed raw document

        :param signed_raw: Signed raw document
        :return:
        """
        from .block import BlockUID

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

        pubkey_to = Certification.parse_field("IdtyIssuer", lines[n])
        n += 1

        Certification.parse_field("IdtyUniqueID", lines[n])
        n += 1

        BlockUID.from_str(Certification.parse_field("IdtyTimestamp", lines[n]))
        n += 1

        Certification.parse_field("IdtySignature", lines[n])
        n += 1

        timestamp = BlockUID.from_str(Certification.parse_field("CertTimestamp", lines[n]))
        n += 1

        signature = Certification.parse_field("Signature", lines[n])

        return cls(version, currency, pubkey_from, pubkey_to, timestamp, signature)

    @classmethod
    def from_inline(cls: Type[CertificationType], version: int, currency: str, blockhash: Optional[str],
                    inline: str) -> CertificationType:
        """
        Return Certification instance from inline document

        :param version: Version of document
        :param currency: Name of the currency
        :param blockhash: Hash of the block
        :param inline: Inline document
        :return:
        """
        from .block import BlockUID
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

    def raw_for_certified(self, certified: Identity) -> str:
        """
        Return a raw document of the self-certification of the Identity

        :param Identity certified: Identity document instance
        :return:
        """
        return """Version: {version}
Type: Certification
Currency: {currency}
Issuer: {issuer}
IdtyIssuer: {certified_pubkey}
IdtyUniqueID: {certified_uid}
IdtyTimestamp: {certified_ts}
IdtySignature: {certified_signature}
CertTimestamp: {timestamp}
""".format(version=self.version,
           currency=self.currency,
           issuer=self.pubkey_from,
           certified_pubkey=certified.pubkey,
           certified_uid=certified.uid,
           certified_ts=certified.timestamp,
           certified_signature=certified.signatures[0],
           timestamp=self.timestamp)

    def sign_for_certified(self, certified: Identity, keys: list) -> None:
        """
        Sign the current document with the keys for the certified Identity given

        Warning : current signatures will be replaced with the new ones.

        :param certified: Identity instance certified
        :param keys: List of libnacl key instances
        """
        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw_for_certified(certified), 'ascii')))
            logging.debug("Signature : \n{0}".format(signing.decode("ascii")))
            self.signatures.append(signing.decode("ascii"))

    def signed_raw_for_certified(self, certified: Identity) -> str:
        """
        Return signed raw document of the certification for the certified Identity instance

        :param certified: Certified Identity instance
        :return:
        """
        raw = self.raw_for_certified(certified)
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw

    def inline(self) -> str:
        """
        Return inline document string

        :return:
        """
        return "{0}:{1}:{2}:{3}".format(self.pubkey_from, self.pubkey_to,
                                        self.timestamp.number, self.signatures[0])


# required to type hint cls in classmethod
RevocationType = TypeVar('RevocationType', bound='Revocation')


class Revocation(Document):
    """
    A document describing a self-revocation.
    """
    re_inline = re.compile("({pubkey_regex}):({signature_regex})\n".format(
        pubkey_regex=PUBKEY_REGEX,
        signature_regex=SIGNATURE_REGEX
    ))

    re_type = re.compile("Type: (Revocation)")
    re_issuer = re.compile("Issuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX))
    re_uniqueid = re.compile("IdtyUniqueID: ([^\n]+)\n")
    re_timestamp = re.compile("IdtyTimestamp: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX))
    re_idtysignature = re.compile("IdtySignature: ({signature_regex})\n".format(signature_regex=SIGNATURE_REGEX))

    fields_parsers = {**Document.fields_parsers, **{
        "Type": re_type,
        "Issuer": re_issuer,
        "IdtyUniqueID": re_uniqueid,
        "IdtyTimestamp": re_timestamp,
        "IdtySignature": re_idtysignature,
    }}

    def __init__(self, version: int, currency: str, pubkey: str, signature: str) -> None:
        """
        Init Revocation instance

        :param version: Version number
        :param currency: Name of the currency
        :param pubkey: Public key of the issuer
        :param signature: Signature
        """
        super().__init__(version, currency, [signature])
        self.pubkey = pubkey

    @classmethod
    def from_inline(cls: Type[RevocationType], version: int, currency: str, inline: str) -> RevocationType:
        """
        Return Revocation document instance from inline string

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
        n += 4

        signature = Revocation.parse_field("Signature", lines[n])
        n += 1

        return cls(version, currency, issuer, signature)

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

    def raw_for_revoked(self, revoked: Identity) -> str:
        """
        Return Revocation raw document string from Identity instance

        :param Identity revoked: Identity instance
        :return:
        """
        return """Version: {version}
Type: Revocation
Currency: {currency}
Issuer: {pubkey}
IdtyUniqueID: {uid}
IdtyTimestamp: {timestamp}
IdtySignature: {signature}
""".format(version=self.version,
           currency=self.currency,
           pubkey=revoked.pubkey,
           uid=revoked.uid,
           timestamp=revoked.timestamp,
           signature=revoked.signatures[0])

    def sign_for_revoked(self, revoked: Identity, keys: list) -> None:
        """
        Sign the current document.
        Warning : current signatures will be replaced with the new ones.

        :param revoked: Identity instance
        :param keys: List of libnacl key instances
        :return:
        """
        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw_for_revoked(revoked), 'ascii')))
            self.signatures.append(signing.decode("ascii"))

    def signed_raw_for_revoked(self, revoked: Identity) -> str:
        """
        Return Revocation signed raw document string for revoked Identity instance

        :param revoked: Identity instance
        :return:
        """
        raw = self.raw_for_revoked(revoked)
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw
