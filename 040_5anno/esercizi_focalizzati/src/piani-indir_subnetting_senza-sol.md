---

# Subnetting IPv4 e piani di indirizzamento

---

## 1. Contesto operativo

Nel lavoro con gli indirizzi IPv4 si presentano due contesti distinti, che richiedono approcci diversi.

Nel contesto degli esercizi, viene fornito un indirizzo di rete iniziale e si richiede di applicare tecniche di subnetting per suddividerlo in sottoreti. L’obiettivo è verificare la correttezza dei calcoli e la capacità di applicare regole formali.

Nel contesto professionale, invece, spesso non esiste una rete assegnata. È necessario scegliere un blocco di indirizzi privati e progettare l’intera struttura della rete. In questo caso l’obiettivo non è solo la correttezza, ma anche:

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

```
192.168.10.25
```

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

Questo modello non è più utilizzato nella progettazione moderna, ma è utile per comprendere i fondamenti.

---

## 4. CIDR (Classless Inter-Domain Routing)

CIDR introduce la notazione:

```
indirizzo/prefisso
```

Esempio:

```
192.168.10.0/27
```

Significa che:

* i primi 27 bit identificano la rete
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

È la tecnica utilizzata nella progettazione reale delle reti.

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

* la colonna “Server” rappresenta indirizzi riservati a servizi statici
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


Nel mondo reale non si ragiona più in termini di “classi” (A, B, C) ma di **blocchi CIDR**, tuttavia gli intervalli privati storici restano un riferimento pratico:

* **10.0.0.0/8** → reti grandi e strutturate
* **172.16.0.0/12** → reti medio-grandi
* **192.168.0.0/16** → reti piccole o segmenti locali

La scelta dipende principalmente da **dimensione, crescita prevista e organizzazione logica**.


---

## 9. Indirizzi privati e progettazione reale

Questa sezione è centrale per comprendere come si opera fuori dal contesto scolastico.

---

### 9.1 Blocchi disponibili

Gli indirizzi privati sono:

* 10.0.0.0/8
* 172.16.0.0/12
* 192.168.0.0/16

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

#### Uso di 172.16.0.0/12

Offre un buon compromesso tra dimensione e semplicità. È molto usato quando il blocco 10 è già occupato o quando si vuole separare ambienti.

Uso reale:

* aziende con più sedi ma non enormi
* reti corporate suddivise per regioni o business unit
* ambienti separati (produzione, test, laboratorio)

Esempio realistico:

```
172.16.10.0/24 → sede Milano (uffici)
172.16.20.0/24 → sede Roma (uffici)
172.16.30.0/24 → laboratorio/test
172.16.100.0/24 → DMZ (web server, reverse proxy)
172.17.0.0/16 → infrastruttura server centralizzata
```

Caratteristica chiave:

* separazione logica per sedi o ambienti
* meno “ingombrante” del 10/8 ma comunque molto scalabile


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

Nella progettazione reale si applicano criteri che non emergono negli esercizi.

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

---

### 12.3 Limiti dell’approccio classful

* spreco di indirizzi
* rigidità
* non adatto a reti moderne

Per questo motivo viene utilizzato solo a scopo didattico.

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

È il metodo utilizzato nella progettazione reale.

Permette di assegnare a ogni rete una dimensione adeguata.

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

# 19. Esercizi

Le seguenti sezioni sono organizzate per livello:

* A → Richiami e basi (classful)
* B → Subnetting CIDR
* C → Progettazione con VLSM

---

## 19.1 Esercizi – Indirizzi Classful

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

## 19.2 Esercizi – CIDR

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

## 19.3 Esercizi – VLSM (Piani di indirizzamento)

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

## 19.4 Osservazioni sugli esercizi

Gli esercizi sono organizzati con difficoltà crescente:

* Classful → comprensione base
* CIDR → capacità di calcolo
* VLSM → progettazione

Le ultime tracce introducono problemi realistici:

* subnet insufficienti
* necessità di cambiare rete di partenza
* presenza di link punto-punto

---



