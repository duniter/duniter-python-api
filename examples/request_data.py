import asyncio
from duniterpy.api.client import Client
from duniterpy.api import bma

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

    # Get the node summary infos (direct REST GET request)
    response = await client.get('node/summary')
    print(response)

    # Get the node summary infos by dedicated method (with json schema validation)
    response = await bma.node.summary(client)
    print(response)

    # Get the money parameters located in the first block
    response = await bma.blockchain.parameters(client)
    print(response)

    # Get the current block
    response = await bma.blockchain.current(client)
    print(response)

    # Get the block number 10
    response = await bma.blockchain.block(client, 10)
    print(response)

    # Close client aiohttp session
    await client.close()

# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
