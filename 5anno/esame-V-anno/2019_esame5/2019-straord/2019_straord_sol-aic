Sistemi e reti - 2019 straordinaria

---

PRIMA PARTE

---

1. PROGETTO DELL’INFRASTRUTTURA TECNOLOGICA

---

ANALISI DEL CONTESTO

Vincoli:

* 6 reparti su 3 piani
* Medici con tablet aziendali
* Accesso wireless
* Server interno in locale tecnico (seminterrato)
* Farmacia collegata allo stesso server
* Autenticazione obbligatoria
* Divieto accesso a siti non autorizzati
* Trattamento dati sanitari (dati sensibili)

Ipotesi aggiuntive ragionevoli:

* 1 armadio rack per piano
* dorsale in fibra ottica verticale
* switch L3 centrale nel locale tecnico
* VLAN separate per segmentazione
* server virtualizzato

---

## 1.1 Architettura di rete

Topologia: gerarchica a stella estesa


    @startuml
    skinparam linetype ortho
    skinparam shadowing false
    hide stereotype

    frame "Ospedale - Infrastruttura rete" {

    node "Piano 1" as P1 {
        node "Reparto A" as RA {
        device "AP A (PoE)\nSSID: MEDICI\nWPA2/WPA3-Enterprise\n802.1X/RADIUS" as APA
        }
        node "Reparto B" as RB {
        device "AP B (PoE)\nSSID: MEDICI\nWPA2/WPA3-Enterprise\n802.1X/RADIUS" as APB
        }
        node "Armadio Piano 1" as RACK1 {
        device "Switch L2 Piano 1\nPoE per AP\nTrunk 802.1Q verso Core" as SW1
        }
    }

    node "Piano 2" as P2 {
        node "Reparto C" as RC {
        device "AP C (PoE)\nSSID: MEDICI\nWPA2/WPA3-Enterprise\n802.1X/RADIUS" as APC
        }
        node "Reparto D" as RD {
        device "AP D (PoE)\nSSID: MEDICI\nWPA2/WPA3-Enterprise\n802.1X/RADIUS" as APD
        }
        node "Armadio Piano 2" as RACK2 {
        device "Switch L2 Piano 2\nPoE per AP\nTrunk 802.1Q verso Core" as SW2
        }
    }

    node "Piano 3" as P3 {
        node "Reparto E" as RE {
        device "AP E (PoE)\nSSID: MEDICI\nWPA2/WPA3-Enterprise\n802.1X/RADIUS" as APE
        }
        node "Reparto F" as RF {
        device "AP F (PoE)\nSSID: MEDICI\nWPA2/WPA3-Enterprise\n802.1X/RADIUS" as APF
        }
        node "Armadio Piano 3" as RACK3 {
        device "Switch L2 Piano 3\nPoE per AP\nTrunk 802.1Q verso Core" as SW3
        }
    }

    node "Piano Seminterrato" as PS {
        node "Locale Tecnico" as LT {
        device "Core Switch L3\nSVI VLAN 10/20/30/99\nRouting inter-VLAN\nACL di base" as CORE
        device "Firewall\nPolicy inter-VLAN\nNAT/Internet (se presente)\nLogging" as FW
        device "Proxy filtrante\nWhitelist siti" as PROXY
        node "DMZ/Server VLAN 30" as DMZ {
            device "Web Server (HTTPS/TLS)\nApp Terapie" as WEB
            database "DB Server\nTerapie" as DB
        }
        device "RADIUS/AAA\n(AD/LDAP)" as RAD
        device "DNS interno" as DNS
        device "DHCP (VLAN 10)\n(oppure su Core/FW)" as DHCP
        device "NTP" as NTP
        }

        node "Farmacia" as FARM {
        device "PC Farmacia\nAccesso applicazione" as PCF
        }
    }

    cloud "Internet\n(opzionale)" as NET

    device "Tablet Medico\nsolo aziendali" as TAB

    TAB ..> APA : WiFi\nVLAN 10
    TAB ..> APB : WiFi\nVLAN 10
    TAB ..> APC : WiFi\nVLAN 10
    TAB ..> APD : WiFi\nVLAN 10
    TAB ..> APE : WiFi\nVLAN 10
    TAB ..> APF : WiFi\nVLAN 10

    APA -- SW1
    APB -- SW1
    APC -- SW2
    APD -- SW2
    APE -- SW3
    APF -- SW3

    SW1 -- CORE : Fibra (1/10G)\nTrunk 802.1Q
    SW2 -- CORE : Fibra (1/10G)\nTrunk 802.1Q
    SW3 -- CORE : Fibra (1/10G)\nTrunk 802.1Q

    PCF -- CORE : Ethernet\nVLAN 20

    CORE -- FW : uplink\nVLAN trunk / routed
    FW -- PROXY : HTTP/HTTPS\npolicy di uscita
    PROXY -- NET : (se consentito)

    FW -- WEB : HTTPS (TLS)\nconsentito da VLAN 10/20
    WEB -- DB : SQL\nsolo VLAN 30

    RAD -- FW : AAA (RADIUS)
    RAD -- CORE : 802.1X/RADIUS
    DNS -- WEB
    DHCP -- CORE
    NTP -- WEB
    NTP -- DB

    note right of CORE
        VLAN 10: Medici WiFi 192.168.10.0/24
        VLAN 20: Farmacia  192.168.20.0/24
        VLAN 30: Server    192.168.30.0/24
        VLAN 99: Mgmt      192.168.99.0/24
    end note
    }

    @enduml  



