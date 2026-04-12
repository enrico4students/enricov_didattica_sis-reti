import os
from pathlib import Path
from PIL import Image

ROOT = Path("./").resolve()

IMAGE_EXTENSIONS = {
    ".png",
    ".bmp",
    ".tiff",
    ".tif",
    ".webp",
    ".gif"
}

marker = "_jpg_generated"


def convert_image(path):

    ext = path.suffix.lower()

    # ignorare file non immagine
    if ext not in IMAGE_EXTENSIONS:
        return

    base_name = path.stem
    parent = path.parent

    jpg_path = parent / f"{base_name}.jpg"

    # evitare sovrascrittura
    if jpg_path.exists():
        print("skip jpg already exists:", jpg_path)
        return

    if marker in base_name:
        print("skip already converted:", path)
        return

    try:

        with Image.open(path) as img:

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.save(jpg_path, "JPEG", quality=95)

        # rinominare file originale
        new_original = parent / f"{base_name}{marker}{ext}"

        path.rename(new_original)

        print("converted:", path, "->", jpg_path)

    except Exception as e:
        print("error:", path, e)


def scan_tree():

    for root, dirs, files in os.walk(ROOT):

        for name in files:

            # skip authoring dir
            if "auth" in root:
                continue
            if "copyright" in name.lower():
                continue    

            path = Path(root) / name

            convert_image(path)


if __name__ == "__main__":

    print("Scanning:", ROOT)

    scan_tree()

    print("done")