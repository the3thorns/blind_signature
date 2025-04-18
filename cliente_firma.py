from operator import inv
from socket import gethostname
import random
from SimpleLenSocket import *
import sys

# Crypto imports
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import rsa, padding


"""
Server defs
"""
SERVER_ADDRESS = gethostname()
SERVER_PORT = 12345

def get_arguments():
    argc = len(sys.argv)
    if argc != 3:
        sys.exit(-1)
    
    return sys.argv[1], sys.argv[2]



def load_public_key(path: str):
    with open(path, "rb") as file:
        public_key = serialization.load_pem_public_key(file.read())
    return public_key



def hash_file(path_original_file) -> bytes:

    with open(path_original_file, "rb") as file:
        digest = hashes.Hash(hashes.SHA256())
        digest.update(file.read())

    return digest.finalize()

"""
Modular arithmetic functions
"""

def extended_gcd(a, b):

    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)

def modular_inverse(a, m):

    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None  # a y m no son coprimos, el inverso no existe
    else:
        return x % m  # Asegura que el resultado sea positivo

"""
Blind signature protocol funcions
"""

def blinding_function(hash, k, n, e) -> int:
    return (pow(k, e, n) * (hash % n)) % n # Se realiza la operación de esta forma para trabajar con números grandes

def deblining_function(blind_sign, inverse_k, n) -> int:
    return (blind_sign * inverse_k) % n



if __name__ == "__main__":
    path_fichero_original, path_public_key = get_arguments()
    public_key = load_public_key(path_public_key)

    public_numbers = public_key.public_numbers()
    e = public_numbers.e
    n = public_numbers.n

    hash = int.from_bytes(hash_file(path_fichero_original))

    k = random.randint(0, 1000000)
    blinded_hash = blinding_function(hash, k, n, e)

    connection_socket = SimpleLenSocket()
    connection_socket.connect(SERVER_ADDRESS, SERVER_PORT)



    connection_socket.close()