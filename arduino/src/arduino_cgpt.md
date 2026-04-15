Di seguito viene fornita **una lezione completa e strutturata in Markdown plain-text**.
Il testo può essere copiato direttamente in un file `arduino_corso_completo.md`.

La lezione è progettata pensando a:

* studenti **17 anni**
* conoscenza **C/C++**
* **zero elettronica**
* obiettivo **livello medio Arduino**
* forte integrazione **teoria + pratica**
* **diagrammi e immagini**
* **laboratori progressivi**

Le immagini usano URL pubblici stabili.

---

```markdown
# Arduino – Corso completo dalle basi al livello intermedio

Materiale didattico per studenti di informatica (17 anni)

Prerequisiti:
programmazione C/C++

Non sono richieste conoscenze di elettronica.

---

# 1. Introduzione: programmare il mondo fisico

Un normale programma su computer lavora con dati digitali.

Un sistema embedded invece interagisce con il mondo reale.

Esempio:

un sistema automatico per irrigazione.

Il sistema deve:

misurare umidità → decidere → attivare pompa.

Schema generale:

```

Ambiente
|
v
+---------+
| Sensore |
+---------+
|
v
+----------------+
| Microcontrollore|
|    Arduino     |
+----------------+
|
v
+-----------+
| Attuatore |
+-----------+
|
v
Ambiente

```

---

# 2. Che cos'è Arduino

Arduino è una piattaforma composta da:

hardware + software + librerie.

Hardware:

una scheda elettronica con un microcontrollore.

Software:

un ambiente di sviluppo.

Librerie:

codice già scritto per controllare dispositivi.

Sito ufficiale  
https://www.arduino.cc

---

# 3. Che cos'è un microcontrollore

Un microcontrollore è un computer miniaturizzato.

Contiene:

CPU  
RAM  
Flash memory  
porte input/output  
timer  
convertitori analogico/digitali

Diagramma interno:

```

+-----------------------------------+
|         Microcontrollore          |
|                                   |
|   CPU                             |
|                                   |
|   Flash memory  (programma)       |
|   RAM          (variabili)        |
|                                   |
|   Timer                           |
|   ADC (analog → digital)          |
|                                   |
|   GPIO pins                       |
|                                   |
+-----------------------------------+

```

Il microcontrollore più comune su Arduino Uno è:

ATmega328P.

---

# 4. La scheda Arduino Uno

Immagine:

https://upload.wikimedia.org/wikipedia/commons/3/38/Arduino_Uno_-_R3.jpg

Componenti principali:

microcontrollore  
porta USB  
regolatore di tensione  
pin digitali  
pin analogici  
clock

---

# 5. Tensione e corrente (minimo indispensabile)

Due concetti fondamentali:

tensione (Volt)  
corrente (Ampere)

Arduino lavora principalmente a:

5V

Questo significa che:

HIGH = 5V  
LOW = 0V

---

# 6. Pin digitali

I pin digitali possono assumere due stati:

LOW  
HIGH

Diagramma logico:

```

LOW  → 0V
HIGH → 5V

```

Utilizzi tipici:

LED  
pulsanti  
relè

---

# 7. Pin analogici

I pin analogici leggono tensioni variabili.

Arduino usa un convertitore ADC a 10 bit.

Questo significa che il valore letto è tra:

0 e 1023.

Conversione approssimativa:

```

0V     → 0
2.5V   → ~512
5V     → 1023

```

---

# 8. Breadboard

Una breadboard permette di costruire circuiti senza saldature.

Immagine:

https://upload.wikimedia.org/wikipedia/commons/4/4f/Breadboard.jpg

Struttura semplificata:

```

* * * * * * * * -

| | | | | | | | |

* * * * * * * * +
                | | | | | | | | |
* * * * * * * * -

```

Le linee orizzontali sono collegate internamente.

---

# 9. Arduino IDE

Ambiente di sviluppo ufficiale.

Download:

https://www.arduino.cc/en/software

Permette di:

scrivere codice  
compilare  
caricare programma

---

# 10. Struttura di un programma Arduino

Un programma Arduino si chiama sketch.

Struttura:

```

void setup()
{

}

void loop()
{

}

```

setup()

viene eseguita una sola volta.

loop()

viene eseguita continuamente.

---

# 11. Primo programma: LED lampeggiante

Componenti:

Arduino  
LED  
resistenza 220Ω

Schema:

```

Pin 13 ---- resistenza ---- LED ---- GND

```

Codice:

```

void setup()
{
pinMode(13, OUTPUT);
}

void loop()
{
digitalWrite(13, HIGH);
delay(1000);

```
digitalWrite(13, LOW);
delay(1000);
```

}

