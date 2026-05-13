from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path


def sanitize_name(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_") or "item"


def sha1_short(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


def relative_posix_path(path: Path, start: Path) -> str:
    return os.path.relpath(path, start).replace("\\", "/")


def line_number_from_index(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def write_text_file_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8", newline="\n")
    return True
