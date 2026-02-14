## Le VPN (Virtual Private Network)

---

## 1. Definizione

Una **VPN (Virtual Private Network)** è un meccanismo che consente di creare un collegamento logico sicuro tra reti o host attraverso una rete pubblica (tipicamente Internet).

Una VPN utilizza:

* tunneling
* cifratura
* autenticazione
* controllo di integrità

Permette quindi di simulare una connessione privata sopra un’infrastruttura condivisa.

---

## 2. Cosa significa “private”

Il termine *private* non indica una rete fisicamente dedicata, ma che:

* il traffico è cifrato
* solo soggetti autenticati possono accedere
* il traffico è isolato logicamente dagli altri utenti della rete pubblica

La “privacy” è quindi ottenuta tramite meccanismi crittografici e controlli di accesso.

---

## 3. Meccanismi tecnici di una VPN

### 3.1 Tunneling

Il traffico originale viene incapsulato in un nuovo pacchetto IP.

Schema:

* pacchetto interno → incapsulamento → trasporto su Internet → decapsulazione

---

### 3.2 Cifratura

Algoritmi simmetrici (es. AES) proteggono i dati.
Lo scambio delle chiavi avviene tramite protocolli sicuri (es. IKE per IPsec, handshake TLS per SSL/TLS).

---

### 3.3 Autenticazione

Verifica l’identità delle parti.

Metodi comuni:

* certificati digitali
* chiavi pre-condivise
* autenticazione a due fattori

---

### 3.4 Integrità

Garantisce che i dati non siano stati modificati durante il trasporto.

Implementata tramite:

* HMAC (Hash-based Message Authentication Code, meccanismo crittografico che usa una funzione di hash insieme a una chiave segreta condivisa per garantire l’integrità e l’autenticità di un messaggio).  
* firme crittografiche

---

## 4. Tipologie di VPN per scenario

### 4.1 Remote Access VPN

Collega un singolo utente alla rete aziendale.

Tipicamente basata su:

* SSL/TLS
* IPsec

Usata per:

* smart working
* accesso di consulenti
* utenti mobili
* BYOD

---

### 4.2 Site-to-Site VPN

Collega due reti aziendali.

Tipicamente basata su:

* IPsec

Usata per:

* collegamento tra sedi
* filiali
* data center

---

## 5. Tecnologie principali

### 5.1 VPN IPsec-based

Caratteristiche:

* opera a livello 3
* modalità Tunnel e Transport
* componenti AH ed ESP
* cifratura, integrità e autenticazione integrate
* standard interoperabile

Casi d’uso:

* collegamenti permanenti tra reti
* site-to-site
* data center interconnessi

È la soluzione più comune per collegamenti stabili tra sedi.

---

### 5.2 VPN SSL/TLS-based

Caratteristiche:

* basata su TLS (come HTTPS)
* opera a livello applicativo o trasporto
* utilizza porta 443 (facile attraversamento firewall)
* accessibile via browser o client leggero
* supporta MFA

Casi d’uso:

* accesso remoto utenti
* smart working
* accessi temporanei

È ideale per utenti mobili e ambienti dinamici.

---

### 5.3 VPN BGP/MPLS-based

Caratteristiche:

* non è una VPN crittografica su Internet
* basata su rete privata dell’operatore
* segmentazione tramite label MPLS
* routing dinamico con BGP
* QoS e SLA garantiti

Casi d’uso:

* WAN aziendali multi-sede
* ambienti mission-critical
* integrazione voce/dati/video

La cifratura non è intrinseca: la sicurezza si basa sull’isolamento logico nel backbone del carrier.
Se necessario, si può aggiungere IPsec sopra MPLS.

---

## 6. Confronto sintetico

IPsec

* cifratura forte su Internet
* ideale per site-to-site

SSL/TLS

* flessibile per utenti
* semplice attraversamento firewall

BGP/MPLS

* rete privata operatore
* QoS elevato
* cifratura opzionale

---

## 7. La sola confidenzialità è sufficiente?

❌ No.

Una VPN sicura deve garantire:

1. Confidenzialità
2. Integrità
3. Autenticazione
4. Controllo degli accessi

La sola cifratura non impedisce:

* accessi non autorizzati
* alterazioni dei dati
* abuso delle risorse interne

---

## 8. Limiti di una VPN

Una VPN non protegge automaticamente contro:

* malware sul client
* errori di configurazione
* attacchi interni
* compromissione credenziali

Per questo viene integrata con:

* firewall
* segmentazione di rete
* autenticazione multifattore
* sistemi di monitoraggio

---

## 9. VPN vs rete privata fisica

Rete privata fisica:

* isolamento materiale
* costi elevati

VPN:

* isolamento logico
* costi inferiori
* dipendenza dalla crittografia

---

## Conclusione

Una VPN è un sistema logico-critttografico che crea un canale sicuro sopra una rete pubblica o condivisa.

Il concetto di “private” è garantito da:

* tunneling
* cifratura
* autenticazione
* integrità
* controllo degli accessi

La sicurezza reale deriva dall’integrazione coordinata di tutti questi elementi, non dalla sola cifratura.
