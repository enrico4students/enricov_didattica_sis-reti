
### Il NGFW è “on-line”? Fa routing?

Nelle architetture enterprise reali il **Next Generation Firewall (NGFW)** è molto spesso **inline (on-line)**, cioè posizionato direttamente nel percorso del traffico tra reti o zone diverse.

Esistono due modalità principali di funzionamento.

#### 1. Routed mode (Layer 3)

In questa modalità il firewall:

* ha **indirizzi IP sulle interfacce**
* mantiene una **tabella di routing**
* può fare **routing tra WAN, LAN e DMZ**
* applica policy di sicurezza durante l’inoltro dei pacchetti.

Documentazione Palo Alto Networks:
[https://docs.paloaltonetworks.com/ngfw/networking/configure-interfaces/layer-3-interfaces/configure-layer-3-interfaces](https://docs.paloaltonetworks.com/ngfw/networking/configure-interfaces/layer-3-interfaces/configure-layer-3-interfaces)

In questo caso il firewall funziona **in modo simile a un router**, ma con capacità di sicurezza molto più avanzate.


#### 2. Transparent mode / Virtual Wire

In questa modalità il firewall è comunque **inline**, ma lavora in modo **trasparente**.

Il firewall:

* non partecipa al routing
* non assegna indirizzi IP alle interfacce del traffico
* analizza e filtra i pacchetti mentre attraversano il dispositivo.

Documentazione Palo Alto Networks:
[https://docs.paloaltonetworks.com/pan-os/11-0/pan-os-networking-admin/configure-interfaces/virtual-wire-interfaces](https://docs.paloaltonetworks.com/pan-os/11-0/pan-os-networking-admin/configure-interfaces/virtual-wire-interfaces)

Questo modello viene usato quando si vuole aggiungere sicurezza **senza modificare l’architettura IP esistente**.

---

#### Architettura enterprise realistica con NGFW

In molte reti aziendali moderne la struttura è simile alla seguente.

##### Schema logico (diagramma testuale)

```
Internet
   |
   |
Edge Router / ISP Router
   |
   | rete di transito
   |
NGFW (inline)
   |        \
   |         \
   |          DMZ
   |
rete interna di transito
   |
Core / Distribution Layer 3 switch
   |
   + VLAN utenti
   + VLAN server
   + VLAN VoIP
   + VLAN WiFi
   + VLAN management
```

Interpretazione:

* il **router edge** gestisce la connessione verso ISP o WAN
* il **NGFW è inline** e controlla il traffico tra zone
* il **NGFW può fare routing tra WAN, LAN e DMZ**
* il **core/distribution switch Layer 3** gestisce il routing tra VLAN interne.

---

# Diagramma PlantUML

```
@startuml

title Architettura enterprise con NGFW inline

left to right direction
skinparam linetype ortho

cloud "Internet" as NET

rectangle "Edge Router\n(ISP / WAN)" as ER
rectangle "NGFW\nSecurity + inspection\n(routed mode)" as FW
rectangle "DMZ\nWeb / reverse proxy\nmail gateway" as DMZ

package "Core / Distribution Layer 3" {

rectangle "SVI VLAN 10\nUtenti"
rectangle "SVI VLAN 20\nServer"
rectangle "SVI VLAN 30\nVoIP"
rectangle "SVI VLAN 40\nWiFi"

}

NET --> ER
ER --> FW
FW --> DMZ
FW --> "Core / Distribution Layer 3"

@enduml
```

---

