from __future__ import annotations

import os
import subprocess
from pathlib import Path

from md_pipeline_context import PipelineContext
from md_pipeline_logging import logger


def build_pandoc_resource_path(ctx: PipelineContext) -> str:
    paths = [
        ctx.step20_md_dir,
        ctx.imgs_dir,
        ctx.puml_dir,
        ctx.src_dir,
        ctx.workspace_root,
        ctx.authoring_dir,
        ctx.authoring_dir / "imgs",
    ]

    return os.pathsep.join(str(path) for path in paths if path.exists())


def has_include_header_arg(args: list[str]) -> bool:
    for arg in args:
        if arg == "-H":
            return True
        if arg == "--include-in-header":
            return True
        if arg.startswith("--include-in-header="):
            return True
    return False


def step40_generate_pdf(
    processed_md: Path,
    previous_dir: Path,
    current_dir: Path,
    next_dir: Path,
    ctx: PipelineContext,
    pandoc_cmd: str = "pandoc",
    pdf_engine: str | None = "xelatex",
    extra_args: list[str] | None = None,
    dry_run: bool = False,
) -> Path:
    logger.info("STEP 40 - Generazione PDF normale")
    logger.info(f"PREVIOUS DIR: {previous_dir}")
    logger.info(f"CURRENT DIR: {current_dir}")
    logger.info(f"NEXT DIR: {next_dir}")

    current_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = current_dir / f"{processed_md.stem}.pdf"

    effective_args = list(extra_args or [])

    if not has_include_header_arg(effective_args) and ctx.default_header.exists():
        effective_args.extend(["-H", str(ctx.default_header)])

    resource_path = build_pandoc_resource_path(ctx)

    command = [
        pandoc_cmd,
        str(processed_md),
        "-o",
        str(output_pdf),
    ]

    if resource_path:
        command.extend(["--resource-path", resource_path])

    if pdf_engine:
        command.extend(["--pdf-engine", pdf_engine])

    command.extend(effective_args)

    logger.info(f"LEGGE: {processed_md}")
    logger.info(f"SCRIVE: {output_pdf}")
    logger.info(f"CWD: {ctx.workspace_root}")
    logger.info(f"RESOURCE-PATH: {resource_path}")
    logger.info(f"COMANDO: {' '.join(command)}")

    if dry_run:
        logger.info(f"[DRY RUN] Generazione PDF simulata: {processed_md} -> {output_pdf}")
        return output_pdf

    result = subprocess.run(
        command,
        cwd=str(ctx.workspace_root),
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
        raise RuntimeError(f"Pandoc fallito per {processed_md}: {stderr.strip()}")

    return output_pdf
