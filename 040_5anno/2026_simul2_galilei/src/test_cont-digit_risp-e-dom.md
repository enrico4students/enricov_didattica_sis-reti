# Sistemi e Reti - Esercizio di preparazione a prova d’esame

## PRIMA PARTE

## Azienda di produzione contenuti digitali per il turismo con nuova sede operativa

Una società che opera nel settore della produzione di contenuti digitali per il turismo apre una nuova sede operativa in un’altra città.

L’azienda realizza video promozionali, contenuti social, pagine informative, cataloghi digitali e materiali multimediali destinati a portali turistici, agenzie di viaggio, strutture ricettive ed enti locali.

All’interno della sede sono previsti i seguenti reparti produttivi:

* Reparto A) Creazione contenuti multimediali per dispositivi mobili
* Reparto B) Creazione contenuti web e pagine informative
* Reparto C) Produzione contenuti digitali avanzati per aziende turistiche

Sono inoltre presenti:

* Reparto D) Revisione, controllo qualità e validazione contenuti
* Reparto E) Coordinamento progetti editoriali e gestione pubblicazioni
* Reparto F) Area amministrativa e gestione contratti

Ogni addetto dispone di una postazione desktop aziendale.

Distribuzione prevista:

| Reparto     | A  | B  | C  | D  | E  | F  |
| ----------- | -- | -- | -- | -- | -- | -- |
| N° computer | 48 | 32 | 96 | 22 | 12 | 18 |

Ogni reparto prevede fino al 10% di postazioni aggiuntive di riserva.

L’accesso ai sistemi deve avvenire tramite autenticazione.

## Vincoli operativi

Gli operatori dei reparti A, B, C devono accedere a:

* Internet
* stampante di reparto
* archivio/file server locale del proprio reparto

Non deve invece essere consentito loro di accedere agli archivi interni degli altri reparti produttivi.

Il reparto D deve:

* accedere agli archivi dei reparti A, B, C
* verificare e validare i contenuti prodotti
* salvare report di revisione
* marcare i contenuti approvati aggiungendo un suffisso al nome della cartella, ad esempio “_APPROVATO”
* rendere i contenuti approvati non modificabili

Il reparto E deve:

* accedere a tutti gli archivi locali della sede
* raccogliere i contenuti approvati
* trasferirli verso un repository centrale remoto presso la sede principale
* aggiungere metadati, documentazione e informazioni di pubblicazione

Il reparto F deve:

* accedere a Internet
* accedere al sistema gestionale remoto presso la sede centrale, usato per contratti, fatturazione e clienti

## Richieste

Il candidato analizzi la situazione e sviluppi:

1. un progetto di massima dell’infrastruttura di rete della nuova sede, anche supportato da uno schema grafico, prevedendo struttura delle sottoreti, apparati, servizi implementati, tipologia delle connessioni interne e verso Internet e un opportuno piano di indirizzamento;

2. le misure e i sistemi per la gestione della sicurezza interna ed esterna;

3. le modalità e i protocolli di collegamento verso i sistemi remoti nella sede centrale;

4. i dettagli di configurazione di uno dei servizi.

---

# SECONDA PARTE

## Quesito I

Il candidato esponga le tipologie di firewall in relazione ai due ruolo di  
- edge/perimeter firewall  
- internal firewall  

Spieghi la relazione fra firewall e le tipologie di DMZ studiate  

---

## Quesito II

In relazione al tema proposto nella prima parte, si immagini di voler concentrare i vari server locali su un unico server fisico molto potente di cui si intende sfruttare pienamente la potenza elaborativa.

Il candidato illustri:

* Le modalità di realizzazione di questo obiettivo e scelga quella che ritiene più migliore, specificando le motivazioni e le eventuali alternative scartate, anche queste con motivazioni

* quali modifiche all’infrastruttura di rete e alla sua configurazione logica e fisica si renderebbero eventualmente necessarie per implementare la modalità scelta

---

## Quesito III

Il candidato definisca con quali modalità implementare la sicurezza della rete WIFI in modo che sia massima relativamente a stanards/tecnologie attuali.  

Uno degli ingegneri interni "storici" spinge per l'adozione di WPE sostenendo che è semplice ed è adeguata.  
Analizzare se la sua posizione è valida.

---

## Quesito IV

In relazione al tema proposto nella prima parte, si ipotizzi che presso la sede centrale siano presenti, oltre al repository remoto dei contenuti e al sistema gestionale, anche alcuni server pubblici per offrire i seguenti servizi:

