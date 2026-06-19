# SOLUZIONE SCOLASTICA

## Ipotesi iniziali

Si ipotizza che la società abbia una sede centrale con alcuni uffici tecnici e che possa gestire contemporaneamente 2 o 3 cantieri.

Per ogni cantiere si ipotizza la presenza di:

* alcuni tablet rugged usati dagli operatori;
* uno o due dispositivi di scansione 3D;
* alcune fotocamere timelapse;
* vari sensori di sicurezza;
* una piccola infrastruttura di rete temporanea;
* un collegamento verso Internet e verso la sede centrale.

Il sistema BIM non viene trattato dal punto di vista edilizio, ma dal punto di vista informatico.  
Per la rete, infatti, il problema principale è trasferire dati tra cantiere e sede centrale in modo sicuro e affidabile.

## PRIMA PARTE

## 1. Infrastruttura di rete da realizzare in un cantiere

In ogni cantiere si può realizzare una rete locale temporanea, installata in un piccolo armadio di rete. La rete deve collegare tablet, fotocamere, sensori e apparati di trasmissione verso la sede centrale.

Uno schema generale può essere il seguente:

```
Tablet rugged / scanner 3D / LiDAR
             |
          Wi-Fi
             |
      Access point
             |
      Switch gestito
             |
      Router / Firewall
             |
    Collegamento Internet
   fibra / FWA / 4G / 5G
             |
          VPN
             |
       Sede centrale
```

Alla stessa rete sono collegati anche:

```
Fotocamere timelapse
             |
    Wi-Fi oppure cavo Ethernet
             |
      Switch gestito

Sensori di sicurezza
             |
      Gateway sensori
             |
      Switch / Router
```

Il router/firewall è l’apparato principale del cantiere, perché collega la rete locale alla rete geografica e protegge i dispositivi interni. Lo switch permette di collegare più apparati tramite cavo. Gli access point permettono il collegamento Wi-Fi dei tablet e di altri dispositivi mobili.

Per alimentare fotocamere e access point può essere utile uno switch PoE.  
Il PoE permette di alimentare alcuni dispositivi usando lo stesso cavo Ethernet usato per i dati.

## Suddivisione della rete del cantiere

Per evitare che tutti i dispositivi siano nella stessa rete, conviene usare VLAN diverse.  
Una VLAN è una rete logica separata creata sugli switch.

Esempio di indirizzamento per il cantiere 1:

```
Rete generale del cantiere:
    10.10.1.0/24

VLAN 10 - Tablet e strumenti BIM:
    10.10.1.0/26

VLAN 20 - Fotocamere timelapse:
    10.10.1.64/26

VLAN 30 - Sensori di sicurezza:
    10.10.1.128/26

VLAN 40 - Gestione apparati:
    10.10.1.192/27
```

Per il cantiere 2 si può usare:

```
10.10.2.0/24
```

Per il cantiere 3:

```
10.10.3.0/24
```

In questo modo ogni cantiere ha una rete privata diversa e non si creano conflitti di indirizzi.

## Servizi di rete nel cantiere

Nel cantiere si possono usare i seguenti servizi:

```
DHCP
    per assegnare automaticamente gli indirizzi IP ai dispositivi

DNS
    per risolvere i nomi dei server

NTP
    per mantenere sincronizzato l’orario dei dispositivi

VPN
    per collegare in modo sicuro il cantiere alla sede centrale

HTTPS / SFTP
    per trasferire dati e file in modo sicuro

Syslog
    per inviare log alla sede centrale
```

Per i sensori si può usare un gateway locale che raccoglie i dati e li invia alla sede centrale. Il gateway è utile perché molti sensori non devono comunicare direttamente con Internet.

## Sicurezza della rete del cantiere

La rete Wi-Fi deve essere protetta almeno con WPA2 o WPA3. Se possibile, è meglio usare autenticazione personale degli utenti, non una password unica condivisa.

Il firewall deve permettere solo il traffico necessario. Ad esempio:

