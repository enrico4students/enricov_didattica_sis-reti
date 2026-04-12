
---

## RADIUS AAA Server

<img src="https://www.inkbridgenetworks.com/web/image/3558-fb43d2bc/radius_diagram_auth_3324x2535.webp?access_token=01528220-784d-49e6-b2ee-f9ed2fc16e95" width="80%"/>

<img src="https://miro.medium.com/0%2A9WZnM_foBQEql8nh.png" width="80%"/>

<img src="https://upload.wikimedia.org/wikipedia/commons/1/1f/802.1X_wired_protocols.png" width="80%"/>

<img src="https://media.licdn.com/dms/image/v2/D5612AQEr5797TWza-w/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1713631795614?e=2147483647&t=XHmyBBcYsC2Of8oZjvMddVOmFca4mZCWMm4gRxkw6o8&v=beta" width="80%"/>

RADIUS (protocollo): Remote Authentication Dial-In User Service

---

# 1) Che cos’è un server RADIUS

Un **server RADIUS** è un server che implementa il protocollo **RADIUS (Remote Authentication Dial-In User Service)** e che ha il compito di fornire servizi di **AAA**, cioè:

Authentication
Authorization
Accounting

Per comprendere il ruolo di RADIUS è utile pensare a un problema molto concreto che si presenta in qualsiasi rete di una certa dimensione: **come controllare chi può accedere alla rete e cosa può fare una volta entrato**.

In una rete molto piccola questo controllo può essere fatto direttamente nei dispositivi di rete. Ad esempio un router domestico può avere una lista di utenti locali oppure una password Wi-Fi condivisa da tutti. Tuttavia questo approccio diventa rapidamente ingestibile quando il numero di utenti cresce.

In una rete aziendale o universitaria possono esserci:

centinaia o migliaia di utenti
decine o centinaia di access point
switch distribuiti su molti edifici

Gestire le credenziali direttamente su ogni dispositivo diventerebbe impossibile.

Il ruolo di RADIUS è proprio quello di **centralizzare il controllo degli accessi alla rete**. I dispositivi di rete non devono più sapere chi sono gli utenti autorizzati. Devono semplicemente chiedere al server RADIUS se una determinata connessione è autorizzata oppure no.

In questo senso RADIUS rappresenta un **punto centrale di decisione per l’accesso alla rete**.

Il protocollo RADIUS è stato standardizzato dallo **IETF** ed è uno dei protocolli AAA più diffusi. Nel tempo è stato affiancato da un protocollo più moderno chiamato **DIAMETER**, progettato per architetture più scalabili e con maggiore sicurezza, ma RADIUS rimane ancora oggi estremamente diffuso nelle infrastrutture di rete.

---

# 2) Il modello AAA

Il funzionamento di RADIUS è basato sul modello **AAA**, che rappresenta tre funzioni fondamentali per la gestione dell’accesso a una rete.

## Authentication

L’autenticazione consiste nella verifica dell’identità di un utente o di un dispositivo.

Quando un utente tenta di connettersi alla rete, il sistema deve stabilire se quell’utente è realmente chi dichiara di essere. Questo processo può utilizzare diversi meccanismi di autenticazione, ad esempio:

username e password
certificati digitali
smart card
token OTP (One Time Password)

Nel contesto di una rete Wi-Fi enterprise, ad esempio, il dispositivo dell’utente invia le credenziali all’access point, che le inoltra al server RADIUS. Il server verifica queste credenziali e decide se accettarle oppure rifiutarle.

---

## Authorization

Una volta che l’identità dell’utente è stata verificata, il sistema deve stabilire **cosa quell’utente è autorizzato a fare**.

Non tutti gli utenti devono necessariamente avere lo stesso livello di accesso alla rete. In molte organizzazioni è utile differenziare i privilegi.

Ad esempio:

gli studenti possono accedere solo a Internet
i docenti possono accedere ai server interni
gli amministratori possono accedere ai dispositivi di rete

