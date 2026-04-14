
---  

Da rivedere, scelta indirizzi errata, probabilmente molti altri dettagli errati


---

## PRIMA PARTE – Progettazione della rete dell’albergo e dello stabilimento balneare

### A. Struttura della rete e apparati necessari

**Ipotesi aggiuntive** (dichiarate per chiarezza):
- L’albergo dispone di un locale tecnico dove concentrare router/firewall, switch principali e server.
- Il cablaggio strutturato prevede almeno un punto di accesso Wi‑Fi per ogni piano/camere (AP PoE).
- La gestione delle credenziali Wi‑Fi avviene tramite RADIUS integrato con il database delle prenotazioni.
- Lo stabilimento balneare è raggiungibile via ponte radio (line‑of‑sight dalla terrazza, 500 m).

**Apparati necessari**:

| Apparato | Quantità | Ruolo |
|----------|----------|-------|
| Router/Firewall (es. pfSense, FortiGate) | 1 | Collegamento a Internet (FTTH), NAT, policy‑based routing, VPN per eventuale backup |
| Switch core managed (Layer 3) | 1 | Aggregazione VLAN, routing inter‑VLAN con ACL, uplink a router e server |
| Switch di piano/armadio PoE (Layer 2) | 4‑6 | Distribuzione cablaggio camere, uffici, sale convegni; alimentazione AP e telecamere (se previste) |
| Access Point Wi‑Fi (802.11ax, WPA2‑Enterprise) | ~8‑10 | Copertura camere, sale, ristorante, piscina, esterni |
| Controller Wi‑Fi (opzionale, o cloud) | 1 | Gestione centralizzata AP e roaming |
| Server RADIUS + DB (VM o fisico) | 1 | Autenticazione ospiti/dipendenti, integrazione con prenotazioni |
| Server gestionale intranet | 1 (esistente) | Software di gestione albergo |
| Server web (DMZ) | 1 (esistente) | Sito web pubblico |
| Bridge radio (5 GHz, 802.11ac/ax, direzionale) | 2 (albergo + stabilimento) | Collegamento punto‑punto per estendere LAN e Wi‑Fi ospiti |
| Switch PoE (stabilimento) | 1 | Alimenta AP e collegamento ponte radio |
| AP Wi‑Fi (stabilimento) | 2‑3 | Copertura spiaggia e bar |

**Topologia di rete (testo)**:

```
                     [INTERNET]
                          │
                    [Router/Firewall]
                     │     │     │
              (DMZ)  │     │     │ (LAN)
              [Web Server] │  [Switch Core L3]
                           │     │    │    │
                     ┌─────┼─────┼────┼────┼─────┐
                     │     │     │    │    │     │
                  [VLAN10] [VLAN20] [VLAN30] [VLAN40] [VLAN50] [VLAN60]
                   Ospiti  Uffici  Sale    Server   EV     Bridge→
                             │      convegni  gest.           │
                     [Server gestionale]                    [Stabilimento]
                                                              │
                                                         [Switch PoE]
                                                              │
                                                      [AP spiaggia]
```

**Architettura di sicurezza**:
- Firewall con regole di default “deny all”, solo traffico esplicitamente consentito.
- VLAN separate per ogni dominio (ospiti, dipendenti, sale convegni, server, EV, collegamento spiaggia).
- ACL sullo switch core: gli ospiti (VLAN10) possono solo uscire verso Internet, non verso altre VLAN. I dipendenti (VLAN20) possono raggiungere il server gestionale (VLAN40) e Internet. I partecipanti ai convegni (VLAN30) possono accedere a Internet e, se necessario, a risorse specifiche per videoconferenza.
- Il ponte radio (VLAN60) trasporta due sotto‑VLAN: una per il traffico dipendenti (verso server gestionale) e una per il traffico ospiti (verso Internet, con autenticazione RADIUS centralizzata). Sul firewall, il traffico proveniente dal ponte viene trattato come proveniente dalle VLAN corrispondenti.
- Autenticazione Wi‑Fi: 802.1X/EAP‑PEAP per dipendenti, captive portal con credenziali della prenotazione per ospiti. Il captive portal interroga il database prenotazioni tramite API.