Struttura:

Tablet (WiFi)
↓
Access Point (PoE)
↓
Switch di piano (L2)
↓ (fibra)
Core Switch L3 (locale tecnico)
↓
Firewall
↓
Server Web + DB
↓
Collegamento farmacia

Caratteristiche:

* Dorsale: fibra ottica multimodale 1/10 Gbps
* Accesso: Ethernet 1 Gbps
* WiFi: 802.11ac/ax
* VLAN per separazione traffico

Segmentazione proposta:

VLAN 10 – Medici (WiFi)
VLAN 20 – Farmacia
VLAN 30 – Server
VLAN 99 – Management

Motivazione:

* isolamento traffico
* controllo ACL
* maggiore sicurezza
* applicazione firewall inter-VLAN

Routing inter-VLAN effettuato dallo switch L3 centrale.

---

## 1.2 Piano di indirizzamento

Si utilizza rete privata 192.168.0.0/16

Scelta: una subnet per VLAN

VLAN 10 – 192.168.10.0/24
VLAN 20 – 192.168.20.0/24
VLAN 30 – 192.168.30.0/24
VLAN 99 – 192.168.99.0/24

Esempio assegnazioni:

Gateway VLAN 10 → 192.168.10.1
Gateway VLAN 20 → 192.168.20.1
Gateway VLAN 30 → 192.168.30.1

Server web → 192.168.30.10
Server DB → 192.168.30.20
Firewall → 192.168.30.254

Motivazione:

* subnet /24 sufficienti
* struttura chiara
* correlazione VLAN-numero subnet

---

## 1.3 Servizi di rete

DHCP

* attivo per VLAN 10 (tablet)
* disattivo per server (IP statici)

DNS interno

* risoluzione nome server (es. terapia.ospedale.local)

RADIUS

* autenticazione 802.1X WiFi
* integrazione con Active Directory

Firewall

* blocco traffico Internet
* consentito solo traffico HTTPS verso server interno
* blocco accesso da VLAN 10 verso VLAN 20

Proxy filtrante

* whitelist domini consentiti

NTP

* sincronizzazione oraria per audit

HTTPS

* certificato interno
* TLS obbligatorio

Backup

* snapshot giornalieri DB
* replica secondaria

---

2. PROGETTO BASE DI DATI

---

ANALISI ENTITÀ PRINCIPALI

Entità:

MEDICO
REPARTO
PAZIENTE
VISITA
PARAMETRI_VITALI
PRESCRIZIONE
FARMACO

Relazioni:

* Un medico effettua molte visite
* Una visita riguarda un paziente
* Una visita può generare più prescrizioni
* Una prescrizione può includere più farmaci

---

