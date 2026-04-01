## DISPOSITIVI DI RETE COMUNI IN UNA LAN AZIENDALE

In una rete aziendale moderna esistono molti tipi di apparati di rete, ma tre categorie svolgono il ruolo più importante nell’architettura della rete:

* **Switch** → distribuzione del traffico all’interno della LAN
* **Router / Edge Gateway** → collegamento tra la LAN e altre reti (Internet o WAN)
* **Firewall / NGFW** → protezione della rete e applicazione delle politiche di sicurezza

Questi dispositivi svolgono funzioni diverse ma complementari e spesso sono installati nello stesso armadio di rete.

---

# 1. SWITCH DI RETE (Layer 2 / Layer 3)

## Ruolo nella rete aziendale

Lo **switch** è il dispositivo principale della rete locale (LAN).
Il suo compito è collegare tra loro i dispositivi interni della rete:

* computer
* server
* stampanti
* telefoni VoIP
* access point Wi-Fi
* altri switch

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

---

### Switch managed (Layer 2)

È la tipologia più diffusa nelle reti aziendali.

Caratteristiche:

* supporto **VLAN 802.1Q**
* QoS
* **Spanning Tree**
* monitoring **SNMP**
* gestione tramite web, CLI o cloud

Permette di segmentare la rete e controllare il traffico.

---

### Switch Layer 3

Oltre alle funzionalità di livello 2 offre anche:

* routing IP
* routing inter-VLAN
* ACL di base
* routing statico

Nelle architetture aziendali viene spesso utilizzato come:

* **distribution switch**
* **core switch**

---

## Numero di porte e caratteristiche tipiche

Numero porte comuni:

* 8
* 16
* 24
* 48

Velocità più diffuse:

* **1 Gbps** → standard aziendale
* **2.5 Gbps** → sempre più diffuso negli access switch
* **10 Gbps** → spesso usato per uplink

Uplink tipici:

* **SFP (1G)**
* **SFP+ (10G)**
* nei modelli enterprise anche **25G**

Supporto PoE:

* **PoE (802.3af)**
* **PoE+ (802.3at)**
* **PoE++** nei modelli più recenti

---

## Funzionalità principali degli switch aziendali

* VLAN 802.1Q
* QoS
* Link Aggregation (**LACP**)
* Spanning Tree (**RSTP / MSTP**)
* monitoring **SNMP**
* ACL
* gestione locale o cloud

---

## Altre caratteristiche tecniche rilevanti

Quando si valutano switch professionali si considerano anche:

* **switching capacity** (Gbps)
* **forwarding rate**
* **budget PoE totale**
* alimentazione ridondata
* possibilità di **stacking**

---

## Modelli rappresentativi

### Cisco Catalyst 9200 Series

