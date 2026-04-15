AVVIO RAPIDO – Progetto Socket TCP/UDP

1. PREREQUISITI
   - Sistema operativo: Windows
   - Compilatore: g++ (MSYS2 o MinGW)
   - Verifica: eseguire da terminale il comando:
       g++ --version
   - Visual Studio Code installato (facoltativo ma consigliato)

2. COMPILAZIONE VELOCE

   TCP:
     - Aprire terminale in socket_programs_vscode/tcp
     - Compilare e avviare:
         g++ tcp_receiver.cpp -o tcp_receiver.exe -lws2_32
         tcp_receiver.exe
     - Aprire un secondo terminale:
         g++ tcp_sender.cpp -o tcp_sender.exe -lws2_32
         tcp_sender.exe

   UDP:
     - Stessa procedura in socket_programs_vscode/udp:
         g++ udp_receiver.cpp -o udp_receiver.exe -lws2_32
         udp_receiver.exe
     - Nuovo terminale:
         g++ udp_sender.cpp -o udp_sender.exe -lws2_32
         udp_sender.exe

3. UTILIZZO CON VISUAL STUDIO CODE

   - Aprire la cartella `socket_programs_vscode` in VS Code
   - Premere CTRL+SHIFT+B per compilare
   - Premere F5 per eseguire i target `receiver`
   - È possibile eseguire anche i file .bat per test rapido

4. VERIFICA CONFIGURAZIONE
   - Eseguire:
       python check_env.py

5. USCITA DAI PROGRAMMI
   - Premere CTRL+C nei terminali aperti