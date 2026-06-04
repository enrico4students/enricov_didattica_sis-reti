## Soluzione prova Sistemi e Reti 2018 suppletiva

# **NB non ancora controllata!!!**  

## Prima parte

## Ipotesi iniziali

Il comprensorio è formato da tre capannoni distanti meno di 100 metri. Il primo contiene gli uffici di MyStart e la sala server. Gli altri due capannoni ospitano 8 start-up ciascuno, per un totale di 16 start-up.

Ogni start-up può avere:

```
8 PC cablati
1 stampante condivisa
16 dispositivi Wi-Fi
accesso ai server centralizzati nel primo capannone
```

Numero massimo stimato:

```
16 start-up × 8 PC = 128 PC cablati
16 stampanti = 16 stampanti
16 start-up × 16 dispositivi Wi-Fi = 256 dispositivi mobili
uffici MyStart = 5 PC + 1 stampante
server, apparati di rete, access point, sistemi di gestione
```

Totale massimo indicativo: circa 430 dispositivi.

## 1. Architettura dell’infrastruttura di rete

Si propone una rete gerarchica a tre livelli:

```
livello core/distribution nel primo capannone;
livello access nei tre capannoni;
server farm nel locale tecnico;
firewall perimetrale verso Internet;
separazione logica tramite VLAN.
```

Schema logico:

```
Internet
   |
Router ISP
   |
Firewall UTM / Next Generation Firewall
   |
Core switch L3 ridondato - Capannone 1
   |
   |--- VLAN MyStart uffici
   |--- VLAN server farm
   |--- VLAN management
   |--- VLAN Wi-Fi guest/aziendale
   |
   |--- fibra verso Capannone 2
   |       |
   |       |--- switch access startup 1-8
   |
   |--- fibra verso Capannone 3
           |
           |--- switch access startup 9-16
```

## Risorse hardware

Nel locale tecnico del primo capannone:

```
2 firewall in alta affidabilità;
2 core switch layer 3 ridondati;
server fisici per virtualizzazione;
storage NAS/SAN;
UPS;
sistema di backup;
rack, patch panel, cablaggio strutturato;
sistema di monitoraggio.
```

Nei capannoni 2 e 3:

```
switch access gestibili;
access point Wi-Fi aziendali;
armadi di piano/rack;
collegamenti in fibra ottica verso il capannone 1.
```

Per ogni start-up:

```
porte Ethernet dedicate;
VLAN dedicata;
stampante nella stessa VLAN;
access point o SSID associato alla VLAN della start-up.
```

## Risorse software

```
hypervisor per virtualizzazione, ad esempio Proxmox, VMware ESXi o Hyper-V;
server DHCP;
server DNS interno;
directory service, ad esempio Active Directory o LDAP;
sistema di autenticazione centralizzata;
firewall con NAT, VPN, IDS/IPS;
reverse proxy per pubblicare servizi web;
sistema di backup;
sistema di monitoraggio, ad esempio Zabbix o equivalente;
logging centralizzato.
```

## Piano di indirizzamento

Si usa una rete privata 10.10.0.0/16.

Esempio di piano IP:

```
VLAN 10 - MyStart uffici
rete: 10.10.10.0/24
gateway: 10.10.10.1

VLAN 20 - Server farm
rete: 10.10.20.0/24
gateway: 10.10.20.1

VLAN 30 - Management apparati
rete: 10.10.30.0/24
gateway: 10.10.30.1

VLAN 40 - Wi-Fi ospiti
rete: 10.10.40.0/24
gateway: 10.10.40.1

VLAN 101 - Start-up 1
rete: 10.10.101.0/24
gateway: 10.10.101.1

VLAN 102 - Start-up 2
rete: 10.10.102.0/24
gateway: 10.10.102.1

...

VLAN 116 - Start-up 16
rete: 10.10.116.0/24
gateway: 10.10.116.1
```

