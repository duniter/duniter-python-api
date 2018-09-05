"""
duniter public and private keys

@author: inso
"""

import base64
import libnacl.sign
import libnacl.encode

from duniterpy.documents import Document
from duniterpy.documents.ws2p.heads import HeadV2
from .base58 import Base58Encoder


class VerifyingKey(libnacl.sign.Verifier):
    """
    Class to verify documents
    """
    def __init__(self, pubkey: str) -> None:
        """
        Creates a Verify class from base58 pubkey
        :param pubkey:
        """
        key = libnacl.encode.hex_encode(Base58Encoder.decode(pubkey))
        super().__init__(key)

    def verify_document(self, document: Document, **kwargs) -> bool:
        """
        Check specified document
        :param duniterpy.documents.Document document:
        :return:
        """
        signature = base64.b64decode(document.signatures[0])
        prepended = signature + bytes(document.raw(**kwargs), 'ascii')

        try:
            self.verify(prepended)
            return True
        except ValueError:
            return False

    def verify_ws2p_head(self, head: HeadV2) -> bool:
        """
        Check specified document
        :param HeadV2 head:
        :return:
        """
        signature = base64.b64decode(head.signature)
        inline = head.inline()
        prepended = signature + bytes(inline, 'ascii')

        try:
            self.verify(prepended)
            return True
        except ValueError:
            return False

    def verify_message(self, message: bytes) -> str:
        """
        Check specified signed message signature and return message

        Return error message if signature is invalid

        :param bytes message: Message + signature
        :return str:
        """
        return self.verify(message).decode('utf-8')

