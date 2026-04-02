# Architetture N-Tier e Java Enterprise Edition

## 1. Perché nascono le architetture n-tier

Nei primi sistemi informatici aziendali molte applicazioni erano **monolitiche**: tutta la logica era contenuta in un unico programma che gestiva interfaccia utente, logica applicativa e accesso ai dati.

Questo modello presenta vari limiti:

* difficile manutenzione
* scarsa scalabilità
* forte accoppiamento tra componenti
* difficoltà nel riuso del codice

Con l’aumento della complessità dei sistemi informativi aziendali è diventato necessario **separare le responsabilità** dell’applicazione.
Nascono così le **architetture multi-tier (n-tier)**.

---

# 2. Che cosa significa architettura n-tier

Una **architettura n-tier** divide un’applicazione in **livelli logici separati**, ognuno responsabile di una parte specifica del sistema.

I livelli possono essere eseguiti:

* sullo stesso computer
* su server diversi
* su infrastrutture distribuite

Il numero dei livelli può variare (n-tier), ma il modello più comune è quello **a tre livelli**.

---

# 3. Architettura a tre livelli (3-tier)

## Presentation tier

Gestisce l’interazione con l’utente.

Componenti tipici:

* pagine HTML
* interfacce web
* applicazioni mobile
* frontend Javascript

Responsabilità principali:

* mostrare i dati
* raccogliere input
* inviare richieste al livello applicativo

---

## Application tier (business logic)

Contiene la **logica dell’applicazione**.

Esempi di responsabilità:

* validazione dei dati
* implementazione delle regole di business
* coordinamento delle operazioni
* gestione delle transazioni

Questo livello è spesso implementato tramite **application server**.

---

## Data tier

Gestisce la **persistenza dei dati**.

Componenti tipici:

* database relazionali
* database NoSQL
* sistemi di storage

Responsabilità:

* memorizzazione dei dati
* recupero delle informazioni
* gestione dell’integrità dei dati

---

# 4. Vantaggi delle architetture n-tier

Separazione delle responsabilità
Ogni livello ha un compito preciso.

Scalabilità
È possibile aumentare le risorse solo nei livelli più utilizzati.

Manutenibilità
Il codice è più modulare.

Riutilizzo
La logica applicativa può essere usata da più interfacce.

Distribuzione
I livelli possono essere distribuiti su macchine diverse.

---

# Java Enterprise Edition

## 5. Che cos’è Java Enterprise Edition

**Java Enterprise Edition (Java EE)** è una piattaforma per lo sviluppo di **applicazioni enterprise distribuite**.

Dal 2018 il progetto è stato trasferito alla Eclipse Foundation e oggi prende il nome di:

**Jakarta EE**

La piattaforma fornisce:

* API standard
* servizi infrastrutturali
* componenti riutilizzabili

per facilitare lo sviluppo di sistemi n-tier.

---

# 6. Componenti principali della piattaforma

Tra le tecnologie principali della piattaforma:

Servlet
Gestione delle richieste HTTP.

JSP (Java Server Pages)
Generazione dinamica di pagine web.

EJB (Enterprise Java Beans)
Componenti per la logica applicativa.

JPA (Java Persistence API)
Gestione della persistenza dei dati.

JTA
Gestione delle transazioni.

---

# Application Server

## 7. Che cos’è un application server

Un **application server** è un software che esegue applicazioni enterprise e fornisce servizi infrastrutturali.

Si tratta di un **ambiente di esecuzione specializzato** per applicazioni distribuite.

Un application server gestisce automaticamente vari aspetti infrastrutturali,
quindi secondari dal punto di vista del business, ma tecnicamente importanti e complessi da gestire manualmente:

---

**Sicurezza**
L’application server controlla automaticamente chi può accedere a una applicazione o a una specifica funzione.
Esempio: un utente autenticato come **amministratore** può accedere alla pagina di gestione degli utenti, mentre un utente normale può solo visualizzare i propri dati.

---

