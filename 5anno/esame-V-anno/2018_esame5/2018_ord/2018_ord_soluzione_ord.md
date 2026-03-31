
SOLUZIONE DELLA PRIMA PARTE

Impostazione generale

La scelta progettuale migliore non è mescolare i dispositivi IoT con la rete didattica solo perché usano gli stessi switch fisici. La traccia chiede infatti esplicitamente di usare la rete esistente ma mantenendo separazione logica tra rete didattica e rete del teleriscaldamento; inoltre chiede che il router sia configurato per gestire due reti logicamente separate e che venga impedito alla rete didattica di accedere ai sensori. 

Quindi la soluzione corretta non è una sola LAN “più grande”, ma una segmentazione logica, tipicamente con VLAN, SSID distinti, regole firewall e instradamento controllato. Dal punto di vista tecnico è anche la scelta più sensata, perché i dispositivi IoT hanno esigenze e rischi diversi dai PC didattici: sono numerosi, poco presidiati, spesso con software meno aggiornabile e non devono essere raggiungibili liberamente dagli utenti.

Si adottano quindi queste ipotesi aggiuntive, coerenti con la traccia:
rete didattica separata logicamente dalla rete IoT del riscaldamento; switch di piano sostituiti o configurati come switch gestiti 802.1Q; collegamenti tra switch configurati come trunk; access point connessi agli switch di piano; SSID dedicato ai dispositivi del teleriscaldamento; firewall capace di filtrare anche traffico tra VLAN interne; piccolo gateway/collector IoT locale per concentrare i dati e inoltrarli al server remoto in modo sicuro.

A) Schema della rete wireless e modifiche alla rete esistente

Logica della scelta

La traccia richiede almeno 6 access point per piano, quindi 24 AP totali. Non avrebbe senso collegare gli AP a una rete indistinta, perché il requisito di separazione logica verrebbe rispettato male o in modo fragile. La soluzione robusta consiste nel mantenere l’infrastruttura fisica esistente ma introdurre VLAN.

Architettura proposta

Si definiscono almeno tre VLAN:
VLAN 10 = rete didattica
VLAN 20 = rete IoT teleriscaldamento
VLAN 99 = rete di management degli AP e degli apparati di rete

La VLAN 99 non è strettamente obbligatoria dalla traccia, ma è una scelta professionale corretta: evita di amministrare AP e switch dalla rete utenti o dalla rete IoT.

Per ogni piano:
6 access point PoE collegati allo switch di piano
gli AP pubblicano almeno lo SSID “Riscaldamento-IoT”, associato alla VLAN 20
eventuali SSID didattici possono restare associati alla VLAN 10, se già presenti o previsti
tutti i termostati e tutti gli attuatori si associano solo allo SSID IoT
gli AP ricevono IP di management nella VLAN 99

Gli uplink tra gli switch di piano e lo switch del piano terra devono essere trunk 802.1Q, perché devono trasportare contemporaneamente più VLAN sullo stesso collegamento fisico. Se gli switch esistenti non sono gestibili, vanno sostituiti con switch managed.

Schema logico testuale

Internet
|
Router
|
Firewall
|
Core switch / switch piano terra
|--------- trunk ---------- switch piano 1 ---- 6 AP
|--------- trunk ---------- switch piano 2 ---- 6 AP
|--------- trunk ---------- switch piano 3 ---- 6 AP
|--------- trunk ---------- switch piano terra ---- 6 AP locali piano terra

Sulle tratte trunk transitano VLAN 10, VLAN 20 e VLAN 99.
Sulle porte verso i PC didattici si usa access VLAN 10.
Sulle porte verso gli AP si può usare trunk, perché l’AP deve gestire almeno la VLAN IoT e quella di management; se l’AP gestisce anche SSID didattici, ciò diventa ancora più opportuno.
Sulla porta verso il dispositivo di telecontrollo della caldaia si usa access VLAN 20.
Sulle porte verso i normali client didattici non deve transitare VLAN 20.

Modifiche necessarie alla rete esistente

La rete originaria della traccia mostra solo switch in cascata, firewall e router. Per soddisfare davvero i vincoli, occorre:
sostituire o riconfigurare gli switch con modelli managed 802.1Q;
configurare trunk tra i piani;
predisporre porte PoE o iniettori PoE per 24 AP;
configurare VLAN e, preferibilmente, una VLAN di management;
rendere il firewall consapevole delle diverse zone logiche o almeno delle subnet associate;
eventualmente inserire un wireless controller centralizzato oppure usare AP gestibili centralmente via software.

