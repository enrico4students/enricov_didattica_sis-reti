# Firewall

## 1. Definizione e natura del firewall

Un firewall è un sistema di sicurezza che controlla e filtra il traffico di rete tra zone con diverso livello di fiducia.

Esempi tipici:

* Internet e rete aziendale;
* rete uffici e rete server;
* VLAN utenti e VLAN amministrazione;
* rete interna e DMZ.

Il firewall applica regole di sicurezza basate su:

* indirizzi IP;
* porte TCP/UDP;
* protocolli;
* stato delle connessioni;
* applicazioni;
* identità utente;
* contenuti del traffico nei firewall moderni.

Il firewall non è semplicemente “un dispositivo”.

È soprattutto una funzione logica composta da:

* motore di ispezione;
* policy di sicurezza;
* regole di filtraggio;
* meccanismi di logging e controllo.

Dal punto di vista pratico può essere implementato come:

* appliance hardware dedicata;
* firewall virtuale;
* firewall cloud;
* software installato direttamente su server o endpoint.

---

# 2. Ruolo architetturale del firewall

Nel modello aziendale moderno il firewall rappresenta il punto centrale di controllo del traffico.

Le sue funzioni principali includono:

* controllo accessi;
* segmentazione;
* protezione perimetrale;
* pubblicazione controllata di servizi;
* filtraggio del traffico;
* monitoraggio;
* VPN;
* NAT;
* ispezione avanzata del traffico.

Il firewall viene normalmente collocato:

* tra Internet e LAN;
* tra sedi collegate tramite VPN;
* tra VLAN interne;
* davanti alla DMZ;
* davanti a server pubblici;
* in ambienti cloud;
* tra reti con differenti livelli di sicurezza.

---

# 3. Architettura perimetrale aziendale

## 3.1 Il CPE (Customer Premises Equipment)

Il CPE è l’apparato di telecomunicazione installato presso la sede del cliente e collegato alla rete dell’operatore.

Rappresenta:

* l’ultimo dispositivo della rete ISP;
* il primo dispositivo visibile dal cliente;
* il punto di confine tra rete del provider e rete aziendale.

Può essere:

* ONT GPON;
* modem VDSL;
* modem DOCSIS;
* CPE Ethernet su linea dedicata;
* apparato MPLS;
* router fornito dall’ISP.

Il termine corretto generale è “CPE”, anche quando integra funzionalità di routing.

---

## 3.2 Architettura tipica

Schema molto comune:

Internet
→ CPE ISP
→ Firewall
→ Switch core/distribuzione
→ VLAN interne

Schema logico:

```text
                              INTERNET
                                  │
                                  ▼
        ┌───────────────────────────────────────────────┐
        │                    CPE ISP                    │
        │  ONT / Modem / CPE Ethernet                   │
        └───────────────────────────────────────────────┘
                                  │
                                  ▼
        ┌───────────────────────────────────────────────┐
        │                    FIREWALL                   │
        │  WAN | LAN | eventuale DMZ                    │
        │  Policy, NAT, VPN, IPS, ACL                   │
        └───────────────────────────────────────────────┘
                                  │
                                  ▼
        ┌───────────────────────────────────────────────┐
        │             SWITCH CORE / DISTRIBUZIONE       │
        │  trunk 802.1Q – porte access                  │
        └───────────────────────────────────────────────┘
                   │                │                │
                   ▼                ▼                ▼
                VLAN 10          VLAN 20          VLAN 30
                Uffici           Server           VoIP
```

Il firewall rappresenta quindi il punto di passaggio obbligato del traffico tra:

* WAN;
* LAN;
* reti interne;
* eventuale DMZ.

---

# 4. Modalità operative del firewall

## 4.1 Firewall routed (Layer 3)

È la modalità oggi più diffusa in ambito aziendale.

Il firewall opera come dispositivo Layer 3.

Caratteristiche:

* possiede interfacce IP;
* collega reti differenti;
* instrada traffico;
* è normalmente default gateway della LAN;
* applica policy durante l’inoltro dei pacchetti.

