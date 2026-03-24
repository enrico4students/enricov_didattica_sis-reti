## Recupero rapido di Sistemi e Reti

Lezione essenziale: da IPv4 ai piani di indirizzamento VLSM

Obiettivo della lezione

Arrivare, nel minor tempo possibile, a capire e saper applicare questi concetti:

- struttura di un indirizzo IPv4
- differenza tra rete e host
- subnet mask e prefisso CIDR
- indirizzo di rete, broadcast e host utilizzabili
- classi IPv4 e loro significato storico
- subnetting
- VLSM
- progettazione di un piccolo piano di indirizzamento

La lezione è pensata per uno studente che deve recuperare rapidamente. 
Per questo motivo si parte dalle idee minime indispensabili e si procede passo passo.

## 1. Le prime potenze di 2

Le potenze di 2 servono continuamente nel subnetting e nel VLSM.

Tabella essenziale:

- 2^0 = 1
- 2^1 = 2
- 2^2 = 4
- 2^3 = 8
- 2^4 = 16
- 2^5 = 32
- 2^6 = 64
- 2^7 = 128
- 2^8 = 256
- 2^9 = 512
- 2^10 = 1024

Valori molto importanti da ricordare a memoria:

- 8 bit = 256 combinazioni
- 2 host bit danno 4 indirizzi totali
- 3 host bit danno 8 indirizzi totali
- 4 host bit danno 16 indirizzi totali
- 5 host bit danno 32 indirizzi totali
- 6 host bit danno 64 indirizzi totali
- 7 host bit danno 128 indirizzi totali
- 8 host bit danno 256 indirizzi totali

Negli esercizi sugli host utilizzabili si usa quasi sempre questa formula:

    host utilizzabili = 2^n - 2

Dove n è il numero di bit host.

Il meno 2 dipende dal fatto che in ogni sottorete ci sono due indirizzi speciali:

- indirizzo di rete
- indirizzo di broadcast

Se si vuole essere più precisi bisogna tenere conto del fatto che prendono un indirizzo IP anche
- router
- servers

## 2. Che cos'è un indirizzo IPv4

Un indirizzo IPv4 è formato da 32 bit.

Di solito viene scritto in notazione decimale puntata, cioè in 4 gruppi separati da un punto:

    200.69.96.0

Ogni gruppo è un ottetto, cioè 8 bit.

Quindi:

    1 ottetto = 8 bit
    4 ottetti = 32 bit

Ogni ottetto può valere da 0 a 255, perché con 8 bit si hanno 256 combinazioni.

Esempio:

    192.168.1.10

significa che i 32 bit sono stati spezzati in 4 gruppi da 8 bit ciascuno.

## 3. Parte rete e parte host

Un indirizzo IP non va letto come un numero qualsiasi. Va letto come:

- parte rete
- parte host

La subnet mask, o il prefisso CIDR, serve proprio a dire dove finisce la parte rete e dove inizia la parte host.

Esempio:

    192.168.1.10/24

Il /24 significa:

- i primi 24 bit sono la parte rete
- gli ultimi 8 bit sono la parte host

Dato che 24 + 8 = 32, l'indirizzo è completo.

## 4. Subnet mask e CIDR

La subnet mask è un numero che, in binario, contiene:

- tutti 1 nella parte rete
- tutti 0 nella parte host

Esempio:

    /24  corrisponde a 255.255.255.0

Perché:

    11111111.11111111.11111111.00000000

In decimale diventa:

    255.255.255.0

Altri prefissi importanti:

- /25 = 255.255.255.128
- /26 = 255.255.255.192
- /27 = 255.255.255.224
- /28 = 255.255.255.240
- /29 = 255.255.255.248
- /30 = 255.255.255.252

Questi prefissi sono i più usati negli esercizi di subnetting su reti di classe C.

## 5. Indirizzo di rete, broadcast e host

In ogni sottorete esistono sempre tre tipi di indirizzi:

1. indirizzo di rete
2. indirizzo di broadcast
3. indirizzi host utilizzabili

Esempio con rete:

    192.168.1.0/24

Qui:

- indirizzo di rete = 192.168.1.0
- broadcast = 192.168.1.255
- host utilizzabili = da 192.168.1.1 a 192.168.1.254

