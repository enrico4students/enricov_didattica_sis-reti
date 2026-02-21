# Concetti base  

---

## 1. ADSL

ADSL significa **Asymmetric Digital Subscriber Line**.

Caratteristiche principali:

* utilizza il doppino telefonico in rame
* connessione asimmetrica (download maggiore dell’upload)
* fortemente influenzata dalla distanza dalla centrale

Prestazioni tipiche:

* download fino a circa 20 Mbit/s (in condizioni ideali)
* upload fino a circa 1 Mbit/s
* latenza relativamente elevata rispetto alla fibra

Limiti:

* velocità limitata
* degrado significativo oltre pochi chilometri
* tecnologia oggi superata dove è disponibile la fibra

---

## 2. Fibra ottica

La fibra trasmette dati tramite impulsi luminosi in un cavo in vetro o plastica.

Vantaggi generali:

* velocità molto elevate
* bassa latenza
* maggiore stabilità
* minore attenuazione rispetto al rame

---

## 3. FTTC (Fiber To The Cabinet)

Struttura:

* fibra fino all’armadio stradale
* ultimo tratto in rame fino all’abitazione

Tecnologia tipica:

* VDSL o VDSL2 sull’ultimo tratto

Prestazioni realistiche:

* download: 30–200 Mbit/s (dipende dalla distanza dall’armadio)
* upload: 10–30 Mbit/s
* latenza inferiore all’ADSL ma superiore alla FTTH

Fattore critico:

* più si è lontani dall’armadio, più la velocità diminuisce
* il tratto in rame resta un collo di bottiglia

Quando ha senso:

* aree dove non è disponibile la fibra completa
* buon compromesso tra costo e prestazioni

---

## 4. FTTH (Fiber To The Home)

Struttura:

* fibra ottica fino all’interno dell’abitazione
* nessun tratto finale in rame

Prestazioni tipiche:

* download: 300 Mbit/s, 1 Gbit/s o superiore
* upload: spesso 100 Mbit/s – 1 Gbit/s
* latenza molto bassa

Caratteristica importante:

* le prestazioni non dipendono in modo significativo dalla distanza urbana
* maggiore stabilità nel tempo

Quando ha senso:

* streaming ad alta definizione
* smart working
* gaming online
* trasferimento di file di grandi dimensioni
* utilizzo simultaneo da parte di più dispositivi

---

## 5. Confronto sintetico delle prestazioni

ADSL:

* velocità bassa
* upload molto limitato
* latenza più alta

FTTC:

* velocità medio-alta
* dipende dalla distanza dall’armadio
* buon compromesso

FTTH:

* velocità molto alta
* upload elevato
* latenza bassa
* soluzione più performante disponibile oggi

---

## Conclusione

ADSL è una tecnologia su rame con limiti strutturali.
FTTC migliora le prestazioni ma mantiene un tratto in rame.
FTTH elimina il rame e rappresenta la soluzione più veloce, stabile e adatta alle esigenze moderne.


<hr/>  

# Connettività Internet aziendale in Europa – Tecnologie di accesso  
<br/>
<br/>

La connettività aziendale europea si basa principalmente su: **linee dedicate in fibra (FTTO / leased line)**, **FTTH/GPON**, **VDSL (FTTC)**, **DOCSIS**, e soluzioni **4G/5G business**.
La scelta dipende da budget, necessità di banda simmetrica, SLA e continuità operativa.

---

# 1. Linee dedicate in fibra (FTTO / Leased Line)

Questa è la soluzione tipicamente enterprise.

## FTTO (Fiber To The Office)

Fibra dedicata fino alla sede aziendale.

### Velocità tipiche

* 100 Mbps simmetrici
* 1 Gbps simmetrico
* 10 Gbps su richiesta

## Leased Line / Fibra dedicata L2/L3

Collegamento punto-punto o accesso Internet con banda garantita.

### Velocità tipiche

* 10 Mbps – 10 Gbps simmetrici
* Banda garantita 100%
* SLA elevati (99.9%–99.99%)

### Caratteristiche

