# DHCP: Protocollo, Architettura e Utilizzo nelle Reti Moderne

## Introduzione

Quando un dispositivo viene collegato a una rete IP deve ricevere almeno alcune informazioni fondamentali:

* indirizzo IP;
* subnet mask;
* gateway predefinito;
* server DNS.

Nei primi anni delle reti TCP/IP tali parametri venivano configurati manualmente su ogni macchina. Questo approccio funziona in reti molto piccole, ma diventa rapidamente impraticabile quando il numero di dispositivi cresce.

Il protocollo DHCP (Dynamic Host Configuration Protocol) nasce per automatizzare questo processo.

Grazie a DHCP, un dispositivo può collegarsi alla rete e ottenere automaticamente tutte le informazioni necessarie per comunicare.

Oggi DHCP è utilizzato praticamente ovunque:

* reti domestiche;
* aziende;
* scuole;
* università;
* hotspot Wi-Fi;
* data center;
* reti industriali.

Comprendere DHCP significa capire uno dei meccanismi fondamentali che permettono il funzionamento quotidiano delle reti IP.

---

# 1. Cos'è DHCP

DHCP è l'acronimo di:

**Dynamic Host Configuration Protocol**

Si tratta di un protocollo applicativo definito dalla RFC 2131.

Il suo scopo principale è fornire automaticamente configurazioni IP ai client.

Invece di configurare ogni dispositivo manualmente, un server DHCP distribuisce le impostazioni necessarie ai dispositivi che ne fanno richiesta.

Tra le informazioni normalmente fornite troviamo:

* indirizzo IP;
* subnet mask;
* gateway;
* server DNS;
* durata della concessione (lease);
* dominio DNS;
* server NTP;
* altre opzioni specifiche.

DHCP rappresenta l'evoluzione del protocollo BOOTP, utilizzato negli anni precedenti.

---

# 2. Problema che DHCP risolve

Immaginare una scuola con:

* 400 PC;
* 200 notebook;
* 300 smartphone;
* stampanti;
* dispositivi IoT.

Configurare manualmente ogni dispositivo significherebbe:

* assegnare un indirizzo IP;
* evitare duplicati;
* configurare DNS e gateway;
* aggiornare eventuali modifiche.

L'errore umano diventerebbe inevitabile.

DHCP centralizza la gestione.

Il client richiede una configurazione.

Il server la assegna automaticamente.

---

# 3. Componenti dell'architettura DHCP

Un'infrastruttura DHCP coinvolge generalmente tre elementi.

## Client DHCP

È il dispositivo che richiede la configurazione.

Esempi:

* PC Windows;
* Linux;
* smartphone;
* tablet;
* smart TV;
* stampanti di rete.

---

## Server DHCP

È il sistema che distribuisce le configurazioni.

Può essere:

* un router domestico;
* un firewall;
* un server Linux;
* un server Windows;
* un appliance dedicato.

---

## Relay DHCP

Permette ai client di ottenere configurazioni da un server situato su un'altra rete.

È un componente fondamentale nelle reti aziendali.

Verrà analizzato più avanti.

---

# 4. Informazioni distribuite dal DHCP

Molti pensano che DHCP assegni soltanto l'indirizzo IP.

In realtà può distribuire numerosi parametri.

## Indirizzo IP

Esempio:

192.168.1.50

---

## Subnet Mask

Esempio:

255.255.255.0

---

## Gateway

Esempio:

192.168.1.1

---

## DNS

Esempio:

8.8.8.8

1.1.1.1

---

## Lease Time

Durata dell'assegnazione.

Ad esempio:

* 1 ora;
* 8 ore;
* 24 ore;
* 7 giorni.

---

## Parametri aggiuntivi

Tra i più comuni:

* server NTP;
* dominio DNS;
* server PXE;
* server VoIP;
* opzioni specifiche per telefoni IP.

---

# 5. Il concetto di Lease

Uno dei concetti più importanti di DHCP è il lease.

Un indirizzo IP non viene normalmente assegnato in modo permanente.

Viene "prestato" al client per un certo periodo.

Ad esempio:

IP assegnato:

192.168.1.50

Lease:

24 ore

Dopo 24 ore il client dovrà rinnovare la concessione.

Questo meccanismo permette di riutilizzare gli indirizzi quando i dispositivi lasciano la rete.

---

# 6. Il processo DORA

Il funzionamento di DHCP è spesso descritto tramite l'acronimo DORA.

* Discover
* Offer
* Request
* Acknowledge

Questa sequenza è fondamentale.

---

## Fase 1: DHCP Discover

Il client non possiede ancora un indirizzo IP.

Non sa nemmeno quale sia il server DHCP.

Invia quindi un messaggio broadcast.

Destinazione:

