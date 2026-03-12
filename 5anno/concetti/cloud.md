
---

# Cloud Computing Overview

## 1. Che cos’è il Cloud Computing

Il **cloud computing** è un modello di erogazione di risorse informatiche tramite Internet.
Invece di possedere fisicamente server, storage e reti, si utilizzano infrastrutture remote messe a disposizione da grandi provider. Secondo il National Institute of Standards and Technology (NIST), il cloud è un modello che consente accesso on-demand a risorse configurabili (rete, server, storage, applicazioni) rapidamente attivabili e rilasciabili. ([Google Cloud][1])

Caratteristiche fondamentali:

* Accesso via rete
* Scalabilità elastica
* Pagamento a consumo
* Provisioning rapido
* Gestione centralizzata

---

# 2. Modelli di servizio  

## 2.1 IaaS – Infrastructure as a Service

Nel modello IaaS il provider fornisce **infrastruttura virtuale**. ([Google Cloud][2])

### Cosa trova disponibile il cliente all’istante zero

Appena creato l’account sono disponibili:

* Console di gestione web
* API di automazione
* Catalogo di immagini di sistemi operativi (Linux, Windows)
* Creazione di macchine virtuali
* Reti virtuali configurabili
* Firewall virtuali
* Storage a blocchi e oggetti

Non è presente alcuna applicazione pronta: esiste solo l’infrastruttura.

### Offerte IaaS attualmente disponibili

