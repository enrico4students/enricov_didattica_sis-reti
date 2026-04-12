
Un punto difficile, di solito, è questo: 
core switch e distribution switch non sono “due switch uno sopra l’altro” che fanno quasi la stessa cosa.  
In una architettura gerarchica a 3 layer hanno ruoli diversi, anche se in prodotti moderni alcune funzioni possono sovrapporsi.

Conviene immaginare i 3 layer così:

- access layer: collegare i dispositivi finali  
- distribution layer: organizzare, separare, controllare, instradare localmente
- core layer: trasportare il traffico molto velocemente tra le varie parti della rete

La relazione fra core e distribution è quindi soprattutto questa:
- il distribution è il punto in cui le reti locali vengono raccolte, separate e spesso instradate;
- il core è il dorsale centrale ad alta velocità che collega tra loro tutti i distribution.  

In altre parole, 
- il distribution “sa” molto bene cosa c’è nella propria zona della rete; 
- il core “non vuole sapere troppi dettagli”, ma deve portare i pacchetti rapidamente da una zona all’altra.
!EV ritornarci


Una buona analogia è questa.

L’access layer è fatto dalle strade di quartiere.
Il distribution layer è fatto dagli svincoli o dalle tangenziali locali che raccolgono il traffico di più quartieri.
Il core layer è fatto dall’autostrada principale che collega città o grandi zone.

Il traffico non parte normalmente dal core. 
- Parte quasi sempre da un host collegato all’access,  
- sale al distribution, 
- e solo se necessario attraversa il core per raggiungere un’altra parte della rete.

#### 1. Ruolo concettuale del distribution layer

Il distribution layer è il livello in cui spesso si trovano le funzioni “intelligenti” di controllo del traffico. Per esempio:

- aggregare più access switch
- fare routing tra VLAN
- applicare ACL
- applicare policy di sicurezza e QoS
- fare summarization delle rotte verso il core !EV spiegare
- essere default gateway delle VLAN di una certa area o edificio

Quindi il distribution è spesso il punto in cui il traffico viene “capito” dal punto di vista logico.

Esempio.

In un edificio scolastico o aziendale si possono avere:

VLAN 10 amministrazione
VLAN 20 laboratori
VLAN 30 docenti
VLAN 40 ospiti

Gli access switch collegano PC, stampanti e access point.
I distribution switch ricevono i trunk dagli access switch, conoscono le VLAN e spesso ospitano le SVI, cioè le interfacce logiche di routing come:

VLAN 10 -> 10.10.10.1
VLAN 20 -> 10.10.20.1
VLAN 30 -> 10.10.30.1
VLAN 40 -> 10.10.40.1

In questo caso il distribution non si limita a inoltrare frame Ethernet: fa anche vero routing IP tra le subnet/VLAN.
!EV: assunzione non necessaria tecnicamente ma frequente: 1 rete IP <-> VLAN


#### 2. Ruolo concettuale del core layer

Il core layer invece ha l’obiettivo principale di trasportare traffico nel modo più rapido, affidabile e ridondato possibile.

Tipicamente il core:

- collega i distribution dei diversi edifici, piani o aree
- fornisce backbone ad alta velocità
- usa collegamenti molto veloci e spesso ridondati
- mantiene tabelle di routing meno dettagliate, spesso grazie alla **summarization**
- cerca di evitare policy troppo pesanti che rallenterebbero il forwarding

Il core quindi è una specie di “spina dorsale” della rete.

Non è il posto ideale per concentrare troppe ACL molto complesse, NAT, filtri applicativi o logiche troppo locali. Quelle di solito stanno prima, cioè nel distribution o nei firewall.

#### 3. Rapporto concreto fra distribution e core

La relazione concreta è questa:

- ogni distribution raccoglie il traffico dei propri access switch;
- se la destinazione è locale alla sua area, il distribution può risolvere tutto da solo;
- se la destinazione è remota, il distribution inoltra il traffico al core;
- il core trasporta il traffico fino al distribution corretto;
- il distribution di destinazione lo porta verso l’access switch finale.

Questa è la dinamica fondamentale.

Quindi il core non “gestisce le VLAN degli utenti finali” nel dettaglio, salvo casi particolari. In genere trasporta traffico tra **blocchi di rete già organizzati dai distribution**. !EV:todo dettagliare

#### 4. Primo esempio pratico: comunicazione dentro la stessa VLAN

