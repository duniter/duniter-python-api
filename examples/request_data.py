"""
Copyright  2014-2021 Vincent Texier <vit@free.fr>

DuniterPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DuniterPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import asyncio
from duniterpy.api.client import Client, RESPONSE_AIOHTTP
from duniterpy.api import bma

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT] [PATH]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT] [PATH]
# Here we use the secure BASIC_MERKLED_API (BMAS)
BMAS_ENDPOINT = "BMAS g1-test.duniter.org 443"


################################################


async def main():
    """
    Main code (synchronous requests)
    """
    # Create Client from endpoint string in Duniter format
    client = Client(BMAS_ENDPOINT)

    # Get the node summary infos by dedicated method (with json schema validation)
    print("\nCall bma.node.summary:")
    response = await client(bma.node.summary)
    print(response)

    # Get the money parameters located in the first block
    print("\nCall bma.blockchain.parameters:")
    response = await client(bma.blockchain.parameters)
    print(response)

    # Get the current block
    print("\nCall bma.blockchain.current:")
    response = await client(bma.blockchain.current)
    print(response)

    # Get the block number 10
    print("\nCall bma.blockchain.block(10):")
    response = await client(bma.blockchain.block, 10)
    print(response)

    # jsonschema validator
    summary_schema = {
        "type": "object",
        "properties": {
            "duniter": {
                "type": "object",
                "properties": {
                    "software": {"type": "string"},
                    "version": {"type": "string"},
                    "forkWindowSize": {"type": "number"},
                },
                "required": ["software", "version"],
            }
        },
        "required": ["duniter"],
    }

    # Get the node summary infos (direct REST GET request)
    print("\nCall direct get on node/summary")
    response = await client.get(
        "node/summary", rtype=RESPONSE_AIOHTTP, schema=summary_schema
    )
    print(response)

    # Close client aiohttp session
    await client.close()


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
