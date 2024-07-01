import csv
from cryptography.hazmat.primitives.asymmetric import  padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
import os
import base64


def find_public_key(filename, username):
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Username'] == username:
                return row['Pubkey'].replace('\\n', '\n')
    return None

def generate_symmetric_key():
    sym_key = os.urandom(32)
    return sym_key

def encrypt_symmetric_key(sym_key, public_key):
    public_key_bytes = public_key.encode()
    public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
    encrypted_sym_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_sym_key

def encrypt_message(message, sym_key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()

    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    return iv + encrypted_message

def encrypt(username, message, csv_filename):

    public_key = find_public_key(csv_filename, username)
    if not public_key:
        #print(f"Public key for recipient {username} not found.")
        exit(0)

    sym_key = generate_symmetric_key()
    encrypted_sym_key = encrypt_symmetric_key(sym_key, public_key)
    encrypted_message = encrypt_message(message, sym_key)

    #print("Encrypted symmetric key:", len(base64.b64encode(encrypted_sym_key)))
    #print("Encrypted message:", base64.b64encode(encrypted_message))

    # Zaszyfrowany klucz publiczny w postaci kodu base64 ma stałą długość 344 znaków.
    ciphertext = base64.b64encode(encrypted_sym_key) + base64.b64encode(encrypted_message)

    print(ciphertext)

encrypt("john", "ŻÓŁĆ", "pubkeys.csv")