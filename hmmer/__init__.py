from importlib import import_module as _import_module

from . import typing
from ._testit import test
from .domtbl import read_domtbl
from .hmmer import HMMER
from .tbl import read_tbl

try:
    __version__ = getattr(_import_module("hmmer._version"), "version", "x.x.x")
except ModuleNotFoundError:
    __version__ = "x.x.x"

__all__ = ["__version__", "test", "read_domtbl", "read_tbl", "HMMER", "typing"]