**Transazioni**
L’application server garantisce che una serie di operazioni sul database venga eseguita completamente oppure annullata se si verifica un errore.
Esempio: durante un bonifico bancario devono essere eseguite due operazioni (prelievo da un conto e accredito su un altro); se la seconda operazione fallisce, la prima viene annullata automaticamente.

---

**Gestione dei thread**
L’application server gestisce i thread necessari per servire più richieste contemporaneamente senza che il programmatore debba crearli manualmente.
Esempio: cento utenti aprono contemporaneamente la stessa applicazione web e il server assegna automaticamente thread diversi per gestire le richieste.

---

**Pool di connessioni al database**
L’application server mantiene un insieme di connessioni già aperte verso il database e le riutilizza quando servono, evitando di crearle ogni volta.
Esempio: invece di aprire e chiudere una connessione al database per ogni richiesta web, l’application server riutilizza una delle connessioni disponibili nel pool.

---

**Gestione delle risorse**
L’application server gestisce in modo centralizzato risorse come connessioni a database, file, servizi esterni o code di messaggi.
Esempio: l’indirizzo del database o le credenziali di accesso vengono configurati nel server e tutte le applicazioni li utilizzano senza doverli definire nel codice.

---

**Comunicazione tra componenti**
L’application server fornisce meccanismi standard per far comunicare tra loro i diversi componenti dell’applicazione.
Esempio: un servlet può chiamare direttamente un **Enterprise Bean** per eseguire la logica applicativa senza doversi occupare dei dettagli della comunicazione tra oggetti distribuiti.


---

**Questo permette agli sviluppatori di concentrarsi sulla logica applicativa.**

---

# 8. Differenza tra web server e application server

Un **web server** gestisce principalmente:

* richieste HTTP
* contenuti statici
* pagine web

Un **application server** gestisce anche:

* componenti applicativi
* logica di business
* accesso ai database
* sicurezza applicativa
* transazioni

Molti application server includono anche un web server o, piu' spesso, container.

---

# 9. Application server diffusi

