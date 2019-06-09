"""
Created on 2 déc. 2014

@author: inso
"""
import re
from typing import TypeVar, Type, Optional

from .block_uid import BlockUID
from .document import Document, MalformedDocumentError
from ..constants import BLOCK_UID_REGEX, SIGNATURE_REGEX, PUBKEY_REGEX

# required to type hint cls in classmethod
MembershipType = TypeVar("MembershipType", bound="Membership")


class Membership(Document):
    """
.. note:: A membership document is specified by the following format :

    | Version: VERSION
    | Type: Membership
    | Currency: CURRENCY_NAME
    | Issuer: ISSUER
    | Block: NUMBER-HASH
    | Membership: MEMBERSHIP_TYPE
    | UserID: USER_ID
    | CertTS: CERTIFICATION_TS

    """

    # PUBLIC_KEY:SIGNATURE:NUMBER:HASH:TIMESTAMP:USER_ID
    re_inline = re.compile(
        "({pubkey_regex}):({signature_regex}):({ms_block_uid_regex}):({identity_block_uid_regex}):([^\n]+)\n".format(
            pubkey_regex=PUBKEY_REGEX,
            signature_regex=SIGNATURE_REGEX,
            ms_block_uid_regex=BLOCK_UID_REGEX,
            identity_block_uid_regex=BLOCK_UID_REGEX,
        )
    )
    re_type = re.compile("Type: (Membership)")
    re_issuer = re.compile(
        "Issuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX)
    )
    re_block = re.compile(
        "Block: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX)
    )
    re_membership_type = re.compile("Membership: (IN|OUT)")
    re_userid = re.compile("UserID: ([^\n]+)\n")
    re_certts = re.compile(
        "CertTS: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX)
    )

    fields_parsers = {
        **Document.fields_parsers,
        **{
            "Type": re_type,
            "Issuer": re_issuer,
            "Block": re_block,
            "Membership": re_membership_type,
            "UserID": re_userid,
            "CertTS": re_certts,
        },
    }

    def __init__(
        self,
        version: int,
        currency: str,
        issuer: str,
        membership_ts: BlockUID,
        membership_type: str,
        uid: str,
        identity_ts: BlockUID,
        signature: Optional[str] = None,
    ) -> None:
        """
        Create a membership document

        :param version: Version of the document
        :param currency: Name of the currency
        :param issuer: Public key of the issuer
        :param membership_ts: BlockUID of this membership
        :param membership_type: "IN" or "OUT" to enter or quit the community
        :param uid: Unique identifier of the identity
        :param identity_ts:  BlockUID of the identity
        :param signature: Signature of the document
        """
        if signature:
            signatures = [signature]
        else:
            signatures = []
        super().__init__(version, currency, signatures)

        self.issuer = issuer
        self.membership_ts = membership_ts
        self.membership_type = membership_type
        self.uid = uid
        self.identity_ts = identity_ts

    @classmethod
    def from_inline(
        cls: Type[MembershipType],
        version: int,
        currency: str,
        membership_type: str,
        inline: str,
    ) -> MembershipType:
        """
        Return Membership instance from inline format

        :param version: Version of the document
        :param currency: Name of the currency
        :param membership_type: "IN" or "OUT" to enter or exit membership
        :param inline: Inline string format
        :return:
        """
        data = Membership.re_inline.match(inline)
        if data is None:
            raise MalformedDocumentError("Inline membership ({0})".format(inline))
        issuer = data.group(1)
        signature = data.group(2)
        membership_ts = BlockUID.from_str(data.group(3))
        identity_ts = BlockUID.from_str(data.group(4))
        uid = data.group(5)
        return cls(
            version,
            currency,
            issuer,
            membership_ts,
            membership_type,
            uid,
            identity_ts,
            signature,
        )

    @classmethod
    def from_signed_raw(cls: Type[MembershipType], signed_raw: str) -> MembershipType:
        """
        Return Membership instance from signed raw format

        :param signed_raw: Signed raw format string
        :return:
        """
        lines = signed_raw.splitlines(True)
        n = 0

        version = int(Membership.parse_field("Version", lines[n]))
        n += 1

        Membership.parse_field("Type", lines[n])
        n += 1

        currency = Membership.parse_field("Currency", lines[n])
        n += 1

        issuer = Membership.parse_field("Issuer", lines[n])
        n += 1

        membership_ts = BlockUID.from_str(Membership.parse_field("Block", lines[n]))
        n += 1

        membership_type = Membership.parse_field("Membership", lines[n])
        n += 1

        uid = Membership.parse_field("UserID", lines[n])
        n += 1

        identity_ts = BlockUID.from_str(Membership.parse_field("CertTS", lines[n]))
        n += 1

        signature = Membership.parse_field("Signature", lines[n])
        n += 1

        return cls(
            version,
            currency,
            issuer,
            membership_ts,
            membership_type,
            uid,
            identity_ts,
            signature,
        )

    def raw(self) -> str:
        """
        Return signed raw format string of the Membership instance

        :return:
        """
        return """Version: {0}
Type: Membership
Currency: {1}
Issuer: {2}
Block: {3}
Membership: {4}
UserID: {5}
CertTS: {6}
""".format(
            self.version,
            self.currency,
            self.issuer,
            self.membership_ts,
            self.membership_type,
            self.uid,
            self.identity_ts,
        )

    def inline(self) -> str:
        """
        Return inline string format of the Membership instance
        :return:
        """
        return "{0}:{1}:{2}:{3}:{4}".format(
            self.issuer,
            self.signatures[0],
            self.membership_ts,
            self.identity_ts,
            self.uid,
        )
