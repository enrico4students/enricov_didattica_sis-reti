## Proxy Overview

1. Definizione  

Un proxy è un sistema intermedio che riceve una richiesta di rete da un client e la inoltra verso la destinazione per suo conto.  

Il flusso diventa:  

Client  
→ Proxy  
→ Server di destinazione  

Il server vede come sorgente il proxy, non il client originale (salvo header specifici come X-Forwarded-For).  

---

2. A cosa serve  

Un proxy può:  

* Controllare e filtrare traffico  
* Registrare accessi (logging)  
* Applicare policy (es. blocco categorie web)  
* Fare caching  
* Terminare TLS  
* Proteggere server interni  
* Nascondere la rete interna  

---

3. Tipologie principali

3.1 Forward Proxy (proxy “classico”)

Si trova tra client interni e Internet.

LAN
→ Forward Proxy
→ Internet

Funzioni tipiche:  
* Controllo navigazione web
* Autenticazione utenti
* Filtro URL
* Logging

Il server remoto non vede direttamente il client.

Uso tipico: controllo traffico web aziendale.

---

3.2 Reverse Proxy

Si trova davanti a server interni esposti.

Internet
→ Reverse Proxy
→ Web server interno

Funzioni tipiche:

* Terminazione TLS
* Load balancing
* Rate limiting
* Protezione applicativa
* Nascondere IP reali dei server

Uso tipico: pubblicazione sicura di servizi web.

---

3.3 Transparent Proxy

Il client non è configurato manualmente.
Il traffico viene intercettato a livello di rete (es. tramite firewall o switch).

Vantaggio: nessuna configurazione sui client.
Svantaggio: più complesso da implementare correttamente.

---

3.4 Proxy applicativi specifici

* HTTP/HTTPS proxy
* SMTP relay
* DNS proxy
* SOCKS proxy

Ogni proxy può operare a livello applicativo (Layer 7).

---

4. Relazione con altri componenti di rete

4.1 Con il firewall

Il firewall:

* controlla traffico tra zone
* decide cosa può passare

Il proxy:

* intermedia e comprende il contenuto applicativo

Spesso:

Client → Proxy → Firewall → Internet

Oppure il proxy è integrato nel firewall (NGFW con web proxy integrato).

---

4.2 Con il router

Il router:

* decide il percorso del traffico (routing IP)

Il proxy:

* non fa routing di rete
* opera sopra il livello IP

Il router non sostituisce il proxy.

---

4.3 Con il WAF

Il WAF è un tipo specializzato di reverse proxy focalizzato sulla sicurezza applicativa web.

Reverse proxy generico: bilanciamento, TLS, caching
WAF: protezione da SQL injection, XSS, attacchi HTTP

---

4.4 Con il load balancer

Molti reverse proxy moderni includono load balancing.

Reverse proxy = può essere anche load balancer
Load balancer puro = può non fare ispezione applicativa

---

5. Modalità tipiche di deployment in azienda

5.1 Forward proxy centralizzato

LAN
→ Proxy server (dedicato o virtuale)
→ Firewall
→ Internet

Tipico per controllo navigazione dipendenti.

Può essere:

* Appliance dedicata
* VM
* Servizio cloud (Secure Web Gateway)

---

5.2 Reverse proxy in DMZ

Internet
→ Firewall
→ DMZ
→ Reverse proxy
→ Web server interno

Oppure:

Internet
→ Reverse proxy (in DMZ)
→ Firewall interno
→ Server

Protegge applicazioni pubblicate.

---

5.3 Proxy integrato nel firewall NGFW

Molti NGFW includono:

* Web proxy
* SSL inspection
* URL filtering

In questo caso non esiste un proxy separato.

---

5.4 Proxy cloud (Secure Web Gateway)

Client
→ Internet
→ Proxy cloud del provider sicurezza
→ Destinazione

Molto usato in ambienti con smart working.

---

6. Tipologie oggi in uso in azienda

6.1 Forward Proxy / Secure Web Gateway

* Appliance on-premise
* VM in data center
* Servizio cloud (es. SWG)

Usato per controllo navigazione, DLP, controllo utenti.

---

6.2 Reverse Proxy / Application Delivery Controller

Usato per:

* Pubblicazione web
* Bilanciamento carico
* Terminazione TLS
* Zero trust access

---

6.3 WAF (come reverse proxy specializzato)

Usato per protezione applicazioni web pubbliche.

---

7. Differenza chiave tra proxy e firewall

Firewall:

* decide se il traffico può passare tra reti.

Proxy:

* si interpone nella comunicazione applicativa e parla al posto del client o del server.

Il firewall controlla il traffico.
Il proxy lo termina e lo rigenera.

---

8. Sintesi concettuale finale

Un proxy è un intermediario applicativo.

Può operare:

* in uscita (forward proxy)
* in ingresso (reverse proxy)
* in modo trasparente o esplicito
* on-premise o cloud

In azienda moderna è spesso:

* integrato in un NGFW
* usato come reverse proxy davanti ai servizi web
* erogato come servizio cloud per controllo navigazione

È un componente di sicurezza e controllo, non un sostituto del routing e non equivalente a un firewall, anche se talvolta le funzioni possono coesistere nello stesso apparato.
