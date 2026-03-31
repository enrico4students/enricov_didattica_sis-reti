---

marp: false
theme: portrait

---  


<link rel="stylesheet" href="./themes/portrait.css">

## VLAN – Concetti essenziali


<img src="https://images.wondershare.com/edrawmax/templates/vlan-network-diagram.png" width="75%" />

&nbsp;

<img src="https://i.adroitacademy.com/blog/43604421.png" style="background-color: white; display: inline-block; padding: 10px;" width="75%" />

&nbsp;

<img src="https://images.ctfassets.net/aoyx73g9h2pg/3Bv0UJzi0ZOIpeIDn4SvEM/7f63324da001b246a7e263860cb9d89a/What-is-802-1Q-Port-Tagging-Diagram.jpg" width="75%" />

&nbsp;

<img src="https://cdn.networkacademy.io/sites/default/files/2025-06/802-1q-vlan-tagging.gif" width="75%" />


## 1. Che cos’è una VLAN

Una **VLAN (Virtual LAN)** è una suddivisione logica di una rete fisica a livello 2 (Data Link).

Permette di creare più reti separate utilizzando lo stesso switch fisico.

Esempio:

* VLAN 10 → Ufficio amministrazione
* VLAN 20 → Reparto tecnico
* VLAN 30 → Wi-Fi ospiti

Anche se tutti i dispositivi sono collegati allo stesso switch, **non possono comunicare tra VLAN diverse senza routing**.  


Per ribadire il livello a cui sono le VLAN, livello 2, conviene fare riferimento a queste frasi:  
- Una VLAN **separa il traffico Ethernet** Ethernet.  
- Il routing **collega le reti IP**        IP.  
- VLAN e sotto/reti IP sono a **livelli diversi**,  
- solitamente si faranno coincidere VLAN diverse con reti IP diverse per praticità/comodità,  
ma tecnicamente non è una proprietà intrinseca delle VLAN, non è un requisito o caratteristica tecnica.  


---

## 2. Concetti principali

**Access Port**:  
Porta assegnata a una sola VLAN.  
Usata per collegare PC, stampanti, server.  

**Trunk Port**:  
Porta di switch configurata per trasportare traffico appartenente a più VLAN sullo stesso collegamento fisico (cavo xtp, fibra).  
Tipicamente utilizzata tra switch oppure tra switch e dispositivi di livello superiore (router, firewall, hypervisor, access point).  
Le VLAN sono identificate tramite tagging IEEE 802.1Q inserito nei frame Ethernet; normalmente i frame sono taggati, mentre la native VLAN può essere trasmessa senza tag.

**native VLAN**: la VLAN di default per il traffico non taggato su una trunk port.


**VLAN ID**:  
Numero identificativo (1–4094), serve a distinguere i frame (12 bits, 0 - 4095 ma 0 e 4095 sono per usi riservati e non possono essere usati)  

### Separazione logica

I dispositivi in VLAN diverse:

* non vedono i broadcast reciproci
* non comunicano direttamente
* **necessitano di routing Layer 3**

---

## 3. Benefici rispetto a NON usare VLAN (rete piatta)

In una rete senza VLAN:

* tutto è nello stesso dominio di broadcast
* nessuna segmentazione
* traffico elevato
* minore sicurezza

Con VLAN:  

- **Riduzione broadcast**: Ogni VLAN costituisce un dominio di broadcast separato.
- **Isolamento logico della rete**, ciò non è di per sè un meccanismo di sicurezza ma facilita i meccanismi di sicurezza.
- **Migliore organizzazione**: La rete riflette la struttura aziendale.  
- **Flessibilità**: spostare un utente di reparto richiede solo cambiare la VLAN sulla porta dello switch, senza modificare il cablaggio. Senza VLAN il cambio di rete richiedeva spesso modifiche fisiche (switch, cablaggio o subnet).    
- **Facilitazione del controllo del traffico**: il traffico tra VLAN deve passare da un dispositivo di livello 3; tale dispositivo può applicare policy come:
  * ACL
  * firewall
  * QoS  


---

## 4. Differenza rispetto al subnetting

- VLAN = separazione a livello 2  
- Subnet = separazione a livello 3  

Nella pratica di progettazione si segue quasi sempre questa regola:  
una VLAN ↔ una subnet IP  
**ma tecnicamente sono concetti distinti**.  

### Switch senza VLAN ma con più subnet:

* separazione logica IP esiste
* ma a livello fisico possono condividere lo stesso dominio L2

Esempio: Uno switch con quattro host:  
PC1 → 192.168.1.10 PC2 → 192.168.1.20 PC3 → 192.168.2.10 PC4 → 192.168.2.20 Quindi:  
- gli host condividono lo stesso dominio L2  
- i broadcast Ethernet vengono inviati a tutte le porte dello switch (eccetto quella di ingresso ovviamente)  
- la separazione è solo logica a livello IP  