255.255.255.255

Richiesta:

"C'è un server DHCP disponibile?"

---

## Fase 2: DHCP Offer

Uno o più server DHCP rispondono.

Ogni server propone:

* indirizzo IP;
* subnet mask;
* gateway;
* lease.

---

## Fase 3: DHCP Request

Il client sceglie una delle offerte.

Comunica quale intende utilizzare.

---

## Fase 4: DHCP Acknowledge

Il server conferma definitivamente l'assegnazione.

Il client può ora utilizzare l'indirizzo IP ricevuto.

---

# 7. Porte utilizzate

DHCP utilizza il protocollo UDP.

Porte standard:

| Funzione | Porta  |
| -------- | ------ |
| Client   | UDP 68 |
| Server   | UDP 67 |

Queste porte devono essere consentite da firewall e apparati di sicurezza.

---

# 8. Perché DHCP usa il Broadcast

All'avvio il client non possiede ancora un indirizzo IP.

Non conosce il server DHCP.

L'unica possibilità è trasmettere un broadcast.

Questo spiega perché DHCP normalmente non attraversa i router.

I router, per impostazione predefinita, bloccano i broadcast.

Da qui nasce la necessità del DHCP Relay.

---

# 9. DHCP Relay

## Il problema

Supporre una rete aziendale composta da:

* VLAN 10 Amministrazione
* VLAN 20 Docenti
* VLAN 30 Studenti

Il server DHCP è collocato nel data center.

I broadcast provenienti dalle VLAN non possono attraversare i router.

Senza ulteriori configurazioni i client non riceverebbero alcun indirizzo IP.

---

## La soluzione

Configurare un DHCP Relay.

Il relay:

1. riceve il broadcast;
2. lo converte in traffico unicast;
3. lo inoltra al server DHCP.

Il server risponde al relay.

Il relay inoltra la risposta al client.

---

# 10. DHCP e VLAN

In ambienti professionali DHCP e VLAN lavorano quasi sempre insieme.

Tipicamente:

| VLAN | Rete            |
| ---- | --------------- |
| 10   | 192.168.10.0/24 |
| 20   | 192.168.20.0/24 |
| 30   | 192.168.30.0/24 |

Il server DHCP mantiene scope separati.

Ogni VLAN riceve configurazioni differenti.

Questo permette:

* segmentazione;
* sicurezza;
* gestione semplificata.

---

# 11. Scope DHCP

Uno scope rappresenta un insieme di indirizzi distribuibili.

Esempio:

Rete:

192.168.1.0/24

Range DHCP:

192.168.1.100 – 192.168.1.200

In questo caso il server può distribuire soltanto tali indirizzi.

---

# 12. Esclusioni

Alcuni indirizzi non devono essere assegnati automaticamente.

Esempio:

192.168.1.1 Router

192.168.1.2 Firewall

192.168.1.3 Server DNS

192.168.1.4 NAS

Questi indirizzi vengono esclusi dal pool DHCP.

---

# 13. Prenotazioni DHCP

Talvolta un dispositivo deve ricevere sempre lo stesso indirizzo.

Si utilizza una prenotazione.

La prenotazione associa:

MAC Address → IP

Esempio:

00:11:22:33:44:55

↓

192.168.1.20

Il dispositivo continua a usare DHCP ma riceve sempre lo stesso indirizzo.

---

# 14. Differenza tra Prenotazione e IP Statico

Molti amministratori confondono i due concetti.

## IP statico sul dispositivo

Configurazione effettuata manualmente.

Il server DHCP non interviene.

---

## Prenotazione DHCP

Configurazione centralizzata.

Il client usa DHCP.

L'indirizzo resta costante.

In ambienti professionali la prenotazione è generalmente preferibile.

---

# 15. Quando usare DHCP

DHCP è la scelta corretta per:

* PC degli utenti;
* notebook;
* smartphone;
* tablet;
* dispositivi Wi-Fi;
* laboratori scolastici;
* workstation aziendali.

In generale per tutti i dispositivi che non richiedono un indirizzo permanente gestito manualmente.

---

# 16. Quando NON usare DHCP

Alcuni dispositivi devono essere raggiungibili sempre allo stesso indirizzo.

Esempi:

* router;
* firewall;
* server DNS;
* server web;
* server database;
* controller di dominio;
* switch gestiti;
* access point professionali;
* sistemi di monitoraggio.

Per questi dispositivi si preferisce normalmente:

* IP statico;
  oppure
* prenotazione DHCP accuratamente documentata.

---

# 17. DHCP in una rete domestica

Nelle abitazioni moderne il router svolge generalmente il ruolo di:

* gateway;
* DNS forwarder;
* server DHCP.

L'utente spesso non si accorge nemmeno della sua esistenza.

