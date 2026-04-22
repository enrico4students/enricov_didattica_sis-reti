
ARCHITETTURA DI RIFERIMENTO DI UNA RETE AZIENDALE
Soluzione modello sintetica

1. Impostazione generale

Si propone una rete aziendale realistica, progettata secondo criteri di segmentazione, sicurezza, continuità operativa e scalabilità.

Vengono definite due possibili versioni:

* una architettura 2-layer, consigliata come soluzione standard
* una architettura 3-layer, da adottare in campus più estesi o complessi

In entrambi i casi la rete deve supportare:

* utenti cablati
* WiFi corporate
* WiFi guest
* servizi pubblici on-site
* servizi interni business-critical
* rete di management
* collegamento con sede secondaria a 600 metri in line-of-sight
* collegamento VPN site-to-site verso sede in altro continente
* accesso remoto consentito solo ai manager
* integrazione con servizi cloud/serverless
* sistemi IDS/IPS e NMS
* cluster big data interno di circa 10 nodi

2. Scelta dell’architettura

Come soluzione principale si adotta una architettura 2-layer composta da:

* layer di accesso
* collapsed core, che unisce core e distribution

Questa scelta è adatta perché offre:

* buona semplicità
* costi inferiori
* gestione più lineare
* realismo tecnico per una organizzazione medio-grande

La versione 3-layer viene mantenuta come variante evoluta, con:

* access layer
* distribution layer
* core layer

Essa è preferibile solo se il campus è più grande, distribuito su più edifici o destinato a crescere molto.

3. Segmentazione logica

La rete viene suddivisa in VLAN e sottoreti distinte per separare traffico, utenti e servizi.

Esempio di segmentazione:

* VLAN 10  uffici operativi
* VLAN 20  management utenti
* VLAN 30  WiFi corporate
* VLAN 40  WiFi guest
* VLAN 50  server business interni
* VLAN 60  DBMS e backend SAP
* VLAN 70  documentale riservato al management
* VLAN 80  MongoDB documentale ordinario con RBAC
* VLAN 90  big data client / ingest
* VLAN 91  big data data plane
* VLAN 100 big data management
* VLAN 110 management di rete
* VLAN 120 security, NMS, SIEM
* VLAN 130 DMZ
* VLAN 140 transito WAN / VPN
* VLAN 150 sede secondaria utenti
* VLAN 160 sede secondaria guest
* VLAN 170 sede secondaria management

Questa segmentazione permette di limitare i movimenti laterali, migliorare la sicurezza e semplificare il controllo dei flussi.

4. Perimetro e DMZ

Tra Internet e la rete interna viene posto un firewall NGFW in alta affidabilità.

Il firewall svolge funzioni di:

* filtraggio
* NAT
* terminazione VPN
* IDS/IPS inline
* logging e controllo dei flussi

I servizi pubblici on-site vengono collocati in DMZ. In particolare:

* reverse proxy / WAF
* web server pubblico
* interfaccia REST / SOAP pubblicata

La DMZ è separata dalla LAN interna. Internet può raggiungere solo i servizi pubblicati in DMZ. Non deve essere possibile raggiungere direttamente:

* DBMS interni
* SAP
* documentale riservato
* MongoDB interno
* rete di management
* sistemi NMS / SIEM
* cluster big data

5. Server interni

Nella rete interna vengono collocati:

* DBMS relazionale
* sistema SAP
* applicativo business custom
* server documentale altamente riservato, accessibile solo al management
* MongoDB per documentazione ordinaria con accesso regolato da RBAC
* sistemi di monitoraggio, logging e sicurezza
* cluster big data

I flussi tra DMZ e rete interna devono essere ammessi solo se strettamente necessari, ad esempio tra API pubblicate e backend applicativi.

6. WiFi corporate e guest

Si prevedono almeno due SSID distinti:

* WiFi corporate
* WiFi guest

Il WiFi corporate viene associato a una VLAN interna dedicata e autenticato preferibilmente con 802.1X / RADIUS.

Il WiFi guest viene isolato dalla rete aziendale e abilitato solo verso Internet.

In questo modo gli ospiti non possono accedere ai sistemi interni.

