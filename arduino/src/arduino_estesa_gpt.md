# Arduino – Corso completo dalle basi al livello intermedio

Destinatari: studenti 17 anni  
Prerequisiti: conoscenza C/C++  
Prerequisiti elettronica: nessuno

Obiettivo del corso:

- comprendere cosa è un microcontrollore
- comprendere come funziona una scheda Arduino
- imparare a collegare componenti elettronici
- leggere sensori
- controllare attuatori
- progettare piccoli sistemi automatici

------------------------------------------------

# 1 Introduzione ai sistemi embedded

Un sistema embedded è un computer integrato in un dispositivo fisico.

Esempi reali:

- robot
- automobile
- drone
- lavatrice
- termostato
- stampante 3D

Schema generale di funzionamento:

ambiente fisico
      |
      v
+------------+
|  sensori   |
+------------+
      |
      v
+----------------+
| microcontrollore|
+----------------+
      |
      v
+-------------+
| attuatori   |
+-------------+
      |
      v
ambiente fisico

------------------------------------------------

# 2 Cos'è Arduino

Arduino è una piattaforma composta da tre elementi:

hardware  
software  
librerie  

Hardware: scheda con microcontrollore  
Software: ambiente di sviluppo  
Librerie: codice per controllare dispositivi

Sito ufficiale

https://www.arduino.cc

------------------------------------------------

# 3 Arduino Uno

Arduino Uno è la scheda più diffusa.

Immagine reale della scheda:

https://upload.wikimedia.org/wikipedia/commons/3/38/Arduino_Uno_-_R3.jpg

------------------------------------------------

# 4 Componenti principali della scheda

## Microcontrollore

Il microcontrollore è il vero computer della scheda.

Arduino Uno usa:

ATmega328P

Immagine del chip:

https://upload.wikimedia.org/wikipedia/commons/7/72/Atmel_ATmega328P.jpg

Funzioni del microcontrollore:

- eseguire il programma
- controllare i pin
- gestire timer
- gestire comunicazioni

------------------------------------------------

## Oscillatore

L'oscillatore genera il clock del microcontrollore.

Frequenza:

16 MHz

Immagine:

https://upload.wikimedia.org/wikipedia/commons/3/3f/Crystal_oscillator.jpg

------------------------------------------------

## Regolatore di tensione

Stabilizza la tensione di alimentazione.

Immagine:

https://upload.wikimedia.org/wikipedia/commons/6/6b/Voltage_regulator_7805.jpg

------------------------------------------------

## Convertitore USB-seriale

Permette la comunicazione tra PC e microcontrollore.

------------------------------------------------

# 5 Pin Arduino

Arduino espone pin per collegare componenti.

## Pin digitali

Possono assumere due stati:

LOW = 0V  
HIGH = 5V

Diagramma logico:

HIGH ───────
LOW      ───────

Utilizzi tipici:

LED  
pulsanti  
relè

------------------------------------------------

## Pin analogici

Permettono di leggere tensioni variabili.

Arduino usa un convertitore ADC a 10 bit.

Valori possibili:

0 → 1023

Conversione:

0V → 0  
2.5V → circa 512  
5V → 1023

------------------------------------------------

# 6 Breadboard

La breadboard serve per costruire circuiti senza saldature.

Immagine:

https://upload.wikimedia.org/wikipedia/commons/4/4f/Breadboard.jpg

Struttura semplificata:

+ + + + + + + +
| | | | | | | |
+ + + + + + + +
| | | | | | | |

Le linee orizzontali sono collegate internamente.

------------------------------------------------

# 7 Componenti elettronici fondamentali

------------------------------------------------

## LED

LED significa Light Emitting Diode.

Produce luce quando attraversato da corrente.

Immagine:

https://upload.wikimedia.org/wikipedia/commons/0/05/LED_5mm.jpg

Il LED ha due terminali:

anodo (+)  
catodo (−)

------------------------------------------------

## Resistenza

Serve per limitare la corrente.

Immagine:

https://upload.wikimedia.org/wikipedia/commons/3/3b/Resistor.jpg

Unità di misura:

Ohm

------------------------------------------------

## Pulsante

Permette input manuale.

Immagine:

https://upload.wikimedia.org/wikipedia/commons/e/e5/Push_button_switch.jpg

------------------------------------------------

## Servomotore

Motore controllabile con precisione angolare.

Immagine:

https://upload.wikimedia.org/wikipedia/commons/3/3a/Servo_motor.jpg

------------------------------------------------

## Sensore ultrasuoni

Misura distanza tramite eco ultrasonico.

Immagine:

https://upload.wikimedia.org/wikipedia/commons/9/9b/HC-SR04.jpg

------------------------------------------------

# 8 Struttura di un programma Arduino

Ogni programma Arduino si chiama sketch.

Struttura minima:

void setup()
{

}

void loop()
{

}

setup()

viene eseguita una volta.

loop()

viene eseguita continuamente.

------------------------------------------------

# 9 Primo circuito – LED lampeggiante

Componenti:

Arduino  
LED  
resistenza 220Ω

Schema circuito:

pin13 ---- resistenza ---- LED ---- GND

Codice:

void setup()
{
    pinMode(13, OUTPUT);
}

void loop()
{
    digitalWrite(13, HIGH);
    delay(1000);

    digitalWrite(13, LOW);
    delay(1000);
}

------------------------------------------------

# 10 Lettura di un pulsante

Schema circuito:

5V ---- pulsante ---- pin2
          |
         10kΩ
          |
         GND

Codice:

int button = 2;
int led = 13;

void setup()
{
    pinMode(button, INPUT);
    pinMode(led, OUTPUT);
}

void loop()
{
    int state = digitalRead(button);

    if(state == HIGH)
        digitalWrite(led, HIGH);
    else
        digitalWrite(led, LOW);
}

------------------------------------------------

# 11 Sensore analogico

Fotoresistenza.

Immagine:

https://upload.wikimedia.org/wikipedia/commons/7/75/Photoresistor.jpg

Schema:

5V --- fotoresistenza --- A0 --- resistenza --- GND

Codice:

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    int luce = analogRead(A0);

    Serial.println(luce);
}

------------------------------------------------

# 12 PWM

PWM significa Pulse Width Modulation.

Permette di simulare segnali analogici.

Diagramma:

HIGH ██████      ██████
LOW      ██████

Codice:

analogWrite(9,128);

------------------------------------------------

# 13 Comunicazioni hardware

Arduino supporta tre protocolli principali.

Serial  
TX RX

I2C  
SDA SCL

SPI  
MOSI MISO SCK CS

------------------------------------------------

# 14 Versioni Arduino

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

------------------------------------------------

# 15 Simulazione

Simulatore Arduino

https://wokwi.com

Permette di testare circuiti senza hardware.

------------------------------------------------

# 16 Kit hardware consigliato

Arduino Uno  
breadboard  
LED  
resistenze  
pulsanti  
servo  
sensore distanza  
fotoresistenza  
display LCD

------------------------------------------------

# 17 Documentazione

https://docs.arduino.cc

https://www.arduino.cc/en/Tutorial/HomePage