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

Se si desidera, è possibile aggiungere una sezione su come SD-WAN combina concetti MPLS e IPsec e perché oggi viene considerata l’evoluzione architetturale delle WAN aziendali.
