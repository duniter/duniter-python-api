"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json

from typing import Optional

from duniterpy.documents import Document
from duniterpy.key import VerifyingKey, SigningKey
from duniterpy.tools import get_ws2p_challenge


class HandshakeMessage(Document):
    version = 2
    auth = ""

    def __init__(
        self,
        currency: str,
        pubkey: str,
        challenge: Optional[str] = None,
        signature: Optional[str] = None,
    ) -> None:
        """
        Init Connect message document

        :param currency: Name of the currency
        :param pubkey: Public key of the node
        :param challenge: [Optional, default=None] Big random string, typically an uuid
        :param signature: [Optional, default=None] Base64 encoded signature of raw formated document
        """
        if signature is not None:
            signatures = [signature]
        else:
            signatures = []

        super().__init__(self.version, currency, signatures)

        self.pubkey = pubkey

        if challenge is None:
            # create challenge
            self.challenge = get_ws2p_challenge()
        else:
            self.challenge = challenge

        if signature is not None:
            # verify signature
            verifying_key = VerifyingKey(self.pubkey)
            verifying_key.verify_document(self)

    def raw(self):
        """
        Return the document in raw format

        :return:
        """
        return "WS2P:{auth}:{currency}:{pub}:{challenge}".format(
            auth=self.auth,
            currency=self.currency,
            pub=self.pubkey,
            challenge=self.challenge,
        )

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
            "sig": self.signatures[0],
        }
        return json.dumps(data)

    def __str__(self) -> str:
        return self.raw()


class Connect(HandshakeMessage):
    auth = "CONNECT"


class Ack(HandshakeMessage):
    auth = "ACK"

    def __init__(
        self,
        currency: str,
        pubkey: str,
        challenge: str,
        signature: Optional[str] = None,
    ) -> None:
        """
        Init Connect message document

        :param currency: Name of the currency
        :param pubkey: Public key of the node
        :param challenge: Big random string, typically an uuid
        :param signature: [Optional, default=None] Base64 encoded signature of raw formated document
        """
        super().__init__(currency, pubkey, challenge, signature)

    def get_signed_json(self, signing_key: SigningKey) -> str:
        """
        Return the signed message in json format

        :param signing_key: Signing key instance

        :return:
        """
        self.sign([signing_key])
        data = {"auth": self.auth, "pub": self.pubkey, "sig": self.signatures[0]}
        return json.dumps(data)


class Ok(HandshakeMessage):
    auth = "OK"

    def __init__(
        self,
        currency: str,
        pubkey: str,
        challenge: str,
        signature: Optional[str] = None,
    ) -> None:
        """
        Init Connect message document

        :param currency: Name of the currency
        :param pubkey: Public key of the node
        :param challenge: Big random string, typically an uuid
        :param signature: [Optional, default=None] Base64 encoded signature of raw formated document
        """
        super().__init__(currency, pubkey, challenge, signature)

    def get_signed_json(self, signing_key: SigningKey) -> str:
        """
        Return the signed message in json format

        :param signing_key: Signing key instance

        :return:
        """
        self.sign([signing_key])
        data = {"auth": self.auth, "sig": self.signatures[0]}
        return json.dumps(data)


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
        5: "block",
    }

    def get_json(self, document_type_id: int, document: str) -> str:
        """
        Return the document message in json format

        :param document_type_id: Id of the document type, use class properties
        :param document: Raw or Inline Document to send
        """
        data = {
            "body": {
                "name": document_type_id,
                self.DOCUMENT_TYPE_NAMES[document_type_id]: document,
            }
        }
        return json.dumps(data)
