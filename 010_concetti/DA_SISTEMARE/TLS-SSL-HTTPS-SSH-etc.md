## 1) SSL e TLS

### SSL (Secure Sockets Layer)

SSL è un protocollo crittografico sviluppato negli anni ’90 per proteggere comunicazioni su rete TCP.

Versioni:

* SSL 2.0 → obsoleta
* SSL 3.0 → obsoleta e vulnerabile

Oggi SSL non è più considerato sicuro.

---

### TLS (Transport Layer Security)

TLS è l’evoluzione di SSL.

Versioni principali:

* TLS 1.0 → deprecato
* TLS 1.1 → deprecato
* TLS 1.2 → ancora ampiamente usato
* TLS 1.3 → standard moderno e raccomandato

Attualmente:

✅ TLS 1.2 e TLS 1.3 sono in uso
❌ SSL e TLS 1.0/1.1 non devono essere usati

TLS fornisce:

* Cifratura dei dati
* Autenticazione del server (certificato X.509)
* Integrità dei messaggi

---

## 2) HTTPS

HTTPS = HTTP over TLS

Non è un protocollo nuovo, ma:

HTTP + TLS

Flusso:

Client
→ handshake TLS
→ canale cifrato
→ scambio HTTP dentro TLS

Funzioni:

* Protegge traffico web
* Autentica il server tramite certificato
* Previene intercettazione e manomissione

Uso attuale:

✅ Tutti i siti web moderni usano HTTPS
TLS 1.3 è sempre più diffuso

---

## 3) Differenza tra SSL, TLS e HTTPS

SSL:

* Protocollo obsoleto
* Non deve essere usato

TLS:

* Protocollo crittografico generico
* Protegge molte applicazioni (HTTPS, SMTPS, IMAPS, ecc.)

HTTPS:

* Applicazione specifica: HTTP protetto da TLS

In sintesi:

TLS è il protocollo di sicurezza
HTTPS è un protocollo applicativo che usa TLS

---

## 4) Casi d’uso di TLS oggi

TLS è usato per:

* HTTPS (web)
* SMTPS (email)
* IMAPS / POP3S
* VPN TLS
* API REST
* Microservizi interni

È lo standard dominante per cifratura su TCP.

---

## 5) SSH (Secure Shell)

SSH è un protocollo crittografico per:

* Accesso remoto sicuro a server
* Esecuzione comandi
* Tunneling
* Port forwarding

Funziona su TCP (porta 22 di default).

Differenza fondamentale da TLS:

* TLS è usato per proteggere applicazioni esistenti.
* SSH è un protocollo autonomo con proprio sistema di autenticazione (password o chiavi pubbliche).

Uso tipico:

Amministrazione remota di server Linux/Unix.

---

## 6) SFTP e FTPS

Entrambi servono per trasferimento file sicuro, ma sono molto diversi.

---

### SFTP (SSH File Transfer Protocol)

SFTP:

* Funziona sopra SSH
* Usa una sola connessione (porta 22)
* È parte dell’ecosistema SSH

Caratteristiche:

* Sicuro
* Semplice da configurare (una porta)
* Non è FTP cifrato, è un protocollo diverso

Uso moderno:

✅ Molto diffuso in ambito aziendale

---

### FTPS (FTP over TLS)

FTPS:

* È FTP tradizionale con TLS
* Usa certificati TLS
* Mantiene struttura FTP (connessione controllo + dati)

Due modalità:

* Implicita
* Esplicita

Problema:

* Usa più porte
* Più complesso da configurare con firewall/NAT

Uso attuale:

Ancora presente, ma meno semplice da gestire rispetto a SFTP.

---

## 7) Differenze tra SFTP e FTPS

SFTP:

* Basato su SSH
* Porta singola
* Protocollo completamente diverso da FTP
* Più semplice lato firewall

FTPS:

* FTP + TLS
* Più porte
* Compatibilità con sistemi legacy FTP

---

## 8) Confronto sintetico

TLS:

* Protegge trasporto
* Usato da HTTPS e altri protocolli

HTTPS:

* HTTP cifrato con TLS

SSH:

* Protocollo per accesso remoto sicuro

SFTP:

* Trasferimento file sopra SSH

FTPS:

* FTP protetto con TLS

---

## 9) Stato attuale delle tecnologie

Attualmente in uso e raccomandati:

✅ TLS 1.2
✅ TLS 1.3
✅ HTTPS
✅ SSH
✅ SFTP

Obsoleti o sconsigliati:

❌ SSL
❌ TLS 1.0
❌ TLS 1.1

---

## 10) Sintesi finale

TLS è lo standard moderno per cifrare comunicazioni su TCP.
HTTPS è la sua applicazione più diffusa.
SSH è il protocollo sicuro per amministrazione remota.
SFTP usa SSH per trasferire file in modo sicuro.
FTPS usa TLS per proteggere il vecchio protocollo FTP.

Nel mondo aziendale moderno, TLS 1.2/1.3, HTTPS, SSH e SFTP sono le tecnologie dominanti.
