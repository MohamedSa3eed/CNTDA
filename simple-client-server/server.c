#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>

#define IP "localhost" // the IP address users will be connecting to
#define PORT "90001" // the port users will be connecting to
#define BACKLOG 10 // how many pending connections queue will hold

int main(int argc, char *argv[]) {
  // string store data to send to client 
  char hostname[255];
  char serMsg[255] = "Message from the server to the "
                     "client \'Hello Client\' "; 
  struct sockaddr_storage their_addr;
  socklen_t addr_size;
  struct addrinfo hints, *servinfo;
  int sockfd, value;

  printf("enter number between 1 and 100: ");
  scanf("%d", &value);

  // first, load up address structs with getaddrinfo():
  memset(&hints, 0, sizeof hints);
  hints.ai_family = AF_UNSPEC; // use IPv4 or IPv6, whichever
  hints.ai_socktype = SOCK_STREAM; // TCP
  hints.ai_flags = AI_PASSIVE; // fill in my IP for me (replace IP with NULL)
  int info = getaddrinfo(NULL, PORT, &hints, &servinfo);
  if (info != 0) {
    fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(info));
    exit(EXIT_FAILURE);
  }

  // make a socket:
  sockfd = socket(servinfo->ai_family, servinfo->ai_socktype, servinfo->ai_protocol);
  if (sockfd == -1) {
    perror("socket");
    exit(EXIT_FAILURE);
  }
  // bind it to the port we passed in to getaddrinfo():
  int rc = bind(sockfd, servinfo->ai_addr, servinfo->ai_addrlen);
  if (rc == -1) {
    perror("bind");
    exit(EXIT_FAILURE);
  }

  // get the host name
  int res =  gethostname(hostname, sizeof(hostname));
  if (res == -1) {
    perror("gethostname");
    exit(EXIT_FAILURE);
  }
  printf("server: host name is %s\n", hostname);

  while (1){
    printf("server: waiting for connections...\n");
    int connection = listen(sockfd, BACKLOG);
    if (connection == -1) {
      perror("listen");
      exit(EXIT_FAILURE);
    }

    printf ("server: accepting connection...\n");
    addr_size = sizeof(their_addr);
    int client_fd = accept(sockfd, (struct sockaddr *)&their_addr, &addr_size);
    if (client_fd == -1) {
      perror("accept");
      exit(EXIT_FAILURE);
    }
    else {
      // get the client address
      struct sockaddr_in peeraddr;
      socklen_t peeraddr_len = sizeof(peeraddr);
      if(getpeername(client_fd, (struct sockaddr*)&peeraddr, &peeraddr_len) != -1){
        char peername[INET_ADDRSTRLEN];
        int peerport;
        inet_ntop(AF_INET, (struct sockaddr*)&peeraddr, peername, sizeof(peername));
        peerport = ntohs(peeraddr.sin_port);
        printf("server: got connection from %s:%d\n", peername, peerport);
      }

      printf("server: receiving message from client...\n");
      char buf[255];
      int recvMsg = recv(client_fd, buf, sizeof(buf), 0);
      if (recvMsg == -1) {
        perror("recv");
        exit(EXIT_FAILURE);
      }
      else {
        printf("server: received message from client\n");
        int num = atoi(buf);
        printf("Server: received %d\n", num);
        if (num > 100 || num < 1){
          printf("server: out of range\n");
          freeaddrinfo(servinfo); // free the linked-list
          close(client_fd);
          close(sockfd);
          exit(EXIT_FAILURE);
        }
      }
      // Calculate the length needed for the string representation
      int length = snprintf(NULL, 0, "%d", value) + 1;
      // Allocate memory for the string
      char stringValue[length];
      // Use snprintf to convert the integer to a string
      snprintf(stringValue, length, "%d", value);

      // send message to client 
      // it returns the number of bytes sent 
      // or -1 if an error occurred
      // if the whole message is not sent its up to you to resend the rest
      int sent_bytes = send(client_fd, stringValue, sizeof(stringValue), 0);
      if (sent_bytes == -1) {
        perror("send");
        exit(EXIT_FAILURE);
      }
      sent_bytes = send(client_fd, hostname, sizeof(hostname), 0);
      if (sent_bytes == -1) {
        perror("send");
        exit(EXIT_FAILURE);
      }
      else {
        printf("server: sent message to client\n");
      }
    }
    close(client_fd);
  }
  freeaddrinfo(servinfo); // free the linked-list
  close(sockfd);
  return EXIT_SUCCESS;
}
