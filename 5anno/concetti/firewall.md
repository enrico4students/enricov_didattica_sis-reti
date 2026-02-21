# Firewall

## 1. Definizione

Un firewall è un sistema di sicurezza che controlla e filtra il traffico di rete tra due o più zone con diverso livello di fiducia (per esempio Internet e LAN aziendale, oppure tra VLAN interne).

Applica regole basate su:

* indirizzi IP
* porte
* protocolli
* stato della connessione
* applicazioni (nei firewall moderni)
* identità utente

Il firewall è una funzione **logica** (motore di ispezione + policy) e può essere implementato come:

* Appliance hardware dedicata (dispositivo fisico standalone)
* Firewall virtuale (VM su hypervisor)
* Firewall cloud (servizio gestito in VPC/VNet)
* Firewall host-based (software su server o endpoint)

---

# 2. Posizionamento nel perimetro aziendale

## 2.1 CPE (Customer Premises Equipment)

Il CPE è l’apparato di telecomunicazione installato presso la sede del cliente e collegato alla rete dell’operatore.

Caratteristiche:

* È l’ultimo dispositivo della rete ISP
* È il primo dispositivo visibile dal cliente
* Segna il confine tra rete dell’operatore e rete locale

Può essere:

* ONT (fibra GPON)
* Modem VDSL (xDSL)
* Modem DOCSIS (rete coassiale)
* CPE Ethernet su linee dedicate (fibra punto-punto, MPLS)

Il termine corretto è **CPE**, non “router ISP”, anche se il CPE può integrare funzioni di routing.

---

## 2.2 Collegamento tipico nel perimetro aziendale

Internet
→ CPE dell’operatore
→ Interfaccia WAN del firewall
→ Interfaccia LAN del firewall
→ Switch core o switch di distribuzione
→ VLAN e host interni

Il collegamento è normalmente point-to-point Ethernet tra:

* CPE ISP e firewall (WAN)
* Firewall e switch core (LAN)

---

## 2.3 Schema architetturale completo

```
                              INTERNET
                                  │
                                  │ (rete pubblica ISP)
                                  ▼
        ┌───────────────────────────────────────────────┐
        │                CPE ISP                        │
        │-----------------------------------------------│
        │  ONT GPON / Modem VDSL / Modem DOCSIS         │
        │  oppure CPE Ethernet fornito dall’operatore   │
        │                                               │
        │  Porta LAN (Ethernet verso cliente)           │
        └───────────────────────────────────────────────┘
                                  │
                                  │ cavo Ethernet
                                  ▼
        ┌───────────────────────────────────────────────┐
        │                 FIREWALL                      │
        │-----------------------------------------------│
        │  Interfaccia WAN (verso ISP)                  │
        │  Interfaccia LAN (verso rete interna)         │
        │  Policy, NAT, IPS, VPN, ACL                   │
        └───────────────────────────────────────────────┘
                                  │
                                  │ uplink LAN
                                  ▼
        ┌───────────────────────────────────────────────┐
        │           SWITCH CORE / DISTRIBUZIONE         │
        │-----------------------------------------------│
        │  Porte trunk (802.1Q)                         │
        │  Porte access                                 │
        └───────────────────────────────────────────────┘
                   │                │                 │
                   │                │                 │
                   ▼                ▼                 ▼
        ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
        │   VLAN 10    │   │   VLAN 20    │   │   VLAN 30    │
        │    Uffici    │   │    Server    │   │     VoIP     │
        └──────────────┘   └──────────────┘   └──────────────┘
             │                   │                   │
             ▼                   ▼                   ▼
        PC, stampanti        Server, NAS        Telefoni IP
```

---

# 3. Modalità operative del firewall

## 3.1 Modalità Routed (Layer 3 – la più comune)

Il firewall opera come nodo Layer 3 con almeno due interfacce IP (WAN, LAN, eventuale DMZ).

Caratteristiche:

* Non è un bridge trasparente
* È punto di transito obbligato
* Ogni zona ha subnet diversa
* È il default gateway della LAN
* Il traffico viene instradato attraverso di esso

È il **modello dominante in ambito aziendale moderno.**

---

## 3.2 Modalità Trasparente (Layer 2 – bridge / pass-through)

Il firewall funziona come bridge L2.

Caratteristiche:

* Non modifica gli indirizzi IP
* Non è gateway IP
* È inserito in linea tra due dispositivi
* Filtra il traffico restando trasparente a livello IP

Collegamento tipico:

CPE ISP
→ Firewall (bridge)
→ Switch core

Il firewall è fisicamente in pass-through senza modificare la topologia IP.

---

# 4. Collegamenti fisici del firewall

## 4.1 Lato WAN

Collegamento diretto a:

* ONT (FTTH/GPON)
* Modem VDSL (xDSL)
* Modem DOCSIS (rete coassiale)
* CPE Ethernet su linee dedicate (fibra punto-punto o MPLS)

## 4.2 Lato LAN

Collegamento diretto a:

* Switch core Layer 3
* Switch di distribuzione
* Switch access (ambienti piccoli)

## 4.3 Architetture con DMZ

Ecco la sezione corretta ed estesa, mantenendo lo stesso livello di dettaglio e la stessa struttura.

---

## 4.3 Architetture con DMZ

La DMZ può essere implementata in due modalità principali.

### A) Firewall con almeno tre interfacce (tri-homed)

