
# DISPOSITIVI DI RETE COMUNI IN UNA LAN AZIENDALE

In una rete aziendale moderna esistono molti tipi di apparati di rete, ma tre categorie svolgono il ruolo più importante per quanto riguarda la funzionalità ed una quarta è utile a fini pratici:

* **Switch** → distribuzione del traffico all’interno della LAN
* **Router / Edge Gateway** → collegamento tra la LAN e altre reti (Internet o WAN)
* **Firewall / NGFW** → protezione della rete e applicazione delle politiche di sicurezza
* **patch panel**  → gestione cavi  

Questi dispositivi svolgono funzioni diverse ma complementari e spesso sono installati nello stesso armadio di rete.

---

# SWITCH DI RETE (Layer 2 / Layer 3)

## Ruolo nella rete aziendale

Lo **switch** è il dispositivo **principale** della rete locale (LAN).
Il suo compito è collegare tra loro i dispositivi interni della rete:
* **altri switch**, computer, server, stampanti, telefoni VoIP, access point Wi-Fi

Lo switch opera normalmente al **livello 2 del modello OSI (Data Link)**, inoltrando i frame Ethernet in base agli **indirizzi MAC**.

Negli switch **Layer 3** sono presenti anche funzionalità di **routing IP**, spesso utilizzate per il **routing tra VLAN (inter-VLAN routing)**.

---

## Tipologie più comuni

### Switch unmanaged

Caratteristiche principali:

* nessuna configurazione
* nessun supporto VLAN
* nessun controllo QoS
* installazione plug-and-play

Utilizzati principalmente in:

* piccoli uffici
* reti temporanee
* espansioni molto semplici della rete

Opera principalmente a livello 2 del modello OSI, quindi inoltra i frame in base agli indirizzi MAC e non effettua routing IP tra VLAN diverse.

---

### Switch Layer 3

Oltre alle funzionalità di livello 2 offre anche:

* routing IP
* routing inter-VLAN
* ACL di base
* routing statico

Internamente usa delle **SVI (Switched Virtual Interface)**, cioè interfacce virtuali associate alle VLAN che funzionano come gateway IP delle relative subnet.  

![PlantUML 1](../imgs/dispositivi_img1_r61_dispositivi_1_r61_puml.jpg){ width=70% }


Le SVI vengono spesso rappresentate esternamente nei diagrammi, ma in realtà sono interne allo switch: sono interfacce logiche, non sono porte fisiche, sono configurazioni software associate alle VLAN e utilizzate come gateway IP delle subnet.
<br/><br/>

![PlantUML 2](../imgs/dispositivi_img2_r67_dispositivi_2_r108_puml.jpg){ width=70% }



Esempio didattico di switch che fa routing fra 3 VLAN


Lo switch Layer 3 effettua quindi **routing tra subnet appartenenti a VLAN diverse**, inoltrando i pacchetti tra le SVI tramite la propria tabella di routing, spesso con forwarding hardware ad alte prestazioni.

Nelle architetture aziendali viene spesso utilizzato come:

* **distribution switch**
* **core switch**

In ambito professionale il numero di porte **più diffuso è 48**, seguito da **24**.

Questo dipende soprattutto dalla progettazione degli **armadi di rete (rack)** negli edifici e dal fatto che si cerca di concentrare molti collegamenti su pochi apparati.

Una formulazione concisa e realistica può essere questa.

---

## Numero di porte e caratteristiche tipiche

###### Numero porte comuni:

* **48 porte** (più diffuso nelle reti aziendali)
* **24 porte** (molto comune in uffici e piani con meno postazioni)
* 16 porte
* 8 porte (più frequente in piccoli uffici o laboratori)

Gli switch a **48 porte** sono molto usati perché permettono di collegare molti dispositivi con un solo apparato rack e di ridurre il numero di switch necessari nell’armadio di rete.


###### Velocità più diffuse:

* **1 Gbps** → standard aziendale
* **2.5 Gbps** → sempre più diffuso negli access switch
* **10 Gbps** → spesso usato per uplink

###### Uplink tipici:

* SFP (1G)
* SFP+ (10G)
* nei modelli enterprise anche 25G  

_**SFP (Small Form-factor Pluggable)** è un modulo transceiver di rete **rimovibile** che si inserisce nelle porte degli switch o router per realizzare collegamenti in **fibra ottica o rame**, tipicamente fino a **1 Gbit/s**._



###### Supporto PoE:

* **PoE (802.3af)**
* **PoE+ (802.3at)**
* **PoE++** nei modelli più recenti