2.1 Modello concettuale (E-R descritto)

MEDICO (id_medico, nome, cognome, reparto)
REPARTO (id_reparto, nome, piano)
PAZIENTE (id_paziente, nome, cognome, data_nascita)
VISITA (id_visita, data_ora, note)
PARAMETRI (pressione_min, pressione_max, temperatura, freq_cardiaca)
PRESCRIZIONE (id_prescrizione, posologia)
FARMACO (id_farmaco, nome, descrizione)

Relazioni:

MEDICO — effettua — VISITA (1:N)
PAZIENTE — riceve — VISITA (1:N)
VISITA — genera — PRESCRIZIONE (1:N)
PRESCRIZIONE — include — FARMACO (N:M)

PlantUML (E-R)

```
@startuml
hide circle
skinparam linetype ortho

entity "MEDICO" as MEDICO {
  * id_medico : int <<PK>>
  --
  nome : varchar
  cognome : varchar
  id_reparto : int <<FK>>
}

entity "REPARTO" as REPARTO {
  * id_reparto : int <<PK>>
  --
  nome : varchar
  piano : int
}

entity "PAZIENTE" as PAZIENTE {
  * id_paziente : int <<PK>>
  --
  nome : varchar
  cognome : varchar
  data_nascita : date
}

entity "VISITA" as VISITA {
  * id_visita : int <<PK>>
  --
  data_ora : datetime
  note : text
  id_medico : int <<FK>>
  id_paziente : int <<FK>>
}

entity "PARAMETRI" as PARAMETRI {
  * id_visita : int <<PK,FK>>
  --
  pressione_min : int
  pressione_max : int
  temperatura : decimal
  freq_cardiaca : int
}

entity "PRESCRIZIONE" as PRESCRIZIONE {
  * id_prescrizione : int <<PK>>
  --
  id_visita : int <<FK>>
}

entity "FARMACO" as FARMACO {
  * id_farmaco : int <<PK>>
  --
  nome : varchar
  descrizione : text
}

entity "PRESCRIZIONE_FARMACO" as PF {
  * id_prescrizione : int <<PK,FK>>
  * id_farmaco : int <<PK,FK>>
  --
  posologia : varchar
}

REPARTO ||--o{ MEDICO : "assegna"
MEDICO  ||--o{ VISITA : "effettua"
PAZIENTE||--o{ VISITA : "riceve"
VISITA  ||--|| PARAMETRI : "ha"
VISITA  ||--o{ PRESCRIZIONE : "genera"
PRESCRIZIONE ||--o{ PF : "include"
FARMACO      ||--o{ PF : "composto da"
@enduml
```

---

## 2.2 Modello logico relazionale

MEDICO(
id_medico PK,
nome,
cognome,
id_reparto FK
)

REPARTO(
id_reparto PK,
nome,
piano
)

PAZIENTE(
id_paziente PK,
nome,
cognome,
data_nascita
)

VISITA(
id_visita PK,
data_ora,
note,
id_medico FK,
id_paziente FK
)

PARAMETRI(
id_visita PK FK,
pressione_min,
pressione_max,
temperatura,
freq_cardiaca
)

PRESCRIZIONE(
id_prescrizione PK,
id_visita FK
)

FARMACO(
id_farmaco PK,
nome,
descrizione
)

PRESCRIZIONE_FARMACO(
id_prescrizione FK,
id_farmaco FK,
posologia,
PRIMARY KEY(id_prescrizione, id_farmaco)
)

Motivazioni:

* separazione parametri per normalizzazione
* tabella ponte per relazione N:M

PlantUML (modello logico relazionale)

