import getpass
from duniterpy.key import SigningKey
import libnacl.sign

################################################

SIGNED_MESSAGE_FILENAME = 'duniter_signed_message.bin'

if __name__ == '__main__':

    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password: ")

    # Create key object
    key = SigningKey(salt, password)

    # Display your public key
    print("Public key for your credentials: %s" % key.pubkey)

    message = input("Enter your message: ")

    # Sign the message, the signed string is the message itself plus the
    # signature
    signed_message = key.sign(bytes(message, 'utf-8'))  # type: bytes

    # To create a verifier pass in the verify key:
    veri = libnacl.sign.Verifier(key.hex_vk())
    # Verify the message!
    verified = veri.verify(signed_message)

    # save signed message in a file
    with open(SIGNED_MESSAGE_FILENAME, 'wb') as file_handler:
        file_handler.write(signed_message)

    print("Signed message saved in file ./{0}".format(SIGNED_MESSAGE_FILENAME))