---

## Riepilogo funzionalità principali degli switch aziendali

* **VLAN 802.1Q** 
  Permette di segmentare la rete creando più reti logiche separate sulla stessa infrastruttura fisica.

* **QoS (Quality of Service)** 
  Consente di dare priorità a determinati tipi di traffico, ad esempio VoIP o video.

* **Link Aggregation (LACP)** 
  Permette di combinare più collegamenti fisici tra dispositivi in un unico collegamento logico più veloce e ridondante.

* **Spanning Tree (RSTP / MSTP)** 
  Previene i loop di rete disabilitando automaticamente collegamenti ridondanti non necessari.

* **Monitoring SNMP** 
  Permette di monitorare lo stato dello switch e delle porte tramite sistemi di gestione della rete.

* **ACL (Access Control List)** 
  Consente di applicare regole di filtraggio del traffico per controllare quali comunicazioni sono permesse.

* **Gestione locale o cloud** 
  Lo switch può essere configurato tramite interfaccia web, CLI oppure tramite piattaforme di gestione centralizzata.

Ecco la stessa sezione con **una breve frase esplicativa per ogni punto**, mantenendo la sintesi.

---

## Altre caratteristiche tecniche rilevanti

Quando si valutano switch professionali si considerano anche:

* **Switching capacity (Gbps)**
  Quantità massima di traffico che lo switch può gestire complessivamente su tutte le porte.

* **Forwarding rate**
  Numero massimo di pacchetti che lo switch può inoltrare al secondo senza degradare le prestazioni.

* **Budget PoE totale**
  Potenza elettrica complessiva disponibile per alimentare dispositivi PoE come access point, telefoni IP e telecamere.

* **Alimentazione ridondata**
  Possibilità di avere alimentatori duplicati per garantire il funzionamento anche in caso di guasto.

* **Stacking**
  Permette di collegare più switch in modo che funzionino come un unico apparato logico con gestione centralizzata.


---

## SWITCH: Modelli rappresentativi

Alcuni modelli rappresentativi di dispositivi organizzati per:
- ambito
  * enterprise
  * PMI / small business
  * familiare / SOHO
- ruolo architetturale
  * core
  * distribution
  * access

Quando una combinazione **non è significativa nella pratica** è stato indicato esplicitamente **N/A**.

---

### ENTERPRISE

#### Core switch

##### Cisco Catalyst 9500 Series  

Categoria: **enterprise**
Ruolo tipico: **core switch** nelle architetture campus aziendali

