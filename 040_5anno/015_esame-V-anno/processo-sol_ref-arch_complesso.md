

# Materiale per tracce di Sistemi e Reti

## 1. Idea di base

Nell’esame di Stato non conviene progettare ogni volta tutto da zero.

Conviene conoscere quasi a memoria:

* una procedura di soluzione;
* una reference architecture a 2 livelli;
* una reference architecture a 3 livelli;
* gli elementi ricorrenti: VLAN, DMZ, firewall, Wi-Fi interno/guest, VPN, cloud, server interni, rete di management, monitoraggio, sicurezza, backup, accesso remoto.

Durante la prova si lavora soprattutto sulle differenze richieste dalla traccia.

NB questa è la versione dettagliata,  
è più dettagliata e complessa di quanto serve in esame,
ho prodotto una versione più semplice che dovrebbe essere ancora reperibile.

L'approccio consigliato è:
- per identificare carenze e imparare qualche concetto addizionale esaminare questa in prima istanza, senza scoraggiarsi , tenendo presente che è oltre il nostro livello di dettaglio e programma
- utilizzare poi la più semplice, richiedetela se non già condivisa

---

# 2. Processo di soluzione della traccia

## 2.1 Lettura iniziale della traccia

Leggere la traccia cercando subito:

* sedi presenti;
* numero di utenti;
* reparti aziendali;
* server interni;
* servizi pubblici esposti su Internet;
* vincoli di sicurezza;
* presenza di Wi-Fi;
* presenza di sedi remote;
* presenza di cloud;
* richieste di scalabilità;
* richieste di prestazioni elevate;
* dati riservati;
* accesso remoto dei dipendenti.

Obiettivo: distinguere ciò che è obbligatorio da ciò che è una scelta progettuale.

---

## 2.2 Identificazione delle zone di rete

Una rete aziendale realistica non è una sola LAN piatta.

Le zone più frequenti sono:

* collegamenti WAN;
* LAN utenti;
* LAN management;
* VLAN server interni;
* VLAN management;
* VLAN guest Wi-Fi;
* DMZ pubblica;
* collegamenti VPN;
* rete ufficio secondario.
* VLAN IoT/stampanti/dispositivi tecnici;
* rete backup;
* rete big data / elaborazione distribuita;
* cloud VPC/VNet;

L'ultimo, cloud VPC/VNet, non è nel nostro programma.
Cloud VPC/VNet è una rete privata virtuale creata dentro un cloud provider, è l’equivalente cloud di una rete aziendale interna, ma realizzata su infrastruttura cloud (AWS la chiama VPC, cioè Virtual Private Cloud, Azure la chiama VNet, cioè Virtual Network, Google Cloud usa il termine VPC). Serve per organizzare e proteggere le risorse cloud, ad esempio:  
- server virtuali;  
- database cloud;  
- funzioni serverless;  
- API gateway;  
- bilanciatori di carico;  
- subnet pubbliche e private;  
- regole firewall;  
- collegamenti VPN verso la sede aziendale.)  

---

## 2.3 Scelta tra architettura a 2 layers e 3 layers

Usare una rete a 2 layers quando:

* la sede è medio-piccola;
* gli armadi di rete sono pochi;
* il traffico interno è significativo ma non enorme;
* access e distribution possono essere accorpati;
* si vuole una soluzione più semplice da spiegare.  
  
Usare una rete a 3 layers quando:

* la sede è grande;
* ci sono molti switch access;
* ci sono più edifici o piani;
* il traffico interno è elevato;
* ci sono server farm, big data, storage, backup;
* serve alta disponibilità;
* è utile separare chiaramente access, distribution e core.

Il modello gerarchico access/distribution/core è una struttura classica del campus LAN:  
l’access collega gli endpoint,  
la distribution aggrega gli switch di accesso e può rappresentare il confine Layer 2/Layer 3,  
il core collega le diverse aree ad alte prestazioni.  

Cisco descrive la distribution come livello di aggregazione e confine tra dominio Layer 2 ISO/OSI di accesso e dominio Layer 3 ISO/OSI verso il resto della rete. ([Cisco][1])

