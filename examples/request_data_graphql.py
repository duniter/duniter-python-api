import sys
import json

from duniterpy.api.client import Client
from graphql import get_introspection_query, build_client_schema, language, validate
from graphql.error import GraphQLSyntaxError

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the secure BASIC_MERKLED_API (BMAS) for standard http over ssl requests
GVA_ENDPOINT = "GVA S g1.librelois.fr 443 gva"


################################################


async def main():
    client = Client(GVA_ENDPOINT)

    # get query to get schema from api
    query = get_introspection_query(False)
    # get schema from api
    response = await client.query(query)
    # convert response dict to schema
    schema = build_client_schema(response["data"])

    # create currentUd query
    query = """{
        currentUd {
            amount
            }
        }
    """

    # check query syntax
    try:
        ast_document = language.parse(query)
    except GraphQLSyntaxError as exception:
        print(f"Query syntax error: {exception.message}")
        sys.exit(1)

    # validate query against schema
    errors = validate(schema, ast_document)
    if errors:
        print(f"Schema errors: {errors}")
        sys.exit(1)

    # send valid query to api
    response = await client.query(query)
    if isinstance(response, str):
        print(response)
    else:
        print(json.dumps(response, indent=2))

    # Close client aiohttp session
    await client.close()


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
