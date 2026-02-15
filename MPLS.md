---

# 12. MPLS oggi ha ancora senso?

Domanda molto importante.

Negli ultimi 15 anni l’uso di MPLS è stato messo in discussione dall’aumento di:

* banda Internet a basso costo
* affidabilità della connettività pubblica
* maturità di IPsec
* diffusione di SD-WAN

Tuttavia MPLS **non è scomparso**. È ancora utilizzato in molti contesti enterprise.

Per capire se ha senso, bisogna confrontare cosa offre realmente rispetto a IPsec.

---

# 13. Cosa IPsec può fare (e cosa no)

IPsec:

* cifra traffico
* autentica peer
* crea tunnel su qualunque rete IP
* funziona su Internet
* è relativamente economico

Ma IPsec:

* non garantisce qualità del servizio
* non controlla il percorso del traffico
* non garantisce latenza
* non garantisce jitter
* non garantisce perdita pacchetti
* dipende dalla qualità della rete sottostante

IPsec protegge.
Non controlla l’infrastruttura.

---

# 14. Cosa MPLS può fare che IPsec non può fare

MPLS offre caratteristiche strutturali di rete che IPsec non può fornire da solo.

## 14.1 Controllo del percorso (Traffic Engineering)

MPLS permette:

* definizione di Label Switched Path (LSP)
* controllo esplicito del percorso
* instradamento non solo “best path IP”

Questo consente:

* evitare congestioni
* bilanciare carico
* garantire latenza prevedibile

IPsec non controlla il routing Internet.

---

## 14.2 Qualità del Servizio (QoS) end-to-end

In una MPLS VPN il provider può:

* applicare classi di servizio
* riservare banda
* garantire priorità VoIP
* differenziare traffico critico

Con Internet + IPsec:

* il traffico è best effort
* il provider Internet non garantisce QoS reale tra città o paesi

Per VoIP mission critical questo è rilevante.

---

## 14.3 SLA contrattuali

Con MPLS il provider offre:

* SLA su latenza
* SLA su jitter
* SLA su perdita pacchetti
* monitoraggio continuo

Internet non offre SLA equivalenti (o li offre in modo molto limitato).

---

## 14.4 Scalabilità centralizzata

In grandi reti (100+ sedi):

MPLS L3 VPN:

* usa BGP
* separa VRF per cliente
* scala molto bene
* non richiede tunnel full mesh IPsec

IPsec classico:

* richiede gestione tunnel
* complessità cresce con il numero di sedi

SD-WAN oggi risolve in parte questo problema.

---

# 15. Quando MPLS ha ancora senso oggi

MPLS ha senso in:

1. Grandi aziende multi-sede
2. Settore bancario
3. Settore sanitario
4. Ambienti industriali
5. Reti con VoIP critico
6. Ambienti con compliance rigorosa
7. Backbone nazionali o internazionali

In questi casi servono:

* prestazioni garantite
* prevedibilità
* isolamento forte
* controllo del percorso

---

# 16. Quando IPsec (o SD-WAN) è preferibile

IPsec è preferibile in:

* PMI
* sedi piccole
* contesti con budget limitato
* ambienti cloud-first
* reti con traffico non real-time

Oggi molte aziende adottano:

```
Internet + IPsec
```

oppure
SD-WAN + IPsec

per ridurre costi rispetto a MPLS.

---

# 17. Tendenza attuale del mercato

Negli ultimi anni:

* molte aziende stanno riducendo MPLS
* adottano SD-WAN multi-link
* usano Internet broadband + backup LTE/5G
* cifrano tutto con IPsec o TLS

Ma:

MPLS non è obsoleto.
È meno diffuso rispetto al passato, ma ancora usato in reti critiche.

---

# 18. Conclusione tecnica finale

MPLS e IPsec non sono alternative dirette.

Sono tecnologie diverse:

MPLS:

* tecnologia di forwarding
* controlla rete
* garantisce QoS
* non cifra

IPsec:

* tecnologia di sicurezza
* cifra
* non controlla la rete sottostante

Domanda corretta non è:

“Meglio MPLS o IPsec?”

ma:

“Serve controllo di rete garantito o solo cifratura?”

Se serve:

* sicurezza → IPsec
* qualità garantita → MPLS
* entrambi → MPLS + IPsec