---

## 2.4 Definizione delle VLAN

Una possibile struttura che include le tipologie di reti citate è la seguente

| VLAN | Nome                  | Uso                                             |
| ---: | --------------------- | ----------------------------------------------- |
|   10 | MANAGEMENT            | gestione switch, AP, firewall, server           |
|   20 | ADMIN                 | amministrazione, segreteria, uffici generali    |
|   30 | MANAGEMENT_USERS      | dirigenti / management aziendale                |
|   40 | DIPENDENTI            | normali dipendenti                              |
|   50 | GUEST_WIFI            | ospiti, solo Internet                           |
|   60 | SERVER_INTERNI        | server applicativi interni                      |
|   70 | DB                    | database interni                                |
|   80 | DOCUMENTALE_RISERVATO | documenti riservati management                  |
|   90 | DOCUMENTALE_GENERALE  | MongoDB / documenti non altamente confidenziali |
|  100 | SAP_ERP               | SAP o ERP aziendale                             |
|  110 | CUSTOM_BUSINESS       | applicativo aziendale custom                    |
|  120 | DMZ_ON_PREMISE        | servizi pubblici on-site                        |
|  130 | BIG_DATA              | cluster distribuito 10 nodi                     |
|  140 | BACKUP_STORAGE        | backup, NAS, repository                         |
|  150 | IOT_PRINT             | stampanti, IoT, dispositivi tecnici             |
|  160 | WIFI_CORPORATE        | dispositivi aziendali Wi-Fi                     |
|  170 | UFFICIO_SECONDARIO    | sede secondaria a 600 m                         |
|  180 | VPN_REMOTE_MANAGERS   | accesso remoto dei soli manager                 |


## Traccia esame

Normalmente avrete molte meno reti, ma sono molto probabili:

- una (V)LAN utenti  
- una (V)LAN server
- una (V)LAN DMZ
- una (V)LAN management
- una (V)LAN guest Wi-Fi (se Wi-Fi presente)

Più altre reti eventualmente specifiche alla traccia.

---

## 2.5 Regola fondamentale sui permessi

Non tutte le VLAN devono parlare con tutte le altre.

Schema consigliato:

| Da                 | Verso                        | Permesso                                         |
| ------------------ | ---------------------------- | ------------------------------------------------ |
| Dipendenti         | Internet                     | consentito filtrato                              |
| Guest Wi-Fi        | Internet                     | consentito, isolato                              |
| Guest Wi-Fi        | LAN interna                  | negato                                           |
| Dipendenti         | MongoDB documentale generale | consentito secondo RBAC                          |
| Dipendenti         | documentale riservato        | negato                                           |
| Management         | documentale riservato        | consentito                                       |
| Management         | SAP / ERP                    | consentito                                       |
| Management         | VPN remota                   | consentito con MFA                               |
| Normali dipendenti | VPN remota                   | negato                                           |
| Server applicativi | DB                           | consentito solo su porte necessarie              |
| DMZ                | DB interni                   | vietato direttamente, salvo API controllate      |
| Cloud serverless   | API on-site                  | consentito tramite canale sicuro/API gateway/VPN |
| Management network | apparati                     | consentito solo da postazioni amministrative     |
| Big data nodes     | tra loro                     | consentito ad alta banda                         |
| Big data           | DB/Storage                   | consentito solo dove necessario                  |

---

# 3. Reference architecture a 2 layers

## 3.1 Quando usarla

Questa architettura è adatta a una sede principale di dimensione media, con:

* alcuni switch di accesso;
* server interni;
* DMZ;
* Wi-Fi aziendale e guest;
* collegamento a ufficio secondario vicino;
* VPN verso sede estera;
* collegamento cloud;
* cluster big data interno di circa 10 nodi.

In una rete a 2 layers si hanno:

* Access layer: switch a cui si collegano utenti, AP, stampanti, telefoni, dispositivi;
* Collapsed core/distribution: coppia di switch Layer 3 centrali che aggregano tutto.

---

## 3.2 Schema logico a 2 layers