Caso molto tipico.

PC-A è nella VLAN 20, IP 10.10.20.15
PC-B è nella VLAN 20, IP 10.10.20.80

Se stanno nello stesso dominio Layer 2, il traffico può anche non arrivare né al distribution né al core, dipende da dove si trovano.

Caso A: i due PC sono sullo stesso access switch
Il traffico resta nello switch di accesso.
PC-A fa ARP per sapere il MAC di PC-B, poi invia direttamente i frame Ethernet.
Distribution e core non intervengono.

Caso B: i due PC sono su access switch diversi ma sempre nella stessa VLAN estesa
Il traffico sale dagli access switch verso il distribution, ma resta traffico Layer 2.
Il distribution inoltra i frame verso il ramo corretto.
Il core, in una rete ben progettata, spesso non è coinvolto se la VLAN è locale al medesimo blocco di distribution.

Qui si vede già una cosa importante: non tutto il traffico “passa dal core”. Anzi, in una buona progettazione si cerca di non mandare inutilmente tutto al core.

#### 5. Secondo esempio pratico: traffico fra VLAN diverse nella stessa area

PC-A:          VLAN 20, IP 10.10.20.15
Server locale: VLAN 30, IP 10.10.30.50

Il PC vuole parlare con un host che sta in un’altra subnet. Quindi non manda direttamente il frame al server, ma al proprio default gateway, ad esempio 10.10.20.1, che è sul distribution switch.

Succede questo:

1. PC-A vede che 10.10.30.50 non è nella sua subnet.
2. PC-A fa ARP per il default gateway 10.10.20.1.
3. Il frame va dall’access switch al distribution.
4. Il distribution riceve il pacchetto IP, controlla la destinazione, consulta la tabella di routing.
5. Vede che la rete 10.10.30.0/24 è direttamente connessa tramite la SVI della VLAN 30.
6. Riscrive l’intestazione Layer 2 e inoltra verso il server nella VLAN 30. !EV:todo dettagliare

In questo caso il core non serve.

Questa è una delle idee più importanti da visualizzare: 
il distribution non è solo “un passaggio verso il core”. 
Molto spesso risolve localmente una grande quantità di traffico.

#### 6. Terzo esempio pratico: traffico fra aree diverse, quindi attraverso il core

Immaginare due edifici.

Edificio A

* VLAN 20 studenti: 10.10.20.0/24
* Distribution A

Edificio B

* VLAN 120 segreteria: 10.20.120.0/24
* Distribution B

In mezzo c’è il core.

Uno studente del edificio A deve raggiungere un server amministrativo nel edificio B.

Il percorso tipico è questo:

host sorgente -> access A -> distribution A -> core -> distribution B -> access/server B

Vediamolo logicamente.

Il PC sorgente invia al suo default gateway sul Distribution A.
Il Distribution A guarda la destinazione 10.20.120.x.
Capisce che quella rete non è locale.
Ha una route verso il core, oppure una route specifica appresa dal core. EV:todo dettagliare un route verso uno switch non ha senso
Inoltra il pacchetto al core.

Il core non si occupa del dettaglio del singolo host studente.
Il core vede che la rete 10.20.120.0/24, oppure magari il blocco riassunto 10.20.0.0/16, è raggiungibile tramite Distribution B. EV:todo dettagliare bloccoo riassunto
Quindi inoltra il pacchetto verso Distribution B.

Il Distribution B riceve il pacchetto, vede che la subnet di destinazione è direttamente connessa alla sua VLAN o al suo segmento locale, risolve il MAC se serve e lo inoltra al destinatario.

Questa è la **relazione tipica core-distribution**: 
il distribution porta il traffico “verso il backbone”, il core lo trasporta fino al distribution corretto.

#### 7. Quarto esempio pratico: uscita verso Internet

Un altro caso tipicissimo è il traffico verso Internet.

PC utente -> access -> distribution -> core -> firewall/router edge -> Internet

Perché spesso passa dal core?

Perché il firewall o il router verso Internet si trovano in una zona centrale del campus o del datacenter, collegata al core.

Sequenza logica:

il PC invia al default gateway sul distribution
il distribution capisce che la destinazione non è una rete interna locale
inoltra verso il core
il core sa che la default route o la rete esterna è verso il firewall/router centrale
inoltra lì
il firewall applica le policy, poi invia verso Internet