Poiché gli host appartengono a due subnet IP diverse ( 192.168.1.0/24 e 192.168.2.0/24 ) la comunicazione tra host di reti diverse richiede un router.  
Il router deve avere un indirizzo IP per ogni subnet.  
Molti router permettono di configurare più indirizzi IP sulla stessa interfaccia (configurazione chiamata spesso secondary IP address o multiple addresses per interface), in questo caso è sufficiente collegare una sola porta dello switch al router. 

Esempio: due indirizzi sulla interfaccia Ethernet:
router interface
192.168.1.1/24
192.168.2.1/24


### Switch con più VLAN  

Quando è configurato con più VLAN lo switch 
- mantiene **tabelle MAC separate per VLAN** e  
- **non inoltra i frame tra VLAN diverse** cioè i frame di una VLAN **non vengono consegnati alle porte di un’altra VLAN**, 
- c'è separazione L2; le VLAN **non possono comunicare direttamente tra loro**  
  - ci sono **più domini di broadcast separati**, uno per ogni VLAN.  

Esempio: switch con due VLAN

VLAN 10 → PC1, PC2  
VLAN 20 → PC3, PC4  
* VLAN 10 e VLAN 20 sono **reti L2 separate**
* i broadcast non attraversano le VLAN


### Switch con più VLAN diverse appartenenti alla stessa (sub)net IP:  

E' tecnicamente possibile avere VLAN diverse che appartengono alla stessa subnet IP,  
ma è una configurazione **anomala e generalmente sconsigliata**.  
(In una progettazione di rete standard si usa quasi sempre la regola: una VLAN → una subnet IP)

Esempio:  
VLAN 10: PC1 → 192.168.1.10/24  
VLAN 20: PC2 → 192.168.1.20/24  

In questo caso i due host appartengono alla **stessa subnet IP (192.168.1.0/24)** ma si trovano in **domini di livello 2 separati**.

Questa configurazione crea problemi perchè il protocollo IP presuppone che gli host della stessa subnet possano comunicare **direttamente** a livello 2, ciò in questo caso non è vero. 

Prima di inviare un pacchetto IP, un host deve conoscere il **MAC address** del destinatario se
1. PC1 vuole comunicare con 192.168.1.20  
2. PC1 vede che l’indirizzo appartiene alla **stessa subnet**  
3. PC1 invia una **richiesta ARP broadcast** per trovare il MAC di PC2   

Il problema è che il broadcast ARP rimane **limitato alla VLAN** quindi  
* la richiesta ARP viene diffusa solo nella VLAN 10  
* PC2 non la riceve e non risponde quindi   
* PC1 non ottiene il MAC address di PC2    
Di conseguenza la comunicazione **non può avvenire**.  

Il router non risolve il problema perchè normalmente il router interviene quando la destinazione è **fuori subnet**.  
In questo caso però l’indirizzo di destinazione è nella **stessa rete IP**, quindi l’host **non invia il traffico al router**.

Esistono alcune tecniche che possono far funzionare una configurazione di questo tipo, Tuttavia queste soluzioni:  
* complicano molto la rete  
* rendono il troubleshooting difficile  
* violano il modello di progettazione normale  


### Switch con più VLAN diverse corrispodenti ognuna ad una (sotto)rete IP:  

Il caso normale.

Per permettere la comunicazione serve **routing di livello 3**, questo processo si chiama **inter-VLAN routing**.

Esistono tre modalità principali:  
- Router con più interfacce fisiche  
- Router-on-a-stick  
- Switch Layer 3  

---

#### Router con più interfacce fisiche

Ogni VLAN è collegata a una porta diversa del router.

Esempio:  
VLAN 10 → switch → porta 1 router → 192.168.10.1  
VLAN 20 → switch → porta 2 router → 192.168.20.1  

Il router inoltra i pacchetti tra le reti.

Questa soluzione è semplice ma poco scalabile.

---

#### Router-on-a-stick

Si usa **un solo collegamento fisico tra switch e router**, configurato come **trunk 802.1Q**.

Si chiama router-on-a-stick perché:
- c’è un solo cavo tra router e switch  
- su quel cavo passano tutte le VLAN  

Il router crea **subinterfacce VLAN**, cioè subinterfacce logiche sulla stessa porta,  
Su ogni subinterfaccia si configura l’IP della subnet. Esempio:  
- interfaccia router eth0.10 → VLAN 10 → 192.168.10.1  
- interfaccia router eth0.20 → VLAN 20 → 192.168.20.1  

Il traffico arriva taggato allo switch e il router effettua il routing tra VLAN.

Esempio di comunicazione tra VLAN