Questa scelta è preferibile a una rete fisicamente separata parallela perché riusa l’infrastruttura esistente, come richiesto dalla traccia, ma senza rinunciare alla sicurezza.

B) Piano di indirizzamento IP e configurazione del router

Logica della scelta

Il sistema di sensori e attuatori comprende:
4 piani
12 locali per piano
in ogni locale 1 termostato + 1 attuatore

Totale dispositivi IoT di campo = 4 × 12 × 2 = 96. 

A questi conviene aggiungere almeno:
1 dispositivo di telecontrollo della caldaia
1 gateway/collector IoT locale
24 AP, ma nella rete di management, non nella stessa rete dei sensori

Se si volesse separare per piano in sottoreti diverse, il progetto diventerebbe più complesso senza che la traccia lo richieda. La richiesta chiave è la separazione tra rete didattica e rete IoT, quindi si può usare una sola subnet per la rete IoT e una per la didattica. Questa scelta semplifica il routing, riduce errori e resta pienamente coerente.

Piano di indirizzamento proposto

Rete didattica:
VLAN 10
192.168.10.0/24
gateway 192.168.10.1

Rete IoT teleriscaldamento:
VLAN 20
192.168.20.0/25
gateway 192.168.20.1

Rete management apparati:
VLAN 99
192.168.99.0/27
gateway 192.168.99.1

Perché 192.168.20.0/25 per l’IoT?
Una /25 offre 126 indirizzi host utilizzabili, quindi è sufficiente per 96 dispositivi di campo più margine per caldaia, gateway, eventuali espansioni e qualche riserva.

Assegnazione ordinata nella rete IoT

Per evitare confusione nella gestione, gli indirizzi vengono assegnati per piano e per locale, pur restando nella stessa subnet.

Piano terra:
locali 1-12
termostati 192.168.20.10 - 192.168.20.21
attuatori 192.168.20.30 - 192.168.20.41

Piano 1:
termostati 192.168.20.50 - 192.168.20.61
attuatori 192.168.20.70 - 192.168.20.81

Piano 2:
termostati 192.168.20.90 - 192.168.20.101
attuatori 192.168.20.102 - 192.168.20.113

Piano 3:
termostati 192.168.20.114 - 192.168.20.125
attuatori alcuni indirizzi finali andrebbero oltre .125, quindi questa distribuzione così lineare non è ottimale.

Meglio allora usare una distribuzione realmente corretta fin dall’inizio:

Gateway VLAN 20: 192.168.20.1
Caldaia/controllore: 192.168.20.2
Gateway IoT locale: 192.168.20.3

Piano terra:
termostati 192.168.20.10 - 192.168.20.21
attuatori 192.168.20.22 - 192.168.20.33

Piano 1:
termostati 192.168.20.34 - 192.168.20.45
attuatori 192.168.20.46 - 192.168.20.57

Piano 2:
termostati 192.168.20.58 - 192.168.20.69
attuatori 192.168.20.70 - 192.168.20.81

Piano 3:
termostati 192.168.20.82 - 192.168.20.93
attuatori 192.168.20.94 - 192.168.20.105

Restano liberi 192.168.20.106 - 192.168.20.126 per espansioni, dispositivi speciali, riserva.

Subnet mask IoT:
255.255.255.128

Network address:
192.168.20.0

Broadcast:
192.168.20.127

Per la rete didattica si mantiene:
network 192.168.10.0
mask 255.255.255.0
broadcast 192.168.10.255

Per la rete management:
network 192.168.99.0
mask 255.255.255.224
broadcast 192.168.99.31

Configurazione del router

La traccia chiede che il router gestisca le due reti logicamente separate. 
La soluzione tipica è router-on-a-stick oppure firewall/L3 switch con interfacce VLAN. Dato che in topologia esiste già un firewall tra switch e router, la configurazione più pulita è:
lo switch invia le VLAN al firewall;
il firewall filtra;
il router gestisce l’uscita WAN verso Internet.
Se però si vuole aderire letteralmente alla richiesta sul router, si può attribuire al router anche le subinterfacce VLAN oppure farlo terminare sul firewall. La soluzione più ordinata è:

core switch trunk verso firewall
firewall con interfaccia inside trunkata o subinterfacce:
inside.10 = 192.168.10.254/24
inside.20 = 192.168.20.254/25
inside.99 = 192.168.99.30/27
firewall default route verso router
router LAN-side = 192.168.x.x lato firewall
router WAN-side verso ISP

Se invece si vuole porre il router come gateway delle VLAN:
G0/0.10 encapsulation dot1q 10 ip 192.168.10.1/24
G0/0.20 encapsulation dot1q 20 ip 192.168.20.1/25
G0/0.99 encapsulation dot1q 99 ip 192.168.99.1/27
G0/1 WAN verso firewall/router ISP

Questa seconda opzione è didatticamente semplice, ma in pratica la prima, con firewall come punto di separazione tra zone, è spesso migliore.

C) Connessione criptata verso il server remoto, configurazione firewall e possibile configurazione router

Logica della scelta

La traccia richiede una connessione criptata tramite Internet per inviare i dati al server remoto. 
La soluzione tecnicamente più corretta non è esporre direttamente tutti i sensori su Internet. Sarebbe una scelta debole sia sul piano della sicurezza sia su quello operativo. È molto meglio concentrare i dati in un gateway locale e poi instaurare un tunnel sicuro verso la sede remota.

Per questo si introduce un gateway/collector IoT locale nella VLAN 20. I sensori e gli attuatori dialogano internamente con esso; il gateway invia poi i dati al server remoto.

Scelta della tecnologia crittografica

La scelta più adatta è una VPN IPsec site-to-site tra l’istituto e l’ufficio scolastico regionale. I motivi sono:
protegge il traffico a livello IP;
nasconde il traffico dalla rete pubblica;
consente autenticazione reciproca tra i due gateway;
evita di far “vedere” i dispositivi IoT direttamente su Internet.

In alternativa si potrebbe usare TLS applicativo dal gateway verso il server remoto, per esempio HTTPS o MQTT over TLS. Anche questa sarebbe corretta, ma IPsec è più tipica quando la traccia parla di configurazione di router e firewall.

Architettura

Sensori/attuatori -> AP -> VLAN 20 -> Gateway IoT locale -> Firewall/Router -> Tunnel IPsec -> Server remoto regionale

Configurazione del firewall

Regole consigliate:
negare ogni connessione in ingresso da Internet verso la rete IoT interna;
consentire solo al gateway IoT locale di avviare il traffico verso il server remoto o verso la subnet remota del tunnel;
consentire i protocolli necessari alla VPN tra i due estremi, ad esempio IKE/ISAKMP UDP 500, NAT-T UDP 4500, ESP protocollo 50 se non si usa solo NAT-T;
consentire nel tunnel soltanto il traffico dal gateway IoT o, al massimo, dalla subnet IoT verso il server remoto autorizzato;
bloccare ogni altro traffico IoT verso Internet.

In forma logica:
deny any from Internet to VLAN20
permit VPN peer public IP <-> apparato locale VPN
permit src 192.168.20.3 dst server_remoto through tunnel
deny src VLAN20 dst Internet any
permit didattica to Internet per normali necessità
deny didattica to VLAN20

Configurazione possibile del router

Il router deve avere:
rotta di default verso ISP;
parametri della VPN IPsec;
eventuale crypto map o interfaccia tunnel;
rotta verso la rete remota nel tunnel.

Esempio logico:
rete remota regionale: 10.50.0.0/24
server remoto: 10.50.0.10

access-list traffico interessante:
permit ip host 192.168.20.3 host 10.50.0.10

IKE phase 1:
peer = IP pubblico sede regionale
autenticazione con PSK o, meglio, certificati
algoritmi = AES, SHA-2, DH adeguato

IPsec phase 2:
trasform-set AES-GCM oppure AES/SHA
perfect forward secrecy se disponibile

route:
ip route 10.50.0.0 255.255.255.0 tunnel/VPN next-hop

Perché questa soluzione è preferibile

Perché riduce la superficie d’attacco: Internet non vede i sensori ma solo il gateway o l’apparato VPN. Inoltre la cifratura non è delegata a decine di dispositivi IoT potenzialmente deboli, ma a un apparato più controllabile.

D) Infrastruttura per impedire alla rete didattica di accedere ai sensori

Logica della scelta

La sola separazione con indirizzi IP diversi non basta. Se esiste routing tra le reti, un host della rete didattica potrebbe comunque provare a raggiungere la rete IoT. Occorre quindi un controllo esplicito del traffico inter-VLAN.

