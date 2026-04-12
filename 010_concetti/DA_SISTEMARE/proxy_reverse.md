
### Architetture reverse proxy 

#### 1️⃣ Scenario più comune (architettura corretta in ambito aziendale)

##### Posizione logica

Internet
→ Firewall
→ **DMZ (Reverse Proxy)**
→ Firewall (regole interne)
→ **LAN / Rete server interna (Application Server)**

##### Spiegazione

* Il **reverse proxy** è collocato nella **DMZ**.
* Il **server applicativo reale** è nella **rete interna** (non direttamente esposto).
* Il firewall consente:

  * Da Internet → solo 443 verso reverse proxy.
  * Dal reverse proxy → solo le porte necessarie verso il server interno (es. 8080 o 8000).
  * Nessun accesso diretto Internet → server interno.

##### Perché è corretto

* Se il reverse proxy viene compromesso, l’attaccante non è automaticamente nella LAN.
* La DMZ è una zona “cuscinetto” tra Internet e rete interna.
* Separazione dei livelli di rischio.

---

#### 2️⃣ Variante con doppia DMZ (architettura più strutturata)

Internet
→ Firewall esterno
→ DMZ pubblica (Reverse Proxy / WAF)
→ Firewall interno
→ DMZ applicativa (Application Server)
→ Firewall interno
→ LAN server (DB, servizi interni)

Qui si segmentano ulteriormente i livelli:

* Reverse proxy più esposto.
* Server applicativo meno esposto.
* Database ancora più protetto.

---

#### 3️⃣ Configurazione meno sicura (piccole realtà)

Internet
→ Firewall
→ Reverse proxy + server applicativo nella stessa DMZ

In questo caso:

* Reverse proxy e server web stanno nella stessa rete DMZ.
* È accettabile in contesti piccoli, ma meno sicuro rispetto alla separazione.

---

#### 4️⃣ Configurazione sconsigliata

Internet
→ Firewall
→ LAN
→ Reverse proxy + server nella LAN

Qui non esiste DMZ.

* Il reverse proxy è direttamente nella LAN.
* Se compromesso, l’attaccante è già dentro la rete interna.
* Non è buona pratica in ambito professionale.

---

#### Riassunto sintetico delle posizioni corrette

Reverse Proxy:

* Sta tra Internet e server applicativo.
* Di norma in **DMZ**.
* È il primo punto di contatto con l’esterno.

Server applicativo:

* Sta dietro al reverse proxy.
* Preferibilmente in **rete interna separata** dalla DMZ.
* Non deve essere raggiungibile direttamente da Internet.

Firewall:

* Sta tra Internet e DMZ.
* Deve anche filtrare il traffico tra DMZ e LAN.

---

#### Regola progettuale fondamentale

Internet non deve mai poter raggiungere direttamente:

* server applicativo
* database
* rete utenti

Il reverse proxy è il “filtro controllato” esposto, non il server reale.



### Proxy (forward proxy)

Un **proxy** “classico” (forward proxy) si mette tra **client interni** e Internet.

Schema logico:

Client → Proxy → Internet → Server esterno

Caratteristiche principali:

* I client sanno di usare il proxy (lo configurano nel browser o nel sistema).
* Il proxy rappresenta i client verso l’esterno.
* Serve per:

  * filtrare la navigazione web
  * controllare accessi e log
  * fare caching di contenuti
  * nascondere l’IP reale dei client

Esempio tipico:
In un’azienda, tutti i PC navigano tramite un proxy che blocca siti non autorizzati e registra il traffico.





### Reverse proxy

Un **reverse proxy** è un server che si mette “davanti” al vero server web.
si mette tra **Internet** e uno o più server interni.

Schema logico:

Client Internet → Reverse Proxy → Server interno

Caratteristiche principali:

* I client esterni non sanno che esiste.
* Il reverse proxy rappresenta i server interni.
* Serve per:

  * proteggere il server reale
  * gestire HTTPS (terminazione TLS)
  * bilanciare il carico tra più server
  * applicare rate limiting e regole di sicurezza (WAF)

Esempio tipico:
Un sito web pubblico espone solo il reverse proxy; il vero server applicativo resta in rete interna.

In pratica:

* Il client (browser) non parla direttamente con il server applicativo.
* Parla con il reverse proxy.
* Il reverse proxy riceve la richiesta, la controlla e poi la inoltra al server interno.

Perché si usa:

* Nasconde il server reale (non è esposto direttamente su Internet).
* Permette di controllare e filtrare il traffico.
* Può distribuire il carico su più server (bilanciamento).

---

### Proxy differenza fra forward e reverse

* Il **proxy (forward)** protegge e controlla i client.
* Il **reverse proxy** protegge e controlla i server.

Oppure, in modo ancora più sintetico:

* Forward proxy: sta “davanti ai client”.
* Reverse proxy: sta “davanti ai server”.

---

## Differenze operative

Configurazione:

* Forward proxy → configurato sui client.
* Reverse proxy → configurato lato server/infrastruttura.

Visibilità IP:

* Forward proxy nasconde gli IP dei client verso Internet.
* Reverse proxy nasconde gli IP dei server verso Internet.

Scopo principale:

* Forward proxy → controllo e filtraggio della navigazione.
* Reverse proxy → protezione, sicurezza e gestione del traffico verso un servizio web.



### Terminazione TLS

“Terminazione TLS” significa che:

* La connessione HTTPS cifrata viene decifrata dal reverse proxy.
* Il traffico tra proxy e server interno può essere in chiaro (se rete interna sicura) o ancora cifrato.

Vantaggio:

* Si centralizza la gestione dei certificati.
* Si alleggerisce il carico del server applicativo.

---

### WAF (Web Application Firewall)

Un **WAF** è un firewall specializzato per proteggere applicazioni web.

Non lavora solo su IP e porte, ma analizza il contenuto delle richieste HTTP.

Serve per bloccare attacchi come:

* SQL injection
* Cross-Site Scripting (XSS)
* Tentativi di accesso anomali
* Upload di file malevoli

---

### Rate limiting

Il **rate limiting** limita il numero di richieste che un utente può fare in un certo intervallo di tempo.

Esempio:

* Massimo 100 richieste al minuto per IP.

Serve per:

* Ridurre attacchi di tipo brute force (es. tentativi di login ripetuti).
* Mitigare attacchi di tipo DoS leggeri.
* Evitare sovraccarichi accidentali.

---

### In sintesi molto semplice

Reverse proxy + WAF = “filtro intelligente” davanti al sito.

* Riceve le richieste.
* Le controlla.
* Blocca quelle sospette.
* Protegge il server vero.
* Gestisce HTTPS e certificati.
* Limita abusi e attacchi comuni.