Il server RADIUS può quindi restituire al dispositivo di rete una serie di parametri che definiscono i permessi dell’utente. Tra questi possono esserci:

la VLAN da assegnare all’utente
le ACL da applicare
limiti di banda
tempo massimo di sessione

In questo modo l’autorizzazione diventa **dinamica** e controllata centralmente.

---

## Accounting

La terza componente del modello AAA è l’accounting.

L’accounting consiste nella registrazione delle informazioni relative alle sessioni di rete. In altre parole il sistema mantiene un registro delle attività svolte dagli utenti.

Queste informazioni possono includere:

ora di inizio della sessione
ora di fine della sessione
quantità di traffico generato
indirizzo IP assegnato

Questo tipo di informazioni può essere utile per diversi motivi:

analisi del traffico di rete
monitoraggio dell’utilizzo delle risorse
audit di sicurezza
conformità normativa

---

# 3) Come funziona una autenticazione tramite RADIUS

Per comprendere meglio il funzionamento del protocollo è utile analizzare il flusso tipico di una autenticazione Wi-Fi enterprise.

In questo scenario entrano in gioco tre componenti principali:

il client (cioè il dispositivo dell’utente)
l’access point o lo switch di rete
il server RADIUS

Il dispositivo di rete che controlla l’accesso viene chiamato **NAS (Network Access Server)**.

Quando l’utente tenta di connettersi alla rete Wi-Fi, il client non ottiene immediatamente accesso alla rete. L’access point blocca temporaneamente il traffico e richiede l’autenticazione.

Le credenziali inserite dall’utente vengono quindi inoltrate al server RADIUS. L’access point non verifica direttamente la password. Funziona semplicemente come intermediario tra il client e il server di autenticazione.

Il server RADIUS verifica le credenziali utilizzando uno dei suoi database interni oppure consultando una directory esterna, come Active Directory.

Se le credenziali sono valide, il server restituisce un messaggio di accettazione e può includere anche alcune informazioni di configurazione, ad esempio la VLAN da assegnare all’utente.

Solo a questo punto l’access point consente al client di accedere alla rete.

---

# 4) Porte e protocolli utilizzati

Il protocollo RADIUS utilizza normalmente il protocollo UDP per le comunicazioni tra i dispositivi di rete e il server di autenticazione.

Le porte più utilizzate sono:

UDP 1812 per autenticazione
UDP 1813 per accounting

In versioni storiche del protocollo venivano utilizzate anche le porte:

UDP 1645
UDP 1646

Nelle reti moderne vengono generalmente utilizzate le porte standard 1812 e 1813.

---

# 5) Dove si colloca un server RADIUS nella rete

Dal punto di vista architetturale il server RADIUS è generalmente collocato all’interno della rete aziendale, spesso su un server dedicato oppure integrato in un server di dominio.

Gli access point e gli switch di accesso non prendono decisioni autonome sull’autenticazione. Delegano sempre questa decisione al server RADIUS.

Questo significa che la logica di sicurezza è concentrata in un unico punto. In questo modo diventa molto più semplice gestire policy di accesso coerenti su tutta la rete.

In molte organizzazioni il server RADIUS è protetto da firewall e collocato in una zona di rete sicura, poiché rappresenta un componente critico dell’infrastruttura.

---

# 6) Integrazione con altri software

Un server RADIUS raramente funziona completamente da solo. Nella maggior parte dei casi è parte di un ecosistema più ampio di servizi di autenticazione e gestione delle identità.

Uno degli scenari più comuni è l’integrazione con una **directory aziendale**.

Le directory come Active Directory o LDAP contengono le informazioni sugli utenti dell’organizzazione. Invece di mantenere un database separato di utenti, il server RADIUS può interrogare direttamente queste directory.

In questo modo lo stesso account utente può essere utilizzato per molti servizi diversi:

accesso al computer aziendale
accesso alla rete Wi-Fi
accesso VPN
accesso a sistemi applicativi

