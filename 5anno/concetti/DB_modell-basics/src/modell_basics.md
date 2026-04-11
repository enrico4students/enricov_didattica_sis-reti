
---

# Modellazione dei database – dalle basi al modello ER

* concetti fondamentali della modellazione ER
* criteri pratici per distinguere entità, relazioni e attributi
* un procedimento per passare dal testo al modello ER
* gli errori più comuni
* un metodo di verifica del modello

---

# 1. Concetti fondamentali del modello ER

## Entità

Una **entità** rappresenta un oggetto o concetto del dominio reale che ha **identità propria** nel sistema.

Caratteristiche tipiche:

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

Esempio: Studente — segue — Corso

Una relazione: 
* collega entità
* può avere cardinalità
* può avere attributi (in alcuni casi)

---

# 2. Individuare entità e relazioni

Un metodo molto usato consiste nell'analizzare il testo del problema.

Regola pratica:

sostantivi → entità
verbi → relazioni
proprietà → attributi

Esempio.

Frase:

Uno studente si iscrive a un corso.

Analisi:

studente → entità
corso → entità
si iscrive → relazione

---

# 3. Quando qualcosa diventa una entità invece che una relazione

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

---

# 4. Test pratici usati nella progettazione

Quando non è chiaro come modellare un concetto si possono usare alcuni **test mentali**.

## Test dell’identità

Questo oggetto ha una identità propria?

Se sì → probabilmente è una entità.

---

## Test dell’esistenza indipendente

Può esistere da solo nel sistema?

Se sì → entità.

Se esiste solo come collegamento → relazione.

---

## Test degli attributi

Questo concetto ha molti attributi propri?

Se sì → spesso diventa una entità.

---

## Test dell’evento

Rappresenta un evento nel tempo?

Molti eventi diventano entità.

Esempi:

* prenotazione
* pagamento
* iscrizione
* ordine

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

Le relazioni N:M spesso diventano entità associative.

---

## Passo 7 – verificare il modello

Controllare che il modello rappresenti correttamente il sistema reale.

---

# 6. Esempio completo di modellazione

## Testo

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

La modellazione ER è uno strumento fondamentale per progettare correttamente un database.

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

Se lo si desidera, nel passo successivo si può anche creare:

* una **versione migliorata per studenti di 16-17 anni**, più didattica
* oppure **una seconda lezione** su come trasformare il **modello ER nello schema relazionale** (passaggio tipico nei compiti di basi di dati).