* endpoint REST per consentire ricerche e accesso ai contenuti da programma
* VPN per smartwork, che preserva i normali limiti di accesso

Descrivere tale parte dell’infrastruttura di rete dell’azienda.


---

# SOLUZIONE

## PRIMA PARTE

## 1. Analisi del problema

La sede operativa deve ospitare reparti con esigenze diverse. La scelta più importante non è solo collegare tutti i computer alla rete, ma separare correttamente i reparti.

I reparti A, B e C producono contenuti digitali diversi. Ciascun reparto deve lavorare sul proprio archivio locale e non deve accedere agli archivi degli altri reparti produttivi. Questo requisito porta naturalmente a una rete segmentata, nella quale ogni reparto viene collocato in una VLAN distinta.

La VLAN permette di separare logicamente i reparti anche se fisicamente gli apparati possono essere collegati alla stessa infrastruttura di switch. Tuttavia la VLAN da sola non basta: se lo switch centrale effettua routing tra VLAN, occorrono ACL o regole firewall per stabilire quali comunicazioni siano consentite e quali debbano essere bloccate.

I reparti D, E e F hanno esigenze particolari:

* il reparto D deve accedere agli archivi dei reparti A, B e C per revisionare e validare i contenuti;
* il reparto E deve accedere a tutti gli archivi locali e trasferire i contenuti approvati verso la sede centrale;
* il reparto F deve accedere a Internet e al gestionale remoto, ma non ha necessità di accedere agli archivi produttivi.

Questa organizzazione porta a una rete con:

* switch di accesso per collegare PC, stampanti e server locali;
* switch centrale Layer 3 per gestire VLAN e routing interno;
* firewall per accesso a Internet, NAT, VPN e protezione perimetrale;
* file server o archivi locali associati ai reparti produttivi;
* collegamento sicuro verso la sede centrale.

---

## 2. Calcolo degli host e scelta delle sottoreti

Il testo indica che ogni reparto deve prevedere fino al 10% di postazioni aggiuntive di riserva.

I numeri diventano quindi:

| Reparto | PC previsti | +10% circa | Host necessari |
|--------|------------|------------|----------------|
| A      | 48         | 4,8        | 53             |
| B      | 32         | 3,2        | 36             |
| C      | 96         | 9,6        | 106            |
| D      | 22         | 2,2        | 25             |
| E      | 12         | 1,2        | 14             |
| F      | 18         | 1,8        | 20             |

A questi numeri sarebbe opportuno aggiungere almeno gateway, stampanti e file server. Per questo motivo vengono scelte sottoreti leggermente abbondanti.

La rete 192.168.10.0/24 da sola non è sufficiente per tutti i reparti, perché:

* una /25 fornisce 126 host utili;
* due /26 forniscono 62 + 62 host utili;
* altre sottoreti servono per D, E e F.

Serve quindi estendere il piano almeno a un secondo blocco, ad esempio 192.168.11.0/24.

---

## 3. Piano di indirizzamento

Si usa VLSM, assegnando prima le sottoreti più grandi.

Il reparto C è il più numeroso e richiede almeno 106 host. La sottorete minima adatta è una /25, perché:

* /26 offre 62 host utili, quindi non basta;
* /25 offre 126 host utili, quindi basta.

Il reparto A richiede circa 53 host. Una /26 offre 62 host utili, quindi è adatta.

Il reparto B richiede circa 36 host. Anche qui una /26 è sufficiente.

I reparti D e F richiedono circa 25 e 20 host. Una /27 offre 30 host utili, quindi è adeguata.

Il reparto E richiede circa 14 host. Una /28 offre 14 host utili esatti. In una soluzione reale sarebbe meglio usare una /27 per avere margine; in una prova d’esame si può usare /28 se si vuole ottimizzare lo spazio.

| Reparto | VLAN | Subnet              | Gateway           | Host utili |
|--------|------|---------------------|-------------------|------------|
| C      | 30   | 192.168.10.0/25     | 192.168.10.1      | 126        |
| A      | 10   | 192.168.10.128/26   | 192.168.10.129    | 62         |
| B      | 20   | 192.168.10.192/26   | 192.168.10.193    | 62         |
| D      | 40   | 192.168.11.0/27     | 192.168.11.1      | 30         |
| F      | 60   | 192.168.11.32/27    | 192.168.11.33     | 30         |
| E      | 50   | 192.168.11.64/28    | 192.168.11.65     | 14         |

