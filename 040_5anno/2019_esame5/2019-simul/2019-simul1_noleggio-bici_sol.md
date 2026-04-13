

---

1. ANALISI DELLA REALTÀ E IPOTESI AGGIUNTIVE

---

Dalla traccia emergono questi vincoli:

* ogni stazione ha 50 slot;
* ogni bici ha un identificativo univoco letto via RFID;
* ogni utente ha una smart card contactless con identificativo utente;
* per ogni operazione occorre registrare bici, utente, data/ora, stazione;
* i dati devono essere trasmessi in tempo reale al centro;
* la mappa deve mostrare biciclette disponibili e slot liberi;
* il sistema deve consentire di sapere in ogni momento chi ha in uso una certa bici. 

Ipotesi progettuali aggiuntive:

1. Ogni stazione dispone di un controller locale industriale.
2. Ogni stazione ha connettività primaria su fibra/FTTC o 4G/5G industriale, con VPN verso il centro.
3. Il pagamento con carta non viene gestito memorizzando il numero completo della carta nel sistema comunale; viene invece usato un token restituito da un payment gateway esterno.
4. Una bici può essere:

   * disponibile in uno slot,
   * in uso,
   * fuori servizio,
   * in manutenzione.
5. Una riconsegna può essere accettata solo in uno slot libero e operativo.
6. Un noleggio può essere avviato solo se l’utente è attivo, non sospeso e non ha già un noleggio aperto.
7. La tariffazione è calcolata centralmente sulla durata del noleggio.

---

2. PROGETTO DELL’INFRASTRUTTURA TECNOLOGICA

---

2.1 Architettura generale

Si adotta una architettura centralizzata con intelligenza locale minima nelle stazioni.

Schema logico testuale:

Utente
smart card contactless
lettore stazione
controller locale stazione
router industriale / firewall VPN
rete pubblica
data center comunale / cloud pubblico qualificato
API server
application server
database server
message broker
monitoring server
web server / mobile backend

Ogni stazione contiene:

* un lettore contactless per la tessera utente;
* 50 slot con sensore di presenza, RFID reader e attuatore del blocco meccanico;
* un controller locale che governa i dispositivi;
* un router/firewall industriale;
* un UPS;
* eventuali telecamere e sensori anti-manomissione.

Il controller locale non è il sistema “di verità” dei dati: mantiene solo una coda locale temporanea per tollerare brevi disconnessioni. Il dato ufficiale risiede nel centro.

2.2 Infrastruttura di comunicazione

Canali

Per una città di medie dimensioni la soluzione più equilibrata è:

* canale primario: connettività fissa IP, dove disponibile;
* canale di backup: modem 4G/5G industriale;
* cifratura: VPN IPsec site-to-site tra stazione e centro.

Motivazione:

* la connettività fissa ha costi prevedibili e buona stabilità;
* il 4G/5G consente continuità di servizio in caso di guasto della linea primaria;
* la VPN protegge il traffico su rete pubblica.

Protocolli

Tra stazioni e centro:

* IP
* TCP
* HTTPS per API REST
* MQTT su TLS come opzione molto adatta per telemetria ed eventi rapidi
* NTP per sincronizzazione oraria
* SNMP o telemetria equivalente per monitoraggio apparati

Scelta consigliata:

* HTTPS REST per operazioni gestionali e interrogazioni;
* MQTT/TLS per eventi asincroni come:

  * noleggio avviato,
  * bici estratta,
  * bici inserita,
  * slot guasto,
  * allarme anti-manomissione.

Motivazione:

* REST è semplice da integrare con backend web;
* MQTT è leggero, affidabile e adatto a dispositivi periferici.

2.3 Apparati e componenti nelle stazioni

Hardware di stazione

* controller industriale fanless o mini-PC rugged;
* lettore contactless smart card/NFC;
* 50 RFID reader integrati negli slot;
* 50 attuatori elettromeccanici di blocco/sblocco;
* sensori presenza bici;
* router/firewall industriale dual WAN;
* switch industriale se necessario;
* UPS locale;
* eventuale pannello di stato / display di servizio.

