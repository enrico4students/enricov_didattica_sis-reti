# Lezione: Subnetting IPv4 e piani di indirizzamento
(Istituto Tecnico Informatico – Sistemi e Reti)


---

## 1. Richiami teorici essenziali

### 1.1 Struttura di un indirizzo IPv4
Un indirizzo IPv4 è composto da:
- 32 bit
- suddivisi in 4 ottetti (8 bit ciascuno)
- rappresentati in notazione decimale puntata

Esempio:
192.168.10.25

Ogni indirizzo è suddiviso logicamente in:
- parte di rete
- parte di host

La suddivisione è determinata dalla subnet mask o dal prefisso CIDR.

---

### 1.2 Indirizzamento classful
Storicamente le reti erano divise in classi.

Classe A
- Primo bit **0**
- Range: 0.0.0.0 – 127.255.255.255
- Default mask: 255.0.0.0 (/8)

Classe B
- Primi bit **10**
- Range: 128.0.0.0 – 191.255.255.255
- Default mask: 255.255.0.0 (/16)

Classe C
- Primi bit **110**
- Range: 192.0.0.0 – 223.255.255.255
- Default mask: 255.255.255.0 (/24)

Limite principale: spreco di indirizzi, 
a causa del fatto che i bits che identificano la classe sono "bloccati"

---

### 1.3 CIDR (Classless Inter-Domain Routing)
CIDR introduce la notazione:

Indirizzo/prefisso

Esempio:
192.168.10.0/27

Significa che i primi 27 bit identificano la rete in questo esempio.

Vantaggi:
- flessibilità
- aggregazione di rotte
- riduzione sprechi

---

### 1.4 VLSM (Variable Length Subnet Mask)
VLSM permette di:
- suddividere una rete in sottoreti di dimensioni diverse
- assegnare a ciascuna sottorete solo gli indirizzi necessari

È fondamentale nella progettazione di un piano di indirizzamento aziendale.

---

## 2. Obiettivo e formato standard delle soluzioni

### 2.1 Obiettivo operativo
Definire, per ogni rete o sottorete, tutti i parametri necessari all’assegnazione coerente degli indirizzi:
- Rete (Network ID)
- Subnet mask (o prefisso)
- Gateway/Router (indirizzo del router nella sottorete)
- Eventuali server o servizi con IP statico (DNS, DHCP, file server, ecc.)
- Intervallo host assegnabile ai client
- Broadcast

Nota terminologica (per coerenza con la tabella):
- La colonna “Server” può indicare uno o più indirizzi riservati a servizi statici (non necessariamente un solo server).

---

### 2.2 Tabella standard
Nei piani di indirizzamneto è consigliabile una struttura tabellare e, per uniformità, usare sempre lo stesso formato:

| Rete | Subnet mask | Router | Server | Host | Broadcast |

In presenza di link punto-punto (/30):
- “Server” può essere indicato come N/D
- “Host” coincide con i due indirizzi utilizzabili (oppure indicare direttamente i due endpoint)

---

## 3. Regole generali (metodo deterministico e ripetibile)

### 3.1 Scelta di criteri fissi
Lavorare sempre con regole ripetibili:
- scegliere un criterio fisso per il gateway (spesso ultimo host utilizzabile oppure primo host utilizzabile)
- scegliere un criterio fisso per i server/servizi statici (spesso primo host utilizzabile, o un blocco iniziale dedicato)
- definire chiaramente quali indirizzi si riservano (router, server, stampanti, AP, switch management, ecc.)

---

### 3.2 Stimare correttamente gli host richiesti
Nel dimensionare una sottorete:
- contare i dispositivi reali che richiedono IP nella sottorete (PC, server, stampanti, AP, gestione switch, ecc.)
- aggiungere riserve coerenti (crescita utenti, nuovi dispositivi, margine tecnico)

Poi scegliere una subnet tale che:
- host_utilizzabili **>**= host_richiesti

Nota:
- Network ID e broadcast esistono sempre nella sottorete, ma non corrispondono a dispositivi “assegnabili”.

---

# PARTE 1 – PROCEDURE OPERATIVE

## 4. Piano di indirizzamento classful
Si usa quando si considera la rete secondo la maschera “di default” della classe (A=/8, B=/16, C=/24), senza subnetting aggiuntivo.

Procedura:
1. Determinare la classe dall’ottetto iniziale (A, B, C).
2. Associare la subnet mask di default della classe.
3. Determinare:
   - Network ID (di fatto “già dato” dalla classe)
   - Broadcast (tutti i bit host a 1)
   - Primo host (network + 1)
   - Ultimo host (broadcast - 1)
4. Definire le assegnazioni usando le regole generali (gateway, server, riserve), mantenendo criteri fissi e dichiarati.

Risultato atteso:
- una singola riga (o poche righe) di tabella per ogni rete classful.

---

## 5. Piano di indirizzamento CIDR (subnetting “a taglia unica”)
Si usa quando si sceglie un prefisso /n e lo si applica in modo uniforme (tutte le sottoreti hanno la stessa dimensione). È tipico quando si divide una rete in N sottoreti uguali.

Procedura:
1. Identificare l’indirizzo di partenza e il prefisso /n.
2. Calcolare:
   - subnet mask corrispondente a /n
   - numero di indirizzi per sottorete: 2^(32-n)
   - host utilizzabili: 2^(32-n) - 2 (eccetto casi speciali come /31 in scenari particolari)
3. Calcolare l’incremento (block size) nell’ottetto interessato:
   - esempio /26: blocchi da 64 nell’ultimo ottetto
   - esempio /20: blocchi da 16 nel terzo ottetto
4. Elencare le sottoreti (se richiesto) aggiungendo l’incremento:
   - ogni sottorete ha un Network ID “allineato” al block size
5. Per ogni sottorete determinare i campi della tabella standard (Network ID, host, broadcast) e poi applicare le regole generali di assegnazione.

Risultato atteso:
- una tabella con una riga per ogni sottorete richiesta.

---

## 6. Piano di indirizzamento VLSM (subnetting “a taglia variabile”)
Si usa quando le sottoreti devono avere dimensioni diverse (reale progettazione: reparti, VLAN diverse, link punto-punto, DMZ, Wi-Fi guest, ecc.).

Procedura:
1. Elencare i fabbisogni reali:
   - per ogni sottorete: numero di host richiesti
   - includere riserve coerenti (router, server, dispositivi di rete, crescita)
2. Ordinare i fabbisogni in ordine decrescente (sempre).
3. Per ogni fabbisogno scegliere la sottorete minima sufficiente:
   - trovare il più piccolo blocco 2^k tale che (2^k - 2) >= host_richiesti
   - prefisso = 32 - k
   - esempio: 60 host -> serve blocco 64 -> /26
4. Allocare le sottoreti in sequenza, partendo dall’inizio della rete di partenza:
   - la prima sottorete usa il primo blocco disponibile
   - la seconda parte dal primo indirizzo libero dopo il broadcast della prima
   - ogni Network ID deve essere “allineato” alla dimensione del blocco
5. Per ogni sottorete calcolare i campi della tabella standard:
   - Network ID
   - Broadcast (ultimo indirizzo del blocco)
   - Primo host = network + 1
   - Ultimo host = broadcast - 1
6. Assegnare gli indirizzi interni con le regole generali (gateway, server, riserve), mantenendo criteri fissi e dichiarati.
7. Verifica finale obbligatoria:
   - nessuna sovrapposizione tra sottoreti
   - tutte le richieste soddisfatte
   - tutte le sottoreti rientrano nella rete di partenza
   - nessun buco “strano” dovuto a mancato allineamento

Risultato atteso:
- una tabella con una riga per ogni sottorete (LAN, DMZ, Wi-Fi, p2p), con parametri completi.


## 7. Valutazione  
Per valutare in modo completo lo svolgimento di un **esercizio di subnetting e piano di indirizzamento**, conviene separare i criteri di valutazione in alcune aree logiche.
Questo consente anche di attribuire facilmente punteggi parziali.

Di seguito una possibile **struttura completa e didatticamente coerente**.

---

# 1. Analisi dei requisiti del problema

Verificare se è stata compresa correttamente la traccia.

Sottopunti possibili:

* identificazione corretta delle **reti necessarie**
* identificazione del **numero di host richiesti per ogni rete**
* eventuale identificazione di **reti speciali** (DMZ, link punto-punto, rete management, ecc.)
* riconoscimento dei **vincoli** indicati nella traccia (indirizzo di partenza, uso di VLSM, rete classful, ecc.)

Questo punto valuta la **comprensione del problema**, non ancora il calcolo.

---

# 2. Identificazione delle sottoreti

Valutare se lo studente ha determinato correttamente le sottoreti logiche.

Sottopunti:

* numero corretto di sottoreti
* identificazione delle funzioni delle reti (LAN utenti, server, link router-router, ecc.)
* eventuale distinzione tra **reti LAN e reti di collegamento**

In molti esercizi questo punto precede il subnetting vero e proprio.

---

# 3. Scelta dell’architettura di rete

Valutare la correttezza della progettazione logica.

Sottopunti:

* separazione delle reti tramite **router**
* eventuale utilizzo di **VLAN**
* coerenza tra architettura scelta e requisiti
* presenza di eventuali **reti di interconnessione tra router**

Questo punto è importante negli esercizi di **progettazione di rete**, non solo di subnetting.

---

# 4. Calcolo delle dimensioni delle sottoreti

Valutare se sono state determinate correttamente le dimensioni delle subnet.

Sottopunti:

* numero minimo di **bit host necessari**
* dimensione della sottorete scelta
* eventuale uso corretto del **VLSM**
* verifica che il numero di host disponibili sia sufficiente

Errori frequenti:

* sottoreti troppo piccole
* sottoreti eccessivamente grandi senza motivo

---

# 5. Calcolo della subnet mask / prefisso

Valutare la correttezza del subnetting.

Sottopunti:

* subnet mask corretta
* prefisso CIDR corretto
* relazione corretta tra **bit di rete e bit host**
* coerenza con il numero di host richiesto

---

# 6. Determinazione degli indirizzi delle subnet

Valutare il calcolo degli indirizzi di rete.

Sottopunti:

* indirizzo di rete corretto
* indirizzo broadcast corretto
* primo indirizzo utilizzabile
* ultimo indirizzo utilizzabile

Questo è uno dei punti più importanti negli esercizi.

---

# 7. Costruzione del piano di indirizzamento

Valutare la completezza della tabella finale.

Sottopunti:

* assegnazione delle subnet alle diverse reti
* indirizzi assegnati ai router
* indirizzi assegnati ai server
* indirizzi assegnati agli host
* eventuale indirizzo gateway corretto

---

# 8. Coerenza globale del piano

Controllare che il piano di indirizzamento sia internamente consistente.

Sottopunti:

* assenza di **sovrapposizioni tra subnet**
* tutte le subnet appartengono alla rete di partenza
* nessun uso di indirizzi riservati (network o broadcast)
* corretta sequenza degli indirizzi

---

# 9. Rappresentazione e chiarezza

Valutare la qualità della presentazione.

Sottopunti:

* presenza di **tabella delle subnet**
* eventuale schema di rete
* chiarezza dei calcoli
* uso corretto della notazione CIDR

Questo punto è utile nelle verifiche scolastiche.

---

# 10. Verifica finale

Valutare se lo studente ha controllato il risultato.

Sottopunti:

* verifica del numero di host disponibili
* verifica della correttezza delle subnet
* verifica dell'assenza di conflitti

---

# Esempio sintetico di griglia di valutazione

Una versione molto compatta potrebbe essere:

1. Analisi della traccia
2. Identificazione delle reti logiche
3. Scelta dell'architettura (router / VLAN)
4. Calcolo dimensione subnet
5. Calcolo subnet mask / prefisso
6. Determinazione indirizzi di rete e broadcast
7. Piano di indirizzamento degli host
8. Coerenza complessiva
9. Chiarezza e rappresentazione

---

Di seguito una **griglia di valutazione più robusta**, organizzata esplicitamente secondo le quattro fasi cognitive tipiche della risoluzione di un esercizio di subnetting e piano di indirizzamento:

1. analisi del problema
2. progettazione della rete
3. calcolo del subnetting
4. costruzione del piano di indirizzamento

Questo schema è utile perché permette di **attribuire punteggi parziali anche quando un errore iniziale influenza i passaggi successivi**, evitando di penalizzare eccessivamente lo studente.

---

## Griglia di valutazione DETTAGLIATA – Subnetting e piano di indirizzamento IPv4 (20 punti)

| Criterio                                  | Punti max | Criteri di assegnazione                                                                                                                                                                                              |
| ----------------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Analisi della traccia                     | 2         | 2 punti: requisiti completamente identificati (numero di reti, numero host per rete, eventuali reti speciali). 1 punto: piccolo errore nella lettura dei requisiti. 0 punti: interpretazione errata della traccia.   |
| Identificazione delle reti logiche        | 3         | 3 punti: tutte le reti individuate correttamente (LAN, server, link router, ecc.). 2 punti: errore minore nel numero o nel ruolo di una rete. 1 punto: progettazione parziale. 0 punti: struttura delle reti errata. |
| Scelta dell’architettura di rete          | 2         | 2 punti: separazione corretta delle reti (router o VLAN) coerente con la traccia. 1 punto: architettura parzialmente corretta. 0 punti: architettura incoerente o assente.                                           |
| Ordinamento delle subnet (VLSM)           | 2         | 2 punti: subnet ordinate correttamente per dimensione (host maggiori → minori). 1 punto: ordinamento parzialmente corretto. 0 punti: nessun criterio di ordinamento.                                                 |
| Dimensionamento delle subnet              | 3         | 3 punti: numero di host e dimensione delle subnet corretti. 2 punti: un errore isolato. 1 punto: più errori ma metodo corretto. 0 punti: dimensionamento errato.                                                     |
| Determinazione dei prefissi / subnet mask | 3         | 3 punti: prefissi CIDR o subnet mask corretti. 2 punti: errore isolato. 1 punto: errori multipli ma metodo riconoscibile. 0 punti: prefissi errati.                                                                  |
| Calcolo degli indirizzi delle subnet      | 3         | 3 punti: indirizzi di rete e broadcast corretti. 2 punti: errore isolato. 1 punto: errori multipli ma metodo corretto. 0 punti: indirizzi errati.                                                                    |
| Costruzione del piano di indirizzamento   | 1         | 1 punto: assegnazione coerente di indirizzi a router, server e host. 0 punti: piano incoerente.                                                                                                                      |
| Verifica della coerenza del piano         | 1         | 1 punto: nessuna sovrapposizione tra subnet e rispetto della rete iniziale. 0 punti: sovrapposizioni o errori logici.                                                                                                |
| Totale                                    | 20        |                                                                                                                                                                                                                      |

---

Struttura logica della valutazione

Analisi del problema

* comprensione della traccia
* identificazione delle reti

Progettazione della rete

* architettura (router/VLAN)
* ordinamento subnet (VLSM)

Calcolo matematico

* dimensionamento subnet
* prefissi CIDR
* indirizzi network/broadcast

Applicazione operativa

* piano di indirizzamento
* verifica di coerenza

---

Vantaggi di questa griglia

Permette di valutare separatamente:

* comprensione del problema
* progettazione della rete
* capacità di calcolo
* correttezza operativa finale

Utile negli esercizi di **Sistemi e Reti**, dove spesso uno studente:

* comprende bene la rete ma sbaglia un calcolo
* oppure sa fare i calcoli ma non progetta correttamente le reti.

---  

Di seguito una **versione semplificata e molto robusta (6 criteri)** pensata per verifiche di **Sistemi e Reti per studenti 16-19 anni**.

Gli obiettivi sono:

* rendere la **correzione molto rapida**
* mantenere **equità nella valutazione**
* separare chiaramente **progettazione, calcolo e risultato**

Il totale rimane **20 punti**.

---

## Griglia di valutazione semplificata – Subnetting e piano di indirizzamento (20 punti)

| Criterio                                        | Punti max | Criteri di assegnazione                                                                                                                                                                                                             |
| ----------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Comprensione della traccia                      | 3         | 3 punti: numero di reti e host richiesti corretti. 2 punti: errore minore nella comprensione. 1 punto: comprensione parziale. 0 punti: interpretazione errata della traccia.                                                        |
| Identificazione delle sottoreti                 | 3         | 3 punti: tutte le reti individuate correttamente. 2 punti: errore minore. 1 punto: struttura parziale. 0 punti: reti non identificate.                                                                                              |
| Dimensionamento delle subnet                    | 4         | 4 punti: dimensioni delle subnet corrette per tutte le reti. 3 punti: un errore isolato. 2 punti: più errori ma metodo corretto. 1 punto: metodo parzialmente corretto. 0 punti: dimensionamento errato.                            |
| Calcolo delle subnet (CIDR, network, broadcast) | 5         | 5 punti: prefissi, network e broadcast corretti. 4 punti: errore isolato. 3 punti: alcuni errori ma metodo corretto. 2 punti: errori multipli ma procedura comprensibile. 1 punto: tentativo incompleto. 0 punti: risultato errato. |
| Piano di indirizzamento                         | 3         | 3 punti: assegnazione coerente di indirizzi a router e host. 2 punti: errori minori. 1 punto: piano parziale. 0 punti: piano incoerente.                                                                                            |
| Coerenza e chiarezza della soluzione            | 2         | 2 punti: tabella chiara e nessuna sovrapposizione tra subnet. 1 punto: soluzione comprensibile ma con imperfezioni. 0 punti: soluzione confusa o incoerente.                                                                        |
| Totale                                          | 20        |                                                                                                                                                                                                                                     |

---

Caratteristiche

* **6 criteri sono facili da ricordare**
* si corregge **in meno di un minuto per compito**
* gli studenti capiscono facilmente **dove hanno perso punti**

La struttura implicita è:

1. comprensione del problema
2. progettazione delle reti
3. calcolo del subnetting
4. piano di indirizzamento
5. verifica finale


---  


## Griglia di correzione rapida – Subnetting e piano di indirizzamento IPv4

| Criterio                                      | 0 punti                | livello intermedio    | livello buono  | livello pieno               | punti assegnati |
| --------------------------------------------- | ---------------------- | --------------------- | -------------- | --------------------------- | --------------- |
| Comprensione della traccia (3)                | interpretazione errata | comprensione parziale | piccolo errore | requisiti corretti          |                 |
| Identificazione sottoreti (3)                 | sottoreti errate       | struttura incompleta  | piccolo errore | tutte corrette              |                 |
| Dimensionamento subnet (4)                    | dimensionamento errato | metodo parziale       | un errore      | tutte corrette              |                 |
| Calcolo subnet (CIDR, network, broadcast) (5) | calcoli errati         | molti errori          | errore isolato | tutti corretti              |                 |
| Piano di indirizzamento (3)                   | piano incoerente       | piano incompleto      | errori minori  | assegnazione corretta       |                 |
| Coerenza e chiarezza (2)                      | soluzione confusa      | leggibilità parziale  | —              | soluzione chiara e coerente |                 |
| Totale                                        |                        |                       |                |                             | 20              |

---

Esempio di compilazione durante la correzione

| Criterio                  | livello scelto | punti |
| ------------------------- | -------------- | ----- |
| Comprensione traccia      | piccolo errore | 2     |
| Identificazione sottoreti | tutte corrette | 3     |
| Dimensionamento subnet    | un errore      | 3     |
| Calcolo subnet            | errore isolato | 4     |
| Piano indirizzamento      | corretto       | 3     |
| Chiarezza                 | buona          | 2     |
| Totale                    |                | 17    |

---

Vantaggi di questa griglia

* consente una **correzione molto veloce**
* riduce la soggettività della valutazione
* rende **trasparente il motivo della perdita di punti**
* è facile da **stampare e compilare a mano**


---  

## **griglia di correzione basata sulle penalità**  

Utile quando si correggono molti compiti perché permette di:

* partire dal **punteggio massimo**
* sottrarre rapidamente punti per **errori tipici**
* evitare lunghe valutazioni qualitative

Punteggio iniziale: **20 punti**

---

Griglia di correzione – metodo delle penalità

| Errore                                                    | Penalità |
| --------------------------------------------------------- | -------- |
| Interpretazione errata della traccia (numero reti o host) | −3       |
| Una sottorete mancante o non identificata                 | −2       |
| Errore nell’ordinamento delle subnet (VLSM)               | −1       |
| Dimensionamento errato di una subnet                      | −2       |
| Subnet mask o prefisso CIDR errato                        | −1       |
| Errore nel calcolo dell’indirizzo di rete                 | −2       |
| Errore nel calcolo dell’indirizzo broadcast               | −2       |
| Errore nel calcolo dell’intervallo host                   | −1       |
| Sovrapposizione tra subnet                                | −3       |
| Assegnazione errata di indirizzi a router o host          | −1       |
| Uso di indirizzo network o broadcast come host            | −2       |
| Piano di indirizzamento incompleto                        | −1       |
| Soluzione poco chiara o senza tabella                     | −1       |

---

Vantaggi 

* estremamente **veloce**
* molto **oggettivo**
* facile da usare quando si correggono **20–30 compiti**


Limitazioni

Questo metodo funziona meglio quando:

* gli esercizi sono **molto standardizzati**
* la soluzione è **abbastanza strutturata**


---

# Struttura consigliata della risposta dello studente

Per facilitare la correzione è utile richiedere sempre una tabella finale come questa.

| Rete        | Prefisso | Subnet mask     | Network | Primo host | Ultimo host | Broadcast |
| ----------- | -------- | --------------- | ------- | ---------- | ----------- | --------- |
| LAN1        | /26      | 255.255.255.192 | …       | …          | …           | …         |
| LAN2        | /27      | 255.255.255.224 | …       | …          | …           | …         |
| Link router | /30      | 255.255.255.252 | …       | …          | …           | …         |


---

# A. 20 esercizi – Indirizzi Classful

1. Data la rete 10.0.0.0, determinare classe, mask di default, numero host disponibili.
2. La rete 172.16.0.0 appartiene a quale classe? Quanti host totali consente?
3. Determinare se 192.168.5.10 è classe A, B o C e indicare la mask di default.
4. Calcolare numero reti e host nella classe B.
5. Data la rete 130.25.0.0, indicare classe e numero host per rete.
6. Verificare se 200.10.5.0 è rete pubblica di classe C.
7. Determinare intervallo indirizzi validi per rete 192.168.1.0 classful.
8. Per 15.0.0.0 indicare classe e numero massimo di host.
9. Per 180.20.0.0 indicare broadcast classful.
10. Identificare la classe di 126.10.1.1.
11. Identificare la classe di 191.255.1.1.
12. Identificare la classe di 223.0.0.1.
13. Quanti host utilizzabili in 172.20.0.0 classful?
14. Quanti bit host in classe C?
15. Data 150.10.10.10 indicare rete classful.
16. Data 192.10.10.10 indicare rete classful.
17. Data 11.5.6.7 indicare rete classful.
18. Determinare se 224.0.0.1 è classe A, B o C.
19. Spiegare perché 127.0.0.1 non è usabile come rete normale.
20. Data la rete 12.0.0.0, determinare classe, mask di default, numero host disponibili.

---

# B. 20 esercizi – CIDR

1. Data 192.168.10.0/26 determinare host utilizzabili.
2. Data 192.168.10.0/27 determinare broadcast.
3. Data 10.0.0.0/12 determinare numero reti possibili rispetto classful.
4. Data 172.16.0.0/20 determinare range completo.
5. Data 192.168.1.64/26 determinare primo e ultimo host.
6. Data 192.168.1.128/25 determinare broadcast.
7. Data 10.10.10.0/30 determinare host utilizzabili.
8. Data 192.168.5.0/29 determinare numero sottoreti in una /24.
9. Data 172.16.0.0/22 determinare numero host per sottorete.
10. Data 192.168.1.0/28 determinare numero host.
11. Data 192.168.1.16/28 determinare intervallo.
12. Data 192.168.1.0/23 determinare totale host.
13. Data 10.0.0.0/8 suddividere in /16: quante sottoreti?
14. Data 172.16.0.0/24 rispetto a classful cosa cambia?
15. Data 192.168.1.0/30 quanti host?
16. Data 192.168.1.4/30 determinare broadcast.
17. Data 192.168.100.0/21 determinare intervallo.
18. Data 10.0.0.0/18 determinare host per rete.
19. Data 172.16.0.0/26 determinare numero sottoreti in una /24.
20. Data 192.168.0.0/19 determinare host totali.

---

# C. 20 esercizi – VLSM (piani di indirizzamento)

1. Progettare piano per rete 192.168.10.0/24 con: 60 host, 30 host, 10 host.
2. Progettare piano per 10.0.0.0/24 con: 100 host, 50 host, 20 host.
3. Progettare piano per 172.16.0.0/24 con 4 reti da 50 host.
4. Progettare rete 192.168.1.0/24 con: 120 host, 60 host, 30 host.
5. Progettare rete 10.0.0.0/23 con: 200 host, 100 host, 50 host, 20 host.
6. Rete 192.168.0.0/24 con: 80 host, 40 host, 20 host, 10 host.
7. Rete 172.16.10.0/24 con: 70 host, 30 host, 10 host.
8. Rete 192.168.5.0/24 con: 2 link punto-punto (/30) e 1 LAN da 100 host.
9. Rete 10.1.0.0/24 con: 120 host, 60 host, 60 host.
10. Rete 192.168.50.0/24 con: 90 host, 40 host, 20 host.
11. Rete 172.20.0.0/24 con: 4 reti da 30 host.
12. Rete 10.0.10.0/24 con: 200 host, 20 host.
13. Rete 192.168.200.0/24 con: 100 host, 50 host, 25 host, 10 host.
14. Rete 172.16.5.0/24 con: 3 reti da 60 host.
15. Rete 10.10.0.0/24 con: 120 host, 30 host, 30 host, 10 host.
16. Rete 192.168.0.0/23 con: 300 host, 100 host, 50 host.
17. Rete 172.16.0.0/23 con: 200 host, 60 host, 60 host.
18. Rete 10.0.0.0/22 con: 500 host, 200 host, 100 host.
19. Rete 192.168.100.0/24 con: 150 host, 50 host, 20 host.
20. Rete 172.16.100.0/24 con: 100 host, 30 host, 10 host, 2 link p2p.

---

## A. SOLUZIONI – INDIRIZZI CLASSFUL

A1) Data la rete 10.0.0.0, determinare classe, mask di default, numero host disponibili.

| Rete     | Subnet mask | Router | Server | Host                                                                 | Broadcast      |
| -------- | ----------- | ------ | ------ | -------------------------------------------------------------------- | -------------- |
| 10.0.0.0 | 255.0.0.0   | N/D    | N/D    | da 10.0.0.1 a 10.255.255.254 ; Classe=A ; host_utilizzabili=16777214 | 10.255.255.255 |

A2) La rete 172.16.0.0 appartiene a quale classe? Quanti host totali consente?

| Rete       | Subnet mask | Router | Server | Host                                                                | Broadcast      |
| ---------- | ----------- | ------ | ------ | ------------------------------------------------------------------- | -------------- |
| 172.16.0.0 | 255.255.0.0 | N/D    | N/D    | da 172.16.0.1 a 172.16.255.254 ; Classe=B ; host_utilizzabili=65534 | 172.16.255.255 |

A3) Determinare se 192.168.5.10 è classe A, B o C e indicare la mask di default.

| Rete        | Subnet mask   | Router | Server | Host                                                                                        | Broadcast     |
| ----------- | ------------- | ------ | ------ | ------------------------------------------------------------------------------------------- | ------------- |
| 192.168.5.0 | 255.255.255.0 | N/D    | N/D    | da 192.168.5.1 a 192.168.5.254 ; Classe=C ; host_utilizzabili=254 ; IP_esempio=192.168.5.10 | 192.168.5.255 |

A4) Calcolare numero reti e host nella classe B.

| Rete      | Subnet mask | Router | Server | Host                                                                                                              | Broadcast     |
| --------- | ----------- | ------ | ------ | ----------------------------------------------------------------------------------------------------------------- | ------------- |
| 128.0.0.0 | 255.255.0.0 | N/D    | N/D    | da 128.0.0.1 a 128.0.255.254 ; Classe=B ; host_utilizzabili=65534 ; in classe B: 16384 reti ; 65534 host per rete | 128.0.255.255 |

A5) Data la rete 130.25.0.0, indicare classe e numero host per rete.

| Rete       | Subnet mask | Router | Server | Host                                                                | Broadcast      |
| ---------- | ----------- | ------ | ------ | ------------------------------------------------------------------- | -------------- |
| 130.25.0.0 | 255.255.0.0 | N/D    | N/D    | da 130.25.0.1 a 130.25.255.254 ; Classe=B ; host_utilizzabili=65534 | 130.25.255.255 |

A6) Verificare se 200.10.5.0 è rete pubblica di classe C.

| Rete       | Subnet mask   | Router | Server | Host                                                                                                    | Broadcast    |
| ---------- | ------------- | ------ | ------ | ------------------------------------------------------------------------------------------------------- | ------------ |
| 200.10.5.0 | 255.255.255.0 | N/D    | N/D    | da 200.10.5.1 a 200.10.5.254 ; Classe=C ; host_utilizzabili=254 ; non è in range privati: rete pubblica | 200.10.5.255 |

A7) Determinare intervallo indirizzi validi per rete 192.168.1.0 classful.

| Rete        | Subnet mask   | Router | Server | Host                                                              | Broadcast     |
| ----------- | ------------- | ------ | ------ | ----------------------------------------------------------------- | ------------- |
| 192.168.1.0 | 255.255.255.0 | N/D    | N/D    | da 192.168.1.1 a 192.168.1.254 ; Classe=C ; host_utilizzabili=254 | 192.168.1.255 |

A8) Per 15.0.0.0 indicare classe e numero massimo di host.

| Rete     | Subnet mask | Router | Server | Host                                                                 | Broadcast      |
| -------- | ----------- | ------ | ------ | -------------------------------------------------------------------- | -------------- |
| 15.0.0.0 | 255.0.0.0   | N/D    | N/D    | da 15.0.0.1 a 15.255.255.254 ; Classe=A ; host_utilizzabili=16777214 | 15.255.255.255 |

A9) Per 180.20.0.0 indicare broadcast classful.

| Rete       | Subnet mask | Router | Server | Host                                                                | Broadcast      |
| ---------- | ----------- | ------ | ------ | ------------------------------------------------------------------- | -------------- |
| 180.20.0.0 | 255.255.0.0 | N/D    | N/D    | da 180.20.0.1 a 180.20.255.254 ; Classe=B ; host_utilizzabili=65534 | 180.20.255.255 |

A10) Identificare la classe di 126.10.1.1.

| Rete      | Subnet mask | Router | Server | Host                                                                                           | Broadcast       |
| --------- | ----------- | ------ | ------ | ---------------------------------------------------------------------------------------------- | --------------- |
| 126.0.0.0 | 255.0.0.0   | N/D    | N/D    | da 126.0.0.1 a 126.255.255.254 ; Classe=A ; host_utilizzabili=16777214 ; IP_esempio=126.10.1.1 | 126.255.255.255 |

A11) Identificare la classe di 191.255.1.1.

| Rete        | Subnet mask | Router | Server | Host                                                                                           | Broadcast       |
| ----------- | ----------- | ------ | ------ | ---------------------------------------------------------------------------------------------- | --------------- |
| 191.255.0.0 | 255.255.0.0 | N/D    | N/D    | da 191.255.0.1 a 191.255.255.254 ; Classe=B ; host_utilizzabili=65534 ; IP_esempio=191.255.1.1 | 191.255.255.255 |

A12) Identificare la classe di 223.0.0.1.

| Rete      | Subnet mask   | Router | Server | Host                                                                                 | Broadcast   |
| --------- | ------------- | ------ | ------ | ------------------------------------------------------------------------------------ | ----------- |
| 223.0.0.0 | 255.255.255.0 | N/D    | N/D    | da 223.0.0.1 a 223.0.0.254 ; Classe=C ; host_utilizzabili=254 ; IP_esempio=223.0.0.1 | 223.0.0.255 |

A13) Quanti host utilizzabili in 172.20.0.0 classful?

| Rete       | Subnet mask | Router | Server | Host                                                                | Broadcast      |
| ---------- | ----------- | ------ | ------ | ------------------------------------------------------------------- | -------------- |
| 172.20.0.0 | 255.255.0.0 | N/D    | N/D    | da 172.20.0.1 a 172.20.255.254 ; Classe=B ; host_utilizzabili=65534 | 172.20.255.255 |

A14) Quanti bit host in classe C?

| Rete      | Subnet mask   | Router | Server | Host                                                                                    | Broadcast   |
| --------- | ------------- | ------ | ------ | --------------------------------------------------------------------------------------- | ----------- |
| 192.0.0.0 | 255.255.255.0 | N/D    | N/D    | da 192.0.0.1 a 192.0.0.254 ; Classe=C ; host_utilizzabili=254 ; in classe C: 8 bit host | 192.0.0.255 |

A15) Data 150.10.10.10 indicare rete classful.

| Rete       | Subnet mask | Router | Server | Host                                                                                          | Broadcast      |
| ---------- | ----------- | ------ | ------ | --------------------------------------------------------------------------------------------- | -------------- |
| 150.10.0.0 | 255.255.0.0 | N/D    | N/D    | da 150.10.0.1 a 150.10.255.254 ; Classe=B ; host_utilizzabili=65534 ; IP_esempio=150.10.10.10 | 150.10.255.255 |

A16) Data 192.10.10.10 indicare rete classful.

| Rete        | Subnet mask   | Router | Server | Host                                                                                        | Broadcast     |
| ----------- | ------------- | ------ | ------ | ------------------------------------------------------------------------------------------- | ------------- |
| 192.10.10.0 | 255.255.255.0 | N/D    | N/D    | da 192.10.10.1 a 192.10.10.254 ; Classe=C ; host_utilizzabili=254 ; IP_esempio=192.10.10.10 | 192.10.10.255 |

A17) Data 11.5.6.7 indicare rete classful.

| Rete     | Subnet mask | Router | Server | Host                                                                                       | Broadcast      |
| -------- | ----------- | ------ | ------ | ------------------------------------------------------------------------------------------ | -------------- |
| 11.0.0.0 | 255.0.0.0   | N/D    | N/D    | da 11.0.0.1 a 11.255.255.254 ; Classe=A ; host_utilizzabili=16777214 ; IP_esempio=11.5.6.7 | 11.255.255.255 |

A18) Determinare se 224.0.0.1 è classe A, B o C.

| Rete      | Subnet mask | Router | Server | Host                                                          | Broadcast |
| --------- | ----------- | ------ | ------ | ------------------------------------------------------------- | --------- |
| 224.0.0.1 | N/D         | N/D    | N/D    | Classe=D (multicast) ; subnetting non applicabile in classful | N/D       |

A19) Spiegare suggerendo la motivazione perché 127.0.0.1 non è usabile come rete normale.

| Rete      | Subnet mask | Router | Server | Host                                                           | Broadcast |
| --------- | ----------- | ------ | ------ | -------------------------------------------------------------- | --------- |
| 127.0.0.1 | 255.0.0.0   | N/D    | N/D    | Classe=A (127/8) ; riservato loopback, non assegnabile in rete | N/D       |

A20) Data la rete 12.0.0.0, determinare classe, mask di default, numero host disponibili.

| Rete     | Subnet mask | Router | Server | Host                                                                 | Broadcast      |
| -------- | ----------- | ------ | ------ | -------------------------------------------------------------------- | -------------- |
| 12.0.0.0 | 255.0.0.0   | N/D    | N/D    | da 12.0.0.1 a 12.255.255.254 ; Classe=A ; host_utilizzabili=16777214 | 12.255.255.255 |

---

## B. SOLUZIONI – CIDR

B1) Data 192.168.10.0/26 determinare host utilizzabili.

| Rete         | Subnet mask     | Router | Server | Host                                                   | Broadcast     |
| ------------ | --------------- | ------ | ------ | ------------------------------------------------------ | ------------- |
| 192.168.10.0 | 255.255.255.192 | N/D    | N/D    | da 192.168.10.1 a 192.168.10.62 ; host_utilizzabili=62 | 192.168.10.63 |

B2) Data 192.168.10.0/27 determinare broadcast.

| Rete         | Subnet mask     | Router | Server | Host                                                   | Broadcast     |
| ------------ | --------------- | ------ | ------ | ------------------------------------------------------ | ------------- |
| 192.168.10.0 | 255.255.255.224 | N/D    | N/D    | da 192.168.10.1 a 192.168.10.30 ; host_utilizzabili=30 | 192.168.10.31 |

B3) Data 10.0.0.0/12 determinare numero reti possibili rispetto classful.

| Rete     | Subnet mask | Router | Server | Host                                                                                      | Broadcast     |
| -------- | ----------- | ------ | ------ | ----------------------------------------------------------------------------------------- | ------------- |
| 10.0.0.0 | 255.240.0.0 | N/D    | N/D    | da 10.0.0.1 a 10.15.255.254 ; host_utilizzabili=1048574 ; in 10.0.0.0/8: 16 sottoreti /12 | 10.15.255.255 |

B4) Data 172.16.0.0/20 determinare range completo.

| Rete       | Subnet mask   | Router | Server | Host                                                   | Broadcast     |
| ---------- | ------------- | ------ | ------ | ------------------------------------------------------ | ------------- |
| 172.16.0.0 | 255.255.240.0 | N/D    | N/D    | da 172.16.0.1 a 172.16.15.254 ; host_utilizzabili=4094 | 172.16.15.255 |

B5) Data 192.168.1.64/26 determinare primo e ultimo host.

| Rete         | Subnet mask     | Router | Server | Host                                                   | Broadcast     |
| ------------ | --------------- | ------ | ------ | ------------------------------------------------------ | ------------- |
| 192.168.1.64 | 255.255.255.192 | N/D    | N/D    | da 192.168.1.65 a 192.168.1.126 ; host_utilizzabili=62 | 192.168.1.127 |

B6) Data 192.168.1.128/25 determinare broadcast.

| Rete          | Subnet mask     | Router | Server | Host                                                     | Broadcast     |
| ------------- | --------------- | ------ | ------ | -------------------------------------------------------- | ------------- |
| 192.168.1.128 | 255.255.255.128 | N/D    | N/D    | da 192.168.1.129 a 192.168.1.254 ; host_utilizzabili=126 | 192.168.1.255 |

B7) Data 10.10.10.0/30 determinare host utilizzabili.

| Rete       | Subnet mask     | Router | Server | Host                                             | Broadcast  |
| ---------- | --------------- | ------ | ------ | ------------------------------------------------ | ---------- |
| 10.10.10.0 | 255.255.255.252 | N/D    | N/D    | da 10.10.10.1 a 10.10.10.2 ; host_utilizzabili=2 | 10.10.10.3 |

B8) Data 192.168.5.0/29 determinare numero sottoreti in una /24.

| Rete        | Subnet mask     | Router | Server | Host                                                                              | Broadcast   |
| ----------- | --------------- | ------ | ------ | --------------------------------------------------------------------------------- | ----------- |
| 192.168.5.0 | 255.255.255.248 | N/D    | N/D    | da 192.168.5.1 a 192.168.5.6 ; host_utilizzabili=6 ; in una /24: 32 sottoreti /29 | 192.168.5.7 |

B9) Data 172.16.0.0/22 determinare numero host per sottorete.

| Rete       | Subnet mask   | Router | Server | Host                                                  | Broadcast    |
| ---------- | ------------- | ------ | ------ | ----------------------------------------------------- | ------------ |
| 172.16.0.0 | 255.255.252.0 | N/D    | N/D    | da 172.16.0.1 a 172.16.3.254 ; host_utilizzabili=1022 | 172.16.3.255 |

B10) Data 192.168.1.0/28 determinare numero host.

| Rete        | Subnet mask     | Router | Server | Host                                                 | Broadcast    |
| ----------- | --------------- | ------ | ------ | ---------------------------------------------------- | ------------ |
| 192.168.1.0 | 255.255.255.240 | N/D    | N/D    | da 192.168.1.1 a 192.168.1.14 ; host_utilizzabili=14 | 192.168.1.15 |

B11) Data 192.168.1.16/28 determinare intervallo.

| Rete         | Subnet mask     | Router | Server | Host                                                  | Broadcast    |
| ------------ | --------------- | ------ | ------ | ----------------------------------------------------- | ------------ |
| 192.168.1.16 | 255.255.255.240 | N/D    | N/D    | da 192.168.1.17 a 192.168.1.30 ; host_utilizzabili=14 | 192.168.1.31 |

B12) Data 192.168.1.0/23 determinare totale host.

| Rete        | Subnet mask   | Router | Server | Host                                                                                                                          | Broadcast     |
| ----------- | ------------- | ------ | ------ | ----------------------------------------------------------------------------------------------------------------------------- | ------------- |
| 192.168.0.0 | 255.255.254.0 | N/D    | N/D    | da 192.168.0.1 a 192.168.1.254 ; host_utilizzabili=510 ; nota: per /23 la rete correttamente allineata sarebbe 192.168.0.0/23 | 192.168.1.255 |

B13) Data 10.0.0.0/8 suddividere in /16: quante sottoreti?

| Rete     | Subnet mask | Router | Server | Host                                                                                                                         | Broadcast      |
| -------- | ----------- | ------ | ------ | ---------------------------------------------------------------------------------------------------------------------------- | -------------- |
| 10.0.0.0 | 255.0.0.0   | N/D    | N/D    | da 10.0.0.1 a 10.255.255.254 ; host_utilizzabili=16777214 ; suddivisione in /16: 256 sottoreti ; 65534 host per ciascuna /16 | 10.255.255.255 |

B14) Data 172.16.0.0/24 rispetto a classful cosa cambia?

| Rete       | Subnet mask   | Router | Server | Host                                                                                                                                             | Broadcast    |
| ---------- | ------------- | ------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| 172.16.0.0 | 255.255.255.0 | N/D    | N/D    | da 172.16.0.1 a 172.16.0.254 ; host_utilizzabili=254 ; rispetto a classful (B=/16): è una sottorete più piccola ; in 172.16.0.0/16: 256 reti /24 | 172.16.0.255 |

B15) Data 192.168.1.0/30 quanti host?

| Rete        | Subnet mask     | Router | Server | Host                                               | Broadcast   |
| ----------- | --------------- | ------ | ------ | -------------------------------------------------- | ----------- |
| 192.168.1.0 | 255.255.255.252 | N/D    | N/D    | da 192.168.1.1 a 192.168.1.2 ; host_utilizzabili=2 | 192.168.1.3 |

B16) Data 192.168.1.4/30 determinare broadcast.

| Rete        | Subnet mask     | Router | Server | Host                                               | Broadcast   |
| ----------- | --------------- | ------ | ------ | -------------------------------------------------- | ----------- |
| 192.168.1.4 | 255.255.255.252 | N/D    | N/D    | da 192.168.1.5 a 192.168.1.6 ; host_utilizzabili=2 | 192.168.1.7 |

B17) Data 192.168.100.0/21 determinare intervallo.

| Rete         | Subnet mask   | Router | Server | Host                                                                                                            | Broadcast       |
| ------------ | ------------- | ------ | ------ | --------------------------------------------------------------------------------------------------------------- | --------------- |
| 192.168.96.0 | 255.255.248.0 | N/D    | N/D    | da 192.168.96.1 a 192.168.103.254 ; host_utilizzabili=2046 ; rete effettiva (allineamento /21): 192.168.96.0/21 | 192.168.103.255 |

B18) Data 10.0.0.0/18 determinare host per rete.

| Rete     | Subnet mask   | Router | Server | Host                                                | Broadcast   |
| -------- | ------------- | ------ | ------ | --------------------------------------------------- | ----------- |
| 10.0.0.0 | 255.255.192.0 | N/D    | N/D    | da 10.0.0.1 a 10.0.63.254 ; host_utilizzabili=16382 | 10.0.63.255 |

B19) Data 172.16.0.0/26 determinare numero sottoreti in una /24.

| Rete       | Subnet mask     | Router | Server | Host                                                                             | Broadcast   |
| ---------- | --------------- | ------ | ------ | -------------------------------------------------------------------------------- | ----------- |
| 172.16.0.0 | 255.255.255.192 | N/D    | N/D    | da 172.16.0.1 a 172.16.0.62 ; host_utilizzabili=62 ; in una /24: 4 sottoreti /26 | 172.16.0.63 |

B20) Data 192.168.0.0/19 determinare host totali.

| Rete        | Subnet mask   | Router | Server | Host                                                     | Broadcast      |
| ----------- | ------------- | ------ | ------ | -------------------------------------------------------- | -------------- |
| 192.168.0.0 | 255.255.224.0 | N/D    | N/D    | da 192.168.0.1 a 192.168.31.254 ; host_utilizzabili=8190 | 192.168.31.255 |

---

## C. SOLUZIONI – VLSM (piani di indirizzamento)

C1) Progettare piano per rete 192.168.10.0/24 con: 60 host, 30 host, 10 host.

| Rete          | Subnet mask     | Router         | Server        | Host                                                              | Broadcast      |
| ------------- | --------------- | -------------- | ------------- | ----------------------------------------------------------------- | -------------- |
| 192.168.10.0  | 255.255.255.192 | 192.168.10.62  | 192.168.10.1  | da 192.168.10.2 a 192.168.10.61 ; LAN_60 ; host_utilizzabili=62   | 192.168.10.63  |
| 192.168.10.64 | 255.255.255.224 | 192.168.10.94  | 192.168.10.65 | da 192.168.10.66 a 192.168.10.93 ; LAN_30 ; host_utilizzabili=30  | 192.168.10.95  |
| 192.168.10.96 | 255.255.255.240 | 192.168.10.110 | 192.168.10.97 | da 192.168.10.98 a 192.168.10.109 ; LAN_10 ; host_utilizzabili=14 | 192.168.10.111 |

C2) Progettare piano per 10.0.0.0/24 con: 100 host, 50 host, 20 host.

| Rete       | Subnet mask     | Router     | Server     | Host                                                       | Broadcast  |
| ---------- | --------------- | ---------- | ---------- | ---------------------------------------------------------- | ---------- |
| 10.0.0.0   | 255.255.255.128 | 10.0.0.126 | 10.0.0.1   | da 10.0.0.2 a 10.0.0.125 ; LAN_100 ; host_utilizzabili=126 | 10.0.0.127 |
| 10.0.0.128 | 255.255.255.192 | 10.0.0.190 | 10.0.0.129 | da 10.0.0.130 a 10.0.0.189 ; LAN_50 ; host_utilizzabili=62 | 10.0.0.191 |
| 10.0.0.192 | 255.255.255.224 | 10.0.0.222 | 10.0.0.193 | da 10.0.0.194 a 10.0.0.221 ; LAN_20 ; host_utilizzabili=30 | 10.0.0.223 |

C3) Progettare piano per 172.16.0.0/24 con 4 reti da 50 host.

| Rete         | Subnet mask     | Router       | Server       | Host                                                             | Broadcast    |
| ------------ | --------------- | ------------ | ------------ | ---------------------------------------------------------------- | ------------ |
| 172.16.0.0   | 255.255.255.192 | 172.16.0.62  | 172.16.0.1   | da 172.16.0.2 a 172.16.0.61 ; LAN_50_1 ; host_utilizzabili=62    | 172.16.0.63  |
| 172.16.0.64  | 255.255.255.192 | 172.16.0.126 | 172.16.0.65  | da 172.16.0.66 a 172.16.0.125 ; LAN_50_2 ; host_utilizzabili=62  | 172.16.0.127 |
| 172.16.0.128 | 255.255.255.192 | 172.16.0.190 | 172.16.0.129 | da 172.16.0.130 a 172.16.0.189 ; LAN_50_3 ; host_utilizzabili=62 | 172.16.0.191 |
| 172.16.0.192 | 255.255.255.192 | 172.16.0.254 | 172.16.0.193 | da 172.16.0.194 a 172.16.0.253 ; LAN_50_4 ; host_utilizzabili=62 | 172.16.0.255 |

C4) Progettare rete 192.168.1.0/24 con: 120 host, 60 host, 30 host.

| Rete          | Subnet mask     | Router        | Server        | Host                                                             | Broadcast     |
| ------------- | --------------- | ------------- | ------------- | ---------------------------------------------------------------- | ------------- |
| 192.168.1.0   | 255.255.255.128 | 192.168.1.126 | 192.168.1.1   | da 192.168.1.2 a 192.168.1.125 ; LAN_120 ; host_utilizzabili=126 | 192.168.1.127 |
| 192.168.1.128 | 255.255.255.192 | 192.168.1.190 | 192.168.1.129 | da 192.168.1.130 a 192.168.1.189 ; LAN_60 ; host_utilizzabili=62 | 192.168.1.191 |
| 192.168.1.192 | 255.255.255.224 | 192.168.1.222 | 192.168.1.193 | da 192.168.1.194 a 192.168.1.221 ; LAN_30 ; host_utilizzabili=30 | 192.168.1.223 |

C5) Progettare rete 10.0.0.0/23 con: 200 host, 100 host, 50 host, 20 host.

| Rete       | Subnet mask     | Router     | Server     | Host                                                       | Broadcast  |
| ---------- | --------------- | ---------- | ---------- | ---------------------------------------------------------- | ---------- |
| 10.0.0.0   | 255.255.255.0   | 10.0.0.254 | 10.0.0.1   | da 10.0.0.2 a 10.0.0.253 ; LAN_200 ; host_utilizzabili=254 | 10.0.0.255 |
| 10.0.1.0   | 255.255.255.128 | 10.0.1.126 | 10.0.1.1   | da 10.0.1.2 a 10.0.1.125 ; LAN_100 ; host_utilizzabili=126 | 10.0.1.127 |
| 10.0.1.128 | 255.255.255.192 | 10.0.1.190 | 10.0.1.129 | da 10.0.1.130 a 10.0.1.189 ; LAN_50 ; host_utilizzabili=62 | 10.0.1.191 |
| 10.0.1.192 | 255.255.255.224 | 10.0.1.222 | 10.0.1.193 | da 10.0.1.194 a 10.0.1.221 ; LAN_20 ; host_utilizzabili=30 | 10.0.1.223 |

C6) Rete 192.168.0.0/24 con: 80 host, 40 host, 20 host, 10 host.

| Rete          | Subnet mask     | Router        | Server        | Host                                                             | Broadcast     |
| ------------- | --------------- | ------------- | ------------- | ---------------------------------------------------------------- | ------------- |
| 192.168.0.0   | 255.255.255.128 | 192.168.0.126 | 192.168.0.1   | da 192.168.0.2 a 192.168.0.125 ; LAN_80 ; host_utilizzabili=126  | 192.168.0.127 |
| 192.168.0.128 | 255.255.255.192 | 192.168.0.190 | 192.168.0.129 | da 192.168.0.130 a 192.168.0.189 ; LAN_40 ; host_utilizzabili=62 | 192.168.0.191 |
| 192.168.0.192 | 255.255.255.224 | 192.168.0.222 | 192.168.0.193 | da 192.168.0.194 a 192.168.0.221 ; LAN_20 ; host_utilizzabili=30 | 192.168.0.223 |
| 192.168.0.224 | 255.255.255.240 | 192.168.0.238 | 192.168.0.225 | da 192.168.0.226 a 192.168.0.237 ; LAN_10 ; host_utilizzabili=14 | 192.168.0.239 |

C7) Rete 172.16.10.0/24 con: 70 host, 30 host, 10 host.

| Rete          | Subnet mask     | Router        | Server        | Host                                                             | Broadcast     |
| ------------- | --------------- | ------------- | ------------- | ---------------------------------------------------------------- | ------------- |
| 172.16.10.0   | 255.255.255.128 | 172.16.10.126 | 172.16.10.1   | da 172.16.10.2 a 172.16.10.125 ; LAN_70 ; host_utilizzabili=126  | 172.16.10.127 |
| 172.16.10.128 | 255.255.255.224 | 172.16.10.158 | 172.16.10.129 | da 172.16.10.130 a 172.16.10.157 ; LAN_30 ; host_utilizzabili=30 | 172.16.10.159 |
| 172.16.10.160 | 255.255.255.240 | 172.16.10.174 | 172.16.10.161 | da 172.16.10.162 a 172.16.10.173 ; LAN_10 ; host_utilizzabili=14 | 172.16.10.175 |

C8) Rete 192.168.5.0/24 con: 2 link punto-punto (/30) e 1 LAN da 100 host.

| Rete          | Subnet mask     | Router        | Server      | Host                                                             | Broadcast     |
| ------------- | --------------- | ------------- | ----------- | ---------------------------------------------------------------- | ------------- |
| 192.168.5.0   | 255.255.255.128 | 192.168.5.126 | 192.168.5.1 | da 192.168.5.2 a 192.168.5.125 ; LAN_100 ; host_utilizzabili=126 | 192.168.5.127 |
| 192.168.5.128 | 255.255.255.252 | N/D           | N/D         | da 192.168.5.129 a 192.168.5.130 ; P2P_1 ; host_utilizzabili=2   | 192.168.5.131 |
| 192.168.5.132 | 255.255.255.252 | N/D           | N/D         | da 192.168.5.133 a 192.168.5.134 ; P2P_2 ; host_utilizzabili=2   | 192.168.5.135 |

C9) Rete 10.1.0.0/24 con: 120 host, 60 host, 60 host.

| Rete       | Subnet mask     | Router     | Server     | Host                                                         | Broadcast  |
| ---------- | --------------- | ---------- | ---------- | ------------------------------------------------------------ | ---------- |
| 10.1.0.0   | 255.255.255.128 | 10.1.0.126 | 10.1.0.1   | da 10.1.0.2 a 10.1.0.125 ; LAN_120 ; host_utilizzabili=126   | 10.1.0.127 |
| 10.1.0.128 | 255.255.255.192 | 10.1.0.190 | 10.1.0.129 | da 10.1.0.130 a 10.1.0.189 ; LAN_60_1 ; host_utilizzabili=62 | 10.1.0.191 |
| 10.1.0.192 | 255.255.255.192 | 10.1.0.254 | 10.1.0.193 | da 10.1.0.194 a 10.1.0.253 ; LAN_60_2 ; host_utilizzabili=62 | 10.1.0.255 |

C10) Rete 192.168.50.0/24 con: 90 host, 40 host, 20 host.

| Rete           | Subnet mask     | Router         | Server         | Host                                                               | Broadcast      |
| -------------- | --------------- | -------------- | -------------- | ------------------------------------------------------------------ | -------------- |
| 192.168.50.0   | 255.255.255.128 | 192.168.50.126 | 192.168.50.1   | da 192.168.50.2 a 192.168.50.125 ; LAN_90 ; host_utilizzabili=126  | 192.168.50.127 |
| 192.168.50.128 | 255.255.255.192 | 192.168.50.190 | 192.168.50.129 | da 192.168.50.130 a 192.168.50.189 ; LAN_40 ; host_utilizzabili=62 | 192.168.50.191 |
| 192.168.50.192 | 255.255.255.224 | 192.168.50.222 | 192.168.50.193 | da 192.168.50.194 a 192.168.50.221 ; LAN_20 ; host_utilizzabili=30 | 192.168.50.223 |

C11) Rete 172.20.0.0/24 con: 4 reti da 30 host.

| Rete        | Subnet mask     | Router       | Server      | Host                                                            | Broadcast    |
| ----------- | --------------- | ------------ | ----------- | --------------------------------------------------------------- | ------------ |
| 172.20.0.0  | 255.255.255.224 | 172.20.0.30  | 172.20.0.1  | da 172.20.0.2 a 172.20.0.29 ; LAN_30_1 ; host_utilizzabili=30   | 172.20.0.31  |
| 172.20.0.32 | 255.255.255.224 | 172.20.0.62  | 172.20.0.33 | da 172.20.0.34 a 172.20.0.61 ; LAN_30_2 ; host_utilizzabili=30  | 172.20.0.63  |
| 172.20.0.64 | 255.255.255.224 | 172.20.0.94  | 172.20.0.65 | da 172.20.0.66 a 172.20.0.93 ; LAN_30_3 ; host_utilizzabili=30  | 172.20.0.95  |
| 172.20.0.96 | 255.255.255.224 | 172.20.0.126 | 172.20.0.97 | da 172.20.0.98 a 172.20.0.125 ; LAN_30_4 ; host_utilizzabili=30 | 172.20.0.127 |

C12) Rete 10.0.10.0/24 con: 200 host, 20 host.

Impossibile soddisfare i requisiti usando la rete di partenza indicata, perché la sottorete necessaria per la richiesta più grande esaurisce lo spazio disponibile.
Rete minima consigliata per rendere possibile l’esercizio: 10.0.10.0/23

| Rete      | Subnet mask     | Router      | Server    | Host                                                         | Broadcast   |
| --------- | --------------- | ----------- | --------- | ------------------------------------------------------------ | ----------- |
| 10.0.10.0 | 255.255.255.0   | 10.0.10.254 | 10.0.10.1 | da 10.0.10.2 a 10.0.10.253 ; LAN_200 ; host_utilizzabili=254 | 10.0.10.255 |
| 10.0.11.0 | 255.255.255.224 | 10.0.11.30  | 10.0.11.1 | da 10.0.11.2 a 10.0.11.29 ; LAN_20 ; host_utilizzabili=30    | 10.0.11.31  |

C13) Rete 192.168.200.0/24 con: 100 host, 50 host, 25 host, 10 host.

| Rete            | Subnet mask     | Router          | Server          | Host                                                                 | Broadcast       |
| --------------- | --------------- | --------------- | --------------- | -------------------------------------------------------------------- | --------------- |
| 192.168.200.0   | 255.255.255.128 | 192.168.200.126 | 192.168.200.1   | da 192.168.200.2 a 192.168.200.125 ; LAN_100 ; host_utilizzabili=126 | 192.168.200.127 |
| 192.168.200.128 | 255.255.255.192 | 192.168.200.190 | 192.168.200.129 | da 192.168.200.130 a 192.168.200.189 ; LAN_50 ; host_utilizzabili=62 | 192.168.200.191 |
| 192.168.200.192 | 255.255.255.224 | 192.168.200.222 | 192.168.200.193 | da 192.168.200.194 a 192.168.200.221 ; LAN_25 ; host_utilizzabili=30 | 192.168.200.223 |
| 192.168.200.224 | 255.255.255.240 | 192.168.200.238 | 192.168.200.225 | da 192.168.200.226 a 192.168.200.237 ; LAN_10 ; host_utilizzabili=14 | 192.168.200.239 |

C14) Rete 172.16.5.0/24 con: 3 reti da 60 host.

| Rete         | Subnet mask     | Router       | Server       | Host                                                             | Broadcast    |
| ------------ | --------------- | ------------ | ------------ | ---------------------------------------------------------------- | ------------ |
| 172.16.5.0   | 255.255.255.192 | 172.16.5.62  | 172.16.5.1   | da 172.16.5.2 a 172.16.5.61 ; LAN_60_1 ; host_utilizzabili=62    | 172.16.5.63  |
| 172.16.5.64  | 255.255.255.192 | 172.16.5.126 | 172.16.5.65  | da 172.16.5.66 a 172.16.5.125 ; LAN_60_2 ; host_utilizzabili=62  | 172.16.5.127 |
| 172.16.5.128 | 255.255.255.192 | 172.16.5.190 | 172.16.5.129 | da 172.16.5.130 a 172.16.5.189 ; LAN_60_3 ; host_utilizzabili=62 | 172.16.5.191 |

C15) Rete 10.10.0.0/24 con: 120 host, 30 host, 30 host, 10 host.

| Rete        | Subnet mask     | Router      | Server      | Host                                                           | Broadcast   |
| ----------- | --------------- | ----------- | ----------- | -------------------------------------------------------------- | ----------- |
| 10.10.0.0   | 255.255.255.128 | 10.10.0.126 | 10.10.0.1   | da 10.10.0.2 a 10.10.0.125 ; LAN_120 ; host_utilizzabili=126   | 10.10.0.127 |
| 10.10.0.128 | 255.255.255.224 | 10.10.0.158 | 10.10.0.129 | da 10.10.0.130 a 10.10.0.157 ; LAN_30_1 ; host_utilizzabili=30 | 10.10.0.159 |
| 10.10.0.160 | 255.255.255.224 | 10.10.0.190 | 10.10.0.161 | da 10.10.0.162 a 10.10.0.189 ; LAN_30_2 ; host_utilizzabili=30 | 10.10.0.191 |
| 10.10.0.192 | 255.255.255.240 | 10.10.0.206 | 10.10.0.193 | da 10.10.0.194 a 10.10.0.205 ; LAN_10 ; host_utilizzabili=14   | 10.10.0.207 |

C16) Rete 192.168.0.0/23 con: 300 host, 100 host, 50 host.

Impossibile soddisfare i requisiti usando la rete di partenza indicata, perché la sottorete necessaria per la richiesta più grande esaurisce lo spazio disponibile.
Rete minima consigliata per rendere possibile l’esercizio: 192.168.0.0/22

| Rete          | Subnet mask     | Router        | Server        | Host                                                             | Broadcast     |
| ------------- | --------------- | ------------- | ------------- | ---------------------------------------------------------------- | ------------- |
| 192.168.0.0   | 255.255.254.0   | 192.168.1.254 | 192.168.0.1   | da 192.168.0.2 a 192.168.1.253 ; LAN_300 ; host_utilizzabili=510 | 192.168.1.255 |
| 192.168.2.0   | 255.255.255.128 | 192.168.2.126 | 192.168.2.1   | da 192.168.2.2 a 192.168.2.125 ; LAN_100 ; host_utilizzabili=126 | 192.168.2.127 |
| 192.168.2.128 | 255.255.255.192 | 192.168.2.190 | 192.168.2.129 | da 192.168.2.130 a 192.168.2.189 ; LAN_50 ; host_utilizzabili=62 | 192.168.2.191 |

C17) Rete 172.16.0.0/23 con: 200 host, 60 host, 60 host.

| Rete        | Subnet mask     | Router       | Server      | Host                                                            | Broadcast    |
| ----------- | --------------- | ------------ | ----------- | --------------------------------------------------------------- | ------------ |
| 172.16.0.0  | 255.255.255.0   | 172.16.0.254 | 172.16.0.1  | da 172.16.0.2 a 172.16.0.253 ; LAN_200 ; host_utilizzabili=254  | 172.16.0.255 |
| 172.16.1.0  | 255.255.255.192 | 172.16.1.62  | 172.16.1.1  | da 172.16.1.2 a 172.16.1.61 ; LAN_60_1 ; host_utilizzabili=62   | 172.16.1.63  |
| 172.16.1.64 | 255.255.255.192 | 172.16.1.126 | 172.16.1.65 | da 172.16.1.66 a 172.16.1.125 ; LAN_60_2 ; host_utilizzabili=62 | 172.16.1.127 |

C18) Rete 10.0.0.0/22 con: 500 host, 200 host, 100 host.

| Rete     | Subnet mask     | Router     | Server   | Host                                                       | Broadcast  |
| -------- | --------------- | ---------- | -------- | ---------------------------------------------------------- | ---------- |
| 10.0.0.0 | 255.255.254.0   | 10.0.1.254 | 10.0.0.1 | da 10.0.0.2 a 10.0.1.253 ; LAN_500 ; host_utilizzabili=510 | 10.0.1.255 |
| 10.0.2.0 | 255.255.255.0   | 10.0.2.254 | 10.0.2.1 | da 10.0.2.2 a 10.0.2.253 ; LAN_200 ; host_utilizzabili=254 | 10.0.2.255 |
| 10.0.3.0 | 255.255.255.128 | 10.0.3.126 | 10.0.3.1 | da 10.0.3.2 a 10.0.3.125 ; LAN_100 ; host_utilizzabili=126 | 10.0.3.127 |

C19) Rete 192.168.100.0/24 con: 150 host, 50 host, 20 host.

Impossibile soddisfare i requisiti usando la rete di partenza indicata, perché la sottorete necessaria per la richiesta più grande esaurisce lo spazio disponibile.
Rete minima consigliata per rendere possibile l’esercizio: 192.168.100.0/23

| Rete           | Subnet mask     | Router          | Server         | Host                                                                 | Broadcast       |
| -------------- | --------------- | --------------- | -------------- | -------------------------------------------------------------------- | --------------- |
| 192.168.100.0  | 255.255.255.0   | 192.168.100.254 | 192.168.100.1  | da 192.168.100.2 a 192.168.100.253 ; LAN_150 ; host_utilizzabili=254 | 192.168.100.255 |
| 192.168.101.0  | 255.255.255.192 | 192.168.101.62  | 192.168.101.1  | da 192.168.101.2 a 192.168.101.61 ; LAN_50 ; host_utilizzabili=62    | 192.168.101.63  |
| 192.168.101.64 | 255.255.255.224 | 192.168.101.94  | 192.168.101.65 | da 192.168.101.66 a 192.168.101.93 ; LAN_20 ; host_utilizzabili=30   | 192.168.101.95  |

C20) Rete 172.16.100.0/24 con: 100 host, 30 host, 10 host, 2 link p2p.

| Rete           | Subnet mask     | Router         | Server         | Host                                                               | Broadcast      |
| -------------- | --------------- | -------------- | -------------- | ------------------------------------------------------------------ | -------------- |
| 172.16.100.0   | 255.255.255.128 | 172.16.100.126 | 172.16.100.1   | da 172.16.100.2 a 172.16.100.125 ; LAN_100 ; host_utilizzabili=126 | 172.16.100.127 |
| 172.16.100.128 | 255.255.255.224 | 172.16.100.158 | 172.16.100.129 | da 172.16.100.130 a 172.16.100.157 ; LAN_30 ; host_utilizzabili=30 | 172.16.100.159 |
| 172.16.100.160 | 255.255.255.240 | 172.16.100.174 | 172.16.100.161 | da 172.16.100.162 a 172.16.100.173 ; LAN_10 ; host_utilizzabili=14 | 172.16.100.175 |
| 172.16.100.176 | 255.255.255.252 | N/D            | N/D            | da 172.16.100.177 a 172.16.100.178 ; P2P_1 ; host_utilizzabili=2   | 172.16.100.179 |
| 172.16.100.180 | 255.255.255.252 | N/D            | N/D            | da 172.16.100.181 a 172.16.100.182 ; P2P_2 ; host_utilizzabili=2   | 172.16.100.183 |