Regola fondamentale:

- il primo indirizzo della sottorete è l'indirizzo di rete
- l'ultimo indirizzo della sottorete è il broadcast
- gli indirizzi in mezzo sono assegnabili agli host

## 6. Come si calcolano gli host utilizzabili

Formula:

    host utilizzabili = 2^n - 2

Dove n è il numero di bit host.

Esempi:

### /24

- bit host = 8
- host totali = 2^8 = 256
- host utilizzabili = 256 - 2 = 254

### /26

- bit host = 6
- host totali = 2^6 = 64
- host utilizzabili = 64 - 2 = 62

### /27

- bit host = 5
- host totali = 2^5 = 32
- host utilizzabili = 32 - 2 = 30

### /30

- bit host = 2
- host totali = 2^2 = 4
- host utilizzabili = 4 - 2 = 2

La /30 è perfetta per collegamenti punto-punto tra router, perché servono solo 2 indirizzi utilizzabili.

## 7. Classi IPv4: a che cosa servono

Storicamente le reti IPv4 erano divise in classi.

Le principali:

- Classe A: primo ottetto da 1 a 126
- Classe B: primo ottetto da 128 a 191
- Classe C: primo ottetto da 192 a 223

Esempio:

    200.69.96.0

Il primo ottetto è 200, quindi è una rete di classe C.

Storicamente una classe C aveva maschera naturale:

    255.255.255.0
    cioè /24

Questo serve per capire il punto di partenza classful.

Attenzione però: negli esercizi moderni, molto spesso non basta il classful. Serve il subnetting, e spesso serve il VLSM.

## 8. Subnetting: dividere una rete in sottoreti

Il subnetting consiste nel prendere una rete e dividerla in reti più piccole.

Esempio di partenza:

    200.69.96.0/24

Questa rete ha 256 indirizzi totali e 254 host utilizzabili.

Se la si divide in sottoreti /26, si ottengono blocchi da 64 indirizzi ciascuno.

Le sottoreti /26 dentro una /24 sono:

- 200.69.96.0/26
- 200.69.96.64/26
- 200.69.96.128/26
- 200.69.96.192/26

Perché il salto è 64.

Il salto si calcola così:

    256 - valore dell'ottetto della mask

Per /26 la mask è 255.255.255.192.

Quindi:

    256 - 192 = 64

Per questo le sottoreti partono da:

- 0
- 64
- 128
- 192

## 9. Metodo pratico del salto

Questo è uno dei metodi più veloci per gli esercizi.

Se la mask è nel quarto ottetto, il salto si calcola così:

    salto = 256 - ultimo ottetto della subnet mask

Esempi:

### /25

Mask:

    255.255.255.128

Salto:

    256 - 128 = 128

Sottoreti:

- .0
- .128

### /26

Mask:

    255.255.255.192

Salto:

    256 - 192 = 64

Sottoreti:

- .0
- .64
- .128
- .192

### /27

Mask:

    255.255.255.224

Salto:

    256 - 224 = 32

Sottoreti:

- .0
- .32
- .64
- .96
- .128
- .160
- .192
- .224

### /28

Mask:

    255.255.255.240

Salto:

    256 - 240 = 16

Sottoreti:

- .0
- .16
- .32
- .48
- ...

### /30

Mask:

    255.255.255.252

Salto:

    256 - 252 = 4

Sottoreti:

- .0
- .4
- .8
- .12
- ...

## 10. Come trovare rete, broadcast e host di una sottorete

Esempio:

    200.69.96.64/26

Una /26 ha blocchi da 64 indirizzi.

Quindi questa sottorete va da:

    200.69.96.64
    fino a 200.69.96.127

Perciò:

- rete = 200.69.96.64
- broadcast = 200.69.96.127
- host utilizzabili = da 200.69.96.65 a 200.69.96.126

Altro esempio:

    200.69.96.128/27

Una /27 ha blocchi da 32 indirizzi.

Quindi questa sottorete va da:

    200.69.96.128
    fino a 200.69.96.159

Perciò:

- rete = 200.69.96.128
- broadcast = 200.69.96.159
- host utilizzabili = da 200.69.96.129 a 200.69.96.158

## 11. Che cos'è il gateway

Il gateway di una LAN è di solito l'indirizzo dell'interfaccia del router presente in quella LAN.

Negli esercizi il gateway viene spesso scelto come:

- primo host utilizzabile
oppure
- ultimo host utilizzabile

Esempio:

Rete:

    200.69.96.64/26

Host utilizzabili:

    200.69.96.65 - 200.69.96.126

Possibili scelte:

- gateway = 200.69.96.65
oppure
- gateway = 200.69.96.126

Se il testo non dice nulla, bisogna dichiarare l'ipotesi.

Negli esercizi scolastici si sceglie spesso il primo host utilizzabile.

## 12. Differenza tra FLSM e VLSM

Due concetti decisivi.

### FLSM

Fixed Length Subnet Mask.

Tutte le sottoreti hanno la stessa subnet mask.

Esempio:

- tutte /26
oppure
- tutte /27

È semplice, ma spreca indirizzi oppure può risultare insufficiente.

### VLSM

Variable Length Subnet Mask.

Le sottoreti possono avere maschere diverse.

Esempio:

- una LAN grande con /26
- una LAN media con /27
- un link router-router con /30

Questo permette di usare bene gli indirizzi disponibili.

VLSM è quasi sempre la scelta migliore quando le reti hanno dimensioni diverse.

## 13. Come scegliere la subnet giusta in base agli host richiesti

Metodo fondamentale.

Si parte dal numero di host richiesti e si cerca la più piccola sottorete che li contenga.

Tabella da sapere:

- /30 -> 2 host utilizzabili
- /29 -> 6 host utilizzabili
- /28 -> 14 host utilizzabili
- /27 -> 30 host utilizzabili
- /26 -> 62 host utilizzabili
- /25 -> 126 host utilizzabili
- /24 -> 254 host utilizzabili

Esempi:

- servono 2 host -> /30
- servono 5 host -> /29
- servono 12 host -> /28
- servono 20 host -> /27
- servono 40 host -> /26
- servono 50 host -> /26

Regola pratica:

Scegliere sempre la sottorete più piccola che basti.

## 14. Procedura generale per fare un piano VLSM

Questa è la procedura da seguire in qualunque esercizio.

### Passo 1. Elencare tutte le reti necessarie

Per esempio:

- LAN della sede A
- LAN della sede B
- LAN della sede C
- link router-router 1
- link router-router 2
- link router-router 3

### Passo 2. Per ogni rete, scrivere quanti host servono

Nelle LAN considerare anche il router se deve avere un indirizzo nella LAN.

### Passo 3. Ordinare le reti dalla più grande alla più piccola

Questo è essenziale nel VLSM.

Prima si assegnano gli spazi grandi, poi quelli piccoli.

### Passo 4. Scegliere per ogni rete il prefisso minimo sufficiente

Usare la tabella:

- 50 host -> /26
- 40 host -> /26
- 20 host -> /27
- 2 host -> /30

### Passo 5. Assegnare i blocchi in ordine, partendo dall'inizio della rete disponibile

Esempio di rete disponibile:

    200.69.96.0/24

Si assegna prima il blocco più grande, poi il successivo, e così via.

### Passo 6. Per ogni blocco trovare:

- rete
- broadcast
- range host
- eventuale gateway

## 15. Esercizio guidato molto semplice

Testo:

Una rete 192.168.1.0/24 deve essere divisa in 2 sottoreti uguali.

### Soluzione

Dividere in 2 sottoreti uguali significa usare 1 bit in più per le subnet.

Si passa quindi da:

    /24

a:

    /25

La /25 ha blocchi da 128 indirizzi.

Le due sottoreti sono:

- 192.168.1.0/25
- 192.168.1.128/25

Prima sottorete:

- rete = 192.168.1.0
- broadcast = 192.168.1.127
- host = 192.168.1.1 - 192.168.1.126

Seconda sottorete:

- rete = 192.168.1.128
- broadcast = 192.168.1.255
- host = 192.168.1.129 - 192.168.1.254

Commento:

Qui non serve VLSM perché le due sottoreti sono uguali.