Apache Tomcat
[https://tomcat.apache.org/](https://tomcat.apache.org/)

WildFly (ex JBoss)
[https://www.wildfly.org/](https://www.wildfly.org/)

GlassFish
[https://glassfish.org/](https://glassfish.org/)

Payara
[https://www.payara.fish/](https://www.payara.fish/)

---

# Enterprise Java Beans

## 10. Che cosa sono gli Enterprise Beans

Gli **Enterprise Java Beans (EJB)** sono componenti software utilizzati per implementare la **business logic** nelle applicazioni enterprise.

Un bean è un **oggetto gestito dal container dell’application server**.

Il container fornisce automaticamente:

* gestione delle transazioni
* sicurezza
* gestione della concorrenza
* lifecycle management
* pooling delle istanze

---

# Tipologie di Enterprise Beans

## 11. Session Beans

I **Session Beans** implementano servizi di business.

Esistono tre tipi principali.

---

### Stateless Session Bean

Non mantengono stato tra le richieste.

Caratteristiche:

* ogni richiesta è indipendente
* il container può riutilizzare le istanze
* alta scalabilità

Esempi:

* servizi REST
* elaborazioni
* operazioni su database

---

### Stateful Session Bean

Mantengono lo stato tra più chiamate.

Caratteristiche:

* associati a uno specifico client
* conservano informazioni temporanee

Esempi:

* carrello di un e-commerce
* processi multi-step

---

### Singleton Session Bean

Esiste una sola istanza per tutta l’applicazione.

Esempi di utilizzo:

* configurazioni globali
* cache condivise
* servizi di inizializzazione

---

# 12. Message Driven Beans

I **Message Driven Beans (MDB)** sono utilizzati per elaborare messaggi asincroni.

Sono integrati con sistemi di messaging come:

JMS (Java Message Service)

Utilizzi tipici:

* sistemi di integrazione
* elaborazione di code di messaggi
* comunicazione tra sistemi distribuiti

---

# JPA – Java Persistence API

## 13. Che cos’è JPA

**JPA (Java Persistence API)** è la tecnologia standard di Java EE per la gestione della **persistenza dei dati**.

Permette di collegare **oggetti Java** alle **tabelle di un database relazionale**.

Questo approccio è chiamato:

**Object Relational Mapping (ORM)**.

L’ORM permette di lavorare con oggetti invece che con query SQL manuali.

---

## Benefici di JPA

Maggiore produttività
Riduce il codice necessario per accedere al database.

Astrazione dal database
Il codice è meno dipendente dal DB specifico.

Migliore integrazione con il modello a oggetti
**Le tabelle vengono rappresentate da classi Java.**

Gestione automatica delle transazioni.

---

## Differenze tra JPA e JDBC

JDBC è una API di basso livello per accedere ai database.

Con JDBC il programmatore deve:

* scrivere manualmente SQL
* gestire connessioni
* convertire risultati SQL in oggetti Java

Esempio di operazioni richieste:

* creare connessione
* creare statement
* eseguire query
* leggere ResultSet
* mappare i dati in oggetti

Con **JPA** invece:

* si definiscono classi che rappresentano le tabelle
* il framework genera molte operazioni automaticamente
* l’accesso ai dati avviene tramite oggetti

Questo riduce la quantità di codice e il rischio di errori.

---

# 14. Diagramma architettura JEE

Schema semplificato di una tipica architettura Java Enterprise.

Client
|
v
Presentation Layer
(HTML, JS, JSP, Servlet)
|
v
Application Server
|
+---------------------------+
|  Business Logic           |
|  Enterprise Beans (EJB)   |
+---------------------------+
|
v
Persistence Layer
(JPA)
|
v
Database

In questo modello:

* il client comunica con il livello di presentazione
* la logica applicativa è gestita dall’application server
* l’accesso ai dati è mediato da JPA

---

# 15. Esempio minimo di Session Bean

Esempio molto semplice di **Stateless Session Bean**.

Classe che fornisce un servizio di calcolo.

```
import jakarta.ejb.Stateless;

@Stateless
public class CalcoloService {

    public int somma(int a, int b) {
        return a + b;
    }

}
```

Significato del codice:

@Stateless
Indica che il bean è uno **Stateless Session Bean**.

Il container dell’application server:

* crea e gestisce le istanze
* gestisce concorrenza e lifecycle
* rende il bean disponibile ad altri componenti.

---

# 16. Utilizzo del bean da un altro componente

Un servlet o un altro componente può usare il bean tramite **injection**.

```
import jakarta.ejb.EJB;

public class TestBean {

    @EJB
    private CalcoloService service;

    public void esempio() {

        int risultato = service.somma(3, 5);

        System.out.println(risultato);

    }

}
```

Il container si occupa automaticamente di:

* creare il bean
* iniettarlo nella classe
* gestirne il ciclo di vita.

---

# 17. Architettura completa di una applicazione JEE

Una applicazione enterprise completa può essere organizzata così:

Client

↓

Presentation Layer
(Servlet, JSP, REST)

↓

Business Layer
(EJB, servizi applicativi)

↓

Persistence Layer
(JPA)

↓

Database

---

# 18. Evoluzione delle architetture enterprise

Negli ultimi anni molte applicazioni enterprise stanno evolvendo verso modelli come:

microservizi, containers (Docker) orchestrati (Kubernetes)
cloud computing

Tuttavia i concetti introdotti da Java EE rimangono fondamentali:

* separazione dei livelli
* container applicativi
* gestione delle transazioni
* componenti riutilizzabili
* accesso ai dati tramite ORM

---

## Alcuni riferimenti

Jakarta EE
[https://jakarta.ee/](https://jakarta.ee/)

Oracle Java EE overview
[https://www.oracle.com/java/technologies/java-ee-glance.html](https://www.oracle.com/java/technologies/java-ee-glance.html)

Apache Tomcat
[https://tomcat.apache.org/](https://tomcat.apache.org/)

WildFly
[https://www.wildfly.org/](https://www.wildfly.org/)

GlassFish
[https://glassfish.org/](https://glassfish.org/)

---