Ogni interfaccia appartiene normalmente a una subnet diversa:

* WAN;
* LAN;
* DMZ;
* VLAN interne.

Esempio:

* WAN: 203.0.113.2/30
* LAN: 10.10.0.1/24
* DMZ: 10.20.0.1/24

In questo modello il traffico attraversa il firewall a livello IP.

Il firewall:

* riceve il pacchetto;
* analizza il traffico;
* applica le policy;
* decide se inoltrarlo;
* esegue eventualmente NAT o ispezione avanzata.

---

## 4.2 Firewall transparent (bridge Layer 2)

In modalità transparent il firewall opera come bridge Ethernet.

Dal punto di vista topologico:

* è inserito a Layer 2;
* non è gateway IP;
* non modifica gli indirizzi IP;
* non richiede normalmente modifiche all’indirizzamento della rete.

Esempio:

CPE ISP
→ Firewall transparent
→ Switch core

In questo caso:

* il gateway IP resta il router a monte;
* il firewall è “invisibile” dal punto di vista IP;
* il traffico continua ad attraversarlo fisicamente.

---

## 4.3 Perché un firewall Layer 2 può analizzare IP e applicazioni

La modalità “transparent” descrive il modo in cui il firewall è inserito nella rete, non il livello massimo che può ispezionare.

Quando riceve un frame Ethernet il firewall:

1. legge l’header Ethernet;
2. esamina il payload;
3. estrae eventualmente il pacchetto IP;
4. analizza:

   * IP sorgente/destinazione;
   * protocollo;
   * porte TCP/UDP;
   * contenuto applicativo.

Nei NGFW può eseguire:

* DPI (Deep Packet Inspection);
* riconoscimento applicativo;
* controllo URL;
* IPS;
* ispezione TLS.

Quindi:

* il deployment è Layer 2;
* l’ispezione può arrivare fino a Layer 7.

Non è necessario effettuare routing per poter filtrare traffico IP.

Per filtrare basta:

* ricevere il traffico;
* analizzarlo;
* decidere se inoltrarlo o bloccarlo.

---

## 4.4 Vantaggi e uso del transparent firewall

La modalità transparent viene spesso usata quando:

* non si vuole modificare l’architettura IP esistente;
* si desidera inserire rapidamente un firewall;
* si vuole introdurre ispezione senza cambiare gateway;
* si aggiunge sicurezza in reti già operative.

È comune in:

* migrazioni;
* retrofit di sicurezza;
* data center;
* segmentazioni temporanee;
* ambienti industriali.

---

# 5. Stateful inspection

I firewall moderni sono normalmente stateful.

Questo significa che mantengono una tabella dello stato delle connessioni.

Esempio:

un client interno apre una connessione HTTPS verso Internet.

Il firewall registra:

* IP sorgente;
* IP destinazione;
* porte;
* stato della sessione;
* timeout;
* informazioni TCP.

Quando arrivano i pacchetti di risposta:

* il firewall verifica che appartengano a una connessione valida;
* permette automaticamente il traffico di ritorno.

Questo approccio è molto diverso da un semplice filtraggio stateless.

Un firewall stateless valuta ogni pacchetto in modo indipendente.

Uno stateful firewall comprende invece il contesto della comunicazione.

---

# 6. Tipologie principali di firewall

## 6.1 Packet filtering stateless

Filtra usando:

* IP;
* porte;
* protocolli.

Non mantiene stato delle connessioni.

È la forma più semplice e storicamente più antica.

---

## 6.2 Stateful firewall

Tiene traccia delle sessioni TCP/UDP.

È il minimo standard normalmente atteso in ambito aziendale.

---

## 6.3 Proxy firewall / application firewall

Il firewall termina direttamente la connessione applicativa.

Il client non comunica realmente con il server finale.

Il firewall:

* riceve la connessione;
* la analizza;
* apre una nuova connessione verso il server.

Questo approccio permette controlli applicativi molto dettagliati.

---

## 6.4 NGFW (Next-Generation Firewall)

