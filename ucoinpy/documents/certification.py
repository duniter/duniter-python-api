import re
import base64
import logging

from .document import Document, MalformedDocumentError
from .constants import pubkey_regex, signature_regex, block_id_regex, block_uid_regex


class SelfCertification(Document):
    """
    A document discribing a self certification.
    """

    re_inline = re.compile("({pubkey_regex}):({signature_regex}):({block_uid_regex}):([^\n]+)\n"
                           .format(pubkey_regex=pubkey_regex,
                                   signature_regex=signature_regex,
                                   block_uid_regex=block_uid_regex))
    re_uid = re.compile("UID:([^\n]+)\n")
    re_timestamp = re.compile("META:TS:({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))

    def __init__(self, version, currency, pubkey, uid, ts, signature):
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

        selfcert_data = SelfCertification.re_inline.match(inline)
        if selfcert_data is None:
            raise MalformedDocumentError("Inline self certification")
        pubkey = selfcert_data.group(1)
        signature = selfcert_data.group(2)
        ts = BlockUID.from_str(selfcert_data.group(3))
        uid = selfcert_data.group(4)

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

    def __init__(self, version, currency, pubkey_from, pubkey_to,
                 timestamp, signature):
        """
        Constructor

        :param str version: the UCP version
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

        :param SelfCertification selfcert:
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


class Revokation(Document):
    """
    A document describing a self-revocation.
    """
    re_inline = re.compile("({pubkey_regex}):({signature_regex})\n".format(
                                pubkey_regex=pubkey_regex,
                                signature_regex=signature_regex
                    ))

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
        cert_data = Revokation.re_inline.match(inline)
        if cert_data is None:
            raise MalformedDocumentError("Revokation")
        pubkey = cert_data.group(1)
        signature = cert_data.group(2)
        return cls(version, currency, pubkey, signature)


    def raw(self, selfcert):
        """

        :param SelfCertification selfcert:
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
