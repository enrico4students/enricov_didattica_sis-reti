---

# PRIMA PARTE

---

# 1. Progetto dell’infrastruttura tecnologica

## 1.a Risorse hardware e servizi software

Si propone un’architettura a tre livelli:

* Presentation Layer (Web Server in DMZ)
* Application Layer (Application Server in LAN)
* Data Layer (Database Server in VLAN dedicata)

### Componenti hardware

* Router WAN con IP pubblico statico
* Firewall UTM (Unified Threat Management)
* Core Switch Layer 3
* Server virtualizzati (cluster)
* NAS per backup
* UPS per continuità elettrica

### Componenti software

* Sistema operativo Linux Server
* Web Server Apache/Nginx
* Linguaggio PHP/Java/Python
* DBMS MySQL/PostgreSQL
* Sistema di autenticazione a ruoli (RBAC)
* Sistema di logging centralizzato

---

## 1.b Misure di sicurezza

### Sicurezza perimetrale

* Firewall con Stateful Inspection
* IDS/IPS (Intrusion Detection/Prevention System)
* NAT (Network Address Translation)
* Segmentazione in VLAN

### Sicurezza applicativa

* HTTPS con TLS 1.2+
* Password hashate (bcrypt)
* Gestione sessioni sicure
* Validazione input contro SQL Injection

### Sicurezza dati

* Backup giornaliero
* Replica DB
* Log di audit

---

## 1.c Modalità operative tecnici

### Connessione sede centrale

* Fibra FTTH Business
* Doppia WAN per ridondanza
* Firewall con VPN IPsec o SSL

### Connessione tecnici

* Laptop aziendale
* Connessione 4G/5G o WiFi cliente
* Accesso via HTTPS o VPN

### Sicurezza comunicazione

* HTTPS
* Certificati digitali validi
* Autenticazione forte

### Convalida report cliente

* Notifica email
* Accesso al portale
* Conferma con eventuale commento
* Cambio stato ticket a “chiuso convalidato”

---

# 2. Progetto della Base di Dati

---

## 2.1 Modello Concettuale (E-R)

Entità:

* Cliente
* Tecnico
* Ticket
* Report

Relazioni:

* Cliente 1 — N Ticket
* Tecnico 1 — N Ticket
* Ticket 1 — N Report

---

## 2.2 Diagramma E-R in PlantUML (sintassi piena)

```
@startuml
entity Cliente {
    +id_cliente : int <<PK>>
    --
    ragione_sociale : varchar
    email : varchar
    password_hash : varchar
}

entity Tecnico {
    +id_tecnico : int <<PK>>
    --
    nome : varchar
    competenza : varchar
    ruolo : varchar
}

entity Ticket {
    +id_ticket : int <<PK>>
    --
    data_apertura : date
    data_chiusura : date
    stato : varchar
    tipo_intervento : varchar
    descrizione : text
    id_cliente : int <<FK>>
    id_tecnico : int <<FK>>
}

entity Report {
    +id_report : int <<PK>>
    --
    data_intervento : datetime
    tempo_impiegato : int
    descrizione_attivita : text
    convalidato : boolean
    commento_cliente : text
    id_ticket : int <<FK>>
}

Cliente ||--o{ Ticket
Tecnico ||--o{ Ticket
Ticket ||--o{ Report

@enduml
```

---

## 2.3 Modello Logico Relazionale

CLIENTI(id_cliente PK, ragione_sociale, email, password_hash)

TECNICI(id_tecnico PK, nome, competenza, ruolo)

TICKETS(id_ticket PK, id_cliente FK, id_tecnico FK, data_apertura, data_chiusura, stato, tipo_intervento, descrizione)

REPORTS(id_report PK, id_ticket FK, data_intervento, tempo_impiegato, descrizione_attivita, convalidato, commento_cliente)

---

# 3. Query SQL

## 3.1 Elenco ticket aperti

```
SELECT c.ragione_sociale,
       t.data_apertura,
       te.nome AS tecnico
FROM TICKETS t
JOIN CLIENTI c ON t.id_cliente = c.id_cliente
JOIN TECNICI te ON t.id_tecnico = te.id_tecnico
WHERE t.stato = 'APERTO';
```

---

## 3.2 Tempo medio chiusura

```
SELECT AVG(DATEDIFF(data_chiusura, data_apertura)) AS tempo_medio
FROM TICKETS
WHERE stato = 'CHIUSO'
  AND data_chiusura BETWEEN '2024-01-01' AND '2024-12-31';
```

---

# Diagramma di rete formale

## Formato testuale

```
Internet
   |
Router WAN
   |
Firewall / UTM
   |
   +--- DMZ --- Web Server
   |
   +--- LAN --- Core Switch L3
                  |
         +--------+--------+--------+
         |        |        |
      VLAN10   VLAN20   VLAN30
      Amm.     Tecnici   Server
                           |
                     App Server
                           |
                      DB Server
```

---

## Diagramma rete in PlantUML (base)

```
@startuml
cloud "Internet" as NET
rectangle "Router" as RTR
rectangle "Firewall/UTM" as FW
rectangle "Web Server (DMZ)" as WEB
rectangle "App Server" as APP
rectangle "DB Server" as DB

NET --> RTR
RTR --> FW
FW --> WEB
WEB --> APP
APP --> DB
@enduml
```

---

# SECONDA PARTE

---

# QUESITO I – Monitoraggio Dirigenziale

### Modifica database

Campo ruolo in TECNICI.

### Architettura pagine

* login.php
* dashboard.php
* statistiche.php (solo DIRIGENTE)

### Esempio controllo accesso (PHP)

```
session_start();
if($_SESSION['ruolo'] != 'DIRIGENTE'){
    die("Accesso negato");
}
```

---

# QUESITO II – Piano di indirizzamento

Rete privata: 192.168.10.0/24

VLAN 10: 192.168.10.0/26
VLAN 20: 192.168.10.64/26
VLAN 30: 192.168.10.128/27
VLAN 40: 192.168.10.160/27

Controllo WiFi:

* WPA3-Enterprise
* 802.1X
* RADIUS

Continuità:

* RAID
* Replica DB
* Doppia WAN
* UPS
* Cluster virtualizzazione

---

# QUESITO III – IPv6

Caratteristiche IPv6:

* Indirizzi a 128 bit
* Eliminazione NAT
* Autoconfigurazione (SLAAC)
* Header semplificato
* Supporto nativo IPsec

Differenze rispetto IPv4:

* Spazio indirizzamento enormemente maggiore
* Nessuna frammentazione intermedia
* Miglior gestione multicast
* Supporto QoS migliorato

---

# QUESITO IV – Trasferimento dati Web

Metodi principali:

1. GET
   Parametri in URL. Idoneo per richieste idempotenti.

2. POST
   Dati nel body HTTP. Idoneo per invio credenziali o dati sensibili.

3. AJAX
   (Asynchronous JavaScript and XML)
   Permette invio asincrono senza ricaricare pagina.

4. WebSocket
   Comunicazione bidirezionale persistente tra client e server.

Esempi:

* Login → POST
* Ricerca → GET
* Aggiornamento ticket dinamico → AJAX
* Notifiche real-time → WebSocket

---

