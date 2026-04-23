## Differenze fra access point aziendale vs. “router” WiFi casalingo

Un access point aziendale è un dispositivo di livello 2 dedicato esclusivamente alla connettività WiFi. Non svolge funzioni di routing, NAT o firewalling, che sono demandate a dispositivi separati (firewall, router). È gestibile centralmente (controller o cloud), supporta più SSID, VLAN, roaming avanzato e autenticazione enterprise (es. 802.1X).

Un “router” WiFi casalingo è un dispositivo all-in-one che integra:

* access point
* router
* NAT
* firewall base
* DHCP

È pensato per semplicità, non per scalabilità. Non supporta gestione centralizzata né funzionalità avanzate di rete aziendale.

---

## Descrivere il roaming (le tipologie incluse nel programma di quest’anno)

Il roaming è la capacità di un dispositivo WiFi di spostarsi tra più access point mantenendo la connessione.

Tipologie principali:

* roaming Layer 2: il client mantiene lo stesso indirizzo IP e si sposta tra AP nella stessa VLAN/subnet. È il caso più comune nelle LAN aziendali.

* roaming Layer 3: il client cambia subnet/VLAN e quindi indirizzo IP. Più complesso, richiede meccanismi aggiuntivi.

* roaming veloce (fast roaming): riduce i tempi di handover. Basato su standard come:

  * 802.11r (fast BSS transition)
  * 802.11k (radio resource management)
  * 802.11v (network assisted roaming)

---

## Descrivere 4G LTE

4G LTE è una tecnologia di rete mobile a banda larga completamente basata su IP.

Caratteristiche principali:

* architettura all-IP (no circuit switching)
* alte velocità di download/upload
* latenza ridotta rispetto al 3G
* uso di tecniche come OFDMA e MIMO

È progettata per servizi dati, voce su IP (VoLTE) e multimedia.

---

## Descrivere MIB (Management Information Base)

La MIB è una struttura dati utilizzata da SNMP per rappresentare le informazioni gestite sui dispositivi.

È organizzata gerarchicamente come un albero di oggetti identificati da OID (Object Identifier).

Contiene variabili come:

* stato interfacce
* traffico
* errori
* configurazioni

Il manager SNMP legge o modifica questi valori tramite operazioni GET/SET.

---

## Descrivere la virtualizzazione: tipologie e caratteristiche

La virtualizzazione consiste nell’astrarre le risorse hardware per creare più ambienti isolati su una stessa macchina fisica.

Tipologie:

* virtualizzazione hardware (VM): tramite hypervisor (es. tipo 1 bare-metal, tipo 2 hosted)
* virtualizzazione a livello di sistema operativo (container)
* virtualizzazione di rete (VLAN, overlay)
* virtualizzazione di storage

Caratteristiche:

* isolamento tra ambienti
* flessibilità
* provisioning rapido
* portabilità
* migliore utilizzo delle risorse

---

## Nell’ambito del WiFi descrivere il concetto di guest e come viene gestito

Una rete guest è una rete WiFi dedicata agli utenti esterni.

Caratteristiche:

* separazione dalla rete interna
* accesso limitato (tipicamente solo Internet)
* autenticazione semplificata (captive portal)

Gestione:

* SSID dedicato
* associato a VLAN separata
* traffico filtrato dal firewall
* isolamento client-to-client spesso attivo

---

## Cos’è una SNMP trap?

Una SNMP trap è un messaggio inviato automaticamente da un agente SNMP al manager.

È asincrona (non richiesta) e serve per notificare eventi, ad esempio:

* dispositivo down
* soglia superata
* errore

Utilizza tipicamente UDP porta 162.

---

## Descrivere l’architettura 3-tier, fornire un esempio concreto

È un’architettura a tre livelli:

* presentation: interfaccia utente
* application: logica applicativa
* data: database

Esempio:

* browser web (presentation)
* server applicativo (application)
* database MySQL (data)

Consente separazione dei ruoli, scalabilità e sicurezza.

---

## Descrivere i componenti principali di una rete di telefonia mobile

Componenti principali:

* UE (User Equipment): dispositivo utente (smartphone)
* RAN (Radio Access Network): stazioni radio base (eNodeB per LTE)
* Core Network (EPC in LTE): gestione mobilità, autenticazione, routing dati
* Internet o reti esterne