PC1 (192.168.10.10) vuole parlare con PC3 (192.168.20.10).
PC1 vede che l’indirizzo è fuori subnet e invia il frame al gateway 192.168.10.1.  
Il frame entra nello switch, appartiene alla VLAN 10, lo switch lo manda sulla porta trunk con tag VLAN 10.  
Il router riceve il frame. Il tag dice al router: questo traffico appartiene alla VLAN 10 quindi viene consegnato alla subinterfaccia: eth0.10.  
Il router esamina il pacchetto IP: destinazione → 192.168.20.10 Il router fa routing verso la rete 192.168.20.0.  
Poi: incapsula di nuovo il frame Ethernet, aggiunge tag VLAN 20, lo rimanda allo switch.  
Lo switch riceve il frame e lo inoltra solo alle porte della VLAN 20.  
PC3 lo riceve.  


---

#### Switch Layer 3

Molti switch moderni possono fare **routing direttamente**.

Lo switch crea **interfacce virtuali di VLAN** (**SVI**: Switched Virtual Interface).  

Esempio:  
- interface vlan 10 → 192.168.10.1  
- interface vlan 20 → 192.168.20.1   

Lo switch Layer-3 effettua il routing tra le VLAN senza usare un router esterno.
Quando si configurano le SVI:  
- interface vlan 10 → 192.168.10.1  
- interface vlan 20 → 192.168.20.1  

si stanno creando vere interfacce IP. Queste interfacce:
- appartengono a subnet diverse  
- hanno una tabella di routing  
- inoltrano pacchetti IP tra reti diverse  

Quindi il dispositivo esegue vero routing IP. Il processo è lo stesso di un router:
- ricezione del frame Ethernet  
- estrazione del pacchetto IP  
- consultazione della routing table  
- inoltro verso la rete di destinazione  

La differenza è che lo switch lo fa in hardware ASIC, quindi molto velocemente.


---

## 5. Quando sono consigliabili le VLAN  

Le VLAN sono consigliabili quando:

* più di 20–30 dispositivi
* presenza di reparti diversi
* server interni
* Wi-Fi ospiti
* esigenza di sicurezza
* VoIP
* controllo traffico

Non sono necessarie in reti domestiche molto piccole.

---

## 6. Dispositivi coinvolti

### Switch (gestito, Managed Switch)

Dispositivo principale per configurare VLAN. Permette:  
* assegnazione porte access
* configurazione trunk
* definizione VLAN ID


La differenza tra **managed switch** e **switch non gestito (unmanaged switch)** riguarda principalmente la **possibilità di configurazione e controllo del dispositivo**.

Uno switch Ethernet, in entrambi i casi, svolge la stessa funzione di base: ricevere frame Ethernet su una porta e inoltrarli verso la porta corretta usando la **tabella MAC**.  
Tuttavia cambia molto **quanto controllo l’amministratore ha sul comportamento dello switch**.

---

##### Switch non gestito (Unmanaged Switch)

Uno **switch non gestito** è un dispositivo molto semplice: 
* non richiede configurazione  
* non ha interfaccia di amministrazione  
* funziona appena viene collegato alla rete  
* tutte le porte appartengono allo stesso dominio di livello 2  
* non supporta VLAN o funzionalità avanzate  

Dal punto di vista operativo funziona come **un semplice bridge Ethernet automatico**.  
In particolare ha i seguenti Limiti:  
* nessuna separazione della rete  
* nessun controllo del traffico  
* nessuna possibilità di monitoraggio  
* nessuna sicurezza configurabile  

---

#### Managed Switch

Uno **switch gestito (managed switch)** permette invece la **configurazione e l’amministrazione del dispositivo**.

Lo switch offre un’interfaccia di gestione che consente di configurare molte funzionalità di rete, ad esempio:  
* interfaccia web  
* console seriale  
* SSH  
* SNMP  

Funzioni tipiche di uno switch gestito:  
- VLAN: separazione della rete in più domini di broadcast
- Trunk 802.1Q: trasporto di più VLAN tra switch
- Spanning Tree: prevenzione dei loop di rete
- QoS: priorità del traffico (voce, video, dati)
- Port security: limitazione dei dispositivi collegati a una porta
- Monitoraggio: statistiche e controllo del traffico
- Link aggregation: unione di più collegamenti per aumentare la banda

---

## Differenza concettuale

Uno **switch non gestito** è un dispositivo che lavora automaticamente con comportamento **fisso**.

Uno **switch gestito** è invece un dispositivo che può essere **progettato e configurato per adattarsi alla rete**.

---

## Differenza nella progettazione di rete

Con uno switch non gestito:  
* esiste **un solo dominio di broadcast**  
* tutti i dispositivi condividono la stessa rete  

