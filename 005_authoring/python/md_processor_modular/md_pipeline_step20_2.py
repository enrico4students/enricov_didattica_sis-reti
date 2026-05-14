"""
STEP 20.2 - Gestione dei blocchi PlantUML.

Questo modulo gestisce i diagrammi PlantUML presenti in un documento
Markdown.

Funzionalità principali:

- individuare blocchi PlantUML fenced o liberi;
- estrarre il contenuto in file .puml;
- generare immagini JPG tramite plantuml.jar;
- sostituire o affiancare i blocchi sorgente con riferimenti immagine;
- produrre un elenco delle azioni eseguite.

Le immagini PlantUML generate vengono salvate nella directory dedicata
ctx.puml_images_dir, normalmente step20_md/imgs_puml.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from md_pipeline_confirm import ConfirmManager
from md_pipeline_context import PipelineContext
from md_pipeline_logging import logger
from md_pipeline_step20_1 import MarkdownTypeInfo
from md_pipeline_step20_4 import build_image_markdown
from md_pipeline_utils import (
    line_number_from_index,
    relative_posix_path,
    sanitize_name,
    write_text_file_if_changed,
)


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
        jpg_path=ctx.puml_images_dir / f"{suffix}_puml.jpg",
    )


def find_plantuml_blocks(
    text: str,
    source_md: Path,
    ctx: PipelineContext,
) -> list[PlantUMLBlock]:
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

        blocks.append(
            make_plantuml_block(
                source_md=source_md,
                ctx=ctx,
                ordinal=ordinal,
                start_line=start_line,
                body=body,
                start_idx=match.start(),
                end_idx=match.end(),
            )
        )

    for match in FREE_PLANTUML_PATTERN.finditer(text):
        if any(start <= match.start() < end for start, end in fenced_spans):
            continue

        ordinal += 1
        start_line = line_number_from_index(text, match.start())
        full_body = text[match.start():match.end()]

        blocks.append(
            make_plantuml_block(
                source_md=source_md,
                ctx=ctx,
                ordinal=ordinal,
                start_line=start_line,
                body=full_body,
                start_idx=match.start(),
                end_idx=match.end(),
            )
        )

    return sorted(blocks, key=lambda block: block.start_idx)


def render_plantuml_to_jpg(
    puml_path: Path,
    jpg_path: Path,
    plantuml_jar: Path,
    dry_run: bool = False,
) -> None:
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
        img_md = build_image_markdown(
            md_type=md_type.kind,
            alt=f"PlantUML {block.ordinal}",
            rel_path=rel_img,
            width_percent=70,
        )

        if keep_source:
            parts.append(text[block.start_idx:block.end_idx] + "\n\n" + img_md)
        else:
            parts.append(img_md)

    parts.append(text[last_idx:])
    return "".join(parts), actions