"""
Modulo per la raccolta e validazione degli input Markdown della pipeline.

Questo modulo individua quali file Markdown devono essere elaborati dalla
pipeline, a partire da un file singolo, da una directory src oppure da una
directory più ampia contenente una o più sottodirectory src.

La logica del modulo applica alcune regole precise:

- vengono accettati solo file Markdown con estensioni riconosciute;

- i file sorgenti devono trovarsi direttamente dentro una directory src;

- i file temporanei con nome che inizia per temp vengono ignorati;

- le directory generate dalla pipeline vengono escluse dalla scansione;

- i file già processati, riconoscibili dal suffisso _processed, vengono
  esclusi.

Estensioni Markdown riconosciute:

- .md
- .markdown
- .mdown
- .mkd

Funzioni principali:

- is_markdown_file():
  verifica se un path corrisponde a un file Markdown valido;

- is_already_processed():
  riconosce file o directory che appartengono a output già generati dalla
  pipeline e che quindi non devono essere rielaborati;

- should_process_md_file():
  applica le regole specifiche per decidere se un file Markdown deve essere
  incluso nell'elaborazione;

- collect_markdown_inputs():
  restituisce l'elenco ordinato dei file Markdown da elaborare, validando
  l'input ricevuto e gestendo tre casi:
    - input come file Markdown singolo;
    - input come directory src;
    - input come directory generica da scandire ricorsivamente.

Il modulo non modifica file e directory: si limita a individuare e validare
gli input da passare alle fasi successive della pipeline. Le informazioni
operative vengono registrate tramite il logger condiviso del progetto.
"""


from __future__ import annotations

from pathlib import Path

from md_pipeline_logging import logger


def is_markdown_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in {".md", ".markdown", ".mdown", ".mkd"}


def is_already_processed(path: Path) -> bool:
    parts_lower = {part.lower() for part in path.parts}
    generated_dirs = {"out", "published", "step20_md", "step40_pdf", "step90_publish"}
    return bool(parts_lower & generated_dirs) or path.stem.endswith("_processed")


def should_process_md_file(md_file: Path) -> bool:
    if md_file.name.lower().startswith("temp"):
        return False
    return md_file.parent.name == "src"


def collect_markdown_inputs(input_path: Path) -> list[Path]:
    input_path = input_path.expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Percorso non trovato: {input_path}")

    if input_path.is_file():
        if not is_markdown_file(input_path):
            raise ValueError(f"Il file indicato non è un file Markdown: {input_path}")
        if not should_process_md_file(input_path):
            raise ValueError(f"Il file Markdown deve trovarsi direttamente in una directory src/: {input_path}")
        logger.info(f"Input file Markdown valido: {input_path}")
        return [input_path]

    if input_path.is_dir() and input_path.name == "src":
        logger.info(f"Input directory src: {input_path}")
        files = sorted(
            path for path in input_path.iterdir()
            if is_markdown_file(path) and should_process_md_file(path)
        )
        logger.info(f"File Markdown trovati direttamente in src/: {len(files)}")
        return files

    if input_path.is_dir():
        logger.info(f"Input directory generica, scansione ricorsiva delle directory src/: {input_path}")
        src_dirs = sorted(
            path for path in input_path.rglob("src")
            if path.is_dir() and not is_already_processed(path)
        )
        logger.info(f"Directory src trovate: {len(src_dirs)}")

        files: list[Path] = []
        for src_dir in src_dirs:
            logger.info(f"Esamino directory src: {src_dir}")
            md_files = sorted(
                path for path in src_dir.iterdir()
                if is_markdown_file(path) and should_process_md_file(path)
            )
            logger.info(f"Markdown trovati in {src_dir}: {len(md_files)}")
            files.extend(md_files)

        return sorted(files)

    raise ValueError(f"Input non valido: {input_path}")
