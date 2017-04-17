#! /usr/bin/python3

import argparse
import os
from parser import ASN1
from cryptosystem import RSACryptoSystem
from constants import exponent, d_encryption, d_signature, n_encryption, n_signature


def encrypt(rsa):
    key = os.urandom(24)
    cipher_text = rsa.encrypt_triple_des(key=key)

    encrypted_key = RSACryptoSystem.rsa_encrypt(
        int.from_bytes(key, byteorder='big'),
        int(exponent, 16),
        int(n_encryption, 16)
    )

    encoded_bytes = ASN1.encode_file(
        int(n_encryption, 16),
        int(exponent, 16),
        encrypted_key,
        len(cipher_text),
        cipher_text
    )

    with open('encryption.efn', 'wb') as file:
        file.write(encoded_bytes)

    return True


def decrypt(rsa):
    asn = ASN1()
    asn.parse_file('encryption.efn')
    restored_module = asn.decoded_values[0]
    restored_exp = asn.decoded_values[1]
    encrypted_key = asn.decoded_values[2]

    restored_key = RSACryptoSystem.rsa_decrypt(
        encrypted_key,
        int(d_encryption, 16),
        restored_module
    )

    restored_key = restored_key.to_bytes((restored_key.bit_length() + 7) // 8, 'big')

    decrypted_text = rsa.decrypt_triple_des(key=restored_key, filename='cipher')
    print('#######################################')
    print(decrypted_text.decode('utf-8', 'ignore'))
    print('#######################################')
    return True


def add_signature():
    pass


def check_signature():
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encrypt", help="Encrypt file", action="store_true")
    parser.add_argument("-d", "--decrypt", help="Decrypt file", action="store_true")
    parser.add_argument("-s", "--signature", help="Add signature", action="store_true")
    parser.add_argument("-c", "--check", help="Check signature", action="store_true")
    parser.add_argument("-f", "--file", help="File")
    args = parser.parse_args()
    rsa = RSACryptoSystem(args.file)
    if args.encrypt:
        print('[+] Encryption mode')
        print('[+] filename: ', args.file)
        if encrypt(rsa):
            print('[+] Encrypted done!')
    elif args.decrypt:
        print('[+] Decryption mode')
        print('[+] filename: ', args.file)
        if decrypt(rsa):
            print('[+] Decrypted: ')
    elif args.signature:
        print('[+] Add signature mode')
        print('[+] filename: ', args.file)
    elif args.check:
        print('[+] Check signature mode')
        print('[+] filename: ', args.file)

if __name__ == '__main__':
    main()