---

# cosa risolve MPS?Cosa si può fare con MPLS che non si può fare con lo stack TCP/IP +IPSEC ?

Domanda corretta e tecnica.
Risposta diretta: **MPLS risolve problemi di controllo del forwarding e di ingegneria del traffico che TCP/IP + IPsec non possono risolvere quando la rete sottostante non è controllata.**

Separiamo i piani.

---

# 1. Cosa risolve MPLS

MPLS nasce per risolvere tre problemi fondamentali nelle reti di grandi dimensioni:

1. Scalabilità del forwarding
2. Traffic engineering (controllo esplicito del percorso)
3. Separazione logica massiva (VPN carrier-grade)

Non nasce per cifrare.

---

# 2. Cosa si può fare con MPLS che non si può fare con TCP/IP + IPsec su Internet

La differenza chiave è questa:

IPsec lavora sopra una rete che non controlla.
MPLS è parte dell’infrastruttura di rete.

Vediamo i casi concreti.

---

## 2.1 Controllo deterministico del percorso (Traffic Engineering)

Con MPLS è possibile:

* Definire LSP (Label Switched Path) espliciti
* Forzare il traffico su un percorso specifico
* Evitare link congestionati
* Separare traffico critico su percorsi dedicati

Con IPsec su Internet:

* Il percorso è deciso dal routing BGP globale
* Non si può imporre il cammino
* Non si può evitare una dorsale congestionata
* Non si può garantire latenza costante

Questo è un limite strutturale.

---

## 2.2 QoS reale end-to-end

In una rete MPLS il provider può:

* Applicare classi di servizio
* Riservare banda
* Garantire priorità al VoIP
* Limitare jitter
* Applicare policing coerente su tutta la rete

Con Internet + IPsec:

* Il traffico è best effort
* Il DSCP può essere ignorato dai provider
* Nessuna garanzia contrattuale su jitter o perdita

IPsec cifra, ma non può imporre QoS globale.

---

## 2.3 SLA garantiti

Con MPLS il provider può contrattualmente garantire:

* Latenza massima tra sedi
* Jitter massimo
* Packet loss massimo
* Disponibilità percentuale

Internet non fornisce SLA equivalenti su scala geografica ampia.

IPsec non può trasformare Internet in rete deterministica.

---

## 2.4 VPN su larga scala (Carrier-grade L3 VPN)

MPLS + BGP permette:

* VRF separate per migliaia di clienti
* Isolamento completo delle routing table
* Scalabilità molto alta

Un ISP può gestire decine di migliaia di VPN.

IPsec classico:

* Richiede tunnel
* Richiede gestione chiavi
* Cresce in complessità con il numero di siti
* Non è progettato per carrier multi-tenant massivi

---

## 2.5 Fast Reroute (convergenza rapidissima)

Con MPLS Fast Reroute:

* Ripristino in decine di millisecondi
* Inferiore a molte convergenze IP tradizionali

Internet + IPsec:

* Dipende dalla convergenza BGP
* Può richiedere secondi
* Non è deterministico

In ambienti finanziari questo è critico.

---

# 3. Cosa MPLS NON può fare

MPLS non può:

* Cifrare traffico
* Garantire riservatezza
* Sostituire IPsec per sicurezza crittografica

Se serve cifratura, serve IPsec o TLS sopra MPLS.

---

# 4. Sintesi tecnica netta

TCP/IP + IPsec può:

* Cifrare
* Autenticare
* Funzionare ovunque ci sia IP

Ma non può:

* Controllare il percorso Internet
* Garantire QoS geografica
* Offrire SLA deterministici
* Gestire separazione massiva carrier-grade
* Applicare traffic engineering core-network

MPLS può fare queste cose perché è dentro la rete.

---

# 5. Conclusione precisa

MPLS risolve problemi di:

* Ingegneria del traffico
* Scalabilità operatore
* Prestazioni deterministiche
* Isolamento multi-tenant su larga scala

IPsec risolve problemi di:

* Sicurezza crittografica

Non sono alternative.
Sono strumenti per livelli diversi del problema.

Se la rete è solo Internet pubblica, MPLS non è applicabile.
Se si gestisce un backbone o una WAN carrier-grade, TCP/IP + IPsec non è sufficiente per gli stessi obiettivi.

