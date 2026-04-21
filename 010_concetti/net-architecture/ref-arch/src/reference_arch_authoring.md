voglio 
creare delle reference architectures di sistemi e reti, cioè architetture realistiche che includano tutti gli elementi che ricorrono piu' spesso nelle reti di organizzazioni del mondo reali. Le reference architectures vanno definite in ottica di traccia di esame di stato ma devono essere il piu' possibile realistiche.
Va creata almeno una versione per il 2 layers e una per il 3 layers.

Le organizzazioni per le quali si crea la rete devono avere tutti i possibili casi di connettività e avere meccanismi di sicurezza. Devono includere almeno
- connettività wifi di interni e ospiti
- server esterni: almeno un server WEB
- server interni: DBMS, sistema SAP, sistema di business custom, applicativo/server documentale dedicato a files con dati aziendali riservati accessibili solo al management, MondoDB per gestione documenti generale accessibile a tutti
- connettività da ufficio secondario ubicato in line-of-sight a 600 metri dalla sede considerata
- un'altra sede principale in un'altro continente, questa sede deve connettersi in VPN site-to-site
- tutti e soli i dipendenti di livello manageriale devono avere accesso per lavorare remotamente
- deve essere prevista una rete di gestione della rete
- l'organizzazione' espone servizi WEB REST su amazon web services, questi servizi per la loro funzionalità invocano servizi implementati in un server interno

