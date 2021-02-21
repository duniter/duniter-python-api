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

from duniterpy.key import SigningKey
import getpass
import os
import sys

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
signer = SigningKey.from_credentials(salt, password)

# check public key
if signer.pubkey != pubkey:
    print("Bad credentials!")
    sys.exit(1)

# save private keys in a file (json format)
signer.save_private_key(PRIVATE_KEYS_FILE_PATH)

# document saved
print("Private keys for public key %s saved in %s" % (pubkey, PRIVATE_KEYS_FILE_PATH))

# load private keys from file
loaded_signer = SigningKey.from_private_key(PRIVATE_KEYS_FILE_PATH)  # type: SigningKey

# check public key from file
print("Public key %s loaded from file %s" % (pubkey, PRIVATE_KEYS_FILE_PATH))

sys.exit(0)
