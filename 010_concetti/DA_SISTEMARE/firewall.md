
# Firewall

## 1. Definizione e natura del firewall

Un firewall è un sistema di sicurezza che controlla e filtra il traffico di rete tra due o più zone con diverso livello di fiducia (ad esempio Internet e LAN aziendale, oppure tra VLAN interne).

Applica regole basate su:

* indirizzi IP
* porte
* protocolli
* stato della connessione
* applicazioni (nei firewall moderni)
* identità utente

Il firewall è una **funzione logica** composta da:

* motore di ispezione
* insieme di policy di sicurezza

Può essere implementato come:

* appliance hardware dedicata
* firewall virtuale (VM su hypervisor)
* firewall cloud (servizio in VPC/VNet)
* firewall host-based (software su server o endpoint)

---

# 2. Architettura perimetrale aziendale

## 2.1 Il CPE (Customer Premises Equipment)

Il CPE è l’apparato di telecomunicazione installato presso la sede del cliente e collegato alla rete dell’operatore.

Caratteristiche:

* è l’ultimo dispositivo della rete ISP
* è il primo dispositivo visibile dal cliente
* segna il confine tra rete dell’operatore e rete locale

Può essere:

* ONT (fibra GPON)
* modem VDSL (xDSL)
* modem DOCSIS (rete coassiale)
* CPE Ethernet su linee dedicate (fibra punto-punto, MPLS)

Il termine corretto è **CPE**, anche quando integra funzioni di routing.

---

## 2.2 Schema architetturale tipico

Architettura perimetrale standard in ambito aziendale:

Internet
→ CPE ISP
→ Firewall
→ Switch core / distribuzione
→ VLAN interne

Collegamenti tipici:

* Ethernet point-to-point tra CPE e firewall (lato WAN)
* uplink LAN tra firewall e switch core

Schema:

```
                              INTERNET
                                  │
                                  ▼
        ┌───────────────────────────────────────────────┐
        │                    CPE ISP                    │
        │  ONT / Modem / CPE Ethernet                   │
        └───────────────────────────────────────────────┘
                                  │
                                  ▼
        ┌───────────────────────────────────────────────┐
        │                    FIREWALL                   │
        │  WAN | LAN | eventuale DMZ                    │
        │  Policy, NAT, VPN, IPS, ACL                   │
        └───────────────────────────────────────────────┘
                                  │
                                  ▼
        ┌───────────────────────────────────────────────┐
        │             SWITCH CORE / DISTRIBUZIONE       │
        │  trunk 802.1Q – porte access                  │
        └───────────────────────────────────────────────┘
                   │                │                │
                   ▼                ▼                ▼
                VLAN 10          VLAN 20          VLAN 30
                Uffici           Server           VoIP
```

---

# 3. Modalità operative del firewall

## 3.1 Modalità Routed (Layer 3)

È la modalità dominante in ambito aziendale moderno.

Caratteristiche:

* il firewall è nodo Layer 3
* possiede almeno due interfacce IP (WAN, LAN, eventuale DMZ)
* ogni zona appartiene a subnet diversa
* è default gateway della LAN
* il traffico viene instradato attraverso di esso

Non è un bridge trasparente: svolge funzione di routing e sicurezza.

---

## 3.2 Modalità Trasparente (Layer 2 – bridge)

Il firewall opera come bridge L2 inserito in linea.

Caratteristiche:

* non modifica indirizzi IP
* non è gateway IP
* filtra traffico restando trasparente a livello IP
* è inserito fisicamente tra due dispositivi

Esempio:

CPE ISP
→ Firewall (bridge)
→ Switch core

---

# 4. DMZ (Demilitarized Zone)

La DMZ è una rete separata destinata a sistemi esposti verso Internet (web server, mail server, reverse proxy).

## 4.1 Firewall tri-homed

Firewall con almeno tre interfacce:

* WAN
* LAN
* DMZ

Schema:

Firewall
→ Interfaccia DMZ
→ Switch DMZ
→ Server esposti

---

## 4.2 DMZ tra due firewall (back-to-back)

Architettura con doppio livello di protezione:

Internet
→ Firewall esterno
→ DMZ
→ Firewall interno
→ LAN

La DMZ è separata sia dalla WAN sia dalla LAN tramite due dispositivi distinti.

---

# 5. Tipologie principali di firewall

## 5.1 Packet filtering (stateless)