```
Internet
   |
Router ISP
   |
Firewall perimetrale / NGFW
   |
   +------------------ DMZ on-premise
   |                    - Web server pubblico
   |                    - API REST/SOAP gateway
   |                    - Reverse proxy / WAF
   |
   +------------------ VPN site-to-site sede estera
   |
   +------------------ VPN remote access manager
   |
   +------------------ Connessione cloud
   |                    - VPN IPsec o Direct Connect/ExpressRoute
   |                    - Cloud VPC/VNet
   |                    - servizi serverless
   |
Coppia switch L3 collapsed core/distribution
   |
   +------------------ Server interni
   |                    - DBMS
   |                    - SAP/ERP
   |                    - sistema custom
   |                    - documentale riservato
   |                    - MongoDB documentale generale
   |
   +------------------ Cluster Big Data 10 nodi
   |
   +------------------ Storage / backup
   |
   +------------------ Switch access piano 1
   |                    - utenti
   |                    - AP Wi-Fi
   |                    - stampanti
   |
   +------------------ Switch access piano 2
   |                    - utenti
   |                    - AP Wi-Fi
   |                    - IoT
   |
   +------------------ Ponte radio PTP 600 m
                        |
                     Ufficio secondario
                     - switch access
                     - utenti
                     - AP Wi-Fi aziendale
```

---

## 3.3 Spiegazione dei componenti

Il firewall perimetrale / NGFW separa Internet, DMZ, LAN interna, VPN e cloud. Deve applicare policy diverse per ogni zona. Può includere funzioni IDS/IPS, filtro applicativo, controllo URL, logging e VPN.

La DMZ contiene i servizi raggiungibili dall’esterno:

* web server pubblico;
* gateway API REST/SOAP;
* reverse proxy;
* WAF.

I database non devono stare normalmente in DMZ. Devono stare in una rete interna più protetta. Il server in DMZ può comunicare con server interni solo su porte strettamente necessarie.

Gli switch Layer 3 centrali fanno routing inter-VLAN, oppure il routing inter-VLAN può essere demandato al firewall. In una soluzione da esame è spesso preferibile dire che:

* il firewall controlla i passaggi tra zone con diverso livello di sicurezza;
* gli switch Layer 3 gestiscono l’instradamento interno ad alte prestazioni dove non ci sono separazioni critiche;
* le ACL sugli switch limitano comunque il traffico non necessario.

---

## 3.4 VLAN principali nella rete a 2 layers

```
VLAN 10  Management
VLAN 20  Amministrazione
VLAN 30  Management aziendale
VLAN 40  Dipendenti
VLAN 50  Guest Wi-Fi
VLAN 60  Server applicativi
VLAN 70  Database
VLAN 80  Documentale riservato
VLAN 90  MongoDB documentale generale
VLAN 100 SAP/ERP
VLAN 110 Applicativo custom
VLAN 120 DMZ on-premise
VLAN 130 Big Data
VLAN 140 Backup/Storage
VLAN 150 IoT/Stampanti
VLAN 160 Wi-Fi corporate
VLAN 170 Ufficio secondario
VLAN 180 VPN manager
```

---

## 3.5 Wi-Fi interno e guest

La rete Wi-Fi deve usare almeno due SSID:

| SSID                          | VLAN | Accesso                     |
| ----------------------------- | ---: | --------------------------- |
| Azienda-Corporate             |  160 | LAN aziendale secondo ruolo |
| Azienda-Guest                 |   50 | solo Internet               |
| Azienda-Management, opzionale |   30 | solo manager autorizzati    |

Gli access point aziendali sono collegati agli switch access tramite trunk 802.1Q. Ogni SSID viene associato a una VLAN.

Il Wi-Fi guest non deve poter accedere a server interni, stampanti aziendali, apparati di rete o management network.

---

## 3.6 Ufficio secondario a 600 metri

Poiché l’ufficio secondario è in line-of-sight a circa 600 metri, si può usare un ponte radio punto-punto.

Schema:

```
Sede principale
   |
Switch L3 centrale
   |
VLAN trunk verso apparato radio PTP
   |
Collegamento radio direzionale 600 m
   |
Apparato radio PTP ufficio secondario
   |
Switch access ufficio secondario
   |
Utenti / AP / stampanti
```

Il ponte radio deve essere:

* cifrato;
* configurato con antenne direzionali;
* monitorato;
* protetto fisicamente;
* preferibilmente ridondato se la continuità è critica.

L’ufficio secondario può usare VLAN proprie oppure estendere alcune VLAN dalla sede principale. In un progetto scolastico è più pulito assegnare subnet dedicate all’ufficio secondario e instradarle centralmente.

---

## 3.7 Sede principale in altro continente

La sede in altro continente deve collegarsi tramite VPN site-to-site.

Schema:

```
Sede principale Italia
   |
Firewall NGFW
   |
Internet
   |
Tunnel IPsec site-to-site
   |
Firewall sede estera
   |
LAN sede estera
```

La VPN site-to-site deve cifrare il traffico tra le due sedi. Le rotte devono permettere solo le comunicazioni necessarie.

Esempi:

* sede estera verso SAP/ERP;
* sede estera verso applicativi business;
* sede estera verso documentale generale;
* eventuale accesso management solo da amministratori autorizzati;
* nessun accesso diretto non necessario ai database.

---

## 3.8 Accesso remoto dei soli manager

La richiesta dice: tutti e soli i dipendenti di livello manageriale devono lavorare remotamente.

Soluzione:

* VPN remote access sul firewall o su concentratore VPN;
* autenticazione con MFA;
* gruppo directory “Managers”;
* accesso consentito solo a utenti nel gruppo manageriale;
* profilo VPN separato;
* log degli accessi;
* accesso limitato ai soli servizi necessari.

Schema:

```
Manager remoto
   |
Client VPN + MFA
   |
Internet
   |
Firewall aziendale
   |
VLAN 180 VPN_REMOTE_MANAGERS
   |
Servizi autorizzati:
- SAP/ERP
- documentale riservato
- applicativo custom
- documentale generale
```

I normali dipendenti non devono avere profilo VPN di accesso remoto.

---

## 3.9 Cloud serverless collegato all’on-premise

L’organizzazione espone anche servizi pubblici su cloud con approccio serverless.

Esempio logico:

```
Utente Internet
   |
API Gateway cloud
   |
Funzioni serverless
   |
Connessione sicura cloud-on-premise
   |
API gateway on-premise / reverse proxy
   |
Servizi REST/SOAP interni
   |
DB o sistemi aziendali
```

Il cloud non deve accedere liberamente alla LAN interna. Deve invocare solo endpoint esposti in modo controllato.

Soluzioni possibili:

* VPN site-to-site tra cloud VPC/VNet e sede;
* collegamento dedicato tipo AWS Direct Connect / Azure ExpressRoute;
* API gateway;
* autenticazione forte tra servizi;
* allowlist degli indirizzi sorgente;
* logging centralizzato.

AWS documenta l’uso di Direct Connect e VPN IPsec per connettività ibrida tra ambienti on-premise e cloud; Direct Connect fornisce una connessione dedicata, mentre IPsec VPN può essere usata per cifratura o collegamenti a minore banda. ([AWS Documentation][2])

---

## 3.10 Rete di management

La rete di management serve per amministrare:

* switch;
* firewall;
* access point;
* server;
* storage;
* hypervisor;
* apparati radio;
* sistemi di monitoraggio.

Deve essere separata dalla rete utenti.

Implementazione consigliata:

```
VLAN 10 MANAGEMENT
   |
Accesso consentito solo da:
   - postazioni amministratori IT
   - jump server / bastion host
   - NMS
   - server logging/SIEM
   |
Accesso negato da:
   - guest Wi-Fi
   - dipendenti normali
   - server pubblici in DMZ
   - dispositivi IoT
```

Motivazione:

* riduce il rischio che un normale client compromesso possa configurare apparati;
* centralizza gli accessi amministrativi;
* consente logging e controllo;
* facilita backup configurazioni;
* permette monitoraggio con NMS.

