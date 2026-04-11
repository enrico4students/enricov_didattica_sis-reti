
---

# Modellazione database – Concetti Base e aspetti pratici


---

# 1. Concetti fondamentali del modello ER

## Entità

Una **entità** rappresenta un oggetto o concetto del dominio reale che ha **identità propria** nel sistema.

Caratteristiche **tipiche**:

* può essere identificata con una chiave
* possiede attributi
* può essere referenziata da altre entità

Esempi: Studente, Cliente, Prodotto, Camera, Corso

## Attributi
Gli **attributi** sono proprietà che descrivono una entità.  
non hanno identità autonoma.

Esempio di entità: **Studente**, attributi:  
* matricola
* nome
* cognome
* email


---

## Relazioni

Una **relazione** rappresenta un legame tra due o più entità.

Esempio: Studente — **segue** — Corso

Una relazione: 
* collega entità
* può avere cardinalità
* può avere attributi (in alcuni casi)

---

# 2. Individuare entità e relazioni

Un metodo molto usato consiste nell'analizzare il testo del problema.

Regola pratica (NB ipersemplificazione iniziale):

- sostantivi → entità  
- proprietà → attributi  
- verbi → relazioni  

Esempio "Uno studente si iscrive a un corso"

- studente → entità  
- corso → entità  
- si iscrive → relazione  

---

# 3. Entità (associativa) o Relazione, that is the question

Molte volte un concetto può essere modellato in due modi diversi.

Il criterio principale è questo:

se il legame ha **informazioni proprie importanti**, diventa una **entità associativa**.

---

## Esempio

Studente — segue — Corso

Se non servono altri dati, la relazione è sufficiente.

Ma spesso bisogna memorizzare:

* data iscrizione
* voto
* stato

In questo caso si introduce una entità:

Iscrizione

Schema:

Studente
Corso
Iscrizione

Relazioni:

Studente — effettua — Iscrizione
Corso — riguarda — Iscrizione

### Entità o Relazione - Approfondimento


Nella modellazione dei database (in particolare nel modello ER), **la scelta tra entità e relazione può dipendere dal contesto, dal punto di vista e dal livello di dettaglio desiderato**. Non è una decisione arbitraria, ma esistono criteri abbastanza consolidati nella letteratura.

---

#### Principio generale: dipendenza dal contesto

Nel modello ER introdotto da Peter Chen, si assume che:

* il modello rappresenta **una realtà osservata**
* ma **la realtà può essere descritta a diversi livelli di astrazione**

Di conseguenza:

* qualcosa può essere modellato come **entità autonoma**
* oppure come **relazione tra altre entità**

→ dipende da **come si vuole descrivere il dominio**

---

#### Caso tipico: relazione che diventa entità

##### Esempio classico

Relazione:

* Studente — frequenta — Corso

Se si considera solo il fatto che uno studente frequenta un corso:

* "frequenta" è una **relazione**

Ma se si introducono attributi:

* data iscrizione
* voto finale
* stato (attivo, ritirato)

allora:

→ la relazione diventa una **entità associativa**

Nuovo modello:

* Studente
* Corso
* Iscrizione (entità)

---

#### Criteri pratici (derivati dalla letteratura)

##### Presenza di **attributi propri**  

Se un elemento ha attributi significativi:

* conviene modellarlo come **entità**

Esempio:

* “Contratto” tra Azienda e Dipendente
  → ha data, tipo, durata → entità

Domanda pratica: "Questo concetto ha molti attributi propri?"  
Se sì → spesso diventa una entità.  

---

##### Identità **autonoma**

Se qualcosa:

* può essere identificato indipendentemente
* ha un proprio identificatore

→ è tipicamente una **entità**


Quando non è chiaro come modellare un concetto si possono usare alcuni **test mentali**.

Domanda pratica: "Questo oggetto ha una identità propria?"
Se sì → probabilmente è una entità.


##### Esistenza indipendente

Domanda Pratica: "Può esistere da solo nel sistema?"
- Se sì → può essere entità.  
- Se esiste solo come collegamento → relazione.


---

##### Stabilità nel tempo

Se l’oggetto:

* ha una propria esistenza nel tempo
* può essere modificato indipendentemente

→ entità

---

##### Cardinalità complessa

Se una relazione:

* è molti-a-molti
* e ha semantica ricca

→ spesso diventa entità

---

##### Ruolo semantico nel dominio

Qui entra il **punto di vista**, ricodiamo che un modello è una rappresentazione semplificata della realtà, sviluppato da un determinato punto di vista:

* in un sistema semplice → relazione
* in un sistema gestionale complesso → entità

Esempio:

* “Prenotazione”

  * in un sistema minimale → relazione Cliente–Hotel
  * in un sistema reale → entità centrale

---

##### Test dell’evento

Domanda pratica: "Rappresenta un evento nel tempo?"

Molti eventi diventano entità.

Esempi:

* prenotazione
* pagamento
* iscrizione
* ordine


---  

#### Formalizzazione nella letteratura

Questi concetti sono trattati in:

##### Testo ""Database System Concepts"

* parla di **entity sets vs relationship sets**
* introduce il concetto di **aggregation** e **associative entity**

---

##### Testo "Fundamentals of Database Systems"

* esplicita chiaramente:

  * quando una relazione deve diventare entità
  * il concetto di **weak entity** e **associative entity**

---

##### Testo "Database design"

* sottolinea che il modello ER è:

  * **concettuale**
  * **dipendente dai requisiti**

