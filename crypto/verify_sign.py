import csv
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


def find_public_key(filename, username):
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Username'] == username:
                return serialization.load_pem_public_key(row['Pubkey'].replace('\\n', '\n').encode('utf-8'))
    return None


def is_signature_true(message, signature, public_key) -> bool:

    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Podpis jest poprawny")
        return True
    except InvalidSignature:
        print("Podpis jest niepoprawny")
        return False


def verify_signature(message, encoded_signature, filename_to_pbukeys_csv, sender_username) -> bool:
    public_key = find_public_key(filename, username)
    signature = base64.b64decode(encoded_signature)
    return is_signature_true(message, signature, public_key)

# Przykładowe dane
message = b"jAUYvRvJgwWRznoFa6zmLsOHnrNP8PY87Wn9ZI3f/0/D7lh4eumC4XBt905HOVbp/s8eq4p4sR/FXfpZFl4owVScStM+dGoNYC1dnmkoAQv46fjZoswRcRuWIdwkh1HsA13DoSyChTnMQtT3xj0nZQ8h2sNFiPgqUc8ezMHMwV2fYVZrdfMOtpGnSKPblw5tMrh9HYf1cnGXr5Ms2WTvXp9ZLcjcrzy9bWfmKRDfr7Vlfr7j2ZmmRYipIFFr/Jv++r60P2TNwX7NvoKglFmVNmjNFE4UEQ/PNV9+X0ljJD4Odyq2Pex3A0mLkYq9EHkDu7E1/W6/t8sof87cA57hOg==SmyfhsHRWA3j+CAs/OouYge6rlxBfaYwM1JtyqMBL50="
encoded_signature = b"jCEMI9vL8hfhI9Xs3KFDlv2jA17Mf5gn6mX+pdTrrQ7yfblc3Qpw+bnrTCt1xhaiwz7CcAD63fExmyiAeTasdmrXWF6obbiREebwWydb/QdkFuIfSWj25y9H2cPxoqPa80KOjPs3+KUUotovCuMKjuv5+RLA1vit7FbkdUOM3AwDv6xuHuiKm9pOGT5fUpc57GrWMR+AqXsGNh1LY97TUWnB6tW7qcl+ZgSoQsXUOUzovdMcZwlOch9qClLXBHG9aPVIh9lAH6CUZlUKz/BIsOUDRc6U9qPRBIYNzKDXMShvcAptYAVAzuiwSHPzhB67dC+VCtVeIJkzD1K+WHy1bg=="
filename = "pubkeys.csv"
username = "john"

verify_signature(message, encoded_signature, filename, username)