Questo approccio consente di mantenere una gestione centralizzata degli utenti e delle credenziali.

Un’altra integrazione molto frequente riguarda i firewall e i sistemi VPN. Molti firewall aziendali utilizzano RADIUS per autenticare gli utenti che si collegano da remoto tramite VPN.

In ambienti più complessi RADIUS può anche essere integrato in sistemi di **Network Access Control (NAC)**. In questi sistemi l’autenticazione non si limita a verificare le credenziali dell’utente ma controlla anche lo stato di sicurezza del dispositivo.

Ad esempio un sistema NAC può verificare:

la presenza di antivirus aggiornato
il livello delle patch di sicurezza
la conformità alle policy aziendali

Se il dispositivo non soddisfa questi requisiti può essere collocato automaticamente in una VLAN isolata.

---

# 7) Differenze tra RADIUS e Active Directory

Una fonte comune di confusione è la relazione tra RADIUS e Active Directory.

Questi due sistemi svolgono ruoli diversi.

Active Directory è una **directory centralizzata di identità**. Il suo scopo principale è memorizzare informazioni sugli utenti, sui gruppi e sui computer della rete.

Active Directory fornisce servizi di autenticazione basati principalmente sul protocollo **Kerberos** e può essere interrogato tramite il protocollo **LDAP**.

RADIUS invece è un **protocollo di autenticazione per l’accesso alla rete**.

Non è una directory di utenti nel senso classico del termine. Il suo compito principale è decidere se un utente può accedere alla rete e con quali privilegi.

Molto spesso RADIUS utilizza Active Directory come backend per la verifica delle credenziali. In questo caso il server RADIUS riceve la richiesta di autenticazione e la inoltra alla directory.

Se Active Directory conferma che la password è corretta, il server RADIUS autorizza la connessione.

---

# 8) Esempi di server RADIUS

Esistono diversi server RADIUS.

Uno dei più diffusi nel mondo open source è **FreeRADIUS**, utilizzato in università, ISP e molte infrastrutture aziendali.

FreeRADIUS è estremamente flessibile e supporta numerosi backend di autenticazione, tra cui LDAP e Active Directory.

In ambienti Windows è molto comune utilizzare **Microsoft NPS (Network Policy Server)**, che è integrato direttamente nel sistema operativo Windows Server.

Nelle infrastrutture di rete enterprise sono diffusi anche sistemi più avanzati come **Cisco ISE**, che integrano funzionalità di autenticazione, autorizzazione e controllo avanzato degli accessi alla rete.

---

# 9) Installare un server RADIUS gratuito su un PC domestico

## Macchina virtuale

Uno dei modi migliori per comprendere il funzionamento di RADIUS è installare un server di prova.

FreeRADIUS può essere installato facilmente su una macchina Linux, ad esempio su una macchina virtuale con Ubuntu Server.

Il sistema può essere installato scaricando l’immagine dal sito ufficiale:

