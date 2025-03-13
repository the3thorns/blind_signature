import os
import sys
import subprocess as sub
from socket import socket, AF_INET, gethostname
import random
from defs import *
from SimpleLenSocket import *

# Crypto imports
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

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

    hash = 12345678

    s = SimpleLenSocket()
    s.connect(SERVER_ADDRESS, SERVER_PORT)

    k = int(random.uniform(0, 10000))
    A = (pow(k, rsa_params["e"], rsa_params["n"]) * (hash % rsa_params["n"])) % rsa_params["n"]

    print(A)
    s.send(A)