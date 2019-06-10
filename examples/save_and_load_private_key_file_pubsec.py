from duniterpy.key import SigningKey
import getpass
import os

if "XDG_CONFIG_HOME" in os.environ:
    home_path = os.environ["XDG_CONFIG_HOME"]
elif "HOME" in os.environ:
    home_path = os.environ["HOME"]
elif "APPDATA" in os.environ:
    home_path = os.environ["APPDATA"]
else:
    home_path = os.path.dirname(__file__)

# CONFIG #######################################

# WARNING : Hide this file in a safe and secure place
# If one day you forget your credentials,
# you'll have to use one of your private keys instead
PRIVATE_KEY_FILE_PATH = os.path.join(home_path, ".duniter_account_pubsec_v1.duniterkey")

################################################

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
    exit(1)

# save private key in a file (PubSec v1 format)
signer.save_pubsec_file(PRIVATE_KEY_FILE_PATH)

# document saved
print(
    "Private key for public key %s saved in %s" % (signer.pubkey, PRIVATE_KEY_FILE_PATH)
)

try:
    # load private keys from file
    loaded_signer = SigningKey.from_pubsec_file(PRIVATE_KEY_FILE_PATH)

    # check public key from file
    print(
        "Public key %s loaded from file %s"
        % (loaded_signer.pubkey, PRIVATE_KEY_FILE_PATH)
    )

except IOError as error:
    print(error)
    exit(1)


exit(0)
