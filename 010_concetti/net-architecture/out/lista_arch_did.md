
# rete aziendale enterprise con segmentazione per reparti, DMZ, VPN site-to-site, VPN utenti, Wi-Fi enterprise e servizi infrastrutturali

A fini didattici, per mostrare tutti i casi possibili, debbo definire un'architettura di rete professionale per una ditta di grandi dimensioni che produce software.

La ditta ha le seguenti unità organizzative le cui reti debbono essere separate:

* programmatori, 300 dipendenti, occupano il primo piano e parte del secondo
* human resources, con 30 dipendenti al secondo piano assieme ai programmatori
* vendite, con 100 dipendenti, al terzo piano e al quarto
* procurement, 10 dipendenti, al quarto piano
* marketing, 20 dipendenti, al quarto piano
* IT interno, 20 persone, che gestiscono i seguenti server situati nel seminterrato (piano 0):

  * WEB server, che deve essere raggiungibile da Internet
  * RDBMS che deve essere raggiungibile dal WEB server e dal DBA che fa parte dell'IT interno
  * (NoSQL) MongoDB server che deve essere raggiungibile dal WEB server e dal DBA che fa parte dell'IT interno
  * Media server per filmati, che deve essere raggiungibile dal WEB server e dal DBA che fa parte dell'IT interno
  * Sistema di intrusion prevention, accessibile solo all'IT interno, centralizzato
  * server vendite interno, accessibile solo dal reparto vendite
  * 5 server di sviluppo che devono essere raggiungibili dai programmatori

Per i server esposti su Internet, e per i server utilizzati dai server esposti su Internet, specificare se vanno posti in DMZ o in rete interna, e perché.

È obbligatorio usare un server RADIUS; per il resto dello IAM la scelta è libera.

La connessione Internet è di importanza vitale: deve essere usata una soluzione veloce per consentire eventuali future implementazioni di hybrid cloud per big data; la connessione deve essere resiliente.

Per ogni gruppo, su tutti i piani, è disponibile accesso Wi-Fi, che deve essere integrato solo con la rete cablata a cui il gruppo ha accesso.

Per tutti i dipendenti deve essere disponibile accesso VPN limitato ai sistemi del gruppo.

Deve essere disponibile una VPN site-to-site con una seconda sede con la stessa organizzazione e dimensioni; ogni reparto dell'altra sede deve avere accesso a tutta e sola la porzione di rete dedicata al reparto corrispondente.

Deve essere mostrata e spiegata la gestione della VPN site-to-site (server dedicato? funzionalità deployata assieme ad altre?) e descritto quale protocollo viene usato, e anche una soluzione commerciale usata attualmente nel mondo corporate.

Si vogliono almeno tre zone logiche distinte: Internet, DMZ, rete interna.

Deve necessariamente essere usato un reverse proxy; la sua posizione deve essere mostrata chiaramente nell'architettura.

DHCP, DNS e NTP devono essere modellati.

Decidere se introdurre una rete di management separata; se sì, spiegare i motivi e definirla con cura.

Decidere se sono necessari o utili:

* armadi di piano
* switch di accesso per piano
* backbone verticale
* core nel seminterrato o in sala server
* eventuale distribuzione a due livelli o tre livelli

Motivare le decisioni.

Tenendo conto che si può avere qualunque indirizzo pubblico si voglia:

* scegliere l'indirizzo in modo ragionato, spiegare i motivi
* spiegare se internamente si usa un indirizzo privato, quale si sceglie e perché

È desiderabile, ma non obbligatoria se esistono soluzioni migliori, un'architettura con WPA2/WPA3-Enterprise e assegnazione VLAN tramite RADIUS.

Risolvi nel seguente modo:

* crea un'architettura professionale attualmente usata nelle grandi aziende, scegliendo l'approccio più usato
* non spiegare i concetti base, sono già spiegati in altre lezioni
* spiega le motivazioni delle scelte, spiegando anche brevemente le alternative scartate e i motivi
* per i vari server e dispositivi di rete indica sempre un dispositivo o software professionale usato attualmente nel mondo reale, inserendo un link verificato alla pagina del prodotto
* comincia con un'analisi testuale chiara, poi crea diagrammi in formato testo e in PlantUML; nei diagrammi inserisci commenti esplicativi senza esagerare per non renderli troppo confusionari


Risolvila nel miglior modo possibile. 
La soluzione deve cominciare con un'analisi chiara, concisa ma completa, deve includere diagrammi in duplice formato testuale e plantuml. 
Non devono essere spiegati concetti base di sistemi e reti, devono essere spiegate le tematiche disposibi e scelte di livello medio-avanzato o professionali dato che le lezioni non entrano in questo ambito.
Il criterio primario è che la soluzione sia professionale e realistica per grandi aziende.  
Se vi sono più alternative fra le soluzioni professionali realistiche e complete scegli quella più adatta alla didattica

---


### Possibili punti semanticamente ambigui (non errori)

Sono solo osservazioni tecniche.

#### 1. “server utilizzati dai server esposti su Internet”

È corretto ma **molto generale**.
Nella soluzione alcuni potrebbero includere:

* database
* media server
* altri backend

Va bene se l'obiettivo è **far discutere la scelta DMZ vs LAN interna**.


#### 2. IPS centralizzato

“Sistema di intrusion prevention, centralizzato” può essere interpretato in due modi:

* IPS inline sulla rete
* piattaforma centralizzata di gestione

Non è un errore ma può produrre **soluzioni architetturali diverse**.

---

#### 3. “server VPN site-to-site”

Hai già migliorato la formulazione.
Ora è corretto perché chiedi esplicitamente se sia:

* server dedicato
* funzionalità di altro apparato

Questa è una buona formulazione didattica.

---

#### Valutazione finale

La traccia ora è:

* molto chiara
* tecnicamente realistica
* abbastanza vincolata
* ma lascia spazio a scelte architetturali

È una **buona traccia da progetto d'esame o laboratorio avanzato di reti**.

