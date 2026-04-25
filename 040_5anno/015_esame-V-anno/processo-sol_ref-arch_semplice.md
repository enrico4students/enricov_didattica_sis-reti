
Obiettivo:

* avere uno schema minimo sempre valido in modo da
* lavorare per estensione (ovviamente modifiche allo schema minimo sono possibili)

Ogni traccia tipicamente puòrichiederà **reti aggiuntive**  
(es. IoT, backup, big data, sedi multiple, cloud avanzato).  

Le strutture seguenti rappresentano **una base minima**  


---

# 1. Processo di soluzione (versione minimale)

## 1.1 Individuare gli elementi della traccia

Leggere la traccia e identificare:

* utenti (uffici, amministrazione, eventuale management)
* server interni
* servizi pubblici (web, API)
* Wi-Fi (interno e/o guest)
* eventuali sedi remote
* eventuale accesso remoto
* eventuale cloud

---

## 1.2 Definire le reti minime

In quasi tutte le tracce servono almeno:

* rete utenti
* rete server
* rete DMZ
* rete management
* rete Wi-Fi guest (se Wi-Fi presente)

Eventuali reti aggiuntive dipendono dalla traccia.

---

## 1.3 Separare le reti con VLAN

NB Normalmente le VLAN corrisponderanno 1 a 1 a (sotto)reti

Usare VLAN per:

* isolare utenti e server
* separare servizi pubblici (DMZ)
* isolare ospiti (guest Wi-Fi)
* proteggere la rete di management


---

## 1.4 DMZ e firewall

Scegliere il tipo di DMZ e specificarlo.

Lo edge firewall deve:

* separare Internet dalla rete interna
* proteggere la DMZ
* filtrare il traffico tra VLAN (direttamente o indirettamente)

valutare se sono necessari anche altri firewall interni

## 1.5 Gestire il Wi-Fi

Se presente normalmente ci sarà almeno:

* una rete Wi-Fi interna (accesso alla LAN)
* una rete Wi-Fi guest (solo Internet)

La traccia può inoltre richiedere che una o più VLAN aziendali siano accessibili tramite Wi-Fi.

In tal caso si associano uno o più SSID alle VLAN corrispondenti.

---

## 1.6 Gestire accessi remoti e sedi

Se richiesto:

* VPN per accesso remoto
* VPN site-to-site per sedi remote


---

## 1.7 Scrivere le regole principali

Sempre indicare:

* guest → solo Internet  
  Gli utenti guest possono navigare su Internet ma non devono accedere alla rete interna per motivi di sicurezza.

* utenti → server consentito   
  Gli utenti interni possono accedere ai server aziendali per utilizzare i servizi (applicativi, file, ecc.).  

* utenti → DB limitato  
  L’accesso diretto ai database deve essere limitato o mediato da applicazioni, per evitare accessi non autorizzati.

* DMZ → LAN limitato  
  I server in DMZ possono comunicare con la LAN interna solo per servizi specifici e controllati, riducendo il rischio di compromissione.

* management → accesso agli apparati  
  Solo la rete di management deve poter configurare e monitorare apparati di rete e server, per garantire sicurezza e controllo.

---


# 2. Reference architecture a 2 layers (semplice)

## 2.1 Quando usarla

Usare questa struttura quando:

* una sola sede
* numero limitato di utenti
* pochi switch
* rete semplice da spiegare

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

Prototipale = limitato alle tipologie di dispositivo. 
Ex. "Switch di accesso" compare una volta sola, ciò non significa che c'è un solo switch di accesso

```
Internet
    |
Router ISP
    |
Firewall (sicurezza e controllo traffico)
    |
    +------ DMZ (servizi pubblici)
    |         - Web server
    |         - API REST/SOAP
    |
Switch centrale (Layer 3)
    |
    +------ Rete server
    |         - server applicativi
    |         - database
    |
    +------ Switch di accesso
              |
              +-- PC utenti
              +-- Access Point Wi-Fi
              +-- Stampanti
```

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

* routing interno → switch Layer 3
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

Questo schema è solo **una base** di partenza da **estendere e modificare** in base a quanto richiesto dalla traccia. (Che avrete letto almeno 3 volte, meglio **almeno** 5)

---

# 3. Reference architecture a 3 layers (semplificata)

## 3.1 Quando usarla

Usare questa struttura quando:

* rete più grande
* più switch o più piani
* maggiore traffico

---

## 3.2 Schema logico

Schema prototipale, rappresenta tipologie di dispositivi. "access" indica una molteplicità di switch, Etc. (Router ISP. Edge firewall sono ovviamente unici, eventualmente ridondati)

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
* Core → trasporto veloce

