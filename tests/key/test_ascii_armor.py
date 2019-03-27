from duniterpy.key import AsciiArmor, SigningKey
from duniterpy.key.ascii_armor import BEGIN_MESSAGE_HEADER, BEGIN_SIGNATURE_HEADER, END_SIGNATURE_HEADER, \
    END_MESSAGE_HEADER
import unittest


class TestAsciiArmor(unittest.TestCase):
    def test_create_encrypted_and_signed(self):
        # pubkey of recipient
        alice_signing_key = SigningKey.from_credentials("alice", "password")

        # signing key of issuer
        bob_signing_key = SigningKey.from_credentials("bob", "password")

        # message
        message = """
Hello world !

Héhé ;-)

This is a utf-8 message...
       
       """
        # create encrypted and signed ascii armor message
        encrypted_and_signed_aa_message = AsciiArmor.create(message, alice_signing_key.pubkey, [bob_signing_key])

        # split in lines for check up
        aa_message_lines = encrypted_and_signed_aa_message.splitlines()

        # check before message
        self.assertEqual(aa_message_lines[0], BEGIN_MESSAGE_HEADER)
        self.assertTrue(aa_message_lines[1].startswith("Version:"))
        self.assertEqual("", aa_message_lines[2].strip())

        # check after message
        self.assertEqual(aa_message_lines[4], BEGIN_SIGNATURE_HEADER)
        self.assertTrue(aa_message_lines[5].startswith("Version:"))
        self.assertEqual("", aa_message_lines[6].strip())
        self.assertEqual(aa_message_lines[8], END_SIGNATURE_HEADER)

        # parse ascii armor message
        result = AsciiArmor.parse(encrypted_and_signed_aa_message, alice_signing_key, [bob_signing_key.pubkey])

        # check result
        self.assertEqual(message + "\n", result['message']['content'])
        self.assertTrue(message + "\n", result['signatures'][0]['valid'])

    def test_create_encrypted(self):
        # pubkey of recipient
        alice_signing_key = SigningKey.from_credentials("alice", "password")

        # message
        message = """
Hello world !

Héhé ;-)

This is a utf-8 message...

       """
        # create encrypted and signed ascii armor message
        encrypted_aa_message = AsciiArmor.create(message, alice_signing_key.pubkey)

        # split in lines for check up
        aa_message_lines = encrypted_aa_message.splitlines()

        # check before message
        self.assertEqual(aa_message_lines[0], BEGIN_MESSAGE_HEADER)
        self.assertTrue(aa_message_lines[1].startswith("Version:"))
        self.assertEqual("", aa_message_lines[2].strip())

        # check after message
        self.assertEqual(aa_message_lines[4], END_MESSAGE_HEADER)

        # parse ascii armor message
        result = AsciiArmor.parse(encrypted_aa_message, alice_signing_key)

        # check result
        self.assertEqual(message + "\n", result['message']['content'])

    def test_create_signed_cleartext(self):
        # signing key of issuer
        bob_signing_key = SigningKey.from_credentials("bob", "password")

        # message
        message = """
Hello world !

Héhé ;-)

This is a utf-8 message...

       """
        # create encrypted and signed ascii armor message
        signed_cleartext_aa_message = AsciiArmor.create(message, None, [bob_signing_key])

        # split in lines for check up
        aa_message_lines = signed_cleartext_aa_message.splitlines()

        # check before message
        self.assertEqual(aa_message_lines[0], BEGIN_MESSAGE_HEADER)
        self.assertEqual("", aa_message_lines[1].strip())

        # check after message
        self.assertEqual(aa_message_lines[10], BEGIN_SIGNATURE_HEADER)
        self.assertTrue(aa_message_lines[11].startswith("Version:"))
        self.assertEqual("", aa_message_lines[12].strip())
        self.assertEqual(aa_message_lines[14], END_SIGNATURE_HEADER)

        # parse ascii armor message
        result = AsciiArmor.parse(signed_cleartext_aa_message, None, [bob_signing_key.pubkey])

        # check result
        self.assertEqual(message + "\n", result['message']['content'])
        self.assertTrue(message + "\n", result['signatures'][0]['valid'])
