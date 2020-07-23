from enum import Enum
from pathlib import Path
from subprocess import check_call, check_output
from typing import Optional, Union

from ._misc import make_path
from .bin import hmmfetch, hmmpress, hmmscan, hmmsearch
from .domtbl import DomTBLData
from .tbl import TBLData

__all__ = ["HMMER", "Result"]


class State(Enum):
    UNKNOWN = 1
    YES = 2
    NO = 3


class Result:
    def __init__(self, tbl: Optional[Path] = None, domtbl: Optional[Path] = None):
        if tbl is None:
            self._tbl = None
        else:
            self._tbl = TBLData(tbl)

        if domtbl is None:
            self._domtbl = None
        else:
            self._domtbl = DomTBLData(domtbl)

    @property
    def has_tbl(self) -> bool:
        return self._tbl is not None

    @property
    def has_domtbl(self) -> bool:
        return self._domtbl is not None

    @property
    def tbl(self) -> TBLData:
        assert self._tbl is not None
        return self._tbl

    @property
    def domtbl(self) -> DomTBLData:
        assert self._domtbl is not None
        return self._domtbl


class HMMER:
    def __init__(self, profile: Union[Path, str]):
        self._profile = make_path(profile).absolute()
        self._indexed = State.UNKNOWN

    def index(self):
        check_call([str(hmmfetch), "--index", self._profile])

    @property
    def is_indexed(self) -> bool:
        if self._indexed == State.UNKNOWN:
            prof = self._profile
            if prof.with_suffix(prof.suffix + ".ssi").exists():
                self._indexed = State.YES
            elif prof.with_suffix(prof.suffix + ".h3m.ssi").exists():
                self._indexed = State.YES
            else:
                self._indexed = State.NO

        return self._indexed == State.YES

    def fetch_profile(self, key: str) -> str:
        return check_output([str(hmmfetch), str(self._profile), key], text=True)

    def press(self):
        check_call([hmmpress, self._profile])

    @property
    def is_pressed(self) -> bool:
        p = self._profile
        exts = [".h3f", ".h3i", ".h3m", ".h3p"]
        return all([p.with_suffix(p.suffix + ext).exists() for ext in exts])

    def scan(
        self,
        target: Union[Path, str],
        output: Optional[Union[Path, str]] = None,
        tblout: Optional[Union[Path, str]] = None,
        domtblout: Optional[Union[Path, str]] = None,
        heuristic=True,
        cut_ga=False,
    ) -> Result:
        return self._scan_search(
            hmmscan, target, output, tblout, domtblout, heuristic, cut_ga
        )

    def search(
        self,
        target: Union[Path, str],
        output: Optional[Union[Path, str]] = None,
        tblout: Optional[Union[Path, str]] = None,
        domtblout: Optional[Union[Path, str]] = None,
        heuristic=True,
        cut_ga=False,
    ) -> Result:
        return self._scan_search(
            hmmsearch, target, output, tblout, domtblout, heuristic, cut_ga
        )

    def _scan_search(
        self,
        bin: Path,
        target: Union[Path, str],
        output: Optional[Union[Path, str]],
        tblout: Optional[Union[Path, str]],
        domtblout: Optional[Union[Path, str]],
        heuristic: bool,
        cut_ga: bool,
    ) -> Result:
        target = make_path(target).absolute()
        options = []

        if output is not None:
            options += ["-o", str(output)]

        if tblout is not None:
            options += ["--tblout", str(tblout)]

        if domtblout is not None:
            options += ["--domtblout", str(domtblout)]

        if not heuristic:
            options += ["--max"]

        if cut_ga:
            options += ["--cut_ga"]

        check_call([str(bin)] + options + [str(self._profile), str(target)])

        if tblout is not None:
            tblout = make_path(tblout)

        if domtblout is not None:
            domtblout = make_path(domtblout)

        return Result(tblout, domtblout)
