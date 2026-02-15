
## 1. Relazione tra HTTPS e TLS

HTTPS non è un protocollo distinto da HTTP: è **HTTP eseguito sopra TLS**.

Struttura reale di una connessione HTTPS:

```
Applicazione:     HTTP
Sicurezza:        TLS
Trasporto:        TCP
Rete:             IP
```

Quindi:

* HTTP definisce richieste e risposte (GET, POST, header, body).
* TLS fornisce cifratura, autenticazione e integrità.
* TCP trasporta i segmenti.
* IP instrada i pacchetti.

HTTPS = HTTP dentro(sopra) TLS dentro(sopra) TCP.

---

## 2. Struttura interna di TLS

TLS non è un blocco unico: è composto da sottoprotocolli logici.

I due principali sono:

1. Handshake Protocol
2. Record Protocol

Esistono anche Alert Protocol e ChangeCipherSpec (nelle versioni precedenti a TLS 1.3), ma qui si considerano i due fondamentali per comprendere HTTPS.

---

## 3. Posizionamento del Record Protocol

Il **Record Protocol** è lo strato base di TLS.

Tutto ciò che passa in TLS viene incapsulato in record TLS.

Funzioni del Record Protocol:

* frammentare i dati
* applicare MAC o AEAD per integrità
* cifrare i dati
* aggiungere header TLS
* inviare il risultato su TCP

Importante:

Anche i messaggi di handshake viaggiano dentro record TLS.

Quindi la gerarchia reale è:

```
HTTP
    ↓
TLS Handshake messages
    ↓
TLS Record Protocol
    ↓
TCP
```

Il Record Protocol è il “contenitore sicuro” universale.

---

## 4. Posizionamento dell’Handshake Protocol

L’Handshake Protocol è un protocollo logico che **serve solo all’inizio** della connessione TLS.

Serve a:

* negoziare versione TLS
* scegliere suite crittografica
* autenticare il server (certificato X.509)
* generare chiavi simmetriche di sessione

Una volta completato l’handshake, non viene più usato (salvo renegotiation nelle vecchie versioni).

---

## 5. Sequenza completa di una connessione HTTPS

### Fase 1 – TCP

```
Client  →  Server  :  SYN
Server  →  Client  :  SYN-ACK
Client  →  Server  :  ACK
```

Connessione TCP stabilita.

---

### Fase 2 – TLS Handshake (incapsulato nel Record Protocol)

Ogni messaggio sotto è trasportato dentro un TLS Record.

Sequenza tipica (TLS 1.2 semplificato):

```
Client  →  Server  :  ClientHello
Server  →  Client  :  ServerHello
Server  →  Client  :  Certificate
Server  →  Client  :  ServerKeyExchange (se necessario)
Server  →  Client  :  ServerHelloDone

Client  →  Server  :  ClientKeyExchange
Client  →  Server  :  ChangeCipherSpec
Client  →  Server  :  Finished

Server  →  Client  :  ChangeCipherSpec
Server  →  Client  :  Finished
```

Cosa succede logicamente:

1. Il client propone algoritmi e parametri.
2. Il server sceglie la suite crittografica.
3. Il server invia il certificato.
4. Viene generato un segreto condiviso (es. ECDHE).
5. Entrambe le parti derivano le chiavi simmetriche.
6. Da questo punto la comunicazione è cifrata.

Tutti questi messaggi sono trasportati dal Record Protocol.

---

### Fase 3 – Trasmissione HTTP cifrata

Ora il client invia:

```
HTTP GET /index.html
```

Ma in realtà ciò che viaggia su TCP è:

```
TLS Record {
    dati HTTP cifrati
}
```

Il server risponde allo stesso modo:

```
TLS Record {
    risposta HTTP cifrata
}
```

HTTP non è consapevole della cifratura.
TLS non interpreta il contenuto HTTP.

---

## 6. Relazione precisa tra Handshake e Record

Schema gerarchico reale:

```
TLS
├── Record Protocol  ← livello base
│       ├── Handshake messages
│       ├── Application Data (HTTP)
│       └── Alert messages
│
└── (logica di gestione chiavi e stato)
```

Quindi:

* L’Handshake Protocol è un tipo di messaggio TLS.
* Il Record Protocol è il meccanismo che trasporta e protegge quei messaggi.
* Dopo l’handshake, i record TLS trasportano dati applicativi (HTTP).

---

## 7. Sintesi concettuale finale

HTTPS = HTTP protetto da TLS.

TLS è composto da:

* Handshake Protocol → stabilisce sicurezza
* Record Protocol → applica sicurezza e trasporta dati

Sequenza logica:

```
TCP stabilito
    ↓
TLS Handshake (dentro record TLS)
    ↓
Chiavi di sessione stabilite
    ↓
HTTP cifrato (dentro record TLS)
```

L’errore comune è pensare che l’handshake sia “fuori” dal record protocol.
In realtà l’handshake è un contenuto trasportato dal record protocol.

---

Sono dette essere interessanti anche le differenze strutturali introdotte da TLS 1.3 rispetto a TLS 1.2, al momento le ignoriamo
