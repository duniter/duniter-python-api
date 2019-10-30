import asyncio
import json
import time

from _socket import gaierror

import aiohttp
import jsonschema
from jsonschema import ValidationError

from duniterpy.tools import get_ws2p_challenge
from duniterpy.key import SigningKey

from duniterpy.helpers.ws2p import handshake
from duniterpy.api.ws2p import requests
from duniterpy.api.client import Client

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

    # Create Client from endpoint string in Duniter format
    client = Client(WS2P_ENDPOINT)

    try:
        # Create a Web Socket connection
        ws = await client.connect_ws()

        print("Connected successfully to web socket endpoint")

        # HANDSHAKE #######################################################
        try:
            await handshake(ws, signing_key, CURRENCY, True)
        except ValidationError as exception:
            print(exception.message)
            print("HANDSHAKE FAILED !")
            exit(1)

        # Send ws2p request
        print("Send getCurrent() request")
        request_id = get_ws2p_challenge()[:8]
        await ws.send_str(requests.get_current(request_id))

        # Wait response with request id
        response = await ws.receive_json()
        while "resId" not in response or (
            "resId" in response and response["resId"] != request_id
        ):
            response = await ws.receive_json()
            time.sleep(1)
        try:
            # Check response format
            jsonschema.validate(response, requests.BLOCK_RESPONSE_SCHEMA)
            # If valid display response
            print("Response: " + json.dumps(response, indent=2))
        except ValidationError:
            # If invalid response...
            try:
                # Check error response format
                jsonschema.validate(response, requests.ERROR_RESPONSE_SCHEMA)
                # If valid, display error response
                print("Error response: " + json.dumps(response, indent=2))
            except ValidationError as exception:
                # If invalid, display exception on response validation
                print(exception)

        # Send ws2p request
        print("Send getBlock(360000) request")
        request_id = get_ws2p_challenge()[:8]
        await ws.send_str(requests.get_block(request_id, 360000))

        # Wait response with request id
        response = await ws.receive_json()
        while "resId" not in response or (
            "resId" in response and response["resId"] != request_id
        ):
            response = await ws.receive_json()
            time.sleep(1)
        try:
            # Check response format
            jsonschema.validate(response, requests.BLOCK_RESPONSE_SCHEMA)
            # If valid display response
            print("Response: " + json.dumps(response, indent=2))
        except ValidationError:
            # If invalid response...
            try:
                # Check error response format
                jsonschema.validate(response, requests.ERROR_RESPONSE_SCHEMA)
                # If valid, display error response
                print("Error response: " + json.dumps(response, indent=2))
            except ValidationError as exception:
                # If invalid, display exception on response validation
                print(exception)

        # Send ws2p request
        print("Send getBlocks(360000, 2) request")
        request_id = get_ws2p_challenge()[:8]
        await ws.send_str(requests.get_blocks(request_id, 360000, 2))

        # Wait response with request id
        response = await ws.receive_json()
        while "resId" not in response or (
            "resId" in response and response["resId"] != request_id
        ):
            response = await ws.receive_json()
            time.sleep(1)
        try:
            # Check response format
            jsonschema.validate(response, requests.BLOCKS_RESPONSE_SCHEMA)
            # If valid display response
            print("Response: " + json.dumps(response, indent=2))
        except ValidationError:
            # If invalid response...
            try:
                # Check error response format
                jsonschema.validate(response, requests.ERROR_RESPONSE_SCHEMA)
                # If valid, display error response
                print("Error response: " + json.dumps(response, indent=2))
            except ValidationError as exception:
                # If invalid, display exception on response validation
                print(exception)

        # Send ws2p request
        print("Send getRequirementsPending(3) request")
        request_id = get_ws2p_challenge()[:8]
        await ws.send_str(requests.get_requirements_pending(request_id, 3))
        # Wait response with request id
        response = await ws.receive_json()
        while "resId" not in response or (
            "resId" in response and response["resId"] != request_id
        ):
            response = await ws.receive_json()
            time.sleep(1)
        try:
            # Check response format
            jsonschema.validate(response, requests.REQUIREMENTS_RESPONSE_SCHEMA)
            # If valid display response
            print("Response: " + json.dumps(response, indent=2))
        except ValidationError:
            # If invalid response...
            try:
                # Check error response format
                jsonschema.validate(response, requests.ERROR_RESPONSE_SCHEMA)
                # If valid, display error response
                print("Error response: " + json.dumps(response, indent=2))
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
