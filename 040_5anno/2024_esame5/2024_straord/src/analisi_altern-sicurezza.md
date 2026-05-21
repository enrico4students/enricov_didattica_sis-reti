# 1. Core switch Layer 3 + ACL

Ogni reparto si trova in una VLAN/rete distinta.

Il routing **fra VLAN** viene eseguito da un core switch Layer 3 **ad alte prestazioni**.

Le ACL applicate alle interfacce VLAN o alle SVI controllano quali reparti possono accedere ai file server e ai servizi degli altri reparti.

Esempio:

* VLAN 10 → reparto A
* VLAN 20 → reparto B
* VLAN 30 → reparto C
* VLAN 40 → reparto D
* VLAN 50 → reparto E
* VLAN 60 → reparto F
* VLAN 100 → server/stampanti

ACL:

* A → solo FS-A e Printer-A
* B → solo FS-B e Printer-B
* D → accesso ai file server A/B/C
* E → accesso completo ai file server locali
* F → accesso solo al gestionale remoto

Il firewall perimetrale resta dedicato a:

* Internet;
* NAT;
* VPN;
* DMZ;
* IDS/IPS.

## Precisazione importante

Il routing inter-VLAN esiste praticamente sempre quando VLAN differenti devono comunicare.

La vera differenza architetturale NON è:

* presenza o assenza di routing inter-VLAN;

ma:

* dove avviene il routing;
* quale apparato lo esegue;
* quale livello di sicurezza viene applicato.

In questa soluzione:

* il routing inter-VLAN avviene sul core switch L3;
* le policy vengono implementate tramite ACL;
* il traffico interno NON attraversa un firewall interno dedicato.

Questa soluzione è molto diffusa perché:

* offre prestazioni elevate grazie al forwarding hardware ASIC  
*(Application-Specific Integrated Circuit, circuito integrato progettato per svolgere in hardware un insieme specifico di operazioni.)*
* riduce complessità;
* evita colli di bottiglia;
* mantiene comunque una buona segmentazione.

## Sicurezza

Molto buona.

Consente:

* segmentazione;
* deny-by-default;
* controllo granulare;
* riduzione movimento laterale.

## Semplicità

Media.

## Numero reti

Molte reti separate.

---

# 2. File server in VLAN/server network dedicate

I file server vengono posti in reti dedicate separate dalle reti utenti.

Esempio:

* utenti A → VLAN 10
* utenti B → VLAN 20
* file server A → VLAN 110
* file server B → VLAN 120

Il routing può essere eseguito:

* da core L3;
* oppure da firewall interno.

## Sicurezza

Molto alta.

Vantaggi:

* isolamento server;
* migliore containment;
* controllo granulare;
* riduzione movimento laterale.

## Semplicità

Media-bassa.

## Numero reti

Alto.

---

# 3. Firewall interno fra reparti

Il routing fra VLAN viene demandato a un firewall interno.

Le VLAN terminano sul firewall che:

* esegue routing;
* applica policy stateful;
* implementa eventuali funzioni NGFW.

Schema:

Utente → Firewall interno → Server

Anche in questo caso il routing inter-VLAN esiste, ma viene eseguito dal firewall anziché dal core switch L3.

Questa architettura consente:

* inspection Layer 7;
* IDS/IPS;
* application awareness;
* logging avanzato;
* controllo molto granulare.

## Sicurezza

Molto alta.

## Semplicità

Bassa.

Architettura più complessa.

Possibile collo di bottiglia.

La differenza fondamentale è:

-  sullo switch L3 il forwarding/routing interno è il compito principale dell’apparato
- sul firewall il forwarding è accompagnato da molte analisi di sicurezza più costose.  


##### Caso 1 — Core switch L3

Schema:

```text id="h8znhv"
PC -> Core L3 -> Server
```

Il core switch:

* guarda IP destinazione;
* consulta tabella routing;
* applica ACL;
* inoltra il pacchetto.

Tutto questo avviene normalmente:

* in hardware ASIC;
* tramite pipeline dedicate;
* con latenze minime.

Il traffico interno viene quindi gestito molto velocemente.

---

##### Caso 2 — Firewall interno

Schema:

```text id="v44dbd"
PC -> Firewall -> Server
```

Il firewall non si limita a:

* instradare;
* applicare ACL.

Spesso deve anche:

* mantenere stato connessioni;
* fare stateful inspection;
* controllare protocolli;
* identificare applicazioni;
* fare IDS/IPS;
* analizzare payload;
* controllare SSL/TLS;
* loggare eventi;
* applicare policy utente.

Queste operazioni sono molto più pesanti.

##### Differenza pratica

###### Switch L3

Operazione tipica:

```text id="vnlmcz"
"pacchetto TCP verso 10.24.100.10 porta 445?"
ACL -> consentito
inoltro
```

Decisione semplice e veloce.

---

###### Firewall NGFW

Operazione tipica:

```text id="g0w6d4"
"connessione SMB?"
"utente autenticato?"
"sessione valida?"
"firma malware?"
"traffico anomalo?"
"payload sospetto?"
"policy applicativa?"
```

Molta più elaborazione.

##### Conseguenza

###### Core L3

Può instradare enormi quantità di traffico interno.

Tipicamente:

* decine/centinaia di Gbps;
* milioni di pacchetti/sec.

Con latenze bassissime.

---

###### Firewall

Le prestazioni reali diminuiscono quando si attivano:

* IDS/IPS;
* DPI;
* SSL inspection;
* logging avanzato;
* antivirus;
* application control.

Molti firewall pubblicizzano:

```text id="bslvzc"
20 Gbps firewall throughput
```

ma magari:

```text id="0d4r3o"
2 Gbps con IPS attivo
1 Gbps con SSL inspection
```
##### Perché il problema emerge soprattutto nel traffico interno?

Perché il traffico interno può essere enorme.

Esempi nella traccia:

* trasferimenti progetti;
* accessi simultanei file server;
* backup;
* sincronizzazioni repository;
* testing QA.

Quindi:

```text id="jjr2ib"
molti PC <-> molti server
```

con throughput elevato e continuo.

##### Invece Internet spesso è più lento

Anche con fibra molto veloce:

```text id="f41m6d"
LAN interna = 10 Gbps
Internet = 1 Gbps
```

Quindi il firewall perimetrale spesso regge bene Internet ma NON necessariamente tutto il traffico LAN interno.

##### Perché quindi usare il firewall?

Perché offre sicurezza superiore.

Esempi:

* IDS/IPS;
* application awareness;
* controllo Layer 7;
* Zero Trust;
* inspection SSL;
* sandboxing.

Quindi il firewall sacrifica:

* semplicità;
* throughput;
* latenza;

in cambio di:

* sicurezza avanzata.

##### Architettura professionale tipica

Per questo nelle reti professionali spesso si fa:

###### Core L3

gestisce:

* routing interno;
* VLAN;
* ACL base;
* traffico ad alte prestazioni.

###### (Edge) Firewall

gestisce:

* Internet;
* VPN;
* DMZ;
* reti critiche;
* traffico sensibile.


##### In sintesi  

Il possibile collo di bottiglia NON deriva dal fatto che il firewall “fa routing”.

Deriva dal fatto che il firewall:

* oltre al routing;
* esegue molte analisi di sicurezza molto costose.

Mentre uno switch L3 ad alte prestazioni:

* fa soprattutto forwarding **hardware altamente ottimizzato**.


## Numero reti

Molte reti separate.

---

# 4. Rete unica senza segmentazione

Tutti i sistemi sono nella stessa LAN.

Gli accessi vengono controllati solo tramite autenticazione o permessi filesystem.

In questo caso il routing inter-VLAN non esiste perché non esistono VLAN separate.

## Sicurezza

Bassa.

Problemi:

* nessun isolamento;
* movimento laterale semplice;
* maggiore superficie d’attacco.

## Semplicità

Molto alta.

## Numero reti

Una sola rete.

---

# 5. Accesso tramite autenticazione applicativa solamente

Le reti possono comunicare liberamente ma i file server consentono accesso solo ad alcuni utenti/gruppi.

Esempio:

* Active Directory;
* gruppi utenti;
* permessi NTFS/share.

Può essere usato:

* con rete unica;
* oppure con VLAN separate.

## Sicurezza

Media.

Protegge i dati ma non segmenta realmente la rete.

## Semplicità

Alta.

## Numero reti

Variabile.

---

# 6. Jump server / bastion host

Gli utenti non accedono direttamente ai file server.

Accedono a un server intermedio autorizzato.

## Sicurezza

Alta.

Vantaggi:

* auditing;
* centralizzazione;
* riduzione esposizione.

## Semplicità