È la categoria oggi più diffusa.

Un NGFW integra:

* stateful inspection;
* DPI;
* IPS/IDS;
* controllo applicativo;
* filtro URL;
* ispezione TLS;
* integrazione con directory utenti;
* controllo utenti/gruppi;
* analisi avanzata del traffico.

Molti NGFW possono riconoscere direttamente applicazioni come:

* YouTube;
* Teams;
* BitTorrent;
* SSH;
* VPN;
* servizi cloud.

Anche quando utilizzano le stesse porte TCP.

---

## 6.5 UTM (Unified Threat Management)

Una soluzione UTM integra molte funzioni di sicurezza in un singolo apparato.

Spesso include:

* firewall;
* antivirus;
* antispam;
* filtro web;
* VPN;
* IPS;
* controllo applicativo.

È molto comune nelle PMI.

---

## 6.6 WAF (Web Application Firewall)

Il WAF protegge applicazioni web HTTP/HTTPS.

Non sostituisce il firewall di rete.

Opera specificamente sul traffico web applicativo.

Può proteggere da:

* SQL injection;
* XSS;
* command injection;
* attacchi HTTP;
* richieste anomale;
* exploit applicativi.

Normalmente viene collocato:

* davanti ai web server;
* davanti a reverse proxy;
* in DMZ;
* in cloud.

Il firewall tradizionale protegge soprattutto rete e trasporto.

Il WAF protegge la logica applicativa web.

---

# 7. NAT e firewall

Molti firewall integrano funzionalità NAT.

Le più comuni sono:

* Source NAT;
* PAT;
* Destination NAT;
* Port forwarding.

Esempio tipico:

un server web interno nella DMZ deve essere pubblicato su Internet.

Il firewall:

* riceve traffico sulla WAN;
* modifica indirizzo e porta di destinazione;
* inoltra il traffico verso il server interno.

Il NAT non è il firewall stesso, ma è molto spesso integrato nel firewall perimetrale.

---

# 8. DMZ e firewall

La DMZ è una rete separata destinata a sistemi esposti verso Internet.

Tipici sistemi presenti in DMZ:

* web server;
* reverse proxy;
* mail gateway;
* VPN concentrator;
* sistemi pubblici.

La DMZ viene normalmente implementata usando il firewall come punto di separazione.

La logica fondamentale è:

* Internet non deve raggiungere direttamente la LAN interna;
* i server pubblici devono essere isolati;
* il traffico deve essere controllato tramite policy specifiche.

---

## 8.1 Firewall tri-homed

Un firewall tri-homed possiede almeno tre interfacce:

* WAN;
* LAN;
* DMZ.

Schema:

```text
                INTERNET
                    │
                    ▼
              ┌──────────┐
              │ FIREWALL │
              └──────────┘
               │    │
        LAN ───┘    └─── DMZ
```

Il firewall controlla:

* traffico WAN↔DMZ;
* traffico WAN↔LAN;
* traffico DMZ↔LAN.

Questo modello è molto diffuso perché:

* semplice;
* economico;
* facilmente gestibile.

---

## 8.2 DMZ back-to-back (dual firewall)

Architettura:

Internet
→ Firewall esterno
→ DMZ
→ Firewall interno
→ LAN

La DMZ viene separata da due dispositivi distinti.

Questo approccio aumenta:

* isolamento;
* separazione dei controlli;
* difesa in profondità.

È più comune in:

* grandi aziende;
* ambienti ad alta sicurezza;
* infrastrutture critiche;
* ambienti regolamentati.

---

## 8.3 DMZ tramite VLAN

In alcune architetture la DMZ viene implementata tramite VLAN separate sul firewall o sugli switch.

In questo caso:

* la separazione è logica;
* non necessariamente fisica.

È una soluzione comune perché:

* riduce costi;
* semplifica cablaggio;
* riduce numero di interfacce fisiche.

Ma l’isolamento fisico è inferiore rispetto a reti completamente separate.

---

# 9. Deployment del firewall

