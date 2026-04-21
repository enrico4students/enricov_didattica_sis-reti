voglio creare delle reference architectures di sistemi e reti, cioè architetture realistiche che includano tutti gli elementi che ricorrono piu' spesso nelle reti di organizzazioni del mondo reale. Le reference architectures vanno definite ovviamente in ottica di traccia di esame di stato ma devono essere il piu' possibile realistiche e includere tutti gli elementi che ricorrono piu' spesso nelle reti di organizzazioni reali. 

Va creata almeno una versione per il 2 layers e una per il 3 layers.

Le organizzazioni per le quali si crea la rete devono avere tutti i ragionevolmente possibili casi di connettività e di sicurezza.

Un esempio di elementi da includere:
- connettività wifi di interni e ospiti
- server esterni: almeno un server WEB e un server che espone endpoints REST e SOAP on-site
- server interni: DBMS, sistema SAP, sistema di business custom, applicativo/server documentale dedicato a files con dati aziendali riservati accessibili solo al management, MongoDB per gestione documenti generale, relativa a documenti non altamente confidenziali accessibili a normali dipendenti secondo RBAC  
- connettività da ufficio secondario ubicato in line-of-sight a 600 metri dalla sede considerata
- un'altra sede principale in un'altro continente, questa sede deve connettersi in VPN site-to-site
- tutti e soli i dipendenti di livello manageriale devono avere accesso per lavorare remotamente
- deve essere prevista e specificata una rete di gestione
- l'organizzazione' espone servizi pubblici oltre che on-site, su un fornitore cloud, usando l'approccio serverless, alcuni di questi servizi per la loro implementazione invocano alcuni dei servizi implementati on-site citati in precedenza
- specificare come viene implementata la rete di management e perchè
- cercare di includere IDS/IPS integrati con NMS
- l'organizzazione fa anche, internamente, nella propria rete (anche se normalmente si tende a preferire il cloud per elasticità Etc.), delle elaborazioni big data utillizzando un sistema distribuito di circa 10 nodi, la rete deve supportare adeguatamente queste elaborazioni e i loro requisiti di trasmissione di grandi quantità di dati in tempi rapidi

### Elenco dei punti da specificare (chatGPT non rivisto/corretto)
Di seguito una **checklist completa e strutturata** di ciò che deve essere definito dagli studenti.
Organizzata su 3 livelli: aree → elementi → dettagli minimi attesi.

---

# 1. Architettura di rete

## 1.1 Topologia generale

* Scelta architettura: 2 layer / 3 layer

  * livelli presenti (access, distribution, core)
  * motivazione della scelta
* Posizionamento apparati principali

  * firewall
  * switch
  * access point

## 1.2 Segmentazione logica

* Definizione reti / VLAN

  * utenti uffici
  * management
  * server interni
  * DMZ
  * WiFi corporate
  * WiFi guest
  * rete gestione
  * rete big data (se separata)
* Associazione VLAN ↔ subnet

## 1.3 Routing

* Modalità di inter-VLAN routing

  * su firewall oppure su switch L3
* Routing verso Internet e altre sedi

---

# 2. Connettività

## 2.1 Accesso Internet

* Tipologia collegamento
* Posizione NAT / firewall

## 2.2 Sedi remote

* Sede su altro continente

  * VPN site-to-site
* Ufficio secondario (LOS 600 m)

  * tecnologia (radio/fibra)
  * L2 o L3

## 2.3 Accesso remoto utenti

* VPN per manager
* restrizioni di accesso

## 2.4 WiFi

* rete corporate
* rete guest
* isolamento tra reti

---

# 3. Servizi e sistemi

## 3.1 Server interni

* DBMS
* sistemi applicativi (SAP, custom)
* server documentale riservato
* MongoDB documentale

## 3.2 Server esposti

* web server
* API REST / SOAP

## 3.3 Cloud

* servizi serverless
* integrazione con servizi on-site

## 3.4 Servizi infrastrutturali

* DNS
* DHCP
* autenticazione centralizzata (AD/LDAP o equivalente)

---

# 4. Sicurezza

## 4.1 Perimetro

* firewall perimetrale
* NAT
* DMZ

  * servizi pubblicati
  * separazione da rete interna

## 4.2 Controllo accessi

* regole tra reti (ACL / policy)

  * chi comunica con chi
* accessi privilegiati (management, VPN)
* RBAC sui sistemi

## 4.3 Monitoraggio sicurezza

* IDS/IPS
* integrazione con NMS

---

# 5. Gestione e monitoraggio

## 5.1 Rete di management

* VLAN dedicata
* accesso limitato
* terminazione (firewall o L3)
* motivazione della scelta

## 5.2 Monitoraggio

* NMS
* raccolta informazioni dai dispositivi

---

# 6. Dati e prestazioni

## 6.1 Cluster big data

* rete dedicata o condivisa
* requisiti di banda
* isolamento dal resto della rete

## 6.2 Flussi principali

* traffico utenti → server
* traffico server → DB
* traffico cloud ↔ on-site

---

# 7. Indirizzamento

## 7.1 Piano IP

* subnet per ogni rete/VLAN
* coerenza e scalabilità

---

# 8. Affidabilità (livello minimo)

## 8.1 Continuità di servizio

* identificazione punti critici
* eventuali ridondanze essenziali

---

## Sintesi

Lo studente deve definire:

* struttura della rete
* segmentazione
* connettività
* servizi
* sicurezza
* gestione
* flussi
* indirizzamento