Software di stazione

* sistema operativo embedded Linux;
* servizio di controllo dispositivi;
* modulo di autorizzazione locale minima;
* coda locale persistente degli eventi;
* client VPN;
* agente di monitoraggio;
* log locale firmato e sincronizzato.

Funzionamento sintetico del noleggio

1. L’utente presenta la smart card.
2. Il controller legge l’ID utente.
3. Il controller invia richiesta di autorizzazione al centro.
4. Il centro verifica:

   * utente attivo,
   * assenza di noleggi aperti,
   * validità amministrativa del profilo.
5. Il centro restituisce autorizzazione.
6. Il controller sblocca una bici disponibile.
7. L’RFID reader dello slot rileva l’uscita della bici.
8. L’evento viene registrato centralmente come apertura del noleggio.

Funzionamento sintetico della riconsegna

1. L’utente inserisce la bici in uno slot libero.
2. Lo slot legge il tag RFID e rileva la presenza.
3. Il controller blocca meccanicamente la bici.
4. Il centro associa la bici a un noleggio aperto.
5. Il sistema chiude il noleggio, calcola durata e costo.

2.4 Componenti hardware e software centrali

Lato centrale

Hardware o VM ridondate:

* load balancer;
* 2 application server;
* database server primario;
* database replica/standby;
* storage per backup;
* server di monitoraggio;
* server di reportistica.

Software centrale:

* backend applicativo;
* DBMS relazionale;
* API REST;
* message broker;
* scheduler per report periodici;
* sistema di logging centralizzato;
* dashboard operativa per i gestori;
* frontend web responsive;
* backend per app mobile.

Scelta DBMS

Si propone PostgreSQL, perché:

* robusto;
* adatto a transazioni;
* supporta vincoli e viste;
* gestisce bene concorrenza e integrità;
* è ottimo anche per estensioni geografiche future.

2.5 Continuità del servizio

Per assicurare continuità:

Nelle stazioni

* UPS locale;
* doppia connettività;
* cache/coda locale persistente;
* watchdog hardware/software;
* modalità degradata temporanea.

Al centro

* ridondanza dei server;
* replica database;
* backup periodici;
* monitoraggio proattivo;
* disaster recovery;
* segmentazione di rete e firewalling.

Modalità degradata ammessa

Se cade temporaneamente il collegamento, la stazione può:

* continuare a registrare localmente gli eventi;
* sincronizzarli appena la connettività ritorna.

Per evitare inconsistenze:

* ogni evento ha un ID univoco globale;
* il centro tratta gli eventi in modo idempotente;
* ogni operazione usa timestamp e identificativo stazione.

---

3. PROGETTO DELLA BASE DI DATI

---

La traccia richiede la gestione di utenti, operazioni di noleggio e riconsegna, biciclette e situazione di occupazione delle stazioni. 

3.1 Scelte progettuali

Per rappresentare bene il dominio, conviene distinguere:

* UTENTE
* SMART_CARD
* STAZIONE
* SLOT
* BICICLETTA
* NOLEGGIO
* TARIFFA
* TRANSAZIONE_PAGAMENTO

Le operazioni di noleggio e riconsegna possono essere modellate in due modi:

A. tabella eventi separata;
B. entità NOLEGGIO con data/ora e stazione di inizio/fine.

Per questa prova la soluzione più chiara è B, perché consente di rispondere facilmente alle query richieste e di sapere subito quali bici sono “attualmente in uso” cercando i noleggi ancora aperti.

3.2 Modello concettuale testuale

Entità

UTENTE

* idUtente
* nome
* cognome
* email
* telefono
* indirizzo
* statoUtente
* dataRegistrazione
* tokenPagamento

SMART_CARD

* idCard
* uidCard
* statoCard
* dataEmissione

BICICLETTA

* idBici
* codiceRFID
* statoBici
* dataAcquisto

