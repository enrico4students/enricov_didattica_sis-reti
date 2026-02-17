---

# PRIMA PARTE

## 1. Schema logico dell’infrastruttura esistente

### Analisi del testo

Dal testo si ricava:

* 2 reti fisicamente separate:

  * rete amministrativa (15 PC, 100 Mb/s)
  * rete didattica (laboratori + docenti, 100 Mb/s)
* 2 linee ADSL separate:

  * 7 Mb/s per amministrazione
  * 24 Mb/s per didattica
* nessuna comunicazione tra le due reti

### Schema logico attuale

Rete amministrativa:
PC → Switch 100 Mb → Router ADSL 7 Mb → Internet

Rete didattica:
PC laboratori → Switch 100 Mb → Router ADSL 24 Mb → Internet

Separazione:

* isolamento fisico
* nessun routing tra le due LAN

Motivazione:
la separazione è ottenuta tramite doppia infrastruttura indipendente.

---

## 2. Progetto di evoluzione dell’infrastruttura

### Procedimento seguito

1. Identificazione degli obiettivi (a–d)
2. Individuazione delle tecnologie adeguate
3. Proposta di architettura logica
4. Scelta degli apparati
5. Definizione dei meccanismi di sicurezza

---

## Ipotesi aggiuntive

* edificio cablato con dorsale centrale
* presenza di locale CED
* numero medio 25 PC per laboratorio
* disponibilità fibra ottica sul territorio

---

## a) Nuova connessione Internet unica

### Scelta tecnica

Sostituire le ADSL con:

Linea in fibra FTTH business simmetrica 1 Gbit/s

Motivazioni:

* banda molto superiore
* bassa latenza
* upload adeguato per servizi interni
* affidabilità maggiore rispetto ADSL

---

## Gestione linea di backup

Mantenere una ADSL come linea di backup.

Implementazione:

* firewall/router con doppia WAN
* configurazione failover automatico
* routing con priorità sulla fibra

Motivazione:
garantire continuità del servizio.

---

## Separazione del traffico

Non più separazione fisica, ma logica tramite:

VLAN:

* VLAN 10 → rete amministrativa
* VLAN 20 → rete didattica
* VLAN 30 → DMZ (server pubblici)

Implementazione:

* switch Layer 2/3 gestiti
* firewall centrale con policy tra VLAN

Motivazione:

* mantenere isolamento
* ridurre costi di cablaggio
* aumentare flessibilità

---

## b) Aumento banda LAN

Attuale: 100 Mb/s

Proposta:

* switch Gigabit (1 Gbit/s)
* dorsale interna a 10 Gbit/s (uplink tra switch principali)

Motivazione:
i laboratori multimediali richiedono maggiore throughput interno.

---

## c) Piattaforma multimediale interna

Proposta:

Server in DMZ con:

* Web server (Apache/Nginx)
* piattaforma e-learning (es. Moodle)
* server streaming (es. RTMP o WebRTC)

Accesso:

* interno: diretto via LAN
* esterno: tramite NAT e firewall

Motivazione:
collocazione in DMZ per proteggere rete interna.

---

## d) Sicurezza della rete

Strumenti:

1. Firewall perimetrale
2. IDS/IPS
3. VLAN e ACL
4. Autenticazione centralizzata (es. Active Directory o LDAP)
5. Backup periodici
6. Segmentazione DMZ

Motivazione:
protezione da minacce esterne e movimenti laterali interni.

---

## Schema logico proposto

Internet
|
Fibra 1 Gbit
|
Firewall con doppia WAN (fibra + ADSL backup)
|
Switch core L3
|---- VLAN 10 Amministrazione
|---- VLAN 20 Didattica
|---- VLAN 30 DMZ
|
Server Web / Streaming

---

## 3. Servizi principali da implementare

* DHCP centralizzato
* DNS interno
* Autenticazione centralizzata
* Web server
* Piattaforma e-learning
* Server file
* Proxy filtrante
* Backup automatico

---

### Esempio configurazione (DHCP per VLAN 20)

Configurazione logica:

Pool Didattica:

* rete: 192.168.20.0/24
* gateway: 192.168.20.1
* DNS: 192.168.30.10
* lease time: 8 ore

Motivazione:

* separazione indirizzamento
* gestione centralizzata
* semplificazione manutenzione

---

## 4. Continuità del servizio piattaforma multimediale

Misure:

* server con RAID
* backup giornaliero
* UPS
* replica su secondo server
* monitoraggio (Zabbix o simili)
* linea di backup Internet

Motivazione:
ridurre downtime e perdita dati.

---

# SECONDA PARTE

Si scelgono i quesiti 1 e 2.

---

# Quesito 1 – BYOD

## Hardware necessario

* Access Point Wi-Fi 6 gestiti
* Controller Wi-Fi centralizzato
* Switch PoE
* VLAN dedicata studenti
* Firewall con captive portal

---

## Limitazione accesso

Soluzioni:

* SSID separato per quinte
* Autenticazione 802.1X
* credenziali individuali
* filtraggio MAC opzionale
* firewall con policy dedicate

Motivazione:
controllo accessi e tracciabilità.

---

## Problemi possibili

1. Sovraccarico Wi-Fi
   → soluzione: AP distribuiti per aula

2. Sicurezza
   → VLAN isolata, accesso solo Internet

3. Distrazione studenti
   → filtro contenuti

4. Malware
   → rete isolata senza accesso LAN interna