Anche qui il core non prende decisioni “applicative” complesse: fa principalmente transito veloce.

#### 8. Quinto esempio pratico: accesso a server in datacenter o server farm

In molte reti enterprise la server farm è collegata al core oppure a un distribution dedicato del datacenter. EV:todo: precisazione non è il caso solito di accesso esterno a WEB server in una DMZ i server WEB sono collegati ad una interfaccia del firewall router

Caso:

utente in ufficio -> server applicativo centrale

Percorso:

PC -> access -> distribution utente -> core -> distribution datacenter oppure direttamente core -> server farm

Il traffico passa dal core perché sta andando da una zona campus a una zona centralizzata.

Se poi il server applicativo deve interrogare un database nella stessa server farm, quella seconda comunicazione può restare interna al blocco datacenter, senza tornare indietro nel campus.

#### 9. Che cosa “sa” il core e che cosa “sa” il distribution

Questo punto aiuta molto la visualizzazione mentale.

Il distribution sa:

quali VLAN ha sotto di sé
quali subnet sono direttamente connesse
quali policy locali applicare
quali access switch e quali utenti appartengono alla sua area

Il core sa:

quali grossi blocchi di rete stanno dietro ciascun distribution
come raggiungerli nel modo più veloce e ridondato
come mantenere la continuità del backbone anche in caso di guasto

Quindi il distribution ha visibilità più “locale e dettagliata”.
Il core ha visibilità più “globale e sintetica”.

#### 10. Perché non collegare tutti gli access direttamente al core?

Perché il core non deve diventare il punto in cui si concentra tutta la complessità di rete.

Se tutti gli access arrivassero direttamente al core:

il core dovrebbe gestire troppe VLAN e troppi dettagli
la rete diventerebbe meno scalabile
aumenterebbe il dominio di guasto
sarebbe più difficile applicare policy per area
il backbone perderebbe il suo ruolo pulito di trasporto EV:precisazione stupitdità il ruolo non è un beneficio per se ma conseguenza degli altri benefici

Il distribution serve proprio a fare da livello intermedio di aggregazione e controllo.

#### 11. Ridondanza: perché spesso si vedono due core e due distribution

Nelle reti reali si vede spesso una coppia di core switch e una coppia di distribution switch.

Non è solo per “avere un backup”, ma per evitare singoli punti di guasto e per distribuire il carico.

Per esempio:

Access switch collegato a Distribution 1 e Distribution 2
Distribution 1 e 2 collegati a Core 1 e Core 2

Così, se cade un link o un apparato, il traffico può passare da un altro percorso.

Qui entrano in gioco protocolli e meccanismi come:

STP nelle parti Layer 2
link aggregation
HSRP/VRRP/GLBP per gateway ridondati
OSPF/EIGRP/IS-IS oppure routing statico nelle parti Layer 3
ECMP per usare più percorsi

Dal punto di vista concettuale, la cosa importante è questa: 
la relazione core-distribution non è solo verticale, ma anche ridondata e spesso “a maglia parziale”.

#### 12. Due modi comuni di progettare il rapporto core-distribution

Esistono due approcci tipici.

##### Primo approccio:  
Layer 2 fino al distribution, routing al distribution
È molto comune nel campus tradizionale.
Gli access switch portano VLAN al distribution tramite trunk.
Le SVI e il routing stanno sul distribution.
Il core riceve traffico già instradato a Layer 3.

Questo modello è molto chiaro didatticamente.

Secondo approccio: più Layer 3 già verso l’access
In architetture più moderne, soprattutto grandi campus, si preferisce spesso limitare il Layer 2 e portare il routing più vicino all’edge.
In questo caso il ruolo del distribution può cambiare o ridursi, e a volte si parla di collapsed core.

Ma nella classica architettura a 3 layer, l’idea base resta: 
distribution organizza e instrada localmente, core trasporta tra domini diversi.

#### 13. Esempio completo semplice

Immaginare una scuola grande con due edifici.

Edificio A

* laboratori informatici
* aule
* access switch ai piani
* distribution A

Edificio B

* segreteria
* presidenza
* server locali
* distribution B

Centro rete

* core
* firewall
* connessione Internet

Caso 1: PC laboratorio A stampa su stampante del laboratorio A
Il traffico può restare nell’access o nel distribution A. Il core non interviene.