* i tablet possono accedere al server BIM;
* le fotocamere possono inviare immagini al repository;
* i sensori possono inviare dati al server di monitoraggio;
* gli apparati di rete possono essere gestiti solo dagli amministratori.

È utile prevedere anche un piccolo NAS o mini-server locale. Questo serve a salvare temporaneamente i dati nel caso in cui il collegamento Internet cada. Quando il collegamento torna disponibile, i dati possono essere inviati alla sede centrale.

## 2. Rete pre-esistente nella sede centrale e proposte di potenziamento

La sede centrale dispone già di una rete locale e di una connessione ADSL. Si può ipotizzare una situazione iniziale di questo tipo:

```
Internet ADSL
      |
   Router
      |
   Switch
      |
PC uffici tecnici
```

Questa rete può essere sufficiente per un normale ufficio, ma non è sufficiente per gestire più cantieri e grandi quantità di dati BIM.

Si propone quindi di potenziare la rete in questo modo:

```
Internet fibra
      |
Firewall aziendale
      |
Switch principale gestito
      |
-------------------------
|          |            |
```

Server     PC uffici     Wi-Fi
BIM       tecnici       aziendale
|
NAS / Storage / Backup

Inoltre si può mantenere una linea secondaria di backup, ad esempio ADSL o 5G, da usare se la linea principale non funziona.

## Miglioramenti necessari

La sede centrale dovrebbe avere:

* connessione in fibra al posto della sola ADSL;
* firewall aziendale;
* switch gestiti;
* server per il sistema BIM;
* NAS o server di archiviazione;
* sistema di backup;
* server di autenticazione;
* separazione della rete tramite VLAN;
* sistema di monitoraggio e raccolta log.

L’ADSL è considerata datata perché ha una capacità limitata, soprattutto in upload. Nel caso dei cantieri il traffico in upload è importante, perché i dati vengono inviati dai cantieri alla sede.

## VLAN nella sede centrale

Anche nella sede centrale conviene dividere la rete:

```
VLAN 10 - Uffici tecnici
VLAN 20 - Server BIM
VLAN 30 - Amministrazione apparati
VLAN 40 - Collegamenti VPN dai cantieri
VLAN 50 - Wi-Fi ospiti
```

Questa separazione migliora la sicurezza. Ad esempio, un dispositivo ospite non deve poter accedere direttamente ai server BIM.

## 3. Canali di comunicazione tra cantieri e sede centrale

Il traffico tra cantieri e sede centrale è composto da dati diversi.

I dati dei sensori sono piccoli, ma devono essere inviati in modo affidabile. Le immagini delle fotocamere timelapse sono più pesanti. Le nuvole di punti generate dagli scanner 3D possono essere molto grandi.

Per questo motivo il collegamento tra cantiere e sede deve avere una buona banda, soprattutto in upload.

Si può stimare in modo semplice:

```
sensori:
    meno di 1 Mbps

fotocamere timelapse:
    alcuni Mbps, in base alla frequenza degli scatti

scansioni 3D:
    traffico molto più pesante, anche decine o centinaia di MB per sessione
```

Per ogni cantiere si può prevedere:

* collegamento principale in fibra, se disponibile;
* in alternativa FWA o 5G;
* router con SIM di backup;
* VPN site-to-site verso la sede centrale.

FWA significa collegamento radio fisso. La VPN site-to-site è un tunnel cifrato permanente tra due reti, ad esempio tra il cantiere e la sede centrale.

Per la sede centrale si propone una connessione più potente, ad esempio fibra FTTH/FTTC business. Sarebbe opportuno avere almeno alcune centinaia di Mbps, perché la sede deve ricevere dati da più cantieri.

Il trasferimento dei file più grandi può essere programmato in orari di minore utilizzo, ad esempio a fine giornata o di notte. Invece i dati dei sensori devono avere priorità maggiore perché possono riguardare la sicurezza.

