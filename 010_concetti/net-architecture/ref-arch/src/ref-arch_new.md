ARCHITETTURE DI RIFERIMENTO PER SISTEMI E RETI

1. Obiettivo generale

Definire due reference architecture realistiche, riusabili in ottica di traccia di esame di stato ma aderenti a casi enterprise reali:

* versione 2-layer
* versione 3-layer

Le due architetture devono includere in modo coerente:

* connettività wired e wireless
* WiFi corporate e WiFi guest
* server pubblici on-site
* servizi interni business-critical
* segmentazione di rete
* DMZ
* rete di management
* accesso remoto solo per il management
* collegamento a sede secondaria locale a 600 m in line-of-sight
* collegamento VPN site-to-site verso altra sede in altro continente
* integrazione con cloud e servizi serverless
* IDS/IPS con integrazione verso NMS / piattaforma di monitoraggio-sicurezza
* cluster big data interno di circa 10 nodi

Questa impostazione è coerente con le guide di campus design Cisco, con le linee guida NIST sui firewall e con le architetture ibride cloud/on-prem documentate da AWS. ([Cisco][1])

2. Servizi e requisiti funzionali comuni

Le due architetture devono supportare gli stessi servizi.

Servizi pubblici on-site:

* web server pubblico
* server o API gateway che espone endpoint REST e SOAP
* reverse proxy / WAF davanti ai servizi web pubblici

Servizi interni:

* DBMS relazionale
* sistema SAP
* business application custom
* server documentale altamente confidenziale, accessibile solo al management
* MongoDB per gestione documentale generale, accessibile ai dipendenti secondo RBAC
* servizi di identità, autenticazione, log e monitoraggio
* NMS
* IDS/IPS e raccolta eventi di sicurezza
* cluster big data di circa 10 nodi

Servizi cloud:

* frontend e servizi pubblici su cloud provider
* funzioni serverless
* invocazione controllata di alcuni servizi on-site da parte di componenti serverless

Connettività geografica:

* sede principale locale
* sede secondaria locale a 600 m LOS
* altra sede principale in altro continente
* accesso remoto consentito solo ai manager

3. Principi architetturali comuni

Le due reference architecture seguono gli stessi principi.

Separazione delle zone:

* zona Internet
* zona DMZ
* zona server interni
* zona utenti
* zona management
* zona security/monitoring
* zona big data

Controllo dei flussi:

* il firewall deve essere il punto di enforcement tra zone con postura di sicurezza diversa
* Internet non deve raggiungere direttamente DBMS, SAP, documentale interno, MongoDB interno, management, NMS, cluster big data
* la DMZ deve poter raggiungere solo i backend strettamente necessari
* il WiFi guest deve uscire solo verso Internet
* il management remoto ordinario non deve esistere; il remote access è consentito solo ai manager, e solo verso risorse loro autorizzate
* la rete di management degli apparati deve essere separata dalla rete degli utenti

Questo è coerente con NIST SP 800-41 Rev. 1, che tratta il firewall come punto di controllo tra reti con livelli di fiducia differenti e richiede policy specifiche e amministrazione sicura. ([NIST Computer Security Resource Center][2])

4. Piano di segmentazione comune

Per entrambe le architetture conviene adottare una segmentazione leggibile e riusabile.

* VLAN 10   Uffici operativi                10.10.10.0/24
* VLAN 20   Management utenti               10.10.20.0/24
* VLAN 30   WiFi corporate                  10.10.30.0/24
* VLAN 40   WiFi guest                      10.10.40.0/24
* VLAN 50   Server business interni         10.10.50.0/24
* VLAN 60   Backend DBMS / SAP              10.10.60.0/24
* VLAN 70   Documentale riservato Mgmt      10.10.70.0/24
* VLAN 80   MongoDB documentale ordinario   10.10.80.0/24
* VLAN 90   Big Data client / ingest        10.10.90.0/24
* VLAN 91   Big Data data plane             10.10.91.0/24
* VLAN 100  Big Data management             10.10.100.0/24
* VLAN 110  Management rete                 10.10.110.0/24
* VLAN 120  Security / NMS / SIEM           10.10.120.0/24
* VLAN 130  DMZ on-site                     10.10.130.0/24
* VLAN 140  Transit / WAN / VPN             10.10.140.0/24
* VLAN 150  Secondario utenti               10.10.150.0/24
* VLAN 160  Secondario guest                10.10.160.0/24
* VLAN 170  Secondario management           10.10.170.0/24

