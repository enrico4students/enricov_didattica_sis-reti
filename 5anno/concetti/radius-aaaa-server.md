## RADIUS AAA Server


<img src="https://www.inkbridgenetworks.com/web/image/3558-fb43d2bc/radius_diagram_auth_3324x2535.webp?access_token=01528220-784d-49e6-b2ee-f9ed2fc16e95" width="80%"/>


<img src="https://miro.medium.com/0%2A9WZnM_foBQEql8nh.png" width="80%"/>

<img src="https://upload.wikimedia.org/wikipedia/commons/1/1f/802.1X_wired_protocols.png" width="80%"/>


<img src="https://media.licdn.com/dms/image/v2/D5612AQEr5797TWza-w/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1713631795614?e=2147483647\&t=XHmyBBcYsC2Of8oZjvMddVOmFca4mZCWMm4gRxkw6o8\&v=beta" width="80%"/>



RADIUS (protocollo): Remote Authentication Dial-In User Service  

## 1) Definizione

Un **RADIUS server** è un server che implementa il protocollo **RADIUS (Remote Authentication Dial-In User Service)** per fornire servizi di **AAA**:

* **Authentication** (Autenticazione)
* **Authorization** (Autorizzazione)
* **Accounting** (Contabilizzazione)

È tipicamente usato in reti aziendali per controllare l’accesso a:

* Wi-Fi (WPA2/WPA3-Enterprise)
* VPN
* accesso 802.1X su rete cablata
* dispositivi di rete (router, switch)

E' un protocollo client - server, standardizzato da IETF, che ha anche standardizzato 
DIAMETER, per AAA per peer2peer

---

## 2) Cosa significa AAA

### Authentication

Verificare l’identità dell’utente o del dispositivo.
Esempio: username/password, certificato digitale, smart card.

### Authorization

Determinare cosa può fare l’utente.
Esempio: assegnare una VLAN, limitare banda, consentire solo certi servizi.

### Accounting

Registrare attività e durata della sessione.
Esempio: tempo di connessione, traffico generato.

---

## 3) Come funziona (flusso tipico Wi-Fi Enterprise)

Componenti:

* Client (utente)
* Access Point (NAS – Network Access Server)
* RADIUS server

Flusso semplificato:

1. L’utente tenta di connettersi al Wi-Fi.
2. L’Access Point inoltra le credenziali al RADIUS.
3. Il RADIUS verifica le credenziali (es. su Active Directory).
4. Se valide:

   * autorizza l’accesso
   * può assegnare VLAN o policy
5. Registra la sessione (accounting).

Il RADIUS comunica tipicamente su:

* UDP 1812 (authentication)
* UDP 1813 (accounting)

---

## 4) Dove si colloca in rete

Il RADIUS server si trova normalmente:

* nella LAN aziendale
* in un server dedicato o integrato nel dominio
* protetto da firewall

Gli Access Point o switch fungono da intermediari tra client e RADIUS.

---

## 5) Esempi di RADIUS server

* Microsoft NPS (Network Policy Server)
* FreeRADIUS (open source)
* Cisco ISE (enterprise)

---

## 6) Differenza tra RADIUS e autenticazione locale

Autenticazione locale (es. password nel router):

* gestione decentralizzata
* difficile da scalare
* nessun accounting centralizzato

RADIUS:

* gestione centralizzata
* integrazione con directory aziendale
* policy dinamiche (VLAN, ACL)
* logging centralizzato

---

## 7) Relazione con 802.1X

Il protocollo **802.1X** usa RADIUS come backend AAA.

Componenti 802.1X:

* Supplicant (client)
* Authenticator (switch/AP)
* Authentication Server (RADIUS)

RADIUS è quindi il server centrale che decide se consentire o meno l’accesso alla rete.

---

## Conclusione

Un **RADIUS AAA server** è un server centralizzato che:

* autentica utenti e dispositivi
* assegna permessi di accesso
* registra le sessioni

È un elemento fondamentale nelle reti aziendali moderne per Wi-Fi Enterprise, VPN e controllo accessi 802.1X.
