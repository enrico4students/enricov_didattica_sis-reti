
1. Requisiti trasformati in vincoli di progetto

L’organizzazione deve prevedere:

* LAN cablata per utenti interni
* Wi-Fi dipendenti e Wi-Fi ospiti separati
* server interni SAP
* server interno di contabilità custom
* file server ad alta riservatezza
* DBMS relazionale locale
* database NoSQL documentale locale
* sede secondaria a 600 m in line-of-sight
* altra sede principale in altro continente con collegamento **site-to-site VPN**
* accesso remoto consentito solo ai dipendenti manageriali
* rete di gestione dedicata
* servizi web pubblicati su AWS
* backend interno FastAPI invocato dai servizi AWS

Sul lato AWS, una connessione **AWS Site-to-Site VPN** è un collegamento IPsec tra rete on-premises e VPC; AWS documenta inoltre l’uso di **due tunnel** per ridondanza. Per i servizi web pubblici, un **Application Load Balancer** è il punto di ingresso tipico e inoltra il traffico ai target group; il controllo del traffico verso il load balancer avviene anche tramite security group. ([docs.aws.amazon.com][2])

2. Principi architetturali comuni alle due soluzioni

Le due reference architectures condividono le stesse scelte di fondo.

La prima scelta è la **segmentazione per VLAN e subnet dedicate**. In un impianto professionale non conviene mescolare utenti, server, guest Wi-Fi, management e collegamenti inter-sede nella stessa rete logica. Occorre invece separare i domini di fiducia, applicare ACL o firewall policy fra le VLAN, centralizzare i log e limitare i movimenti laterali.

La seconda scelta è il **routing inter-VLAN sul firewall/NGFW oppure su una coppia firewall interna/perimetrale**, non sugli switch di accesso. Questo non perché uno switch L3 non sia capace di farlo, ma perché qui la priorità è il controllo di sicurezza: ispezione, policy, logging, IPS, VPN, controllo applicativo, MFA per gli accessi remoti e filtraggio fra reti con diverso livello di fiducia.

La terza scelta è la presenza di una **management network dedicata**, accessibile solo da postazioni amministrative o da un bastion/jump host. La rete di gestione non deve coincidere con la LAN utente.

La quarta scelta è la separazione netta fra:

* servizi interni
* servizi pubblicati in cloud
* servizi di backend interni invocati dal cloud

In particolare, i servizi web esposti su AWS non devono aprire accesso generalizzato verso la rete interna. Devono invece poter raggiungere solo il backend necessario, per esempio il server FastAPI, e solo sulle porte strettamente necessarie.

3. Modello logico comune: segmenti consigliati

Per entrambe le architetture usare una struttura di questo tipo.

* VLAN 10  Uffici operativi
* VLAN 20  Manager
* VLAN 30  Wi-Fi aziendale
* VLAN 40  Wi-Fi ospiti
* VLAN 50  Server applicativi interni
* VLAN 60  Database relazionali
* VLAN 70  Database NoSQL documentale
* VLAN 80  File server riservati
* VLAN 90  Voce/servizi opzionali o dispositivi speciali
* VLAN 100 Management di rete
* VLAN 110 DMZ locale eventuale
* VLAN 120 Collegamento sede secondaria
* VLAN 130 Servizi di sicurezza / bastion / jump host
* VLAN 140 VPN remote access pool
* VLAN 150 Infrastruttura Wi-Fi controller / RADIUS / NAC

Una possibile logica di indirizzamento privata, chiara per studenti, è usare 10.10.0.0/16 e dedicare una /24 per ogni VLAN. Non è un obbligo, ma è molto leggibile in una reference architecture.

4. Reference architecture a 2 layer

Questa è la soluzione più adatta quando il campus principale non è enorme, il numero di apparati è contenuto o medio, ma si vuole comunque un disegno realistico e professionale.

Schema logico sintetico:

Internet / ISP
|
CPE / ONT
|
Coppia Firewall/NGFW in HA
|
Core switch stack L2/L3-lite
|
+-------------------+-------------------+-------------------+
|                   |                   |                   |
Access switch A     Access switch B     Access switch C     Bridge radio PTP
|                   |                   |                   |
Uffici / AP         Server rack         Sale / AP           Sede secondaria 600 m LOS

Sul ramo server locale:

Core switch
|
Server farm / VLAN dedicate
|
SAP
Contabilità custom
File server riservato
DBMS relazionale
MongoDB o altro document DB
FastAPI backend interno

Sul ramo cloud:

Internet
|
AWS VPC
|
Application Load Balancer
|
Web/App tier pubblico
|
Site-to-Site VPN verso sede principale
|
Accesso selettivo al backend FastAPI interno

Questa architettura è detta “2 layer” perché tra accesso e nucleo non esiste un distribution layer dedicato. Gli switch di accesso risalgono direttamente al core. È una scelta molto realistica per una sede di dimensioni medie: meno apparati, meno costo, meno complessità operativa, meno STP e meno uplink da governare, ma senza rinunciare a VLAN, sicurezza, Wi-Fi multiprofilo, collegamenti tra sedi e cloud.

4.1. Ruolo dei componenti nella 2 layer

Il **core** è il punto centrale della LAN. Aggrega gli switch di accesso, il server rack e il collegamento radio verso la sede secondaria. Non dovrebbe ospitare logica superflua: il suo compito è fornire trasporto affidabile e ad alta capacità.

Gli **switch di accesso** collegano PC, stampanti, telefoni IP, access point e apparati locali. In una reference architecture professionale conviene prevedere switch managed PoE almeno dove sono presenti AP e telefoni.

Il **firewall/NGFW** resta l’elemento chiave. Qui terminano:

* traffico Internet
* eventuale inter-VLAN routing, se scelto in ottica security-first
* VPN site-to-site con la sede estera, salvo terminazione dedicata su concentratore
* VPN remote access per i soli manager
* pubblicazioni controllate
* ispezione e logging

4.2. Wi-Fi nella 2 layer

Occorre prevedere almeno due SSID:

* SSID Corporate per dipendenti
* SSID Guest per ospiti

Lo SSID Corporate va associato a VLAN aziendale, idealmente con autenticazione 802.1X/RADIUS o comunque autenticazione forte; lo SSID Guest va isolato in una VLAN autonoma con uscita verso Internet e blocco verso le reti interne. Questo è uno dei punti che più spesso distingue una rete “realistica” da una scolastica troppo semplificata.

4.3. Server interni nella 2 layer

I sistemi SAP e contabilità custom devono stare nella **server farm interna**, non nella DMZ pubblica. Lo stesso vale per file server riservati, DBMS e document database. Il file server con segreti aziendali richiede un trattamento più restrittivo: accesso solo da gruppi autorizzati, auditing, eventuale storage cifrato, accesso vietato da Wi-Fi guest e da client non gestiti.

Il server **FastAPI interno** va trattato come backend applicativo specializzato. Non deve essere esposto direttamente a Internet. Deve essere raggiungibile soltanto:

* dai servizi AWS autorizzati
* da eventuali frontend interni autorizzati
* da postazioni di amministrazione o pipeline di deployment autorizzate

FastAPI è un framework Python per servizi API; il suo uso come backend interno è coerente con un’architettura a microservizi o a servizi applicativi moderni. ([fastapi.tiangolo.com][1])

4.4. Sede secondaria a 600 m LOS nella 2 layer

Per una sede a **600 metri** con **line-of-sight** la soluzione professionale più naturale è un **ponte radio point-to-point**. Questo evita opere civili, riduce costi e consente di estendere connettività IP tra le due sedi in modo controllato. In una reference architecture didattica conviene però precisare che non si deve “allungare indiscriminatamente la LAN”: meglio trasportare solo le VLAN o i servizi realmente necessari, oppure terminare il collegamento su apparati L3/firewall locali e trattarlo come collegamento inter-sede piccolo.

Schema:

Core principale
|
Bridge radio PTP A  ))))))  600 m LOS  ((((((  Bridge radio PTP B
|
Firewall/switch sede secondaria
|
Utenti, AP, piccola server room locale se necessaria

La sede secondaria può essere collegata in due modi professionali:

* come estensione controllata di alcune VLAN
* come sede autonoma con routing L3 e policy locali

La seconda opzione è normalmente migliore sul piano della sicurezza e della scalabilità.

4.5. Sede in altro continente nella 2 layer

Questa sede va collegata con **VPN site-to-site IPsec**. Quando uno dei due estremi è in AWS, AWS documenta l’uso di Site-to-Site VPN con due tunnel per ridondanza; lo stesso principio di ridondanza è opportuno anche per la connessione verso la sede estera, se possibile con doppio uplink o doppio apparato. ([docs.aws.amazon.com][2])

4.6. Remote access solo per manager nella 2 layer

L’accesso remoto nominativo va consentito solo ai manager. In pratica:

* VPN remote access sul firewall/NGFW
* autenticazione forte con MFA
* autorizzazione legata a gruppi directory o identity provider
* assegnazione a pool/VLAN dedicata
* ACL che permettono solo le risorse necessarie

Questa scelta è importante: il requisito non è “alcuni utenti remoti”, ma “tutti e soli i manager”. Quindi non basta configurare la VPN: serve controllo identitario a livello di gruppi.

4.7. Pubblicazione servizi web su AWS nella 2 layer

La parte pubblica va messa su AWS, per esempio:

Internet
|
AWS WAF / Security controls
|
Application Load Balancer
|
Web/App instances o containers
|
Site-to-Site VPN / private connectivity
|
FastAPI interno on-premises

AWS documenta che l’Application Load Balancer è il punto di ingresso per i client e inoltra verso i target group, mentre i security group definiscono quali flussi possono raggiungerlo e quali flussi esso può instaurare verso i target. ([docs.aws.amazon.com][3])

Scelta professionale fondamentale: dal cloud verso l’on-premises non concedere accesso “di rete” alla LAN in generale. Consentire solo il traffico applicativo verso il server FastAPI interno, per esempio sulla sua porta HTTPS o sulla porta applicativa protetta, con allow-list, autenticazione reciproca se possibile, logging e segmentazione.

5. Reference architecture a 3 layer

Questa seconda reference architecture serve come modello per organizzazioni più grandi o per contesti dove si vuole mostrare una struttura campus classica e molto leggibile sul piano didattico.

Schema logico sintetico:

Internet / ISP
|
CPE / ONT
|
Coppia Firewall/NGFW in HA
|
Core layer
|
+-------------------------+-------------------------+
|                         |                         |
Distribution A            Distribution B            Server/Services distribution
|                         |                         |
Access blocks             Access blocks             Server farm, Wi-Fi infra, security zones

Qui il **distribution layer** svolge il ruolo che nella 2 layer non esiste: aggrega gli access switch di una zona, applica policy L3, ACL, routing locale o summarization, isola i fault domain e rende il campus più ordinato quando le dimensioni crescono.

5.1. Quando la 3 layer è preferibile

È preferibile quando ci sono:

* molti piani o edifici
* molti switch di accesso
* molte VLAN
* maggiore esigenza di fault isolation
* necessità di crescita più ordinata
* esigenze di manutenzione e segmentazione per blocchi

5.2. Struttura della 3 layer

Access layer:
collega endpoint, AP, telefoni, piccoli dispositivi IoT o industriali.

Distribution layer:
raccoglie gli switch di accesso per edificio o area; qui si possono applicare policy, ACL, QoS, routing tra blocchi, first-hop redundancy.

Core layer:
trasporto ad alta velocità e bassa latenza tra distribution, firewall, data center locale e servizi centrali.

In una reference architecture “security-first” si può comunque scegliere di non fare routing completo ovunque nel distribution e mantenere il firewall come punto centrale per i flussi più sensibili. È una scelta didatticamente molto utile: mostrare che una rete reale può essere L3-capable in più punti, ma le policy di sicurezza possono restare centralizzate.

5.3. Wi-Fi nella 3 layer

Gli AP si attestano sugli switch di accesso, ma la gestione può essere centralizzata tramite controller Wi-Fi o piattaforma cloud-managed. Gli SSID restano almeno due: corporate e guest. Il traffico guest deve essere separato fino al punto in cui viene consentita solo l’uscita Internet.

5.4. Server interni nella 3 layer

I server critici possono essere collocati su una server distribution dedicata oppure direttamente connessi a una coppia di switch di data center/aggregation interni. Le zone minime da distinguere restano:

* application zone: SAP, contabilità custom, FastAPI
* data zone: DBMS relazionale e document DB
* secure file zone: file server riservati
* management / admin zone
* eventuale local DMZ

Il file server riservato non va nello stesso segmento di una comune file share aziendale. Deve avere policy più restrittive.

5.5. Sede secondaria a 600 m LOS nella 3 layer

La presenza del distribution layer non cambia il principio. Il ponte radio PTP resta una soluzione ottima se esiste line-of-sight reale. La differenza è che si può attestare il link su un distribution dedicato o su una coppia di firewall/router locali e trattare la sede secondaria come “campus edge” separato.

5.6. Sede estera e AWS nella 3 layer

La sede estera si collega via site-to-site VPN verso il firewall principale o verso un concentratore dedicato. AWS può connettersi via Site-to-Site VPN verso la rete principale, oppure verso un segmento di frontiera dedicato. AWS documenta che una Site-to-Site VPN supporta due tunnel per ridondanza; questo si integra bene con un disegno di core e distribution ridondato. ([docs.aws.amazon.com][2])

6. Flussi essenziali da prevedere nelle due architetture

Questa parte è importante perché rende la reference architecture davvero “professionale”.

6.1. Flusso utenti interni verso SAP e contabilità

Consentire:
Uffici / Manager / Wi-Fi corporate -> SAP / Contabilità custom

Bloccare:
Guest Wi-Fi -> SAP / Contabilità
Sede secondaria -> accesso indiscriminato
VPN remota manager -> solo ciò che serve davvero

6.2. Flusso verso file server riservato

Consentire solo:
gruppi autorizzati interni
eventualmente manager remoti con VPN e policy dedicate

Bloccare:
guest
utenti standard non autorizzati
servizi pubblici cloud
accesso diretto dai database

6.3. Flusso verso DBMS e document DB

Regola professionale di base:
i database non sono “reti utenti”. Devono essere raggiunti solo dai server applicativi o da admin autorizzati.

Consentire:
SAP -> DBMS
Contabilità custom -> DBMS
FastAPI -> DBMS o document DB se necessario
admin -> DB solo da management/jump host

Bloccare:
utenti finali -> DB
guest -> DB
AWS web tier -> DB diretti, salvo caso strettamente necessario e molto controllato

6.4. Flusso AWS verso FastAPI interno

Consentire:
AWS application tier -> FastAPI interno su porta definita

Bloccare:
AWS -> reti utenti
AWS -> file server
AWS -> DB diretti, salvo eccezioni rigorosamente motivate

Questa è una delle regole più importanti dell’intera architettura.

7. Meccanismi di sicurezza minimi da includere

Una reference architecture professionale deve esplicitare almeno questi elementi.

* firewall/NGFW ridondato
* IDS/IPS o funzioni equivalenti del NGFW
* VPN IPsec site-to-site
* VPN remote access con MFA
* NAC o almeno controllo 802.1X dove possibile
* rete guest separata
* rete management separata
* logging centralizzato
* backup e monitoraggio
* jump host o bastion per amministrazione
* ACL tra VLAN
* minimo privilegio sui flussi applicativi
* hardening dei server
* protezione dei segreti applicativi e dei certificati

Per il lato AWS, usare almeno security groups stretti e front-end bilanciato; AWS documenta che i security group del load balancer devono consentire il traffico in ingresso richiesto e il traffico verso target e health checks. ([docs.aws.amazon.com][4])

8. Quale delle due far vedere agli studenti come “modello di base”

Per uno studente, la **2 layer** è il modello più semplice da ricordare e più vicino a molte realtà medio-piccole:

access -> core -> firewall -> Internet/cloud

È anche il modello più adatto per spiegare in modo ordinato:

* VLAN
* trunk
* AP con più SSID
* server farm
* VPN
* sede secondaria radio
* cloud AWS con backend interno

La **3 layer** va mostrata come evoluzione naturale della 2 layer quando la sede cresce. Serve per far capire perché il distribution layer non è “sempre obbligatorio”, ma diventa utile quando aumentano edifici, switch, VLAN e requisiti di scalabilità.

9. Sintesi finale pronta da usare come reminder

Versione molto compatta.

Reference architecture 2 layer:
gli switch di accesso collegano utenti, AP e dispositivi locali; tutti gli uplink convergono sul core; il firewall/NGFW protegge Internet, gestisce VPN, filtra i flussi tra reti e governa gli accessi remoti dei soli manager. La server farm interna ospita SAP, contabilità custom, file server riservato, DBMS, document DB e backend FastAPI. Il Wi-Fi corporate e guest usa SSID separati e VLAN separate. La sede secondaria a 600 m LOS usa ponte radio point-to-point. La sede in altro continente usa VPN site-to-site. I servizi web pubblici sono su AWS e raggiungono solo il backend FastAPI interno tramite collegamento controllato.

Reference architecture 3 layer:
gli switch di accesso servono endpoint e AP; gli switch di distribution aggregano per edificio o area, applicano policy e isolano i fault domain; il core fornisce trasporto ad alta capacità tra distribution, firewall e server farm. Tutti i servizi e i meccanismi di sicurezza della 2 layer restano presenti, ma distribuiti in modo più scalabile e ordinato.

10. Scelta consigliata

Per un elaborato didattico con taglio professionale conviene preparare entrambe, ma presentarle così:

* **2 layer** come architettura raccomandata per sede media
* **3 layer** come architettura di riferimento per sede grande o multi-edificio

In questo modo il reminder resta realistico e non trasmette l’idea sbagliata che la 3 layer sia “più professionale” in assoluto. Non è sempre così: spesso è solo più adatta a strutture più grandi.

## Alcuni riferimenti

FastAPI documentation. ([fastapi.tiangolo.com][1])

FastAPI tutorial. ([fastapi.tiangolo.com][5])

AWS Site-to-Site VPN. ([docs.aws.amazon.com][2])

How AWS Site-to-Site VPN works. ([docs.aws.amazon.com][6])

Tunnel options for AWS Site-to-Site VPN. ([docs.aws.amazon.com][7])

AWS Application Load Balancers. ([docs.aws.amazon.com][3])

Security groups for your Application Load Balancer. ([docs.aws.amazon.com][4])

Create an Application Load Balancer. ([docs.aws.amazon.com][8])

Nel messaggio successivo si può trasformare tutto questo in una versione operativa, già pronta come dispensa, con:

* diagramma testuale completo 2 layer
* diagramma testuale completo 3 layer
* piano VLAN/subnet
* tabella dei flussi consentiti e bloccati
* motivazioni tecniche sintetiche ma professionali

[1]: https://fastapi.tiangolo.com/?utm_source=chatgpt.com "FastAPI"
[2]: https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html?utm_source=chatgpt.com "AWS Site-to-Site VPN"
[3]: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html?utm_source=chatgpt.com "Application Load Balancers"
[4]: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html?utm_source=chatgpt.com "Security groups for your Application Load Balancer"
[5]: https://fastapi.tiangolo.com/tutorial/?utm_source=chatgpt.com "Tutorial - User Guide"
[6]: https://docs.aws.amazon.com/vpn/latest/s2svpn/how_it_works.html?utm_source=chatgpt.com "How AWS Site-to-Site VPN works"
[7]: https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html?utm_source=chatgpt.com "Tunnel options for your AWS Site-to-Site VPN connection"
[8]: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-application-load-balancer.html?utm_source=chatgpt.com "Create an Application Load Balancer - AWS Documentation"