Nota importante: la DMZ può avere una subnet dedicata, ma architetturalmente deve essere una security zone separata sul firewall, non semplicemente una VLAN interna “come le altre”. Questo punto è pienamente coerente con le linee guida NIST sui firewall e sulle policy perimetrali. ([NIST Computer Security Resource Center][2])

5. Policy di accesso comuni

Internet verso on-site:

* consentire solo HTTPS verso reverse proxy / WAF / web frontend in DMZ
* consentire gli endpoint pubblici REST/SOAP solo attraverso il livello pubblicato in DMZ
* negare accesso diretto a DBMS, SAP, file server, MongoDB interni, NMS, management, cluster big data

DMZ verso interno:

* consentire solo i flussi applicativi strettamente necessari verso application server interni
* consentire solo le connessioni necessarie dai web/API layer verso i backend
* negare accesso verso VLAN utenti
* negare accesso verso management

Utenti ordinari:

* accesso a business app, SAP front-end, MongoDB documentale ordinario secondo RBAC
* nessun accesso al documentale altamente riservato del management
* nessun accesso alla rete di management
* nessun accesso amministrativo al cluster big data

Management:

* accesso al documentale riservato
* accesso remoto via VPN con MFA
* accesso alle dashboard e ai servizi autorizzati
* nessun accesso implicito alla rete di management degli apparati, salvo ruolo amministrativo specifico

Amministratori IT:

* accesso alla rete di management solo da jump host o postazioni amministrative
* protocolli di gestione solo cifrati
* autenticazione forte
* logging e audit delle sessioni

WiFi guest:

* solo Internet
* isolamento client-to-client
* nessun accesso alla LAN aziendale

6. Reference Architecture 1: campus 2-layer

6.1 Descrizione generale

Questa è la reference architecture da considerare come soluzione base più adatta a una traccia d’esame completa ma ancora leggibile.

Struttura:

* access layer
* collapsed core, che accorpa core e distribution
* cluster NGFW come punto di controllo principale
* DMZ separata sul firewall
* server farm interna
* fabric o blocco dedicato per il cluster big data

Cisco documenta il two-tier design e il collapsed core come approccio reale per campus non enormi, pur mantenendo caratteristiche enterprise di ridondanza, sicurezza e scalabilità. ([Cisco][1])

6.2 Perché scegliere il 2-layer

Il modello 2-layer è preferibile quando:

* il campus non è enorme
* non esistono molti edifici o blocchi indipendenti
* si vuole una topologia più semplice
* si vuole ridurre complessità e costi
* si vuole una soluzione molto spiegabile in sede d’esame

6.3 Diagramma ASCII completo della versione 2-layer