## 16. Esercizio guidato sulle /26

Testo:

Data la rete 200.10.5.0/24, trovare tutte le sottoreti /26.

### Soluzione

Una /26 ha mask:

    255.255.255.192

Il salto è:

    256 - 192 = 64

Quindi le sottoreti sono:

- 200.10.5.0/26
- 200.10.5.64/26
- 200.10.5.128/26
- 200.10.5.192/26

Calcolare la prima:

- rete = 200.10.5.0
- broadcast = 200.10.5.63
- host = 200.10.5.1 - 200.10.5.62

Calcolare la seconda:

- rete = 200.10.5.64
- broadcast = 200.10.5.127
- host = 200.10.5.65 - 200.10.5.126

Commento:

Una /26 offre 62 host utilizzabili.

## 17. Esercizio guidato sulle /30

Testo:

Data la rete 10.0.0.0/24, assegnare le prime tre sottoreti /30 per tre link punto-punto.

### Soluzione

Una /30 ha mask:

    255.255.255.252

Salto:

    256 - 252 = 4

Le prime tre sottoreti sono:

- 10.0.0.0/30
- 10.0.0.4/30
- 10.0.0.8/30

Prima /30:

- rete = 10.0.0.0
- host = 10.0.0.1 e 10.0.0.2
- broadcast = 10.0.0.3

Seconda /30:

- rete = 10.0.0.4
- host = 10.0.0.5 e 10.0.0.6
- broadcast = 10.0.0.7

Terza /30:

- rete = 10.0.0.8
- host = 10.0.0.9 e 10.0.0.10
- broadcast = 10.0.0.11

Commento:

Le /30 si usano spesso per collegare due router.

## 18. Esercizio guidato VLSM semplice

Testo:

Si dispone della rete 192.168.10.0/24. Progettare tre reti:

- R1 con 50 host
- R2 con 20 host
- R3 con 10 host

### Soluzione

Passo 1. Ordinare dalla più grande alla più piccola

- R1 = 50 host
- R2 = 20 host
- R3 = 10 host

Passo 2. Scegliere le subnet minime

- 50 host -> /26 perché /27 arriva solo a 30
- 20 host -> /27 perché offre 30 host
- 10 host -> /28 perché offre 14 host

Passo 3. Assegnare i blocchi in ordine

R1:

    192.168.10.0/26

Questa rete va da .0 a .63

- rete = 192.168.10.0
- broadcast = 192.168.10.63
- host = 192.168.10.1 - 192.168.10.62

R2:

Il blocco successivo libero parte da .64

    192.168.10.64/27

Questa rete va da .64 a .95

- rete = 192.168.10.64
- broadcast = 192.168.10.95
- host = 192.168.10.65 - 192.168.10.94

R3:

Il blocco successivo libero parte da .96

    192.168.10.96/28

Questa rete va da .96 a .111

- rete = 192.168.10.96
- broadcast = 192.168.10.111
- host = 192.168.10.97 - 192.168.10.110

Commento:

Questo è VLSM, perché le tre reti hanno subnet mask diverse.

## 19. Esercizio guidato simile a quello iniziale

Testo semplificato:

Un'azienda ha tre sedi:

- S1 con 50 host
- S2 con 40 host
- S3 con 20 host

Le sedi devono essere collegate con tre link router-router. La rete disponibile è:

    200.69.96.0/24

### Passo 1. Elencare le reti necessarie

Servono:

- LAN S1
- LAN S2
- LAN S3
- link S1-S2
- link S1-S3
- link S2-S3

Totale: 6 reti

### Passo 2. Calcolare gli host richiesti

Se il router della sede ha un'interfaccia nella LAN, anche quell'interfaccia richiede un indirizzo.

Quindi:

- S1: 50 host più 1 gateway = 51
- S2: 40 host più 1 gateway = 41
- S3: 20 host più 1 gateway = 21
- ogni link punto-punto = 2 host

### Passo 3. Trovare la subnet minima per ciascuna rete

- 51 host -> /26
- 41 host -> /26
- 21 host -> /27
- 2 host -> /30
- 2 host -> /30
- 2 host -> /30

### Passo 4. Ordinare dalla più grande alla più piccola

