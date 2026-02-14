
---

1. Switch Layer 2

---

Uno switch L2:

* inoltra frame in base agli indirizzi MAC
* non conosce gli indirizzi IP
* non fa routing
* separa domini di broadcast tramite VLAN

In questo caso, per comunicare tra VLAN diverse serve un router esterno oppure un firewall.

---

2. Switch Layer 3: cosa significa realmente

---

Uno switch Layer 3 integra funzioni di routing IP.

Tecnicamente può:

* avere interfacce IP (SVI – Switch Virtual Interface)
* mantenere una tabella di routing
* fare routing statico o dinamico (OSPF, talvolta BGP nei modelli avanzati)

Quindi può fare routing:

* tra VLAN (inter-VLAN routing)
* verso reti esterne (core, WAN, firewall)
* tra subnet diverse anche senza VLAN (caso meno frequente ma possibile)

---

3. Perché si dice spesso “tra VLAN”?

---

Perché nell’architettura aziendale tipica:

* ogni VLAN corrisponde a una subnet IP
* esempio:

  VLAN 10 → 192.168.10.0/24
  VLAN 20 → 192.168.20.0/24

Uno switch L3 crea un’interfaccia virtuale per ogni VLAN:

interface vlan 10
ip address 192.168.10.1/24

interface vlan 20
ip address 192.168.20.1/24

A questo punto lo switch può instradare il traffico tra le due subnet.

Questa è la funzione più comune e didatticamente rilevante, per questo si parla spesso di routing “tra VLAN”.

---

4. Può fare routing solo tra VLAN?

---

No.

Dipende dalla fascia del dispositivo.

Switch L3 “lite” (SMB):

* routing statico
* inter-VLAN
* niente routing WAN avanzato
* niente NAT

Switch L3 enterprise:

* routing dinamico (OSPF, talvolta BGP)
* ECMP
* policy-based routing
* VRF
* routing verso core o data center

In reti grandi lo switch L3 può essere:

* access layer
* distribution layer
* core layer

---

5. Perché spesso non sostituisce il router?

---

Perché normalmente:

* non fa NAT (funzione tipica del router/firewall)
* non è pensato per routing WAN
* non integra funzioni di sicurezza perimetrale avanzata
* non gestisce PPPoE / linee ISP

Quindi:

Switch L3 → routing interno ad alta velocità (LAN)
Router / Firewall → routing verso Internet o WAN

---

## Conclusione precisa

Dire che uno switch Layer 3 “gestisce routing IP tra VLAN” è corretto ma riduttivo.

Più corretto dire:

Uno switch Layer 3 può eseguire routing IP tra subnet interne (tipicamente associate a VLAN), e nei modelli più avanzati può svolgere anche funzioni di routing dinamico nell’infrastruttura LAN o di core.

Se interessa, si può approfondire la differenza architetturale tra:

* inter-VLAN routing su switch L3
* router-on-a-stick
* core switch vs edge router
* switch L3 vs firewall in architettura a tre livelli

In ambito aziendale queste distinzioni diventano fondamentali.
