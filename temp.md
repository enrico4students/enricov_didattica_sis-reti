

# 6. Routing e gateway

Il routing tra le reti viene effettuato dal firewall mediante **subinterfacce VLAN 802.1Q** sulla porta LAN trunk e una interfaccia separata per la DMZ.

Ogni rete utilizza come gateway l’indirizzo `.1`.

```
VLAN 10    10.10.10.1
VLAN 20    10.10.20.1
VLAN 30    10.10.30.1
VLAN 40    10.10.40.1
VLAN 50    10.10.50.1
VLAN 60    10.10.60.1
VLAN 80    10.10.80.1
VLAN 90    10.10.90.1
DMZ        10.10.70.1
```

Questa convenzione semplifica amministrazione e troubleshooting, perché il gateway è sempre facilmente identificabile.

---

# Aggiornamento numerazione sezioni successive

Dopo questa integrazione la numerazione diventa:

| Vecchia sezione               | Nuova sezione |
| ----------------------------- | ------------- |
| Routing e gateway             | **6**         |
| DHCP e indirizzamento statico | **7**         |
| Trunk 802.1Q                  | **8**         |
| Server web e DBMS             | **9**         |
| Regole di sicurezza           | **10**        |
| Collegamento stabilimento     | **11**        |
| Identificazione Wi-Fi         | **12**        |
| Funzionamento complessivo     | **13**        |
| Progetto database             | **14**        |
| Modello concettuale           | **15**        |
| Modello logico                | **16**        |
| Vincoli applicativi           | **17**        |
| Quesito 1                     | **18**        |
| Quesito 2                     | **19**        |
| Quesito 3                     | **20**        |
| Quesito 4                     | **21**        |

---

Se vuoi, nel messaggio successivo posso anche aggiungere **una tabella finale molto utile nei compiti d’esame** che riassume:

VLAN → gateway → funzione → accesso consentito → accesso negato.

È una cosa che **i commissari apprezzano moltissimo** perché mostra che lo studente ha capito davvero l’architettura di sicurezza della rete.
