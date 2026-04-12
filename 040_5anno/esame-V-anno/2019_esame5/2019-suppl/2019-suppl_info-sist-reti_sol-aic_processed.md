---
# Sistemi e Reti - Suppletiva 2019

# PRIMA PARTE

## Analisi iniziale del problema

La ditta InfoService vuole sviluppare un **sistema di ticketing web** per:

* apertura ticket da parte del cliente
* assegnazione del ticket a un tecnico
* compilazione report da parte del tecnico
* convalida finale da parte del cliente

Il sistema deve garantire:

* accesso autenticato
* sicurezza dei dati
* tracciabilità degli interventi
* gestione remota e in sede

Faccio le seguenti **ipotesi aggiuntive coerenti con una realtà aziendale media (50 dipendenti)**:

* esiste una sede centrale con server locali
* il portale è web-based
* i tecnici usano notebook o tablet aziendali
* i clienti accedono via Internet

---

# 1) PROGETTO DELL’INFRASTRUTTURA

## 1.a Infrastruttura hardware e software

### Architettura generale

Propongo un’architettura a 3 livelli:

* Front-end (web server)
* Application server
* Database server

Questo modello è scelto perché:

* separa i ruoli
* migliora sicurezza
* consente scalabilità

---

### Risorse hardware

* Firewall perimetrale
* Router verso ISP
* Switch gestiti (VLAN)
* Server rack:

  * 1 Web Server
  * 1 Application Server
  * 1 Database Server
* NAS per backup
* Access Point WiFi aziendali
* Notebook aziendali per tecnici

Scarto l’idea di un unico server che fa tutto perché:

* riduce sicurezza  
* crea **single point of failure**  
* meno scalabile  

---

### Servizi software

Sistema operativo server:

* Linux Server (es. Ubuntu Server)

Servizi:

* Web server (Apache o Nginx)
* Application development (PHP, Java Spring o Node) # EV spiegare tipologia
* DBMS (MySQL / PostgreSQL)
* Server SMTP per notifiche email
* Sistema di backup automatico
* Sistema di logging centralizzato

---

## Schema logico dell’infrastruttura

Cliente → Internet → Firewall → DMZ → Web Server → Application Server → Database Server (LAN interna)

La DMZ (Demilitarized Zone) è una rete isolata dove si collocano i server esposti a Internet per limitare eventuali compromissioni.

---

## 1.b Misure di sicurezza

### Sicurezza perimetrale

* Firewall con regole ACL
* NAT
* IDS/IPS

IDS (Intrusion Detection System) rileva attacchi.  
IPS (Intrusion Prevention System) li blocca automaticamente.

---

### Sicurezza applicativa

* HTTPS con TLS
* Autenticazione con password cifrate (hash con salt)
* Gestione sessioni sicure
* Controllo ruoli (cliente, tecnico, dirigente)

Scarto HTTP semplice perché trasmette dati in chiaro.

---

### Sicurezza database

* Accesso consentito solo dall’application server
* Backup giornalieri
* Replica secondaria per continuità

---

## 1.c Compilazione online del report

### Connessione sede centrale

Propongo:

* Fibra FTTH o FTTC business
* IP pubblico statico
* Firewall professionale

Motivo: necessaria affidabilità e banda garantita.

---

### Connessione tecnici in trasferta

* Notebook con SIM dati 4G/5G
* Oppure hotspot mobile

Connessione tramite:

* VPN aziendale (IPsec o SSL VPN)

VPN (Virtual Private Network) crea un tunnel cifrato tra dispositivo remoto e rete aziendale.

Scarto accesso diretto al server senza VPN perché meno sicuro.

---

### Sicurezza comunicazione tecnico ↔ sistema centrale

* HTTPS
* Autenticazione forte
* VPN
* Certificati digitali

---

### Convalida del report da parte del cliente

Procedura:

1. Il tecnico chiude ticket.
2. Il sistema invia email al cliente.
3. Il cliente accede al portale.
4. Visualizza report.
5. Conferma e inserisce commento.

La convalida è registrata nel database con timestamp.

---

# 2) PROGETTO DELLA BASE DI DATI

## Modellazione concettuale (E-R)

Entità principali:

* CLIENTE
* TICKET
* TECNICO
* REPORT
* COMMENTO

