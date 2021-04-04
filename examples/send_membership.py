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

import getpass

from duniterpy.api import bma
from duniterpy.api.client import Client
from duniterpy.documents import BlockUID, Membership
from duniterpy.key import SigningKey

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT] [PATH]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT] [PATH]
# Here we use the secure BASIC_MERKLED_API (BMAS)
BMAS_ENDPOINT = "BMAS g1-test.duniter.org 443"


################################################


def get_membership_document(
    membership_type: str,
    current_block: dict,
    identity: dict,
    key: SigningKey,
) -> Membership:
    """
    Get a Membership document

    :param membership_type: "IN" to ask for membership or "OUT" to cancel membership
    :param current_block: Current block data
    :param identity: identity card from /wot/lookup
    :param key: cryptographic key to sign documents

    :rtype: Membership
    """

    # get current block BlockStamp
    timestamp = BlockUID(current_block["number"], current_block["hash"])

    # get the uid and the timestamp of the corresponding identity
    uid = identity["uids"][0]["uid"]
    identity_timestamp = identity["uids"][0]["meta"]["timestamp"]

    # create membership document
    membership = Membership(
        version=10,
        currency=current_block["currency"],
        issuer=key.pubkey,
        membership_ts=timestamp,
        membership_type=membership_type,
        uid=uid,
        identity_ts=identity_timestamp,
    )

    # sign document
    membership.sign([key])

    return membership


def main():
    """
    Main code
    """
    # Create Client from endpoint string in Duniter format
    client = Client(BMAS_ENDPOINT)

    # Get the node summary infos by dedicated method (with json schema validation)
    response = client(bma.node.summary)
    print(response)

    # capture current block to get version and currency and blockstamp
    current_block = client(bma.blockchain.current)

    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password: ")

    # create key from credentials
    key = SigningKey.from_credentials(salt, password)

    # Look for identities on the network, take the first result since the
    # lookup was done with a pubkey, which should correspond to the first identity
    identities = client(bma.wot.lookup, key.pubkey)
    identity = identities["results"][0]

    # create a membership demand document
    membership = get_membership_document("IN", current_block, identity, key)

    # send the membership signed raw document to the node
    response = client(bma.blockchain.membership, membership.signed_raw())

    if response.status == 200:
        print(response.text())
    else:
        print("Error while publishing membership : {0}".format(response.text()))


if __name__ == "__main__":
    main()
