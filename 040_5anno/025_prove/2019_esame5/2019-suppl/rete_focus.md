Perfetto.
Di seguito riporto **esclusivamente i diagrammi**, costruiti in modo **100% coerente** con la versione “minimal e perfettamente aderente alla traccia d’esame” che ho definito nel messaggio precedente.

Non aggiungo nulla rispetto a quella architettura.
Nessuna HA, nessun doppio ISP, nessun WAF dedicato, nessuna complessità enterprise.

---

# 1) Diagramma infrastruttura generale (logico)

Architettura esattamente come descritta:

Internet
→ Router ISP
→ Firewall
→ DMZ
 → Web Server Ticketing
→ LAN interna
 → Database Server
 → Server Posta
 → PC dipendenti
 → WiFi aziendale

Tecnici in trasferta:
→ Internet
→ VPN su firewall
→ accesso HTTPS

---

## Diagramma PlantUML

```
@startuml
skinparam linetype ortho
skinparam shadowing false

cloud "Internet" as NET

node "Sede InfoService" {

    node "Router ISP" as RTR
    node "Firewall\n(NAT + VPN + ACL)" as FW

    node "DMZ" {
        node "Web Server\nSistema Ticketing" as WEB
    }

    node "LAN Interna" {

        database "Database Server\nTicketing" as DB
        node "Server Posta\n(SMTP)" as MAIL
        node "PC Dipendenti\nHelpdesk / Amministrazione" as PC
        node "Access Point WiFi\n(WPA2/WPA3-Enterprise)" as AP
    }
}

NET -- RTR
RTR -- FW
FW -- WEB
FW -- DB
FW -- MAIL
FW -- PC
FW -- AP

WEB -- DB

note right of FW
- Pubblicazione HTTPS (443)
- VPN per tecnici
- Regole ACL di sicurezza
end note

@enduml
```

---

# 2) Diagramma accesso tecnico in trasferta

Coerente con quanto scritto:

Tecnico
→ Internet
→ VPN su firewall
→ accesso portale HTTPS

---

## Diagramma PlantUML

```
@startuml
skinparam linetype ortho
skinparam shadowing false

node "Tecnico in trasferta\nNotebook aziendale\n(4G/5G o rete cliente)" as TECH

cloud "Internet" as NET

node "Firewall Sede\n(VPN Server)" as FW

node "Web Server Ticketing\n(HTTPS)" as WEB

TECH -- NET
NET -- FW
FW -- WEB

note right of FW
Tunnel VPN cifrato
Autenticazione tecnico
end note

@enduml
```

---

# 3) Diagramma flusso cliente – convalida report

Coerente con la risposta:

Cliente
→ HTTPS
→ Web Server
→ DB
→ visualizzazione report
→ commento e conferma

---

## Diagramma PlantUML

```
@startuml
skinparam linetype ortho
skinparam shadowing false

node "Cliente\nBrowser Web" as CLIENT

cloud "Internet" as NET

node "Firewall" as FW
node "Web Server Ticketing\n(HTTPS)" as WEB
database "Database Server" as DB

CLIENT -- NET
NET -- FW
FW -- WEB
WEB -- DB

note right of CLIENT
- Login con credenziali
- Visualizza report
- Conferma + commento
end note

@enduml
```

---

