import jsonschema

from duniterpy.api import ws2p
from duniterpy.api.client import WSConnection
from duniterpy.documents.ws2p.messages import Connect, Ack, Ok
from duniterpy.key import SigningKey
import logging


async def handshake(ws: WSConnection, signing_key: SigningKey, currency: str):
    """
    Perform ws2p handshake on the web socket connection using the signing_key instance

    :param ws: Web socket connection instance
    :param signing_key: SigningKey instance
    :param currency: Currency name
    :return:
    """
    # START HANDSHAKE #######################################################
    logging.debug("\nSTART HANDSHAKE...")

    connect_document = Connect(currency, signing_key.pubkey)
    connect_message = connect_document.get_signed_json(signing_key)

    logging.debug("Send CONNECT message")
    await ws.send_str(connect_message)

    loop = True
    remote_connect_document = None
    # Iterate on each message received...
    while loop:

        data = await ws.receive_json()

        if "auth" in data and data["auth"] == "CONNECT":
            jsonschema.validate(data, ws2p.network.WS2P_CONNECT_MESSAGE_SCHEMA)

            logging.debug("Received a CONNECT message")

            remote_connect_document = Connect(
                currency, data["pub"], data["challenge"], data["sig"]
            )

            logging.debug("Received CONNECT message signature is valid")

            ack_message = Ack(
                currency, signing_key.pubkey, remote_connect_document.challenge
            ).get_signed_json(signing_key)

            # Send ACK message
            logging.debug("Send ACK message...")
            await ws.send_str(ack_message)

        if "auth" in data and data["auth"] == "ACK":
            jsonschema.validate(data, ws2p.network.WS2P_ACK_MESSAGE_SCHEMA)

            logging.debug("Received an ACK message")

            # Create ACK document from ACK response to verify signature
            Ack(currency, data["pub"], connect_document.challenge, data["sig"])

            logging.debug("Received ACK message signature is valid")

            # If ACK response is ok, create OK message
            ok_message = Ok(
                currency, signing_key.pubkey, connect_document.challenge
            ).get_signed_json(signing_key)

            # Send OK message
            logging.debug("Send OK message...")
            await ws.send_str(ok_message)

        if (
            remote_connect_document is not None
            and "auth" in data
            and data["auth"] == "OK"
        ):
            jsonschema.validate(data, ws2p.network.WS2P_OK_MESSAGE_SCHEMA)

            logging.debug("Received an OK message")

            Ok(
                currency,
                remote_connect_document.pubkey,
                connect_document.challenge,
                data["sig"],
            )

            logging.debug("Received OK message signature is valid")

            # END HANDSHAKE #######################################################
            logging.debug("END OF HANDSHAKE\n")

            # exit loop
            break
