from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineContext:
    workspace_root: Path
    doc_root: Path
    src_dir: Path
    imgs_dir: Path
    puml_dir: Path
    step20_md_dir: Path
    step40_pdf_dir: Path
    publish_dir: Path
    downloaded_images_dir: Path
    puml_images_dir: Path
    authoring_dir: Path
    latex_dir: Path
    default_header: Path
    plantuml_jar: Path | None


def find_workspace_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent

    for parent in [current] + list(current.parents):
        if (parent / "005_authoring").is_dir():
            return parent

    script_path = Path(__file__).resolve()
    for parent in [script_path.parent] + list(script_path.parents):
        if (parent / "005_authoring").is_dir():
            return parent

    return Path.cwd().resolve()


def build_pipeline_context(source_md: Path, plantuml_jar: Path | None = None) -> PipelineContext:
    source_md = source_md.resolve()

    if source_md.parent.name != "src":
        raise ValueError(f"Il file Markdown sorgente deve trovarsi direttamente in una directory src/: {source_md}")

    doc_root = source_md.parent.parent
    workspace_root = find_workspace_root(source_md)
    authoring_dir = workspace_root / "005_authoring"

    return PipelineContext(
        workspace_root=workspace_root,
        doc_root=doc_root,
        src_dir=doc_root / "src",
        imgs_dir=doc_root / "imgs",
        puml_dir=doc_root / "puml",
        step20_md_dir=doc_root / "step20_md",
        step40_pdf_dir=doc_root / "step40_pdf",
        publish_dir=doc_root / "PUBLISH",
        downloaded_images_dir=doc_root / "step20_md" / "imgs_downloaded",
        puml_images_dir=doc_root / "step20_md" / "imgs_puml",
        authoring_dir=authoring_dir,
        latex_dir=authoring_dir / "latex",
        default_header=authoring_dir / "latex" / "header1.tex",
        plantuml_jar=plantuml_jar,
    )


def ensure_pipeline_dirs(ctx: PipelineContext) -> None:
    for directory in [
        ctx.imgs_dir,
        ctx.puml_dir,
        ctx.step20_md_dir,
        ctx.step40_pdf_dir,
        ctx.publish_dir,
        ctx.downloaded_images_dir,
        ctx.puml_images_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)