```
@startuml
hide methods
hide stereotypes
skinparam linetype ortho

class REPARTO {
  +id_reparto : int <<PK>>
  nome : varchar
  piano : int
}

class MEDICO {
  +id_medico : int <<PK>>
  nome : varchar
  cognome : varchar
  id_reparto : int <<FK>>
}

class PAZIENTE {
  +id_paziente : int <<PK>>
  nome : varchar
  cognome : varchar
  data_nascita : date
}

class VISITA {
  +id_visita : int <<PK>>
  data_ora : datetime
  note : text
  id_medico : int <<FK>>
  id_paziente : int <<FK>>
}

class PARAMETRI {
  +id_visita : int <<PK,FK>>
  pressione_min : int
  pressione_max : int
  temperatura : decimal
  freq_cardiaca : int
}

class PRESCRIZIONE {
  +id_prescrizione : int <<PK>>
  id_visita : int <<FK>>
}

class FARMACO {
  +id_farmaco : int <<PK>>
  nome : varchar
  descrizione : text
}

class PRESCRIZIONE_FARMACO {
  +id_prescrizione : int <<PK,FK>>
  +id_farmaco : int <<PK,FK>>
  posologia : varchar
}

REPARTO "1" -- "0..*" MEDICO : id_reparto
MEDICO "1" -- "0..*" VISITA : id_medico
PAZIENTE "1" -- "0..*" VISITA : id_paziente
VISITA "1" -- "1" PARAMETRI : id_visita
VISITA "1" -- "0..*" PRESCRIZIONE : id_visita
PRESCRIZIONE "1" -- "0..*" PRESCRIZIONE_FARMACO : id_prescrizione
FARMACO "1" -- "0..*" PRESCRIZIONE_FARMACO : id_farmaco
@enduml
```

---

3. PROGETTO PAGINE WEB FARMACIA

---

Funzioni richieste:

* visualizzare elenco giornaliero farmaci per reparto
* filtro per data
* raggruppamento per reparto

Esempio SQL:

SELECT r.nome,
f.nome,
pf.posologia
FROM PRESCRIZIONE p
JOIN VISITA v ON p.id_visita = v.id_visita
JOIN MEDICO m ON v.id_medico = m.id_medico
JOIN REPARTO r ON m.id_reparto = r.id_reparto
JOIN PRESCRIZIONE_FARMACO pf ON p.id_prescrizione = pf.id_prescrizione
JOIN FARMACO f ON pf.id_farmaco = f.id_farmaco
WHERE DATE(v.data_ora) = CURDATE()
ORDER BY r.nome;

Esempio porzione PHP:

```
<?php
$conn = new mysqli("localhost","user","pass","ospedale");
$query = "...";
$result = $conn->query($query);
while($row = $result->fetch_assoc()) {
    echo "<tr>";
    echo "<td>".$row['nome']."</td>";
    echo "<td>".$row['posologia']."</td>";
    echo "</tr>";
}
?>
```

---

SECONDA PARTE
Scelti quesiti I e II
---------------------

I. Visualizzazione storico parametri vitali

Query:

SELECT data_ora,
pressione_min,
pressione_max,
temperatura,
freq_cardiaca
FROM VISITA v
JOIN PARAMETRI p ON v.id_visita = p.id_visita
WHERE id_paziente = ?
ORDER BY data_ora DESC;

Interfaccia:

* grafico andamento pressione
* tabella cronologica

Motivazione:

* supporto decisionale medico
* monitoraggio trend

---

II. Sicurezza e continuità

1. Impedire uso dispositivi non autorizzati

   * 802.1X con certificati
   * MDM (Mobile Device Management)
   * MAC filtering (non sufficiente da solo)

2. Autenticazione utenti

   * LDAP / Active Directory
   * autenticazione a due fattori
   * ruoli (RBAC)

3. Continuità servizio

   * server ridondato
   * RAID 1/5
   * backup giornaliero
   * UPS
   * replica database

4. Protezione dati

   * HTTPS (TLS)
   * cifratura database at-rest
   * firewall applicativo

Motivazione:

* dati sanitari = categoria speciale GDPR
* necessaria alta affidabilità

---

AREE TEMATICHE COINVOLTE

* Progettazione reti LAN
* VLAN e routing inter-VLAN
* Piano di indirizzamento IPv4
* Servizi di rete (DHCP, DNS, RADIUS)
* Sicurezza wireless 802.1X
* Firewall e segmentazione
* Modellazione E-R
* Normalizzazione database
* SQL join complesse
* Web application architecture
* Sicurezza applicativa
* Continuità operativa e ridondanza


