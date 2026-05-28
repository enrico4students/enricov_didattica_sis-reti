
# Subnetting IPv4 e piani di indirizzamento

---

## 1. Contesto operativo

Nel lavoro con gli indirizzi IPv4 si presentano due contesti distinti, che richiedono approcci diversi.

Nel contesto degli esercizi, viene fornito un indirizzo di rete iniziale e si richiede di applicare tecniche di subnetting per suddividerlo in sottoreti. L’obiettivo è verificare la correttezza dei calcoli e la capacità di applicare regole formali.

Nel contesto professionale, invece, spesso non esiste una rete assegnata. È necessario **scegliere** un blocco di indirizzi privati e progettare l’intera struttura della rete.  
In questo caso l’obiettivo non è solo la correttezza, ma anche:

* coerenza
* leggibilità
* scalabilità
* manutenibilità

Questa distinzione è fondamentale: una soluzione corretta dal punto di vista matematico può essere inefficiente o problematica dal punto di vista operativo.

---

## 2. Struttura degli indirizzi IPv4

Un indirizzo IPv4 è composto da:

* 32 bit
* suddivisi in 4 ottetti da 8 bit
* rappresentati in notazione decimale puntata

Esempio:


192.168.10.25


Ogni indirizzo è suddiviso logicamente in:

* parte di rete
* parte di host

La separazione è determinata dalla subnet mask o dal prefisso CIDR.

---

## 3. Indirizzamento classful (richiamo)

Storicamente le reti erano suddivise in classi.

Classe A:

* primo bit 0
* intervallo: 0.0.0.0 – 127.255.255.255
* mask: /8

Classe B:

* primi bit 10
* intervallo: 128.0.0.0 – 191.255.255.255
* mask: /16

Classe C:

* primi bit 110
* intervallo: 192.0.0.0 – 223.255.255.255
* mask: /24

Limite principale:

* rigidità
* spreco di indirizzi

Questo modello **non è più utilizzato** nella progettazione moderna, ma è utile per comprendere i fondamenti.

---

## 4. CIDR (Classless Inter-Domain Routing)

CIDR introduce la notazione:

