#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path

from md_pipeline_confirm import ConfirmManager
from md_pipeline_context import build_pipeline_context, ensure_pipeline_dirs
from md_pipeline_input import collect_markdown_inputs
from md_pipeline_logging import configure_logging, logger
from md_processor_step20 import step20_process_markdown
from md_processor_step40 import step40_generate_pdf
from md_processor_step90 import step90_rasterize_pdf


@dataclass(frozen=True)
class ProcessResult:
    source_md: Path
    processed_md: Path
    normal_pdf: Path | None
    publish_pdf: Path | None
    actions: list[str]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pipeline modulare Markdown: src -> step20_md -> step40_pdf -> PUBLISH"
    )
    parser.add_argument("root", nargs="?", default="./", help="File Markdown, directory src o directory radice")
    parser.add_argument("--plantuml-jar", help="Percorso a plantuml.jar")
    parser.add_argument("--yes", action="store_true", help="Conferma automatica")
    parser.add_argument("--verbose", action="store_true", help="Log dettagliato")
    parser.add_argument("--dry-run", action="store_true", help="Simula senza scrivere file")
    parser.add_argument("--keep-plantuml-source", action="store_true", help="Mantiene il codice PlantUML nel Markdown")
    parser.add_argument("--force-remote", action="store_true", help="Riscarica immagini remote anche se il JPG esiste già")
    parser.add_argument("--no-pdf", action="store_true", help="Non genera PDF")
    parser.add_argument("--no-publish", action="store_true", help="Non genera PDF rasterizzato")
    parser.add_argument("--dpi", type=int, default=150, help="DPI per il PDF rasterizzato _ro")
    parser.add_argument("--pandoc", default="pandoc", help="Comando o percorso di pandoc")
    parser.add_argument("--pdf-engine", default="xelatex", help="Motore PDF Pandoc")
    parser.add_argument(
        "--pandoc-arg",
        action="append",
        default=[],
        help="Argomento aggiuntivo da passare a Pandoc. Ripetere l'opzione per più argomenti.",
    )
    return parser


def resolve_plantuml_jar(arg_value: str | None) -> Path | None:
    if arg_value:
        return Path(arg_value).expanduser().resolve()

    env_value = os.environ.get("PLANTUML_JAR", "").strip()
    if env_value:
        return Path(env_value).expanduser().resolve()

    return None


def get_log_file(input_root: Path) -> Path:
    input_root = input_root.expanduser().resolve()

    if input_root.is_file():
        if input_root.parent.name == "src":
            return input_root.parent.parent / "md_processor.log"
        return input_root.parent / "md_processor.log"

    if input_root.is_dir() and input_root.name == "src":
        return input_root.parent / "md_processor.log"

    return input_root / "md_processor.log"


def process_one_file(
    source_md: Path,
    plantuml_jar: Path | None,
    assume_yes: bool,
    keep_plantuml_source: bool,
    dry_run: bool,
    force_remote: bool,
    generate_pdf: bool,
    generate_publish: bool,
    dpi: int,
    pandoc_cmd: str,
    pdf_engine: str | None,
    pandoc_args: list[str],
) -> ProcessResult:
    ctx = build_pipeline_context(source_md, plantuml_jar=plantuml_jar)
    ensure_pipeline_dirs(ctx)

    confirm = ConfirmManager(assume_yes=assume_yes, dry_run=dry_run)

    processed_md, _processed_text, actions20 = step20_process_markdown(
        source_md=source_md,
        previous_dir=ctx.src_dir,
        current_dir=ctx.step20_md_dir,
        next_dir=ctx.step40_pdf_dir,
        ctx=ctx,
        confirm=confirm,
        keep_plantuml_source=keep_plantuml_source,
        dry_run=dry_run,
        force_remote=force_remote,
    )

    normal_pdf = None
    publish_pdf = None
    actions = list(actions20)

    if generate_pdf:
        normal_pdf = step40_generate_pdf(
            processed_md=processed_md,
            previous_dir=ctx.step20_md_dir,
            current_dir=ctx.step40_pdf_dir,
            next_dir=ctx.publish_dir,
            ctx=ctx,
            pandoc_cmd=pandoc_cmd,
            pdf_engine=pdf_engine,
            extra_args=pandoc_args,
            dry_run=dry_run,
        )
        actions.append(f"{'[DRY RUN] Sarebbe stato creato' if dry_run else 'Creato'} PDF normale: {normal_pdf}")

        if generate_publish:
            publish_pdf = step90_rasterize_pdf(
                input_pdf=normal_pdf,
                previous_dir=ctx.step40_pdf_dir,
                current_dir=ctx.publish_dir,
                next_dir=None,
                ctx=ctx,
                dpi=dpi,
                dry_run=dry_run,
            )
            actions.append(f"{'[DRY RUN] Sarebbe stato creato' if dry_run else 'Creato'} PDF rasterizzato: {publish_pdf}")

    return ProcessResult(
        source_md=source_md,
        processed_md=processed_md,
        normal_pdf=normal_pdf,
        publish_pdf=publish_pdf,
        actions=actions,
    )