STAZIONE

* idStazione
* nome
* indirizzo
* latitudine
* longitudine
* statoStazione
* numeroSlot

SLOT

* idSlot
* numeroSlot
* statoSlot

NOLEGGIO

* idNoleggio
* dataOraPrelievo
* dataOraRiconsegna
* costoCalcolato
* statoNoleggio

TARIFFA

* idTariffa
* descrizione
* minutiFranchigia
* costoPrimaOra
* costoOraSuccessiva
* penaleGiornaliera

TRANSAZIONE_PAGAMENTO

* idTransazione
* importo
* dataOraTransazione
* esito
* riferimentoGateway

Relazioni

1. UTENTE possiede SMART_CARD
   cardinalità:
   UTENTE 1 --- 1 SMART_CARD
   oppure 1 --- N se si desidera storicizzare le carte sostituite.
   Scelta consigliata: 1 --- N con una sola attiva.

2. STAZIONE contiene SLOT
   STAZIONE 1 --- N SLOT

3. STAZIONE ospita BICICLETTA tramite SLOT
   operativamente l’occupazione attuale può stare in SLOT con FK opzionale verso BICICLETTA.

4. UTENTE effettua NOLEGGIO
   UTENTE 1 --- N NOLEGGIO

5. BICICLETTA è usata in NOLEGGIO
   BICICLETTA 1 --- N NOLEGGIO

6. STAZIONE è stazione di prelievo del NOLEGGIO
   STAZIONE 1 --- N NOLEGGIO

7. STAZIONE è stazione di riconsegna del NOLEGGIO
   STAZIONE 1 --- N NOLEGGIO

8. TARIFFA si applica a NOLEGGIO
   TARIFFA 1 --- N NOLEGGIO

9. NOLEGGIO genera eventualmente una TRANSAZIONE_PAGAMENTO
   NOLEGGIO 1 --- 0..1 TRANSAZIONE_PAGAMENTO
   oppure 1 --- N se si vogliono consentire riaddebiti o storni.
   Scelta qui: 1 --- 1 opzionale.

3.3 Modello logico relazionale

UTENTE(
id_utente PK,
nome,
cognome,
email UNIQUE,
telefono,
indirizzo,
stato_utente,
data_registrazione,
token_pagamento
)

SMART_CARD(
id_card PK,
uid_card UNIQUE,
id_utente FK -> UTENTE(id_utente),
stato_card,
data_emissione,
data_disattivazione
)

STAZIONE(
id_stazione PK,
nome,
indirizzo,
latitudine,
longitudine,
stato_stazione,
numero_slot CHECK (numero_slot = 50)
)

BICICLETTA(
id_bici PK,
codice_rfid UNIQUE,
stato_bici,
data_acquisto
)

SLOT(
id_slot PK,
id_stazione FK -> STAZIONE(id_stazione),
numero_slot,
stato_slot,
id_bici_corrente FK -> BICICLETTA(id_bici) NULL,
UNIQUE(id_stazione, numero_slot)
)

TARIFFA(
id_tariffa PK,
descrizione,
minuti_franchigia,
costo_prima_ora,
costo_ora_successiva,
penale_giornaliera
)

NOLEGGIO(
id_noleggio PK,
id_utente FK -> UTENTE(id_utente),
id_bici FK -> BICICLETTA(id_bici),
id_stazione_prelievo FK -> STAZIONE(id_stazione),
id_stazione_riconsegna FK -> STAZIONE(id_stazione) NULL,
data_ora_prelievo,
data_ora_riconsegna NULL,
id_tariffa FK -> TARIFFA(id_tariffa),
costo_calcolato NULL,
stato_noleggio
)

TRANSAZIONE_PAGAMENTO(
id_transazione PK,
id_noleggio FK -> NOLEGGIO(id_noleggio) UNIQUE,
importo,
data_ora_transazione,
esito,
riferimento_gateway
)

Vincoli importanti