Bassa-media.

## Numero reti

Generalmente molte reti separate.

---

# 7. Accesso tramite servizi applicativi centralizzati

I file vengono gestiti tramite applicazioni:

* GitLab;
* SVN;
* document management;
* web application.

Gli utenti non accedono direttamente ai file server.

## Sicurezza

Molto alta.

Vantaggi:

* RBAC;
* auditing;
* MFA;
* niente accesso diretto filesystem.

## Semplicità

Media-bassa.

## Numero reti

Variabile.

---

# 8. VPN interna / microsegmentazione / Zero Trust

Ogni accesso fra reparti richiede autenticazione forte e policy specifiche.

## Sicurezza

Estremamente alta.

## Semplicità

Molto bassa.

## Numero reti

Molte reti/logical segments.

---

# 9. Unica VLAN server/stampanti + ACL

Tutti i file server e le stampanti vengono collocati in una VLAN server condivisa.

Le VLAN utenti accedono alla VLAN server tramite ACL/firewall.

Esempio:

* VLAN utenti A
* VLAN utenti B
* VLAN utenti C
* VLAN server condivisa

Nella VLAN server:

* FS-A
* FS-B
* FS-C
* Printer-A
* Printer-B
* Printer-C

Il routing può essere effettuato:

* dal core L3;
* oppure da firewall interno.

ACL:

* A → solo FS-A e Printer-A
* D → tutti i file server
* E → accesso completo

## Sicurezza

Buona.

Migliore della rete unica.

Inferiore alle VLAN server separate.

Problema principale:

* tutti i server condividono lo stesso dominio Layer 2.

## Semplicità

Alta.

Riduce:

* numero VLAN;
* complessità routing;
* numero ACL;
* troubleshooting.

## Numero reti

Medio-basso.

---

# Ranking basato SOLO sulla sicurezza

Dal più sicuro al meno sicuro.

| Posizione | Soluzione                                     |
| --------- | --------------------------------------------- |
| 1         | VPN interna / microsegmentazione / Zero Trust |
| 2         | Firewall interno fra reparti                  |
| 3         | File server in VLAN dedicate                  |
| 4         | Servizi applicativi centralizzati             |
| 5         | Core switch L3 + ACL                          |
| 6         | Jump server / bastion host                    |
| 7         | VLAN server condivisa + ACL                   |
| 8         | Autenticazione applicativa solamente          |
| 9         | Rete unica senza segmentazione                |

---

# Ranking basato SOLO sulla semplicità di implementazione e gestione

Dalla più semplice alla più complessa.

| Posizione | Soluzione                                     |
| --------- | --------------------------------------------- |
| 1         | Rete unica senza segmentazione                |
| 2         | Autenticazione applicativa solamente          |
| 3         | VLAN server condivisa + ACL                   |
| 4         | Core switch L3 + ACL                          |
| 5         | Jump server / bastion host                    |
| 6         | File server in VLAN dedicate                  |
| 7         | Servizi applicativi centralizzati             |
| 8         | Firewall interno fra reparti                  |
| 9         | VPN interna / microsegmentazione / Zero Trust |

---

# Ranking basato sul miglior compromesso sicurezza/semplicità

Dal miglior equilibrio al peggiore equilibrio.

| Posizione | Soluzione                                     |
| --------- | --------------------------------------------- |
| 1         | VLAN server condivisa + ACL                   |
| 2         | Core switch L3 + ACL                          |
| 3         | File server in VLAN dedicate                  |
| 4         | Servizi applicativi centralizzati             |
| 5         | Autenticazione applicativa solamente          |
| 6         | Firewall interno fra reparti                  |
| 7         | Jump server / bastion host                    |
| 8         | VPN interna / microsegmentazione / Zero Trust |
| 9         | Rete unica senza segmentazione                |

---

# Quale soluzione è probabilmente la migliore per questa prova?

Per una seconda prova di Sistemi e Reti:

## Miglior equilibrio realistico

* VLAN utenti separate;
* VLAN server condivisa;
* routing sul core switch Layer 3;
* ACL;
* autenticazione centralizzata.

Oppure:

* VLAN utenti separate;
* file server locali ai reparti;
* routing sul core switch L3;
* ACL.

Entrambe:

* realistiche;
* difendibili;
* implementabili;
* coerenti con il tempo della prova;
* sufficientemente professionali senza diventare eccessivamente enterprise.
