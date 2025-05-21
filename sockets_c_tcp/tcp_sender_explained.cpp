#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

std::string generaStringaCasuale(int lunghezza) {
    std::string risultato;
    for (int i = 0; i < lunghezza; ++i) {
        char carattere = static_cast<char>(33 + rand() % 94);
        risultato += carattere;
    }
    return risultato;
}

int main() {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(12345);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    connect(sock, (sockaddr*)&server, sizeof(server));

    srand(static_cast<unsigned>(time(nullptr)));

    while (true) {
        std::string messaggio = generaStringaCasuale(10);
        std::cout << "TCP mando: " << messaggio << std::endl;
        send(sock, messaggio.c_str(), messaggio.size(), 0);
        std::this_thread::sleep_for(std::chrono::seconds(4));
    }

    closesocket(sock);
    WSACleanup();
    return 0;
}