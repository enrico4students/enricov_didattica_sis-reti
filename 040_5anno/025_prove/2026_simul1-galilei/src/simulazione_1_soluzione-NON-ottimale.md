Si propone di seguito uno svolgimento completo della traccia utilizzando **una architettura a tre livelli (3-layer architecture)**.
È importante chiarire fin dall’inizio che **questa scelta non è la più ottimale per il problema**, ma viene adottata **esclusivamente per finalità didattiche**, per mostrare in modo esplicito il ruolo dei tre livelli classici delle reti enterprise: access layer, distribution layer e core layer.

In una soluzione reale, considerata la dimensione relativamente contenuta della struttura alberghiera e il numero limitato di segmenti di rete, sarebbe più appropriata una **architettura a due livelli (access + core/distribution)**. L’introduzione di un distribution layer separato non è strettamente necessaria e introduce complessità aggiuntiva senza portare benefici proporzionati.

La soluzione che segue è quindi volutamente più articolata del necessario per consentire di analizzare e comprendere meglio la struttura gerarchica delle reti aziendali.

---

# Soluzione

# 1. Impostazione generale del progetto

## 1.1 Architettura di rete adottata

La rete viene progettata utilizzando una **architettura gerarchica a tre livelli** composta da:

access layer
distribution layer
core layer

Questa architettura è tipica delle **reti campus enterprise**, dove la presenza di numerosi edifici, centinaia o migliaia di dispositivi e traffico elevato rende necessario separare chiaramente le funzioni dei vari livelli.

Nel caso della struttura alberghiera descritta nella traccia, tale architettura non rappresenta la scelta più efficiente. La rete non ha dimensioni tali da richiedere un livello di aggregazione separato tra accesso e dorsale. Una soluzione a due livelli sarebbe più semplice, meno costosa e più facile da amministrare.

L’architettura a tre livelli viene quindi adottata **solo per rendere esplicita la struttura gerarchica della rete** e permettere di analizzare con chiarezza il ruolo dei diversi livelli.

---

# 2. Ruolo dei tre livelli della rete

## 2.1 Access layer

L’access layer è il livello più vicino agli utenti e ai dispositivi finali.

Gli switch di accesso collegano direttamente:

PC degli uffici amministrativi
postazioni della reception
terminali del personale
stampanti di rete
access point Wi-fi
terminali di servizio
dispositivi tecnici e infrastrutturali

Ogni porta degli switch di accesso viene configurata in una VLAN specifica, in modo da separare logicamente i diversi tipi di traffico.

L’access layer non svolge funzioni di routing. Il suo compito principale è fornire connettività ai dispositivi finali e trasportare il traffico verso il livello superiore.

---

## 2.2 Distribution layer

Il distribution layer raccoglie il traffico proveniente dagli switch di accesso.

In una architettura enterprise tipica questo livello svolge diverse funzioni:

aggregazione degli access switch
routing inter-VLAN
applicazione di policy e filtri
gestione delle liste di controllo accessi
sintesi delle rotte verso il core

Nel caso della rete descritta nella traccia, però, **questo livello non è strettamente necessario**.

La struttura non presenta un numero elevato di switch di accesso né un traffico tale da richiedere un livello di aggregazione separato. Inoltre, per motivi di sicurezza, il routing tra le VLAN viene affidato al firewall/UTM.

Questo significa che il distribution layer svolge principalmente una funzione di **aggregazione dei collegamenti**, rendendo evidente la struttura gerarchica della rete ma senza essere realmente indispensabile.

---

## 2.3 Core layer

Il core layer rappresenta la dorsale centrale della rete.

Il suo compito è:

trasportare il traffico tra le varie aree della rete
garantire elevate prestazioni
fornire un punto centrale di interconnessione tra i diversi blocchi della rete

In reti campus molto grandi il core deve essere progettato per fornire throughput elevato e ridondanza.

Nel caso di questa rete, la presenza di un core separato è utile soprattutto a scopo didattico. In una rete reale di queste dimensioni il core e il distribution layer potrebbero essere unificati in un unico livello.

---

# 3. Collegamento a Internet

La struttura è collegata a Internet tramite una connessione **FTTH (Fiber To The Home)**.

Il collegamento segue la sequenza:

Internet
ONT/CPE dell’operatore
firewall / UTM
core switch

L’ONT (Optical Network Terminal) converte il segnale ottico della rete GPON dell’operatore in interfaccia Ethernet.