```

---

# 12. Resistenze

Una resistenza limita la corrente.

Il LED deve sempre avere una resistenza.

Altrimenti si brucia.

---

# 13. Lettura di un pulsante

Componenti:

pulsante  
resistenza 10kΩ  
LED

Schema:

```

5V ---- pulsante ---- pin2
|
10kΩ
|
GND

```

Codice:

```

const int button = 2;
const int led = 13;

void setup()
{
pinMode(button, INPUT);
pinMode(led, OUTPUT);
}

void loop()
{
int state = digitalRead(button);

```
if(state == HIGH)
    digitalWrite(led, HIGH);
else
    digitalWrite(led, LOW);
```

}

```

---

# 14. Sensori analogici

Molti sensori producono segnali analogici.

Esempio:

fotoresistenza.

Schema:

```

5V --- fotoresistenza --- A0 --- resistenza --- GND

```

Codice:

```

void setup()
{
Serial.begin(9600);
}

void loop()
{
int luce = analogRead(A0);

```
Serial.println(luce);

delay(200);
```

}

```

---

# 15. Comunicazione seriale

Arduino comunica con il computer tramite seriale.

Funzioni:

```

Serial.begin(9600);
Serial.print();
Serial.println();

```

Serve per:

debug  
visualizzazione dati.

---

# 16. PWM

PWM significa Pulse Width Modulation.

Permette di simulare un segnale analogico.

Diagramma:

```

HIGH ████      ████
LOW      ████

```

Codice:

```

analogWrite(9,128);

```

---

# 17. Servomotori

Un servo è un motore controllabile con precisione.

Collegamenti:

```

rosso  → 5V
marrone → GND
giallo → pin9

```

Codice:

```

#include <Servo.h>

Servo s;

void setup()
{
s.attach(9);
}

void loop()
{
s.write(0);
delay(1000);

```
s.write(90);
delay(1000);

s.write(180);
delay(1000);
```

}

```

---

# 18. Controllo motori

Un motore non può essere collegato direttamente ad Arduino.

Serve un transistor o un driver.

Schema concettuale:

```

Arduino → transistor → motore → alimentazione

```

---

# 19. Versioni di Arduino

Arduino Uno  
Arduino Nano  
Arduino Mega  
Arduino Due  
Arduino MKR  
Arduino Portenta

Arduino Nano:

https://upload.wikimedia.org/wikipedia/commons/3/3f/Arduino_Nano.jpg

Arduino Mega:

https://upload.wikimedia.org/wikipedia/commons/5/5a/Arduino_Mega_2560_R3.jpg

---

# 20. Comunicazione tra dispositivi

Tre protocolli fondamentali.

I2C

due fili:

SDA  
SCL

SPI

quattro fili:

MOSI  
MISO  
SCK  
CS

Seriale

TX  
RX

---

# 21. Laboratorio 1 – Semaforo

Componenti:

3 LED  
3 resistenze

Schema:

```

pin8  → rosso
pin9  → giallo
pin10 → verde

```

Codice:

```

void setup()
{
pinMode(8, OUTPUT);
pinMode(9, OUTPUT);
pinMode(10, OUTPUT);
}

void loop()
{
digitalWrite(10,HIGH);
delay(5000);
digitalWrite(10,LOW);

```
digitalWrite(9,HIGH);
delay(2000);
digitalWrite(9,LOW);

digitalWrite(8,HIGH);
delay(5000);
digitalWrite(8,LOW);
```

}

```

---

# 22. Laboratorio 2 – Sensore di distanza

Sensore ultrasuoni HC-SR04.

Schema:

```

VCC → 5V
GND → GND
Trig → pin9
Echo → pin10

```

---

# 23. Laboratorio 3 – Mini stazione meteo

Componenti:

sensore temperatura  
display  
Arduino

Il sistema legge temperatura e la mostra.

---

# 24. Errori comuni

LED senza resistenza  
GND non collegato  
motori collegati direttamente  
alimentazione sbagliata

---

# 25. Progetti Arduino possibili

robot autonomi  
domotica  
stazioni meteo  
allarmi  
stampanti 3D  
droni

---

# 26. Kit consigliato per studenti

Arduino Uno  
breadboard  
LED  
resistenze  
pulsanti  
servo  
sensore distanza  
fotoresistenza

---

# 27. Documentazione

Arduino official documentation  
https://docs.arduino.cc

Arduino tutorial  
https://www.arduino.cc/en/Tutorial/HomePage

```

---

Se si desidera fare un confronto davvero serio tra AI, nel prossimo passo posso anche generare:

1. **una versione ancora più didattica (40-50 pagine equivalenti)**
2. **diagrammi elettronici professionali stile manuale universitario**
3. **10 laboratori progressivi per un corso di 20 ore**
4. **un diagramma completo dell’architettura interna ATmega328**
5. **una simulazione Arduino con Wokwi per gli studenti**.
