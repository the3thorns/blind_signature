import os
import sys
import subprocess as sub
from socket import socket, AF_INET, gethostname
from threading import Thread
from SimpleLenSocket import *

KEY_FILE = "server_key"
PUBLIC_KEY_FILE = f"{KEY_FILE}.pub"

FILES = [KEY_FILE, PUBLIC_KEY_FILE]

def generate_rsa_keys():
    gen_key_args = ["openssl", "genrsa", "-out", KEY_FILE, "2048"]
    extract_pub_args = ["openssl", "rsa", "-in", KEY_FILE, "-outform", "PEM", "-pubout", "-out", PUBLIC_KEY_FILE]

    sub.call(gen_key_args)
    sub.call(extract_pub_args)

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


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((gethostname(), 12345))
server_socket.listen()

for _ in range(5):
    client_socket = SimpleLenSocket(server_socket.accept()[0])
    print(client_socket.receive())
    
    client_socket.close()

server_socket.close()