Quando uno smartphone si collega al Wi-Fi riceve automaticamente:

* IP;
* gateway;
* DNS.

Tutto grazie al DHCP.

---

# 18. DHCP nelle reti aziendali

In una rete aziendale il DHCP è normalmente centralizzato.

Spesso l'architettura comprende:

* server DHCP ridondati;
* relay DHCP;
* VLAN multiple;
* integrazione con DNS.

Questo permette la gestione di migliaia di dispositivi.

---

# 19. Rischi di sicurezza

DHCP è estremamente utile ma introduce alcuni rischi.

---

## Rogue DHCP Server

Un utente potrebbe collegare un router personale.

Il router inizierebbe a distribuire configurazioni errate.

I client potrebbero:

* perdere connettività;
* utilizzare gateway errati;
* subire attacchi.

---

## DHCP Starvation

Un attaccante può richiedere migliaia di indirizzi.

Il pool viene esaurito.

I client legittimi non ricevono più configurazioni.

---

## Contromisure

Tra le principali:

* DHCP Snooping sugli switch;
* segmentazione VLAN;
* controllo accessi;
* monitoraggio della rete.

---

# 20. DHCPv4 e DHCPv6

Nelle reti IPv6 il concetto rimane simile.

Tuttavia esistono differenze importanti.

IPv6 può utilizzare:

* DHCPv6;
* SLAAC (Stateless Address Autoconfiguration);
* combinazioni dei due.

Molte reti IPv6 moderne utilizzano SLAAC per l'indirizzo e DHCPv6 per informazioni aggiuntive.

---

# 21. Buone pratiche di progettazione

Quando si progetta un'infrastruttura DHCP è consigliabile:

1. separare le VLAN;
2. usare scope distinti;
3. documentare le prenotazioni;
4. escludere gli indirizzi infrastrutturali;
5. predisporre ridondanza;
6. utilizzare DHCP relay invece di moltiplicare i server;
7. attivare DHCP Snooping sugli switch gestiti;
8. monitorare l'utilizzo dei pool.

---

# 22. Esempio reale di progettazione

Piccola scuola:

VLAN 10 – Segreteria

192.168.10.0/24

Pool DHCP:

192.168.10.100–192.168.10.200

---

VLAN 20 – Docenti

192.168.20.0/24

Pool DHCP:

192.168.20.100–192.168.20.250

---

VLAN 30 – Studenti

192.168.30.0/24

Pool DHCP:

192.168.30.50–192.168.30.250

---

Server DHCP centrale:

192.168.1.10

Relay configurato sui router delle VLAN.

Questa architettura è molto comune nelle scuole e nelle piccole aziende.

---

# Conclusioni

DHCP è uno dei servizi fondamentali delle reti IP moderne.

La sua funzione non è semplicemente assegnare indirizzi IP, ma fornire in modo centralizzato tutte le informazioni necessarie alla comunicazione di rete.

Dal punto di vista operativo è essenziale comprendere:

* il processo DORA;
* il concetto di lease;
* la gestione di scope e prenotazioni;
* l'uso dei relay;
* l'integrazione con VLAN e routing.

Una corretta progettazione DHCP riduce gli errori amministrativi, semplifica la gestione della rete e rende possibile il funzionamento efficiente di reti con centinaia o migliaia di dispositivi.

---

# Laboratorio 1 - Verificare la configurazione DHCP in Windows

Aprire il Prompt dei comandi ed eseguire:

```
ipconfig /all
```

Individuare:

* indirizzo IP;
* gateway;
* server DNS;
* voce "DHCP abilitato".

Osservare inoltre il server DHCP utilizzato.

---

# Laboratorio 2 - Rinnovare il lease DHCP

Nel Prompt dei comandi:

```
ipconfig /release
```

Successivamente:

```
ipconfig /renew
```

Osservare l'assegnazione del nuovo indirizzo.

---

# Laboratorio 3 - Linux

Visualizzare la configurazione di rete:

```
ip addr
```

Visualizzare il gateway:

```
ip route
```

Visualizzare i DNS:

```
cat /etc/resolv.conf
```

---

# Laboratorio 4 - Analizzare il traffico DHCP

Installare Wireshark.

Avviare una cattura sulla scheda di rete.

Filtrare:

```
dhcp
```

oppure:

```
bootp
```

Rinnovare il lease DHCP e osservare i messaggi:

* Discover
* Offer
* Request
* Acknowledge

Visualizzare concretamente il processo DORA.

---

# Laboratorio 5 - Individuare il server DHCP della rete

Windows:

```
ipconfig /all
```

Linux:

```
journalctl -u NetworkManager
```

oppure:

```
nmcli device show
```

Verificare quale server ha distribuito la configurazione IP al dispositivo.
