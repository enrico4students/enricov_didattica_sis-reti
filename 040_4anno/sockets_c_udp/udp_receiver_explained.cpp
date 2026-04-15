#include <iostream>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

int main() {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    SOCKET sock = socket(AF_INET, SOCK_DGRAM, 0);

    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(12346);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    bind(sock, (sockaddr*)&serverAddr, sizeof(serverAddr));

    char buffer[1024];
    sockaddr_in clientAddr;
    int clientLen = sizeof(clientAddr);

    while (true) {
        int bytesReceived = recvfrom(sock, buffer, sizeof(buffer) - 1, 0,
                                     (sockaddr*)&clientAddr, &clientLen);
        if (bytesReceived > 0) {
            buffer[bytesReceived] = '\0';
            std::cout << "UDP ricevuto: " << buffer << std::endl;
        }
    }

    closesocket(sock);
    WSACleanup();
    return 0;
}