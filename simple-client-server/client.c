#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

#define PORT "90001" // the port client will be connecting to

int main(int argc, char *argv[]) {
  struct addrinfo hints, *servinfo;
  int sockfd, value, recived_value;
  char hostname[255];

  if (argc != 2) {
    fprintf(stderr, "usage: client server_ip \n");
    exit(EXIT_FAILURE);
  }
  char *IP = argv[1];
  

  printf("enter number between 1 and 100: ");
  scanf("%d", &value);
  // first, load up address structs with getaddrinfo():
  memset(&hints, 0, sizeof hints);
  hints.ai_family = AF_UNSPEC; // use IPv4 or IPv6, whichever
  hints.ai_socktype = SOCK_STREAM; // TCP
  int info = getaddrinfo(IP, PORT, &hints, &servinfo);
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
  printf("client: connecting...\n");
  int connection = connect(sockfd, servinfo->ai_addr, servinfo->ai_addrlen);
  if (connection == -1) {
    perror("connect");
    exit(EXIT_FAILURE);
  }
  else {
    printf("client: connected\n");
    printf("client: sending message to server...\n");
    // Calculate the length needed for the string representation
    int length = snprintf(NULL, 0, "%d", value) + 1;
    // Allocate memory for the string
    char stringValue[length];
    // Use snprintf to convert the integer to a string
    snprintf(stringValue, length, "%d", value);
    int sent_bytes = send(sockfd, stringValue, 12, 0);
    if (sent_bytes == -1) {
      perror("send");
      exit(EXIT_FAILURE);
    }
    else {
      printf("client: sent message to server\n");
    }
    printf("client: receiving message from server...\n");
    char buf[255];
    int recvMsg = recv(sockfd, buf, sizeof(buf), 0);
    if (recvMsg == -1) {
      perror("recv");
      exit(EXIT_FAILURE);
    }
    recived_value = atoi(buf);
    recvMsg = recv(sockfd, buf, sizeof(buf), 0);
    if (recvMsg == -1) {
      perror("recv");
      exit(EXIT_FAILURE);
    }
    // get the host name
    int res =  gethostname(hostname, sizeof(hostname));
    if (res == -1) {
      perror("gethostname");
      exit(EXIT_FAILURE);
    }
    printf("client: the host name is: %s\n", hostname);
    printf("client: the value is: %d\n", value);
    printf("client: the server name is: %s\n", buf);
    printf("client: the server value is: %d\n", recived_value);
    printf("client: the sum of the two values is: %d\n", value + recived_value);
  }
  freeaddrinfo(servinfo); // free the linked-list
  close(sockfd);
  return EXIT_SUCCESS;
}
