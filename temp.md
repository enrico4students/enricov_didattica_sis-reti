

# Sottoreti, precisazione

**Si parla di sottoreti anche con CIDR**, ma il significato del termine  leggermente rispetto al modello classful.

Bisogna distinguere tre concetti **storici** diversi:

1. indirizzamento **classful**  
2. **subnetting** delle reti classful  
3. **CIDR e indirizzamento classless**   

---

# 1. Nel modello classful il concetto di sottorete è fondamentale

Nel modello IPv4 originale le reti erano divise in classi:

| Classe | Prefisso | Esempio     |
| ------ | -------- | ----------- |
| A      | /8       | 10.0.0.0    |
| B      | /16      | 172.16.0.0  |
| C      | /24      | 192.168.1.0 |

Qui esisteva una **rete “naturale”** definita dalla classe.

Esempio, rete classe C: 192.168.1.0 /24

Se si voleva dividere questa rete si **prendevano bit dalla parte host** per creare subnet.

Esempio: 192.168.1.0 /26 ottenendo ad esempio le sottoreti:  
192.168.1.0  
192.168.1.64  
192.168.1.128  
192.168.1.192  

Qui il termine **subnet** è letterale:

una **sottorete di una rete classe C**.

---

# 2. Con CIDR le classi non esistono più

Con l'introduzione di **Classless Inter-Domain Routing (CIDR)** RFC 4632 le classi A, B e C **non hanno più alcun significato operativo**. Gli indirizzi sono semplicemente:
rete + prefisso

esempio:  
10.10.20.0 /24  
172.16.8.0 /21  
192.168.100.0 /26  

Non esiste più una "rete madre" naturale.

---

# 3. Con CIDR la parola sottorete è ancora usata (ma in modo concettuale)

Nel linguaggio pratico degli amministratori di rete la parola **sottorete continua ad essere usata**, ma con un significato diverso. Ora significa semplicemente:

> una rete ottenuta dividendo un blocco di indirizzi più grande.

Esempio, si ha un blocco assegnato 10.0.0.0 /16, si fa la divisione interna:  
10.0.10.0 /24  
10.0.20.0 /24  
10.0.30.0 /24  

Queste vengono normalmente chiamate **sottoreti**, anche se tecnicamente sono solo **prefissi più specifici**.

---

# 4. Esempio reale

Supponiamo che un'azienda possieda: 10.0.0.0 /16  All'interno si definiscono reti per VLAN: 
VLAN 10 → 10.0.10.0 /24  
VLAN 20 → 10.0.20.0 /24  
VLAN 30 → 10.0.30.0 /24  

Formalmente:

* sono prefissi CIDR
* sono anche **sottoreti del blocco 10.0.0.0/16**

Entrambe le affermazioni sono corrette.

---

# 5. Differenza concettuale importante

Nel modello classful:

rete principale → definita dalla classe.

Nel modello CIDR:

rete principale → definita **solo dal prefisso scelto**.

Esempio:

10.0.0.0 /8
10.0.0.0 /16
10.0.0.0 /20

sono **tutte reti valide**.

Non esiste più una gerarchia imposta dal protocollo.

---

# 6. Linguaggio professionale

Nel lavoro quotidiano si usano ancora termini come: subnet, subnetting, subnet mask anche se dal punto di vista teorico CIDR li rende in parte ridondanti. Questo succede per **ragioni storiche e di chiarezza operativa**.
Un amministratore dirà normalmente: 
"questa VLAN usa la subnet 10.10.20.0/24"  
anche se tecnicamente sarebbe più preciso dire:  
"questa rete ha prefisso /24".  

---

# 7. Sintesi

Una formulazione chiara e moderna può essere:

Nel modello IPv4 attuale (CIDR) una rete è definita da un **prefisso**.
Quando si divide un blocco di indirizzi più grande in reti più piccole si parla ancora comunemente di **sottoreti**, anche se non esiste più una rete “di classe” da cui derivano.

---

# 8. Conclusione

Non è corretto dire che il concetto di sottorete esiste solo nel classful addressing.  
È corretto dire che:
* nel modello classful le subnet derivano dalle classi
* nel modello CIDR le subnet sono semplicemente **prefissi più specifici all'interno di un blocco di indirizzi**

---

## Alcuni riferimenti

