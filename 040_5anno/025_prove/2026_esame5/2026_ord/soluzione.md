## IPOTESI DI SOLUZIONE 

# Da rivedere, probabilmente contiene molti errori e imprecisioni, può essere utile per spunti puntuali

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

In ogni cantiere si può realizzare una rete locale temporanea, installata in un piccolo armadio di rete. La rete deve collegare tablet, scanner 3D/LiDAR, fotocamere, sensori, gateway e apparati di trasmissione verso la sede centrale.

Le fotocamere devono essere considerate a tutti gli effetti sensori digitali, in particolare sensori ottici. La distinzione principale non è quindi tra fotocamere e sensori, ma tra dispositivi che si collegano direttamente alla rete IP e dispositivi che richiedono un gateway.

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
      Router / Firewall del cantiere
             |
      CPE / modem / ONT / apparato FWA / router 4G-5G
             |
      Collegamento Internet
      fibra / FWA / 4G / 5G
             |
      Internet
             |
      Tunnel VPN site-to-site
             |
      Firewall sede centrale
             |
      Rete sede centrale
```

Il CPE è l’apparato che collega fisicamente il cantiere alla rete dell’operatore.  
Può essere, ad esempio, un modem fibra, un ONT, un apparato FWA oppure un router 4G/5G.

Il router/firewall può essere un apparato separato dal CPE oppure può coincidere con esso, se si usa un dispositivo integrato. Nel primo caso il CPE fornisce l’accesso a Internet, mentre il router/firewall gestisce la rete locale, le regole di sicurezza, il NAT, le eventuali VLAN e la VPN verso la sede centrale.

Per le VPN verso la sede centrale il protocollo consigliato è IPsec con IKEv2, in modalità **site-to-site**: IPsec/IKEv2 è uno standard molto diffuso nei firewall aziendali, supporta cifratura forte, autenticazione tra apparati e collegamento stabile tra due reti diverse.  
*(Viene invece scartata una VPN del tipo “client-to-site”, perché questa tipologia è volta a collegare un singolo utente alla sede centrale).*


Alla stessa rete locale possono essere collegati anche dispositivi IP collegati via cavo:

```
Fotocamere IP / timelapse / sensori IP
             |
      Cavo Ethernet
             |
      Switch gestito
```

Oppure dispositivi IP collegati via Wi-Fi:

```
Fotocamere IP / timelapse / sensori IP
             |
          Wi-Fi
             |
      Access point
             |
      Switch gestito
```

I sensori non IP non sono in grado di connettersi direttamente alla rete. Si collegano quindi a dispositivi ausiliari che si occupano di mediare tra sensori non IP e rete IP.  Questi dispositivi sono qui chiamati genericamente gateway.

```
Sensori non IP
ad esempio ambientali, strutturali o di sicurezza
             |
      Gateway sensori
             |
      Switch gestito
             |
      Router / Firewall
```

Lo switch permette di collegare più apparati tramite cavo. Gli access point permettono il collegamento Wi-Fi dei tablet e degli altri dispositivi mobili.

Per alimentare access point, fotocamere IP e alcuni sensori di rete può essere utile uno switch PoE, cioè Power over Ethernet. Il PoE permette di alimentare alcuni dispositivi usando lo stesso cavo Ethernet usato per i dati.

## Suddivisione della rete del cantiere

Per evitare che tutti i dispositivi siano nella stessa rete, conviene usare VLAN diverse.
Una VLAN è una rete logica separata creata sugli switch gestiti.

La sola creazione delle VLAN non basta però a garantire la sicurezza. È necessario anche configurare regole di routing e firewall tra le VLAN, in modo che ogni gruppo di dispositivi possa comunicare solo con i sistemi necessari.

Esempio di indirizzamento per il cantiere 1:

```
Rete aggregata del cantiere 1:
    10.10.1.0/24

VLAN 10 - Tablet e strumenti BIM:
    10.10.1.0/26

VLAN 20 - Fotocamere timelapse:
    10.10.1.64/26

VLAN 30 - Sensori di sicurezza:
    10.10.1.128/26

VLAN 40 - Gestione apparati:
    10.10.1.192/27

VLAN 50 - Servizi locali / NAS temporaneo:
    10.10.1.224/28

Spazio libero per espansioni future:
    10.10.1.240/28
```

La rete 10.10.1.0/24 rappresenta la rete complessiva assegnata al cantiere 1. Al suo interno vengono poi ricavate le singole sottoreti usate dalle VLAN.

Per il cantiere 2 si può usare:

```
Rete aggregata del cantiere 2:
    10.10.2.0/24
```

Per il cantiere 3:

```
Rete aggregata del cantiere 3:
    10.10.3.0/24
```

In questo modo ogni cantiere ha una rete privata diversa e non si creano conflitti di indirizzi.

## Servizi di rete nel cantiere

Nel cantiere si possono usare i seguenti servizi:

```
DHCP
    per assegnare automaticamente gli indirizzi IP ai dispositivi

DNS
    per risolvere i nomi dei server e dei servizi interni

