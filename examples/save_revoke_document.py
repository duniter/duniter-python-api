"""
Copyright  2014-2021 Vincent Texier <vit@free.fr>

DuniterPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DuniterPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import asyncio
import getpass
import os
import sys
from typing import Optional

from duniterpy.api import bma
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

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT] [PATH]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT] [PATH]
# Here we use the secure BASIC_MERKLED_API (BMAS)
BMAS_ENDPOINT = "BMAS g1-test.duniter.org 443"

# WARNING : Hide this file in a safe and secure place
# If one day you forget your credentials,
# you'll have to use your private key instead
REVOCATION_DOCUMENT_FILE_PATH = os.path.join(
    home_path, "duniter_account_revocation_document.txt"
)

# Current protocol version
PROTOCOL_VERSION = 10


################################################


async def get_identity_document(
    client: Client, current_block: dict, pubkey: str
) -> Optional[Identity]:
    """
    Get the identity document of the pubkey

    :param client: Client to connect to the api
    :param current_block: Current block data
    :param pubkey: UID/Public key

    :rtype: Identity
    """
    # Here we request for the path wot/lookup/pubkey
    lookup_data = await client(bma.wot.lookup, pubkey)
    identity = None

    # parse results
    for result in lookup_data["results"]:
        if result["pubkey"] == pubkey:
            uids = result["uids"]
            uid_data = uids[0]
            # capture data
            timestamp = BlockUID.from_str(uid_data["meta"]["timestamp"])
            uid = uid_data["uid"]  # type: str
            signature = uid_data["self"]  # type: str

            # return self-certification document
            identity = Identity(
                version=10,
                currency=current_block["currency"],
                pubkey=pubkey,
                uid=uid,
                ts=timestamp,
                signature=signature,
            )
            break

    return identity


def get_signed_raw_revocation_document(
    identity: Identity, salt: str, password: str
) -> str:
    """
    Generate account revocation document for given identity

    :param identity: Self Certification of the identity
    :param salt: Salt
    :param password: Password

    :rtype: str
    """
    revocation = Revocation(PROTOCOL_VERSION, identity.currency, identity, "")

    key = SigningKey.from_credentials(salt, password)
    revocation.sign([key])
    return revocation.signed_raw()


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
    signer = SigningKey.from_credentials(salt, password)

    # check public key
    if signer.pubkey != pubkey:
        print("Bad credentials!")
        sys.exit(0)

    # capture current block to get currency name
    current_block = await client(bma.blockchain.current)

    # create our Identity document to sign the Certification document
    identity = await get_identity_document(client, current_block, pubkey)
    if identity is None:
        print("Identity not found for pubkey {0}".format(pubkey))
        # Close client aiohttp session
        await client.close()
        sys.exit(1)

    # get the revoke document
    revocation_signed_raw_document = get_signed_raw_revocation_document(
        identity, salt, password
    )

    # save revoke document in a file
    fp = open(REVOCATION_DOCUMENT_FILE_PATH, "w")
    fp.write(revocation_signed_raw_document)
    fp.close()

    # document saved
    print("Revocation document saved in %s" % REVOCATION_DOCUMENT_FILE_PATH)

    # Close client aiohttp session
    await client.close()


# Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
# ( https://docs.python.org/3/library/asyncio.html )
asyncio.get_event_loop().run_until_complete(main())
