### VLAN distribuite su più switch

#### Quanto è frequente questa situazione

In una rete reale è molto comune che dispositivi appartenenti alla stessa VLAN siano collegati a **switch diversi**.  
Questo accade perché nelle reti aziendali, scolastiche o alberghiere gli switch sono normalmente distribuiti in vari punti dell’edificio o del campus:  

* uno switch per piano
* uno switch per area (laboratori, uffici, reception, sale conferenze)
* uno switch di core o distribuzione che collega gli altri switch

In questi contesti può essere necessario che dispositivi collocati fisicamente in luoghi diversi facciano parte **della stessa rete logica**.

Esempi tipici:

* PC degli amministrativi distribuiti su più piani ma appartenenti alla stessa rete aziendale
* telefoni VoIP collegati a switch diversi ma appartenenti alla stessa VLAN voce
* access point Wi-Fi che devono appartenere alla stessa VLAN di gestione
* stampanti di reparto distribuite su vari uffici ma nella stessa subnet

In tutti questi casi la VLAN non è limitata a uno switch ma **si estende attraverso più switch della rete**.



Uno switch Ethernet tradizionale non trasmette informazioni sulla VLAN nei frame Ethernet. Se due switch fossero collegati con una porta normale (access port), il secondo switch non saprebbe **a quale VLAN appartiene il traffico ricevuto**, Il collegamento tra switch che deve trasportare più VLAN viene configurato come **trunk** secondo lo standard **IEEE 802.1Q**, che prevede l'inserimento nel frame Ethernet un campo chiamato **VLAN tag** che contiene:

* identificatore della VLAN (VLAN ID)
* informazioni di priorità


Quando PC1 invia un frame:

1. lo switch A identifica che il frame appartiene alla VLAN 10
2. sul trunk inserisce il **tag VLAN 10**
3. lo switch B riceve il frame
4. legge il tag VLAN 10
5. inoltra il frame verso le porte appartenenti alla VLAN 10

Per i due PC sembra quindi di trovarsi **nella stessa rete locale**, anche se sono collegati a switch diversi.

<img src="https://i.adroitacademy.com/blog/43604421.png" style="background-color: white; display: inline-block; padding: 10px;" width="50%" />

---

#### Configurazione tipica

Esempio di configurazione.

```
enable                         ! entra nella modalità privilegiata dello switch
configure terminal             ! entra nella modalità di configurazione globale

vlan 10                        ! crea la VLAN con identificatore 10
name amministrazione           ! assegna un nome descrittivo alla VLAN
exit                           ! torna alla modalità di configurazione globale

interface gig0/10              ! seleziona la porta fisica GigabitEthernet 0/10
switchport mode access         ! imposta la porta come access port (una sola VLAN)
switchport access vlan 10      ! assegna la porta alla VLAN 10
no shutdown                    ! abilita la porta se fosse amministrativamente disattivata
exit                           ! torna alla configurazione globale
```

Configurazione del collegamento tra due switch.

```
interface gig0/1               ! seleziona la porta che collega i due switch
switchport mode trunk          ! imposta la porta come trunk (trasporto di più VLAN)
switchport trunk allowed vlan 10,20,30   ! consente il passaggio delle VLAN 10, 20 e 30 sul trunk
no shutdown                    ! abilita la porta
```

Interpretazione operativa:

porta `gig0/10` → collega un PC e appartiene alla VLAN 10  
porta `gig0/1` → collega un altro switch e trasporta più VLAN tramite trunk 802.1Q  

Quando un frame proveniente dal PC entra nello switch:

* lo switch sa che la porta appartiene alla VLAN 10
* se il frame deve attraversare il trunk, lo switch inserisce il **tag VLAN 10**
* lo switch remoto legge il tag e inoltra il traffico alle porte della VLAN 10.

In questo modo dispositivi collegati a switch diversi possono comportarsi come se fossero nella **stessa rete locale**.

---

#### Vantaggi delle VLAN distribuite

Questa architettura permette di:
- separare logicamente le reti indipendentemente dalla posizione fisica  
- semplificare la gestione delle reti aziendali  
- mantenere la stessa subnet IP per dispositivi distribuiti nell’edificio  
- ridurre la necessità di routing interno  

---

#### Possibili problemi e limiti

Sebbene molto utilizzata, una VLAN distribuita su molti switch può introdurre alcune criticità.

**1. Dominio di broadcast esteso**

Una VLAN è un **broadcast domain**. Se la VLAN è distribuita su molti switch, i broadcast (ARP, DHCP, ecc.) attraversano tutta la rete. Questo può causare:

* traffico inutile
* riduzione delle prestazioni
* maggiore probabilità di tempeste di broadcast.

Per questo motivo nelle reti grandi si tende a **limitare l’estensione delle VLAN**.

---

**2. Maggiore complessità di configurazione**

Tutti gli switch coinvolti devono avere:

* la VLAN configurata
* trunk correttamente configurati
* eventuali VLAN consentite sul trunk

Un errore di configurazione può causare:

* perdita di connettività
* traffico che finisce nella VLAN sbagliata.

---

**3. Problemi di sicurezza**

Se un trunk è configurato in modo errato possono verificarsi problemi di sicurezza, ad esempio:

* VLAN hopping  
* accesso non autorizzato a reti interne.  

Per questo motivo spesso si applicano politiche come:

* limitare le VLAN consentite sul trunk  
* disabilitare trunk automatici.  

---

**4. Architetture moderne preferiscono VLAN locali**

In molte reti moderne si tende a progettare VLAN **più piccole e locali**, associate a specifiche aree della rete.

Il traffico tra VLAN viene poi gestito tramite **routing Layer 3** su switch di distribuzione o core.

Questo modello:

* riduce i domini di broadcast
* migliora la scalabilità
* semplifica il troubleshooting.

---