**Perché non altre scelte**:
- *Un unico VLAN flat*: insicuro, permetterebbe a ospiti malevoli di attaccare i server.
- *NAT separato per ogni VLAN*: non necessario con router che supporta VLAN e ACL; complica la gestione.
- *Cablare lo stabilimento con fibra*: costoso (scavo, permessi), mentre il ponte radio (5 GHz) garantisce >300 Mbps a 500 m con latenza bassa, costo contenuto e installazione rapida. In alternativa, VPN su FTTH separata richiederebbe due abbonamenti e maggiore latenza.

---

### B. Piano di indirizzamento IP (IPv4 privato)

Utilizzo lo spazio `172.20.0.0/16` per facilità di aggregazione.

| VLAN | Nome | Subnet | CIDR | Note |
|------|------|--------|------|------|
| 10 | Ospiti | 172.20.10.0 | /22 | 1022 indirizzi (camere, dispositivi personali) |
| 20 | Uffici | 172.20.20.0 | /24 | 254 indirizzi (7 PC + stampante + crescita) |
| 30 | Sale convegni | 172.20.30.0 | /24 | 254 indirizzi (attrezzature, portatili relatori) |
| 40 | Server e management | 172.20.40.0 | /28 | 14 indirizzi (server gestionale, RADIUS, switch, AP) |
| 50 | EV charging | 172.20.50.0 | /28 | 14 indirizzi (6 colonnine + web app interna) |
| 60 | Ponte stabilimento | 172.20.60.0 | /29 | 6 indirizzi (bridge radio e gestione) |
| 99 | Nativa (out‑of‑band) | 172.20.99.0 | /24 | Gestione out‑of‑band degli switch (opzionale) |

**Gateway predefinito** per ogni VLAN: primo indirizzo utile (es. 172.20.10.1, 172.20.20.1, …).  
Il router ha interfacce su ogni VLAN (router‑on‑a‑stick) oppure switch L3 con routing abilitato.

**Motivazioni**:
- `/22` per ospiti: in alta stagione, 52 camere con 2‑4 dispositivi ciascuna + ospiti in aree comuni → fino a ~300 dispositivi contemporanei. /22 permette espansione futura.
- `/28` per server: sufficiente per server fisici e virtuali; indirizzi extra per futuri servizi (syslog, backup).
- Separazione netta degli intervalli: facilita la stesura di regole firewall (es. deny da 172.20.10.0/22 a 172.20.0.0/16 tranne eccezioni).

**Alternativa scartata**: usare 192.168.x.x. Con 52 camere e tanti dispositivi, i /24 sarebbero stati troppo piccoli per gli ospiti (solo 254 indirizzi). 10.0.0.0/8 sarebbe stato accettabile ma meno leggibile.

---

### C. Collegamento tra albergo e stabilimento balneare

**Soluzione proposta**: ponte radio punto‑punto (5 GHz, 802.11ac/ax) con antenne paraboliche o panel. Velocità tipica > 300 Mbps, distanza 500 m in visibilità diretta.

**Altre soluzioni valutate**:

| Soluzione | Vantaggi | Svantaggi | Scelta |
|-----------|----------|-----------|--------|
| Fibra ottica | Massima affidabilità, immunità RF, alta banda | Costo di scavo, permessi, tempi lunghi, difficoltà in area balneare | Scartata per costi e tempi |
| VPN su FTTH dedicata | Sfrutta doppio contratto internet già disponibile | Costo mensile aggiuntivo, latenza (router‑to‑router), necessita di due linee stabili | Scartata per ridondanza inutile (linea singola già presente) |
| Ponte radio | Basso costo, rapida installazione, banda sufficiente | Richiede linea di vista, sensibile a condizioni meteo estreme | **Scelta** |

