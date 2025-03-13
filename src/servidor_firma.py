import os
import sys
from pathlib import Path
import subprocess as sub
from socket import socket, AF_INET, gethostname
from threading import Thread
from SimpleLenSocket import *
from defs import *

# Crypto
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def openssl_gen_rsa_keys():
    gen_key_args = ["openssl", "genrsa", "-out", KEY_FILE, "2048"]
    extract_pub_args = ["openssl", "rsa", "-in", KEY_FILE, "-outform", "PEM", "-pubout", "-out", PUBLIC_KEY_FILE]

    sub.call(gen_key_args)
    sub.call(extract_pub_args)

def crypto_gen_rsa_keys():
    private_key = rsa.generate_private_key (
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Dump rsa keys

    with open(KEY_FILE, "wb") as privkfile:
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        privkfile.write(private_pem)
    
    with open(PUBLIC_KEY_FILE, "wb") as pubkfile:
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        pubkfile.write(public_pem)


def check_keys():
    if not Path(KEY_FILE).exists() or not Path(PUBLIC_KEY_FILE).exists():
        openssl_gen_rsa_keys()
    
def load_private_key_params(private_key, public_key):
    with open(private_key, "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )
    
    with open(public_key, "rb") as file:
        public_key = serialization.load_pem_public_key(file.read())

    private_numbers = private_key.private_numbers()
    public_numbers = public_key.public_numbers()
    params = {}
    
    params["d"] = private_numbers.d
    params["e"] = public_numbers.e
    params["n"] = public_numbers.n

    return params


def remove_files():
    
    for file_name in FILES:
        try:
            os.remove(file_name)
        except FileNotFoundError:
            print(f"{file_name} not found")
        except PermissionError:
            print(f"The current user does not have the permissions needed to delete {file_name}")
        except Exception:
            print("An error ocurred during cleanup")


"""
Blind signature protocol functions
"""


