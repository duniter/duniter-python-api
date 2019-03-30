import sys

from duniterpy.key import VerifyingKey

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("""
        Usage:
            python verify_signed_message.py SIGNED_MESSAGE_FILEPATH
        """)

    # capture signed message filepath argument
    signed_message_path = sys.argv[1]

    # ask public key of the signer
    pubkeyBase58 = input("Enter public key of the message issuer: ")

    # open signed message file
    with open(signed_message_path, 'rb') as file_handler:
        signed_message = file_handler.read()

    # Verify the message!
    verifier = VerifyingKey(pubkeyBase58)
    try:
        message = verifier.get_verified_data(signed_message).decode('utf-8')
        print("Signature valid for this message:")
    except ValueError as error:
        message = str(error)

    print(message)
