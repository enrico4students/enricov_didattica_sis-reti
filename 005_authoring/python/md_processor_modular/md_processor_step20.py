from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
from PIL import Image

from md_pipeline_confirm import ConfirmManager
from md_pipeline_context import PipelineContext
from md_pipeline_logging import logger
from md_pipeline_utils import (
    line_number_from_index,
    relative_posix_path,
    sanitize_name,
    sha1_short,
    write_text_file_if_changed,
)


@dataclass(frozen=True)
class MarkdownTypeInfo:
    kind: str
    reason: str


@dataclass(frozen=True)
class PlantUMLBlock:
    ordinal: int
    start_line: int
    body: str
    start_idx: int
    end_idx: int
    puml_path: Path
    jpg_path: Path


FENCE_PATTERN = re.compile(
    r"(?ms)^(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>[^\n`]*)\n(?P<body>.*?)^\1[ \t]*$"
)

FREE_PLANTUML_PATTERN = re.compile(
    r"(?ms)^[ \t]*@startuml[ \t]*(?P<info>[^\n]*)\n(?P<body>.*?)^[ \t]*@enduml[ \t]*$"
)

MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)(?P<attrs>\{[^}]*\})?")


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
            return MarkdownTypeInfo("pandoc", f"Rilevato costrutto compatibile con Pandoc Markdown: {pattern}")

    return MarkdownTypeInfo("standard", "Nessun segnale specifico di Marp o Pandoc Markdown")


def flatten_on_white(img: Image.Image) -> Image.Image:
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

    return False


def local_image_to_jpg(src_path: Path, target_jpg_path: Path, dry_run: bool = False) -> None:
    if dry_run:
        logger.info(f"[DRY RUN] Simulata copia/conversione immagine: {src_path} -> {target_jpg_path}")
        return

    target_jpg_path.parent.mkdir(parents=True, exist_ok=True)

    if src_path.suffix.lower() in (".jpg", ".jpeg"):
        if src_path.resolve() != target_jpg_path.resolve():
            shutil.copy2(src_path, target_jpg_path)
        return

    if src_path.suffix.lower() == ".svg":
        png_temp = target_jpg_path.with_suffix(".tmp.png")
        if not convert_svg_to_png(src_path, png_temp):
            raise RuntimeError(f"Conversione SVG fallita: {src_path}")
        try:
            with Image.open(png_temp) as img:
                flatten_on_white(img).save(target_jpg_path, "JPEG", quality=95)
        finally:
            png_temp.unlink(missing_ok=True)
        return

    with Image.open(src_path) as img:
        flatten_on_white(img).save(target_jpg_path, "JPEG", quality=95)


