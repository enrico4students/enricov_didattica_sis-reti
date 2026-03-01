## 1. Cloud Computing

Il **cloud computing** è un modello di erogazione di risorse informatiche tramite Internet.
Invece di possedere fisicamente server, storage e reti, si utilizzano infrastrutture remote messe a disposizione da grandi provider.

Secondo il National Institute of Standards and Technology (NIST), il cloud è un modello che consente accesso on-demand a un insieme condiviso di risorse configurabili (rete, server, storage, applicazioni) rapidamente attivabili e rilasciabili.

Caratteristiche fondamentali:

* Accesso via rete
* Scalabilità elastica
* Pagamento a consumo
* Provisioning rapido
* Gestione centralizzata

---

# 2. Modelli di servizio (con operatività concreta)

## 2.1 IaaS – Infrastructure as a Service

Nel modello IaaS il provider fornisce **infrastruttura virtuale**.

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

Nel modello PaaS il provider fornisce una **piattaforma pronta per eseguire codice**.

### Cosa trova disponibile il cliente all’istante zero

Appena attivato il servizio sono già presenti:

* Sistema operativo gestito
* Runtime (es. Python, Node, Java, .NET)
* Server web configurato
* Scalabilità automatica
* Monitoraggio integrato
* Log centralizzati

Non si gestiscono VM né patch di sistema.

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

Nel modello SaaS il software è completamente pronto all’uso.

Esempi:

* Google Workspace
* Microsoft 365

---

### Cosa trova disponibile il cliente all’istante zero

Subito disponibili:

* Applicazione accessibile via browser
* Autenticazione utenti
* Spazio di archiviazione
* Aggiornamenti automatici
* Backup gestiti dal provider

Non è possibile modificare l’infrastruttura sottostante.

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

Modello in cui si eseguono singole funzioni senza gestire server.

---

### Cosa trova disponibile il cliente all’istante zero

* Ambiente di esecuzione già configurato
* Trigger automatici (HTTP, eventi, code)
* Scalabilità automatica
* Logging integrato

Non esistono macchine virtuali visibili.

---

### Uso tipico: API che elabora richieste HTTP

Passi fondamentali:

1. Scrivere una funzione.
2. Caricarla nel servizio serverless.
3. Collegarla a un endpoint HTTP.
4. Pubblicare l’URL.

Il sistema esegue la funzione solo quando viene chiamata.

---

# 3. Specificità del Cloud

## 3.1 Region e Availability Zone

![Image](https://miro.medium.com/0%2AENYm2-13BhmJbFO6.png)

![Image](https://docs.aws.amazon.com/images/AWSEC2/latest/UserGuide/images/region-with-wavelength-zones.png)

![Image](https://learn.microsoft.com/en-us/azure/reliability/media/cross-region-replication.png)

![Image](https://agileit.com/_astro/az-graphic-two.C0qDynBR_Z3LjvV.webp)

Il cloud è organizzato in:

* Region (area geografica)
* Availability Zone (datacenter separati)

Le applicazioni possono essere replicate su più zone per garantire continuità operativa.

---

## 3.2 Storage nel Cloud

### Object Storage

![Image](https://miro.medium.com/1%2AEfGkQYt_uW8yNG3X7hVjSA.png)

![Image](https://cdn.prod.website-files.com/6758716c1db67a29ec00ebb4/681c9b5b592d590a9a5502d5_Amazon%20S3.png)

![Image](https://d2908q01vomqb2.cloudfront.net/e1822db470e60d090affd0956d743cb0e7cdf113/2023/02/17/Arch_Diagram_Replication_Image2.png)

![Image](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2021/08/02/Fig1-S3-Object.png)

Caratteristiche:

* Accesso via API HTTP
* Scalabilità quasi illimitata
* Replica automatica
* Elevata durabilità

---

## 3.3 Sicurezza e responsabilità condivisa

Nel cloud:

* Il provider protegge l’hardware e i datacenter.
* Il cliente configura accessi, permessi, cifratura applicativa.

Strumenti tipici:

* IAM
* Reti virtuali isolate
* Firewall logici
* Cifratura dati

Errore comune: configurazioni pubbliche involontarie.

---

# 4. I principali provider

## 4.1 Amazon Web Services

![Image](https://res.cloudinary.com/hy4kyit2a/f_auto%2Cfl_lossy%2Cq_70/learn/modules/aws-cloud/explore-the-aws-global-infrastructure/images/c72a7ac57ffc2469619e66dc74dfea24_kix.q8rtdmc6bgiq.png)

![Image](https://assets.aboutamazon.com/dims4/default/9021a44/2147483647/strip/true/crop/5266x2962%2B3%2B0/resize/1440x810%21/quality/90/?url=https%3A%2F%2Famazon-blogs-brightspot.s3.amazonaws.com%2Fa3%2Ff6%2F0abb1c1a4734ba2e727893e6eae2%2Faws-data-center-exterior-1.jpg)

![Image](https://d2908q01vomqb2.cloudfront.net/da4b9237bacccdf19c0760cab7aec4a8359010b0/2024/11/12/01-Console-home-previous-1.png)

![Image](https://d2908q01vomqb2.cloudfront.net/da4b9237bacccdf19c0760cab7aec4a8359010b0/2023/11/14/2023-myapplications-1-console-home.jpg)

Leader mondiale per quota di mercato e ampiezza servizi.

---

## 4.2 Microsoft Azure

![Image](https://learn.microsoft.com/en-us/azure/networking/media/microsoft-global-network/microsoft-global-wan.png)

![Image](https://www.techielass.com/content/images/2021/03/azuredatacentre.jpg)

![Image](https://learn.microsoft.com/en-us/azure/azure-portal/media/azure-portal-dashboards/portal-menu-dashboard.png)

![Image](https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/media/tutorial-logs-dashboards/log-analytics-portal-dashboard.png)

Fortissima integrazione con ecosistema Microsoft.

---

## 4.3 Google Cloud Platform

![Image](https://images.openai.com/static-rsc-3/EdMcuFFCO3u-eMOOHhjKOdaavW9NWZqcXNTm_Sxb4EwhzZVMyoAJL9VsC9Tax5JtLcYts3_KjPfo0-0k_g4gn_TRrhOxRmal-6dv3Q87BEM?purpose=fullsize\&v=1)

![Image](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/unnamed_RTmGiMI.width-1300.png)

![Image](https://docs.cloud.google.com/static/docs/images/overview/console.png)

![Image](https://cloudmaven.github.io/cloud101_cloudproviders/fig/03-gcp-intro-0001.png)

Specializzazione in AI e Big Data.

---

## 4.4 Alibaba Cloud

![Image](https://yqintl.alicdn.com/1fcea5e2afccff733dc41e49b5d7236d3d1fa61b.png)

![Image](https://yqintl.alicdn.com/b20e486124a4fae0cdb9fe023d273fa9c8857ec9.jpeg)

![Image](https://yqintl.alicdn.com/f7bd42edf766b8918888271986ef559daea6498c.png)

![Image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/0113824171/p795313.png)

Leader nel mercato asiatico.

---

# 5. Concetti fondamentali da fissare

Nel cloud:

* Le risorse sono virtuali e distribuite.
* L’infrastruttura è organizzata in region e zone.
* Lo storage è spesso object-based.
* La sicurezza è condivisa.
* L’automazione è centrale.

Il livello di controllo diminuisce passando da IaaS a SaaS, mentre diminuisce anche la complessità di gestione per il cliente.

