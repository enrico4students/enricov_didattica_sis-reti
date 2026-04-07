---

# Server Rack e Server Blade

---

## 1. Overview

In un’azienda o in un data center possono essere presenti decine o centinaia di server.
Sorge quindi un problema organizzativo:
come disporre molte macchine in modo ordinato, sicuro, raffreddato e facilmente manutenibile?

La risposta è l’uso di strutture standardizzate chiamate **rack**, all’interno delle quali vengono installati server progettati appositamente.

---

## 2. Che cos’è un rack

<img src="https://www.penn-elcom.com/media/catalog/product/cache/6964484727c91d8a7ee1545fdc866f01/R/0/R08632MM-19_r0863-2mm-19-23meaq.jpg"
     alt="Rack 19 pollici"
     style="width:8cm; height:auto;">

Un **rack**  
non è un server, non elabora dati, è una struttura di supporto
è un armadio metallico standard largo 19 pollici, dotato di guide verticali forate.  
Serve per contenere in modo ordinato: 
* server
* switch
* firewall
* UPS
* apparati di rete

Il suo scopo è organizzare fisicamente l’infrastruttura IT e facilitarne manutenzione, cablaggio e raffreddamento.

---

## 3. Che cos’è un server rack-mount

Un **server rack-mount** è un server **progettato per essere inserito nel rack**, 
ha CPU, RAM, dischi, esegue sistemi operativi e applicazioni

Un server rack-mount ha alimentazione e raffreddamento autonomi: **ogni server possiede alimentatori e ventole propri**. Questo significa che ogni macchina è elettricamente e termicamente indipendente dalle altre presenti nello stesso rack.
Questa indipendenza è un vantaggio perché consente di spegnere o sostituire un server senza coinvolgere gli altri.

---

## 4. Le unità di altezza (U)

Per inserire apparati di produttori diversi nello stesso rack è necessario uno standard dimensionale.  
L’altezza nel rack non si misura in centimetri ma in **Unità Rack (U)**.

1 U = 1,75 pollici ≈ 4,445 cm.

Di conseguenza:
* un server 1U è alto circa 4,4 cm
* un server 2U è alto circa 8,9 cm
* un server 4U è alto circa 17,8 cm

<img src="https://upload.wikimedia.org/wikipedia/commons/2/28/Rackunit.svg"
     alt="Rack 19 pollici"
     style="width:8cm; height:auto;">

Questo sistema permette di sapere esattamente quanto spazio occuperà ogni apparato e quanti dispositivi potranno essere installati nello stesso rack.

---

## 5. Vantaggi e limiti del modello rack-mount

Un’infrastruttura basata su server rack-mount è flessibile perché ogni server è una macchina completa e indipendente.  
Se un server si guasta, il problema riguarda solo quell’unità.

Il costo iniziale è relativamente contenuto perché non è necessario acquistare un’infrastruttura condivisa: ogni server è un sistema completo.

Gli svantaggi emergono quando il numero di server cresce.  
Il cablaggio aumenta perché ogni server richiede almeno un cavo di alimentazione e uno o più cavi di rete. Se si hanno venti server, si hanno venti alimentazioni e numerose connessioni di rete separate. Anche lo spazio è meno ottimizzato perché ogni server replica alimentatori e sistemi di raffreddamento.

---

## 6. Che cos’è un server blade

Il modello blade nasce per aumentare densità ed efficienza nei grandi data center.

Un sistema blade è composto da:  
* uno **chassis**
* più **blade** (moduli server sottili)

Ogni blade contiene CPU e RAM, ma **utilizza l’infrastruttura comune dello chassis**.

Lo chassis fornisce in modo condiviso:  
- alimentazione elettrica centralizzata, 
- sistemi di raffreddamento con ventole ridondate, 
- connettività di rete tramite moduli I/O integrati
- un backplane interno ad alta velocità che collega le blade senza cablaggio esterno.

Lo chassis integra anche funzioni di gestione centralizzata, come 
- monitoraggio hardware,  
- controllo remoto di accensione e spegnimento,  
- aggiornamenti firmware e gestione delle risorse, 
- e in alcuni modelli può includere moduli storage condivisi o interfacce dirette verso SAN.


<img src="https://i.ebayimg.com/images/g/FkYAAOxyGxxSKdTM/s-l400.jpg"
     alt="Rack 19 pollici"
     style="width:10cm; height:auto;">


<img src="https://expresscomputersystems.com/cdn/shop/files/hpe-c7000-rear_400x.jpg?v=1694711396"
     alt="Rack 19 pollici"
     style="width:10cm; height:auto;">

---

## 7. Perché i blade riducono cablaggio e aumentano densità

Il cablaggio è ridotto perché le blade si collegano internamente allo chassis tramite backplane.  
Verso l’esterno partono poche connessioni aggregate, invece di una serie di cavi separati per ogni server.  

La densità è maggiore perché non si duplicano alimentatori e ventole per ogni macchina: queste componenti sono condivise nello chassis. Eliminando le parti ripetute si ottiene più potenza di calcolo nello stesso spazio fisico.

---

## 8. Vantaggi e limiti dei blade

I blade sono ideali quando lo spazio è costoso e il numero di server è elevato, perché permettono maggiore concentrazione di risorse e gestione centralizzata.

Il costo iniziale è elevato perché è necessario acquistare lo chassis prima delle singole blade.  
Inoltre esiste una maggiore dipendenza dall’infrastruttura comune: se lo chassis ha un problema grave, possono essere coinvolte più blade contemporaneamente.

---

## 9. Confronto diretto

| Aspetto                     | Rack-mount          | Blade             |
| --------------------------- | ------------------- | ----------------- |
| Struttura                   | Server indipendenti | Moduli in chassis |
| Alimentazione               | Per ogni server     | Condivisa         |
| Raffreddamento              | Per ogni server     | Condiviso         |
| Cablaggio                   | Elevato             | Ridotto           |
| Densità                     | Media               | Molto alta        |
| Investimento iniziale       | Più contenuto       | Più elevato       |
| Dipendenza infrastrutturale | Bassa               | Alta              |

---

## 10. Virtualizzazione: una VM può usare più blade?

Una macchina virtuale viene eseguita su un singolo host fisico, che può essere un server rack-mount o una blade. Questo avviene perché l’hypervisor assegna CPU e RAM locali alla macchina virtuale.

In un cluster è possibile migrare una VM da un nodo a un altro senza spegnimento, ma in ogni istante la VM è attiva su un solo server fisico. Più blade possono collaborare in sistemi distribuiti, ma non eseguono simultaneamente la stessa VM come singola entità hardware.

---

## 11. Sintesi

Il modello rack privilegia indipendenza e semplicità.
Il modello blade privilegia densità ed efficienza in ambienti di grandi dimensioni.

La differenza fondamentale è architetturale: nel rack ogni server è autonomo, nel blade l’infrastruttura è condivisa.
