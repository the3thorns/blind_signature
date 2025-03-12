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

def generate_rsa_keys():
    gen_key_args = ["openssl", "genrsa", "-out", KEY_FILE, "2048"]
    extract_pub_args = ["openssl", "rsa", "-in", KEY_FILE, "-outform", "PEM", "-pubout", "-out", PUBLIC_KEY_FILE]

    sub.call(gen_key_args)
    sub.call(extract_pub_args)

def check_keys():
    if not Path(KEY_FILE).exists() or not Path(PUBLIC_KEY_FILE).exists():
        generate_rsa_keys()
    
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


def clean():
    
    for file_name in FILES:
        try:
            os.remove(file_name)
        except FileNotFoundError:
            print(f"{file_name} not found")
        except PermissionError:
            print(f"The current user does not have the permissions needed to delete {file_name}")
        except Exception:
            print("An error ocurred during cleanup")


def start_blind_signature_process(soc: SimpleLenSocket):
    num = soc.receive()
    soc.close()
    print(num)


check_keys()

# Extract RSA params
key_params = load_private_key_params(KEY_FILE, PUBLIC_KEY_FILE)

socket_server = socket(AF_INET, SOCK_STREAM)
socket_server.bind((SERVER_ADDRESS, SERVER_PORT))
socket_server.listen()

while True:
    client_socket = SimpleLenSocket( socket_server.accept()[0] )
    start_blind_signature_process(client_socket)
