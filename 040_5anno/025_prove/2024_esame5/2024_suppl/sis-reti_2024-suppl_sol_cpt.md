
# Soluzione - Sistemi e reti - Suppletiva 2024

## replica testo prova (soluzione segue)  

#### A038 - ESAME DI STATO CONCLUSIVO DEL SECONDO CICLO DI ISTRUZIONE

Indirizzo ITIA - INFORMATICA E TELECOMUNICAZIONI
Articolazione "INFORMATICA"

(Testo valevole anche per gli indirizzi quadriennali IT32)

Disciplina: SISTEMI E RETI

Il candidato svolga la prima parte della prova e due tra i quesiti proposti nella seconda parte.

#### PRIMA PARTE

##### Gestione eventi con grandi folle

Una città italiana di interesse turistico internazionale ha deciso di sperimentare un nuovo sistema di monitoraggio del flusso delle persone in occasione di grandi eventi (culturali, artistici, sportivi). A tali eventi, che si svolgono in un preciso luogo della città, si potrà accedere unicamente mediante biglietti a pagamento o anche gratuiti.

Nell’intera area del comune saranno presenti punti di informazione automatici (totem), basati su touch screen, dove l’utente potrà informarsi su uno o più eventi e acquistare il biglietto in autonomia.

Per la gestione del sistema di monitoraggio del flusso delle persone in occasione di un evento, viene messa a disposizione una sede operativa composta da due piani; al primo piano sarà presente un’area dedicata all’assistenza pre- e post-vendita dei biglietti, dove gli operatori potranno svolgere le loro mansioni; al secondo piano sarà presente la sala di controllo dove il personale addetto, attraverso telecamere di sorveglianza, potrà visionare le immagini in diretta dei luoghi interessati dagli eventi.

Uno degli obiettivi è quello di ridurre il sovraffollamento nelle aree critiche e poter intervenire con prontezza in caso di necessità.

In punti strategici della città verranno infatti collocate telecamere di monitoraggio e dispositivi azionabili a distanza (per esempio semafori, barriere a scomparsa, pannelli informativi o altro) che permetteranno di gestire al meglio il flusso di persone verso il luogo dell’evento, anche con l’ausilio di personale in loco. I dispositivi, azionabili a distanza, verranno gestiti attraverso un server HTTP interno al dispositivo stesso, accessibile da remoto.

Nell’area circostante l’evento (ad esempio un concerto) sarà presente personale addetto alla validazione degli ingressi all’evento, all’assistenza e al pronto intervento. Per lo svolgimento delle proprie mansioni, il personale in loco sarà dotato di un dispositivo mobile con il quale può comunicare con la sede operativa ed essere costantemente aggiornato sullo stato dei dispositivi azionabili a distanza sopra citati.

Il candidato analizzi la realtà di riferimento e, formulate le opportune ipotesi aggiuntive, svolga i seguenti punti:

1. sviluppi una descrizione di massima, anche supportata da uno schema grafico che presenti il sistema (organizzazione della rete informatica della sede operativa, modalità di connessione con le telecamere per il monitoraggio e i dispositivi remoti e loro attivazione e gestione), e ne ponga in evidenza i vari componenti hardware e software necessari, motivando le scelte effettuate;

2. descriva in modo dettagliato le possibili modalità di comunicazione tra la sede operativa ed il personale in loco dedicato alla gestione del flusso delle persone partecipanti all’evento, anche in relazione alla validazione dei biglietti di ingresso;

3. definisca le tecnologie di comunicazione tra la sede operativa e i punti di informazione (totem) dislocati sull’intera area del comune;

4. descriva le modalità attraverso le quali sarà possibile evitare interruzioni di servizio.

#### SECONDA PARTE

##### Quesito I

In relazione al tema proposto nella prima parte, si consideri la gestione dei filmati e delle immagini che vengono trasmessi dalle telecamere per il monitoraggio, e si propongano soluzioni per il relativo salvataggio all’interno dell’infrastruttura della sede centrale oppure nel cloud, definendone vantaggi e svantaggi.

##### Quesito II

