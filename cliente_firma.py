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


def hash_file(original_file) -> bytes:

    with open(original_file, "rb") as file:
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

def blinding_function(hash, k, rsa_params) -> int:
    return (pow(k, rsa_params["e"], rsa_params["n"]) * (hash % rsa_params["n"])) % rsa_params["n"] # Se realiza la operación de esta forma para trabajar con números grandes

def deblining_function(blind_sign, inverse_k, n) -> int:
    return (blind_sign * inverse_k) % n



if __name__ == "__main__":
    ORIGINAL_FILE, PUBLIC_KEY_FILE = get_arguments()
    
    public_key = load_public_key(PUBLIC_KEY_FILE) # Carga la clave pública del servidor
    rsa_params = load_public_numbers(public_key) # Carga los miembros públicos de la clave

    hash = int.from_bytes(hash_file(ORIGINAL_FILE)) # Genera el hash a firmar

    s = SimpleLenSocket()
    s.connect(SERVER_ADDRESS, SERVER_PORT)

    k = int(random.uniform(0, 10000)) # Factor de opacidad
    A = blinding_function(hash, k, rsa_params)
    s.send_int(A)

    """
    The server will perform the signature process and send back an integer
    """

    blind_sig = s.receive_int() # Firma cegada
    s.close()
    
    inverse =  modular_inverse(k ,rsa_params["n"])
    signature = deblining_function(blind_sig, inverse, rsa_params["n"])

    print(signature, end=None)