* **Amazon EC2 (Elastic Compute Cloud)** – servizio per creare e gestire macchine virtuali nel cloud AWS: [https://aws.amazon.com/it/ec2/](https://aws.amazon.com/it/ec2/) ([Amazon Web Services, Inc.][3])
* **Microsoft Azure Virtual Machines** – macchine virtuali scalabili su Azure: [https://azure.microsoft.com/it-it/services/virtual-machines/](https://azure.microsoft.com/it-it/services/virtual-machines/)
* **Google Compute Engine** – macchine virtuali on demand con pagamento a consumo: [https://cloud.google.com/compute](https://cloud.google.com/compute)

---

### Uso tipico: pubblicare un sito web su una macchina virtuale

Passi fondamentali:

1. Creare una macchina virtuale scegliendo sistema operativo e dimensione (CPU/RAM).
2. Configurare rete e regole firewall (aprire porta 80/443).
3. Collegarsi via SSH o RDP.
4. Installare manualmente un web server (es. Apache o Nginx).
5. Caricare il codice del sito.
6. Associare eventualmente un IP pubblico o un DNS.

Il cliente gestisce:

* Sistema operativo
* Aggiornamenti
* Sicurezza applicativa

Responsabilità elevata, massima flessibilità.

---

## 2.2 PaaS – Platform as a Service

Nel modello PaaS il provider fornisce una **piattaforma pronta per eseguire codice**. ([Google Cloud][2])

### Cosa trova disponibile il cliente all’istante zero

Appena attivato il servizio sono già presenti:

* Sistema operativo gestito
* Runtime (es. Python, Node, Java, .NET)
* Server web configurato
* Scalabilità automatica
* Monitoraggio integrato
* Log centralizzati

Non si gestiscono VM né patch di sistema.

### Offerte PaaS attualmente disponibili

* **Azure App Service (Microsoft)** – ambiente per eseguire app web e API: [https://azure.microsoft.com/it-it/services/app-service/](https://azure.microsoft.com/it-it/services/app-service/)
* **Google App Engine** – piattaforma PaaS per applicazioni scalabili: [https://cloud.google.com/appengine](https://cloud.google.com/appengine)
* **AWS Elastic Beanstalk** – servizio che automatizza creazione, deploy e scaling: [https://aws.amazon.com/elasticbeanstalk/](https://aws.amazon.com/elasticbeanstalk/) ([linkedin.com][4])

---

### Uso tipico: pubblicare un’applicazione web

Passi fondamentali:

1. Creare un servizio applicativo.
2. Scegliere linguaggio/runtime.
3. Caricare il codice tramite Git o interfaccia web.
4. Configurare variabili d’ambiente.
5. Attivare il deploy.

Il sistema:

* Avvia automaticamente il server
* Gestisce scaling
* Applica patch di sicurezza

Il cliente gestisce solo il codice e la logica applicativa.

---

## 2.3 SaaS – Software as a Service

Nel modello SaaS il software è completamente pronto all’uso. ([Google Cloud][2])

### Cosa trova disponibile il cliente all’istante zero

Subito disponibili:

* Applicazione accessibile via browser
* Autenticazione utenti
* Spazio di archiviazione
* Aggiornamenti automatici
* Backup gestiti dal provider

Non è possibile modificare l’infrastruttura sottostante.

### Offerte SaaS attualmente disponibili

* **Google Workspace** (posta, documenti, calendario) – [https://workspace.google.com/](https://workspace.google.com/)
* **Microsoft 365** (posta e office online) – [https://www.microsoft.com/it-it/microsoft-365](https://www.microsoft.com/it-it/microsoft-365)
* **Salesforce CRM** – [https://www.salesforce.com/it/](https://www.salesforce.com/it/) (esempio di SaaS enterprise)

---

### Uso tipico: attivare un ambiente di posta aziendale

Passi fondamentali:

1. Registrare dominio aziendale.
2. Creare account utenti.
3. Configurare record DNS.
4. Assegnare licenze.
5. Accedere via browser o client.

Nessuna gestione server.

---

## 2.4 FaaS – Function as a Service (Serverless)

Modello in cui si eseguono singole funzioni senza gestire server. ([Kinsta®][5])

### Cosa trova disponibile il cliente all’istante zero

* Ambiente di esecuzione già configurato
* Trigger automatici (HTTP, eventi, code)
* Scalabilità automatica
* Logging integrato

Non esistono macchine virtuali visibili.

### Offerte FaaS attualmente disponibili

* **AWS Lambda** – esecuzione di funzioni serverless: [https://aws.amazon.com/lambda/](https://aws.amazon.com/lambda/)
* **Azure Functions** – funzioni serverless su Azure: [https://azure.microsoft.com/it-it/services/functions/](https://azure.microsoft.com/it-it/services/functions/)
* **Google Cloud Functions** – esecuzione eventi serverless: [https://cloud.google.com/functions](https://cloud.google.com/functions)

---

### Uso tipico: API che elabora richieste HTTP

Passi fondamentali:

1. Scrivere una funzione.
2. Caricarla nel servizio serverless.
3. Collegarla a un endpoint HTTP.
4. Pubblicare l’URL.

Il sistema esegue la funzione solo quando viene chiamata.

---

Ecco la **versione delle sezioni “as a Service”** (HaaS, DaaS, DBaaS, STaaS, CaaS) *aggiornata e integrabile direttamente nella lezione*, **con collegamenti a offerte commerciali attualmente disponibili**.

---

# 2.5 HaaS – Hardware as a Service

HaaS indica un modello in cui **l’hardware fisico viene fornito come servizio** a fronte di un canone, senza acquisto diretto di dispositivi.

## Cosa trova disponibile il cliente all’istante zero

* Hardware fisico preconfigurato
* Installazione e consegna gestita
* Contratto di manutenzione e sostituzione guasti
* Aggiornamenti pianificati

## Uso tipico

Esempio: laboratorio scolastico con PC in noleggio.

Passi:

1. Definire requisiti hardware.
2. Sottoscrivere contratto di servizio.
3. Ricevere e installare i dispositivi.
4. Pagare canone periodico.
5. Sostituire dispositivi a fine ciclo.

## Offerte commerciali (esempi)

* **Microsoft Windows 365 Business (DaaS / HaaS correlato)** – desktop virtuali cloud con Windows gestito da Microsoft: [https://www.microsoft.com/it-it/windows-365/business/](https://www.microsoft.com/it-it/windows-365/business/) (modello simile a HaaS se integrato con dispositivi gestiti) ([Microsoft][1])
* Provider di HaaS tipici includono aziende che offrono leasing di server bare metal o PC come servizio (consultare fornitori locali o integratori).

*Nota:* HaaS **non** è sempre un’offerta cloud pura ma un modello commerciale di **noleggio hw + servizi**.

---

# 2.6 DaaS – Desktop as a Service

DaaS fornisce **desktop virtuali completi** nel cloud, accessibili via Internet.

## Cosa trova disponibile il cliente all’istante zero

* Desktop virtuale operativo
* Sistema operativo preconfigurato
* Accesso da browser o client
* Storage associato
* Gestione centralizzata utenti

## Uso tipico

Esempio: team in smart working.

Passi:

1. Creare desktop virtuali.
2. Assegnare credenziali.
3. Installare software aziendali.
4. Consentire accesso da qualsiasi device.

## Offerte commerciali

* **Windows 365 Cloud PC (Microsoft)** – Desktop virtuale Windows gestito nel cloud: [https://www.microsoft.com/it-it/windows-365/business/](https://www.microsoft.com/it-it/windows-365/business/) ([Microsoft][1])
* **vDesk.works Desktop DaaS** – Desktop cloud remoto pronto all’uso: [https://vdeskworks.com/offer-DaaS-save](https://vdeskworks.com/offer-DaaS-save) ([vDesk.works][2])
* **Azure Virtual Desktop (Microsoft)** – ambiente desktop virtuale scalabile su Azure: [https://azure.microsoft.com/it-it/services/virtual-desktop/](https://azure.microsoft.com/it-it/services/virtual-desktop/)

---

# 2.7 DBaaS – Database as a Service

DBaaS fornisce **database gestiti** senza che il cliente debba gestire server, patch o backup.

## Cosa trova disponibile il cliente all’istante zero

* Database pronto all’uso (SQL o NoSQL)
* Backup automatici
* Replica e alta disponibilità
* Monitoraggio integrato

## Uso tipico

Esempio: applicazione web con database relazionale.

Passi:

1. Creare istanza database.
2. Configurare utenti e permessi.
3. Collegare l’applicazione al DB.
4. Attivare scaling automatico.

## Offerte commerciali

* **Amazon Relational Database Service (RDS)** – database relazionale gestito da AWS: [https://aws.amazon.com/rds/](https://aws.amazon.com/rds/) ([Wikipedia][3])
* **Google Cloud Datastore (NoSQL DBaaS)** – database NoSQL scalabile: [https://cloud.google.com/datastore/](https://cloud.google.com/datastore/) ([Wikipedia][4])
* **Azure SQL Database** – database SQL completamente gestito su Microsoft Azure: [https://azure.microsoft.com/it-it/services/sql-database/](https://azure.microsoft.com/it-it/services/sql-database/)

---

# 2.8 STaaS – Storage as a Service

STaaS fornisce **spazio di archiviazione remoto scalabile** su richiesta via cloud.

## Cosa trova disponibile il cliente all’istante zero

* Storage configurabile
* Accesso via API o interfaccia di rete
* Replica e durabilità dei dati
* Elevata scalabilità

## Uso tipico

Esempio: backup aziendale o archiviazione di file multimediali.

Passi:

1. Creare bucket (object storage) o volume.
2. Configurare permessi.
3. Caricare i dati.
4. Impostare politiche di conservazione.

## Offerte commerciali

* **Amazon S3 (object storage)** – storage scalabile su AWS: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* **Google Cloud Storage** – storage di oggetti su Google Cloud: [https://cloud.google.com/storage](https://cloud.google.com/storage)
* **Azure Blob Storage** – storage oggetti su Microsoft Azure: [https://azure.microsoft.com/it-it/services/storage/blobs/](https://azure.microsoft.com/it-it/services/storage/blobs/)

---

# 2.9 CaaS – Container as a Service

CaaS fornisce **piattaforme per eseguire e orchestrare container** (es. Kubernetes) senza gestire server fisici.

## Cosa trova disponibile il cliente all’istante zero

* Cluster container gestito
* Orchestrazione (es. Kubernetes)
* Networking containerizzato
* Bilanciamento e scaling automatico

## Uso tipico

Esempio: applicazioni microservizi containerizzate.

Passi:

1. Creare immagini container.
2. Pubblicarle in un registry.
3. Distribuirle nel cluster.
4. Configurare autoscaling.

## Offerte commerciali

* **Google Kubernetes Engine (GKE)** – CaaS gestito su Google Cloud: [https://cloud.google.com/kubernetes-engine/](https://cloud.google.com/kubernetes-engine/) ([Google Cloud][5])
* **Azure Kubernetes Service (AKS)** – servizio Kubernetes gestito su Microsoft Azure: [https://azure.microsoft.com/it-it/services/kubernetes-service/](https://azure.microsoft.com/it-it/services/kubernetes-service/)
* **Amazon Elastic Kubernetes Service (EKS)** – Kubernetes gestito da AWS: [https://aws.amazon.com/eks/](https://aws.amazon.com/eks/)

---

Fonti generiche su modelli “as a Service”: definizioni e classificazioni nel cloud computing. ([Wikipedia][6])

[1]: https://www.microsoft.com/it-it/windows-365/business?utm_source=chatgpt.com "Windows 365 Business Cloud PC"
[2]: https://vdeskworks.com/offer-DaaS-save?utm_source=chatgpt.com "Desktop as a Service Provider DaaS | Cloud DaaS"
[3]: https://en.wikipedia.org/wiki/Amazon_Relational_Database_Service?utm_source=chatgpt.com "Amazon Relational Database Service"
[4]: https://en.wikipedia.org/wiki/Google_Cloud_Datastore?utm_source=chatgpt.com "Google Cloud Datastore"
[5]: https://cloud.google.com/discover/what-is-caas?hl=it&utm_source=chatgpt.com "Che cos'è Container as a Service (CaaS)?"
[6]: https://en.wikipedia.org/wiki/As_a_service?utm_source=chatgpt.com "As a service"

---

# Schema sintetico esteso

| Modello | Livello fornito | Gestione cliente     | Caso tipico       |
| ------- | --------------- | -------------------- | ----------------- |
| IaaS    | Infrastruttura  | SO + applicazioni    | VM con server web |
| PaaS    | Piattaforma     | Solo codice          | Deploy app        |
| SaaS    | Software        | Solo uso             | Posta elettronica |
| FaaS    | Funzione        | Solo funzione        | API serverless    |
| HaaS    | Hardware fisico | Uso e configurazione | Laboratorio PC    |
| DaaS    | Desktop remoto  | Uso desktop          | Smart working     |
| DBaaS   | Database        | Schema e dati        | App con DB        |
| STaaS   | Storage         | Gestione file        | Backup            |
| CaaS    | Container       | Container e servizi  | Microservizi      |

---

Aspetti chiave:  

Ogni modello “XaaS” indica quale livello dell’infrastruttura viene astratto e gestito dal provider.   

Più si sale nella pila dei servizi, 
minore è il controllo tecnico diretto, ma   
minore è anche la complessità gestionale per il cliente.  


---   

# 3. Specificità del Cloud

## 3.1 Region e Availability Zone

---

Il cloud è organizzato in:

* Region: aree geografiche (Europa, USA, Asia)
* Availability Zone: datacenter separati per alta affidabilità

Applicazioni possono essere replicate su più zone per garantire resilienza.

---

## 3.2 Storage nel Cloud

Esistono vari modelli di storage:

**Block storage**
È uno spazio disco virtuale che viene collegato a una macchina virtuale e visto dal sistema operativo come un normale disco.
Esempio: un server cloud utilizza un volume block storage per installare il sistema operativo e salvare il database.

**Object storage**
Memorizza i dati come oggetti indipendenti identificati da un ID e accessibili tramite rete, spesso tramite API HTTP.
Esempio: un sito web salva immagini o file degli utenti in un sistema di object storage accessibile tramite URL.

Esempio minimale di accesso ad un oggetto tramite HTTP (Java):

```
import java.io.InputStream;
import java.net.URL;

public class ReadObjectExample {

    public static void main(String[] args) throws Exception {

        // URL dell'oggetto salvato nello storage
        // esempio tipico: immagine salvata in un bucket
        String objectURL = "https://example-bucket.storage.example.com/foto1.jpg";

        // creazione dell'oggetto URL che rappresenta la risorsa remota
        URL url = new URL(objectURL);

        // apertura dello stream di lettura verso l'oggetto
        InputStream in = url.openStream();

        // lettura dei primi byte dell'oggetto
        int firstByte = in.read();

        // stampa del primo byte letto (solo come dimostrazione)
        System.out.println(firstByte);

        // chiusura dello stream
        in.close();
    }
}
```

si accede direttamente all’oggetto memorizzato nello storage tramite il suo **URL pubblico**, si leggono i dati come se fosse un normale stream di rete.

---

**File system distribuiti**
Sono file system accessibili da più server contemporaneamente e progettati per funzionare su molte macchine.
Esempio: più server di un’applicazione web condividono gli stessi file di configurazione o documenti tramite un file system distribuito.


---

## 3.3 Sicurezza e responsabilità condivisa

Nel cloud:

* Il provider protegge l’infrastruttura
* Il cliente configura accessi, permessi, cifratura

Strumenti tipici:

* IAM
* reti virtuali isolate
* firewall logici
* cifratura dati

Errore comune: dati pubblici involontari.

---

# 4. I principali provider

## 4.1 Amazon Web Services

Provider con il maggior numero di servizi cloud pubblici. ([CloudZero][6])

## 4.2 Microsoft Azure

Forte integrazione con ambienti Microsoft. ([CloudZero][6])

## 4.3 Google Cloud Platform

Particolarmente competente in IA e dati. ([CloudZero][6])

## 4.4 Alibaba Cloud

Leader in Asia. ([Info Data][7])

---

# 5. Concetti fondamentali da fissare

Nel cloud:

* Le risorse sono virtuali e distribuite.
* L’infrastruttura è organizzata in zone e region.
* Lo storage include object storage e altri modelli.
* La sicurezza è responsabilità condivisa.
* L’automazione è centrale.


---  

# Tipologie di Cloud (modelli di distribuzione)

Oltre ai modelli di servizio (IaaS, PaaS, SaaS, FaaS), il cloud si distingue anche per **modalità di distribuzione dell’infrastruttura**.

---

## 1. Public Cloud (Cloud pubblico)

È un’infrastruttura cloud di proprietà di un provider che offre servizi a più clienti contemporaneamente tramite Internet.

Caratteristiche:

* Infrastruttura condivisa tra più organizzazioni (multi-tenant)
* Elevata scalabilità
* Pagamento a consumo
* Nessuna gestione dell’hardware da parte del cliente

Esempi di provider pubblici:

* Amazon Web Services
* Microsoft Azure
* Google Cloud Platform

Uso tipico: startup, siti web pubblici, applicazioni scalabili.

---

## 2. Private Cloud (Cloud privato)

È un’infrastruttura cloud dedicata a una sola organizzazione.

Può essere:

* On-premise (all’interno dell’azienda)
* Ospitato presso un provider ma dedicato

Caratteristiche:

* Maggiore controllo
* Maggiore personalizzazione
* Investimento iniziale più elevato
* Spesso utilizzato per dati sensibili

Uso tipico: enti pubblici, banche, aziende con forti vincoli normativi.

---

## 3. Hybrid Cloud (Cloud ibrido)

È una combinazione di cloud pubblico e privato.

Caratteristiche:

* Parte dei servizi su infrastruttura privata
* Parte su cloud pubblico
* Collegamento sicuro tra i due ambienti

Uso tipico:

* Dati sensibili nel private cloud
* Servizi pubblici o scalabili nel public cloud
* Backup o disaster recovery nel cloud pubblico

Vantaggio principale: equilibrio tra controllo e scalabilità.

---

## 4. Multi-Cloud

Strategia che prevede l’utilizzo simultaneo di più provider cloud pubblici.

Caratteristiche:

* Riduzione dipendenza da un singolo fornitore
* Possibilità di scegliere il servizio migliore per ogni esigenza
* Maggiore complessità gestionale

Esempio: utilizzare AWS per infrastruttura, Google Cloud per AI, Azure per integrazione con ambienti Microsoft.

---

## 5. Community Cloud

Infrastruttura condivisa tra organizzazioni con esigenze simili (es. enti governativi o settore sanitario).

Caratteristiche:

* Accesso limitato a un gruppo specifico
* Costi condivisi
* Requisiti normativi comuni

---

# Schema sintetico

| Tipologia   | Proprietà infrastruttura | Condivisione | Controllo          | Uso tipico            |
| ----------- | ------------------------ | ------------ | ------------------ | --------------------- |
| Public      | Provider                 | Multi-tenant | Medio              | Servizi web, startup  |
| Private     | Organizzazione           | Singola      | Alto               | Dati sensibili        |
| Hybrid      | Mista                    | Parziale     | Alto + Scalabilità | Aziende strutturate   |
| Multi-Cloud | Più provider             | Multi-tenant | Variabile          | Strategie enterprise  |
| Community   | Gruppo organizzazioni    | Limitata     | Medio              | Settori regolamentati |

---

Concetto chiave:
Le tipologie di cloud definiscono **dove si trova l’infrastruttura e chi la condivide**, mentre IaaS/PaaS/SaaS definiscono **quale livello di servizio viene fornito**.


---

# 6. Caso di studio pratico

## Caso: una scuola superiore vuole pubblicare un registro elettronico interno e un sito web istituzionale

### Scenario iniziale

Un istituto scolastico deve:

* pubblicare un sito web istituzionale
* gestire un registro elettronico accessibile da docenti e famiglie
* garantire disponibilità continua
* proteggere dati personali (GDPR)
* evitare costi di acquisto server fisici

Si analizzano le possibili soluzioni cloud.

---

## Soluzione 1: approccio IaaS

Scelta: utilizzare macchine virtuali su Amazon Web Services oppure Microsoft Azure.

### Implementazione possibile

1. Creare una Virtual Machine Linux.
2. Installare manualmente:

   * server web (Nginx/Apache)
   * database (MySQL/PostgreSQL)
3. Configurare firewall virtuale.
4. Attivare backup automatici.
5. Replicare la VM su un’altra Availability Zone.

### Vantaggi

* Massimo controllo.
* Personalizzazione completa.
* Possibilità di installare qualsiasi software.

### Svantaggi

* Richiede competenze sistemistiche.
* Responsabilità diretta per aggiornamenti e patch di sicurezza.
* Maggior rischio di errore di configurazione.

---

## Soluzione 2: approccio PaaS

Scelta: usare ad esempio:

* Azure App Service
* Google App Engine
* AWS Elastic Beanstalk

### Implementazione possibile

1. Caricare il codice del sito.
2. Configurare database gestito (Database-as-a-Service).
3. Attivare scaling automatico.
4. Configurare certificato HTTPS.

### Vantaggi

* Nessuna gestione sistema operativo.
* Aggiornamenti automatici.
* Scalabilità automatica.
* Riduzione rischio di errori infrastrutturali.

### Svantaggi

* Minore controllo sul sistema.
* Dipendenza dal provider.

---

## Soluzione 3: approccio SaaS

Scelta: adottare una piattaforma SaaS già pronta (es. registro elettronico fornito da azienda specializzata).

### Implementazione possibile

1. Attivare abbonamento.
2. Creare account utenti.
3. Configurare dominio e DNS.
4. Formare il personale.

### Vantaggi

* Nessuna gestione tecnica.
* Aggiornamenti automatici.
* Sicurezza gestita dal fornitore.

### Svantaggi

* Personalizzazione limitata.
* Dipendenza totale dal fornitore.
* Costi ricorrenti per utente.

---

## Conclusione del caso

Se l’istituto possiede competenze IT interne → IaaS può essere appropriato.
Se vuole ridurre complessità tecnica → PaaS è spesso la soluzione più equilibrata.
Se vuole eliminare completamente la gestione tecnica → SaaS è la soluzione più semplice.

---

# 7. Tabella riassuntiva per interrogazione

| Aspetto                          | IaaS                                        | PaaS                           | SaaS                            | FaaS                           |
| -------------------------------- | ------------------------------------------- | ------------------------------ | ------------------------------- | ------------------------------ |
| Cosa trova il cliente all’inizio | Infrastruttura virtuale (VM, rete, storage) | Piattaforma pronta con runtime | Software già operativo          | Ambiente per eseguire funzioni |
| Gestione sistema operativo       | Cliente                                     | Provider                       | Provider                        | Provider                       |
| Gestione applicazione            | Cliente                                     | Cliente                        | Provider                        | Cliente (solo funzione)        |
| Livello di controllo             | Molto alto                                  | Medio                          | Basso                           | Molto limitato                 |
| Complessità tecnica              | Alta                                        | Media                          | Bassa                           | Media                          |
| Scalabilità                      | Manuale o automatica                        | Automatica                     | Automatica                      | Automatica                     |
| Esempio tipico                   | VM con server web                           | Deploy app web                 | Posta elettronica online        | API serverless                 |
| Provider noti                    | AWS EC2, Azure VM                           | App Engine, App Service        | Google Workspace, Microsoft 365 | AWS Lambda                     |

---

# 8. Schema sintetico per risposta orale

Per rispondere in modo completo durante interrogazione:

1. Definire il cloud come modello on-demand.
2. Spiegare differenza tra:

   * IaaS → infrastruttura
   * PaaS → piattaforma
   * SaaS → software pronto
   * FaaS → funzioni senza server visibili
3. Spiegare concetto di:

   * Region
   * Availability Zone
   * Responsabilità condivisa
4. Citare almeno tre provider globali:

   * Amazon Web Services
   * Microsoft Azure
   * Google Cloud Platform


---


[1]: https://cloud.google.com/learn/paas-vs-iaas-vs-saas?utm_source=chatgpt.com "PaaS vs. IaaS vs. SaaS vs. CaaS: How are they different?"
[2]: https://cloud.google.com/learn/paas-vs-iaas-vs-saas?hl=it&utm_source=chatgpt.com "PaaS, IaaS, SaaS e CaaS: in che cosa differiscono?"
[3]: https://aws.amazon.com/it/ec2/?utm_source=chatgpt.com "Calcolo sicuro e ridimensionabile nel cloud - Amazon EC2"
[4]: https://www.linkedin.com/posts/sonali-purandare-326ba01a0_cloudcomputing-usa-trending-activity-7350588652428644353-ZMrB?utm_source=chatgpt.com "Understanding IaaS, PaaS, SaaS: A Simple Cloud Service ..."
[5]: https://kinsta.com/blog/types-of-cloud-computing/?utm_source=chatgpt.com "Types of Cloud Computing | IaaS, PaaS, SaaS, XaaS"
[6]: https://www.cloudzero.com/blog/cloud-service-providers/?utm_source=chatgpt.com "21+ Top Cloud Service Providers Globally In 2025"
[7]: https://www.infodata.ilsole24ore.com/2025/12/13/cloud-computing-data-center-e-ai-i-numeri-e-i-protagonisti-del-mercato/?utm_source=chatgpt.com "Cloud computing, data center e Ai. I numeri e i protagonisti del ..."
