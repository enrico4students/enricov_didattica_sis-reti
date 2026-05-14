"""
STEP 20.4 - Cleanup finale e scrittura output.

Questo modulo contiene funzioni di supporto per la fase finale dello
STEP 20.

Responsabilità principali:

- generare sintassi Markdown immagine compatibile con il tipo di documento;
- rimuovere semplici wrapper HTML intorno a immagini Markdown;
- scrivere il file Markdown preprocessato.

Il modulo è usato dal coordinatore STEP 20 e dagli altri sottostep quando
devono produrre riferimenti immagine coerenti.
"""

from __future__ import annotations

import re
from pathlib import Path


def build_image_markdown(
    md_type: str,
    alt: str,
    rel_path: str,
    width_percent: int | None = None,
) -> str:
    alt = alt or "immagine"

    if md_type == "marp":
        if width_percent is not None:
            return f"![width:{width_percent}%]({rel_path})"
        return f"![{alt}]({rel_path})"

    if md_type == "pandoc":
        if width_percent is not None:
            return f"![{alt}]({rel_path}){{ width={width_percent}% }}"
        return f"![{alt}]({rel_path})"

    return f"![{alt}]({rel_path})"


def clean_html_wrappers(text: str) -> str:
    pattern = re.compile(r'(?is)<div[^>]*>\s*(\!\[[^\]]*\]\([^\)]*\)(?:\{[^}]*\})?)\s*</div>')
    return pattern.sub(r"\1", text)


def write_processed_markdown(
    path: Path,
    text: str,
    dry_run: bool = False,
) -> None:
    if dry_run:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

