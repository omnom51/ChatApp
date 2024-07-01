from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
import base64


def load_private_key(filename):
    with open(filename, 'rb') as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None,  # W przypadku zabezpieczonego hasłem klucza, podaj hasło tutaj
            backend=default_backend()
        )
        return private_key


def decrypt_symmetric_key(encrypted_sym_key_base64, private_key):
    encrypted_sym_key = base64.b64decode(encrypted_sym_key_base64)

    try:
        sym_key = private_key.decrypt(
            encrypted_sym_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return sym_key
    except ValueError:
        print("Błąd deszyfrowania klucza symetrycznego.")
        return None


def decrypt_message(encrypted_message, sym_key):
    iv = encrypted_message[:16]
    encrypted_data = encrypted_message[16:]

    cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data_padded = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_data_padded) + unpadder.finalize()

    return decrypted_data


def decrypt(username, long_message, csv_filename):
    encrypted_message_b64 = l_message[344:]
    encrypted_sym_key_b64 = l_message[:344]

    private_key = load_private_key(csv_filename)
    if not private_key:
        print(f"Private key for recipient {username} not found.")
        exit(0)

    sym_key = decrypt_symmetric_key(encrypted_sym_key_b64, private_key)
    if not sym_key:
        print("Symmetric key decryption failed.")
        exit(0)

    decrypted_message = decrypt_message(base64.b64decode(encrypted_message_b64), sym_key)
    print("Decrypted message:", decrypted_message.decode())


# Przykładowe użycie:
l_message = b'dI9d0m5Q2xjBytR0x+3SeUepjKrjEHD/bOIKuvyLkjymTQNv4v6EDTMsXQWpDtlhpfq8Go6o5aJf/DZXikPLgtQiibEzdS7WCIrdB3iifPs4jYNxNzeRDDKU5logv8mttSJvo/eNUJCPDaaO1PNvG08vjKQYSZWR/ZI54XsqatD5NKf5yw3IFCD8mnMxJE1ed3HiBs5Lp6mrpTwCXDpBqiybIbc94zx8WUNth+Mc1yNLMV4KlALkn8XPVGlYlZx+jVwwhMoa8T3TNsBJgUai/RiUFkS996/kECgtzjLQRxtgvexwvoWQJagFYMNPcUfHvZpIXTwAreInznE/eDbM2g==7V8eKGbXk+NMcVteelQD+2bsQ//7eiEBZrh/yGSCxgY='

decrypt("john", l_message, "test_priv_key.txt")