Per gestire le priorità si può usare QoS. Il QoS permette di dare precedenza ad alcuni tipi di traffico rispetto ad altri.

## Apparati da adottare

Nel cantiere:

* router/firewall con supporto VPN;
* switch gestito;
* access point Wi-Fi;
* eventuale gateway per sensori;
* eventuale NAS locale;
* modem 4G/5G o apparato FWA;
* UPS.

Nella sede centrale:

* firewall aziendale;
* router verso Internet;
* switch core gestito;
* server BIM;
* NAS o storage;
* server di autenticazione;
* sistema di backup;
* sistema di monitoraggio.

## 4. Autenticazione degli operatori

Gli operatori devono potersi autenticare sia quando si trovano nella sede centrale sia quando lavorano dai cantieri.

Si può usare un sistema centralizzato di gestione utenti, ad esempio Active Directory o LDAP. In questo modo ogni operatore ha un proprio account personale.

Esempio di gestione:

```
progettisti:
    accesso ai modelli BIM e ai documenti tecnici

operatori di cantiere:
    caricamento scansioni, immagini e dati

responsabili sicurezza:
    accesso ai dati dei sensori e agli allarmi

amministratori:
    gestione degli apparati e dei server
```

Per l’accesso Wi-Fi si può usare WPA2/WPA3 Enterprise, che consente di autenticare gli utenti tramite credenziali personali. Per l’accesso remoto dai cantieri si usa una VPN.

La VPN deve richiedere:

* username;
* password robusta;
* eventualmente autenticazione a due fattori;
* permessi in base al ruolo.

L’autenticazione a due fattori richiede un secondo controllo, ad esempio un codice temporaneo, e rende l’accesso più sicuro.

Tutti gli accessi devono essere registrati nei log, in modo da poter controllare eventuali problemi di sicurezza.

## SECONDA PARTE

La traccia chiede di svolgere due quesiti, ma qui vengono svolti tutti e quattro.

## Quesito I - Archiviazione on premise e cloud-based

Per archiviare scansioni, immagini, dati dei sensori e modelli BIM si possono usare soluzioni on premise oppure cloud-based.

Una soluzione on premise significa che i server e i dati sono conservati nella sede centrale dell’azienda.

Una soluzione cloud-based significa che i dati sono conservati presso un fornitore esterno e raggiunti tramite Internet.

## Soluzione on premise

Nella soluzione on premise l’azienda installa nella sede centrale:

* server BIM;
* NAS o storage;
* sistema di backup;
* firewall;
* sistemi di autenticazione.

Vantaggi:

* maggiore controllo diretto sui dati;
* velocità buona per gli utenti nella sede centrale;
* minore dipendenza da servizi esterni;
* possibilità di configurare direttamente server e permessi.

Svantaggi:

* costo iniziale più alto;
* necessità di manutenzione interna;
* maggiore responsabilità su backup e sicurezza;
* scalabilità più difficile.

## Soluzione cloud-based

Nella soluzione cloud i dati vengono salvati su piattaforme esterne accessibili tramite Internet.

Vantaggi:

* accesso più semplice da cantieri diversi;
* maggiore scalabilità;
* backup e ridondanza spesso già disponibili;
* collaborazione più facile tra utenti in luoghi diversi.

Svantaggi:

* dipendenza dalla connessione Internet;
* costi mensili o annuali;
* necessità di controllare sicurezza e privacy;
* possibile lentezza nel trasferimento di file molto grandi.

## Soluzione proposta

Una soluzione equilibrata è ibrida.

Si può mantenere nella sede centrale un server/NAS per i dati usati più spesso e usare il cloud per backup o condivisione esterna.

Schema:

```
Cantieri
   |
   | VPN
   |
Sede centrale
   |
Server / NAS BIM
   |
Backup cloud cifrato
```

Questa scelta è realistica perché unisce controllo locale e maggiore sicurezza in caso di guasto grave nella sede.

## Quesito II - Sicurezza informatica e continuità trasmissiva