In relazione al tema proposto nella prima parte, si discuta come possono essere attivati e gestiti i dispositivi remoti dotati di server HTTP interno, utilizzando i metodi propri di questo protocollo, fornendo opportune esemplificazioni.

##### Quesito III

Il candidato illustri caratteristiche e possibili campi di applicazione di due tecnologie di comunicazione wireless a corto raggio quali, ad esempio, sistemi basati su RFID, NFC, Bluetooth Low Energy (BLE), IEEE 802.15.4.

##### Quesito IV

In una rete locale è presente un host con la seguente configurazione:

```
hostname: pcserverlab
IP address: 192.168.1.15/24
Default Gateway: 192.168.1.1
DNS1: 192.168.1.2
DNS2: 212.14.128.1
```

Effettuando da un altro PC della rete il ping all’IP Address di tale host, con il comando:

```
C:\Users\admin>ping 192.168.1.15
```

si ottiene in risposta:

```
Esecuzione di Ping 192.168.1.15 con 32 byte di dati:
Risposta da 192.168.1.15: byte=32 durata=41ms TTL=56
Risposta da 192.168.1.15: byte=32 durata=32ms TTL=56
Risposta da 192.168.1.15: byte=32 durata=52ms TTL=56
Risposta da 192.168.1.15: byte=32 durata=38ms TTL=56
```

mentre effettuando il comando:

```
C:\Users\admin>ping pcserverlab
```

si ottiene in risposta:

```
Impossibile trovare l’host pcserverlab.
Verificare che il nome sia corretto e riprovare
```

Inoltre, effettuando il comando:

```
C:\Users\admin>ping www.istruzione.it
```

si ottiene la risposta:

```
Risposta da 92.123.181.19: byte=32 durata=20ms TTL=49
Risposta da 92.123.181.19: byte=32 durata=26ms TTL=49
Risposta da 92.123.181.19: byte=32 durata=214ms TTL=49
Risposta da 92.123.181.19: byte=32 durata=18ms TTL=49
```

Il candidato discuta le possibili cause di tale anomalia; ipotizzando di essere il responsabile dell’infrastruttura di rete, discuta quali passi successivi compirebbe per identificare il problema e porvi rimedio.



# Ipotesi di Soluzione   

## Prima parte

Si progetta un sistema composto da:

* sede operativa su due piani;
* totem informativi e di biglietteria distribuiti nel comune;
* telecamere IP nelle aree critiche;
* dispositivi remoti azionabili, come semafori, barriere e pannelli;
* dispositivi mobili per il personale sul posto;
* piattaforma centrale applicativa.

La soluzione scelta è ibrida: server applicativi e database principali in cloud, sede operativa collegata tramite VPN, dispositivi remoti connessi tramite rete 4G/5G o fibra dove disponibile.

Si scarta una soluzione solo locale perché richiederebbe server, storage, alimentazione ridondata e manutenzione nella sede operativa. Si scarta anche una soluzione completamente distribuita sui singoli dispositivi perché sarebbe più difficile da aggiornare, controllare e proteggere.

## Schema logico

```
Internet / rete 4G-5G / fibra
          |
    Cloud provider
          |
+-----------------------------+
| Web application             |
| API REST HTTPS              |
| Database biglietti/eventi   |
| Storage video               |
| Sistema notifiche           |
+-----------------------------+
      |        |        |
      |        |        |
  VPN sede   Totem   Dispositivi mobili
      |
+-----------------------------+
| Sede operativa              |
| Piano 1: assistenza         |
| Piano 2: sala controllo     |
+-----------------------------+
      |
Firewall / router dual WAN
      |
Switch L3 o firewall interno
      |
VLAN assistenza
VLAN sala controllo
VLAN videosorveglianza
VLAN gestione apparati
```

## Rete della sede operativa

La sede operativa viene divisa in VLAN, cioè reti logiche separate sulla stessa infrastruttura fisica.

Esempio:

| VLAN | Uso                         | Rete            |
| ---- | --------------------------- | --------------- |
| 10   | assistenza biglietti        | 192.168.10.0/24 |
| 20   | sala controllo              | 192.168.20.0/24 |
| 30   | apparati di rete e gestione | 192.168.30.0/24 |
| 40   | videosorveglianza locale    | 192.168.40.0/24 |
| 50   | Wi-Fi ospiti                | 192.168.50.0/24 |