Caso 2: PC laboratorio A accede al registro elettronico interno ospitato nel edificio B
Il traffico sale a Distribution A, poi passa al core, poi arriva a Distribution B, poi al server.

Caso 3: PC segreteria B naviga su Internet
Il traffico va da Distribution B al core e poi al firewall centrale.

Caso 4: PC laboratorio A accede a un server DNS locale presente nel proprio edificio
Il distribution A può inoltrare direttamente senza coinvolgere il core, se il DNS è locale a quel blocco.

#### 14. Dove nasce spesso la confusione

La confusione nasce perché in molti schemi si disegnano solo scatole e linee verticali, e sembra che:

access -> distribution -> core

sia sempre un semplice “salire verso l’alto”.

In realtà ogni livello non è definito dalla posizione nel disegno, ma dalla funzione.

Il distribution non è solo “uno switch intermedio”; è il punto in cui spesso si separano broadcast domain, si fa inter-VLAN routing, si applicano regole, si aggregano access multipli.

Il core non è semplicemente “lo switch più grosso”; è la dorsale di trasporto veloce e affidabile.

Quindi la domanda da porsi è sempre:

questo traffico può essere risolto localmente dal distribution?
Se sì, il core non serve.
Se no, il distribution porta il traffico al core.

#### 15. Regola mentale molto utile

Per visualizzare bene il movimento dei pacchetti, usare questa regola:

stessa VLAN e stesso segmento locale: spesso resta in basso EV:todo:chiarire segmento locale
VLAN diverse ma stessa area servita dallo stesso distribution: sale fino al distribution e lì viene instradato
destinazione in un’altra area o verso servizi centrali: sale al distribution, poi attraversa il core, poi scende nel distribution corretto

Questa è probabilmente la sintesi più utile.

#### 16. Formula finale molto compatta

Si può riassumere così:

l’access collega gli endpoint,
il distribution organizza e instrada le reti locali,
il core collega rapidamente i vari blocchi di distribution.

Oppure, ancora più concretamente:

il distribution decide “se posso consegnare qui oppure devo mandare al backbone”;
il core decide “a quale distribution devo consegnare questo traffico”.


### Diagrammi
Si consideri una rete campus abbastanza tipica con architettura gerarchica a tre livelli. Lo schema seguente è volutamente semplice ma realistico.

SCHEMA LOGICO

```
                    INTERNET
                       |
                    FIREWALL
                       |
                    CORE 1
                   /      \
                CORE 2    (ridondanza)
                 /   \
         ------------- -------------
         |                           |
    DISTRIBUTION A              DISTRIBUTION B
    (Edificio A)                (Edificio B)
       /      \                     /      \
 ACCESS A1  ACCESS A2         ACCESS B1  ACCESS B2
    |           |                |           |
  PC A1       PC A2           PC B1       SERVER B
```

Ipotesi tipica:

VLAN 10 studenti   edificio A → 10.10.10.0/24
VLAN 20 laboratori edificio A → 10.10.20.0/24
VLAN 110 amministr edificio B → 10.20.110.0/24
VLAN 120 server    edificio B → 10.20.120.0/24

I gateway delle VLAN sono sugli switch di distribution.

Esempio:

Distribution A
VLAN 10 → 10.10.10.1 EV:todo: non sono indirizzi di rete
VLAN 20 → 10.10.20.1

Distribution B
VLAN 110 → 10.20.110.1
VLAN 120 → 10.20.120.1

Il core invece vede le reti in modo più sintetico, ad esempio:

10.10.0.0/16 → Distribution A
10.20.0.0/16 → Distribution B

---

CASO 1
COMUNICAZIONE NELLA STESSA VLAN E STESSO ACCESS SWITCH

PC A1 → PC A2
Entrambi VLAN 20
Access A1

Percorso dei pacchetti:

PC A1 -> ACCESS A1 -> PC A2

Il traffico non arriva nemmeno al distribution. Motivo: stesso dominio Layer 2. 

Operazione reale:

1 PC A1 invia ARP
2 ACCESS A1 impara MAC
3 frame Ethernet inviato direttamente al PC B

---

CASO 2
STESSA VLAN MA ACCESS SWITCH DIVERSI

PC A1 VLAN 20 → PC A2 VLAN 20

Schema

PC A1
↓
ACCESS A1
↓ trunk VLAN 20
DISTRIBUTION A
↓ trunk VLAN 20
ACCESS A2
↓
PC A2

In questo caso il traffico è ancora Layer 2.

