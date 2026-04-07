#!/usr/bin/env python3
"""
Genera versioni protette (senza copia/incolla) di file PDF presenti in directory out/
per ogni documento riconosciuto (cartella contenente una sottocartella src/).
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


def rasterize_pdf(input_pdf: Path, output_pdf: Path, dpi: int = 150, force: bool = False):
    """
    Converte ogni pagina del PDF in un'immagine (rasterizzazione) e crea un nuovo PDF
    contenente solo immagini. Il testo non sarà selezionabile né copiabile.
    """
    if output_pdf.exists():
        if force:
            logger.info(f"Sovrascrivo {output_pdf} (forzato)")
        else:
            logger.warning(f"File _ro già esistente: {output_pdf} (usa --force per sovrascrivere)")
            return

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
    except Exception as e:
        logger.error(f"Errore durante l'elaborazione di {input_pdf}: {e}")


def process_document(doc_root: Path, dpi: int, force: bool):
    out_dir = doc_root / "out"
    if not out_dir.is_dir():
        logger.debug(f"Nessuna cartella out/ in {doc_root}")
        return

    pdf_files = list(out_dir.glob("*.pdf"))
    if not pdf_files:
        logger.debug(f"Nessun file PDF in {out_dir}")
        return

    processed = False
    for pdf_file in pdf_files:
        if "_ro" in pdf_file.stem:
            continue
        output_pdf = pdf_file.with_stem(pdf_file.stem + "_ro")
        rasterize_pdf(pdf_file, output_pdf, dpi=dpi, force=force)
        processed = True

    if not processed:
        logger.debug(f"Nessun PDF da elaborare in {out_dir} (tutti già protetti o assenti)")


def main():
    parser = argparse.ArgumentParser(
        description="Trova documenti (con src/) e genera PDF protetti (_ro) senza testo selezionabile."
    )
    parser.add_argument("root", nargs="?", default=".", help="Directory radice da cui iniziare la scansione (default: corrente)")
    parser.add_argument("--dpi", type=int, default=150, help="Risoluzione per la rasterizzazione (default 150, maggiore = qualità più alta)")
    parser.add_argument("--force", action="store_true", help="Sovrascrive i file _ro già esistenti")
    parser.add_argument("--verbose", action="store_true", help="Mostra output dettagliato")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    root_path = Path(args.root).expanduser().resolve()
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
            logger.debug(f"Documento: {doc}")

    for doc_root in documents:
        process_document(doc_root, dpi=args.dpi, force=args.force)

    return 0


if __name__ == "__main__":
    sys.exit(main())