NTP
    per mantenere sincronizzato l’orario dei dispositivi

VPN site-to-site
    per collegare in modo sicuro la rete del cantiere alla sede centrale

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

Il NAS locale non deve essere visto come sostituto del backup centrale, ma come spazio temporaneo di appoggio e continuità operativa.

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

Questa rete può essere sufficiente per un normale ufficio, ma **non è sufficiente per gestire più cantieri e grandi quantità di dati BIM**.

Si propone quindi di potenziare la rete in questo modo:

```
Internet fibra
      |
CPE / modem / ONT
      |
Firewall aziendale
      |
Switch core gestito
      |
--------------------------------
|              |               |
Server BIM     PC uffici       Wi-Fi aziendale
NAS/Backup     tecnici         Access point
```

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

L’ADSL è considerata datata perché ha capacità limitata, maggiore latenza e prestazioni spesso non adeguate al trasferimento di grandi quantità di dati. Inoltre è una tecnologia asimmetrica: l’upload è generalmente molto inferiore al download.

Nel caso dei cantieri è importante soprattutto l’upload dal cantiere verso la sede, perché scansioni, immagini e dati devono essere inviati dal cantiere. Nella sede centrale, invece, è importante avere una buona banda complessiva, in particolare in download per ricevere dati da più cantieri e in upload per backup cloud, sincronizzazioni e condivisione verso l’esterno.

## VLAN nella sede centrale

Anche nella sede centrale conviene dividere la rete:

```
VLAN 10 - Uffici tecnici
VLAN 20 - Server BIM
VLAN 30 - Amministrazione apparati
VLAN 40 - Terminazione VPN e traffico proveniente dai cantieri
VLAN 50 - Wi-Fi ospiti
```

Questa separazione migliora la sicurezza. Ad esempio, un dispositivo ospite non deve poter accedere direttamente ai server BIM.

Anche nella sede centrale, le VLAN devono essere accompagnate da regole di firewalling. Ad esempio, la VLAN ospiti deve poter accedere solo a Internet, mentre la VLAN dei server BIM deve essere raggiungibile solo dagli utenti autorizzati.

## 3. Canali di comunicazione tra cantieri e sede centrale

Il traffico tra cantieri e sede centrale è composto da dati diversi.

I dati dei sensori sono generalmente piccoli, ma devono essere inviati in modo affidabile.
Le immagini delle fotocamere timelapse sono più pesanti.
Le nuvole di punti generate dagli scanner 3D possono essere molto grandi.

Per questo motivo il collegamento tra cantiere e sede deve avere buona banda, soprattutto in upload dal cantiere verso la sede centrale.

Si può stimare in modo semplice:

```
sensori:
    tipicamente meno di 1 Mbps, salvo molti sensori o invii molto frequenti

fotocamere timelapse:
    alcuni Mbps, in base a risoluzione, compressione e frequenza degli scatti

scansioni 3D:
    traffico molto più pesante, da centinaia di MB fino a diversi GB per sessione
```

Per ogni cantiere si può prevedere:

* collegamento principale in fibra, se disponibile;
* in alternativa FWA o 5G;
* connessione di backup, ad esempio tramite SIM 4G/5G;
* VPN site-to-site verso la sede centrale.

FWA significa collegamento radio fisso. La VPN site-to-site è un tunnel cifrato permanente tra due reti, ad esempio tra il cantiere e la sede centrale.

Per la sede centrale si propone una connessione più potente, ad esempio fibra FTTH/FTTC business. Sarebbe opportuno avere almeno alcune centinaia di Mbps, perché la sede deve ricevere dati da più cantieri e deve garantire accesso stabile ai server BIM, ai backup e ai servizi aziendali.

Il trasferimento dei file più grandi può essere programmato in orari di minore utilizzo, ad esempio a fine giornata o di notte. Invece i dati dei sensori devono avere priorità maggiore perché possono riguardare la sicurezza.

Per gestire le priorità si può usare QoS. Il QoS permette di dare precedenza ad alcuni tipi di traffico rispetto ad altri.

## Apparati da adottare

Nel cantiere:

* router/firewall con supporto VPN;
* CPE, modem, ONT, apparato FWA o router 4G/5G, a seconda del tipo di collegamento disponibile;
* switch gestito;
* access point Wi-Fi;
* eventuale gateway per sensori;
* eventuale NAS locale;
* eventuale connessione 4G/5G di backup;
* UPS.

Nella sede centrale:

* CPE, modem o ONT per il collegamento principale;
* firewall aziendale;
* router verso Internet, se separato dal firewall;
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

Per l’accesso Wi-Fi si può usare WPA2/WPA3 Enterprise, che consente di autenticare gli utenti tramite credenziali personali.

Per il collegamento permanente tra cantiere e sede si usa una VPN site-to-site. Questa VPN è normalmente configurata tra apparati di rete e può usare certificati digitali, chiavi precondivise o altre credenziali tecniche.

Per l’accesso remoto dei singoli utenti, invece, si può usare una VPN utente. In questo caso la VPN deve richiedere:

* username personale;
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
   | VPN site-to-site
   |
