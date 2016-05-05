"""
duniter public and private keys

@author: inso
"""

import base58
import base64
import libnacl.sign
from pylibscrypt import scrypt
from .base58 import Base58Encoder


class VerifyingKey(libnacl.sign.Verifier):
    """
    Class to verify documents
    """
    def __init__(self, pubkey):
        """
        Creates a Verify class from base58 pubkey
        :param pubkey:
        """
        key = libnacl.encode.hex_encode(Base58Encoder.decode(pubkey))
        super().__init__(key)

    def verify_document(self, document, **kwargs):
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
