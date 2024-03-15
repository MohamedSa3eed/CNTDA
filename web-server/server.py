#import socket module
from socket import *
from threading import Thread
import sys # In order to terminate the program

def request_handle(connectionSocket):
    try:
        # receive the message from the client
        message = connectionSocket.recv(1024)
        print("message:",message)
        # open the file and read the content (first line)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        #Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        #Send the content of the requested file to the client
        connectionSocket.sendall(outputdata.encode())
        # close the file
        f.close()
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        f = open("notFound.html")
        outputdata = f.read()
        connectionSocket.sendall(outputdata.encode())
        #Close client socket
        connectionSocket.close()

serverHostName = gethostname()
print("Server: host name is",serverHostName)
print("Server: IP address is",gethostbyname(serverHostName))
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
port = 9000
serverSocket.bind((serverHostName, port))
serverSocket.listen(1)
print('listening on port',port)

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        thread = Thread(target=request_handle, args=(connectionSocket,))
        thread.start()
    except KeyboardInterrupt:
        serverSocket.close()
        sys.exit()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
