from http import client, server
import os
import sys
from pathlib import Path
import subprocess as sub
from socket import socket, AF_INET, gethostname
from threading import Thread
from SimpleLenSocket import *
from defs import *

# Crypto
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature


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

    
def load_private_key_params(path_priv, path_pub):
    with open(path_priv, "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )
    
    with open(path_pub, "rb") as file:
        public_key = serialization.load_pem_public_key(file.read())

    private_numbers = private_key.private_numbers()
    public_numbers = public_key.public_numbers()
    params = {}
    
    params["d"] = private_numbers.d
    params["e"] = public_numbers.e
    params["n"] = public_numbers.n

    return private_key, public_key, params


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


def sign_message(private_key, message):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),

            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature

def verificate_signature(public_key, message, signature) -> bool:
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
        return True
    except InvalidSignature:
        return False

crypto_gen_rsa_keys()

private_key, public_key, params = load_private_key_params(KEY_FILE, PUBLIC_KEY_FILE)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
server_socket.listen()

while True:
    client_socket = SimpleLenSocket( server_socket.accept()[0] )
    blinded_message = client_socket.receive_bytes()
    blinded_signature = sign_message(private_key, blinded_message)

    if not verificate_signature(public_key, blinded_message, blinded_signature):
        print("La firma no es correcta")
    else:
        print("La firma es correcta")