Sede centrale
   |
Server / NAS BIM
   |
Backup cloud cifrato
```

Questa scelta è realistica perché unisce controllo locale e maggiore sicurezza in caso di guasto grave nella sede.

Il cloud non deve essere usato senza adeguate misure di protezione. I dati devono essere protetti con autenticazione forte, permessi corretti, cifratura e backup controllati.

## Quesito II - Sicurezza informatica e continuità trasmissiva

Oltre all’autenticazione, servono altre misure di sicurezza.

## Sicurezza nei cantieri

Nei cantieri si possono adottare:

* rete Wi-Fi protetta;
* VLAN separate;
* regole firewall tra le VLAN;
* firewall locale;
* password robuste;
* aggiornamento degli apparati;
* accesso agli apparati solo agli amministratori;
* cifratura delle comunicazioni;
* raccolta dei log.

Le VLAN sono utili perché separano tablet, sensori, fotocamere e apparati di gestione. In questo modo, se un dispositivo ha un problema, non compromette automaticamente tutta la rete.

La separazione tramite VLAN deve essere accompagnata da regole di firewalling. Ad esempio, le fotocamere devono poter inviare immagini al repository, ma non devono poter amministrare gli apparati di rete o accedere liberamente ai server.

## Sicurezza nella sede centrale

Nella sede centrale si devono usare:

* firewall;
* VPN;
* antivirus o soluzioni di protezione endpoint sui PC;
* backup;
* permessi differenziati;
* aggiornamenti periodici;
* monitoraggio;
* log centralizzati.

I server BIM devono essere accessibili solo agli utenti autorizzati. Non devono essere pubblicati direttamente su Internet.

## Sicurezza della comunicazione remota

La comunicazione tra cantiere e sede deve avvenire tramite VPN cifrata. Si possono usare tecnologie come IPsec o OpenVPN.

La VPN protegge i dati durante il passaggio su Internet. Se qualcuno intercettasse il traffico, non dovrebbe poter leggere i dati in chiaro, perché il contenuto viaggia cifrato.

## Continuità del collegamento

Per garantire continuità trasmissiva si possono usare:

* doppia connessione Internet nella sede centrale;
* collegamento di backup nei cantieri, ad esempio 5G;
* router con failover automatico;
* UPS per router, firewall, CPE, switch e access point;
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

Se si usa un filtro DNS, occorre considerare anche DNS over HTTPS e DNS over TLS, perché possono permettere ad alcuni dispositivi di aggirare il DNS scolastico.

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
* nuovi servizi AI;
* DNS cifrato o servizi non ancora classificati dal filtro.

Per questo la soluzione tecnica deve essere accompagnata da regole didattiche e organizzative:

* spiegare chiaramente quando l’uso dell’AI è vietato;
* controllare i laboratori durante le prove;
* valutare anche la spiegazione orale del codice;
* usare esercizi in cui lo studente deve dimostrare di capire quello che scrive;
* eventualmente disattivare Internet durante alcune verifiche pratiche, se compatibile con l’attività richiesta.

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
la regola di port forwarding inoltra il traffico al dispositivo interno 172.16.1.100;
il traffico viene inoltrato normalmente verso la porta SSH interna 22,
salvo diversa configurazione;
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
Router pubblico / firewall
200.1.1.1:25500
   |
   | port forwarding
   |
Host interno
172.16.1.100:22
```

Questa configurazione può servire per amministrare da remoto un server interno. Tuttavia deve essere usata con attenzione, perché espone un accesso SSH verso Internet.

Per renderla più sicura si dovrebbe:

* usare password robuste;
* meglio ancora usare chiavi SSH;
* permettere l’accesso solo da indirizzi IP autorizzati;
* registrare i log;
* aggiornare il sistema;
* disabilitare l’accesso dell’utente root, se presente;
* preferire una VPN quando possibile.

La soluzione più sicura sarebbe collegarsi prima alla VPN e poi accedere via SSH all’indirizzo interno.

## Conclusione generale

La soluzione proposta prevede una rete di cantiere semplice ma ordinata, con router/firewall, CPE, switch, access point, sensori, fotocamere e collegamento sicuro alla sede centrale.

La sede centrale deve essere potenziata perché la vecchia connessione ADSL e una rete non segmentata non sono adatte a gestire il nuovo sistema BIM.

Le comunicazioni tra cantieri e sede devono usare VPN, banda sufficiente e collegamenti di backup. Nei cantieri è importante soprattutto la banda in upload, perché i dati devono essere inviati verso la sede. Nella sede centrale serve invece una connessione stabile e più potente, capace di ricevere dati da più cantieri e di sostenere backup, sincronizzazioni e accessi degli utenti.

I dati più pesanti, come scansioni e immagini, possono essere trasferiti anche in modo programmato, mentre i dati dei sensori devono avere maggiore priorità.

Nel quesito scolastico, invece, non serve una soluzione aziendale complessa: è più corretto proporre firewall, filtro DNS, proxy, VLAN dei laboratori e blocchi programmati, sempre accompagnati da regole didattiche chiare.
