
# PRIMA PARTE

## 1) Progetto dell’infrastruttura tecnologica

## 1.a Architettura della rete e sistemi server

### Analisi dei requisiti

Vincoli fondamentali:

* Contenuti NON memorizzati sui dispositivi
* Accesso solo da minitablet forniti
* Accesso solo previa autenticazione
* Fruizione solo in prossimità del POI
* Validità giornaliera del biglietto

Ne consegue un’architettura:

* centralizzata
* controllata
* con verifica server-side

---

## Architettura proposta

### Struttura logica

```
            INTERNET
                |
           Firewall UTM
                |
           Core Switch L3
                |
     ---------------------------
     |            |            |
 Web Server   DB Server     Storage
     |
 VPN/MPLS cittadina
     |
 Access Point POI
     |
   Minitablet
```

---

### Motivazioni delle scelte

**Centralizzazione server nel CED comunale**

Perché:

* maggiore sicurezza fisica
* continuità elettrica (UPS)
* backup centralizzato
* aggiornamento contenuti semplificato
* costi inferiori rispetto a server distribuiti

---

### Caratteristiche server

**Web Server (cluster HA)**

* Linux
* Nginx/Apache
* HTTPS obbligatorio
* Reverse proxy

**DB Server dedicato**

* PostgreSQL/MySQL
* RAID 1 o 10
* Backup giornaliero

**Storage NAS**

* RAID 5/6
* Collegamento 10Gb interno
* Archiviazione contenuti multimediali

---

## 1.b Comunicazione server-dispositivi

### Protocollo

* HTTPS (HTTP + TLS)
* Autenticazione applicativa
* Sessione server-side

Motivazione:

* protezione password giornaliera
* protezione contenuti
* prevenzione MITM

---

### Flusso autenticazione

1. Inserimento password
2. Verifica:

   * esistenza
   * data valida
   * tariffa
3. Creazione sessione
4. Token associato a minitablet

Il token è salvato lato server.

---

## 1.c Limitazione fruizione solo presso POI

Si adottano tre livelli combinati:

### 1. Controllo rete (VLAN dedicate per POI)

Ogni POI:

* Access Point dedicato
* VLAN separata
* Subnet distinta

Il server verifica IP sorgente.

---

### 2. Geofencing GPS

Il minitablet invia coordinate.

Il server verifica:

* distanza tra utente e POI

Formula distanza approssimata (Haversine semplificata):

Accesso consentito se d ≤ 30 m.

---

### 3. Beacon BLE

Identificatore beacon verificato lato server.

Soluzione raccomandata: WiFi + GPS.

---

# 2) Progetto base di dati

## Modello concettuale (E-R)

Entità:

* VISITATORE
* BIGLIETTO
* TARIFFA
* POI
* CONTENUTO
* LINGUA
* ACCESSO

Relazioni:

* VISITATORE acquista BIGLIETTO
* BIGLIETTO ha TARIFFA
* POI ha CONTENUTI
* BIGLIETTO effettua ACCESSI

---

## Modello logico

### TARIFFA

* id_tariffa (PK)
* nome
* max_poi_avanzati

### BIGLIETTO

* id_biglietto (PK)
* password
* data_validita
* id_tariffa (FK)

### POI

* id_poi (PK)
* nome
* latitudine
* longitudine

### CONTENUTO

* id_contenuto (PK)
* id_poi (FK)
* tipo
* lingua
* url_video

---

# 3) Progettazione pagina web (tariffa base)

Esempio PHP:

```
<?php
session_start();
if(!isset($_SESSION['id_biglietto'])){
    header("Location: login.php");
    exit();
}

$id_poi = $_GET['poi'];
$conn = new mysqli("localhost","user","pass","db");

$query = "SELECT url_video FROM contenuto
          WHERE id_poi=? AND tipo='base' LIMIT 1";

$stmt = $conn->prepare($query);
$stmt->bind_param("i",$id_poi);
$stmt->execute();
$res = $stmt->get_result();
$row = $res->fetch_assoc();
?>

<video controls>
    <source src="<?php echo $row['url_video']; ?>" type="video/mp4">
</video>
```

