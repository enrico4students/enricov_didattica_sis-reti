Socket TCP/UDP – Progetto Didattico in C++

Questo progetto contiene quattro programmi C++ sviluppati per ambiente Windows e GCC (MSYS2):

- TCP Sender: invia ogni 4 secondi una stringa casuale al ricevente via socket TCP.
- TCP Receiver: riceve e stampa le stringhe TCP ricevute.
- UDP Sender: invia ogni 4 secondi una stringa casuale via UDP.
- UDP Receiver: riceve e stampa le stringhe UDP.

Struttura del progetto:
socket_programs_vscode/  
├── .vscode/  
│   ├── launch.json  
│   └── tasks.json  
├── tcp/  
│   ├── tcp_sender.cpp  
│   ├── tcp_receiver.cpp  
│   ├── run_tcp_sender.bat  
│   └── run_tcp_receiver.bat  
├── udp/  
│   ├── udp_sender.cpp  
│   ├── udp_receiver.cpp  
│   ├── run_udp_sender.bat  
│   └── run_udp_receiver.bat  
├── Makefile  
├── README.txt  
└── check_env.py  

Requisiti:
- Windows con MSYS2 o MinGW installato
- g++ accessibile da terminale (verificare con: gcc --version)
- Libreria ws2_32 disponibile
- Visual Studio Code (consigliato)

Compilazione:
Con Makefile:
    make all

Con VS Code:
    CTRL+SHIFT+B per usare i task definiti in .vscode/tasks.json

Esecuzione:
    cd tcp
    g++ tcp_receiver.cpp -o tcp_receiver.exe -lws2_32
    ./tcp_receiver.exe

Aprire un nuovo terminale per tcp_sender.exe e fare lo stesso per i programmi UDP.

Controllo ambiente:
    python check_env.py