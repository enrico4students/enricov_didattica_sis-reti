#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

int main() {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    SOCKET listenSock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(54000);
    server.sin_addr.s_addr = INADDR_ANY;
    bind(listenSock, (sockaddr*)&server, sizeof(server));
    listen(listenSock, SOMAXCONN);
    SOCKET client = accept(listenSock, NULL, NULL);
    char buffer[512];
    while (true) {
        int bytesReceived = recv(client, buffer, sizeof(buffer) - 1, 0);
        if (bytesReceived > 0) {
            buffer[bytesReceived] = 0;
            std::cout << "ricevuto: " << buffer << std::endl;
        }
    }

    closesocket(client);
    closesocket(listenSock);
    WSACleanup();
    return 0;
}