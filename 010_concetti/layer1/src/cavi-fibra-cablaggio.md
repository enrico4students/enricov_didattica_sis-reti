---

marp: false
theme: portrait
paginate: true

--- 

# Cavi Ethernet in rame

Obiettivo: comprendere quale cavo scegliere in base a velocità, distanza e ambiente di utilizzo.

<!-- slideseparator -->

## 1. Struttura del cavo Ethernet

Un cavo Ethernet in rame è composto da:

* 4 coppie di fili intrecciati
* guaina esterna protettiva
* eventuale schermatura metallica
* connettore RJ-45

L’intreccio dei fili riduce le interferenze tra le coppie (**diafonia**).

<!-- slideseparator -->

## 2. Le due classificazioni fondamentali

Quando si sceglie un cavo occorre considerare due parametri distinti:

1. **Categoria (Cat5e, Cat6, Cat6a, …)** → prestazioni elettriche
2. **Schermatura (UTP, STP, FTP, S/FTP)** → protezione dalle interferenze

Sono indipendenti e si combinano tra loro.

Esempio: Cat6 UTP, Cat6a S/FTP.

<!-- slideseparator -->

## 3. Le categorie principali

### Cat5e

![Image](https://images.openai.com/static-rsc-3/DLLpUop897H55KzCWZ-5Un5khTcnGXhebFnoOH_KtZUgYVzuI38Rz3XDkL-WaWvbBH02hHNJuS1k7hwLjz_0d4dOkRBrglkaWcMKGmrzkq4?purpose=fullsize\&v=1){width=50%}

![Image](https://assets.belden.com/m/6872136b20bc04e1/original/10GXW12-JACKET-Blog-Image.jpg){width=50%}

* Frequenza: 100 MHz
* Velocità: fino a 1 Gbit/s
* Distanza massima: 100 m

Uso tipico:

* abitazioni
* laboratori scolastici
* piccoli uffici

<!-- slideseparator -->

### Cat6

![Image](https://images.openai.com/static-rsc-3/8KDzCPXjmNX_A2hu5_sOrMoiTJ3MjHi6A_Io--8JITgEBQVZsiaXjDWTGi-pmUsJk4NNeCybRxIYlFdG0cFeCxnXbjYwbFKtyvB7hDDjN7g?purpose=fullsize\&v=1)

![Image](https://www.metabee.com/media/wysiwyg/Structure_of_CAT6_Cables_-_METABEE.jpg)

* Frequenza: 250 MHz
* 1 Gbit/s fino a 100 m
* 10 Gbit/s fino a circa 55 m

Uso tipico:

* uffici moderni
* nuove installazioni

<!-- slideseparator -->

### Cat6a

![Image](https://images.openai.com/static-rsc-3/8KDzCPXjmNX_A2hu5_sOrMoiTJ3MjHi6A_Io--8JITgEBQVZsiaXjDWTGi-pmUsJk4NNeCybRxIYlFdG0cFeCxnXbjYwbFKtyvB7hDDjN7g?purpose=fullsize\&v=1)


* Frequenza: 500 MHz
* 10 Gbit/s fino a 100 m

Uso tipico:

* reti aziendali evolute
* sale server

<!-- slideseparator -->

## 4. Tipi di schermatura

### UTP (Unshielded Twisted Pair)

* Nessuna schermatura metallica
* Più economico
* Adeguato in ambienti normali

### STP / FTP / S/FTP

* Presenza di schermatura metallica
* Maggiore protezione da interferenze
* Richiede messa a terra corretta

Uso consigliato:

* ambienti industriali
* vicinanza a linee elettriche o macchinari

<!-- slideseparator -->

## 5. Lunghezza massima

Per tutti i cavi Ethernet in rame:

* Lunghezza massima standard: **100 metri**

Oltre questa distanza:

* il segnale si degrada
* è necessario uno switch intermedio o fibra ottica

<!-- slideseparator -->

## 6. Guida pratica alla scelta

Casa o scuola (1 Gbit/s):

* Cat5e UTP
* Cat6 UTP per maggiore durata nel tempo

Ufficio moderno:

* Cat6 UTP

Rete 10 Gigabit:

* Cat6a

Ambiente con interferenze:

* Cat6 o Cat6a schermato

<!-- slideseparator -->

## Conclusione

La scelta dipende da:

* velocità richiesta
* distanza
* ambiente elettromagnetico
* possibilità di espansione futura

Per la maggior parte delle installazioni moderne, **Cat6 UTP rappresenta un buon compromesso tra costo, prestazioni e affidabilità**.



# ISO/IEC 11801 – Cablaggio strutturato per edifici e campus

![Image](https://9233480.fs1.hubspotusercontent-na1.net/hubfs/9233480/tailwind-feat-whatisapatchpanel.jpg){width=70%}

![Image](https://www.techservicetoday.com/hubfs/Cat6%20Wiring%20Diagram.jpg){width=70%}{width=70%}

![Image](https://www.unitekfiber.com/uploads/image/20230815/10/fiber-optic-patch-panel-rack-mount.webp){width=70%}



![Image](https://www.fibertekfibershop.com/cdn/shop/products/rack-mount-sliding-fiber-optic-patch-panel-with-lc-duplex-adapters-1u-height-fpp124-series-27972665_700x700.jpg)
{width=70%}

### 1. Che cos’è ISO/IEC 11801


**ISO/IEC 11801** è uno standard internazionale che definisce i requisiti per il **cablaggio strutturato generico** negli edifici (uffici, scuole, industrie, data center) e nei campus.

È pubblicato da:

* International Organization for Standardization
* International Electrotechnical Commission

Obiettivo principale:
progettare un’infrastruttura di cablaggio **neutra rispetto alle applicazioni**, capace di supportare voce, dati, video e servizi futuri senza rifare l’impianto.

<!-- slideseparator -->

### 2. Concetto di cablaggio strutturato

Il cablaggio strutturato non è un insieme casuale di cavi, ma un sistema organizzato basato su:

* topologia gerarchica
* punti di concentrazione (armadi, rack)
* permutazioni tramite patch panel
* separazione tra cablaggio permanente e cordoni di permutazione

Principio fondamentale:
l’infrastruttura fisica deve essere stabile nel tempo, mentre gli apparati attivi (switch, router) possono cambiare.

<!-- slideseparator -->

### 3. Architettura definita dallo standard

ISO/IEC 11801 definisce una struttura a livelli:

1. **Campus (complesso/comprensorio)backbone**
2. **Building backbone**
3. **Horizontal cabling**
4. **Work area**

Topologia logica: **a stella gerarchica**.

Caratteristiche principali:

* lunghezza massima collegamento orizzontale: 90 m (permanent link)
* 100 m complessivi includendo patch cord
* separazione tra dorsali e cablaggio orizzontale

<!-- slideseparator -->

### 4. Classi e categorie

Lo standard distingue tra:

* **Categorie (Category)** → riferite ai componenti (cavi, connettori)
* **Classi (Class)** → riferite al canale completo

Esempi:

* Cat 5e → Classe D
* Cat 6 → Classe E
* Cat 6A → Classe EA
* Cat 7 → Classe F
* Cat 8 → Classe I / II

Le classi sono definite in base alla **frequenza massima supportata** (MHz).

<!-- slideseparator -->

### 5. Supporto ai servizi Ethernet

Il cablaggio conforme ISO/IEC 11801 consente di supportare standard IEEE come:

* IEEE 802.3

Esempi:

* 1000BASE-T (1 Gbps)
* 10GBASE-T (10 Gbps)
* 25G/40GBASE-T (Cat 8)

Il principio è che lo standard di cablaggio è **indipendente dal protocollo**, ma deve garantire parametri elettrici adeguati (attenuazione, NEXT, FEXT, ecc.).

<!-- slideseparator -->

### 6. Parametri tecnici principali

ISO/IEC 11801 definisce limiti per:

* attenuazione (insertion loss)
* diafonia (NEXT, PSNEXT)
* perdita di ritorno (return loss)
* ritardo di propagazione
* differenza di ritardo (skew)

Questi parametri vengono verificati tramite certificatori di cablaggio.

<!-- slideseparator -->

### 7. Varianti dello standard

Lo standard è suddiviso in più parti:

* ISO/IEC 11801-1 → requisiti generali
* ISO/IEC 11801-2 → edifici per uffici
* ISO/IEC 11801-3 → ambienti industriali
* ISO/IEC 11801-4 → data center
* ISO/IEC 11801-5 → edifici residenziali

Ogni parte adatta i requisiti all’ambiente operativo.

<!-- slideseparator -->

### 8. Differenze rispetto ad altri standard

ISO/IEC 11801 è lo standard internazionale.

Esiste anche lo standard americano:

* Telecommunications Industry Association
* ANSI/TIA-568

Le differenze sono minime a livello tecnico; la scelta dipende dal contesto geografico e normativo.

<!-- slideseparator -->

### 9. Perché è importante in azienda

Vantaggi concreti:

* scalabilità
* interoperabilità tra vendor
* supporto a nuove tecnologie
* riduzione costi nel lungo periodo
* manutenzione semplificata

Un impianto non conforme può generare:

* problemi di performance
* difficoltà di certificazione
* incompatibilità future

Un impianto conforme garantisce:

* prestazioni prevedibili
* documentazione tecnica standardizzata
* longevità dell’infrastruttura

<!-- slideseparator -->

### 10. Sintesi finale

ISO/IEC 11801:

* definisce l’architettura del cablaggio strutturato
* stabilisce classi e categorie
* impone limiti elettrici misurabili
* separa infrastruttura passiva da apparati attivi
* garantisce compatibilità con le tecnologie Ethernet moderne

È la base tecnica di qualsiasi rete aziendale moderna progettata correttamente.


---   

## Fibra ottica per la progettazione di rete (approccio pratico)

![Image](https://images.openai.com/static-rsc-4/vKa6XIzH-sWIMw8WWSINiJADS8gSby-7D6IPmOg55d1FzBXpwId5pnR1Wk-__N0fLNb3o_ZRaRJZDrz61BfYdNsvyD_9hZxw5mnPl12l9wkL43ppcxJmnsXm0_dgl279-3ihS_n1UfZ4FHm8Qf-4SNgeAA_3tS_v1z7OcWOeQS5yExjXjSaeLAvjrDAbgHu1?purpose=fullsize){width=70%}

![Image](https://images.openai.com/static-rsc-4/xs70vXwyMn54D3mB7HFUoLBlcZbFEO5Rh1aj3MubS2yoM4QaKoiLKHhnGN3s3Co4uEkB-uPsfwWVb5REDUd-d-AyglWxH7CEEE_beDI6jQQudXqQCGA-BDHfF1_2BbEnkFdTHc1a8SBvBxMUXYtFdFPRbtyWk784lu60fZISu2IPvYjdv_MA22HzTg4M7w_i?purpose=fullsize){width=70%}

![Image](https://images.openai.com/static-rsc-4/EzsNStErWk36SGikB_qkJH8dl7m2A4xR-ReaRAEjHgRa1PxcgFr7cXobPto61B_SOKl5FaCfvTFSEGv2a9EM0TqFj7zYKMfu6FagXiZ2h7kei-9cgGvJhTpf9IHJtZ5x7iqLwB9gY-cQF6XBzxzhbAnpSDXdGbhDkgm1J-OnFmlwLOSbGytxLdq1yeYE7snY?purpose=fullsize){width=70%}

![Image](https://images.openai.com/static-rsc-4/HmfL-ALvD5Hqa51bmgjR6Jmby97fjmnfOXcCmA66uo5DgFSwA8uJ7d_52WyyyejLFhVexTYZ2EZFvaKpENBRyu3jjvrLlv_CMTN43Gch4wF4SvFGFnOucLKhQ-KsOlz5x8JI7DMD4mhL8eHD2kByC3ehYVtpDQ5bSN3xXVGZNp89OI1CZw2nv82OpR_4W8BL?purpose=fullsize){width=70%}

![Image](https://images.openai.com/static-rsc-4/joKsPiImAiG6XtWTDeiyZAEIscTnQPQ74HVNWzeS4-r8IUNiCUXyZzDP37duBkI9P0sVdqsZiScKyZoJ4rAlhuEdlOBUKeVaI5-clMLLxj1jObRWS4mslw4rn23AcY95AJ2ce20Oo99lzbE5kiMefeHmYCN5TrgzjMysWgyK6lDfSYy7vpT_CZWOXKZy7NIW?purpose=fullsize){width=70%}

la fibra ottica serve per:

* collegare switch tra loro (al momento poco usata in access layer)
* realizzare uplink ad alta velocità
* coprire distanze dove il rame non è sufficiente

---

## Tipologie realmente usate  

### Multimodale (MM)

* tipicamente colore **arancione o acqua (OM3/OM4)**
* usata in LAN e data center
* costo più basso

Distanze tipiche:

* 1 Gbps → fino a **~550** m
* 10 Gbps → **300–400** m (OM3/OM4)

Uso tipico:

* access switch → core (stesso edificio)
* collegamenti tra rack

---

### Monomodale (SM)

* tipicamente colore **giallo**
* usata per lunghe distanze

Distanze tipiche:

* 1 Gbps / 10 Gbps → da km fino a **decine di km**
  (dipende dal modulo SFP)

Uso tipico:

* collegamenti tra edifici
* campus
* connessioni WAN / ISP

---

## Dispositivi necessari

![Image](https://images.openai.com/static-rsc-4/V3eKXCzCh_oWsK6uNl0R7v6HUWWw1l-vULMZTSKyyvmNMQVNZsNCURXj9weMz6wHx0NFBsm-oEQ4HoqRmnpyksi7E5zNBlhv3j7m2Yvxmic2LtuA59dC4cG49UkhW6nStsniMcvQ_Fvi7TCIUzGegYsHjY1z5rGgmKgbLQc9s2RzlWkJ7mKrq3UjgePXUZQ5?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/XAnl81lXD4xivLhnEW5ks-VcJ2TF3MLC9Tr3V7Ckvm4Tu1OqhmA3MVlnrCPPOLtvzPkLmKj4V_ISNNmga8uUd_dGYi4MIp2IFXXVKTzWL3sjfafuBn6w-1o7x6aEu_sbELIN4dtl48N2trpxeHk9mztBKb2Zk9bAYUELwDnYx1C3OCrWXJlBIiIHHurHazMA?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/B0AHbEby-tfTUGWt1sisOQef00UcX9AFhfi4zebuC8a7q_FYMigaPlVabLZ1k3Z2jiW_ClNErcVsAW4aMr6e56GrfE4qUe73q54SAGfXRUDWNRkLIcN5PnpXg__KRiRCgegpMhc-d0BCiAcrNIP-3fN3_gQ5X6CH4EhChRprd6rSlTH9WYzKPQATH_hK8szN?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/KimMruC9eCEKej3O0ziw5oez-WhtNHyuDfQRCfPmrQ0PjG4-WLgqAjJvoxzkYPaaV9Jz_5rICF2RDKf0GyNxwEgzUNyvXZ6L_q5gw7HsrQdeDLo4GR6S27Lh7Aw7861LNhuoZb_Z5eorBflOZtxnvB5OmuQQPV0L35d2tMpqrH9csn5yEMp4NGCz9EPSQ7Dt?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/klVV-Xh6cIGKT5H-oXRu3RE35r-0iXQCFSUCPj8PtBL122USYatz6oeKqRbxyoCOHcNT2FaH_GaTIyPyIzA9hw7rJIkyAxYZLh47m34lUsT_FA-v1f4peujPw2OFNN3mYrE0YIGXyrXmiSMkB0hzLwIKiJGlRAtPHcwBRO49nJz9_YQuctxESFZ6U12-WJe6?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/hxqLuJsCVyer6OIhlfKgmX6JY6D7wdAKFzdDfTb8IQ8cApRl5C6k3FgVBdeh5so01QOaBrNsQU33YbAvpa83y2fzxIqsS7Q_vMUjhQkhH2EmwXy51LYA5pZFHUSYmdCesc2P2BbJJ-Viee-_j9wSSUoxh_CYLLCbDgc7GOkTxk3nISGha4z9LSW2P6XK1Brw?purpose=fullsize)

Per usare la fibra con uno switch servono sempre:

### 1. Slot SFP nello switch

* presenti sugli switch professionali
* spesso usati per uplink

---

### 2. Modulo SFP / SFP+

* converte segnale elettrico ↔ ottico
* determina:

  * velocità (1G, 10G, …)
  * distanza
  * tipo di fibra

---

### 3. Cavo in fibra

* connettore tipico: **LC duplex**
* due fibre:

  * TX (trasmissione)
  * RX (ricezione)

---

## Tabella pratica (da usare nei progetti)

| Scenario                   | Tecnologia consigliata | Motivazione                       |
| -------------------------- | ---------------------- | --------------------------------- |
| Stesso rack                | DAC o fibra corta      | economico e semplice              |
| Stesso edificio            | Multimode (OM3/OM4)    | costo basso, distanza sufficiente |
| Tra edifici (100 m – 2 km) | Monomode               | evita limiti multimode            |
| Distanze elevate           | Monomode               | unica soluzione                   |

---

## Monomode vs Multimode, scelta, criteri pratici

### 1. Distanza

* < 100–300 m → multimode
* > 300–500 m → monomode

---

### 2. Velocità richiesta

* 1 Gbps → entrambe
* 10 Gbps → attenzione ai limiti della multimode
* > 10 Gbps → spesso monomode

---

### 3. Budget

* multimode:

  * cavi più costosi
  * moduli più economici

* monomode:

  * cavi più economici
  * moduli più costosi

---

### 4. Scalabilità futura

Scelta tipica professionale:

> usare direttamente **monomode** per evitare rifacimenti futuri

---

## Compatibilità (punto critico negli esami e nella realtà)

### 1. Compatibilità SFP ↔ switch

* standard esistono
* ma vendor come Cisco Systems o Hewlett Packard Enterprise possono limitare i moduli

Soluzione pratica:

* usare moduli certificati o compatibili

---

### 2. Compatibilità fibra ↔ modulo

* multimode ↔ SFP multimode
* monomode  ↔ SFP monomode

* **non** sono intercambiabili

---

### 3. Compatibilità connettori

* standard più comune: **LC**
* verificare sempre il tipo nell'uso reale

![](../imgs/fibra_connettore_LC_00.png)

---

### 4. Velocità

* SFP 1G ≠ SFP+ 10G
* devono essere compatibili su entrambi i lati

---

## Errori tipici (da evitare)

* usare multimode per distanze troppo lunghe (monomode è la scelta giusta)
* scegliere moduli non compatibili con lo switch (incompatibilità artificiose)
* non verificare TX/RX (fibra invertita)
* mescolare standard diversi (1G vs 10G)
* sottodimensionare gli uplink

---

## Sintesi operativa

In progettazione:

* usare **rame per utenti**
* usare **fibra per collegamenti tra apparati**
* scegliere:

  * multimode → distanze brevi, costo contenuto
  * monomode → distanze lunghe, maggiore flessibilità

e ricordare sempre:

> la fibra funziona solo insieme a moduli SFP corretti e compatibili

---

## Alcuni riferimenti

* [https://it.wikipedia.org/wiki/Fibra_ottica](https://it.wikipedia.org/wiki/Fibra_ottica)
* [https://www.fs.com/blog/what-is-fiber-optic-cable-105.html](https://www.fs.com/blog/what-is-fiber-optic-cable-105.html)
* [https://www.cisco.com/c/en/us/products/interfaces-modules/transceiver-modules/index.html](https://www.cisco.com/c/en/us/products/interfaces-modules/transceiver-modules/index.html)

---