Il firewall/UTM rappresenta il vero punto di frontiera della rete e svolge diverse funzioni fondamentali:

NAT verso Internet
filtraggio del traffico
terminazione VPN
routing tra le VLAN interne
protezione della DMZ
monitoraggio e logging della rete

Il firewall costituisce quindi il principale elemento di sicurezza dell’infrastruttura.

---

# 4. Segmentazione della rete tramite VLAN

Per migliorare sicurezza e organizzazione della rete si utilizza una segmentazione logica basata su VLAN.

Ogni VLAN rappresenta una rete logica separata.

VLAN 10 – UFFICI
VLAN 20 – SERVIZI INTERNI
VLAN 30 – SALE CONVEGNI
VLAN 40 – OSPITI HOTEL
VLAN 50 – OSPITI SPIAGGIA
VLAN 60 – COLONNINE DI RICARICA
VLAN 70 – DMZ
VLAN 80 – MANAGEMENT
VLAN 90 – STAFF STABILIMENTO

La separazione in VLAN permette di isolare il traffico tra le diverse categorie di utenti e di applicare regole di sicurezza specifiche.

---

# 5. Piano di indirizzamento IP

Si utilizza uno spazio di indirizzamento privato.

VLAN 10 UFFICI
rete 10.10.10.0/24

VLAN 20 SERVIZI
rete 10.10.20.0/24

VLAN 30 CONVEGNI
rete 10.10.30.0/24

VLAN 40 OSPITI HOTEL
rete 10.10.40.0/24

VLAN 50 OSPITI SPIAGGIA
rete 10.10.50.0/24

VLAN 60 COLONNINE EV
rete 10.10.60.0/24

VLAN 70 DMZ
rete 10.10.70.0/24

VLAN 80 MANAGEMENT
rete 10.10.80.0/24

VLAN 90 STAFF STABILIMENTO
rete 10.10.90.0/24

Questo schema mantiene una struttura semplice e facilmente leggibile.

---

# 6. Routing tra le VLAN

Il routing tra le VLAN non viene affidato agli switch ma al firewall.

Questo consente di applicare controlli di sicurezza più precisi tra le diverse reti.

Il firewall diventa quindi il gateway delle varie VLAN.

Esempio:

10.10.10.1 gateway VLAN uffici
10.10.20.1 gateway VLAN servizi
10.10.40.1 gateway rete ospiti

Questo approccio migliora il controllo dei flussi tra reti con diverso livello di fiducia.

---

# 7. Collegamento dello stabilimento balneare

Lo stabilimento balneare si trova a circa **500 metri dall’hotel** ed è visibile dalla terrazza della struttura.

Per collegare le due strutture si utilizza un **ponte radio punto-punto**.

Il collegamento consiste in:

bridge radio lato hotel
bridge radio lato stabilimento

Il collegamento trasporta più VLAN tramite trunk 802.1Q.

In particolare:

VLAN 50 ospiti spiaggia
VLAN 90 personale stabilimento

Il personale dello stabilimento può accedere al software gestionale dell’hotel, mentre gli ospiti possono utilizzare la rete Wi-Fi per accedere a Internet.

---

# 8. Servizi di rete

## DHCP

Il servizio DHCP assegna automaticamente gli indirizzi IP ai dispositivi delle varie VLAN.

Può essere collocato nella VLAN servizi.

Il firewall inoltra le richieste DHCP delle varie VLAN tramite relay.

---

## Wi-Fi

Gli access point dell’hotel e dello stabilimento forniscono connettività wireless agli ospiti.

Gli SSID sono separati per:

rete ospiti hotel
rete ospiti spiaggia
rete staff

Ogni SSID viene associato alla VLAN corrispondente.

---

# 9. DMZ

La DMZ ospita i servizi accessibili da Internet.

Nella DMZ si colloca il Web server dell’hotel.

Il database rimane invece nella rete interna protetta.

Le regole di sicurezza sono:

Internet può accedere al Web server solo su porte 80 e 443
Internet non può accedere al database
il Web server può accedere al database solo sulle porte applicative necessarie

Questa configurazione riduce il rischio che un attacco proveniente da Internet comprometta i sistemi interni.

---

# 10. Regole di sicurezza principali

Le politiche di sicurezza prevedono:

gli ospiti possono accedere solo a Internet
gli ospiti non possono accedere alla rete uffici
gli ospiti non possono accedere alla rete management
il personale autorizzato può accedere ai server interni
lo stabilimento può accedere al gestionale dell’hotel

Queste regole vengono implementate sul firewall.

---

# 11. Valutazione della soluzione

La soluzione proposta è tecnicamente valida e rispetta tutti i requisiti della traccia.

Tuttavia l’architettura a tre livelli risulta **più complessa del necessario**.

Le principali criticità sono:

maggiore numero di apparati
maggiore complessità di configurazione
costi più elevati
benefici limitati per una rete di dimensioni moderate

Una soluzione a due livelli avrebbe consentito di ottenere gli stessi risultati con una infrastruttura più semplice.

---

# 12. Conclusione

La rete è stata progettata utilizzando una architettura gerarchica a tre livelli composta da access layer, distribution layer e core layer.

Questa scelta è stata fatta a scopo didattico per mostrare chiaramente la struttura delle reti enterprise.

Dal punto di vista pratico, una architettura a due livelli sarebbe stata più adatta alle dimensioni della rete della struttura alberghiera.

La soluzione proposta garantisce comunque:

segmentazione della rete tramite VLAN
protezione tramite firewall e DMZ
collegamento sicuro dello stabilimento balneare
accesso controllato ai servizi interni
connettività Internet per ospiti e personale

ed è quindi pienamente funzionale e coerente con i requisiti della traccia.

---

