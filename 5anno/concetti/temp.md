## Patch panel Ethernet

![Image](https://assets.tripplite.com/large-image/n062024kj-front-l.jpg)

![Image](https://infinity-cable-products.com/cdn/shop/products/cat6-24-port-patch-panel-close-up_1024x1024.jpg?v=1651519496)

![Image](https://i.sstatic.net/jXHI4.jpg)

![Image](https://m.media-amazon.com/images/S/aplus-media-library-service-media/b1ebf002-7274-43a8-beeb-90d3387984a0.__CR0%2C0%2C1940%2C1200_PT0_SX970_V1___.jpg)




Un **patch panel Ethernet** è un dispositivo passivo utilizzato negli armadi di rete per **terminare e organizzare i cavi Ethernet del cablaggio strutturato** di un edificio.


### Terminare

In ambito di cablaggio di rete, **terminare un cavo** significa collegare in modo stabile e definitivo i fili del cavo a un connettore o a un dispositivo.
Nel caso dei cavi Ethernet, la terminazione consiste nel collegare i singoli fili del cavo:

* ai contatti di una presa di rete
  oppure
* ai contatti di un patch panel

Questa operazione viene normalmente eseguita tramite sistemi chiamati **IDC (Insulation Displacement Contact)** o **punch-down**.

Il cavo Ethernet contiene **8 fili (4 coppie)**. Durante la terminazione questi fili vengono inseriti nei contatti metallici del patch panel seguendo uno schema standard di cablaggio (T568A oppure T568B).

Una volta terminato, il cavo diventa parte permanente dell’infrastruttura dell’edificio e non viene più scollegato.

---  

Il patch panel è installato normalmente in un **rack standard da 19 pollici** insieme ad altri dispositivi di rete come switch, router e firewall.

La sua funzione principale è quella di fornire un punto ordinato in cui arrivano tutti i cavi di rete provenienti dalle prese Ethernet delle varie stanze dell’edificio.

Da questo punto i collegamenti vengono poi effettuati verso gli switch o altri dispositivi tramite cavi più corti chiamati **patch cord**.

---


### Struttura di un patch panel Ethernet

Un patch panel Ethernet è un pannello metallico montabile su rack che contiene una serie di porte RJ45.

I modelli più comuni hanno:

* **24 porte RJ45**
* **48 porte RJ45**

Il dispositivo ha due lati con funzioni diverse.

### lato frontale

Il lato frontale contiene le **porte RJ45** visibili nel rack.

Qui vengono collegati i **patch cord** che portano il traffico verso gli switch di rete.

### lato posteriore

Sul lato posteriore si trovano i terminali IDC nei quali vengono inseriti i fili dei cavi Ethernet provenienti dalle stanze dell’edificio.

Ogni porta frontale è collegata internamente a uno di questi terminali.

---

### Come si inserisce in una rete

In un edificio con cablaggio strutturato ogni presa Ethernet è collegata con un cavo che arriva fino alla sala server o all’armadio di rete.

Questi cavi non vengono collegati direttamente allo switch.

Vengono invece terminati nel patch panel.

Il collegamento completo diventa quindi:

presa Ethernet nella stanza
→ cavo Ethernet nel muro
→ terminazione nel patch panel
→ patch cord
→ switch di rete

Questo sistema permette di separare chiaramente:

* il cablaggio **permanente** dell’edificio  
* i collegamenti **variabili** verso gli apparati di rete

---

### Differenza tra cavo strutturato e patch cord

Il cavo che arriva al patch panel fa parte del **cablaggio strutturato** dell’edificio.

Questo cablaggio è pensato per rimanere installato per molti anni.

Per questo motivo i cavi strutturati:

* non devono essere piegati o scollegati frequentemente
* vengono terminati nel patch panel

I collegamenti che invece possono cambiare frequentemente sono i **patch cord**, cioè cavi Ethernet corti che collegano il patch panel allo switch.

Se cambia la configurazione della rete è sufficiente spostare questi patch cord.

![](./imgs/)

---

### Posizione del patch panel nel rack

In un armadio di rete il patch panel è normalmente posizionato nella parte superiore del rack, mentre gli switch sono montati subito sotto.

Questo consente di usare patch cord molto corti e di mantenere il cablaggio ordinato.

Un esempio di disposizione tipica potrebbe essere:

patch panel 24 porte
patch panel 24 porte
switch 48 porte
router o firewall
UPS

In questo modo tutte le connessioni provenienti dalle stanze entrano nei patch panel e poi vengono distribuite agli switch.

---

### Numerazione ed etichettatura

Un elemento molto importante nell’uso dei patch panel è la **numerazione delle porte**.

Ogni porta del patch panel viene associata a una presa Ethernet nell’edificio.

Ad esempio:

porta 1 → ufficio 101
porta 2 → ufficio 102
porta 3 → sala riunioni

Questo permette agli amministratori di rete di identificare rapidamente la posizione fisica di ogni collegamento.

L’etichettatura è quindi una parte fondamentale della gestione del cablaggio.

---

### Vantaggi dell’uso di patch panel

L’utilizzo di patch panel è uno standard nelle infrastrutture di rete professionali perché offre diversi vantaggi.

Organizzazione del cablaggio
tutti i cavi arrivano in un punto ordinato

Maggiore flessibilità
è possibile cambiare rapidamente i collegamenti spostando i patch cord

Manutenzione più semplice
i guasti possono essere individuati più facilmente

Protezione degli apparati
gli switch non vengono collegati direttamente ai cavi permanenti dell’edificio

---

### Esempio pratico

Immaginare un edificio con 20 uffici, ciascuno con una presa Ethernet.

Tutti i cavi delle prese arrivano nella sala server e vengono terminati in un patch panel da 24 porte.

Per attivare la rete nell’ufficio 103 basta collegare con un patch cord:

porta 3 del patch panel
→ porta dello switch

Se un giorno l’ufficio cambia funzione, è sufficiente spostare il patch cord senza modificare il cablaggio dell’edificio.

---

### Alcuni riferimenti

Patch Panel – Wikipedia
[https://en.wikipedia.org/wiki/Patch_panel](https://en.wikipedia.org/wiki/Patch_panel)

Structured Cabling Basics – Cisco
[https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/10561-3.html](https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/10561-3.html)

Patch Panel vs Switch – FS
[https://www.fs.com/blog/patch-panel-vs-switch-understanding-their-role-in-the-network-7846.html](https://www.fs.com/blog/patch-panel-vs-switch-understanding-their-role-in-the-network-7846.html)

Structured Cabling Guide – RackSolutions
[https://www.racksolutions.com/news/blog/patch-panel/](https://www.racksolutions.com/news/blog/patch-panel/)