Per maggiore sicurezza, la rete di management può essere:

* una VLAN dedicata;
* instradata solo dal firewall;
* accessibile solo da jump server;
* protetta con ACL;
* monitorata da IDS/NMS;
* separata fisicamente nei casi più critici.

---

## 3.11 IDS/IPS integrati con NMS

Il sistema deve prevedere:

* IDS/IPS sul firewall perimetrale;
* sensori IDS nelle zone interne più critiche;
* NMS per monitoraggio apparati;
* SIEM o sistema di logging centralizzato;
* alert automatici.

Schema:

```
Firewall / NGFW con IPS
   |
Log / eventi
   |
SIEM / Log server
   |
NMS
   |
Alert amministratori
```

Possibili punti di controllo:

* traffico Internet-DMZ;
* traffico DMZ-LAN;
* traffico VPN-LAN;
* traffico cloud-on-premise;
* traffico verso server critici;
* traffico anomalo nel cluster big data.

---

## 3.12 Big data interno con 10 nodi

Il cluster big data interno genera traffico elevato tra nodi e verso storage.

Requisiti:

* VLAN o subnet dedicata;
* switch ad alte prestazioni;
* collegamenti almeno 10 Gbit/s per i nodi;
* uplink aggregati verso core/distribution;
* bassa latenza;
* separazione dal traffico utenti;
* accesso controllato ai dati;
* storage adeguato;
* backup separato.

Schema:

```
Coppia switch L3 centrale
   |
Switch ToR / aggregation Big Data 10/25 Gbit/s
   |
+---- Nodo 1
+---- Nodo 2
+---- Nodo 3
+---- ...
+---- Nodo 10
   |
Storage / backup dedicato
```

Il traffico del cluster non deve saturare la rete utenti. Per questo si usa una rete dedicata o almeno una VLAN dedicata con uplink ad alta capacità.

---

# 4. Reference architecture a 3 layers

## 4.1 Quando usarla

Questa architettura è adatta a una sede più grande, con:

* molti utenti;
* più piani o edifici;
* server farm interna;
* DMZ;
* cluster big data;
* rete di management;
* alta disponibilità;
* collegamenti WAN;
* cloud ibrido;
* sede estera.

I tre livelli sono:

* access layer;
* distribution layer;
* core layer.

---

## 4.2 Schema logico a 3 layers

```
Internet
   |
Router ISP
   |
Coppia firewall NGFW in HA
   |
   +------------------ DMZ pubblica
   |                    - WAF / reverse proxy
   |                    - Web server pubblico
   |                    - API REST/SOAP gateway
   |
   +------------------ VPN remote manager
   |
   +------------------ VPN site-to-site sede estera
   |
   +------------------ Cloud VPC/VNet
   |                    - API Gateway
   |                    - funzioni serverless
   |                    - VPN / Direct Connect
   |
Core layer ridondato
   |
   +------------------ Distribution block utenti edificio A
   |                       |
   |                    Access switch
   |                    AP Wi-Fi
   |                    utenti
   |
   +------------------ Distribution block utenti edificio B
   |                       |
   |                    Access switch
   |                    AP Wi-Fi
   |                    stampanti / IoT
   |
   +------------------ Distribution server farm
   |                       |
   |                    Server interni
   |                    DBMS
   |                    SAP/ERP
   |                    custom business
   |                    documentale
   |
   +------------------ Distribution big data
   |                       |
   |                    Cluster 10 nodi
   |                    Storage ad alte prestazioni
   |
   +------------------ Distribution management
   |                       |
   |                    NMS
   |                    SIEM
   |                    jump server
   |
   +------------------ Ponte radio PTP 600 m
                           |
                        Ufficio secondario
```

---

## 4.3 Funzione dei livelli

## Access layer

Collega dispositivi finali:

* PC;
* telefoni IP;
* stampanti;
* access point;
* dispositivi IoT;
* client aziendali.

Funzioni tipiche:

* porte access;
* trunk verso AP;
* PoE;
* autenticazione 802.1X se prevista;
* VLAN assignment;
* port security;
* DHCP snooping;
* storm control.

