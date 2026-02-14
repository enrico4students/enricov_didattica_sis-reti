## Certificato digitale – concetto generale

![Image](https://www.researchgate.net/publication/322926088/figure/fig5/AS%3A631614061158460%401527599935434/Format-of-X-509-Certificate.png)
&nbsp;

![Image](https://knowledge.digicert.com/content/dam/kb/attachments/ssl-tls-certificates/certificate-chain/figure-chain.jpg)
&nbsp;


![Image](https://cf-assets.www.cloudflare.com/slt3lc6tev37/5aYOr5erfyNBq20X5djTco/3c859532c91f25d961b2884bf521c1eb/tls-ssl-handshake.png)
&nbsp;

![Image](https://hpbn.co/assets/diagrams/b83b75dbbf5b7e4be31c8000f91fc1a8.svg)
&nbsp;

---

## 1. Definizione

Un **certificato digitale** è un documento elettronico standardizzato (formato **X.509**) che:

* associa una **chiave pubblica** a un’identità
* è firmato digitalmente da un’autorità fidata (Certification Authority, CA)
* consente autenticazione, cifratura e verifica di integrità

È un elemento centrale della **PKI (Public Key Infrastructure)**.

In termini semplici:
è una carta d’identità crittografica che collega una chiave pubblica a un soggetto (persona, server, organizzazione).

---

## 2. Struttura di un certificato X.509

Un singolo certificato contiene:

* Version
* Serial Number
* Signature Algorithm
* Issuer (chi lo ha firmato)
* Validity (Not Before / Not After)
* Subject (identità)
* Subject Alternative Name (SAN)
* Subject Public Key
* Extensions (Key Usage, Extended Key Usage, ecc.)
* Digital Signature della CA

### Diagramma logico semplificato

```
+--------------------------------------------------+
|                 X.509 Certificate                |
+--------------------------------------------------+
| Version                                          |
| Serial Number                                    |
| Signature Algorithm                              |
+--------------------------------------------------+
| Issuer (CA che firma)                            |
+--------------------------------------------------+
| Validity                                         |
+--------------------------------------------------+
| Subject (es. www.example.com)                    |
+--------------------------------------------------+
| Public Key                                       |
+--------------------------------------------------+
| Extensions (SAN, Key Usage, ecc.)                |
+--------------------------------------------------+
| Firma digitale dell'Issuer                       |
+--------------------------------------------------+
```

Importante:
la **catena di fiducia non è contenuta dentro questo certificato**.
Il certificato contiene solo l’identità dell’Issuer e la sua firma.

---

## 3. Catena di fiducia (Trust Chain)

Un browser non si fida direttamente del certificato del server.

La fiducia si basa su una **catena di certificati separati**:

```
Root CA  (già presente nel sistema)
    ↓ firma
Intermediate CA
    ↓ firma
Server Certificate
```

Il certificato del server:

* è firmato da una CA intermedia
* non contiene l’intera catena
* contiene solo il riferimento all’Issuer

Il browser ricostruisce la catena:

1. Verifica che il certificato del server sia firmato dall’intermedia.
2. Verifica che l’intermedia sia firmata dalla Root.
3. Controlla che la Root sia nel trust store locale.

Se la catena è valida → certificato accettato.

Un certificato self-signed non ha catena pubblica.

---

## 4. Tipologie e casi d’uso

### a) Certificati per Web server (HTTPS)

* autenticare un dominio
* abilitare TLS
* proteggere traffico HTTP

---

### b) Certificati client

* autenticazione utenti
* VPN
* accesso a reti aziendali

---

### c) Certificati di firma digitale

* firma documenti
* firma email (S/MIME)
* code signing

---

## 5. Uso del certificato in SSL/TLS

SSL (obsoleto) e TLS (attuale) utilizzano il certificato per:

1. Autenticare il server.
2. Permettere lo scambio sicuro della chiave di sessione.
3. Abilitare cifratura simmetrica.

Sequenza semplificata:

```
ClientHello
ServerHello
Invio certificato
Verifica firma e catena
Scambio chiave
Comunicazione cifrata
```

Il certificato contiene solo la chiave pubblica.
La chiave privata rimane segreta nel server.

---

## 6. LAB – Creazione di un certificato self-signed

Requisito: OpenSSL installato.

### Installazione in Windows

I comandi funzionano anche in Windows se:

* OpenSSL è installato
* la directory bin è nel PATH

Possibili ambienti:

* OpenSSL per Windows
* Git Bash
* WSL
* MSYS2

---

### Generare chiave privata

```
openssl genrsa -out server.key 2048
```

File generato:

* server.key → chiave privata

---

### Creare certificato self-signed

```
openssl req -new -x509 -key server.key -out server.crt -days 365
```

File generato:

* server.crt → certificato

---

### Verifica contenuto

```
openssl x509 -in server.crt -text -noout
```

---

## 7. Codice sorgente di un certificato X.509 (formato PEM)

Un certificato è codificato in ASN.1 e serializzato in DER o PEM.

Esempio minimale PEM:

```
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJANUEexample123MA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAklUMQ8wDQYDVQQIDAZMYXppbzEPMA0GA1UEBwwGUm9tYTEPMA0GA1UEAwwG
bG9jYWxob3N0MB4XDTI2MDIxNDEwMDAwMFoXDTI3MDIxNDEwMDAwMFowRTELMAkG
A1UEBhMCSVQxDzANBgNVBAgMBkxhemlvMQ8wDQYDVQQHDAZSb21hMQ8wDQYDVQQD
DAZsb2NhbGhvc3QwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCexample
QWERTY1234567890abcdefghijkExampleKeyData
-----END CERTIFICATE-----
```

È una rappresentazione Base64 del certificato binario DER.

---

## 8. Installazione su Web server

### File coinvolti

Self-signed:

* server.key
* server.crt

Certificato CA reale:

* server.key
* server.crt
* intermediate.crt
* oppure fullchain.pem (server + intermedi)

La Root CA non viene inviata: è già nel browser.

---

### Configurazione Apache

Configurazione minima:

```
SSLEngine on
SSLCertificateFile "C:/percorso/server.crt"
SSLCertificateKeyFile "C:/percorso/server.key"
```

Configurazione con CA intermedia:

```
SSLEngine on
SSLCertificateFile "C:/percorso/server.crt"
SSLCertificateKeyFile "C:/percorso/server.key"
SSLCertificateChainFile "C:/percorso/intermediate.crt"
```

Configurazione moderna consigliata:

```
SSLEngine on
SSLCertificateFile "C:/percorso/fullchain.pem"
SSLCertificateKeyFile "C:/percorso/server.key"
```

Riavviare Apache dopo la modifica.

---

## 9. Differenze tra certificato self-signed e certificato CA

| Caratteristica      | Self-signed         | CA pubblica   |
| ------------------- | ------------------- | ------------- |
| Firma               | Autonoma            | Firmato da CA |
| Catena di fiducia   | Assente             | Presente      |
| Fiducia browser     | Avviso di sicurezza | Accettato     |
| Identità verificata | No                  | Sì            |
| Uso produzione      | No                  | Sì            |

Limiti del certificato creato nel LAB:

* genera warning nel browser
* non garantisce identità verificata
* non ha fiducia globale

È adatto solo per:

* laboratorio
* test locali
* ambienti didattici

---

## Conclusione

Un certificato digitale:

* lega una chiave pubblica a un’identità
* è firmato da una CA
* si basa su una catena di fiducia esterna
* è essenziale per TLS/HTTPS

Un certificato self-signed dimostra il meccanismo tecnico,
ma solo un certificato firmato da una CA consente utilizzo sicuro e riconosciuto in produzione.
