
---

# Tecnologie di accesso a Internet

## Fondamenti, architetture e soluzioni operative

---

# 1. Livelli di classificazione delle tecnologie di accesso

Per comprendere correttamente le tecnologie di connettività è utile distinguere quattro livelli concettuali diversi.

## 1.1 Mezzo fisico di trasmissione

Indica il supporto utilizzato per trasportare i dati.

Principali mezzi:

rame
fibra ottica
cavo coassiale
radio (reti cellulari)

## 1.2 Architettura dell’accesso

Indica **fino a dove arriva la fibra o la rete dell’operatore**.

Esempi:  
FTTC  
FTTH  
FTTO  
reti HFC  

## 1.3 Tecnologia di rete

Indica **come i dati vengono trasmessi sulla rete**.

Esempi:  
ADSL
VDSL
GPON
XGS-PON
EPON
DOCSIS

## 1.4 Tipo di servizio

Indica **come l’operatore fornisce la connettività**.

Esempi:  
FTTH residenziale  
FTTH business  
leased line  
backup 4G/5G  

Separare questi livelli evita confusione tra concetti che spesso vengono mescolati.

---

# 2. Mezzi fisici di trasmissione

## 2.1 Rame (doppino telefonico)

Storicamente la rete Internet domestica utilizzava il **doppino telefonico**.  
Su questo mezzo sono state sviluppate tecnologie DSL.

### ADSL

ADSL significa Asymmetric Digital Subscriber Line.  

Caratteristiche principali:  
utilizza il doppino telefonico in rame
connessione asimmetrica
download maggiore dell’upload
prestazioni dipendenti dalla distanza dalla centrale

Prestazioni tipiche:  
download fino a circa 20 Mbit/s  
upload circa 1 Mbit/s  

Limiti:  
velocità limitata  
degrado rapido oltre pochi chilometri  
latenza relativamente elevata  

Questa tecnologia oggi è considerata **superata nelle aree raggiunte dalla fibra**.

---

## 2.2 Fibra ottica

La fibra ottica trasmette dati tramite **impulsi luminosi** all’interno di un filamento di vetro o plastica.  

Vantaggi principali:  
velocità molto elevate
bassa latenza
maggiore stabilità
minore attenuazione del segnale rispetto al rame

La fibra è oggi il mezzo principale per le nuove reti di accesso.

---

## 2.3 Cavo coassiale  

Il cavo coassiale è utilizzato nelle reti TV via cavo.  

In queste reti l’accesso Internet utilizza la tecnologia DOCSIS.  

La struttura della rete è tipicamente **HFC (Hybrid Fiber Coaxial)**:  
fibra fino a nodi di distribuzione  
coassiale fino agli utenti  

---

## 2.4 Radio (reti cellulari)

Le reti cellulari forniscono accesso Internet tramite collegamenti radio.

Tecnologie principali:  
4G LTE
5G NR

Sono utilizzate spesso come:
connessione primaria in zone isolate  
linea di backup aziendale  
connessione temporanea.  

---

# 3. Architetture di accesso alla rete

Questa classificazione descrive **dove arriva la fibra o la rete dell’operatore**.

---

## 3.1 FTTC – Fiber To The Cabinet

La fibra arriva fino all’armadio stradale.  
L’ultimo tratto verso l’abitazione utilizza il doppino in rame.  

Tecnologia tipica:  
VDSL o VDSL2.

Prestazioni realistiche:  
download 30–200 Mbit/s
upload 10–30 Mbit/s

Caratteristica importante:  
la velocità dipende dalla distanza dall’armadio.  
Il tratto in rame rappresenta un collo di bottiglia.  

---

## 3.2 FTTH – Fiber To The Home

La fibra ottica arriva direttamente all’abitazione o all’ufficio.

Non esiste tratto finale in rame.  

Prestazioni tipiche:  
300 Mbit/s  
1 Gbit/s  
velocità superiori con nuove tecnologie  

Caratteristiche:  
- latenza molto bassa  
- alta stabilità  
- prestazioni indipendenti dalla distanza urbana  

Applicazioni tipiche:  
- streaming  
- smart working  
- gaming online  
- trasferimento file pesanti  
- uso simultaneo di molti dispositivi  

---

## 3.3 FTTO – Fiber To The Office

È una variante dell’FTTH applicata alle aziende.

La fibra arriva direttamente alla sede aziendale.

Spesso viene utilizzata per:

linee dedicate
leased line
collegamenti con banda garantita.

---

## 3.4 Architettura HFC

Hybrid Fiber Coaxial.

Utilizzata nelle reti DOCSIS.

Struttura:

fibra fino a nodi di distribuzione
coassiale fino agli utenti.

---

# 4. Tecnologie utilizzate sulle reti in fibra

Quando la fibra arriva fino all’utente (FTTH o FTTO) devono essere utilizzate tecnologie specifiche per condividere la rete.

Le principali appartengono alla famiglia **PON (Passive Optical Network)** oppure alle reti **punto-punto Ethernet**.

---

## 4.1 GPON

GPON significa Gigabit Passive Optical Network.

È la tecnologia FTTH più diffusa.

Caratteristiche principali:  
- rete ottica passiva condivisa
- assenza di apparati alimentati tra centrale e utenti
- utilizzo di splitter ottici passivi

Una singola fibra viene suddivisa tra più utenti.

Componenti principali:
- OLT nella centrale operatore  
- splitter ottici  
- ONT presso il cliente  

Velocità teoriche:  
- 2.5 Gbit/s downstream  
- 1.25 Gbit/s upstream  

La banda è condivisa tra gli utenti dello stesso ramo.

---

## 4.2 XGS-PON