Il distribution non fa routing.
Fa solo forwarding Ethernet tra trunk.

Il core non interviene perché la VLAN è locale al blocco Distribution A.

---

CASO 3
TRAFFICO TRA VLAN DIVERSE NELLO STESSO EDIFICIO

PC A1 VLAN 20
IP 10.10.20.15

Server locale VLAN 10
IP 10.10.10.50

Gateway VLAN 20
10.10.20.1 (Distribution A)

Percorso

PC A1
↓
ACCESS A1
↓
DISTRIBUTION A (routing inter-VLAN)
↓
ACCESS A2
↓
SERVER

Sequenza logica:

1 PC vede che 10.10.10.50 è fuori subnet
2 usa il default gateway 10.10.20.1
3 il pacchetto arriva al Distribution A
4 Distribution A consulta tabella routing
5 trova rete 10.10.10.0 direttamente connessa
6 riscrive MAC destinazione
7 inoltra verso VLAN 10

Il core non viene usato.

Questa è una funzione tipica del distribution.

---

CASO 4
COMUNICAZIONE TRA EDIFICI (ATTRAVERSO IL CORE)

PC A1 laboratorio
10.10.20.15

Server amministrativo
10.20.110.30

Percorso reale

PC A1
↓
ACCESS A1
↓
DISTRIBUTION A
↓
CORE
↓
DISTRIBUTION B
↓
ACCESS B1
↓
SERVER

Sequenza tecnica

1 PC A1 invia al gateway 10.10.20.1
2 Distribution A riceve il pacchetto
3 tabella routing → rete 10.20.0.0 via core
4 inoltro verso CORE
5 il CORE guarda la route
6 rete 10.20.0.0 → Distribution B
7 inoltro a Distribution B
8 Distribution B vede subnet locale
9 inoltra verso ACCESS B1
10 consegna al server

Il core qui agisce come dorsale di trasporto.

---

CASO 5
ACCESSO A INTERNET

PC A1 → sito web

Percorso

PC A1
↓
ACCESS A1
↓
DISTRIBUTION A
↓
CORE
↓
FIREWALL
↓
INTERNET

Sequenza

1 PC invia al gateway locale
2 Distribution A vede destinazione esterna
3 usa route verso core
4 core inoltra al firewall
5 firewall applica NAT e policy
6 traffico esce su Internet

---

VISUALIZZAZIONE SEMPLIFICATA DEL FLUSSO

tra host stessa VLAN

HOST
↓
ACCESS
↓
HOST

tra VLAN nello stesso edificio

HOST
↓
ACCESS
↓
DISTRIBUTION (routing)
↓
ACCESS
↓
HOST

tra edifici diversi

HOST
↓
ACCESS
↓
DISTRIBUTION
↓
CORE
↓
DISTRIBUTION
↓
ACCESS
↓
HOST

verso Internet

HOST
↓
ACCESS
↓
DISTRIBUTION
↓
CORE
↓
FIREWALL
↓
INTERNET

---

IDEA CHIAVE PER VISUALIZZARE CORE E DISTRIBUTION

Distribution

• aggrega access switch
• gestisce VLAN
• fa routing inter-VLAN
• applica policy
• conosce i dettagli locali

Core

• collega i diversi distribution
• trasporta traffico molto velocemente
• mantiene routing più semplice
• minimizza funzioni pesanti

---

### Risposta 3

Punto fondamentale: 
**in una architettura a tre layer il routing IP è presente sia nel core sia nel distribution**.  
Quello che cambia non è l’esistenza delle routing tables, ma **il tipo di informazioni che contengono e il ruolo che svolgono nel percorso dei pacchetti**.

In altre parole:

* gli **access switch** normalmente non fanno routing (sono Layer-2);
* i **distribution switch** fanno routing **locale** tra le reti dell’area che servono;
* i **core switch** fanno routing tra le varie **aree** della rete.

Quindi **sia il core sia il distribution hanno routing tables**.

La differenza è concettuale:

distribution → routing **dettagliato e locale**
core →         routing **aggregato e di backbone**

---

#### 1. Routing tables nei distribution switch

In generale, i **distribution switch hanno routing tables complete per le reti locali**.

Queste tabelle includono tipicamente:

1. **reti direttamente connesse**

Sono le VLAN presenti sotto quel distribution.
Ogni VLAN ha una SVI (Switched Virtual Interface) che funge da gateway.

