
# Architetture di rete aziendali reali

Nelle aziende di dimensioni medio-grandi la rete è progettata seguendo un **modello gerarchico**.
Questo modello divide la rete in livelli con ruoli diversi per ottenere:

* scalabilità
* prestazioni prevedibili
* alta affidabilità
* facilità di gestione

Il modello più diffuso è il **modello a tre livelli**:

* Access layer
* Distribution layer
* Core layer

Questo approccio è usato nelle cosiddette **campus network**, cioè reti aziendali con uno o più edifici e centinaia o migliaia di utenti. ([NetworkLessons.com][1])

---

# 1. Schema generale di una rete aziendale reale

Schema tipico:

```
Internet
   |
   |
Router ISP / Edge router
   |
   |
Firewall aziendale
   |
   |
Core switch
   |
Distribution switch
   |
Access switch
   |
Dispositivi utenti
```

A questo si aggiungono spesso:

* **DMZ** per i server pubblici
* **server interni**
* **Wi-Fi aziendale e guest**

---

# 2. Router più esterno (edge router)

## Ruolo reale

Il router più esterno è spesso chiamato **edge router**.

Il suo compito principale è:

* collegare la rete aziendale al provider Internet
* gestire protocolli WAN
* scambiare rotte con l’ISP

Gli edge router collegano le reti interne con le reti del provider o con Internet. ([Allied Telesis][2])

---

## Fa routing su molte reti interne?

Nella maggior parte dei casi **no**.

Nelle reti moderne l’edge router:

* gestisce la **connettività WAN**
* non conosce le singole VLAN interne

Tipicamente vede solo:

```
rete aziendale
rete ISP
```

Ad esempio:

```
10.0.0.0/16  → rete aziendale
0.0.0.0/0    → ISP
```

Il router quindi **non gestisce direttamente le VLAN interne**.

Il routing interno è svolto da:

* firewall
* distribution switch
* core switch

---

## Quando invece fa routing complesso

In alcune aziende grandi il router può:

* terminare più connessioni ISP
* usare BGP
* gestire più reti pubbliche

Questo succede soprattutto quando l’azienda ha:

* Autonomous System
* collegamenti multipli a Internet
* data center grandi.

---

# 3. Firewall aziendale

## Il firewall è quasi sempre inline

Nelle reti moderne il firewall è **quasi sempre inline**. Questo significa che **tutto il traffico passa attraverso il firewall**.

Schema tipico:

```
Internet
   |
Router ISP
   |
Firewall
   |
LAN
```

Il firewall quindi è il **punto di controllo principale**.

---

## Il firewall fa routing?

Quasi sempre **sì**.

Il firewall collega più reti:

* WAN
* LAN
* DMZ
* eventuali reti interne separate

Esempio:

```
porta 1 → WAN
porta 2 → LAN
porta 3 → DMZ
porta 4 → rete guest
```

Poiché collega reti diverse, il firewall mantiene una **tabella di routing** e inoltra i pacchetti tra queste reti.

La differenza rispetto a un router è che prima applica:

* policy di sicurezza
* filtraggio
* ispezione del traffico.

---

## Architettura tipica con DMZ

```
Internet
   |
Router ISP
   |
Firewall
 |     |
LAN   DMZ
```

DMZ = rete per server pubblici:

* web server
* reverse proxy
* mail gateway

---

# 4. Core switch

Il **core switch** è il cuore della rete interna.

NB Il core switch **non** è il “coordinatore” o il router della rete. Il suo ruolo è:

* fornire una dorsale ad altissima velocità
* collegare i distribution switch
* trasportare grandi volumi di traffico

Il core deve essere:

* molto veloce
* ridondante
* con latenza minima

Le connessioni sono tipicamente:

* 10 Gbit
* 40 Gbit
* 100 Gbit.

Il core layer costituisce il backbone della rete e collega i vari segmenti distribuiti. ([Wikipedia][3])

NB Il core normalmente non implementa policy complesse.  
Linee guida classiche di progettazione:  
- evitare ACL sul core  
- evitare NAT  
- evitare filtri complessi  
- mantenere il core semplice e veloce  


---

# 5. Distribution switch

Il **distribution layer** è il livello intermedio.

Funzioni principali:

* aggregare gli access switch
* effettuare **routing** tra VLAN (cioè tra reti, di solito 1 vlan corrisponde a una (sotto) rete IP)
* applicare policy (ACL, QoS)
* isolare domini di broadcast

In molte reti aziendali il **routing tra VLAN avviene proprio qui** e il vero punto di controllo logico è il distribution layer.

Qui si trovano tipicamente:  
- routing tra VLAN  
- ACL  
- policy di rete  
- QoS  
- talvolta firewall interni  

Per questo motivo in molti testi Cisco il distribution layer è chiamato: policy layer


Esempio:

```
VLAN 10 → utenti
VLAN 20 → server
VLAN 30 → VoIP
VLAN 40 → guest
```

Il distribution switch possiede interfacce virtuali:

```
interface vlan 10 → gateway utenti
interface vlan 20 → gateway server
```

Il traffico tra VLAN passa da qui.

---

# 6. Access switch

Gli **access switch** sono quelli collegati direttamente ai dispositivi finali.

Dispositivi tipici:

* PC
* telefoni VoIP
* stampanti
* access point Wi-Fi
* videocamere IP

Funzioni principali:

* assegnazione VLAN
* PoE
* sicurezza delle porte.


---  
# 6 bis Errori frequenti  

---

### Errore: Pensare che il router esterno gestisca tutta la rete interna

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

### Errore: Pensare che tutte le VLAN passino dal router

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

### Errore: Pensare che il firewall sia sempre separato dal routing

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

### Errore: credere che tutte le VLAN attraversino tutta la rete

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

# 7. Varianti reali dell’architettura

Non tutte le reti hanno tre livelli.

---

## Architettura a due livelli

Molto comune nelle aziende medie.

```
Internet
   |
Firewall
   |
Core / Distribution (unico livello)
   |
Access switch
```

Qui **core e distribution coincidono**.

---

## Architettura con firewall centrale

Molte aziende fanno passare **anche il traffico interno tra VLAN attraverso il firewall**.

Schema:

```
Access switch
   |
Core switch
   |
Firewall
   |
Core switch
```

Questo permette:

* controllo di sicurezza tra VLAN
* segmentazione più forte.

---

## Architettura con routing sugli switch

Nelle reti moderne è comune che:

* gli switch facciano routing
* il firewall faccia solo sicurezza.

Esempio:

```
Access → Distribution (routing VLAN) → Core → Firewall → Internet
```

---

# 8. Chi fa veramente routing nella rete aziendale

Riassunto realistico:

| dispositivo         | routing                   |
| ------------------- | ------------------------- |
| router ISP          | routing verso Internet    |
| firewall            | routing tra WAN, LAN, DMZ |
| core switch         | routing backbone          |
| distribution switch | routing tra VLAN          |
| access switch       | raramente routing         |

---

# 9. Routing interno tipico

Il routing interno usa protocolli come:

* OSPF
* IS-IS
* talvolta BGP interno

I router aziendali possono anche scambiare rotte con ISP usando **BGP**. ([Wikipedia][4])

---

# 10. Architettura realistica completa

Schema semplificato:

```
                Internet
                    |
                Edge Router
                    |
                 Firewall
                    |
                Core Switch
                /        \
       Distribution1   Distribution2
          /    \           /     \
      Access  Access    Access  Access
       PC      AP        PC      VoIP
```

---

# 11. Punti fondamentali da ricordare   

1. Il router più esterno **non gestisce tutta la rete interna**.

2. Il firewall **è quasi sempre inline**.

3. Il firewall **spesso fa routing tra le zone**.

4. Il routing tra VLAN **avviene normalmente sugli switch Layer 3**.

5. Il modello core-distribution-access serve a rendere la rete **scalabile e gestibile**.


---   


[1]: https://networklessons.com/network-fundamentals/cisco-campus-network-design-basics?utm_source=chatgpt.com "Cisco Campus Network Design Basics"
[2]: https://www.alliedtelesis.com/us/en/foundations/what-network-router?utm_source=chatgpt.com "What is a network router?"
[3]: https://en.wikipedia.org/wiki/Hierarchical_internetworking_model?utm_source=chatgpt.com "Hierarchical internetworking model"
[4]: https://en.wikipedia.org/wiki/Router_%28computing%29?utm_source=chatgpt.com "Router (computing)"
