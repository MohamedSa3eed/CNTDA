from socket import *
import time

# Set the server address to variable serverName
serverName = 'localhost'
# Set the server port to variable serverPort
serverPort = 12000

# Create a UDP socket
clientSocket = socket(AF_INET,SOCK_DGRAM)

#set the sequence number to 1
sequence_number = 1

#set the message to "Ping"
message = "hello world!"

while sequence_number <= 10 :
    #send the message to the server
    start = time.time()
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    try :
        #set the timeout to 1 second
        clientSocket.settimeout(1)
        #receive the message from the server
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        # get the RTT time
        RTT_time = time.time() - start
        print(f'Ping {sequence_number} {RTT_time} ')
        #set the timeout to None
        clientSocket.settimeout(None)
    except timeout:
        print("Request timed out")
    sequence_number += 1
