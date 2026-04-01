
---

### 1. Pensare che il router esterno gestisca tutta la rete interna

Molti studenti immaginano una rete aziendale come una rete domestica ingrandita:

```
Internet - Router - Switch - PC
```

Questo schema è **quasi sempre falso nelle reti professionali**.

Nelle aziende il router esterno normalmente:

* termina la connessione con l’ISP
* gestisce protocolli WAN
* inoltra il traffico verso la rete aziendale

Ma **non gestisce direttamente le VLAN interne**.

Molto spesso vede solo una o poche reti interne, ad esempio:

```
10.0.0.0/16 → rete aziendale
```

Il routing tra le VLAN interne avviene invece su:

* switch Layer 3
* firewall
* distribution switch

---

### 2. Pensare che tutte le VLAN passino dal router

Gli studenti spesso immaginano qualcosa del genere:

```
PC VLAN 10
      \
       Router
      /
PC VLAN 20
```

Questa configurazione esiste (router-on-a-stick), ma **non è quella più comune nelle reti medio-grandi**.

Nelle reti aziendali reali il routing tra VLAN viene quasi sempre fatto da:

* **switch Layer 3**

Esempio reale:

```
Access switch
      |
Distribution switch (routing VLAN)
      |
Core switch
```

Il router esterno **non è coinvolto nel traffico interno tra VLAN**.

---

### 3. Pensare che il firewall sia sempre separato dal routing

Un errore molto comune è credere che:

* il router faccia routing
* il firewall faccia solo filtraggio

Nelle reti moderne **il firewall fa quasi sempre anche routing**.

Schema reale tipico:

```
Internet
   |
Router ISP
   |
Firewall
 |   |
LAN  DMZ
```

Il firewall possiede più interfacce:

```
porta WAN
porta LAN
porta DMZ
```

Poiché queste appartengono a reti diverse, il firewall:

* mantiene una **tabella di routing**
* inoltra pacchetti tra queste reti
* applica **policy di sicurezza prima dell’inoltro**

Quindi il firewall è contemporaneamente:

* router
* filtro di sicurezza
* punto di controllo della rete.

---

### 4. Errore molto frequente: credere che tutte le VLAN attraversino tutta la rete

Gli studenti spesso immaginano VLAN estese ovunque:

```
VLAN 10
presente su tutti gli switch
```

In molte reti moderne invece si cerca di **limitare l’estensione delle VLAN**.

Motivi principali:

* ridurre i domini di broadcast
* migliorare la scalabilità
* semplificare il troubleshooting

Quindi è comune trovare:

```
piano 1 → VLAN 10
piano 2 → VLAN 20
piano 3 → VLAN 30
```

Il traffico tra queste VLAN viene gestito da routing.

---