Le VLAN permettono di separare gli operatori dell’assistenza dagli addetti alla sala controllo. Questo riduce il rischio che un problema su una postazione comprometta tutta la rete.

Il routing tra VLAN può essere svolto da uno switch Layer 3 o da un firewall. Scelgo uno switch Layer 3 per il traffico ordinario interno, perché è più veloce; uso il firewall per filtrare traffico verso Internet, VPN, cloud e reti sensibili.

## Componenti principali

La sede operativa richiede:

* firewall/NGFW con VPN;
* router dual WAN;
* switch gestiti con VLAN;
* access point Wi-Fi separati per rete interna e ospiti;
* PC operatori;
* monitor multipli per sala controllo;
* UPS per continuità elettrica;
* sistema di autenticazione centralizzato.

NGFW significa firewall di nuova generazione: oltre a filtrare IP e porte può controllare applicazioni, utenti e traffico cifrato. UPS significa gruppo di continuità: mantiene alimentati gli apparati per alcuni minuti o ore in caso di mancanza di corrente.

## Collegamento con telecamere e dispositivi remoti

Le telecamere IP trasmettono video verso la piattaforma centrale tramite HTTPS, RTSP su VPN o protocollo sicuro del produttore.

RTSP è un protocollo usato per lo streaming video. In una soluzione scolastica è sufficiente indicare che il flusso video deve essere cifrato o protetto da VPN.

I dispositivi remoti azionabili hanno un piccolo server HTTP/HTTPS interno. La sede o la piattaforma cloud invia comandi autenticati, ad esempio:

```
POST /api/barriera/12/comando
{
    "azione": "chiudi",
    "motivo": "sovraffollamento ingresso nord"
}
```

Si usa POST perché modifica lo stato del dispositivo. Si evita GET per i comandi critici, perché GET dovrebbe essere usato solo per leggere informazioni.

## Comunicazione con personale in loco

Il personale sul luogo dell’evento usa smartphone o tablet con app web o app mobile.

Le funzioni principali sono:

* ricevere notifiche dalla sala controllo;
* validare biglietti tramite QR code;
* comunicare problemi;
* ricevere lo stato di barriere, semafori e pannelli;
* inviare foto o segnalazioni.

La validazione del biglietto avviene così:

```
1. l’operatore legge il QR code;
2. il dispositivo invia il codice al server tramite HTTPS;
3. il server controlla nel database se il biglietto esiste;
4. il server verifica che non sia già stato usato;
5. se valido, registra l’ingresso;
6. l’app mostra “accesso consentito” o “accesso negato”.
```

Si prevede anche una modalità offline limitata: il dispositivo può scaricare prima dell’evento una lista cifrata dei biglietti validi. Se la rete mobile non funziona, può validare provvisoriamente i biglietti e sincronizzare dopo. Questa soluzione è utile, ma va limitata perché aumenta il rischio di doppie validazioni.

## Comunicazione con i totem

I totem sono distribuiti nell’intera area comunale. Possono collegarsi:

* tramite fibra o rete comunale dove disponibile;
* tramite router 4G/5G con SIM dati;
* tramite VPN verso il cloud o la sede.

Scelgo principalmente 4G/5G con VPN, perché i totem sono distribuiti in luoghi diversi e non sempre è disponibile cablaggio fisico.

Il totem funziona come client web:

```
Totem -> HTTPS -> Web application cloud -> Database
```

Questa scelta semplifica gli aggiornamenti, perché l’applicazione viene aggiornata sul server e non su ogni totem.

Si scarta una soluzione con applicazione locale completa su ogni totem perché richiederebbe aggiornamenti separati, manutenzione maggiore e maggiore rischio di incoerenza dei dati.

## Continuità di servizio

Per evitare interruzioni di servizio si adottano più livelli di ridondanza:

* doppia connessione Internet nella sede operativa: fibra principale e 4G/5G di backup;
* router dual WAN con failover automatico;
* cloud con server replicati;
* database con backup automatici;
* storage video ridondato;
* UPS nella sede operativa;
* doppia SIM per dispositivi critici;
* monitoraggio continuo di telecamere, totem e dispositivi IoT.

