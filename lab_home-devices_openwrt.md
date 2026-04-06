**laboratorio da circa 90 minuti** con: scelta dell’hardware, installazione e configurazione di OpenWrt, costruzione della topologia, esperimenti su routing, NAT, firewall, analisi del traffico e introduzione alle VLAN.

---

# Laboratorio di networking con OpenWrt

## Routing, NAT, firewall e VLAN in una rete domestica

## Obiettivo della dispensa

Questa attività permette di costruire un **piccolo laboratorio di rete reale** utilizzando dispositivi economici e software open source. Lo scopo è acquisire familiarità pratica con concetti fondamentali del networking:

routing IP
NAT
gateway e subnet
firewall tra reti
analisi del traffico con Wireshark
segmentazione di rete con VLAN

La configurazione utilizza due router con OpenWrt e uno switch gestibile economico. In questo modo è possibile simulare una rete con più segmenti, simile in piccolo a una rete aziendale.

---

## Hardware necessario

Configurazione consigliata.

Router OpenWrt (2 unità)

GL.iNet GL-MT3000 Beryl AX
Pagina ufficiale
[https://www.gl-inet.com/products/gl-mt3000/](https://www.gl-inet.com/products/gl-mt3000/)

Supporto OpenWrt
[https://openwrt.org/toh/gl.inet/gl-mt3000](https://openwrt.org/toh/gl.inet/gl-mt3000)

Switch gestibile

TP-Link TL-SG105E
Pagina ufficiale
[https://www.tp-link.com/it/business-networking/easy-smart-switch/tl-sg105e/](https://www.tp-link.com/it/business-networking/easy-smart-switch/tl-sg105e/)

Software

Wireshark
[https://www.wireshark.org/download.html](https://www.wireshark.org/download.html)

Documentazione OpenWrt

Guida introduttiva
[https://openwrt.org/docs/guide-user/start](https://openwrt.org/docs/guide-user/start)

Configurazione firewall
[https://openwrt.org/docs/guide-user/firewall/firewall_configuration](https://openwrt.org/docs/guide-user/firewall/firewall_configuration)

Configurazione VLAN
[https://openwrt.org/docs/guide-user/network/dsa/dsa-mini-tutorial](https://openwrt.org/docs/guide-user/network/dsa/dsa-mini-tutorial)

---

## Architettura della rete di laboratorio

Topologia utilizzata:

Internet
↓
FRITZ!Box 7530
↓
Router R1 OpenWrt
↓
Switch
├── PC laboratorio
└── Router R2 OpenWrt
  └── client Wi-Fi o rete interna

R1 rappresenta il **router principale della rete**.
R2 rappresenta una **rete secondaria o filiale**.

Questa configurazione consente di simulare:

una rete principale
una rete remota
routing tra reti
policy firewall differenti

---

## Piano di indirizzamento

La rete viene divisa in tre segmenti.

Rete FRITZ!Box
192.168.178.0/24

Rete laboratorio principale
192.168.10.0/24

Rete laboratorio secondaria
192.168.20.0/24

Configurazione IP:

FRITZ!Box
192.168.178.1

Router R1
WAN → DHCP dal FRITZ!Box
LAN → 192.168.10.1

Router R2
WAN → 192.168.10.2
LAN → 192.168.20.1

PC laboratorio
192.168.10.100
gateway 192.168.10.1

---

## Preparazione del laboratorio

## Collegamenti fisici

Eseguire i collegamenti nel seguente ordine:

porta LAN del FRITZ!Box → porta WAN di R1
porta LAN di R1 → switch
PC → switch
porta WAN di R2 → switch

Accendere prima R1, poi R2.

---

## Accesso all’interfaccia di configurazione

I router GL.iNet includono una propria interfaccia web. Tuttavia OpenWrt utilizza normalmente l’interfaccia **LuCI**.

Aprire il browser e collegarsi all’indirizzo:

192.168.8.1 (configurazione iniziale tipica dei router GL.iNet)

Una volta configurato l’indirizzo LAN del router, accedere tramite:

192.168.10.1

---

### Fase 1 – Configurazione della rete principale

Configurare R1.

LAN address

192.168.10.1
subnet mask 255.255.255.0

Attivare DHCP.

Range DHCP:

192.168.10.100 – 192.168.10.200

Verificare:

dal PC

ping 192.168.10.1

verificare navigazione Internet.

---

### Fase 2 – Configurazione del router secondario

Configurare R2.

WAN interface

IP statico

192.168.10.2
gateway 192.168.10.1

LAN interface

192.168.20.1
subnet mask 255.255.255.0

Attivare DHCP sulla rete LAN.

Range DHCP

192.168.20.100 – 192.168.20.200

Verificare che un dispositivo collegato al Wi-Fi di R2 ottenga indirizzo IP.

---

### Fase 3 – Verifica della connettività

Dal PC laboratorio verificare:

ping verso router R1

ping 192.168.10.1

ping verso router R2

ping 192.168.10.2

Dal client dietro R2 verificare:

ping 192.168.20.1

verificare navigazione Internet.

In questa fase il traffico passa attraverso due router e due NAT.

---

### Fase 4 – Comprendere il NAT

Situazione attuale:

client rete 192.168.20.0
↓
NAT su R2
↓
rete 192.168.10.0
↓
NAT su R1
↓
Internet

Questo scenario permette di osservare il comportamento del NAT.

Utilizzare Wireshark sul PC e catturare traffico mentre un client dietro R2 esegue un ping verso Internet.

Osservare:

indirizzi IP sorgente
TTL
ICMP echo request e reply.

---

### Fase 5 – Routing statico tra le reti

Per rendere la rete più didattica si può eliminare il NAT su R2 e usare routing puro.

Su R1 aggiungere una route statica:

destinazione

192.168.20.0/24

next hop

192.168.10.2

Su R2 configurare gateway predefinito:

192.168.10.1

Ora il traffico tra le due reti è instradato.

Verificare dal PC:

ping 192.168.20.1

---

### Fase 6 – Configurazione firewall

Creare una politica differenziata tra reti.

Consentire traffico

192.168.10.0 → 192.168.20.0

Bloccare traffico

192.168.20.0 → 192.168.10.0

Consentire uscita Internet per entrambe.

Questo esercizio mostra il concetto di **zone firewall** utilizzate da OpenWrt.

---

### Fase 7 – Analisi del traffico con Wireshark

Installare Wireshark.

[https://www.wireshark.org/download.html](https://www.wireshark.org/download.html)

Eseguire cattura sulla scheda Ethernet del PC.

Provare:

ping verso R1
ping verso R2
ping verso client dietro R2

Osservare:

ARP requests
ICMP
MAC addresses
TTL dei pacchetti.

Questo passaggio aiuta a capire come il traffico attraversa i router.

---

### Fase 8 – Introduzione alle VLAN

Lo switch TL-SG105E consente di creare VLAN.

Configurazione esempio.

VLAN 10 – rete principale
VLAN 20 – rete secondaria
VLAN 30 – rete ospiti

Configurazione porte:

porta verso R1 → trunk VLAN 10,20,30
porta PC → access VLAN 10
porta verso R2 → access VLAN 20

In OpenWrt creare subinterfacce VLAN su R1.

Esempio logico:

eth0.10
eth0.20
eth0.30

Associare ogni VLAN a una subnet diversa.

Questo esercizio introduce i concetti di:

VLAN access port
VLAN trunk
inter-VLAN routing.

---

#### Sequenza didattica consigliata

Ordine di apprendimento:

1 configurazione IP
2 DHCP
3 NAT
4 routing statico
5 firewall
6 analisi traffico
7 VLAN

Questo ordine permette di introdurre gradualmente la complessità.

---

#### Competenze acquisite

Dopo il laboratorio si dovrebbe avere familiarità con:

configurazione di router reali
indirizzamento IPv4
gateway e subnet
routing statico
NAT
firewall tra reti
analisi pacchetti
segmentazione VLAN.

Queste sono le competenze di base utilizzate nella gestione di reti aziendali.


---

### Alcuni riferimenti

OpenWrt documentation
[https://openwrt.org/docs/guide-user/start](https://openwrt.org/docs/guide-user/start)

Firewall configuration
[https://openwrt.org/docs/guide-user/firewall/firewall_configuration](https://openwrt.org/docs/guide-user/firewall/firewall_configuration)

OpenWrt VLAN tutorial
[https://openwrt.org/docs/guide-user/network/dsa/dsa-mini-tutorial](https://openwrt.org/docs/guide-user/network/dsa/dsa-mini-tutorial)

GL.iNet GL-MT3000
[https://www.gl-inet.com/products/gl-mt3000/](https://www.gl-inet.com/products/gl-mt3000/)

OpenWrt hardware page
[https://openwrt.org/toh/gl.inet/gl-mt3000](https://openwrt.org/toh/gl.inet/gl-mt3000)

TP-Link TL-SG105E
[https://www.tp-link.com/it/business-networking/easy-smart-switch/tl-sg105e/](https://www.tp-link.com/it/business-networking/easy-smart-switch/tl-sg105e/)

Wireshark
[https://www.wireshark.org/download.html](https://www.wireshark.org/download.html)

---

# Laboratorio avanzato di networking con OpenWrt

### Routing dinamico, architettura core–distribution, DMZ e monitoraggio

Questa seconda attività estende il laboratorio precedente. La rete costruita nella prima parte viene riutilizzata e ampliata per simulare una struttura più simile a una piccola rete aziendale.

L’obiettivo è acquisire esperienza pratica con:

routing dinamico OSPF
simulazione di una architettura core–distribution
segmentazione di rete con DMZ
monitoraggio SNMP
analisi dei percorsi dei pacchetti

La durata tipica dell’attività è circa due o tre ore.

---

## Architettura di rete utilizzata

La rete viene riorganizzata per simulare una struttura più simile a una rete campus o aziendale.

Internet
↓
FRITZ!Box
↓
Router R1 OpenWrt (core / edge)
↓
Switch gestibile
├── PC amministrazione
├── Router R2 OpenWrt (distribution)
└── Server o PC DMZ

R1 assume il ruolo di **router principale della rete** e rappresenta il livello core o edge.
R2 rappresenta un **distribution router** che gestisce una rete locale.

La DMZ viene simulata collegando un host direttamente allo switch ma su una rete separata.

---

## Piano di indirizzamento esteso

La rete viene suddivisa in quattro segmenti.

Rete FRITZ!Box
192.168.178.0/24

Rete core
192.168.10.0/24

Rete distribution (rete utenti)
192.168.20.0/24

Rete DMZ
192.168.30.0/24

Configurazione degli indirizzi:

FRITZ!Box
192.168.178.1

Router R1

WAN
DHCP dal FRITZ!Box

LAN core
192.168.10.1

Router R2

WAN
192.168.10.2

LAN utenti
192.168.20.1

Server DMZ

192.168.30.10

Gateway
192.168.30.1

---

## Fase 1 – Creazione della rete DMZ

Configurare su R1 una nuova interfaccia di rete.

Interfaccia LAN2 o VLAN dedicata:

indirizzo

192.168.30.1
subnet mask 255.255.255.0

Collegare il server o il PC DMZ allo switch.

Configurare sul server:

IP
192.168.30.10

gateway
192.168.30.1

Verificare:

ping 192.168.30.1

---

## Fase 2 – Configurazione delle zone firewall

In OpenWrt le regole firewall sono organizzate in **zone**.

Creare tre zone:

LAN
rete 192.168.10.0 e 192.168.20.0

DMZ
rete 192.168.30.0

WAN
Internet

Configurazione tipica:

LAN → consentito verso WAN
LAN → consentito verso DMZ
DMZ → consentito verso WAN
DMZ → bloccato verso LAN

Questa configurazione simula una tipica architettura aziendale.

---

## Fase 3 – Simulazione di un servizio nella DMZ

Avviare un semplice servizio HTTP sul server DMZ.

Su un PC Linux:

installare un server HTTP semplice:

python3 -m http.server 80

Oppure su Windows installare un server web semplice.

Verificare dal PC della rete LAN:

aprire nel browser

[http://192.168.30.10](http://192.168.30.10)

Il traffico passa dal router R1 verso la DMZ.

---

## Fase 4 – Routing dinamico con OSPF

Per sperimentare il routing dinamico è possibile installare **FRRouting** su OpenWrt.

FRRouting
[https://frrouting.org](https://frrouting.org)

Installazione su OpenWrt:

opkg update
opkg install frr frr-ospfd

Attivare il servizio.

Configurare OSPF su R1 e R2.

Esempio di configurazione minima.

Su R1

router ospf
network 192.168.10.0/24 area 0
network 192.168.30.0/24 area 0

Su R2

router ospf
network 192.168.10.0/24 area 0
network 192.168.20.0/24 area 0

Dopo l’attivazione i router scambiano automaticamente le rotte.

Verificare con il comando:

show ip route

---

## Fase 5 – Analisi del routing

Verificare che R1 abbia appreso la rete:

192.168.20.0/24

Verificare che R2 abbia appreso la rete:

192.168.30.0/24

Queste rotte sono state distribuite automaticamente dal protocollo OSPF.

---

## Fase 6 – Analisi del percorso dei pacchetti

Dal PC eseguire:

traceroute 192.168.30.10

Il percorso dovrebbe mostrare:

PC
↓
Router R1
↓
Server DMZ

Eseguire traceroute dal client dietro R2.

Il percorso diventa:

client
↓
Router R2
↓
Router R1
↓
Server DMZ

Questo esercizio rende evidente il percorso reale dei pacchetti.

---

## Fase 7 – Monitoraggio con SNMP

Installare il supporto SNMP su R1.

Pacchetto OpenWrt:

opkg install net-snmpd

Configurare il servizio SNMP.

community

public

Permettere accesso dalla rete LAN.

Dal PC utilizzare uno strumento SNMP.

Esempio con snmpwalk:

snmpwalk -v2c -c public 192.168.10.1

Questo comando restituisce informazioni su:

interfacce di rete
traffico
stato delle porte

SNMP è uno dei protocolli più utilizzati per il monitoraggio delle reti.

---

## Fase 8 – Analisi del traffico di routing

Aprire Wireshark sul PC.

Filtrare il traffico OSPF.

Filtro:

ospf

Osservare i pacchetti di tipo:

Hello
Database Description
Link State Update

Questi pacchetti servono ai router per costruire la mappa della rete.

---

## Fase 9 – Simulazione di una architettura core–distribution

La rete costruita nel laboratorio rappresenta una versione ridotta di una architettura a tre livelli.

Router R1 rappresenta il **core / edge**.

Router R2 rappresenta il **distribution**.

Gli host rappresentano l’**access layer**.

Il traffico segue questo percorso:

client rete utenti
↓
router distribution
↓
router core
↓
DMZ o Internet

Questa struttura è concettualmente simile a quella utilizzata in molte reti aziendali.

---

## Esperimenti aggiuntivi

Provare a modificare la topologia per osservare effetti diversi.

Bloccare completamente la DMZ verso Internet.

Consentire solo HTTPS.

Creare una nuova rete VLAN per ospiti.

Installare una VPN WireGuard tra R1 e R2.

Misurare traffico con iperf.

Iperf
[https://iperf.fr](https://iperf.fr)

---

## Competenze acquisite

Dopo il laboratorio completo si acquisisce familiarità con:

routing statico
routing dinamico OSPF
architetture di rete gerarchiche
segmentazione DMZ
policy firewall tra reti
monitoraggio SNMP
analisi dei protocolli con Wireshark

Queste competenze rappresentano una base concreta per lo studio di reti aziendali e infrastrutture di sicurezza.

---

## Alcuni riferimenti

FRRouting
[https://frrouting.org](https://frrouting.org)

OpenWrt documentation
[https://openwrt.org/docs/guide-user/start](https://openwrt.org/docs/guide-user/start)

OpenWrt firewall guide
[https://openwrt.org/docs/guide-user/firewall/firewall_configuration](https://openwrt.org/docs/guide-user/firewall/firewall_configuration)

OpenWrt VLAN tutorial
[https://openwrt.org/docs/guide-user/network/dsa/dsa-mini-tutorial](https://openwrt.org/docs/guide-user/network/dsa/dsa-mini-tutorial)

Wireshark download
[https://www.wireshark.org/download.html](https://www.wireshark.org/download.html)

SNMP tutorial
[https://www.net-snmp.org/wiki/index.php/Tutorials](https://www.net-snmp.org/wiki/index.php/Tutorials)

---

## Laboratorio opzionale: simulazione di rete aziendale con architettura core–distribution e VLAN multiple

Questa terza attività estende i laboratori precedenti e utilizza la stessa infrastruttura fisica. Lo scopo è simulare una piccola rete aziendale con segmentazione in VLAN e una struttura logica simile alle architetture gerarchiche utilizzate nelle reti enterprise.

Gli obiettivi principali sono:

comprendere la segmentazione tramite VLAN
simulare una architettura core–distribution
realizzare inter-VLAN routing
applicare politiche firewall tra reti
analizzare il traffico di rete

Questo laboratorio utilizza sempre due router OpenWrt e uno switch gestibile.

---

## Architettura logica

La rete viene organizzata come segue.

Internet
↓
FRITZ!Box
↓
Router R1 OpenWrt (core / edge)
↓
Switch gestibile VLAN
├── PC amministrazione (VLAN 10)
├── PC laboratorio (VLAN 20)
├── Router R2 OpenWrt (distribution)
└── Server DMZ (VLAN 30)

Il router R1 svolge il ruolo di **core router**.

Il router R2 rappresenta un **distribution router** collegato a una delle VLAN.

Lo switch gestisce la segmentazione delle reti tramite VLAN.

---

## Piano di indirizzamento

VLAN amministrazione
VLAN ID 10
rete 192.168.10.0/24
gateway 192.168.10.1

VLAN laboratorio
VLAN ID 20
rete 192.168.20.0/24
gateway 192.168.20.1

VLAN DMZ
VLAN ID 30
rete 192.168.30.0/24
gateway 192.168.30.1

Rete core interna
192.168.100.0/24

FRITZ!Box
192.168.178.1

Router R1
WAN 192.168.178.x
core LAN 192.168.100.1

Router R2
WAN 192.168.100.2
LAN utenti 192.168.40.1

---

## Configurazione delle VLAN sullo switch

Accedere alla gestione web dello switch.

Creare tre VLAN.

VLAN 10 amministrazione
VLAN 20 laboratorio
VLAN 30 DMZ

Configurare le porte.

porta verso router R1
modalità trunk
VLAN consentite 10,20,30

porta PC amministrazione
access VLAN 10

porta PC laboratorio
access VLAN 20

porta server DMZ
access VLAN 30

porta verso router R2
access VLAN 20

Questo schema simula un tipico collegamento tra core router e switch access.

---

## Configurazione delle interfacce VLAN su R1

Su OpenWrt creare tre interfacce VLAN.

Interfaccia VLAN 10

indirizzo
192.168.10.1

Interfaccia VLAN 20

indirizzo
192.168.20.1

Interfaccia VLAN 30

indirizzo
192.168.30.1

Ogni VLAN rappresenta una subnet indipendente.

Il router R1 svolge quindi la funzione di **gateway per tutte le VLAN**.

---

## Verifica della segmentazione

Configurare i PC con indirizzi nella subnet corretta.

PC amministrazione

192.168.10.10
gateway 192.168.10.1

PC laboratorio

192.168.20.10
gateway 192.168.20.1

Server DMZ

192.168.30.10
gateway 192.168.30.1

Verificare che dispositivi appartenenti a VLAN diverse non possano comunicare direttamente senza passare dal router.

---

## Inter-VLAN routing

Poiché tutte le VLAN hanno il gateway su R1, il router può instradare il traffico tra le reti.

Esempio.

PC amministrazione → server DMZ

percorso

PC
↓
switch
↓
router R1
↓
switch
↓
server DMZ

Questo processo è chiamato **inter-VLAN routing**.

---

## Politiche firewall tra VLAN

Configurare sul router R1 regole firewall.

consentire

VLAN amministrazione → VLAN laboratorio
VLAN amministrazione → DMZ

limitare

VLAN laboratorio → VLAN amministrazione

bloccare

DMZ → LAN interne

Questo tipo di configurazione è comune nelle reti aziendali.

---

## Integrazione del router R2

R2 viene collegato alla VLAN laboratorio.

WAN R2

192.168.20.2
gateway 192.168.20.1

LAN R2

192.168.40.1
rete 192.168.40.0/24

Questo simula una **rete remota collegata al distribution layer**.

---

## Routing verso la rete remota

Configurare su R1 una route statica.

destinazione
192.168.40.0/24

gateway
192.168.20.2

Su R2 impostare gateway predefinito.

192.168.20.1

Ora i client delle VLAN interne possono raggiungere la rete dietro R2.

---

## Verifica del percorso dei pacchetti

Dal PC amministrazione eseguire:

traceroute 192.168.40.10

Il percorso dovrebbe essere:

PC amministrazione
↓
router R1
↓
router R2
↓
host remoto

Questo esercizio rende visibile il percorso reale del traffico.

---

## Analisi del traffico con Wireshark

Installare Wireshark.

[https://www.wireshark.org/download.html](https://www.wireshark.org/download.html)

Eseguire cattura mentre avviene traffico tra VLAN.

Osservare:

frame Ethernet
tag VLAN 802.1Q
pacchetti IP
ICMP

Questo permette di vedere concretamente come funzionano VLAN e routing.

---

## Interpretazione dell’architettura

La rete simulata rappresenta una versione semplificata di una architettura aziendale.

router R1
core / edge

switch
access layer

router R2
distribution di una rete remota

VLAN
segmentazione delle reti utenti

DMZ
rete esposta a servizi pubblici

Questa struttura riproduce molti concetti utilizzati nelle reti reali.

---

## Esperimenti suggeriti

Creare una nuova VLAN per ospiti.

Configurare QoS per limitare banda alla rete laboratorio.

Installare WireGuard su R2 e simulare un accesso remoto.

Monitorare traffico con SNMP.

Configurare un server DNS interno.

---

## Competenze acquisite nell’intero percorso

Al termine dei tre laboratori si acquisisce esperienza pratica su:

configurazione di router reali
indirizzamento IPv4
routing statico
routing dinamico
NAT
firewall e segmentazione
VLAN e trunk
analisi pacchetti
architetture di rete gerarchiche

Questo percorso rappresenta una base solida per comprendere la progettazione e la gestione delle reti aziendali.

---

## Alcuni riferimenti

OpenWrt documentation
[https://openwrt.org/docs/guide-user/start](https://openwrt.org/docs/guide-user/start)

OpenWrt firewall guide
[https://openwrt.org/docs/guide-user/firewall/firewall_configuration](https://openwrt.org/docs/guide-user/firewall/firewall_configuration)

OpenWrt VLAN configuration
[https://openwrt.org/docs/guide-user/network/dsa/dsa-mini-tutorial](https://openwrt.org/docs/guide-user/network/dsa/dsa-mini-tutorial)

Wireshark download
[https://www.wireshark.org/download.html](https://www.wireshark.org/download.html)

FRRouting
[https://frrouting.org](https://frrouting.org)

---