Oltre all’autenticazione, servono altre misure di sicurezza.

## Sicurezza nei cantieri

Nei cantieri si possono adottare:

* rete Wi-Fi protetta;
* VLAN separate;
* firewall locale;
* password robuste;
* aggiornamento degli apparati;
* accesso agli apparati solo agli amministratori;
* cifratura delle comunicazioni;
* raccolta dei log.

Le VLAN sono utili perché separano tablet, sensori, fotocamere e apparati di gestione. In questo modo, se un dispositivo ha un problema, non compromette automaticamente tutta la rete.

## Sicurezza nella sede centrale

Nella sede centrale si devono usare:

* firewall;
* VPN;
* antivirus sui PC;
* backup;
* permessi differenziati;
* aggiornamenti periodici;
* monitoraggio;
* log centralizzati.

I server BIM devono essere accessibili solo agli utenti autorizzati. Non devono essere pubblicati direttamente su Internet.

## Sicurezza della comunicazione remota

La comunicazione tra cantiere e sede deve avvenire tramite VPN cifrata. Si possono usare tecnologie come IPsec o OpenVPN.

La VPN protegge i dati durante il passaggio su Internet. Anche se qualcuno intercettasse il traffico, non potrebbe leggerlo facilmente.

## Continuità del collegamento

Per garantire continuità trasmissiva si possono usare:

* doppia connessione Internet nella sede centrale;
* collegamento di backup nei cantieri, ad esempio 5G;
* router con failover automatico;
* UPS per router, firewall e switch;
* salvataggio temporaneo locale dei dati;
* monitoraggio della linea.

Il failover è il passaggio automatico alla connessione di riserva quando quella principale non funziona.

Per i sensori di sicurezza è importante che gli allarmi locali funzionino anche se la sede centrale non è raggiungibile. Il cantiere deve quindi avere un sistema locale capace di generare almeno gli avvisi più importanti.

## Quesito III - Blocco delle piattaforme di Intelligenza Artificiale in una scuola

In questo quesito il contesto è diverso dalla prima parte. Non si tratta di una rete aziendale, ma di una rete didattica scolastica.

In una scuola la soluzione deve essere proporzionata, semplice da gestire e limitata ai laboratori o agli orari in cui serve. Non si deve progettare una infrastruttura troppo complessa come quella di una grande azienda.

Il problema è impedire agli studenti, durante certe attività di laboratorio, di usare piattaforme di Intelligenza Artificiale per farsi generare il codice.

## Struttura della rete scolastica

La rete della scuola può essere divisa in reti separate:

```
VLAN 10 - Segreteria
VLAN 20 - Docenti
VLAN 30 - Laboratorio informatico 1
VLAN 31 - Laboratorio informatico 2
VLAN 40 - Wi-Fi studenti
VLAN 50 - Ospiti
```

Il blocco delle piattaforme AI deve essere applicato soprattutto alle VLAN dei laboratori durante verifiche o esercitazioni specifiche.

## Misure tecniche

Si possono usare:

* firewall scolastico;
* filtro DNS;
* proxy web;
* blocco di categorie di siti;
* blocco di domini specifici;
* regole per fascia oraria;
* regole per laboratorio;
* autenticazione degli utenti.

Il filtro DNS impedisce ai computer di raggiungere certi nomi di dominio. Il proxy web controlla il traffico web degli utenti.

Esempio:

```
Laboratorio 1
dalle 10:00 alle 12:00
blocco siti AI attivo

Laboratorio 2
nessun blocco, se non ci sono verifiche

rete docenti
accesso consentito
```

Si può anche impedire agli studenti di usare DNS esterni, obbligandoli a usare il DNS della scuola. Altrimenti potrebbero aggirare facilmente alcuni blocchi.

## Schedulazione del blocco

Il blocco può essere programmato nel firewall o nel proxy.

Esempio:

