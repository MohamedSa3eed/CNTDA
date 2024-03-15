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

RTTs = []

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
        RTTs.append(RTT_time)
        print(f'Ping {sequence_number} {RTT_time} ')
        #set the timeout to None
        clientSocket.settimeout(None)
    except timeout:
        print("Request timed out")
    sequence_number += 1

#close the clientSocket 
clientSocket.close()
#calculate the average RTT
RTT_avarage = sum(RTTs) / len(RTTs)
print(f'Average RTT: {RTT_avarage}')
#calculate the maximum RTT 
RTT_max = max(RTTs)
print(f'Maximum RTT: {RTT_max}')
#calculate the minimum RTT
RTT_min = min(RTTs)
print(f'Minimum RTT: {RTT_min}')
#claculate the packetloss rate
packet_loss_rate = (10 - len(RTTs)) / 10 * 100
print(f'Packet loss rate: {packet_loss_rate}%')