# diagramma dettagliato

    @startuml
    title Struttura alberghiera con stabilimento balneare - Architettura 3 layer didattica

    left to right direction
    skinparam backgroundColor white
    skinparam shadowing false
    skinparam linetype ortho
    skinparam packageStyle rectangle
    skinparam roundcorner 18
    skinparam nodesep 40
    skinparam ranksep 35
    skinparam defaultTextAlignment center

    skinparam rectangle {
    BorderColor #333333
    FontColor #111111
    FontSize 15
    }

    skinparam cloud {
    BorderColor #333333
    FontColor #111111
    FontSize 15
    }

    skinparam database {
    BorderColor #333333
    FontColor #111111
    FontSize 14
    }

    skinparam note {
    BackgroundColor #FFF8DC
    BorderColor #B8860B
    FontSize 13
    }

    cloud "Internet" as INTERNET #DDEBF7
    rectangle "ONT / CPE FTTH\nTerminazione operatore" as CPE #E2F0D9

    rectangle "Firewall / UTM\nNAT - ACL - VPN - Routing inter-VLAN\nControllo accessi tra reti" as FW #F4CCCC

    package "DMZ" #FCE4D6 {
    rectangle "Web Server\nHTTPS 443 / HTTP 80" as WEB
    }

    package "Core Layer\nDidattico: separato ma non strettamente necessario" #D9EAD3 {
    rectangle "Core Switch\nBackbone centrale" as CORE
    }

    package "Distribution Layer" #FFF2CC {
    rectangle "Distribution Switch Hotel\nAggregazione area hotel" as DIST_H
    rectangle "Distribution Switch Remoto\nAggregazione collegamento stabilimento" as DIST_R
    }

    package "Access Layer - Hotel" #D9EAF7 {
    rectangle "Access Switch Uffici / Reception" as ACC_OFF
    rectangle "Access Switch Sale Convegni" as ACC_CONF
    rectangle "Access Switch Servizi / Tecnici" as ACC_SRV
    rectangle "Access Switch Wi-Fi Hotel" as ACC_WIFI_H
    }

    package "Access Layer - Stabilimento" #EADCF8 {
    rectangle "Access Switch Stabilimento" as ACC_BEACH
    rectangle "Bridge Radio PTP\nlato Hotel" as BR_H
    rectangle "Bridge Radio PTP\nlato Stabilimento" as BR_B
    }

    package "Server e servizi interni" #E2F0D9 {
    rectangle "Server Gestionale Hotel\nVLAN 20 - 10.10.20.10" as APP
    rectangle "DHCP / DNS / RADIUS / Wi-Fi Controller\nVLAN 20" as INFRA
    database "RDBMS\nVLAN 20 - 10.10.20.20" as DB
    rectangle "Management / Monitoraggio\nVLAN 80" as MGMT
    }

    package "Dispositivi finali hotel" #F3F3F3 {
    rectangle "PC Uffici\nVLAN 10" as PC_OFF
    rectangle "Reception / Terminali gestionali\nVLAN 10" as RECEPT
    rectangle "Sale convegni\nprese dati / apparati\nVLAN 30" as CONF_DEV
    rectangle "Access Point Ospiti Hotel\nSSID hotel_guest\nVLAN 40" as AP_H_GUEST
    rectangle "Access Point Staff / Tecnici\nSSID staff\nVLAN 10/80" as AP_H_STAFF
    rectangle "Colonnine EV\nVLAN 60" as EV
    }

    package "Dispositivi finali stabilimento" #F3F3F3 {
    rectangle "Postazioni personale stabilimento\nVLAN 90" as STAFF_BEACH
    rectangle "Access Point Ospiti Spiaggia\nSSID beach_guest\nVLAN 50" as AP_BEACH
    }

    INTERNET -down- CPE : WAN
    CPE -down- FW : Ethernet WAN

    FW -left- WEB : zona DMZ
    FW -down- CORE : trunk 802.1Q\nVLAN 10,20,30,40,50,60,80,90

    CORE -down- DIST_H : trunk 802.1Q
    CORE -down- DIST_R : trunk 802.1Q

    DIST_H -down- ACC_OFF : trunk 802.1Q
    DIST_H -down- ACC_CONF : trunk 802.1Q
    DIST_H -down- ACC_SRV : trunk 802.1Q
    DIST_H -down- ACC_WIFI_H : trunk 802.1Q
    DIST_R -down- BR_H : trunk 802.1Q\nVLAN 50,90

    BR_H .. BR_B : ponte radio punto-punto\n500 m LOS
    BR_B -down- ACC_BEACH : trunk 802.1Q\nVLAN 50,90

    ACC_OFF -down- PC_OFF : access VLAN 10
    ACC_OFF -down- RECEPT : access VLAN 10

    ACC_CONF -down- CONF_DEV : access VLAN 30

    ACC_SRV -down- APP : access VLAN 20
    ACC_SRV -down- INFRA : access VLAN 20
    ACC_SRV -down- DB : access VLAN 20
    ACC_SRV -down- MGMT : access VLAN 80
    ACC_SRV -down- EV : access VLAN 60

    ACC_WIFI_H -down- AP_H_GUEST : trunk/AP multi-SSID\nVLAN 40
    ACC_WIFI_H -down- AP_H_STAFF : trunk/AP multi-SSID\nVLAN 10,80

    ACC_BEACH -down- STAFF_BEACH : access VLAN 90
    ACC_BEACH -down- AP_BEACH : trunk/AP multi-SSID\nVLAN 50

    WEB .. DB : solo traffico applicativo consentito
    STAFF_BEACH .. APP : accesso consentito al gestionale
    AP_H_GUEST .. INTERNET : solo Internet tramite firewall
    AP_BEACH .. INTERNET : solo Internet tramite firewall

    note right of FW
    Il firewall resta il punto centrale
    per routing inter-VLAN e sicurezza.
    In una vera soluzione 3 layer,
    parte del routing potrebbe stare
    nel distribution layer, ma qui
    si preferisce mantenerlo sul firewall
    per controllare meglio i flussi.
    end note

    note bottom of CORE
    Core separato inserito solo
    a fini didattici.
    Per questa traccia un core distinto
    porta benefici limitati.
    end note

    note bottom of DIST_H
    Distribution layer usato per mostrare
    l'aggregazione degli access switch.
    Nella traccia reale non è
    strettamente necessario.
    end note

    note right of DIST_R
    Raccoglie il traffico
    proveniente dallo stabilimento.
    Anche questo livello è
    più didattico che necessario.
    end note

    legend right
    |= Colore |= Significato |
    |<#F4CCCC>| Firewall / sicurezza perimetrale |
    |<#FCE4D6>| DMZ |
    |<#D9EAD3>| Core layer e servizi interni |
    |<#FFF2CC>| Distribution layer |
    |<#D9EAF7>| Access layer hotel |
    |<#EADCF8>| Access layer / collegamento stabilimento |
    |<#F3F3F3>| Dispositivi finali |
    ----
    Linea continua: collegamento Ethernet
    Linea tratteggiata: traffico logico / radio / flusso applicativo
    Testo "trunk 802.1Q": collegamento con più VLAN
    Testo "access VLAN X": porta associata a una sola VLAN
    endlegend

    @enduml
