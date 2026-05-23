
---

# PRIMA PARTE

## 1. Architettura della rete e sua evoluzione

### Ipotesi progettuali realistiche

* backbone regionale in **fibra ottica**
* rete basata su:

  * **IP/MPLS**
  * routing interno (OSPF o IS-IS)
* presenza di:

  * PoP distribuiti
  * data-center regionale (FSE)
* segmentazione logica tramite:

  * **VRF o MPLS L3VPN**

---

## Architettura esistente

La rete connette:

* enti locali
* scuole
* sanità pubblica
* data-center regionale

---

## Evoluzione per sanità privata

Introduzione di un nuovo dominio:

* strutture sanitarie private convenzionate
* accesso **solo al data-center**
* nessun accesso Internet

---

## Scelta progettuale fondamentale

Utilizzare:

* **VRF o MPLS L3VPN**

Motivazioni:

* isolamento completo tra strutture
* rispetto requisito traccia
* evitare ACL complesse
* maggiore sicurezza e scalabilità

---

## Schema architetturale (PlantUML)

```
@startuml
skinparam linetype ortho
skinparam shadowing false

cloud "Backbone Regionale" {

    node "Data Center Regionale\n(FSE, DB, Storage)" as DC

    frame "VRF SANITA PRIVATA" {
        node "Struttura 1" as S1
        node "Struttura 2" as S2
        node "Struttura N" as SN
    }

    frame "Altri domini" {
        node "Enti locali"
        node "Scuole"
        node "Sanità pubblica"
    }
}

S1 --> DC
S2 --> DC
SN --> DC

S1 -[hidden]-> S2

@enduml
```

---

# 2. Piano di indirizzamento

## Rete assegnata

```
10.100.0.0/16
```

---

## Requisiti

* circa 2000 strutture
* minimo 8 indirizzi ciascuna
* crescita futura

---

## Scelta subnet

### Analisi

* /29 → 8 indirizzi (6 utilizzabili) ❌ insufficiente
* /28 → 16 indirizzi (14 utilizzabili) ✔ corretto

---

## Motivazioni scelta /28

* soddisfa requisito minimo
* spazio per:

  * gateway
  * apparati
  * gestione
* margine di espansione
* scalabilità elevata

---

## Capacità complessiva

* subnet disponibili: 4096
* strutture richieste: ~2000
* ampia espandibilità futura

---

## Schema assegnazione

Pattern:

* incremento: 16
* gateway: primo indirizzo utile

---

## Tabella esempio

| Struttura | Subnet         | Gateway     | Range host     | Broadcast   |
| --------- | -------------- | ----------- | -------------- | ----------- |
| Str1      | 10.100.0.0/28  | 10.100.0.1  | 10.100.0.1–14  | 10.100.0.15 |
| Str2      | 10.100.0.16/28 | 10.100.0.17 | 10.100.0.17–30 | 10.100.0.31 |
| Str3      | 10.100.0.32/28 | 10.100.0.33 | 10.100.0.33–46 | 10.100.0.47 |

---

## Struttura logica indirizzamento

```
10.100.0.0/16
    ├── 10.100.0.0/28     → Struttura 1
    ├── 10.100.0.16/28    → Struttura 2
    ├── 10.100.0.32/28    → Struttura 3
    └── ...
```

---

## Scelta progettuale critica

❗ NON permettere routing tra subnet

Soluzioni:

* VRF (consigliato)
* oppure ACL centralizzate

✔ scelta preferita: VRF/MPLS

---

# 3. Dispositivo fornito (CPE)

## Tipologia

Router/firewall gestito centralmente

---

## Caratteristiche hardware

* 1 porta WAN:

  * SFP (fibra) o Ethernet
* 2–4 porte LAN Gigabit
* supporto:

  * VLAN 802.1Q
  * routing Layer 3
  * VPN IPsec
* CPU per cifratura
* memoria per logging

---

## Configurazione

* WAN:

  * IP statico dalla subnet assegnata
* LAN:

  * collegamento alla rete interna

---

## Servizi configurati

* routing verso backbone
* ACL restrittive:

  * traffico solo verso data-center
* VPN IPsec (opzionale ma consigliata)
* monitoraggio:

  * SNMP
  * syslog
* gestione remota:

  * SSH limitato

---

## Motivazione

* controllo centralizzato
* riduzione errori locali
* maggiore sicurezza

---

# 4. Integrazione con LAN esistente

## Scenario tipico

* LAN privata (es. 192.168.x.x)
* router Internet già presente

---

## Problema

* separare traffico sanitario da Internet
* evitare NAT verso rete regionale

---

## Soluzione

Rete separata tramite CPE

---

## Schema (PlantUML)

```
@startuml
skinparam linetype ortho
skinparam shadowing false

node "Router Internet" as R
node "LAN interna\n192.168.x.x" as LAN
node "CPE regionale\n10.100.x.x" as CPE
node "Backbone regionale" as BB

R --> LAN
LAN --> CPE
CPE --> BB

@enduml
```

---

## Variante evoluta

* separazione tramite VLAN dedicate

Motivazione:

* maggiore sicurezza
* migliore controllo traffico

---

# 5. Sicurezza

## Dati a riposo

* cifratura (AES-256)
* controllo accessi (RBAC)

---

## Dati in transito

* TLS
* VPN IPsec

Motivazione:

* dati sanitari → GDPR

---

## Rete

* isolamento tramite VRF
* blocco traffico laterale

---

## Logging

* audit accessi
* SIEM centrale

---

# 6. Trasferimento dati

## Modalità

* asincrona (batch)
* oppure near real-time per piccoli dati

---

## Motivazione

* file grandi (immagini/video)
* riduzione carico rete

---

## Schedulazione

* fascia notturna (22:00–06:00)

---

## Affidabilità

* retry automatico
* checksum
* trasferimenti resumable
* buffer locale

---

# SECONDA PARTE

## I. Gestione malfunzionamenti

Problemi:

* interruzione connessione
* errori scrittura

---

## Soluzioni

* buffer locale temporaneo
* retry automatico
* ACK applicativo
* checksum
* replica dati

---

## Storage

* RAID
* replica geografica
* backup

---

# II. Autenticazione utenti

## Soluzioni

* SPID
* CIE
* CNS

---

## MFA

* password + OTP
* app autenticazione
* certificati

---

## Motivazione

* accesso a dati sanitari → sicurezza elevata

---

# III. Pubblicazione server (NAT)

Scenario:

* 1 IP pubblico
* server interno

---

## Configurazione

```
ip nat inside source static tcp 192.168.1.10 80 interface WAN 80
ip nat inside source static tcp 192.168.1.10 443 interface WAN 443
ip nat inside source static tcp 192.168.1.10 22 interface WAN 22
```

---

## Misure di sicurezza

* limitare SSH per IP
* usare chiavi
* evitare password

---

# IV. Troubleshooting

## Metodo

1. verifica rete locale
2. verifica DNS
3. verifica routing

---

## Strumenti

* ping
* nslookup
* tracert

---

## Cause possibili

* gateway errato
* DNS non funzionante
* firewall

---

# CONCLUSIONE

## Scelte progettuali principali

* subnet /28 per scalabilità
* isolamento tramite VRF/MPLS
* separazione completa tra strutture
* nessun accesso Internet
* trasferimenti batch sicuri
* controllo centralizzato

---