## 9.1 Firewall dedicato separato dal router

Architettura tipica enterprise:

Internet
→ Router/CPE
→ Firewall
→ LAN

Il router:

* gestisce connettività WAN;
* collegamenti ISP;
* BGP;
* linee multiple;
* routing operatore.

Il firewall:

* applica policy;
* protegge la LAN;
* esegue NAT;
* controlla il traffico;
* gestisce VPN e ispezione.

Questo modello offre:

* maggiore modularità;
* migliore separazione dei ruoli;
* maggiore scalabilità;
* sostituzione indipendente dei dispositivi.

È molto comune nelle medie e grandi aziende.

---

## 9.2 Firewall con routing integrato

In molte reti moderne il firewall integra direttamente le funzioni di routing.

Schema:

Internet
→ CPE ISP
→ Firewall
→ LAN

Il firewall:

* riceve traffico WAN;
* esegue routing;
* applica policy;
* inoltra verso LAN.

In questo caso:

* router edge e firewall coincidono;
* si riduce il numero di apparati;
* si semplifica la gestione.

È molto comune:

* nelle PMI;
* nelle filiali;
* negli uffici remoti;
* nelle reti di dimensioni moderate.

---

## 9.3 Firewall virtuali

Molti firewall possono essere deployati come macchine virtuali.

Esempi:

* VMware;
* Hyper-V;
* KVM;
* cloud public.

Vantaggi:

* flessibilità;
* rapidità di deployment;
* snapshot;
* integrazione cloud;
* scalabilità.

Sono molto usati:

* nei data center;
* in ambienti cloud;
* in laboratori;
* in reti virtualizzate.

---

## 9.4 Firewall cloud

Nei cloud provider il firewall può essere:

* servizio gestito;
* appliance virtuale;
* funzione distribuita.

Può proteggere:

* VPC;
* VNet;
* subnet cloud;
* workload virtuali.

Il concetto logico resta lo stesso:

* controllare il traffico tra zone differenti.

---

# 10. Alta affidabilità (HA)

In ambienti enterprise il firewall è spesso ridondato.

Configurazioni comuni:

* active/passive;
* active/active.

In caso di guasto:

* il firewall secondario prende il controllo;
* le sessioni possono essere sincronizzate;
* il downtime viene ridotto.

Questo è importante perché il firewall è spesso un punto centrale della rete.

Un suo guasto può interrompere:

* accesso Internet;
* VPN;
* comunicazioni inter-sede;
* accesso ai servizi.

---

# 11. Soluzioni diffuse in ambito aziendale

## 11.1 NGFW enterprise

### Fortinet FortiGate 100F