7. Collegamento con sede secondaria a 600 metri

Poiché la sede secondaria si trova a circa 600 metri ed è in line-of-sight, la soluzione più realistica è un ponte radio point-to-point.

Questo collegamento consente di connettere la sede secondaria senza posa di nuova fibra, mantenendo buone prestazioni.

Anche nella sede secondaria si mantiene segmentazione separata per:

* utenti
* guest
* management

8. Collegamento con sede in altro continente

La sede situata in altro continente viene collegata tramite VPN site-to-site IPsec terminata sul firewall.

Questo consente di:

* cifrare il traffico tra sedi
* controllare i prefissi instradati
* applicare regole di sicurezza
* centralizzare logging e audit

9. Accesso remoto

L’accesso remoto è consentito solo ai dipendenti di livello manageriale.

Implementazione:

* remote access VPN sul firewall
* autenticazione forte con MFA
* autorizzazione basata su gruppo directory
* accesso limitato alle sole risorse consentite

I dipendenti non manageriali non dispongono di accesso remoto generale.

10. Rete di management

La rete di management deve essere separata dalla rete utenti.

In essa vengono collocati gli indirizzi di gestione di:

* switch
* access point
* firewall
* controller
* hypervisor
* schede iLO / iDRAC / IPMI
* sensori di sicurezza
* eventuali UPS e storage

L’accesso deve essere permesso solo da postazioni amministrative dedicate o da jump host.

Questa scelta è importante perché:

* riduce la superficie di attacco
* protegge gli apparati di rete
* separa traffico utente e traffico amministrativo
* migliora audit e troubleshooting

11. IDS/IPS e NMS

L’architettura deve prevedere:

* IPS inline sul firewall per il traffico nord-sud
* sensori IDS per traffico est-ovest rilevante
* integrazione con NMS e piattaforma centralizzata di sicurezza

Il NMS raccoglie dati di disponibilità, performance e inventario.

La piattaforma di sicurezza raccoglie:

* eventi IDS/IPS
* log
* alert
* correlazioni di sicurezza

12. Big data interno

L’organizzazione esegue anche elaborazioni big data on-site tramite un cluster distribuito di circa 10 nodi.

Per supportare adeguatamente questi carichi si prevede:

* area dedicata del data center
* rete separata o blocco dedicato
* distinzione tra traffico client, traffico dati interno e management
* collegamenti ad alta capacità, preferibilmente superiori alla normale LAN office

Questo evita che il traffico massivo del cluster interferisca con il traffico quotidiano degli utenti.

13. Integrazione con cloud e serverless

L’organizzazione espone anche servizi pubblici nel cloud attraverso funzioni serverless.

Alcuni di questi servizi invocano funzioni o API presenti on-site.

Per questo motivo si adotta una architettura ibrida in cui:

* il cloud pubblica frontend e servizi serverless
* alcune funzioni chiamano API on-site selezionate
* l’accesso verso on-site avviene in modo controllato, autenticato e tracciato
* non viene esposta indiscriminatamente la rete interna

14. Conclusione

La soluzione più adatta come modello di riferimento è la versione 2-layer, perché unisce:

* realismo
* completezza
* semplicità espositiva

La versione 3-layer rappresenta la naturale evoluzione per campus più grandi.

In entrambe le varianti i punti essenziali sono:

* segmentazione in VLAN
* firewall perimetrale con DMZ
* server interni separati dai servizi pubblici
* WiFi corporate e guest distinti
* management network separata
* VPN site-to-site verso altra sede
* remote access solo per manager
* integrazione IDS/IPS e NMS
* supporto a cloud ibrido e big data interno

Versione molto breve, adatta come chiusura finale:

Si propone una architettura enterprise segmentata e sicura, basata su firewall NGFW, DMZ, VLAN separate per utenti e servizi, rete di management dedicata, accesso remoto riservato ai manager, collegamento radio PTP verso sede secondaria, VPN site-to-site verso sede estera, integrazione con servizi cloud/serverless e supporto a cluster big data interno. Come soluzione standard si preferisce il modello 2-layer per semplicità e realismo; il modello 3-layer viene adottato nei campus più estesi.

