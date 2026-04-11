
---

# ✔️ CHECKLIST OPERATIVA – VERSIONE “CORREZIONE MATURITÀ”

## 1. Architettura generale

1.1 Scelta architettura (2 layer / 3 layer)
Descrizione: definire struttura access–core oppure access–distribution–core
Criterio: corretto se coerente con dimensioni e complessità

1.2 Motivazione architettura
Descrizione: spiegare perché NON usare (o usare) il distribution layer
Criterio: premiante se motivazione tecnica (costo, complessità, inutilità)

1.3 Presenza firewall perimetrale
Descrizione: dispositivo tra LAN e Internet
Criterio: errore se assente

1.4 Posizione del firewall
Descrizione: tra Internet e rete interna (eventualmente con DMZ)
Criterio: corretto se posizione chiara e coerente

1.5 Presenza core switch
Descrizione: nodo centrale di aggregazione
Criterio: corretto se presente in reti medio-piccole

1.6 Collegamento Internet → firewall → core
Descrizione: flusso principale della rete
Criterio: errore se struttura non chiara o non realistica

---

## 2. VLAN e segmentazione

2.1 VLAN utenti interni
Descrizione: rete dedicata agli uffici
Criterio: errore se assente

2.2 VLAN server interni
Descrizione: rete separata per server
Criterio: corretto se distinta dagli utenti

2.3 VLAN ospiti
Descrizione: rete separata per guest
Criterio: errore grave se assente

2.4 VLAN management
Descrizione: rete per gestione apparati
Criterio: premiante se presente

2.5 VLAN DMZ
Descrizione: rete per server esposti
Criterio: corretto se presente quando serve

2.6 Coerenza numero VLAN
Descrizione: non troppe, non troppo poche
Criterio: premiante se bilanciato

2.7 Coerenza VLAN ↔ funzione
Descrizione: ogni VLAN ha ruolo chiaro
Criterio: errore se VLAN inutili o confuse

---

## 3. Piano di indirizzamento IP

3.1 Uso indirizzi privati
Descrizione: rete interna con RFC1918
Criterio: errore se IP pubblici usati senza motivo

3.2 Scelta blocco IP coerente
Descrizione: es. 10.10.0.0/16
Criterio: premiante se ordinato

3.3 Subnet per ogni VLAN
Descrizione: 1 VLAN = 1 subnet
Criterio: errore se non coerente

3.4 Gateway per ogni subnet
Descrizione: IP del router/firewall
Criterio: errore se mancante

3.5 Struttura leggibile
Descrizione: es. 10.10.X.0/24
Criterio: premiante

3.6 Assenza sovrapposizioni
Descrizione: subnet distinte
Criterio: errore grave se overlap

---

## 4. Posizionamento server

4.1 Ubicazione server WEB
Descrizione: in DMZ
Criterio: errore se in LAN interna

4.2 Ubicazione database
Descrizione: in rete interna protetta
Criterio: errore grave se in DMZ o pubblico

4.3 Separazione WEB / DB
Descrizione: front-end separato da back-end
Criterio: premiante

4.4 Posizionamento server interni
Descrizione: in VLAN server
Criterio: corretto se isolati

4.5 Posizionamento DHCP/DNS
Descrizione: coerente con rete interna
Criterio: corretto se realistico

---

## 5. Pubblicazione servizi (WEB)

5.1 Raggiungibilità server WEB
Descrizione: accessibile da Internet
Criterio: errore se non previsto

5.2 Metodo pubblicazione
Descrizione: NAT / port forwarding / reverse proxy
Criterio: corretto se concreto

5.3 Uso NAT per pubblicazione
Descrizione: DNAT o port forwarding
Criterio: corretto se coerente

5.4 Eventuale IP pubblico diretto
Descrizione: alternativa al NAT
Criterio: premiante se motivato

5.5 Apertura porte corrette
Descrizione: solo 80/443
Criterio: errore se troppo permissivo

---

## 6. Routing

6.1 Presenza inter-VLAN routing
Descrizione: comunicazione tra reti
Criterio: errore se assente

