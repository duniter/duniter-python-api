import jsonschema

from duniterpy.api import ws2p
from duniterpy.api.client import WSConnection
from duniterpy.documents.ws2p.messages import Connect, Ack, Ok
from duniterpy.key import SigningKey


async def handshake(
    ws: WSConnection, signing_key: SigningKey, currency: str, verbose: bool = False
):
    """
    Perform ws2p handshake on the web socket connection using the signing_key instance

    :param ws: Web socket connection instance
    :param signing_key: SigningKey instance
    :param currency: Currency name
    :param verbose: Default=False, True to see console progress messages
    :return:
    """
    # START HANDSHAKE #######################################################
    if verbose:
        print("\nSTART HANDSHAKE...")

    connect_document = Connect(currency, signing_key.pubkey)
    connect_message = connect_document.get_signed_json(signing_key)
    if verbose:
        print("Send CONNECT message")
    await ws.send_str(connect_message)

    loop = True
    remote_connect_document = None
    # Iterate on each message received...
    while loop:

        data = await ws.receive_json()

        if "auth" in data and data["auth"] == "CONNECT":
            jsonschema.validate(data, ws2p.network.WS2P_CONNECT_MESSAGE_SCHEMA)
            if verbose:
                print("Received a CONNECT message")

            remote_connect_document = Connect(
                currency, data["pub"], data["challenge"], data["sig"]
            )
            if verbose:
                print("Received CONNECT message signature is valid")

            ack_message = Ack(
                currency, signing_key.pubkey, remote_connect_document.challenge
            ).get_signed_json(signing_key)

            # Send ACK message
            if verbose:
                print("Send ACK message...")

            await ws.send_str(ack_message)

        if "auth" in data and data["auth"] == "ACK":
            jsonschema.validate(data, ws2p.network.WS2P_ACK_MESSAGE_SCHEMA)
            if verbose:
                print("Received a ACK message")

            # Create ACK document from ACK response to verify signature
            Ack(currency, data["pub"], connect_document.challenge, data["sig"])
            if verbose:
                print("Received ACK message signature is valid")

            # If ACK response is ok, create OK message
            ok_message = Ok(
                currency, signing_key.pubkey, connect_document.challenge
            ).get_signed_json(signing_key)

            # Send OK message
            if verbose:
                print("Send OK message...")

            await ws.send_str(ok_message)

        if (
            remote_connect_document is not None
            and "auth" in data
            and data["auth"] == "OK"
        ):
            jsonschema.validate(data, ws2p.network.WS2P_OK_MESSAGE_SCHEMA)
            if verbose:
                print("Received a OK message")

            Ok(
                currency,
                remote_connect_document.pubkey,
                connect_document.challenge,
                data["sig"],
            )
            if verbose:
                print("Received OK message signature is valid")

            # END HANDSHAKE #######################################################
            if verbose:
                print("END OF HANDSHAKE\n")

            # exit loop
            break