```
+---------------------- INTERNET ----------------------+
                          |
                          |
                  +----------------+
                  |  ISP CPE / ONT |
                  +----------------+
                          |
                          |
                +----------------------+
                | NGFW CLUSTER HA      |
                | NAT / ACL / IPS      |
                | RA VPN / S2S VPN     |
                +----------------------+
                 |         |         |
                 |         |         |
                 |         |         +--------------------+
                 |         |                              |
                 |         |                      +------------------+
                 |         |                      |  DMZ ON-SITE     |
                 |         |                      |  VLAN 130        |
                 |         |                      |------------------|
                 |         |                      | Reverse Proxy    |
                 |         |                      | WAF              |
                 |         |                      | Web Public       |
                 |         |                      | REST/SOAP Facade |
                 |         |                      +------------------+
                 |         |
                 |         +-----------------------------------------------+
                 |                                                         |
         +--------------------------+                             +----------------------+
         | COLLAPSED CORE PAIR      |                             | WAN / VPN SERVICES   |
         | L3 campus aggregation    |                             | VLAN 140             |
         | redundant uplinks        |                             +----------------------+
         +--------------------------+
            |        |         |             \
            |        |         |              \
            |        |         |               \
            |        |         |                \
            |        |         |                 \
    +-----------+ +-----------+ +-----------+   +-------------------------+
    | Access SW | | Access SW | | Access SW |   | Server / BigData Agg    |
    | users     | | office    | | wireless  |   | 10/25 GbE recommended   |
    +-----------+ +-----------+ +-----------+   +-------------------------+
        |             |             |                  |         |        |
        |             |             |                  |         |        |
    PC / VoIP     PC / printer     APs            +--------+ +--------+ +------------------+
                                                  | Server | | SecOps | | Big Data Fabric  |
                                                  | Farm   | | / NMS  | | 10 nodes         |
                                                  +--------+ +--------+ +------------------+
                                                     |          |           |      |    |
                                                     |          |           |      |    |
                                            +----------------+  |     +----------------------+
                                            | VLAN 50        |  |     | VLAN 90 client/ing  |
                                            | Business App   |  |     | VLAN 91 data plane  |
                                            +----------------+  |     | VLAN100 mgmt       |
                                                                 |     +----------------------+
                                            +----------------+   |
                                            | VLAN 60        |   |
                                            | DBMS / SAP     |   |
                                            +----------------+   |
                                                                 |
                                            +----------------+   |
                                            | VLAN 70        |   |
                                            | Doc Mgmt only  |   |
                                            +----------------+   |
                                                                 |
                                            +----------------+   |
                                            | VLAN 80        |   |
                                            | MongoDB RBAC   |   |
                                            +----------------+   |
                                                                 |
                                            +----------------+   |
                                            | VLAN 110       |<--+
                                            | Mgmt network   |
                                            +----------------+
                                                                 |
                                            +----------------+
                                            | VLAN 120       |
                                            | NMS / SIEM     |
                                            | IDS collector  |
                                            +----------------+

Collegamenti geografici:

    COLLAPSED CORE / NGFW
           |
           +---- bridge radio PTP A  )) 600 m LOS ((  bridge radio PTP B ----+
                                                                               |
                                                                        +--------------+
                                                                        | SW secondario|
                                                                        +--------------+
                                                                          |     |     |
                                                                          |     |     |
                                                                     VLAN150 VLAN160 VLAN170
                                                                     users   guest   mgmt

    NGFW CLUSTER
           |
           +---- Site-to-Site VPN IPsec ---- Internet ---- Remote HQ another continent

    NGFW CLUSTER
           |
           +---- Remote Access VPN (MFA) ---- only managerial users
```

6.4 Diagramma PlantUML completo della versione 2-layer

```
@startuml
skinparam componentStyle rectangle
skinparam shadowing false
skinparam defaultTextAlignment left

cloud "Internet" as Internet
node "ISP CPE / ONT" as ISP
node "NGFW Cluster HA\nNAT / ACL / IPS\nRA VPN / S2S VPN" as FW
node "DMZ On-Site\nVLAN 130" as DMZ
node "Collapsed Core Pair\nCampus aggregation" as CORE

node "Access SW Users" as ASW1
node "Access SW Office" as ASW2
node "Access SW Wireless" as ASW3
node "Server / BigData Aggregation\n10/25 GbE recommended" as SVA

node "Business App Servers\nVLAN 50" as APP
node "DBMS / SAP Backend\nVLAN 60" as DB
node "Reserved Document Server\nMgmt only\nVLAN 70" as DOC
database "MongoDB Document Store\nRBAC\nVLAN 80" as MDB
node "Management Network\nVLAN 110" as MGMT
node "NMS / SIEM / IDS Collector\nVLAN 120" as SEC
node "Big Data Cluster\n10 nodes\nVLAN 90/91/100" as BD

node "Reverse Proxy / WAF" as WAF
node "Public Web Server" as WEB
node "REST/SOAP Public Facade" as API

node "PTP Radio A" as PTA
node "PTP Radio B" as PTB
node "Secondary Office Switch" as BR2
node "Secondary Users\nVLAN 150" as BUSER
node "Secondary Guest\nVLAN 160" as BGUEST
node "Secondary Mgmt\nVLAN 170" as BMGMT

node "Remote Main Site\nAnother Continent" as RHQ
actor "Managers Remote Users" as MGR

Internet -- ISP
ISP -- FW

FW -- DMZ
FW -- CORE
FW -- RHQ
FW -- MGR

DMZ -- WAF
DMZ -- WEB
DMZ -- API

CORE -- ASW1
CORE -- ASW2
CORE -- ASW3
CORE -- SVA

SVA -- APP
SVA -- DB
SVA -- DOC
SVA -- MDB
SVA -- MGMT
SVA -- SEC
SVA -- BD

CORE -- PTA
PTA -- PTB
PTB -- BR2
BR2 -- BUSER
BR2 -- BGUEST
BR2 -- BMGMT

note right of FW
Main security enforcement point:
- Internet/DMZ
- DMZ/Internal
- Remote Access VPN
- Site-to-Site VPN
end note

note right of MGMT
Separate management network:
switches, APs, firewalls,
hypervisors, iDRAC/iLO/IPMI,
security sensors
end note

note right of BD
Distributed processing and
high east-west traffic.
Separate data and mgmt planes.
end note
@enduml
```