6.2 Posizione routing
Descrizione: firewall o switch L3
Criterio: corretto se coerente

6.3 Gateway coerente con routing
Descrizione: gateway = dispositivo di routing
Criterio: errore se incoerente

6.4 Presenza default route
Descrizione: verso Internet
Criterio: errore se mancante

6.5 Percorso traffico chiaro
Descrizione: client → gateway → firewall → Internet
Criterio: premiante se esplicito

---

## 7. NAT e accesso Internet

7.1 PAT per client interni
Descrizione: molti host → 1 IP pubblico
Criterio: corretto se presente

7.2 Distinzione NAT uscita / NAT ingresso
Descrizione: PAT vs port forwarding
Criterio: premiante se chiaro

7.3 Coerenza NAT ↔ firewall
Descrizione: NAT accompagnato da regole
Criterio: errore se isolato

---

## 8. Sicurezza e firewall

8.1 Regola Internet → WEB
Descrizione: consentire solo HTTP/HTTPS
Criterio: corretto se limitato

8.2 Regola WEB → DB
Descrizione: accesso su porta DB
Criterio: corretto se esplicito

8.3 Blocco Internet → DB
Descrizione: nessun accesso diretto
Criterio: errore grave se permesso

8.4 Blocco accesso ospiti → LAN
Descrizione: isolamento guest
Criterio: errore grave se non presente

8.5 Controllo traffico inter-VLAN
Descrizione: non tutto è libero
Criterio: premiante se filtrato

8.6 Protezione management
Descrizione: accesso limitato
Criterio: premiante

---

## 9. Switching e trunk

9.1 Porte access per host
Descrizione: PC su access
Criterio: errore se trunk

9.2 Trunk tra switch
Descrizione: trasporto VLAN
Criterio: corretto se presente

9.3 Trunk verso firewall/router
Descrizione: se routing centralizzato
Criterio: corretto se coerente

9.4 VLAN coerenti su più switch
Descrizione: propagate via trunk
Criterio: errore se incoerente

---

## 10. Wi-Fi

10.1 AP collegato a switch
Descrizione: integrazione LAN
Criterio: corretto

10.2 SSID interni / ospiti separati
Descrizione: due reti wireless
Criterio: errore se unico SSID

10.3 SSID → VLAN mapping
Descrizione: associazione logica
Criterio: premiante

10.4 Isolamento Wi-Fi ospiti
Descrizione: no accesso LAN
Criterio: errore grave se manca

---

## 11. Collegamenti sedi (se presenti)

11.1 Scelta tecnologia (VPN / radio)
Descrizione: soluzione plausibile
Criterio: corretto se realistico

11.2 Sicurezza collegamento
Descrizione: cifratura o isolamento
Criterio: premiante

11.3 Routing tra sedi
Descrizione: raggiungibilità subnet remote
Criterio: errore se assente

---

## 12. Schema e tabelle

12.1 Schema di rete presente
Descrizione: rappresentazione grafica
Criterio: premiante

12.2 Coerenza schema ↔ testo
Descrizione: stessi elementi
Criterio: errore se divergente

12.3 Tabella VLAN
Descrizione: VLAN, rete, funzione
Criterio: premiante

12.4 Tabella IP
Descrizione: subnet e gateway
Criterio: premiante

---

## 13. Verifica finale

13.1 Coerenza generale
Descrizione: tutte le parti funzionano insieme
Criterio: errore se contraddizioni

13.2 Funzionamento reale
Descrizione: rete implementabile
Criterio: premiante

13.3 Assenza errori gravi
Descrizione:

* DB esposto
* no VLAN
* no routing
* IP errati
  Criterio: penalizzazione forte

13.4 Motivazioni tecniche
Descrizione: spiegazione delle scelte
Criterio: premiante

---

# ✔️ Uso immediato in correzione

Metodo rapido:

* segnare ogni voce:

  * OK
  * PARZIALE
  * ERRATO

Oppure:

* assegnare:

  * 0 errore
  * 1 parziale
  * 2 corretto

---