**Implementazione**:
- All’albergo: bridge master con IP 172.20.60.1/29, connesso a switch core su VLAN60.
- Allo stabilimento: bridge slave con IP 172.20.60.2/29, connesso a switch PoE locale.
- Sul ponte si trasportano due VLAN taggate (802.1Q):
  - VLAN10-ospiti (per accesso Internet con captive portal centralizzato)
  - VLAN20-dipendenti (per raggiungere il server gestionale 172.20.40.10)
- Sicurezza: cifratura WPA2‑AES (o WPA3‑SAE) + ACL MAC opzionale. I bridge utilizzano indirizzi IP fissi su subnet di gestione separata.

**Perché questa soluzione soddisfa i requisiti**:
- I dipendenti dello stabilimento si collegano al gestionale come se fossero in albergo (stessa VLAN20).
- Gli ospiti in spiaggia accedono al Wi‑Fi con le stesse credenziali (RADIUS via tunnel sul ponte → al server di autenticazione in albergo).
- Non è necessario aprire porte su Internet, tutto il traffico rimane in LAN estesa.

---

### D. Progettazione database per prenotazioni e credenziali Wi‑Fi

#### Modello concettuale (ER)

Entità:
- **OSPITE** (id_ospite PK, nome, cognome, email, telefono)
- **CAMERA** (id_camera PK, numero, tipologia, piano, max_ospiti)
- **PRENOTAZIONE** (id_prenotazione PK, id_ospite FK, id_camera FK, data_checkin, data_checkout, stato)
- **CREDENZIALI_WIFI** (id_credenziale PK, id_prenotazione FK, username, password, data_creazione, data_scadenza)

Relazioni:
- Un OSPITE può avere molte PRENOTAZIONI (1:N)
- Una CAMERA può essere associata a molte PRENOTAZIONI (ma non sovrapposte) (1:N)
- Una PRENOTAZIONE genera un set di CREDENZIALI_WIFI (1:1 – una prenotazione produce un solo username/password)

**Diagramma ER (testo)**:

```
+-----------+       +---------------+       +-----------+
|  OSPITE   |       |  PRENOTAZIONE |       |  CAMERA   |
+-----------+       +---------------+       +-----------+
| id_ospite |<------| id_ospite     |       | id_camera |
| nome      |       | id_camera     |------>| numero    |
| cognome   |       | data_checkin  |       | tipologia |
| email     |       | data_checkout |       | piano     |
| telefono  |       | stato         |       +-----------+
+-----------+       +---------------+
                         |
                         | 1
                         | genera
                         |
                    +-------------------+
                    | CREDENZIALI_WIFI  |
                    +-------------------+
                    | id_credenziale    |
                    | id_prenotazione   |
                    | username          |
                    | password          |
                    | data_creazione    |
                    | data_scadenza     |
                    +-------------------+
```

#### Modello logico (SQL DDL)

```sql
CREATE TABLE ospite (
    id_ospite INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20)
);

CREATE TABLE camera (
    id_camera INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(5) NOT NULL UNIQUE,
    tipologia ENUM('singola', 'doppia', 'suite') NOT NULL,
    piano TINYINT NOT NULL,
    max_ospiti TINYINT NOT NULL
);

CREATE TABLE prenotazione (
    id_prenotazione INT AUTO_INCREMENT PRIMARY KEY,
    id_ospite INT NOT NULL,
    id_camera INT NOT NULL,
    data_checkin DATE NOT NULL,
    data_checkout DATE NOT NULL,
    stato ENUM('confermata', 'checkin_effettuato', 'completata', 'cancellata') DEFAULT 'confermata',
    FOREIGN KEY (id_ospite) REFERENCES ospite(id_ospite) ON DELETE RESTRICT,
    FOREIGN KEY (id_camera) REFERENCES camera(id_camera) ON DELETE RESTRICT,
    CHECK (data_checkout > data_checkin)
);

CREATE TABLE credenziali_wifi (
    id_credenziale INT AUTO_INCREMENT PRIMARY KEY,
    id_prenotazione INT NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,  -- hash + sale per sicurezza
    data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_scadenza DATE NOT NULL,
    FOREIGN KEY (id_prenotazione) REFERENCES prenotazione(id_prenotazione) ON DELETE CASCADE
);

-- Indice per ricerca veloce su username (usato da RADIUS)
CREATE INDEX idx_wifi_username ON credenziali_wifi(username);
```