6.5 Funzionamento logico

Nel modello 2-layer:

* gli access switch servono terminali, AP, telefoni, stampanti
* il collapsed core aggrega il traffico del campus
* il firewall mantiene il ruolo di controllo interzona e perimetrale
* la DMZ è separata
* le zone server e big data sono dedicate

È opportuno evitare che tutta la logica di sicurezza venga delegata al solo switching multilayer del campus. La scelta migliore, per questa reference architecture, è fare in modo che il traffico tra zone con differente livello di fiducia sia visibile e controllabile dal NGFW.

6.6 WiFi corporate e guest

Cisco tratta esplicitamente l’accesso wireless enterprise, il guest wireless, la sicurezza WLAN e l’alta disponibilità dei controller/AP nel design campus. ([Cisco][1])

Scelta progettuale:

* SSID Corp-WiFi -> VLAN 30
* SSID Guest-WiFi -> VLAN 40
* autenticazione corporate preferibilmente 802.1X / RADIUS
* guest access separato e confinato verso Internet
* eventuale captive portal per guest

6.7 DMZ on-site

In DMZ:

* reverse proxy / WAF
* web server pubblico
* facade REST/SOAP
* eventuale load balancer reverse

Flussi tipici:

* Internet -> WAF / reverse proxy
* WAF -> web / API facade
* API facade -> application server interno specifico
* application server -> DB specifico se necessario
* nessun accesso DMZ -> management
* nessun accesso Internet -> DB interni

6.8 Ufficio secondario a 600 m LOS

Per un sito a 600 metri con line-of-sight, la soluzione più realistica è un ponte radio point-to-point dedicato.

Scelta consigliata:

* radio bridge PTP
* preferibilmente collegamento routed oppure trunk limitato
* subnet locali separate per il sito secondario
* segmentazione locale users/guest/management

La soluzione evita di trattare il sito remoto come “un piano in più” dello stesso edificio. È un sito separato, pur vicino.

6.9 Sede in altro continente

Collegamento:

* VPN site-to-site IPsec terminata sul firewall
* scambio controllato dei prefissi
* filtri espliciti tra reti
* logging centralizzato

6.10 Remote access solo per i manager

Implementazione:

* remote access VPN sul firewall
* MFA obbligatoria
* autorizzazione basata su gruppo directory “Managers”
* rete VPN dedicata
* ACL che consentono solo le risorse necessarie ai manager

Questo significa che non tutti i dipendenti possono lavorare da remoto: solo quelli appartenenti al gruppo manageriale.

6.11 Rete di management

La rete di management deve essere implementata come rete separata e protetta.

Implementazione:

* VLAN 110 dedicata
* indirizzi di management di switch, AP, firewall, controller, hypervisor, server management board, UPS, storage
* accessibile solo da postazioni amministrative o jump host
* protocolli solo sicuri: SSH, HTTPS, SNMPv3, syslog cifrato quando supportato
* nessun accesso dagli utenti ordinari

Motivazione:

* ridurre la superficie di attacco
* impedire che una compromissione su una VLAN utente diventi compromissione degli apparati
* centralizzare audit e controllo
* separare traffico utente e traffico amministrativo

NIST richiede amministrazione sicura dei firewall e l’uso di autenticazione forte e canali protetti; lo stesso principio va esteso alla management network in modo coerente. ([NIST Computer Security Resource Center][2])

6.12 IDS/IPS integrato con NMS

Snort è documentato come Network Intrusion Detection & Prevention System. Wazuh documenta integrazioni con NIDS come Suricata e inoltro verso piattaforme analitiche. ([Snort][3])

Quindi, nella reference architecture:

* IPS inline sul NGFW per il traffico nord-sud
* sensore NIDS passivo per traffico est-ovest critico
* raccolta eventi su piattaforma security centrale
* integrazione con NMS per correlare performance, availability e security alert

Occorre distinguere:

* NMS: disponibilità, inventario, telemetria, allarmi infrastrutturali
* piattaforma security / SIEM / XDR: eventi IDS/IPS, log, correlazione, incident analysis

6.13 Cluster big data

Hadoop HDFS documenta un modello di storage distribuito su cluster e tratta anche la rack awareness. Questo giustifica una progettazione che distingua bene traffico client, traffico dati interno e management del cluster. ([Apache Hadoop][4])

Scelta progettuale:

* circa 10 nodi
* separazione tra:

  * access/ingest plane
  * data plane / replica
  * management plane
* collegamento con fabric dedicata o blocco server ad alta capacità
* preferenza progettuale per 10/25 GbE sui collegamenti del cluster
* evitare che il traffico di replica saturi la rete office

La scelta 10/25 GbE è una scelta di progetto coerente con la presenza di traffico east-west elevato; non è un obbligo della fonte Hadoop, ma una conseguenza tecnica ragionevole del tipo di carico. ([Apache Hadoop][4])

7. Reference Architecture 2: campus 3-layer

7.1 Descrizione generale

La versione 3-layer mantiene gli stessi servizi e gli stessi requisiti, ma separa chiaramente:

* access layer
* distribution layer
* core layer

Cisco tratta esplicitamente both two-tier design e three-tier design nelle guide di campus design. ([Cisco][1])

7.2 Perché scegliere il 3-layer

Il 3-layer è preferibile quando:

* il campus è più grande
* esistono più edifici o blocchi
* serve maggiore modularità
* serve miglior isolamento dei domini di guasto
* si vuole una crescita più ordinata nel tempo

7.3 Diagramma ASCII completo della versione 3-layer

```
+---------------------- INTERNET ----------------------+
                          |
                          |
                  +----------------+
                  |  ISP CPE / ONT |
                  +----------------+
                          |
                          |
                +----------------------+
                | NGFW CLUSTER HA      |
                | NAT / ACL / IPS      |
                | RA VPN / S2S VPN     |
                +----------------------+
                 |         |         |
                 |         |         +--------------------+
                 |         |                              |
                 |         |                      +------------------+
                 |         |                      |  DMZ ON-SITE     |
                 |         |                      |  VLAN 130        |
                 |         |                      |------------------|
                 |         |                      | Reverse Proxy    |
                 |         |                      | WAF              |
                 |         |                      | Web Public       |
                 |         |                      | REST/SOAP Facade |
                 |         |                      +------------------+
                 |         |
                 |         +-----------------------------------------------+
                 |                                                         |
                +---------------------------+
                | CORE PAIR                 |
                | high-speed backbone       |
                +---------------------------+
                    |                  |
                    |                  |
         +------------------+   +------------------+
         | Distribution A   |   | Distribution B   |
         | block A          |   | block B          |
         +------------------+   +------------------+
          |      |      |         |      |       |
          |      |      |         |      |       |
     +--------+ +--------+ +--------+ +--------+ +----------------------+
     |Access  | |Access  | |Access  | |Access  | | Server/BigData Dist  |
     |Users   | |Office  | |Wireless| |Spare   | | aggregation          |
     +--------+ +--------+ +--------+ +--------+ +----------------------+
                                                     |        |         |
                                                     |        |         |
                                              +-----------+ +---------+ +------------------+
                                              | Server    | | SecOps  | | Big Data Fabric  |
                                              | Farm      | | / NMS   | | 10 nodes         |
                                              +-----------+ +---------+ +------------------+
                                                 |             |            |      |      |
                                                 |             |            |      |      |
                                          +----------------+   |    +----------------------+
                                          | VLAN 50        |   |    | VLAN 90 client/ing  |
                                          | Business App   |   |    | VLAN 91 data plane  |
                                          +----------------+   |    | VLAN100 mgmt       |
                                                               |    +----------------------+
                                          +----------------+   |
                                          | VLAN 60        |   |
                                          | DBMS / SAP     |   |
                                          +----------------+   |
                                                               |
                                          +----------------+   |
                                          | VLAN 70        |   |
                                          | Doc Mgmt only  |   |
                                          +----------------+   |
                                                               |
                                          +----------------+   |
                                          | VLAN 80        |   |
                                          | MongoDB RBAC   |   |
                                          +----------------+   |
                                                               |
                                          +----------------+   |
                                          | VLAN 110       |<--+
                                          | Mgmt network   |
                                          +----------------+
                                                               |
                                          +----------------+
                                          | VLAN 120       |
                                          | NMS / SIEM     |
                                          | IDS collector  |
                                          +----------------+

Collegamenti geografici:

      Core / Distribution / NGFW
                 |
                 +---- bridge radio PTP A  )) 600 m LOS ((  bridge radio PTP B ----+
                                                                                     |
                                                                              +--------------+
                                                                              | Dist/Access  |
                                                                              | secondario   |
                                                                              +--------------+
                                                                                |    |     |
                                                                                |    |     |
                                                                            VLAN150 VLAN160 VLAN170
                                                                            users   guest   mgmt

      NGFW CLUSTER
                 |
                 +---- Site-to-Site VPN IPsec ---- Internet ---- Remote HQ another continent

      NGFW CLUSTER
                 |
                 +---- Remote Access VPN (MFA) ---- only managerial users
```

