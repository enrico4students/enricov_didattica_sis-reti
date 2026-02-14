
## DISPOSITIVI DI RETE PIÙ UTILIZZATI IN AMBITO AZIENDALE

1. SWITCH DI RETE (Layer 2 / Layer 3)

Ruolo
Lo switch è il dispositivo centrale della LAN aziendale. Opera prevalentemente a livello 2 (MAC), ma nei modelli Layer 3 può gestire anche routing IP tra VLAN (non solo tra VLAN. Ma nella pratica aziendale è quello l’uso più tipico.).

Tipologie più usate

Unmanaged
Utilizzo in piccoli uffici o ambienti temporanei. Nessuna configurazione, nessuna VLAN, nessun controllo QoS.

Managed (L2)
Tipologia più diffusa in ambito aziendale. Supporta VLAN, QoS, STP, monitoring SNMP.

Layer 3
Oltre alle funzioni L2 consente routing tra VLAN, inter-VLAN routing, ACL di base. Usato come core o distribution switch.

Numero porte e caratteristiche tipiche

8 / 16 / 24 / 48 porte RJ45
Velocità:

* 1 Gbps (standard aziendale)
* 2.5 Gbps (multi-gigabit crescente diffusione)
* 10 Gbps per uplink

Uplink:

* SFP / SFP+ (1G / 10G)
* in modelli enterprise anche 25G

PoE:

* PoE (802.3af)
* PoE+ (802.3at)
* PoE++ nei modelli più recenti

Funzionalità principali

* VLAN 802.1Q
* QoS
* Link Aggregation (LACP)
* Spanning Tree (RSTP/MSTP)
* SNMP monitoring
* ACL
* gestione locale o cloud

Altre caratteristiche importanti

* Capacità di switching (Gbps)
* Throughput forwarding rate
* Budget PoE totale (in Watt)
* Alimentazione ridondata nei modelli enterprise
* Stackability (alcuni modelli Cisco)

Modelli rappresentativi

Cisco Catalyst 9200 Series