Failover significa passaggio automatico a una linea o sistema di riserva quando quello principale non funziona.

La soluzione alternativa sarebbe affidarsi a una sola connessione Internet, ma viene scartata perché un guasto alla linea isolerebbe la sede operativa durante l’evento.

# Seconda parte

## Quesito I - Salvataggio filmati e immagini

I filmati possono essere salvati in sede centrale oppure nel cloud.

Nel salvataggio locale si usano server NAS o NVR nella sede operativa.

NAS significa archivio di rete. NVR significa registratore video di rete per telecamere IP.

Vantaggi del salvataggio locale:

* controllo diretto dei dati;
* minore dipendenza da Internet;
* costo prevedibile dopo l’acquisto iniziale;
* accesso rapido dalla sala controllo.

Svantaggi:

* servono dischi, backup, manutenzione e sicurezza fisica;
* se la sede ha un guasto grave, i dati possono non essere disponibili;
* scalare lo spazio richiede nuovo hardware.

Nel salvataggio cloud i video vengono inviati a uno storage remoto.

Vantaggi:

* alta scalabilità;
* backup e replica più semplici;
* accesso da più sedi autorizzate;
* integrazione con analisi video e intelligenza artificiale.

Svantaggi:

* costo dipendente da traffico e spazio occupato;
* forte dipendenza dalla connettività;
* necessità di rispettare privacy, tempi di conservazione e autorizzazioni.

La scelta più equilibrata è ibrida: registrazione locale temporanea dei flussi completi e invio al cloud solo di eventi rilevanti, clip di allarme, immagini periodiche e metadati.

## Quesito II - Gestione dispositivi remoti con HTTP

I dispositivi remoti hanno un server HTTP interno. Le operazioni possono essere modellate con metodi HTTP.

Esempi:

```
GET /stato
```

Serve per leggere lo stato del dispositivo.

Risposta:

```
{
    "id": "semaforo-12",
    "stato": "verde",
    "connessione": "ok"
}

POST /comandi
```

Serve per inviare un nuovo comando.

Esempio:

```
{
    "azione": "rosso",
    "durata_secondi": 120
}

PUT /configurazione
```

Serve per sostituire o aggiornare la configurazione.

```
{
    "nome": "pannello-ingresso-nord",
    "zona": "varco nord"
}

DELETE /messaggio
```

Può servire per rimuovere un messaggio visualizzato su un pannello.

Per sicurezza si usa HTTPS, autenticazione con token, log dei comandi e autorizzazioni per ruolo. Non si devono esporre dispositivi critici direttamente su Internet senza protezione.

## Quesito III - RFID e NFC

RFID è una tecnologia di identificazione a radiofrequenza. Un tag RFID contiene un codice letto da un reader senza contatto fisico diretto.

Applicazioni:

* badge;
* logistica;
* controllo accessi;
* biglietti elettronici;
* inventario.

Nel caso dell’evento, RFID può essere usato per braccialetti o pass di servizio. È utile perché la lettura è rapida e può funzionare anche con molte persone.

NFC è una tecnologia wireless a cortissimo raggio, normalmente pochi centimetri. È usata in smartphone, pagamenti contactless e badge digitali.

Applicazioni:

* pagamento contactless;
* biglietti digitali;
* accesso tramite smartphone;
* identificazione rapida presso un varco.

RFID è più adatto quando si vogliono leggere molti tag rapidamente o a distanza maggiore. NFC è più adatto quando si vuole un’interazione volontaria e ravvicinata, ad esempio avvicinare lo smartphone al lettore.

## Quesito IV - Problema ping IP riuscito ma ping nome fallito

L’host ha configurazione:

```
hostname: pcserverlab
IP: 192.168.1.15/24
gateway: 192.168.1.1
DNS1: 192.168.1.2
DNS2: 212.14.128.1
```

Il ping verso 192.168.1.15 funziona, quindi:

* l’host è acceso;
* la rete locale funziona;
* l’indirizzo IP è raggiungibile.

