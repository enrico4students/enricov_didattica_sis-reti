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
