#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

int main() {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    SOCKET sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(54001);
    server.sin_addr.s_addr = INADDR_ANY;
    bind(sock, (sockaddr*)&server, sizeof(server));

    char buffer[512];
    sockaddr_in from;
    int fromlen = sizeof(from);
    while (true) {
        int bytesReceived = recvfrom(sock, buffer, sizeof(buffer) - 1, 0, (sockaddr*)&from, &fromlen);
        if (bytesReceived > 0) {
            buffer[bytesReceived] = 0;
            std::cout << "UDP ricevuto: " << buffer << std::endl;
        }
    }

    closesocket(sock);
    WSACleanup();
    return 0;
}