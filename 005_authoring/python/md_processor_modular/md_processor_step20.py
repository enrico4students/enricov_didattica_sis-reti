"""
STEP 20 - Coordinatore del preprocessamento Markdown.

Questo modulo coordina la sub-pipeline STEP 20, che prepara un file
Markdown sorgente per le fasi successive della pipeline Markdown → PDF.

Sottostep eseguiti:

- STEP 20.1:
  analisi del tipo di Markdown;

- STEP 20.2:
  estrazione e rendering dei blocchi PlantUML;

- STEP 20.3:
  normalizzazione delle immagini Markdown;

- STEP 20.4:
  cleanup finale e scrittura del Markdown elaborato.

La funzione principale è step20_process_markdown().
"""

from __future__ import annotations

from pathlib import Path

from md_pipeline_confirm import ConfirmManager
from md_pipeline_context import PipelineContext
from md_pipeline_logging import logger
from md_pipeline_step20_1 import detect_markdown_type
from md_pipeline_step20_2 import process_plantuml_blocks
from md_pipeline_step20_3 import normalize_images_in_text
from md_pipeline_step20_4 import clean_html_wrappers, write_processed_markdown


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
    ctx.downloaded_images_dir.mkdir(parents=True, exist_ok=True)
    ctx.puml_images_dir.mkdir(parents=True, exist_ok=True)

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

    text_after_images, actions_img = normalize_images_in_text(
        text=text_after_puml,
        source_md=source_md,
        processed_md=processed_md,
        ctx=ctx,
        md_type=md_type,
        confirm=confirm,
        dry_run=dry_run,
        force_remote=force_remote,
    )

    final_text = clean_html_wrappers(text_after_images)

    write_processed_markdown(
        path=processed_md,
        text=final_text,
        dry_run=dry_run,
    )

    if dry_run:
        logger.info(f"[DRY RUN] File non scritto: {processed_md}")

    actions = [
        f"Tipo: {md_type.kind}",
        f"Motivo tipo: {md_type.reason}",
        *actions_puml,
        *actions_img,
        f"{'[DRY RUN] Sarebbe stato creato' if dry_run else 'Creato'} Markdown elaborato: {processed_md}",
    ]

    return processed_md, final_text, actions