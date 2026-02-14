# firewall

1. Che cos’è un firewall
   Un firewall è un sistema di sicurezza che controlla e filtra il traffico di rete tra due o più zone con diverso livello di fiducia (per esempio Internet e LAN aziendale, oppure tra VLAN interne).
   Applica regole basate su indirizzi IP, porte, protocolli, stato della connessione e, nei firewall moderni, anche su applicazioni e identità utente.

2. È un dispositivo fisico o logico?  
   Il firewall è una funzione logica (motore di ispezione + policy), ma può essere implementato come:

* Appliance hardware dedicata (dispositivo fisico standalone).
* Firewall virtuale (VM su hypervisor).
* Firewall cloud (servizio gestito all’interno di una VPC/VNet).
* Firewall host-based (software installato su server o endpoint).

3. È un dispositivo pass-through?
   Dipende dall’architettura.

Modalità tipiche:

A) Modalità routed (Layer 3 – la più comune)
Il firewall opera come nodo Layer 3 con almeno due interfacce IP (es. WAN, LAN, DMZ).
Il traffico viene instradato attraverso di esso. In questo caso:

* Non è un semplice bridge trasparente.
* È un punto di transito obbligato.
* Ogni zona ha una subnet diversa.
* Il firewall è il default gateway della LAN.

Collegamento tipico (perimetro aziendale):

Internet
→ CPE dell’operatore (es. ONT GPON, modem VDSL, modem DOCSIS, o CPE Ethernet fornito dall’ISP)
→ Interfaccia WAN del firewall
→ Interfaccia LAN del firewall
→ Switch core o switch di distribuzione
→ VLAN e host interni

Il collegamento è normalmente point-to-point Ethernet tra:

* CPE dell’ISP e firewall (WAN)
* Firewall e switch core (LAN)

B) Modalità trasparente (Layer 2 – bridge / pass-through)
In questo caso il firewall funziona come bridge L2:

* Non modifica gli indirizzi IP.
* Non è gateway IP.
* È inserito “in linea” tra due dispositivi.
* Filtra il traffico pur restando trasparente a livello IP.

Collegamento tipico:

CPE dell’ISP
→ Firewall (bridge)
→ Switch core

Qui il firewall è effettivamente un dispositivo pass-through fisico inserito tra due apparati, senza cambiare topologia IP.

4. A quali dispositivi viene collegato direttamente?

Nel perimetro aziendale:

Lato WAN
Collegato direttamente a:

* ONT (Optical Network Terminal) in caso di fibra FTTH/GPON.
* Modem VDSL nel caso di collegamenti xDSL.
* Modem DOCSIS per collegamenti via cavo.
* CPE Ethernet fornito dall’operatore su linee dedicate (es. fibra punto-punto o MPLS).

Nota: il termine corretto è CPE (Customer Premises Equipment), non “router ISP”, anche se spesso il CPE integra funzioni di routing.

Lato LAN
Collegato direttamente a:

* Switch core Layer 3.
* Switch di distribuzione.
* In ambienti piccoli, direttamente a uno switch access.

In architetture con DMZ:

Firewall con almeno 3 interfacce:

* WAN (verso CPE ISP)
* LAN (verso rete interna)
* DMZ (verso switch o server esposti)

5. Tipologie principali di firewall

5.1 Packet filtering (stateless)
Filtra su IP/porta/protocollo senza mantenere stato di connessione.

5.2 Stateful firewall
Tiene traccia dello stato delle sessioni TCP/UDP. È il minimo standard in ambito aziendale.

5.3 Proxy / Application firewall
Intermedia la connessione a livello applicativo (termina e riapre la sessione).

5.4 NGFW (Next-Generation Firewall)
Include:

* Stateful inspection
* DPI (Deep Packet Inspection)
* IPS/IDS
* Controllo applicativo
* Filtro URL
* Ispezione TLS
* Integrazione con directory utenti

È oggi la tipologia più diffusa nel mondo aziendale.

5.5 UTM (Unified Threat Management)
Soluzione integrata con più funzioni di sicurezza in un’unica appliance.

5.6 WAF (Web Application Firewall)
Protegge applicazioni web HTTP/HTTPS.
Si posiziona davanti ai web server (in DMZ o in cloud).
Non sostituisce il firewall di rete.

6. Tipologie attualmente più diffuse in azienda (con esempi)

6.1 NGFW perimetrali enterprise

