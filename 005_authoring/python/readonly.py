#!/usr/bin/env python3
"""
Genera versioni protette (senza copia/incolla) dei PDF presenti nelle cartelle out/
dei documenti riconosciuti come cartelle contenenti una sottocartella src/.
"""

import argparse
import logging
import sys
from pathlib import Path

import pymupdf  # PyMuPDF


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def find_documents(root: Path):
    """Genera il percorso della directory radice di ogni documento contenente src/."""
    for src_dir in root.rglob("src"):
        if src_dir.is_dir():
            yield src_dir.parent


def rasterize_pdf(input_pdf: Path, output_pdf: Path, dpi: int = 150, force: bool = False):
    """
    Converte ogni pagina del PDF in immagine e crea un nuovo PDF rasterizzato.
    Il testo non sarà selezionabile né copiabile.
    """
    input_pdf = input_pdf.resolve()
    output_pdf = output_pdf.resolve()

    if output_pdf.exists():
        if force:
            logger.info(f"Sovrascrivo: {output_pdf}")
        else:
            logger.warning(f"File già esistente: {output_pdf} - usare --force per sovrascrivere")
            return False

    logger.info(f"Input : {input_pdf}")
    logger.info(f"Output: {output_pdf}")
    logger.info(f"DPI   : {dpi}")

    doc = None
    out_doc = None

    try:
        doc = pymupdf.open(input_pdf)
        out_doc = pymupdf.open()

        zoom = dpi / 72.0
        mat = pymupdf.Matrix(zoom, zoom)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=mat, alpha=False)

            width_pt = pix.width / zoom
            height_pt = pix.height / zoom

            new_page = out_doc.new_page(width=width_pt, height=height_pt)
            new_page.insert_image(new_page.rect, pixmap=pix)

        out_doc.save(output_pdf, garbage=4, deflate=True, clean=True)

        logger.info(f"Creato: {output_pdf}")
        return True

    except Exception as e:
        logger.error(f"Errore durante l'elaborazione di {input_pdf}: {e}")
        return False

    finally:
        if out_doc is not None:
            out_doc.close()
        if doc is not None:
            doc.close()


def process_document(doc_root: Path, dpi: int, force: bool):
    out_dir = doc_root / "out"

    if not out_dir.is_dir():
        logger.debug(f"Nessuna cartella out/ in: {doc_root.resolve()}")
        return 0

    pdf_files = list(out_dir.glob("*.pdf"))

    if not pdf_files:
        logger.debug(f"Nessun PDF in: {out_dir.resolve()}")
        return 0

    count = 0

    for pdf_file in pdf_files:
        if pdf_file.stem.endswith("_ro"):
            logger.debug(f"Salto file già rasterizzato: {pdf_file.resolve()}")
            continue

        output_pdf = pdf_file.with_name(pdf_file.stem + "_ro" + pdf_file.suffix)

        if rasterize_pdf(pdf_file, output_pdf, dpi=dpi, force=force):
            count += 1

    if count == 0:
        logger.debug(f"Nessun PDF generato in: {out_dir.resolve()}")

    return count


def main():
    parser = argparse.ArgumentParser(
        description="Trova documenti con src/ e genera PDF rasterizzati _ro nelle relative cartelle out/."
    )

    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Directory radice da cui iniziare la scansione"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="Risoluzione per la rasterizzazione"
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

    if not root_path.exists():
        logger.error(f"Directory non trovata: {root_path}")
        return 1

    logger.info(f"Directory di partenza: {root_path}")

    documents = list(find_documents(root_path))

    if not documents:
        logger.warning(f"Nessun documento con cartella src/ trovato in: {root_path}")
        return 0

    logger.info(f"Trovati {len(documents)} documento/i")

    total_created = 0

    for doc_root in documents:
        logger.debug(f"Documento: {doc_root.resolve()}")
        total_created += process_document(doc_root, dpi=args.dpi, force=args.force)

    logger.info(f"PDF generati: {total_created}")

    return 0


if __name__ == "__main__":
    sys.exit(main())