* un utente non può avere più di un noleggio aperto;
* una bici non può comparire in due noleggi aperti;
* uno slot contiene al massimo una bici;
* alla riconsegna si valorizzano:
  id_stazione_riconsegna, data_ora_riconsegna, costo_calcolato.

I primi due vincoli si implementano bene con indici parziali o logica applicativa transazionale.

Esempio concettuale di vincolo:

* NOLEGGIO aperto = record con data_ora_riconsegna IS NULL.

3.4 Situazione di occupazione delle stazioni

La traccia chiede anche la situazione di occupazione delle stazioni. 

La soluzione più corretta è non duplicare inutilmente il dato se lo si può derivare da SLOT.

Per ogni stazione:

* biciclette disponibili = numero di slot con id_bici_corrente non NULL e stato_slot = 'OK'
* slot liberi = numero di slot con id_bici_corrente NULL e stato_slot = 'OK'

Quindi l’occupazione corrente è derivabile dalla tabella SLOT.

---

4. PROGETTO DELLE PAGINE WEB

---

La traccia richiede:
a) verifica disponibilità bici a partire da una mappa delle stazioni;
b) visualizzazione per il gestore delle bici attualmente in uso, con utente e stazione di prelievo. 

4.1 Pagina pubblica “Mappa stazioni”

Funzioni:

* visualizzare la mappa cittadina;
* mostrare marker per ogni stazione;
* al click sul marker mostrare:

  * nome stazione
  * bici disponibili
  * slot liberi
  * stato stazione
  * ultimo aggiornamento

Interfaccia:

* mappa centrale;
* pannello laterale con ricerca stazione;
* colori marker:

  * verde: molte bici disponibili
  * giallo: poche bici
  * rosso: nessuna bici disponibile
  * grigio: stazione fuori servizio

API utile:
GET /api/stazioni

Risposta JSON esempio:
[
{
"idStazione": 12,
"nome": "Piazza Roma",
"lat": 41.9001,
"lng": 12.5002,
"biciDisponibili": 17,
"slotLiberi": 33,
"stato": "ATTIVA",
"ultimoAggiornamento": "2026-04-13T15:20:00"
}
]

4.2 Pagina gestore “Bici attualmente in uso”

Accesso riservato con autenticazione.

Colonne:

* ID noleggio
* codice bici
* utente
* data/ora prelievo
* stazione di prelievo
* durata attuale
* stato

Filtri:

* per stazione di prelievo;
* per intervallo temporale;
* per utente;
* per bici.

La logica dati è semplice:

* mostrare tutti i record NOLEGGIO con data_ora_riconsegna IS NULL.

4.3 Codifica di una pagina: esempio originale

Si propone di codificare la funzione “verificare se una stazione ha biciclette disponibili”, con backend PHP e query SQL.

Esempio backend PHP semplificato:

```
<?php
$pdo = new PDO(
    "mysql:host=localhost;dbname=bikesharing;charset=utf8mb4",
    "user",
    "password",
    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
);

$idStazione = isset($_GET['id_stazione']) ? (int)$_GET['id_stazione'] : 0;

$sql = "
    SELECT
        s.id_stazione,
        s.nome,
        SUM(CASE WHEN sl.id_bici_corrente IS NOT NULL AND sl.stato_slot = 'OK' THEN 1 ELSE 0 END) AS bici_disponibili,
        SUM(CASE WHEN sl.id_bici_corrente IS NULL AND sl.stato_slot = 'OK' THEN 1 ELSE 0 END) AS slot_liberi
    FROM STAZIONE s
    JOIN SLOT sl ON sl.id_stazione = s.id_stazione
    WHERE s.id_stazione = :id_stazione
    GROUP BY s.id_stazione, s.nome
";

$stmt = $pdo->prepare($sql);
$stmt->execute(['id_stazione' => $idStazione]);
$row = $stmt->fetch(PDO::FETCH_ASSOC);

header('Content-Type: application/json; charset=utf-8');

if (!$row) {
    echo json_encode([
        "ok" => false,
        "messaggio" => "Stazione non trovata"
    ]);
    exit;
}

echo json_encode([
    "ok" => true,
    "id_stazione" => $row["id_stazione"],
    "nome" => $row["nome"],
    "bici_disponibili" => (int)$row["bici_disponibili"],
    "slot_liberi" => (int)$row["slot_liberi"],
    "noleggio_possibile" => ((int)$row["bici_disponibili"] > 0)
]);
```

