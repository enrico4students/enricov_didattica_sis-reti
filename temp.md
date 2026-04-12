

Il browser ricostruisce la catena:

1. Verifica che il certificato del server sia firmato dall’intermedia

   * usa la **chiave pubblica della Intermediate CA**

2. Verifica che l’intermedia sia firmata dalla Root. Il browser, oltre a verificare altre cose
   (validità temporale, corrispondenza dominio, revoca…), avendo il certificato della Intermediate CA e il certificato della Root CA (già nel sistema):

   * calcola l’hash del **contenuto (TBS, To Be Signed)** del certificato della Intermediate
   * prende la **firma presente nel certificato intermedio**
   * verifica la firma usando la **chiave pubblica della Root CA**

3. Controlla che la Root sia nel trust store locale
