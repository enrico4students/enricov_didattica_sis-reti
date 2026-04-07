Un firewall “Layer 2”, come può analizzare IP (Layer 3)?

La chiave è questa:

**“Transparent” descrive il modo in cui è inserito in rete, non il livello massimo che può ispezionare.**

---

# 1. Come fa un firewall transparent a esaminare il livello IP

Un firewall in modalità trasparente funziona come un **bridge Ethernet (Layer 2)**:

* riceve frame Ethernet
* non modifica indirizzi IP
* non è gateway
* inoltra i frame tra due segmenti

Ma internamente non si limita a guardare il MAC.

## Cosa succede realmente

Quando riceve un frame Ethernet:

1. Legge l’intestazione Ethernet (MAC sorgente/destinazione)
2. Analizza il payload del frame
3. Se il payload è un pacchetto IP:

   * estrae header IP
   * legge IP sorgente/destinazione
   * legge protocollo (TCP/UDP/ICMP)
   * può leggere porte TCP/UDP
   * può fare DPI (se NGFW)

Quindi:

* È **inserito a livello 2**
* Ma può **ispezionare fino a Layer 7**

Non serve essere router per leggere un pacchetto IP.
Serve solo poter accedere al contenuto del frame.

---

# 2. Come blocca il traffico pericoloso

Il firewall transparent può:

* Droppare il frame prima di inoltrarlo
* Resettare la sessione TCP
* Bloccare specifiche firme IPS
* Bloccare per IP, porta, applicazione, URL

## Processo semplificato

Frame arriva →
Analisi MAC →
Analisi IP →
Applicazione policy →

Se consentito → inoltro
Se vietato → drop

Dal punto di vista dei dispositivi ai lati, il firewall è “invisibile” a livello IP, ma filtra attivamente il traffico.

---

# 3. Perché non serve routing per filtrare

Il routing serve a:

* decidere quale interfaccia usare per inoltrare un pacchetto verso una rete diversa

Ma per filtrare basta:

* ricevere il traffico
* analizzarlo
* decidere se inoltrarlo o no

Un bridge può farlo perfettamente.

---

# 4. Esempio concreto

Architettura:

CPE
→ Firewall (transparent)
→ Switch

Il gateway IP resta il router a monte.

Il firewall:

* non assegna IP
* non cambia subnet
* non fa default gateway

Ma può bloccare:

* traffico da IP blacklist
* scansioni di porte
* exploit
* traffico verso server non autorizzati

---

# 5. Sintesi tecnica

Un firewall transparent:

* È Layer 2 dal punto di vista topologico
* È Layer 3/4/7 dal punto di vista ispettivo
* Non instrada traffico
* Può filtrare come un firewall routed

La modalità (routed vs transparent) riguarda l’architettura di rete.
Il tipo di ispezione riguarda il motore di sicurezza.