```
lunedì 3ª e 4ª ora
VLAN laboratorio 1
bloccare piattaforme AI

martedì 1ª ora
VLAN laboratorio 2
bloccare piattaforme AI
```

Alla fine della fascia oraria il blocco viene rimosso automaticamente.

In una soluzione scolastica è utile permettere ai docenti o all’amministratore di attivare/disattivare il blocco in base al calendario delle verifiche.

## Limiti della soluzione

Queste misure non sono perfette. Uno studente potrebbe usare:

* smartphone personale con rete mobile;
* VPN;
* siti non ancora bloccati;
* proxy esterni;
* nuovi servizi AI.

Per questo la soluzione tecnica deve essere accompagnata da regole didattiche e organizzative:

* spiegare chiaramente quando l’uso dell’AI è vietato;
* controllare i laboratori durante le prove;
* valutare anche la spiegazione orale del codice;
* usare esercizi in cui lo studente deve dimostrare di capire quello che scrive;
* eventualmente disattivare Internet durante alcune verifiche pratiche.

Quindi la rete può aiutare, ma non risolve da sola tutto il problema.

## Quesito IV - Comando SSH e port forwarding

Il comando è:

```
ssh -p 25500 administrator@200.1.1.1
```

SSH è un protocollo che permette di accedere da remoto a un dispositivo tramite terminale in modo cifrato.

L’opzione:

```
-p 25500
```

indica che non si usa la porta standard di SSH, che è la 22, ma la porta 25500.

L’indirizzo:

```
200.1.1.1
```

è il dispositivo raggiungibile dall’esterno, probabilmente un router o firewall con indirizzo pubblico.

La traccia dice che su questo dispositivo è configurata una regola che reindirizza il traffico in ingresso sulla porta 25500 verso il dispositivo interno:

```
172.16.1.100
```

Quindi, quando viene dato il comando, succede questo:

```
il client tenta una connessione SSH verso 200.1.1.1 porta 25500;
il router/firewall riceve la richiesta;
la regola di port forwarding inoltra il traffico al dispositivo 172.16.1.100;
l’utente administrator tenta di autenticarsi sul dispositivo interno.
```

Il dispositivo 172.16.1.100 ha un indirizzo privato, quindi normalmente non è raggiungibile direttamente da Internet.

Lo scopo del port forwarding è permettere di raggiungere dall’esterno un servizio che si trova dentro una rete privata.

Schema:

```
PC remoto
   |
   | ssh -p 25500 administrator@200.1.1.1
   |
Router pubblico
200.1.1.1:25500
   |
   | inoltro porta
   |
Host interno
172.16.1.100
```

Questa configurazione può servire per amministrare da remoto un server interno. Tuttavia deve essere usata con attenzione, perché espone un accesso SSH verso Internet.

Per renderla più sicura si dovrebbe:

* usare password robuste;
* meglio ancora usare chiavi SSH;
* permettere l’accesso solo da indirizzi IP autorizzati;
* registrare i log;
* aggiornare il sistema;
* preferire una VPN quando possibile.

La soluzione più sicura sarebbe collegarsi prima alla VPN e poi accedere via SSH all’indirizzo interno.

## Conclusione generale

La soluzione proposta prevede una rete di cantiere semplice ma ordinata, con router/firewall, switch, access point, sensori, fotocamere e collegamento sicuro alla sede centrale.

La sede centrale deve essere potenziata perché la vecchia connessione ADSL e una rete non segmentata non sono adatte a gestire il nuovo sistema BIM.

Le comunicazioni tra cantieri e sede devono usare VPN, banda sufficiente e collegamenti di backup. I dati più pesanti, come scansioni e immagini, possono essere trasferiti anche in modo programmato, mentre i dati dei sensori devono avere maggiore priorità.

Nel quesito scolastico, invece, non serve una soluzione aziendale complessa: è più corretto proporre firewall, filtro DNS, proxy, VLAN dei laboratori e blocchi programmati, sempre accompagnati da regole didattiche chiare.