def download_remote_image_to_jpg(url: str, target_jpg_path: Path, dry_run: bool = False) -> bool:
    if dry_run:
        logger.info(f"[DRY RUN] Simulato download immagine: {url} -> {target_jpg_path}")
        return True

    temp_path = target_jpg_path.with_suffix(".download")
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(temp_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    file.write(chunk)

        local_image_to_jpg(temp_path, target_jpg_path)
        return True
    except Exception as exc:
        logger.error(f"Download/conversione immagine remota fallita: {url}: {exc}")
        return False
    finally:
        temp_path.unlink(missing_ok=True)


def make_plantuml_block(
    source_md: Path,
    ctx: PipelineContext,
    ordinal: int,
    start_line: int,
    body: str,
    start_idx: int,
    end_idx: int,
) -> PlantUMLBlock:
    base_name = sanitize_name(source_md.stem)
    suffix = f"{base_name}_{ordinal}_r{start_line}"
    return PlantUMLBlock(
        ordinal=ordinal,
        start_line=start_line,
        body=body,
        start_idx=start_idx,
        end_idx=end_idx,
        puml_path=ctx.puml_dir / f"{suffix}.puml",
        jpg_path=ctx.imgs_dir / f"{suffix}_puml.jpg",
    )


def find_plantuml_blocks(text: str, source_md: Path, ctx: PipelineContext) -> list[PlantUMLBlock]:
    blocks: list[PlantUMLBlock] = []
    fenced_spans: list[tuple[int, int]] = []
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
        blocks.append(make_plantuml_block(source_md, ctx, ordinal, start_line, body, match.start(), match.end()))

    for match in FREE_PLANTUML_PATTERN.finditer(text):
        if any(start <= match.start() < end for start, end in fenced_spans):
            continue

        ordinal += 1
        start_line = line_number_from_index(text, match.start())
        full_body = text[match.start():match.end()]
        blocks.append(make_plantuml_block(source_md, ctx, ordinal, start_line, full_body, match.start(), match.end()))

    return sorted(blocks, key=lambda block: block.start_idx)


def render_plantuml_to_jpg(puml_path: Path, jpg_path: Path, plantuml_jar: Path, dry_run: bool = False) -> None:
    if dry_run:
        logger.info(f"[DRY RUN] Simulata generazione PlantUML: {puml_path} -> {jpg_path}")
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
        raise RuntimeError(f"PNG non generato da PlantUML: {generated_png}")

    jpg_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(generated_png) as img:
        flatten_on_white(img).save(jpg_path, "JPEG", quality=95)

    generated_png.unlink(missing_ok=True)


def build_image_markdown(md_type: str, alt: str, rel_path: str, width_percent: int | None = None) -> str:
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
    source_md: Path,
    processed_md: Path,
    ctx: PipelineContext,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    keep_source: bool,
    dry_run: bool,
) -> tuple[str, list[str]]:
    blocks = find_plantuml_blocks(text, source_md, ctx)
    if not blocks:
        return text, []

    if ctx.plantuml_jar is None:
        raise RuntimeError("Sono presenti blocchi PlantUML: specificare --plantuml-jar o PLANTUML_JAR")

    actions: list[str] = []
    parts: list[str] = []
    last_idx = 0

    for block in blocks:
        parts.append(text[last_idx:block.start_idx])
        last_idx = block.end_idx

        desc = (
            f"Trovato blocco PlantUML (riga {block.start_line}).\n"
            f"File .puml: {block.puml_path}\n"
            f"Immagine: {block.jpg_path}"
        )
        if not confirm.ask(desc):
            parts.append(text[block.start_idx:block.end_idx])
            actions.append(f"PlantUML blocco {block.ordinal}: saltato")
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
            render_plantuml_to_jpg(block.puml_path, block.jpg_path, ctx.plantuml_jar)
            actions.append(f"PlantUML blocco {block.ordinal}: creato/aggiornato JPG")
        else:
            actions.append(f"PlantUML blocco {block.ordinal}: JPG già aggiornato")

        rel_img = relative_posix_path(block.jpg_path, processed_md.parent)
        img_md = build_image_markdown(md_type.kind, f"PlantUML {block.ordinal}", rel_img, width_percent=70)

        if keep_source:
            parts.append(text[block.start_idx:block.end_idx] + "\n\n" + img_md)
        else:
            parts.append(img_md)

    parts.append(text[last_idx:])
    return "".join(parts), actions


def resolve_local_image_source(base_dir: Path, src: str) -> Path | None:
    src = src.strip().strip("<>").strip()
    src = src.split()[0].strip()

    candidate = Path(src) if os.path.isabs(src) else base_dir / src
    candidate = candidate.resolve()

    if candidate.exists():
        return candidate

    for suffix in [".jpg", ".jpeg", ".png", ".svg", ".webp"]:
        alt = candidate.with_suffix(suffix)
        if alt.exists():
            return alt

    return None


