# md_processor modulare

Pipeline:

- `src/` contiene i Markdown sorgenti.
- `imgs/` contiene immagini locali normalizzate.
- `step20_md/imgs_downloaded/` contiene immagini remote scaricate.
- `step20_md/imgs_puml/` contiene immagini generate da PlantUML.
- `puml/` contiene i file PlantUML estratti.
- `step20_md/` contiene il Markdown preprocessato.

- `step40_pdf/` contiene il PDF normale generato da Pandoc.
- `PUBLISH/` contiene il PDF rasterizzato pubblicabile.

File principali:

- `md_processor.py`: entry point CLI.
- `md_pipeline_context.py`: contesto della pipeline e directory.
- `md_pipeline_input.py`: raccolta input.
- `md_processor_step20.py`: preprocessing Markdown, PlantUML, immagini.
- `md_processor_step40.py`: generazione PDF Pandoc.
- `md_processor_step90.py`: rasterizzazione PDF.
- `md_pipeline_logging.py`: logging console/file.
- `md_pipeline_confirm.py`: conferme.
- `md_pipeline_utils.py`: funzioni di utilità.

Esempio launch.json:

    {
        "name": "-> .md loc. Py modulare",
        "type": "debugpy",
        "request": "launch",
        "program": "${workspaceFolder}/005_authoring/python/md_processor.py",
        "console": "integratedTerminal",
        "args": [
            "--yes",
            "--verbose",
            "--pdf-engine",
            "xelatex",
            "${file}"
        ],
        "cwd": "${workspaceFolder}"
    }

Il programma cerca automaticamente:

    ${workspaceFolder}/005_authoring/latex/header1.tex

e lo passa a Pandoc se esiste e se non è già stato passato manualmente un header.

Per PlantUML usare una delle due opzioni:

    --plantuml-jar
    C:\path\plantuml.jar

oppure impostare la variabile ambiente:

    PLANTUML_JAR

Nota importante:

La versione compatta normalizza immagini Markdown standard e blocchi PlantUML.
I tag HTML `<img>` possono essere aggiunti in uno step successivo, mantenendo la stessa architettura.
