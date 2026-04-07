# Wi-Fi – Overview

## 1. Introduzione

Il Wi-Fi è una tecnologia di rete locale senza fili (WLAN – Wireless Local Area Network) che permette la trasmissione di dati tramite onde radio.

Si basa sugli standard della famiglia **IEEE 802.11**, definiti dall’ente di standardizzazione IEEE.

L’obiettivo del Wi-Fi è fornire connettività IP in modo:

* mobile
* flessibile
* scalabile
* economicamente efficiente rispetto al cablaggio completo

---

## 2. Architettura di una rete Wi-Fi

![Image](https://cdn.shopify.com/s/files/1/0736/7566/9719/files/SEOon_wap_connect_with_switch_4925ef36-957d-4223-a07b-d73c343af1ee.jpg?v=1747894486)

![Image](https://www.conceptdraw.com/How-To-Guide/picture/Ultra-high-performance-WLAN.png)

![Image](https://images.openai.com/static-rsc-3/okPqYUBMLYtW2oXoSH9LNmZvCkNa3NpvzzfTVXuE7w16hTBBWkj18fg---bMtndf1PKovmCKVgJs4KK-08JUZUemY3tcQbT3tIeGrhw_GkU?purpose=fullsize\&v=1)

![Image](https://images.openai.com/static-rsc-3/ZqhYtsCd5tKa6ywb0XpGG7DHhgho8qzAyguC1xEYGwEV9BQC9QYWULsnUFMhDgBOtCoc8iXIB7eTLs6nImcSghdPjf66dh7wphV5kjuDm9I?purpose=fullsize\&v=1)

### Componenti fondamentali

* **Access Point (AP)**: dispositivo che collega la rete radio alla rete cablata.
* **Client wireless**: notebook, smartphone, tablet, stampanti.
* **Switch**: collega gli AP alla LAN cablata.
* **Firewall/gateway**: controlla e filtra il traffico verso Internet.
* Eventuale **controller Wi-Fi** (in ambito aziendale).

L’AP funziona come bridge di livello 2: inoltra frame tra rete radio e rete Ethernet.

---

## 3. Deployment tipico: casa vs azienda

### 3.1 Scenario domestico

Nella maggior parte delle abitazioni si utilizza un unico dispositivo “router Wi-Fi” che integra:

* modem/ONT (in alcuni casi separato)
* router IP con NAT
* firewall di base
* piccolo switch Ethernet
* access point Wi-Fi

Architettura tipica:

Router Wi-Fi (tutto-in-uno)
→ Internet

Se si aggiunge un AP separato, esso viene collegato a una porta LAN del router o a uno switch collegato al router.

Caratteristiche principali:

* autenticazione quasi sempre WPA2/WPA3-PSK
* rete unica o rete + guest
* assenza di VLAN complesse
* gestione locale semplificata

---

### 3.2 Scenario aziendale (medio-grande)

In azienda l’Access Point viene normalmente collegato via Ethernet a uno **switch di accesso**, spesso con **PoE (Power over Ethernet)** per fornire alimentazione.

La porta verso l’AP può essere:

* access (una sola VLAN)
* trunk 802.1Q (più VLAN per SSID diversi)

Architettura tipica semplificata:

Access Point
→ Switch di accesso (PoE)
→ Switch di distribuzione / Core
→ Firewall perimetrale (con funzioni di routing)
→ Collegamento WAN / ISP
→ Internet

In molte reti aziendali il firewall svolge anche la funzione di router verso l’esterno.

In ambienti piccoli (micro-azienda) l’AP può essere collegato direttamente allo switch integrato nel gateway/firewall aziendale. Non esiste un divieto tecnico: cambia il livello di complessità dell’infrastruttura.

Caratteristiche tipiche aziendali:

* gestione centralizzata degli AP (controller on-prem o cloud)
* segmentazione tramite VLAN
* autenticazione 802.1X con server RADIUS
* firewall con policy differenziate
* logging e monitoraggio

---

## 4. Bande di frequenza

### 2.4 GHz

* Maggiore copertura
* Più interferenze
* Velocità inferiori
* Solo 3 canali realmente non sovrapposti (1, 6, 11)

### 5 GHz

* Minori interferenze
* Maggior numero di canali
* Velocità elevate
* Copertura inferiore rispetto a 2.4 GHz

### 6 GHz (Wi-Fi 6E)

* Spettro più ampio
* Minore congestione
* Richiede dispositivi compatibili

La scelta dipende da distanza, densità utenti e tipo di traffico.

---

## 5. Standard principali IEEE 802.11

| Standard      | Nome commerciale | Note principali           |
| ------------- | ---------------- | ------------------------- |
| 802.11n       | Wi-Fi 4          | Introduce MIMO            |
| 802.11ac      | Wi-Fi 5          | Solo 5 GHz, alte velocità |
| 802.11ax      | Wi-Fi 6          | OFDMA, alta efficienza    |
| 802.11ax (6E) | Wi-Fi 6E         | Estensione ai 6 GHz       |

Tecnologie chiave:

* **MIMO**: più antenne per aumentare throughput.
* **MU-MIMO**: comunicazione simultanea con più client.
* **Beamforming**: concentrazione del segnale verso il client.
* **OFDMA**: suddivisione del canale in sottoportanti per migliorare efficienza in ambienti affollati.

Oggi, in ambito aziendale, lo standard consigliato è Wi-Fi 6.

---

## 6. Concetti radio fondamentali

**SSID**: nome della rete visibile agli utenti.
**BSSID**: MAC address radio dell’AP.
**Canale**: porzione di spettro utilizzata per trasmettere.
**Interferenza**: sovrapposizione di segnali radio che degrada le prestazioni.

Maggiore potenza non significa sempre migliore qualità: può aumentare interferenza e rumore.

---

## 7. Sicurezza Wi-Fi

![Image](https://www.researchgate.net/publication/315011118/figure/fig3/AS%3A471866793041922%401489513218666/Authentication-message-flow.png)

![Image](https://datasave.qsfptek.com/upload/2024-08-30/1725001354281.jpg)

![Image](https://www.inkbridgenetworks.com/web/image/3558-fb43d2bc/radius_diagram_auth_3324x2535.webp?access_token=01528220-784d-49e6-b2ee-f9ed2fc16e95)

![Image](https://www.researchgate.net/publication/267200782/figure/fig2/AS%3A295681374867457%401447507341325/Basic-RADIUS-Authentication-Process-Frahim-Santos-2006-p-216.png)

### Evoluzione dei protocolli

| Protocollo | Stato            |
| ---------- | ---------------- |
| WEP        | ❌ Insicuro       |
| WPA        | ❌ Obsoleto       |
| WPA2       | Ancora diffuso   |
| WPA3       | Standard attuale |

WEP e WPA non sono più considerati sicuri.

---

## 8. PSK vs Enterprise

### WPA2/WPA3-PSK

* Password condivisa
* Nessuna identificazione individuale
* Adatto a casa

### WPA2/WPA3-Enterprise

Basato su:

* 802.1X
* server RADIUS
* credenziali individuali (utente/password o certificato)

Processo:

1. Il client si associa all’AP.
2. L’AP inoltra la richiesta al server RADIUS.
3. Il server verifica le credenziali.
4. Se valide, l’accesso viene autorizzato.

Vantaggi:

* revoca selettiva utenti
* tracciabilità
* integrazione con dominio aziendale

---

## 9. Segmentazione tramite VLAN

In azienda è normale separare:

* rete dipendenti
* rete ospiti
* rete IoT
* rete amministrativa

Ogni SSID può essere associato a una VLAN diversa.
Il firewall applica regole differenti tra le VLAN.

Questo aumenta sicurezza e controllo del traffico.

---

## 10. Attacchi comuni

* Deauthentication attack
* Evil Twin (finto AP)
* Brute force su PSK
* Sniffing su reti aperte

Mitigazioni:

* WPA3
* 802.1X
* disabilitare WPS
* aggiornamenti firmware
* segmentazione VLAN
* monitoraggio centralizzato

---

## 11. Differenze sintetiche casa vs azienda

| Aspetto        | Casa                 | Azienda                   |
| -------------- | -------------------- | ------------------------- |
| AP             | Integrato nel router | Dispositivo dedicato      |
| Collegamento   | Diretto al router    | Switch PoE + firewall     |
| Autenticazione | PSK                  | 802.1X                    |
| Segmentazione  | Minima               | VLAN multiple             |
| Gestione       | Locale               | Centralizzata             |
| Sicurezza      | Base                 | Policy avanzate e logging |

---

## 12. Conclusione

Il Wi-Fi moderno è un’infrastruttura complessa che integra:

* radiofrequenza
* switching
* routing
* firewall
* autenticazione
* segmentazione

In ambito aziendale, una soluzione tecnicamente corretta e coerente con le richieste tipiche di una prova d’esame prevede:

Wi-Fi 6 + WPA3-Enterprise + 802.1X + RADIUS + VLAN + firewall perimetrale con policy differenziate.

Questo rappresenta l’approccio professionale attuale
