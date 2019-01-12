import asyncio
import getpass

import duniterpy.api.bma as bma
from duniterpy.api.client import Client
from duniterpy.documents import BlockUID, Identity, Certification
from duniterpy.key import SigningKey

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the secure BASIC_MERKLED_API (BMAS)
BMAS_ENDPOINT = "BMAS g1-test.duniter.org 443"


################################################


async def get_identity_document(client: Client, current_block: dict, pubkey: str) -> Identity:
    """
    Get the identity document of the pubkey

    :param client: Client to connect to the api
    :param current_block: Current block data
    :param pubkey: UID/Public key

    :rtype: Identity
    """
    # Here we request for the path wot/lookup/pubkey
    lookup_data = await client(bma.wot.lookup, pubkey)

    # init vars
    uid = None
    timestamp = BlockUID.empty()
    signature = None

    # parse results
    for result in lookup_data['results']:
        if result["pubkey"] == pubkey:
            uids = result['uids']
            for uid_data in uids:
                # capture data
                timestamp = BlockUID.from_str(uid_data["meta"]["timestamp"])
                uid = uid_data["uid"]
                signature = uid_data["self"]

            # return self-certification document
            return Identity(
                version=10,
                currency=current_block['currency'],
                pubkey=pubkey,
                uid=uid,
                ts=timestamp,
                signature=signature
            )


def get_certification_document(current_block: dict, self_cert_document: Identity, from_pubkey: str) -> Certification:
    """
    Create and return a Certification document

    :param current_block: Current block data
    :param self_cert_document: Identity document
    :param from_pubkey: Pubkey of the certifier

    :rtype: Certification
    """
    # construct Certification Document
    return Certification(version=10, currency=current_block['currency'], pubkey_from=from_pubkey,
                                  identity=self_cert_document,
                                  timestamp=BlockUID(current_block['number'], current_block['hash']), signature="")


async def main():
    """
    Main code
    """
    # Create Client from endpoint string in Duniter format
    client = Client(BMAS_ENDPOINT)

    # Get the node summary infos to test the connection
    response = await client(bma.node.summary)
    print(response)

    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password: ")

    # create key from credentials
    key = SigningKey.from_credentials(salt, password)
    pubkey_from = key.pubkey

    # prompt entry
    pubkey_to = input("Enter certified pubkey: ")

    # capture current block to get version and currency and blockstamp
    current_block = await client(bma.blockchain.current)

    # create our Identity document to sign the Certification document
    identity = await get_identity_document(client, current_block, pubkey_to)

    # send the Certification document to the node
    certification = get_certification_document(current_block, identity, pubkey_from)

    # sign document
    certification.sign([key])

    # Here we request for the path wot/certify
    response = await client(bma.wot.certify, certification.signed_raw())

    if response.status == 200:
        print(await response.text())
    else:
        print("Error while publishing certification: {0}".format(await response.text()))

    # Close client aiohttp session
    await client.close()


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
