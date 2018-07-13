import asyncio
from _socket import gaierror

import aiohttp
import jsonschema

from duniterpy.api.client import Client, parse_text
from duniterpy.api import ws2p

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the secure BASIC_MERKLED_API (BMAS)
WS2P_ENDPOINT = "WS2P id ip port"

################################################


async def main():
    """
    Main code (synchronous requests)
    """
    # Create Client from endpoint string in Duniter format
    client = Client(WS2P_ENDPOINT)

    # Get the node summary infos by dedicated method (with json schema validation)
    print("\nCall ws2p.heads:")
    try:
        # Create Web Socket connection on block path
        ws_connection = client(ws2p.network.heads)

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
            print("Connected successfully to web socket block path")
            # Iterate on each message received...
            async for msg in ws:
                # if message type is text...
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print("Received a block")
                    # Validate jsonschema and return a the json dict
                    block_data = parse_text(msg.data, ws2p.network.WS2P_HEADS_SCHEMA)
                    print(block_data)
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    # Connection is closed
                    print("Web socket connection closed !")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    # Connection error
                    print("Web socket connection error !")

                # Close session
                await client.close()

    except (aiohttp.WSServerHandshakeError, ValueError) as e:
        print("Websocket block {0} : {1}".format(type(e).__name__, str(e)))
    except (aiohttp.ClientError, gaierror, TimeoutError) as e:
        print("{0} : {1}".format(str(e), WS2P_ENDPOINT))
    except jsonschema.ValidationError as e:
        print("{:}:{:}".format(str(e.__class__.__name__), str(e)))


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
