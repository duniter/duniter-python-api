import asyncio
from _socket import gaierror

import aiohttp
import jsonschema

from duniterpy.api import bma
from duniterpy.api.client import Client, parse_text

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
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
        # Create Web Socket connection on block path
        ws_connection = client(bma.ws.block)

        # Mandatory to get the "for msg in ws" to work !
        # But it should work on the ws_connection which is a ClientWebSocketResponse object...
        # https://docs.aiohttp.org/en/stable/client_quickstart.html#websockets
        async with ws_connection as ws:
            print("Connected successfully to block ws")
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print("Received a block")
                    block_data = parse_text(msg.data, bma.ws.WS_BLOCK_SCHEMA)
                    print(block_data)
                    await client.close()
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    print("Web socket connection closed !")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print("Web socket connection error !")

    except (aiohttp.WSServerHandshakeError, ValueError) as e:
        print("Websocket block {0} : {1}".format(type(e).__name__, str(e)))
    except (aiohttp.ClientError, gaierror, TimeoutError) as e:
        print("{0} : {1}".format(str(e), BMAS_ENDPOINT))
    except jsonschema.ValidationError as e:
        print("{:}:{:}".format(str(e.__class__.__name__), str(e)))


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
