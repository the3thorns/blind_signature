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

public_key = load_public_key(PUBLIC_KEY_FILE)
public_numbers = public_key.public_numbers()

RSA_n = public_numbers.n
RSA_e = public_numbers.e

hash = 12345678

s = SimpleLenSocket()
s.connect(SERVER_ADDRESS, SERVER_PORT)

k = int(random.uniform(0, 10000))
A = (pow(k, RSA_e, RSA_n) * (hash % RSA_n)) % RSA_n
print(A)

s.send(A)