Ogni start-up riceve una subnet /24. È sovradimensionata rispetto ai circa 25 dispositivi previsti, ma semplifica gestione, isolamento, DHCP, firewalling e crescita futura.

Per ogni start-up:

```
gateway: 10.10.x.1
stampante: 10.10.x.10
PC cablati: DHCP 10.10.x.50 - 10.10.x.99
Wi-Fi: DHCP 10.10.x.100 - 10.10.x.199
indirizzi riservati: 10.10.x.2 - 10.10.x.49
```

## Collegamento Internet

Si propone una connessione business in fibra ottica simmetrica, ad esempio almeno 1 Gbps, con SLA garantito.

Caratteristiche richieste:

```
banda garantita;
indirizzi IP pubblici statici;
router professionale;
SLA con tempi di ripristino definiti;
possibilità di seconda linea di backup;
supporto a VPN;
monitoraggio della connettività.
```

Soluzione consigliata:

```
linea primaria in fibra FTTH/FTTO;
linea secondaria con operatore diverso;
failover automatico sul firewall;
bilanciamento o backup della connessione.
```

## Continuità del servizio

Per garantire continuità:

```
firewall in coppia HA;
core switch ridondati;
collegamenti in fibra ridondati, se economicamente possibile;
UPS per sala server e apparati principali;
server virtualizzati in cluster;
storage ridondato RAID;
backup periodici;
snapshot delle macchine virtuali;
replica dei dati;
monitoraggio proattivo;
contratti di assistenza.
```

Per i server delle start-up è opportuno usare virtualizzazione: ogni start-up può avere una o più VM isolate, con backup e snapshot.

## 2. Protezione tra start-up e sicurezza dei server

## Isolamento locale tra start-up

Il rischio principale è che una start-up possa accedere ai dispositivi o ai servizi di un’altra.

Le tecniche principali sono:

```
VLAN separate;
ACL sui router/switch layer 3;
firewall interno tra VLAN;
SSID Wi-Fi separati;
autenticazione WPA2/WPA3 Enterprise;
disabilitazione delle porte inutilizzate;
port security sugli switch;
separazione della rete guest;
logging degli accessi.
```

Ogni start-up deve vedere:

```
i propri PC;
la propria stampante;
i propri server o servizi autorizzati;
Internet.
```

Non deve vedere:

```
le reti delle altre start-up;
la rete di management;
gli apparati di rete;
i server non assegnati.
```

Esempio di regola logica:

```
VLAN 101 può accedere a Internet
VLAN 101 può accedere ai server assegnati
VLAN 101 non può accedere a VLAN 102-116
VLAN 101 non può accedere a VLAN 30 management
```

## Protezione dei server

I server nel locale tecnico devono essere protetti sia da attacchi esterni sia da accessi interni non autorizzati.

Soluzioni:

```
firewall perimetrale verso Internet;
DMZ per i servizi pubblici;
reverse proxy per HTTP/HTTPS;
pubblicazione solo delle porte necessarie;
VPN per amministrazione remota;
autenticazione forte;
aggiornamenti regolari;
antivirus/EDR sui server;
IDS/IPS;
backup;
logging centralizzato;
separazione delle VM delle diverse start-up;
hardening dei sistemi operativi;
principio del minimo privilegio.
```

I server pubblici non devono stare direttamente nella stessa rete degli uffici o delle start-up. Conviene usare una DMZ o una VLAN server dedicata con regole firewall molto restrittive.

## 3. Servizi di rete necessari

I principali servizi di rete sono:

```
DHCP;
DNS interno;
DNS forwarding verso Internet;
autenticazione centralizzata;
directory utenti;
NTP;
servizio VPN;
servizio di backup;
monitoraggio;
logging;
eventuale proxy web;
gestione certificati TLS.
```

## Esempio di configurazione DHCP

Si può usare un server DHCP centrale con scope separati per VLAN. Gli switch layer 3 o il firewall inoltrano le richieste DHCP tramite DHCP relay.

