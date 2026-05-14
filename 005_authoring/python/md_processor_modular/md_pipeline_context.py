"""
Modulo per la configurazione e inizializzazione del contesto operativo
della pipeline Markdown → PDF.

Questo modulo definisce:

- la struttura dati PipelineContext, che raccoglie in modo centralizzato
  tutti i path utilizzati dalla pipeline;

- le funzioni di individuazione automatica della root del workspace;

- la costruzione del contesto completo a partire da un file Markdown
  sorgente;

- la creazione automatica delle directory operative necessarie.

La pipeline è progettata per lavorare con una struttura di progetto
organizzata in directory standardizzate, ad esempio:

    progetto/
    ├── 005_authoring/
    ├── documento/
    │   ├── src/
    │   ├── imgs/
    │   ├── puml/
    │   ├── step20_md/
    │   ├── step40_pdf/
    │   └── PUBLISH/

La classe PipelineContext contiene tutti i riferimenti ai percorsi
utilizzati durante le varie fasi di elaborazione, evitando la costruzione
ripetuta di path nel resto del codice.

Directory principali gestite:

- src:
  contiene i file Markdown sorgenti;

- imgs:
  contiene immagini statiche locali già presenti nel progetto;

- puml:
  contiene i file sorgente PlantUML estratti dal Markdown;

- step20_md:
  contiene file Markdown intermedi e risorse generate;

- imgs_downloaded:
  contiene immagini remote scaricate localmente;

- imgs_puml:
  contiene immagini generate da diagrammi PlantUML;

- step40_pdf:
  contiene i PDF intermedi o finali generati;

- PUBLISH:
  contiene gli artefatti finali pronti per distribuzione o pubblicazione.

Funzioni principali:

- find_workspace_root():
  ricerca automaticamente la root del workspace individuando la directory
  005_authoring;

- build_pipeline_context():
  costruisce un oggetto PipelineContext validando la posizione del file
  sorgente Markdown;

- ensure_pipeline_dirs():
  crea automaticamente tutte le directory operative mancanti.

Il modulo non esegue direttamente conversioni Markdown, rendering PDF o
generazione PlantUML: fornisce esclusivamente il contesto condiviso e la
preparazione dell'ambiente filesystem necessario alla pipeline.
"""

from __future__ import annotations


import os
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

    resolved_plantuml_jar = plantuml_jar

    if resolved_plantuml_jar is None:
        env_plantuml_jar = os.environ.get("PLANTUML_JAR")
        if env_plantuml_jar:
            resolved_plantuml_jar = Path(env_plantuml_jar).expanduser().resolve()

    if resolved_plantuml_jar is None:
        default_plantuml_jar = authoring_dir / "tools" / "plantuml.jar"
        if default_plantuml_jar.exists():
            resolved_plantuml_jar = default_plantuml_jar

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
        plantuml_jar=resolved_plantuml_jar,
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
