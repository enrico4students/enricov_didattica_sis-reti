#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
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


@dataclass
class MarkdownTypeInfo:
    kind: str
    reason: str


@dataclass
class PlantUMLBlock:
    ordinal: int
    start_line: int
    fence: Optional[str]      # None se blocco libero (senza backtick)
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
    def __init__(self, assume_yes: bool = False) -> None:
        self.assume_yes = assume_yes

    def ask(self, description: str) -> bool:
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


def find_plantuml_blocks(text: str, md_file: Path) -> List[PlantUMLBlock]:
    """
    Trova blocchi PlantUML in due forme:
    1. Fenced code blocks: ```plantuml ... ```
    2. Plain blocks: @startuml ... @enduml (non annidati in fence)
    """
    blocks: List[PlantUMLBlock] = []
    ordinal = 0
    base_name = sanitize_name(md_file.stem)
    puml_dir = md_file.parent / "puml"
    img_dir = md_file.parent / "imgs"
    ensure_dir(puml_dir)
    ensure_dir(img_dir)

    # 1. Rilevamento blocchi con fence (```plantuml, ```puml, ```uml)
    fence_pattern = re.compile(
        r"(?ms)^(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>[^\n`]*)\n(?P<body>.*?)^\1[ \t]*$"
    )
    for match in fence_pattern.finditer(text):
        info = (match.group("info") or "").strip().lower()
        # Accetta plantuml, puml, uml
        if not any(keyword in info for keyword in ("plantuml", "puml", "uml")):
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

    # 2. Rilevamento blocchi liberi @startuml ... @enduml (non all'interno di fence)
    #    Per evitare doppioni, escludiamo le aree già coperte dai blocchi con fence.
    #    Costruiamo una lista di intervalli già processati.
    occupied_intervals = [(b.start_idx, b.end_idx) for b in blocks]

    def is_occupied(pos: int) -> bool:
        return any(start <= pos < end for start, end in occupied_intervals)

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


