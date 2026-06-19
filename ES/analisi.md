## Analisi concisa della prova

La prova è una traccia di progettazione di rete, non una traccia sul BIM in senso stretto. Il BIM è citato come contesto applicativo: il BIM è un modello digitale dell’edificio che raccoglie dati geometrici, tecnici e documentali utili alla progettazione e gestione dei lavori.

Il candidato deve progettare una infrastruttura di comunicazione per cantieri temporanei collegati a una sede centrale. 
**Il problema principale è far viaggiare in modo sicuro dati pesanti, dati continui e dati critici**: scansioni 3D, immagini timelapse e dati dei sensori.

La prima parte richiede quattro elementi: 
- rete locale di cantiere, 
- potenziamento della rete centrale, 
- collegamento WAN tra cantieri e sede, 
- autenticazione degli operatori. 

La WAN è la rete geografica che collega sedi distanti, ad esempio tramite fibra, 4G/5G, xDSL, VPN o collegamenti dedicati.

Le tecnologie citate servono solo a capire il tipo di traffico.  
I tablet rugged sono tablet rinforzati per ambienti difficili come cantieri.  
Il laser scanner 3D acquisisce molte misure di distanza per ricostruire una superficie.  
Il LiDAR è un sensore che misura distanze tramite impulsi luminosi.  
La nuvola di punti è l’insieme dei punti 3D rilevati dallo scanner e usati per ricostruire un modello.  
Le fotocamere timelapse scattano foto a intervalli regolari per creare video accelerati.  
I sensori di sicurezza raccolgono dati ambientali o di rischio, come temperatura, gas, vibrazioni o fumi.

**La soluzione non deve descrivere in dettaglio il funzionamento fisico di scanner, LiDAR o fotocamere. Deve invece tradurre questi dispositivi in esigenze di rete**:  
- banda elevata per scansioni e immagini, 
- affidabilità per i sensori, 
- copertura wireless in cantiere, 
- sicurezza degli accessi,  
- raccolta centralizzata dei dati, 
- logging e continuità del collegamento.


La sede centrale ha già una rete locale e una connessione ADSL, ma **l’ADSL è probabilmente insufficiente** per il nuovo scenario perché ha banda limitata, soprattutto in upload, e non è adatta a molti cantieri che inviano file pesanti. La proposta realistica deve prevedere 
- potenziamento della connettività,  
- firewall, server o storage centralizzato,  
- VLAN,  
- servizi di autenticazione e accesso remoto sicuro.

La seconda parte propone quesiti opzionali. 
- Il primo chiede il confronto tra archiviazione on premise e cloud-based: on premise significa mantenere server e storage nella propria sede, cloud-based significa usare risorse di un fornitore esterno tramite Internet.  
- Il secondo chiede misure di sicurezza e continuità trasmissiva, quindi firewall, VPN, cifratura, ridondanza dei collegamenti, backup, monitoraggio e controllo accessi.  
- Il terzo sposta il tema su una rete scolastica e chiede come bloccare l’accesso a piattaforme di Intelligenza Artificiale, cioè servizi online che generano testi o codice in modo automatico.  
- Il quarto riguarda SSH e port forwarding: SSH è un protocollo per accedere in modo sicuro a un sistema remoto da terminale, mentre il port forwarding reindirizza una connessione ricevuta su una porta verso un altro dispositivo interno.

La prova valuta **soprattutto capacità progettuale**.  
Non basta elencare apparati: occorre 
- fare ipotesi,  
- dimensionare in modo ragionevole,  
- distinguere traffico locale e remoto,  
- proporre uno schema di rete, 
- indicare indirizzamenti, protocolli, servizi e misure di sicurezza.

La difficoltà principale è che il testo contiene molte tecnologie non necessariamente studiate. Tuttavia sono quasi tutte descrittive: il candidato può trattarle come sorgenti di dati da collegare alla rete. La parte veramente disciplinare riguarda reti locali, reti wireless, router, switch, firewall, VPN, indirizzamento IP, autenticazione, sicurezza, servizi di rete e collegamenti geografici.
