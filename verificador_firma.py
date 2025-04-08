from hmac import digest
import sys

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

def hash_file(original_file) -> bytes:

    with open(original_file, "rb") as file:
        digest = hashes.Hash(hashes.SHA256())
        digest.update(file.read())

    return digest.finalize()


def get_arguments():
    argc = len(sys.argv)

    hash = hash_file(sys.argv[1])

    if argc != 4:
        sys.exit(-1)
    
    with open(sys.argv[2], "r") as signature_file:
        int_sig = int(signature_file.read())
        signature = int_sig
        #signature = int_sig.to_bytes(
        #    length=2048//8,
        #    byteorder='little'
        #)

        #d = hashes.Hash(hashes.SHA256())
        #d.update(signature)
        #signature = d.finalize()
    
    # Read public key
    
    with open(sys.argv[3], "rb") as file:
        public_key = serialization.load_pem_public_key(file.read())
        
    return hash, signature, public_key


def verificate_signature(public_key, hash, signature) -> bool:
    public_members = public_key.public_numbers()
    n = public_members.n
    e = public_members.e

    mensaje_recuperado = pow(signature, e, n)

    return hash == mensaje_recuperado

if __name__ == "__main__":
    hash, signature, public_key = get_arguments()

    if verificate_signature(public_key, hash, signature):
        print("FIRMA VÁLIDA")
    else:
        print("FIRMA NO VÁLIDA")