7.4 Diagramma PlantUML completo della versione 3-layer

```
@startuml
skinparam componentStyle rectangle
skinparam shadowing false
skinparam defaultTextAlignment left

cloud "Internet" as Internet
node "ISP CPE / ONT" as ISP
node "NGFW Cluster HA\nNAT / ACL / IPS\nRA VPN / S2S VPN" as FW
node "DMZ On-Site\nVLAN 130" as DMZ

node "Core Pair\nHigh-speed backbone" as CORE
node "Distribution A" as DISTA
node "Distribution B" as DISTB

node "Access Users" as ASW1
node "Access Office" as ASW2
node "Access Wireless" as ASW3
node "Access Spare / Expansion" as ASW4

node "Server / BigData Distribution" as SVD

node "Business App Servers\nVLAN 50" as APP
node "DBMS / SAP Backend\nVLAN 60" as DB
node "Reserved Document Server\nMgmt only\nVLAN 70" as DOC
database "MongoDB Document Store\nRBAC\nVLAN 80" as MDB
node "Management Network\nVLAN 110" as MGMT
node "NMS / SIEM / IDS Collector\nVLAN 120" as SEC
node "Big Data Cluster\n10 nodes\nVLAN 90/91/100" as BD

node "Reverse Proxy / WAF" as WAF
node "Public Web Server" as WEB
node "REST/SOAP Public Facade" as API

node "PTP Radio A" as PTA
node "PTP Radio B" as PTB
node "Secondary Dist/Access" as BR2
node "Secondary Users\nVLAN 150" as BUSER
node "Secondary Guest\nVLAN 160" as BGUEST
node "Secondary Mgmt\nVLAN 170" as BMGMT

node "Remote Main Site\nAnother Continent" as RHQ
actor "Managers Remote Users" as MGR

Internet -- ISP
ISP -- FW

FW -- DMZ
FW -- CORE
FW -- RHQ
FW -- MGR

DMZ -- WAF
DMZ -- WEB
DMZ -- API

CORE -- DISTA
CORE -- DISTB

DISTA -- ASW1
DISTA -- ASW2
DISTA -- ASW3
DISTB -- ASW4
DISTB -- SVD

SVD -- APP
SVD -- DB
SVD -- DOC
SVD -- MDB
SVD -- MGMT
SVD -- SEC
SVD -- BD

DISTB -- PTA
PTA -- PTB
PTB -- BR2
BR2 -- BUSER
BR2 -- BGUEST
BR2 -- BMGMT

note right of DISTA
L3 aggregation for campus blocks,
policy handoff toward core/firewall,
better modularity and scalability
end note

note right of FW
Main enforcement point for:
- Internet edge
- VPN access
- DMZ/Internal traffic
end note

note right of BD
Distributed internal big data platform
with separated access, data, and
management planes
end note
@enduml
```

7.5 Ruolo dei layer

Access:

* collega endpoint utente, AP, telefoni, periferiche
* applica VLAN, edge policy, eventuale NAC/802.1X
* PoE per AP e telefoni, se necessario

Distribution:

* aggrega i blocchi di accesso
* costituisce il confine L3 locale
* migliora modularità, fault isolation e scalabilità
* consente gateway ridondati, ACL locali e migliore controllo dei domini

Core:

* trasporto veloce e resiliente
* backbone interno
* minimo numero di policy applicative
* massima efficienza di forwarding

7.6 Cosa cambia rispetto al 2-layer

Restano invariati:

* DMZ
* VPN
* WiFi corporate e guest
* remote access solo per manager
* management network
* integrazione IDS/IPS con NMS
* cluster big data
* servizi cloud/serverless ibridi

Cambia:

* la gerarchia interna del campus
* la distribuzione delle funzioni L3
* la scalabilità
* la capacità di crescita ordinata su più edifici o blocchi

8. Cloud e servizi serverless ibridi

AWS documenta scenari in cui API Gateway funge da singolo punto di ingresso per workload ibridi e in cui API private possono essere raggiunte in modo controllato da reti on-prem tramite VPN site-to-site o Direct Connect. ([Amazon Web Services, Inc.][5])

Per la reference architecture si prevede:

In cloud:

* frontend pubblici
* API pubbliche cloud-native
* funzioni serverless
* eventuale orchestrazione applicativa

Interazione con on-site:

* alcune funzioni serverless invocano API on-site specifiche
* le API on-site esposte al cloud non sono “tutta la LAN”, ma solo servizi selezionati
* autenticazione forte tra cloud e on-prem
* logging e rate limiting
* preferenza per transitare attraverso API facade / gateway controllati

Diagramma logico sintetico del blocco cloud:

```
+------------------------- CLOUD PROVIDER -------------------------+
|                                                                 |
|   +------------------+      +-------------------------------+   |
|   | API Gateway      |----->| Serverless Functions          |   |
|   | public/private   |      | business logic / orchestration|   |
|   +------------------+      +-------------------------------+   |
|              |                             |                    |
|              +-----------------------------+                    |
|                              |                                  |
+------------------------------|----------------------------------+
                               |
                    Hybrid link / controlled VPN
                               |
                        +--------------+
                        | NGFW / DMZ   |
                        +--------------+
                               |
                    selected on-site APIs only
```

9. Rete di management: implementazione e motivazione

Questa parte va sempre esplicitata, perché nelle reti reali è essenziale.

Implementazione:

* management network separata, VLAN 110
* indirizzi dedicati per switch, AP, firewall, controller, sensori IDS, hypervisor, storage, iLO/iDRAC/IPMI
* accesso consentito solo da:

  * postazioni amministrative dedicate
  * jump host
  * eventuale VPN amministrativa distinta dalla VPN dei manager
* protocolli amministrativi solo sicuri
* firewall e ACL dedicate
* logging centralizzato

Motivazione:

* separare piano dati e piano di gestione
* ridurre rischio di compromissione laterale
* migliorare auditabilità
* semplificare troubleshooting e change management
* evitare che utenti normali possano anche solo raggiungere gli indirizzi di gestione degli apparati

In altre parole, la rete di management non è “una VLAN in più”: è un dominio separato, con un livello di esposizione molto più basso.

10. IDS/IPS, NMS e piattaforma security

Integrazione realistica:

* NGFW con IPS inline
* sensore NIDS per traffico est-ovest critico
* NMS per availability, inventory, performance, syslog, SNMPv3, telemetria
* piattaforma security per eventi IDS/IPS, log, correlazione
* dashboard condivise o integrate tra monitoraggio operativo e monitoraggio di sicurezza

Snort e Wazuh, sulla base della documentazione ufficiale verificata, sono riferimenti adatti per giustificare un’architettura di questo tipo. ([Snort][3])

11. Big data interno

HDFS è un filesystem distribuito progettato per cluster e grandi dataset; la documentazione ufficiale Hadoop giustifica quindi una rete pensata per traffico intenso tra nodi e separazione topologica dei piani di comunicazione. ([Apache Hadoop][4])

Scelta progettuale:

* circa 10 nodi
* 1 o 2 nodi di coordinamento / management
* resto nodi worker / data
* rete separata o fabric dedicata
* separazione:

  * ingest/client plane
  * data/replication plane
  * management plane
* uplink più veloci della LAN office ordinaria
* preferenza progettuale per 10/25 GbE sul blocco big data

Questa scelta è importante perché un cluster big data non deve contendere banda con il traffico degli utenti d’ufficio.

12. Confronto finale 2-layer vs 3-layer

2-layer:

* più semplice
* più leggibile
* meno costoso
* ideale come reference architecture standard per tracce d’esame
* realistico per organizzazioni medio-grandi ma non enormi

3-layer:

* più modulare
* più scalabile
* più adatto a campus grandi o multi-building
* migliore fault isolation
* più vicino ai campus enterprise più estesi