Esempio frontend HTML + JavaScript essenziale:

```
<!doctype html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <title>Disponibilità stazione</title>
</head>
<body>
    <h1>Verifica disponibilità biciclette</h1>

    <label for="id_stazione">ID stazione:</label>
    <input type="number" id="id_stazione" min="1">
    <button id="btnVerifica">Verifica</button>

    <div id="risultato"></div>

    <script>
    document.getElementById("btnVerifica").addEventListener("click", async function () {
        const id = document.getElementById("id_stazione").value;
        const res = await fetch("disponibilita_stazione.php?id_stazione=" + encodeURIComponent(id));
        const data = await res.json();

        const box = document.getElementById("risultato");

        if (!data.ok) {
            box.innerHTML = "<p>" + data.messaggio + "</p>";
            return;
        }

        box.innerHTML =
            "<p>Stazione: " + data.nome + "</p>" +
            "<p>Biciclette disponibili: " + data.bici_disponibili + "</p>" +
            "<p>Slot liberi: " + data.slot_liberi + "</p>" +
            "<p>Esito: " + (data.noleggio_possibile ? "noleggio possibile" : "nessuna bici disponibile") + "</p>";
    });
    </script>
</body>
</html>
```

---

5. QUESITO I – REPORT PERIODICO UTENTE

---

La traccia chiede di integrare il progetto con pagine per un report contenente:

* bici noleggiate da un utente,
* stazioni di prelievo e restituzione,
* durata,
* costi,
  e di discutere l’invio periodico automatico in base a una temporizzazione impostata dall’utente. 

5.1 Pagine da aggiungere

Area utente

A. Pagina “Storico noleggi”
Campi visualizzati:

* data e ora prelievo
* stazione prelievo
* data e ora riconsegna
* stazione riconsegna
* bici utilizzata
* durata
* costo

Filtri:

* mese
* intervallo date
* solo noleggi conclusi

B. Pagina “Preferenze report”
Campi:

* frequenza invio:

  * settimanale
  * mensile
  * trimestrale
* formato:

  * email HTML
  * PDF allegato
* indirizzo email di recapito
* consenso ricezione report

Tabella aggiuntiva proposta:

PREFERENZA_REPORT(
id_preferenza PK,
id_utente FK -> UTENTE(id_utente),
frequenza,
formato,
email_destinazione,
attivo,
ultimo_invio,
prossimo_invio
)

5.2 Produzione del report

Il report si genera interrogando NOLEGGIO con join verso:

* BICICLETTA
* STAZIONE come prelievo
* STAZIONE come riconsegna

Campi derivati:

* durata = data_ora_riconsegna - data_ora_prelievo
* costo = costo_calcolato

5.3 Invio periodico automatico

Problema

L’invio automatico non va fatto direttamente durante il login o durante la consultazione di una pagina, perché:

* aumenterebbe i tempi di risposta;
* rischierebbe invii duplicati;
* sarebbe fragile in caso di errori email.

Soluzione corretta

Usare uno scheduler centrale, per esempio:

* cron job;
* task scheduler applicativo;
* coda di job asincroni.

Flusso proposto

1. Un processo schedulato gira periodicamente, ad esempio ogni 15 minuti.
2. Cerca gli utenti con report attivo e prossimo_invio <= adesso.
3. Genera il report.
4. Lo invia via email.
5. Registra esito invio.
6. Aggiorna ultimo_invio e prossimo_invio.

Tabella consigliata per audit:

LOG_INVIO_REPORT(
id_log PK,
id_utente FK -> UTENTE(id_utente),
data_ora_tentativo,
esito,
messaggio,
periodo_da,
periodo_a
)

