from socket import *
import ssl
import base64

username = "user@gmail.com"
password = "password"

recipient = "user@example.com"

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
print(f'connected to {mailserver}')
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
 print('250 reply not received from server.')

# Upgrade the connection to a secure SSL/TLS connection
TTLCommand = 'STARTTLS\r\n'
clientSocket.send(TTLCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
context = ssl.create_default_context()
secure_clientSocket = context.wrap_socket(clientSocket , server_hostname=mailserver[0])

# Send EHLO command and print server response.
ehloCommand = 'EHLO Alice\r\n'
secure_clientSocket.send(ehloCommand.encode())
recv = secure_clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send AUTH LOGIN command and print server response.
AUTHCommand = 'AUTH LOGIN\r\n'
secure_clientSocket.send(AUTHCommand.encode())
recv = secure_clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server.')

# Send username and print server response.
usernameCommand = base64.b64encode(username.encode()) + '\r\n'.encode()
secure_clientSocket.send(usernameCommand)
recv = secure_clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server.')

# Send password and print server response.
passwordCommand = base64.b64encode(password.encode()) + '\r\n'.encode()
secure_clientSocket.send(passwordCommand)
recv = secure_clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '235':
    print('235 reply not received from server.')


# Send MAIL FROM command and print server response.
mailFromCommand = 'MAIL FROM <' + username + '>\r\n'
secure_clientSocket.send(mailFromCommand.encode())
recv = secure_clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
 print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptToCommand = 'RCPT TO <' + recipient + '>\r\n'
secure_clientSocket.send(rcptToCommand.encode())
recv = secure_clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
secure_clientSocket.send(dataCommand.encode())
recv = secure_clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
secure_clientSocket.send(msg.encode())

# Message ends with a single period.
secure_clientSocket.send(endmsg.encode())
recv = secure_clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
secure_clientSocket.send(quitCommand.encode())
recv = secure_clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '221':
    print('221 reply not received from server.')

clientSocket.close()
