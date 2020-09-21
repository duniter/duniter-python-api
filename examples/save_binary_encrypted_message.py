"""
Copyright  2014-2020 Vincent Texier <vit@free.fr>

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

from duniterpy.key import PublicKey

# CONFIG #######################################

ENCRYPTED_MESSAGE_FILENAME = "/tmp/duniter_encrypted_message.bin"

################################################

if __name__ == "__main__":
    # Ask public key of the recipient
    pubkeyBase58 = input("Enter public key of the message recipient: ")

    # Enter the message
    message = input("Enter your message: ")

    # Encrypt the message, only the recipient secret key will be able to decrypt the message
    pubkey_instance = PublicKey(pubkeyBase58)
    encrypted_message = pubkey_instance.encrypt_seal(message)

    # Save encrypted message in a file
    with open(ENCRYPTED_MESSAGE_FILENAME, "wb") as file_handler:
        file_handler.write(encrypted_message)

    print("Encrypted message saved in file ./{0}".format(ENCRYPTED_MESSAGE_FILENAME))