Soluzione proposta

La soluzione corretta è composta da tre livelli:
separazione L2 con VLAN diverse;
separazione L3 con subnet diverse;
filtraggio L3/L4 sul firewall o su un apparato interno di segmentazione.

In pratica:
VLAN 10 didattica
VLAN 20 IoT
default policy: traffico dalla VLAN 10 alla VLAN 20 negato
eccezioni: solo la postazione amministrativa tecnica o il server di supervisione può accedere alla VLAN 20
nessun dispositivo IoT può iniziare connessioni verso la VLAN didattica
gli AP devono accettare i client IoT solo sullo SSID dedicato

Regole esempio:
deny ip 192.168.10.0/24 -> 192.168.20.0/25
deny ip 192.168.20.0/25 -> 192.168.10.0/24
permit host 192.168.10.50 -> 192.168.20.0/25 tcp/udp porte di gestione strettamente necessarie
permit host 192.168.20.3 -> rete remota regionale nel tunnel VPN

Nuovi apparati eventualmente inseribili

Se il firewall esistente non supporta bene il filtraggio tra VLAN interne, si può inserire:
un firewall a tre zone o multi-interfaccia;
oppure un firewall interno dedicato tra rete didattica e rete IoT;
oppure uno switch layer 3 con ACL, anche se la soluzione con firewall dedicato è più robusta.

La scelta migliore, in un compito di questo tipo, è dichiarare che il firewall viene configurato a zone:
zona DIDATTICA
zona IOT
zona MGMT
zona WAN

Tra DIDATTICA e IOT la politica di default è deny.
Tra MGMT e IOT la politica è permit solo per amministrazione.
Tra IOT e WAN la politica è deny, salvo VPN verso il server remoto.

Conclusione prima parte

La rete viene quindi riutilizzata fisicamente, ma la separazione richiesta dalla traccia viene realizzata logicamente con VLAN, subnet distinte, trunk 802.1Q, AP dedicati, policy firewall e tunnel IPsec. Questa è la scelta più coerente con tutti i punti A, B, C e D della consegna. 

SOLUZIONE DELLA SECONDA PARTE
Vengono risolti tutti e quattro i quesiti opzionali richiesti dall’utente, anche se la prova ministeriale ne richiedeva due. 

Quesito 1
Sito pubblico con dati di efficienza energetica: architettura sicura

Logica della scelta

Il punto critico è che il sito deve essere pubblico, ma i dati nascono da una rete interna IoT e occorre tutelare sia sicurezza sia riservatezza. Quindi non bisogna pubblicare direttamente il database della rete di controllo, né mettere i sensori o il server di raccolta direttamente esposti su Internet.

Architettura proposta

Internet
|
Router
|
Firewall
|---------------- DMZ ------------------ Web server / reverse proxy
|
|---------------- LAN interna ---------- Server raccolta dati / Gateway IoT
Database interno completo
Rete sensori VLAN 20

In DMZ si colloca il server web pubblico, o meglio ancora un reverse proxy web davanti al server applicativo. Nella LAN interna si mantiene il server di raccolta dati dai sensori. Dal server interno si esportano verso la DMZ solo dati aggregati, anonimizzati o comunque già filtrati per la pubblicazione.

Questa scelta è preferibile a un database unico pubblico/interno, perché un eventuale attacco al sito non comprometterebbe immediatamente la rete di controllo del riscaldamento.

Configurazione apparati

Sul firewall:
consentire da Internet alla DMZ solo HTTPS verso il server web pubblico;
negare accesso da Internet verso la LAN interna;
consentire dalla LAN interna alla DMZ solo il flusso necessario per aggiornare i dati pubblici, per esempio replica su porta SQL specifica, trasferimento file via SFTP o chiamata API autenticata;
negare traffico iniziato dalla DMZ verso la rete IoT interna, salvo eccezioni rigidissime;
consentire amministrazione del web server solo da rete management.

Sul server web in DMZ:
pubblicare solo pagine e API con dati aggregati;
disabilitare servizi non necessari;
usare certificato TLS valido;
tenere separate area web e dati grezzi.

Sul server interno:
ricevere i dati dal gateway IoT;
conservare il dataset completo;
produrre un dataset derivato destinato alla pubblicazione.

Scelta conclusiva

La chiave è questa: il sito pubblico sta in DMZ, il sistema di controllo e raccolta resta in LAN interna, la DMZ riceve solo dati già selezionati. In questo modo si soddisfano contemporaneamente disponibilità del sito e riservatezza dei dati sensibili.