Ordine:

- S1 -> /26
- S2 -> /26
- S3 -> /27
- link 1 -> /30
- link 2 -> /30
- link 3 -> /30

### Passo 5. Assegnare i blocchi

S1:

    200.69.96.0/26

Intervallo:

- rete = 200.69.96.0
- broadcast = 200.69.96.63
- host = 200.69.96.1 - 200.69.96.62

S2:

    200.69.96.64/26

Intervallo:

- rete = 200.69.96.64
- broadcast = 200.69.96.127
- host = 200.69.96.65 - 200.69.96.126

S3:

    200.69.96.128/27

Intervallo:

- rete = 200.69.96.128
- broadcast = 200.69.96.159
- host = 200.69.96.129 - 200.69.96.158

Link S1-S2:

    200.69.96.160/30

- rete = 200.69.96.160
- host = 200.69.96.161 - 200.69.96.162
- broadcast = 200.69.96.163

Link S1-S3:

    200.69.96.164/30

- rete = 200.69.96.164
- host = 200.69.96.165 - 200.69.96.166
- broadcast = 200.69.96.167

Link S2-S3:

    200.69.96.168/30

- rete = 200.69.96.168
- host = 200.69.96.169 - 200.69.96.170
- broadcast = 200.69.96.171

### Passo 6. Rispondere alle domande finali

Domanda 1. Scrivere l'indirizzo del terzo host della prima rete S1.

La rete S1 è:

    200.69.96.0/26

Gli host partono da:

- primo host = 200.69.96.1
- secondo host = 200.69.96.2
- terzo host = 200.69.96.3

Risposta:

    200.69.96.3

Domanda 2. Scrivere l'indirizzo del gateway della seconda rete S2.

La rete S2 è:

    200.69.96.64/26

Gli host vanno da:

    200.69.96.65 a 200.69.96.126

Se si sceglie il primo host come gateway, allora:

    gateway S2 = 200.69.96.65

Commento importante:

Il testo non specifica quale host debba essere il gateway. In una verifica conviene scrivere esplicitamente:

    si assume come gateway il primo host utile della sottorete

## 20. Perché questo esercizio non è risolvibile in modo classful puro

Se si usasse una sola subnet mask uguale per tutte le reti, ci sarebbero due problemi.

Con /26:

- ogni rete avrebbe 62 host utilizzabili, quindi le LAN andrebbero bene
- ma le sottoreti dentro una /24 sarebbero solo 4
- invece qui servono 6 reti

Con /27:

- le sottoreti sarebbero 8, quindi il numero di reti basterebbe
- ma ogni sottorete avrebbe solo 30 host utilizzabili
- quindi S1 e S2 non ci starebbero

Quindi il problema richiede VLSM, non classful puro.

## 21. Errori tipici da evitare

Errore 1. Dimenticare il router nella LAN.

Se il router deve avere un IP nella LAN, anche quell'interfaccia va contata.

Errore 2. Usare una /27 per 40 o 50 host.

Una /27 offre solo 30 host utilizzabili.

Errore 3. Dimenticare rete e broadcast.

Se una rete ha 32 indirizzi totali, quelli utilizzabili non sono 32 ma 30.

Errore 4. Assegnare blocchi senza rispettare i confini corretti.

Per esempio una /27 deve iniziare a multipli di 32 nell'ultimo ottetto:

- 0
- 32
- 64
- 96
- 128
- 160
- 192
- 224

Errore 5. Non ordinare le reti dalla più grande alla più piccola.

Nel VLSM questo porta facilmente a sprechi o a sovrapposizioni.

## 22. Mini schema mentale da usare in verifica

Quando compare un esercizio VLSM, procedere sempre così:

1. elencare tutte le reti da creare
2. contare gli host necessari per ciascuna
3. aggiungere il gateway nelle LAN se serve
4. ordinare dalla rete più grande alla più piccola
5. scegliere la subnet minima sufficiente
6. assegnare i blocchi partendo dal primo indirizzo libero
7. trovare rete, broadcast, host e gateway
8. rispondere alle domande finali del testo

## 23. Esercizi rapidi commentati

### Esercizio A

