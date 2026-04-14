---

## Mappatura protocolli sui livelli ISO/OSI

| Livello | Nome livello      | Funzione principale                                              | Protocolli / Tecnologie tipiche            |
| ------- | ----------------- | ---------------------------------------------------------------- | ------------------------------------------ |
| 7       | Applicazione      | Servizi all’utente, logica applicativa, interazione con software | HTTP, HTTPS, FTP, SMTP, DNS, SNMP, SSH     |
| 6       | Presentazione     | Formattazione dati, cifratura, compressione                      | TLS, SSL                                   |
| 5       | Sessione          | Gestione sessioni, apertura/chiusura connessioni logiche         | NetBIOS, RPC                               |
| 4       | Trasporto         | Trasporto end-to-end, affidabilità, controllo flusso             | TCP, UDP                                   |
| 3       | Rete              | Instradamento, indirizzamento logico                             | IP, ICMP, IPsec                            |
| 2       | Collegamento dati | Trasmissione su rete locale, MAC, frame                          | Ethernet, Wi-Fi, ARP, VLAN 802.1Q          |
| 1       | Fisico            | Trasmissione bit su mezzo fisico                                 | Cavi Ethernet, fibra ottica, segnali radio |

---

## Osservazioni

### 1. Alcuni protocolli “non sono puri”

* non si collocano perfettamente in un solo livello
* **coprono più livelli**

Esempio:

* TLS è spesso associato al livello 6, ma viene percepito come “tra applicazione e trasporto”

---

### 2. Stack TCP/IP  


| ISO/OSI | TCP/IP equivalente |
| ------- | ------------------ |
| 7-6-5   | Applicazione       |
| 4       | Trasporto          |
| 3       | Internet           |
| 2-1     | Accesso rete       |

---

### 3. Esempio concreto completo

Navigazione web:

* HTTP → livello 7
* TLS → livello 6
* TCP → livello 4
* IP → livello 3
* Ethernet → livello 2

---

## Sintesi operativa (utile per verifiche)

* Livello 7 → protocolli applicativi (HTTP, DNS, SNMP)
* Livello 4 → TCP / UDP
* Livello 3 → IP e routing
* Livello 2 → Ethernet, VLAN, MAC
* Livello 1 → mezzo fisico

---

Di seguito una serie di esercizi progressivi sul modello ISO/OSI, adatti a studenti con livello base–intermedio.

---

# Esercizi – ISO/OSI e protocolli

## Esercizio 1 – Associazione protocollo → livello

Indicare il livello ISO/OSI corretto per ciascun protocollo:

1. HTTP
2. TCP
3. IP
4. Ethernet
5. DNS
6. UDP
7. TLS
8. SNMP

---

## Esercizio 2 – Associazione livello → funzione

Per ogni livello indicare la funzione principale:

* Livello 7 → ______
* Livello 4 → ______
* Livello 3 → ______
* Livello 2 → ______

---

## Esercizio 3 – Vero / Falso

Indicare se le affermazioni sono corrette:

1. SNMP lavora al livello trasporto
2. TCP garantisce affidabilità
3. IP si occupa dell’instradamento
4. Ethernet lavora al livello fisico
5. UDP è connection-oriented
6. TLS cifra i dati

---

## Esercizio 4 – Analisi scenario reale

Considerare la navigazione su un sito HTTPS.

Indicare:

* protocollo applicativo utilizzato
* protocollo di cifratura
* protocollo di trasporto
* protocollo di rete

---

## Esercizio 5 – Individuazione errori

Nel seguente elenco sono presenti errori. Correggere:

* HTTP → livello 4
* IP → livello 2
* TCP → livello 3
* Ethernet → livello 7

---

## Esercizio 6  

Spiegare brevemente SNMP e specificare il suo livello  

---

## Esercizio 7 – Classificazione avanzata

Classificare i seguenti protocolli indicando:

* livello ISO/OSI
* ruolo principale

Protocolli:

* ICMP
* ARP
* SSH
* FTP

---

## Esercizio 8 – Scenario reale

Un amministratore di rete:

* monitora router e switch
* riceve notifiche di errore
* consulta parametri di utilizzo CPU e banda

Domande:

1. Quale protocollo viene utilizzato?
2. A quale livello ISO/OSI appartiene?
3. Su quale protocollo di trasporto si basa?

---

## Esercizio 9 – Completamento

Completare la catena:

Applicazione → ______ → ______ → Rete → ______ → Fisico

---

## Esercizio 10 – Caso pratico

Un PC invia una richiesta DNS.

Indicare la sequenza dei protocolli coinvolti (dal livello 7 al livello 2).

---

# Soluzioni (per docente)

## Esercizio 1

1 → 7
2 → 4
3 → 3
4 → 2
5 → 7
6 → 4
7 → 6
8 → 7

---

## Esercizio 2

* 7 → servizi applicativi
* 4 → trasporto dati end-to-end
* 3 → instradamento
* 2 → trasmissione locale (frame/MAC)

---

## Esercizio 3

1 ❌
2 ✅
3 ✅
4 ❌
5 ❌
6 ✅

---

## Esercizio 4

* HTTP
* TLS
* TCP
* IP

---

## Esercizio 5

* HTTP → livello 7
* IP → livello 3
* TCP → livello 4
* Ethernet → livello 2

---

## Esercizio 6

Perché definisce la logica applicativa di gestione, mentre UDP è solo il mezzo di trasporto.

---

## Esercizio 7

* ICMP → livello 3 → diagnostica rete
* ARP → livello 2 → risoluzione IP/MAC
* SSH → livello 7 → accesso remoto sicuro
* FTP → livello 7 → trasferimento file

---

## Esercizio 8

1 → SNMP
2 → livello 7
3 → UDP

---

## Esercizio 9

Applicazione → Presentazione → Trasporto → Rete → Data Link → Fisico

---

## Esercizio 10

DNS → UDP → IP → Ethernet

---

