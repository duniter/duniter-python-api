import asyncio
import json
import time

from _socket import gaierror

import aiohttp
import jsonschema
from jsonschema import ValidationError

from duniterpy.helpers import get_ws2p_challenge
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

    # # prompt hidden user entry
    # salt = getpass.getpass("Enter your passphrase (salt): ")
    #
    # # prompt hidden user entry
    # password = getpass.getpass("Enter your password: ")
    salt = password = "toto"

    # init signing_key instance
    signing_key = SigningKey.from_credentials(salt, password)

    connect_document = Connect(CURRENCY, signing_key.pubkey)
    connect_message = connect_document.get_signed_json(signing_key)

    # Create Client from endpoint string in Duniter format
    client = Client(WS2P_ENDPOINT)

    try:
        # Create Web Socket connection on block path
        ws_connection = client.connect_ws()

        # From the documentation ws_connection should be a ClientWebSocketResponse object...
        #
        # https://docs.aiohttp.org/en/stable/client_quickstart.html#websockets
        #
        # In reality, aiohttp.session.ws_connect() returns a aiohttp.client._WSRequestContextManager instance.
        # It must be used in a with statement to get the ClientWebSocketResponse instance from it (__aenter__).
        # At the end of the with statement, aiohttp.client._WSRequestContextManager.__aexit__ is called
        # and close the ClientWebSocketResponse in it.

        # Mandatory to get the "for msg in ws" to work !
        async with ws_connection as ws:
            print("Connected successfully to web socket endpoint")

            # START HANDSHAKE #######################################################
            print("\nSTART HANDSHAKE...")

            print("Send CONNECT message")
            await ws.send_str(connect_message)

            # Iterate on each message received...
            async for msg in ws:
                # if message type is text...
                if msg.type == aiohttp.WSMsgType.TEXT:
                    # print(msg.data)
                    try:
                        # Validate json string with jsonschema and return a dict
                        data = parse_text(msg.data, ws2p.network.WS2P_CONNECT_MESSAGE_SCHEMA)

                    except jsonschema.exceptions.ValidationError:
                        try:
                            # Validate json string with jsonschema and return a dict
                            data = parse_text(msg.data, ws2p.network.WS2P_ACK_MESSAGE_SCHEMA)

                        except jsonschema.exceptions.ValidationError:
                            try:
                                # Validate json string with jsonschema and return a dict
                                data = parse_text(msg.data, ws2p.network.WS2P_OK_MESSAGE_SCHEMA)

                            except jsonschema.exceptions.ValidationError:
                                continue

                            print("Received a OK message")

                            Ok(CURRENCY, remote_connect_document.pubkey, connect_document.challenge, data["sig"])
                            print("Received OK message signature is valid")
                            # do not wait for messages anymore
                            break

                        print("Received a ACK message")

                        # create ACK document from ACK response to verify signature
                        Ack(CURRENCY, data["pub"], connect_document.challenge, data["sig"])
                        print("Received ACK message signature is valid")
                        # Si ACK response ok, create OK message
                        ok_message = Ok(CURRENCY, signing_key.pubkey, connect_document.challenge).get_signed_json(
                            signing_key)

                        # send OK message
                        print("Send OK message...")
                        await ws.send_str(ok_message)
                        continue

                    print("Received a CONNECT message")

                    remote_connect_document = Connect(CURRENCY, data["pub"], data["challenge"], data["sig"])
                    print("Received CONNECT message signature is valid")

                    ack_message = Ack(CURRENCY, signing_key.pubkey,
                                      remote_connect_document.challenge).get_signed_json(
                        signing_key)
                    # send ACK message
                    print("Send ACK message...")
                    await ws.send_str(ack_message)

                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    # Connection is closed
                    print("Web socket connection closed !")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    # Connection error
                    print("Web socket connection error !")

            # END HANDSHAKE #######################################################
            print("END OF HANDSHAKE\n")

            # send ws2p request
            print("Send getCurrent() request")
            request_id = get_ws2p_challenge()[:8]
            await ws.send_str(requests.get_current(request_id))

            # wait response with request id
            response_str = await ws.receive_str()
            while "resId" not in json.loads(response_str) or (
                    "resId" in json.loads(response_str) and json.loads(response_str)["resId"] != request_id):
                response_str = await ws.receive_str()
                time.sleep(1)
            try:
                # check response format
                parse_text(response_str, requests.BLOCK_RESPONSE_SCHEMA)
                # if valid display response
                print("Response: " + response_str)
            except ValidationError as exception:
                # if invalid response...
                try:
                    # check error response format
                    parse_text(response_str, requests.ERROR_RESPONSE_SCHEMA)
                    # if valid, display error response
                    print("Error response: " + response_str)
                except ValidationError as e:
                    # if invalid, display exception on response validation
                    print(exception)

            # send ws2p request
            print("Send getBlock(360000) request")
            request_id = get_ws2p_challenge()[:8]
            await ws.send_str(requests.get_block(request_id, 360000))

            # wait response with request id
            response_str = await ws.receive_str()
            while "resId" not in json.loads(response_str) or (
                    "resId" in json.loads(response_str) and json.loads(response_str)["resId"] != request_id):
                response_str = await ws.receive_str()
                time.sleep(1)
            try:
                # check response format
                parse_text(response_str, requests.BLOCK_RESPONSE_SCHEMA)
                # if valid display response
                print("Response: " + response_str)
            except ValidationError as exception:
                # if invalid response...
                try:
                    # check error response format
                    parse_text(response_str, requests.ERROR_RESPONSE_SCHEMA)
                    # if valid, display error response
                    print("Error response: " + response_str)
                except ValidationError as e:
                    # if invalid, display exception on response validation
                    print(exception)

            # send ws2p request
            print("Send getBlocks(360000, 2) request")
            request_id = get_ws2p_challenge()[:8]
            await ws.send_str(requests.get_blocks(request_id, 360000, 2))

            # wait response with request id
            response_str = await ws.receive_str()
            while "resId" not in json.loads(response_str) or (
                    "resId" in json.loads(response_str) and json.loads(response_str)["resId"] != request_id):
                response_str = await ws.receive_str()
                time.sleep(1)
            try:
                # check response format
                parse_text(response_str, requests.BLOCKS_RESPONSE_SCHEMA)
                # if valid display response
                print("Response: " + response_str)
            except ValidationError as exception:
                # if invalid response...
                try:
                    # check error response format
                    parse_text(response_str, requests.ERROR_RESPONSE_SCHEMA)
                    # if valid, display error response
                    print("Error response: " + response_str)
                except ValidationError as e:
                    # if invalid, display exception on response validation
                    print(exception)

            # send ws2p request
            print("Send getRequirementsPending(3) request")
            request_id = get_ws2p_challenge()[:8]
            await ws.send_str(requests.get_requirements_pending(request_id, 3))
            # wait response with request id
            response_str = await ws.receive_str()
            while "resId" not in json.loads(response_str) or (
                    "resId" in json.loads(response_str) and json.loads(response_str)["resId"] != request_id):
                response_str = await ws.receive_str()
                time.sleep(1)
            try:
                # check response format
                parse_text(response_str, requests.REQUIREMENTS_RESPONSE_SCHEMA)
                # if valid display response
                print("Response: " + response_str)
            except ValidationError as exception:
                # if invalid response...
                try:
                    # check error response format
                    parse_text(response_str, requests.ERROR_RESPONSE_SCHEMA)
                    # if valid, display error response
                    print("Error response: " + response_str)
                except ValidationError as e:
                    # if invalid, display exception on response validation
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
