import asyncio
import aiohttp
import duniterpy.api.bma as bma
from duniterpy.documents import BMAEndpoint, BlockUID, Identity
from duniterpy.documents import Revocation
from duniterpy.key import SigningKey
import getpass
import os

if "XDG_CONFIG_HOME" in os.environ:
    home_path = os.environ["XDG_CONFIG_HOME"]
elif "HOME" in os.environ:
    home_path = os.environ["HOME"]
elif "APPDATA" in os.environ:
    home_path = os.environ["APPDATA"]
else:
    home_path = os.path.dirname(__file__)

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the BASIC_MERKLED_API
BMA_ENDPOINT = "BASIC_MERKLED_API g1.duniter.org 10901"

# WARNING : Hide this file in a safe and secure place
# If one day you forget your credentials,
# you'll have to use your private key instead
REVOKE_DOCUMENT_FILE_PATH = os.path.join(home_path, "duniter_account_revoke_document.txt")

################################################
AIOHTTP_SESSION = aiohttp.ClientSession()

# Current protocol version
PROTOCOL_VERSION = 10

async def get_identity_document(connection, currency, pubkey):
    """
    Get the Identity document of the pubkey

    :param bma.api.ConnectionHandler connection: Connection handler
    :param str currency: Currency name
    :param str pubkey: Public key

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
                version=PROTOCOL_VERSION,
                currency=currency,
                pubkey=pubkey,
                uid=uid,
                ts=timestamp,
                signature=signature
            )


def get_revoke_document(identity, salt, password):
    """
    Generate account revocation document for given identity

    :param Identity identity: Self Certification of the identity
    :param str salt: Salt
    :param str password: Password

    :return: the revokation document
    :rtype: duniterpy.documents.certification.Revocation
    """
    document = Revocation(PROTOCOL_VERSION, identity.currency, identity.pubkey, "")

    key = SigningKey(salt, password)
    document.sign(identity, [key])
    return document.signed_raw(identity)

async def main():
    """
    Main code
    """
    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password: ")

    # prompt public key
    pubkey = input("Enter your public key: ")

    # init signer instance
    signer = SigningKey(salt, password)

    # check public key
    if signer.pubkey != pubkey:
        print("Bad credentials !")
        exit(0)

    # connection handler from BMA endpoint
    connection = next(BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler(AIOHTTP_SESSION))
    # capture current block to get currency name
    current_block = await bma.blockchain.current(connection)

    # create our Identity document to sign the revoke document
    identity_document = await get_identity_document(connection, current_block['currency'], pubkey)

    # get the revoke document
    revoke_document = get_revoke_document(identity_document, salt, password)

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
