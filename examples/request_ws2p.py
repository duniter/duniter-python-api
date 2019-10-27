import asyncio
import json
import time

from _socket import gaierror

import aiohttp
import jsonschema
from jsonschema import ValidationError

from duniterpy.tools import get_ws2p_challenge
from duniterpy.key import SigningKey

from duniterpy.api import ws2p
from duniterpy.api.ws2p import requests
from duniterpy.documents.ws2p.messages import Connect, Ack, Ok
from duniterpy.api.client import Client, parse_text

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the WS2P API (WS2P)
WS2P_ENDPOINT = "WS2P 2f731dcd 127.0.0.1 20900"
CURRENCY = "g1-test"


################################################


async def main():
    """
    Main code
    """

    # # Prompt hidden user entry
    # salt = getpass.getpass("Enter your passphrase (salt): ")
    #
    # # Prompt hidden user entry
    # password = getpass.getpass("Enter your password: ")
    salt = password = "toto"

    # Init signing_key instance
    signing_key = SigningKey.from_credentials(salt, password)

    connect_document = Connect(CURRENCY, signing_key.pubkey)
    connect_message = connect_document.get_signed_json(signing_key)

    # Create Client from endpoint string in Duniter format
    client = Client(WS2P_ENDPOINT)

    try:
        # Create a Web Socket connection
        ws = await client.connect_ws()

        print("Connected successfully to web socket endpoint")

        # START HANDSHAKE #######################################################
        print("\nSTART HANDSHAKE...")

        print("Send CONNECT message")
        await ws.send_str(connect_message)

        loop = True
        # Iterate on each message received...
        while loop:
            print("ws.receive_str()")
            msg = await ws.receive_str()

            # Display incoming message from peer
            print(msg)

            try:
                # Validate json string with jsonschema and return a dict
                data = parse_text(msg, ws2p.network.WS2P_CONNECT_MESSAGE_SCHEMA)

            except jsonschema.exceptions.ValidationError:
                try:
                    # Validate json string with jsonschema and return a dict
                    data = parse_text(msg, ws2p.network.WS2P_ACK_MESSAGE_SCHEMA)

                except jsonschema.exceptions.ValidationError:
                    try:
                        # Validate json string with jsonschema and return a dict
                        data = parse_text(msg, ws2p.network.WS2P_OK_MESSAGE_SCHEMA)

                    except jsonschema.exceptions.ValidationError:
                        continue

                    print("Received a OK message")

                    Ok(
                        CURRENCY,
                        remote_connect_document.pubkey,
                        connect_document.challenge,
                        data["sig"],
                    )
                    print("Received OK message signature is valid")

                    # END HANDSHAKE #######################################################
                    print("END OF HANDSHAKE\n")

                    # Uncomment the following command to stop listening for messages anymore
                    break

                    # Uncomment the following commands to continue to listen incoming messages
                    # print("waiting for incoming messages...\n")
                    # continue

                print("Received a ACK message")

                # Create ACK document from ACK response to verify signature
                Ack(CURRENCY, data["pub"], connect_document.challenge, data["sig"])
                print("Received ACK message signature is valid")
                # If ACK response is ok, create OK message
                ok_message = Ok(
                    CURRENCY, signing_key.pubkey, connect_document.challenge
                ).get_signed_json(signing_key)

                # Send OK message
                print("Send OK message...")
                await ws.send_str(ok_message)
                continue

            print("Received a CONNECT message")

            remote_connect_document = Connect(
                CURRENCY, data["pub"], data["challenge"], data["sig"]
            )
            print("Received CONNECT message signature is valid")

            ack_message = Ack(
                CURRENCY, signing_key.pubkey, remote_connect_document.challenge
            ).get_signed_json(signing_key)
            # Send ACK message
            print("Send ACK message...")
            await ws.send_str(ack_message)

        # Send ws2p request
        print("Send getCurrent() request")
        request_id = get_ws2p_challenge()[:8]
        await ws.send_str(requests.get_current(request_id))

        # Wait response with request id
        response_str = await ws.receive_str()
        while "resId" not in json.loads(response_str) or (
            "resId" in json.loads(response_str)
            and json.loads(response_str)["resId"] != request_id
        ):
            response_str = await ws.receive_str()
            time.sleep(1)
        try:
            # Check response format
            parse_text(response_str, requests.BLOCK_RESPONSE_SCHEMA)
            # If valid display response
            print("Response: " + response_str)
        except ValidationError:
            # If invalid response...
            try:
                # Check error response format
                parse_text(response_str, requests.ERROR_RESPONSE_SCHEMA)
                # If valid, display error response
                print("Error response: " + response_str)
            except ValidationError as exception:
                # If invalid, display exception on response validation
                print(exception)

        # Send ws2p request
        print("Send getBlock(360000) request")
        request_id = get_ws2p_challenge()[:8]
        await ws.send_str(requests.get_block(request_id, 360000))

        # Wait response with request id
        response_str = await ws.receive_str()
        while "resId" not in json.loads(response_str) or (
            "resId" in json.loads(response_str)
            and json.loads(response_str)["resId"] != request_id
        ):
            response_str = await ws.receive_str()
            time.sleep(1)
        try:
            # Check response format
            parse_text(response_str, requests.BLOCK_RESPONSE_SCHEMA)
            # If valid display response
            print("Response: " + response_str)
        except ValidationError:
            # If invalid response...
            try:
                # Check error response format
                parse_text(response_str, requests.ERROR_RESPONSE_SCHEMA)
                # If valid, display error response
                print("Error response: " + response_str)
            except ValidationError as exception:
                # If invalid, display exception on response validation
                print(exception)

        # Send ws2p request
        print("Send getBlocks(360000, 2) request")
        request_id = get_ws2p_challenge()[:8]
        await ws.send_str(requests.get_blocks(request_id, 360000, 2))

        # Wait response with request id
        response_str = await ws.receive_str()
        while "resId" not in json.loads(response_str) or (
            "resId" in json.loads(response_str)
            and json.loads(response_str)["resId"] != request_id
        ):
            response_str = await ws.receive_str()
            time.sleep(1)
        try:
            # Check response format
            parse_text(response_str, requests.BLOCKS_RESPONSE_SCHEMA)
            # If valid display response
            print("Response: " + response_str)
        except ValidationError:
            # If invalid response...
            try:
                # Check error response format
                parse_text(response_str, requests.ERROR_RESPONSE_SCHEMA)
                # If valid, display error response
                print("Error response: " + response_str)
            except ValidationError as exception:
                # If invalid, display exception on response validation
                print(exception)

        # Send ws2p request
        print("Send getRequirementsPending(3) request")
        request_id = get_ws2p_challenge()[:8]
        await ws.send_str(requests.get_requirements_pending(request_id, 3))
        # Wait response with request id
        response_str = await ws.receive_str()
        while "resId" not in json.loads(response_str) or (
            "resId" in json.loads(response_str)
            and json.loads(response_str)["resId"] != request_id
        ):
            response_str = await ws.receive_str()
            time.sleep(1)
        try:
            # Check response format
            parse_text(response_str, requests.REQUIREMENTS_RESPONSE_SCHEMA)
            # If valid display response
            print("Response: " + response_str)
        except ValidationError:
            # If invalid response...
            try:
                # Check error response format
                parse_text(response_str, requests.ERROR_RESPONSE_SCHEMA)
                # If valid, display error response
                print("Error response: " + response_str)
            except ValidationError as exception:
                # If invalid, display exception on response validation
                print(exception)

        # Close session
        await client.close()

    except (aiohttp.WSServerHandshakeError, ValueError) as e:
        print("Websocket handshake {0} : {1}".format(type(e).__name__, str(e)))
    except (aiohttp.ClientError, gaierror, TimeoutError) as e:
        print("{0} : {1}".format(str(e), WS2P_ENDPOINT))
    except jsonschema.ValidationError as e:
        print("{:}:{:}".format(str(e.__class__.__name__), str(e)))


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