---

## 3.4 VLAN minime

Uguali alla versione a 2 layers:

```
VLAN 10  MANAGEMENT
VLAN 20  UTENTI
VLAN 30  SERVER
VLAN 40  DMZ
VLAN 50  GUEST_WIFI
```

---

## 3.5 Spiegazione sintetica

* access collega utenti
* distribution aggrega e separa le VLAN
* core collega le varie parti della rete
* firewall gestisce sicurezza e accesso Internet

---

## 3.6 Modello frase esplicativa 

Ovviamente da personalizzare
“La rete è progettata secondo un modello gerarchico a tre livelli (access, distribution, core), che migliora scalabilità e prestazioni. Il firewall protegge la rete e separa la DMZ dai sistemi interni.”

---

# 4. Regole sempre valide (da ricordare)

* i database non devono essere esposti su Internet
* la DMZ contiene solo servizi pubblici
* il Wi-Fi guest deve essere isolato
* la rete di management deve essere separata
* il firewall controlla i flussi tra zone
* le VLAN servono per isolamento e sicurezza

---


# 6. Aggiunta: indirizzamento IP e VLSM

## 6.1 Rete privata di partenza

Per una prova d’esame si può scegliere una rete privata, ad esempio:

```
192.168.10.0/24
```

Da questa rete si ricavano sottoreti più piccole usando VLSM.

---

## 6.2 Esempio di fabbisogno host

| Rete       | Host richiesti |
| ---------- | -------------: |
| UTENTI     |             50 |
| SERVER     |             20 |
| GUEST_WIFI |             30 |
| MANAGEMENT |             10 |
| DMZ        |             10 |

---

## 6.3 Ordinare le reti dalla più grande alla più piccola

Con VLSM si parte sempre dalla rete con più host:

1. UTENTI → 50 host
2. GUEST_WIFI → 30 host
3. SERVER → 20 host
4. MANAGEMENT → 10 host
5. DMZ → 10 host

---

## 6.4 Piano di indirizzamento possibile

| VLAN | Nome       | Rete              | Netmask         | Gateway        | Host utilizzabili               |
| ---: | ---------- | ----------------- | --------------- | -------------- | ------------------------------- |
|   20 | UTENTI     | 192.168.10.0/26   | 255.255.255.192 | 192.168.10.1   | 192.168.10.1 - 192.168.10.62    |
|   50 | GUEST_WIFI | 192.168.10.64/27  | 255.255.255.224 | 192.168.10.65  | 192.168.10.65 - 192.168.10.94   |
|   30 | SERVER     | 192.168.10.96/27  | 255.255.255.224 | 192.168.10.97  | 192.168.10.97 - 192.168.10.126  |
|   10 | MANAGEMENT | 192.168.10.128/28 | 255.255.255.240 | 192.168.10.129 | 192.168.10.129 - 192.168.10.142 |
|   40 | DMZ        | 192.168.10.144/28 | 255.255.255.240 | 192.168.10.145 | 192.168.10.145 - 192.168.10.158 |

---

## 6.5 Broadcast delle sottoreti

| VLAN | Nome       | Rete              | Broadcast      |
| ---: | ---------- | ----------------- | -------------- |
|   20 | UTENTI     | 192.168.10.0/26   | 192.168.10.63  |
|   50 | GUEST_WIFI | 192.168.10.64/27  | 192.168.10.95  |
|   30 | SERVER     | 192.168.10.96/27  | 192.168.10.127 |
|   10 | MANAGEMENT | 192.168.10.128/28 | 192.168.10.143 |
|   40 | DMZ        | 192.168.10.144/28 | 192.168.10.159 |

---

## 6.6 Spazio libero per reti aggiuntive

La parte finale della rete rimane libera:

```
192.168.10.160 - 192.168.10.255
```

Può essere usata per reti aggiuntive richieste dalla traccia, ad esempio:

* sede secondaria
* IoT
* backup
* VPN
* laboratorio
* videosorveglianza
* rete amministrazione separata

---

## 6.7 Modello frase esplicativa da inserire, MODIFICATA E IN STILE STUDENTE, nella soluzione

“L’indirizzamento è stato progettato con tecnica VLSM, assegnando prima le sottoreti più grandi e poi quelle più piccole. Ogni VLAN corrisponde a una sottorete IP distinta, in modo da semplificare routing, sicurezza e applicazione delle ACL. Lo spazio non assegnato rimane disponibile per eventuali reti aggiuntive richieste dalla traccia.”

