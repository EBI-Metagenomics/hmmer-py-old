from pathlib import Path as _Path
from sys import platform as _platform

__all__ = [
    "hmmfetch",
    "hmmpress",
    "hmmscan",
    "hmmsearch",
    "hmmemit",
    "phmmer",
    "binary_version",
]

binary_version = "3.3.2"

if _platform not in ["linux", "darwin"]:
    raise RuntimeError(f"Unsupported platform: {_platform}.")

_suffix = "manylinux2010_x86_64"
if _platform == "darwin":
    _suffix = "macosx_10_9_x86_64"


_bin = _Path(__file__).parent.absolute() / f"v{binary_version}"

hmmemit = _bin / f"hmmemit_{_suffix}"
hmmfetch = _bin / f"hmmfetch_{_suffix}"
hmmpress = _bin / f"hmmpress_{_suffix}"
hmmscan = _bin / f"hmmscan_{_suffix}"
hmmsearch = _bin / f"hmmsearch_{_suffix}"
phmmer = _bin / f"phmmer_{_suffix}"
