

La relazione “prenotazione” tra ospite e stanza non è univocamente di un solo tipo, ma nella modellazione corretta è una relazione molti-a-molti (N:M):
- Un ospite può effettuare più prenotazioni nel tempo
- Una stanza può essere prenotata più volte nel tempo

La relazione prenotazione normalmente contiene attributi come:
data_inizio
data_fine
stato (confermata, cancellata, etc.)
numero_persone

è consigliabile modellarla come entità associativa (entità debole / relazione con attributi)

Si ottiene:
* Entità: Ospite
* Entità: Stanza
* Entità (associativa): Prenotazione   

relazioni:  
* Ospite (1,N) → Prenotazione  
* Stanza (1,N) → Prenotazione  

---

# Definire/leggere una cardinalità, regola pratica

fissare **UNA sola istanza dell’entità** e contare **quante volte può partecipare alla relazione**

Esempi con **Ospite, Prenotazione, Stanza**  


**Ospite — *effettua* — Prenotazione**

fissiamo **un ospite concreto**, ad esempio: *Mario Rossi*
quante prenotazioni può avere?
  * prenotazione 1 → giugno
  * prenotazione 2 → luglio
  * prenotazione 3 → agosto

* Mario Rossi partecipa a **più prenotazioni** quindi: **lato Ospite = 1..N**

---

**Prenotazione — riguarda — Stanza**  

Esempi: 
famiglia Rossi di 4 persone prenota due stanze
Ufficio viaggi IBM prenota per 5 dipendenti che partecipano ad un congresso

In ognunci dei casi fissiamo **una prenotazione**, 

famiglia prenotazione 123 della famiglia Rossi relativa a stanze 10 e 11
* prenotazione 123 → stanza 10 # (Rossi padre figlio)
* prenotazione 123 → stanza 11 # (Rossi madre figlia)

IBM prenotazione 124
* prenotazione 124 -> stanza 20 # IBM dipendente 1
* prenotazione 124 -> stanza 21 # IBM dipendente 2
* prenotazione 124 -> stanza 23 # IBM dipendente 2

la stessa prenotazione compare più volte nella relazione quindi lato Prenotazione = 1..N (una prenotazione può riguardare più stanze)

---



