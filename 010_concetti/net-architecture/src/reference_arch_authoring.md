voglio creare delle reference architectures di sistemi e reti, cioè architetture realistiche che includano tutti gli elementi, sia per il 2 layers sia per il 3 layers.
Le architetture servono come reminder a studenti ma devono avere un approccio professionale. Le organizzazioni per le quali si crea la rete devono avere tutti i possibili casi di connettività e avere meccamismi di sicurezza. Devono includere almeno
- connettività wifi di interni e ospiti
- server interni SAP  e contabilità custom, server di condivisione sicura files con segreti aziendali
- server locali DBMS e server NOSQL orientato al documento (ex. mongodb)
- connettività da ufficio secondario ubicato in line-of-sight a 600 metri dalla sede considerata
- un'altra sede principale in un'altro continente, questa sede deve connettersi in VPN site-to-site
- tutti e soli i dipendenti di livello manageriale devono avere accesso per lavorare remotamente
- deve essere prevista una rete di gestione della rete
- la ditta espone servizi WEB EST su amazon web services, questi servizi per la loro funzionalità invocano servizi implementati in FASTPAI in un server  interno