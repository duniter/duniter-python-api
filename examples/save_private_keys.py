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
PRIVATE_KEYS_FILE_PATH = os.path.join(home_path, ".duniter_account_private_keys.txt")

################################################

# prompt hidden user entry
salt = getpass.getpass("Enter your passphrase (salt): ")

# prompt hidden user entry
password = getpass.getpass("Enter your password: ")

# prompt public key
pubkey = input("Enter your public key: ")

# init signer instance
signer = SigningKey(salt, password)

# check public key
if signer.pubkey != pubkey:
    print("Bad credentials!")
    exit(1)

# save private keys in a file (json format)
signer.save(PRIVATE_KEYS_FILE_PATH)

# document saved
print("Private keys for public key %s saved in %s" % (pubkey, PRIVATE_KEYS_FILE_PATH))
