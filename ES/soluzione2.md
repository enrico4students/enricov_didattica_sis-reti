Sì. Ecco una soluzione più compatta, meno dispersiva e più simile a quella che potrebbe scrivere un bravo studente di quinta ITIS.

## Soluzione compatta

## Ipotesi iniziali

Si ipotizza che la società abbia una sede centrale con uffici tecnici e che debba gestire 2 o 3 cantieri contemporaneamente. Ogni cantiere dispone di tablet rugged, scanner 3D/LiDAR, fotocamere timelapse e sensori di sicurezza. Lo scopo della rete è permettere la raccolta dei dati in cantiere e il loro trasferimento sicuro verso la sede centrale, dove sono presenti i sistemi BIM.

## Prima parte

## 1. Rete da realizzare in cantiere

In ogni cantiere si prevede una rete locale temporanea composta da router/firewall, switch gestito, access point Wi-Fi, eventuale gateway per i sensori e collegamento Internet.

Schema generale:

```
Tablet / scanner / LiDAR
          |
        Wi-Fi
          |
    Access point
          |
    Switch gestito
          |
    Router / firewall
          |
    VPN verso sede centrale
```

Le fotocamere timelapse possono essere collegate via Wi-Fi o Ethernet, mentre i sensori possono comunicare tramite un gateway dedicato, che raccoglie i dati e li invia alla sede.

Per maggiore sicurezza si separano i dispositivi con VLAN:

```
VLAN 10 - tablet e strumenti BIM
VLAN 20 - fotocamere
VLAN 30 - sensori
VLAN 40 - gestione apparati
```

Esempio di indirizzamento per il cantiere 1:

```
rete cantiere: 10.10.1.0/24
tablet:        10.10.1.0/26
fotocamere:    10.10.1.64/26
sensori:       10.10.1.128/26
gestione:      10.10.1.192/27
```

Per gli altri cantieri si possono usare reti diverse, ad esempio 10.10.2.0/24 e 10.10.3.0/24.

I servizi principali sono DHCP per assegnare gli indirizzi IP, DNS per la risoluzione dei nomi, NTP per sincronizzare l’orario, HTTPS/SFTP per trasferire dati in modo sicuro e VPN per collegare il cantiere alla sede.

La rete Wi-Fi deve essere protetta con WPA2/WPA3. Il firewall deve consentire solo il traffico necessario: i tablet verso il server BIM, le fotocamere verso il repository immagini, i sensori verso il sistema di monitoraggio.

## 2. Rete della sede centrale

La sede dispone già di una rete locale e di un collegamento ADSL, ma questa soluzione è insufficiente per il nuovo sistema, perché i dati BIM e le immagini possono essere molto pesanti.

La rete centrale può essere potenziata così:

```
Internet fibra
      |
Firewall aziendale
      |
Switch principale
      |
-------------------------
|          |            |
```

Server     Uffici       Wi-Fi
BIM       tecnici      aziendale
|
NAS / backup

Si propone quindi di aggiungere:

* collegamento in fibra al posto della sola ADSL;
* firewall aziendale con VPN;
* switch gestiti;
* server BIM;
* NAS o storage centrale;
* sistema di backup;
* server di autenticazione;
* VLAN separate.

Anche in sede si possono usare VLAN:

```
VLAN uffici tecnici
VLAN server BIM
VLAN gestione apparati
VLAN VPN cantieri
VLAN ospiti
```

In questo modo i server BIM non sono accessibili direttamente da tutti i dispositivi della rete.

## 3. Collegamenti tra cantieri e sede

Il collegamento tra cantiere e sede deve supportare tre tipi di traffico:

* dati dei sensori, leggeri ma importanti;
* immagini timelapse, più pesanti;
* scansioni 3D, molto pesanti.

Per ogni cantiere si può usare un collegamento principale in fibra, FWA o 5G, con una linea di backup se possibile. Il traffico deve passare attraverso una VPN site-to-site, cioè un collegamento cifrato tra la rete del cantiere e quella della sede.

La sede centrale dovrebbe avere una fibra business, perché deve ricevere dati da più cantieri. L’ADSL può rimanere solo come linea di emergenza.

Per la capacità trasmissiva, si può ipotizzare:

```
sensori: pochi Kbps o meno di 1 Mbps
fotocamere: alcuni Mbps
scansioni 3D: traffico elevato, da trasferire anche in orari programmati
```

I dati urgenti, come allarmi dei sensori, devono avere priorità rispetto ai file pesanti. Per questo si può usare QoS, cioè una gestione delle priorità del traffico.

## 4. Autenticazione degli operatori

Gli utenti devono autenticarsi con credenziali personali. È opportuno usare un sistema centralizzato, ad esempio Active Directory o LDAP.

Gli operatori possono avere ruoli diversi:

```
progettisti:
    accesso ai modelli BIM

operatori di cantiere:
    caricamento scansioni e immagini

responsabili sicurezza:
    accesso ai dati dei sensori

amministratori:
    gestione della rete e dei server
```

