# UNITÀ DIDATTICA

## Arduino e Raspberry Pi: sistemi embedded e sistemi general purpose

---

# LEZIONE 1 – Arduino

## 1.1 Che cos’è Arduino  

<!--


![Image](https://images.openai.com/static-rsc-4/Rn4W82_gJ3jU2lSJWFMb1XLjf9QeCcXwISRXqHyXpjZnfRqftZYssRKOkCa-5ihuyYPP4Myv859keLMAdxDbkjqebPwOWDto91Pa9R-o9KJnq_1oZyo5_n5NYQENSgiiVLlDkWrS_Il4shXDBxhP3EjRLqT01cfyTMcX-3vW4o0oYH5zkXNlgl1PYakbsNfU?purpose=fullsize){width=70%}


![Image](https://images.openai.com/static-rsc-4/Vz9aOSyg07-W442ezBVuiCqDdBriLz76GAhqYAJqooBfFS9fcUlkuBMQWy9fEyRUIC601f6KZIEYB1IeUZ1nLSkLmieiJnCT49-4rd_UC_Fgcnd2pO-IJ4rV22EI5GVabtxjwTMCOH2gnwaeBjbCG-1B_kN3zq1PEU04i6Ve7oFYZv2Dwpnvb2qJfI4CyyFz?purpose=fullsize){width=70%}


![Image](https://images.openai.com/static-rsc-4/VojsuUv2_N4QZ9Q67rvdlhbfphazXNfIhwWahGnH1I0N2giWs9O3F3rorOGQjBoZHyOOfjwzExsqQ8P9_FbueJ7MIYdmPONhjslUD0kr5l600y4ibSPZtlVf3V2I350Rm2r4HJol8JrlUMF05HJYrv2JRXqmafOHEZ2rbl1pQ672Stz2iN-OU8O7rCMsepy_?purpose=fullsize){width=70%}


![Image](https://images.openai.com/static-rsc-4/e0-9UlQX22q6tuOKcMpgj0OliggpeB1zgTO-PCkjBC7hjJt20J5ae2BZa15iWZ4Y7ItP2U0FR-ssTXeIMNkdGzrOoN-yu9ko7D-KS27Ng2_-H8EXl7NMrtY1LgBi4_6Mubn7S7ajWQPYY305ApunLIxQDUd0-6zTGnPP1SE3ph_I036A9_Cxf5RMd8q92w3k?purpose=fullsize){width=70%}



![Image](https://images.openai.com/static-rsc-4/RH1ohQWk1r8V_VPiGwIutfweRo5YGzRuzvUYPDc3OZAwTIYzLrFcv8ppXeH4bWtbjxkyQ11MjHf_1cRkSfrUxaT-xyb9CPtjvb2St4ThnbCGLDSBioHI1USWNOo_dtgZxI7cKbeq-M9MsgJVB_t39MvfCoZG6zdDrwvWbmqOYapy-6e3oUEQ4tZBMAtoOvP4?purpose=fullsize){width=70%}


-->

Arduino non è un “mini computer”, ma una **scheda elettronica programmabile basata su microcontrollore**.

Un **microcontrollore** è un componente che integra:

* CPU
* memoria limitata
* periferiche di input/output

tutto nello stesso chip.

![Image](https://images.openai.com/static-rsc-4/_acg5B2Erfo0hLnlPRypxHN1ZCRsq2bUPLsV2cyxv6kKsBwhB3RoMllhEAgnACGgJf9FCZ8YU5vBg5qTx20jldkux2cfe9LfEm53gXPUAQkQDoQdWTvTq8ah6LmsSTMDKydPgcylQRU4ZqzVKjRN7L_8G_3IEYWEtg3wg-UqVqTSa8NOgZ9ACbOaMa1jjjOR?purpose=fullsize){width=70%}


Arduino è progettato per:

* **controllare dispositivi fisici**
* reagire a segnali elettrici
* eseguire un comportamento specifico

Non è progettato per eseguire applicazioni generiche come un PC.

---

## 1.2 Differenza fondamentale rispetto a un PC

Un PC funziona così:

* sistema operativo (Windows, Linux)
* gestione di più programmi contemporaneamente
* interazione con utente (mouse, tastiera, GUI)

Arduino funziona così:

* **NON** ha sistema operativo
* esegue **un solo programma**
* il programma gira in un **ciclo continuo**

Struttura tipica:

```
void setup() {
    // inizializzazione
}

void loop() {
    // eseguito continuamente
}
```

Questo modello è radicalmente diverso dal PC:

* non esistono “finestre”
* non esiste multitasking reale
* non esiste gestione avanzata della memoria

---

## 1.3 Perché Arduino esiste  

Arduino è stato progettato per un problema preciso:

**controllare il mondo fisico in modo semplice e affidabile**

Caratteristiche chiave:

* accesso diretto ai pin (ingressi/uscite)
* gestione precisa del tempo (millisecondi, microsecondi)
* comportamento deterministico (non totalmente preciso, vedi precisazione)

Esempio:

* accendere un LED dopo esattamente 100 ms
* leggere un sensore ogni 10 ms

Un PC NON è adatto a questo:

* il sistema operativo introduce ritardi imprevedibili


---  

#### Arduino: tempo di esecuzione e comportamento deterministico

Arduino, ad esempio una scheda come Arduino Uno, è basato su un microcontrollore che esegue il programma in modo **sequenziale**, senza sistema operativo e senza meccanismi di multitasking.

Quando si afferma che Arduino ha un **comportamento deterministico**, non si intende che il tempo di risposta sia sempre costante, ma che è **prevedibile**: a parità di codice e condizioni, il tempo di esecuzione sarà sempre lo stesso.

Questo implica che il tempo di risposta dipende direttamente dal codice scritto. Se nel `loop()` si inseriscono cicli molto lunghi o nidificati che richiedono, ad esempio, 10 secondi per completarsi, il sistema impiegherà effettivamente quei 10 secondi prima di tornare a eseguire il resto del programma. Durante questo intervallo non verranno letti ingressi, aggiornate uscite o gestiti eventi: il sistema risulterà temporaneamente non reattivo.

Il determinismo quindi non garantisce velocità o reattività, ma **coerenza nei tempi di esecuzione**. Ogni istruzione richiede un numero noto di cicli di clock, e il tempo totale può essere stimato con buona precisione.

---

#### Gestione del tempo con millis()

La funzione `millis()` restituisce il numero di millisecondi trascorsi dall’avvio della scheda e permette di gestire il tempo **senza bloccare il programma**.

Il principio è semplice: confrontare il tempo corrente con un istante salvato in precedenza.

```
se (tempo_attuale - tempo_iniziale >= intervallo)
    eseguire operazione
```

In questo modo il programma continua a girare e può svolgere altre attività mentre “attende”.

---

#### Limite importante di millis()

`millis()` evita il blocco durante l’attesa, ma **non rende non-bloccante il codice eseguito**.

Se l’operazione eseguita è lunga:

```
if (millis() - last >= 1000) {
    last = millis();

    operazione_lunga();   // es. ciclo da 10 secondi
}
```

il microcontrollore resterà occupato per tutta la durata dell’operazione, risultando comunque non reattivo.

---

#### Come mantenere la reattività

Per ottenere un sistema realmente reattivo:

* evitare `delay()` prolungati
* evitare operazioni lunghe eseguite in un unico blocco
* suddividere il lavoro in piccoli passi
* eseguire un passo per volta ad ogni iterazione del `loop()`

Esempio concettuale:

```
if (millis() - last >= 10) {
    last = millis();
    eseguire_un_piccolo_passo();
}
```

In questo modo ogni ciclo dura poco e il sistema può continuare a gestire ingressi, uscite ed eventi.

---

#### Sintesi

Arduino consente un controllo preciso e prevedibile del tempo, ma richiede attenzione nella progettazione del codice:

* il tempo di esecuzione è deterministico, ma dipende dal codice
* `millis()` evita blocchi durante l’attesa
* operazioni lunghe restano bloccanti
* la reattività si ottiene solo progettando codice non bloccante


---  

### Arduino e breadboard  


![Image](https://images.openai.com/static-rsc-4/7I_gOEb_usHdGKza9lVU1ZAmnLy7oMHtjVUn1jW5Xolqc8x7XG_IwuWcOVbriWgSyIYV98T37oVcODoDpdBqSskHOTFVWa525Trzs3i-U-KJ8qsFYl3NErzqlWGYqCHWy4sgAGZYYC_RbC7uQosDcQuVXLB-fu5OZydmarUhxSRtvWaKk4OzSxTGOkHlFWoI?purpose=fullsize){width=70%}


---

## 1.4 Ambiti in cui Arduino è preferibile

Arduino è la scelta corretta quando:

* si controllano dispositivi fisici
* serve precisione temporale
* il sistema deve essere semplice e robusto
* il consumo deve essere minimo

---

## 1.5 Casi d’uso tipici

* sistemi di controllo (termostati)
* robotica semplice
* sensori ambientali
* automazione domestica base
* sistemi embedded industriali

---

# LEZIONE 2 – Raspberry Pi

## 2.1 Che cos’è Raspberry Pi

![Image](https://images.openai.com/static-rsc-4/ToD3Q4dF3Qrpg5WCb9h8ugkmAoa-wSbqtGI3RRvk154_jPJKyZaA95hwGtqA06VuoHh7FtlETo9xPYKDVkBCcSL5g3kY9nJ4bj-7O6h44Eeqvjd9uLGfWDj0kS02y3-2cmtuTaCnoLYfzkH4FT3eT6u8aDIgu9N47rxsebY__tYzoKLsABCrvFw-L-rv5G5G?purpose=fullsize)  


![Image](https://images.openai.com/static-rsc-4/mebY_J_g48FbzXMvGkJjLZYVMtspRZvrTIg8A76oh1nXrGQza8hMIHAXsl_FxtIzK0grHSYHF66WINfRWSfYP21gM1UV7RsAcfd0vfqO50O4U4C0d3cc-WWg4PhHysV4MXFnXYW8zhBZUdGT7oAbJc5OFXroyvJlsaAPNWnBT_9mllGMw-KmtOaIyp6013fv?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/hnEHjQWzhCOR636KIWuq2OPsueU0_sJr9V3_NQ1R1PM3PFjDhJRo7Eb8OB2hYKp0jq1pEQJm0w50YdF3t9a5ko43Hk9xaPSYqunUDsk0de80yc6jYoDN3aOSkroHDmnPMp5baxVHsxFm54GjyOKyYNzayY4YNaTNTIVt7yKrx87TWUhQjyoctGdDUBSm97ps?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Z6IAVriwMYlFtCW_VRSXfULBkKvaoRPXWkCP5yH5MYDS3P7XwexWKLYX_hn2dieDoY3xn8crZNgDhZrG1QEw7c2HgFsQD7PZcb_Uq_oej0uXFfxeI8qi3sX2K-0MK0BII0_Zm3zGrY9XB3t9XVxkUx6kKNocoBiMovc-yj-WbUryKIpPNC8gkTZXuVKeAZDT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yV7w14_QPf_mFxgYPOVSxC106DgOb8L-gVB5S5ZW6meisMB7jqVYcpcJKe1IuoP_LLBivCJ80uOYjuhZzB7sWbWiBiHerOkljaLi2blRxwvRi2Yg7nUoZZky5VkjQinJ0y2G1BAeZop8C_0ry8kt0uoVv3kwWUTZIymcBwns9LmkrqfyMJoPbXGZ20THECVk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/hZ-eOoG-SyazGd1O8yoBVvqxyxWO8KWvyrbzKuDOTH-v4uL7h_LaRDKn7Hwl1vwBwy4FnHWzBEPkLUGBj8wOwc61IBnQvSVaF2mETOgoV307GHMDxaV31XaoBmCOsMAFF_zFP12mgA5ABgy0DYf5SOexvU7DxaI0t9_PHEWdeXxz3B0KYbgNSlIRRFKHrpw-?purpose=fullsize)

Raspberry Pi è un **single-board computer (SBC)**, cioè un computer completo su una singola scheda.

![Image](https://images.openai.com/static-rsc-4/3S1ABFBPCXVK480EU-zfv7Uh8y3Qhg4jNKMQD68wetTWKKE3ebodQcYBi6eOM6cmnyTKvR-RkwcZp8z3UEnWDBDmtdaEgbnUiaAOFj_ufL0K-br6tc6dI5bjb920rvQsgi3VAspeijYtXKkXW9K0ARO7kMFoppaKzspg-B7CauIX9fkawwWFZwrvOYm_F_R2?purpose=fullsize){width=70%}


Include:

* CPU
* RAM
* storage (microSD)
* porte USB, rete, video

E soprattutto:

✔ esegue un sistema operativo (Linux)

---

## 2.2 Differenza rispetto a un PC

Dal punto di vista concettuale:

* Raspberry Pi è un PC

Ma con differenze:

* meno potente
* molto più piccolo
* consumo ridotto
* accesso diretto a pin hardware (GPIO)

---

## 2.3 Caratteristiche distintive di Raspberry Pi

Raspberry Pi è interessante perché unisce:

* mondo dei PC (software complesso)
* mondo embedded (interazione hardware)

Può:

* eseguire server web
* gestire database
* controllare sensori
* comunicare in rete

---

## 2.4 Quando è preferibile a un PC

Raspberry Pi è preferibile quando serve:

* un sistema sempre acceso
* basso consumo
* dimensioni ridotte
* integrazione con hardware

---

## 2.5 Casi d’uso tipici

* server web leggero
* sistemi IoT
* videosorveglianza
* gateway di rete
* automazione avanzata
* sistemi di controllo con interfaccia web

---

# LEZIONE 3 – Differenze tra Arduino e Raspberry Pi

## 3.1 Differenza concettuale fondamentale

Arduino:

* dispositivo di controllo
* orientato all’hardware

Raspberry Pi:

* computer completo
* orientato al software

---

## 3.2 Sistema operativo

Arduino:

* nessun sistema operativo
* esecuzione diretta del codice

Raspberry Pi:

* sistema operativo Linux
* multitasking

---

## 3.3 Tempo e determinismo

Arduino:

* comportamento deterministico
* ideale per real-time

Raspberry Pi:

* non deterministico
* il sistema operativo può introdurre ritardi

---

## 3.4 Interazione con hardware

Arduino:

* diretta
* precisa
* immediata

Raspberry Pi:

* mediata dal sistema operativo
* meno precisa nei tempi

---

## 3.5 Complessità

Arduino:

* semplice
* codice lineare

Raspberry Pi:

* complesso
* gestione OS, servizi, rete

---

## 3.6 Sintesi operativa

* Arduino   → controllo fisico diretto
* Raspberry → gestione logica e servizi

---

# LEZIONE 4 – Scelta e casi d’uso

## 4.1 Quando usare Arduino

Usare Arduino quando:

* si leggono sensori
* si controllano attuatori
* serve risposta immediata

Esempi:

* controllo temperatura
* gestione motori
* sistemi di sicurezza base

---

## 4.2 Quando usare Raspberry Pi

Usare Raspberry Pi quando:

* serve elaborazione dati
* serve rete
* serve interfaccia utente

Esempi:

* server web
* sistema di monitoraggio
* dashboard

---

## 4.3 Uso combinato (concetto chiave)

Molti sistemi reali usano entrambi.

Schema tipico:

```
Sensori → Arduino → Raspberry Pi → Server
```

Arduino:

* acquisisce dati

Raspberry:

* elabora
* invia in rete

---

## 4.4 Motivazione tecnica

Arduino:

* veloce nel controllo fisico

Raspberry:

* potente nell’elaborazione

Insieme:

✔ sistema completo ed efficiente

---

# LEZIONE 5 – Casi d’uso da esame

## 5.1 Monitoraggio sanitario (coerente con tracce reali)

Scenario:

* rilevazione parametri paziente

Soluzione:

* Arduino:

  * legge sensori (temperatura, battito)
* Raspberry:

  * invia dati al data-center

Motivazione:

* separazione acquisizione / comunicazione

---

## 5.2 Smart building

* Arduino:

  * controlla luci, sensori, porte
* Raspberry:

  * interfaccia web
  * log eventi

---

## 5.3 Sistema industriale

* Arduino:

  * controllo macchine
* Raspberry:

  * raccolta dati
  * analisi

---

## 5.4 Rete IoT distribuita

* molti nodi Arduino (sensori)
* Raspberry come gateway

---

## 5.5 Tipico errore da evitare (importante per esame)

Errore:

* usare Raspberry Pi per controllo real-time

Problema:

* il sistema operativo introduce ritardi

Soluzione corretta:

✔ usare Arduino per il controllo diretto

---

# CONCLUSIONE  

Arduino e Raspberry Pi non sono alternative equivalenti.

Sono strumenti diversi progettati per problemi diversi:

* Arduino → mondo fisico (tempo reale)
* Raspberry → mondo logico (software e rete)

La competenza richiesta nella traccia generalmente non è “saperli usare”, ma:  
✔ saper scegliere correttamente quale usare  
✔ saper giustificare la scelta  

---

# LEZIONE 6 – Connettività di rete: Arduino e Raspberry Pi

## 6.1 Concetto generale

Nei sistemi moderni (IoT, automazione, industria 4.0) la connettività di rete è fondamentale.

Permette di:

* trasmettere dati a server remoti
* integrare dispositivi in sistemi distribuiti
* gestire monitoraggio e controllo remoto

Differenza chiave:

* Arduino → **rete opzionale (moduli esterni)**
* Raspberry Pi → **rete nativa (integrata)**

---

## 6.2 Connettività di rete di Arduino

### Architettura

Arduino non include quasi mai connettività di rete integrata (eccezioni moderne a parte).

Serve quindi aggiungere moduli hardware.

---

### 6.2.1 Connessione Ethernet (rete cablata)

![Image](https://images.openai.com/static-rsc-4/wu9Mav2sr15bAzzQTSosX_5MlLB0ZE6dRMT_zcELgmuWpibejTNkV5qBVrULD1keeMSJ-GsjTWIXIFWd79TfAz1GH8Z3uHix0e78_ir1k0lpY8f59EwxW1AD4qGafgMesONQ-PSg3BCTDdR_1oeX6nCsGbaSA0wh4Cxmwqz9CYv-H7Iyucy2GNlFhbbusKM-?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/aj7QVABNaboKeUN3VGQWDiIqBbLJjRYlm826ywEY1Ff_6nw0M1LV16ns9gl7ujFFLwfhuzKKMZDFIEV_BNWiID1y3BJybJ_-sPVYWLkJ8HJIhwZGuzMz1Qlf5yqKUTfz5pzkzyWe0Ex5deUmeNbV8soUI033bPZQOgxysxFYv0ItRQZI4nBhkjid06TleInO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Wb7eAYUkgGqznVqgbHv1rl2J4IxrOLxDilzzvu4Z3i2EHqkpmmVCk9iaSC1rnBIecGTsoe5SRtg0EYqQ9rn_owjmT8OSg-7qUP8weArq1hNeqTdX7XMUIHdWOK8TsUWeSvXd3wDT-Izq43ndBNWtE9dzy1p5bIOaasQnWfN2C6CCzNYzdFK4ISNwjbw2Dt9c?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/oB0QFcg8uFlpFUdO8G2cPk7JJ1vhvIbi4n34x252xz_X6x6s-zvU_mKeWwNddzd5Z3CXZ-93SDRdImEV_qagTuclKbnIMGJrnJlc_cppkdP1yWZZPm46ARStFYYEZd4ukzcq7ZrKsCf71gzrou6Iv6e2W8IB7u0eabosIEfZvqZiU0LB3o9QGbBAYl_Qoul2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/coX4JNE7wqVm2FaIDxtDxCoscZ0yE4vBnYsFHRIMHdXBnGxnO0d2h9tCgxz-z3jMsjoRZ95Po1IKtkUVTUGTV1jy5kL6KVNUbXy2ohMEBoPr_Poym_05X0qR1BohtQ6LZqAN8yYjP-EdhfNNK8iryRGceK3gXxS75O0FKpfaidun5lf86OAXtZ-XOxvqoCQe?purpose=fullsize)

Componenti utilizzati:

* **Ethernet Shield (W5100 / W5500)** → soluzione più stabile e diffusa
* moduli economici (ENC28J60) → meno performanti

Caratteristiche:

* connessione RJ45
* uso di protocollo TCP/IP
* librerie ufficiali Arduino (Ethernet.h)

Uso tipico:

* Arduino come **client HTTP**
* Arduino come **server web minimale**

Limiti:

* memoria molto ridotta
* gestione rete semplificata

---

### 6.2.2 Connessione Wi-Fi

![Image](https://images.openai.com/static-rsc-4/4y6NSHbOhO0R_YXJPmvOJqB8Ljx6kE27GO5CSNKNqBxoiT8FlDeyPv9vLpka5dw0DBh6ZSp_iTsvV9p_PLD2XKRz0izDBrLLWrgYKvdCoDC2CkR10AJJHHUBHH_1A15H6cCasZU2bX4T1mDwYWdfQkIRPgtvC-6z9vM9SGRyeNNRvzLiDb-y8j3lVgIESrFa?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/iZE6HgRCyV6AhmovHCgi6fnG6lTUbibG2awgieoCyP5GQrXpAcgL7QjmE8uqEhDSkoBAntlzMpNWtQc2DzwtpUQLxUOW4vyYv5FXdwrTCZjdUnUwHlvfKZxYF571wwDdY7X_gc3_JP0AZkZJbLVNzc8EkJpxswY4Ce8mpsUEwedTecv4mSYTGkwUyGkWjPHk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GOScVRUq5Si2I-SoWjLyh_gAOAkukFoDopso6N6P6BW7em-5GmQWkRpikA2GpQUj8_qG0LcZmPJanmT545IgVd2uN3cAseWV7Z-nGh_LXxyyEXK2Qd05enS7IbHb06gQhtGItGiRvzynJyueLfw_zrJ6miN9du042pOaQuV_BV89DkmwVBtzdsYLfbpFpPin?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_rDYTzdQiWYH6t76G72SXFDFr8jqUsl9qMlqCfLLRkWFN1CWDXwPKxUtSue4Ugq8MVk69Vu17JCU21SNqN1acui5VlBrMzTx2nXmRYzXoYdgKcRykpslH6aabmwMib57CB-JGM-wr_inJ8ERSFzyJpupfJzTyf-PiQf3L2wBeSEDxO9fZNRqHh65KQXdtIk9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/XwbmhJglnnXe0SwOb1uK3fYXQh1b8bS0RHOIcuEP3SPopau3XK-joFNMvElkWkggJxiDzNz6ax9aHBpqOZ7IBW02Zb8wW4jHrKF9p-m1s1ME6ihtipGXFib7YTP30Hy0NVPNMZYgakpDigoHR8y4DSu75_Xm3pZpB_cICbR6pohla29QBAtJiPkadULLdNNE?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/2AMQ8zdsDkP_STFHshYqFS-s_dNBV2UuhDygGCsvXTdEM-uBNKXmuiBNNrjnEdD-f89y08yARWPXPqAM2tN4INESlrhQOJuTNx9ptFxJTs4CkBa2CjQLo4gblm2H0bEkOYhpNfAQkLtFc7L-TPJdgahLETG3jIF2cr2qGF6o0OneZI6B7atOi5IogFD6SwlM?purpose=fullsize)

Soluzioni più diffuse oggi:

* moduli **ESP8266**
* moduli **ESP32** (molto più usati oggi)
* vecchi WiFi Shield (meno diffusi)

Osservazione importante:

Oggi spesso si evita Arduino + WiFi shield e si usa direttamente:

* ESP8266 o ESP32 → **microcontrollori con Wi-Fi integrato**

Caratteristiche:

* supporto TCP/IP completo
* supporto HTTP, MQTT
* basso costo

---

### 6.2.3 Altri protocolli di rete (IoT)

Arduino può usare anche:

* Bluetooth (HC-05, BLE)
* ZigBee (XBee)
* LoRa (reti a lungo raggio)

Uso tipico:

* sensori distribuiti
* reti IoT a basso consumo

---

### 6.2.4 Limiti tecnici di Arduino in rete

* RAM molto limitata (pochi KB)
* gestione connessioni semplificata
* difficoltà con protocolli complessi (HTTPS, TLS avanzato)

Conclusione:

Arduino è adatto a:

✔ inviare dati semplici
✔ ricevere comandi
❌ non adatto a fare da server complesso

---

## 6.3 Connettività di rete di Raspberry Pi

### Architettura

Raspberry Pi integra già tutto:

* porta Ethernet (nei modelli standard)
* Wi-Fi integrato (modelli recenti)
* Bluetooth

---

### 6.3.1 Connessione Ethernet

![Image](https://images.openai.com/static-rsc-4/y6QDbuDuk_lZfYBQR_q3S0_pG7saDpkrz9F2J5NSYFCAP3b3ekVH2fgsHrAzhOIzctdZYDhmu3i7on6seNtx5H5eE9t9tsVU4PugTyv3OhyM2CoOPJswmSh-NQxGZDKtUz5_xwsNVIbXjN0eSm_kL4m_jZfrCUqcscnYH7lcfgJzPabY19Wk0A7URdkiDqef?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/BnyCDT9ZHraH6rV76p8cOjbuliXCedlnQDVeiY_KHe-Eq0ciBWl6gCBm3etR-uzNUZgMMUkAlSWJ4ek0If_u9ymSAftGz6uh4_DSBoYMptdF6Z030o4j6yU-wUOTEDUNTHqc0AOqRvnUu-6da3pIUeRPHaTq3staQAgUHvZoiGY8F2shNu9L5DoWHp3pPHlW?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_fqHwErCFeYb6523eEXs7CI6vpnkquL8b4GP2ndO86mgizAPVEZiYdOkwW4mai4YGIVz8gpQuu-SY6AvSdYUJS3whgkxjFvVjmAmk_BKriIEs2mqZQQZVzRH8o87jv6gAO5e5oXkjry2Vq-gNmLAFZ6GfKARebWP9OwVvI800L7r1PoYS6eo-ZQWj9gWaHsD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/kppFXthYAJXcTtpavBtEAD3P9iJr74PAogN0ejJNqguWvtLKczBri4LCkrVd5e5750FlZ6odOT3PdGeZpH2wCU_Xcan4MfsXAQhnYI-zN6OK2ZWYzY9rKqknlgveLSBVZkvkPd0QFP7oCgS-Jsr0ZXk8nAQgstuHSAR-HZbS-SeGRE0fVgBkepIJkR8_ZW3q?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/cdYNmwk0c-AlJt2fhHr7sT2Vkh8dsUUa3UTfWwxnS3Wch3EiUjE0fMdnVa_XT1TvahMIDAy5Tmlct9taRz4pRq1eRI0Pvc3DnMIyEX5-ZL2zeLa1OUcMkfWzgKhxcnN6EHNHIexC1Rest3dF4f8SwnaYNP0UoGojiz4HsvRLYxDWxbLpUM4jCNtgD8GIpZY1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3Wtp_7x8s-T8lIAMqMCjuqGSSN302JZyBPxx9DR4fBjpXFD1SKfmA36DKFg4ZHa3h_6QfA0pqzBBMsm3ZSU0VZ7hQbrB-A99J2PAraUu_oyUHEKeh0xcZZFKQ7APN0kqwGUhSX1PxIjhHv9D29piWeanx7Leh2KAv_FUnc-EloEYuujAS3rlZStz1x8NfqL-?purpose=fullsize)

Caratteristiche:

* interfaccia di rete completa
* supporto nativo Linux
* configurazione tramite:

  ifconfig
  ip addr
  dhclient

Uso:

* server web (Apache, Nginx)
* gateway di rete
* nodo di rete stabile

---

### 6.3.2 Connessione Wi-Fi

![Image](https://images.openai.com/static-rsc-4/tDmwzaINRNOa0s8SVCJiP0dYZJH-FCbyz1GcqCLXkmSvwx3dgRy7w-hXidhInHL48xJf1tTwHsM4jik3aTtWb2QkxkjwicLbOPUdnySijUXAo_PceqLy7uVnXl8qByQi5Z4VvshoTI9GhTpmqix3OA69YM_TZ4yMYpyW_0xwMf4T0JZ0iam0HgHAyxLRr16u?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Lxm6qHFf6YCdj6wTnYO0sHG9DNp36tBOPhrZQuQ3OUQey2qPHC3xRko8Ps7cMB7Gz9r8HdomFYl-oX2uLNzwhs23ZnqA8r-EnUWN5E766t9opp2VITHgPdRDkwRNa2D5t9iYBkRyQ45GNtIWGqtxMU7pNqY_Nk2GpNeFB7sr7hdc50lnxN-UKO0k_TWBarMF?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/-Dpu4jbEQG8vnwRfrgpjdem0BySd5ZjnJML8rKgGxevnyL4n4x5ZNcvmWMO2UZTv-qvGYAHC8WGYqwLVDETuFQnwgskFHup5OgsljLtTfSSLU9w8D0pTmvBM3-U7A1_7Uuc1M_xl0ieELuPct1kObSnvanJSJXqDho4c97frdROMir8sJi-ppLODp21urkVv?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/O8zfoRdLoIr4Up9pXNwfRD_xWwAKJzOMDUMQtKzZhxoWtjsojJttTzMKVuJdMpLP7yvcpPHB-UXyo2dSEKo1nG2eWJq_f2hqshJuR6rfHuPABnJM9xqrfq7MOBbl7pAKo6agzrRIjkbCW7PNhL-DNLLsERuM4O0ZIL_q3mpznMQeJeyyyTcy9_9h1ki1_omP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/xb24jHS2itNwKvYMF4bgqRcIyHMc_0C0RQcAPxRcnAh4MHMIclvt4WYrqVvnBGTdMma_4gtvnCq0P7r3nI27OV9WNEsVM_QI-PV88J7cm453WvizG-qSDY7Bc5QCtzoC3efY2FBYwM9D3qwBc-VQMqCwvEw8helIxrmXw79bQUhJ6maHEr4xKv83RHkcsk6f?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/d7t2cE5b5YYH69j8XwzAxL9PTN7964c2Xiv0MaPrFC5nQYz6Vi7dR6dJzSwA6tcDKhDROKVLIfqrsxTi9JZ8P8NZZj87HExttbyhzv5f1ykIF8NAXQVrSX4fxBmvbB004ZtzWJioyoLaCC4MZep2qYZiIbSSW3yHViAdSwa1F8ou7h7PEDfge8BmCfYCnqqW?purpose=fullsize)

Caratteristiche:

* Wi-Fi integrato (Raspberry Pi 3 e successivi)
* configurazione tramite:

  /etc/wpa_supplicant/wpa_supplicant.conf

Supporto completo:

* DHCP
* DNS
* routing
* VPN

---

### 6.3.3 Capacità avanzate di rete

Raspberry Pi può funzionare come:

* server web completo
* server database (MySQL, PostgreSQL)
* reverse proxy
* firewall (iptables, nftables)
* gateway IoT
* broker MQTT (Mosquitto)

Questo è possibile perché:

✔ esegue Linux
✔ ha stack TCP/IP completo

---

## 6.4 Confronto rete Arduino vs Raspberry Pi

| Caratteristica        | Arduino        | Raspberry Pi |
| --------------------- | -------------- | ------------ |
| Rete integrata        | No (di base)   | Sì           |
| Complessità rete      | Bassa          | Alta         |
| Protocollo supportati | Limitati       | Completi     |
| Server web            | Molto semplice | Completo     |
| Sicurezza (HTTPS)     | Limitata       | Completa     |

Sintesi:

* Arduino → nodo semplice di rete
* Raspberry → nodo intelligente di rete

---

## 6.5 Architetture reali (fondamentale per esame)

### 6.5.1 Architettura IoT classica

```
[Sensori] → Arduino → Raspberry Pi → Internet → Cloud
```

Ruoli:

* Arduino:

  * acquisizione dati
  * invio via seriale / Wi-Fi

* Raspberry:

  * aggregazione dati
  * invio al cloud

---

### 6.5.2 Raspberry come gateway IoT

Funzioni:

* raccoglie dati da più Arduino
* normalizza i dati
* li invia a server remoto

Protocolli tipici:

* MQTT
* HTTP REST
* WebSocket

---

### 6.5.3 Caso reale da traccia d’esame

Scenario:

Sistema di monitoraggio ambientale distribuito.

Soluzione corretta:

* nodi periferici:

  * Arduino + sensori + Wi-Fi (ESP32)

* nodo centrale:

  * Raspberry Pi

Funzioni Raspberry:

* server MQTT
* database locale
* dashboard web

Motivazione tecnica:

✔ separazione livelli
✔ scalabilità
✔ affidabilità

---

## 6.6 Add-on più usati oggi (aggiornamento tecnologico)

Situazione attuale (importante):

NON è più comune usare:

❌ Arduino + shield Wi-Fi costosi

Si usa invece:

✔ ESP32 → microcontrollore con Wi-Fi integrato
✔ Raspberry Pi → nodo centrale

Quindi:

* ESP32 sta in parte sostituendo Arduino nei progetti di rete
* Arduino “classico” resta utile per controllo puro

---

## 6.7 Errori tipici nelle tracce d’esame

Errore 1:

* usare Arduino come server web complesso
  ❌ non ha risorse sufficienti

Errore 2:

* usare Raspberry per controllo real-time
  ❌ non deterministico

Errore 3:

* non separare acquisizione e rete
  ❌ architettura non scalabile

Soluzione corretta:

✔ Arduino/ESP → acquisizione
✔ Raspberry → rete e servizi

---

## 6.8 Sintesi operativa finale

Arduino:

* nodo periferico
* acquisizione dati
* comunicazione semplice

Raspberry Pi:

* nodo centrale
* gestione rete
* servizi avanzati

Sistema completo:

✔ sensori → microcontrollori → gateway → cloud

---

# INTEGRAZIONE ALLA CONCLUSIONE

La scelta tra Arduino e Raspberry Pi deve considerare anche la rete:

* Arduino → rete limitata, uso periferico
* Raspberry → rete completa, uso centrale

Nei sistemi reali:

✔ la rete è gestita dal Raspberry
✔ i dati sono prodotti da Arduino/ESP

La competenza richiesta all’esame è quindi:

✔ progettare correttamente l’architettura di rete
✔ scegliere il dispositivo in base al ruolo
✔ motivare tecnicamente la scelta