[https://www.fortinet.com/resources/data-sheets/fortigate-100f-series](https://www.fortinet.com/resources/data-sheets/fortigate-100f-series)

### Palo Alto Networks PA-440

[https://www.paloaltonetworks.com/resources/datasheets/pa-400-series](https://www.paloaltonetworks.com/resources/datasheets/pa-400-series)

### Cisco Firepower 1010

[https://www.cisco.com/c/en/us/products/collateral/security/firepower-1000-series/datasheet-c78-742469.html](https://www.cisco.com/c/en/us/products/collateral/security/firepower-1000-series/datasheet-c78-742469.html)

---

## 11.2 NGFW / UTM per PMI

### Sophos XGS Series

[https://www.sophos.com/en-us/products/next-gen-firewall/xgs-smb-firewalls](https://www.sophos.com/en-us/products/next-gen-firewall/xgs-smb-firewalls)

### WatchGuard Firebox T40

[https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html](https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html)

### Check Point Quantum Spark 1600

[https://www.checkpoint.com/resources/datasheet-4532/datasheet-quantum-spark-16001800](https://www.checkpoint.com/resources/datasheet-4532/datasheet-quantum-spark-16001800)

---

## 11.3 Security gateway branch enterprise

### Juniper SRX340

[https://www.juniper.net/documentation/us/en/hardware/srx340/topics/topic-map/srx340-overview.html](https://www.juniper.net/documentation/us/en/hardware/srx340/topics/topic-map/srx340-overview.html)

---

## 11.4 Firewall cloud

### Microsoft Azure Firewall

[https://azure.microsoft.com/it-it/products/azure-firewall](https://azure.microsoft.com/it-it/products/azure-firewall)

Overview tecnico:

[https://learn.microsoft.com/en-us/azure/firewall/overview](https://learn.microsoft.com/en-us/azure/firewall/overview)


---

# 12. Dispositivi che possono svolgere funzioni simili a un firewall

Alcuni dispositivi di rete non sono firewall veri e propri, ma possono implementare funzioni di filtraggio o controllo del traffico.

In genere offrono controlli meno approfonditi rispetto a un firewall dedicato o a un NGFW.

---

## 12.1 Router

I router possono applicare ACL (Access Control List) per:

* consentire o bloccare indirizzi IP;
* filtrare protocolli;
* filtrare porte TCP/UDP;
* limitare traffico tra reti.

Possono quindi svolgere un filtraggio basilare di sicurezza.

Tuttavia normalmente:

* non eseguono DPI avanzato;
* non analizzano applicazioni;
* non offrono IPS evoluto;
* non effettuano ispezione Layer 7 avanzata come un NGFW.

---

## 12.2 Switch Layer 3

Gli switch Layer 3 possono applicare ACL tra VLAN.

Esempio:

* bloccare traffico utenti → server;
* consentire solo specifici protocolli;
* limitare accesso a reti amministrative.

Sono molto veloci perché il filtraggio avviene direttamente nell’hardware dello switch.

Tuttavia il loro scopo principale resta:

* switching;
* routing interno.

Non sostituiscono normalmente un firewall completo.

---

## 12.3 Proxy server

Un proxy può controllare traffico applicativo specifico, ad esempio:

* HTTP;
* HTTPS;
* posta elettronica.

Può:

* filtrare URL;
* autenticare utenti;
* registrare traffico;
* applicare policy web.

Ma normalmente protegge solo specifici protocolli applicativi e non sostituisce un firewall generale di rete.

---

## 12.4 Access point Wi-Fi enterprise

Molti access point enterprise e controller wireless integrano funzioni di sicurezza:

* isolamento client;
* ACL wireless;
* captive portal;
* filtraggio traffico;
* controllo accessi utenti.

Tuttavia queste funzioni sono limitate principalmente all’ambiente Wi-Fi.

---

## 12.5 Host firewall

Sistemi operativi moderni includono firewall software locali.

Esempi:

* Windows Defender Firewall;
* nftables/iptables su Linux;
* pf su BSD;
* Application Firewall su macOS.

Proteggono il singolo host controllando:

* connessioni in ingresso;
* connessioni in uscita;
* porte;
* applicazioni.

Non sostituiscono però il firewall perimetrale aziendale.

---

## 12.6 IDS e IPS

Un IDS/IPS non è necessariamente un firewall.

Un IDS:

* rileva attività sospette;
* genera allarmi.

Un IPS:

* può bloccare traffico malevolo.

Molti NGFW integrano funzionalità IPS, ma concettualmente:

* firewall e IPS non sono la stessa cosa.

Il firewall controlla principalmente il traffico secondo policy di accesso.
L’IPS analizza il traffico per individuare attacchi o comportamenti anomali.



# 13. Conclusione

Nel modello aziendale moderno il firewall è uno dei componenti centrali della sicurezza di rete.

Può operare:

* come firewall perimetrale;
* come firewall interno;
* come firewall virtuale;
* come firewall cloud;
* come gateway VPN;
* come punto di segmentazione.

Oggi il firewall non si limita più a filtrare porte e indirizzi IP.

I NGFW moderni eseguono:

* analisi applicativa;
* DPI;
* controllo utenti;
* ispezione TLS;
* IPS;
* monitoraggio avanzato.

La funzione fondamentale resta comunque invariata:  
controllare il traffico tra reti con differente livello di fiducia applicando policy di sicurezza centralizzate.