Il traffico passa da UE → RAN → Core → Internet.

Meno sinteticamente

## Descrivere i componenti principali di una rete di telefonia mobile

Componenti principali:

* UE (User Equipment): dispositivo utente (smartphone)
* RAN (Radio Access Network): stazioni radio base (eNodeB per LTE)
  * allocazione dinamica delle risorse radio (chi trasmette, quando e su quali frequenze)
  * gestione della qualità del segnale e adattamento della modulazione
  * decisioni rapide di handover tra celle vicine

* Core Network (EPC in LTE): gestione mobilità, autenticazione, routing dati
  È il punto principale di "intelligenza" della rete. Componenti:
  * MME: gestisce mobilità e autenticazione degli utenti
  * HSS: database centrale degli utenti (profili, credenziali)
  * SGW/PGW: instradamento del traffico dati verso Internet
    * autenticazione e autorizzazione
    * assegnazione indirizzo IP
    * gestione delle sessioni
    * applicazione delle policy (QoS, priorità, limiti)

* Internet o reti esterne
  Non appartiene alla rete mobile, ma riceve i dati instradati dal core.

Sintesi del flusso con “intelligenza”:

* UE: esecuzione delle richieste della rete
* RAN: controllo radio in tempo reale (intelligenza locale)
* Core: controllo logico e decisionale globale (intelligenza centrale)

Il traffico segue il percorso:
UE → RAN → Core → Internet
ma le decisioni principali vengono prese soprattutto nel Core Network e, per la parte radio, nella RAN.


---

## Vantaggi e sfide del cloud ibrido

Vantaggi:

* flessibilità (uso combinato di risorse locali e cloud)
* scalabilità
* ottimizzazione costi
* continuità operativa

Sfide:

* complessità di gestione
* integrazione tra ambienti
* sicurezza e compliance
* gestione delle latenze

---

## Descrivere i dati utilizzati nel network management

Nel network management si utilizzano diversi tipi di dati:

* dati di configurazione: parametri dei dispositivi
* dati operativi: stato (up/down)
* dati prestazionali: traffico, latenza, errori
* log ed eventi: notifiche, allarmi
* dati storici: trend e analisi

Questi dati sono raccolti tramite SNMP, syslog, NetFlow.

---

## Sicurezza WiFi

Elementi principali:

* autenticazione:

  * WPA2/WPA3 Personal (PSK)
  * WPA2/WPA3 Enterprise (802.1X)

* cifratura:

  * AES (CCMP)

* segmentazione:

  * VLAN per separare utenti

* protezioni:

  * disabilitazione WPS
  * isolamento client
  * filtraggio MAC (limitato)

* monitoraggio:

  * rilevazione access point rogue

---

## Creare un piano di indirizzamento VLSM partendo da 10.0.0.0/24 per 120, 60, 30, 10 host

Il VLSM è necessario perché le reti hanno dimensioni diverse.

Calcolo prefissi:

* 120 host → /25
* 60 host → /26
* 30 host → /27
* 10 host → /28

Schema bit (ultimo ottetto):

* /25 → 0xxxxxxx
* /26 → 10xxxxxx
* /27 → 110xxxxx
* /28 → 1110xxxx

Tabella:

| Rete | Host | Subnet        | Netmask         | Router     | Primo host | Ultimo host | Broadcast  |
| ---- | ---: | ------------- | --------------- | ---------- | ---------- | ----------- | ---------- |
| R1   |  120 | 10.0.0.0/25   | 255.255.255.128 | 10.0.0.1   | 10.0.0.1   | 10.0.0.126  | 10.0.0.127 |
| R2   |   60 | 10.0.0.128/26 | 255.255.255.192 | 10.0.0.129 | 10.0.0.129 | 10.0.0.190  | 10.0.0.191 |
| R3   |   30 | 10.0.0.192/27 | 255.255.255.224 | 10.0.0.193 | 10.0.0.193 | 10.0.0.222  | 10.0.0.223 |
| R4   |   10 | 10.0.0.224/28 | 255.255.255.240 | 10.0.0.225 | 10.0.0.225 | 10.0.0.238  | 10.0.0.239 |

Spazio residuo: 10.0.0.240–10.0.0.255 disponibile per ulteriori subnet.
