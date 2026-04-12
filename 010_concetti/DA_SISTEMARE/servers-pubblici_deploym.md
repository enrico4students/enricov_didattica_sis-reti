
## **deployment professionale di un web server in DMZ** 

Oggi è diverso da quello che spesso si trova nei vecchi libri di networking.
Nella pratica moderna il server **quasi sempre usa un indirizzo IP privato**, 
mentre l’indirizzo pubblico è gestito dal firewall o da un reverse proxy.

Abbiamo tre modelli.

---

# 1. Modello moderno più comune (NAT verso server con IP privato)

È la configurazione più diffusa nelle reti aziendali.

Architettura logica: Internet → Firewall → DMZ → Web server

Configurazione tipica:  

* il **firewall possiede uno o più IP pubblici**  
* il **web server ha un indirizzo IP privato**  
* il firewall esegue **NAT o port forwarding**  

Esempio:  
IP pubblico firewall: 203.0.113.10
Web server DMZ:      192.168.50.10

Regola firewall:

```
203.0.113.10:80  → 192.168.50.10:80
203.0.113.10:443 → 192.168.50.10:443
```

Quindi:  
il client su Internet si connette a 203.0.113.10 (indirizzo pubblico firewall)
ma il traffico viene inoltrato al server 192.168.50.10 (indirizzo privato Web server DMZ)

Vantaggi:  
* maggiore sicurezza
* il server non è direttamente esposto
* possibilità di cambiare server senza cambiare IP pubblico
* gestione centralizzata delle policy di sicurezza

Questo è il **modello più comune oggi**.

---

# 2. Modello con reverse proxy o load balancer (molto diffuso)

In ambienti professionali moderni spesso si aggiunge un ulteriore livello.

Architettura:

Internet Firewall → Reverse proxy/Load balancer → Web server (DMZ o rete interna)

In questo caso:  
* l’IP pubblico appartiene al **reverse proxy**
* i web server hanno **indirizzi privati**
* il proxy inoltra le richieste HTTP/HTTPS

Esempio di tecnologie usate: NGINX, HAProxy, Apache reverse proxy, F5, cloud load balancer  

Vantaggi:  
* bilanciamento del carico  
* TLS termination  
* protezioni applicative  
* maggiore scalabilità  

Questo è molto comune in **architetture moderne e cloud**.

---

# 3. Modello più vecchio (web server con IP pubblico)

In passato era abbastanza diffuso assegnare direttamente un IP pubblico al server in DMZ.

Architettura:

    Internet → Firewall → DMZ → Web server con IP pubblico

Esempio:
Web server: 203.0.113.10
Il firewall semplicemente permette traffico: porta 80, porta 443

Questo modello oggi è **meno comune** perché:  
* espone direttamente il server
* riduce il controllo centralizzato
* rende più difficile cambiare server

Si trova ancora in alcune infrastrutture legacy.

---

# 4. Conclusione

Nel deployment professionale moderno:

il **web server in DMZ usa quasi sempre un indirizzo IP privato**  
mentre l’**indirizzo pubblico è sul firewall o sul reverse proxy**.

Schema tipico reale:  

    Internet → IP pubblico firewall → NAT → Web server con IP privato nella DMZ  

oppure  

    Internet → firewall → reverse proxy → web server con IP privato  


---

# 5. Conclusione

Nel **deployment più comune nelle reti aziendali moderne**

Il web server nella DMZ usa normalmente un indirizzo IP privato; 
l’indirizzo pubblico è gestito dal firewall o da un reverse proxy che inoltra le richieste al server


---

## Alcuni riferimenti

NIST SP 800-41 – Guidelines on Firewalls and Firewall Policy
[https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf)

OWASP Secure Architecture Design
[https://cheatsheetseries.owasp.org/cheatsheets/Architecture_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Architecture_Cheat_Sheet.html)

Cisco DMZ Design Guide
[https://www.cisco.com/c/en/us/support/docs/security-vpn/remote-authentication-dial-user-service-radius/13739-40.html](https://www.cisco.com/c/en/us/support/docs/security-vpn/remote-authentication-dial-user-service-radius/13739-40.html)
