import re
import base64
import logging

from .document import Document, MalformedDocumentError
from .constants import pubkey_regex, signature_regex, block_id_regex, block_uid_regex, uid_regex


class Identity(Document):
    """
    A document describing a self certification.
    """

    re_inline = re.compile("({pubkey_regex}):({signature_regex}):({block_uid_regex}):([^\n]+)\n"
                           .format(pubkey_regex=pubkey_regex,
                                   signature_regex=signature_regex,
                                   block_uid_regex=block_uid_regex))
    re_type = re.compile("Type: (Identity)")
    re_issuer = re.compile("Issuer: ({pubkey_regex})\n".format(pubkey_regex=pubkey_regex))
    re_unique_id = re.compile("UniqueID: ({uid_regex})\n".format(uid_regex=uid_regex))
    re_uid = re.compile("UID:([^\n]+)\n")
    re_meta_ts = re.compile("META:TS:({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))
    re_timestamp = re.compile("Timestamp: ({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))

    fields_parsers = {**Document.fields_parsers, **{
        "Type": re_type,
        "UniqueID": re_unique_id,
        "Issuer": re_issuer,
        "Timestamp": re_timestamp
    }}

    def __init__(self, version, currency, pubkey, uid, ts, signature):
        """
        Create an identity document

        :param int version: Version of the document
        :param str currency: Name of the currency
        :param str pubkey:  Public key of the account linked to the identity
        :param str uid: Unique identifier
        :param BlockUID ts: Block timestamp
        :param str|None signature: Signature of the document
        """
        if signature:
            super().__init__(version, currency, [signature])
        else:
            super().__init__(version, currency, [])
        self.pubkey = pubkey
        self.timestamp = ts
        self.uid = uid

    @classmethod
    def from_inline(cls, version, currency, inline):
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
    def from_signed_raw(cls, signed_raw):
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

    def raw(self):
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

    def inline(self):
        return "{pubkey}:{signature}:{timestamp}:{uid}".format(
            pubkey=self.pubkey,
            signature=self.signatures[0],
            timestamp=self.timestamp,
            uid=self.uid)


class Certification(Document):
    """
    A document describing a certification.
    """

    re_inline = re.compile("({certifier_regex}):({certified_regex}):({block_id_regex}):({signature_regex})\n".format(
                                certifier_regex=pubkey_regex,
                                certified_regex=pubkey_regex,
                                block_id_regex=block_id_regex,
                                signature_regex=signature_regex
                    ))
    re_timestamp = re.compile("META:TS:({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))
    re_type = re.compile("Type: (Certification)")
    re_issuer = re.compile("Issuer: ({pubkey_regex})\n".format(pubkey_regex=pubkey_regex))
    re_idty_issuer = re.compile("IdtyIssuer: ({pubkey_regex})\n".format(pubkey_regex=pubkey_regex))
    re_idty_unique_id = re.compile("IdtyUniqueID: ({uid_regex})\n".format(uid_regex=uid_regex))
    re_idty_timestamp = re.compile("IdtyTimestamp: ({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))
    re_idty_signature = re.compile("IdtySignature: ({signature_regex})\n".format(signature_regex=signature_regex))
    re_cert_timestamp = re.compile("CertTimestamp: ({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))

    fields_parsers = {**Document.fields_parsers, **{
        "Type": re_type,
        "Issuer": re_issuer,
        "CertTimestamp": re_cert_timestamp,
        "IdtyIssuer": re_idty_issuer,
        "IdtyUniqueID": re_idty_unique_id,
        "IdtySignature": re_idty_signature,
        "IdtyTimestamp": re_idty_timestamp
    }}

    def __init__(self, version, currency, pubkey_from, pubkey_to,
                 timestamp, signature):
        """
        Constructor

        :param int version: the UCP version
        :param str currency: the currency of the blockchain
        :param str pubkey_from:
        :param str pubkey_to:
        :param BlockUID timestamp: the blockuid
        :param str signature: the signature of the document
        """
        super().__init__(version, currency, [signature])
        self.pubkey_from = pubkey_from
        self.pubkey_to = pubkey_to
        self.timestamp = timestamp

    @classmethod
    def from_signed_raw(cls, signed_raw):
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
    def from_inline(cls, version, currency, blockhash, inline):
        """
        From inline version in block
        :param version:
        :param currency:
        :param blockhash:
        :param inline:
        :return:
        """
        from .block import Block, BlockUID
        cert_data = Certification.re_inline.match(inline)
        if cert_data is None:
            raise MalformedDocumentError("Certification ({0})".format(inline))
        pubkey_from = cert_data.group(1)
        pubkey_to = cert_data.group(2)
        blockid = int(cert_data.group(3))
        if blockid == 0:
            timestamp = BlockUID.empty()
        else:
            timestamp = BlockUID(blockid, blockhash)

        signature = cert_data.group(4)
        return cls(version, currency, pubkey_from, pubkey_to, timestamp, signature)

    def raw(self, selfcert):
        """

        :param Identity selfcert:
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
           certified_pubkey=selfcert.pubkey,
           certified_uid=selfcert.uid,
           certified_ts=selfcert.timestamp,
           certified_signature=selfcert.signatures[0],
           timestamp=self.timestamp)

    def sign(self, selfcert, keys):
        """
        Sign the current document.
        Warning : current signatures will be replaced with the new ones.
        """
        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(selfcert), 'ascii')))
            logging.debug("Signature : \n{0}".format(signing.decode("ascii")))
            self.signatures.append(signing.decode("ascii"))

    def signed_raw(self, selfcert):
        raw = self.raw(selfcert)
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw

    def inline(self):
        return "{0}:{1}:{2}:{3}".format(self.pubkey_from, self.pubkey_to,
                                        self.timestamp.number, self.signatures[0])


class Revocation(Document):
    """
    A document describing a self-revocation.
    """
    re_inline = re.compile("({pubkey_regex}):({signature_regex})\n".format(
                                pubkey_regex=pubkey_regex,
                                signature_regex=signature_regex
                    ))

    re_type = re.compile("Type: (Revocation)")
    re_issuer = re.compile("Issuer: ({pubkey_regex})\n".format(pubkey_regex=pubkey_regex))
    re_uniqueid = re.compile("IdtyUniqueID: ([^\n]+)\n")
    re_timestamp = re.compile("IdtyTimestamp: ({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))
    re_idtysignature = re.compile("IdtySignature: ({signature_regex})\n".format(signature_regex=signature_regex))

    fields_parsers = {**Document.fields_parsers, **{
        "Type": re_type,
        "Issuer": re_issuer,
        "IdtyUniqueID": re_uniqueid,
        "IdtyTimestamp": re_timestamp,
        "IdtySignature": re_idtysignature,
    }}

    def __init__(self, version, currency, pubkey, signature):
        """
        Constructor
        """
        super().__init__(version, currency, [signature])
        self.pubkey = pubkey

    @classmethod
    def from_inline(cls, version, currency, inline):
        """
        From inline version in block
        :param int version:
        :param str currency:
        :param str pubkey:
        :param str signature:
        :return:
        """
        cert_data = Revocation.re_inline.match(inline)
        if cert_data is None:
            raise MalformedDocumentError("Revokation")
        pubkey = cert_data.group(1)
        signature = cert_data.group(2)
        return cls(version, currency, pubkey, signature)

    @classmethod
    def from_signed_raw(cls, signed_raw):
        """
        Instanciates a revocation from a signed raw file
        :param str signed_raw: raw document file in duniter format
        :return: a revocation instance
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
    def extract_self_cert(signed_raw):
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

    def inline(self):
        return "{0}:{1}".format(self.pubkey, self.signatures[0])

    def raw(self, selfcert):
        """

        :param Identity selfcert:
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
           pubkey=selfcert.pubkey,
           uid=selfcert.uid,
           timestamp=selfcert.timestamp,
           signature=selfcert.signatures[0])

    def sign(self, selfcert, keys):
        """
        Sign the current document.
        Warning : current signatures will be replaced with the new ones.
        """
        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(selfcert), 'ascii')))
            self.signatures.append(signing.decode("ascii"))

    def signed_raw(self, selfcert):
        raw = self.raw(selfcert)
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw
