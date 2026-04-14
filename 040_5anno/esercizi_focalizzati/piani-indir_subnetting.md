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


# 20. Soluzioni

---

## 20.1 Soluzioni – Indirizzi Classful

---

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

## 20.2 Soluzioni – CIDR

---

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

## 20.3 Soluzioni – VLSM

---

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




---

# 21. Appendice – Valutazione

---

## 21.1 Struttura della valutazione

La valutazione di un esercizio di subnetting e piano di indirizzamento può essere suddivisa in quattro fasi logiche:

1. analisi del problema
2. progettazione della rete
3. calcolo del subnetting
4. costruzione del piano di indirizzamento

Questa suddivisione consente di valutare separatamente:

* comprensione
* progettazione
* capacità di calcolo
* correttezza operativa

---

## 21.2 Griglia sintetica (20 punti)

| Criterio                        | Punti max | Descrizione                             |
| ------------------------------- | --------- | --------------------------------------- |
| Comprensione della traccia      | 3         | corretta identificazione di reti e host |
| Identificazione delle sottoreti | 3         | numero e ruolo delle reti               |
| Dimensionamento delle subnet    | 4         | scelta corretta delle dimensioni        |
| Calcolo delle subnet            | 5         | prefissi, network, broadcast            |
| Piano di indirizzamento         | 3         | assegnazione di gateway e host          |
| Coerenza complessiva            | 2         | assenza di errori logici                |

Totale: 20 punti

---

## 21.3 Criteri di assegnazione

Per ciascun criterio:

* punteggio massimo → corretto
* punteggio intermedio → piccoli errori
* punteggio minimo → errori gravi o incompleto

Questo consente una valutazione proporzionata anche in presenza di errori parziali.

---

## 21.4 Metodo a penalità

Alternativa più rapida:

* si parte da 20 punti
* si sottraggono punti per errori

---

### Errori tipici

| Errore                                    | Penalità |
| ----------------------------------------- | -------- |
| Interpretazione errata della traccia      | −3       |
| Sottorete mancante                        | −2       |
| Dimensionamento errato                    | −2       |
| Subnet mask errata                        | −1       |
| Errore network ID                         | −2       |
| Errore broadcast                          | −2       |
| Intervallo host errato                    | −1       |
| Sovrapposizione subnet                    | −3       |
| Uso errato di network/broadcast come host | −2       |
| Piano incompleto                          | −1       |
| Soluzione poco chiara                     | −1       |

---

## 21.5 Uso pratico

Il metodo a penalità è utile quando:

* si correggono molti compiti
* gli esercizi sono standardizzati
* serve rapidità

La griglia a criteri è più adatta quando:

* si vuole una valutazione più analitica
* si vogliono distinguere le diverse competenze

---

## 21.6 Struttura consigliata per le risposte

Per facilitare la correzione, è utile richiedere sempre una tabella finale.

Formato consigliato:

| Rete | Prefisso | Subnet mask | Network | Primo host | Ultimo host | Broadcast |

Oppure:

| Nome rete | Network | Prefisso | Gateway | Statici | Host |

---

## 21.7 Coerenza della valutazione

Una valutazione efficace deve:

* distinguere tra errore di metodo ed errore di calcolo
* non penalizzare eccessivamente errori propagati
* premiare la struttura corretta della soluzione

---

## 21.8 Sintesi

Un esercizio completo richiede:

* comprensione del problema
* progettazione delle subnet
* corretto calcolo
* costruzione del piano finale

---

## 21.9 Osservazione finale

Subnetting e piano di indirizzamento valutano competenze diverse:

* subnetting → capacità tecnica
* piano di indirizzamento → capacità progettuale

Entrambe sono necessarie per operare in contesti reali.

---

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

