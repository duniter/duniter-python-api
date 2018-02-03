import asyncio
import aiohttp
import getpass

import duniterpy.api.bma as bma
from duniterpy.documents import BMAEndpoint, BlockUID, Identity
from duniterpy.key import SigningKey


# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the BASIC_MERKLED_API
BMA_ENDPOINT = "BASIC_MERKLED_API g1.duniter.org 10901"

# Your unique identifier in the Web of Trust
UID = "MyIdentity"

################################################
# Latest duniter-python-api is asynchronous and you have to create an aiohttp session to send request
# ( http://pythonhosted.org/aiohttp )
AIOHTTP_SESSION = aiohttp.ClientSession()


def get_identity_document(current_block, uid, salt, password):
    """
    Get an Identity document

    :param dict current_block: Current block data
    :param str uid: Unique Identifier
    :param str salt: Passphrase of the account
    :param str password: Password of the account

    :rtype: Identity
    """

    # get current block BlockStamp
    timestamp = BlockUID(current_block['number'], current_block['hash'])

    # create keys from credentials
    key = SigningKey(salt, password)

    # create identity document
    identity = Identity(
        version=10,
        currency=current_block['currency'],
        pubkey=key.pubkey,
        uid=uid,
        ts=timestamp,
        signature=None
    )

    # sign document
    identity.sign([key])

    return identity


async def main():
    """
    Main code
    """

    # connection handler from BMA endpoint
    connection = next(BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler(AIOHTTP_SESSION))
    # capture current block to get version and currency and blockstamp
    current_block = await bma.blockchain.current(connection)

    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password: ")

    # create our signed identity document
    identity = get_identity_document(current_block, UID, salt, password)

    # send the identity document to the node
    response = await bma.wot.add(connection, identity.signed_raw())
    if response.status == 200:
        print(await response.text())
    else:
        print("Error while publishing identity : {0}".format(await response.text()))
    response.close()

# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )

with AIOHTTP_SESSION:
    asyncio.get_event_loop().run_until_complete(main())
