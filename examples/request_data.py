import asyncio
import aiohttp
import duniterpy.api.bma as bma
from duniterpy.documents import BMAEndpoint

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the BASIC_MERKLED_API
BMA_ENDPOINT = "BASIC_MERKLED_API g1.duniter.org 10901"

################################################

# Latest duniter-python-api is asynchronous and you have to create an aiohttp session to send request
# ( http://pythonhosted.org/aiohttp )
AIOHTTP_SESSION = aiohttp.ClientSession()

async def main():
    """
    Main code
    """
    # connection handler from BMA endpoint
    connection = next(BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler(AIOHTTP_SESSION))

    # Get the node summary infos
    response = await bma.node.summary(connection)
    print(response)

    # Get the current block data
    response = await bma.blockchain.parameters(connection)
    print(response)

    # Get the current block data
    response = await bma.blockchain.current(connection)
    print(response)

    # Get the block number 10
    response = await bma.blockchain.block(connection, 10)
    print(response)

with AIOHTTP_SESSION:

    # Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
    # ( https://docs.python.org/3/library/asyncio.html )
    asyncio.get_event_loop().run_until_complete(main())
