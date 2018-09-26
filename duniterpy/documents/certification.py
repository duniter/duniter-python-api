import base64
import logging
import re
from typing import Optional, TypeVar, Type, Union
from .block_uid import BlockUID
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

    def __init__(self, version: int, currency: str, pubkey_from: str, identity: Union[Identity, str],
                 timestamp: BlockUID, signature: str) -> None:
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
    def from_signed_raw(cls: Type[CertificationType], signed_raw: str) -> CertificationType:
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

        identity_timestamp = BlockUID.from_str(Certification.parse_field("IdtyTimestamp", lines[n]))
        n += 1

        identity_signature = Certification.parse_field("IdtySignature", lines[n])
        n += 1

        timestamp = BlockUID.from_str(Certification.parse_field("CertTimestamp", lines[n]))
        n += 1

        signature = Certification.parse_field("Signature", lines[n])

        identity = Identity(version, currency, identity_pubkey, identity_uid, identity_timestamp, identity_signature)

        return cls(version, currency, pubkey_from, identity, timestamp, signature)

    @classmethod
    def from_inline(cls: Type[CertificationType], version: int, currency: str, blockhash: Optional[str],
                    inline: str) -> CertificationType:
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
            raise MalformedDocumentError("Can not return full certification document created from inline")

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
           certified_pubkey=self.identity.pubkey,
           certified_uid=self.identity.uid,
           certified_ts=self.identity.timestamp,
           certified_signature=self.identity.signatures[0],
           timestamp=self.timestamp)

    def sign(self, keys: list) -> None:
        """
        Sign the current document with the keys for the certified Identity given

        Warning : current signatures will be replaced with the new ones.

        :param keys: List of libnacl key instances
        """
        if not isinstance(self.identity, Identity):
            raise MalformedDocumentError("Can not return full certification document created from inline")

        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(), 'ascii')))
            logging.debug("Signature : \n{0}".format(signing.decode("ascii")))
            self.signatures.append(signing.decode("ascii"))

    def signed_raw(self) -> str:
        """
        Return signed raw document of the certification for the certified Identity instance

        :return:
        """
        if not isinstance(self.identity, Identity):
            raise MalformedDocumentError("Can not return full certification document created from inline")

        raw = self.raw()
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

    def __init__(self, version: int, currency: str, identity: Union[Identity, str], signature: str) -> None:
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
    def from_inline(cls: Type[RevocationType], version: int, currency: str, inline: str) -> RevocationType:
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

        identity = Identity(version, currency, issuer, identity_uid, identity_timestamp, identity_signature)

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
            raise MalformedDocumentError("Can not return full revocation document created from inline")

        return """Version: {version}
Type: Revocation
Currency: {currency}
Issuer: {pubkey}
IdtyUniqueID: {uid}
IdtyTimestamp: {timestamp}
IdtySignature: {signature}
""".format(version=self.version,
           currency=self.currency,
           pubkey=self.identity.pubkey,
           uid=self.identity.uid,
           timestamp=self.identity.timestamp,
           signature=self.identity.signatures[0])

    def sign(self, keys: list) -> None:
        """
        Sign the current document.
        Warning : current signatures will be replaced with the new ones.

        :param keys: List of libnacl key instances
        :return:
        """
        if not isinstance(self.identity, Identity):
            raise MalformedDocumentError("Can not return full revocation document created from inline")

        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(), 'ascii')))
            self.signatures.append(signing.decode("ascii"))

    def signed_raw(self) -> str:
        """
        Return Revocation signed raw document string

        :return:
        """
        if not isinstance(self.identity, Identity):
            raise MalformedDocumentError("Can not return full revocation document created from inline")

        raw = self.raw()
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw
