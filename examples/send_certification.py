import asyncio
import aiohttp
import duniterpy.api.bma as bma
from duniterpy.documents import BMAEndpoint, BlockUID, SelfCertification, Certification
from duniterpy.key import SigningKey


# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the BASIC_MERKLED_API
BMA_ENDPOINT = "BASIC_MERKLED_API cgeek.fr 9330"

# Public key of the certifier
FROM_PUBKEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Credentials should be prompted or kept in a separate secure file
# create a file with the salt on the first line and the password on the second line
# the script will load them from the file
FROM_CREDENTIALS_FILE = "/home/username/.credentials.txt"

# Public key to certified
TO_PUBKEY = "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"

################################################


# Latest duniter-python-api is asynchronous and you have to create an aiohttp session to send request
# ( http://pythonhosted.org/aiohttp )
AIOHTTP_SESSION = aiohttp.ClientSession()

async def get_current_block(connection):
    """
    Get the current block data

    :param bma.api.ConnectionHandler connection: Connection handler
    :rtype: dict
    """
    # Here we request for the path blockchain/block/N
    return await bma.blockchain.Current(connection).get(AIOHTTP_SESSION)

async def get_identity_document(connection, current_block, pubkey):
    """
    Get the identity document of the pubkey

    :param bma.api.ConnectionHandler connection: Connection handler
    :param dict current_block: Current block data
    :param str pubkey: Public key

    :rtype: SelfCertification
    """
    # Here we request for the path wot/lookup/pubkey
    lookup_data = await bma.wot.Lookup(connection, pubkey).get(AIOHTTP_SESSION)

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
            return SelfCertification(
                version=2,
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
    :param SelfCertification self_cert_document: SelfCertification document
    :param str from_pubkey: Pubkey of the certifier
    :param str salt: Secret salt (DO NOT SHOW IT ANYWHERE, IT IS SECRET !!!)
    :param str password: Secret password (DO NOT SHOW IT ANYWHERE, IT IS SECRET !!!)

    :rtype: Certification
    """
    # construct Certification Document
    certification = Certification(
        version=2,
        currency=current_block['currency'],
        pubkey_from=from_pubkey,
        pubkey_to=self_cert_document.pubkey,
        timestamp=BlockUID(current_block['number'], current_block['hash']),
        signature=""
    )
    # sign document
    key = SigningKey(salt, password)
    certification.sign(self_cert_document, [key])

    return certification

async def main():
    """
    Main code
    """
    # connection handler from BMA endpoint
    connection = BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler()

    # capture current block to get version and currency and blockstamp
    current_block = await get_current_block(connection)

    # create our SelfCertification document to sign the Certification document
    identity = await get_identity_document(connection, current_block, TO_PUBKEY)

    # load credentials from a text file
    salt, password = open(FROM_CREDENTIALS_FILE).readlines()

    # cleanup newlines
    salt, password = salt.strip(), password.strip()

    # send the Certification document to the node
    certification = get_certification_document(current_block, identity, FROM_PUBKEY, salt, password)

    # Here we request for the path wot/certify
    data = {'cert': certification.signed_raw(identity)}
    response = await bma.wot.Certify(connection).post(AIOHTTP_SESSION, **data)

    print(response)

    response.close()

with AIOHTTP_SESSION:

    # Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
    # ( https://docs.python.org/3/library/asyncio.html )
    asyncio.get_event_loop().run_until_complete(main())
