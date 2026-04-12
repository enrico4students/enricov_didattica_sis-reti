# **IEEE 802.3ab** 

standard Ethernet che definisce il funzionamento del **Gigabit Ethernet su cavo in rame**.

Nome completo:
**1000BASE-T** (definito da IEEE nel 1999 come estensione dello standard Ethernet 802.3)

---

## Cosa definisce

Lo standard 802.3ab specifica:

* Velocità: **1000 Mbit/s (1 Gbit/s)**
* Mezzo trasmissivo: **cavo in rame a doppino intrecciato (twisted pair)**
* Connettore: **RJ-45**
* Distanza massima: **100 metri**
* Modalità: **full-duplex**

---

## Come funziona (in modo semplice)

A differenza del Fast Ethernet (100BASE-TX), che usa solo 2 coppie del cavo,
**1000BASE-T utilizza tutte e 4 le coppie** del cavo Ethernet.

Ogni coppia:

* trasmette e riceve dati contemporaneamente
* lavora in entrambe le direzioni (full-duplex reale)

Per raggiungere 1 Gbit/s su rame:

* utilizza una modulazione chiamata **PAM-5**
* divide i dati sulle 4 coppie
* usa tecniche di cancellazione dell’eco per separare trasmissione e ricezione

---

## Cavi richiesti

Minimo richiesto:

* **Categoria 5e (Cat5e)**

Funziona anche con:

* Cat6
* Cat6a

Non è garantito con Cat5 standard.

---

## Dove viene usato

È lo standard più diffuso nelle LAN aziendali e domestiche per:

* collegare PC agli switch
* collegare switch tra loro (se non si usa fibra)
* collegare server di piccole/medie dimensioni

È lo standard “classico” delle porte Gigabit Ethernet degli switch aziendali.

---

## Differenza rispetto ad altri standard Gigabit

* 802.3z → Gigabit su **fibra ottica**
* 802.3ab → Gigabit su **rame (RJ-45)**

---

## Riassunto

IEEE 802.3ab =
Gigabit Ethernet (1000 Mbps) su cavo in rame fino a 100 metri, usando tutte e 4 le coppie del cavo.

È lo standard che permette alla maggior parte delle reti moderne di funzionare a 1 Gbit/s tramite normali cavi Ethernet RJ-45.
