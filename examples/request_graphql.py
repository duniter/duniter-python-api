import asyncio

from duniterpy.api.client import Client

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the secure BASIC_MERKLED_API (BMAS)
SWAPI_ENDPOINT = "BMAS swapi.graph.cool 443"


################################################


async def main():
    client = Client(SWAPI_ENDPOINT)

    query = """query {
       allFilms {
        title,
        characters {
          name
        }
      }
     }
    """

    response = await client.query(query)
    print(response)

    # Close client aiohttp session
    await client.close()


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