Evoluzione di GPON.

Velocità:  
- 10 Gbit/s downstream
- 10 Gbit/s upstream

Architettura identica a GPON.

Viene utilizzata per:  
- connessioni FTTH di nuova generazione  
- servizi business ad alta banda.  


---

## 4.3 EPON

Ethernet Passive Optical Network.

Standard IEEE 802.3ah.

Caratteristiche:

trasporto diretto di frame Ethernet
diffusione maggiore in Asia

Velocità tipiche:

circa 1 Gbit/s.

---

## 4.4 10G-EPON

Evoluzione di EPON.

Velocità:

fino a 10 Gbit/s.

Mantiene l’architettura PON condivisa.

---

## 4.5 Active Ethernet

Tecnologia alternativa alle PON.

Caratteristiche:

fibra dedicata per ogni utente
presenza di switch attivi nella rete
banda non condivisa

Velocità tipiche:

1 Gbit/s
10 Gbit/s

È utilizzata spesso in:

reti aziendali
reti metropolitane
alcune implementazioni FTTH.

---   
## 4.6 Confronto tra tecnologie ottiche

Tecnologia | Tipo rete | Velocità
--- | --- | ---
GPON | PON condivisa | 2.5 / 1.25 Gbit/s
XGS-PON | PON condivisa | 10 / 10 Gbit/s
EPON | PON condivisa | 1 Gbit/s
10G-EPON | PON condivisa | 10 Gbit/s
Active Ethernet | punto-punto | 1–10 Gbit/s


---

# 5. Dispositivi nelle reti in fibra

## 5.1 OLT

Optical Line Terminal.

È il dispositivo presente nella centrale dell’operatore che gestisce la rete GPON.

---

## 5.2 ONT

Optical Network Terminal.

Dispositivo installato presso il cliente.

Funzione:  
- terminare la fibra ottica  
- convertire il segnale ottico in Ethernet.  

Schema tipico:  
- operatore  
- OLT  
- rete GPON  
- splitter ottici  
- ONT presso cliente  
- router o firewall locale  

L’ONT può essere:  
- dispositivo separato  
- integrato nel modem/router.


---

## 5.3 ONU

Optical Network Unit.

Termine più generico. Spesso usato come sinonimo di ONT.

Storicamente:  
- ONU = dispositivo generico
- ONT = terminale utente finale.
  

---

## 5.4 Terminologia utilizzata dagli operatori
  
Termine | Significato
--- | ---
FTTH / GPON | ONT
FTTB / GPON | ONT o ONU
fibra punto-punto | NTU
terminologia generica | CPE (Customer Premises Equipment)

---

# 6. Soluzioni di connettività aziendale

Le aziende utilizzano diverse tecnologie di accesso a seconda delle esigenze.

---

## 6.1 Linee dedicate in fibra (FTTO / leased line)

Soluzione tipicamente enterprise.

Caratteristiche:  
- banda simmetrica
- banda garantita  
- IP pubblici statici  
- SLA contrattuali elevati  

Velocità tipiche:  
- 100 Mbps
- 1 Gbps  
- 10 Gbps  

Utilizzi:  
- data center  
- sedi corporate  
- VPN site-to-site  
- VoIP enterprise  
- applicazioni critiche  

Differenza principale rispetto FTTH:  
- FTTH → banda condivisa  
- leased line → banda dedicata.  

---

## 6.2 FTTH business (GPON)

Molte aziende utilizzano FTTH anche per attività professionali.

Velocità tipiche:

1 Gbit/s download
300–1000 Mbps upload

Caratteristiche:

alta banda
latenza bassa
costo relativamente contenuto.

Utilizzi:

PMI
cloud computing
backup remoto
smart working.

---

## 6.3 VDSL (FTTC)

Ancora utilizzata dove la fibra completa non è disponibile.

Velocità tipiche:

50–200 Mbps download
10–30 Mbps upload.

Utilizzi:

piccoli uffici
linee secondarie.

---

## 6.4 DOCSIS

Tecnologia Internet su rete via cavo.

Velocità tipiche:

300 Mbps – 1 Gbps download
20–100 Mbps upload

Banda condivisa tra utenti dello stesso nodo.

---

## 6.5 4G / 5G business

Accesso Internet tramite rete cellulare.

Velocità tipiche:

4G:

30–150 Mbps download

5G:

100 Mbps – 1 Gbps download.

Utilizzi principali:

backup automatico
sedi temporanee
cantieri
ridondanza di rete.

---

# 7. Confronto tra principali soluzioni di accesso

Tecnologia | Banda | Simmetria | SLA | Uso tipico
FTTO / leased line | molto alta | sì | alto | aziende enterprise
FTTH GPON | alta | parziale | medio | PMI
VDSL | media | no | basso | piccoli uffici
DOCSIS | medio-alta | no | medio | PMI urbane
4G/5G | variabile | parziale | basso | backup

---

# 8. Considerazioni progettuali

Scenario tipico in Europa:

PMI
FTTH primaria
backup 4G/5G

azienda medio-grande
leased line primaria
FTTH backup

enterprise multi-sede
MPLS o SD-WAN su linee dedicate.

La scelta della tecnologia influenza:

continuità operativa
latenza applicativa
prestazioni cloud
resilienza della rete.

---

Questa struttura elimina quasi tutte le duplicazioni perché:

GPON è spiegato una sola volta
FTTH è trattato prima come architettura e poi come servizio
FTTC compare una sola volta
le tecnologie ottiche sono raggruppate
le soluzioni aziendali sono separate dal livello tecnologico

e rende esplicita la gerarchia concettuale:

mezzo fisico → architettura → tecnologia → dispositivi → servizi → progettazione.
