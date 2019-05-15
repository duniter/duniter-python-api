import json

from typing import Optional, Any

from duniterpy.documents import Document
from duniterpy.key import VerifyingKey, SigningKey
from duniterpy.helpers import get_ws2p_challenge


class Connect(Document):
    version = 2
    auth = "CONNECT"

    def __init__(self, currency: str, pubkey: str, challenge: Optional[str] = None,
                 signature: Optional[str] = None) -> None:
        """
        Init Connect message document

        :param currency: Name of currency
        :param pubkey: Public key of node
        :param challenge: [Optional, default=None] Big random string, typically an uuid
        :param signature: [Optional, default=None] Base64 encoded signature of raw formated document
        """
        super().__init__(self.version, currency, [signature])

        self.pubkey = pubkey
        if challenge is None:
            # create challenge
            self.challenge = get_ws2p_challenge()
        else:
            self.challenge = challenge
        # add and verify signature
        if signature is not None:
            self.signatures.append(signature)
            verifying_key = VerifyingKey(self.pubkey)
            verifying_key.verify_document(self)

    def raw(self):
        """
        Return the document in raw format

        :return:
        """
        return "WS2P:CONNECT:{currency}:{pub}:{challenge}".format(currency=self.currency, pub=self.pubkey,
                                                                  challenge=self.challenge)

    def get_signed_json(self, signing_key: SigningKey) -> str:
        """
        Return the signed message in json format

        :param signing_key: Signing key instance

        :return:
        """
        self.sign([signing_key])
        data = {
            "auth": self.auth,
            "pub": self.pubkey,
            "challenge": self.challenge,
            "sig": self.signatures[0]
        }
        return json.dumps(data)

    def __str__(self) -> str:
        return self.raw()


class Ack(Document):
    version = 2
    auth = "ACK"

    def __init__(self, currency: str, pubkey: str, challenge: str,
                 signature: Optional[str] = None) -> None:
        """
        Init Ack message document

        :param currency: Name of currency
        :param pubkey: Public key of node
        :param challenge: The challenge sent in the connect message
        :param signature: [Optional, default=None] Base64 encoded signature of raw formated document
        """
        super().__init__(self.version, currency, [signature])

        self.pubkey = pubkey
        self.challenge = challenge
        # add and verify signature
        if signature is not None:
            self.signatures.append(signature)
            verifying_key = VerifyingKey(self.pubkey)
            verifying_key.verify_document(self)

    def raw(self):
        """
        Return the document in raw format

        :return:
        """
        return "WS2P:ACK:{currency}:{pub}:{challenge}".format(currency=self.currency, pub=self.pubkey,
                                                              challenge=self.challenge)

    def get_signed_json(self, signing_key: SigningKey) -> str:
        """
        Return the signed message in json format

        :param signing_key: Signing key instance

        :return:
        """
        self.sign([signing_key])
        data = {
            "auth": self.auth,
            "pub": self.pubkey,
            "sig": self.signatures[0]
        }
        return json.dumps(data)

    def __str__(self) -> str:
        return self.raw()


class Ok(Document):
    version = 2
    auth = "OK"

    def __init__(self, currency: str, pubkey: str, challenge: str,
                 signature: Optional[str] = None) -> None:
        """
        Init Ok message document

        :param currency: Name of currency
        :param pubkey: Public key of node
        :param challenge: The challenge sent in the connect message
        :param signature: [Optional, default=None] Base64 encoded signature of raw formated document
        """
        super().__init__(self.version, currency, [signature])

        self.pubkey = pubkey
        self.challenge = challenge
        # add and verify signature
        if signature is not None:
            self.signatures.append(signature)
            verifying_key = VerifyingKey(self.pubkey)
            verifying_key.verify_document(self)

    def raw(self):
        """
        Return the document in raw format

        :return:
        """
        return "WS2P:OK:{currency}:{pub}:{challenge}".format(currency=self.currency, pub=self.pubkey,
                                                             challenge=self.challenge)

    def get_signed_json(self, signing_key: SigningKey) -> str:
        """
        Return the signed message in json format

        :param signing_key: Signing key instance

        :return:
        """
        self.sign([signing_key])
        data = {
            "auth": self.auth,
            "sig": self.signatures[0]
        }
        return json.dumps(data)

    def __str__(self) -> str:
        return self.raw()


# fixme: the document format to send is to be determine
# does raw or inline format works ?
class DocumentMessage:
    PEER_TYPE_ID = 0
    TRANSACTION_TYPE_ID = 1
    MEMBERSHIP_TYPE_ID = 2
    CERTIFICATION_TYPE_ID = 3
    IDENTITY_TYPE_ID = 4
    BLOCK_TYPE_ID = 5

    DOCUMENT_TYPE_NAMES = {
        0: "peer",
        1: "transaction",
        2: "membership",
        3: "certification",
        4: "identity",
        5: "block"
    }

    def get_json(self, document_type_id: int, document: Any) -> str:
        """
        Return the document message in json format

        :param document_type_id: Id of the document type, use class properties
        :param document: Document object to send
        :return:
        """
        data = {
            "body": {
                "name": document_type_id,
                self.DOCUMENT_TYPE_NAMES[document_type_id]: document
            }
        }
        return json.dumps(data)