Vantaggi

* robustezza;
* tracciabilità;
* niente duplicazioni;
* gestione dei retry;
* migliore separazione tra frontend e processi batch.

---

6. QUESITO II – QUERY SQL

---

La traccia chiede:
a) dato il codice di una bicicletta, elencare gli utenti che l’hanno utilizzata nel mese corrente;
b) mostrare la stazione presso la quale è stato effettuato il maggior numero di noleggi in un dato periodo. 

Si assumono:

* codice bici = BICICLETTA.id_bici oppure codice_rfid; qui si usa id_bici come parametro;
* “mese corrente” = dal primo giorno del mese corrente fino al primo giorno del mese successivo.

6.1 Query a

Versione SQL standard ragionevole:

```
SELECT DISTINCT
    u.id_utente,
    u.nome,
    u.cognome,
    u.email
FROM NOLEGGIO n
JOIN UTENTE u
    ON u.id_utente = n.id_utente
WHERE n.id_bici = :id_bici
  AND n.data_ora_prelievo >= DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')
  AND n.data_ora_prelievo < DATE_FORMAT(DATE_ADD(CURRENT_DATE, INTERVAL 1 MONTH), '%Y-%m-01')
ORDER BY u.cognome, u.nome;
```

Se si preferisce filtrare sul codice RFID:

```
SELECT DISTINCT
    u.id_utente,
    u.nome,
    u.cognome,
    u.email
FROM NOLEGGIO n
JOIN UTENTE u
    ON u.id_utente = n.id_utente
JOIN BICICLETTA b
    ON b.id_bici = n.id_bici
WHERE b.codice_rfid = :codice_rfid
  AND n.data_ora_prelievo >= DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')
  AND n.data_ora_prelievo < DATE_FORMAT(DATE_ADD(CURRENT_DATE, INTERVAL 1 MONTH), '%Y-%m-01')
ORDER BY u.cognome, u.nome;
```

6.2 Query b

Si assume che il periodo sia definito da due parametri:

* :data_inizio
* :data_fine

Query:

```
SELECT
    s.id_stazione,
    s.nome,
    COUNT(*) AS numero_noleggi
FROM NOLEGGIO n
JOIN STAZIONE s
    ON s.id_stazione = n.id_stazione_prelievo
WHERE n.data_ora_prelievo >= :data_inizio
  AND n.data_ora_prelievo < :data_fine
GROUP BY s.id_stazione, s.nome
ORDER BY numero_noleggi DESC
LIMIT 1;
```

Se si volessero gestire ex aequo, invece di LIMIT 1 si potrebbe usare una sottoquery con MAX.

---

7. OSSERVAZIONI SULL’INTEGRITÀ DEL SISTEMA

---

Per evitare errori logici:

1. Noleggio

   * transazione atomica:

     * verifica utente;
     * verifica disponibilità bici;
     * sblocco;
     * registrazione noleggio aperto;
     * aggiornamento slot.

2. Riconsegna

   * transazione atomica:

     * lettura RFID;
     * verifica noleggio aperto della bici;
     * blocco meccanico;
     * chiusura noleggio;
     * aggiornamento slot;
     * calcolo costo.

3. Concorrenza

   * locking sul record bici/slot;
   * vincoli su noleggio aperto.

4. Sicurezza

   * autenticazione forte per i gestori;
   * cifratura TLS;
   * VPN per le stazioni;
   * tokenizzazione dei dati di pagamento;
   * log e audit trail.


---  
Hai ragione. Di seguito una versione molto più sintetica, in stile risposta da compito, inseribile direttamente in coda alla precedente.

---

9. QUESITO III – NORMALIZZAZIONE DELLA RELAZIONE QUADRO

---

Si consideri la relazione:

QUADRO(
Cod_Quadro,
Cod_Museo,
Titolo_Quadro,
Nome_Museo,
Citta_Museo,
Prezzo,
DataInizioEsposizione,
DataFineEsposizione
)