Esempio per la start-up 1:

```
subnet: 10.10.101.0/24
gateway: 10.10.101.1
DNS: 10.10.20.10
dominio interno: startup1.mystart.local
range DHCP PC: 10.10.101.50 - 10.10.101.99
range DHCP Wi-Fi: 10.10.101.100 - 10.10.101.199
stampante: 10.10.101.10, indirizzo statico o prenotazione DHCP
```

Esempio in stile ISC DHCP Server:

```
subnet 10.10.101.0 netmask 255.255.255.0 {
    range 10.10.101.50 10.10.101.199;
    option routers 10.10.101.1;
    option domain-name-servers 10.10.20.10;
    option domain-name "startup1.mystart.local";
    default-lease-time 3600;
    max-lease-time 86400;
}

host stampante_startup1 {
    hardware ethernet AA:BB:CC:DD:EE:01;
    fixed-address 10.10.101.10;
}
```

Per ogni VLAN si crea uno scope simile, cambiando rete, gateway e range.

## 4. Accesso remoto ai server

Sono richieste due possibili soluzioni.

## Soluzione 1: VPN

Ogni start-up accede da remoto tramite VPN.

Caratteristiche:

```
accesso cifrato;
autenticazione con username, password e secondo fattore;
profili separati per start-up;
accesso consentito solo ai server autorizzati;
logging delle connessioni.
```

Tecnologie possibili:

```
IPsec VPN;
SSL VPN;
WireGuard;
OpenVPN.
```

Vantaggio: soluzione sicura e adatta all’amministrazione tecnica.

## Soluzione 2: portale web di gestione / bastion host

Si può predisporre un server bastion o un portale di gestione accessibile via HTTPS.

Funzionamento:

```
l’utente si autentica sul portale;
il portale consente accesso a pannelli di controllo, SSH via browser, RDP gateway o strumenti di deploy;
il server bastion è l’unico punto autorizzato a collegarsi ai server interni.
```

Vantaggi:

```
controllo centralizzato;
logging completo;
minore esposizione dei server;
possibilità di limitare comandi e permessi.
```

È preferibile evitare l’esposizione diretta su Internet di SSH, RDP, database o pannelli amministrativi.

## Seconda parte - Quesito II

## Macchine virtuali sui server del locale tecnico

L’uso di macchine virtuali è particolarmente adatto a questo scenario, perché MyStart deve ospitare servizi diversi appartenenti a start-up diverse.

## Vantaggi

Il primo vantaggio è l’isolamento. Ogni start-up può avere una o più macchine virtuali separate dalle altre. In questo modo un problema su un server applicativo non coinvolge direttamente i servizi degli altri clienti.

Il secondo vantaggio è la flessibilità. Una start-up può richiedere Linux, un’altra Windows Server, una può usare PHP e MySQL, un’altra Node.js e PostgreSQL. Con la virtualizzazione è possibile offrire ambienti diversi sullo stesso hardware fisico.

Il terzo vantaggio è la gestione semplificata. Le VM possono essere create, clonate, spostate, sospese o eliminate rapidamente. Questo è utile in un incubatore di imprese, dove le esigenze possono cambiare spesso.

Il quarto vantaggio riguarda backup e ripristino. Le VM possono essere salvate tramite snapshot e backup centralizzati. In caso di errore o aggiornamento non riuscito è possibile tornare a uno stato precedente.

Il quinto vantaggio è la continuità del servizio. Se si usa un cluster di virtualizzazione, una VM può essere riavviata su un altro host in caso di guasto del server fisico.

## Svantaggi

Il primo svantaggio è la maggiore complessità tecnica. Servono competenze per gestire hypervisor, storage, rete virtuale, snapshot, backup e sicurezza.

Il secondo svantaggio è il rischio di concentrazione. Se molti servizi sono ospitati su pochi server fisici, un guasto importante può avere effetto su molte start-up. Per questo servono ridondanza e backup.

