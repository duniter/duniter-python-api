import asyncio
import json
from _socket import gaierror

import aiohttp
import jsonschema

from duniterpy.api import bma
from duniterpy.api.client import Client

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT] [PATH]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT] [PATH]
# Here we use the secure BASIC_MERKLED_API (BMAS)
BMAS_ENDPOINT = "BMAS g1-test.duniter.org 443"


################################################


async def main():
    """
    Main code
    """
    # Create Client from endpoint string in Duniter format
    client = Client(BMAS_ENDPOINT)

    try:
        # Create Web Socket connection on block path (async method)
        ws = await client(bma.ws.block)  # Type: WSConnection

        print("Connected successfully to web socket block path")

        loop = True
        # Iterate on each message received...
        while loop:
            print("Waiting message...")
            # Wait and capture next message
            data = await ws.receive_json()
            jsonschema.validate(data, bma.ws.WS_BLOCK_SCHEMA)
            print("Message received:")
            print(json.dumps(data, indent=2))

        # Close session
        await client.close()

    except (aiohttp.WSServerHandshakeError, ValueError) as e:
        print("Websocket block {0} : {1}".format(type(e).__name__, str(e)))
    except (aiohttp.ClientError, gaierror, TimeoutError) as e:
        print("{0} : {1}".format(str(e), BMAS_ENDPOINT))
    except jsonschema.ValidationError as e:
        print("{:}:{:}".format(str(e.__class__.__name__), str(e)))


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