La relazione è in prima forma normale, perché tutti gli attributi sono atomici.
Non è però in seconda né in terza forma normale.

Infatti si possono assumere le seguenti dipendenze funzionali:

```
Cod_Quadro -> Titolo_Quadro
Cod_Museo -> Nome_Museo, Citta_Museo
(Cod_Quadro, Cod_Museo, DataInizioEsposizione) -> DataFineEsposizione, Prezzo
```

Assumendo come chiave composta:

```
(Cod_Quadro, Cod_Museo, DataInizioEsposizione)
```

si osserva che Titolo_Quadro dipende solo da Cod_Quadro, mentre Nome_Museo e Citta_Museo dipendono solo da Cod_Museo.
Sono quindi presenti dipendenze parziali dalla chiave composta, e questo viola la seconda forma normale.
La relazione presenta inoltre ridondanze e anomalie di aggiornamento, inserimento e cancellazione.

Una decomposizione corretta in terza forma normale è la seguente:

```
QUADRO(
    Cod_Quadro PK,
    Titolo_Quadro
)

MUSEO(
    Cod_Museo PK,
    Nome_Museo,
    Citta_Museo
)

ESPOSIZIONE(
    Cod_Quadro FK,
    Cod_Museo FK,
    DataInizioEsposizione,
    DataFineEsposizione,
    Prezzo,
    PRIMARY KEY (Cod_Quadro, Cod_Museo, DataInizioEsposizione)
)
```

In questo modo ogni attributo dipende dalla chiave della propria relazione, da tutta la chiave e solo dalla chiave, lo schema risultante è quindi in terza forma normale. 

---

10. QUESITO IV – AUTENTICAZIONE DEGLI UTENTI IN RETE


L’autenticazione serve a verificare l’identità di un utente che accede a un sistema di rete.
Le principali tecniche si basano su tre fattori:

* qualcosa che l’utente conosce, ad esempio password o PIN;
* qualcosa che possiede, ad esempio smart card, token OTP o smartphone;
* qualcosa che è, ad esempio impronta digitale o riconoscimento facciale.

La password è la tecnica più semplice ed economica, ma è anche la più debole, perché può essere intercettata, indovinata o sottratta con phishing.
Le tecniche basate sul possesso, come smart card o token, aumentano molto la sicurezza ma comportano costi maggiori e la gestione di smarrimenti o sostituzioni.
La biometria è comoda, ma presenta problemi di privacy e non è facilmente revocabile in caso di compromissione.

Per questo oggi si preferisce l’autenticazione multifattore, che combina almeno due fattori, ad esempio password più OTP.
Questa soluzione è molto più sicura della sola password.

Nei sistemi di rete si usano spesso protocolli e sistemi centralizzati come:

* LDAP o Active Directory, per la gestione centralizzata degli utenti;
* Kerberos, basato su ticket e adatto al single sign-on;
* RADIUS, usato per accessi di rete, Wi-Fi enterprise e VPN;
* 802.1X, per il controllo di accesso a rete cablata e wireless;
* SAML e OpenID Connect, diffusi nelle applicazioni web e cloud.

In conclusione, la sola password oggi non è sufficiente per sistemi esposti o dati sensibili.
La soluzione più efficace consiste nell’unire autenticazione multifattore, protocolli sicuri, cifratura delle comunicazioni e gestione centralizzata delle identità. 


---

8. CONCLUSIONE


La soluzione proposta:

* realizza un’architettura centralizzata con stazioni periferiche intelligenti ma leggere;
* garantisce trasmissione in tempo reale con tolleranza ai guasti;
* consente di conoscere in ogni momento chi ha in uso una bici;
* modella correttamente utenti, biciclette, stazioni, slot e noleggi;
* permette sia la consultazione pubblica della disponibilità sia il controllo gestionale delle bici in uso;
* integra la reportistica periodica automatica;
* fornisce query SQL aderenti ai requisiti.

