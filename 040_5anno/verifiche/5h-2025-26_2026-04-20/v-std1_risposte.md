## Cosa è SSID, come viene usato nelle architetture per più tipologie di utenti, eventuale relazione con VLAN

SSID (Service Set Identifier) è il nome logico di una rete WiFi, visibile ai client, che identifica una specifica rete wireless gestita da un Access Point.

Nelle architetture con più tipologie di utenti (dipendenti, ospiti, dispositivi IoT), si configurano più SSID sullo stesso Access Point. Ogni SSID rappresenta una rete distinta con proprie regole di autenticazione e sicurezza.

Relazione con VLAN: ogni SSID è generalmente associato a una VLAN. Il traffico WiFi viene taggato (802.1Q) e instradato nella VLAN corrispondente, garantendo isolamento tra le diverse tipologie di utenti.

---

## SNMP: a che livello ISO/OSI corrisponde e quali protocolli di livello inferiore utilizza

SNMP opera al livello Applicazione (livello 7 del modello ISO/OSI).

Utilizza:

* UDP (livello Trasporto), porte 161 e 162
* IP (livello Rete)

---

## Descrivere 4G LTE e 5G

4G LTE è una tecnologia di rete mobile a banda larga basata su architettura IP, con alte velocità di trasmissione e latenze ridotte rispetto alle generazioni precedenti.

5G è l’evoluzione del 4G e introduce:

* velocità molto elevate (fino a Gbps)
* latenza molto bassa
* supporto massivo a dispositivi IoT
* network slicing per servizi differenziati

---

## Architettura 3-tier: descriverla e fornire un esempio concreto

Architettura a tre livelli separati:

* Presentation tier: interfaccia utente
* Application tier: logica applicativa
* Data tier: gestione dei dati

Esempio: applicazione web aziendale

* browser (presentation)
* server web/applicativo (application)
* database (data)

Consente maggiore scalabilità, sicurezza e manutenibilità.

---

## Funzionalità di un NMS

Un NMS (Network Management System) è un sistema centralizzato per la gestione della rete.

Funzioni:

* monitoraggio stato dispositivi
* raccolta metriche (CPU, traffico, errori)
* configurazione remota
* gestione allarmi
* logging e analisi
* integrazione con SNMP

---

## Elencare e descrivere le tipologie di cloud

Modelli di servizio:

* IaaS: infrastruttura (VM, rete, storage), gestione OS a carico dell’utente
* PaaS: piattaforma completa per sviluppo e deploy
* SaaS: applicazioni accessibili via web

Modelli di deployment:

* Public cloud: infrastruttura condivisa
* Private cloud: infrastruttura dedicata
* Hybrid cloud: combinazione dei due

---

## Descrivere il funzionamento di base di SNMP

SNMP prevede:

* Manager (NMS)
* Agent (sui dispositivi)
* MIB (database delle variabili)

Il manager invia richieste (GET, SET) agli agent.
Gli agent rispondono con i dati richiesti.
Gli agent possono inviare notifiche asincrone (TRAP).

---

## Vantaggi virtualizzazione

* migliore utilizzo delle risorse hardware
* isolamento tra sistemi
* snapshot e backup semplificati
* provisioning rapido
* scalabilità
* riduzione dei costi

---

## Creare un piano di indirizzamento VLSM usando 192.168.10.0/24


## Creare un piano di indirizzamento VLSM usando 192.168.10.0/24 per sottoreti di 100 host, 50 host, 25 host, 10 host

In questo caso il VLSM è necessario.  
Con subnet a lunghezza fissa, partendo da 192.168.10.0/24, bisognerebbe scegliere una subnet mask adatta alla rete più grande, cioè quella da 100 host. Per 100 host serve almeno una sottorete /25, che offre 126 host utilizzabili. Però un /24 può essere diviso solo in 2 sottoreti /25, quindi non sarebbe possibile ottenere 4 sottoreti distinte.


Procedimento di calcolo, in breve:

1. ordinare le reti dalla più grande alla più piccola;
2. per ogni rete, trovare il numero minimo di bit host necessario;
3. scegliere la subnet mask corrispondente;
4. assegnare le sottoreti in sequenza, partendo dall’inizio del blocco disponibile;
5. per ogni sottorete calcolare:

   * indirizzo di rete
   * primo host
   * ultimo host
   * broadcast
   * indirizzo del router, normalmente il primo host utile.

## Creare un piano di indirizzamento VLSM usando 192.168.10.0/24 per sottoreti di 100 host, 50 host, 25 host, 10 host