def normalize_images_in_text(
    text: str,
    source_md: Path,
    processed_md: Path,
    ctx: PipelineContext,
    md_type: MarkdownTypeInfo,
    confirm: ConfirmManager,
    dry_run: bool,
    force_remote: bool,
) -> tuple[str, list[str]]:
    actions: list[str] = []
    parts: list[str] = []
    last_idx = 0
    ordinal = 0

    for match in MARKDOWN_IMAGE_PATTERN.finditer(text):
        src = match.group("src").strip()
        alt = match.group("alt") or "immagine"
        attrs = match.group("attrs") or ""

        # Evitare immagini dentro URL con parentesi o sintassi complessa non gestita.
        if not src:
            continue

        ordinal += 1
        parts.append(text[last_idx:match.start()])
        last_idx = match.end()

        start_line = line_number_from_index(text, match.start())
        source_stem = "remote_" + sha1_short(src) if src.lower().startswith(("http://", "https://")) else sanitize_name(Path(src).stem)
        target_jpg = ctx.imgs_dir / f"{sanitize_name(source_md.stem)}_img{ordinal}_r{start_line}_{source_stem}.jpg"
        rel_jpg = relative_posix_path(target_jpg, processed_md.parent)

        desc = (
            f"Trovata immagine Markdown.\n"
            f"Riga: {start_line}\n"
            f"Riferimento: {src}\n"
            f"Target: {target_jpg}\n"
            f"Percorso nel Markdown elaborato: {rel_jpg}"
        )
        if not confirm.ask(desc):
            parts.append(match.group(0))
            actions.append(f"Immagine riga {start_line}: saltata")
            continue

        if src.lower().startswith(("http://", "https://")):
            if target_jpg.exists() and not force_remote:
                actions.append(f"Immagine remota riga {start_line}: JPG già esistente")
            elif download_remote_image_to_jpg(src, target_jpg, dry_run=dry_run):
                actions.append(f"Immagine remota riga {start_line}: salvata come {target_jpg.name}")
            else:
                actions.append(f"Immagine remota riga {start_line}: conversione fallita, riferimento originale mantenuto")
                parts.append(match.group(0))
                continue
        else:
            source_path = resolve_local_image_source(source_md.parent, src)
            if source_path is None:
                actions.append(f"Immagine locale riga {start_line}: sorgente non trovata, riferimento invariato")
                parts.append(match.group(0))
                continue

            if target_jpg.exists() and not dry_run and not needs_regeneration(source_path, target_jpg):
                actions.append(f"Immagine locale riga {start_line}: JPG già aggiornato")
            else:
                local_image_to_jpg(source_path, target_jpg, dry_run=dry_run)
                actions.append(f"Immagine locale riga {start_line}: salvata come {target_jpg.name}")

        replacement = build_image_markdown(md_type.kind, alt, rel_jpg)
        if attrs and md_type.kind != "marp":
            replacement += attrs

        parts.append(replacement)

    parts.append(text[last_idx:])
    return "".join(parts), actions


def clean_html_wrappers(text: str) -> str:
    pattern = re.compile(r'(?is)<div[^>]*>\s*(\!\[[^\]]*\]\([^\)]*\)(?:\{[^}]*\})?)\s*</div>')
    return pattern.sub(r"\1", text)


def step20_process_markdown(
    source_md: Path,
    previous_dir: Path,
    current_dir: Path,
    next_dir: Path,
    ctx: PipelineContext,
    confirm: ConfirmManager,
    keep_plantuml_source: bool = False,
    dry_run: bool = False,
    force_remote: bool = False,
) -> tuple[Path, str, list[str]]:
    logger.info("STEP 20 - Preprocessamento Markdown")
    logger.info(f"PREVIOUS DIR: {previous_dir}")
    logger.info(f"CURRENT DIR: {current_dir}")
    logger.info(f"NEXT DIR: {next_dir}")

    current_dir.mkdir(parents=True, exist_ok=True)
    ctx.imgs_dir.mkdir(parents=True, exist_ok=True)
    ctx.puml_dir.mkdir(parents=True, exist_ok=True)

    processed_md = current_dir / source_md.name

    desc = f"Creazione file elaborato:\n  {source_md}\n  -> {processed_md}"
    if not confirm.ask(desc):
        raise RuntimeError("Operazione annullata")

    original_text = source_md.read_text(encoding="utf-8-sig")
    md_type = detect_markdown_type(original_text)

    logger.info(f"File: {source_md}")
    logger.info(f"Tipo Markdown: {md_type.kind}")

    text_after_puml, actions_puml = process_plantuml_blocks(
        text=original_text,
        source_md=source_md,
        processed_md=processed_md,
        ctx=ctx,
        md_type=md_type,
        confirm=confirm,
        keep_source=keep_plantuml_source,
        dry_run=dry_run,
    )

    final_text, actions_img = normalize_images_in_text(
        text=text_after_puml,
        source_md=source_md,
        processed_md=processed_md,
        ctx=ctx,
        md_type=md_type,
        confirm=confirm,
        dry_run=dry_run,
        force_remote=force_remote,
    )

    final_text = clean_html_wrappers(final_text)

    if dry_run:
        logger.info(f"[DRY RUN] File non scritto: {processed_md}")
    else:
        processed_md.write_text(final_text, encoding="utf-8", newline="\n")

    actions = [
        f"Tipo: {md_type.kind}",
        f"Motivo tipo: {md_type.reason}",
        *actions_puml,
        *actions_img,
        f"{'[DRY RUN] Sarebbe stato creato' if dry_run else 'Creato'} Markdown elaborato: {processed_md}",
    ]

    return processed_md, final_text, actions
