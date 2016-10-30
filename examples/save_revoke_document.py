import asyncio
import aiohttp
import duniterpy.api.bma as bma
from duniterpy.documents import BMAEndpoint, BlockUID, SelfCertification
from duniterpy.documents import Revocation
from duniterpy.key import SigningKey

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the BASIC_MERKLED_API
BMA_ENDPOINT = "BASIC_MERKLED_API cgeek.fr 9330"

# Credentials should be prompted or kept in a separate secure file
# create a file with the salt on the first line and the password on the second line
# the script will load them from the file
CREDENTIALS_FILE_PATH = "/home/username/.credentials.txt"

# Public key of the revoked identity account
PUBKEY = "XXXXXXXX"

# WARNING : Hide this file in a safe and secure place
# If one day you forget your credentials,
# you'll have to use your private key instead
REVOKE_DOCUMENT_FILE_PATH = "/home/username/duniter_account_revoke_document.txt"

################################################

# Latest duniter-python-api is asynchronous and you have to create an aiohttp session to send request
# ( http://pythonhosted.org/aiohttp )
AIOHTTP_SESSION = aiohttp.ClientSession()

# Current protocole version
PROTOCOL_VERSION = 2

async def get_current_block():
    """
    Get the current block data

    :rtype: dict
    """
    # Here we request for the path blockchain/current
    return await bma.blockchain.Current(BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler()) \
        .get(AIOHTTP_SESSION)

async def get_self_certification_document(currency, pubkey):
    """
    Get the SelfCertification document of the pubkey

    :param str currency: Currency name
    :param str pubkey: Public key

    :rtype: SelfCertification
    """
    # Here we request for the path wot/lookup/pubkey
    lookup_data = await bma.wot.Lookup(BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler(), pubkey)\
        .get(AIOHTTP_SESSION)

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
                version=PROTOCOL_VERSION,
                currency=currency,
                pubkey=pubkey,
                uid=uid,
                ts=timestamp,
                signature=signature
            )


async def get_revoke_document(self_certification, salt, password):
    """
    Generate account revokation document for given identity

    :param SelfCertification self_certification: Self Certification of the identity
    :param str salt: Salt
    :param str password: Password

    :return: the revokation document
    :rtype: duniterpy.documents.certification.Revocation
    """
    document = Revocation(PROTOCOL_VERSION, self_certification.currency, self_certification.pubkey, "")

    key = SigningKey(salt, password)
    document.sign(self_certification, [key])
    return document.signed_raw(self_certification)

async def main():
    """
    Main code
    """
    # capture current block to get currency name
    current_block = await get_current_block()

    # create our SelfCertification document to sign the revoke document
    self_cert_document = await get_self_certification_document(current_block['currency'], PUBKEY)

    # load credentials from a text file
    salt, password = open(CREDENTIALS_FILE_PATH).readlines()

    # get the revoke document
    revoke_document = await get_revoke_document(self_cert_document, salt, password)

    # save revoke document in a file
    fp = open(REVOKE_DOCUMENT_FILE_PATH, 'w')
    fp.write(revoke_document)
    fp.close()

    # document saved
    print("Revoke document saved in %s" % REVOKE_DOCUMENT_FILE_PATH)

with AIOHTTP_SESSION:

    # Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
    # ( https://docs.python.org/3/library/asyncio.html )
    asyncio.get_event_loop().run_until_complete(main())
