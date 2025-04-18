import os
import subprocess as sub
from socket import socket, AF_INET, gethostname
from SimpleLenSocket import *
# from defs import *

# Crypto
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

"""
File defs
"""
SERVER_ADDRESS = gethostname()
SERVER_PORT = 12345
KEY_FILE = "server_key"
PUBLIC_KEY_FILE = f"{KEY_FILE}.pub"
FILES = [KEY_FILE, PUBLIC_KEY_FILE]


def rsa_keygen():
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

    
def load_rsa_keys(path_priv, path_pub):
    with open(path_priv, "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )
    
    with open(path_pub, "rb") as file:
        public_key = serialization.load_pem_public_key(file.read())

    return private_key, public_key


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


def sign_message(n, d, message):
    return pow(message, d, n)

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


if __name__ == "__main__":
    remove_files()
    rsa_keygen()

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen()
    print(f"Server listening at {SERVER_ADDRESS}:{SERVER_PORT}")

    while True:
        accepted_socket, _a = server_socket.accept()
        connection_socket = SimpleLenSocket(accepted_socket)
        print("== NEW SESSION STARTED ==")

        connection_socket.close()
        print("== SESSION ENDED ==")
