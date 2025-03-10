import os
import sys
import subprocess as sub
import socket
from threading import Thread

class WorkerThread(Thread):
    
    def __init__(self, client_socket=None):
        super().__init__()
        if client_socket == None:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.soc = client_socket

    def run(self):
        return super().run()

# Creating a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 12345))
server_socket.listen()

# Server loop

for _ in range(5):
    client_socket, address = server_socket.accept()

    message = client_socket.recv()
    print(message)
    client_socket.shutdown()
    client_socket.close()


server_socket.shutdown()
server_socket.close()    