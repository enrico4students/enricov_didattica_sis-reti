#include <iostream>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

int main() {
    

    /*
    La struttura WSADATA viene utilizzata dalla funzione WSAStartup per fornire informazioni
    sulla versione della libreria Winsock che è stata inizializzata.

    Definizione (semplificata) di WSADATA (dalla documentazione ufficiale di Microsoft):
    
    typedef struct WSAData {
        WORD           wVersion;        // versione richiesta (es. 2.2)
        WORD           wHighVersion;    // versione massima supportata
        char           szDescription[WSADESCRIPTION_LEN+1]; // descrizione della DLL Winsock
        char           szSystemStatus[WSASYSSTATUS_LEN+1];  // stato del sistema Winsock
        unsigned short iMaxSockets;     // numero massimo di socket supportati (non più utilizzato)
        unsigned short iMaxUdpDg;       // dimensione massima datagram UDP (non più utilizzato)
        char FAR*      lpVendorInfo;    // informazioni aggiuntive (non usata di solito)
    } WSADATA;

    In pratica:
    ✅ Si dichiara una variabile di tipo WSADATA, ad esempio:
       WSADATA wsaData;

    ✅ Si passa un puntatore a questa variabile alla funzione WSAStartup:
       WSAStartup(MAKEWORD(2, 2), &wsaData);

    ✅ Questo inizializza la libreria Winsock per poter usare socket su Windows.

    ⚠️ Se WSAStartup non viene chiamata, l'uso dei socket (socket(), bind(), send(), ecc.) fallisce.

    🧪 In questi programmi, viene sempre invocato:
       WSAStartup(MAKEWORD(2, 2), &wsaData);
    per inizializzare la versione 2.2 della libreria Winsock.
    */
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);



    /*
    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, 0);

    ✅ Questa istruzione crea un **socket**, cioè un "endpoint" di comunicazione.

    ▸ SOCKET è un tipo definito da Winsock (typedef UINT_PTR SOCKET): rappresenta un descrittore di socket.

    ▸ La funzione `socket()` restituisce un valore di tipo SOCKET e prende tre parametri fondamentali:

        1. AF_INET
           ➤ Specifica il tipo di indirizzo: AF_INET indica IPv4.
           ➤ Significa che il socket userà indirizzi del tipo 192.168.x.x.

        2. SOCK_STREAM
           ➤ Specifica il tipo di comunicazione.
           ➤ SOCK_STREAM indica un socket orientato alla connessione, cioè TCP.
           ➤ Se si usasse SOCK_DGRAM sarebbe un socket UDP (senza connessione).

        3. 0
           ➤ Protocollo specifico da usare.
           ➤ 0 indica che si vuole il **protocollo predefinito** per il tipo scelto (TCP per SOCK_STREAM).
           ➤ Si potrebbe anche scrivere IPPROTO_TCP, ma 0 è equivalente e più generico.

    ✅ Quindi, questa istruzione:
       ➤ Crea un socket IPv4, basato su TCP, con protocollo automatico.
       ➤ Se ha successo, restituisce un valore valido (≠ INVALID_SOCKET).
       ➤ In caso di errore restituisce INVALID_SOCKET.

    ❗ Nota:
       ➤ Dopo la creazione, il socket deve essere legato a un indirizzo IP e porta (con bind())
         e messo in ascolto (con listen()) per ricevere connessioni.
    */
    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, 0);




    /*
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(12345);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    ✅ Questo blocco di codice configura un indirizzo IP e una porta
       su cui il socket deve essere associato (bind) per ricevere connessioni o pacchetti.

/*
    Definizione della struttura sockaddr_in
    ----------------------------------------

    La struttura `sockaddr_in` è usata per rappresentare un indirizzo di socket IPv4.
    Serve a specificare indirizzo IP e numero di porta, ed è utilizzata con funzioni
    come `bind()`, `connect()`, `sendto()`, `recvfrom()`.

    Definizione semplificata (presa da <winsock2.h>):

    struct sockaddr_in {
        short          sin_family;   // Tipo di indirizzo (es: AF_INET per IPv4)
        unsigned short sin_port;     // Numero di porta (in network byte order)
        struct in_addr sin_addr;     // Indirizzo IP (IPv4)
        char           sin_zero[8];  // Padding (non usato, serve a mantenere stessa dimensione di sockaddr)
    };

    Dettagli campo per campo:

    ▸ sin_family
       ➤ Deve essere impostato a AF_INET per indicare indirizzi IPv4.

    ▸ sin_port
       ➤ Numero di porta TCP o UDP da associare.
       ➤ Deve essere convertito in network byte order con htons().

    ▸ sin_addr
       ➤ È una struttura `in_addr` che contiene l'indirizzo IPv4.
         La sua rappresentazione più usata è:
         sin_addr.s_addr = inet_addr("127.0.0.1");  oppure INADDR_ANY

    ▸ sin_zero
       ➤ Array di 8 caratteri usato solo per allineamento strutturale.
       ➤ Non deve essere modificato; solitamente viene azzerato con memset().

    ✅ Nota:
       `sockaddr_in` è una specializzazione di `sockaddr` per IPv4.
       Le funzioni socket generalmente accettano `sockaddr*`, quindi si fa il cast:
       (sockaddr*)&serverAddr

    1. serverAddr.sin_family = AF_INET;
       ➤ Indica che si sta usando un indirizzo IPv4.
       ➤ Deve sempre essere impostato a AF_INET per i socket IPv4.

    2. serverAddr.sin_port = htons(12345);
       ➤ Specifica il numero di porta (in questo caso 12345) su cui il server "ascolta".
       ➤ La funzione htons() (host to network short) converte l’intero da formato host (little endian)
         a formato di rete (big endian), come richiesto dai protocolli di rete.

    3. serverAddr.sin_addr.s_addr = INADDR_ANY;
       ➤ Specifica l’indirizzo IP su cui il socket sarà in ascolto.
       ➤ INADDR_ANY significa: *accetta connessioni da qualunque interfaccia di rete locale*.
         - Ad esempio: rete Wi-Fi, Ethernet, localhost (127.0.0.1), ecc.
         - Il socket sarà visibile su tutte le schede di rete disponibili sul sistema.

    ✅ In sintesi:
       ➤ Si configura un socket che ascolta su tutte le interfacce,
         sulla porta TCP 12345, utilizzando indirizzamento IPv4.
*/
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(12345);
    serverAddr.sin_addr.s_addr = INADDR_ANY;


    /*
    bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));

    ✅ La funzione `bind()` associa un socket a un indirizzo IP locale e a una porta specifica.
       Questo è un passaggio necessario per i socket che devono *ricevere* dati
       (es. server TCP o ricevente UDP).

    ▸ Parametri:

        1. serverSocket
           ➤ È il descrittore del socket precedentemente creato con `socket()`.
           ➤ Deve essere valido e già inizializzato.

        2. (sockaddr*)&serverAddr
           ➤ È un cast esplicito: `serverAddr` è di tipo `sockaddr_in`, ma `bind()`
             richiede un puntatore a `sockaddr`, che è la struttura generica per indirizzi.
           ➤ Il cast serve per compatibilità tra i due tipi.

        3. sizeof(serverAddr)
           ➤ Dimensione della struttura `serverAddr` in byte.
           ➤ Specifica quanti byte di dati rappresentano l’indirizzo.

    ✅ Esempio pratico:
       Se `serverAddr` è stato configurato per:
         ▸ sin_family = AF_INET
         ▸ sin_port = htons(12345)
         ▸ sin_addr.s_addr = INADDR_ANY
       allora il socket verrà associato a *tutti gli indirizzi IP* locali,
       sulla *porta 12345*.

    ❗ Se `bind()` fallisce (restituisce SOCKET_ERROR), il socket **non può essere usato per ricevere**.
       ➤ È buona pratica controllare il valore restituito e usare `WSAGetLastError()` in caso di errore.

    📌 Nota:
       - Nei programmi TCP, `bind()` viene seguito da `listen()`.
       - Nei programmi UDP riceventi, `bind()` è sufficiente per ricevere datagrammi.

    */
    bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));



    /*
    listen(serverSocket, SOMAXCONN);

    ✅ La funzione `listen()` mette il socket TCP in modalità "ascolto", cioè lo prepara ad accettare
       connessioni in ingresso tramite la funzione `accept()`.

    ▸ Parametri:

        1. serverSocket
           ➤ È il descrittore del socket precedentemente creato e associato a un indirizzo/porta con `bind()`.

        2. SOMAXCONN
           ➤ È una costante che definisce il numero massimo di connessioni pendenti che il sistema
             può accodare nella "listen queue" (coda delle connessioni in attesa).
           ➤ Il valore esatto dipende dal sistema operativo (es. su Windows di solito è  SOMAXCONN = 5 o più).
           ➤ Usare `SOMAXCONN` consente di lasciare al sistema la scelta del valore massimo permesso.

    ✅ In pratica:
       - Il socket TCP viene configurato per diventare un "server socket".
       - Dopo `listen()`, il programma può chiamare `accept()` per gestire le richieste di connessione in arrivo.

    ❗ Se `listen()` fallisce (restituisce SOCKET_ERROR), non sarà possibile accettare connessioni.
       ➤ È buona pratica controllare il valore restituito e chiamare `WSAGetLastError()` in caso di errore.

    ⚠️ Importante:
       - `listen()` si applica **solo a socket TCP (SOCK_STREAM)**.
       - Non va usato per socket UDP (SOCK_DGRAM), perché non sono basati su connessioni.
    */
    listen(serverSocket, SOMAXCONN);



    /*
    SOCKET clientSocket = accept(serverSocket, (sockaddr*)&clientAddr, &clientSize);

    ✅ La funzione `accept()` serve a **completare** una connessione in ingresso su un socket TCP
       che è stato precedentemente messo in ascolto con `listen()`.

    ▸ Parametri:

        1. serverSocket
           ➤ È il socket "server", creato con `socket()`, configurato con `bind()` e abilitato con `listen()`.
           ➤ Deve essere un socket di tipo SOCK_STREAM (TCP).

        2. (sockaddr*)&clientAddr
           ➤ Puntatore a una struttura `sockaddr` (cast da `sockaddr_in`) dove verranno salvate
             le informazioni sull’host remoto (IP e porta del client che si connette).
           ➤ Se non interessano queste informazioni, si può passare `nullptr`.

        3. &clientSize
           ➤ Puntatore a un intero che inizialmente contiene la dimensione della struttura `clientAddr`.
           ➤ Al ritorno, conterrà il numero effettivo di byte usati.

    ✅ Comportamento:
       - La chiamata si blocca finché non arriva una richiesta di connessione.
       - Quando una connessione viene accettata, viene restituito un nuovo `SOCKET`:
         ➤ Questo nuovo socket (`clientSocket`) rappresenta **la connessione attiva** con il client.
         ➤ Si usa per `recv()` e `send()`.
       - Il socket `serverSocket` invece resta in ascolto per altre connessioni.

    ❗ Se `accept()` fallisce, restituisce `INVALID_SOCKET`.
       ➤ È buona pratica verificare l'output e usare `WSAGetLastError()` in caso di errore.

    ✅ In sintesi:
       - `accept()` crea un nuovo socket per ogni client connesso.
       - Permette al server di gestire **più client**, ognuno con il proprio socket di comunicazione.
    */

    sockaddr_in clientAddr;
    int clientSize = sizeof(clientAddr);
    SOCKET clientSocket = accept(serverSocket, (sockaddr*)&clientAddr, &clientSize);

    char buffer[1024];

    while (true) {
        int bytesReceived = recv(clientSocket, buffer, sizeof(buffer) - 1, 0);
        if (bytesReceived > 0) {
            buffer[bytesReceived] = '\0';
            std::cout << "TCP ricevuto: " << buffer << std::endl;
        }
    }

    closesocket(clientSocket);
    closesocket(serverSocket);
    WSACleanup();
    return 0;
}