Pagina ufficiale produttore:
[https://www.cisco.com/c/en/us/products/switches/catalyst-9200-series-switches/index.html](https://www.cisco.com/c/en/us/products/switches/catalyst-9200-series-switches/index.html)

Immagine diretta:
[https://www.cisco.com/c/dam/en/us/products/collateral/switches/catalyst-9200-series-switches/nb-06-cat9200-ser-data-sheet-cte-en.docx/_jcr_content/renditions/nb-06-cat9200-ser-data-sheet-cte-en_0.png](https://www.cisco.com/c/dam/en/us/products/collateral/switches/catalyst-9200-series-switches/nb-06-cat9200-ser-data-sheet-cte-en.docx/_jcr_content/renditions/nb-06-cat9200-ser-data-sheet-cte-en_0.png)

Caratteristiche:

* 24 o 48 porte 1G
* versioni PoE+
* uplink modulari 1G/10G/25G
* gestione Cisco IOS-XE
* stacking

---

TP-Link Omada SG3218XP-M2

Pagina ufficiale produttore:
[https://www.omadanetworks.com/it/business-networking/omada-switch-access-pro/sg3218xp-m2/](https://www.omadanetworks.com/it/business-networking/omada-switch-access-pro/sg3218xp-m2/)

Immagine diretta:
[https://static.tp-link.com/upload/image-line/TL-SG3218XP-M2_UN_1.0_overview_02_normal_20250126032358m.jpg](https://static.tp-link.com/upload/image-line/TL-SG3218XP-M2_UN_1.0_overview_02_normal_20250126032358m.jpg)

Caratteristiche:

* 16 porte 2.5G
* 8 porte PoE+
* 2 uplink SFP+ 10G
* gestione cloud Omada
* L2+ con routing statico

---

Zyxel XGS1935 Series (es. XGS1935-28HP)

Pagina ufficiale produttore:
[https://www.zyxel.com/global/en/products/switch/24-48-port-gbe-lite-l3-smart-managed-switch-with-4-10g-uplink-xgs1935-series](https://www.zyxel.com/global/en/products/switch/24-48-port-gbe-lite-l3-smart-managed-switch-with-4-10g-uplink-xgs1935-series)

Immagine diretta:
[https://www.zyxel.com/sites/zyxel/files/library/assets/products/xgs1935-series/img_xgs1935-28hp_p_600x600.jpg](https://www.zyxel.com/sites/zyxel/files/library/assets/products/xgs1935-series/img_xgs1935-28hp_p_600x600.jpg)

Caratteristiche:

* 24 o 48 porte 1G
* uplink 10G
* versioni PoE
* gestione smart L3 lite
* VLAN e QoS avanzate

---

2. ROUTER AZIENDALI / EDGE GATEWAY

---

Ruolo
Connessione tra LAN aziendale e Internet / WAN. Gestione NAT, VPN, firewall base.

Tipologie più usate

* Router multi-WAN
* Router con SD-WAN
* Router VPN hardware
* Router con controller centralizzato

Porte tipiche

* 1 o più porte WAN (Gigabit o 10G)
* 4–8 porte LAN
* Talvolta SFP

Funzionalità principali

* NAT
* VPN IPsec / SSL
* Firewall stateful
* Load balancing WAN
* Failover automatico
* VLAN support

Modelli rappresentativi

TP-Link Omada ER8411

Pagina ufficiale produttore:
[https://www.omadanetworks.com/it/business-networking/omada-router-wired-router/er8411/](https://www.omadanetworks.com/it/business-networking/omada-router-wired-router/er8411/)

Immagine diretta:
[https://static.tp-link.com/upload/image-line/ER8411_UN_1.0_overview_01_normal_20220617022403i.jpg](https://static.tp-link.com/upload/image-line/ER8411_UN_1.0_overview_01_normal_20220617022403i.jpg)

Caratteristiche:

* porte 10G
* multi-WAN
* VPN hardware
* firewall integrato
* gestione cloud Omada

---

Cisco RV340 Series

Pagina ufficiale produttore:
[https://www.cisco.com/c/en/us/support/routers/rv340-router/model.html](https://www.cisco.com/c/en/us/support/routers/rv340-router/model.html)

Immagine diretta:
[https://www.cisco.com/c/dam/en/us/support/docs/SWTG/ProductImages/routers-small-business-rv-series-rv340-family.jpg](https://www.cisco.com/c/dam/en/us/support/docs/SWTG/ProductImages/routers-small-business-rv-series-rv340-family.jpg)

Caratteristiche:

* Dual WAN
* VPN IPsec
* firewall integrato
* destinato a PMI

---

3. FIREWALL / NEXT-GENERATION FIREWALL (NGFW)

---

Ruolo
Protezione perimetrale della rete aziendale.

Tipologie

* Stateful firewall
* NGFW (application-aware)
* UTM (Unified Threat Management)

Funzionalità principali

* Stateful packet inspection
* Deep Packet Inspection
* IPS / IDS
* Anti-malware
* Web filtering
* VPN
* controllo applicazioni

Altre caratteristiche rilevanti

* Throughput firewall (Gbps)
* Throughput VPN
* numero massimo sessioni simultanee
* porte multi-gigabit
* gestione centralizzata

Modelli rappresentativi

WatchGuard Firebox T40

Pagina ufficiale produttore:
[https://www.watchguard.com/wgrd-products/appliances-compare/firebox-t40](https://www.watchguard.com/wgrd-products/appliances-compare/firebox-t40)

Immagine diretta:
[https://www.watchguard.com/sites/default/files/styles/medium/public/t40_compare.png?itok=pBaky2ud](https://www.watchguard.com/sites/default/files/styles/medium/public/t40_compare.png?itok=pBaky2ud)

Caratteristiche:

* NGFW
* IPS
* VPN
* gestione centralizzata WatchGuard

---

Fortinet FortiGate 40F

Pagina ufficiale produttore (datasheet ufficiale):
[https://www.fortinet.com/resources/data-sheets/fortigate-fortiwifi-40f-series](https://www.fortinet.com/resources/data-sheets/fortigate-fortiwifi-40f-series)

Immagine diretta:
[https://computer.milano.it/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/f/g/fg40f_1648711_base_1.jpg](https://computer.milano.it/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/f/g/fg40f_1648711_base_1.jpg)

Caratteristiche:

* firewall NGFW
* IPS
* SSL inspection
* VPN
* elevato throughput per fascia SMB

---

## SINTESI OPERATIVA

Switch
Dispositivo di distribuzione interna LAN.
Segmentazione tramite VLAN.
PoE per access point e telefoni IP.

Router
Connessione WAN/Internet.
Gestione NAT e VPN.

Firewall NGFW
Protezione perimetrale avanzata.
Controllo applicazioni e intrusioni.

---

