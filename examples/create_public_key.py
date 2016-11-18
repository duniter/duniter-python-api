import getpass
from duniterpy.key import SigningKey

################################################

if __name__ == '__main__':

    # prompt hidden user entry
    salt = getpass.getpass("Enter your passphrase (salt): ")

    # prompt hidden user entry
    password = getpass.getpass("Enter your password: ")

    # Create key object
    key = SigningKey(salt, password)

    # Display your public key
    print("Public key for your credentials: %s" % key.pubkey)