Conclusione pratica:

* usare il 2-layer come modello principale
* usare il 3-layer come variante evoluta per campus più ampi

13. Formula sintetica pronta da riusare

Versione 2-layer

L’architettura proposta è un campus 2-layer con access switch ridondati e collapsed core, protetto da cluster NGFW. La LAN è segmentata in VLAN separate per uffici, management utenti, WiFi corporate, WiFi guest, server interni, backend DB/SAP, documentale riservato management, MongoDB documentale ordinario, big data, security tools e management network. I servizi pubblici on-site sono pubblicati in DMZ tramite reverse proxy/WAF e API facade, senza esposizione diretta dei database interni. L’ufficio secondario a 600 metri viene collegato tramite ponte radio point-to-point in line-of-sight. La sede estera è collegata in site-to-site VPN. L’accesso remoto è consentito solo ai manager, tramite VPN con MFA e autorizzazione per gruppo. La rete di management è separata e accessibile solo da jump host amministrativi. IDS/IPS e NMS convergono su una piattaforma centralizzata di monitoraggio e sicurezza. Il cluster big data interno usa una rete server dedicata ad alta capacità per supportare il traffico distribuito tra i nodi. Questa impostazione è realistica, completa e didatticamente solida. ([Cisco][1])

Versione 3-layer

L’architettura proposta è un campus 3-layer con access, distribution e core separati. La segmentazione logica, i servizi pubblici e interni, le policy di sicurezza, la DMZ, la VPN intersede, il remote access per i soli manager, la management network, l’integrazione IDS/IPS-NMS e il cluster big data restano invariati rispetto alla versione 2-layer. La differenza principale è la presenza del distribution layer, che aggrega i blocchi di accesso, costituisce il confine L3 locale e migliora scalabilità, modularità e isolamento dei guasti. Questa versione è preferibile in campus più grandi o multi-building, mentre la 2-layer resta in genere la scelta più lineare per organizzazioni meno estese. ([Cisco][1])

14. Alcuni riferimenti

Cisco - Campus LAN and Wireless LAN Solution Design Guide
[https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html](https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html)

Cisco - Campus Wired LAN Technology Design Guide
[https://www.cisco.com/c/dam/en/us/td/docs/solutions/CVD/Aug2014/CVD-CampusWiredLANDesignGuide-AUG14.pdf](https://www.cisco.com/c/dam/en/us/td/docs/solutions/CVD/Aug2014/CVD-CampusWiredLANDesignGuide-AUG14.pdf)

NIST - SP 800-41 Rev. 1 Guidelines on Firewalls and Firewall Policy
[https://csrc.nist.gov/pubs/sp/800/41/r1/final](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

AWS Compute Blog - Powering hybrid workloads with Amazon API Gateway
[https://aws.amazon.com/blogs/compute/powering-hybrid-workloads-with-amazon-api-gateway/](https://aws.amazon.com/blogs/compute/powering-hybrid-workloads-with-amazon-api-gateway/)

Apache Hadoop - HDFS Users Guide
[https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html)

Snort - official site
[https://www.snort.org/](https://www.snort.org/)

Wazuh - Network IDS integration
[https://documentation.wazuh.com/current/proof-of-concept-guide/integrate-network-ids-suricata.html](https://documentation.wazuh.com/current/proof-of-concept-guide/integrate-network-ids-suricata.html)

Nel messaggio successivo si può trasformare questo testo in una versione ancora più operativa, ad esempio:

* versione “soluzione modello da maturità” più sintetica
* versione con elenco dei flussi ammessi/negati tabellato
* versione con addressing plan dettagliato host/gateway/broadcast
* versione in file .md oppure .docx.

[1]: https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html "Design Zone - Campus LAN and Wireless LAN Solution Design Guide - Cisco"
[2]: https://csrc.nist.gov/pubs/sp/800/41/r1/final "SP 800-41 Rev. 1, Guidelines on Firewalls and Firewall Policy | CSRC"
[3]: https://www.snort.org/ "
      Snort - Network Intrusion Detection & Prevention System
  "
[4]: https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html "Apache Hadoop 3.3.5 – HDFS Users Guide"
[5]: https://aws.amazon.com/blogs/compute/powering-hybrid-workloads-with-amazon-api-gateway/ "Powering hybrid workloads with Amazon API Gateway | AWS Compute Blog"
