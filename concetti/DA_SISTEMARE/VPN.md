---

# Le VPN (Virtual Private Network)

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

* HMAC (Hash-based Message Authentication Code)
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
* opera sopra TCP o UDP
* utilizza porta 443 (facile attraversamento firewall)
* richiede un client o accesso via browser
* supporta MFA

Casi d’uso:

* accesso remoto utenti
* smart working
* accessi temporanei
* dispositivi mobili su rete pubblica

È ideale per utenti mobili e ambienti dinamici.

---

### 5.2.1 OpenVPN

**OpenVPN** è una delle implementazioni più diffuse di VPN SSL/TLS-based.

Caratteristiche tecniche:

* utilizza TLS per autenticazione e scambio chiavi
* usa cifratura simmetrica per il traffico dati (es. AES)
* può operare su UDP (più performante) o TCP
* funziona in modalità client-to-server
* disponibile su Windows, Linux, macOS, Android

Architettura tipica:

Dispositivo (client OpenVPN)
⇄ Internet
⇄ Server OpenVPN

Ogni dispositivo stabilisce un tunnel cifrato verso il server.

È particolarmente adatta a:

* tablet e smartphone
* utenti con IP dinamico
* reti mobili (4G/5G)
* accessi temporanei

---

### Differenza e relazione tra OpenVPN e TLS

TLS (Transport Layer Security):

* è un protocollo crittografico
* protegge connessioni applicative (es. HTTPS)
* fornisce autenticazione, cifratura e integrità

OpenVPN:

* non è TLS
* utilizza TLS come meccanismo di sicurezza
* incapsula traffico IP dentro un canale protetto da TLS

In sintesi:

TLS = protocollo crittografico
OpenVPN = applicazione VPN che usa TLS

OpenVPN crea un **tunnel IP cifrato tramite TLS**, mentre TLS da solo protegge singole applicazioni (es. browser).

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

**La cifratura non è intrinseca: la sicurezza si basa sull’isolamento logico nel backbone del carrier**.  
Se necessario, si può aggiungere IPsec sopra MPLS.

---

## 6. Confronto sintetico

IPsec

* cifratura forte a livello IP
* ideale per site-to-site
* integrato nei router/firewall

SSL/TLS (es. OpenVPN)

* flessibile per utenti mobili
* funziona bene con IP dinamici
* attraversa facilmente NAT e firewall

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

IPsec è dominante nei collegamenti permanenti tra reti.
OpenVPN è una soluzione TLS-based ideale per accesso remoto e dispositivi mobili.

La sicurezza reale deriva dall’integrazione coordinata di tutti questi elementi, non dalla sola cifratura.
