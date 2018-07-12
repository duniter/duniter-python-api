import asyncio

from duniterpy.api import bma
from duniterpy.api.client import Client

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the secure BASIC_MERKLED_API (BMAS)
BMAS_ENDPOINT = "BMAS g1-test.duniter.org 443"


################################################


async def print_response(request):
    print(await request)


async def main():
    """
    Main code (asynchronous requests)

    You can send one millions request with aiohttp :

    https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html

    But don't do that on one server, it's DDOS !

    """
    # Create Client from endpoint string in Duniter format
    client = Client(BMAS_ENDPOINT)
    tasks = []

    # Get the node summary infos by dedicated method (with json schema validation)
    print("\nCall bma.node.summary:")
    task = asyncio.ensure_future(client(bma.node.summary))
    tasks.append(task)

    # Get the money parameters located in the first block
    print("\nCall bma.blockchain.parameters:")
    task = asyncio.ensure_future(client(bma.blockchain.parameters))
    tasks.append(task)

    responses = await asyncio.gather(*tasks)
    # you now have all response bodies in this variable
    print("\nResponses:")
    print(responses)

    # Close client aiohttp session
    await client.close()


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
