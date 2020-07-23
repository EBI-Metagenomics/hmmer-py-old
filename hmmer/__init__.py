from . import domtbl, tbl
from ._testit import test
from ._version import __version__
from .domtbl import read_domtbl
from .tbl import read_tbl

__all__ = ["__version__", "test", "tbl", "domtbl", "read_domtbl", "read_tbl"]
