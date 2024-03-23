from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IPAddress Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(5)

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.read()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
        tcpCliSock.sendall(outputdata.encode())
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.","",1)
            print(hostn)
            try:
                # Connect to the socket to port 80
                c.connect((hostn,80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                # fileobj = c.makefile('r', 0)
                # fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")
                http_request = f"GET / HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
                c.send(http_request.encode())
                # Read the response into buffer
                response = b""
                while True:
                    data = c.recv(1024)
                    if not data:
                        break
                    response += data
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                tmpFile.write(response)
                tcpCliSock.send(response)
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
    # Close the client and the server sockets
    except KeyboardInterrupt:
        tcpSerSock.close()
        tcpCliSock.close()
        sys.exit()
    tcpCliSock.close()

tcpSerSock.close()
sys.exit()