I gateway sono configurati come interfacce virtuali VLAN, cioè SVI, sullo switch Layer 3 oppure sul firewall.

In questa soluzione si sceglie lo switch Layer 3 per il routing interno, perché il traffico autorizzato tra reparti può essere frequente, soprattutto quello del reparto D verso gli archivi A, B e C e quello del reparto E verso tutti gli archivi locali.

Il firewall rimane invece il punto di controllo per:

* accesso a Internet;
* NAT;
* VPN verso la sede centrale;
* protezione perimetrale;
* eventuale IDS/IPS.

---

## 4. Schema PlantUML

    @startuml
    title Nuova sede operativa - rete segmentata in VLAN

    skinparam linetype ortho
    skinparam shadowing false
    skinparam rectangle {
      BorderColor #333333
      BackgroundColor #F8F8F8
    }

    cloud "Internet" as Internet
    rectangle "Sede centrale\nRepository contenuti\nGestionale remoto" as Centrale

    rectangle "Firewall perimetrale\nNAT, VPN IPsec,\nfiltraggio verso Internet" as FW

    rectangle "Core switch Layer 3\nSVI VLAN, routing interno,\nACL inter-VLAN" as CORE

    rectangle "Access switch reparto A\nVLAN 10\n192.168.10.128/26" as SWA
    rectangle "Access switch reparto B\nVLAN 20\n192.168.10.192/26" as SWB
    rectangle "Access switch reparto C\nVLAN 30\n192.168.10.0/25" as SWC
    rectangle "Access switch reparto D\nVLAN 40\n192.168.11.0/27" as SWD
    rectangle "Access switch reparto E\nVLAN 50\n192.168.11.64/28" as SWE
    rectangle "Access switch reparto F\nVLAN 60\n192.168.11.32/27" as SWF

    rectangle "PC + Stampante + Archivio contenuti A" as A
    rectangle "PC + Stampante + Archivio contenuti B" as B
    rectangle "PC + Stampante + Archivio contenuti C" as C
    rectangle "PC reparto D\nRevisione e validazione" as D
    rectangle "PC reparto E\nCoordinamento e pubblicazione" as E
    rectangle "PC reparto F\nAmministrazione" as F

    Internet -- FW
    FW -- Centrale : VPN site-to-site IPsec
    FW -- CORE : rete interna / default gateway verso Internet

    CORE -- SWA : trunk 802.1Q
    CORE -- SWB : trunk 802.1Q
    CORE -- SWC : trunk 802.1Q
    CORE -- SWD : trunk 802.1Q
    CORE -- SWE : trunk 802.1Q
    CORE -- SWF : trunk 802.1Q

    SWA -- A : access VLAN 10
    SWB -- B : access VLAN 20
    SWC -- C : access VLAN 30
    SWD -- D : access VLAN 40
    SWE -- E : access VLAN 50
    SWF -- F : access VLAN 60

    note right of CORE
    Regole principali:
    - A, B, C isolati tra loro
    - D può accedere agli archivi A/B/C
    - E può accedere a tutti gli archivi
    - F può accedere a Internet e gestionale remoto
    end note

    @enduml

---

## 5. Apparati e struttura fisica

Ogni reparto viene collegato tramite uno o più switch di accesso. Le porte verso i PC sono configurate come porte access nella VLAN del reparto.

I collegamenti tra switch di accesso e core switch sono trunk 802.1Q. Il trunk consente di trasportare traffico VLAN marcato. Anche se un singolo switch di reparto può servire principalmente una sola VLAN, il trunk verso il centro rete è una scelta ordinata e scalabile.

Il core switch Layer 3 contiene le interfacce VLAN:

* interface vlan 10: gateway reparto A;
* interface vlan 20: gateway reparto B;
* interface vlan 30: gateway reparto C;
* interface vlan 40: gateway reparto D;
* interface vlan 50: gateway reparto E;
* interface vlan 60: gateway reparto F.

Il firewall è collegato al core switch. Il core switch invia al firewall il traffico destinato a Internet o alla sede centrale. Il firewall effettua NAT per Internet e crea la VPN site-to-site verso la sede centrale.

---

## 6. Regole di sicurezza interna

La separazione in VLAN da sola non basta, perché se il core switch fa routing inter-VLAN, in assenza di regole tutti i reparti potrebbero comunicare tra loro.