Per il Wi-Fi si può usare WPA2/WPA3 Enterprise con autenticazione personale. Per l’accesso da cantiere si usa la VPN. Dove possibile, è consigliabile aggiungere l’autenticazione a due fattori.

Tutti gli accessi importanti devono essere registrati nei log.

## Seconda parte

La traccia chiede di svolgere due quesiti; qui vengono svolti tutti e quattro in forma sintetica.

## Quesito I - On premise e cloud

Una soluzione on premise prevede che server e dati siano conservati nella sede centrale. Ha il vantaggio di dare maggiore controllo sui dati e buona velocità per gli utenti interni, ma richiede costi iniziali, manutenzione e gestione dei backup.

Una soluzione cloud-based prevede che i dati siano salvati presso un fornitore esterno. Ha il vantaggio di essere più scalabile e accessibile da più sedi, ma dipende dalla connessione Internet e comporta costi ricorrenti.

La soluzione più equilibrata è ibrida: dati principali e lavoro quotidiano su server/NAS in sede, backup o sincronizzazione anche su cloud. In questo modo si uniscono controllo locale e maggiore sicurezza in caso di guasto.

## Quesito II - Sicurezza e continuità

Per la sicurezza si adottano firewall, VPN, VLAN, password robuste, aggiornamenti, backup, log e cifratura delle comunicazioni.

Nei cantieri i sensori, le fotocamere e i tablet devono stare su reti separate. In sede i server BIM devono essere protetti e accessibili solo agli utenti autorizzati.

La comunicazione tra cantiere e sede deve avvenire tramite VPN, così i dati viaggiano cifrati anche se passano da Internet.

Per garantire continuità si possono usare:

```
doppia connessione Internet in sede;
linea di backup nei cantieri;
router con failover;
UPS per apparati importanti;
salvataggio locale temporaneo dei dati.
```

Se la connessione cade, i dati meno urgenti possono essere conservati localmente e inviati dopo. Gli allarmi dei sensori devono invece poter funzionare anche localmente.

## Quesito III - Blocco piattaforme AI nella rete scolastica

Questo quesito riguarda una scuola, quindi la soluzione deve essere più semplice e proporzionata rispetto al contesto aziendale.

Si può dividere la rete scolastica in VLAN:

```
segreteria
docenti
laboratorio 1
laboratorio 2
Wi-Fi studenti
ospiti
```

Il blocco delle piattaforme AI va applicato soprattutto alle VLAN dei laboratori durante verifiche o esercitazioni.

Le misure possibili sono:

* filtro DNS;
* firewall;
* proxy web;
* blocco di domini e categorie di siti;
* regole per laboratorio;
* regole per orario.

Esempio:

```
laboratorio 1
lunedì dalle 10:00 alle 12:00
blocco piattaforme AI attivo
```

Il blocco può poi essere disattivato automaticamente alla fine dell’attività.

La soluzione non è perfetta, perché gli studenti potrebbero usare smartphone, VPN o siti non ancora bloccati. Per questo il controllo tecnico deve essere accompagnato da regole didattiche: consegne chiare, vigilanza del docente, spiegazione orale del codice e verifiche in ambiente controllato.

## Quesito IV - SSH e port forwarding

Il comando è:

```
ssh -p 25500 administrator@200.1.1.1
```

Il protocollo SSH permette di accedere da remoto a un dispositivo tramite terminale in modo cifrato.

L’opzione:

```
-p 25500
```

indica che si usa la porta 25500 invece della porta standard 22.

Il dispositivo 200.1.1.1 riceve la connessione sulla porta 25500 e, grazie a una regola di port forwarding, la inoltra al dispositivo interno:

```
172.16.1.100
```

Quindi il comando permette di accedere via SSH a un host interno che normalmente non sarebbe raggiungibile direttamente da Internet.

Schema:

```
PC remoto
    |
200.1.1.1:25500
    |
port forwarding
    |
172.16.1.100
```

La finalità è amministrare da remoto un dispositivo interno. Tuttavia questa configurazione deve essere protetta con password robuste, chiavi SSH, log e possibilmente accesso limitato solo da alcuni indirizzi IP. Una soluzione ancora più sicura sarebbe usare prima una VPN e poi collegarsi al dispositivo interno.

## Conclusione

La soluzione proposta realizza una rete di cantiere semplice ma sicura, collegata alla sede centrale tramite VPN. La sede deve essere potenziata con fibra, firewall, server BIM, storage e backup.

I dati pesanti, come scansioni e immagini, possono essere trasferiti in modo programmato, mentre i dati dei sensori devono avere priorità. La sicurezza si basa su VLAN, firewall, VPN, autenticazione personale e log.

Nel caso scolastico, invece, la soluzione deve essere più semplice: VLAN dei laboratori, filtro DNS, firewall/proxy e blocchi programmati solo dove e quando servono.
