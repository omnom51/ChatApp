from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import base64

def get_private_key(filename):
    with open(filename, 'r') as file:
        return file.read().encode('utf-8')
    return None


def sign_message(message, private_key_str):

    private_key = serialization.load_pem_private_key(private_key_str, password=None)
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


message = b"jAUYvRvJgwWRznoFa6zmLsOHnrNP8PY87Wn9ZI3f/0/D7lh4eumC4XBt905HOVbp/s8eq4p4sR/FXfpZFl4owVScStM+dGoNYC1dnmkoAQv46fjZoswRcRuWIdwkh1HsA13DoSyChTnMQtT3xj0nZQ8h2sNFiPgqUc8ezMHMwV2fYVZrdfMOtpGnSKPblw5tMrh9HYf1cnGXr5Ms2WTvXp9ZLcjcrzy9bWfmKRDfr7Vlfr7j2ZmmRYipIFFr/Jv++r60P2TNwX7NvoKglFmVNmjNFE4UEQ/PNV9+X0ljJD4Odyq2Pex3A0mLkYq9EHkDu7E1/W6/t8sof87cA57hOg==SmyfhsHRWA3j+CAs/OouYge6rlxBfaYwM1JtyqMBL50="
filename = "test_priv_key.txt"
print(base64.b64encode(sign_message(message, get_private_key(filename))))