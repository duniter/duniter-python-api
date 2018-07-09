import asyncio
import getpass

import duniterpy.api.bma as bma
from duniterpy.api.client import Client
from duniterpy.documents import BlockUID, Identity, Membership
from duniterpy.key import SigningKey

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the secure BASIC_MERKLED_API (BMAS)
BMAS_ENDPOINT = "BMAS g1-test.duniter.org 443"


################################################


def get_identity_document(current_block: dict, uid: str, salt: str, password: str) -> Identity:
    """
    Get an Identity document

    :param current_block: Current block data
    :param uid: Unique Identifier
    :param salt: Passphrase of the account
    :param password: Password of the account

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


def get_membership_document(membership_type: str, current_block: dict, identity: Identity, salt: str,
                            password: str) -> Membership:
    """
    Get a Membership document

    :param membership_type: "IN" to ask for membership or "OUT" to cancel membership
    :param current_block: Current block data
    :param identity: Identity document
    :param salt: Passphrase of the account
    :param password: Password of the account

    :rtype: Membership
    """

    # get current block BlockStamp
    timestamp = BlockUID(current_block['number'], current_block['hash'])

    # create keys from credentials
    key = SigningKey(salt, password)

    # create identity document
    membership = Membership(
        version=10,
        currency=current_block['currency'],
        issuer=key.pubkey,
        membership_ts=timestamp,
        membership_type=membership_type,
        uid=identity.uid,
        identity_ts=identity.timestamp,
        signature=None
    )

    # sign document
    membership.sign([key])

    return membership


async def main():
    """
    Main code
    """
    # Create Client from endpoint string in Duniter format
    client = Client(BMAS_ENDPOINT)

    # Get the node summary infos by dedicated method (with json schema validation)
    response = await client(bma.node.summary)
    print(response)

    # capture current block to get version and currency and blockstamp
    current_block = await client(bma.blockchain.current)

    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password: ")

    # prompt entry
    uid = input("Enter your UID: ")

    # create our signed identity document
    identity = get_identity_document(current_block, uid, salt, password)

    # create a membership demand document
    membership = get_membership_document("IN", current_block, identity, salt, password)

    # send the membership signed raw document to the node
    response = await client(bma.blockchain.membership, membership.signed_raw())

    if response.status == 200:
        print(await response.text())
    else:
        print("Error while publishing membership : {0}".format(await response.text()))

    # Close client aiohttp session
    await client.close()


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
