
### 1. Beacon BLE

Un **beacon BLE** è un piccolo dispositivo che trasmette periodicamente un identificatore tramite **Bluetooth Low Energy (BLE)**.

Caratteristiche principali:

* Non stabilisce una vera connessione
* Trasmette pacchetti pubblicitari (advertising packets)
* Contiene un identificatore (UUID, Major, Minor)
* Portata tipica: 5–30 metri (configurabile)
* Consumo energetico molto basso (anni con una batteria)

Esempi noti:

* iBeacon (Apple)
* Eddystone (Google)

Il beacon **non sa chi lo sta ascoltando**.
Si limita a trasmettere un ID.

---

### 2. Come funziona l’approccio “Beacon BLE verificato lato server”

Scenario tipico: controllo presenza in aula / ufficio.

#### Architettura

Beacon fisico installato in aula
↓
Smartphone rileva beacon
↓
App invia dati al server
↓
Server verifica validità

---

#### Processo passo per passo

1. Il beacon trasmette continuamente il suo ID.

2. L’app sullo smartphone rileva l’ID.

3. L’app invia al server:

   * ID beacon
   * ID utente
   * timestamp
   * coordinate GPS (se disponibili)
   * informazioni sulla rete WiFi corrente

4. Il server verifica:

   * che l’ID beacon sia valido
   * che sia associato a quella sede
   * che il segnale sia plausibile (RSSI)
   * che la rete WiFi e la posizione siano coerenti

La verifica “lato server” evita manipolazioni locali.

---

### 3. Cosa significa “inviare rete WiFi”

Non significa inviare traffico WiFi o password.

L’app può inviare **metadati della rete WiFi a cui il dispositivo è connesso**, ad esempio:

* **SSID** → nome della rete (es. `Istituto_WiFi`)
* **BSSID** → indirizzo MAC dell’access point
* eventualmente livello di segnale (RSSI)

Il **BSSID (Basic Service Set Identifier)** è il MAC address fisico dell’access point WiFi.

Un SSID può essere lo stesso in tutta la scuola, ma ogni access point ha un BSSID diverso.

Esempio:

SSID: `Istituto_WiFi`

* Aula 1 → BSSID 11:22:33:44:55:66
* Aula 2 → BSSID 77:88:99:AA:BB:CC

Se lo studente dichiara presenza in Aula 1 ma risulta connesso al BSSID dell’Aula 2, il server può rilevare incongruenza.

---

### 4. Perché si consiglia WiFi + GPS

Il beacon BLE da solo non è sicuro.

Problemi:

* L’ID può essere copiato (spoofing)
* Si può simulare un beacon
* Si può intercettare il codice e riutilizzarlo

Per questo si combinano più fattori:

* **Beacon BLE** → prossimità locale (precisione indoor)
* **WiFi (SSID + BSSID)** → verifica access point coerente
* **GPS** → verifica posizione geografica (macro-area)

Il server incrocia:

* Beacon corretto
* Coordinate compatibili
* BSSID coerente con quella sede

Più fattori → minore possibilità di falsificazione.

---

### 5. Cosa significa “identificatore beacon verificato lato server”

Significa che:

* L’app non decide autonomamente la validità
* Il server controlla che l’ID sia registrato
* Il server può ruotare o invalidare ID
* Si possono applicare controlli anti-replay

Esempio:

Il server memorizza:
Beacon_Aula_3 → edificio X, piano 1

Se uno studente invia Beacon_Aula_3 ma:

* GPS indica un’altra città
* BSSID non corrisponde a un access point registrato

la richiesta viene respinta.

---

### 6. Limiti dell’approccio

* Il BLE non autentica il beacon
* Possibile relay attack
* Indoor GPS poco preciso
* WiFi spoofabile

Per ambienti ad alta sicurezza servono meccanismi aggiuntivi:

* Token temporanei
* Firma crittografica
* Beacon con rolling code

---

### 7. Sintesi tecnica

Un beacon BLE è:

* Trasmettitore di identificatore
* Tecnologia di prossimità indoor

L’approccio WiFi (SSID + BSSID) + GPS + verifica server:

* Non si basa su un solo fattore
* Riduce spoofing
* Aumenta affidabilità del controllo presenza

Se necessario si può integrare con meccanismi crittografici per aumentare il livello di sicurezza.