Servono quindi ACL o regole firewall interne.

Esempio logico di regole:

* VLAN A può accedere a Internet, stampante A e archivio A;
* VLAN A non può accedere a VLAN B, C, D, E, F;
* VLAN B può accedere a Internet, stampante B e archivio B;
* VLAN B non può accedere a VLAN A, C, D, E, F;
* VLAN C può accedere a Internet, stampante C e archivio C;
* VLAN C non può accedere a VLAN A, B, D, E, F;
* VLAN D può accedere agli archivi A, B, C, ma non ai PC degli operatori;
* VLAN E può accedere agli archivi di tutti i reparti;
* VLAN F può accedere a Internet e al gestionale remoto nella sede centrale.

La regola importante è distinguere l’accesso a una VLAN dall’accesso a uno specifico server. Il reparto D, ad esempio, non dovrebbe avere libero accesso a tutti i PC dei reparti A, B e C, ma solo ai rispettivi archivi/file server, usando protocolli specifici come SMB/CIFS o SFTP.

---

## 7. Sicurezza esterna

Il firewall perimetrale deve gestire:

* NAT per l’uscita verso Internet;
* blocco delle connessioni entranti non richieste;
* VPN site-to-site verso la sede centrale;
* filtraggio del traffico tra nuova sede e sede centrale;
* eventuale IDS/IPS.

È opportuno centralizzare i log di sicurezza, in modo che accessi anomali, tentativi di connessione non autorizzati o errori di autenticazione siano registrati.

Per l’autenticazione degli utenti si può usare un dominio centralizzato, ad esempio Active Directory o LDAP. In questo modo ogni accesso ai PC e agli archivi è riconducibile a un utente specifico.

---

## 8. Collegamento verso la sede centrale

La scelta più adatta è una VPN site-to-site IPsec tra firewall della nuova sede e firewall della sede centrale.

Questa scelta è coerente perché:

* il repository dei contenuti si trova nella sede centrale;
* il gestionale remoto si trova nella sede centrale;
* gli utenti non devono configurare manualmente una VPN personale;
* il traffico tra sedi viene cifrato;
* le reti delle due sedi possono comunicare come reti private collegate.

Il traffico ammesso nella VPN deve essere limitato. Non è corretto permettere a tutta la nuova sede di accedere liberamente a tutta la rete centrale.

Regole consigliate:

* VLAN E verso repository centrale dei contenuti: consentito;
* VLAN F verso gestionale remoto: consentito;
* VLAN A/B/C verso repository centrale: normalmente non necessario;
* VLAN D verso repository centrale: normalmente non necessario;
* traffico generico tra sedi: bloccato salvo eccezioni.

---

## 9. Configurazione di un servizio: archivio/file server di reparto

Si considera l’archivio del reparto A. Lo stesso modello può essere replicato per B e C.

Cartelle principali:

    \\archivio-a\contenuti
    \\archivio-a\contenuti\in_lavorazione
    \\archivio-a\contenuti\in_revisione
    \\archivio-a\contenuti\approvati

Permessi consigliati:

| Gruppo utenti | Permessi |
|--------------|----------|
| Creatori_A | lettura/scrittura sui contenuti A |
| Revisori_D | lettura, scrittura report, rinomina cartelle autorizzate |
| Coordinatori_E | lettura/scrittura completa |
| Altri reparti | nessun accesso |

Il reparto D deve poter aggiungere un report, rinominare una cartella con suffisso come “_APPROVATO” e impostare il contenuto come non modificabile.

Questa funzione può essere realizzata con permessi specifici sul file server oppure, meglio, con una procedura applicativa o uno script che riduca il rischio di errori manuali.

In una soluzione più professionale, il reparto D non dovrebbe avere libertà completa sulle cartelle di produzione, ma dovrebbe usare una cartella di revisione oppure un workflow controllato.

Esempio:

    contenuto_in_lavorazione
    contenuto_in_revisione
    contenuto_APPROVATO

Quando la revisione è superata, il revisore deposita il report e cambia lo stato del contenuto. Il sistema può poi impostare automaticamente la cartella in sola lettura.

---

# SECONDA PARTE

Di seguito le risposte **più concise e tecniche**, con indicazioni operative chiare.

---

# SECONDA PARTE – SOLUZIONE


## Quesito I

### Firewall edge vs internal + DMZ

**Firewall perimetrale (edge)**
Protegge il confine Internet ↔ rete aziendale.

