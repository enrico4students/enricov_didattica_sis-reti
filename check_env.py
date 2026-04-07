#!/usr/bin/env python3
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
from typing import List, Optional, Tuple
from urllib.parse import urlparse, unquote

import requests
from PIL import Image

# Configurazione logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class MarkdownTypeInfo:
    kind: str
    reason: str


@dataclass
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


@dataclass
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


@dataclass
class ProcessResult:
    processed_text: str
    actions: List[str]


def sanitize_name(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_") or "item"


def sha1_short(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def relative_posix_path(path: Path, start: Path) -> str:
    return os.path.relpath(path, start).replace("\\", "/")


def is_remote_url(value: str) -> bool:
    return value.lower().startswith(("http://", "https://"))


def infer_extension_from_url(url: str) -> str:
    parsed = urlparse(url)
    ext = Path(unquote(parsed.path)).suffix.lower()
    return ext or ".bin"


def line_number_from_index(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def has_yaml_frontmatter(text: str) -> bool:
    return bool(re.match(r"\A---\s*\n.*?\n---\s*(?:\n|$)", text, re.DOTALL))


def extract_yaml_frontmatter(text: str) -> str:
    m = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    return m.group(1) if m else ""


def detect_markdown_type(text: str) -> MarkdownTypeInfo:
    frontmatter = extract_yaml_frontmatter(text) if has_yaml_frontmatter(text) else ""

    if re.search(r"(?mi)^\s*marp\s*:\s*(true|false)\s*$", frontmatter):
        return MarkdownTypeInfo("marp", "Front matter YAML con chiave 'marp:'")

    pandoc_signals = [
        r"\{[^\n}]*\swidth\s*=\s*[^}]+\}",
        r"\[\^[^\]]+\]:",
        r"(?m)^Table:\s",
        r"(?m)^\s*:[^:\n]+:\s",
    ]
    for pattern in pandoc_signals:
        if re.search(pattern, text):
            return MarkdownTypeInfo("pandoc", f"Rilevato costrutto compatibile con Pandoc Markdown: {pattern}")

    return MarkdownTypeInfo("standard", "Nessun segnale specifico di Marp o Pandoc Markdown")


class ConfirmManager:
    def __init__(self, assume_yes: bool = False, dry_run: bool = False) -> None:
        self.assume_yes = assume_yes
        self.dry_run = dry_run

    def ask(self, description: str) -> bool:
        if self.dry_run:
            print("\n[DRY RUN] Operazione simulata:")
            print(textwrap.indent(description.strip(), prefix="    "))
            return True  # Simula conferma per vedere cosa accadrebbe

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


# ==================== NUOVE FUNZIONI PER LA STRUTTURA RIGIDA ====================

def should_process_md_file(md_file: Path) -> bool:
    """
    Restituisce True solo se il file è un documento valido:
    - non inizia con 'temp' (case-insensitive)
    - si trova direttamente in una directory chiamata 'src'
    """
    if md_file.name.lower().startswith("temp"):
        return False
    return md_file.parent.name == "src"


def get_dirs_for_valid_md(md_file: Path) -> Tuple[Path, Path]:
    """
    Precondizione: md_file è valido (should_process_md_file(md_file) == True)
    Restituisce (img_dir, puml_dir)
    """
    root = md_file.parent.parent  # la directory che contiene src/
    return root / "imgs", root / "plantuml"


# ==================== FUNZIONI ESISTENTI MODIFICATE ====================

def find_plantuml_blocks(text: str, md_file: Path) -> List[PlantUMLBlock]:
    blocks: List[PlantUMLBlock] = []
    ordinal = 0
    base_name = sanitize_name(md_file.stem)

    # Determina le directory in base alla struttura
    if should_process_md_file(md_file):
        img_dir, puml_dir = get_dirs_for_valid_md(md_file)
    else:
        # Fallback per sicurezza (non dovrebbe accadere perché chiamato solo per file validi)
        img_dir = md_file.parent / "imgs"
        puml_dir = md_file.parent / "puml"

    ensure_dir(puml_dir)
    ensure_dir(img_dir)

    # Fenced blocks
    fence_pattern = re.compile(
        r"(?ms)^(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>[^\n`]*)\n(?P<body>.*?)^\1[ \t]*$"
    )
    for match in fence_pattern.finditer(text):
        info = (match.group("info") or "").strip().lower()
        if not any(kw in info for kw in ("plantuml", "puml", "uml")):
            continue
        ordinal += 1
        start_idx = match.start()
        start_line = line_number_from_index(text, start_idx)
        suffix = f"{base_name}_{ordinal}_r{start_line}"
        blocks.append(
            PlantUMLBlock(
                ordinal=ordinal,
                start_line=start_line,
                fence=match.group("fence"),
                info=match.group("info"),
                body=match.group("body"),
                start_idx=start_idx,
                end_idx=match.end(),
                puml_path=puml_dir / f"{suffix}.puml",
                jpg_path=img_dir / f"{suffix}_puml.jpg",
            )
        )

    # Free @startuml/@enduml blocks (non nested)
    occupied = [(b.start_idx, b.end_idx) for b in blocks]

    def is_occupied(pos: int) -> bool:
        return any(start <= pos < end for start, end in occupied)

    free_pattern = re.compile(
        r"(?ms)^[ \t]*@startuml[ \t]*(?P<info>[^\n]*)\n(?P<body>.*?)^[ \t]*@enduml[ \t]*$"
    )
    for match in free_pattern.finditer(text):
        if is_occupied(match.start()):
            continue
        ordinal += 1
        start_idx = match.start()
        start_line = line_number_from_index(text, start_idx)
        suffix = f"{base_name}_{ordinal}_r{start_line}"
        blocks.append(
            PlantUMLBlock(
                ordinal=ordinal,
                start_line=start_line,
                fence=None,
                info=match.group("info") or "",
                body=match.group("body"),
                start_idx=start_idx,
                end_idx=match.end(),
                puml_path=puml_dir / f"{suffix}.puml",
                jpg_path=img_dir / f"{suffix}_puml.jpg",
            )
        )

    return blocks


def write_text_file_if_changed(path: Path, content: str) -> bool:
    """
    Scrive il file solo se il contenuto è diverso da quello esistente.
    Restituisce True se il file è stato scritto (o creato), False se era identico.
    """
    ensure_dir(path.parent)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return False
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def render_plantuml_to_jpg(puml_path: Path, jpg_path: Path, plantuml_jar: Path, dry_run: bool = False) -> None:
    if dry_run:
        logger.info(f"[DRY RUN] Simulata generazione JPG da {puml_path} -> {jpg_path}")
        return

    if not plantuml_jar.exists():
        raise FileNotFoundError(f"PlantUML jar non trovato: {plantuml_jar}")

    # Genera PNG (affidabile), poi converti in JPG
    result = subprocess.run(
        ["java", "-jar", str(plantuml_jar), "-tpng", str(puml_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"PlantUML fallito con codice {result.returncode}\n"
            f"File: {puml_path}\n"
            f"Stderr: {result.stderr.strip()}\n"
            f"Stdout: {result.stdout.strip()}"
        )

    generated_png = puml_path.with_suffix(".png")
    if not generated_png.exists():
        raise RuntimeError(f"PlantUML non ha generato il PNG atteso: {generated_png}")

    ensure_dir(jpg_path.parent)
    with Image.open(generated_png) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(jpg_path, "JPEG", quality=95)

    generated_png.unlink()


def build_image_markdown(md_type: str, alt: str, rel_path: str, width_percent: Optional[int] = None) -> str:
    alt = alt or "immagine"
    if md_type == "pandoc":
        if width_percent is not None:
            return f"![{alt}]({rel_path}){{ width={width_percent}% }}"
        return f"![{alt}]({rel_path})"
    if md_type == "marp":
        if width_percent is not None:
            return f"![width:{width_percent}%]({rel_path})"
        return f"![{alt}]({rel_path})"
    return f"![{alt}]({rel_path})"


def find_html_images(text: str) -> List[ImageReference]:
    img_tag_pattern = re.compile(r'(?is)<img\b[^>]*>')
    src_pattern = re.compile(r'''(?is)\bsrc\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))''')
    alt_pattern = re.compile(r'''(?is)\balt\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))''')
    width_pattern = re.compile(r'''(?is)\bwidth\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))''')

    refs: List[ImageReference] = []
    ordinal = 0
    for match in img_tag_pattern.finditer(text):
        tag = match.group(0)
        src_m = src_pattern.search(tag)
        if not src_m:
            continue
        src = (src_m.group(2) or src_m.group(3) or src_m.group(4) or "").strip()
        alt_m = alt_pattern.search(tag)
        width_m = width_pattern.search(tag)
        alt = (alt_m.group(2) or alt_m.group(3) or alt_m.group(4) or "").strip() if alt_m else ""
        width = (width_m.group(2) or width_m.group(3) or width_m.group(4) or "").strip() if width_m else None
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
                html_width=width,
            )
        )
    return refs


def parse_markdown_image(inner: str) -> Tuple[str, Optional[str]]:
    inner = inner.strip()
    if not inner:
        return "", None

    if inner.startswith("<"):
        close = inner.find(">")
        if close != -1:
            src = inner[1:close].strip()
            rest = inner[close + 1 :].strip()
            title = None
            if rest.startswith('"') and rest.endswith('"') and len(rest) >= 2:
                title = rest[1:-1]
            elif rest.startswith("'") and rest.endswith("'") and len(rest) >= 2:
                title = rest[1:-1]
            return src, title

    m = re.match(r'''^(?P<src>.+?)(?:\s+(?P<title>"[^"]*"|'[^']*'))?$''', inner)
    if not m:
        return inner, None

    src = (m.group("src") or "").strip()
    title = m.group("title")
    if title:
        title = title.strip("\"'")

    if len(src) >= 2 and ((src[0] == src[-1] == '"') or (src[0] == src[-1] == "'")):
        src = src[1:-1]

    return src, title


def find_markdown_images(text: str) -> List[ImageReference]:
    pattern = re.compile(r'''(?s)!\[(?P<alt>[^\]]*)\]\((?P<inner>.*?)\)(?P<attrs>\{[^}]*\})?''')
    refs: List[ImageReference] = []
    ordinal = 0
    for match in pattern.finditer(text):
        raw = match.group(0)
        inner = match.group("inner") or ""
        src, title = parse_markdown_image(inner)
        if not src:
            continue
        ordinal += 1
        refs.append(
            ImageReference(
                ordinal=ordinal,
                start_idx=match.start(),
                end_idx=match.end(),
                start_line=line_number_from_index(text, match.start()),
                source_type="markdown",
                raw=raw,
                alt=match.group("alt") or "",
                src=src,
                title=title,
                attrs=match.group("attrs"),
                html_width=None,
            )
        )
    return refs


def download_remote_image(url: str, target_path: Path, timeout: int = 30, dry_run: bool = False) -> bool:
    """
    Scarica un'immagine remota. Restituisce True se successo, False se errore.
    In dry_run simula e restituisce True.
    """
    if dry_run:
        logger.info(f"[DRY RUN] Simulato download da {url} -> {target_path}")
        return True

    ensure_dir(target_path.parent)
    try:
        with requests.get(url, stream=True, timeout=timeout) as response:
            response.raise_for_status()
            with open(target_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
        return True
    except requests.RequestException as e:
        logger.error(f"Download fallito per {url}: {e}")
        return False


def copy_or_convert_to_jpg(src_path: Path, target_jpg_path: Path, dry_run: bool = False) -> None:
    if dry_run:
        logger.info(f"[DRY RUN] Simulata copia/conversione da {src_path} -> {target_jpg_path}")
        return

    ensure_dir(target_jpg_path.parent)
    with Image.open(src_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(target_jpg_path, "JPEG", quality=95)


def normalize_remote_to_jpg(url: str, target_jpg_path: Path, temp_dir: Path, dry_run: bool = False) -> bool:
    """
    Scarica e converte un'immagine remota in JPG.
    Restituisce True se successo, False altrimenti.
    """
    if dry_run:
        logger.info(f"[DRY RUN] Simulata normalizzazione remota {url} -> {target_jpg_path}")
        return True

    ensure_dir(temp_dir)
    ext = infer_extension_from_url(url)
    temp_path = temp_dir / f"download_{sha1_short(url)}{ext}"
    if not download_remote_image(url, temp_path, dry_run=dry_run):
        return False
    try:
        copy_or_convert_to_jpg(temp_path, target_jpg_path, dry_run=dry_run)
        return True
    finally:
        try:
            temp_path.unlink(missing_ok=True)
        except Exception:
            pass


def local_image_to_jpg(src_path: Path, target_jpg_path: Path, dry_run: bool = False) -> None:
    ext = src_path.suffix.lower()
    if dry_run:
        logger.info(f"[DRY RUN] Simulata copia/conversione locale da {src_path} -> {target_jpg_path}")
        return

    if ext in (".jpg", ".jpeg"):
        ensure_dir(target_jpg_path.parent)
        if src_path.resolve() != target_jpg_path.resolve():
            shutil.copy2(src_path, target_jpg_path)
        return
    copy_or_convert_to_jpg(src_path, target_jpg_path, dry_run=False)


def build_target_jpg_path_for_image(md_file: Path, ordinal: int, line_no: int, source: str) -> Path:
    if should_process_md_file(md_file):
        img_dir, _ = get_dirs_for_valid_md(md_file)
    else:
        # Fallback per sicurezza (non dovrebbe accadere)
        img_dir = md_file.parent / "imgs"

    base = sanitize_name(md_file.stem)
    if is_remote_url(source):
        source_stem = "remote_" + sha1_short(source)
    else:
        source_stem = sanitize_name(Path(source).stem)
    filename = f"{base}_img{ordinal}_r{line_no}_{source_stem}.jpg"
    return img_dir / filename


def replace_images_in_text(
    text: str, md_file: Path, md_type: MarkdownTypeInfo, confirm: ConfirmManager, dry_run: bool = False
) -> Tuple[str, List[str]]:
    if should_process_md_file(md_file):
        img_dir, _ = get_dirs_for_valid_md(md_file)
    else:
        img_dir = md_file.parent / "imgs"
    temp_dir = img_dir / "_tmp"
    if not dry_run:
        ensure_dir(img_dir)
        ensure_dir(temp_dir)

    refs = find_html_images(text) + find_markdown_images(text)
    refs = sorted(refs, key=lambda r: r.start_idx)

    actions: List[str] = []
    result_parts: List[str] = []
    last_idx = 0

    for ordinal, ref in enumerate(refs, start=1):
        result_parts.append(text[last_idx:ref.start_idx])
        last_idx = ref.end_idx

        target_jpg_path = build_target_jpg_path_for_image(
            md_file=md_file,
            ordinal=ordinal,
            line_no=ref.start_line,
            source=ref.src,
        )

        if is_remote_url(ref.src):
            replacement, ref_actions = handle_remote_image_reference(
                ref=ref,
                ordinal=ordinal,
                md_file=md_file,
                md_type=md_type,
                confirm=confirm,
                target_jpg_path=target_jpg_path,
                temp_dir=temp_dir,
                dry_run=dry_run,
            )
        else:
            replacement, ref_actions = handle_local_image_reference(
                ref=ref,
                ordinal=ordinal,
                md_file=md_file,
                md_type=md_type,
                confirm=confirm,
                target_jpg_path=target_jpg_path,
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


def handle_remote_image_reference(
    ref: ImageReference,
    ordinal: int,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    target_jpg_path: Path,
    temp_dir: Path,
    dry_run: bool = False,
) -> Tuple[str, List[str]]:
    actions: List[str] = []
    rel_jpg = relative_posix_path(target_jpg_path, md_file.parent)

    desc = f"""Trovata immagine remota.
Riga: {ref.start_line}
Origine: {ref.src}
Verrà scaricata e normalizzata in:
    {target_jpg_path}
Nel file _processed verrà usato solo il file locale in ./imgs/."""
    if not confirm.ask(desc):
        actions.append(f"Immagine remota riga {ref.start_line}: operazione saltata")
        return ref.raw, actions

    if target_jpg_path.exists() and not dry_run:
        actions.append(f"Immagine remota riga {ref.start_line}: JPG target già esistente, preservato")
        replacement = build_replacement_image_markup(md_type, ref, rel_jpg, ordinal)
        return replacement, actions

    success = normalize_remote_to_jpg(ref.src, target_jpg_path, temp_dir, dry_run=dry_run)
    if success:
        if not dry_run:
            actions.append(f"Immagine remota riga {ref.start_line}: salvata come {target_jpg_path.name}")
        else:
            actions.append(f"[DRY RUN] Immagine remota riga {ref.start_line}: sarebbe stata salvata come {target_jpg_path.name}")
        replacement = build_replacement_image_markup(md_type, ref, rel_jpg, ordinal)
        return replacement, actions
    else:
        actions.append(f"Immagine remota riga {ref.start_line}: download fallito, riferimento originale mantenuto")
        return ref.raw, actions


def handle_local_image_reference(
    ref: ImageReference,
    ordinal: int,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    target_jpg_path: Path,
    dry_run: bool = False,
) -> Tuple[str, List[str]]:
    actions: List[str] = []
    rel_jpg = relative_posix_path(target_jpg_path, md_file.parent)

    requested_source = (md_file.parent / ref.src).resolve() if not os.path.isabs(ref.src) else Path(ref.src)
    effective_source = requested_source if requested_source.exists() else None

    # Cerca alternativa .jpg/.jpeg (mantenuto ma senza modifiche)
    if effective_source is None:
        candidate_jpg = requested_source.with_suffix(".jpg")
        if candidate_jpg.exists():
            effective_source = candidate_jpg
        else:
            candidate_jpeg = requested_source.with_suffix(".jpeg")
            if candidate_jpeg.exists():
                effective_source = candidate_jpeg

    desc = f"""Trovata immagine locale.
Riga: {ref.start_line}
Riferimento originale: {ref.src}
File sorgente richiesto:
    {requested_source}
File sorgente effettivo:
    {effective_source if effective_source is not None else 'NON TROVATO'}
Target finale:
    {target_jpg_path}
Il file _processed verrà aggiornato per usare soltanto il file locale JPG in ./imgs/."""
    if not confirm.ask(desc):
        actions.append(f"Immagine locale riga {ref.start_line}: operazione saltata")
        return ref.raw, actions

    if effective_source is None:
        actions.append(
            f"Immagine locale riga {ref.start_line}: sorgente non trovata ({requested_source}), nessuna .jpg/.jpeg alternativa trovata; riferimento lasciato invariato"
        )
        return ref.raw, actions

    if target_jpg_path.exists() and not dry_run:
        actions.append(f"Immagine locale riga {ref.start_line}: JPG target già esistente, preservato")
        replacement = build_replacement_image_markup(md_type, ref, rel_jpg, ordinal)
        return replacement, actions

    if dry_run:
        actions.append(f"[DRY RUN] Immagine locale riga {ref.start_line}: sarebbe stata copia/convertita da {effective_source} a {target_jpg_path}")
    else:
        local_image_to_jpg(effective_source, target_jpg_path, dry_run=False)
        if effective_source.suffix.lower() not in (".jpg", ".jpeg"):
            actions.append(
                f"Immagine locale riga {ref.start_line}: convertita da {effective_source.suffix} a JPG e salvata come {target_jpg_path.name}"
            )
        elif effective_source != requested_source:
            actions.append(
                f"Immagine locale riga {ref.start_line}: file originale non trovato, usata immagine JPG alternativa {effective_source.name} e copiata come {target_jpg_path.name}"
            )
        else:
            actions.append(f"Immagine locale riga {ref.start_line}: copiata come {target_jpg_path.name}")

    replacement = build_replacement_image_markup(md_type, ref, rel_jpg, ordinal)
    return replacement, actions


def build_replacement_image_markup(
    md_type: MarkdownTypeInfo,
    ref: ImageReference,
    relative_jpg_path: str,
    ordinal: int,
) -> str:
    return build_image_markdown(
        md_type.kind,
        ref.alt or f"image_{ordinal}",
        relative_jpg_path,
        70 if ref.source_type == "html" else None,
    )


def process_plantuml_blocks(
    text: str,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    plantuml_jar: Optional[Path],
    replace_block: bool = False,
    dry_run: bool = False,
) -> Tuple[str, List[str]]:
    blocks = find_plantuml_blocks(text, md_file)
    if not blocks:
        return text, []

    actions: List[str] = []
    result_parts: List[str] = []
    last_idx = 0

    for block in blocks:
        result_parts.append(text[last_idx:block.start_idx])
        last_idx = block.end_idx

        desc = f"""Trovato blocco PlantUML embedded.
File Markdown: {md_file}
Numero blocco: {block.ordinal}
Riga iniziale: {block.start_line}
Tipo: {'fenced' if block.fence else 'libero (startuml/enduml)'}
File sorgente PlantUML da creare:
    {block.puml_path}
Immagine JPG da generare:
    {block.jpg_path}
Il file _processed riceverà un link all'immagine {'in sostituzione del blocco' if replace_block else 'subito dopo il blocco PlantUML'}."""
        if not confirm.ask(desc):
            result_parts.append(text[block.start_idx:block.end_idx])
            actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: operazione saltata")
            continue

        # Preparazione contenuto .puml
        body_content = block.body.strip()
        if not body_content:
            body_content = 'note "Diagramma vuoto"'

        if not re.match(r'^\s*@startuml', body_content, re.IGNORECASE):
            puml_content = f"@startuml\n{body_content}\n@enduml"
        else:
            puml_content = body_content

        # Scrittura file .puml solo se cambiato
        if dry_run:
            actions.append(f"[DRY RUN] PlantUML blocco {block.ordinal} riga {block.start_line}: sarebbe stato scritto {block.puml_path.name}")
        else:
            if write_text_file_if_changed(block.puml_path, puml_content):
                actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: creato/aggiornato {block.puml_path.name}")
            else:
                actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: file {block.puml_path.name} invariato, non sovrascritto")

        # Generazione JPG
        if plantuml_jar is None:
            raise RuntimeError("Specificare --plantuml-jar oppure impostare PLANTUML_JAR.")

        if block.jpg_path.exists() and not dry_run:
            actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: JPG già esistente, preservato")
        else:
            if dry_run:
                actions.append(f"[DRY RUN] PlantUML blocco {block.ordinal} riga {block.start_line}: sarebbe stato generato JPG {block.jpg_path.name}")
            else:
                render_plantuml_to_jpg(block.puml_path, block.jpg_path, plantuml_jar, dry_run=False)
                actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: creato {block.jpg_path.name}")

        # Aggiunta immagine nel testo
        rel_img = relative_posix_path(block.jpg_path, md_file.parent)
        img_md = build_image_markdown(md_type.kind, f"PlantUML {block.ordinal}", rel_img, 70)
        if replace_block:
            result_parts.append(img_md)
            actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: blocco originale rimosso e sostituito con immagine")
        else:
            result_parts.append(text[block.start_idx:block.end_idx] + "\n\n" + img_md)
            actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: aggiunta immagine dopo il blocco")

    result_parts.append(text[last_idx:])
    return "".join(result_parts), actions


def create_processed_copy_path(md_file: Path) -> Path:
    return md_file.with_name(f"{md_file.stem}_processed{md_file.suffix}")


def is_markdown_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in {".md", ".markdown", ".mdown", ".mkd"}


def is_already_processed(path: Path) -> bool:
    return path.stem.endswith("_processed")


def iter_markdown_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for path in root.rglob("*"):
        if not is_markdown_file(path):
            continue
        if is_already_processed(path):
            continue
        files.append(path)
    return sorted(files)


def process_markdown_file(
    md_file: Path,
    plantuml_jar: Optional[Path],
    assume_yes: bool = False,
    replace_plantuml: bool = False,
    dry_run: bool = False,
) -> ProcessResult:
    if not md_file.exists():
        raise FileNotFoundError(f"File Markdown non trovato: {md_file}")

    original_text = md_file.read_text(encoding="utf-8-sig")
    md_type = detect_markdown_type(original_text)
    confirm = ConfirmManager(assume_yes=assume_yes, dry_run=dry_run)

    logger.info(f"File: {md_file}")
    logger.info(f"Tipo Markdown rilevato: {md_type.kind} ({md_type.reason})")

    processed_path = create_processed_copy_path(md_file)
    desc = f"""Verrà creata una copia del file Markdown con suffisso _processed.
Origine:
    {md_file}
Destinazione:
    {processed_path}"""
    if not confirm.ask(desc):
        raise RuntimeError("Creazione file _processed annullata.")

    text_after_img, actions_img = replace_images_in_text(original_text, md_file, md_type, confirm, dry_run=dry_run)
    final_text, actions_puml = process_plantuml_blocks(
        text_after_img, md_file, md_type, confirm, plantuml_jar, replace_block=replace_plantuml, dry_run=dry_run
    )

    if not dry_run:
        processed_path.write_text(final_text, encoding="utf-8", newline="\n")
    else:
        logger.info(f"[DRY RUN] File _processed non scritto: {processed_path}")

    actions = [f"Tipo markdown rilevato: {md_type.kind} ({md_type.reason})"]
    actions.extend(actions_img)
    actions.extend(actions_puml)
    if not dry_run:
        actions.append(f"Creato file elaborato: {processed_path}")
    else:
        actions.append(f"[DRY RUN] Sarebbe stato creato file elaborato: {processed_path}")

    return ProcessResult(final_text, actions)


def process_tree(
    root: Path,
    plantuml_jar: Optional[Path],
    assume_yes: bool = False,
    replace_plantuml: bool = False,
    dry_run: bool = False,
) -> int:
    if not root.exists():
        raise FileNotFoundError(f"Radice non trovata: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"La radice non è una directory: {root}")

    files = iter_markdown_files(root)
    logger.info(f"Radice scansione: {root}")
    logger.info(f"File Markdown trovati da elaborare: {len(files)}")

    if not files:
        return 0

    total = 0
    failures = 0
    for md_file in files:
        total += 1

        # 1. Ignora file temporanei (temp*)
        if md_file.name.lower().startswith("temp"):
            logger.warning(f"Ignoro il file temporaneo (temp): {md_file}")
            continue

        # 2. Controlla struttura valida: deve essere .../src/nome.md
        if not should_process_md_file(md_file):
            logger.warning(
                f"File saltato: {md_file} non si trova direttamente in una directory 'src'. "
                f"Per elaborarlo, spostalo in .../<root_documento>/src/<file>.md"
            )
            continue

        try:
            result = process_markdown_file(md_file, plantuml_jar, assume_yes, replace_plantuml, dry_run)
            print("\nOperazioni completate per il file corrente:")
            for action in result.actions:
                print(f" - {action}")
        except Exception as exc:
            failures += 1
            logger.error(f"ERRORE nel file {md_file}: {exc}", exc_info=False)

    logger.info(f"Riepilogo finale: elaborati {total} file, errori {failures}.")
    return 1 if failures else 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Processa tutti i Markdown di un sottoalbero, estraendo PlantUML embedded e normalizzando tutte le immagini in ./imgs/.\n"
                    "I file .md devono trovarsi direttamente in una cartella 'src' (es. <root>/src/file.md). "
                    "Le immagini e i file PlantUML vengono salvati in cartelle sibling 'imgs' e 'plantuml'."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default="./",
        help="Directory radice del sottoalbero da percorrere. Default: ./",
    )
    parser.add_argument("--plantuml-jar", help="Percorso a plantuml.jar.")
    parser.add_argument("--yes", action="store_true", help="Eseguire tutte le operazioni senza chiedere conferma.")
    parser.add_argument(
        "--replace-plantuml",
        action="store_true",
        help="Sostituisci il blocco PlantUML originale con l'immagine generata (default: aggiunge l'immagine dopo il blocco).",
    )
    parser.add_argument("--verbose", action="store_true", help="Mostra output dettagliato (debug).")
    parser.add_argument("--dry-run", action="store_true", help="Simula le operazioni senza scrivere file né scaricare nulla.")
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
    # Hardcoding preservato come richiesto
    if root == Path("./").resolve():        
        root = Path("D:\\00_data\\08-dev\\didattica\\enricov_didattica_sis-reti\\5anno\\concetti\\dispositivi").resolve()
        custom_root = True

    plantuml_jar = resolve_plantuml_jar(args.plantuml_jar)
    if plantuml_jar is None:
        logger.error("Nessun plantuml.jar specificato. Usa --plantuml-jar o imposta la variabile d'ambiente PLANTUML_JAR.")
        return 1

    try:
        return process_tree(
            root,
            plantuml_jar,
            assume_yes=args.yes,
            replace_plantuml=args.replace_plantuml,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        logger.error(f"ERRORE FATALE: {exc}")
        return 1
    finally:
        if custom_root:
            logger.info(f"Nota: è stato usato un percorso di root personalizzato per testing:\n{root}")


if __name__ == "__main__":
    raise SystemExit(main())