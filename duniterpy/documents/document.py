import base64
import hashlib
import logging
import re
from typing import TypeVar, Type, Any, List

from ..constants import SIGNATURE_REGEX


class MalformedDocumentError(Exception):
    """
    Malformed document exception
    """

    def __init__(self, field_name: str) -> None:
        """
        Init exception instance

        :param field_name: Name of the wrong field
        """
        super().__init__("Could not parse field {0}".format(field_name))


# required to type hint cls in classmethod
DocumentType = TypeVar("DocumentType", bound="Document")


class Document:
    re_version = re.compile("Version: ([0-9]+)\n")
    re_currency = re.compile("Currency: ([^\n]+)\n")
    re_signature = re.compile(
        "({signature_regex})\n".format(signature_regex=SIGNATURE_REGEX)
    )

    fields_parsers = {
        "Version": re_version,
        "Currency": re_currency,
        "Signature": re_signature,
    }

    def __init__(self, version: int, currency: str, signatures: List[str]) -> None:
        """
        Init Document instance

        :param version: Version of the Document
        :param currency: Name of the currency
        :param signatures: List of signatures
        """
        self.version = version
        self.currency = currency
        if signatures:
            self.signatures = [s for s in signatures if s is not None]
        else:
            self.signatures = []

    @classmethod
    def parse_field(cls: Type[DocumentType], field_name: str, line: str) -> Any:
        """
        Parse a document field with regular expression and return the value

        :param field_name: Name of the field
        :param line: Line string to parse
        :return:
        """
        try:
            match = cls.fields_parsers[field_name].match(line)
            if match is None:
                raise AttributeError
            value = match.group(1)
        except AttributeError:
            raise MalformedDocumentError(field_name)
        return value

    def sign(self, keys: list) -> None:
        """
        Sign the current document.

        Warning : current signatures will be replaced with the new ones.

        :param keys: List of libnacl keys instance
        """
        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(), "ascii")))
            logging.debug("Signature : \n%s", signing.decode("ascii"))
            self.signatures.append(signing.decode("ascii"))

    def raw(self) -> str:
        """
        Returns the raw document in string format
        """
        raise NotImplementedError("raw() is not implemented")

    def signed_raw(self) -> str:
        """
        If keys are None, returns the raw + current signatures
        If keys are present, returns the raw signed by these keys
        :return:
        """
        raw = self.raw()
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw

    @property
    def sha_hash(self) -> str:
        """
        Return uppercase hex sha256 hash from signed raw document

        :return:
        """
        return hashlib.sha256(self.signed_raw().encode("ascii")).hexdigest().upper()