Il terzo svantaggio riguarda le prestazioni. Le VM condividono CPU, RAM, storage e rete. È necessario dimensionare correttamente l’hardware per evitare rallentamenti.

Il quarto svantaggio è la sicurezza. Un errore di configurazione della rete virtuale può permettere comunicazioni indesiderate tra ambienti diversi. Occorre quindi separare correttamente VLAN, firewall virtuali e permessi.

## Scelta consigliata

La soluzione consigliata è usare un cluster di virtualizzazione con almeno due host fisici, storage ridondato e backup esterno.

Ogni start-up dovrebbe avere:

```
una VLAN dedicata;
una o più VM dedicate;
regole firewall specifiche;
backup separato;
accesso amministrativo solo tramite VPN o bastion host.
```

Questa soluzione risponde bene alle esigenze di isolamento, flessibilità e continuità del servizio.

## Seconda parte - Quesito III

## Tracciamento degli accessi web e ottimizzazione della banda

In una rete locale può essere necessario controllare gli accessi ai siti web per motivi di sicurezza, diagnostica, rispetto delle policy aziendali e ottimizzazione della banda.

## Soluzioni tecniche

Una prima soluzione è l’uso di un proxy web. Il proxy riceve le richieste dei client e le inoltra verso Internet. Può registrare gli accessi, applicare filtri, bloccare categorie di siti e memorizzare in cache alcuni contenuti.

Una seconda soluzione è il firewall UTM o Next Generation Firewall. Questo dispositivo può controllare traffico HTTP/HTTPS, applicare regole per utente o gruppo, bloccare malware, filtrare contenuti e produrre log.

Una terza soluzione è il DNS filtering. In questo caso si controlla la risoluzione dei nomi di dominio, impedendo l’accesso a domini pericolosi o non consentiti.

Una quarta soluzione è il traffic shaping, cioè la gestione della banda. Alcuni servizi possono essere limitati, mentre altri possono avere priorità. Ad esempio si può dare priorità a videoconferenze, servizi aziendali e accesso ai server, limitando streaming non lavorativo o download pesanti.

## Cache e ottimizzazione

Il proxy può memorizzare localmente contenuti richiesti frequentemente. Questo riduce il consumo di banda e migliora i tempi di risposta. Tuttavia oggi l’efficacia della cache è minore rispetto al passato, perché molti siti usano HTTPS e contenuti dinamici.

L’ottimizzazione può quindi avvenire soprattutto tramite:

```
limitazione della banda per categoria;
priorità ai servizi essenziali;
blocco di traffico indesiderato;
monitoraggio dei consumi;
aggiornamenti centralizzati dei sistemi.
```

## Privacy

Il tracciamento degli accessi web è delicato perché può rivelare abitudini, interessi, attività personali e dati potenzialmente sensibili degli utenti.

Per essere corretto, il monitoraggio deve rispettare alcuni principi:

```
informare chiaramente gli utenti;
raccogliere solo i dati necessari;
limitare l’accesso ai log;
conservare i log per un tempo definito;
usare i log per finalità legittime;
evitare controlli sproporzionati;
distinguere sicurezza tecnica e controllo individuale.
```

In un contesto come MyStart, è importante distinguere le reti delle diverse start-up. MyStart può gestire la sicurezza dell’infrastruttura, ma non dovrebbe controllare in modo invasivo l’attività dei dipendenti delle singole start-up senza adeguata base contrattuale, informativa e regole chiare.

## Conclusione

La soluzione migliore per il comprensorio è una rete strutturata con cablaggio in fibra tra i capannoni, core switch nel primo capannone, VLAN separate per ogni start-up, firewall centrale, server virtualizzati, servizi DHCP/DNS centralizzati, VPN per l’accesso remoto e meccanismi di alta affidabilità.

I punti chiave sono:

```
separazione tra start-up;
protezione dei server;
continuità del servizio;
gestione centralizzata;
accesso remoto sicuro;
scalabilità futura.
