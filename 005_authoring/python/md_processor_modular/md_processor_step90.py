from __future__ import annotations

from pathlib import Path

import pymupdf

from md_pipeline_context import PipelineContext
from md_pipeline_logging import logger


def step90_rasterize_pdf(
    input_pdf: Path,
    previous_dir: Path,
    current_dir: Path,
    next_dir: Path | None,
    ctx: PipelineContext,
    dpi: int = 150,
    dry_run: bool = False,
) -> Path:
    logger.info("STEP 90 - Rasterizzazione PDF pubblicabile")
    logger.info(f"PREVIOUS DIR: {previous_dir}")
    logger.info(f"CURRENT DIR: {current_dir}")
    logger.info(f"NEXT DIR: {next_dir if next_dir else 'NESSUNA'}")

    if dpi <= 0:
        raise ValueError("Il valore DPI deve essere maggiore di zero")

    current_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = current_dir / f"{input_pdf.stem}_ro.pdf"

    logger.info(f"LEGGE: {input_pdf}")
    logger.info(f"SCRIVE: {output_pdf}")
    logger.info(f"DPI: {dpi}")

    if dry_run:
        logger.info(f"[DRY RUN] Simulata rasterizzazione PDF: {input_pdf} -> {output_pdf}")
        return output_pdf

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

    return output_pdf