**Motivazioni delle scelte**:
- `CHECK` su data_checkout > data_checkin garantisce integrità.
- `UNIQUE` su `credenziali_wifi.id_prenotazione` evita duplicati (una prenotazione → un paio di credenziali).
- La password viene salvata hashata (non in chiaro) per sicurezza, ma il RADIUS dovrà confrontare con l’hash.
- La scadenza delle credenziali può essere impostata a data_checkout + 1 giorno.
- Campo `stato` in prenotazione permette di gestire il ciclo di vita (es. non generare credenziali se cancellata).

**Alternativa scartata**: mettere username/password direttamente in prenotazione. Separando in tabella dedicata si facilita la rotazione delle credenziali (es. rigenerazione senza alterare la prenotazione) e l’integrazione con RADIUS (che tipicamente si appoggia a una tabella utenti dedicata).

---

## SECONDA PARTE – Quesiti opzionali (risposti tutti e quattro)

### I. Colonna di ricarica per auto elettriche – socket

**Formato di trasmissione** (esempio JSON compatto):
```json
{
  "ts": "2025-08-15T14:30:00Z",
  "client_id": "EV12345",
  "soc": 78,
  "energy_kwh": 12.4
}
```
**Ruolo dei socket** (TCP): forniscono un canale di comunicazione bidirezionale tra la colonnina (client) e il server remoto. Incapsulano i dati in segmenti TCP garantendo affidabilità, controllo di flusso e ordinamento.

**Funzioni principali** (lato colonnina):
- `socket()`: crea un endpoint di comunicazione (specifica dominio AF_INET, tipo SOCK_STREAM).
- `connect()`: stabilisce la connessione TCP verso il server (indirizzo IP e porta nota).
- `send()` / `write()`: invia il messaggio (es. JSON serializzato) al server.
- `recv()` / `read()`: riceve eventuali ACK o comandi dal server.
- `close()`: termina la connessione e rilascia le risorse.

**Lato server**:
- `socket()` + `bind()` (associa a porta fissa) + `listen()` (mette in ascolto) + `accept()` (accetta connessione in ingresso, crea un nuovo socket per il dialogo).

**Motivazione dell’uso di socket raw (non HTTP)**: riduce overhead, adatto a dispositivi embedded con risorse limitate. In alternativa si potrebbe usare MQTT su TCP (più leggero di HTTP), ma il testo richiede esplicitamente il ruolo dei socket.

---

### II. Filtraggio contenuti nella scuola

**Dispositivi necessari**:
- Firewall / router (es. pfSense, OPNSense) – gestisce NAT e regole di separazione VLAN.
- Proxy server trasparente (es. Squid + SquidGuard) – filtraggio URL e contenuti.
- Switch gestiti VLAN – separano traffico studenti, uffici, didattica.

**Configurazione ipotetica**:
- VLAN10_Studenti: subnet 10.0.10.0/24 – traffico HTTP/HTTPS forzato verso proxy tramite **Policy Based Routing** o **WCCP** (Web Cache Coordination Protocol). Il proxy blocca categorie (giochi, social, violenza).
- VLAN20_Uffici: subnet 10.0.20.0/24 – esente da proxy (o con filtro meno restrittivo). Regola firewall: da VLAN20 a Internet permesso diretto.

**Vantaggi**:
- Controllo centralizzato (log, statistiche, whitelist/blacklist).
- Possibilità di filtraggio per fascia oraria e autenticazione utente.
- Protezione da malware tramite blacklist aggiornate.

**Limiti**:
- Il proxy trasparente può introdurre latenza e non filtrare HTTPS se non si implementa SSL bump (che richiede installazione di certificato su ogni client e solleva questioni di privacy).
- Gli studenti esperti potrebbero usare VPN/Tor per aggirare il filtro.
- Carico aggiuntivo sul proxy (hardware dimensionato adeguatamente).

