
# NOTA BENE

## Draft/ Work in progress, segnalare errori, sviste Etc.


# 0. Obiettivo  

* avere uno schema minimo di elementi ricorrenti in modo da  
* lavorare per estensione  


---

# 1. Processo di soluzione  

( Al momento parziale/embrionale, frammisto alle le architetture  )


## 1.1 Individuare comunità di attori "significative"   

Gruppi di utenti umani (ex. dipendenti, visitatori) ma anche di sistemi (ex. server interni)

---

## 1.2 Identificare reti e architettura  

Tipicamente ad ogni gruppo di attori corrisponde un segmento di rete dedicato, ex:  

* rete utenti "interni" (dipendenti o simili)
* rete "visitatori" (ex. Wi-Fi guest)
* rete DMZ (servers raggiungibili da internet, ex. WEB Server, API Endpoints)
* rete **server** interni (spesso utilizzati da server in DMZ, ex eventuale server RDBMS usato da server WEB, applicazioni di business specifiche all'azienda Etc.)
* rete management (separata logicamente o, in contesti di alta sicurezza, separatafisicamente)

* eventuali altre reti in dipendenza dalla traccia.


In base al numero di reti ed attori decidere se è più adatta una architettura di rete a 2 layers o a 3 (non confondere con il 3 tier delle architetture sistemiche!!!)  

(qui andrebbero indicati alcuni criteri quantitativi, TBD)  

---

## 1.3 Decidere le modalità precise di segmentazione

NB Normalmente le VLAN corrisponderanno 1:1 a (sotto)reti IP,  
è la pratica standard ma è **utile spiegarlo esplicitamente**  

Consigliabile inserire nella traccia i motivi anche se ovvi:  

* isolare utenti e server  
* esporre solo servizi pubblici (DMZ) e proteggere server interni (rete dedicata)  
* isolare ospiti (guest Wi-Fi)  
* proteggere la rete di management  
* Etc.  

---

## 1.4 DMZ e firewall

### 1.4.1
Normalmente avremo un edge firewall che deve:

* separare Internet dalla rete interna
* proteggere la DMZ
* filtrare il traffico  

**Sempre valutare se sono necessari anche altri firewall interni**  

### 1.4.2  

Scegliere il tipo di DMZ e motivare la scelta.

Abbiamo studiato due tipologie di DMZ nel libro di testo ...   
 

## 1.5 Gestire il Wi-Fi

Spesso avremo almeno:

* una rete Wi-Fi interna (accesso alla LAN "interni")
    - non infrequentemente dovremo avere, per N gruppi di utenti interni, N reti Wi-fi (SSID Service Set Identifier) mappate su N VLAN  
* una rete Wi-Fi guest (accesso solo a Internet)


---

## 1.6 Gestire accessi remoti e sedi

Se richiesto:

* VPN per accesso remoto client server, tipicamente di singolo dipendente (smart work)  
    - Specificare la "terminazione" TLS (se si è sicuri dell'argomento    
* VPN site-to-site per sedi remote  
    - consigliabile specificare gestione se si è sicuri dell'argomento   

---

## 1.7 Principali regole di accessibilità  

Se si è sicuri di averne il tempo specificare le connessioni consentite, anche qui abbiamo casi abbastanza comuni e ovvi che dovremmo conoscere a memoria per poterci focalizzare su eventuali specificità della traccia.  

Esempio di casi ricorrenti:  

* guest → solo Internet  
  Gli utenti guest possono navigare su Internet ma non devono accedere alla rete interna per motivi di sicurezza.

* utenti → server consentito   
  Gli utenti interni, in generale, possono accedere ai server aziendali "standard" per utilizzare i servizi (applicativi, file, ecc.).  
    - Se alcuni servizi/applicazioni sono confidenziali o dedicati solo ad alcuni gruppi ciò va gestito, quasi sempre con RBAC (role based access control) ma è possibile, e va valutato, sia necessario porre il server in segmenti di rete accessibil solo al gruppo di utenti interessati (la rete di gestione è un esempio di ciò in ambito tecnico, lo stesso può avvenire in ambito business)  

* utenti → DB limitato  
  In generale l’accesso **diretto** ai database non è consentito, normalmente è mediato da applicazioni.

* DMZ → LAN limitato  
  I server in DMZ possono comunicare con la LAN interna (meglio: con i segmenti di LAN interna) solo per servizi specifici e controllati, riducendo il rischio di compromissione.

* management → accesso agli apparati  
  Solo la rete di management deve poter configurare e monitorare apparati di rete e server. Solo gli amministratori devono avere accesso ad applicazioni e rete di management. Concetto utile da citare se lo si padroneggia: "bastion host"  

---

# Definire piano di indirizzamento   

Argomento chiave che va trattato a parte

Annotazioni dedicate disponibili

--- 



# 2. Reference architecture a 2 layers (semplice)

## 2.1 Quando usarla

Usare questa struttura quando:

* una sola sede  
* numero limitato di utenti  
* pochi switch  
* rete semplice  

---

## 2.2 Idea generale (prima di vedere lo schema)

La rete è divisa in due livelli:

* **Access** → dove si collegano i dispositivi (PC, Wi-Fi, stampanti)
* **Core/Distribution (collassato)** → dove si concentrano:

  * VLAN  
  * routing  
  * collegamento ai server  
  * uscita verso Internet  


Il firewall separa la rete interna da Internet e protegge i servizi pubblici.  

---

## 2.3 Schema prototipale

Uno diagramma con le reti più comuni e la DMZ di tipo meno "severo" potrebbe essere il seguente:  

```
Internet
    |
Router ISP
    |
Firewall / NGFW
(zone: WAN / LAN / DMZ)
    |
    +---------------------- DMZ (zona separata su interfaccia dedicata)
    |                         |
    |                         +-- Web Server
    |                         +-- API REST / SOAP
    |                         +-- Reverse Proxy / WAF (opzionale)
    |
    +---------------------- LAN (trunk verso core switch)
                              |
                    Switch centrale Layer 3
                    (routing inter-VLAN)
                              |
    -----------------------------------------------------------------
    |                |                |                |              |
VLAN interni     VLAN visitatori   VLAN server     VLAN management  (altre VLAN)
    |                |                |                |
    |                |                |                |
Switch accesso   Access Point     Server farm      Rete gestione
    |            (SSID guest)         |                |
    |                |                |                |
+-- PC dip.      +-- Smartphone   +-- App server   +-- Mgmt switch
+-- Laptop       +-- Notebook     +-- DB server    +-- Mgmt firewall
+-- Stampanti                     +-- File server  +-- Monitoring
```

Punti chiave:  

* La DMZ è collegata direttamente al firewall, NON passa dallo switch centrale
* Il firewall ha almeno 3 interfacce: WAN, LAN, DMZ (architettura “three-legged firewall”)
* Lo switch centrale Layer 3 gestisce tutte le VLAN interne
* Il routing interno (inter-VLAN) avviene sullo switch centrale (2 layers utilizzato per reti di dimensioni contenute)
* Il traffico tra VLAN può essere:

  * filtrato dallo switch L3 (ACL)
  * oppure forzato verso il firewall (design più sicuro, tipico enterprise)

Separazioni fondamentali:

* VLAN visitatori → solo Internet (isolata da tutte le altre)
* VLAN server interni → accessibile solo da VLAN autorizzate
* VLAN management → accessibile solo da amministratori
* DMZ → accessibile da Internet ma isolata dalla LAN



---

## 2.4 Spiegazione

### Internet → Router → Firewall

* il router collega l’azienda a Internet
* il firewall controlla tutto il traffico:

  * blocca accessi non autorizzati
  * permette solo i servizi necessari

---

### DMZ (zona intermedia)

* contiene i servizi pubblici
* è separata dalla rete interna
* serve per esporre servizi senza mettere a rischio la LAN

Esempio:

* sito web aziendale
* API pubbliche

---

### Switch centrale (core switch)

È il punto più importante della rete.

In una architettura a 2 layers questo dispositivo è uno **switch Layer 3 (collapsed core)** e svolge sia funzioni di core sia di distribution.

* gestisce le VLAN
* fa routing tra le VLAN (inter-VLAN routing), cioè instrada il traffico tra le reti interne (utenti, server, management, ecc.)
* collega:

  * server
  * utenti
  * accesso a Internet (tramite firewall)

**Chiarimento importante sul routing:**

* lo switch centrale gestisce il **routing interno**, cioè tra le reti locali (VLAN)
* il traffico destinato a Internet viene invece inviato al **firewall**, che a sua volta lo inoltra al **router ISP**

Quindi:

* routing interno       → switch Layer 3
* uscita verso Internet → firewall + router ISP

In questo modo si separano:

* il traffico interno (gestito velocemente dallo switch)
* il traffico esterno (controllato dal firewall per motivi di sicurezza)


---

### Rete server

Separata dagli utenti per sicurezza:

* server applicativi
* database

Motivazione:

* protezione dei dati
* controllo degli accessi
Di seguito il brano riscritto includendo la precisazione sugli switch gestiti:

---

### Switch di accesso

Collegano i dispositivi finali:

* PC utenti
* access point Wi-Fi
* stampanti

Sono generalmente **switch gestiti (managed switch)**, quindi configurabili dall’amministratore e in grado di supportare VLAN e altre funzionalità di rete.

Sono più “semplici” rispetto allo switch centrale perché:

* operano principalmente a livello 2 (switching, VLAN)
* non fanno routing tra reti
* non gestiscono logiche complesse di instradamento o sicurezza

Il loro compito è quindi collegare i dispositivi alla rete e inoltrare il traffico verso lo switch centrale.

---

## 2.5 Flusso del traffico  

Esempio: un utente apre un sito web interno

```
PC → switch access → switch centrale → server
```

Esempio: un utente naviga su Internet

```
PC → switch access → switch centrale → firewall → Internet
```

Esempio: un utente Internet accede al sito aziendale

```
Internet → firewall → DMZ → web server
```

---

## 2.6 Modello di frase esplicativa per traccia   

La rete è organizzata su due livelli: uno di accesso, che collega i dispositivi degli utenti, e uno centrale che gestisce VLAN e routing. Il firewall separa la rete interna da Internet e protegge la DMZ, dove sono collocati i servizi pubblici.

Va ovviamente **modificata**  

---

## 2.7 Reminder

Questo schema è solo **una base** di partenza da **estendere e modificare** in base a quanto richiesto dalla traccia. (Che in sede di esame prima di cominciare il lavoro architetturale avrete letto con attenzione più di una volta ...)  

---

# 3. Reference architecture a 3 layers (semplificata)

## 3.1 Quando usarla

Usare questa struttura quando:

* rete più grande
* più switch o più piani
* maggiore traffico

---

## 3.2 Schema logico

Schema **prototipale**, rappresenta tipologie di dispositivi.  
ex. "access" indica una tipologia, quindi una molteplicità di switch concreti, Etc.  
(Router ISP. Edge firewall sono ovviamente unici, eventualmente ridondati)

```
Internet
    |
Router ISP
    |
Firewall
    |
    +------ DMZ
    |        - Web server
    |        - API
    |
Core (Layer 3)
    |
    +------ Distribution
    |        |
    |        +------ Access
    |               - utenti
    |               - AP Wi-Fi
    |
    +------ Server farm
             - server applicativi
             - database
```

---

## 3.3 Ruolo dei livelli

* Access → dispositivi finali
* Distribution → aggregazione e VLAN
* Core → trasporto veloce, backbone interno ad alte prestazioni  

---

## 3.4 VLAN tipiche  

Qulle ricorrenti sono le stesse discusse inzialmente e viste nel 2 layers, ad esempio:

```
VLAN 10  MANAGEMENT
VLAN 20  UTENTI
VLAN 30  SERVER INTERNI
VLAN 40  DMZ
VLAN 50  GUEST_WIFI
Etc.
```

Il 3 layer si usa su reti più complesse/estese quindi l'implementazione tenderà ad essere più estesa  

---

## 3.5 Spiegazione sintetica

* **access layer**: collega utenti   
* **distribution layer**: aggrega e separa le VLAN
* **core layer**: collega le varie parti della rete
* **edge firewall**: gestisce sicurezza e accesso Internet
* **internal firewals**: protezione interna, ad hoc o nel distribution layer 

---

## 3.6 Modello frase esplicativa 

Ovviamente da personalizzare nello svolgimento:  
“La rete è progettata secondo un modello gerarchico a tre livelli (access, distribution, core), che migliora scalabilità e prestazioni. Il firewall protegge la rete e separa la DMZ dai sistemi interni.”

---

# 4. Regole tipiche  

* database (server DB e server interni) non devono essere esposti su Internet
* la DMZ contiene solo servizi pubblici
* il Wi-Fi guest deve essere isolato
* la rete di management deve essere separata
* il firewall controlla i flussi tra zone
* le VLAN servono per isolamento e sicurezza


---

# 6. Addizionale: indirizzamento IP e VLSM

A fronte del fatto che l'argomento sembra presentare difficoltà per alcuni studenti viene riportato un esempio (NB vi sono annotazioni dedicate ai piani di indirizzamento)  

## 6.1 Rete privata di partenza

Si utilizzi una rete privata di classe C:

```
192.168.10.0/24
```

Questa rete verrà suddivisa tramite VLSM.

---

## 6.2 Fabbisogno host

| Rete       | Dispositivi | Gateway | Totale richiesto |
| ---------- | ----------: | ------: | ---------------: |
| UTENTI     |          50 |       1 |               51 |
| GUEST_WIFI |          30 |       1 |               31 |
| SERVER     |          20 |       1 |               21 |
| MANAGEMENT |          10 |       1 |               11 |
| DMZ        |          10 |       1 |               11 |

---

## 6.3 Scelta delle subnet (VLSM)

Si sceglie la subnet minima che soddisfa ogni fabbisogno:

| Rete       | Totale richiesto | Subnet scelta | Host disponibili |
| ---------- | ---------------- | ------------- | ---------------- |
| UTENTI     | 51               | /26           | 62               |
| GUEST_WIFI | 31               | /26           | 62               |
| SERVER     | 21               | /27           | 30               |
| MANAGEMENT | 11               | /28           | 14               |
| DMZ        | 11               | /28           | 14               |

---

## 6.4 Ordinamento (VLSM)

Si assegnano le reti dalla più grande alla più piccola:

1. UTENTI (/26)
2. GUEST_WIFI (/26)
3. SERVER (/27)
4. MANAGEMENT (/28)
5. DMZ (/28)

---

## 6.5 Piano di indirizzamento

| VLAN | Nome       | Rete              | Netmask         | Gateway        | Host utilizzabili               |
| ---: | ---------- | ----------------- | --------------- | -------------- | ------------------------------- |
|   20 | UTENTI     | 192.168.10.0/26   | 255.255.255.192 | 192.168.10.1   | 192.168.10.1 - 192.168.10.62    |
|   50 | GUEST_WIFI | 192.168.10.64/26  | 255.255.255.192 | 192.168.10.65  | 192.168.10.65 - 192.168.10.126  |
|   30 | SERVER     | 192.168.10.128/27 | 255.255.255.224 | 192.168.10.129 | 192.168.10.129 - 192.168.10.158 |
|   10 | MANAGEMENT | 192.168.10.160/28 | 255.255.255.240 | 192.168.10.161 | 192.168.10.161 - 192.168.10.174 |
|   40 | DMZ        | 192.168.10.176/28 | 255.255.255.240 | 192.168.10.177 | 192.168.10.177 - 192.168.10.190 |

Nota: il gateway è incluso nel range degli host utilizzabili ed è stato scelto come primo indirizzo disponibile.

---

## 6.6 Broadcast delle sottoreti

| VLAN | Nome       | Rete              | Broadcast      |
| ---: | ---------- | ----------------- | -------------- |
|   20 | UTENTI     | 192.168.10.0/26   | 192.168.10.63  |
|   50 | GUEST_WIFI | 192.168.10.64/26  | 192.168.10.127 |
|   30 | SERVER     | 192.168.10.128/27 | 192.168.10.159 |
|   10 | MANAGEMENT | 192.168.10.160/28 | 192.168.10.175 |
|   40 | DMZ        | 192.168.10.176/28 | 192.168.10.191 |

---

## 6.7 Spazio residuo

Notare che rimane disponibile il seguente intervallo:

```
192.168.10.192 - 192.168.10.255
```

---

## 6.7 Modello frase esplicativa da inserire, MODIFICATA E IN STILE STUDENTE, nella soluzione

“L’indirizzamento è stato progettato con tecnica VLSM, assegnando prima le sottoreti più grandi e poi quelle più piccole. Ogni VLAN corrisponde a una sottorete IP distinta, in modo da semplificare routing, sicurezza e applicazione delle ACL. Lo spazio non assegnato rimane disponibile per eventuali reti aggiuntive richieste dalla traccia.”