Filtra su IP, porta, protocollo senza mantenere stato di connessione.

---

## 5.2 Stateful firewall

Tiene traccia dello stato delle sessioni TCP/UDP.
È il minimo standard in ambito aziendale.

---

## 5.3 Proxy / Application firewall

Intermedia la connessione a livello applicativo (termina e riapre la sessione).

---

## 5.4 NGFW (Next-Generation Firewall)

Include:

* stateful inspection
* DPI (Deep Packet Inspection)
* IPS/IDS
* controllo applicativo
* filtro URL
* ispezione TLS
* integrazione con directory utenti

È la tipologia oggi più diffusa nel mondo aziendale.

---

## 5.5 UTM (Unified Threat Management)

Soluzione integrata che unisce più funzioni di sicurezza in un’unica appliance.

---

## 5.6 WAF (Web Application Firewall)

Protegge applicazioni web HTTP/HTTPS.
Si posiziona davanti ai web server (in DMZ o in cloud).
Non sostituisce il firewall di rete.

---

# 6. Router e firewall: relazione architetturale

## 6.1 Router e firewall separati

Percorso traffico:

1. Router edge
2. Firewall
3. Switch
4. Host

Il router:

* gestisce routing WAN (BGP, linee multiple)
* riceve traffico ISP
* instrada verso rete interna

Il firewall:

* applica policy di sicurezza
* esegue NAT
* ispeziona traffico
* protegge la LAN

In questo modello il firewall è fisicamente e logicamente dietro il router.

---

## 6.2 Firewall con routing integrato

Architettura:

Internet
→ CPE ISP
→ Firewall (routing + sicurezza)
→ LAN

Il dispositivo è unico, ma le funzioni sono logicamente sequenziali:

1. decisione di routing
2. applicazione della policy firewall
3. inoltro verso LAN

---

# 7. Soluzioni attualmente diffuse in azienda

## 7.1 NGFW perimetrali enterprise

Fortinet FortiGate 100F
[https://www.fortinet.com/resources/data-sheets/fortigate-100f-series](https://www.fortinet.com/resources/data-sheets/fortigate-100f-series)

Palo Alto Networks PA-440 (serie PA-400)
[https://www.paloaltonetworks.com/resources/datasheets/pa-400-series](https://www.paloaltonetworks.com/resources/datasheets/pa-400-series)

Cisco Firepower 1010
[https://www.cisco.com/c/en/us/products/collateral/security/firepower-1000-series/datasheet-c78-742469.html](https://www.cisco.com/c/en/us/products/collateral/security/firepower-1000-series/datasheet-c78-742469.html)

---

## 7.2 NGFW / UTM per PMI

Sophos XGS Series
[https://www.sophos.com/en-us/products/next-gen-firewall/xgs-smb-firewalls](https://www.sophos.com/en-us/products/next-gen-firewall/xgs-smb-firewalls)

WatchGuard Firebox T40
[https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html](https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html)

Check Point Quantum Spark 1600
[https://www.checkpoint.com/resources/datasheet-4532/datasheet-quantum-spark-16001800](https://www.checkpoint.com/resources/datasheet-4532/datasheet-quantum-spark-16001800)

---

## 7.3 Security gateway branch enterprise

Juniper SRX340
[https://www.juniper.net/documentation/us/en/hardware/srx340/topics/topic-map/srx340-overview.html](https://www.juniper.net/documentation/us/en/hardware/srx340/topics/topic-map/srx340-overview.html)

---

## 7.4 Firewall cloud gestito

Microsoft Azure Firewall
[https://azure.microsoft.com/it-it/products/azure-firewall](https://azure.microsoft.com/it-it/products/azure-firewall)

Overview tecnico
[https://learn.microsoft.com/en-us/azure/firewall/overview](https://learn.microsoft.com/en-us/azure/firewall/overview)

---

# 8. Conclusione

Nel modello aziendale moderno il firewall:

* è generalmente un NGFW
* opera in modalità routed
* è collegato tra CPE e switch core
* può avere interfacce dedicate per DMZ o segmentazione interna

Rappresenta il punto centrale di:

* segmentazione
* controllo accessi
* monitoraggio
* riduzione della superficie di attacco

La struttura è ora lineare, senza ripetizioni del flusso perimetrale, senza duplicazioni del ruolo del CPE e senza ridondanze nella spiegazione del rapporto tra routing e policy firewall.
