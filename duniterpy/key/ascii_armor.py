import base64
import libnacl
from re import compile
from typing import Optional, List, Dict, Any

from duniterpy.key import SigningKey, PublicKey, VerifyingKey
from duniterpy.key.scrypt_params import ScryptParams

# Headers constants
BEGIN_MESSAGE_HEADER = "-----BEGIN DUNITER MESSAGE-----"
END_MESSAGE_HEADER = "-----END DUNITER MESSAGE-----"
BEGIN_SIGNATURE_HEADER = "-----BEGIN DUNITER SIGNATURE-----"
END_SIGNATURE_HEADER = "-----END DUNITER SIGNATURE-----"
HEADER_PREFIX = "-----"

# Version field value
VERSION_FIELD_VALUE = "Python Libnacl " + libnacl.__version__

# Parser cursor status
ON_MESSAGE_FIELDS = 1
ON_MESSAGE_CONTENT = 2
ON_SIGNATURE_FIELDS = 3
ON_SIGNATURE_CONTENT = 4


# Custom exceptions
class MissingPublickeyAndSigningKeyException(Exception):
    """
    Raise when the message created is not encrypted and not signed...
    """
    pass


# Custom exceptions
class ParserMissingSigningKeyException(Exception):
    """
    Raise when the message is encrypted but no SigningKey instance is provided
    """
    pass


# Custom exceptions
class ParserMissingPublicKeysException(Exception):
    """
    Raise when there is at least one signature but no public keys are provided
    """
    pass


# Exception messages listed here
PARSER_MISSING_SIGNING_KEY_EXCEPTION = ParserMissingSigningKeyException('The message is encrypted but no SigningKey '
                                                                        'instance is provided')
PARSER_MISSING_PUBLIC_KEYS_EXCEPTION = ParserMissingPublicKeysException('At least one signature but no public keys '
                                                                        'are provided')

MISSING_PUBLIC_KEY_AND_SIGNING_KEY_EXCEPTION = MissingPublickeyAndSigningKeyException('Ascii Armor Message needs a '
                                                                                      'public key or a SigningKey but '
                                                                                      'none are provided')


