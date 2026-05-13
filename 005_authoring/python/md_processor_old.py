#!/usr/bin/env python3
"""
Pipeline di processamento Markdown per documenti organizzati in cartelle src/.

Il programma accetta come parametro un file o una directory.

Comportamento previsto:

- Se il parametro è un file Markdown:
  - il file deve trovarsi direttamente dentro una directory chiamata src;
  - se non è così, il programma segnala errore ed esce;
  - se è valido, viene elaborato solo quel file.

- Se il parametro è una directory chiamata src:
  - vengono elaborati tutti i file Markdown direttamente contenuti in quella directory;
  - non vengono scansionate ricorsivamente eventuali sottodirectory di src.

- Se il parametro è una directory con nome diverso da src:
  - viene scansionato ricorsivamente l'albero;
  - ogni directory src trovata viene trattata come unità di input;
  - per ciascuna src vengono elaborati i soli file Markdown direttamente contenuti in essa;
  - i file Markdown fuori da src non vengono elaborati.

Per ogni file Markdown valido la pipeline produce:

- step20_md/      Markdown elaborato, con immagini e PlantUML normalizzati;
- step40_pdf/     PDF non rasterizzato generato con Pandoc;
- step90_PUBLISH/ PDF rasterizzato *_ro, pensato per la pubblicazione.

Il programma traccia su console e, se configurato nel codice corrente, su file di log,
i passi eseguiti, i file letti, i file scritti e gli eventuali errori.
"""
from __future__ import annotations

import argparse
import hashlib
import logging
import os
import re
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from urllib.parse import unquote, urlparse

import requests
from PIL import Image
import pymupdf  # PyMuPDF

logger = logging.getLogger("md_pipeline")


def configure_logging(verbose: bool, log_file: Path) -> None:
    """Configura logging sia su console sia su file."""
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info(f"Log file: {log_file}")


def log_step(message: str) -> None:
    logger.info(f"STEP: {message}")


def log_read(path: Path) -> None:
    logger.info(f"LEGGE: {path}")


def log_write(path: Path) -> None:
    logger.info(f"SCRIVE: {path}")


@dataclass(frozen=True)
class MarkdownTypeInfo:
    kind: str
    reason: str


@dataclass(frozen=True)
class PlantUMLBlock:
    ordinal: int
    start_line: int
    fence: Optional[str]
    info: str
    body: str
    start_idx: int
    end_idx: int
    puml_path: Path
    jpg_path: Path


@dataclass(frozen=True)
class ImageReference:
    ordinal: int
    start_idx: int
    end_idx: int
    start_line: int
    source_type: str
    raw: str
    alt: str
    src: str
    title: Optional[str]
    attrs: Optional[str]
    html_width: Optional[str]


@dataclass(frozen=True)
class ProcessResult:
    processed_text: str
    actions: List[str]


FENCE_PATTERN = re.compile(
    r"(?ms)^(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>[^\n`]*)\n(?P<body>.*?)^\1[ \t]*$"
)

FREE_PLANTUML_PATTERN = re.compile(
    r"(?ms)^[ \t]*@startuml[ \t]*(?P<info>[^\n]*)\n(?P<body>.*?)^[ \t]*@enduml[ \t]*$"
)


# -----------------------------------------------------------------------------
# Utility generali
# -----------------------------------------------------------------------------


def sanitize_name(name: str) -> str:
    """Rende una stringa utilizzabile in modo sicuro come parte di un nome file."""
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_") or "item"


