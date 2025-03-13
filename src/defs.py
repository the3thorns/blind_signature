from socket import gethostname

KEY_FILE = "server_key"
PUBLIC_KEY_FILE = f"{KEY_FILE}.pub"
ORIGINAL_FILE = "fichero_original"

FILES = [KEY_FILE, PUBLIC_KEY_FILE]

# Network defs
SERVER_ADDRESS = gethostname()
SERVER_PORT = 12345
