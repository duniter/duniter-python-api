import sys

from duniterpy.key import SigningKey

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(
            """
        Usage:
            python load_scuttlebutt_file.py FILEPATH
        """
        )

    # capture filepath argument
    scuttlebutt_filepath = sys.argv[1]

    # create SigningKey instance from file
    signing_key_instance = SigningKey.from_ssb_file(
        scuttlebutt_filepath
    )  # type: SigningKey

    # print pubkey
    print("Public key from scuttlebutt file: {}".format(signing_key_instance.pubkey))
