"""
Created on 2 déc. 2014

@author: inso
"""
from .document import Document, MalformedDocumentError
from .constants import block_uid_regex, signature_regex, pubkey_regex

import re


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
    re_inline = re.compile("({pubkey_regex}):({signature_regex}):({ms_block_uid_regex}):({identity_block_uid_regex}):([^\n]+)\n"
                                .format(pubkey_regex=pubkey_regex, signature_regex=signature_regex,
                                        ms_block_uid_regex=block_uid_regex,
                                        identity_block_uid_regex=block_uid_regex))
    re_type = re.compile("Type: (Membership)")
    re_issuer = re.compile("Issuer: ({pubkey_regex})\n".format(pubkey_regex=pubkey_regex))
    re_block = re.compile("Block: ({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))
    re_membership_type = re.compile("Membership: (IN|OUT)")
    re_userid = re.compile("UserID: ([^\n]+)\n")
    re_certts = re.compile("CertTS: ({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))

    fields_parsers = {**Document.fields_parsers, **{
        "Type": re_type,
        "Issuer": re_issuer,
        "Block": re_block,
        "Membership": re_membership_type,
        "UserID": re_userid,
        "CertTS": re_certts
    }}

    def __init__(self, version, currency, issuer, membership_ts,
                 membership_type, uid, identity_ts, signature):
        """
        Create a membership document

        :param int version: Version of the document
        :param currency: Name of the currency
        :param issuer: Public key of the issuer
        :param BlockUID membership_ts: BlockUID of this membership
        :param membership_type: "IN" or "OUT" to enter or quit the community
        :param str uid: Unique identifier of the identity
        :param BlockUID identity_ts:  BlockUID of the identity
        :param str|None signature: Signature of the document
        """
        super().__init__(version, currency, [signature])
        self.issuer = issuer
        self.membership_ts = membership_ts
        self.membership_type = membership_type
        self.uid = uid
        self.identity_ts = identity_ts

    @classmethod
    def from_inline(cls, version, currency, membership_type, inline):
        from .block import BlockUID
        data = Membership.re_inline.match(inline)
        if data is None:
            raise MalformedDocumentError("Inline membership ({0})".format(inline))
        issuer = data.group(1)
        signature = data.group(2)
        membership_ts = BlockUID.from_str(data.group(3))
        identity_ts = BlockUID.from_str(data.group(4))
        uid = data.group(5)
        return cls(version, currency, issuer, membership_ts, membership_type, uid, identity_ts, signature)

    @classmethod
    def from_signed_raw(cls, signed_raw):
        from .block import BlockUID
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

        return cls(version, currency, issuer, membership_ts,
                   membership_type, uid, identity_ts, signature)

    def raw(self):
        return """Version: {0}
Type: Membership
Currency: {1}
Issuer: {2}
Block: {3}
Membership: {4}
UserID: {5}
CertTS: {6}
""".format(self.version,
                      self.currency,
                      self.issuer,
                      self.membership_ts,
                      self.membership_type,
                      self.uid,
                      self.identity_ts)

    def inline(self):
        return "{0}:{1}:{2}:{3}:{4}".format(self.issuer,
                                        self.signatures[0],
                                        self.membership_ts,
                                        self.identity_ts,
                                        self.uid)