Quesito 2
Socket client-server per trasmettere il testo dei termostati

Logica della scelta

Il messaggio è testuale, strutturato, delimitato da “inizio;” e “fine”. La soluzione più semplice e robusta è usare TCP, non UDP, perché il dato deve arrivare completo e ordinato. Un sensore apre una connessione al server, invia il blocco di testo, il server verifica il formato e risponde con ACK oppure NACK.

Pseudo-codice lato server

```
creare socket TCP
bind su IP_server, porta 5000
listen()

ciclo infinito:
    connessione = accept()
    buffer = ""
    mentre vero:
        dati = recv(connessione)
        se dati vuoto:
            interrompere
        buffer = buffer + dati
        se "fine" presente nel buffer:
            interrompere

    se formato_valido(buffer):
        estrarre:
            id sensore
            data
            ora
            temperatura
        salvare su database o file
        inviare "ACK"
    altrimenti:
        inviare "NACK"

    close(connessione)
```

Pseudo-codice lato client sensore

```
messaggio =
    "inizio;\n" +
    "sensore 20-01;\n" +
    "data 31-03-2026;\n" +
    "ora 10-30;\n" +
    "temperatura rilevata 21.7;\n" +
    "fine\n"

creare socket TCP
connect(IP_server, 5000)
send(messaggio)
risposta = recv()
se risposta == "ACK":
    considerare invio riuscito
altrimenti:
    memorizzare per ritrasmissione
close()
```

Funzione di validazione

```
formato_valido(buffer):
    verificare presenza di:
        riga "inizio;"
        riga "sensore ..."
        riga "data ..."
        riga "ora ..."
        riga "temperatura rilevata ..."
        riga finale "fine"
    verificare che la temperatura sia numerica
    verificare che data e ora siano plausibili
    restituire vero o falso
```

Osservazione tecnica

Se si volesse aumentare la sicurezza, questo socket TCP potrebbe essere protetto con TLS. Però la richiesta del quesito riguarda il socket di comunicazione, quindi la parte essenziale è mostrare la logica client-server affidabile, con connessione, invio, ricezione, validazione e conferma.

Quesito 3
DMZ e difesa contro IP Spoofing e IP Smurfing

Logica della scelta

La domanda chiede due cose:
una possibile architettura DMZ;
la configurazione per mitigare IP spoofing e IP smurfing. 

Architettura proposta

La struttura classica e corretta è un firewall a tre interfacce:
interfaccia WAN verso Internet
interfaccia DMZ verso server pubblici
interfaccia LAN verso rete interna aziendale

Schema logico

Internet
|
Firewall
|------ DMZ ------ Web server, Mail relay, DNS pubblico
|
|------ LAN ------ client interni, server interni, database

Questa architettura è migliore della semplice pubblicazione diretta da LAN perché isola i servizi esposti.

Difesa contro IP spoofing

Lo spoofing consiste nel falsificare l’indirizzo IP sorgente. Le contromisure principali sono:
ingress filtering sulla WAN: scartare pacchetti entranti da Internet con indirizzi sorgente impossibili o riservati, come RFC1918, loopback, link-local, multicast improprio, indirizzi interni aziendali;
egress filtering: permettere verso Internet solo pacchetti con sorgente appartenente realmente alla propria rete pubblica o ai propri blocchi leciti;
uRPF o controlli antispoof sulle interfacce, se supportati;
regole che scartano sulla WAN qualunque pacchetto che dichiari come sorgente la LAN o la DMZ aziendale.

Esempi logici di policy:
deny in on WAN src 10.0.0.0/8
deny in on WAN src 172.16.0.0/12
deny in on WAN src 192.168.0.0/16
deny in on WAN src subnet_DMZ
deny in on WAN src subnet_LAN
deny out on WAN src non appartenente agli indirizzi leciti aziendali

Difesa contro IP smurfing

Lo smurfing sfrutta richieste ICMP verso indirizzi broadcast, con sorgente falsificata, per amplificare il traffico contro una vittima. Le contromisure fondamentali sono:
non inoltrare directed broadcast sui router;
disabilitare risposte ICMP a broadcast sugli host e sui router;
bloccare pacchetti ICMP echo-request diretti a indirizzi broadcast;
limitare ICMP dove opportuno.

