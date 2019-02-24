import getpass
from duniterpy import __version__

from duniterpy.key import AsciiArmor, SigningKey

################################################

AA_ENCRYPTED_MESSAGE_FILENAME = 'duniter_aa_encrypted_message.txt'

if __name__ == '__main__':
    # Ask public key of the recipient
    pubkeyBase58 = input("Enter public key of the message issuer: ")

    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password: ")

    # init SigningKey instance
    signing_key = SigningKey.from_credentials(salt, password)

    # Load ascii armor encrypted message from a file
    with open(AA_ENCRYPTED_MESSAGE_FILENAME, 'r') as file_handler:
        ascii_armor_block = file_handler.read()

    print("Ascii Armor Encrypted message loaded from file ./{0}".format(AA_ENCRYPTED_MESSAGE_FILENAME))

    print(AsciiArmor.parse(ascii_armor_block, signing_key, [pubkeyBase58]))
