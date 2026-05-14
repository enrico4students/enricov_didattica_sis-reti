"""
STEP 20.1 - Analisi del tipo di Markdown.

Questo modulo riconosce il tipo di Markdown usato da un documento sorgente.

Tipi riconosciuti:

- marp:
  documento con front matter YAML contenente la chiave marp;

- pandoc:
  documento con costrutti tipici di Pandoc Markdown;

- standard:
  documento senza segnali specifici di Marp o Pandoc.

Il risultato dell'analisi viene usato dagli step successivi per generare
sintassi immagine compatibile con il tipo di documento.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownTypeInfo:
    kind: str
    reason: str


def detect_markdown_type(text: str) -> MarkdownTypeInfo:
    frontmatter_match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    frontmatter = frontmatter_match.group(1) if frontmatter_match else ""

    if re.search(r"(?mi)^\s*marp\s*:\s*(true|false)\s*$", frontmatter):
        return MarkdownTypeInfo("marp", "Front matter YAML con chiave 'marp:'")

    pandoc_signals = [
        r"\{[^\n}]*\swidth\s*=\s*[^}]+\}",
        r"\[\^[^\]]+\]:",
        r"(?m)^Table:\s",
        r"(?m)^\s*:[^:\n]+:\s*",
    ]

    for pattern in pandoc_signals:
        if re.search(pattern, text):
            return MarkdownTypeInfo(
                "pandoc",
                f"Rilevato costrutto compatibile con Pandoc Markdown: {pattern}",
            )

    return MarkdownTypeInfo(
        "standard",
        "Nessun segnale specifico di Marp o Pandoc Markdown",
    )