def process_tree(
    root: Path,
    plantuml_jar: Path | None,
    assume_yes: bool = False,
    keep_plantuml_source: bool = False,
    dry_run: bool = False,
    force_remote: bool = False,
    generate_pdf: bool = True,
    generate_publish: bool = True,
    dpi: int = 150,
    pandoc_cmd: str = "pandoc",
    pdf_engine: str | None = "xelatex",
    pandoc_args: list[str] | None = None,
) -> int:
    logger.info("STEP 00 - Raccolta input")
    files = collect_markdown_inputs(root)
    logger.info(f"File Markdown da elaborare: {len(files)}")

    if not files:
        logger.warning(f"Nessun file Markdown valido trovato in: {root}")
        return 0

    processed = 0
    failures = 0

    for source_md in files:
        try:
            result = process_one_file(
                source_md=source_md,
                plantuml_jar=plantuml_jar,
                assume_yes=assume_yes,
                keep_plantuml_source=keep_plantuml_source,
                dry_run=dry_run,
                force_remote=force_remote,
                generate_pdf=generate_pdf,
                generate_publish=generate_publish,
                dpi=dpi,
                pandoc_cmd=pandoc_cmd,
                pdf_engine=pdf_engine,
                pandoc_args=pandoc_args or [],
            )

            processed += 1

            print("\nAzioni:")
            for action in result.actions:
                print(f" - {action}")
                logger.info(f"AZIONE: {action}")

        except Exception as exc:
            failures += 1
            logger.error(f"ERRORE in {source_md}: {exc}", exc_info=True)

    logger.info(f"Riepilogo: elaborati {processed}, errori {failures}")
    return 1 if failures else 0


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    custom_root = False

    if root == Path("./").resolve():
        root = Path(input("Inserire radice root: ").strip()).expanduser().resolve()
        custom_root = True

    configure_logging(args.verbose, get_log_file(root))

    plantuml_jar = resolve_plantuml_jar(args.plantuml_jar)
    if plantuml_jar is None:
        plantuml_jar = os.environ.get("PLANTUML_JAR")


    try:
        return process_tree(
            root=root,
            plantuml_jar=plantuml_jar,
            assume_yes=args.yes,
            keep_plantuml_source=args.keep_plantuml_source,
            dry_run=args.dry_run,
            force_remote=args.force_remote,
            generate_pdf=not args.no_pdf,
            generate_publish=not args.no_publish,
            dpi=args.dpi,
            pandoc_cmd=args.pandoc,
            pdf_engine=args.pdf_engine,
            pandoc_args=args.pandoc_arg,
        )
    except Exception as exc:
        logger.error(f"Errore fatale: {exc}", exc_info=True)
        return 1
    finally:
        if custom_root:
            logger.info(f"Root personalizzato: {root}")


if __name__ == "__main__":
    raise SystemExit(main())