def write_text_file(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8", newline="\n")

def render_plantuml_to_jpg(puml_path: Path, jpg_path: Path, plantuml_jar: Path) -> None:
    if not plantuml_jar.exists():
        raise FileNotFoundError(f"PlantUML jar non trovato: {plantuml_jar}")

    # Genera PNG (affidabile, poi convertiamo in JPG)
    result = subprocess.run(
        ["java", "-jar", str(plantuml_jar), "-tpng", str(puml_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"PlantUML fallito con codice {result.returncode}\n"
            f"File: {puml_path}\n"
            f"Stderr: {result.stderr.strip()}\n"
            f"Stdout: {result.stdout.strip()}"
        )

    # Il PNG viene generato nella stessa directory del .puml
    generated_png = puml_path.with_suffix(".png")
    if not generated_png.exists():
        raise RuntimeError(f"PlantUML non ha generato il PNG atteso: {generated_png}")

    # Converti PNG in JPG nella destinazione desiderata
    ensure_dir(jpg_path.parent)
    with Image.open(generated_png) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(jpg_path, "JPEG", quality=95)

    # Rimuovi il PNG temporaneo
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


def download_remote_image(url: str, target_path: Path, timeout: int = 30) -> None:
    ensure_dir(target_path.parent)
    with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        with open(target_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)


def copy_or_convert_to_jpg(src_path: Path, target_jpg_path: Path) -> None:
    ensure_dir(target_jpg_path.parent)
    with Image.open(src_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(target_jpg_path, "JPEG", quality=95)


def normalize_remote_to_jpg(url: str, target_jpg_path: Path, temp_dir: Path) -> None:
    ensure_dir(temp_dir)
    ext = infer_extension_from_url(url)
    temp_path = temp_dir / f"download_{sha1_short(url)}{ext}"
    download_remote_image(url, temp_path)
    copy_or_convert_to_jpg(temp_path, target_jpg_path)
    try:
        temp_path.unlink(missing_ok=True)
    except Exception:
        pass


def local_image_to_jpg(src_path: Path, target_jpg_path: Path) -> None:
    ext = src_path.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        ensure_dir(target_jpg_path.parent)
        if src_path.resolve() != target_jpg_path.resolve():
            shutil.copy2(src_path, target_jpg_path)
        return
    copy_or_convert_to_jpg(src_path, target_jpg_path)


def make_target_image_name(md_file: Path, ordinal: int, line_no: int, source: str) -> str:
    base = sanitize_name(md_file.stem)
    source_name = sanitize_name(Path(source).stem) if not is_remote_url(source) else "remote"
    return f"{base}_img{ordinal}_r{line_no}_{source_name}_{sha1_short(source)}.jpg"


def process_plantuml_blocks(
    text: str,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    plantuml_jar: Optional[Path],
    replace_block: bool = False,
) -> Tuple[str, List[str]]:
    """
    replace_block: se True, il blocco PlantUML originale viene rimosso e sostituito dall'immagine.
                   se False (default), l'immagine viene aggiunta DOPO il blocco.
    """
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
        if confirm.ask(desc):

            if block.puml_path.exists():
                actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: file .puml già esistente, preservato")
            else:
                body_content = block.body.strip()
                if not body_content:
                    body_content = 'note "Diagramma vuoto"'

                # Aggiungi @startuml/@enduml se non già presenti (ignorando spazi iniziali)
                if not re.match(r'^\s*@startuml', body_content, re.IGNORECASE):
                    puml_content = f"@startuml\n{body_content}\n@enduml"
                else:
                    puml_content = body_content

                write_text_file(block.puml_path, puml_content)
                actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: creato {block.puml_path.name}")

            if plantuml_jar is None:
                raise RuntimeError("Specificare --plantuml-jar oppure impostare PLANTUML_JAR.")
            if block.jpg_path.exists():
                actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: JPG già esistente, preservato")
            else:
                render_plantuml_to_jpg(block.puml_path, block.jpg_path, plantuml_jar)
                actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: creato {block.jpg_path.name}")

            rel_img = relative_posix_path(block.jpg_path, md_file.parent)
            img_md = build_image_markdown(md_type.kind, f"PlantUML {block.ordinal}", rel_img, 70)
            print(f"[DEBUG] img_md = {img_md}")
            if replace_block:
                # Sostituisci il blocco con l'immagine
                result_parts.append(img_md)
                actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: blocco originale rimosso e sostituito con immagine")
            else:
                # Mantieni il blocco e aggiungi immagine dopo
                result_parts.append(text[block.start_idx:block.end_idx] + "\n\n" + img_md)
                actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: aggiunta immagine dopo il blocco")
        else:
            # Non elaborare questo blocco: lascialo invariato
            result_parts.append(text[block.start_idx:block.end_idx])
            actions.append(f"PlantUML blocco {block.ordinal} riga {block.start_line}: operazione saltata")

    result_parts.append(text[last_idx:])
    return "".join(result_parts), actions


def filter_overlapping_image_references(refs: List[ImageReference]) -> List[ImageReference]:
    refs = sorted(refs, key=lambda r: r.start_idx)
    filtered: List[ImageReference] = []
    last_end = -1
    for ref in refs:
        if ref.start_idx < last_end:
            continue
        filtered.append(ref)
        last_end = ref.end_idx
    return filtered


def resolve_local_image_source(md_file: Path, ref: ImageReference) -> Tuple[Path, Optional[Path]]:
    src_str = ref.src.replace("\\", "/")
    requested_source = (md_file.parent / src_str).resolve() if not os.path.isabs(src_str) else Path(src_str)

    if requested_source.exists():
        return requested_source, requested_source

    candidate_jpg = requested_source.with_suffix(".jpg")
    if candidate_jpg.exists():
        return requested_source, candidate_jpg

    candidate_jpeg = requested_source.with_suffix(".jpeg")
    if candidate_jpeg.exists():
        return requested_source, candidate_jpeg

    return requested_source, None


def build_target_jpg_path_for_image(md_file: Path, ordinal: int, line_no: int, source: str) -> Path:
    img_dir = md_file.parent / "imgs"
    base = sanitize_name(md_file.stem)
    source_stem = "remote" if is_remote_url(source) else sanitize_name(Path(source).stem)
    filename = f"{base}_img{ordinal}_r{line_no}_{source_stem}.jpg"
    return img_dir / filename


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


def handle_remote_image_reference(
    ref: ImageReference,
    ordinal: int,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    target_jpg_path: Path,
    temp_dir: Path,
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

    if target_jpg_path.exists():
        actions.append(f"Immagine remota riga {ref.start_line}: JPG target già esistente, preservato")
    else:
        normalize_remote_to_jpg(ref.src, target_jpg_path, temp_dir)
        actions.append(f"Immagine remota riga {ref.start_line}: salvata come {target_jpg_path.name}")

    replacement = build_replacement_image_markup(md_type, ref, rel_jpg, ordinal)
    return replacement, actions


def handle_local_image_reference(
    ref: ImageReference,
    ordinal: int,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    target_jpg_path: Path,
) -> Tuple[str, List[str]]:
    actions: List[str] = []
    rel_jpg = relative_posix_path(target_jpg_path, md_file.parent)

    requested_source, effective_source = resolve_local_image_source(md_file, ref)

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

    if target_jpg_path.exists():
        actions.append(f"Immagine locale riga {ref.start_line}: JPG target già esistente, preservato")
    else:
        local_image_to_jpg(effective_source, target_jpg_path)
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


def replace_images_in_text(text: str, md_file: Path, md_type: MarkdownTypeInfo, confirm: ConfirmManager) -> Tuple[str, List[str]]:
    img_dir = md_file.parent / "imgs"
    temp_dir = img_dir / "_tmp"
    ensure_dir(img_dir)
    ensure_dir(temp_dir)

    refs = find_html_images(text) + find_markdown_images(text)
    refs = filter_overlapping_image_references(refs)

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
            )
        else:
            replacement, ref_actions = handle_local_image_reference(
                ref=ref,
                ordinal=ordinal,
                md_file=md_file,
                md_type=md_type,
                confirm=confirm,
                target_jpg_path=target_jpg_path,
            )

        actions.extend(ref_actions)
        result_parts.append(replacement)

    result_parts.append(text[last_idx:])

    try:
        if temp_dir.exists() and not any(temp_dir.iterdir()):
            temp_dir.rmdir()
    except Exception:
        pass

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
) -> ProcessResult:
    if not md_file.exists():
        raise FileNotFoundError(f"File Markdown non trovato: {md_file}")

    original_text = md_file.read_text(encoding="utf-8")
    md_type = detect_markdown_type(original_text)
    confirm = ConfirmManager(assume_yes=assume_yes)

    print(f"\nFile: {md_file}")
    print(f"Tipo Markdown rilevato: {md_type.kind}")
    print(f"Motivo: {md_type.reason}")

    processed_path = create_processed_copy_path(md_file)
    desc = f"""Verrà creata una copia del file Markdown con suffisso _processed.
Origine:
    {md_file}
Destinazione:
    {processed_path}"""
    if not confirm.ask(desc):
        raise RuntimeError("Creazione file _processed annullata.")

    text_after_puml, actions_puml = process_plantuml_blocks(
        original_text, md_file, md_type, confirm, plantuml_jar, replace_block=replace_plantuml
    )
    final_text, actions_img = replace_images_in_text(text_after_puml, md_file, md_type, confirm)

    processed_path.write_text(final_text, encoding="utf-8", newline="\n")
    actions = [f"Tipo markdown rilevato: {md_type.kind} ({md_type.reason})"]
    actions.extend(actions_puml)
    actions.extend(actions_img)
    actions.append(f"Creato file elaborato: {processed_path}")

    return ProcessResult(final_text, actions)


def process_tree(root: Path, plantuml_jar: Optional[Path], assume_yes: bool = False, replace_plantuml: bool = False) -> int:

    if not root.exists():
        raise FileNotFoundError(f"Radice non trovata: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"La radice non è una directory: {root}")

    files = iter_markdown_files(root)
    print(f"Radice scansione: {root}")
    print(f"File Markdown trovati da elaborare: {len(files)}")

    if not files:
        return 0

    total = 0
    failures = 0
    for md_file in files:
        total += 1
        try:
            result = process_markdown_file(md_file, plantuml_jar, assume_yes, replace_plantuml)
            print("\nOperazioni completate per il file corrente:")
            for action in result.actions:
                print(f" - {action}")
        except Exception as exc:
            failures += 1
            print(f"\nERRORE nel file {md_file}: {exc}", file=sys.stderr)

    print(f"\nRiepilogo finale: elaborati {total} file, errori {failures}.")
    return 1 if failures else 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Processa tutti i Markdown di un sottoalbero, estraendo PlantUML embedded e normalizzando tutte le immagini in ./imgs/."
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

    root = Path(args.root).expanduser().resolve()
    
    # Questo è ok per testing:
    if root == Path("./").resolve(): 
        root = Path("D:\\00_data\\08-dev\\didattica\\enricov_didattica_sis-reti\\5anno\\concetti\\net-architecture\\es-didat_rete_enterprise_completa_01")

    plantuml_jar = resolve_plantuml_jar(args.plantuml_jar)
    # Opzionale: se ancora None, imposta un path di default
    if plantuml_jar is None:
        plantuml_jar = Path("D:\\programs\\plantuml\\plantuml.jar")

    try:
        return process_tree(root, plantuml_jar, args.yes, args.replace_plantuml)
    except Exception as exc:
        print(f"\nERRORE: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())