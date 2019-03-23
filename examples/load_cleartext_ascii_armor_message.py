from duniterpy.key import AsciiArmor

# CONFIG #######################################

CLEARTEXT_AA_MESSAGE_PATH = '/tmp/duniter_cleartext_aa_message.txt'

################################################

if __name__ == '__main__':
    # Ask public key of the issuer
    pubkeyBase58 = input("Enter public key of the message issuer: ")

    # Load cleartext ascii armor message from a file
    with open(CLEARTEXT_AA_MESSAGE_PATH, 'r') as file_handler:
        ascii_armor_block = file_handler.read()

    print("Cleartext Ascii Armor Message loaded from file ./{0}".format(CLEARTEXT_AA_MESSAGE_PATH))

    result = AsciiArmor.parse(ascii_armor_block, None, [pubkeyBase58])
    print('------------- MESSAGE ------------\n' + result['message']['content'] + '----------------------------------')
    print(result)
