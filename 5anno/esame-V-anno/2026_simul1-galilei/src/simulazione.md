

MINISTERO DELL’ISTRUZIONE E DEL MERITO 
UFFICIO SCOLASTICO REGIONALE PER IL LAZIO 
POLO TECNICO-PROFESSIONALE “GALILEO“ 
I.T.I.S. “G. GALILEI” 
Municipio I – Ambito Territoriale I – SCUOLA POLO PER LA FORMAZIONE 
Via Conte Verde 51, 00185 ROMA - 0677071943 / 0677071947  
rmtf090003@istruzione.it - rmtf090003@pec.istruzione.it 
sito web: www.itisgalilei.edu.it 
C.M. RMTF090003 - C.F. 80122150586 - C.C.P. 59189001 



# SIMULAZIONE ESAME DI MATURITA’
# Disciplina: SISTEMI E RETI  
Il candidato svolga la prima parte della prova e risponda a due tra i quesiti proposti nella  seconda parte.  

## PRIMA PARTE  

Una struttura alberghiera in una località di mare dispone di  
- 52 camere per gli ospiti,  
- quattro sale per convegni,  
- ristorante e piscina.  

Le sale convegni, attrezzate con  videoproiettore o monitor di grande formato, sono allestite anche per eventi in videoconferenza.  

Nel parcheggio dell’albergo sei postazioni di ricarica per veicoli elettrici sono a disposizione dei clienti registrati.  

L’attivazione della postazione di ricarica e la contabilizzazione avvengono tramite web app.  

L’albergo è stato oggetto di lavori di manutenzione straordinaria con la realizzazione di un cablaggio  strutturato che ha interessato le camere, le sale convegni,  gli uffici e la reception. 
In ogni camera sono presenti due prese LAN per la SmartTV ed eventuali PC dei clienti.   
In  tutti i locali (camere, sale convegni, ristorante e altri spazi comuni) è disponibile la rete wireless  con accesso autenticato e differenziato tra ospiti, dipendenti e partecipanti ai convegni.  

Negli  uffici sono presenti sette postazioni di lavoro, una stampante di rete e un server per il software  gestionale in intranet.  
È presente anche un secondo server, esposto in internet, per il sito web  della struttura.  

Dalla terrazza dell’albergo è visibile, a 500m di distanza, lo stabilimento balneare, riservato agli  ospiti, con annesso bar/ristorante sulla spiaggia.  

Il personale in servizio presso lo stabilimento balneare verifica le presenze giornaliere e le prenotazioni del ristorante collegandosi al software  gestionale dell’albergo.  

Gli ospiti in spiaggia possono disporre di accesso ad internet tramite rete wi-fi **con le stesse modalità di identificazione con cui accedono in albergo**.  
Sia l’albergo che lo stabilimento balneare possono attivare contratti per connessione internet FTTH con i principali provider in quanto la zona risulta coperta dal servizio. 

Il candidato, sulla base delle specifiche fornite e fatte le eventuali ipotesi aggiuntive ritenute  necessarie:  

    A. disegni la struttura della rete individuando gli apparati necessari per il funzionamento in sicurezza;  

    B. proponga un piano di indirizzamento tenendo in considerazione la separazione tra ospiti, uffici, servizi e sale convegni;  

    C. descriva, valutando le diverse soluzioni possibili, il tipo di collegamento tra albergo e  stabilimento balneare che consente l’attività dei dipendenti e l’accesso ad internet agli ospiti;  

    D. progetti una base di dati per la gestione delle prenotazioni delle camere, modellando le anagrafiche degli ospiti (dati personali e email), le camere (numero, tipologia) e le relative prenotazioni con i periodi di permanenza (data check-in, data check-out).  

Il candidato preveda anche la memorizzazione delle credenziali per l'accesso al WiFi (username e password) che saranno relative alla prenotazione.  

Si richiedono, in particolare, il modello concettuale e il corrispondente modello logico.

## SECONDA PARTE  
Il candidato scelga due fra i seguenti quesiti e per ciascun quesito scelto formuli una risposta **della lunghezza massima di 20 righe** esclusi eventuali grafici, schemi e tabelle.  

    I. Una colonnina di ricarica per auto elettriche è gestita da un sistema automatico a  microcontrollore che comunica con un server. Dopo aver definito un formato di trasmissione che  includa i seguenti dati: data/ora, id_cliente, percentuale_carica, energia erogata, si descriva a livello teorico il ruolo dei socket come interfaccia di comunicazione. 
    In particolare, si illustrino le funzioni principali necessarie per stabilire una connessione, gestire il flusso di dati parametri  e chiudere la sessione tra la colonnina e il server remoto  

    II. Una scuola ha necessità di implementare un sistema di filtraggio dei contenuti per tutelare la  navigazione degli studenti impedendo l’accesso a siti non consentiti. Attraverso il medesimo  sistema deve poter transitare, protetto dal resto della rete didattica e con minori vincoli, il traffico  degli uffici. Si descriva i dispositivi necessari ed una ipotetica configurazione illustrandone  vantaggi e limiti.  

    III. Sempre più frequentemente troviamo gli URL dei siti iniziare con https://.... Si descriva in cosa differisce il protocollo HTTPS dal protocollo HTTP e quali vantaggi comporta  per il visitatore del sito.  

    IV. In una rete aziendale dal browser di un PC non si riesce ad aprire pagine web esterne. Le  risorse di rete locale continuano invece ad essere accessibili. Sapendo che il gateway ha per  indirizzo 192.168.24.1 e sulla rete è presente un server DNS con indirizzo 192.168.24.5, si  descriva una ipotetica sequenza di verifiche che il tecnico può eseguire per individuare l’origine  del problema.  