## Distribution layer

Aggrega gli switch access.

Funzioni tipiche:

* routing inter-VLAN locale;
* ACL;
* ridondanza;
* aggregazione uplink;
* confine dei domini Layer 2;
* policy tra VLAN;
* collegamento verso core.

## Core layer

È il backbone veloce della rete.

Funzioni tipiche:

* trasporto ad alte prestazioni;
* ridondanza;
* bassa latenza;
* collegamento tra distribution block;
* collegamento verso firewall, data center, cloud e WAN.

Nel core si evitano regole troppo complesse. Le policy di sicurezza principali sono applicate su firewall, distribution e sistemi dedicati.

---

## 4.4 Server farm interna

La server farm interna contiene:

* DBMS;
* SAP/ERP;
* applicativo business custom;
* server documentale riservato;
* MongoDB documentale generale;
* server autenticazione/directory;
* backup;
* logging;
* NMS;
* eventuale virtualizzazione.

Schema:

```
Distribution server farm
   |
VLAN 60  Server applicativi
VLAN 70  Database
VLAN 80  Documentale riservato
VLAN 90  Documentale generale MongoDB
VLAN 100 SAP/ERP
VLAN 110 Custom business
VLAN 140 Backup/Storage
```

Regola progettuale: separare applicazioni, database, documentale, backup e management, perché hanno livelli di criticità diversi.

---

## 4.5 DMZ nella rete a 3 layers

La DMZ deve stare dietro firewall, non direttamente nella LAN.

Schema:

```
Internet
   |
Firewall HA
   |
DMZ
   |
- WAF
- reverse proxy
- web server pubblico
- API gateway REST/SOAP on-premise
```

Comunicazioni consentite:

| Da          | A                 | Regola                                  |
| ----------- | ----------------- | --------------------------------------- |
| Internet    | WAF/reverse proxy | HTTPS                                   |
| WAF         | web server        | HTTPS interno                           |
| API gateway | servizi interni   | solo API necessarie                     |
| DMZ         | DB interni        | vietato o fortemente limitato           |
| LAN interna | DMZ               | solo amministrazione controllata        |
| Management  | DMZ               | solo amministratori tramite jump server |

---

## 4.6 Cloud serverless nella rete a 3 layers

Schema:

```
Internet
   |
Cloud provider
   |
API Gateway cloud
   |
Funzioni serverless
   |
VPC/VNet privata
   |
VPN / Direct Connect / ExpressRoute
   |
Firewall aziendale
   |
API gateway on-premise
   |
Servizi REST/SOAP interni
```

Principio importante: il cloud non deve entrare liberamente nella LAN. Deve invocare endpoint specifici, autenticati, tracciati e filtrati.

NIST descrive lo Zero Trust come un approccio che sposta il focus dal semplice perimetro di rete alla protezione di utenti, asset e risorse; per un’architettura ibrida è quindi corretto controllare identità, dispositivo, applicazione, dati e policy, non solo “da dove arriva il pacchetto”. ([csrc.nist.gov][3])

---

## 4.7 Big data nella rete a 3 layers

Nell’architettura a 3 layers il cluster big data deve essere trattato quasi come una piccola server farm ad alte prestazioni.

Schema:

```
Core layer
   |
Distribution big data
   |
Switch dedicati 10/25 Gbit/s
   |
10 nodi big data
   |
Storage / data lake interno / backup
```

Scelte consigliate:

* rete dedicata per traffico tra nodi;
* uplink ridondati;
* almeno 10 Gbit/s per nodo;
* storage separato o rete storage dedicata;
* QoS se necessario;
* monitoraggio del traffico;
* accesso degli utenti solo tramite applicazioni o gateway;
* accesso amministrativo solo da VLAN management.

---

## 4.8 Management network nella rete a 3 layers

Implementazione consigliata:

```
VLAN 10 MANAGEMENT
   |
Distribution management
   |
Jump server / bastion host
   |
NMS
   |
SIEM / log server
   |
Backup configurazioni
   |
Accesso agli apparati:
   - switch access
   - switch distribution
   - core
   - firewall
   - AP
   - server
   - storage
   - radio PTP
```