RFC 4632 – Classless Inter-Domain Routing (CIDR)
[https://datatracker.ietf.org/doc/html/rfc4632](https://datatracker.ietf.org/doc/html/rfc4632)

Cisco – Introduction to CIDR
[https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html)

Cloudflare – What is CIDR
[https://www.cloudflare.com/learning/network-layer/what-is-cidr/](https://www.cloudflare.com/learning/network-layer/what-is-cidr/)


---

# Come si lavora realmente con i piani di indirizzamento nelle reti professionali

Nei libri di testo il subnetting viene spesso insegnato come esercizio matematico: si parte da una rete assegnata, si calcolano i bit di subnet e si ottengono sottoreti consecutive (ad esempio .0, .32, .64, .96 ecc.).

Questo approccio è utile per comprendere il funzionamento tecnico del protocollo IPv4, ma **non riflette completamente il modo in cui si progettano le reti nel mondo professionale**.

Nelle infrastrutture reali la progettazione degli indirizzi IP è guidata principalmente da criteri di **leggibilità, organizzazione e crescita futura**, più che dal puro calcolo sui bit.

---

## Obiettivi di un piano di indirizzamento professionale

Quando si progetta una rete aziendale si cercano soprattutto questi risultati:

* facilità di comprensione della rete
* facilità di troubleshooting
* possibilità di espansione futura
* coerenza con la struttura organizzativa
* possibilità di automatizzare configurazioni

Per questo motivo il piano di indirizzamento viene progettato **prima della configurazione dei dispositivi**, spesso insieme alla progettazione delle VLAN e della topologia di rete.

---

## Uso di indirizzi privati nelle reti interne

Nelle reti aziendali quasi sempre si utilizzano **indirizzi IPv4 privati**, definiti dallo standard:

RFC 1918

Questi indirizzi non sono instradabili su Internet e sono pensati proprio per reti interne.

Gli intervalli sono tre:

| Intervallo                    | Dimensione   |
| ----------------------------- | ------------ |
| 10.0.0.0 – 10.255.255.255     | molto grande |
| 172.16.0.0 – 172.31.255.255   | medio        |
| 192.168.0.0 – 192.168.255.255 | piccolo      |

Nella maggior parte delle aziende l’accesso a Internet avviene tramite **NAT sul firewall o sul router**, che traduce gli indirizzi privati in indirizzi pubblici.

---

## Quali indirizzi vengono scelti più spesso

Nel mondo professionale esistono alcune scelte molto comuni.

### Piccole reti (casa, piccoli uffici)

Molto diffuso:

192.168.1.0/24

oppure

192.168.0.0/24

Motivo:
molti router domestici sono già configurati così.

Controindicazione:
può creare problemi con VPN o reti interconnesse perché è **troppo comune**.

---

### Aziende medie

Molto frequente utilizzare blocchi della rete:

10.0.0.0/8

oppure una porzione come:

10.10.0.0/16
10.20.0.0/16

Motivo:

* spazio enorme
* facile da suddividere
* possibilità di creare molte sottoreti.

---

### Grandi organizzazioni

Spesso viene assegnato un **intero schema gerarchico**, ad esempio:

10.0.0.0/8

poi suddiviso in modo strutturato:

10.sede.rete.host

Esempio:

10.1.10.0/24 → sede Milano VLAN uffici
10.1.20.0/24 → sede Milano VLAN server
10.2.10.0/24 → sede Roma VLAN uffici

Questo permette di **capire immediatamente la funzione della rete guardando l'indirizzo IP**.

---

## Come vengono scelti gli indirizzi delle sottoreti

Nei libri di testo spesso si vede questo schema:

rete iniziale:
192.168.1.0 /24

sottoreti:

192.168.1.0
192.168.1.32
192.168.1.64
192.168.1.96

Questo è corretto dal punto di vista matematico, ma nella pratica **raramente si lavora così**.

Nel mondo reale si preferiscono schemi **più leggibili e regolari**.

---

## Numerazione leggibile delle reti

Molti amministratori di rete scelgono di far corrispondere il numero della rete al numero della VLAN o al reparto.

Esempio:

VLAN 10 → 10.10.10.0/24
VLAN 20 → 10.10.20.0/24
VLAN 30 → 10.10.30.0/24

Oppure:

VLAN 10 → 192.168.10.0/24
VLAN 20 → 192.168.20.0/24
VLAN 30 → 192.168.30.0/24

Questo consente di:

* riconoscere immediatamente la rete
* evitare confusione
* ridurre gli errori di configurazione.

In altre parole **si preferiscono incrementi di 10, 20, 30 ecc.** invece che incrementi matematici derivati dai bit.

---

## Un esempio realistico

Una piccola azienda con tre VLAN potrebbe usare:

VLAN 10 uffici
192.168.10.0/24

VLAN 20 server
192.168.20.0/24

VLAN 30 wifi ospiti
192.168.30.0/24

Gateway tipico:

192.168.10.1
192.168.20.1
192.168.30.1

Questo schema è estremamente leggibile.

---

## Lasciare spazio per la crescita

Un altro principio molto importante nella progettazione reale è **lasciare spazio per reti future**.

Esempio.

Invece di usare:

192.168.1.0
192.168.1.32
192.168.1.64

si preferisce:

192.168.10.0
192.168.20.0
192.168.30.0

così restano disponibili:

192.168.40.0
192.168.50.0
192.168.60.0

per future espansioni.

---

## Caveats professionali

Alcune scelte comuni dei professionisti.

Evitare reti troppo comuni come:

192.168.0.0/24
192.168.1.0/24

perché spesso causano problemi con VPN.

Separare sempre reti diverse tramite VLAN:

uffici
server
wifi ospiti
management
dispositivi IoT.

Usare sempre una struttura coerente nel tempo: cambiare schema di indirizzamento durante la crescita della rete può diventare molto costoso.

Documentare sempre il piano di indirizzamento in un documento di rete.

---

## Riassunto

L'approccio scolastico al subnetting serve per capire il funzionamento dei bit e delle maschere.

Nel lavoro reale invece si progettano i piani di indirizzamento privilegiando:

* leggibilità
* organizzazione
* espandibilità
* coerenza con VLAN e topologia

Per questo motivo nelle reti professionali è molto comune vedere schemi come:

192.168.10.0
192.168.20.0
192.168.30.0

oppure

10.10.10.0
10.10.20.0
10.10.30.0

anche se dal punto di vista matematico non sono la suddivisione "più compatta".

---

## Alcuni riferimenti

RFC 1918 – Address Allocation for Private Internets
[https://datatracker.ietf.org/doc/html/rfc1918](https://datatracker.ietf.org/doc/html/rfc1918)

Cisco – Private IP Addressing
[https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/13772-12.html](https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/13772-12.html)

Cloudflare – Private IP Addresses Explained
[https://www.cloudflare.com/learning/network-layer/what-is-a-private-ip-address/](https://www.cloudflare.com/learning/network-layer/what-is-a-private-ip-address/)