---

# Quesito 2 – Sistema news

## Schema concettuale (ER)

Entità:

AUTORE

* id_autore
* nome
* ruolo

NEWS

* id_news
* titolo
* contenuto
* data_inserimento
* media_url
* id_autore (FK)

Relazione:
AUTORE 1 — N NEWS

Motivazione:
un autore può scrivere più news.

---

## Schema logico relazionale

AUTORE (id_autore PK, nome, ruolo)

NEWS (id_news PK, titolo, contenuto, data_inserimento, media_url, id_autore FK)

---

## Pagina Web visualizzazione (esempio PHP)

Estratto significativo:

```
<?php
$id = $_GET["id"];
$conn = new mysqli("localhost","user","pass","scuola");
$query = "SELECT titolo, contenuto, data_inserimento, media_url
          FROM NEWS WHERE id_news = $id";
$result = $conn->query($query);
$row = $result->fetch_assoc();
?>
<h1><?php echo $row["titolo"]; ?></h1>
<p><?php echo $row["contenuto"]; ?></p>
<p><?php echo $row["data_inserimento"]; ?></p>
```

Motivazione:

* semplicità
* separazione dati/presentazione
* uso database relazionale

---

# Quesito 3

Crittografia simmetrica e asimmetrica

## Struttura logica della risposta

1. Definizione rigorosa
2. Caratteristiche tecniche
3. Limiti
4. Impiego reale nei protocolli Internet

---

## 1. Crittografia simmetrica

### Definizione

Un’unica chiave segreta condivisa viene usata per cifrare e decifrare.

### Caratteristiche

* Elevata velocità
* Basso costo computazionale
* Adatta a grandi quantità di dati

### Limite principale

Problema della distribuzione sicura della chiave.

### Algoritmi tipici

AES, ChaCha20.

---

## 2. Crittografia asimmetrica

### Definizione

Uso di coppia di chiavi:

* pubblica
* privata

### Caratteristiche

* Risolve il problema dello scambio iniziale
* Permette firma digitale e autenticazione
* Più lenta della simmetrica

### Algoritmi tipici

RSA, ECC.

---

## 3. Impiego reale: modello ibrido (es. TLS)

### Procedimento

1. Il server invia certificato con chiave pubblica.
2. Il client verifica il certificato.
3. Viene generata chiave di sessione simmetrica.
4. La chiave di sessione viene protetta con crittografia asimmetrica.
5. Il traffico dati usa crittografia simmetrica.

---

## Schema grafico

Client
|
| --- richiesta HTTPS --->
|
Server
| --- certificato (chiave pubblica) --->
|
Client genera chiave di sessione
|
| --- chiave cifrata con chiave pubblica --->
|
Server decifra con chiave privata
|
Comunicazione cifrata simmetricamente

---

## Motivazione tecnica

* Asimmetrica → sicurezza nello scambio iniziale
* Simmetrica → efficienza nelle comunicazioni

Conclusione: i protocolli moderni usano modello combinato.

---

# Quesito 4

Scambio dati sicuro tra sedi e personale remoto

## Struttura logica

1. Esigenza: sicurezza su rete pubblica
2. Soluzione: tunnel cifrato
3. Analisi protocolli
4. Confronto tecnico

---

# 1. VPN

Definizione:
Creazione di tunnel cifrato su Internet.

Obiettivi:

* Riservatezza
* Integrità
* Autenticazione

---

# 2. VPN Site-to-Site

Uso:
Collegamento permanente tra due sedi.

Protocollo tipico:
IPsec (modalità tunnel)

Schema:

LAN Sede A
|
Gateway VPN A
| ===== Tunnel IPsec =====
Gateway VPN B
|
LAN Sede B

Caratteristiche:

* Trasparente agli utenti
* Sicurezza a livello rete (Layer 3)

---

# 3. VPN Remote Access

Uso:
Accesso singolo utente da remoto.

Schema:

PC remoto
|
Client VPN
| ===== Tunnel cifrato =====
Firewall/VPN Gateway
|
LAN aziendale

Protocolli:

* IPsec
* SSL/TLS VPN

---

# 4. IPsec

Opera a livello rete.

Modalità:

Transport → cifra payload
Tunnel → cifra intero pacchetto IP

Componenti:

* ESP (cifratura + integrità)
* AH (autenticazione)

---

# 5. SSL/TLS VPN

Opera sopra TCP.

Vantaggi:

* attraversa NAT/firewall facilmente
* configurazione più semplice per utenti mobili

---

# Confronto tecnico

IPsec:

* migliore per collegamenti tra sedi
* più complesso

SSL VPN:

* migliore per accesso remoto individuale
* maggiore flessibilità

---

# Conclusione ad alto livello

Per sedi multiple:
VPN site-to-site IPsec in modalità tunnel.

Per personale in trasferta:
VPN remote access con TLS e autenticazione forte (MFA).

Motivazione:
garantire riservatezza, integrità, autenticazione e continuità operativa su rete pubblica.



# Conclusione

Il progetto:

* unifica l’accesso Internet mantenendo isolamento tramite VLAN
* aumenta banda interna con Gigabit
* introduce DMZ per servizi pubblici
* implementa sicurezza multilivello
* garantisce continuità con backup e failover

Le scelte sono motivate da:

* scalabilità
* sicurezza
* affidabilità
* ottimizzazione costi
* aderenza a pratiche aziendali reali.