Relazioni:

* Cliente apre Ticket (1:N)
* Ticket assegnato a Tecnico (N:1)
* Ticket genera Report (1:N)
* Cliente scrive Commento su Report (1:1 opzionale)

---

## Modello logico (relazionale)

CLIENTE(
id_cliente PK,
ragione_sociale,
email,
password_hash
)

TECNICO(
id_tecnico PK,
nome,
cognome,
ruolo
)

TICKET(
id_ticket PK,
id_cliente FK,
id_tecnico FK,
data_apertura,
stato
)

REPORT(
id_report PK,
id_ticket FK,
descrizione_intervento,
tempo_impiegato,
data_chiusura
)

COMMENTO(
id_commento PK,
id_report FK,
testo,
data_commento
)

---

# 3) QUERY SQL

## 3.1 Elenco ticket aperti

```
SELECT c.ragione_sociale,
       t.data_apertura,
       te.nome,
       te.cognome
FROM TICKET t
JOIN CLIENTE c ON t.id_cliente = c.id_cliente
JOIN TECNICO te ON t.id_tecnico = te.id_tecnico
WHERE t.stato = 'APERTO';
```

Uso JOIN per collegare le tabelle tramite chiavi esterne.

---

## 3.2 Tempo medio di chiusura in un intervallo

```
SELECT AVG(DATEDIFF(r.data_chiusura, t.data_apertura)) AS tempo_medio
FROM TICKET t
JOIN REPORT r ON t.id_ticket = r.id_ticket
WHERE r.data_chiusura BETWEEN '2023-01-01' AND '2023-12-31';
```

DATEDIFF calcola differenza in giorni.

Scarto il calcolo manuale perché SQL fornisce già funzioni aggregate.

---

# SECONDA PARTE

Scelgo Quesito I e II.

---

# QUESITO I – Monitoraggio dirigenti

## Modifica database

Aggiungo tabella:

DIRIGENTE(
id_dirigente PK,
nome,
cognome,
email,
password_hash
)

Oppure soluzione migliore: campo ruolo nella tabella UTENTE.

Scelgo tabella UTENTE unica con campo ruolo perché:

* più scalabile
* evita duplicazioni

---

## Architettura pagine

* login.php
* dashboard_dirigente.php
* statistiche.php

Accesso consentito solo se:

```
if($_SESSION['ruolo'] != 'DIRIGENTE') {
    exit("Accesso negato");
}
```

---

## Esempio pagina PHP per statistiche

```
$query = "SELECT AVG(DATEDIFF(r.data_chiusura, t.data_apertura)) AS tempo_medio
          FROM TICKET t
          JOIN REPORT r ON t.id_ticket = r.id_ticket";

$result = mysqli_query($conn, $query);
$row = mysqli_fetch_assoc($result);
echo "Tempo medio: " . $row['tempo_medio'];
```

---

# QUESITO II – Piano di indirizzamento

## Scelgo rete privata 192.168.10.0/24

Divisione VLAN:

VLAN 10 – Server → 192.168.10.0/26
VLAN 20 – Uffici → 192.168.10.64/26
VLAN 30 – WiFi → 192.168.10.128/26
VLAN 40 – Management → 192.168.10.192/26

Uso VLSM per suddividere la rete in sottoreti di dimensione adeguata.

---

## Controllo accesso WiFi

* WPA3-Enterprise
* Autenticazione 802.1X
* Server RADIUS

RADIUS gestisce autenticazione centralizzata.

Scarto WPA2-PSK perché meno sicuro in ambiente aziendale.

---

## Continuità del servizio

* UPS per server
* RAID 1 o RAID 5
* Backup giornaliero
* Replica database
* Doppia linea Internet (failover)

Failover = commutazione automatica su linea secondaria.

---

# QUESITO III

## IPv6: caratteristiche e differenze rispetto a IPv4

## 1. Perché nasce IPv6

IPv4 utilizza indirizzi a 32 bit, quindi il numero massimo teorico di indirizzi è:

genui{"math_block_widget_always_prefetched": {"content": "2^32"}}

≈ 4,3 miliardi di indirizzi.

Con la crescita di Internet e dell’IoT (Internet of Things, cioè dispositivi connessi come sensori, telecamere, elettrodomestici), questo numero non è più sufficiente.

