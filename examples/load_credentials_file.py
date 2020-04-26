import sys

from duniterpy.key import SigningKey

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_credentials_file.py FILEPATH")
        sys.exit(1)

    # capture filepath argument
    credentials_filepath = sys.argv[1]

    # create SigningKey instance from file
    signing_key_instance = SigningKey.from_credentials_file(
        credentials_filepath
    )  # type: SigningKey

    # print pubkey
    print("Public key from credentials file: {}".format(signing_key_instance.pubkey))