Con uno switch gestito è possibile:  
* creare **più VLAN**  
* isolare traffico  
* controllare la rete  
* integrare router e firewall  

### Switch Layer 3

Può fare routing tra VLAN.
Utile in reti medio-grandi.

### Router

Effettua routing inter-VLAN (router-on-a-stick).

### Firewall

Controlla traffico tra VLAN.
Applica regole di sicurezza.

### Access Point

Mappa SSID diversi su VLAN diverse.
Esempio:

* SSID aziendale → VLAN 10
* SSID guest → VLAN 30

--- 

## possibilità teoriche inizio


Ricordiamo che VLAN e IP operano a livelli diversi, una VLAN è un concetto di **livello 2 (Ethernet)** che serve a **separare il traffico Ethernet** in domini distinti. Una rete IP invece appartiene al **livello 3**.  
VLAN → livello 2  
IP network → livello 3  

**Una VLAN non definisce automaticamente una rete IP** anche se nella pratica spesso ma non sempre verranno configurati in modo che coincidano


Una VLAN definisce:  
* un **dominio di broadcast Layer 2**  
* un **insieme di porte dello switch**  
* un **tag VLAN nei frame Ethernet**  
In pratica:
tutti i dispositivi nella stessa VLAN ricevono i broadcast Ethernet.

Nella pratica di progettazione si segue quasi sempre questa regola:
una VLAN → una subnet IP. Esempio tipico:
VLAN 10 192.168.10.0/24
VLAN 20 192.168.20.0/24
VLAN 30 192.168.30.0/24

Il motivo è semplice:  
* il routing diventa chiaro  
* la gestione è semplice  
* si evitano problemi di broadcast  
* il troubleshooting è molto più facile  
Per questo nei corsi di reti si insegna spesso la regola:
"una VLAN corrisponde a una rete IP".
Ma è **una scelta progettuale**, non un vincolo tecnico.

---

### Caso 1 — Più VLAN con la stessa rete IP (possibile ma raro)

È tecnicamente possibile avere:  
VLAN 10 → 192.168.1.0/24
VLAN 20 → 192.168.1.0/24

In questo caso:  
* sono due domini Layer 2 separati  
* ma usano lo stesso indirizzamento IP  
Conseguenze:  
* i dispositivi **credono di essere nella stessa rete**  
* ma **non possono comunicare** perché sono in VLAN diverse  
Questo crea facilmente problemi ARP e di connettività.  
Per questo motivo **si evita quasi sempre**.  

---

# 5. Caso 2 — Più reti IP nella stessa VLAN

È invece abbastanza possibile avere:  
VLAN 10 host A → 192.168.10.5 host B → 192.168.20.8

I due host sono:  
* nella stessa VLAN  
* ma in reti IP diverse  

Quindi:  
* Ethernet funziona  
* ma la comunicazione IP richiede comunque routing  

Questo scenario può capitare ad esempio:  
* durante migrazioni di rete  
* in reti legacy  
* in ambienti di laboratorio  

---

Ripetiamo:  

Nelle reti ben progettate si usa **una subnet IP per ogni VLAN**, ma non è una regola obbligatoria.


---

## 7. Esempi realistici (tipici nei test di informatica)

### Caso 1 – Piccola azienda (25 PC)

Richiesta:

* Amministrazione
* Tecnici
* Wi-Fi ospiti

Soluzione:

VLAN 10 → 192.168.10.0/24
VLAN 20 → 192.168.20.0/24
VLAN 30 → 192.168.30.0/24

Domande tipiche:

* configurare porte access
* indicare porta trunk
* spiegare perché isolare guest

---

### Caso 2 – Azienda con server interno

Richiesta:

* PC utenti
* Database
* Web server

Soluzione:

VLAN 10 → LAN utenti
VLAN 20 → Server
VLAN 30 → DMZ

Regola firewall:

* VLAN 10 può accedere al DB
* VLAN 30 non può accedere alla LAN

Domanda tipica:

* spiegare perché il server non deve stare nella stessa VLAN degli utenti

---

### Caso 3 – Ufficio su due piani

Switch piano 1
Switch piano 2

Collegamento trunk tra switch.

VLAN 10 presente su entrambi i piani.
Le VLAN possono estendersi su più switch tramite trunk.

Domande tipiche:

* differenza tra access e trunk
* cosa succede se si collega un PC a una porta trunk
* perché serve 802.1Q

---

## Conclusione

Le VLAN permettono:

* segmentazione logica
* riduzione broadcast
* maggiore sicurezza
* flessibilità organizzativa
* controllo del traffico

Nei test di informatica vengono richiesti:

* definizione VLAN
* differenza access/trunk
* associazione VLAN-subnet
* motivazione della segmentazione
* proposta di progettazione logica

