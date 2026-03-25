## Soluzione

### 1. Analisi iniziale e logica generale di progetto

La traccia descrive una struttura alberghiera con  
- 52 camere,  
- quattro sale convegni,  
- ristorante,  
- piscina,  
- sei colonnine di ricarica, 
- uffici con sette postazioni,  
- server gestionale *interno*,  
- server web esposto su Internet, 
- Wi-Fi differenziato per 
    - ospiti, 
    - dipendenti e 
    - partecipanti ai convegni, oltre allo 
- stabilimento balneare collegato funzionalmente all’hotel.  

Quindi la prima esigenza è evitare una rete unica e piatta.  
Serve invece una rete **segmentata**, con **separazione logica** dei vari tipi di utenti e servizi, così da migliorare sicurezza, gestione e prestazioni. 

La logica seguita è questa:

1. separare le reti tramite VLAN;
2. usare un firewall/UTM come punto centrale di controllo;
3. mettere in DMZ il server web pubblico;
4. tenere il gestionale nella rete interna;
5. collocare anche il server RDBMS nella stessa DMZ del web server, ma senza pubblicarlo su Internet;
6. consentire al database connessioni solo dal WEB server;
7. collegare lo stabilimento con un link dedicato e sicuro;
8. consentire agli ospiti Internet ma non accesso alla LAN interna.

Questa deriva dal fatto che la traccia richiede  
- esplicitamente funzionamento in sicurezza e  
- separazione fra ospiti, uffici, servizi e sale convegni.  


### 2. Architettura di rete proposta

Si ipotizza una struttura con:

* accesso Internet FTTH lato hotel;
* firewall/UTM centrale;
* core switch gestito;
* access switch gestiti e, dove utile, PoE;
* access point gestiti con SSID distinti;
* DMZ unica;
* server gestionale in rete interna;
* collegamento radio punto-punto verso stabilimento;
* eventuale autenticazione centralizzata Wi-Fi.

La scelta del firewall/UTM come nodo centrale è motivata dal fatto che deve svolgere molte funzioni:

* filtraggio tra VLAN;
* NAT verso Internet;
* pubblicazione del server web;
* blocco dell’accesso diretto al DB;
* logging;
* eventuale VPN futura;
* eventuale captive portal o integrazione AAA/RADIUS.

Una semplice soluzione con solo router del provider e switch non sarebbe sufficiente, perché offrirebbe protezione e controllo troppo limitati.

### 3. DMZ scelta e motivazione

La DMZ scelta è una DMZ unica collegata al firewall. In questa DMZ si trovano:

* il WEB server, accessibile da Internet;
* il server RDBMS, non accessibile da Internet.