Pagina ufficiale produttore
[https://www.cisco.com/site/us/en/products/networking/switches/catalyst-9200-series-switches/index.html](https://www.cisco.com/site/us/en/products/networking/switches/catalyst-9200-series-switches/index.html)

<img src="./imgs/nb-06-cat9200-ser-data-sheet-cte-en_0.webp" width="70%">


Caratteristiche principali:

* 24 o 48 porte 1G
* versioni PoE+
* uplink modulari 1G / 10G / 25G
* sistema operativo **Cisco IOS-XE**
* stacking

---

### TP-Link Omada SG3218XP-M2

Pagina ufficiale produttore
[https://www.omadanetworks.com/it/business-networking/omada-switch-access-pro/sg3218xp-m2/](https://www.omadanetworks.com/it/business-networking/omada-switch-access-pro/sg3218xp-m2/)

Immagine online
[https://static.tp-link.com/upload/image-line/TL-SG3218XP-M2_UN_1.0_overview_02_normal_20250126032358m.jpg](https://static.tp-link.com/upload/image-line/TL-SG3218XP-M2_UN_1.0_overview_02_normal_20250126032358m.jpg)

<img src="./imgs/TL-SG3218XP-M2_UN_1.0_overview_02_normal_20250126032358m.jpg" width="70%">



Caratteristiche:

* 16 porte **2.5G**
* 8 porte **PoE+**
* 2 uplink **SFP+ 10G**
* gestione cloud Omada
* switch **L2+ con routing statico**

---

### Zyxel XGS1935 Series (esempio XGS1935-28HP)

Pagina ufficiale produttore
[https://www.zyxel.com/global/en/products/switch/24-48-port-gbe-lite-l3-smart-managed-switch-with-4-10g-uplink-xgs1935-series](https://www.zyxel.com/global/en/products/switch/24-48-port-gbe-lite-l3-smart-managed-switch-with-4-10g-uplink-xgs1935-series)

Immagine online
[https://www.zyxel.com/sites/zyxel/files/library/assets/products/xgs1935-series/img_xgs1935-28hp_p_600x600.jpg](https://www.zyxel.com/sites/zyxel/files/library/assets/products/xgs1935-series/img_xgs1935-28hp_p_600x600.jpg)

<img src="./imgs/img_xgs1935-28hp_p_600x600.jpg" width="70%">


Caratteristiche:

* 24 o 48 porte 1G
* uplink **10G**
* versioni PoE
* gestione **smart L3 lite**
* VLAN e QoS avanzate

---

# 2. ROUTER AZIENDALI / EDGE GATEWAY

## Ruolo nella rete

Il **router aziendale** (o edge gateway) collega la LAN interna con:

* Internet
* reti WAN
* reti di sedi remote

Svolge anche funzioni di:

* NAT
* VPN
* firewall di base
* gestione del traffico WAN

---

## Tipologie più comuni

* router **multi-WAN**
* router con **SD-WAN**
* router **VPN hardware**
* router con **controller centralizzato**

---

## Porte tipiche

* 1 o più porte **WAN**
* 4–8 porte LAN
* talvolta **porte SFP**

---

## Funzionalità principali

* **NAT**
* VPN **IPsec / SSL**
* firewall stateful
* **load balancing WAN**
* **failover automatico**
* supporto **VLAN**

---

## Modelli rappresentativi

### TP-Link Omada ER8411

Pagina ufficiale produttore
[https://www.omadanetworks.com/it/business-networking/omada-router-wired-router/er8411/](https://www.omadanetworks.com/it/business-networking/omada-router-wired-router/er8411/)

Immagine online
[https://static.tp-link.com/upload/image-line/ER8411_UN_1.0_overview_01_normal_20220617022403i.jpg](https://static.tp-link.com/upload/image-line/ER8411_UN_1.0_overview_01_normal_20220617022403i.jpg)

<img src="./IMGS/ER8411_UN_1.0_overview_01_normal_20220617022403i.jpg" width="70%">
./imgs/tplink_er8411.jpg

Caratteristiche:

* porte **10G**
* multi-WAN
* VPN hardware
* firewall integrato
* gestione cloud Omada

---

### MikroTik RB5009UG+S+IN

Pagina ufficiale produttore
[https://mikrotik.com/product/rb5009ug_s_in](https://mikrotik.com/product/rb5009ug_s_in)

Immagine online
[https://i.mt.lv/cdn/product_files/RB5009UGS-IN_220903.png](https://i.mt.lv/cdn/product_files/RB5009UGS-IN_220903.png)

<img src="./imgs/2065_lg.webp" width="70%">



Caratteristiche:

* router ad alte prestazioni
* porta **10G SFP+**
* porte gigabit multiple
* sistema operativo **RouterOS**
* VPN e routing avanzato

---

# 3. FIREWALL / NEXT-GENERATION FIREWALL (NGFW)

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

## Modelli rappresentativi

### WatchGuard Firebox T40

Pagina ufficiale produttore
[https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html](https://www.watchguard.com/help/docs/help-center/en-US/Content/en-US/Hardware-Guides/firebox-t40-hardware-guide.html)

Immagine online
[https://www.watchguard.com/sites/default/files/styles/medium/public/t40_compare.png](https://www.watchguard.com/sites/default/files/styles/medium/public/t40_compare.png)

<img src="./imgs/t40_compare.png" width="70%">


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

<img src="./IMGS/61YoNT4HPZL._AC_SL1500_.jpg" width="70%">
<br/>

Caratteristiche:

* firewall **NGFW**
* IPS
* **SSL inspection**
* VPN
* throughput elevato per fascia SMB

---

# SINTESI OPERATIVA

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
