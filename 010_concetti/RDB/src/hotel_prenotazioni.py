
import os
import sqlite3
from datetime import datetime, date
from typing import List, Optional, Tuple


DB_PATH = os.path.splitext(os.path.abspath(__file__))[0] + ".db"


class HotelBookingApp:
    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_schema()

    def create_schema(self) -> None:
        cur = self.conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ospite (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cognome TEXT NOT NULL,
                email TEXT,
                telefono TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS stanza (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT NOT NULL UNIQUE,
                tipo TEXT NOT NULL,
                capienza INTEGER NOT NULL CHECK (capienza > 0)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS prenotazione (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referente_nome TEXT NOT NULL,
                referente_contatto TEXT,
                data_inizio TEXT NOT NULL,
                data_fine TEXT NOT NULL,
                note TEXT,
                CHECK (date(data_inizio) < date(data_fine))
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS prenotazione_ospite (
                prenotazione_id INTEGER NOT NULL,
                ospite_id INTEGER NOT NULL,
                PRIMARY KEY (prenotazione_id, ospite_id),
                FOREIGN KEY (prenotazione_id) REFERENCES prenotazione(id) ON DELETE CASCADE,
                FOREIGN KEY (ospite_id) REFERENCES ospite(id) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS prenotazione_stanza (
                prenotazione_id INTEGER NOT NULL,
                stanza_id INTEGER NOT NULL,
                PRIMARY KEY (prenotazione_id, stanza_id),
                FOREIGN KEY (prenotazione_id) REFERENCES prenotazione(id) ON DELETE CASCADE,
                FOREIGN KEY (stanza_id) REFERENCES stanza(id) ON DELETE RESTRICT
            )
        """)

        self.conn.commit()

    def seed_demo_data(self) -> None:
        cur = self.conn.cursor()

        cur.execute("SELECT COUNT(*) FROM stanza")
        stanze_presenti = cur.fetchone()[0]
        if stanze_presenti == 0:
            stanze = [
                ("10", "Singola", 1),
                ("11", "Doppia", 2),
                ("12", "Doppia", 2),
                ("20", "Doppia", 2),
                ("21", "Doppia", 2),
                ("22", "Tripla", 3),
                ("23", "Tripla", 3),
                ("30", "Suite", 4),
                ("31", "Suite", 4),
                ("40", "Familiare", 5),
            ]
            cur.executemany(
                "INSERT INTO stanza (numero, tipo, capienza) VALUES (?, ?, ?)",
                stanze
            )

        cur.execute("SELECT COUNT(*) FROM ospite")
        ospiti_presenti = cur.fetchone()[0]
        if ospiti_presenti == 0:
            ospiti = [
                ("Mario", "Rossi", "mario.rossi@example.com", "3331111111"),
                ("Anna", "Rossi", "anna.rossi@example.com", "3332222222"),
                ("Luca", "Bianchi", "luca.bianchi@example.com", "3333333333"),
                ("Sara", "Verdi", "sara.verdi@example.com", "3334444444"),
                ("Paolo", "Neri", "paolo.neri@example.com", "3335555555"),
            ]
            cur.executemany(
                "INSERT INTO ospite (nome, cognome, email, telefono) VALUES (?, ?, ?, ?)",
                ospiti
            )

        self.conn.commit()

        cur.execute("SELECT COUNT(*) FROM prenotazione")
        prenotazioni_presenti = cur.fetchone()[0]
        if prenotazioni_presenti == 0:
            cur.execute("SELECT id, numero FROM stanza")
            map_stanze = {numero: stanza_id for stanza_id, numero in cur.fetchall()}

            cur.execute("SELECT id, nome, cognome FROM ospite")
            map_ospiti = {(nome, cognome): ospite_id for ospite_id, nome, cognome in cur.fetchall()}

            self.create_booking(
                referente_nome="Mario Rossi",
                referente_contatto="mario.rossi@example.com",
                data_inizio=date(2026, 5, 10),
                data_fine=date(2026, 5, 13),
                ospite_ids=[map_ospiti[("Mario", "Rossi")]],
                stanza_ids=[map_stanze["10"]],
                note="Prenotazione demo con una sola stanza",
            )

            self.create_booking(
                referente_nome="Anna Rossi",
                referente_contatto="anna.rossi@example.com",
                data_inizio=date(2026, 5, 15),
                data_fine=date(2026, 5, 20),
                ospite_ids=[map_ospiti[("Anna", "Rossi")], map_ospiti[("Luca", "Bianchi")]],
                stanza_ids=[map_stanze["11"], map_stanze["12"]],
                note="Prenotazione demo con due stanze",
            )

            self.create_booking(
                referente_nome="Ufficio Viaggi IBM",
                referente_contatto="travel.office@ibm.example.com",
                data_inizio=date(2026, 6, 1),
                data_fine=date(2026, 6, 6),
                ospite_ids=[
                    map_ospiti[("Sara", "Verdi")],
                    map_ospiti[("Paolo", "Neri")],
                    map_ospiti[("Mario", "Rossi")],
                ],
                stanza_ids=[map_stanze["20"], map_stanze["21"], map_stanze["22"]],
                note="Prenotazione demo aziendale con tre stanze",
            )

    @staticmethod
    def parse_date(value: str) -> date:
        try:
            return datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError("Data non valida. Usare il formato YYYY-MM-DD.") from exc

    def list_stanze(self) -> List[Tuple[int, str, str, int]]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, numero, tipo, capienza FROM stanza ORDER BY numero")
        return cur.fetchall()

    def list_ospiti(self) -> List[Tuple[int, str, str, Optional[str], Optional[str]]]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, nome, cognome, email, telefono
            FROM ospite
            ORDER BY cognome, nome
        """)
        return cur.fetchall()

    def add_ospite(self, nome: str, cognome: str, email: str = "", telefono: str = "") -> int:
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO ospite (nome, cognome, email, telefono)
            VALUES (?, ?, ?, ?)
        """, (nome.strip(), cognome.strip(), email.strip() or None, telefono.strip() or None))
        self.conn.commit()
        return cur.lastrowid

    def add_stanza(self, numero: str, tipo: str, capienza: int) -> int:
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO stanza (numero, tipo, capienza)
            VALUES (?, ?, ?)
        """, (numero.strip(), tipo.strip(), capienza))
        self.conn.commit()
        return cur.lastrowid

    def find_overlaps(self, stanza_ids: List[int], data_inizio: date, data_fine: date) -> List[Tuple[str, int, str, str]]:
        if not stanza_ids:
            return []

        placeholders = ",".join("?" for _ in stanza_ids)
        query = f"""
            SELECT s.numero, p.id, p.data_inizio, p.data_fine
            FROM prenotazione p
            JOIN prenotazione_stanza ps ON ps.prenotazione_id = p.id
            JOIN stanza s ON s.id = ps.stanza_id
            WHERE ps.stanza_id IN ({placeholders})
              AND date(p.data_inizio) < date(?)
              AND date(?) < date(p.data_fine)
            ORDER BY s.numero, p.data_inizio
        """
        params = stanza_ids + [data_fine.isoformat(), data_inizio.isoformat()]
        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

    def create_booking(
        self,
        referente_nome: str,
        referente_contatto: str,
        data_inizio: date,
        data_fine: date,
        ospite_ids: List[int],
        stanza_ids: List[int],
        note: str = "",
    ) -> int:
        if data_inizio >= data_fine:
            raise ValueError("La data di fine deve essere successiva alla data di inizio.")

        if not stanza_ids:
            raise ValueError("Selezionare almeno una stanza.")

        overlaps = self.find_overlaps(stanza_ids, data_inizio, data_fine)
        if overlaps:
            dettagli = []
            for numero, pren_id, dal, al in overlaps:
                dettagli.append(
                    f"Stanza {numero} già occupata dalla prenotazione {pren_id} nel periodo {dal} -> {al}"
                )
            raise ValueError("Overlap rilevato:\n" + "\n".join(dettagli))

        cur = self.conn.cursor()
        try:
            cur.execute("""
                INSERT INTO prenotazione (referente_nome, referente_contatto, data_inizio, data_fine, note)
                VALUES (?, ?, ?, ?, ?)
            """, (
                referente_nome.strip(),
                referente_contatto.strip() or None,
                data_inizio.isoformat(),
                data_fine.isoformat(),
                note.strip() or None,
            ))
            prenotazione_id = cur.lastrowid

            for ospite_id in ospite_ids:
                cur.execute("""
                    INSERT INTO prenotazione_ospite (prenotazione_id, ospite_id)
                    VALUES (?, ?)
                """, (prenotazione_id, ospite_id))

            for stanza_id in stanza_ids:
                cur.execute("""
                    INSERT INTO prenotazione_stanza (prenotazione_id, stanza_id)
                    VALUES (?, ?)
                """, (prenotazione_id, stanza_id))

            self.conn.commit()
            return prenotazione_id
        except Exception:
            self.conn.rollback()
            raise

    def list_bookings(self) -> List[Tuple]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT p.id, p.referente_nome, p.referente_contatto, p.data_inizio, p.data_fine, p.note
            FROM prenotazione p
            ORDER BY p.data_inizio, p.id
        """)
        bookings = cur.fetchall()
        result = []

        for booking in bookings:
            pren_id = booking[0]

            cur.execute("""
                SELECT o.nome, o.cognome
                FROM prenotazione_ospite po
                JOIN ospite o ON o.id = po.ospite_id
                WHERE po.prenotazione_id = ?
                ORDER BY o.cognome, o.nome
            """, (pren_id,))
            ospiti = [f"{r[0]} {r[1]}" for r in cur.fetchall()]

            cur.execute("""
                SELECT s.numero
                FROM prenotazione_stanza ps
                JOIN stanza s ON s.id = ps.stanza_id
                WHERE ps.prenotazione_id = ?
                ORDER BY s.numero
            """, (pren_id,))
            stanze = [r[0] for r in cur.fetchall()]

            result.append(booking + (ospiti, stanze))

        return result

    def get_booking_by_id(self, prenotazione_id: int) -> Optional[Tuple]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT p.id, p.referente_nome, p.referente_contatto, p.data_inizio, p.data_fine, p.note
            FROM prenotazione p
            WHERE p.id = ?
        """, (prenotazione_id,))
        booking = cur.fetchone()
        if not booking:
            return None

        cur.execute("""
            SELECT o.nome, o.cognome
            FROM prenotazione_ospite po
            JOIN ospite o ON o.id = po.ospite_id
            WHERE po.prenotazione_id = ?
            ORDER BY o.cognome, o.nome
        """, (prenotazione_id,))
        ospiti = [f"{r[0]} {r[1]}" for r in cur.fetchall()]

        cur.execute("""
            SELECT s.numero
            FROM prenotazione_stanza ps
            JOIN stanza s ON s.id = ps.stanza_id
            WHERE ps.prenotazione_id = ?
            ORDER BY s.numero
        """, (prenotazione_id,))
        stanze = [r[0] for r in cur.fetchall()]

        return booking + (ospiti, stanze)

    def cancel_booking(self, prenotazione_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM prenotazione WHERE id = ?", (prenotazione_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def reset_database(self) -> None:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM prenotazione_ospite")
        cur.execute("DELETE FROM prenotazione_stanza")
        cur.execute("DELETE FROM prenotazione")
        cur.execute("DELETE FROM ospite")
        cur.execute("DELETE FROM stanza")
        self.conn.commit()
        self.seed_demo_data()

    def close(self) -> None:
        self.conn.close()


def print_stanze(app: HotelBookingApp) -> None:
    print("\nStanze disponibili nel sistema")
    print("-" * 60)
    for stanza_id, numero, tipo, capienza in app.list_stanze():
        print(f"[{stanza_id}] camera {numero} - {tipo} - capienza {capienza}")


def print_ospiti(app: HotelBookingApp) -> None:
    print("\nOspiti registrati")
    print("-" * 60)
    for ospite_id, nome, cognome, email, telefono in app.list_ospiti():
        print(f"[{ospite_id}] {nome} {cognome} - email: {email or '-'} - tel: {telefono or '-'}")


def print_bookings(app: HotelBookingApp) -> None:
    bookings = app.list_bookings()
    print("\nPrenotazioni")
    print("-" * 80)
    if not bookings:
        print("Nessuna prenotazione presente.")
        return

    for pren in bookings:
        pren_id, referente_nome, referente_contatto, data_inizio, data_fine, note, ospiti, stanze = pren
        print(f"ID: {pren_id}")
        print(f"Referente: {referente_nome} ({referente_contatto or '-'})")
        print(f"Periodo: {data_inizio} -> {data_fine}")
        print(f"Ospiti: {', '.join(ospiti) if ospiti else '-'}")
        print(f"Stanze: {', '.join(stanze) if stanze else '-'}")
        print(f"Note: {note or '-'}")
        print("-" * 80)


def input_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Inserire un numero intero valido.")


def input_id_list(prompt: str) -> List[int]:
    raw = input(prompt).strip()
    if not raw:
        return []
    try:
        values = [int(x.strip()) for x in raw.split(",") if x.strip()]
        return list(dict.fromkeys(values))
    except ValueError as exc:
        raise ValueError("Inserire una lista di ID numerici separati da virgola.") from exc


def menu_add_ospite(app: HotelBookingApp) -> None:
    print("\nInserimento nuovo ospite")
    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    email = input("Email: ").strip()
    telefono = input("Telefono: ").strip()

    if not nome or not cognome:
        print("Nome e cognome sono obbligatori.")
        return

    ospite_id = app.add_ospite(nome, cognome, email, telefono)
    print(f"Ospite creato con ID {ospite_id}.")


def menu_add_stanza(app: HotelBookingApp) -> None:
    print("\nInserimento nuova stanza")
    numero = input("Numero stanza: ").strip()
    tipo = input("Tipo stanza: ").strip()
    capienza = input_int("Capienza: ")

    if not numero or not tipo:
        print("Numero e tipo sono obbligatori.")
        return

    try:
        stanza_id = app.add_stanza(numero, tipo, capienza)
        print(f"Stanza creata con ID {stanza_id}.")
    except sqlite3.IntegrityError as exc:
        print(f"Errore inserimento stanza: {exc}")


def menu_create_booking(app: HotelBookingApp) -> None:
    print("\nCreazione prenotazione")
    referente_nome = input("Referente prenotazione: ").strip()
    referente_contatto = input("Contatto referente: ").strip()
    data_inizio_str = input("Data inizio (YYYY-MM-DD): ").strip()
    data_fine_str = input("Data fine   (YYYY-MM-DD): ").strip()
    note = input("Note: ").strip()

    if not referente_nome:
        print("Il referente è obbligatorio.")
        return

    try:
        data_inizio = app.parse_date(data_inizio_str)
        data_fine = app.parse_date(data_fine_str)
    except ValueError as exc:
        print(exc)
        return

    print_ospiti(app)
    try:
        ospite_ids = input_id_list("ID ospiti da associare, separati da virgola: ")
    except ValueError as exc:
        print(exc)
        return

    print_stanze(app)
    try:
        stanza_ids = input_id_list("ID stanze da prenotare, separati da virgola: ")
    except ValueError as exc:
        print(exc)
        return

    try:
        prenotazione_id = app.create_booking(
            referente_nome=referente_nome,
            referente_contatto=referente_contatto,
            data_inizio=data_inizio,
            data_fine=data_fine,
            ospite_ids=ospite_ids,
            stanza_ids=stanza_ids,
            note=note,
        )
        print(f"Prenotazione creata con ID {prenotazione_id}.")
    except ValueError as exc:
        print(f"Errore: {exc}")
    except sqlite3.IntegrityError as exc:
        print(f"Errore database: {exc}")


def menu_show_booking_by_id(app: HotelBookingApp) -> None:
    print("\nDettaglio prenotazione per ID")
    prenotazione_id = input_int("Inserire l'ID della prenotazione: ")
    pren = app.get_booking_by_id(prenotazione_id)

    if not pren:
        print("Prenotazione non trovata.")
        return

    pren_id, referente_nome, referente_contatto, data_inizio, data_fine, note, ospiti, stanze = pren
    print("-" * 80)
    print(f"ID: {pren_id}")
    print(f"Nome di chi ha prenotato: {referente_nome}")
    print(f"Contatto referente: {referente_contatto or '-'}")
    print(f"Periodo: {data_inizio} -> {data_fine}")
    print(f"Ospiti associati: {', '.join(ospiti) if ospiti else '-'}")
    print(f"Camere incluse nella prenotazione: {', '.join(stanze) if stanze else '-'}")
    print(f"Note: {note or '-'}")
    print("-" * 80)


def menu_cancel_booking(app: HotelBookingApp) -> None:
    print_bookings(app)
    prenotazione_id = input_int("Inserire l'ID della prenotazione da cancellare: ")
    if app.cancel_booking(prenotazione_id):
        print("Prenotazione cancellata.")
    else:
        print("Prenotazione non trovata.")


def menu_reset_database(app: HotelBookingApp) -> None:
    print("\nReset completo database e ricaricamento dati demo")
    conferma = input("Scrivere SI per confermare: ").strip()
    if conferma == "SI":
        app.reset_database()
        print("Database azzerato e ripopolato con 10 stanze, 5 clienti e 3 prenotazioni demo.")
    else:
        print("Operazione annullata.")


def menu_show_all_tables(app: HotelBookingApp) -> None:
    print("\nContenuto di tutte le tabelle")
    cur = app.conn.cursor()
    tables = ["ospite", "stanza", "prenotazione", "prenotazione_ospite", "prenotazione_stanza"]
    for table_name in tables:
        print(f"\nTabella: {table_name}")
        print("-" * 60)
        rows = cur.execute(f"SELECT * FROM {table_name}").fetchall()
        if not rows:
            print("(vuota)")
        else:
            for row in rows:
                print(row)


def main() -> None:
    app = HotelBookingApp()
    app.seed_demo_data()

    try:
        while True:
            print("\n" + "=" * 60)
            print("GESTIONE PRENOTAZIONI ALBERGO")
            print("=" * 60)
            print("1. Elencare stanze")
            print("2. Elencare ospiti")
            print("3. Inserire ospite")
            print("4. Inserire stanza")
            print("5. Creare prenotazione")
            print("6. Elencare prenotazioni")
            print("7. Mostrare dettaglio prenotazione per ID")
            print("8. Cancellare prenotazione")
            print("9. Reset database e ricaricare dati demo")
            print("10. Mostrare contenuto di tutte le tabelle")
            print("0. Uscire")

            scelta = input("Scelta: ").strip()

            if scelta == "1":
                print_stanze(app)
            elif scelta == "2":
                print_ospiti(app)
            elif scelta == "3":
                menu_add_ospite(app)
            elif scelta == "4":
                menu_add_stanza(app)
            elif scelta == "5":
                menu_create_booking(app)
            elif scelta == "6":
                print_bookings(app)
            elif scelta == "7":
                menu_show_booking_by_id(app)
            elif scelta == "8":
                menu_cancel_booking(app)
            elif scelta == "9":
                menu_reset_database(app)
            elif scelta == "10":
                menu_show_all_tables(app)
            elif scelta == "0":
                break
            else:
                print("Scelta non valida.")
    finally:
        app.close()


if __name__ == "__main__":
    main()
