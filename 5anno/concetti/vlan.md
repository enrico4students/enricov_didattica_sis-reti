## VLAN – Concetti essenziali


<img src="https://images.wondershare.com/edrawmax/templates/vlan-network-diagram.png" width="75%" />

&nbsp;

<img src="https://i.adroitacademy.com/blog/43604421.png" style="background-color: white; display: inline-block; padding: 10px;" width="75%" />

&nbsp;

<img src="https://images.ctfassets.net/aoyx73g9h2pg/3Bv0UJzi0ZOIpeIDn4SvEM/7f63324da001b246a7e263860cb9d89a/What-is-802-1Q-Port-Tagging-Diagram.jpg" width="75%" />

&nbsp;

<img src="https://cdn.networkacademy.io/sites/default/files/2025-06/802-1q-vlan-tagging.gif" width="75%" />

"
## 1. Che cos’è una VLAN

Una **VLAN (Virtual LAN)** è una suddivisione logica di una rete fisica a livello 2 (Data Link).

Permette di creare più reti separate utilizzando lo stesso switch fisico.

Esempio:

* VLAN 10 → Ufficio amministrazione
* VLAN 20 → Reparto tecnico
* VLAN 30 → Wi-Fi ospiti

Anche se tutti i dispositivi sono collegati allo stesso switch, non possono comunicare tra VLAN diverse senza routing.


Per ribadire il livello a cui sono le VLAN, livello 2, conviene fare riferimento a queste frasi:  
- Una VLAN **separa il traffico Ethernet**.  
- Il routing **collega le reti IP**.  
- VLAN e sotto/reti IP sono a livelli diversi, solitamente si faranno coincidere VLAN diverse con reti IP diverse ma tecnicamente non è una proprietà intrinseca delle VLAN.  


---

## 2. Concetti principali

### Access Port

Porta assegnata a una sola VLAN.
Usata per collegare PC, stampanti, server.

### Trunk Port

Porta che trasporta più VLAN contemporaneamente.
Usata tra switch o tra switch e router.
Utilizza il tagging IEEE 802.1Q.

### VLAN ID

Numero identificativo (1–4094).
Serve a distinguere i frame.

### Separazione logica

I dispositivi in VLAN diverse:

* non vedono i broadcast reciproci
* non comunicano direttamente
* necessitano di routing Layer 3

---

## 3. Benefici rispetto a NON usare VLAN (rete piatta)

In una rete senza VLAN:

* tutto è nello stesso dominio di broadcast
* nessuna segmentazione
* traffico elevato
* minore sicurezza

Con VLAN:

### 1. Riduzione broadcast

Ogni VLAN è un dominio di broadcast separato.

### 2. Maggiore sicurezza

Separazione tra:

* utenti
* server
* ospiti
* reparti

### 3. Migliore organizzazione

La rete riflette la struttura aziendale.

### 4. Flessibilità

Spostare un utente di reparto richiede solo cambiare VLAN sulla porta, non il cablaggio.

### 5. Controllo del traffico

È possibile applicare:

* ACL
* firewall
* QoS
  tramite routing inter-VLAN.

---

## 4. Differenza rispetto al subnetting

- VLAN = separazione a livello 2  
- Subnet = separazione a livello 3  

Nella pratica di progettazione si segue quasi sempre questa regola:  
una VLAN → una subnet IP  
**ma sono concetti distinti**.  

Senza VLAN ma con subnet:

* separazione logica IP esiste
* ma a livello fisico possono condividere lo stesso dominio L2

Senza subnet ma con VLAN:

* separazione L2 esiste
* ma routing e controllo avanzato risultano limitati

La progettazione corretta usa entrambe.

---

## 5. Quando sono consigliabili

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

### Switch gestito (Managed Switch)

Dispositivo principale per configurare VLAN.
Permette:

* assegnazione porte access
* configurazione trunk
* definizione VLAN ID

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