Quindi:
no ip directed-broadcast sulle interfacce router
deny icmp any -> subnet_broadcast
rate-limit ICMP
eventuale disattivazione risposta a ping broadcast sugli host

Conclusione

La protezione corretta non è una singola regola ma una combinazione di DMZ, filtering in ingresso e in uscita, antispoof per interfaccia e blocco dei directed broadcast. Questa è la risposta tecnicamente più completa.

Quesito 4
Inserimento di un server DHCP in una rete attualmente tutta statica

Logica della scelta

La rete attuale ha 2 server dati e 52 host con indirizzi statici; si vuole aggiungere un server DHCP per portatili di studenti e docenti, minimizzando i disservizi. 
La scelta corretta non è convertire di colpo tutta la rete a DHCP. Questo creerebbe rischio di conflitti e interruzioni. Occorre invece introdurre il servizio gradualmente, mantenendo statici server e host già configurati.

Soluzione hardware

Si può usare:
un server dedicato DHCP collegato alla LAN;
oppure uno dei server esistenti, se adeguato e affidabile;
oppure il firewall/router, se ha servizio DHCP robusto.

In un compito d’esame, la soluzione più chiara è un server DHCP dedicato o una VM dedicata, perché separa il ruolo DHCP da altri servizi.

Esempio di configurazione

Si supponga rete esistente 192.168.1.0/24.
Server dati statici:
192.168.1.10
192.168.1.11

Apparati di rete statici:
router/firewall 192.168.1.1
switch managed 192.168.1.2 - 192.168.1.5
stampanti e host statici già presenti in fascia 192.168.1.20 - 192.168.1.120

Pool DHCP da riservare ai portatili:
192.168.1.200 - 192.168.1.239

Subnet mask:
255.255.255.0

Gateway distribuito dal DHCP:
192.168.1.1

DNS distribuiti:
192.168.1.10 oppure DNS esterni, secondo architettura

Lease time:
breve o medio, per esempio 8 ore o 1 giorno, adatto a portatili che entrano ed escono

È fondamentale escludere dal pool tutti gli indirizzi già usati staticamente, altrimenti si generano conflitti IP.

Procedure per attivare il servizio con minimo disservizio

Prima fase: censimento
rilevare tutti gli IP statici già assegnati;
identificare gateway, server, stampanti, switch, eventuali AP;
scegliere una fascia DHCP completamente libera.

Seconda fase: preparazione
installare il server DHCP;
configurare scope, gateway, DNS, lease, esclusioni;
non attivare ancora il servizio in produzione oppure provarlo su rete isolata o su un solo client di test.

Terza fase: prevenzione errori
verificare che non esista già un altro DHCP attivo;
attivare, se possibile, DHCP snooping sugli switch per evitare server DHCP non autorizzati.

Quarta fase: avvio graduale
attivare il servizio DHCP;
configurare solo i portatili nuovi o mobili in “ottieni automaticamente un indirizzo IP”;
lasciare invariati i dispositivi statici già funzionanti.

Quinta fase: verifica
controllare assegnazione corretta di IP, mask, gateway, DNS;
verificare navigazione e accesso alle risorse interne;
monitorare eventuali conflitti.

Perché questa soluzione è la migliore

Perché soddisfa l’obiettivo della mobilità per portatili e riduce al minimo i cambiamenti sulla rete esistente. I server dati e gli apparati infrastrutturali restano statici, mentre solo i client mobili usano DHCP.

Conclusione generale

La logica complessiva della prova porta a una soluzione fondata su tre idee centrali: riuso dell’infrastruttura fisica esistente, separazione logica rigorosa tra rete didattica e rete IoT, controllo della sicurezza con VLAN, firewall e cifratura del traffico verso l’esterno. È importante osservare che la soluzione più debole sarebbe stata limitarsi a “mettere access point e indirizzi IP”; la traccia invece chiede chiaramente segmentazione, routing controllato, cifratura e protezione dell’accesso ai sensori. 

## Alcuni riferimenti

Prova caricata dall’utente:
Sistemi_e_Reti_2018_ord.pdf
[sandbox:/mnt/data/Sistemi_e_Reti_2018_ord.pdf](sandbox:/mnt/data/Sistemi_e_Reti_2018_ord.pdf)

Testo della traccia consultato nel file caricato:




Se serve, nel messaggio successivo si può trasformare questa soluzione in una versione “da compito scritto”, più compatta e direttamente copiabile come elaborato d’esame.
