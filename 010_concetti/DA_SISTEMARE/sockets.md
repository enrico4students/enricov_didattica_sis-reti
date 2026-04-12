## Numeri di porta e socket nel modello TCP/IP

### 1. Introduzione

Nella comunicazione di rete basata sul modello TCP/IP, i programmi applicativi non comunicano direttamente tra loro tramite indirizzi IP soltanto.
Per permettere a più applicazioni di usare la rete contemporaneamente, il sistema utilizza **numeri di porta** e **socket**.

Comprendere chiaramente questi due concetti è essenziale per capire come funzionano servizi come HTTP, DNS o SSH.

---

## 2. Numeri di porta

Un **numero di porta** identifica un servizio o un punto di accesso al livello di trasporto su un host.

In altre parole, la porta indica **a quale applicazione devono essere consegnati i dati ricevuti dalla rete**.

Esempio:

IP server:

```
203.0.113.10
```

servizi attivi:

| servizio | protocollo | porta |
| -------- | ---------- | ----- |
| HTTP     | TCP        | 80    |
| HTTPS    | TCP        | 443   |
| DNS      | UDP        | 53    |
| SSH      | TCP        | 22    |

Quando arriva un pacchetto TCP destinato alla porta 80, il sistema operativo lo consegna al **server HTTP**.

---

## 3. Le porte sono locali al protocollo

Un punto molto importante è che **i numeri di porta non sono globali**, ma **sono locali al protocollo di trasporto**.

Esistono quindi spazi di numerazione separati per:

TCP
UDP

Questo significa che lo **stesso numero di porta può essere usato contemporaneamente da protocolli diversi**.

Esempio reale: DNS

porta:

```
53 / UDP
53 / TCP
```

UDP è usato per la maggior parte delle query DNS.
TCP è usato per risposte molto grandi o trasferimenti di zona.

---

## 4. Cos'è un socket

Un **socket** è un **endpoint di comunicazione di rete**.

È una struttura software creata dal sistema operativo che consente a un processo di:

* inviare dati sulla rete
* ricevere dati dalla rete

Dal punto di vista concettuale, un socket rappresenta:

(IP locale, protocollo, porta)

Esempio:

```
TCP
203.0.113.10
porta 80
```

Questo è l’endpoint TCP che rappresenta il servizio HTTP su quel server.

---

## 5. Socket di ascolto

Un server crea inizialmente uno **socket di ascolto**.

Nel caso di un server HTTP:

porta:

```
TCP 80
```

operazioni tipiche:

```
socket()
bind(80)
listen()
```

Questo socket:

* resta nello stato **LISTEN**
* serve solo per **ricevere richieste di connessione**
* non viene usato per scambiare dati HTTP.

---

## 6. Arrivo di un client

Quando un client (browser) vuole collegarsi al server HTTP, apre una connessione TCP verso:

```
server_IP : porta 80
```

Dopo il three-way handshake TCP, il server può accettare la connessione.

Il server esegue:

```
accept()
```

---

## 7. Creazione di un nuovo socket

Quando il server chiama `accept()`, il sistema operativo:

* estrae la connessione dalla coda
* **crea un nuovo socket**

A questo punto esistono due socket nel server.

### socket di ascolto

porta:

```
TCP 80
```

stato:

```
LISTEN
```

serve per accettare nuove connessioni.

---

### socket della connessione

associato al client:

```
TCP
server_IP:80 ↔ client_IP:porta_client
```

stato:

```
ESTABLISHED
```

Questo socket è usato per la comunicazione HTTP.

---

## 8. Comunicazione HTTP

La richiesta HTTP avviene sul nuovo socket.

Esempio:

client invia:

```
GET /index.html HTTP/1.1
```

server risponde:

```
HTTP/1.1 200 OK
```

Quando la comunicazione termina, il socket della connessione viene chiuso.

---

## 9. Un processo può avere più socket?

Sì.

Un singolo processo può avere **molti socket contemporaneamente**.

Un server HTTP reale può avere:

* uno **socket di ascolto**
* molti **socket di connessione**, uno per ogni client.

Esempio con tre client connessi:

socket:

```
LISTEN → porta 80
```

socket connessione:

```
client A
```

socket connessione:

```
client B
```

socket connessione:

```
client C
```

Ogni client comunica con il server tramite **il proprio socket dedicato**.

---

## 10. Riassunto

Numero di porta

* identifica un servizio su un host
* è locale al protocollo di trasporto
* TCP e UDP hanno spazi di porte separati.

Socket

* endpoint di comunicazione di rete
* oggetto software creato dal sistema operativo
* usato dai processi per comunicare.

Server HTTP

* crea uno socket di ascolto sulla porta 80
* quando arriva un client chiama `accept()`
* viene creato un nuovo socket per quella connessione.

Un processo può avere molti socket contemporaneamente, uno per ogni connessione attiva.

