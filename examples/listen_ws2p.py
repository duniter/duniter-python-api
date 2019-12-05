import asyncio
import json

from _socket import gaierror

import aiohttp
import jsonschema
from jsonschema import ValidationError

from duniterpy.key import SigningKey

from duniterpy.helpers.ws2p import handshake
from duniterpy.api.client import Client

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT] [PATH]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT] [PATH]
# Here we use the WS2P API (WS2P [UUID] [DOMAIN] [PORT] [PATH])
# You can find the UUID of a node with the /network/ws2p/heads BMA API request,
# using the UUID of the HEAD with step 0
# or in your node user interface in the network view in the WS2PID column
WS2P_ENDPOINT = "WS2P 96675302 g1-test.duniter.org 443"
CURRENCY = "g1-test"


################################################


async def main():
    """
    Main code
    """
    # Arbitrary credentials to create the node key pair to sign ws2p documents
    salt = password = "test"

    # Init signing_key instance
    signing_key = SigningKey.from_credentials(salt, password)

    # Create Client from endpoint string in Duniter format
    client = Client(WS2P_ENDPOINT)

    try:
        # Create a Web Socket connection
        ws = await client.connect_ws()

        print("Successfully connected to the web socket endpoint")

        # HANDSHAKE #######################################################
        try:
            # Resolve handshake
            print("Handshake...")
            await handshake(ws, signing_key, CURRENCY, True)
        except ValidationError as exception:
            print(exception.message)
            print("HANDSHAKE FAILED !")
            exit(1)

        print("Handshake ok")

        loop = True
        # Iterate on each message received...
        while loop:
            print("Waiting message...")
            # Wait and capture next message
            data = await ws.receive_json()
            print("Message received:")
            print(json.dumps(data, indent=2))

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
