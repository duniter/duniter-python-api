import getpass
import sys

from duniterpy.key import SigningKey

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("""
        Usage:
            python decrypt_message.py ENCRYPTED_MESSAGE_FILEPATH
        """)

    # capture encrypted message filepath argument
    signed_message_path = sys.argv[1]

    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password: ")

    # Create key object
    signing_key_instance = SigningKey.from_credentials(salt, password)

    # open encrypted message file
    with open(signed_message_path, 'rb') as file_handler:
        encrypted_message = file_handler.read()

    # Decrypt the message!
    try:
        message = signing_key_instance.decrypt_seal(encrypted_message)
        print("Decrypted message:")
    except ValueError as error:
        message = str(error)

    print(message)
