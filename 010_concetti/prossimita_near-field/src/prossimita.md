## 1. Beacon BLE

Un beacon BLE è un piccolo dispositivo che trasmette periodicamente un identificatore tramite tecnologia BLE (Bluetooth Low Energy).

BLE è una variante del Bluetooth progettata per ridurre drasticamente il consumo energetico. Questo permette a piccoli dispositivi di funzionare anche per anni con una semplice batteria.

I beacon BLE vengono usati soprattutto per:

* localizzazione indoor;
* controllo presenza;
* marketing di prossimità;
* automazioni;
* tracciamento ambienti.

Esempi noti:

* iBeacon (Apple);
* Eddystone (Google).

---

### 1.1 Caratteristiche principali

Un beacon BLE normalmente:

* non stabilisce una vera connessione;
* non scambia dati complessi;
* non conosce i dispositivi che lo ascoltano;
* trasmette piccoli messaggi radio chiamati advertising packets.

Le caratteristiche principali sono:

* basso consumo energetico;
* funzionamento continuo;
* semplicità hardware;
* supporto diffuso sugli smartphone moderni.

La portata dipende da:

* potenza trasmissione;
* ostacoli;
* ambiente;
* configurazione.

In ambienti indoor reali la distanza utile è spesso:

* circa 3–15 metri;
* fino a circa 30 metri in condizioni favorevoli.

Pareti, persone e strutture metalliche possono ridurre significativamente il segnale.

---

### 1.2 Identificatori trasmessi

Il beacon trasmette normalmente:

* UUID;
* Major;
* Minor.

Questi valori permettono di identificare:

* organizzazione;
* edificio;
* aula;
* singolo dispositivo.

Esempio:

* UUID → scuola;
* Major → edificio;
* Minor → aula specifica.

Il beacon normalmente non contiene dati personali.

Trasmette soltanto identificatori.

---

## 2. Architettura di controllo presenza

Uno scenario molto comune consiste nel controllo presenza in aula o ufficio.

Schema generale:

    Beacon installato nell’ambiente  
                ↓  
    Smartphone rileva beacon  
                ↓  
    Applicazione invia dati al server  
                ↓  
    Server verifica validità e coerenza  

In questa architettura il server centrale prende le decisioni di validazione.

---

### 2.1 Processo operativo

---

#### 2.1.1 Fase 1 — Trasmissione beacon

Il beacon BLE trasmette continuamente il proprio identificatore.

La trasmissione avviene automaticamente a intervalli regolari.

---

#### 2.1.2 Fase 2 — Rilevamento smartphone

L’applicazione sullo smartphone ascolta i pacchetti BLE.

Quando rileva un beacon noto:

* legge identificatori;
* misura la potenza del segnale;
* raccoglie informazioni contestuali.

---

#### 2.1.3 Fase 3 — Invio dati al server

L’app invia al server:

* ID beacon;
* ID utente;
* timestamp;
* livello segnale BLE;
* coordinate GPS, se disponibili;
* informazioni rete WiFi.

L’app non decide autonomamente la validità della presenza.

---

#### 2.1.4 Fase 4 — Verifica lato server

Il server verifica:

* validità beacon;
* posizione prevista;
* coerenza temporale;
* plausibilità segnale;
* coerenza rete WiFi;
* eventuale posizione geografica.

Questa architettura riduce molte manipolazioni locali.

---

### 2.2 RSSI e stima della distanza

Quando uno smartphone riceve un segnale BLE può stimarne la potenza.

Questo valore viene chiamato RSSI (Received Signal Strength Indicator).

RSSI rappresenta la potenza del segnale ricevuto.

In generale:

* segnale forte → dispositivo vicino;
* segnale debole → dispositivo lontano.

La stima non è perfetta perché:

* muri;
* persone;
* interferenze;
* riflessioni radio

possono alterare il valore.

Per questo RSSI viene usato come indicatore probabilistico e non come misura esatta della distanza.

---

### 2.3 Uso delle informazioni WiFi

L’app può inviare alcuni metadati della rete WiFi.

Ad esempio:

* SSID;
* BSSID;
* livello segnale.

---

#### 2.3.1 SSID e BSSID

**SSID** è il nome logico della rete WiFi.
Esempio: `Istituto_WiFi`

**BSSID** è l’indirizzo MAC fisico del singolo access point.
ex. in una organizzazione possono esistere molti access point con lo stesso SSID ma BSSID differenti.

Esempio:
SSID: `Galilei Test`

Access point Aula 101: `11:22:33:44:55:66`

Access point Aula 120: `77:88:99:AA:BB:CC`

Il server può usare queste informazioni per verificare la coerenza della presenza.

Se uno studente dichiara presenza in Aula 101 ma risulta collegato al BSSID dell’Aula 120, il sistema può rilevare un’incongruenza.

---

## 3. Sicurezza e verifiche

Un beacon BLE da solo non è sufficientemente sicuro.

Problemi possibili:

* copia identificatore beacon;
* spoofing;
* simulazione beacon;
* replay dati;
* relay attack.

Per aumentare l’affidabilità vengono combinati più fattori.

---

### 3.1 Combinazione BLE + WiFi + GPS

Il sistema può combinare:

* Beacon BLE;
* rete WiFi;
* GPS;
* controlli server.

Ruolo dei vari elementi:

| Tecnologia | Funzione principale            |
| ---------- | ------------------------------ |
| Beacon BLE | prossimità indoor              |
| WiFi       | verifica rete locale           |
| GPS        | verifica macro-area geografica |
| Server     | controlli sicurezza            |

Il server incrocia tutti i dati ricevuti.

Esempio:

* beacon corretto;
* GPS coerente;
* BSSID compatibile con l’aula.

