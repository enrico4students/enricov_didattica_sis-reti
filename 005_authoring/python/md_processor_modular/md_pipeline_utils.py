"""
Modulo di utilità generali per la pipeline Markdown.

Questo modulo raccoglie funzioni helper riutilizzabili utilizzate in più
parti della pipeline di elaborazione Markdown → PDF.

Le utility fornite coprono principalmente:

- normalizzazione di nomi e filename;
- generazione di identificatori hash brevi;
- conversione di path in formato POSIX;
- calcolo del numero di linea all'interno di testi;
- scrittura ottimizzata di file testuali evitando riscritture inutili.

Funzioni principali:

- sanitize_name():
  converte una stringa arbitraria in un nome sicuro utilizzabile come
  filename o identificatore filesystem-friendly.

  Caratteristiche:
    - sostituisce caratteri non validi con underscore;
    - comprime underscore consecutivi;
    - rimuove underscore iniziali e finali;
    - garantisce un valore valido restituendo "item" se il risultato è
      vuoto.

- sha1_short():
  genera un identificatore SHA1 abbreviato a 10 caratteri esadecimali,
  utile per:
    - nomi univoci di file;
    - cache;
    - fingerprint leggere;
    - identificatori stabili.

- relative_posix_path():
  restituisce un path relativo con separatori POSIX "/" indipendentemente
  dal sistema operativo in uso.

  Questo comportamento è utile per:
    - link Markdown;
    - riferimenti HTML;
    - compatibilità Pandoc;
    - output multipiattaforma.

- line_number_from_index():
  converte una posizione assoluta all'interno di una stringa nel numero di
  linea corrispondente.

  La funzione è utile per:
    - logging;
    - diagnostica;
    - reporting errori;
    - estrazione blocchi Markdown o PlantUML.

- write_text_file_if_changed():
  scrive un file testuale solo se il contenuto è realmente cambiato.

  Comportamento:
    - crea automaticamente le directory mancanti;
    - evita riscritture inutili;
    - preserva timestamp dei file invariati;
    - restituisce True se il file è stato modificato;
    - restituisce False se il contenuto era già identico.

  La scrittura usa sempre:
    - codifica UTF-8;
    - terminatori di linea UNIX "\\n".

Il modulo non contiene logica specifica di business della pipeline:
fornisce esclusivamente funzionalità di supporto generiche e riutilizzabili.
"""


from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path


def sanitize_name(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_") or "item"


def sha1_short(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


def relative_posix_path(path: Path, start: Path) -> str:
    return os.path.relpath(path, start).replace("\\", "/")


def line_number_from_index(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def write_text_file_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8", newline="\n")
    return True
