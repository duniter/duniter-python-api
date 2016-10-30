from duniterpy.key import SigningKey

# CONFIG #######################################

# CREDENTIALS in Duniter are a couple of strings:
# - A secret pass-phrase
# - A password
# They create a seed which create keys (some are private and one is public)

# Credentials should be prompted or kept in a separate secure file
# create a file with the salt on the first line and the password on the second line
# the script will load them from the file
CREDENTIALS_FILE_PATH = "/home/username/.credentials.txt"

################################################

if __name__ == '__main__':

    # Load your credentials from a text file
    salt, password = open(CREDENTIALS_FILE_PATH).readlines()
    # Cleanup newlines
    salt, password = salt.strip(), password.strip()

    # Create key object
    key = SigningKey(salt, password)

    # Display your public key
    print("Public key for your credentials: %s" % key.pubkey)


