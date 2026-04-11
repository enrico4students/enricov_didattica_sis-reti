Di seguito la versione **corretta, completa e rigorosa per ambito professionale**, con tutte le precisazioni necessarie integrate.

---

# ✔️ Collegamento tipico (versione rigorosa)

Architettura reale (access layer):

* Access Point → collegato a **switch di accesso (managed)**
* Switch di accesso → collegato al **core di rete o al firewall perimetrale**

👉 Nota fondamentale:

* il **firewall perimetrale** è il dispositivo posto tra rete interna e ISP
* è tipicamente a valle dell’ONT/CPE del provider

👉 In architetture più strutturate:

* access switch → distribution/core switch → firewall

---

## ✔️ Ruolo dei dispositivi

### Switch di accesso (livello 2)

* collega dispositivi finali (AP, PC, telefoni IP)
* trasporta il traffico dati
* trasporta le VLAN tramite **trunk 802.1Q**
* può alimentare l’AP tramite **PoE (se supportato)**

❗ Nota:

* lo switch **non “gestisce da solo” le VLAN**, ma:

  * le trasporta (tagging)
  * applica configurazioni L2 (access/trunk, VLAN consentite)

---

### Access Point

* NON crea VLAN
* NON effettua routing IP
* NON assegna indirizzi IP
* associa ogni rete Wi-Fi (SSID) a una VLAN configurata

👉 Funzione reale:

* ponte tra rete wireless e rete cablata
* mapping **SSID → VLAN**

---

### Firewall / Router (da specificare)

Nel contesto professionale:

👉 si intende **firewall perimetrale**

* posizionato tra LAN e Internet
* collegato all’ONT/CPE ISP

Funzioni:

* routing tra VLAN (in architetture 2 layer) oppure solo verso Internet
* sicurezza (policy, filtering)
* NAT
* DHCP (spesso, ma non obbligatorio)

---

### Switch Layer 3 (se presente)

* routing tra VLAN (inter-VLAN routing)
* tipico in architetture a 3 layer o core avanzati

---

# ✔️ Come funzionano le VLAN sugli access point

## ❗ Punto fondamentale

L’access point **non rileva automaticamente le VLAN**.

👉 Le VLAN devono essere:

* definite nell’infrastruttura (switch / firewall / core)
* configurate esplicitamente nell’access point

---

## ✔️ Meccanismo reale

1. Lo switch collega l’AP tramite una porta configurata come:

   * **trunk 802.1Q**

2. Sul trunk transitano più VLAN (frame taggati)

3. L’access point:

   * riceve e invia traffico Ethernet con tag VLAN
   * non “sceglie” le VLAN automaticamente

4. Per ogni SSID:

   * si configura manualmente un **VLAN ID**

👉 Risultato:

* SSID → VLAN → rete IP

---

## ✔️ Come l’AP gestisce le VLAN

### 1) Associazione SSID → VLAN

Esempio:

* SSID "Ufficio" → VLAN 10
* SSID "Ospiti" → VLAN 20
* SSID "IoT" → VLAN 30

---

### 2) Tagging del traffico

Quando un client trasmette:

* il client **non è consapevole delle VLAN**
* l’AP:

  * incapsula il traffico
  * aggiunge il **tag VLAN (802.1Q)**

---

### 3) Invio allo switch

Il traffico:

* esce dall’AP sulla porta Ethernet
* con tag VLAN corretto
* lo switch inoltra nella VLAN appropriata

---

## ✔️ Sintesi tecnica corretta

* VLAN definite nell’infrastruttura
* AP configura mapping SSID → VLAN
* switch trasporta VLAN (L2)
* routing e IP gestiti da firewall o L3 switch

---

# ✔️ Esempio pratico reale (Ubiquiti UniFi)

## Scenario

* Switch managed UniFi (access layer)
* Access point UniFi (es. U6 Pro)
* Firewall perimetrale (es. UniFi Gateway o equivalente)

---

## ✔️ Obiettivo

Creare 3 reti Wi-Fi separate:

| SSID    | VLAN | Rete IP       |
| ------- | ---- | ------------- |
| Ufficio | 10   | 10.10.10.0/24 |
| Ospiti  | 20   | 10.10.20.0/24 |
| IoT     | 30   | 10.10.30.0/24 |

---

## ✔️ Configurazione passo-passo

### 1) Configurazione rete (firewall o L3)

Due possibili scenari:

#### Caso A (2 layer, tipico PMI)

* gateway e routing su firewall perimetrale

* VLAN 10 → 10.10.10.1

* VLAN 20 → 10.10.20.1

* VLAN 30 → 10.10.30.1

* DHCP attivo su firewall

---

#### Caso B (3 layer)

* routing su switch Layer 3

* firewall usato solo per traffico Internet

---

### 2) Configurazione switch (access layer)

Porta verso AP:

* modalità: **trunk 802.1Q**
* VLAN consentite: 10, 20, 30
* (opzionale) VLAN di management non taggata

---

### 3) Configurazione access point

Nel controller:

* SSID "Ufficio"

  * VLAN ID: 10

* SSID "Ospiti"

  * VLAN ID: 20

* SSID "IoT"

  * VLAN ID: 30

👉 L’AP applica il tagging VLAN in base alla configurazione

---

## ✔️ Cosa succede nella pratica

1. dispositivo si connette a SSID "Ospiti"
2. AP associa VLAN 20
3. traffico inviato con tag VLAN 20
4. switch inoltra nella VLAN 20
5. DHCP assegna IP 10.10.20.x
6. routing gestito da firewall o L3

---

# ✔️ Errori comuni (ambito professionale)

❌ Porta AP configurata come access → VLAN multiple non funzionano
❌ VLAN non configurata sull’AP → traffico errato
❌ DHCP assente → client senza IP
❌ Routing non configurato → VLAN isolate
❌ Ambiguità su “firewall” → progettazione incoerente

---

# ✔️ Differenza chiave da ricordare

* VLAN → livello 2 (trasporto su switch)
* IP → livello 3 (firewall o L3 switch)
* AP → associazione Wi-Fi ↔ VLAN
* firewall perimetrale → sicurezza e accesso Internet

---

# ✔️ Nota sulla classificazione della rete Wi-Fi

* SSID aziendale → rete interna (ma spesso segmentata e a fiducia limitata)
* SSID ospiti → rete esterna / non trusted

---

# ✔️ Sintesi finale (rigorosa)

Un access point professionale opera nell’access layer e si collega a uno switch managed tramite una porta trunk 802.1Q quando sono presenti più SSID associati a VLAN diverse. Le VLAN non sono rilevate automaticamente ma devono essere configurate esplicitamente sia nell’infrastruttura di rete sia nell’access point. L’AP associa ogni SSID a una VLAN e inserisce il traffico nella VLAN corretta, mentre il trasporto avviene tramite lo switch e il routing IP è gestito dal firewall perimetrale o da uno switch Layer 3, a seconda dell’architettura adottata.
