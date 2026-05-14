"""
Modulo per la gestione centralizzata delle conferme operative.

Questo modulo definisce la classe ConfirmManager, utilizzata per richiedere
conferma all'utente prima di eseguire operazioni potenzialmente modificanti
o distruttive, come la creazione, sovrascrittura, eliminazione o modifica di
file e directory.

La classe supporta tre modalità principali:

- modalità interattiva:
  ogni operazione proposta viene mostrata all'utente e richiede una scelta
  esplicita;

- modalità automatica:
  se assume_yes è attivo, tutte le operazioni vengono confermate senza
  ulteriori richieste interattive;

- modalità simulazione:
  se dry_run è attivo, l'operazione viene soltanto descritta a video e
  considerata confermata, senza che il chiamante debba distinguere il caso
  dalla normale conferma.

Le risposte supportate in modalità interattiva sono:

- y:
  confermare l'operazione corrente;

- n:
  rifiutare l'operazione corrente;

- a:
  confermare l'operazione corrente e tutte le successive;

- q:
  interrompere immediatamente il programma con codice di uscita 1.

La classe non esegue direttamente alcuna operazione sui file o sul sistema:
si limita a gestire la decisione di conferma. Il codice chiamante resta
responsabile dell'esecuzione effettiva dell'azione proposta.
"""

from __future__ import annotations

import sys
import textwrap


class ConfirmManager:
    def __init__(self, assume_yes: bool = False, dry_run: bool = False) -> None:
        self.assume_yes = assume_yes
        self.dry_run = dry_run

    def ask(self, description: str) -> bool:
        if self.dry_run:
            print("\n[DRY RUN] Operazione simulata:")
            print(textwrap.indent(description.strip(), prefix="    "))
            return True

        print("\nOperazione proposta:")
        print(textwrap.indent(description.strip(), prefix="    "))

        if self.assume_yes:
            print("    Esecuzione automatica attiva (--yes o scelta precedente 'a').")
            return True

        while True:
            answer = input("Confermare? [y] sì / [n] no / [a] tutte le successive / [q] termina: ").strip().lower()
            if answer == "y":
                return True
            if answer == "n":
                return False
            if answer == "a":
                self.assume_yes = True
                return True
            if answer == "q":
                print("Interruzione richiesta dall'utente.")
                sys.exit(1)
            print("Risposta non valida.")
