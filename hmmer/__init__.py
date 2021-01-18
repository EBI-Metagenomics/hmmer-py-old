from importlib import import_module as _import_module

from . import typing
from ._example import example_filepath
from ._testit import test
from .bin import binary_version
from .domtbl import read_domtbl
from .hmmer import HMMER, SeqDB
from .tbl import read_tbl

try:
    __version__ = getattr(_import_module("hmmer._version"), "version", "x.x.x")
except ModuleNotFoundError:
    __version__ = "x.x.x"

__all__ = [
    "HMMER",
    "SeqDB",
    "__version__",
    "example_filepath",
    "binary_version",
    "read_domtbl",
    "read_tbl",
    "test",
    "typing",
]
