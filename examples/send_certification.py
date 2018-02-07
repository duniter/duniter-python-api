import asyncio
import aiohttp
import getpass
import duniterpy.api.bma as bma
from duniterpy.documents import BMAEndpoint, BlockUID, Identity, Certification
from duniterpy.key import SigningKey, ScryptParams


# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the BASIC_MERKLED_API
BMA_ENDPOINT = "BASIC_MERKLED_API g1-test.duniter.org 10900"

################################################

# Latest duniter-python-api is asynchronous and you have to create an aiohttp session to send request
# ( http://pythonhosted.org/aiohttp )
AIOHTTP_SESSION = aiohttp.ClientSession()

async def get_identity_document(connection, current_block, pubkey):
    """
    Get the identity document of the pubkey

    :param bma.api.ConnectionHandler connection: Connection handler
    :param dict current_block: Current block data
    :param str pubkey: UID/Public key

    :rtype: Identity
    """
    # Here we request for the path wot/lookup/pubkey
    lookup_data = await bma.wot.lookup(connection, pubkey)

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


def get_certification_document(current_block, self_cert_document, from_pubkey, salt, password):
    """
    Create and return a Certification document

    :param dict current_block: Current block data
    :param Identity self_cert_document: Identity document
    :param str from_pubkey: Pubkey of the certifier
    :param str salt: Secret salt (DO NOT SHOW IT ANYWHERE, IT IS SECRET !!!)
    :param str password: Secret password (DO NOT SHOW IT ANYWHERE, IT IS SECRET !!!)

    :rtype: Certification
    """
    # construct Certification Document
    certification = Certification(
        version=10,
        currency=current_block['currency'],
        pubkey_from=from_pubkey,
        pubkey_to=self_cert_document.pubkey,
        timestamp=BlockUID(current_block['number'], current_block['hash']),
        signature=""
    )
    # sign document
    key = SigningKey(salt, password, ScryptParams(4096, 16, 1))
    certification.sign(self_cert_document, [key])

    return certification

async def main():
    """
    Main code
    """
    # connection handler from BMA endpoint
    connection = next(BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler(AIOHTTP_SESSION))

    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password: ")

    # prompt entry
    pubkey_from = input("Enter your pubkey: ")

    # prompt entry
    pubkey_to = input("Enter certified pubkey: ")

    # capture current block to get version and currency and blockstamp
    current_block = await bma.blockchain.current(connection)

    # create our Identity document to sign the Certification document
    identity = await get_identity_document(connection, current_block, pubkey_to)

    # send the Certification document to the node
    certification = get_certification_document(current_block, identity, pubkey_from, salt, password)

    # Here we request for the path wot/certify
    response = await bma.wot.certify(connection, certification.signed_raw(identity))

    if response.status == 200:
        print(await response.text())
    else:
        print("Error while publishing certification: {0}".format(await response.text()))
    response.close()

with AIOHTTP_SESSION:

    # Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
    # ( https://docs.python.org/3/library/asyncio.html )
    asyncio.get_event_loop().run_until_complete(main())
