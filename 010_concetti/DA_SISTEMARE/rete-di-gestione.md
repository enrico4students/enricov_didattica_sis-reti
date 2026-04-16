## Reti di gestione (Management Network)

Normalmente la gestione degli apparati (switch, router, firewall, access point, server) non avviene sulla stessa rete utilizzata dagli utenti o dai servizi applicativi. 
Viene realizzata una rete **dedicata alla gestione**, progettata per garantire sicurezza, controllo e affidabilità.


Una **rete di gestione** è una rete **separata **utilizzata esclusivamente per:

* configurare i dispositivi (SSH, HTTPS, console remota)
* monitorare lo stato (SNMP, telemetry, syslog)
* aggiornare firmware e software
* raccogliere log e metriche

L’obiettivo è evitare che il traffico di gestione sia esposto o interferisca con il traffico operativo.

---

## Separazione della rete di gestione

La separazione può essere realizzata in due modi principali.

### 1. Separazione logica (più comune)

Si utilizza una **VLAN dedicata alla gestione** (es. VLAN 80 Management):

* ogni dispositivo ha un indirizzo IP **di management**
* il traffico di gestione viaggia su VLAN separata
* accessibile solo da host autorizzati (es. PC amministratore, jump server)

Questo approccio è molto diffuso perché:

* semplice da implementare
* non richiede cablaggio aggiuntivo
* sufficiente nella maggior parte dei contesti aziendali

---

### 2. Separazione fisica (più sicura)

Si utilizza una rete completamente separata:

* switch **dedicati** alla gestione
* interfacce di management fisiche (es. porta “mgmt”)
* cablaggio **indipendente**

È tipica di ambienti critici:

* data center
* infrastrutture militari o industriali
* ambienti con requisiti elevati di sicurezza

---

## Indirizzamento e accesso

Ogni dispositivo di rete dispone di un indirizzo IP **di management**:

* associato a una **SVI** (negli switch L3) oppure
* assegnato a una **interfaccia dedicata** (router/firewall)

L’accesso deve essere rigidamente controllato:

* consentire solo protocolli sicuri (SSH, HTTPS)
* limitare gli IP sorgente (ACL, firewall)
* autenticazione centralizzata (RADIUS, TACACS+)

---

## Servizi tipici nella rete di gestione

All’interno della rete di management operano servizi specifici:

* **SSH / HTTPS** → configurazione remota
* **SNMP** → monitoraggio
* **Syslog** → raccolta log centralizzata
* **NTP** → sincronizzazione oraria
* **NetFlow / telemetry** → analisi traffico

Spesso viene introdotto un **server di gestione centralizzato** (NMS – Network Management System), che raccoglie dati da tutti i dispositivi.
Lo NMS spesso è una sorgente dati per i sistemi di cybersecurity:
- legame più importante è con un sistema come SIEM
  - L’NMS raccoglie dati (SNMP, log, metriche)
  - Il SIEM li correla con eventi di sicurezza
ex aumento anomalo traffico su una porta → NMS lo rileva
il SIEM lo correla con tentativi di accesso → possibile attacco

- IDS / IPS (sistemi che analizzano il traffico per individuare attacchi).
  - NMS fornisce contesto (topologia, dispositivi coinvolti)
  - IDS/IPS rileva pattern malevoli

- SOAR (automazione della risposta)
  - NMS rileva un’anomalia (es. device down o traffico anomalo)
  - SIEM la classifica come minaccia
  - SOAR esegue automaticamente azioni (es. isolamento VLAN, blocco IP)


---

## Best practices

Una rete di gestione deve rispettare i seguenti principi:

* isolamento dal traffico utente e da Internet
* accesso consentito solo da postazioni autorizzate
* utilizzo esclusivo di protocolli cifrati
* logging centralizzato di tutte le operazioni
* possibilità di accesso anche in caso di guasto della rete principale

E' importante evitare che un utente compromesso possa raggiungere la rete di gestione: per questo motivo spesso viene filtrata direttamente dal firewall o completamente isolata.

---

## Sintesi  

Nelle architetture a 2 layer o 3 layer, la rete di gestione è tipicamente:

* una VLAN dedicata trasportata in trunk sugli switch
* terminata su un firewall o su uno switch L3
* accessibile solo da una zona amministrativa



## Puntualizzazione "rete di gestione terminata su un firewall o su uno switch L3"

**“Terminata”** indica il punto della rete in cui una VLAN **smette di essere solo traffico Layer 2 (switching)** e viene associata a una **interfaccia Layer 3 con indirizzo IP**, cioè dove avviene il routing.

In termini semplici:

* finché la VLAN è sugli switch → è solo traffico L2 (frame Ethernet)
* nel punto di terminazione → diventa una **rete IP con gateway**

---

## VLAN di management terminata su firewall

* la VLAN (es. VLAN 80) arriva al firewall tramite trunk
* sul firewall esiste una **interfaccia (fisica o subinterfaccia VLAN)** con IP, ad esempio:

  * 10.10.80.1 → gateway della rete di management  

Effetto pratico

* tutti i dispositivi di rete (switch, AP, router) hanno IP nella VLAN 80
* usano il firewall come **gateway**
* il firewall può:

  * filtrare accessi (ACL, policy)
  * permettere solo SSH/HTTPS solo da host autorizzati
  * bloccare completamente l’accesso da altre VLAN

La rete di management è **controllata dal firewall**, quindi:

* massima sicurezza
* visibilità completa del traffico di gestione
* possibilità di logging e auditing

---

## VLAN di management terminata su switch Layer 3

Significa che:

* la VLAN arriva allo switch L3
* sullo switch è configurata una **SVI (Switch Virtual Interface)**, ad esempio:

  * interface vlan 80
    ip address 10.10.80.1

Quindi

* lo switch L3 diventa il **gateway della VLAN di management**
* il routing tra VLAN avviene direttamente nello switch
* il traffico può non passare dal firewall

La gestione è:

* più veloce (routing locale nello switch)
* meno controllata dal punto di vista della sicurezza (se non si applicano ACL)

---

## Differenze fra i due approcci

* Terminazione su firewall
  → priorità alla sicurezza, controllo centralizzato

* Terminazione su switch L3
  → priorità a prestazioni e semplicità interna

---

## Esempio  

Si consideri:

* VLAN 80 = management
* IP rete: 10.10.80.0/24

### Caso firewall

* firewall: 10.10.80.1
* switch: 10.10.80.10
* accesso consentito solo da PC admin

→ tutto il traffico passa dal firewall

---

### Caso switch L3

* SVI switch: 10.10.80.1
* firewall vede il traffico solo se diretto fuori

→ meno controllo, ma più efficienza interna