[https://ubuntu.com/download/server](https://ubuntu.com/download/server)

Dopo l’installazione del sistema operativo è possibile installare FreeRADIUS tramite il gestore di pacchetti.

Aggiornare prima l’elenco dei pacchetti:

```
sudo apt update
```

Installare il server RADIUS:

```
sudo apt install freeradius
```

Una volta completata l’installazione il servizio può essere avviato con:

```
sudo systemctl start freeradius
```

Per verificare che il servizio sia attivo si può usare il comando:

```
sudo systemctl status freeradius
```

Uno degli strumenti più utili per imparare il funzionamento del server è la modalità debug.

Il comando:

```
sudo freeradius -X
```

avvia il server mostrando in tempo reale tutte le operazioni interne e le richieste di autenticazione.

Questo è estremamente utile per capire come il server gestisce le richieste AAA.

---  

## Freeradius da docker

URL utili:  
Docker Hub, immagine ufficiale:  
[https://hub.docker.com/r/freeradius/freeradius-server/](https://hub.docker.com/r/freeradius/freeradius-server/)  

FreeRADIUS su GitHub:  
[https://github.com/FreeRADIUS/freeradius-server](https://github.com/FreeRADIUS/freeradius-server)  

Documentazione FreeRADIUS Docker/LDAP: [https://www.freeradius.org/documentation/freeradius-server/4.0.0/howto/modules/ldap/bootstrap_openldap/docker.html](https://www.freeradius.org/documentation/freeradius-server/4.0.0/howto/modules/ldap/bootstrap_openldap/docker.html)  


Di seguito viene mostrato un setup semplice, adatto a laboratorio o uso didattico, su Windows con Docker Desktop oppure su Linux. Il principio è questo: non conviene partire dal container “vuoto” e poi modificare file all’interno; conviene invece preparare una piccola cartella locale di configurazione e costruire una propria immagine sopra quella ufficiale, come suggerito anche su Docker Hub. ([hub.docker.com][1])

1. Prerequisiti

Installare Docker Desktop. Su Windows normalmente viene usato con WSL 2. Per verificare il corretto funzionamento:

```
docker --version
docker compose version
```

Se questi comandi rispondono correttamente, si può procedere. La parte FreeRADIUS non richiede altro lato host, tranne che per i test: il comando `radtest` è fornito dagli strumenti FreeRADIUS e la documentazione ufficiale lo usa per verificare l’autenticazione. ([hub.docker.com][1])

2. Struttura minima della cartella di lavoro

Creare una cartella, ad esempio:

```
freeradius-docker/
```

All’interno creare questa struttura:

```
freeradius-docker/
    Dockerfile
    raddb/
        clients.conf
        mods-config/
            files/
                authorize
```

Questa struttura deriva dall’esempio ufficiale, che mostra una `Dockerfile` con `COPY raddb/ /etc/raddb/`, un `clients.conf` e il file utenti `mods-config/files/authorize`. ([hub.docker.com][1])

3. File Dockerfile

Nel file `Dockerfile` inserire:

```
FROM freeradius/freeradius-server:latest
COPY raddb/ /etc/raddb/
```

Questo è esattamente il modello mostrato nella documentazione Docker Hub dell’immagine ufficiale. ([hub.docker.com][1])

4. File clients.conf

Nel file `raddb/clients.conf` inserire una definizione client minima. Per laboratorio locale, se il test arriva dalla macchina host o da una rete Docker vicina, si può iniziare con un intervallo ampio solo per prove:

```
client dockernet {
    ipaddr = 172.17.0.0/16
    secret = testing123
}
```

L’esempio ufficiale usa proprio un blocco simile con rete Docker `172.17.0.0/16` e secret `testing123`. In un ambiente reale conviene restringere molto l’indirizzo IP del client RADIUS e usare un secret robusto. ([hub.docker.com][1])

Se si desidera testare da localhost e dalla macchina host, in alcuni casi può essere più semplice aggiungere anche un client locale esplicito:

```
client localhost {
    ipaddr = 127.0.0.1
    secret = testing123
}
```

Questa seconda parte è una normale scelta pratica di configurazione; il punto importante, confermato dalla documentazione ufficiale, è che senza definire i client in `clients.conf` il server nel container non risponde alle query reali. ([hub.docker.com][1])

5. File authorize con un primo utente

Nel file `raddb/mods-config/files/authorize` inserire almeno un utente di test:

```
bob    Cleartext-Password := "test"
```

Docker Hub mostra proprio questo esempio e specifica che poi l’autenticazione si può verificare con `radtest bob test 127.0.0.1 0 testing123`, ottenendo `Access-Accept`. ([hub.docker.com][1])

Si possono aggiungere anche altri utenti, per esempio:

```
alice  Cleartext-Password := "alice123"
mario  Cleartext-Password := "mario123"
```

6) Costruzione dell’immagine

Dalla cartella `freeradius-docker/` eseguire:

```
docker build -t my-radius-image -f Dockerfile .
```

La documentazione ufficiale mostra esattamente questo flusso: costruire una propria immagine locale a partire da quella ufficiale e dalla cartella `raddb`. ([hub.docker.com][1])

7. Avvio normale del container

Per esporre autenticazione e accounting, avviare:

```
docker run --rm -d --name my-radius -p 1812-1813:1812-1813/udp my-radius-image
```

La documentazione ufficiale indica proprio il forwarding di `1812/udp` e `1813/udp`, che sono le porte tipiche usate dal server per autenticazione e accounting. ([hub.docker.com][1])

8. Avvio in debug, molto consigliato

Per studiare davvero FreeRADIUS, la modalità corretta è il debug:

```
docker run --rm --name my-radius -t -p 1812-1813:1812-1813/udp my-radius-image -X
```

La documentazione ufficiale afferma esplicitamente che FreeRADIUS “should always be tested in debug mode” con `-X`, e aggiunge che il flag `-t` serve anche per l’output colorato. Questa è la modalità migliore per capire cosa succede durante l’autenticazione. ([hub.docker.com][1])

9. Come testare il server

La documentazione ufficiale usa `radtest`. Da una macchina Linux o da WSL si può installare il client FreeRADIUS e poi eseguire:

```
radtest bob test 127.0.0.1 0 testing123
```

Se tutto è corretto, il server deve rispondere con:

```
Access-Accept
```

Questo test verifica contemporaneamente tre cose: il client è autorizzato in `clients.conf`, l’utente esiste nel file `authorize`, e il container è raggiungibile sulla porta UDP 1812. ([hub.docker.com][1])

Su Windows puro, se non si vuole usare WSL, si può comunque lavorare così:

* eseguire il container con Docker Desktop
* aprire una shell Linux in WSL solo per lanciare `radtest`
* in alternativa usare un client RADIUS esterno di test

Per uso didattico, WSL è spesso la soluzione più lineare.

10. Cosa osservare nella console di debug

Quando si avvia il server con `-X`, conviene guardare questi punti:

* ricezione di `Access-Request`
* identificazione del client RADIUS
* ricerca dell’utente nel file `authorize`
* verifica della password
* produzione di `Access-Accept` oppure `Access-Reject`

La documentazione ufficiale rimanda anche a linee guida per leggere l’output di debug. ([hub.docker.com][1])

11. Variante con immagine Alpine

L’immagine ufficiale offre anche varianti Alpine, più piccole. Docker Hub segnala però che le immagini `-alpine` sono più leggere ma, per mantenere la dimensione bassa, non includono tutte le librerie necessarie per tutti i moduli; se servono moduli aggiuntivi, bisogna installare le librerie nel proprio Dockerfile. Quindi, per un primo laboratorio, è più semplice partire dalla variante standard; per ridurre l’ingombro, si può poi passare a `latest-3.2-alpine` o ad altra tag Alpine. ([hub.docker.com][1])

Esempio Dockerfile Alpine:

```
FROM freeradius/freeradius-server:latest-3.2-alpine
COPY raddb/ /etc/raddb/
```

12) Persistenza e modifica della configurazione

Per laboratorio, costruire l’immagine con `COPY` è il modo più pulito. Se invece si desidera modificare la configurazione più rapidamente senza ricostruire ogni volta, si può usare un bind mount. Esempio:

```
docker run --rm --name my-radius -t \
    -p 1812-1813:1812-1813/udp \
    -v ${PWD}/raddb:/etc/raddb \
    freeradius/freeradius-server:latest -X
```

Su Windows PowerShell, `${PWD}` funziona, ma a volte è più semplice usare il percorso assoluto completo. Questa parte è una pratica Docker generale; la posizione `/etc/raddb` nel container è coerente con l’esempio ufficiale di Docker Hub. ([hub.docker.com][1])

13. Uso con Docker Compose

Per non dover ricordare ogni volta il comando lungo, conviene creare un `compose.yaml`:

```
services:
  freeradius:
    image: my-radius-image
    container_name: my-radius
    ports:
      - "1812:1812/udp"
      - "1813:1813/udp"
    command: ["-X"]
```

Poi avviare con:

```
docker compose up
```

Questa soluzione non è mostrata direttamente nella documentazione ufficiale dell’immagine, ma è equivalente al `docker run` ufficiale con `-X` e con il mapping delle stesse due porte UDP. Le informazioni fondamentali, cioè porta 1812/1813 e avvio con `-X`, vengono dalla documentazione ufficiale. ([hub.docker.com][1])

14. Integrazione con LDAP in container

Se più avanti si desidera integrare FreeRADIUS con LDAP, la documentazione ufficiale FreeRADIUS contiene una guida Docker specifica per avviare anche un container OpenLDAP, con schema e dati di test. Questa parte è utile quando si vuole superare il semplice file `authorize` e passare a una directory esterna. La guida mostra l’uso di `osixia/openldap`, il caricamento degli schema FreeRADIUS e la popolazione dei dati di test. ([freeradius.org][2])

15. Errori tipici

Gli errori più comuni, in pratica, sono questi.

Primo: dimenticare `clients.conf`. In tal caso FreeRADIUS vede la richiesta ma non considera affidabile il client che la invia. Docker Hub è esplicito: senza aggiungere i client e gli utenti minimi, il container rifiuta le query. ([hub.docker.com][1])

Secondo: secret diverso tra test client e `clients.conf`. Se in `clients.conf` c’è `testing123`, anche `radtest` deve usare `testing123`. L’esempio ufficiale usa proprio questa corrispondenza. ([hub.docker.com][1])

Terzo: testare senza modalità debug. In teoria il server parte anche normalmente, ma per capire perché un’autenticazione fallisce la modalità `-X` è quasi indispensabile. La documentazione ufficiale la raccomanda esplicitamente. ([hub.docker.com][1])

Quarto: usare certificati di default in scenari seri. Docker Hub segnala che l’immagine contiene certificati self-signed “for convenience” e che non devono essere usati in produzione. ([hub.docker.com][1])

16. Setup minimo completo, pronto da copiare

Contenuto dei file:

`Dockerfile`

```
FROM freeradius/freeradius-server:latest
COPY raddb/ /etc/raddb/
```

`raddb/clients.conf`

```
client localhost {
    ipaddr = 127.0.0.1
    secret = testing123
}

client dockernet {
    ipaddr = 172.17.0.0/16
    secret = testing123
}
```

`raddb/mods-config/files/authorize`

```
bob    Cleartext-Password := "test"
alice  Cleartext-Password := "alice123"
```

Comandi:

```
docker build -t my-radius-image -f Dockerfile .
docker run --rm --name my-radius -t -p 1812:1812/udp -p 1813:1813/udp my-radius-image -X
```

Test:

```
radtest bob test 127.0.0.1 0 testing123
radtest alice alice123 127.0.0.1 0 testing123
```

17) Quando questo setup ha senso

Questo setup ha senso per:

* imparare il funzionamento base di FreeRADIUS
* fare test AAA locali
* simulare autenticazione per un laboratorio 802.1X o VPN
* preparare poi una fase successiva con LDAP o Active Directory

Per produzione, invece, il semplice file `authorize` non basta quasi mai: si passa tipicamente a backend come LDAP, OpenLDAP o Microsoft Active Directory, che FreeRADIUS supporta secondo la descrizione dell’immagine ufficiale. ([hub.docker.com][1])

## Alcuni riferimenti

Docker Hub, immagine ufficiale FreeRADIUS:
[https://hub.docker.com/r/freeradius/freeradius-server/](https://hub.docker.com/r/freeradius/freeradius-server/)

GitHub ufficiale FreeRADIUS:
[https://github.com/FreeRADIUS/freeradius-server](https://github.com/FreeRADIUS/freeradius-server)

Documentazione FreeRADIUS su Docker e LDAP:
[https://www.freeradius.org/documentation/freeradius-server/4.0.0/howto/modules/ldap/bootstrap_openldap/docker.html](https://www.freeradius.org/documentation/freeradius-server/4.0.0/howto/modules/ldap/bootstrap_openldap/docker.html)

Se serve, nel messaggio successivo si può fornire anche una versione già pronta con:

* `compose.yaml`
* configurazione EAP/PEAP
* integrazione iniziale con Active Directory
* mini lab didattico passo passo per studenti.

[1]: https://hub.docker.com/r/freeradius/freeradius-server/ "freeradius/freeradius-server - Docker Image"
[2]: https://www.freeradius.org/documentation/freeradius-server/4.0.0/howto/modules/ldap/bootstrap_openldap/docker.html "Docker :: The FreeRADIUS project - Documentation"


---

# LAB 1 – Osservare il funzionamento interno di RADIUS

Il primo laboratorio ha l’obiettivo di osservare il comportamento del server durante una richiesta di autenticazione.

Per eseguire il laboratorio è necessario installare il pacchetto contenente gli strumenti di test:

```
sudo apt install freeradius-utils
```

Successivamente si può eseguire un test di autenticazione utilizzando il comando:

```
radtest testuser password123 localhost 0 testing123
```

Nel terminale dove è stato avviato il server in modalità debug sarà possibile osservare tutte le fasi dell’autenticazione.

Questo permette di comprendere come il server riceve la richiesta, verifica le credenziali e genera la risposta.

---

# LAB 2 – Creare utenti locali

Nel file di configurazione degli utenti è possibile aggiungere credenziali locali.

Il file si trova normalmente in:

```
/etc/freeradius/3.0/users
```

Aggiungendo alcune righe come:

```
studente1 Cleartext-Password := "1234"
studente2 Cleartext-Password := "abcd"
```

si possono creare utenti di test.

Dopo aver riavviato il servizio è possibile verificare il funzionamento utilizzando il comando radtest.

Questo laboratorio consente di capire come il server RADIUS gestisce il proprio database interno di utenti.

---

# 10) Integrazione con Active Directory

Nelle infrastrutture reali il server RADIUS non contiene quasi mai un database locale di utenti.

Nella maggior parte dei casi utilizza una directory centrale come Active Directory.

Questo permette agli utenti di utilizzare le stesse credenziali per:

accesso al computer aziendale
accesso alla rete Wi-Fi
accesso VPN

L’integrazione viene normalmente realizzata utilizzando il protocollo LDAP oppure tramite meccanismi di autenticazione Kerberos.

Il server RADIUS diventa quindi un intermediario tra i dispositivi di rete e la directory aziendale.

---

# LAB 3 – Integrazione concettuale con Active Directory

In un laboratorio più avanzato è possibile integrare FreeRADIUS con Active Directory.

Questo richiede la presenza di un server Windows configurato come controller di dominio.

Il server FreeRADIUS deve essere configurato per interrogare Active Directory tramite LDAP.

Questo avviene modificando i file di configurazione relativi al modulo LDAP e specificando:

indirizzo del server
base DN
credenziali di accesso

Una volta completata la configurazione il server RADIUS utilizzerà la directory per verificare le password degli utenti.

In questo modo qualsiasi utente del dominio potrà autenticarsi sulla rete Wi-Fi enterprise.

---

# Conclusione

Il protocollo RADIUS rappresenta uno dei pilastri dell’autenticazione nelle reti moderne.

Attraverso il modello AAA consente di centralizzare il controllo degli accessi alla rete, applicare policy di sicurezza e monitorare l’utilizzo delle risorse.

La sua integrazione con sistemi di directory come Active Directory lo rende uno strumento estremamente potente per la gestione delle identità nelle infrastrutture aziendali.

Comprendere il funzionamento di RADIUS è quindi fondamentale per chi si occupa di progettazione e gestione delle reti.


