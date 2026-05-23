# Lezione - Spiegazione della soluzione della seconda prova di Sistemi e Reti 2024

## Introduzione

Questa lezione spiega passo per passo una possibile soluzione della seconda prova di Sistemi e Reti della sessione straordinaria 2024.

L’obiettivo non è soltanto mostrare una soluzione “corretta”, ma soprattutto comprendere:

* come analizzare una traccia;
* come trasformare i requisiti in una architettura di rete;
* come scegliere VLAN, indirizzamento, firewall e VPN;
* come motivare le scelte tecniche;
* come evitare errori concettuali frequenti.

La traccia descrive una azienda informatica che apre una nuova sede in una città diversa dalla sede principale.

I reparti principali sono:

* sviluppo mobile;
* sviluppo web;
* sviluppo software di settore;
* test qualità;
* project management;
* amministrazione.

La richiesta più importante della traccia è la separazione dei reparti.

Gli sviluppatori devono lavorare isolati dagli altri reparti di sviluppo, mentre il reparto test e il project management devono avere accessi controllati trasversali.

---

# 1. Analisi iniziale della traccia

## Comprendere i requisiti

Il primo passo di una prova di Sistemi e Reti consiste nel trasformare il testo in requisiti tecnici.

La traccia fornisce diversi vincoli:

| Requisito                      | Conseguenza tecnica           |
| ------------------------------ | ----------------------------- |
| Reparti A/B/C separati         | VLAN differenti + ACL         |
| Accesso Internet               | firewall + NAT                |
| File server locali             | server dedicati o VLAN server |
| Accesso controllato reparto D  | ACL specifiche                |
| Collegamento con sede centrale | VPN site-to-site              |
| Autenticazione utenti          | Active Directory / LDAP       |
| Sicurezza interna              | segmentazione + controlli     |

Molti studenti leggono la traccia in modo troppo superficiale.

In realtà la parte più importante è capire:

* chi deve comunicare;
* chi NON deve comunicare;
* quali sistemi devono essere pubblici;
* quali sistemi devono essere interni.

---

# 2. Perché usare le VLAN

## Problema senza VLAN

Se tutti i PC appartenessero alla stessa rete:

* tutti potrebbero raggiungere tutti;
* sarebbe difficile applicare regole diverse;
* aumenterebbe il traffico broadcast;
* un problema di sicurezza potrebbe propagarsi facilmente.

La traccia invece richiede isolamento.

Per questo motivo si usano VLAN separate.

## VLAN della soluzione

Nella soluzione vengono usate VLAN differenti:

| VLAN    | Funzione                 |
| ------- | ------------------------ |
| VLAN 10 | utenti reparto A         |
| VLAN 20 | utenti reparto B         |
| VLAN 30 | utenti reparto C         |
| VLAN 40 | test qualità             |
| VLAN 50 | project management       |
| VLAN 60 | amministrazione          |
| VLAN 70 | servizi infrastrutturali |
| VLAN 80 | management apparati      |
| VLAN 90 | ospiti                   |
| VLAN 99 | backup                   |

Separare utenti, server, management e backup è una pratica professionale molto comune.

---

# 3. Routing inter-VLAN corretto

## Errore concettuale molto frequente

Un errore frequente consiste nel fare tutto il routing sul firewall.

Questo approccio è spesso sbagliato.

In una rete aziendale reale:

* il traffico interno tra reparti può essere molto elevato;
* i file server generano molto traffico;
* il firewall diventerebbe un collo di bottiglia.

## Soluzione corretta

Nella soluzione corretta:

* il routing inter-VLAN ordinario viene svolto dal core switch Layer 3;
* il firewall protegge Internet, VPN, DMZ e reti critiche.

Schema logico:

```
PC VLAN A
    |
Switch accesso
    |
Core Switch Layer 3
    |
ACL tra VLAN
    |
Firewall / NGFW
    |
Internet
```

## Perché il core switch Layer 3

Uno switch Layer 3:

* instrada pacchetti tra VLAN;
* usa hardware dedicato;
* è molto veloce;
* riduce il carico sul firewall.

Il firewall viene invece usato dove serve maggiore controllo:

* Internet;
* VPN;
* DMZ;
* IDS/IPS;
* filtraggio avanzato.

---

