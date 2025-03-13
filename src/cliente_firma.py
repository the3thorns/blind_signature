import os
import sys
import subprocess as sub
from socket import socket, AF_INET, gethostname
import random
from defs import *
from SimpleLenSocket import *

# Crypto imports
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

def load_public_key(path):
    with open(path, "rb") as file:
        public_key = serialization.load_pem_public_key(file.read())
    return public_key

def load_public_numbers(public_key):
    public_numbers = public_key.public_numbers()
    params = {}
    params["n"] = public_numbers.n
    params["e"] = public_numbers.e

    return params


def digest_file(original_file) -> bytes:

    with open(original_file, "rb") as file:
        digest = hashes.Hash(hashes.SHA256())
        digest.update(file.read())

    return digest.finalize()

"""
Blind signature protocol funcions
"""

def blinding_function(hash, k, rsa_params):
    return (pow(k, rsa_params["e"], rsa_params["n"]) * (hash % rsa_params["n"])) % rsa_params["n"]

def deblinding_function(blinded_hash, k, rsa_params):
    pass

if __name__ == "__main__":
    public_key = load_public_key(PUBLIC_KEY_FILE)
    rsa_params = load_public_numbers(public_key)

    hash = int.from_bytes(digest_file(ORIGINAL_FILE))

    s = SimpleLenSocket()
    s.connect(SERVER_ADDRESS, SERVER_PORT)

    k = int(random.uniform(0, 10000))
    A = (pow(k, rsa_params["e"], rsa_params["n"]) * (hash % rsa_params["n"])) % rsa_params["n"]

    print(A)
    s.send(A)