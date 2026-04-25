# UNITÀ DIDATTICA

## Arduino e Raspberry Pi: sistemi embedded e sistemi general purpose

---

# LEZIONE 1 – Arduino

## 1.1 Che cos’è Arduino  

![Image](https://images.openai.com/static-rsc-4/Vz9aOSyg07-W442ezBVuiCqDdBriLz76GAhqYAJqooBfFS9fcUlkuBMQWy9fEyRUIC601f6KZIEYB1IeUZ1nLSkLmieiJnCT49-4rd_UC_Fgcnd2pO-IJ4rV22EI5GVabtxjwTMCOH2gnwaeBjbCG-1B_kN3zq1PEU04i6Ve7oFYZv2Dwpnvb2qJfI4CyyFz?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/7I_gOEb_usHdGKza9lVU1ZAmnLy7oMHtjVUn1jW5Xolqc8x7XG_IwuWcOVbriWgSyIYV98T37oVcODoDpdBqSskHOTFVWa525Trzs3i-U-KJ8qsFYl3NErzqlWGYqCHWy4sgAGZYYC_RbC7uQosDcQuVXLB-fu5OZydmarUhxSRtvWaKk4OzSxTGOkHlFWoI?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/VojsuUv2_N4QZ9Q67rvdlhbfphazXNfIhwWahGnH1I0N2giWs9O3F3rorOGQjBoZHyOOfjwzExsqQ8P9_FbueJ7MIYdmPONhjslUD0kr5l600y4ibSPZtlVf3V2I350Rm2r4HJol8JrlUMF05HJYrv2JRXqmafOHEZ2rbl1pQ672Stz2iN-OU8O7rCMsepy_?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_acg5B2Erfo0hLnlPRypxHN1ZCRsq2bUPLsV2cyxv6kKsBwhB3RoMllhEAgnACGgJf9FCZ8YU5vBg5qTx20jldkux2cfe9LfEm53gXPUAQkQDoQdWTvTq8ah6LmsSTMDKydPgcylQRU4ZqzVKjRN7L_8G_3IEYWEtg3wg-UqVqTSa8NOgZ9ACbOaMa1jjjOR?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/e0-9UlQX22q6tuOKcMpgj0OliggpeB1zgTO-PCkjBC7hjJt20J5ae2BZa15iWZ4Y7ItP2U0FR-ssTXeIMNkdGzrOoN-yu9ko7D-KS27Ng2_-H8EXl7NMrtY1LgBi4_6Mubn7S7ajWQPYY305ApunLIxQDUd0-6zTGnPP1SE3ph_I036A9_Cxf5RMd8q92w3k?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/RH1ohQWk1r8V_VPiGwIutfweRo5YGzRuzvUYPDc3OZAwTIYzLrFcv8ppXeH4bWtbjxkyQ11MjHf_1cRkSfrUxaT-xyb9CPtjvb2St4ThnbCGLDSBioHI1USWNOo_dtgZxI7cKbeq-M9MsgJVB_t39MvfCoZG6zdDrwvWbmqOYapy-6e3oUEQ4tZBMAtoOvP4?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Rn4W82_gJ3jU2lSJWFMb1XLjf9QeCcXwISRXqHyXpjZnfRqftZYssRKOkCa-5ihuyYPP4Myv859keLMAdxDbkjqebPwOWDto91Pa9R-o9KJnq_1oZyo5_n5NYQENSgiiVLlDkWrS_Il4shXDBxhP3EjRLqT01cfyTMcX-3vW4o0oYH5zkXNlgl1PYakbsNfU?purpose=fullsize)

Arduino non è un “mini computer”, ma una **scheda elettronica programmabile basata su microcontrollore**.

Un microcontrollore è un componente che integra:

* CPU
* memoria limitata
* periferiche di input/output

tutto nello stesso chip.

Questo significa che Arduino è progettato per:

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

* NON ha sistema operativo
* esegue un solo programma
* il programma gira in un ciclo continuo

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

## 1.3 Perché Arduino esiste (unicità)

Arduino è stato progettato per un problema preciso:

**controllare il mondo fisico in modo semplice e affidabile**

Caratteristiche chiave:

* accesso diretto ai pin (ingressi/uscite)
* gestione precisa del tempo (millisecondi, microsecondi)
* comportamento deterministico

Esempio:

* accendere un LED dopo esattamente 100 ms
* leggere un sensore ogni 10 ms

Un PC NON è adatto a questo:

* il sistema operativo introduce ritardi imprevedibili

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

![Image](https://images.openai.com/static-rsc-4/3S1ABFBPCXVK480EU-zfv7Uh8y3Qhg4jNKMQD68wetTWKKE3ebodQcYBi6eOM6cmnyTKvR-RkwcZp8z3UEnWDBDmtdaEgbnUiaAOFj_ufL0K-br6tc6dI5bjb920rvQsgi3VAspeijYtXKkXW9K0ARO7kMFoppaKzspg-B7CauIX9fkawwWFZwrvOYm_F_R2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/mebY_J_g48FbzXMvGkJjLZYVMtspRZvrTIg8A76oh1nXrGQza8hMIHAXsl_FxtIzK0grHSYHF66WINfRWSfYP21gM1UV7RsAcfd0vfqO50O4U4C0d3cc-WWg4PhHysV4MXFnXYW8zhBZUdGT7oAbJc5OFXroyvJlsaAPNWnBT_9mllGMw-KmtOaIyp6013fv?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/hnEHjQWzhCOR636KIWuq2OPsueU0_sJr9V3_NQ1R1PM3PFjDhJRo7Eb8OB2hYKp0jq1pEQJm0w50YdF3t9a5ko43Hk9xaPSYqunUDsk0de80yc6jYoDN3aOSkroHDmnPMp5baxVHsxFm54GjyOKyYNzayY4YNaTNTIVt7yKrx87TWUhQjyoctGdDUBSm97ps?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Z6IAVriwMYlFtCW_VRSXfULBkKvaoRPXWkCP5yH5MYDS3P7XwexWKLYX_hn2dieDoY3xn8crZNgDhZrG1QEw7c2HgFsQD7PZcb_Uq_oej0uXFfxeI8qi3sX2K-0MK0BII0_Zm3zGrY9XB3t9XVxkUx6kKNocoBiMovc-yj-WbUryKIpPNC8gkTZXuVKeAZDT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yV7w14_QPf_mFxgYPOVSxC106DgOb8L-gVB5S5ZW6meisMB7jqVYcpcJKe1IuoP_LLBivCJ80uOYjuhZzB7sWbWiBiHerOkljaLi2blRxwvRi2Yg7nUoZZky5VkjQinJ0y2G1BAeZop8C_0ry8kt0uoVv3kwWUTZIymcBwns9LmkrqfyMJoPbXGZ20THECVk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/hZ-eOoG-SyazGd1O8yoBVvqxyxWO8KWvyrbzKuDOTH-v4uL7h_LaRDKn7Hwl1vwBwy4FnHWzBEPkLUGBj8wOwc61IBnQvSVaF2mETOgoV307GHMDxaV31XaoBmCOsMAFF_zFP12mgA5ABgy0DYf5SOexvU7DxaI0t9_PHEWdeXxz3B0KYbgNSlIRRFKHrpw-?purpose=fullsize)

Raspberry Pi è un **single-board computer (SBC)**, cioè un computer completo su una singola scheda.

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

## 2.3 Unicità di Raspberry Pi

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

* Arduino → controllo fisico diretto
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

# CONCLUSIONE DIDATTICA

Arduino e Raspberry Pi non sono alternative equivalenti.

Sono strumenti diversi progettati per problemi diversi:

* Arduino → mondo fisico (tempo reale)
* Raspberry → mondo logico (software e rete)

La competenza richiesta nella traccia generalmente non è “saperli usare”, ma:  
✔ saper scegliere correttamente quale usare  
✔ saper giustificare la scelta  

