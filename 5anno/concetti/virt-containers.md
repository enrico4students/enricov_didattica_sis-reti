---

# Virtualizzazione – Concetti Base **DRAFT!!!**  

---

## 1. Perché nasce la virtualizzazione

Un server fisico tradizionale esegue un solo sistema operativo e un numero limitato di applicazioni. 
Nelle infrastrutture moderne questo modello è inefficiente perché spesso l’hardware non viene utilizzato completamente: **CPU e RAM rimangono parzialmente inutilizzate**.

La virtualizzazione nasce per sfruttare meglio le risorse hardware, consentendo a un singolo server fisico di eseguire più sistemi operativi contemporaneamente in modo isolato (non sotto-utilizzando l'hardware "host" disponibile).  
*(Nasce anche per altri benefici, illustrati in seguito)*  

---

## 2. Che cos’è la virtualizzazione

La virtualizzazione **server** _(che NON è assolutamente l'unico tipo ma è il tipo piu' noto e semplice)_ è una tecnologia che permette di creare **macchine virtuali (VM)**, cioè computer simulati che funzionano come sistemi indipendenti ma condividono lo stesso hardware fisico.

Ogni macchina virtuale:

* ha un proprio sistema operativo
* dispone di CPU virtuale, RAM virtuale e disco virtuale
* è isolata dalle altre VM

Dal punto di vista del sistema operativo installato, la macchina virtuale si comporta come un normale computer.

---

## 3. Il ruolo dell’hypervisor

L’elemento centrale della virtualizzazione è l’hypervisor, cioè il software che gestisce la creazione e l’esecuzione delle macchine virtuali.

L’hypervisor:

* assegna CPU e RAM alle VM
* gestisce l’accesso al disco
* controlla la rete virtuale
* garantisce isolamento tra le macchine

Esiste piu' di una tipologia di hypervisor  

### Hypervisor di tipo 1 (bare-metal)

Sono installati direttamente sull’hardware fisico e sono utilizzati nei data center.

Prodotti diffusi:

* VMware ESXi
  [https://www.vmware.com/products/esxi-and-esx.html](https://www.vmware.com/products/esxi-and-esx.html)

* Microsoft Hyper-V
  [https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-overview](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-overview)

* KVM (Kernel-based Virtual Machine)
  [https://www.linux-kvm.org](https://www.linux-kvm.org)

---

### Hypervisor di tipo 2 (desktop/laboratorio)

Sono installati sopra un sistema operativo esistente e sono ideali per studio, test e sviluppo.

Prodotti di interesse per studenti:

* Oracle VirtualBox
  [https://www.virtualbox.org](https://www.virtualbox.org)

* VMware Workstation Player
  [https://www.vmware.com/products/workstation-player.html](https://www.vmware.com/products/workstation-player.html)

* Parallels Desktop (ambiente macOS)
  [https://www.parallels.com/products/desktop/](https://www.parallels.com/products/desktop/)

Utile per uso personale e didattico e in technical pre-sales.  

---

## 4. Come funziona in pratica

Il server fisico fornisce CPU, RAM, disco e rete. L’hypervisor crea uno strato intermedio che suddivide queste risorse tra più macchine virtuali.

Ad esempio, un server con 32 GB di RAM e 8 core CPU può ospitare più VM, ciascuna con una quota assegnata di memoria e processori virtuali.

Le risorse possono essere allocate in modo statico o dinamico.

---

## 5. Virtualizzazione vs hosting classico

### Hosting classico (server fisico dedicato)

In questo modello tradizionale **NON** abbiamo virtualizzaione:

* un’applicazione viene installata su un server fisico dedicato
* ogni server svolge un solo ruolo principale
* l’espansione richiede nuovo hardware

Questo approccio comporta:

* basso utilizzo medio delle risorse
* costi hardware elevati
* scarsa flessibilità

---

### Virtualizzazione in ambito aziendale e data center

Con la virtualizzazione:

* più server logici condividono lo stesso hardware
* è possibile creare o eliminare VM rapidamente
* è possibile migrare VM tra host fisici
* si riduce il numero totale di server fisici

In un data center moderno:

* pochi server fisici potenti ospitano molte VM
* si implementano cluster con alta disponibilità
* si automatizzano backup e replica

Questo modello migliora:

* efficienza energetica
* continuità operativa
* scalabilità

---

## 6. Vantaggi della virtualizzazione

La virtualizzazione consente:

* migliore utilizzo dell’hardware
* riduzione dei costi
* isolamento tra ambienti
* rapidità di provisioning
* facilità di backup e snapshot

Un vantaggio strategico è la migrazione live, cioè lo spostamento di una VM da un host a un altro senza interruzione del servizio.

---

## 7. Virtualizzazione e cloud

La virtualizzazione è la base tecnica del cloud computing.

I provider cloud utilizzano grandi cluster di server virtualizzati per offrire macchine virtuali su richiesta.

Esempi di servizi cloud basati su VM:

* Amazon EC2
  [https://aws.amazon.com/ec2/](https://aws.amazon.com/ec2/)

* Microsoft Azure Virtual Machines
  [https://azure.microsoft.com/en-us/products/virtual-machines](https://azure.microsoft.com/en-us/products/virtual-machines)

* Google Compute Engine
  [https://cloud.google.com/compute](https://cloud.google.com/compute)

Quando si crea una VM nel cloud, si sta utilizzando una macchina virtuale eseguita su un hypervisor in un data center remoto.

---

## 8. I container: concetti fondamentali

I container rappresentano un’evoluzione diversa rispetto alla virtualizzazione tradizionale.

Mentre una macchina virtuale virtualizza l’hardware e include un intero sistema operativo, un container virtualizza il sistema operativo a livello di kernel. Più container condividono lo stesso kernel del sistema host, ma rimangono isolati tra loro tramite meccanismi come namespace e cgroups (nel caso di Linux).

Un container contiene:

* applicazione
* librerie necessarie
* configurazione
* dipendenze

ma non include un sistema operativo completo.

Questo comporta:

* avvio molto più rapido rispetto a una VM
* consumo di memoria ridotto
* maggiore densità di applicazioni per server

Il limite principale è che i container devono essere compatibili con il kernel del sistema host, mentre le VM possono eseguire sistemi operativi completamente diversi.

Strumenti diffusi per i container:

* Docker
  [https://www.docker.com](https://www.docker.com)

* Kubernetes (orchestrazione di container)
  [https://kubernetes.io](https://kubernetes.io)

In ambito aziendale moderno, VM e container spesso convivono: le VM forniscono isolamento forte a livello infrastrutturale, mentre i container permettono distribuzione rapida e scalabile delle applicazioni.

---

## 9. Differenze tra VM e container e quando usarli

La differenza principale è il livello di virtualizzazione.

Le macchine virtuali virtualizzano l’hardware e includono un sistema operativo completo; i container virtualizzano il sistema operativo e condividono il kernel dell’host.

Di conseguenza:

* le VM offrono isolamento più forte
* i container sono più leggeri e rapidi da avviare
* le VM consumano più risorse
* i container permettono maggiore densità applicativa

Le VM sono preferibili quando:

* è necessario eseguire sistemi operativi diversi sullo stesso hardware
* è richiesto un isolamento forte tra ambienti
* si gestiscono infrastrutture tradizionali o legacy

I container sono preferibili quando:

* si sviluppano applicazioni moderne (microservizi)
* è richiesta elevata scalabilità
* servono avvii molto rapidi
* si vuole massimizzare la densità di applicazioni

Nei data center moderni il modello più comune è ibrido: VM per isolare e segmentare l’infrastruttura, container per distribuire applicazioni in modo agile e scalabile.


---  


## 10. Relazione tra virtualizzazione e hardware dei data center

Le tecnologie di virtualizzazione (VM e container) non richiedono un tipo di hardware specifico: possono funzionare su qualunque server compatibile con i sistemi operativi e gli hypervisor utilizzati. Tuttavia nei data center moderni si utilizzano quasi sempre **server progettati per infrastrutture ad alta densità e alta affidabilità**.

### Server rack

Il tipo di server più comune è il **rack server**.
Si tratta di server montati in armadi standard da 19 pollici chiamati rack.

Caratteristiche principali:

* installazione modulare nei rack
* alimentazioni ridondanti
* molte CPU core e grandi quantità di RAM
* molte interfacce di rete ad alta velocità

Un singolo rack server può ospitare decine o centinaia di macchine virtuali, a seconda delle risorse disponibili.

Questo è oggi il modello più diffuso nei data center.

---

### Blade server

Un’altra architettura diffusa è quella dei **blade server**.

In questo modello più server molto compatti (le *blade*) vengono inseriti in uno chassis comune che fornisce:

* alimentazione
* raffreddamento
* connettività di rete
* backplane interno

Ogni blade contiene CPU e RAM ma utilizza l’infrastruttura condivisa dello chassis.

Il vantaggio principale è **l’elevata densità di calcolo**, utile nei grandi data center.

---

### Server iperconvergenti

Negli ultimi anni si sono diffusi anche i sistemi **iperconvergenti (HCI – Hyper-Converged Infrastructure)**.

In questi sistemi ogni nodo server fornisce contemporaneamente:

* calcolo (CPU e RAM)
* storage distribuito
* virtualizzazione

Più nodi formano un cluster che esegue macchine virtuali e gestisce lo storage in modo distribuito.

Prodotti diffusi:

* VMware vSAN
  [https://www.vmware.com/products/vsan.html](https://www.vmware.com/products/vsan.html)

* Nutanix HCI
  [https://www.nutanix.com/platform](https://www.nutanix.com/platform)

---

### Hardware nei cloud provider

I grandi provider cloud utilizzano infrastrutture simili ma su scala molto più grande.

Nei data center di cloud pubblici si trovano:

* grandi cluster di **rack servers**
* storage distribuito
* reti ad alta velocità (10–100 Gbit o più)

Su questi server fisici vengono eseguiti hypervisor e piattaforme di orchestrazione che permettono di creare:

* macchine virtuali
* container
* servizi cloud.

---

### Sintesi

La virtualizzazione è principalmente **una tecnologia software**, ma per funzionare in modo efficiente richiede server potenti e affidabili.

Nella pratica le infrastrutture virtualizzate utilizzano soprattutto:

* rack servers (soluzione più comune)
* blade servers (alta densità)
* nodi iperconvergenti

su cui vengono eseguiti hypervisor e piattaforme di orchestrazione per VM e container.


---

## 11. Sintesi finale

La virtualizzazione permette di eseguire più sistemi operativi su un singolo hardware fisico tramite un hypervisor che assegna e isola le risorse.

Rispetto al modello tradizionale con server fisici dedicati, offre maggiore efficienza, flessibilità e scalabilità ed è il fondamento tecnico dei moderni data center e del cloud computing.

I container rappresentano un modello complementare, più leggero e orientato alla distribuzione applicativa, basato sulla condivisione del kernel anziché sulla virtualizzazione completa dell’hardware.