Esempio:

VLAN 20 → 10.10.20.1
VLAN 30 → 10.10.30.1

Queste reti appaiono nella routing table come **connected routes**.

2. **rotte verso altre aree della rete**

Le reti non locali vengono instradate verso il core.

3. **default route (spesso)**

Il distribution spesso ha una route:

0.0.0.0/0 → core

che indica che tutto ciò che non è locale deve andare al core.

4. **rotte apprese dinamicamente**

Se si usa OSPF, IS-IS o EIGRP, il distribution apprende le reti delle altre aree tramite il core.

---

#### 2. Routing tables nei core switch

Il core **fa routing tra distribution**, ma normalmente non ha tutte le subnet dettagliate della rete.

Il core usa spesso **route aggregate (summarization)**.

Esempio:

**tutte** le reti dell'edificio A
10.10.0.0/16

**tutte** le reti dell'edificio B
10.20.0.0/16

In questo modo la routing table del core resta piccola e veloce.

Una routing table tipica del core contiene:

* route aggregate verso i distribution
* default route verso firewall / Internet
* eventuali rotte verso server farm o datacenter

Il core quindi **non ha bisogno di conoscere ogni VLAN**.

---

#### 3. Come avviene il routing in pratica

Quando un pacchetto arriva a uno switch Layer-3 succede questo:

1. lo switch legge l'indirizzo IP di destinazione
2. consulta la routing table
3. sceglie la route più specifica
4. determina l'interfaccia di uscita
5. **riscrive** l'intestazione Ethernet
6. inoltra il pacchetto

Questo processo è identico sia nel core sia nel distribution.

---

#### 4. Applicazione all'esempio della rete precedente

Rete semplificata:

Edificio A
Distribution A

VLAN 10 studenti → 10.10.10.0/24
VLAN 20 laboratori → 10.10.20.0/24

Edificio B
Distribution B

VLAN 110 amministrazione → 10.20.110.0/24
VLAN 120 server → 10.20.120.0/24

Il core collega i due distribution.

---

#### 5. Routing table del Distribution A

Distribution A conosce le proprie VLAN.

Routing table tipica:

10.10.10.0/24 → directly connected (VLAN10)
10.10.20.0/24 → directly connected (VLAN20)
10.20.0.0/16  → via core
0.0.0.0/0     → via core

Interpretazione:

le reti 10.10.x sono locali
tutte le reti 10.20.x stanno dietro Distribution B tramite il core

---

#### 6. Routing table del Distribution B

Routing table:

10.20.110.0/24 → directly connected
10.20.120.0/24 → directly connected
10.10.0.0/16   → via core
0.0.0.0/0      → via core

---

#### 7. Routing table del Core

Il core vede i due blocchi di rete.

Routing table:

10.10.0.0/16 → Distribution A
10.20.0.0/16 → Distribution B
0.0.0.0/0    → firewall

Il core non contiene le singole VLAN.

Non serve sapere:

10.10.10.0
10.10.20.0

gli basta sapere che **tutto il blocco 10.10.x è dietro Distribution A**.

---

#### 10. Riassunto concettuale molto importante

In una architettura a 3 layer:

distribution switch

* hanno routing tables dettagliate
* conoscono le VLAN locali
* fanno inter-VLAN routing
* inviano traffico remoto verso il core

core switch

* hanno routing tables più piccole
* usano route aggregate
* trasportano traffico tra distribution
* mantengono il backbone semplice e veloce

---

Una regola molto utile per visualizzare il routing è questa:

distribution decide **se la destinazione è locale o remota**
core decide **verso quale distribution inviare il traffico**.

#### risposta 4

Quando si parla di **core switch** in una architettura a tre livelli, il termine *zona* non è un termine tecnico di routing standard. È un 
termine **descrittivo** usato per indicare una **porzione della rete che sta dietro un certo distribution layer**.  
In pratica significa semplicemente **un blocco logico di rete**.

Una zona può corrispondere a:

* un edificio
* un piano
* un reparto aziendale
* un campus secondario
* una server farm
* una rete remota collegata con VPN

Quindi *zona* = **insieme di subnet gestite da uno o più distribution switch**.

Non è una struttura formale del protocollo IP. È solo un modo per descrivere la topologia.

---

#### 1. La routing table del core ha una route per ogni distribution?

In generale **no**.

