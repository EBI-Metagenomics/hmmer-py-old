import tempfile
from enum import Enum
from io import StringIO
from pathlib import Path
from subprocess import PIPE, Popen, check_call, check_output
from typing import List, Optional, TextIO, Union

from fasta_reader import FASTAItem, FASTAParser

from ._misc import make_path
from .bin import hmmemit, hmmfetch, hmmpress, hmmscan, hmmsearch
from .domtbl import DomTBLRow, read_domtbl
from .tbl import TBLRow, read_tbl

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
            self._tbl = read_tbl(tbl)

        if domtbl is None:
            self._domtbl = None
        else:
            self._domtbl = read_domtbl(domtbl)

    @property
    def has_tbl(self) -> bool:
        return self._tbl is not None

    @property
    def has_domtbl(self) -> bool:
        return self._domtbl is not None

    @property
    def tbl(self) -> List[TBLRow]:
        assert self._tbl is not None
        return self._tbl

    @property
    def domtbl(self) -> List[DomTBLRow]:
        assert self._domtbl is not None
        return self._domtbl


def _optional_filepath(
    filepath_or_bool: Union[Path, str, bool], tmp_filepath: Path
) -> Optional[Path]:

    if isinstance(filepath_or_bool, str):
        filepath_or_bool = Path(filepath_or_bool)

    opt_filepath: Optional[Path] = None
    if isinstance(filepath_or_bool, bool):
        if filepath_or_bool:
            opt_filepath = tmp_filepath
    else:
        opt_filepath = filepath_or_bool

    return opt_filepath


class Options:
    def __init__(
        self,
        output: Optional[Union[Path, str]],
        tblout: Optional[Path],
        domtblout: Optional[Path],
        heuristic: bool,
        cut_ga: bool,
        hmmkey: Optional[str],
        Z: Optional[int],
    ):
        self._options = []

        if output is not None:
            self._options += ["-o", str(output)]

        if tblout is not None:
            self._options += ["--tblout", str(tblout)]

        if domtblout is not None:
            self._options += ["--domtblout", str(domtblout)]

        if not heuristic:
            self._options += ["--max"]

        if cut_ga:
            self._options += ["--cut_ga"]

        if Z:
            self._options += ["-Z", str(Z)]

        self._tblout = tblout
        self._domtblout = domtblout
        self._hmmkey = hmmkey

    def aslist(self):
        return self._options

    @property
    def tblout(self):
        return self._tblout

    @property
    def domtblout(self):
        return self._domtblout

    @property
    def has_hmmkey(self) -> bool:
        return self._hmmkey is not None

    @property
    def hmmkey(self) -> str:
        assert isinstance(self._hmmkey, str)
        return self._hmmkey


def make_target(target: Union[Path, str, TextIO], tmpdir: Path) -> Path:
    if isinstance(target, str):
        target = Path(target)

    if isinstance(target, Path):
        return target

    with open(tmpdir / "target.fasta", "w") as file:
        file.write(target.read())

    return tmpdir / "target.fasta"


class HMMER:
    def __init__(self, profile: Union[Path, str]):
        self._profile = make_path(profile).absolute()
        self._indexed = State.UNKNOWN
        self._timeout = 15

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: int):
        self._timeout = timeout

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

    def emit(self, hmmkey: str, nsamples=1, consensus=False, seed=0) -> List[FASTAItem]:
        options = []
        if consensus:
            options.append("-c")
        if nsamples != 1:
            options += ["-N", str(nsamples)]
        if seed != 0:
            options += ["-seed", str(seed)]

        flags = " ".join(options)
        cmd = f"{hmmfetch} {self._profile} {hmmkey} | {hmmemit} {flags} -"
        output = check_output(cmd, shell=True, text=True)
        return FASTAParser(StringIO(output)).read_items()

    def scan(
        self,
        target: Union[Path, str, TextIO],
        output: Optional[Union[Path, str]] = None,
        tblout: Union[Path, str, bool] = True,
        domtblout: Union[Path, str, bool] = True,
        heuristic=True,
        cut_ga=False,
        hmmkey: Optional[str] = None,
        Z: Optional[int] = None,
    ) -> Result:

        with tempfile.TemporaryDirectory() as tmpdir:
            tbl_file = _optional_filepath(tblout, Path(tmpdir) / "tbl.txt")
            domtbl_file = _optional_filepath(domtblout, Path(tmpdir) / "domtbl.txt")

            opts = Options(output, tbl_file, domtbl_file, heuristic, cut_ga, hmmkey, Z)
            target = make_target(target, Path(tmpdir))
            return self._match(hmmscan, target, opts)

    def search(
        self,
        target: Union[Path, str, TextIO],
        output: Optional[Union[Path, str]] = None,
        tblout: Union[Path, str, bool] = True,
        domtblout: Union[Path, str, bool] = True,
        heuristic=True,
        cut_ga=False,
        hmmkey: Optional[str] = None,
        Z: Optional[int] = None,
    ) -> Result:

        with tempfile.TemporaryDirectory() as tmpdir:
            tbl_file = _optional_filepath(tblout, Path(tmpdir) / "tbl.txt")
            domtbl_file = _optional_filepath(domtblout, Path(tmpdir) / "domtbl.txt")

            opts = Options(output, tbl_file, domtbl_file, heuristic, cut_ga, hmmkey, Z)
            target = make_target(target, Path(tmpdir))
            return self._match(hmmsearch, target, opts)

    def _match(self, bin: Path, target: Path, options: Options) -> Result:
        target = target.absolute()

        cmd_match = [str(bin)] + options.aslist()

        if options.has_hmmkey:

            cmd_fetch = [str(hmmfetch), str(self._profile), options.hmmkey]
            with Popen(cmd_fetch, stdout=PIPE) as pfetch:
                cmd_match += ["-", str(target)]
                with Popen(cmd_match, stdin=pfetch.stdout) as pmatch:
                    pmatch.wait(timeout=self._timeout)

        else:
            cmd_match += [str(self._profile), str(target)]
            check_call(cmd_match)

        return Result(options.tblout, options.domtblout)