Questa soluzione è meno complessa di una DMZ con due firewalls (l'altra tipologia delle due), ma resta sicura se si applicano regole corrette.

Le regole essenziali sono:

* Internet -> WEB server: consentito solo su 80 e 443;
* Internet -> RDBMS: negato;
* WEB server -> RDBMS: solo tramite la porta del database (es. 3306/5432), restrizione realizzata tramite configurazione del DBMS o firewall host-based (locale all'host del RDBMS).  
* LAN interna -> RDBMS: negato, salvo amministrazione controllata;
* DMZ -> LAN interna: negato salvo servizi strettamente necessari;
* LAN interna -> DMZ: consentito solo per amministrazione o backup autorizzati.

Notare che il DBMS può stare ed è nella stessa DMZ del WEB server, ma  
- non deve essere pubblicato e  
- non deve accettare connessioni da host diversi dal WEB server.  


### 4. Diagramma testuale completo della rete

```
INTERNET
    |
[ONT / CPE FTTH]
    |
[FIREWALL / UTM]
  |            \
  |             \
  |              \------ DMZ 10.10.70.0/24
  |                         |
  |                         +--- WEB SERVER      10.10.70.10
  |                         |
  |                         +--- RDBMS SERVER    10.10.70.20
  |
  +------ [CORE SWITCH gestito, trunk 802.1Q]
              |
              +--- VLAN 10: UFFICI         10.10.10.0/24
              |      |
              |      +--- PC reception
              |      +--- PC direzione
              |      +--- PC uffici
              |      +--- Stampante di rete
              |
              +--- VLAN 20: SERVIZI        10.10.20.0/24
              |      |
              |      +--- Server gestionale   10.10.20.10
              |      +--- NAS / backup
              |      +--- Controller Wi-Fi / RADIUS
              |
              +--- VLAN 30: CONVEGNI       10.10.30.0/24
              |      |
              |      +--- AP sale convegni
              |      +--- client convegni
              |
              +--- VLAN 40: OSPITI HOTEL   10.10.40.0/24
              |      |
              |      +--- AP camere / hall / ristorante
              |      +--- SmartTV e dispositivi ospiti
              |
              +--- VLAN 60: COLONNINE EV   10.10.60.0/24
              |      |
              |      +--- colonnina 1..6
              |
              +--- VLAN 80: MANAGEMENT     10.10.80.0/24
                     |
                     +--- switch management
                     +--- AP management
                     +--- console amministrazione
```

Dal core switch parte anche il collegamento verso lo stabilimento:

```
[CORE SWITCH HOTEL]
     |
[Bridge radio PTP (point to point) A]
     ))))))))) 500 m LOS (Line of Sight) (((((((( 
[Bridge radio PTP (point to point) B]
     |
[Switch stabilimento]
  |
  +--- VLAN 90 STAFF STABILIMENTO   10.10.90.0/24
  |      |
  |      +--- PC cassa / bar / personale
  |
  +--- VLAN 50 OSPITI SPIAGGIA      10.10.50.0/24
         |
         +--- AP spiaggia
         +--- dispositivi ospiti
```

### 5. PlantUML completo della rete

```
@startuml
left to right direction
skinparam shadowing false
skinparam defaultTextAlignment center
skinparam linetype ortho
skinparam roundcorner 18

cloud "Internet" as INTERNET
node "ONT / CPE FTTH" as ONT
node "Firewall / UTM\nWAN - LAN - DMZ" as FW

rectangle "DMZ\n10.10.70.0/24" as DMZ {
    node "WEB Server\n10.10.70.10" as WEB
    database "RDBMS Server\n10.10.70.20" as DB
}

package "LAN Hotel" as LAN {
    node "Core Switch\ntrunk 802.1Q" as CORE

    rectangle "VLAN 10 - UFFICI\n10.10.10.0/24" as VLAN10 {
        node "PC uffici"
        node "Stampante di rete"
    }

    rectangle "VLAN 20 - SERVIZI\n10.10.20.0/24" as VLAN20 {
        database "Server Gestionale\n10.10.20.10" as GEST
        node "NAS / Backup"
        node "Controller Wi-Fi / RADIUS"
    }

    rectangle "VLAN 30 - CONVEGNI\n10.10.30.0/24" as VLAN30 {
        node "AP sale convegni"
        node "Client convegni"
    }

    rectangle "VLAN 40 - OSPITI HOTEL\n10.10.40.0/24" as VLAN40 {
        node "AP camere / hall"
        node "Client ospiti hotel"
    }

    rectangle "VLAN 60 - COLONNINE EV\n10.10.60.0/24" as VLAN60 {
        node "Colonnine 1..6"
    }

    rectangle "VLAN 80 - MANAGEMENT\n10.10.80.0/24" as VLAN80 {
        node "Console amministrazione"
    }
}

folder "Collegamento PTP 500 m" as LINK {
    node "Bridge radio A" as RA
    node "Bridge radio B" as RB
}

package "Stabilimento balneare" as BEACH {
    node "Switch stabilimento" as BSW

    rectangle "VLAN 90 - STAFF\n10.10.90.0/24" as VLAN90 {
        node "PC cassa / bar"
    }

    rectangle "VLAN 50 - OSPITI SPIAGGIA\n10.10.50.0/24" as VLAN50 {
        node "AP spiaggia"
        node "Client spiaggia"
    }
}

INTERNET -- ONT
ONT -- FW
FW -- WEB : 80/443
WEB -- DB : porta DBMS
FW -- CORE
CORE -- VLAN10
CORE -- VLAN20
CORE -- VLAN30
CORE -- VLAN40
CORE -- VLAN60
CORE -- VLAN80
CORE -- RA
RA -- RB
RB -- BSW
BSW -- VLAN90
BSW -- VLAN50

note top of FW
Regole:
Internet -> WEB consentito
Internet -> DB negato
Guest -> LAN negato
Staff stabilimento -> gestionale consentito
end note

note right of DB
DB non pubblicato.
Accesso solo dal WEB server.
end note
@enduml
```

### 6. Apparati necessari

Gli apparati necessari sono:

* ONT/CPE FTTH del provider;
* firewall/UTM con almeno tre interfacce logiche o fisiche;
* core switch gestito;
* access switch gestiti;
* access point gestiti;
* server gestionale interno;
* WEB server in DMZ;
* RDBMS server in DMZ;
* NAS o sistema di backup;
* controller Wi-Fi e/o server RADIUS;
* due bridge radio punto-punto per il collegamento allo stabilimento;
* switch gestito presso lo stabilimento;
* UPS per gli apparati principali.

### 7. Piano di indirizzamento

Per semplicità e chiarezza si usa una sottorete /24 per ogni segmento logico. In un compito scritto è una scelta leggibile, ordinata e facilmente espandibile.

```
VLAN 10   UFFICI               10.10.10.0/24    gateway 10.10.10.1
VLAN 20   SERVIZI INTERNI      10.10.20.0/24    gateway 10.10.20.1
VLAN 30   CONVEGNI             10.10.30.0/24    gateway 10.10.30.1
VLAN 40   OSPITI HOTEL         10.10.40.0/24    gateway 10.10.40.1
VLAN 50   OSPITI SPIAGGIA      10.10.50.0/24    gateway 10.10.50.1
VLAN 60   COLONNINE EV         10.10.60.0/24    gateway 10.10.60.1
VLAN 70   DMZ                  10.10.70.0/24    gateway 10.10.70.1
VLAN 80   MANAGEMENT           10.10.80.0/24    gateway 10.10.80.1
VLAN 90   STAFF STABILIMENTO   10.10.90.0/24    gateway 10.10.90.1
```

Assegnazioni significative:

```
WEB server            10.10.70.10
RDBMS server          10.10.70.20
Server gestionale     10.10.20.10
Controller Wi-Fi      10.10.20.30
```

### 8. Motivazione delle scelte di indirizzamento e segmentazione

Ho scelto reti diverse per ospiti, uffici, servizi, convegni e colonnine perché la traccia richiede esplicitamente tale separazione.  
- La VLAN ospiti hotel e la VLAN ospiti spiaggia devono poter accedere a Internet ma non alla rete interna.  
- La VLAN uffici e la VLAN servizi devono poter usare il gestionale.  
- La VLAN convegni deve avere accesso separato per i partecipanti agli eventi.  
- Le colonnine vanno isolate, perché sono dispositivi dedicati che non devono dialogare liberamente con tutto il resto della rete.  


### 9. Regole firewall principali

Le regole più importanti sono:

* Internet -> WEB server: consentire solo TCP 80 e 443;
* Internet -> RDBMS: negare;
* Internet -> LAN interna: negare;
* **NON FIREWALL PRINCIPALE** WEB server -> RDBMS: consentire solo sulla porta del DBMS;
* VLAN ospiti hotel -> Internet: consentire;
* VLAN ospiti hotel -> LAN interna: negare;
* VLAN ospiti spiaggia -> Internet: consentire;
* VLAN ospiti spiaggia -> LAN interna: negare;
* VLAN staff stabilimento -> server gestionale: consentire;
* VLAN management -> apparati di rete: consentire;
* VLAN colonnine -> solo servizi web/applicativi autorizzati: consentire.

### 10. Collegamento tra hotel e stabilimento: confronto soluzioni

La traccia precisa che lo stabilimento è visibile dalla terrazza e dista 500 metri. Inoltre entrambe le sedi possono avere FTTH. Quindi le soluzioni principali sono due. 

#### Soluzione A: ponte radio punto-punto

Vantaggi:

* molto adatto a 500 m con visibilità ottica;
* alte prestazioni;
* costo operativo ridotto;
* gestione centralizzata dell’accesso.

Limiti:

* richiede installazione esterna;
* dipende dalla qualità del link radio;
* richiede allineamento e manutenzione.

#### Soluzione B: doppia FTTH + VPN site-to-site

Vantaggi:

* ogni sede ha autonomia Internet;
* architettura più flessibile;
* riduce la dipendenza da un unico link fisico tra sedi.

Limiti:

* costi maggiori;
* maggiore complessità;
* richiede VPN permanente.

### 11. Scelta effettuata per il collegamento

La soluzione preferenziale è il ponte radio punto-punto cifrato, perché la distanza è ridotta e la visibilità ottica è già dichiarata. È la scelta più naturale, quasi suggerita dalla traccia, più economica. Lo switch dello stabilimento distribuirà poi due reti separate:

* VLAN 90 per il personale;
* VLAN 50 per gli ospiti della spiaggia.

Il personale dello stabilimento deve poter consultare il software gestionale dell’albergo.  
Gli ospiti della spiaggia devono usare Internet con modalità di identificazione analoghe a quelle dell’hotel. 

### 12. Progetto della base di dati

La base di dati deve gestire:

* anagrafiche ospiti con dati personali ed email;
* camere con numero e tipologia;
* prenotazioni con check-in e check-out;
* credenziali Wi-Fi legate alla prenotazione. 

La scelta migliore è modellare le credenziali Wi-Fi come entità separata collegata alla prenotazione. In questo modo si rappresenta correttamente il fatto che **la credenziale vale per uno specifico soggiorno** e non genericamente per l’ospite.

### 13. Modello concettuale

Entità:

* OSPITE
* CAMERA
* PRENOTAZIONE
* CREDENZIALE_WIFI

Relazioni:

* un ospite effettua molte prenotazioni nel tempo;
* una camera compare in molte prenotazioni nel tempo;
* ogni prenotazione si riferisce a un solo ospite e a una sola camera;
* ogni prenotazione genera una credenziale Wi-Fi.

### 14. PlantUML del modello concettuale

```
@startuml
hide circle
skinparam linetype ortho

entity OSPITE {
    * id_ospite : INT
    --
    nome : VARCHAR
    cognome : VARCHAR
    email : VARCHAR
    telefono : VARCHAR
    documento : VARCHAR
}

entity CAMERA {
    * id_camera : INT
    --
    numero : VARCHAR
    tipologia : VARCHAR
}

entity PRENOTAZIONE {
    * id_prenotazione : INT
    --
    data_check_in : DATE
    data_check_out : DATE
    stato : VARCHAR
    id_ospite : INT
    id_camera : INT
}

entity CREDENZIALE_WIFI {
    * id_wifi : INT
    --
    username : VARCHAR
    password : VARCHAR
    data_attivazione : DATETIME
    data_scadenza : DATETIME
    id_prenotazione : INT
}

OSPITE ||--o{ PRENOTAZIONE : effettua
CAMERA ||--o{ PRENOTAZIONE : riguarda
PRENOTAZIONE ||--|| CREDENZIALE_WIFI : genera
@enduml
```

### 15. Motivazione delle cardinalità

Cardinalità OSPITE 1:N PRENOTAZIONE perché uno stesso ospite può soggiornare più volte. 
Cardinalità CAMERA 1:N PRENOTAZIONE perché una stessa camera può essere prenotata molte volte, ma in periodi diversi. 
Cardinalità PRENOTAZIONE 1:1 CREDENZIALE_WIFI: una prenotazione produce una coppia username-password per l’accesso Wi-Fi.

### 16. Modello logico relazionale

```
OSPITE(
    id_ospite PK,
    nome,
    cognome,
    email UNIQUE,
    telefono,
    documento
)

CAMERA(
    id_camera PK,
    numero UNIQUE,
    tipologia
)

PRENOTAZIONE(
    id_prenotazione PK,
    id_ospite FK -> OSPITE(id_ospite),
    id_camera FK -> CAMERA(id_camera),
    data_check_in,
    data_check_out,
    stato
)

CREDENZIALE_WIFI(
    id_wifi PK,
    id_prenotazione FK UNIQUE -> PRENOTAZIONE(id_prenotazione),
    username UNIQUE,
    password,
    data_attivazione,
    data_scadenza
)
```

### 17. PlantUML del modello logico

```
@startuml
hide circle
skinparam linetype ortho

entity "OSPITE" as OSP {
    * id_ospite : INT <<PK>>
    --
    nome : VARCHAR(50)
    cognome : VARCHAR(50)
    email : VARCHAR(100) <<UQ>>
    telefono : VARCHAR(20)
    documento : VARCHAR(30)
}

entity "CAMERA" as CAM {
    * id_camera : INT <<PK>>
    --
    numero : VARCHAR(10) <<UQ>>
    tipologia : VARCHAR(30)
}

entity "PRENOTAZIONE" as PRE {
    * id_prenotazione : INT <<PK>>
    --
    id_ospite : INT <<FK>>
    id_camera : INT <<FK>>
    data_check_in : DATE
    data_check_out : DATE
    stato : VARCHAR(20)
}

entity "CREDENZIALE_WIFI" as WIFI {
    * id_wifi : INT <<PK>>
    --
    id_prenotazione : INT <<FK,UQ>>
    username : VARCHAR(50) <<UQ>>
    password : VARCHAR(100)
    data_attivazione : DATETIME
    data_scadenza : DATETIME
}

OSP ||--o{ PRE
CAM ||--o{ PRE
PRE ||--|| WIFI
@enduml
```

### 18. Vincoli applicativi importanti

Per rendere il sistema corretto servono almeno questi controlli:

* data_check_out > data_check_in;
* non sovrapporre prenotazioni della stessa camera nello stesso periodo;
* username Wi-Fi univoco;
* eventuale scadenza automatica delle credenziali al termine del soggiorno.

### 19. Seconda parte, quesito 1: colonnina di ricarica e socket

Formato di trasmissione possibile:

```
{
  "data_ora": "2026-03-20T10:15:00Z",
  "id_cliente": "CLI145",
  "percentuale_carica": 78,
  "energia_erogata_kWh": 12.4
}
```

Scelgo JSON perché è leggibile, semplice da trasmettere e facile da interpretare sia da microcontrollore sia dal server.

I socket rappresentano l’interfaccia software con cui due processi in rete comunicano.  
In una soluzione con connessione e  affidabilite (non nel senso "forte" di robusta) usare TCP. Il server crea un socket, esegue bind su una porta, poi listen e accept per ricevere la connessione.  
La colonnina crea il socket client ed esegue connect verso il server remoto.  
Una volta stabilita la connessione, i dati vengono inviati e ricevuti con send/recv oppure write/read.  
Al termine della sessione entrambi chiudono il socket con close.  

TCP è preferibile a UDP perché **garantisce** consegna, ordine dei dati e controllo degli errori, aspetti importanti quando si trasmettono dati di contabilizzazione energetica.

Schema:

```
[Colonnina]
    |
socket TCP client
    |
  rete
    |
socket TCP server
    |
 [Server]
```

### 20. Seconda parte, quesito 2: filtraggio contenuti a scuola

Per una scuola userei  
- firewall/UTM,  
- switch gestito con VLAN,  
- proxy o content filter e  
- DNS filtering.  

Gli studenti starebbero in una VLAN separata da quella degli uffici.  
Il firewall distinguerebbe le politiche: sulla rete studenti si applicherebbero filtri più rigidi, blocco di categorie, DNS filtrato, logging e limiti applicativi.  
Sulla rete uffici si userebbero regole più permissive ma sempre isolate dalla rete didattica. Il content filter può controllare il traffico web, mentre il DNS filtering impedisce di risolvere domini vietati.  
Il vantaggio è una navigazione più sicura e una separazione chiara dei contesti d’uso.  
I limiti sono i costi, la complessità e il fatto che parte del traffico HTTPS possa richiedere analisi più avanzate.

Schema:

```
INTERNET
   |
[Firewall / UTM + filtro contenuti]
   |
[Switch gestito]
  |                 |
VLAN studenti    VLAN uffici
```

### 21. Seconda parte, quesito 3: differenza tra HTTP e HTTPS

HTTP è un protocollo applicativo usato per scambiare pagine web e risorse, ma in chiaro. HTTPS è HTTP protetto da TLS. Questo comporta tre vantaggi fondamentali:  
- cifratura,  
- autenticazione del server tramite certificato,  
- integrità dei dati.  

Con HTTP un intercettatore può leggere o modificare il traffico; con HTTPS il browser verifica il certificato e crea un canale cifrato col server. Per il visitatore del sito ciò significa maggiore protezione di credenziali, dati personali e pagamenti, oltre a minore rischio di attacchi man-in-the-middle e alterazione dei contenuti.

Schema:

```
HTTP
Browser ---- dati in chiaro ---- Server

HTTPS
Browser ==== canale TLS cifrato ==== Server
```

### 22. Seconda parte, quesito 4: PC che non apre siti esterni ma vede la LAN

La sequenza corretta di verifiche è procedere per esclusione. Per prima cosa  
- controllare configurazione IP, subnet mask, gateway 192.168.24.1 e DNS 192.168.24.5.  
- Poi eseguire il ping del gateway. Se non risponde, il problema è locale o di instradamento interno.  
- Se risponde, verificare il DNS locale con ping 192.168.24.5.  
- Successivamente provare il ping verso un IP pubblico, ad esempio 8.8.8.8.  
- Se questo funziona ma i siti non si aprono, è probabile un problema DNS; allora usare nslookup per verificare la risoluzione dei nomi.  
- Se invece non si raggiunge l’IP pubblico, il problema può stare nel gateway, nel NAT, nel firewall o nella connettività Internet.  
- Infine controllare eventuale proxy errato nel browser e usare tracert per capire dove il traffico si interrompe.

Schema:

```
1. controllare IP / mask / gateway / DNS
2. ping 192.168.24.1
3. ping 192.168.24.5
4. ping IP pubblico
5. nslookup dominio
6. tracert
7. controllare proxy browser
```

### 23. Conclusione finale

La soluzione proposta rispetta i requisiti posti dalla traccia perché usa una rete segmentata, protegge i servizi esposti con una DMZ, mantiene il gestionale nella rete interna, collega in modo sicuro lo stabilimento balneare e modella correttamente le prenotazioni e le credenziali Wi-Fi.  
La scelta della DMZ unica con WEB server e RDBMS nello stesso segmento è valida purché il database non sia pubblicato e accetti connessioni solo dal WEB server. In questo modo si ottiene una soluzione realistica, ordinata e tecnicamente coerente. 

