from pathlib import Path
from typing import Union

__all__ = ["decomment", "make_path"]


def decomment(rows):
    for row in rows:
        if row.startswith("#"):
            continue
        yield row


def make_path(path: Union[Path, str]) -> Path:
    if isinstance(path, str):
        path = Path(path)
    return path
