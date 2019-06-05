import re
from typing import Optional, TypeVar, Type

from .block_uid import BlockUID
from ..constants import PUBKEY_REGEX, SIGNATURE_REGEX, BLOCK_UID_REGEX, UID_REGEX
from .document import Document, MalformedDocumentError

# required to type hint cls in classmethod
IdentityType = TypeVar("IdentityType", bound="Identity")


class Identity(Document):
    """
    A document describing a self certification.
    """

    re_inline = re.compile(
        "({pubkey_regex}):({signature_regex}):({block_uid_regex}):([^\n]+)\n".format(
            pubkey_regex=PUBKEY_REGEX,
            signature_regex=SIGNATURE_REGEX,
            block_uid_regex=BLOCK_UID_REGEX,
        )
    )
    re_type = re.compile("Type: (Identity)")
    re_issuer = re.compile(
        "Issuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX)
    )
    re_unique_id = re.compile("UniqueID: ({uid_regex})\n".format(uid_regex=UID_REGEX))
    re_uid = re.compile("UID:([^\n]+)\n")
    re_meta_ts = re.compile(
        "META:TS:({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX)
    )
    re_timestamp = re.compile(
        "Timestamp: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX)
    )

    fields_parsers = {
        **Document.fields_parsers,
        **{
            "Type": re_type,
            "UniqueID": re_unique_id,
            "Issuer": re_issuer,
            "Timestamp": re_timestamp,
        },
    }

    def __init__(
        self,
        version: int,
        currency: str,
        pubkey: str,
        uid: str,
        ts: BlockUID,
        signature: Optional[str],
    ) -> None:
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
    def from_inline(
        cls: Type[IdentityType], version: int, currency: str, inline: str
    ) -> IdentityType:
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
""".format(
            version=self.version,
            currency=self.currency,
            pubkey=self.pubkey,
            uid=self.uid,
            timestamp=self.timestamp,
        )

    def inline(self) -> str:
        """
        Return an inline string of the Identity
        :return:
        """
        return "{pubkey}:{signature}:{timestamp}:{uid}".format(
            pubkey=self.pubkey,
            signature=self.signatures[0],
            timestamp=self.timestamp,
            uid=self.uid,
        )