def sha1_short(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def relative_posix_path(path: Path, start: Path) -> str:
    """Restituisce un path relativo con separatori '/', adatto a Markdown/Pandoc/Marp."""
    return os.path.relpath(path, start).replace("\\", "/")


def is_remote_url(value: str) -> bool:
    return value.lower().startswith(("http://", "https://"))


def infer_extension_from_url(url: str) -> str:
    parsed = urlparse(url)
    ext = Path(unquote(parsed.path)).suffix.lower()
    return ext or ".bin"


def line_number_from_index(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def write_text_file_if_changed(path: Path, content: str) -> bool:
    ensure_dir(path.parent)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


# -----------------------------------------------------------------------------
# Rilevamento tipo Markdown
# -----------------------------------------------------------------------------


def has_yaml_frontmatter(text: str) -> bool:
    return bool(re.match(r"\A---\s*\n.*?\n---\s*(?:\n|$)", text, re.DOTALL))


def extract_yaml_frontmatter(text: str) -> str:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    return match.group(1) if match else ""


def detect_markdown_type(text: str) -> MarkdownTypeInfo:
    frontmatter = extract_yaml_frontmatter(text) if has_yaml_frontmatter(text) else ""

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
            return MarkdownTypeInfo("pandoc", f"Rilevato costrutto compatibile con Pandoc Markdown: {pattern}")

    return MarkdownTypeInfo("standard", "Nessun segnale specifico di Marp o Pandoc Markdown")


# -----------------------------------------------------------------------------
# Conferme interattive
# -----------------------------------------------------------------------------


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



# ----------------------------------------------------------------------------
# Dir/path utilities, per gli steps
# -----------------------------------------------------------------------------

def get_doc_root_from_processed_md(markdown_path: Path) -> Path:
    if markdown_path.parent.name == "step20_md":
        return markdown_path.parent.parent
    return markdown_path.parent


def get_pandoc_resource_path_for_processed_md(markdown_path: Path) -> str:
    doc_root = get_doc_root_from_processed_md(markdown_path)

    resource_paths = [
        markdown_path.parent,      # step20_md
        doc_root / "imgs",         # immagini generate
        doc_root / "puml",         # eventuali sorgenti/risorse PlantUML
        doc_root / "src",          # eventuali risorse ancora relative al sorgente
    ]

    existing_paths = [str(path) for path in resource_paths if path.exists()]
    return os.pathsep.join(existing_paths)


# -----------------------------------------------------------------------------
# Layout progetto
# -----------------------------------------------------------------------------


def should_process_md_file(md_file: Path) -> bool:
    """Sono elaborati solo i Markdown direttamente contenuti in una cartella src/."""
    if md_file.name.lower().startswith("temp"):
        return False
    return md_file.parent.name == "src"


def get_dirs_for_valid_md(md_file: Path) -> Tuple[Path, Path]:
    doc_root = md_file.parent.parent
    return doc_root / "imgs", doc_root / "puml"


def get_output_path_for_md(md_file: Path) -> Path:
    """Restituisce il path del Markdown elaborato: step20_md/."""
    if should_process_md_file(md_file):
        doc_root = md_file.parent.parent
        return doc_root / "step20_md" / md_file.name
    return md_file.with_name(f"{md_file.stem}_processed{md_file.suffix}")


def get_pdf_output_path_for_md(md_file: Path) -> Path:
    """Restituisce il path del PDF non rasterizzato: step40_pdf/."""
    if should_process_md_file(md_file):
        doc_root = md_file.parent.parent
        return doc_root / "step40_pdf" / f"{md_file.stem}.pdf"
    return get_output_path_for_md(md_file).with_suffix(".pdf")


def get_publish_output_path_for_md(md_file: Path) -> Path:
    """Restituisce il path del PDF rasterizzato pubblicabile: step90_PUBLISH/."""
    if should_process_md_file(md_file):
        doc_root = md_file.parent.parent
        return doc_root / "step90_PUBLISH" / f"{md_file.stem}_ro.pdf"
    output_path = get_output_path_for_md(md_file)
    return output_path.parent / f"{output_path.stem}_ro.pdf"


def get_image_dir_for_md(md_file: Path) -> Path:
    if should_process_md_file(md_file):
        img_dir, _ = get_dirs_for_valid_md(md_file)
        return img_dir
    return md_file.parent / "imgs"


def get_puml_dir_for_md(md_file: Path) -> Path:
    if should_process_md_file(md_file):
        _, puml_dir = get_dirs_for_valid_md(md_file)
        return puml_dir
    return md_file.parent / "puml"


# -----------------------------------------------------------------------------
# Conversione immagini
# -----------------------------------------------------------------------------


def flatten_on_white(img: Image.Image) -> Image.Image:
    """Rimuove la trasparenza prima del salvataggio JPEG."""
    if img.mode in ("RGBA", "LA"):
        rgba = img.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        return Image.alpha_composite(background, rgba).convert("RGB")

    if img.mode == "P" and "transparency" in img.info:
        rgba = img.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        return Image.alpha_composite(background, rgba).convert("RGB")

    if img.mode != "RGB":
        return img.convert("RGB")

    return img


def needs_regeneration(source: Path, target: Path) -> bool:
    if not target.exists():
        return True
    try:
        return source.stat().st_mtime_ns > target.stat().st_mtime_ns
    except FileNotFoundError:
        return True


def convert_svg_to_png(svg_path: Path, png_path: Path) -> bool:
    """Converte SVG in PNG usando cairosvg o rsvg-convert."""
    try:
        import cairosvg

        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), background_color="white")
        return True
    except Exception as exc:
        logger.warning(f"Conversione SVG con cairosvg fallita per {svg_path}: {exc}")

    if shutil.which("rsvg-convert"):
        result = subprocess.run(
            ["rsvg-convert", "-b", "white", "-o", str(png_path), str(svg_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and png_path.exists():
            return True
        logger.warning(f"Conversione SVG con rsvg-convert fallita per {svg_path}: {result.stderr}")

    logger.error(f"Impossibile convertire SVG: {svg_path}. Installare cairosvg o rsvg-convert.")
    return False


def download_remote_image(url: str, target_path: Path, timeout: int = 30, dry_run: bool = False) -> bool:
    if dry_run:
        logger.info(f"[DRY RUN] Simulato download da {url} -> {target_path}")
        return True

    ensure_dir(target_path.parent)
    try:
        with requests.get(url, stream=True, timeout=timeout) as response:
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "").lower()
            if content_type and not content_type.startswith("image/"):
                logger.warning(f"Content-Type non immagine per {url}: {content_type}")

            with open(target_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=65536):
                    if chunk:
                        file.write(chunk)
        return True
    except requests.RequestException as exc:
        logger.error(f"Download fallito per {url}: {exc}")
        return False


def copy_or_convert_to_jpg(src_path: Path, target_jpg_path: Path, dry_run: bool = False) -> None:
    if dry_run:
        logger.info(f"[DRY RUN] Simulata copia/conversione da {src_path} -> {target_jpg_path}")
        return

    ensure_dir(target_jpg_path.parent)
    with Image.open(src_path) as img:
        img = flatten_on_white(img)
        img.save(target_jpg_path, "JPEG", quality=95)


def normalize_remote_to_jpg(url: str, target_jpg_path: Path, temp_dir: Path, dry_run: bool = False) -> bool:
    if dry_run:
        logger.info(f"[DRY RUN] Simulata normalizzazione remota {url} -> {target_jpg_path}")
        return True

    ensure_dir(temp_dir)
    temp_path = temp_dir / f"download_{sha1_short(url)}{infer_extension_from_url(url)}"

    if not download_remote_image(url, temp_path, dry_run=dry_run):
        return False

    try:
        if temp_path.suffix.lower() == ".svg":
            png_temp = temp_path.with_suffix(".png")
            if not convert_svg_to_png(temp_path, png_temp):
                return False
            copy_or_convert_to_jpg(png_temp, target_jpg_path, dry_run=dry_run)
            png_temp.unlink(missing_ok=True)
            return True

        copy_or_convert_to_jpg(temp_path, target_jpg_path, dry_run=dry_run)
        return True
    finally:
        temp_path.unlink(missing_ok=True)


def local_image_to_jpg(src_path: Path, target_jpg_path: Path, dry_run: bool = False) -> None:
    if dry_run:
        logger.info(f"[DRY RUN] Simulata copia/conversione locale da {src_path} -> {target_jpg_path}")
        return

    if src_path.suffix.lower() in (".jpg", ".jpeg"):
        ensure_dir(target_jpg_path.parent)
        if src_path.resolve() != target_jpg_path.resolve():
            shutil.copy2(src_path, target_jpg_path)
        return

    if src_path.suffix.lower() == ".svg":
        png_temp = target_jpg_path.with_suffix(".tmp.png")
        if not convert_svg_to_png(src_path, png_temp):
            raise RuntimeError(f"Conversione SVG fallita: {src_path}")
        try:
            copy_or_convert_to_jpg(png_temp, target_jpg_path, dry_run=False)
        finally:
            png_temp.unlink(missing_ok=True)
        return

    copy_or_convert_to_jpg(src_path, target_jpg_path, dry_run=False)


# -----------------------------------------------------------------------------
# Parsing di blocchi da escludere
# -----------------------------------------------------------------------------


def get_fenced_spans(text: str) -> List[Tuple[int, int]]:
    return [(match.start(), match.end()) for match in FENCE_PATTERN.finditer(text)]


def get_inline_code_spans(text: str) -> List[Tuple[int, int]]:
    spans: List[Tuple[int, int]] = []
    i = 0
    n = len(text)

    while i < n:
        if text[i] != "`":
            i += 1
            continue

        start = i
        tick_count = 1
        i += 1
        while i < n and text[i] == "`":
            tick_count += 1
            i += 1

        fence = "`" * tick_count
        close = text.find(fence, i)
        if close == -1:
            continue

        spans.append((start, close + tick_count))
        i = close + tick_count

    return spans


def get_html_code_spans(text: str) -> List[Tuple[int, int]]:
    pattern = re.compile(r"(?is)<(code|pre)\b[^>]*>.*?</\1\s*>")
    return [(match.start(), match.end()) for match in pattern.finditer(text)]


def merge_spans(spans: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    sorted_spans = sorted(spans)
    if not sorted_spans:
        return []

    merged = [sorted_spans[0]]
    for start, end in sorted_spans[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def is_inside_spans(pos: int, spans: List[Tuple[int, int]]) -> bool:
    return any(start <= pos < end for start, end in spans)


# -----------------------------------------------------------------------------
# PlantUML
# -----------------------------------------------------------------------------


def make_plantuml_block(
    md_file: Path,
    ordinal: int,
    start_line: int,
    fence: Optional[str],
    info: str,
    body: str,
    start_idx: int,
    end_idx: int,
) -> PlantUMLBlock:
    base_name = sanitize_name(md_file.stem)
    suffix = f"{base_name}_{ordinal}_r{start_line}"
    return PlantUMLBlock(
        ordinal=ordinal,
        start_line=start_line,
        fence=fence,
        info=info,
        body=body,
        start_idx=start_idx,
        end_idx=end_idx,
        puml_path=get_puml_dir_for_md(md_file) / f"{suffix}.puml",
        jpg_path=get_image_dir_for_md(md_file) / f"{suffix}_puml.jpg",
    )


def find_plantuml_blocks(text: str, md_file: Path) -> List[PlantUMLBlock]:
    """Rileva blocchi PlantUML senza creare directory o file."""
    blocks: List[PlantUMLBlock] = []
    fenced_spans: List[Tuple[int, int]] = []
    ordinal = 0

    for match in FENCE_PATTERN.finditer(text):
        fenced_spans.append((match.start(), match.end()))

        info = (match.group("info") or "").strip().lower()
        body = match.group("body") or ""

        is_declared_plantuml = any(keyword in info for keyword in ("plantuml", "puml", "uml"))
        is_body_plantuml = bool(re.search(r"(?mi)^\s*@startuml\b", body)) and bool(
            re.search(r"(?mi)^\s*@enduml\b", body)
        )

        if not (is_declared_plantuml or is_body_plantuml):
            continue

        ordinal += 1
        start_line = line_number_from_index(text, match.start())
        blocks.append(
            make_plantuml_block(
                md_file=md_file,
                ordinal=ordinal,
                start_line=start_line,
                fence=match.group("fence"),
                info=match.group("info") or "",
                body=body,
                start_idx=match.start(),
                end_idx=match.end(),
            )
        )

    for match in FREE_PLANTUML_PATTERN.finditer(text):
        if is_inside_spans(match.start(), fenced_spans):
            continue

        ordinal += 1
        start_line = line_number_from_index(text, match.start())
        full_body = text[match.start() : match.end()]
        blocks.append(
            make_plantuml_block(
                md_file=md_file,
                ordinal=ordinal,
                start_line=start_line,
                fence=None,
                info=match.group("info") or "",
                body=full_body,
                start_idx=match.start(),
                end_idx=match.end(),
            )
        )

    return sorted(blocks, key=lambda block: block.start_idx)


def render_plantuml_to_jpg(puml_path: Path, jpg_path: Path, plantuml_jar: Path, dry_run: bool = False) -> None:
    if dry_run:
        logger.info(f"[DRY RUN] Simulata generazione JPG da {puml_path} -> {jpg_path}")
        return

    if not plantuml_jar.exists():
        raise FileNotFoundError(f"PlantUML jar non trovato: {plantuml_jar}")

    result = subprocess.run(
        ["java", "-jar", str(plantuml_jar), "-tpng", str(puml_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"PlantUML fallito: {result.stderr}")

    generated_png = puml_path.with_suffix(".png")
    if not generated_png.exists():
        raise RuntimeError("PNG non generato da PlantUML")

    ensure_dir(jpg_path.parent)
    with Image.open(generated_png) as img:
        img = flatten_on_white(img)
        img.save(jpg_path, "JPEG", quality=95)

    generated_png.unlink(missing_ok=True)


def build_image_markdown(md_type: str, alt: str, rel_path: str, width_percent: Optional[int] = None) -> str:
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


def process_plantuml_blocks(
    text: str,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    plantuml_jar: Optional[Path],
    keep_source: bool = False,
    dry_run: bool = False,
) -> Tuple[str, List[str]]:
    blocks = find_plantuml_blocks(text, md_file)
    if not blocks:
        return text, []

    if plantuml_jar is None:
        raise RuntimeError("Sono presenti blocchi PlantUML: specificare --plantuml-jar o PLANTUML_JAR")

    actions: List[str] = []
    result_parts: List[str] = []
    last_idx = 0
    out_file = get_output_path_for_md(md_file)

    if not dry_run:
        ensure_dir(get_puml_dir_for_md(md_file))
        ensure_dir(get_image_dir_for_md(md_file))

    for block in blocks:
        result_parts.append(text[last_idx:block.start_idx])
        last_idx = block.end_idx

        desc = (
            f"Trovato blocco PlantUML (riga {block.start_line}).\n"
            f"File .puml: {block.puml_path}\n"
            f"Immagine: {block.jpg_path}"
        )
        if not confirm.ask(desc):
            result_parts.append(text[block.start_idx:block.end_idx])
            actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: saltato")
            continue

        body = block.body.strip() or 'note "Diagramma vuoto"'
        puml_content = body if re.match(r"^\s*@startuml", body, re.IGNORECASE) else f"@startuml\n{body}\n@enduml"

        if dry_run:
            actions.append(f"[DRY RUN] PlantUML blocco {block.ordinal}: scritto {block.puml_path.name}")
        elif write_text_file_if_changed(block.puml_path, puml_content):
            actions.append(f"PlantUML blocco {block.ordinal}: creato/aggiornato {block.puml_path.name}")
        else:
            actions.append(f"PlantUML blocco {block.ordinal}: invariato")

        if dry_run:
            actions.append(f"[DRY RUN] PlantUML blocco {block.ordinal}: generato/aggiornato JPG")
        elif needs_regeneration(block.puml_path, block.jpg_path):
            render_plantuml_to_jpg(block.puml_path, block.jpg_path, plantuml_jar, dry_run=False)
            actions.append(f"PlantUML blocco {block.ordinal}: creato/aggiornato JPG")
        else:
            actions.append(f"PlantUML blocco {block.ordinal}: JPG già aggiornato")

        rel_img = relative_posix_path(block.jpg_path, out_file.parent)
        img_md = build_image_markdown(md_type.kind, f"PlantUML {block.ordinal}", rel_img, width_percent=70)

        if keep_source:
            result_parts.append(text[block.start_idx:block.end_idx] + "\n\n" + img_md)
        else:
            result_parts.append(img_md)

    result_parts.append(text[last_idx:])
    return "".join(result_parts), actions


# -----------------------------------------------------------------------------
# Rilevamento immagini Markdown e HTML
# -----------------------------------------------------------------------------


def find_html_images(text: str, excluded_spans: Optional[List[Tuple[int, int]]] = None) -> List[ImageReference]:
    excluded_spans = excluded_spans or []
    img_tag_pattern = re.compile(r"(?is)<img\b[^>]*>")
    src_pattern = re.compile(r'''(?is)\bsrc\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))''')
    alt_pattern = re.compile(r'''(?is)\balt\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))''')
    width_pattern = re.compile(r'''(?is)\bwidth\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))''')
    style_pattern = re.compile(r'''(?is)\bstyle\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))''')

    refs: List[ImageReference] = []
    ordinal = 0

    for match in img_tag_pattern.finditer(text):
        if is_inside_spans(match.start(), excluded_spans):
            continue

        tag = match.group(0)
        src_match = src_pattern.search(tag)
        if not src_match:
            continue

        src = (src_match.group(2) or src_match.group(3) or src_match.group(4) or "").strip()
        alt_match = alt_pattern.search(tag)
        width_match = width_pattern.search(tag)
        style_match = style_pattern.search(tag)

        alt = (alt_match.group(2) or alt_match.group(3) or alt_match.group(4) or "").strip() if alt_match else ""
        width = (
            (width_match.group(2) or width_match.group(3) or width_match.group(4) or "").strip()
            if width_match
            else None
        )
        style = (
            (style_match.group(2) or style_match.group(3) or style_match.group(4) or "").strip()
            if style_match
            else None
        )

        html_width = width
        if not html_width and style:
            style_width = re.search(r"(?i)\b(?:max-width|width)\s*:\s*(\d+)\s*%", style)
            if style_width:
                html_width = f"{style_width.group(1)}%"

        ordinal += 1
        refs.append(
            ImageReference(
                ordinal=ordinal,
                start_idx=match.start(),
                end_idx=match.end(),
                start_line=line_number_from_index(text, match.start()),
                source_type="html",
                raw=tag,
                alt=alt,
                src=src,
                title=None,
                attrs=None,
                html_width=html_width,
            )
        )

    return refs


def parse_markdown_image_inner(inner: str) -> Tuple[str, Optional[str]]:
    inner = inner.strip()
    if not inner:
        return "", None

    if inner.startswith("<"):
        close = inner.find(">")
        if close != -1:
            src = inner[1:close].strip()
            rest = inner[close + 1 :].strip()
            if len(rest) >= 2 and rest[0] == rest[-1] and rest[0] in "'\"":
                return src, rest[1:-1]
            return src, None

    match = re.match(r'^(?P<src>.+?)\s+(?P<title>"[^"]*"|\'[^\']*\')\s*$', inner, re.DOTALL)
    if match:
        src = (match.group("src") or "").strip()
        title = (match.group("title") or "").strip().strip("\"'")
        return src, title

    return inner, None


def find_matching_paren(text: str, start_pos: int) -> int:
    depth = 0
    i = start_pos
    in_angle = False

    while i < len(text):
        char = text[i]
        if char == "<" and depth == 1 and not in_angle:
            in_angle = True
        elif char == ">" and in_angle:
            in_angle = False
        elif not in_angle:
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    return i
        i += 1

    return -1


def parse_attrs_block(text: str, pos: int) -> Tuple[Optional[str], int]:
    if pos >= len(text) or text[pos] != "{":
        return None, pos

    depth = 0
    i = pos
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[pos : i + 1], i + 1
        i += 1

    return None, pos


def find_markdown_images(text: str, excluded_spans: Optional[List[Tuple[int, int]]] = None) -> List[ImageReference]:
    excluded_spans = excluded_spans or []
    refs: List[ImageReference] = []
    ordinal = 0
    i = 0

    while i < len(text):
        pos = text.find("![", i)
        if pos == -1:
            break

        if is_inside_spans(pos, excluded_spans):
            i = pos + 2
            continue

        alt_end = text.find("]", pos + 2)
        if alt_end == -1 or alt_end + 1 >= len(text) or text[alt_end + 1] != "(":
            i = pos + 2
            continue

        paren_start = alt_end + 1
        paren_end = find_matching_paren(text, paren_start)
        if paren_end == -1:
            i = pos + 2
            continue

        attrs = None
        end_idx = paren_end + 1
        attrs_candidate, new_pos = parse_attrs_block(text, end_idx)
        if attrs_candidate is not None:
            attrs = attrs_candidate
            end_idx = new_pos

        raw = text[pos:end_idx]
        alt = text[pos + 2 : alt_end]
        inner = text[paren_start + 1 : paren_end]
        src, title = parse_markdown_image_inner(inner)

        if src:
            ordinal += 1
            refs.append(
                ImageReference(
                    ordinal=ordinal,
                    start_idx=pos,
                    end_idx=end_idx,
                    start_line=line_number_from_index(text, pos),
                    source_type="markdown",
                    raw=raw,
                    alt=alt,
                    src=src,
                    title=title,
                    attrs=attrs,
                    html_width=None,
                )
            )

        i = end_idx

    return refs


def extract_width_percent_from_ref(ref: ImageReference) -> Optional[int]:
    """Estrae una larghezza percentuale da HTML width/style o da attributi Pandoc."""
    candidates = [ref.html_width or "", ref.attrs or "", ref.raw or ""]
    for candidate in candidates:
        match = re.search(r"(?i)(?:width|max-width)\s*[:=]\s*(\d+)\s*%", candidate)
        if match:
            return int(match.group(1))

    if ref.html_width:
        match = re.match(r"^\s*(\d+)\s*%\s*$", ref.html_width)
        if match:
            return int(match.group(1))

    return None


def build_replacement_image_markup(
    md_type: MarkdownTypeInfo,
    ref: ImageReference,
    rel_path: str,
    ordinal: int,
) -> str:
    alt = ref.alt or f"image_{ordinal}"
    width_percent = extract_width_percent_from_ref(ref)

    # Per immagini Markdown si conservano gli attributi Pandoc originali, se presenti.
    if ref.source_type == "markdown" and ref.attrs and md_type.kind != "marp":
        return f"![{alt}]({rel_path}){ref.attrs}"

    return build_image_markdown(md_type.kind, alt, rel_path, width_percent=width_percent)


def build_target_jpg_path_for_image(md_file: Path, ordinal: int, line_no: int, source: str) -> Path:
    base = sanitize_name(md_file.stem)
    source_stem = "remote_" + sha1_short(source) if is_remote_url(source) else sanitize_name(Path(source).stem)
    filename = f"{base}_img{ordinal}_r{line_no}_{source_stem}.jpg"
    return get_image_dir_for_md(md_file) / filename


# -----------------------------------------------------------------------------
# Gestione singole immagini
# -----------------------------------------------------------------------------


def handle_remote_image_reference(
    ref: ImageReference,
    ordinal: int,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    target_jpg_path: Path,
    temp_dir: Path,
    output_dir: Path,
    dry_run: bool,
    force_remote: bool = False,
) -> Tuple[str, List[str]]:
    actions: List[str] = []
    rel_path = relative_posix_path(target_jpg_path, output_dir)

    desc = (
        f"Trovata immagine remota.\n"
        f"Riga: {ref.start_line}\n"
        f"Origine: {ref.src}\n"
        f"Verrà scaricata e convertita in JPG.\n"
        f"Target: {target_jpg_path}\n"
        f"Nel file out/: {rel_path}"
    )
    if not confirm.ask(desc):
        actions.append(f"Immagine remota riga {ref.start_line}: operazione saltata")
        return ref.raw, actions

    if target_jpg_path.exists() and not dry_run and not force_remote:
        actions.append(f"Immagine remota riga {ref.start_line}: JPG già esistente")
        return build_replacement_image_markup(md_type, ref, rel_path, ordinal), actions

    if normalize_remote_to_jpg(ref.src, target_jpg_path, temp_dir, dry_run=dry_run):
        prefix = "[DRY RUN] " if dry_run else ""
        actions.append(f"{prefix}Immagine remota riga {ref.start_line}: salvata come {target_jpg_path.name}")
        return build_replacement_image_markup(md_type, ref, rel_path, ordinal), actions

    actions.append(f"Immagine remota riga {ref.start_line}: conversione fallita, riferimento originale mantenuto")
    return ref.raw, actions


def resolve_local_image_source(md_file: Path, src: str) -> Optional[Path]:
    requested_source = Path(src) if os.path.isabs(src) else md_file.parent / src
    requested_source = requested_source.resolve()

    if requested_source.exists():
        return requested_source

    # Utile quando il Markdown punta già a un nome logico, ma l'immagine è stata salvata come JPG/JPEG.
    for candidate in [requested_source.with_suffix(".jpg"), requested_source.with_suffix(".jpeg")]:
        if candidate.exists():
            return candidate

    return None


def handle_local_image_reference(
    ref: ImageReference,
    ordinal: int,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    target_jpg_path: Path,
    output_dir: Path,
    dry_run: bool,
) -> Tuple[str, List[str]]:
    actions: List[str] = []
    rel_jpg = relative_posix_path(target_jpg_path, output_dir)
    requested_source = Path(ref.src) if os.path.isabs(ref.src) else md_file.parent / ref.src
    effective_source = resolve_local_image_source(md_file, ref.src)

    desc = (
        f"Trovata immagine locale.\n"
        f"Riga: {ref.start_line}\n"
        f"Riferimento: {ref.src}\n"
        f"Sorgente richiesta: {requested_source.resolve()}\n"
        f"Sorgente effettiva: {effective_source if effective_source else 'NON TROVATA'}\n"
        f"Target: {target_jpg_path}\n"
        f"Percorso in out/: {rel_jpg}"
    )
    if not confirm.ask(desc):
        actions.append(f"Immagine locale riga {ref.start_line}: operazione saltata")
        return ref.raw, actions

    if effective_source is None:
        actions.append(f"Immagine locale riga {ref.start_line}: sorgente non trovata, riferimento lasciato invariato")
        return ref.raw, actions

    if target_jpg_path.exists() and not dry_run and not needs_regeneration(effective_source, target_jpg_path):
        actions.append(f"Immagine locale riga {ref.start_line}: JPG già aggiornato")
        return build_replacement_image_markup(md_type, ref, rel_jpg, ordinal), actions

    if dry_run:
        actions.append(f"[DRY RUN] Immagine locale riga {ref.start_line}: copia/convertita in {target_jpg_path.name}")
    else:
        local_image_to_jpg(effective_source, target_jpg_path, dry_run=False)
        actions.append(f"Immagine locale riga {ref.start_line}: salvata come {target_jpg_path.name}")

    return build_replacement_image_markup(md_type, ref, rel_jpg, ordinal), actions


def replace_images_in_text(
    text: str,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    dry_run: bool = False,
    force_remote: bool = False,
) -> Tuple[str, List[str]]:
    img_dir = get_image_dir_for_md(md_file)
    temp_dir = img_dir / "_tmp"
    output_dir = get_output_path_for_md(md_file).parent

    if not dry_run:
        ensure_dir(img_dir)
        ensure_dir(temp_dir)

    plantuml_spans = [(block.start_idx, block.end_idx) for block in find_plantuml_blocks(text, md_file)]
    excluded_spans = merge_spans(
        get_fenced_spans(text) + get_inline_code_spans(text) + get_html_code_spans(text) + plantuml_spans
    )

    refs = find_html_images(text, excluded_spans=excluded_spans) + find_markdown_images(text, excluded_spans=excluded_spans)
    refs = sorted(refs, key=lambda ref: ref.start_idx)

    actions: List[str] = []
    result_parts: List[str] = []
    last_idx = 0

    for ordinal, ref in enumerate(refs, start=1):
        result_parts.append(text[last_idx : ref.start_idx])
        last_idx = ref.end_idx

        target_jpg_path = build_target_jpg_path_for_image(md_file, ordinal, ref.start_line, ref.src)

        if is_remote_url(ref.src):
            replacement, ref_actions = handle_remote_image_reference(
                ref=ref,
                ordinal=ordinal,
                md_type=md_type,
                confirm=confirm,
                target_jpg_path=target_jpg_path,
                temp_dir=temp_dir,
                output_dir=output_dir,
                dry_run=dry_run,
                force_remote=force_remote,
            )
        else:
            replacement, ref_actions = handle_local_image_reference(
                ref=ref,
                ordinal=ordinal,
                md_file=md_file,
                md_type=md_type,
                confirm=confirm,
                target_jpg_path=target_jpg_path,
                output_dir=output_dir,
                dry_run=dry_run,
            )

        actions.extend(ref_actions)
        result_parts.append(replacement)

    result_parts.append(text[last_idx:])

    if not dry_run:
        try:
            if temp_dir.exists() and not any(temp_dir.iterdir()):
                temp_dir.rmdir()
        except Exception:
            pass

    return "".join(result_parts), actions


# -----------------------------------------------------------------------------
# Generazione PDF e rasterizzazione
# -----------------------------------------------------------------------------


def render_markdown_to_pdf(
    markdown_path: Path,
    pdf_path: Path,
    pandoc_cmd: str = "pandoc",
    pdf_engine: Optional[str] = None,
    extra_args: Optional[List[str]] = None,
    dry_run: bool = False,
) -> None:
    """Genera il PDF non rasterizzato con Pandoc."""
    command = [pandoc_cmd, str(markdown_path), "-o", str(pdf_path)]

    resource_path = get_pandoc_resource_path_for_processed_md(markdown_path)
    if resource_path:
        command.extend(["--resource-path", resource_path])

    if pdf_engine:
        command.extend(["--pdf-engine", pdf_engine])

    if extra_args:
        command.extend(extra_args)

    logger.info(f"LEGGE: {markdown_path}")
    logger.info(f"SCRIVE: {pdf_path}")
    logger.info(f"RESOURCE-PATH: {resource_path}")
    logger.info(f"COMANDO: {' '.join(command)}")

    if dry_run:
        logger.info(f"[DRY RUN] Generazione PDF simulata: {markdown_path} -> {pdf_path}")
        return

    ensure_dir(pdf_path.parent)

    result = subprocess.run(
        command,
        cwd=str(markdown_path.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    stdout = result.stdout or ""
    stderr = result.stderr or ""

    if stdout.strip():
        logger.debug(stdout.strip())

    if stderr.strip():
        logger.warning(stderr.strip())

    if result.returncode != 0:
        raise RuntimeError(f"Pandoc fallito per {markdown_path}: {stderr.strip()}")

def rasterize_pdf(input_pdf: Path, output_pdf: Path, dpi: int = 150, dry_run: bool = False) -> None:
    """Crea una versione rasterizzata del PDF, rendendo il testo non selezionabile."""
    if dry_run:
        logger.info(f"[DRY RUN] Simulata rasterizzazione PDF: {input_pdf} -> {output_pdf}")
        return

    if dpi <= 0:
        raise ValueError("Il valore DPI deve essere maggiore di zero")

    ensure_dir(output_pdf.parent)

    doc = None
    out_doc = None

    try:
        doc = pymupdf.open(input_pdf)
        out_doc = pymupdf.open()

        zoom = dpi / 72.0
        matrix = pymupdf.Matrix(zoom, zoom)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=matrix, alpha=False)

            width_pt = pix.width / zoom
            height_pt = pix.height / zoom

            new_page = out_doc.new_page(width=width_pt, height=height_pt)
            new_page.insert_image(new_page.rect, pixmap=pix)

        out_doc.save(output_pdf, garbage=4, deflate=True, clean=True)
    finally:
        if out_doc is not None:
            out_doc.close()
        if doc is not None:
            doc.close()


# -----------------------------------------------------------------------------
# Pulizia e processamento file
# -----------------------------------------------------------------------------


def clean_html_wrappers(text: str) -> str:
    pattern = re.compile(r'(?is)<div[^>]*>\s*(\!\[[^\]]*\]\([^\)]*\)(?:\{[^}]*\})?)\s*</div>')
    return pattern.sub(r"\1", text)


def is_markdown_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in {".md", ".markdown", ".mdown", ".mkd"}


def is_already_processed(path: Path) -> bool:
    parts_lower = {part.lower() for part in path.parts}
    generated_dirs = {"out", "published", "step20_md", "step40_pdf", "step90_publish"}
    return bool(parts_lower & generated_dirs) or path.stem.endswith("_processed")


def iter_markdown_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for path in root.rglob("*"):
        if is_markdown_file(path) and not is_already_processed(path):
            files.append(path)
    return sorted(files)


def process_markdown_file(
    md_file: Path,
    plantuml_jar: Optional[Path],
    assume_yes: bool = False,
    keep_plantuml_source: bool = False,
    dry_run: bool = False,
    force_remote: bool = False,
    generate_pdf: bool = True,
    dpi: int = 150,
    pandoc_cmd: str = "pandoc",
    pdf_engine: Optional[str] = None,
    pandoc_args: Optional[List[str]] = None,
) -> ProcessResult:
    if not md_file.exists():
        raise FileNotFoundError(f"File non trovato: {md_file}")

    original_text = md_file.read_text(encoding="utf-8-sig")
    md_type = detect_markdown_type(original_text)
    confirm = ConfirmManager(assume_yes=assume_yes, dry_run=dry_run)
    output_path = get_output_path_for_md(md_file)

    logger.info(f"File: {md_file}")
    logger.info(f"Tipo: {md_type.kind}")

    desc = f"Creazione file elaborato:\n  {md_file}\n  -> {output_path}"
    if not confirm.ask(desc):
        raise RuntimeError("Annullata")

    text_after_puml, actions_puml = process_plantuml_blocks(
        text=original_text,
        md_file=md_file,
        md_type=md_type,
        confirm=confirm,
        plantuml_jar=plantuml_jar,
        keep_source=keep_plantuml_source,
        dry_run=dry_run,
    )

    final_text, actions_img = replace_images_in_text(
        text=text_after_puml,
        md_file=md_file,
        md_type=md_type,
        confirm=confirm,
        dry_run=dry_run,
        force_remote=force_remote,
    )

    final_text = clean_html_wrappers(final_text)

    if dry_run:
        logger.info(f"[DRY RUN] File non scritto: {output_path}")
    else:
        ensure_dir(output_path.parent)
        output_path.write_text(final_text, encoding="utf-8", newline="\n")

    actions = [f"Tipo: {md_type.kind}", f"Motivo tipo: {md_type.reason}"] + actions_puml + actions_img
    actions.append(f"{'[DRY RUN] Sarebbe stato creato' if dry_run else 'Creato'}: {output_path}")

    if generate_pdf:
        # Pipeline esplicita:
        # step20_md/      Markdown elaborato
        # step40_pdf/     PDF non rasterizzato
        # step90_PUBLISH/ PDF rasterizzato pubblicabile
        normal_pdf_path = get_pdf_output_path_for_md(md_file)
        ro_pdf_path = get_publish_output_path_for_md(md_file)

        render_markdown_to_pdf(
            markdown_path=output_path,
            pdf_path=normal_pdf_path,
            pandoc_cmd=pandoc_cmd,
            pdf_engine=pdf_engine,
            extra_args=pandoc_args,
            dry_run=dry_run,
        )
        actions.append(f"{'[DRY RUN] Sarebbe stato creato' if dry_run else 'Creato'} PDF normale: {normal_pdf_path}")

        rasterize_pdf(
            input_pdf=normal_pdf_path,
            output_pdf=ro_pdf_path,
            dpi=dpi,
            dry_run=dry_run,
        )
        actions.append(f"{'[DRY RUN] Sarebbe stato creato' if dry_run else 'Creato'} PDF rasterizzato: {ro_pdf_path}")

    return ProcessResult(final_text, actions)


def collect_markdown_inputs(input_path: Path) -> List[Path]:
    """Raccoglie i Markdown da elaborare secondo la logica file/src/albero."""
    input_path = input_path.expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Percorso non trovato: {input_path}")

    if input_path.is_file():
        if not is_markdown_file(input_path):
            raise ValueError(f"Il file indicato non è un file Markdown: {input_path}")
        if not should_process_md_file(input_path):
            raise ValueError(
                f"Il file Markdown deve trovarsi direttamente in una directory src/: {input_path}"
            )
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

        files: List[Path] = []
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


def process_tree(
    root: Path,
    plantuml_jar: Optional[Path],
    assume_yes: bool = False,
    keep_plantuml_source: bool = False,
    dry_run: bool = False,
    force_remote: bool = False,
    generate_pdf: bool = True,
    dpi: int = 150,
    pandoc_cmd: str = "pandoc",
    pdf_engine: Optional[str] = None,
    pandoc_args: Optional[List[str]] = None,
) -> int:
    """Elabora un file Markdown, una directory src o un albero contenente directory src."""
    logger.info("STEP: 00 - Raccolta input")
    files = collect_markdown_inputs(root)
    logger.info(f"File Markdown da elaborare: {len(files)}")

    if not files:
        logger.warning(f"Nessun file Markdown valido trovato in: {root}")
        return 0

    processed = 0
    failures = 0

    for md_file in files:
        try:
            result = process_markdown_file(
                md_file=md_file,
                plantuml_jar=plantuml_jar,
                assume_yes=assume_yes,
                keep_plantuml_source=keep_plantuml_source,
                dry_run=dry_run,
                force_remote=force_remote,
                generate_pdf=generate_pdf,
                dpi=dpi,
                pandoc_cmd=pandoc_cmd,
                pdf_engine=pdf_engine,
                pandoc_args=pandoc_args,
            )
            processed += 1
            print("\nAzioni:")
            for action in result.actions:
                print(f" - {action}")
                logger.info(f"AZIONE: {action}")
        except Exception as exc:
            failures += 1
            logger.error(f"ERRORE in {md_file}: {exc}", exc_info=True)

    logger.info(f"Riepilogo: elaborati {processed}, errori {failures}")
    return 1 if failures else 0


# -----------------------------------------------------------------------------
# CLI-------------------
# CLI
# -----------------------------------------------------------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Processa Markdown con immagini e PlantUML")
    parser.add_argument("root", nargs="?", default="./", help="Directory radice")
    parser.add_argument("--plantuml-jar", help="Percorso a plantuml.jar")
    parser.add_argument("--yes", action="store_true", help="Conferma automatica")
    parser.add_argument("--verbose", action="store_true", help="Log dettagliato")
    parser.add_argument("--dry-run", action="store_true", help="Simula senza scrivere file")
    parser.add_argument("--keep-plantuml-source", action="store_true", help="Mantiene il codice PlantUML nel Markdown")
    parser.add_argument("--force-remote", action="store_true", help="Riscarica immagini remote anche se il JPG esiste già")
    parser.add_argument("--no-pdf", action="store_true", help="Non genera PDF")
    parser.add_argument("--dpi", type=int, default=150, help="DPI per il PDF rasterizzato _ro")
    parser.add_argument("--pandoc", default="pandoc", help="Comando o percorso di pandoc")
    parser.add_argument("--pdf-engine", default=None, help="Motore PDF Pandoc, per esempio xelatex")
    parser.add_argument(
        "--pandoc-arg",
        action="append",
        default=[],
        help="Argomento aggiuntivo da passare a Pandoc. Ripetere l'opzione per più argomenti.",
    )
    return parser


def resolve_plantuml_jar(arg_value: Optional[str]) -> Optional[Path]:
    if arg_value:
        return Path(arg_value).expanduser().resolve()

    env_value = os.environ.get("PLANTUML_JAR", "").strip()
    if env_value:
        return Path(env_value).expanduser().resolve()

    return None


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    root = Path(args.root).expanduser().resolve()
    custom_root = False

    if root == Path("./").resolve():
        root = Path(input("Inserire radice root: ").strip()).expanduser().resolve()
        custom_root = True

    # deve stare dopo risoluzione di root
    log_file = root.parent / "md_processor.log" if root.is_file() else root / "md_processor.log"
    configure_logging(args.verbose, log_file)

    plantuml_jar = resolve_plantuml_jar(args.plantuml_jar)

    try:
        return process_tree(
            root=root,
            plantuml_jar=plantuml_jar,
            assume_yes=args.yes,
            keep_plantuml_source=args.keep_plantuml_source,
            dry_run=args.dry_run,
            force_remote=args.force_remote,
            generate_pdf=not args.no_pdf,
            dpi=args.dpi,
            pandoc_cmd=args.pandoc,
            pdf_engine=args.pdf_engine,
            pandoc_args=args.pandoc_arg,
        )
    except Exception as exc:
        logger.error(f"Errore fatale: {exc}")
        return 1
    finally:
        if custom_root:
            logger.info(f"Root personalizzato: {root}")


if __name__ == "__main__":
    # raise SystemExit(main())
    main()
