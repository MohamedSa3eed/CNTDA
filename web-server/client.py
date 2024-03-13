#! /usr/bin/python
from socket import *
import sys

if len(sys.argv) != 4:
    print("Usage: python client.py server_host server_port filename")
    sys.exit(1)

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
requestedFile = sys.argv[3]

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, int(serverPort)))

request = 'GET /' + requestedFile + ' HTTP/1.1\r\n\r\n'
clientSocket.send(request.encode())

response = clientSocket.recv(1024)
print('From Server:', response.decode())
