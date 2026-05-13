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
