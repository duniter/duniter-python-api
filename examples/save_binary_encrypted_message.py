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