Pagina ufficiale produttore
[https://www.cisco.com/site/us/en/products/networking/switches/catalyst-9500-series-switches/index.html](https://www.cisco.com/site/us/en/products/networking/switches/catalyst-9500-series-switches/index.html)

Immagine online
[https://www.cisco.com/c/dam/en/us/products/collateral/switches/catalyst-9500-series-switches/nb-06-cat9500-series-switches.jpg](https://www.cisco.com/c/dam/en/us/products/collateral/switches/catalyst-9500-series-switches/nb-06-cat9500-series-switches.jpg)


![image_3](../imgs/dispositivi_img3_r207_cisco-catalyst_9500_ks17112-car9500-600x300.jpg){width=70%}


Caratteristiche principali:

* porte **10G / 25G / 40G / 100G**
* switching capacity molto elevata
* routing Layer 3 avanzato
* **Cisco IOS-XE**
* progettato per ruolo **core o aggregation**

---

#### Distribution switch

##### Cisco Catalyst 9300 Series  

Categoria: **enterprise**
Ruolo tipico: **distribution switch** oppure access avanzato

Pagina ufficiale produttore
[https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9300-series-switches/nb-06-cat9300-ser-data-sheet-cte-en.html](https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9300-series-switches/nb-06-cat9300-ser-data-sheet-cte-en.html)

Immagine online
[https://www.cisco.com/content/dam/en/us/products/collateral/switches/catalyst-9300-series-switches/images/ks14049-car9500-600x300.png](https://www.cisco.com/content/dam/en/us/products/collateral/switches/catalyst-9300-series-switches/images/ks14049-car9500-600x300.png)

![image_4](../imgs/dispositivi_img4_r233_cisco_catalyst-9300ks14049-car9500-600x300.jpg){width=70%}


Caratteristiche:

* 24 o 48 porte 1G / 2.5G
* uplink **10G / 25G**
* supporto **stacking**
* routing Layer 3 completo
* ampia diffusione nelle reti campus

---

#### Access switch

##### Cisco Catalyst 9200 Series

Categoria: **switch enterprise (rete aziendale)**
Ruolo tipico: **access switch**

Pagina ufficiale produttore
[https://www.cisco.com/site/us/en/products/networking/switches/catalyst-9200-series-switches/index.html](https://www.cisco.com/site/us/en/products/networking/switches/catalyst-9200-series-switches/index.html)


![image_5](../imgs/dispositivi_img5_r257_nb-06-cat9200-ser-data-sheet-cte-en_0.jpg){width=60%}

Caratteristiche principali:

* 24 o 48 porte 1G
* versioni PoE+
* uplink modulari 1G / 10G / 25G
* sistema operativo **Cisco IOS-XE**
* stacking

---

### PMI / SMALL BUSINESS

#### Core switch

**N/A**

Nelle reti PMI il ruolo di core spesso **non esiste come apparato separato**.
Uno switch di distribution o access svolge anche funzione di core.

---

#### Distribution switch

##### Zyxel XGS1935 Series (esempio XGS1935-28HP)

Categoria: **PMI / small business**
Ruolo tipico: **distribution switch leggero** oppure access avanzato

Pagina ufficiale produttore
[https://www.zyxel.com/global/en/products/switch/24-48-port-gbe-lite-l3-smart-managed-switch-with-4-10g-uplink-xgs1935-series](https://www.zyxel.com/global/en/products/switch/24-48-port-gbe-lite-l3-smart-managed-switch-with-4-10g-uplink-xgs1935-series)

Immagine online
[https://www.zyxel.com/sites/zyxel/files/library/assets/products/xgs1935-series/img_xgs1935-28hp_p_600x600.jpg](https://www.zyxel.com/sites/zyxel/files/library/assets/products/xgs1935-series/img_xgs1935-28hp_p_600x600.jpg)

![image_6](../imgs/dispositivi_img6_r293_img_xgs1935-28hp_p_600x600.jpg){width=70%}


Caratteristiche:

* 24 o 48 porte 1G
* uplink **10G**
* versioni PoE
* gestione **smart L3 lite**
* VLAN e QoS avanzate

---

#### Access switch

##### TP-Link Omada SG3218XP-M2

Categoria: **PMI / small business**
Ruolo tipico: **access switch**

Pagina ufficiale produttore
[https://www.omadanetworks.com/it/business-networking/omada-switch-access-pro/sg3218xp-m2/](https://www.omadanetworks.com/it/business-networking/omada-switch-access-pro/sg3218xp-m2/)

Immagine online
[https://static.tp-link.com/upload/image-line/TL-SG3218XP-M2_UN_1.0_overview_02_normal_20250126032358m.jpg](https://static.tp-link.com/upload/image-line/TL-SG3218XP-M2_UN_1.0_overview_02_normal_20250126032358m.jpg)


![image_7](../imgs/dispositivi_img7_r320_TL-SG3218XP-M2_UN_1.0_overview_02_normal_20250126032358m.jpg){width=70%}



Caratteristiche:

* 16 porte **2.5G**
* 8 porte **PoE+**
* 2 uplink **SFP+ 10G**
* gestione cloud Omada
* switch **L2+ con routing statico**

---

### FAMILIARE / SOHO

#### Core switch

**N/A**

Le reti domestiche **non hanno architettura gerarchica core/distribution/access**.  


#### Distribution switch

**N/A**
Le reti domestiche **non hanno architettura gerarchica core/distribution/access**.

---

#### Access switch

##### Netgear GS108   

Categoria: **familiare / SOHO**
Ruolo tipico: **access switch**

Pagina ufficiale produttore
[https://www.netgear.com/business/wired/switches/unmanaged/gs108/](https://www.netgear.com/business/wired/switches/unmanaged/gs108/)

Immagine online
[https://www.netgear.com/media/GS108v4_tcm148-73992.png](https://www.netgear.com/media/GS108v4_tcm148-73992.png)


![image_8](../imgs/dispositivi_img8_r364_B3_gs108_32.jpg){width=70%}



Caratteristiche:

* 8 porte Gigabit
* switch **unmanaged**
* nessuna configurazione
* plug-and-play
* molto diffuso in reti domestiche o piccoli uffici


---

# ROUTER AZIENDALI / EDGE GATEWAY

## Ruolo nella rete

Il **router aziendale** (o **edge gateway**) collega la rete locale aziendale con:

* Internet
* reti WAN
* reti di sedi remote (VPN site-to-site)

Il suo ruolo principale è quindi gestire il **traffico tra la rete interna e reti esterne**.

Svolge spesso anche funzioni di:

* **NAT** (traduzione degli indirizzi privati della LAN verso Internet)
* **VPN** (connessioni sicure verso sedi remote o utenti remoti)
* **firewall di base**
* gestione del traffico WAN

notare che nelle architetture aziendali moderne il router di edge  
**non gestisce normalmente il routing tra le reti interne della LAN**.  

Il routing tra VLAN e subnet interne è generalmente svolto da:

* **switch Layer 3** (distribution o core switch)
* oppure **firewall interni**

In altre parole:

* il router collega **la rete aziendale al resto del mondo**
* gli switch Layer 3 o firewall collegano **le reti interne tra loro**

---

## Tipologie più comuni

* router **multi-WAN**  
  permettono di collegare più connessioni Internet o WAN.

* router con **SD-WAN**  
  ottimizzano automaticamente il traffico tra più collegamenti WAN.   
  _(**SD-WAN Software-Defined Wide Area Network** è una tecnologia che gestisce e ottimizza via software il traffico tra più collegamenti WAN (Internet, MPLS, LTE ecc.), instradando dinamicamente i dati sul percorso più efficiente e affidabile.)_  

* router **VPN hardware**  
  progettati per gestire molte connessioni VPN cifrate.

* router con **controller centralizzato**  
  gestiti da piattaforme di orchestrazione o cloud.

---

## Porte tipiche

* 1 o più porte **WAN**
* porte **LAN**
* talvolta **porte SFP**  
  _(**SFP Small Form-factor Pluggable** è uno slot modulare che permette di inserire un transceiver rimovibile per realizzare collegamenti di rete in **fibra ottica o rame**, tipicamente fino a **1 Gbit/s**.)_  


Nei router **PMI o edge router compatti** è comune trovare:

* 4–8 porte LAN integrate

Nei router **enterprise di fascia alta** spesso invece:

* le porte LAN sono poche
* oppure sono presenti **slot modulari**
* oppure il router si collega direttamente a **switch di rete**.

---

## Funzionalità principali

* **NAT**
* VPN **IPsec / SSL**
* **firewall stateful**
* **load balancing WAN**
* **failover automatico**
* supporto **VLAN**

Va però osservato che nelle reti aziendali medio-grandi il filtraggio avanzato del traffico è spesso affidato a **firewall dedicati (NGFW)**, mentre il router svolge principalmente funzioni di **routing e connettività WAN**.

---


## ROUTER AZIENDALI / EDGE GATEWAY: Modelli rappresentativi

---

### ENTERPRISE

#### Core router

##### Cisco ASR 1000 Series  

Categoria: **enterprise / carrier grade**
Ruolo tipico: **core router o WAN edge router**

Pagina ufficiale produttore
[https://www.cisco.com/c/en/us/products/routers/asr-1000-series-aggregation-services-routers/index.html](https://www.cisco.com/c/en/us/products/routers/asr-1000-series-aggregation-services-routers/index.html)

Immagine online
[https://www.cisco.com/c/dam/en/us/products/collateral/routers/asr-1000-series-aggregation-services-routers/datasheet-c78-731632.docx/_jcr_content/renditions/datasheet-c78-731632_0.png](https://www.cisco.com/c/dam/en/us/products/collateral/routers/asr-1000-series-aggregation-services-routers/datasheet-c78-731632.docx/_jcr_content/renditions/datasheet-c78-731632_0.png)


![image_9](../imgs/dispositivi_img9_r484_cisco_asr-1000_datasheet-c78-731632_0.jpg){width=70%} 

Caratteristiche:

* routing ad alte prestazioni
* supporto **BGP / MPLS**
* throughput multi-gigabit
* architettura modulare
* utilizzato in **data center e backbone aziendali**

---

#### Distribution router

**N/A**

Nelle architetture moderne il routing di distribuzione è quasi sempre svolto da **switch Layer 3**.

---

#### Edge router

##### MikroTik RB5009UG+S+IN

Categoria: **PMI / professionale**
Ruolo tipico: **edge router**

Pagina ufficiale produttore
[https://mikrotik.com/product/rb5009ug_s_in](https://mikrotik.com/product/rb5009ug_s_in)

Immagine online
[https://i.mt.lv/cdn/product_files/RB5009UGS-IN_220903.png](https://i.mt.lv/cdn/product_files/RB5009UGS-IN_220903.png)


![image_10](../imgs/dispositivi_img10_r518_2065_lg.jpg){width=70%}



Caratteristiche:

* router ad alte prestazioni
* porta **10G SFP+**
* porte gigabit multiple
* sistema operativo **RouterOS**
* VPN e routing avanzato

---

### PMI / SMALL BUSINESS

#### Edge router

##### TP-Link Omada ER8411

Categoria: **PMI / small enterprise**
Ruolo tipico: **edge router / WAN gateway**

Pagina ufficiale produttore
[https://www.omadanetworks.com/it/business-networking/omada-router-wired-router/er8411/](https://www.omadanetworks.com/it/business-networking/omada-router-wired-router/er8411/)

Immagine online
[https://static.tp-link.com/upload/image-line/ER8411_UN_1.0_overview_01_normal_20220617022403i.jpg](https://static.tp-link.com/upload/image-line/ER8411_UN_1.0_overview_01_normal_20220617022403i.jpg)


![image_11](../imgs/dispositivi_img11_r548_ER8411_UN_1.0_overview_01_normal_20220617022403i.jpg){width=70%}


Caratteristiche:

* porte **10G**
* multi-WAN
* VPN hardware
* firewall integrato
* gestione cloud Omada

---

## FAMILIARE / SOHO

#### Edge router

##### AVM FRITZ!Box 7530   

Categoria: **familiare / SOHO**
Ruolo tipico: **router domestico**

Pagina ufficiale produttore
[https://fritz.com/en-it/products/fritz-box-7530-ax-20002944](https://fritz.com/en-it/products/fritz-box-7530-ax-20002944)

Immagine online
[https://fritz.com/cdn/shop/files/fritzbox_7530_ax_dsl_2000x2000px.jpg?v=1773999787&width=1000](https://fritz.com/cdn/shop/files/fritzbox_7530_ax_dsl_2000x2000px.webp?v=1773999787&width=1000)

![image_12](../imgs/dispositivi_img12_r576_fritzbox_7530_ax_dsl_2000x2000px.jpg){width=70%}

Caratteristiche:

* modem DSL integrato
* router NAT
* Wi-Fi
* switch LAN integrato
* funzioni domestiche (VoIP, NAS, parental control)


---

# FIREWALL / NEXT-GENERATION FIREWALL (NGFW)

## Ruolo nella rete

Il **firewall** protegge la rete aziendale controllando il traffico tra:

* LAN interna
* Internet
* eventuali DMZ

Nei dispositivi moderni il firewall è spesso un **NGFW (Next-Generation Firewall)** con funzionalità di sicurezza avanzate.

---

## Tipologie

* **Stateful firewall**
* **NGFW**
* **UTM (Unified Threat Management)**

---

## Funzionalità principali

* Stateful packet inspection
* **Deep Packet Inspection**
* **IPS / IDS**
* anti-malware
* **web filtering**
* VPN
* controllo applicazioni

---

## Altre caratteristiche importanti

* **throughput firewall**
* throughput **VPN**
* numero massimo di **sessioni simultanee**
* porte multi-gigabit
* gestione centralizzata

---

## FIREWALL / NEXT-GENERATION FIREWALL (NGFW): Modelli rappresentativi

### WatchGuard Firebox T40

Pagina ufficiale produttore
[https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html](https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html)

Immagine online
[https://www.watchguard.com/sites/default/files/styles/medium/public/t40_compare.png](https://www.watchguard.com/sites/default/files/styles/medium/public/t40_compare.png)

./imgs/t40_compare.png

![image_13](../imgs/dispositivi_img13_r645_t40_compare.jpg){ width=70% }

Caratteristiche:

* firewall **NGFW**
* **IPS**
* VPN
* gestione centralizzata WatchGuard

---

### Fortinet FortiGate 40F

Pagina ufficiale (datasheet)
[https://www.fortinet.com/resources/data-sheets/fortigate-fortiwifi-40f-series](https://www.fortinet.com/resources/data-sheets/fortigate-fortiwifi-40f-series)

Immagine online
[https://computer.milano.it/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/f/g/fg40f_1648711_base_1.jpg](https://computer.milano.it/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/f/g/fg40f_1648711_base_1.jpg)



![image_14](../imgs/dispositivi_img14_r666_61YoNT4HPZL._AC_SL1500.jpg){ width=70% }




Caratteristiche:

* firewall **NGFW**
* IPS
* **SSL inspection**
* VPN
* throughput elevato per fascia SMB

---

# Patch Panel  

## Patch panel Ethernet


Un **patch panel Ethernet** è un dispositivo passivo utilizzato negli armadi di rete per **terminare e organizzare i cavi Ethernet del cablaggio strutturato** di un edificio.

Video Tutorials:  
semplice, ottimo: https://www.youtube.com/watch?v=FfQui0mk85Q  
https://www.youtube.com/watch?v=lhz8cn0PEv4 



### Terminare

In ambito di cablaggio di rete, **terminare un cavo** significa collegare in modo stabile e definitivo i fili del cavo a un connettore o a un dispositivo.  
Nel caso dei cavi Ethernet, la terminazione consiste nel collegare i singoli fili del cavo:

* ai contatti di una presa di rete
  oppure
* ai contatti di un patch panel

Questa operazione viene normalmente eseguita tramite sistemi chiamati **IDC (Insulation Displacement Contact)** o **punch-down**.

Il cavo Ethernet contiene **8 fili (4 coppie)**. Durante la terminazione questi fili vengono inseriti nei contatti metallici del patch panel seguendo uno schema standard di cablaggio (T568A oppure T568B).

![Image](../imgs/dispositivi_img15_r707_remote_580092d2e2.jpg){width=60%}

![Image](../imgs/dispositivi_img16_r709_remote_a0268afc7e.jpg){width=60%}



Una volta terminato, il cavo diventa parte permanente dell’infrastruttura dell’edificio e non viene più scollegato.

---  

Il patch panel è installato normalmente in un **rack standard da 19 pollici** insieme ad altri dispositivi di rete come switch, router e firewall.

La sua funzione principale è quella di fornire un punto ordinato in cui arrivano tutti i cavi di rete provenienti dalle prese Ethernet delle varie stanze dell’edificio.

Da questo punto i collegamenti vengono poi effettuati verso gli switch o altri dispositivi tramite cavi più corti chiamati **patch cord**.

---


### Struttura di un patch panel Ethernet

Un patch panel Ethernet è un pannello metallico montabile su rack che contiene una serie di porte RJ45.

I modelli più comuni hanno:

* **24 porte RJ45**
* **48 porte RJ45**

Il dispositivo ha due lati con funzioni diverse.

### lato frontale

Il lato frontale contiene le **porte RJ45** visibili nel rack.

Qui vengono collegati i **patch cord** che portano il traffico verso gli switch di rete.

### lato posteriore

Sul lato posteriore si trovano i terminali IDC nei quali vengono inseriti i fili dei cavi Ethernet provenienti dalle stanze dell’edificio.

Ogni porta frontale è collegata internamente a uno di questi terminali.

---

### Come si inserisce in una rete

In un edificio con cablaggio strutturato ogni presa Ethernet è collegata con un cavo che arriva fino alla sala server o all’armadio di rete.

Questi cavi non vengono collegati direttamente allo switch.

Vengono invece terminati nel patch panel.

Il collegamento completo diventa quindi:

presa Ethernet nella stanza
→ cavo Ethernet nel muro
→ terminazione nel patch panel
→ patch cord
→ switch di rete

![image_17](../imgs/dispositivi_img17_r767_patch-panel_switch_schema_02.jpg){width=60%}


![image_18](../imgs/dispositivi_img18_r770_path-panel_switch_photo01.jpg){width=60%}


Questo sistema permette di separare chiaramente:

* il cablaggio **permanente** dell’edificio  
* i collegamenti **variabili** verso gli apparati di rete

---

### Differenza tra cavo strutturato e patch cord

Il cavo che arriva al patch panel fa parte del **cablaggio strutturato** dell’edificio.

Questo cablaggio è pensato per rimanere installato per molti anni.

Per questo motivo i cavi strutturati:

* non devono essere piegati o scollegati frequentemente
* vengono terminati nel patch panel

I collegamenti che invece possono cambiare frequentemente sono i **patch cord**, cioè cavi Ethernet corti che collegano il patch panel allo switch.

Se cambia la configurazione della rete è sufficiente spostare questi patch cord.

![image_19](../imgs/dispositivi_img19_r795_patch-pane_switch_diagram.jpg)

---

### Posizione del patch panel nel rack

In un armadio di rete il patch panel è normalmente posizionato nella parte superiore del rack, mentre gli switch sono montati subito sotto.

Questo consente di usare patch cord molto corti e di mantenere il cablaggio ordinato.

Un esempio di disposizione tipica potrebbe essere:

patch panel 24 porte
patch panel 24 porte
switch 48 porte
router o firewall
UPS

In questo modo tutte le connessioni provenienti dalle stanze entrano nei patch panel e poi vengono distribuite agli switch.

---

### Numerazione ed etichettatura

Un elemento molto importante nell’uso dei patch panel è la **numerazione delle porte**.

Ogni porta del patch panel viene associata a una presa Ethernet nell’edificio.

Ad esempio:

porta 1 → ufficio 101
porta 2 → ufficio 102
porta 3 → sala riunioni

Questo permette agli amministratori di rete di identificare rapidamente la posizione fisica di ogni collegamento.

L’etichettatura è quindi una parte fondamentale della gestione del cablaggio.

---

### Vantaggi dell’uso di patch panel

L’utilizzo di patch panel è uno standard nelle infrastrutture di rete professionali perché offre diversi vantaggi.

Organizzazione del cablaggio
tutti i cavi arrivano in un punto ordinato

Maggiore flessibilità
è possibile cambiare rapidamente i collegamenti spostando i patch cord

Manutenzione più semplice
i guasti possono essere individuati più facilmente

Protezione degli apparati
gli switch non vengono collegati direttamente ai cavi permanenti dell’edificio

---

### Esempio pratico

Immaginare un edificio con 20 uffici, ciascuno con una presa Ethernet.

Tutti i cavi delle prese arrivano nella sala server e vengono terminati in un patch panel da 24 porte.

Per attivare la rete nell’ufficio 103 basta collegare con un patch cord:

porta 3 del patch panel
→ porta dello switch

Se un giorno l’ufficio cambia funzione, è sufficiente spostare il patch cord senza modificare il cablaggio dell’edificio.

---

### Alcuni riferimenti

Patch Panel – Wikipedia
[https://en.wikipedia.org/wiki/Patch_panel](https://en.wikipedia.org/wiki/Patch_panel)

Structured Cabling Basics – Cisco
[https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/10561-3.html](https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/10561-3.html)

Patch Panel vs Switch – FS
[https://www.fs.com/blog/patch-panel-vs-switch-understanding-their-role-in-the-network-7846.html](https://www.fs.com/blog/patch-panel-vs-switch-understanding-their-role-in-the-network-7846.html)

Structured Cabling Guide – RackSolutions
[https://www.racksolutions.com/news/blog/patch-panel/](https://www.racksolutions.com/news/blog/patch-panel/)


---   

### Patch Panel – SINTESI OPERATIVA

Switch
Distribuzione del traffico all’interno della LAN.
Segmentazione della rete tramite VLAN.
Supporto PoE per access point e telefoni IP.

Router / Edge Gateway
Collegamento tra LAN e Internet o WAN.
Gestione NAT, routing e VPN.

Firewall NGFW
Protezione perimetrale della rete.
Controllo delle applicazioni e prevenzione delle intrusioni.

---

# Access Point

Architettura

* Access Point → collegato a **switch di accesso (managed)**
* Switch di accesso → collegato al **core di rete o al firewall perimetrale**


In architetture più strutturate:

* access switch → distribution/core switch → firewall

---

## Ruolo dei dispositivi

### Switch di accesso (livello 2)

* collega dispositivi finali (AP, PC, telefoni IP)
* trasporta il traffico dati
* trasporta le VLAN tramite **trunk 802.1Q**
* può alimentare l’AP tramite **PoE (se supportato)**

---

### Access Point

* NON effettua routing IP
* NON assegna indirizzi IP
* NON crea VLAN
* associa ogni rete Wi-Fi (SSID) a una VLAN configurata

Funzione reale:

* ponte tra rete wireless e rete cablata
* mapping **SSID → VLAN**

---

### Firewall / Router (da specificare)

**firewall perimetrale**

* posizionato tra LAN e Internet
* collegato all’ONT/CPE ISP

Funzioni:

* routing tra VLAN (in architetture 2 layer) oppure solo verso Internet
* sicurezza (policy, filtering)
* NAT
* DHCP (spesso, ma non obbligatorio)

---

### Switch Layer 3 (se presente)

* routing tra VLAN (inter-VLAN routing)
* tipico in architetture a 3 layer o core avanzati

---

# ✔️ Come funzionano le VLAN sugli access point

L’access point **non rileva automaticamente le VLAN**.
Le VLAN devono essere:

* definite nell’infrastruttura (switch / firewall / core)
* configurate esplicitamente nell’access point

1. Lo switch collega l’AP tramite una porta configurata come:

   * **trunk 802.1Q**

2. Sul trunk transitano più VLAN (frame taggati)

3. L’access point:

   * riceve e invia traffico Ethernet con tag VLAN
   * non “sceglie” le VLAN automaticamente

4. Per ogni SSID:

   * si configura manualmente un **VLAN ID**

👉 Risultato:

* SSID → VLAN → rete IP

---

## Come l’AP gestisce le VLAN

### 1) Associazione SSID → VLAN

Esempio:

* SSID "Ufficio" → VLAN 10
* SSID "Ospiti" → VLAN 20
* SSID "IoT" → VLAN 30

---

### 2) Tagging del traffico

Quando un client trasmette:

* il client **non è consapevole delle VLAN**
* l’AP:

  * incapsula il traffico
  * aggiunge il **tag VLAN (802.1Q)**

---

### 3) Invio allo switch

Il traffico:

* esce dall’AP sulla porta Ethernet
* con tag VLAN corretto
* lo switch inoltra nella VLAN appropriata

---

## ✔️ Sintesi tecnica corretta

* VLAN definite nell’infrastruttura
* AP configura mapping SSID → VLAN
* switch trasporta VLAN (L2)
* routing e IP gestiti da firewall o L3 switch

---

# ✔️ Esempio pratico reale (Ubiquiti UniFi)

## Scenario

* Switch managed UniFi (access layer)
* Access point UniFi (es. U6 Pro)
* Firewall perimetrale (es. UniFi Gateway o equivalente)

---

## ✔️ Obiettivo

Creare 3 reti Wi-Fi separate:

| SSID    | VLAN | Rete IP       |
| ------- | ---- | ------------- |
| Ufficio | 10   | 10.10.10.0/24 |
| Ospiti  | 20   | 10.10.20.0/24 |
| IoT     | 30   | 10.10.30.0/24 |

---

## ✔️ Configurazione passo-passo

### 1) Configurazione rete (firewall o L3)

Due possibili scenari:

#### Caso A (2 layer, tipico PMI)

* gateway e routing su firewall perimetrale

* VLAN 10 → 10.10.10.1

* VLAN 20 → 10.10.20.1

* VLAN 30 → 10.10.30.1

* DHCP attivo su firewall

---

#### Caso B (3 layer)

* routing su switch Layer 3

* firewall usato solo per traffico Internet

---

### 2) Configurazione switch (access layer)

Porta verso AP:

* modalità: **trunk 802.1Q**
* VLAN consentite: 10, 20, 30
* (opzionale) VLAN di management non taggata

---

### 3) Configurazione access point

Nel controller:

* SSID "Ufficio"

  * VLAN ID: 10

* SSID "Ospiti"

  * VLAN ID: 20

* SSID "IoT"

  * VLAN ID: 30

👉 L’AP applica il tagging VLAN in base alla configurazione

---

## ✔️ Cosa succede nella pratica

1. dispositivo si connette a SSID "Ospiti"
2. AP associa VLAN 20
3. traffico inviato con tag VLAN 20
4. switch inoltra nella VLAN 20
5. DHCP assegna IP 10.10.20.x
6. routing gestito da firewall o L3

---

# ✔️ Errori comuni (ambito professionale)

❌ Porta AP configurata come access → VLAN multiple non funzionano
❌ VLAN non configurata sull’AP → traffico errato
❌ DHCP assente → client senza IP
❌ Routing non configurato → VLAN isolate
❌ Ambiguità su “firewall” → progettazione incoerente

---

# ✔️ Differenza chiave da ricordare

* VLAN → livello 2 (trasporto su switch)
* IP → livello 3 (firewall o L3 switch)
* AP → associazione Wi-Fi ↔ VLAN
* firewall perimetrale → sicurezza e accesso Internet

---

# ✔️ Nota sulla classificazione della rete Wi-Fi

* SSID aziendale → rete interna (ma spesso segmentata e a fiducia limitata)
* SSID ospiti → rete esterna / non trusted

---

# ✔️ Sintesi finale (rigorosa)

Un access point professionale opera nell’access layer e si collega a uno switch managed tramite una porta trunk 802.1Q quando sono presenti più SSID associati a VLAN diverse. Le VLAN non sono rilevate automaticamente ma devono essere configurate esplicitamente sia nell’infrastruttura di rete sia nell’access point. L’AP associa ogni SSID a una VLAN e inserisce il traffico nella VLAN corretta, mentre il trasporto avviene tramite lo switch e il routing IP è gestito dal firewall perimetrale o da uno switch Layer 3, a seconda dell’architettura adottata.
