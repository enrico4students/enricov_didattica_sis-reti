
---

# ✔️ CHECKLIST OPERATIVA - **Auto**verifica di completezza tecnica

NB Da **NON** confondere con le griglie di valutazione che sono molto diverse,
tipicamente molto piu' generali
- per il voto si tiene conto delle griglie di valutazione, svolgere test avendo in mente queste griglie
- per **auto**verificare le proprie conoscenze e lacune e punti eventualmente da inserire nella parte tecnica si può usare questa griglia

## 1. Architettura generale

1.1 Scelta architettura (2 layer / 3 layer)
Descrizione: definire struttura access–core oppure access–distribution–core


1.2 Motivazione architettura
Descrizione: spiegare perché NON usare (o usare) il distribution layer


1.3 Presenza firewall perimetrale
Descrizione: dispositivo tra LAN e Internet


1.4 Posizione del firewall
Descrizione: tra Internet e rete interna (eventualmente con DMZ)


1.5 Presenza core switch
Descrizione: nodo centrale di aggregazione


1.6 Collegamento Internet → firewall → core
Descrizione: flusso principale della rete


---

## 2. VLAN e segmentazione

2.1 VLAN utenti interni
Descrizione: rete dedicata agli uffici


2.2 VLAN server interni
Descrizione: rete separata per server


2.3 VLAN ospiti
Descrizione: rete separata per guest


2.4 VLAN management
Descrizione: rete per gestione apparati


2.5 VLAN DMZ
Descrizione: rete per server esposti


2.6 Coerenza numero VLAN
Descrizione: non troppe, non troppo poche


2.7 Coerenza VLAN ↔ funzione
Descrizione: ogni VLAN ha ruolo chiaro


---

## 3. Piano di indirizzamento IP

3.1 Uso indirizzi privati
Descrizione: rete interna con RFC1918


3.2 Scelta blocco IP coerente
Descrizione: es. 10.10.0.0/16


3.3 Subnet per ogni VLAN
Descrizione: 1 VLAN = 1 subnet


3.4 Gateway per ogni subnet
Descrizione: IP del router/firewall


3.5 Struttura leggibile
Descrizione: es. 10.10.X.0/24


3.6 Assenza sovrapposizioni
Descrizione: subnet distinte


---

## 4. Posizionamento server

4.1 Ubicazione server WEB
Descrizione: in DMZ


4.2 Ubicazione database
Descrizione: in rete interna protetta


4.3 Separazione WEB / DB
Descrizione: front-end separato da back-end


4.4 Posizionamento server interni
Descrizione: in VLAN server


4.5 Posizionamento DHCP/DNS
Descrizione: coerente con rete interna


---

## 5. Pubblicazione servizi (WEB)

5.1 Raggiungibilità server WEB
Descrizione: accessibile da Internet


5.2 Metodo pubblicazione
Descrizione: NAT / port forwarding / reverse proxy


5.3 Uso NAT per pubblicazione
Descrizione: DNAT o port forwarding


5.4 Eventuale IP pubblico diretto
Descrizione: alternativa al NAT


5.5 Apertura porte corrette
Descrizione: solo 80/443


---

## 6. Routing

6.1 Presenza inter-VLAN routing
Descrizione: comunicazione tra reti


6.2 Posizione routing
Descrizione: firewall o switch L3


6.3 Gateway coerente con routing
Descrizione: gateway = dispositivo di routing


6.4 Presenza default route
Descrizione: verso Internet


6.5 Percorso traffico chiaro
Descrizione: client → gateway → firewall → Internet


---

## 7. NAT e accesso Internet

7.1 PAT per client interni
Descrizione: molti host → 1 IP pubblico


7.2 Distinzione NAT uscita / NAT ingresso
Descrizione: PAT vs port forwarding


7.3 Coerenza NAT ↔ firewall
Descrizione: NAT accompagnato da regole


---

## 8. Sicurezza e firewall

8.1 Regola Internet → WEB
Descrizione: consentire solo HTTP/HTTPS


8.2 Regola WEB → DB
Descrizione: accesso su porta DB


8.3 Blocco Internet → DB
Descrizione: nessun accesso diretto


8.4 Blocco accesso ospiti → LAN
Descrizione: isolamento guest


8.5 Controllo traffico inter-VLAN
Descrizione: non tutto è libero


8.6 Protezione management
Descrizione: accesso limitato


---

## 9. Switching e trunk

9.1 Porte access per host
Descrizione: PC su access


9.2 Trunk tra switch
Descrizione: trasporto VLAN


9.3 Trunk verso firewall/router
Descrizione: se routing centralizzato


9.4 VLAN coerenti su più switch
Descrizione: propagate via trunk


---

## 10. Wi-Fi

10.1 AP collegato a switch
Descrizione: integrazione LAN


10.2 SSID interni / ospiti separati
Descrizione: due reti wireless


10.3 SSID → VLAN mapping
Descrizione: associazione logica


10.4 Isolamento Wi-Fi ospiti
Descrizione: no accesso LAN


---

## 11. Collegamenti sedi (se presenti)

11.1 Scelta tecnologia (VPN / radio)
Descrizione: soluzione plausibile


11.2 Sicurezza collegamento
Descrizione: cifratura o isolamento


11.3 Routing tra sedi
Descrizione: raggiungibilità subnet remote


---

## 12. Schema e tabelle

12.1 Schema di rete presente
Descrizione: rappresentazione grafica


12.2 Coerenza schema ↔ testo
Descrizione: stessi elementi


12.3 Tabella VLAN
Descrizione: VLAN, rete, funzione


12.4 Tabella IP
Descrizione: subnet e gateway


---

## 13. Verifica finale

13.1 Coerenza generale
Descrizione: tutte le parti funzionano insieme


13.2 Funzionamento reale
Descrizione: rete implementabile


13.3 Assenza errori gravi
Descrizione:

* DB esposto
* no VLAN
* no routing
* IP errati
  Criterio: penalizzazione forte

13.4 Motivazioni tecniche  
Descrizione: spiegazione delle scelte



