    1. Cos’è una firma digitale (concetto generale)

Una firma digitale è un meccanismo crittografico che permette di verificare due cose:

* integrità: il contenuto non è stato modificato dopo la firma
* autenticità: la firma è stata prodotta da chi possiede una specifica chiave privata

In pratica:

* si calcola l’hash del file (impronta)
* si firma l’hash con la chiave privata
* chi riceve verifica la firma con la chiave pubblica

La firma digitale NON cifra automaticamente il contenuto (confidenzialità e firma sono funzioni diverse).

Nota terminologica importante (Italia):

* “firma digitale” in senso tecnico-crittografico: quanto descritto sopra
* “firma digitale” in senso legale (firma qualificata): richiede certificati qualificati e dispositivi/servizi conformi; una firma “autoprodotta” serve per laboratorio e non equivale a una firma qualificata

2. Strumenti gratuiti su Windows per creare firme digitali (uso didattico)

A) Gpg4win (OpenPGP) – firma di file e messaggi

* sito: Gpg4win – Download: [https://gpg4win.org/download.html](https://gpg4win.org/download.html)  ([Gpg4win][1])
* cosa permette: generare coppia di chiavi, firmare file, verificare firme

B) LibreOffice (X.509) – firma di documenti Office (e gestione firme)

* guida: LibreOffice Help – Using Digital Signatures: [https://help.libreoffice.org/latest/he/text/shared/guide/digital_signatures.html](https://help.libreoffice.org/latest/he/text/shared/guide/digital_signatures.html)  ([LibreOffice Help][2])
* nota: su Windows i certificati X.509 sono gestiti dal sistema (certmgr.msc), e per OpenPGP LibreOffice rimanda a Gpg4win ([LibreOffice Help][3])

C) OpenSSL (per creare certificati X.509 “di laboratorio”, self-signed)

* sito: Shining Light Productions – Win32/Win64 OpenSSL: [https://slproweb.com/products/Win32OpenSSL.html](https://slproweb.com/products/Win32OpenSSL.html)  ([Shining Light Productions][4])
* uso tipico: generare chiavi/certificati per test, lab TLS, firma X.509 “non pubblicamente fidata”

3. LAB semplice (Windows) – creare e verificare una firma digitale con Gpg4win (consigliato per studenti)

Obiettivo: firmare un file e verificarne la firma.

Passo 0: installare Gpg4win

* scaricare e installare da: [https://gpg4win.org/download.html](https://gpg4win.org/download.html) ([Gpg4win][1])
* durante l’installazione includere Kleopatra (interfaccia grafica)

Passo 1: generare una coppia di chiavi

* aprire “Kleopatra”
* creare nuova coppia di chiavi OpenPGP (nuova identità)
* impostare una passphrase per proteggere la chiave privata

Passo 2: creare un file di prova

* creare un file, esempio: prova.txt (con una frase qualsiasi)

Passo 3: firmare il file

* in Kleopatra selezionare “Sign / Encrypt…”
* scegliere “Sign”
* selezionare prova.txt
* ottenere un file di firma (tipicamente prova.txt.sig oppure prova.txt.asc, dipende dal formato scelto)

Passo 4: verificare la firma

* in Kleopatra usare “Verify” sul file di firma (e/o sul file firmato, in base al formato)
* risultato atteso: verifica valida

Passo 5: dimostrare l’integrità

* modificare prova.txt (anche solo un carattere)
* ripetere la verifica
* risultato atteso: verifica non valida

4. Firma digitale nei certificati Web (HTTPS)

Nel Web non si firma “il sito”: si firma il certificato del server.

* il server possiede una chiave privata
* il certificato X.509 contiene la chiave pubblica del server e l’identità (dominio)
* una CA (Certification Authority) firma il certificato con la propria chiave privata
* il browser verifica la firma con la chiave pubblica della CA (catena di fiducia)

Questa firma della CA serve a dire: “questa chiave pubblica appartiene davvero a questo dominio” (secondo il livello di verifica della CA).

5. Come viene usato il certificato in SSL/TLS

Durante l’handshake TLS (HTTPS):

* il server invia il proprio certificato
* il client verifica:

  * validità temporale
  * corrispondenza del dominio (SAN/CN)
  * firma della CA e catena di fiducia
* se tutto è valido, si stabiliscono chiavi di sessione e si passa alla cifratura simmetrica dei dati

Quindi:

* firma digitale (della CA sul certificato): autenticazione del server e fiducia
* cifratura TLS: confidenzialità dei dati in transito
* integrità TLS: rilevazione manomissioni dei dati in transito

6. Limiti della firma “da studente” rispetto a una CA (Web e non solo)

Firma “da studente” (OpenPGP o X.509 self-signed):

* ✅ utile per capire il meccanismo tecnico (chiavi, firma, verifica, integrità)
* ❌ non è automaticamente fidata da terzi (browser/sistemi) perché manca una fiducia preinstallata
* ❌ per uso pubblico (HTTPS reale) genera warning se il certificato è self-signed

Firma/certificato emesso da CA:

* ✅ fiducia automatica nei browser (se la CA è nel trust store)
* ✅ catena di fiducia verificabile
* ✅ adatto a produzione e uso pubblico (HTTPS senza avvisi, se configurato correttamente)

Se si desidera, si può aggiungere un secondo lab breve su X.509 self-signed con OpenSSL (Windows) e prova su un server locale HTTPS (es. localhost), mantenendo chiaro che il browser mostrerà avvisi finché non si aggiunge manualmente fiducia al certificato.

[1]: https://gpg4win.org/download.html?utm_source=chatgpt.com "Download Gpg4win"
[2]: https://help.libreoffice.org/latest/he/text/shared/guide/digital_signatures.html?utm_source=chatgpt.com "Using Digital Signatures"
[3]: https://help.libreoffice.org/latest/he/text/shared/01/digitalsignatures.html?utm_source=chatgpt.com "Digital Signatures"
[4]: https://slproweb.com/products/Win32OpenSSL.html?utm_source=chatgpt.com "Win32/Win64 OpenSSL Installer for Windows"
