import base64
import re
import logging
import hashlib
from .constants import signature_regex


class MalformedDocumentError(Exception):
    """
    Malformed document exception
    """
    def __init__(self, field_name):
        super().__init__("Could not parse field {0}".format(field_name))


class Document:
    re_version = re.compile("Version: ([0-9]+)\n")
    re_currency = re.compile("Currency: ([^\n]+)\n")
    re_signature = re.compile("({signature_regex})\n".format(signature_regex=signature_regex))

    fields_parsers = {
        "Version": re_version,
        "Currency": re_currency,
        "Signature": re_signature
    }

    @classmethod
    def parse_field(cls, field_name, line):
        """

        :param field_name:
        :param line:
        :return:
        """
        try:
            value = cls.fields_parsers[field_name].match(line).group(1)
        except AttributeError:
            raise MalformedDocumentError(field_name)
        return value

    def __init__(self, version, currency, signatures):
        if version < 2:
            raise MalformedDocumentError("Version 1 documents are not handled by duniterpy>0.2")
        self.version = version
        self.currency = currency
        if signatures:
            self.signatures = [s for s in signatures if s is not None]
        else:
            self.signatures = []

    def sign(self, keys):
        """
        Sign the current document.
        Warning : current signatures will be replaced with the new ones.
        """
        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(), 'ascii')))
            logging.debug("Signature : \n{0}".format(signing.decode("ascii")))
            self.signatures.append(signing.decode("ascii"))

    def raw(self):
        """
        Returns the raw document in string format
        """
        raise NotImplementedError()

    def signed_raw(self):
        """
        If keys are None, returns the raw + current signatures
        If keys are present, returns the raw signed by these keys
        """
        raw = self.raw()
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw

    @property
    def sha_hash(self):
        return hashlib.sha256(self.signed_raw().encode("ascii")).hexdigest().upper()
