import asyncio
import getpass
import os

import duniterpy.api.bma as bma
from duniterpy.api.client import Client
from duniterpy.documents import Revocation, BlockUID, Identity
from duniterpy.key import SigningKey

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
# Here we use the secure BASIC_MERKLED_API (BMAS)
BMAS_ENDPOINT = "BMAS g1-test.duniter.org 443"

# WARNING : Hide this file in a safe and secure place
# If one day you forget your credentials,
# you'll have to use your private key instead
REVOCATION_DOCUMENT_FILE_PATH = os.path.join(home_path, "duniter_account_revocation_document.txt")

# Current protocol version
PROTOCOL_VERSION = 10


################################################


async def get_identity_document(client: Client, currency: str, pubkey: str) -> Identity:
    """
    Get the Identity document of the pubkey

    :param client: Client to connect to the api
    :param currency: Currency name
    :param pubkey: Public key

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
                version=PROTOCOL_VERSION,
                currency=currency,
                pubkey=pubkey,
                uid=uid,
                ts=timestamp,
                signature=signature
            )


def get_signed_raw_revocation_document(identity: Identity, salt: str, password: str) -> str:
    """
    Generate account revocation document for given identity

    :param identity: Self Certification of the identity
    :param salt: Salt
    :param password: Password

    :rtype: str
    """
    revocation = Revocation(PROTOCOL_VERSION, identity.currency, identity.pubkey, "")

    key = SigningKey(salt, password)
    revocation.sign_for_revoked(identity, [key])
    return revocation.signed_raw_for_revoked(identity)


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

    # prompt public key
    pubkey = input("Enter your public key: ")

    # init signer instance
    signer = SigningKey(salt, password)

    # check public key
    if signer.pubkey != pubkey:
        print("Bad credentials!")
        exit(0)

    # capture current block to get currency name
    current_block = await client(bma.blockchain.current)

    # create our Identity document to sign the revoke document
    identity_document = await get_identity_document(client, current_block['currency'], pubkey)

    # get the revoke document
    revocation_signed_raw_document = get_signed_raw_revocation_document(identity_document, salt, password)

    # save revoke document in a file
    fp = open(REVOCATION_DOCUMENT_FILE_PATH, 'w')
    fp.write(revocation_signed_raw_document)
    fp.close()

    # document saved
    print("Revocation document saved in %s" % REVOCATION_DOCUMENT_FILE_PATH)

    # Close client aiohttp session
    await client.close()


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
