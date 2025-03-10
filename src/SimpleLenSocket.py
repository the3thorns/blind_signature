import os
import sys
import subprocess as sub
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import struct

"""
Protocol: SimpleLen

Message: [H-LEN][PAYLOAD]
"""

class SimpleLenSocket():

    def __init__(self, soc=None):
        if soc == None:
            self.soc = socket(AF_INET, SOCK_STREAM)
        else:
            self.soc = soc
    
    def connect(self, host: str, port: int):
        self.soc.connect((host, port))
    
    def send(self, msg: str):
        payload = msg.encode("utf-8")
        length = len(payload)
        header = struct.pack(">I", length)

        packet = header + payload
        self.soc.send(packet)


    def receive(self): # Returns a hash
        header = self.soc.recv(4)

        if not header:
            return None
        
        length = struct.unpack(">I", header)[0]

        payload = b""
        
        while len(payload) < length:
            chunk = self.soc.recv(length - len(payload))

            if not chunk:
                return None
            payload += chunk
        
        decoded_msg = payload.decode("utf-8")
        return decoded_msg
    
    def close(self):
        self.soc.close()