---

#### Regola operativa sintetica

Si può sintetizzare così:

* Se serve solo collegare → relazione
* Se serve descrivere → entità

oppure in forma più tecnica:

* relazione = legame
* entità = oggetto con identità + attributi

---

#### NB non esiste una scelta “assolutamente giusta”

Questo perchè i modelli sono fatti da deterinati punti di vista e non sono **assoluti**

Due modellazioni diverse possono essere entrambe corrette se:

* soddisfano i requisiti
* sono coerenti internamente

Questo è un punto fondamentale:

→ la modellazione ER **non è unica**

---

#### Caso reale

Sistema eventi sportivi:

* Utente — partecipa — Evento

Versione semplice:

* relazione

Versione reale:

* Partecipazione:

  * ruolo (portiere, attaccante)
  * skill
  * stato (confermato, lista attesa)

→ diventa entità

---

#### Entità o Relazione - Conclusione

La scelta dipende da:

* livello di dettaglio
* requisiti applicativi
* punto di vista

Ma non è arbitraria:




---

# 5. Procedura in 7 passi per costruire un modello ER

Durante gli esercizi è utile seguire un procedimento sistematico.

## Passo 1 – leggere il dominio applicativo

Analizzare il testo e individuare i concetti principali.

---

## Passo 2 – individuare le entità candidate

Selezionare gli oggetti che hanno identità propria.

---

## Passo 3 – identificare gli attributi

Per ogni entità individuare le proprietà descrittive.

---

## Passo 4 – individuare le relazioni

Osservare i verbi che collegano le entità.

---

## Passo 5 – determinare le cardinalità

Stabilire quante istanze di una entità possono essere collegate a un’altra.

---

## Passo 6 – gestire le relazioni molti-a-molti

Le relazioni N:M spesso, non sempre, diventano entità associative.

---

## Passo 7 – verificare il modello

Controllare che il modello rappresenti correttamente il sistema reale.

---

# 6. Esempio completo di modellazione

## Descrizione realtà da modellare  

Una biblioteca gestisce utenti e libri.
Gli utenti possono prendere in prestito i libri.

Per ogni prestito si registrano:

* data prestito
* data restituzione prevista
* data restituzione effettiva.

---

## Individuazione delle entità

Utente
Libro
Prestito

---

## Attributi

Utente

* idUtente
* nome
* email

Libro

* ISBN
* titolo
* autore

Prestito

* dataPrestito
* dataRestituzionePrevista
* dataRestituzioneEffettiva

---

## Relazioni

Utente — effettua — Prestito
Libro — riguarda — Prestito

---

## Cardinalità

Utente (1) → (N) Prestito
Libro (1) → (N) Prestito

---

# 7. Entità deboli

Una **entità debole** non può esistere senza un’altra entità.

Esempio.

Ordine
RigaOrdine

Una riga d’ordine esiste solo all’interno di un ordine.

La chiave della riga è composta da:

* idOrdine
* numeroRiga

---

# 8. Gerarchie (generalizzazione)

Il modello ER permette di rappresentare **sottotipi di entità**.

Esempio.

Docente

sottotipi

* ProfessoreOrdinario
* ProfessoreContratto

Il sottotipo può avere attributi aggiuntivi.

Esempio.

ProfessoreContratto

* aziendaProvenienza

---

# 9. Errori molto comuni nella modellazione

## Modellare attributi come entità

Errore:

Studente — ha — Nome

Nome deve essere un attributo.

---

## Modellare entità come attributi

Errore:

Studente

* nome
* corso

Corso deve essere entità.

---

## Modellare eventi come semplici relazioni

Errore:

Cliente — prenota — Camera

Se la prenotazione ha dati propri deve diventare entità.

---

## Inserire attributi nella entità sbagliata

Errore:

Studente

* voto

Il voto appartiene all’esame o all’iscrizione.

---

# 10. Metodo professionale di verifica

## Test delle domande operative

Dopo aver costruito il modello si formulano domande realistiche che il sistema deve supportare.

Se il modello permette di rispondere facilmente, la progettazione è probabilmente corretta.

---

### Esempio

Sistema universitario.

Entità:

Studente
Corso
Iscrizione

---

Domande.

Quali corsi segue uno studente?

Studente → Iscrizione → Corso

---

Quali studenti seguono un corso?

Corso → Iscrizione → Studente

---

Quale voto ha ottenuto uno studente in un corso?

Studente → Iscrizione → voto

---

Se il modello permette di rispondere a tutte queste domande, è corretto.

---

# 11. Regole pratiche da ricordare

Oggetti del sistema → entità

Proprietà → attributi

Legami tra oggetti → relazioni

Eventi con dati propri → entità associative

Oggetti che dipendono da altri → entità deboli

Tipi diversi dello stesso oggetto → gerarchie

---

# 12. Conclusione

Il processo tipico è:

analisi del dominio
costruzione del modello ER
verifica con domande operative
raffinamento del modello

La progettazione è quasi sempre **iterativa**: il modello viene migliorato progressivamente fino a rappresentare correttamente il sistema.

---

## Alcuni riferimenti

Database System Concepts – Silberschatz, Korth, Sudarshan
[https://www.db-book.com](https://www.db-book.com)

Fundamentals of Database Systems – Elmasri, Navathe
[https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003458](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003458)

Stanford Databases Course
[https://online.stanford.edu/courses/soe-ydatabases-databases](https://online.stanford.edu/courses/soe-ydatabases-databases)

---