* Banda simmetrica
* IP pubblici statici
* Bassa latenza
* SLA contrattuale
* Monitoraggio H24

### Casi d’uso

* Data center
* Sedi corporate
* Server esposti pubblicamente
* VPN site-to-site critiche
* VoIP enterprise
* Applicazioni finanziarie o industriali

### Differenza chiave rispetto FTTH

* FTTH = banda condivisa, best effort
* Leased line = banda dedicata, garantita, simmetrica

---

# 2. FTTH – GPON (fibra fino alla sede)

### Tecnologia

Fibra ottica passiva fino all’edificio aziendale.

### Velocità tipiche (Europa 2024–2026)

* 1 Gbps download / 300–1000 Mbps upload
* 2.5 Gbps su offerte business avanzate
* Latenza molto bassa (<10 ms verso rete ISP)

### Casi d’uso

* PMI moderne
* Aziende cloud-centric
* Backup remoto
* VPN e smart working
* Videoconferenze intensive

### Caratteristiche

* Alta stabilità
* Banda elevata
* Upload adeguato ma spesso asimmetrico

---

# 3. VDSL – FTTC (rame ultimo tratto)

### Tecnologia

Fibra fino all’armadio stradale, ultimo tratto su rame.

### Velocità tipiche

* 50–200 Mbps download
* 10–30 Mbps upload
* Latenza 15–30 ms tipica

### Casi d’uso

* Piccoli studi professionali
* Uffici in zone non raggiunte da FTTH
* Linea secondaria di backup

### Limiti

* Prestazioni dipendenti dalla distanza
* Upload limitato

---

# 4. DOCSIS – rete via cavo (HFC)  
Diffuso in USA,presente e operativo in Europa, ma meno rispetto agli Stati Uniti, in progressiva sostituzione con FTTH, adatto a PMI urbane con traffico prevalentemente in download

### Tecnologia

Fibra + coassiale (Hybrid Fiber Coaxial).

### Velocità tipiche

* 300 Mbps – 1 Gbps download
* 20–100 Mbps upload
* Banda condivisa tra utenti dello stesso nodo

### Casi d’uso

* PMI urbane
* Studi con traffico prevalentemente in download
* Soluzione alternativa a FTTC

### Limiti

* Upload asimmetrico
* Prestazioni variabili in ore di punta

---

# 5. 4G / 5G Business

### Tecnologia

Accesso radio mobile tramite rete cellulare LTE (4G) o NR (5G).

### Velocità tipiche

* 4G: 30–150 Mbps download / 10–50 Mbps upload
* 5G: 100 Mbps – 1 Gbps download / 50–200 Mbps upload
* Latenza variabile (10–40 ms in 5G buone condizioni)

### Caratteristiche

* Installazione rapida
* Nessuna posa di cavi
* Prestazioni dipendenti da copertura e congestione radio

### Casi d’uso

* Linea di backup (failover)
* Sedi temporanee
* Cantieri, eventi
* Piccole filiali
* Ridondanza per continuità operativa

---

# Confronto sintetico

| Tecnologia         | Banda       | Simmetria | SLA         | Uso tipico           |
| ------------------ | ----------- | --------- | ----------- | -------------------- |
| FTTO / Leased line | Molto alta  | Sì        | Alto        | Aziende enterprise   |
| FTTH GPON          | Alta        | Parziale  | Medio       | PMI                  |
| VDSL               | Media-bassa | No        | Basso       | Piccoli uffici       |
| DOCSIS             | Media-alta  | No        | Medio       | PMI urbane           |
| 4G/5G              | Variabile   | Parziale  | Basso-Medio | Backup / sedi mobili |

---

# Considerazioni progettuali

In Europa, scenario tipico aziendale:

* PMI → FTTH + linea secondaria 4G/5G
* Azienda medio-grande → Leased line primaria + FTTH backup
* Enterprise multi-sede → MPLS o SD-WAN su linee dedicate

La scelta della tecnologia influisce direttamente su:

* continuità operativa
* qualità servizi cloud
* latenza applicativa
* resilienza infrastrutturale