indirizzo/**prefisso**

Esempio: 192.168.10.0/**27**

Significa che:

* i primi **27** bit identificano la rete
* i restanti bit identificano gli host

Vantaggi:

* maggiore flessibilità
* riduzione dello spreco
* possibilità di aggregazione delle rotte

---

## 5. VLSM (Variable Length Subnet Mask)

VLSM consente di:

* creare sottoreti di dimensioni diverse
* adattare ogni rete al numero reale di dispositivi

È la tecnica **utilizzata nella progettazione reale** delle reti.

---

## 6. Obiettivo di un piano di indirizzamento

Per ogni rete o sottorete devono essere definiti:

* Network ID
* Subnet mask (o prefisso)
* Gateway
* indirizzi statici (server, servizi)
* intervallo host assegnabile
* Broadcast

È utile utilizzare una struttura tabellare standard.

Formato tipico:

| Rete | Subnet mask | Router | Server | Host | Broadcast |

Nota:

* la colonna “Server” rappresenta indirizzi riservati a servizi **statici**  
* nei link punto-punto può essere non applicabile  

---

## 7. Regole operative generali

Per ottenere risultati coerenti è necessario adottare criteri fissi.

### 7.1 Assegnazione degli indirizzi

* gateway: primo o ultimo host (scelta coerente)
* server: blocco iniziale della rete
* host: intervallo restante

---

### 7.2 Dimensionamento

* stimare il numero reale di dispositivi   
* aggiungere margine di crescita  
* scegliere subnet con:

  host_utilizzabili >= host_richiesti

---

### 7.3 Verifiche

* nessuna sovrapposizione tra subnet
* corretto allineamento
* uso corretto di network e broadcast

---

## 8. Differenza operativa fondamentale

Negli esercizi:

* la rete è assegnata

Nel mondo reale:

* la rete viene scelta

Questa è la differenza più importante nella pratica professionale.


Nel mondo reale **non si ragiona** più in termini di “classi” (A, B, C) ma di **blocchi CIDR**, tuttavia gli intervalli privati storici restano un riferimento pratico:

* **10.0.0.0/8** → reti grandi e strutturate
* **172.16.0.0/12** → reti medio-grandi
* **192.168.0.0/16** → reti piccole o segmenti locali

La scelta dipende principalmente da **dimensione, crescita prevista e organizzazione logica**.

**NELLA SCUOLA E' CONSIGLIABILE SEGUIRE L'APPROCCIO DEL LIBRO DI TESTO E VERIFICARE ESPLICITAMENTE CON IL DOCENTE**  


---

## 9. Indirizzi privati e progettazione reale

Questa sezione è centrale per comprendere come si opera fuori dal contesto scolastico.

---

### 9.1 Blocchi disponibili

Gli indirizzi privati sono:

* 10.0.0.0/8
* 172.16.0.0/**12**   NB /**12**, non /16
* 192.168.0.0/**16**  NB /**16**, non /24

---

### 9.2 Scelta nel mondo professionale

#### Uso di 10.0.0.0/8

È il blocco più usato nelle reti aziendali strutturate.

Motivi:

* spazio enorme
* organizzazione gerarchica semplice
* facile espansione

Esempio:

```
10.10.10.0/24 → uffici amministrativi
10.10.20.0/24 → server interni
10.10.30.0/24 → rete ospiti
10.10.40.0/24 → WiFi aziendale
10.20.10.0/24 → sede secondaria (altra città)
10.30.0.0/16 → data center
```

Caratteristica chiave:

* organizzazione gerarchica (es. terzo ottetto = VLAN o sede)
* facile espansione senza ristrutturare la rete

---  

#### Uso di 172.16.0.0/**12**

Offre un buon compromesso tra dimensione e semplicità.  
È molto usato quando il blocco 10 è già occupato.  

Uso reale:

* aziende con più sedi ma non enormi
* reti corporate suddivise per regioni o business unit
* ambienti separati (produzione, test, laboratorio)

Il blocco 172.16.0.0/12 comprende tutti gli indirizzi da:

    172.16.0.0 a 172.31.255.255

Contiene 16 reti /16 complete:

    172.16.0.0/16
    172.17.0.0/16
    ...
    172.31.0.0/16

Oppure 4096 reti /24
(4 bits e quindi 16 reti dal "resto" del secondo ottetto × 256 reti dal terzo ottetto)

    172.16.0.0/24
    172.16.1.0/24
    ...
    172.31.254.0/24
    172.31.255.0/24


---

#### Esempi

##### /24

172.16.10.0/24 → sede Milano (uffici)  
172.16.20.0/24 → sede Roma (uffici)  
172.16.30.0/24 → laboratorio/test  
172.16.100.0/24 → DMZ (web server, reverse proxy)  
172.17.0.0/16 → infrastruttura server centralizzata  

È una scelta pratica perché:

* semplice da amministrare
* broadcast limitato
* facile separazione delle VLAN
* buona leggibilità del piano IP

##### /16


172.16.0.0/16 → sede Milano (uffici)  
172.17.0.0/16 → sede Roma (uffici)  
172.18.0.0/16 → laboratorio/test  
172.19.0.0/16 → DMZ (web server, reverse proxy)  
172.20.0.0/16 → infrastruttura server centralizzata  

In questo caso ogni rete /16 contiene 65.536 indirizzi (circa 65533 disponibili)  


#### Differenza pratica tra /24 e /16

Le reti /24:

* sono più piccole
* limitano il traffico broadcast
* sono più facili da segmentare
* sono molto usate nelle VLAN aziendali

Le reti /16:

* sono enormi
* possono contenere decine di migliaia di host
* sono adatte a grandi sedi o macro-ambienti
* possono aumentare traffico broadcast e complessità se usate direttamente in Layer 2

Nella pratica reale:

* /24 è molto comune per VLAN utenti
* /16 viene spesso assegnata come blocco generale a una sede o regione
* all’interno della /16 si creano poi sottoreti più piccole


---

#### Uso di 192.168.0.0/16

È il più diffuso in assoluto, ma principalmente per reti di dimensioni ridotte.

Uso reale:

* piccoli uffici
* filiali singole
* reti domestiche o SOHO
* segmenti isolati dentro reti più grandi

Esempio realistico:

```
192.168.1.0/24 → rete ufficio
192.168.2.0/24 → rete WiFi ospiti
192.168.10.0/24 → rete dispositivi (stampanti, IoT)
192.168.100.0/24 → piccola DMZ locale
```

Caratteristica chiave:

* semplicità
* facile configurazione
* poco adatto a grandi espansioni

---

### 9.3 Criteri progettuali reali

Nella progettazione reale si applicano criteri che **non** emergono negli esercizi.
(il vostro insegnante vi ricorda che GLI INSEGNANTI SONO ABITUATI AL CONTESTO DEGLI ESERCIZI ... )

* organizzazione gerarchica degli indirizzi
* separazione per funzione (VLAN)
* previsione di crescita
* coerenza nella numerazione

---

### 9.4 Errori tipici

* uso casuale degli indirizzi
* riutilizzo della stessa rete in più contesti
* assenza di struttura
* mancata previsione di espansione

---

### 9.5 Buone pratiche

* mantenere ordine logico negli indirizzi
* evitare sovrapposizioni
* progettare pensando al futuro
* documentare il piano

---

## 10. Struttura del piano di indirizzamento

È utile distinguere due livelli.

### 10.1 Livello di calcolo

| Network | Subnet mask | Primo host | Ultimo host | Broadcast |

---

### 10.2 Livello operativo

| Nome rete | Network | Prefisso | Gateway | Statici | Host |

---

## 11. Introduzione alle procedure operative

Le procedure operative si distinguono in:

* classful (approccio base)
* CIDR (subnetting uniforme)
* VLSM (subnetting reale)

Le procedure dettagliate sono sviluppate nella parte successiva.

---

## 12. Piano di indirizzamento classful

Questo approccio considera la rete utilizzando la **subnet mask di default della classe**, senza ulteriori suddivisioni.

È utile come base concettuale e come esercizio introduttivo.

---

### 12.1 Procedura operativa

1. Determinare la classe dell’indirizzo osservando il primo ottetto.
2. Associare la subnet mask di default:

   * Classe A → /8
   * Classe B → /16
   * Classe C → /24
3. Determinare i parametri principali:

   * Network ID
   * Broadcast
   * Primo host
   * Ultimo host
4. Applicare criteri di assegnazione (gateway, eventuali server).

---

### 12.2 Osservazioni operative

* Il Network ID è determinato automaticamente dalla classe.
* Il broadcast si ottiene ponendo a 1 tutti i bit della parte host.
* Il numero di host disponibili è:

  2^(bit_host) − 2

dobbiamo ricordare che il router ed eventuali server hanno bisogno di IP che quindi non sono disponibili per dispositivi utente

---

### 12.3 Limiti dell’approccio classful

* spreco di indirizzi
* rigidità
* non adatto a reti moderne

Per questo motivo **viene utilizzato solo a scopo didattico**.

---

## 13. Piano di indirizzamento CIDR (subnetting uniforme)

In questo approccio si utilizza un prefisso fisso per tutte le sottoreti.

È tipico degli esercizi in cui si richiede di suddividere una rete in parti uguali.

---

### 13.1 Procedura operativa

1. Identificare l’indirizzo di partenza e il prefisso.

2. Calcolare:

   * subnet mask

   * numero totale di indirizzi:

     2^(32 − n)

   * numero di host utilizzabili:

     2^(32 − n) − 2

3. Determinare il **block size** (incremento):

   * /26 → blocchi da 64
   * /27 → blocchi da 32
   * /28 → blocchi da 16

4. Individuare le sottoreti:

   * partendo dal Network ID iniziale
   * aggiungendo il block size

5. Per ogni sottorete determinare:

   * Network ID
   * Primo host
   * Ultimo host
   * Broadcast

6. Applicare criteri di assegnazione.

---

### 13.2 Concetto di allineamento

Ogni sottorete deve iniziare su un indirizzo multiplo del block size.

Esempio:

Con /26 (blocchi da 64):

```
192.168.1.0
192.168.1.64
192.168.1.128
192.168.1.192
```

Un indirizzo come 192.168.1.20 non può essere Network ID.

---

### 13.3 Errori tipici

* mancato allineamento
* calcolo errato del block size
* errore nel broadcast
* sovrapposizione tra subnet

---

## 14. Piano di indirizzamento VLSM (subnetting variabile)

È il metodo **utilizzato nella progettazione reale**.

Permette di assegnare a ogni rete una dimensione adeguata.

In una traccia di un test importante, ex. esame di stato, usarlo se effettivamente necessario.  

---

### 14.1 Procedura operativa

1. Elencare le reti richieste con numero di host.

2. Ordinare le reti in ordine decrescente.

3. Per ogni rete:

   * determinare la dimensione minima:

     trovare 2^k tale che (2^k − 2) ≥ host richiesti

   * calcolare il prefisso:

     prefisso = 32 − k

4. Allocare le sottoreti:

   * partire dall’inizio della rete disponibile
   * assegnare il primo blocco
   * proseguire dal primo indirizzo libero successivo

5. Per ogni sottorete calcolare:

   * Network ID
   * Broadcast
   * intervallo host

6. Applicare le regole operative:

   * gateway
   * indirizzi statici

---

### 14.2 Verifica finale

* nessuna sovrapposizione
* corretto allineamento
* tutte le reti contenute nel blocco iniziale
* numero host sufficiente

---

### 14.3 Osservazioni operative

* la prima rete assegnata è la più grande
* l’ordine è fondamentale
* errori iniziali compromettono tutto il piano

---

## 15. Gestione dei casi particolari

### 15.1 Link punto-punto

Tipicamente si utilizzano subnet /30:

* 4 indirizzi totali
* 2 utilizzabili

Struttura:

* network
* host 1
* host 2
* broadcast

---

### 15.2 Subnet troppo piccole

Errore tipico:

* scegliere una subnet con host insufficienti

È necessario verificare sempre:

```
host_utilizzabili ≥ host richiesti
```

---

### 15.3 Subnet troppo grandi

* non è un errore tecnico
* ma è un errore progettuale

Spreca indirizzi e riduce l’ordine del piano.

---

### 15.4 Reti non allineate

Esempio:

```
192.168.1.20/26
```

Non è un Network ID valido.

La rete corretta è:

```
192.168.1.0/26
```

---

## 16. Costruzione della tabella finale

La soluzione deve essere presentata in modo strutturato.

Formato tipico:

| Rete | Prefisso | Subnet mask | Network | Primo host | Ultimo host | Broadcast |

Oppure, in forma operativa:

| Nome rete | Network | Prefisso | Gateway | Statici | Host |

---

## 17. Coerenza del piano di indirizzamento

Un piano corretto deve rispettare:

* assenza di sovrapposizioni
* corretto utilizzo degli indirizzi
* coerenza nella numerazione
* completezza delle informazioni

---

## 18. Collegamento con la progettazione reale

Le procedure viste permettono di risolvere esercizi.

Nella realtà si aggiunge un ulteriore livello:

* scelta del blocco iniziale
* organizzazione logica della rete
* separazione per VLAN o funzioni
* previsione di crescita

Esempio reale:

```
10.10.10.0/24 → uffici
10.10.20.0/24 → server
10.10.30.0/24 → WiFi
10.10.40.0/24 → guest
```

Questo tipo di struttura:

* non deriva da un esercizio
* ma da una scelta progettuale

---