Firewall con almeno tre interfacce:

* WAN (verso CPE ISP)
* LAN (verso rete interna)
* DMZ (verso switch o server esposti)

Schema DMZ:

Firewall
→ Interfaccia DMZ
→ Switch DMZ
→ Web server / mail server / reverse proxy

---

### B) DMZ tra due firewall (back-to-back)

La DMZ è collocata tra due dispositivi di sicurezza.

Schema DMZ:

Internet
→ Firewall esterno
→ DMZ
→ Firewall interno
→ LAN

In questo modello la rete DMZ è separata sia dalla WAN sia dalla LAN tramite due firewall distinti.

---

# 5. Tipologie principali di firewall

## 5.1 Packet filtering (stateless)

Filtra su IP/porta/protocollo senza mantenere stato di connessione.

## 5.2 Stateful firewall

Tiene traccia dello stato delle sessioni TCP/UDP.  
**È il minimo standard in ambito aziendale.**  

## 5.3 Proxy / Application firewall

Intermedia la connessione a livello applicativo (termina e riapre la sessione).

## 5.4 NGFW (Next-Generation Firewall)

Include:

* Stateful inspection
* DPI (Deep Packet Inspection)
* IPS/IDS
* Controllo applicativo
* Filtro URL
* Ispezione TLS
* Integrazione directory utenti

È oggi la tipologia più diffusa nel mondo aziendale.

## 5.5 UTM (Unified Threat Management)

Soluzione integrata con più funzioni di sicurezza in un’unica appliance.

## 5.6 WAF (Web Application Firewall)

Protegge applicazioni web HTTP/HTTPS.
Si posiziona davanti ai web server (in DMZ o in cloud).
Non sostituisce il firewall di rete.

---

# 6. Tipologie attualmente diffuse in azienda (con esempi)

## 6.1 NGFW perimetrali enterprise

Fortinet FortiGate 100F
[https://www.fortinet.com/resources/data-sheets/fortigate-100f-series](https://www.fortinet.com/resources/data-sheets/fortigate-100f-series)

Palo Alto Networks PA-440 (serie PA-400)
[https://www.paloaltonetworks.com/resources/datasheets/pa-400-series](https://www.paloaltonetworks.com/resources/datasheets/pa-400-series)

Cisco Firepower 1010
[https://www.cisco.com/c/en/us/products/collateral/security/firepower-1000-series/datasheet-c78-742469.html](https://www.cisco.com/c/en/us/products/collateral/security/firepower-1000-series/datasheet-c78-742469.html)

---

## 6.2 NGFW / UTM per PMI e filiali

Sophos XGS Series
[https://www.sophos.com/en-us/products/next-gen-firewall/xgs-smb-firewalls](https://www.sophos.com/en-us/products/next-gen-firewall/xgs-smb-firewalls)

WatchGuard Firebox T40
[https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html](https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html)

Check Point Quantum Spark 1600
[https://www.checkpoint.com/resources/datasheet-4532/datasheet-quantum-spark-16001800](https://www.checkpoint.com/resources/datasheet-4532/datasheet-quantum-spark-16001800)

---

## 6.3 Security gateway branch enterprise

Juniper SRX340
[https://www.juniper.net/documentation/us/en/hardware/srx340/topics/topic-map/srx340-overview.html](https://www.juniper.net/documentation/us/en/hardware/srx340/topics/topic-map/srx340-overview.html)

---

## 6.4 Firewall cloud gestito

Microsoft Azure Firewall
[https://azure.microsoft.com/it-it/products/azure-firewall](https://azure.microsoft.com/it-it/products/azure-firewall)

Overview tecnico
[https://learn.microsoft.com/en-us/azure/firewall/overview](https://learn.microsoft.com/en-us/azure/firewall/overview)

---

# 7. Posizionamento del router rispetto al firewall

## 7.1 Router e firewall separati

Percorso traffico in ingresso:

1. Router edge
2. Firewall
3. Switch
4. PC

Il router:

* gestisce routing WAN (BGP, linee multiple)
* riceve traffico ISP
* instrada verso rete interna

Il firewall:

* applica policy di sicurezza
* esegue NAT
* ispeziona traffico
* protegge la LAN

In questa architettura il firewall è logicamente e fisicamente dietro il router.

---

## 7.2 Firewall che integra routing

Internet
→ CPE ISP
→ Firewall (routing + sicurezza)
→ LAN

Il dispositivo è unico, ma internamente le funzioni sono sequenziali:

1. Decisione di routing
2. Applicazione policy firewall
3. Inoltro verso LAN

La funzione di routing precede logicamente l’applicazione della policy.

---

# 8. Conclusione strutturale

Se router e firewall sono separati → il traffico attraversa prima il router, poi il firewall.

Se routing e firewall sono integrati nello stesso dispositivo → il dispositivo è il primo apparato aziendale che riceve il traffico, ma internamente la funzione di routing precede quella di firewall.

Nell’IT aziendale moderno il modello dominante è:

* NGFW
* Modalità routed
* Collegamento point-to-point al CPE lato WAN
* Collegamento diretto allo switch core lato LAN
* Eventuali interfacce dedicate per DMZ o segmentazione interna

Il firewall rappresenta il punto centrale di:

* segmentazione
* controllo accessi
* monitoraggio
* riduzione della superficie di attacco

---
