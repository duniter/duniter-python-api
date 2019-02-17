import base64
import libnacl
from typing import Optional, List

from duniterpy.key import SigningKey, PublicKey, SCRYPT_PARAMS, SEED_LENGTH

# Headers constants
BEGIN_MESSAGE_HEADER = "-----BEGIN DUNITER MESSAGE-----"
END_MESSAGE_HEADER = "-----END DUNITER MESSAGE-----"
BEGIN_SIGNATURE_HEADER = "-----BEGIN DUNITER SIGNATURE-----"
END_SIGNATURE_HEADER = "-----END DUNITER SIGNATURE-----"

# Version field values
AA_MESSAGE_VERSION = "Python Libnacl " + libnacl.__version__
AA_SIGNATURE_VERSION = "Python Libnacl " + libnacl.__version__


class AsciiArmor:
    """
    Class to handle writing and reading of ascii armor messages
    """

    @staticmethod
    def encrypt(message: str, pubkey: str, signing_keys: Optional[List[SigningKey]] = None,
                message_comment: Optional[str] = None, signatures_comment: Optional[str] = None) -> str:
        """
        Encrypt a message in ascii armor format, optionally signing it

        :param message: Utf-8 message
        :param pubkey: Public key of recipient for encryption
        :param signing_keys: Optional list of SigningKey instances
        :param message_comment: Optional message comment field
        :param signatures_comment: Optional signatures comment field
        :return:
        """
        pubkey_instance = PublicKey(pubkey)
        base64_encrypted_message = base64.b64encode(pubkey_instance.encrypt_seal(message))  # type: bytes
        script_field = AsciiArmor._get_scrypt_field()

        # create block with headers
        ascii_armor_msg = """
{begin_message_header}
Version: {version}
{script_field}
""".format(begin_message_header=BEGIN_MESSAGE_HEADER, version=AA_MESSAGE_VERSION,
           script_field=script_field)

        # add message comment if specified
        if message_comment:
            ascii_armor_msg += AsciiArmor._get_comment_field(message_comment)

        # add encrypted message
        ascii_armor_msg += """
{base64_encrypted_message}
""".format(base64_encrypted_message=base64_encrypted_message.decode('utf-8'))

        # if no signature...
        if signing_keys is None:
            # add message tail
            ascii_armor_msg += END_MESSAGE_HEADER
        else:
            # add signature blocks and close block on last signature
            count = 1
            for signing_key in signing_keys:
                ascii_armor_msg += AsciiArmor._get_signature_block(message, signing_key, count == len(signing_keys),
                                                                   signatures_comment)
                count += 1

        return ascii_armor_msg

    @staticmethod
    def _get_scrypt_field():
        """
        Return the Scrypt field

        :return:
        """
        return "Scrypt: N={0};r={1};p={2};len={3}".format(SCRYPT_PARAMS['N'], SCRYPT_PARAMS['r'], SCRYPT_PARAMS['p'],
                                                          SEED_LENGTH)

    @staticmethod
    def _get_comment_field(comment: str) -> str:
        """
        Return a comment field

        :param comment: Comment text
        :return:
        """
        return "Comment: {comment}\n".format(comment=comment)

    @staticmethod
    def _get_signature_block(message: str, signing_key: SigningKey, close_block: bool = True,
                             comment: Optional[str] = None) -> str:
        """
        Return a signature block

        :param message: Message (not encrypted!) to sign
        :param signing_key: The libnacl SigningKey instance of the keypair
        :param close_block: Optional flag to close the signature block with the signature tail header
        :param comment: Optional comment field content
        :return:
        """
        script_param_field = AsciiArmor._get_scrypt_field()
        base64_signature = base64.b64encode(signing_key.signature(message))

        block = """{begin_signature_header}
Version: {version}
Scrypt: {script_params}
""".format(begin_signature_header=BEGIN_SIGNATURE_HEADER, version=AA_SIGNATURE_VERSION,
            script_params=script_param_field)

        # add message comment if specified
        if comment:
            block += AsciiArmor._get_comment_field(comment)

        block += """
{base64_signature}
""".format(base64_signature=base64_signature.decode('utf-8'))

        if close_block:
            block += END_SIGNATURE_HEADER

        return block