**Alternativa scartata**: solo firewall con filtraggio a livello IP (blocco domini tramite DNS) – facilmente aggirabile e non filtra contenuti dentro HTTPS. Meglio proxy + DNS filtering combinato.

---

### III. Differenze tra HTTPS e HTTP

**HTTP** (HyperText Transfer Protocol) trasmette dati in chiaro (plain text). **HTTPS** (HTTP over TLS/SSL) incapsula HTTP in un tunnel cifrato.

**Differenze tecniche**:
- Porta default: HTTP → 80, HTTPS → 443.
- Handshake TLS: il client verifica il certificato del server (rilasciato da una CA) e si scambiano chiavi per stabilire una sessione cifrata.
- Tutti i dati (URI, header, corpo) sono cifrati simmetricamente dopo l’handshake.

**Vantaggi per il visitatore**:
1. **Privacy** – Nessun terzo (ISP, malintenzionato sulla stessa rete) può leggere il contenuto delle pagine, i cookie o i dati inviati (es. password, numeri di carta di credito).
2. **Integrità** – Impossibile modificare i dati in transito (attacco man‑in‑the‑middle) senza che il client lo rilevi (il TLS fornisce autenticazione del messaggio).
3. **Autenticazione del sito** – Il certificato digitale garantisce che il sito sia effettivamente quello dichiarato (mitiga attacchi di phishing via DNS spoofing).
4. **SEO e fiducia** – I browser moderni marcano i siti HTTP come “non sicuri”, scoraggiando l’utente dall’inserire dati sensibili.

**Perché HTTP è ancora usato**: su siti puramente informativi senza scambio di dati personali, per ridurre carico CPU (cifratura) o per compatibilità con vecchi dispositivi. Tuttavia non è raccomandato.

---

### IV. Verifica guido – Pagine web esterne non accessibili

**Scenario**: ping verso gateway (192.168.24.1) funziona, risorse locali accessibili, ma nessuna pagina web esterna. DNS server noto (192.168.24.5).

**Sequenza di verifiche (dal tecnico)**:

1. **Test di risoluzione DNS**  
   `nslookup google.com 192.168.24.5`  
   - Se fallisce → problema sul server DNS (servizio fermo, ACL, forwarder non funzionanti).  
   - Se restituisce indirizzo IP → DNS funziona.

2. **Test di raggiungibilità IP esterno**  
   `ping 8.8.8.8` (o altra IP nota)  
   - Se fallisce → problema di routing verso Internet o blocco firewall sul gateway.  
   - Se riesce → il problema è solo sul nome (già escluso al punto 1) oppure sul protocollo (HTTP/HTTPS).

3. **Test con telnet sulla porta 80 di un IP esterno**  
   `telnet 8.8.8.8 80`  
   - Se la connessione viene rifiutata o scade → firewall sta bloccando le porte (80/443) o manca la regola NAT.  
   - Se la connessione funziona → il problema è a livello applicativo (proxy, browser).

4. **Verifica configurazione proxy nel browser**  
   Controllare se è impostato un proxy manuale (es. per la rete scolastica) e se è raggiungibile. Disabilitare temporaneamente.

5. **Verifica regole NAT sul gateway**  
   `iptables -t nat -L` (o comandi equivalenti su router) – assicurarsi che esista una regola MASQUERADE per le subnet interne verso l’interfaccia WAN.

6. **Verifica ACL sul firewall**  
   Controllare che la VLAN del PC abbia permesso il traffico outgoing verso le porte 80/443. Eventualmente analizzare log firewall.

**Motivazione dell’ordine**:
- Si parte dai livelli più bassi (ICMP, DNS) per isolare il problema.  
- Se il ping verso IP esterno funziona, il routing e il NAT sono OK → il problema è nel DNS o nel proxy.  
- Se il ping verso IP esterno fallisce, il problema è a livello di rete (gateway, firewall, NAT).

---

**Nota**: tutti i diagrammi PlantUML sono embeddati nei blocchi `plantuml`; per visualizzarli è sufficiente un visualizzatore PlantUML (plugin, server, o locale). Le versioni testo sono fornite per leggibilità immediata.