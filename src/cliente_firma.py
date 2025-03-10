import os
import sys
import subprocess as sub
from socket import socket, AF_INET, gethostname
from threading import Thread
from SimpleLenSocket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect((gethostname(), 12345))

client_socket = SimpleLenSocket(soc=s)

client_socket.send("hola mundo")