Il core **non ha normalmente una route per ogni distribution switch**,  
ma piuttosto **una route per ogni blocco di rete** che sta dietro quel distribution.

La routing table contiene **destinazioni di rete**, non dispositivi.

Quindi le entry sono del tipo:

rete → next-hop

non

switch → next-hop

---

#### 2. Che cosa rappresentano le route del core

Le route del core rappresentano **blocchi di indirizzi IP**.

Questi blocchi sono spesso **aggregazioni di subnet** (route summarization).

Questo è molto importante perché:

* riduce la dimensione delle routing tables
* aumenta la velocità del forwarding
* rende la rete più stabile

---

#### 3. Esempio semplice

Supponiamo questa rete.

Edificio A
Distribution A

VLAN 10 → 10.10.10.0/24
VLAN 20 → 10.10.20.0/24
VLAN 30 → 10.10.30.0/24

Edificio B
Distribution B

VLAN 110 → 10.20.110.0/24
VLAN 120 → 10.20.120.0/24

Il core **non ha bisogno di conoscere ogni VLAN**.

Può avere questa routing table:

10.10.0.0/16 → Distribution A
10.20.0.0/16 → Distribution B

Quindi solo **due route** invece di cinque.

Questo è il concetto di **route summarization**.

---

#### 4. Perché non avere tutte le subnet nel core

Il core potrebbe anche avere tutte le subnet.

Esempio:

10.10.10.0/24  → Distribution A
10.10.20.0/24  → Distribution A
10.10.30.0/24  → Distribution A
10.20.110.0/24 → Distribution B
10.20.120.0/24 → Distribution B

Questo funziona.

Ma non è ideale perché:

* la routing table cresce molto
* aumenta il traffico dei protocolli di routing
* aumenta la complessità
* peggiora la scalabilità

Per questo si preferisce la **summarization**.

---

#### 5. Next-hop nella routing table del core

Ogni route del core punta a un **next-hop IP**, che è tipicamente un'interfaccia del distribution.

Esempio reale.

Routing table del core:

10.10.0.0/16 → 192.168.1.2
10.20.0.0/16 → 192.168.1.3

Dove

192.168.1.2 = Distribution A
192.168.1.3 = Distribution B

Quindi la routing table **non contiene il nome dello switch**, ma il suo indirizzo IP.

---

#### 6. Caso con ridondanza

In molte reti il core è collegato a **due distribution** per ridondanza.

Esempio:

Core
↓
Distribution A1
Distribution A2

Entrambi servono lo stesso edificio.

La routing table del core può avere:

10.10.0.0/16 → A1
10.10.0.0/16 → A2

Questo si chiama **ECMP (Equal Cost Multi Path)**.

Il traffico può essere bilanciato tra i due percorsi.

---

#### 7. Esempio completo con routing tables

Architettura:

PC laboratorio edificio A
10.10.20.15

Server amministrativo edificio B
10.20.110.30

Distribution A gestisce:

10.10.10.0/24
10.10.20.0/24

Distribution B gestisce:

10.20.110.0/24
10.20.120.0/24

---

Routing table Distribution A

10.10.10.0/24 → connected
10.10.20.0/24 → connected
10.20.0.0/16 → core

---

Routing table Core

10.10.0.0/16 → Distribution A
10.20.0.0/16 → Distribution B

---

Routing table Distribution B

10.20.110.0/24 → connected
10.20.120.0/24 → connected
10.10.0.0/16 → core

---

#### 8. Percorso reale del pacchetto

PC 10.10.20.15 → server 10.20.110.30

passo 1

PC invia al gateway 10.10.20.1
Distribution A

passo 2

Distribution A controlla routing table

destinazione 10.20.110.30
match → 10.20.0.0/16

next-hop → core

passo 3

Core riceve il pacchetto

match → 10.20.0.0/16

next-hop → Distribution B

passo 4

Distribution B controlla routing table

match → 10.20.110.0/24

rete direttamente connessa

passo 5

inoltro allo switch access e quindi al server

---

#### 9. Regola fondamentale da ricordare

La routing table non rappresenta **dispositivi**, ma **reti IP**.

Quindi il core non instrada verso uno switch perché è uno switch, ma perché **quello switch è il next-hop verso una certa rete**.

---

#### 10. Formula mentale molto utile

Distribution layer

routing dettagliato delle subnet locali

Core layer

routing aggregato tra blocchi di rete

---
