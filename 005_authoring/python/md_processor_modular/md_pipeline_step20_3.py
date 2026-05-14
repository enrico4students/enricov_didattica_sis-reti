"""
STEP 20.3 - Normalizzazione immagini Markdown.

Questo modulo gestisce i riferimenti immagine presenti nel Markdown.

Funzionalità principali:

- riconoscere immagini Markdown locali e remote;
- scaricare immagini remote HTTP/HTTPS;
- convertire immagini locali e remote in JPG;
- appiattire immagini con trasparenza su sfondo bianco;
- aggiornare i riferimenti immagine nel Markdown elaborato.

Le immagini remote scaricate vengono salvate nella directory dedicata
ctx.downloaded_images_dir, normalmente step20_md/imgs_downloaded.

Le immagini locali convertite vengono salvate in ctx.imgs_dir.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import requests
from PIL import Image

from md_pipeline_confirm import ConfirmManager
from md_pipeline_context import PipelineContext
from md_pipeline_logging import logger
from md_pipeline_step20_1 import MarkdownTypeInfo
from md_pipeline_step20_2 import flatten_on_white, needs_regeneration
from md_pipeline_step20_4 import build_image_markdown
from md_pipeline_utils import (
    line_number_from_index,
    relative_posix_path,
    sanitize_name,
    sha1_short,
)


MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)(?P<attrs>\{[^}]*\})?")


def convert_svg_to_png(svg_path: Path, png_path: Path) -> bool:
    try:
        import cairosvg

        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(png_path),
            background_color="white",
        )
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


def local_image_to_jpg(
    src_path: Path,
    target_jpg_path: Path,
    dry_run: bool = False,
) -> None:
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


def download_remote_image_to_jpg(
    url: str,
    target_jpg_path: Path,
    dry_run: bool = False,
) -> bool:
    if dry_run:
        logger.info(f"[DRY RUN] Simulato download immagine: {url} -> {target_jpg_path}")
        return True

    target_jpg_path.parent.mkdir(parents=True, exist_ok=True)
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

        if not src:
            continue

        ordinal += 1

        parts.append(text[last_idx:match.start()])
        last_idx = match.end()

        start_line = line_number_from_index(text, match.start())
        is_remote = src.lower().startswith(("http://", "https://"))

        if is_remote:
            source_stem = "remote_" + sha1_short(src)
            target_jpg = ctx.downloaded_images_dir / (
                f"{sanitize_name(source_md.stem)}_img{ordinal}_r{start_line}_{source_stem}.jpg"
            )
        else:
            source_stem = sanitize_name(Path(src).stem)
            target_jpg = ctx.imgs_dir / (
                f"{sanitize_name(source_md.stem)}_img{ordinal}_r{start_line}_{source_stem}.jpg"
            )

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

        if is_remote:
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
                local_image_to_jpg(
                    src_path=source_path,
                    target_jpg_path=target_jpg,
                    dry_run=dry_run,
                )
                actions.append(f"Immagine locale riga {start_line}: salvata come {target_jpg.name}")

        replacement = build_image_markdown(
            md_type=md_type.kind,
            alt=alt,
            rel_path=rel_jpg,
        )

        if attrs and md_type.kind != "marp":
            replacement += attrs

        parts.append(replacement)

    parts.append(text[last_idx:])
    return "".join(parts), actions