Rete disponibile:

    192.168.0.0/24

Servono due LAN:

- 60 host
- 20 host

Soluzione ragionata:

- 60 host -> /26 perché offre 62 host
- 20 host -> /27 perché offre 30 host

Assegnazione:

- LAN1 = 192.168.0.0/26
- LAN2 = 192.168.0.64/27

Commento:

La seconda rete parte da .64 perché la prima /26 occupa .0-.63.

### Esercizio B

Quanti host utilizzabili ha una /28?

Soluzione:

- bit host = 4
- 2^4 = 16 indirizzi totali
- 16 - 2 = 14 host utilizzabili

Risposta:

    14

### Esercizio C

Qual è il broadcast della rete 172.16.5.128/27?

Soluzione:

Una /27 ha blocchi da 32.

La rete che parte da .128 arriva a:

    128 + 31 = 159

Quindi:

- rete = 172.16.5.128
- broadcast = 172.16.5.159

### Esercizio D

Qual è il quarto host della rete 10.0.1.64/26?

Soluzione:

Gli host partono da:

- 10.0.1.65 primo host
- 10.0.1.66 secondo host
- 10.0.1.67 terzo host
- 10.0.1.68 quarto host

Risposta:

    10.0.1.68

## 24. Esercizi finali per allenamento

Esercizio 1.

Data la rete 192.168.50.0/24, creare:

- una LAN da 70 host
- una LAN da 25 host
- una LAN da 10 host

Suggerimento:

- 70 host -> /25
- 25 host -> /27
- 10 host -> /28

Esercizio 2.

Data la rete 10.1.0.0/24, trovare:

- la seconda sottorete /26
- il broadcast della seconda sottorete /26
- il primo host della seconda sottorete /26

Esercizio 3.

Data la rete 200.10.20.0/24, progettare:

- una LAN da 50 host
- una LAN da 30 host
- due link router-router

Suggerimento:

- 50 host -> /26
- 30 host -> /27
- link -> /30

## 25. Soluzioni sintetiche degli esercizi finali

### Soluzione esercizio 1

- LAN 70 host -> 192.168.50.0/25
- LAN 25 host -> 192.168.50.128/27
- LAN 10 host -> 192.168.50.160/28

### Soluzione esercizio 2

Le /26 sono:

- 10.1.0.0/26
- 10.1.0.64/26
- 10.1.0.128/26
- 10.1.0.192/26

Quindi:

- seconda sottorete = 10.1.0.64/26
- broadcast = 10.1.0.127
- primo host = 10.1.0.65

### Soluzione esercizio 3

Una possibile soluzione:

- LAN 50 host -> 200.10.20.0/26
- LAN 30 host -> 200.10.20.64/27
- link 1 -> 200.10.20.96/30
- link 2 -> 200.10.20.100/30

## 26. Ripasso finale in 10 righe

- IPv4 ha 32 bit, scritti in 4 ottetti.
- La subnet mask separa parte rete e parte host.
- In ogni sottorete esistono rete, broadcast e host utilizzabili.
- Gli host utilizzabili si calcolano con 2^n - 2.
- /26 offre 62 host, /27 offre 30, /28 offre 14, /30 offre 2.
- Il salto si calcola con 256 meno il valore dell'ottetto della mask.
- Il gateway è di solito il primo o l'ultimo host utile.
- FLSM usa una sola mask per tutte le sottoreti.
- VLSM usa mask diverse e sfrutta meglio gli indirizzi.
- Negli esercizi VLSM bisogna ordinare le reti dalla più grande alla più piccola.

## 27. Conclusione

Dopo questa lezione bisogna essere in grado di:

- riconoscere se un esercizio è classful, subnetting fisso oppure VLSM
- calcolare host, rete e broadcast di una sottorete
- scegliere il prefisso corretto in base agli host richiesti
- costruire un semplice piano di indirizzamento VLSM
- rispondere a domande come terzo host, gateway, broadcast, prima o seconda sottorete

Per recuperare davvero in fretta conviene fare subito, senza guardare la teoria, almeno questi tre esercizi:

- uno con sottoreti /26
- uno con sottoreti /27 e /30
- uno completo con VLSM su una /24