In questo caso il VLSM è necessario, perché con subnet a lunghezza fissa non sarebbe possibile ottenere 4 sottoreti adeguate partendo da una sola rete /24. Infatti la rete più grande richiede almeno una /25, e dividendo un /24 in sottoreti /25 si ottengono solo 2 sottoreti.

Procedimento sintetico:

* ordinare le richieste dalla più grande alla più piccola;
* scegliere per ciascuna il prefisso minimo sufficiente;
* assegnare le reti in sequenza, senza sovrapposizioni.

Calcolo dei prefissi:

* 100 host: servono 7 bit host, quindi /25
* 50 host: servono 6 bit host, quindi /26
* 25 host: servono 5 bit host, quindi /27
* 10 host: servono 4 bit host, quindi /28

Rappresentazione dei bit per ogni sottorete

Rete di partenza:
192.168.10.0/24

```
11000000.10101000.00001010.xxxxxxxx
<----------- rete /24 -----------><-- ultimo ottetto -->
```

Sottorete da 100 host: /25

```
11000000.10101000.00001010.0xxxxxxx
<----------- rete /24 -----------><s><-- host ----->
```

* bit rete iniziale: 24
* bit sottorete: 1
* bit host: 7

Sottorete da 50 host: /26

```
11000000.10101000.00001010.10xxxxxx
<----------- rete /24 -----------><ss><- host ---->
```

* bit rete iniziale: 24
* bit sottorete: 2
* bit host: 6

Sottorete da 25 host: /27

```
11000000.10101000.00001010.110xxxxx
<----------- rete /24 -----------><sss>< host --->
```

* bit rete iniziale: 24
* bit sottorete: 3
* bit host: 5

Sottorete da 10 host: /28

```
11000000.10101000.00001010.1110xxxx
<----------- rete /24 -----------><ssss><host-->
```

* bit rete iniziale: 24
* bit sottorete: 4
* bit host: 4

Tabella del piano di indirizzamento

| Sottorete | Host richiesti | Indirizzo di sottorete | Netmask         | Router         | Primo host     | Ultimo host    | Broadcast      |
| --------- | -------------: | ---------------------- | --------------- | -------------- | -------------- | -------------- | -------------- |
| Rete 1    |            100 | 192.168.10.0/25        | 255.255.255.128 | 192.168.10.1   | 192.168.10.1   | 192.168.10.126 | 192.168.10.127 |
| Rete 2    |             50 | 192.168.10.128/26      | 255.255.255.192 | 192.168.10.129 | 192.168.10.129 | 192.168.10.190 | 192.168.10.191 |
| Rete 3    |             25 | 192.168.10.192/27      | 255.255.255.224 | 192.168.10.193 | 192.168.10.193 | 192.168.10.222 | 192.168.10.223 |
| Rete 4    |             10 | 192.168.10.224/28      | 255.255.255.240 | 192.168.10.225 | 192.168.10.225 | 192.168.10.238 | 192.168.10.239 |

Restano liberi gli indirizzi da 192.168.10.240 a 192.168.10.255, cioè un ulteriore blocco 192.168.10.240/28 utilizzabile in futuro.
  

Restano liberi gli indirizzi da 192.168.10.240 a 192.168.10.255, che corrispondono al blocco 192.168.10.240/28, utilizzabile per un’eventuale sottorete futura.


---

## Descrivere i tipi di DMZ, per ogni tipo vantaggi, svantaggi e casi d’uso

DMZ con firewall a 3 interfacce:

* semplice ed economica
* unico punto di controllo ma anche di rischio
* adatta a piccole/medie reti

DMZ con doppio firewall:

* maggiore sicurezza (difesa a più livelli)
* maggiore costo e complessità
* usata in ambienti enterprise

DMZ su VLAN:

* flessibile e senza hardware dedicato
* isolamento inferiore
* adatta a contesti virtualizzati o piccoli

---

## Dove collocare un server WEB pubblico e un server RDBMS usato dal server WEB

Server WEB:

* in DMZ
* accessibile da Internet su 80/443

Server RDBMS:

* in rete interna
* accessibile solo dal server WEB

Regole:
Internet → WEB consentito
Internet → DB bloccato

---

## Elencare vantaggi e svantaggi del cloud rispetto a inhouse/on-premises

Vantaggi cloud:

* scalabilità immediata
* costi iniziali ridotti
* alta disponibilità
* gestione infrastruttura delegata

Svantaggi cloud:

* dipendenza dal provider
* costi variabili nel tempo
* minore controllo
* problematiche di compliance

Vantaggi on-premises:

* controllo completo
* personalizzazione
* prevedibilità costi a lungo termine

Svantaggi on-premises:

* alti costi iniziali
* gestione interna complessa
* scalabilità limitata