Il ping verso [www.istruzione.it](http://www.istruzione.it) funziona, quindi:

* almeno un DNS riesce a risolvere nomi Internet;
* la connessione verso Internet funziona.

Il ping verso pcserverlab non funziona. Quindi il problema riguarda la risoluzione del nome locale.

Possibili cause:

* pcserverlab non è registrato nel DNS interno;
* il DNS 192.168.1.2 non gestisce la zona locale;
* il client usa il DNS pubblico 212.14.128.1, che non conosce nomi interni;
* manca il suffisso DNS locale, ad esempio dominio.lan;
* NetBIOS/LLMNR non è attivo o non funziona;
* il nome corretto sarebbe pcserverlab.dominio.local.

Passi di diagnosi:

```
ipconfig /all
```

Per controllare DNS, suffisso DNS e configurazione IP.

```
nslookup pcserverlab
```

Per vedere quale DNS viene interrogato e quale risposta restituisce.

```
nslookup pcserverlab 192.168.1.2
```

Per interrogare direttamente il DNS interno.

```
ping pcserverlab.dominio.local
```

Per verificare se serve il nome completo FQDN.

```
hostname
```

Da eseguire sul server per verificare il nome reale della macchina.

Soluzione:

* creare o correggere il record DNS A:

  pcserverlab -> 192.168.1.15

* configurare correttamente il suffisso DNS sui client;

* usare come DNS primario il DNS interno;

* usare il DNS pubblico solo come forwarder del DNS interno, non direttamente sui client.

Si scarta l’ipotesi di problema fisico o di routing perché il ping all’indirizzo IP funziona.

# Soluzioni online trovate

Dopo lo svolgimento ex novo, risultano disponibili queste risorse online:

* Testo ufficiale MIM della prova: [https://www.istruzione.it/esame_di_stato/202324/Istituti%20tecnici/Suppletiva/A038_SUP24.pdf](https://www.istruzione.it/esame_di_stato/202324/Istituti%20tecnici/Suppletiva/A038_SUP24.pdf) ([Istruzione][1])
* Soluzione Mauro De Berardis, pagina download: [https://www.maurodeberardis.it/index.php?Itemid=338&catid=18&cid=636&option=com_jdownloads&view=viewdownload](https://www.maurodeberardis.it/index.php?Itemid=338&catid=18&cid=636&option=com_jdownloads&view=viewdownload) ([maurodeberardis.it][2])
* Pagina raccolta soluzioni Mauro De Berardis: [https://www.maurodeberardis.it/index.php?Itemid=338&catid=18&option=com_jdownloads&view=viewcategory](https://www.maurodeberardis.it/index.php?Itemid=338&catid=18&option=com_jdownloads&view=viewcategory) ([maurodeberardis.it][3])
* Pagina articolo Mauro De Berardis: [https://www.maurodeberardis.it/index.php?Itemid=328&catid=12&id=127%3Asoluzione-prova-scritta-di-sistemi-e-reti-esame-2024-sessione-suppletiva&option=com_content&view=article](https://www.maurodeberardis.it/index.php?Itemid=328&catid=12&id=127%3Asoluzione-prova-scritta-di-sistemi-e-reti-esame-2024-sessione-suppletiva&option=com_content&view=article) ([maurodeberardis.it][4])

[1]: https://www.istruzione.it/esame_di_stato/202324/Istituti%20tecnici/Suppletiva/A038_SUP24.pdf?utm_source=chatgpt.com "Suppletiva"
[2]: https://www.maurodeberardis.it/index.php?Itemid=338&catid=18&cid=636&option=com_jdownloads&view=viewdownload&utm_source=chatgpt.com "Soluzione della seconda prova scritta di Sistemi e Reti Esame ..."
[3]: https://www.maurodeberardis.it/index.php?Itemid=338&catid=18&option=com_jdownloads&view=viewcategory&utm_source=chatgpt.com "Soluzioni prove scritte Esame di Stato Sistemi e Reti e ..."
[4]: https://www.maurodeberardis.it/index.php?Itemid=328&catid=12&id=127%3Asoluzione-prova-scritta-di-sistemi-e-reti-esame-2024-sessione-suppletiva&option=com_content&view=article&utm_source=chatgpt.com "Soluzione prova scritta di Sistemi e Reti 2024 Sessione ..."