IPv6 nasce per risolvere questo problema.

---

## 2. Struttura di IPv6

IPv6 utilizza indirizzi a 128 bit:

genui{"math_block_widget_always_prefetched": {"content": "2^128"}}

Numero enormemente superiore, praticamente inesauribile.

Forma di scrittura:

2001:0db8:85a3:0000:0000:8a2e:0370:7334

Espressi in esadecimale e separati da “:”.

---

## 3. Caratteristiche principali di IPv6

### a) Spazio di indirizzamento enorme

Permette indirizzamento diretto senza NAT.

NAT (Network Address Translation) è il meccanismo che in IPv4 consente a più dispositivi privati di condividere un IP pubblico.

IPv6 elimina la necessità strutturale del NAT.

---

### b) Autoconfigurazione

Supporta SLAAC (Stateless Address Autoconfiguration).

Il dispositivo può generare automaticamente il proprio indirizzo senza DHCP.

---

### c) Header semplificato

L’header IPv6 è più semplice e più efficiente per l’instradamento.

---

### d) IPsec integrato

IPsec è un insieme di protocolli per cifratura e autenticazione a livello rete.

In IPv6 è previsto come parte integrante dello standard.

---

### e) Supporto migliorato al multicast

Elimina il broadcast.
Usa multicast e anycast per ottimizzare il traffico.

---

## 4. Differenze IPv4 vs IPv6

| Aspetto             | IPv4             | IPv6           |
| ------------------- | ---------------- | -------------- |
| Lunghezza indirizzo | 32 bit           | 128 bit        |
| Notazione           | Decimale puntata | Esadecimale    |
| NAT                 | Necessario       | Non necessario |
| Configurazione      | Manuale/DHCP     | SLAAC/DHCPv6   |
| Broadcast           | Presente         | Eliminato      |
| Sicurezza           | Opzionale        | IPsec previsto |

---

## 5. Perché non è stato abbandonato IPv4

Non è possibile passare improvvisamente a IPv6 perché:

* molte reti sono ancora IPv4
* molti dispositivi legacy non supportano IPv6

Si usano tecniche come:

* Dual Stack (IPv4 + IPv6)
* Tunneling
* NAT64

---

# QUESITO IV

## Metodi di trasferimento dati client → server

In un’applicazione web dinamica l’utente invia dati al server.

I metodi principali sono:

---

## 1. Metodo GET

I dati sono inseriti nell’URL.

Esempio:

```
www.sito.it/login?user=mario&pass=123
```

Caratteristiche:

* visibile nella barra URL
* lunghezza limitata
* memorizzabile nei preferiti

Uso tipico:

* ricerche
* filtri

Scarto GET per invio password perché non sicuro.

---

## 2. Metodo POST

I dati sono nel body della richiesta HTTP.

Non visibili nell’URL.

Uso tipico:

* login
* invio form
* upload file

È più sicuro di GET, ma comunque deve essere usato con HTTPS.

---

## 3. Cookie

Piccoli file memorizzati nel browser.

Usati per:

* gestione sessioni
* preferenze utente

Non adatti per trasmettere grandi quantità di dati.

---

## 4. Sessioni server-side

Il server assegna un ID di sessione.

Il browser conserva solo l’identificativo.

I dati veri restano sul server.

È il metodo più sicuro per mantenere stato.

---

## 5. AJAX

AJAX (Asynchronous JavaScript And XML) permette invio dati asincrono senza ricaricare la pagina.

Esempio:

* aggiornamento dinamico stato ticket

Vantaggio:

* migliore esperienza utente

---

## 6. WebSocket

Protocollo bidirezionale persistente.

Utile per:

* notifiche in tempo reale
* aggiornamenti live

Scarto WebSocket per semplice form di ticket perché troppo complesso per il caso base.

---

## Confronto sintetico

| Metodo    | Sicurezza              | Uso tipico            |
| --------- | ---------------------- | --------------------- |
| GET       | Bassa                  | Ricerca               |
| POST      | Media (con HTTPS alta) | Form                  |
| Cookie    | Variabile              | Sessione              |
| Sessione  | Alta                   | Stato utente          |
| AJAX      | Dipende da HTTPS       | Interazioni dinamiche |
| WebSocket | Alta (con TLS)         | Real-time             |

---