La rete di management può essere:

* in-band, cioè passa sugli stessi apparati ma in VLAN separata;
* out-of-band, cioè usa una rete fisicamente separata per apparati critici.

Per una traccia d’esame si può scrivere:

“Si prevede una VLAN di management separata, raggiungibile solo da postazioni amministrative e da un jump server. Gli apparati espongono le interfacce di gestione solo su tale VLAN. L’accesso è protetto da ACL, autenticazione forte e logging centralizzato. In ambienti ad alta criticità si può prevedere una rete out-of-band fisicamente separata.”

---

# 5. Confronto tra 2 layers e 3 layers

| Aspetto              | 2 layers                   | 3 layers           |
| -------------------- | -------------------------- | ------------------ |
| Complessità          | minore                     | maggiore           |
| Costo                | minore                     | maggiore           |
| Scalabilità          | media                      | alta               |
| Prestazioni interne  | buone                      | migliori           |
| Ridondanza           | possibile                  | più strutturata    |
| Adatta a             | sedi medio-piccole         | sedi grandi/campus |
| Spiegazione in esame | più semplice               | più professionale  |
| Big data interno     | possibile, ma più delicato | più naturale       |
| Molti edifici/piani  | meno adatta                | più adatta         |

---

# 6. Formula riutilizzabile da scrivere nella soluzione

Una possibile frase standard:

“La rete viene progettata secondo un modello gerarchico, separando le funzioni di accesso, aggregazione, sicurezza, server farm, DMZ, management e collegamenti geografici. Le VLAN permettono di isolare reparti, server, ospiti, dispositivi tecnici e traffico amministrativo. Il traffico tra zone con diverso livello di sicurezza viene filtrato da firewall/ACL. I servizi pubblici sono collocati in DMZ o nel cloud, mentre i database e i sistemi interni rimangono in reti protette. L’accesso remoto è consentito solo ai manager tramite VPN con autenticazione forte. La rete di management è separata e accessibile solo agli amministratori autorizzati.”

---

# 7. Cosa imparare quasi a memoria

Gli studenti dovrebbero memorizzare almeno:

* differenza tra LAN, VLAN, DMZ, WAN, VPN, cloud;
* struttura access/distribution/core;
* struttura access/collapsed core;
* ruolo del firewall;
* ruolo della DMZ;
* perché i database non vanno esposti direttamente;
* perché il guest Wi-Fi deve essere isolato;
* perché la rete di management deve essere separata;
* differenza tra VPN remote access e site-to-site;
* differenza tra server pubblici e server interni;
* differenza tra servizi on-premise e cloud serverless;
* necessità di IDS/IPS, NMS, logging e backup;
* requisiti di rete per cluster big data.

---

## Alcuni riferimenti

Cisco Campus LAN and Wireless LAN Solution Design Guide
[https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html](https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html)

NIST SP 800-207 Zero Trust Architecture
[https://csrc.nist.gov/pubs/sp/800/207/final](https://csrc.nist.gov/pubs/sp/800/207/final)

CISA Zero Trust Maturity Model
[https://www.cisa.gov/zero-trust-maturity-model](https://www.cisa.gov/zero-trust-maturity-model)

AWS Direct Connect and IPSec VPN
[https://docs.aws.amazon.com/wellarchitected/latest/hybrid-networking-lens/aws-direct-connect-and-ipsec-vpn.html](https://docs.aws.amazon.com/wellarchitected/latest/hybrid-networking-lens/aws-direct-connect-and-ipsec-vpn.html)

[1]: https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html?utm_source=chatgpt.com "Campus LAN and Wireless LAN Solution Design Guide"
[2]: https://docs.aws.amazon.com/wellarchitected/latest/hybrid-networking-lens/aws-direct-connect-and-ipsec-vpn.html?utm_source=chatgpt.com "AWS Direct Connect and IPSec VPN"
[3]: https://csrc.nist.gov/pubs/sp/800/207/final?utm_source=chatgpt.com "SP 800-207, Zero Trust Architecture | CSRC"