---

# 4) Gestione fasce tariffarie

## Tariffa Base

Solo contenuti base.

## Tariffa Intermedia

Tabella BIGLIETTO_POI_AVANZATI:

* id_biglietto
* id_poi

Max 3 record.

## Tariffa Piena

Nessun limite.

---

# SECONDA PARTE

---

# Quesito I – Media voti

## Integrazione DB

COMMENTO

* id_commento
* id_poi
* voto (1–5)
* testo

---

## Media voti

Query SQL:

```
SELECT p.nome, AVG(c.voto) as media
FROM poi p
JOIN commento c ON p.id_poi=c.id_poi
GROUP BY p.id_poi;
```

---

# Quesito II – Dispositivi personali

## Ipotesi 1 – Solo minitablet

Soluzioni:

* MAC filtering
* certificato client installato su tablet
* autenticazione tramite MDM
* blocco user-agent

Soluzione robusta: certificato client TLS.

---

## Ipotesi 2 – Consentire smartphone personali

Integrazione:

1. Associare biglietto a un solo device ID
2. Generare QR code su biglietto
3. Registrazione dispositivo
4. Token associato a IMEI o device fingerprint
5. Geofencing mantenuto

Limitare:

* un solo dispositivo per biglietto
* scadenza giornaliera

---

# Quesito III – Sicurezza DBMS

Obiettivo:

Limitare accesso dati in base al ruolo.

---

## Strumenti DBMS

* CREATE USER
* GRANT
* REVOKE
* ROLE
* VIEW
* Stored Procedure

---

## Esempio (PostgreSQL)

Creazione ruolo segreteria alunni:

```
CREATE ROLE segreteria_alunni;
GRANT SELECT, INSERT ON studenti TO segreteria_alunni;
REVOKE ALL ON docenti FROM segreteria_alunni;
```

Creazione utente:

```
CREATE USER mario PASSWORD 'pwd';
GRANT segreteria_alunni TO mario;
```

---

## Uso VIEW

```
CREATE VIEW elenco_studenti AS
SELECT nome, cognome FROM studenti;
```

Concessione solo sulla view:

```
GRANT SELECT ON elenco_studenti TO segreteria_alunni;
```

---

Principi applicati:

* Least privilege
* Separazione dei ruoli
* Minimizzazione accesso dati

---

# Quesito IV – Accesso remoto e VPN

## Scenario

* 2 sedi operative
* agenti commerciali mobili

---

## 1. VPN Site-to-Site

Protocollo: IPsec

Funzionamento:

* tunnel cifrato tra firewall sedi
* routing interno condiviso

Vantaggi:

* rete unica logica
* sicurezza elevata

---

## 2. VPN Remote Access

Agenti:

* client VPN SSL
* autenticazione 2FA
* IP virtuale assegnato

Flusso:

1. Connessione Internet
2. Autenticazione
3. Tunnel cifrato
4. Accesso a server interno

---

## Protocolli

* IPsec
* OpenVPN
* WireGuard
* SSL VPN

---

## Sicurezza aggiuntiva

* MFA
* VLAN separate
* Logging centralizzato
* Firewall applicativo

---

# Aree tematiche coinvolte

1. Architetture client-server
2. Progettazione reti LAN/WAN
3. VLAN e segmentazione
4. Geolocalizzazione e geofencing
5. HTTPS e TLS
6. Certificati digitali
7. Modellazione E-R
8. Progettazione basi dati relazionali
9. Linguaggio SQL
10. Sicurezza DBMS
11. Gestione ruoli e privilegi
12. Programmazione Web server-side
13. Media e funzioni aggregate SQL
14. VPN site-to-site
15. VPN remote access

---
