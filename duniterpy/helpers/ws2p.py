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

import jsonschema
from typing import Union
from duniterpy.api import ws2p, bma
from duniterpy.api.client import WSConnection, Client
from duniterpy.api.endpoint import BMAEndpoint, SecuredBMAEndpoint, WS2PEndpoint
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


async def generate_ws2p_endpoint(
    bma_endpoint: Union[str, BMAEndpoint, SecuredBMAEndpoint]
) -> WS2PEndpoint:
    """
    Retrieve WS2P endpoints from BMA peering
    Take the first one found
    """
    bma_client = Client(bma_endpoint)
    peering = await bma_client(bma.network.peering)
    await bma_client.close()

    for endpoint in peering["endpoints"]:
        if endpoint.startswith("WS2P"):
            return WS2PEndpoint.from_inline(endpoint)
    raise ValueError("No WS2P endpoint found")