Fortinet FortiGate 100F
Pagina prodotto:
[https://www.fortinet.com/resources/data-sheets/fortigate-100f-series](https://www.fortinet.com/resources/data-sheets/fortigate-100f-series)

Palo Alto Networks PA-440 (serie PA-400)
Pagina prodotto:
[https://www.paloaltonetworks.com/resources/datasheets/pa-400-series](https://www.paloaltonetworks.com/resources/datasheets/pa-400-series)

Cisco Firepower 1010 (serie Firepower 1000)
Pagina prodotto:
[https://www.cisco.com/c/en/us/products/collateral/security/firepower-1000-series/datasheet-c78-742469.html](https://www.cisco.com/c/en/us/products/collateral/security/firepower-1000-series/datasheet-c78-742469.html)

6.2 NGFW / UTM per PMI e filiali

Sophos XGS Series (es. XGS 116)
Pagina prodotto:
[https://www.sophos.com/en-us/products/next-gen-firewall/xgs-smb-firewalls](https://www.sophos.com/en-us/products/next-gen-firewall/xgs-smb-firewalls)

WatchGuard Firebox T40
Pagina hardware ufficiale:
[https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html](https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html)

Check Point Quantum Spark 1600
Pagina prodotto:
[https://www.checkpoint.com/resources/datasheet-4532/datasheet-quantum-spark-16001800](https://www.checkpoint.com/resources/datasheet-4532/datasheet-quantum-spark-16001800)

6.3 Security gateway branch enterprise

Juniper SRX340
Overview ufficiale:
[https://www.juniper.net/documentation/us/en/hardware/srx340/topics/topic-map/srx340-overview.html](https://www.juniper.net/documentation/us/en/hardware/srx340/topics/topic-map/srx340-overview.html)

6.4 Firewall cloud gestito

Microsoft Azure Firewall
Pagina prodotto:
[https://azure.microsoft.com/it-it/products/azure-firewall](https://azure.microsoft.com/it-it/products/azure-firewall)

Overview tecnico Microsoft Learn:
[https://learn.microsoft.com/en-us/azure/firewall/overview](https://learn.microsoft.com/en-us/azure/firewall/overview)

7. Schema architetturale riassuntivo (caso aziendale tipico)

Internet
→ ONT / modem / CPE dell’operatore
→ Firewall (modalità routed, gateway LAN)
→ Switch core L3
→ VLAN interne (utenti, server, VoIP, WiFi, ecc.)

Eventuale DMZ:

Firewall
→ Interfaccia DMZ
→ Switch DMZ
→ Web server / mail server / reverse proxy

8. Sintesi concettuale finale

Il firewall non è semplicemente “un filtro”, ma un punto di controllo centrale che:

* Segmenta zone di sicurezza.
* Impone politiche di accesso.
* Registra e monitora traffico.
* Riduce superficie di attacco.

Nell’IT aziendale moderno il modello dominante è NGFW in modalità routed, collegato point-to-point al CPE dell’operatore lato WAN e allo switch core lato LAN, con eventuali interfacce dedicate per DMZ o segmentazione interna.


<hr/>
## Posizionamento del router


## Chiarificazone elementare

Il firewall è dietro il router
cioè nel percorso logico del traffico, il firewall è più interno rispetto al router edge.
Mettere il firewall prima del router non è corretto perché il firewall non può ricevere traffico da Internet senza un’interfaccia WAN con routing valido verso l’ISP.




Se router e firewall sono dispositivi separati (architettura enterprise classica):

Un pacchetto che arriva da Internet verso un PC della LAN attraversa:

1. Router edge
2. Firewall
3. Switch
4. PC


Il router riceve un pacchetto in arrivo dalla rete dell’ISP e lo inoltra verso il firewall.
Il firewall decide se permettere o bloccare il traffico.

---

Perché l’ordine è questo?

Il router ha il compito di:

* gestire il routing WAN (es. BGP, linee multiple)
* ricevere traffico dal provider
* instradare verso la rete interna

Il firewall ha il compito di:

* applicare policy di sicurezza
* fare NAT
* ispezionare il traffico
* proteggere la LAN


---

Caso diverso: firewall che integra anche il router

Internet
→ CPE ISP
→ Firewall (routing + sicurezza)
→ LAN

Qui il pacchetto attraversa solo il firewall (che svolge entrambe le funzioni).


Firewall e router sono lo stesso dispositivo fisico, ma internamente le funzioni sono logiche e sequenziali.
Un pacchetto che arriva da Internet verso un PC della LAN:
Arriva sull’interfaccia WAN del firewall  
Viene prima gestita la parte di routing (decisione di instradamento)  
Viene applicata la policy firewall (controllo di sicurezza)  
Viene inoltrato verso l’interfaccia LAN  

---

Conclusione netta:

Se router e firewall sono separati → il pacchetto passa prima dal router, poi dal firewall.

Se sono integrati si possono vedere affermazioni errate (ad esempio da chatGPT) tipo "il firewall è il primo apparato aziendale che lo riceve."
Se routing e firewall sono integrati, il dispositivo unico, chiamato firewall per semplicità, è il primo apparato aziendale che riceve il traffico; al suo interno la decisione di instradamento precede l’applicazione della policy di sicurezza quindi il routing anche in questo caso è prima del firewall


