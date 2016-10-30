import asyncio
import aiohttp
from aiohttp.client_reqrep import ClientResponse
import duniterpy.api.bma as bma
from duniterpy.documents import BMAEndpoint

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the BASIC_MERKLED_API
BMA_ENDPOINT = "BASIC_MERKLED_API cgeek.fr 9330"

################################################

# Latest duniter-python-api is asynchronous and you have to create an aiohttp session to send request
# ( http://pythonhosted.org/aiohttp )
AIOHTTP_SESSION = aiohttp.ClientSession()

async def get_summary_info():
    """
    Get the node info

    :rtype: ClientResponse
    """
    # Here we request for the path /node/summary
    return await bma.node.Summary(BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler()).get(AIOHTTP_SESSION)

async def get_current_block():
    """
    Get the current block data

    :rtype: ClientResponse
    """
    # Here we request for the path blockchain/current
    return await bma.blockchain.Current(BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler()) \
        .get(AIOHTTP_SESSION)

async def get_block(block_number):
    """
    Get the a block data
    :param: int block_number Number of the block

    :rtype: ClientResponse
    """
    # Here we request for the path blockchain/block/N
    return await bma.blockchain.Block(BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler(), block_number)\
        .get(AIOHTTP_SESSION)


async def main():
    """
    Main code
    """
    print(await get_summary_info())

    print(await get_current_block())

    print(await get_block(0))

with AIOHTTP_SESSION:

    # Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
    # ( https://docs.python.org/3/library/asyncio.html )
    asyncio.get_event_loop().run_until_complete(main())