Funzioni principali:

* NAT
* VPN (site-to-site e remote access)
* stateful inspection
* filtraggio applicativo (NGFW)

Regola base:

* inbound: deny by default
* outbound: allow controllato

---

**Firewall interno**

Segmenta la rete interna (VLAN, server, DMZ).

Obiettivi:

* limitare lateral movement
* applicare principio minimo privilegio

Implementazione:

* firewall dedicato oppure ACL su switch L3

---

### Relazione con DMZ

**DMZ = zona intermedia controllata**

Tipi:

1. **Single firewall (3 interfacce)**

   * WAN / DMZ / LAN
   * meno sicura ma semplice

2. **Dual firewall**

   * FW1: Internet ↔ DMZ
   * FW2: DMZ ↔ LAN
   * più sicura (defence in depth)

---

**Ruoli:**

* firewall edge → controlla Internet ↔ DMZ
* firewall interno → controlla DMZ ↔ LAN

---

## Quesito II

### Consolidamento server

**Scelta: virtualizzazione con hypervisor tipo 1**

Motivazioni:

* isolamento forte tra servizi
* gestione indipendente
* snapshot/backup
* standard industriale

Alternative scartate:

* container → isolamento insufficiente per file server
* unico OS → nessun isolamento, rischio alto

---

### Implementazione

Host fisico con hypervisor (es. VMware ESXi)

VM separate:

* archivio A
* archivio B
* archivio C

---

### Modifiche di rete (obbligatorie)

1. Porta switch → **trunk 802.1Q**
2. Hypervisor → **virtual switch VLAN-aware**
3. Mapping:

* VM A → VLAN 10
* VM B → VLAN 20
* VM C → VLAN 30

4. Gateway resta su switch L3 o firewall

---

### Nota critica

La virtualizzazione **non deve unire le VLAN**
→ isolamento deve restare identico a prima

---

## Quesito III

### Sicurezza WiFi

**Configurazione corretta:**

* WPA3-Enterprise
* autenticazione 802.1X
* server RADIUS
* credenziali individuali

Opzionale compatibilità:

* WPA2-Enterprise fallback

---

### Configurazione pratica

* SSID interno → VLAN aziendale
* SSID guest → VLAN separata
* isolamento client attivo
* disabilitare WEP e WPA

---

### Valutazione WEP

Posizione ingegnere: **errata**

Motivi:

* cifratura compromessa
* attacco in pochi minuti
* non conforme a standard attuali

Conclusione:

* WEP = **non utilizzabile**

---

## Quesito IV

### REST + VPN sede centrale

---

### Architettura

Zone:

* Internet
* DMZ
* LAN interna

---

### Posizionamento servizi

DMZ:

* endpoint REST
* VPN gateway

LAN:

* repository contenuti
* gestionale

---

## VPN – configurazione precisa

### Tipo

* Remote Access VPN
* Protocollo: **IPsec o SSL VPN (TLS)**

Scelta pratica:

* SSL VPN (più semplice lato client)
* IPsec (più performante, più complesso)

---

### Configurazione minima

1. **Autenticazione**

   * username/password + MFA (obbligatorio)
   * integrazione con AD/LDAP

2. **Assegnazione IP**

   * pool dedicato (es. 10.10.10.0/24)

3. **Access control (fondamentale)**

   * NON full access
   * ACL per gruppi:

   esempi:

   * amministrazione → solo gestionale
   * project manager → repository
   * altri → accessi limitati

4. **Split tunneling**

   * disabilitato per sicurezza
     oppure
   * abilitato solo se necessario

5. **Logging**

   * accessi utenti
   * tentativi falliti
   * traffico anomalo

---

### Flussi

* utente remoto → VPN → accesso filtrato LAN
* sede remota → VPN site-to-site → repository
* Internet → REST (DMZ) → accesso controllato LAN

---

### Sicurezza REST

* reverse proxy / WAF davanti alle API
* limitazione endpoint
* autenticazione API (token, OAuth)
* rate limiting

---

## Conclusione

Scelte corrette:

* firewall separati per ruoli diversi
* DMZ per servizi esposti
* virtualizzazione con isolamento VLAN
* WiFi con WPA3-Enterprise
* VPN configurata con:

  * MFA
  * ACL per ruolo
  * segmentazione accessi

Errore grave da evitare:

* accessi “flat” (tutti a tutto)
* uso di WEP
* VM senza separazione di rete
