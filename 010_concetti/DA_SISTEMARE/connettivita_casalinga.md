Di seguito viene descritta, in modo sistematico, la **collocazione logica e fisica** dei principali componenti di una connessione domestica **ADSL** e **Fibra ottica (FTTH/FTTC)**, distinguendo tra:

* LAN (rete locale dell’abitazione)
* WAN (interfaccia verso l’operatore)
* Rete ISP (infrastruttura dell’operatore)

Si distinguono inoltre:

* componenti hardware
* componenti software/logici (servizi di rete)

---

SEZIONE 1 – ARCHITETTURA GENERALE

In una connessione domestica tipica esistono tre domini:

1. LAN (Local Area Network)
   Comprende tutti i dispositivi dell’abitazione:

   * PC
   * smartphone
   * stampanti
   * smart TV
   * NAS

2. WAN (Wide Area Network – lato utente)
   È l’interfaccia del modem/router che comunica con l’ISP.

3. Rete ISP
   Infrastruttura dell’operatore (centrali, router di aggregazione, backbone, accesso a Internet).

Il modem/router domestico è il punto di confine tra LAN e WAN.

---

SEZIONE 2 – COMPONENTI HARDWARE

1. Porta DSL (ADSL/VDSL)
   Collocazione: WAN
   Perché: collega fisicamente il modem al doppino telefonico che arriva dalla centrale.
   Lato ISP: è collegata a un DSLAM in centrale.

2. Porta ottica (FTTH)
   Collocazione: WAN
   Perché: riceve il segnale ottico proveniente dalla rete in fibra dell’ISP.
   Lato ISP: è collegata a OLT in centrale.

3. ONT (Optical Network Terminal)
   Collocazione: lato utente ma interfaccia WAN
   Perché: converte il segnale ottico in segnale Ethernet.
   Può essere:

   * esterno (scatola separata)
   * integrato nel modem

4. Porta WAN Ethernet (nei modem fibra)
   Collocazione: WAN
   Perché: riceve traffico dal ONT o da un modem esterno.

5. Switch Ethernet interno (porte LAN)
   Collocazione: LAN
   Perché: smista il traffico tra dispositivi locali.

6. Access Point Wi-Fi
   Collocazione: LAN
   Perché: fornisce accesso wireless ai dispositivi interni.

7. CPU del router
   Collocazione: dispositivo domestico
   Funzione: esegue il sistema operativo e tutti i servizi di rete.

8. Memoria RAM/Flash
   Collocazione: dispositivo domestico
   Funzione: esecuzione firmware e configurazione.

---

SEZIONE 3 – COMPONENTI SOFTWARE / LOGICI

1. Firmware / Sistema operativo del router
   Collocazione: dispositivo domestico
   Perché: gestisce routing, NAT, firewall, DHCP.

2. Server DHCP (LAN)
   Collocazione: LAN
   Perché:

   * assegna IP privati ai dispositivi domestici (es. 192.168.1.x)
   * opera solo nella rete locale
     Non è visibile dalla WAN.

3. Client DHCP (WAN)
   Collocazione: WAN
   Perché:

   * il router riceve un IP pubblico o privato dall’ISP
   * il server DHCP che assegna l’IP si trova nella rete ISP

4. NAT (Network Address Translation)
   Collocazione: nel router, tra LAN e WAN
   Perché:

   * traduce IP privati LAN in IP pubblico WAN
   * è il meccanismo che consente a più dispositivi di condividere un IP pubblico
     Opera sul confine LAN ↔ WAN.

5. Routing
   Collocazione:

   * routing locale: nel router domestico
   * routing Internet: nella rete ISP e backbone Internet

   Perché:

   * il router domestico instrada tra LAN e WAN
   * i router ISP instradano verso Internet globale

6. Firewall
   Collocazione: nel router domestico
   Perché:

   * filtra traffico in ingresso dalla WAN verso la LAN
   * protegge dispositivi interni
     Opera principalmente sul traffico WAN → LAN.

7. PPPoE (nelle ADSL/VDSL tradizionali)
   Collocazione: WAN
   Perché:

   * crea sessione autenticata con ISP
   * termina su server BRAS dell’ISP

8. DNS Relay / DNS Forwarder
   Collocazione: LAN
   Perché:

   * il router riceve richieste DNS dai dispositivi locali
   * le inoltra ai server DNS dell’ISP o pubblici (WAN)

9. UPnP
   Collocazione: LAN
   Perché:

   * permette ai dispositivi interni di aprire porte sul NAT

10. QoS
    Collocazione: router domestico
    Perché:

    * gestisce priorità traffico prima dell’uscita verso WAN

---

SEZIONE 4 – COMPONENTI NELLA RETE ISP

1. DSLAM (ADSL/VDSL)
   Collocazione: rete ISP (centrale)
   Funzione:

   * aggrega linee ADSL degli utenti

2. OLT (FTTH)
   Collocazione: rete ISP
   Funzione:

   * gestisce le linee in fibra ottica

3. BRAS / BNG
   Collocazione: rete ISP
   Funzione:

   * termina sessioni PPPoE
   * assegna IP

4. Router di aggregazione
   Collocazione: rete ISP
   Funzione:

   * instradamento verso backbone

5. Server DNS ISP
   Collocazione: rete ISP
   Funzione:

   * risoluzione nomi per clienti

---

SEZIONE 5 – SCHEMA RIASSUNTIVO

LAN (casa)

* PC, smartphone
* Switch interno
* Wi-Fi AP
* Server DHCP (LAN)
* DNS relay
* UPnP
* parte LAN del firewall

