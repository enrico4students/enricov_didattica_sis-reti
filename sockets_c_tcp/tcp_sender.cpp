#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <string>
#include <thread>
#include <chrono>
#include <cstdlib>
#pragma comment(lib, "ws2_32.lib")

std::string generate_random_string(size_t length = 10) {
    const char charset[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    std::string result;
    result.resize(length);
    for (size_t i = 0; i < length; i++) {
        result[i] = charset[rand() % (sizeof(charset) - 1)];
    }
    return result;
}

int main() {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(54000);
    inet_pton(AF_INET, "127.0.0.1", &server.sin_addr);
    connect(sock, (sockaddr*)&server, sizeof(server));

    while (true) {
        std::string message = generate_random_string();
        std::cout << "TCP mando: " << message << std::endl;
        send(sock, message.c_str(), message.length(), 0);
        std::this_thread::sleep_for(std::chrono::seconds(4));
    }

    closesocket(sock);
    WSACleanup();
    return 0;
}