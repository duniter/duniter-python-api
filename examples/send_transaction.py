import asyncio
import getpass
import aiohttp

from duniterpy.api import bma
from duniterpy.documents import BMAEndpoint, BlockUID, Transaction
from duniterpy.documents.transaction import InputSource, OutputSource, Unlock, SIGParameter
from duniterpy.grammars.output import Condition, SIG
from duniterpy.key import SigningKey

# CONFIG #######################################

# You can either use a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
# or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
# Here we use the BASIC_MERKLED_API
BMA_ENDPOINT = "BASIC_MERKLED_API g1.duniter.org 10901"


################################################


# Latest duniter-python-api is asynchronous and you have to create an aiohttp session to send request
# ( http://pythonhosted.org/aiohttp )
AIOHTTP_SESSION = aiohttp.ClientSession()

# Version of the transaction document
TRANSACTION_VERSION = 3


def get_transaction_document(current_block, source, from_pubkey, to_pubkey):
    """
    Return a Transaction document

    :param dict current_block: Current block infos
    :param dict source: Source to send
    :param str from_pubkey: Public key of the issuer
    :param str to_pubkey: Public key of the receiver

    :return: Transaction
    """
    # list of inputs (sources)
    inputs = [
        InputSource(
            amount=source['amount'],
            base=source['base'],
            source=source['type'],
            origin_id=source['identifier'],
            index=source['noffset']
        )
    ]

    # list of issuers of the inputs
    issuers = [
        from_pubkey
    ]

    # list of unlocks of the inputs
    unlocks = [
        Unlock(
            # inputs[index]
            index=0,
            # unlock inputs[index] if signatures[0] is from public key of issuers[0]
            parameters=[SIGParameter(0)]
        )
    ]

    # lists of outputs
    outputs = [
        OutputSource(
            amount=source['amount'],
            base=source['base'],
            # only the receiver of the output can use it as input in another transaction
            conditions=Condition.token(SIG.token(to_pubkey))
        )
    ]

    transaction = Transaction(
        version=TRANSACTION_VERSION,
        currency=current_block['currency'],
        blockstamp=BlockUID(current_block['number'], current_block['hash']),
        locktime=0,
        issuers=issuers,
        inputs=inputs,
        unlocks=unlocks,
        outputs=outputs,
        comment='',
        signatures=None
    )

    return transaction

async def main():
    """
    Main code
    """
    # connection handler from BMA endpoint
    connection = next(BMAEndpoint.from_inline(BMA_ENDPOINT).conn_handler(AIOHTTP_SESSION))

    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password : ")

    # prompt hidden user entry
    pubkey_from = getpass.getpass("Enter your pubkey : ")

    # prompt hidden user entry
    pubkey_to = getpass.getpass("Enter recipient pubkey : ")

    # capture current block to get version and currency and blockstamp
    current_block = await bma.blockchain.current(connection)

    # capture sources of account
    response = await bma.tx.sources(connection, pubkey_from)

    if len(response['sources']) == 0:
        print("no sources found for account %s" % pubkey_to)
        exit(1)

    # get the first source
    source = response['sources'][0]

    # create the transaction document
    transaction = get_transaction_document(current_block, source, pubkey_from, pubkey_to)

    # create keys from credentials
    key = SigningKey(salt, password)

    # sign document
    transaction.sign([key])

    # send the Transaction document to the node
    response = await bma.tx.process(connection, transaction.signed_raw())

    if response.status == 200:
        print(await response.text())
    else:
        print("Error while publishing transaction : {0}".format(await response.text()))
    response.close()


with AIOHTTP_SESSION:

    # Latest duniter-python-api is asynchronous and you have to use asyncio, an asyncio loop and a "as" on the data.
    # ( https://docs.python.org/3/library/asyncio.html )
    asyncio.get_event_loop().run_until_complete(main())
