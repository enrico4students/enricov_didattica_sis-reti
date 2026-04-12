Il **subnetting** è la tecnica con cui una rete IP viene suddivisa in **sottoreti logiche più piccole**, modificando la subnet mask (o il prefisso CIDR) per “prendere in prestito” bit dalla parte host e destinarli alla parte rete.

**Perché si fa**

* Ridurre il dominio di broadcast.
* Migliorare sicurezza e isolamento tra reparti o servizi.
* Ottimizzare l’uso degli indirizzi IP.
* Rendere più efficiente routing e gestione ACL/firewall.

**Come si fa**

* Partire da una rete (es. 192.168.1.0/24).
* Aumentare il prefisso (es. /26).
* Calcolare numero di sottoreti e host per sottorete.
* Assegnare ogni subnet a un’interfaccia di router o a una VLAN.
* Configurare gateway e routing tra le subnet.

**Come viene fatto normalmente nell’IT aziendale**

* Progettazione iniziale con piano di indirizzamento (spesso VLSM).
* Creazione di VLAN sugli switch.
* Associazione di ogni VLAN a una subnet IP.
* Routing tra subnet tramite router o switch Layer 3.
* Applicazione di ACL e policy di sicurezza tra le reti.
