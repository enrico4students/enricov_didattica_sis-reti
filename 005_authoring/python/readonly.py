#!/usr/bin/env python3
"""
Genera versioni protette (senza copia/incolla) di file PDF presenti in directory out/
per ogni documento riconosciuto (cartella contenente una sottocartella src/).

Alla fine elenca il full pathname dei file PDF generati.
"""

import argparse
import logging
import sys
from pathlib import Path

import fitz  # PyMuPDF

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def find_documents(root: Path):
    """Genera il percorso della directory radice di ogni documento (con src/)."""
    for src_dir in root.rglob("src"):
        if src_dir.is_dir():
            yield src_dir.parent


def rasterize_pdf(
    input_pdf: Path,
    output_pdf: Path,
    dpi: int = 150,
    force: bool = False
) -> Path | None:
    """
    Converte ogni pagina del PDF in un'immagine raster e crea un nuovo PDF
    contenente solo immagini.

    Restituisce il Path assoluto del file generato, oppure None se non è stato creato.
    """
    input_pdf = input_pdf.resolve()
    output_pdf = output_pdf.resolve()

    if output_pdf.exists():
        if force:
            logger.info(f"Sovrascrivo {output_pdf} (forzato)")
        else:
            logger.warning(
                f"File _ro già esistente: {output_pdf} "
                f"(usa --force per sovrascrivere)"
            )
            return None

    logger.info(f"Generazione {output_pdf} da {input_pdf} (DPI={dpi})")

    try:
        doc = fitz.open(input_pdf)
        out_doc = fitz.open()

        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=mat, alpha=False)

            width_pt = pix.width / zoom
            height_pt = pix.height / zoom

            new_page = out_doc.new_page(width=width_pt, height=height_pt)
            new_page.insert_image(new_page.rect, pixmap=pix)

        out_doc.save(output_pdf, garbage=4, deflate=True, clean=True)
        out_doc.close()
        doc.close()

        logger.info(f"Creato: {output_pdf}")
        return output_pdf

    except Exception as e:
        logger.error(f"Errore durante l'elaborazione di {input_pdf}: {e}")
        return None


def process_document(doc_root: Path, dpi: int, force: bool) -> list[Path]:
    """
    Elabora i PDF nella cartella out/ del documento.

    Restituisce la lista dei PDF _ro generati.
    """
    generated_files: list[Path] = []

    out_dir = doc_root / "out"

    if not out_dir.is_dir():
        logger.debug(f"Nessuna cartella out/ in {doc_root}")
        return generated_files

    pdf_files = list(out_dir.glob("*.pdf"))

    if not pdf_files:
        logger.debug(f"Nessun file PDF in {out_dir}")
        return generated_files

    processed = False

    for pdf_file in pdf_files:
        if "_ro" in pdf_file.stem:
            continue

        output_pdf = pdf_file.with_stem(pdf_file.stem + "_ro")

        generated_pdf = rasterize_pdf(
            pdf_file,
            output_pdf,
            dpi=dpi,
            force=force
        )

        if generated_pdf is not None:
            generated_files.append(generated_pdf)

        processed = True

    if not processed:
        logger.debug(
            f"Nessun PDF da elaborare in {out_dir} "
            f"(tutti già protetti o assenti)"
        )

    return generated_files


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Trova documenti (con src/) e genera PDF protetti (_ro) "
            "senza testo selezionabile."
        )
    )

    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Directory radice da cui iniziare la scansione (default: corrente)"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="Risoluzione per la rasterizzazione (default 150, maggiore = qualità più alta)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Sovrascrive i file _ro già esistenti"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostra output dettagliato"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    root_path = Path(args.root).expanduser().resolve()

    # Percorso fisso attualmente usato.
    # Rimuovere questa riga se si vuole usare il parametro root da riga di comando.
    # root_path = Path(
    #     "C:\\00_data\\08_dev\\08_dev-didattica\\enricov_didattica_sis-reti\\040_5anno\\esercizi_focalizzati"
    # ).resolve()

    if not root_path.exists():
        logger.error(f"Directory {root_path} non trovata")
        return 1

    documents = list(find_documents(root_path))

    if not documents:
        logger.warning(f"Nessun documento (cartella src/) trovato in {root_path}")
        return 0

    logger.info(f"Trovati {len(documents)} documento(i)")

    if args.verbose:
        for doc in documents:
            logger.debug(f"Documento: {doc.resolve()}")

    generated_files: list[Path] = []

    for doc_root in documents:
        generated_files.extend(
            process_document(doc_root, dpi=args.dpi, force=args.force)
        )

    print()
    print("File PDF generati:")
    print("------------------")

    if generated_files:
        for file_path in generated_files:
            print(file_path.resolve())
    else:
        print("Nessun nuovo file generato.")

    return 0


if __name__ == "__main__":
    sys.exit(main())