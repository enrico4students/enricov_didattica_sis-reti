
# Sistemi e Reti - Esercizio di preparazione a prova d’esame

## PRIMA PARTE

## Azienda di produzione contenuti digitali per il turismo con nuova sede operativa

Una società che opera nel settore della produzione di contenuti digitali per il turismo apre una nuova sede operativa in un’altra città.

L’azienda realizza video promozionali, contenuti social, pagine informative, cataloghi digitali e materiali multimediali destinati a portali turistici, agenzie di viaggio, strutture ricettive ed enti locali.

All’interno della sede sono previsti i seguenti reparti produttivi:

* Reparto A) Creazione contenuti multimediali per dispositivi mobili
* Reparto B) Creazione contenuti web e pagine informative
* Reparto C) Produzione contenuti digitali avanzati per aziende turistiche

Sono inoltre presenti:

* Reparto D) Revisione, controllo qualità e validazione contenuti
* Reparto E) Coordinamento progetti editoriali e gestione pubblicazioni
* Reparto F) Area amministrativa e gestione contratti

Ogni addetto dispone di una postazione desktop aziendale.

Distribuzione prevista:

| Reparto     | A  | B  | C  | D  | E  | F  |
| ----------- | -- | -- | -- | -- | -- | -- |
| N° computer | 48 | 32 | 96 | 22 | 12 | 18 |

Ogni reparto prevede fino al 10% di postazioni aggiuntive di riserva.

L’accesso ai sistemi deve avvenire tramite autenticazione.

## Vincoli operativi

Gli operatori dei reparti A, B, C devono accedere a:

* Internet
* stampante di reparto
* archivio/file server locale del proprio reparto

Non deve invece essere consentito loro di accedere agli archivi interni degli altri reparti produttivi.

Il reparto D deve:

* accedere agli archivi dei reparti A, B, C
* verificare e validare i contenuti prodotti
* salvare report di revisione
* marcare i contenuti approvati aggiungendo un suffisso al nome della cartella, ad esempio “_APPROVATO”
* rendere i contenuti approvati non modificabili

Il reparto E deve:

* accedere a tutti gli archivi locali della sede
* raccogliere i contenuti approvati
* trasferirli verso un repository centrale remoto presso la sede principale
* aggiungere metadati, documentazione e informazioni di pubblicazione

Il reparto F deve:

* accedere a Internet
* accedere al sistema gestionale remoto presso la sede centrale, usato per contratti, fatturazione e clienti

## Richieste

Il candidato analizzi la situazione e sviluppi:

1. un progetto di massima dell’infrastruttura di rete della nuova sede, anche supportato da uno schema grafico, prevedendo struttura delle sottoreti, apparati, servizi implementati, tipologia delle connessioni interne e verso Internet e un opportuno piano di indirizzamento;

2. le misure e i sistemi per la gestione della sicurezza interna ed esterna;

3. le modalità e i protocolli di collegamento verso i sistemi remoti nella sede centrale;

4. i dettagli di configurazione di uno dei servizi.

---

# SECONDA PARTE

## Quesito I

Il candidato esponga le tipologie di firewall in relazione ai ruoli di  
- edge/perimeter firewall  
- internal firewall  

Spieghi la relazione fra firewall e le tipologie di DMZ studiate  

---

## Quesito II

In relazione al tema proposto nella prima parte, si immagini di voler concentrare i vari server locali su un unico server fisico molto potente di cui si intende sfruttare al massimo la potenza elaborativa.

Il candidato illustri:

* Le modalità di realizzazione di questo obiettivo e scelga quella che ritiene migliore, specificando le motivazioni e le eventuali alternative scartate, anche queste con motivazioni

* quali modifiche all’infrastruttura di rete e alla sua configurazione logica e fisica si renderebbero eventualmente necessarie per implementare la modalità scelta

---

## Quesito III

Il candidato definisca con quali modalità implementare la sicurezza della rete WIFI in modo che sia massima relativamente a stanards/tecnologie attuali.  

Uno degli ingegneri interni "storici" spinge per l'adozione di WEP sostenendo che è semplice ed è adeguata.  
Analizzare se la sua posizione è valida.

---

## Quesito IV

In relazione al tema proposto nella prima parte, si ipotizzi che presso la sede centrale siano presenti, oltre al repository remoto dei contenuti e al sistema gestionale, anche alcuni server pubblici per offrire i seguenti servizi:

* endpoint REST per consentire ricerche e accesso ai contenuti da programma
* VPN per smartwork, che preserva i normali limiti di accesso

Descrivere tale parte dell’infrastruttura di rete dell’azienda.


---
