import subprocess as sub
from socket import socket, AF_INET, SOCK_STREAM, error
import struct

"""
Protocol: SimpleLen

Message: [H-LEN][PAYLOAD]
"""

class SimpleLenSocket():

    def __init__(self, soc : socket | None =None):
        if soc == None:
            self.soc = socket(AF_INET, SOCK_STREAM)
        else:
            self.soc = soc
    
    def connect(self, host: str, port: int):
        self.soc.connect((host, port))
    
    def send(self, msg: int):
        num_bytes = (msg.bit_length() + 7) // 8
        payload = msg.to_bytes(length=num_bytes, byteorder="big", signed=False)

        header = struct.pack("!I", num_bytes)

        packet = header + payload
        try:
            self.soc.send(packet)
        except error:
            print("No se ha podido realizar el envío")

    def receive(self) -> int : # Returns a hash
        header = self.soc.recv(4)
        length = struct.unpack("!I", header)[0]

        bytes_readed = 0
        payload_parts = []
        while bytes_readed < length:
            readed = self.soc.recv(length - bytes_readed)

            if not readed: # Se ha cerrado la conexión
                return None

            bytes_readed += len(readed)
            payload_parts.append(readed)
        
        payload = b''.join(payload_parts)

        num = int.from_bytes(payload, byteorder="big", signed=False)
        return num

        
    
    def close(self):
        self.soc.close()