class AsciiArmor:
    """
    Class to handle writing and parsing of ascii armor messages
    """
    @staticmethod
    def create(message: str, pubkey: Optional[str] = None, signing_keys: Optional[List[SigningKey]] = None,
               message_comment: Optional[str] = None, signatures_comment: Optional[str] = None,
               scrypt_params: Optional[ScryptParams] = None) -> str:
        """
        Encrypt a message in ascii armor format, optionally signing it

        :param message: Utf-8 message
        :param pubkey: Public key of recipient for encryption
        :param signing_keys: Optional list of SigningKey instances
        :param message_comment: Optional message comment field
        :param signatures_comment: Optional signatures comment field
        :param scrypt_params: Optional ScryptParams instance

        :return:
        """
        # if no public key and no signing key...
        if not pubkey and not signing_keys:
            # We can not create an Ascii Armor Message
            raise MISSING_PUBLIC_KEY_AND_SIGNING_KEY_EXCEPTION

        if scrypt_params is None:
            scrypt_params = ScryptParams()

        # TODO: improve cleaning of spaces and tab at end of lines
        # remove last newline of the message if any
        message = message.strip("\n\r")

        # create block with headers
        ascii_armor_block = """
{begin_message_header}
""".format(begin_message_header=BEGIN_MESSAGE_HEADER)

        # if encrypted message...
        if pubkey:
            # add encrypted message fields
            ascii_armor_block += """{version_field}
{script_field}
""".format(version_field=AsciiArmor._get_version_field(), script_field=AsciiArmor._get_scrypt_field(scrypt_params))

        # add message comment if specified
        if message_comment:
            ascii_armor_block += """{comment_field}
""".format(comment_field=AsciiArmor._get_comment_field(message_comment))

        # blank line separator
        ascii_armor_block += '\n'

        if pubkey:
            # add encrypted message
            pubkey_instance = PublicKey(pubkey)
            base64_encrypted_message = base64.b64encode(pubkey_instance.encrypt_seal(message))  # type: bytes
            ascii_armor_block += """{base64_encrypted_message}
""".format(base64_encrypted_message=base64_encrypted_message.decode('utf-8'))
        else:
            # TODO: Dash escape cleartext
            # clear text message
            ascii_armor_block += message + "\n"

        # if no signature...
        if signing_keys is None:
            # add message tail
            ascii_armor_block += END_MESSAGE_HEADER
        else:
            # add signature blocks and close block on last signature
            count = 1
            for signing_key in signing_keys:
                ascii_armor_block += AsciiArmor._get_signature_block(message, signing_key, count == len(signing_keys),
                                                                     signatures_comment, scrypt_params)
                count += 1

        return ascii_armor_block

    @staticmethod
    def _get_version_field() -> str:
        """
        Return the Version field

        :return:
        """
        return "Version: {version}".format(version=VERSION_FIELD_VALUE)

    @staticmethod
    def _get_scrypt_field(scrypt_params: Optional[ScryptParams] = None) -> str:
        """
        Return the Scrypt field

        :param scrypt_params: Optional ScryptParams instance
        :return:
        """
        if scrypt_params is None:
            scrypt_params = ScryptParams()

        return "Scrypt: N={0};r={1};p={2};len={3}".format(scrypt_params.N, scrypt_params.r, scrypt_params.p,
                                                          scrypt_params.seed_length)

    @staticmethod
    def _get_comment_field(comment: str) -> str:
        """
        Return a comment field

        :param comment: Comment text
        :return:
        """
        return "Comment: {comment}".format(comment=comment)

    @staticmethod
    def _get_signature_block(message: str, signing_key: SigningKey, close_block: bool = True,
                             comment: Optional[str] = None,
                             scrypt_params: Optional[ScryptParams] = None) -> str:
        """
        Return a signature block

        :param message: Message (not encrypted!) to sign
        :param signing_key: The libnacl SigningKey instance of the keypair
        :param close_block: Optional flag to close the signature block with the signature tail header
        :param comment: Optional comment field content
        :param scrypt_params: Optional ScriptParams instance

        :return:
        """
        if scrypt_params is None:
            scrypt_params = ScryptParams()

        base64_signature = base64.b64encode(signing_key.signature(message))

        block = """{begin_signature_header}
{version_field}
{script_field}
""".format(begin_signature_header=BEGIN_SIGNATURE_HEADER, version_field=AsciiArmor._get_version_field(),
           script_field=AsciiArmor._get_scrypt_field(scrypt_params))

        # add message comment if specified
        if comment:
            block += """{comment_field}
""".format(comment_field=AsciiArmor._get_comment_field(comment))

        # blank line separator
        block += '\n'

        block += """{base64_signature}
""".format(base64_signature=base64_signature.decode('utf-8'))

        if close_block:
            block += END_SIGNATURE_HEADER

        return block

    # TODO: add parse from credentials to use scrypt field creating SigningKey

    @staticmethod
    def parse(ascii_armor_block: str, signing_key: Optional[SigningKey] = None,
              sender_pubkeys: Optional[List[str]] = None) -> dict:
        """
        Return a dict with parsed content (decrypted message, signature validation)

        {
            'message':
                {
                    'fields': {},
                    'content': str,
                 },
            'signatures': [
                {'pubkey': str, 'valid': bool, fields: {}}
            ]
        }

        :param ascii_armor_block: The Ascii Armor Message Block including BEGIN and END headers
        :param signing_key: Optional Libnacl SigningKey instance to decrypt message
        :param sender_pubkeys: Optional sender's public keys list to verify signatures
        :exception libnacl.CryptError: Raise an exception if keypair fail to decrypt the message
        :exception MissingSigningKeyException: Raise an exception if no keypair given for encrypted message

        :return:
        """
        regex_begin_message = compile(BEGIN_MESSAGE_HEADER)
        regex_end_message = compile(END_MESSAGE_HEADER)
        regex_begin_signature = compile(BEGIN_SIGNATURE_HEADER)
        regex_end_signature = compile(END_SIGNATURE_HEADER)
        regex_fields = compile("^(Version|Scrypt|Comment): (.+)$")

        # trim message to get rid of empty lines
        ascii_armor_block.strip(" \t\n\r")
        parsed_result = {
            'message':
                {
                    'fields': {},
                    'content': '',
                 },
            'signatures': []
        }  # type: Dict[str, Any]
        cursor_status = 0
        message = ''
        signatures_index = 0
        for line in ascii_armor_block.splitlines():

            # if begin message header detected...
            if regex_begin_message.match(line):
                cursor_status = ON_MESSAGE_FIELDS
                continue

            # if we are on the fields lines...
            if cursor_status == ON_MESSAGE_FIELDS:
                # parse field
                m = regex_fields.match(line.strip())
                if m:
                    # capture field
                    msg_field_name = m.groups()[0]
                    msg_field_value = m.groups()[1]
                    parsed_result['message']['fields'][msg_field_name] = msg_field_value
                    continue

                # if blank line...
                if line.strip("\n\t\r ") == '':
                    cursor_status = ON_MESSAGE_CONTENT
                    continue

            # if we are on the message content lines...
            if cursor_status == ON_MESSAGE_CONTENT:

                # if a header is detected...
                if line.startswith(HEADER_PREFIX):

                    # if field Version is present...
                    if 'Version' in parsed_result['message']['fields']:
                        # If keypair instance not given...
                        if signing_key is None:
                            # SigningKey keypair is mandatory to decrypt the message...
                            raise PARSER_MISSING_SIGNING_KEY_EXCEPTION

                        # decrypt message with secret key from keypair
                        message = AsciiArmor._decrypt(message, signing_key)

                    # save message content in result
                    parsed_result['message']['content'] = message

                    # if message end header...
                    if regex_end_message.match(line):
                        # stop parsing
                        break

                    # if signature begin header...
                    if regex_begin_signature.match(line):
                        # add signature dict in list
                        parsed_result['signatures'].append({
                            'fields': {}
                        })
                        cursor_status = ON_SIGNATURE_FIELDS
                        continue
                else:
                    # concatenate line to message content
                    message += line

            # if we are on a signature fields zone...
            if cursor_status == ON_SIGNATURE_FIELDS:

                # TODO: Handle Dash escaped cleartext

                # parse field
                m = regex_fields.match(line.strip())
                if m:
                    # capture field
                    sig_field_name = m.groups()[0]
                    sig_field_value = m.groups()[1]
                    parsed_result['signatures'][signatures_index]['fields'][sig_field_name] = sig_field_value
                    continue

                # if blank line...
                if line.strip("\n\t\r ") == '':
                    cursor_status = ON_SIGNATURE_CONTENT
                    continue

            # if we are on the signature content...
            if cursor_status == ON_SIGNATURE_CONTENT:

                # if no public keys provided...
                if sender_pubkeys is None:
                    # raise exception
                    raise PARSER_MISSING_PUBLIC_KEYS_EXCEPTION

                # if end signature header detected...
                if regex_end_signature.match(line):
                    # end of parsing
                    break

                # if begin signature header detected...
                if regex_begin_signature.match(line):
                    signatures_index += 1
                    cursor_status = ON_SIGNATURE_FIELDS
                    continue

                for pubkey in sender_pubkeys:
                    verifier = VerifyingKey(pubkey)
                    signature = base64.b64decode(line)
                    parsed_result['signatures'][signatures_index]['pubkey'] = pubkey
                    try:
                        libnacl.crypto_sign_verify_detached(signature, message, verifier.vk)
                        parsed_result['signatures'][signatures_index]['valid'] = True
                    except ValueError:
                        parsed_result['signatures'][signatures_index]['valid'] = False

        return parsed_result

    @staticmethod
    def _decrypt(ascii_armor_message: str, signing_key: SigningKey) -> str:
        """
        Decrypt a message from ascii armor format

        :param ascii_armor_message: Utf-8 message
        :param signing_key: SigningKey instance created from credentials
        :return:
        """
        message = signing_key.decrypt_seal(base64.b64decode(ascii_armor_message))

        return message
