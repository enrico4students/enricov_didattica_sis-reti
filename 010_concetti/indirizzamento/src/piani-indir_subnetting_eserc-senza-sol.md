

# 19. Esercizi

Le seguenti sezioni sono organizzate per livello:

* A → Richiami e basi (classful)
* B → Subnetting CIDR
* C → Progettazione con VLSM

---

## 19.1 Esercizi – Indirizzi Classful

1. Data la rete 10.0.0.0, determinare classe, mask di default, numero host disponibili.
2. La rete 172.16.0.0 appartiene a quale classe? Quanti host totali consente?
3. Determinare se 192.168.5.10 è classe A, B o C e indicare la mask di default.
4. Calcolare numero reti e host nella classe B.
5. Data la rete 130.25.0.0, indicare classe e numero host per rete.
6. Verificare se 200.10.5.0 è rete pubblica di classe C.
7. Determinare intervallo indirizzi validi per rete 192.168.1.0 classful.
8. Per 15.0.0.0 indicare classe e numero massimo di host.
9. Per 180.20.0.0 indicare broadcast classful.
10. Identificare la classe di 126.10.1.1.
11. Identificare la classe di 191.255.1.1.
12. Identificare la classe di 223.0.0.1.
13. Quanti host utilizzabili in 172.20.0.0 classful?
14. Quanti bit host in classe C?
15. Data 150.10.10.10 indicare rete classful.
16. Data 192.10.10.10 indicare rete classful.
17. Data 11.5.6.7 indicare rete classful.
18. Determinare se 224.0.0.1 è classe A, B o C.
19. Spiegare perché 127.0.0.1 non è usabile come rete normale.
20. Data la rete 12.0.0.0, determinare classe, mask di default, numero host disponibili.

---

## 19.2 Esercizi – CIDR

1. Data 192.168.10.0/26 determinare host utilizzabili.
2. Data 192.168.10.0/27 determinare broadcast.
3. Data 10.0.0.0/12 determinare numero reti possibili rispetto classful.
4. Data 172.16.0.0/20 determinare range completo.
5. Data 192.168.1.64/26 determinare primo e ultimo host.
6. Data 192.168.1.128/25 determinare broadcast.
7. Data 10.10.10.0/30 determinare host utilizzabili.
8. Data 192.168.5.0/29 determinare numero sottoreti in una /24.
9. Data 172.16.0.0/22 determinare numero host per sottorete.
10. Data 192.168.1.0/28 determinare numero host.
11. Data 192.168.1.16/28 determinare intervallo.
12. Data 192.168.1.0/23 determinare totale host.
13. Data 10.0.0.0/8 suddividere in /16: quante sottoreti?
14. Data 172.16.0.0/24 rispetto a classful cosa cambia?
15. Data 192.168.1.0/30 quanti host?
16. Data 192.168.1.4/30 determinare broadcast.
17. Data 192.168.100.0/21 determinare intervallo.
18. Data 10.0.0.0/18 determinare host per rete.
19. Data 172.16.0.0/26 determinare numero sottoreti in una /24.
20. Data 192.168.0.0/19 determinare host totali.

---

## 19.3 Esercizi – VLSM (Piani di indirizzamento)

1. Progettare piano per rete 192.168.10.0/24 con: 60 host, 30 host, 10 host.
2. Progettare piano per 10.0.0.0/24 con: 100 host, 50 host, 20 host.
3. Progettare piano per 172.16.0.0/24 con 4 reti da 50 host.
4. Progettare rete 192.168.1.0/24 con: 120 host, 60 host, 30 host.
5. Progettare rete 10.0.0.0/23 con: 200 host, 100 host, 50 host, 20 host.
6. Rete 192.168.0.0/24 con: 80 host, 40 host, 20 host, 10 host.
7. Rete 172.16.10.0/24 con: 70 host, 30 host, 10 host.
8. Rete 192.168.5.0/24 con: 2 link punto-punto (/30) e 1 LAN da 100 host.
9. Rete 10.1.0.0/24 con: 120 host, 60 host, 60 host.
10. Rete 192.168.50.0/24 con: 90 host, 40 host, 20 host.
11. Rete 172.20.0.0/24 con: 4 reti da 30 host.
12. Rete 10.0.10.0/24 con: 200 host, 20 host.
13. Rete 192.168.200.0/24 con: 100 host, 50 host, 25 host, 10 host.
14. Rete 172.16.5.0/24 con: 3 reti da 60 host.
15. Rete 10.10.0.0/24 con: 120 host, 30 host, 30 host, 10 host.
16. Rete 192.168.0.0/23 con: 300 host, 100 host, 50 host.
17. Rete 172.16.0.0/23 con: 200 host, 60 host, 60 host.
18. Rete 10.0.0.0/22 con: 500 host, 200 host, 100 host.
19. Rete 192.168.100.0/24 con: 150 host, 50 host, 20 host.
20. Rete 172.16.100.0/24 con: 100 host, 30 host, 10 host, 2 link p2p.

---

## 19.4 Osservazioni sugli esercizi

Gli esercizi sono organizzati con difficoltà crescente:

* Classful → comprensione base
* CIDR → capacità di calcolo
* VLSM → progettazione

Le ultime tracce introducono problemi realistici:

* subnet insufficienti
* necessità di cambiare rete di partenza
* presenza di link punto-punto

---



