from operator import inv, invert
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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

"""
Blind signature protocol funcions
"""

def blinding_function(hash, k, n, e) -> int:
    
    return (pow(k, e, n) * (hash % n)) % n # Se realiza la operación de esta forma para trabajar con números grandes

def deblining_function(blind_sign, k, n) -> int:
    inverse_k = mod_inverse(k, n)
    return (blind_sign * inverse_k) % n



if __name__ == "__main__":
    path_fichero_original, path_public_key = get_arguments()
    public_key = load_public_key(path_public_key)

    public_numbers = public_key.public_numbers()
    e = public_numbers.e
    n = public_numbers.n

    hash = int.from_bytes(hash_file(path_fichero_original))

    k = random.randint(1, n - 1)
    while gcd(k, n) != 1:
        r = random.randint(1, n-1)

    blinded_hash = blinding_function(hash, k, n, e)

    connection_socket = SimpleLenSocket()
    connection_socket.connect(SERVER_ADDRESS, SERVER_PORT)
    connection_socket.send_int(blinded_hash)

    blinded_signature = connection_socket.receive_int()
    connection_socket.close()
    
    deblinded_signature = deblining_function(blinded_signature, k, n)
    num_bytes = (deblinded_signature.bit_length() + 7) // 8
    db_bytes = deblinded_signature.to_bytes(num_bytes, byteorder='big')
    hex_string = ':'.join(format(x, '02X') for x in db_bytes)
    print(hex_string, end="")