Più fattori vengono verificati, più diventa difficile falsificare la presenza.

---

### 3.2 Limiti del GPS indoor

Il GPS funziona molto bene all’esterno.

Negli edifici però il segnale satellitare può degradarsi fortemente.

Problemi tipici:

* precisione ridotta;
* segnale assente;
* errori di posizione.

Per questo motivo il BLE viene spesso usato come tecnologia indoor complementare.

---

### 3.3 Verifica lato server

Quando si parla di “beacon verificato lato server” significa che il controllo reale viene effettuato dal server centrale.

Il server:

* verifica che l’ID esista;
* controlla che sia associato alla sede corretta;
* può invalidare beacon;
* può ruotare identificatori;
* può applicare controlli anti-replay.

Esempio:

Il server memorizza:

```
Beacon_Aula_3 → edificio X, piano 1
```

Se arriva una richiesta incompatibile:

* GPS di un’altra città;
* BSSID non coerente;
* timestamp anomalo;

la richiesta può essere rifiutata.

---

### 3.4 Problemi di sicurezza residui

Il BLE non autentica automaticamente il beacon.

Problemi ancora possibili:

* spoofing beacon;
* relay attack;
* clonazione identificatori;
* WiFi spoofing;
* replay pacchetti.

Per ambienti ad alta sicurezza possono servire:

* token temporanei;
* rolling code;
* firme crittografiche;
* autenticazione forte;
* challenge-response.

---

## 4. Tecnologie moderne di prossimità

Le tecnologie di prossimità permettono di identificare dispositivi o utenti a breve distanza.

Le più diffuse oggi sono:

* NFC;
* RFID;
* BLE;
* UWB.

---

### 4.1 NFC (Near Field Communication)

NFC è una delle tecnologie di prossimità più diffuse negli smartphone moderni.

Caratteristiche principali:

* distanza molto breve;
* tipicamente pochi centimetri;
* comunicazione bidirezionale;
* semplicità d’uso elevata.

Applicazioni molto diffuse:

* pagamenti contactless;
* badge;
* trasporti pubblici;
* lettura tag;
* autenticazione dispositivi.

Esempi reali:

* Apple Pay;
* Google Pay;
* badge universitari;
* tessere contactless.

La distanza molto ridotta migliora la sicurezza pratica perché richiede vicinanza fisica reale.

---

### 4.2 RFID (Radio Frequency Identification)

RFID è una famiglia di tecnologie per identificazione radio.

Esistono:

* tag passivi;
* tag attivi.

I tag passivi non hanno batteria.

Vengono alimentati temporaneamente dal campo elettromagnetico del lettore.

RFID è molto diffuso in:

* logistica;
* magazzini;
* supply chain;
* controllo accessi;
* antitaccheggio;
* tracciamento prodotti.

La distanza operativa dipende dalla tecnologia utilizzata.

Può andare da pochi centimetri fino a diversi metri.

---

### 4.3 BLE Beacon

I beacon BLE sono ottimizzati per:

* prossimità indoor;
* basso consumo;
* smartphone;
* localizzazione approssimativa.

Usi tipici:

* presenza in aula;
* marketing proximity;
* musei;
* localizzazione indoor.

BLE offre maggiore flessibilità rispetto a NFC ma minore sicurezza fisica.

---

### 4.4 UWB (Ultra Wideband)

UWB è una tecnologia più recente.

Permette di stimare la distanza con precisione molto maggiore rispetto al BLE.

Caratteristiche:

* elevata precisione spaziale;
* buona resistenza a interferenze;
* misura accurata della distanza.

Applicazioni moderne:

* chiavi digitali auto;
* tracking preciso;
* localizzazione dispositivi.

Esempi noti:

* Apple AirTag;
* localizzazione dispositivi Samsung;
* sistemi keyless avanzati.

UWB è in crescita ma ancora meno diffuso rispetto a NFC e BLE.

---

### 4.5 Differenze fra RFID, NFC e BLE

Le varie tecnologie hanno obiettivi differenti.

#### RFID

Ottimizzato per:

* identificazione automatica;
* industria;
* logistica;
* inventario.

---

#### NFC

Ottimizzato per:

* interazione molto ravvicinata;
* smartphone;
* pagamenti;
* autenticazione rapida.

---

#### BLE

Ottimizzato per:

* prossimità indoor;
* basso consumo;
* localizzazione approssimativa;
* interazione smartphone.

---

### 4.6 Confronto  

| Tecnologia | Distanza tipica | Precisione | Diffusione attuale | Uso tipico       |
| ---------- | --------------- | ---------- | ------------------ | ---------------- |
| NFC        | pochi cm        | molto alta | molto alta         | pagamenti        |
| RFID       | cm → metri      | media      | molto alta         | logistica        |
| BLE Beacon | metri           | media      | alta               | indoor proximity |
| UWB        | metri           | molto alta | media              | tracking preciso |

---

## 5. Sintesi  

Le tecnologie di prossimità sono oggi fondamentali in moltissimi sistemi moderni.

BLE permette:

* localizzazione indoor;
* controllo presenza;
* prossimità smartphone.

NFC è dominante nei:

* pagamenti;
* badge;
* autenticazioni contactless.

RFID è molto usato in:

* industria;
* logistica;
* tracciamento automatico.

UWB rappresenta invece una tecnologia emergente ad alta precisione.

Nessuna tecnologia è perfettamente sicura da sola.

Per questo i sistemi moderni combinano spesso:

* BLE;
* WiFi;
* GPS;
* controlli server;
* meccanismi crittografici.

L’obiettivo è aumentare affidabilità, ridurre spoofing e migliorare la sicurezza complessiva del sistema.