Confine LAN ↔ WAN

* NAT
* Routing domestico
* Firewall
* QoS

WAN (interfaccia esterna del router)

* Porta DSL o porta WAN Ethernet
* PPPoE client
* DHCP client WAN
* ONT (fibra)

Rete ISP

* DSLAM / OLT
* BRAS / BNG
* DHCP server pubblico
* DNS ISP
* Router backbone

---

SEZIONE 6 – DIFFERENZA ADSL vs FIBRA

ADSL

* Mezzo fisico: doppino telefonico
* Porta DSL nel modem
* Necessaria modulazione DSL
* DSLAM in centrale

FTTH

* Mezzo fisico: fibra ottica
* ONT converte segnale
* OLT in centrale
* Nessuna modulazione DSL

Dal punto di vista logico (DHCP, NAT, firewall, routing) il funzionamento è sostanzialmente identico.

---

-----------------------------

Di seguito vengono prodotti **diagrammi architetturali chiari** per:

1. Connessione ADSL/VDSL
2. Connessione FTTH (fibra ottica pura)

Le immagini sono organizzate per livelli: LAN – Confine Router – WAN – Rete ISP.

---

## 1) Architettura ADSL / VDSL

![Image](https://www.open.edu/openlearncreate/pluginfile.php/259785/mod_oucontent/oucontent/35343/4d74da75/dc44f95b/cn_white_fig1.jpg)

![Image](https://www.researchgate.net/publication/360039255/figure/fig3/AS%3A11431281086907858%401664425698850/Typical-ADSL-configuration-which-connects-the-home-network-and-the-telecommunication.png)

![Image](https://docs.oracle.com/cd/E19120-01/open.solaris/819-1634/images/PPPoE-basic.gif)

![Image](https://www.ciscopress.com/content/images/chap3_9781587134326/elementLinks/03fig10_alt.jpg)

### Struttura logica dettagliata

```
DISPOSITIVI CASA (LAN)
---------------------------------------------------
PC        Smartphone       Smart TV       NAS
   |            |              |           |
   ------------------ Switch LAN -----------
                     |
               Access Point WiFi
                     |
              [ ROUTER / MODEM ]
---------------------------------------------------
              COMPONENTI INTERNI ROUTER
---------------------------------------------------
  - Server DHCP (assegna IP 192.168.x.x)
  - NAT (traduce IP privati → IP pubblico)
  - Firewall (blocca traffico WAN→LAN)
  - DNS Relay
  - Routing locale
  - QoS
---------------------------------------------------
                    |
                 Interfaccia WAN
                    |
               Client PPPoE
                    |
                 Porta DSL
---------------------------------------------------
                 Doppino telefonico
---------------------------------------------------
                DSLAM (ISP)
                    |
                BRAS / BNG
                    |
             Router di aggregazione ISP
                    |
                 Internet
```

### Collocazione funzionale

LAN:

* Switch interno
* WiFi
* DHCP server
* DNS relay
* UPnP

Confine LAN/WAN:

* NAT
* Firewall
* Routing

WAN:

* Porta DSL
* Client PPPoE
* DHCP client WAN (se previsto)

Rete ISP:

* DSLAM
* BRAS/BNG
* DNS ISP
* Backbone

---

## 2) Architettura FTTH (Fibra Ottica)

![Image](https://cdn.shopify.com/s/files/1/0106/6339/5391/files/FTTH_PON_Architecture_1024x1024.jpg?v=1719537131)

![Image](https://kmpic.asus.com/images/2022/07/01/a4d21bed-f0f3-422b-b533-50f27f26dca5.png)

![Image](https://www.researchgate.net/publication/3199579/figure/fig1/AS%3A638823323168771%401529318757375/Network-architecture-of-an-EPON-with-one-optical-line-terminal-OLT-and-N-5-optical.png)

![Image](https://cdn.shopify.com/s/files/1/0613/4041/8306/files/GPON_Technology2.jpg?v=1649843890)

### Struttura logica dettagliata

```
DISPOSITIVI CASA (LAN)
---------------------------------------------------
Laptop     Smartphone     Stampante      TV
    |            |             |          |
    -------------- Switch LAN --------------
                      |
                Access Point WiFi
                      |
                 [ ROUTER ]
---------------------------------------------------
              COMPONENTI INTERNI ROUTER
---------------------------------------------------
  - Server DHCP LAN
  - NAT
  - Firewall
  - Routing
  - QoS
---------------------------------------------------
                      |
                Porta WAN Ethernet
                      |
                   ONT
                      |
                Fibra Ottica
---------------------------------------------------
                    OLT (ISP)
                      |
                 BNG / Router ISP
                      |
                   Internet
```

### Differenze chiave rispetto ad ADSL

ADSL:

* Modulazione DSL
* Porta DSL nel router
* DSLAM in centrale

FTTH:

* Nessuna modulazione DSL
* ONT converte ottico → Ethernet
* OLT in centrale

Dal punto di vista software:

* DHCP LAN sempre nel router
* NAT sempre nel router
* Firewall sempre nel router
* IP pubblico assegnato da ISP
* Routing globale gestito da ISP

---

## 3) Vista Concettuale a Blocchi (Generale)

```
[ LAN CASA ]
    |
    |  IP privati (192.168.x.x)
    v
[ ROUTER ]
    - DHCP server (LAN)
    - NAT
    - Firewall
    - Routing
    - QoS
    |
    |  IP pubblico
    v
[ RETE ISP ]
    - Accesso (DSLAM / OLT)
    - BNG
    - Router backbone
    - DNS ISP
    |
    v
[ INTERNET ]
```

---