# 4. ACL e isolamento tra reparti

## Obiettivo della traccia

La traccia richiede che:

* A non possa accedere a B e C;
* B non possa accedere ad A e C;
* C non possa accedere ad A e B.

Questo si ottiene con ACL.

## Esempio concettuale

ACL semplificata:

```
deny VLAN_A -> VLAN_B
deny VLAN_A -> VLAN_C
permit VLAN_A -> FileServer_A
permit VLAN_A -> Internet
```

Le ACL vengono applicate sulle interfacce VLAN del core switch Layer 3.

## Deny by default

Regola professionale molto importante:

“tutto bloccato salvo ciò che è esplicitamente consentito”.

Questo approccio riduce:

* errori;
* accessi non previsti;
* superfici di attacco.

---

# 5. Piano di indirizzamento e VLSM

## Perché usare VLSM

Ogni reparto ha dimensioni differenti.

Il reparto C richiede oltre 100 host.

Il reparto E invece richiede pochi host.

Usare sempre la stessa subnet sarebbe inefficiente.

Per questo si usa VLSM:

Variable Length Subnet Mask.

## Esempio

Reparto C:

* circa 110 host;
* serve almeno una /25;
* una /25 offre 126 host utilizzabili.

Subnet:

```
10.24.30.0/25
```

Calcoli:

* Network ID: 10.24.30.0
* Broadcast: 10.24.30.127
* Host utilizzabili: 10.24.30.1 - 10.24.30.126

## Gateway e primo host

Errore frequente:

confondere “host utilizzabili” con “primo IP assegnabile ai client”.

Esempio:

```
gateway: 10.24.30.1
```

Quindi:

```
primo IP normalmente assegnato a PC:
10.24.30.2
```

Questa distinzione deve essere chiarita nelle tabelle.

---

# 6. Perché separare server e utenti

## Approccio semplice

Una soluzione semplice potrebbe mettere:

* PC;
* file server;
* stampanti;

nella stessa VLAN.

Questo però riduce sicurezza e controllabilità.

## Approccio professionale

Nella soluzione completa:

* utenti in una VLAN;
* server in una VLAN diversa.

Esempio:

| VLAN    | Contenuto        |
| ------- | ---------------- |
| VLAN 10 | utenti reparto A |
| VLAN 11 | server reparto A |

Vantaggi:

* ACL più precise;
* maggiore sicurezza;
* logging migliore;
* minore propagazione di problemi.

---

# 7. Autenticazione centralizzata

## Problema senza autenticazione centralizzata

Senza autenticazione centralizzata:

* ogni PC avrebbe utenti locali;
* gestione difficile;
* password non uniformi;
* controllo scarso.

## Soluzione

La soluzione propone:

* Active Directory;
  oppure
* LDAP/Kerberos.

## Vantaggi

Permette:

* login centralizzato;
* gruppi utenti;
* gestione permessi;
* policy comuni;
* auditing.

## Gruppi

Esempi:

* DEV_A;
* DEV_B;
* TEST_QA;
* PROJECT_MANAGER.

I permessi vengono assegnati ai gruppi e non ai singoli utenti.

Questo è molto importante nelle reti aziendali.

---

# 8. Reparto D e gestione delle versioni finali

## Richiesta della traccia

Il reparto D deve:

* testare i progetti;
* scrivere report;
* rinominare la cartella;
* renderla read-only.

## Errore progettuale possibile

Errore comune:

“i tester non devono avere permessi”.

Questo contraddice la traccia.

La traccia richiede esplicitamente che possano farlo.

## Soluzione corretta

I tester possono:

* accedere solo alle cartelle in test;
* rinominare le versioni finali;
* impostare permessi read-only.

La procedura può essere:

* manuale;
  oppure
* automatizzata tramite script.

Ma lo script deve essere eseguito dagli operatori D.

Non deve sostituirli.

---

# 9. Repository centrale e DevOps

## Problema di una copia manuale

Dire semplicemente:

“il project manager copia i file sul repository”

è poco professionale.

## Soluzione corretta

La soluzione migliorata propone:

* Git;
* GitLab/Gitea/Bitbucket;
* HTTPS;
* Git over HTTPS;
* pipeline CI/CD.

## Perché è migliore

Permette:

* tracciabilità;
* versionamento;
* controllo accessi;
* log;
* automazione.

Il project manager rimane il responsabile del rilascio.

Ma il trasferimento avviene con strumenti professionali.

---

# 10. VPN site-to-site

## Scopo

Le due sedi sono in città differenti.

Serve quindi un collegamento sicuro.

## VPN IPsec

La soluzione usa:

VPN IPsec site-to-site.

## Concetto importante

La VPN NON è un dispositivo separato.

È:

* un tunnel logico;
* tra i due firewall;
* attraverso Internet.

Schema corretto:

```
Firewall sede nuova
    |
Tunnel IPsec cifrato
    |
Firewall sede centrale
```

Errore concettuale frequente:

rappresentare la VPN come un cloud o dispositivo autonomo.

---

# 11. DMZ e server pubblici

## Perché usare una DMZ

I server pubblici:

* web server;
* mail gateway;

non devono stare nella LAN interna.

Si usa quindi una DMZ.

## Schema

```
Internet
    |
Firewall
    |
    |-- DMZ
    |     |-- Web server
    |     |-- Mail gateway
    |
    |-- LAN interna
```

## Vantaggi

Se un server pubblico viene compromesso:

* l’attaccante non entra automaticamente nella LAN.

La DMZ riduce l’impatto degli attacchi.

---

# 12. Proxy, reverse proxy e WAF

## Errore molto comune

Molti studenti confondono:

* proxy;
* reverse proxy;
* WAF.

## Forward proxy

Usato dai client interni.

Serve per:

* filtrare navigazione;
* registrare accessi;
* applicare policy.

## Reverse proxy

Riceve richieste da Internet e le inoltra ai server.

Può:

* terminare TLS;
* bilanciare carico;
* nascondere server reali.

## WAF

WAF significa:

Web Application Firewall.

Protegge applicazioni HTTP/HTTPS.

Blocca:

* SQL injection;
* XSS;
* richieste anomale.

Può essere integrato in un reverse proxy.

---

# 13. Sicurezza WiFi

## Evoluzione protocolli

| Protocollo | Stato         |
| ---------- | ------------- |
| WEP        | insicuro      |
| WPA        | superato      |
| WPA2       | molto diffuso |
| WPA3       | più moderno   |

## Personal vs Enterprise

WPA2/WPA3 Personal:

* password condivisa.

WPA2/WPA3 Enterprise:

* autenticazione individuale;
* server RADIUS.

## Soluzione aziendale corretta

Per una azienda:

* WPA2-Enterprise;
  oppure
* WPA3-Enterprise.

---

# 14. Virtualizzazione

## Idea principale

Più server virtuali nello stesso host fisico.

## Vantaggi

* minori costi;
* gestione semplificata;
* backup più semplici;
* migliore utilizzo hardware.

## Attenzione importante

Le VM devono rimanere separate logicamente.

Quindi:

* VLAN differenti;
* trunk 802.1Q;
* virtual switch.

## Hypervisor tipo 1 e tipo 2

Tipo 1:

* installato direttamente sull’hardware;
* più adatto a produzione.

Tipo 2:

* installato sopra un sistema operativo;
* più adatto a laboratorio.

---

# 15. Errori da evitare nella prova

## Errori molto comuni

### Fare tutto il routing sul firewall

Produce colli di bottiglia.

### Non separare le VLAN

Contraddice la traccia.

### Confondere gateway e primo host client

Errore molto frequente nel VLSM.

### Mettere database direttamente in DMZ

Molto pericoloso.

### Dire “VPN cloud separato”

La VPN è un tunnel logico.

### Confondere proxy e WAF

Sono componenti differenti.

---

# 16. Conclusione

Una buona soluzione di Sistemi e Reti deve:

* essere coerente con la traccia;
* essere tecnicamente corretta;
* motivare le scelte;
* usare terminologia corretta;
* distinguere chiaramente:

  * VLAN;
  * routing;
  * ACL;
  * firewall;
  * VPN;
  * DMZ;
  * proxy;
  * WAF.

L’aspetto più importante non è inserire tecnologie “complicate”, ma mostrare di avere compreso:

* la logica della segmentazione;
* la sicurezza;
* i flussi di comunicazione;
* il ruolo dei diversi apparati di rete.
