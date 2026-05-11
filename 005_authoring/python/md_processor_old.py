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


def should_process_md_file(md_file: Path) -> bool:
    if md_file.name.lower().startswith("temp"):
        return False
    return md_file.parent.name == "src"


def get_dirs_for_valid_md(md_file: Path) -> Tuple[Path, Path]:
    root = md_file.parent.parent
    return root / "imgs", root / "puml"


def get_output_path_for_md(md_file: Path) -> Path:
    if should_process_md_file(md_file):
        doc_root = md_file.parent.parent
        out_dir = doc_root / "out"
        return out_dir / md_file.name
    return md_file.with_name(f"{md_file.stem}_processed{md_file.suffix}")


def flatten_on_white(img: Image.Image) -> Image.Image:
    if img.mode in ("RGBA", "LA"):
        rgba = img.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        composited = Image.alpha_composite(background, rgba)
        return composited.convert("RGB")

    if img.mode == "P" and "transparency" in img.info:
        rgba = img.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        composited = Image.alpha_composite(background, rgba)
        return composited.convert("RGB")

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
    try:
        import cairosvg
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), background_color="white")
        return True
    except Exception as e:
        logger.warning(f"Conversione SVG con cairosvg fallita per {svg_path}: {e}")

    if shutil.which("rsvg-convert"):
        result = subprocess.run(
            ["rsvg-convert", "-b", "white", "-o", str(png_path), str(svg_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and png_path.exists():
            return True
        logger.warning(f"Conversione SVG con rsvg-convert fallita per {svg_path}: {result.stderr}")

    logger.error(
        f"Impossibile convertire SVG: {svg_path}. Installare cairosvg (pip install cairosvg) o rsvg-convert."
    )
    return False


def write_text_file_if_changed(path: Path, content: str) -> bool:
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

    result = subprocess.run(
        ["java", "-jar", str(plantuml_jar), "-tpng", str(puml_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"PlantUML fallito: {result.stderr}")

    generated_png = puml_path.with_suffix(".png")
    if not generated_png.exists():
        raise RuntimeError("PNG non generato")

    ensure_dir(jpg_path.parent)
    with Image.open(generated_png) as img:
        img = flatten_on_white(img)
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


def find_plantuml_blocks(text: str, md_file: Path) -> List[PlantUMLBlock]:
    blocks: List[PlantUMLBlock] = []
    ordinal = 0
    base_name = sanitize_name(md_file.stem)

    if should_process_md_file(md_file):
        img_dir, puml_dir = get_dirs_for_valid_md(md_file)
    else:
        img_dir = md_file.parent / "imgs"
        puml_dir = md_file.parent / "puml"

    ensure_dir(puml_dir)
    ensure_dir(img_dir)

    fence_pattern = re.compile(
        r"(?ms)^(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>[^\n`]*)\n(?P<body>.*?)^\1[ \t]*$"
    )

    all_fenced_spans: List[Tuple[int, int]] = []

    for match in fence_pattern.finditer(text):
        all_fenced_spans.append((match.start(), match.end()))

        info = (match.group("info") or "").strip().lower()
        body = match.group("body") or ""

        is_declared_plantuml = any(kw in info for kw in ("plantuml", "puml", "uml"))
        is_body_plantuml = re.search(r"(?mi)^\s*@startuml\b", body) and re.search(r"(?mi)^\s*@enduml\b", body)

        if not (is_declared_plantuml or is_body_plantuml):
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

    def is_inside_any_fenced_block(pos: int) -> bool:
        return any(start <= pos < end for start, end in all_fenced_spans)

    free_pattern = re.compile(
        r"(?ms)^[ \t]*@startuml[ \t]*(?P<info>[^\n]*)\n(?P<body>.*?)^[ \t]*@enduml[ \t]*$"
    )

    for match in free_pattern.finditer(text):
        if is_inside_any_fenced_block(match.start()):
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

    blocks.sort(key=lambda b: b.start_idx)
    return blocks


def get_fenced_spans(text: str) -> List[Tuple[int, int]]:
    spans: List[Tuple[int, int]] = []
    fence_pattern = re.compile(
        r"(?ms)^(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>[^\n`]*)\n(?P<body>.*?)^\1[ \t]*$"
    )
    for match in fence_pattern.finditer(text):
        spans.append((match.start(), match.end()))
    return spans


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
    spans: List[Tuple[int, int]] = []
    pattern = re.compile(r"(?is)<(code|pre)\b[^>]*>.*?</\1\s*>")
    for match in pattern.finditer(text):
        spans.append((match.start(), match.end()))
    return spans


def merge_spans(spans: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not spans:
        return []
    spans = sorted(spans)
    merged = [spans[0]]
    for start, end in spans[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def is_inside_spans(pos: int, spans: List[Tuple[int, int]]) -> bool:
    for start, end in spans:
        if start <= pos < end:
            return True
    return False


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
        src_m = src_pattern.search(tag)
        if not src_m:
            continue

        src = (src_m.group(2) or src_m.group(3) or src_m.group(4) or "").strip()
        alt_m = alt_pattern.search(tag)
        width_m = width_pattern.search(tag)
        style_m = style_pattern.search(tag)

        alt = (alt_m.group(2) or alt_m.group(3) or alt_m.group(4) or "").strip() if alt_m else ""
        width = (width_m.group(2) or width_m.group(3) or width_m.group(4) or "").strip() if width_m else None
        style = (style_m.group(2) or style_m.group(3) or style_m.group(4) or "").strip() if style_m else None

        html_width = width
        if not html_width and style:
            m = re.search(r"(?i)\bmax-width\s*:\s*(\d+)\s*%", style)
            if m:
                html_width = f"{m.group(1)}%"
            else:
                m = re.search(r"(?i)\bwidth\s*:\s*(\d+)\s*%", style)
                if m:
                    html_width = f"{m.group(1)}%"

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



def extract_width_percent_from_html_ref(ref: ImageReference) -> Optional[int]:
    if ref.html_width:
        m = re.match(r"^\s*(\d+)\s*%\s*$", ref.html_width)
        if m:
            return int(m.group(1))

    m = re.search(r"(?i)\bmax-width\s*:\s*(\d+)\s*%", ref.raw)
    if m:
        return int(m.group(1))

    m = re.search(r"(?i)\bwidth\s*:\s*(\d+)\s*%", ref.raw)
    if m:
        return int(m.group(1))

    return None


def parse_markdown_image_inner(inner: str) -> Tuple[str, Optional[str]]:
    inner = inner.strip()
    if not inner:
        return "", None

    if inner.startswith("<"):
        close = inner.find(">")
        if close != -1:
            src = inner[1:close].strip()
            rest = inner[close + 1:].strip()
            title = None
            if rest.startswith('"') and rest.endswith('"') and len(rest) >= 2:
                title = rest[1:-1]
            elif rest.startswith("'") and rest.endswith("'") and len(rest) >= 2:
                title = rest[1:-1]
            return src, title

    title = None
    m = re.match(r'^(?P<src>.+?)\s+(?P<title>"[^"]*"|\'[^\']*\')\s*$', inner, re.DOTALL)
    if m:
        src = (m.group("src") or "").strip()
        title = (m.group("title") or "").strip().strip("\"'")
        return src, title

    return inner, None


def find_matching_paren(text: str, start_pos: int) -> int:
    depth = 0
    i = start_pos
    in_angle = False
    while i < len(text):
        ch = text[i]

        if ch == "<" and depth == 1 and not in_angle:
            in_angle = True
        elif ch == ">" and in_angle:
            in_angle = False
        elif not in_angle:
            if ch == "(":
                depth += 1
            elif ch == ")":
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
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[pos:i + 1], i + 1
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
        alt = text[pos + 2:alt_end]
        inner = text[paren_start + 1:paren_end]
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


def download_remote_image(url: str, target_path: Path, timeout: int = 30, dry_run: bool = False) -> bool:
    if dry_run:
        logger.info(f"[DRY RUN] Simulato download da {url} -> {target_path}")
        return True

    ensure_dir(target_path.parent)
    try:
        with requests.get(url, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            with open(target_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=65536):
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
        img = flatten_on_white(img)
        img.save(target_jpg_path, "JPEG", quality=95)


def normalize_remote_to_jpg(url: str, target_jpg_path: Path, temp_dir: Path, dry_run: bool = False) -> bool:
    if dry_run:
        logger.info(f"[DRY RUN] Simulata normalizzazione remota {url} -> {target_jpg_path}")
        return True

    ensure_dir(temp_dir)
    ext = infer_extension_from_url(url)
    temp_path = temp_dir / f"download_{sha1_short(url)}{ext}"

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
        img_dir = md_file.parent / "imgs"

    base = sanitize_name(md_file.stem)
    if is_remote_url(source):
        source_stem = "remote_" + sha1_short(source)
    else:
        source_stem = sanitize_name(Path(source).stem)

    filename = f"{base}_img{ordinal}_r{line_no}_{source_stem}.jpg"
    return img_dir / filename

def extract_width_percent_from_html_ref(ref: ImageReference) -> Optional[int]:
    if ref.html_width:
        m = re.match(r"^\s*(\d+)\s*%\s*$", ref.html_width)
        if m:
            return int(m.group(1))

    m = re.search(r'(?i)\bstyle\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s>]+))', ref.raw)
    if m:
        style = (m.group(2) or m.group(3) or m.group(4) or "").strip()

        m2 = re.search(r"(?i)\bmax-width\s*:\s*(\d+)\s*%", style)
        if m2:
            return int(m2.group(1))

        m2 = re.search(r"(?i)\bwidth\s*:\s*(\d+)\s*%", style)
        if m2:
            return int(m2.group(1))

    return None


def build_replacement_image_markup(
    md_type: MarkdownTypeInfo,
    ref: ImageReference,
    rel_path: str,
    ordinal: int
) -> str:
    alt = ref.alt or f"image_{ordinal}"

    if ref.source_type == "markdown":
        if ref.attrs:
            return f"![{alt}]({rel_path}){ref.attrs}"
        return f"![{alt}]({rel_path})"

    width_percent = extract_width_percent_from_html_ref(ref)
    if width_percent is not None:
        return f"![{alt}]({rel_path}){{width={width_percent}%}}"

    return f"![{alt}]({rel_path})"


def handle_remote_image_reference(
    ref: ImageReference,
    ordinal: int,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    target_jpg_path: Path,
    temp_dir: Path,
    output_dir: Path,
    dry_run: bool
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

    if target_jpg_path.exists() and not dry_run:
        actions.append(f"Immagine remota riga {ref.start_line}: JPG già esistente")
        replacement = build_replacement_image_markup(md_type, ref, rel_path, ordinal)
        return replacement, actions

    success = normalize_remote_to_jpg(ref.src, target_jpg_path, temp_dir, dry_run=dry_run)
    if success:
        if not dry_run:
            actions.append(f"Immagine remota riga {ref.start_line}: salvata come {target_jpg_path.name}")
        else:
            actions.append(f"[DRY RUN] Immagine remota riga {ref.start_line}: salvata come {target_jpg_path.name}")
        replacement = build_replacement_image_markup(md_type, ref, rel_path, ordinal)
        return replacement, actions

    actions.append(f"Immagine remota riga {ref.start_line}: conversione fallita, riferimento originale mantenuto")
    return ref.raw, actions


def handle_local_image_reference(
    ref: ImageReference,
    ordinal: int,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    target_jpg_path: Path,
    output_dir: Path,
    dry_run: bool
) -> Tuple[str, List[str]]:
    actions: List[str] = []
    rel_jpg = relative_posix_path(target_jpg_path, output_dir)

    requested_source = (md_file.parent / ref.src).resolve() if not os.path.isabs(ref.src) else Path(ref.src)
    effective_source = requested_source if requested_source.exists() else None
    if effective_source is None:
        for cand in [requested_source.with_suffix(".jpg"), requested_source.with_suffix(".jpeg")]:
            if cand.exists():
                effective_source = cand
                break

    desc = (
        f"Trovata immagine locale.\n"
        f"Riga: {ref.start_line}\n"
        f"Riferimento: {ref.src}\n"
        f"Sorgente: {requested_source}\n"
        f"Effettivo: {effective_source if effective_source else 'NON TROVATO'}\n"
        f"Target: {target_jpg_path}\n"
        f"Percorso in out/: {rel_jpg}"
    )
    if not confirm.ask(desc):
        actions.append(f"Immagine locale riga {ref.start_line}: operazione saltata")
        return ref.raw, actions

    if effective_source is None:
        actions.append(f"Immagine locale riga {ref.start_line}: sorgente non trovata, riferimento lasciato invariato")
        return ref.raw, actions

    if target_jpg_path.exists() and not dry_run:
        if not needs_regeneration(effective_source, target_jpg_path):
            actions.append(f"Immagine locale riga {ref.start_line}: JPG già aggiornato")
            replacement = build_replacement_image_markup(md_type, ref, rel_jpg, ordinal)
            return replacement, actions

    if dry_run:
        actions.append(
            f"[DRY RUN] Immagine locale riga {ref.start_line}: copia/convertita da {effective_source} a {target_jpg_path}"
        )
    else:
        local_image_to_jpg(effective_source, target_jpg_path, dry_run=False)
        actions.append(f"Immagine locale riga {ref.start_line}: salvata come {target_jpg_path.name}")

    replacement = build_replacement_image_markup(md_type, ref, rel_jpg, ordinal)
    return replacement, actions


def replace_images_in_text(
    text: str,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    dry_run: bool = False
) -> Tuple[str, List[str]]:
    if should_process_md_file(md_file):
        img_dir, _ = get_dirs_for_valid_md(md_file)
    else:
        img_dir = md_file.parent / "imgs"

    temp_dir = img_dir / "_tmp"
    if not dry_run:
        ensure_dir(img_dir)
        ensure_dir(temp_dir)

    output_dir = get_output_path_for_md(md_file).parent

    excluded_spans = merge_spans(
        get_fenced_spans(text)
        + get_inline_code_spans(text)
        + get_html_code_spans(text)
        + [(b.start_idx, b.end_idx) for b in find_plantuml_blocks(text, md_file)]
    )

    refs = find_html_images(text, excluded_spans=excluded_spans) + find_markdown_images(text, excluded_spans=excluded_spans)
    refs = sorted(refs, key=lambda r: r.start_idx)

    actions: List[str] = []
    result_parts: List[str] = []
    last_idx = 0

    for ordinal, ref in enumerate(refs, start=1):
        result_parts.append(text[last_idx:ref.start_idx])
        last_idx = ref.end_idx

        target_jpg_path = build_target_jpg_path_for_image(md_file, ordinal, ref.start_line, ref.src)

        if is_remote_url(ref.src):
            replacement, ref_actions = handle_remote_image_reference(
                ref, ordinal, md_file, md_type, confirm, target_jpg_path, temp_dir, output_dir, dry_run
            )
        else:
            replacement, ref_actions = handle_local_image_reference(
                ref, ordinal, md_file, md_type, confirm, target_jpg_path, output_dir, dry_run
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


def process_plantuml_blocks(
    text: str,
    md_file: Path,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    plantuml_jar: Optional[Path],
    keep_source: bool = False,
    dry_run: bool = False
) -> Tuple[str, List[str]]:
    blocks = find_plantuml_blocks(text, md_file)
    if not blocks:
        return text, []

    actions: List[str] = []
    result_parts: List[str] = []
    last_idx = 0
    out_file = get_output_path_for_md(md_file)

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

        body = block.body.strip()
        if not body:
            body = 'note "Diagramma vuoto"'

        if not re.match(r"^\s*@startuml", body, re.IGNORECASE):
            puml_content = f"@startuml\n{body}\n@enduml"
        else:
            puml_content = body

        if dry_run:
            actions.append(f"[DRY RUN] PlantUML blocco {block.ordinal}: scritto {block.puml_path.name}")
        else:
            if write_text_file_if_changed(block.puml_path, puml_content):
                actions.append(f"PlantUML blocco {block.ordinal}: creato/aggiornato {block.puml_path.name}")
            else:
                actions.append(f"PlantUML blocco {block.ordinal}: invariato")

        if plantuml_jar is None:
            raise RuntimeError("Specificare --plantuml-jar")

        if dry_run:
            actions.append(f"[DRY RUN] PlantUML blocco {block.ordinal}: generato/aggiornato JPG")
        else:
            if needs_regeneration(block.puml_path, block.jpg_path):
                render_plantuml_to_jpg(block.puml_path, block.jpg_path, plantuml_jar, dry_run=False)
                actions.append(f"PlantUML blocco {block.ordinal}: creato/aggiornato JPG")
            else:
                actions.append(f"PlantUML blocco {block.ordinal}: JPG già aggiornato")

        rel_img = relative_posix_path(block.jpg_path, out_file.parent)
        img_md = build_image_markdown(md_type.kind, f"PlantUML {block.ordinal}", rel_img, 70)

        if keep_source:
            result_parts.append(text[block.start_idx:block.end_idx] + "\n\n" + img_md)
        else:
            result_parts.append(img_md)

    result_parts.append(text[last_idx:])
    return "".join(result_parts), actions


def clean_html_wrappers(text: str) -> str:
    pattern = re.compile(
        r'(?is)<div[^>]*>\s*(\!\[[^\]]*\]\([^\)]*\)(?:\{[^}]*\})?)\s*</div>'
    )
    return pattern.sub(r"\1", text)


def is_markdown_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in {".md", ".markdown", ".mdown", ".mkd"}


def is_already_processed(path: Path) -> bool:
    return "out" in path.parts or path.stem.endswith("_processed")


def iter_markdown_files(root: Path) -> List[Path]:
    files = []
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
    keep_plantuml_source: bool = False,
    dry_run: bool = False
) -> ProcessResult:
    if not md_file.exists():
        raise FileNotFoundError(f"File non trovato: {md_file}")

    original_text = md_file.read_text(encoding="utf-8-sig")
    md_type = detect_markdown_type(original_text)
    confirm = ConfirmManager(assume_yes=assume_yes, dry_run=dry_run)

    logger.info(f"File: {md_file}")
    logger.info(f"Tipo: {md_type.kind}")

    output_path = get_output_path_for_md(md_file)
    desc = f"Creazione file elaborato:\n  {md_file}\n  -> {output_path}"
    if not confirm.ask(desc):
        raise RuntimeError("Annullata")

    text_after_puml, actions_puml = process_plantuml_blocks(
        original_text,
        md_file,
        md_type,
        confirm,
        plantuml_jar,
        keep_source=keep_plantuml_source,
        dry_run=dry_run,
    )

    final_text, actions_img = replace_images_in_text(
        text_after_puml,
        md_file,
        md_type,
        confirm,
        dry_run=dry_run,
    )

    final_text = clean_html_wrappers(final_text)

    if not dry_run:
        ensure_dir(output_path.parent)
        output_path.write_text(final_text, encoding="utf-8", newline="\n")
    else:
        logger.info(f"[DRY RUN] File non scritto: {output_path}")

    actions = [f"Tipo: {md_type.kind}"] + actions_puml + actions_img
    if not dry_run:
        actions.append(f"Creato: {output_path}")
    else:
        actions.append(f"[DRY RUN] Sarebbe stato creato: {output_path}")

    return ProcessResult(final_text, actions)


def process_tree(
    root: Path,
    plantuml_jar: Optional[Path],
    assume_yes: bool = False,
    keep_plantuml_source: bool = False,
    dry_run: bool = False
) -> int:
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Root non valida: {root}")

    files = iter_markdown_files(root)
    logger.info(f"Radice: {root}, file trovati: {len(files)}")
    if not files:
        return 0

    processed = 0
    skipped = 0
    failures = 0

    for md_file in files:
        if md_file.name.lower().startswith("temp"):
            skipped += 1
            logger.warning(f"Ignoro file temporaneo: {md_file}")
            continue

        if not should_process_md_file(md_file):
            skipped += 1
            logger.warning(f"File saltato (non in src/): {md_file}")
            continue

        try:
            result = process_markdown_file(
                md_file,
                plantuml_jar,
                assume_yes,
                keep_plantuml_source,
                dry_run
            )
            processed += 1
            print("\nAzioni:")
            for a in result.actions:
                print(f" - {a}")
        except Exception as e:
            failures += 1
            logger.error(f"ERRORE in {md_file}: {e}", exc_info=False)

    logger.info(
        f"Riepilogo: trovati {len(files)}, elaborati {processed}, saltati {skipped}, errori {failures}"
    )
    return 1 if failures else 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Processa Markdown con immagini e PlantUML")
    parser.add_argument("root", nargs="?", default="./", help="Directory radice")
    parser.add_argument("--plantuml-jar", help="Percorso a plantuml.jar")
    parser.add_argument("--yes", action="store_true", help="Conferma automatica")
    parser.add_argument("--verbose", action="store_true", help="Log dettagliato")
    parser.add_argument("--dry-run", action="store_true", help="Simula")
    parser.add_argument("--keep-plantuml-source", action="store_true", help="Mantieni codice PlantUML")
    return parser


def resolve_plantuml_jar(arg_value: Optional[str]) -> Optional[Path]:
    if arg_value:
        return Path(arg_value).expanduser().resolve()
    env = os.environ.get("PLANTUML_JAR", "").strip()
    return Path(env).expanduser().resolve() if env else None


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    root = Path(args.root).expanduser().resolve()
    custom_root = False
    if root == Path("./").resolve():
        root = Path(input("inserire radice root: ").strip()).expanduser().resolve()
        custom_root = True

    plantuml_jar = resolve_plantuml_jar(args.plantuml_jar)
    if plantuml_jar is None:
        logger.error("PlantUML jar non specificato. Usare --plantuml-jar o variabile PLANTUML_JAR.")
        return 1

    try:
        return process_tree(root, plantuml_jar, args.yes, args.keep_plantuml_source, args.dry_run)
    except Exception as e:
        logger.error(f"Errore fatale: {e}")
        return 1
    finally:
        if custom_root:
            logger.info(f"Root personalizzato: {root}")


if __name__ == "__main__":
    raise SystemExit(main())