from __future__ import annotations

from pathlib import Path
from typing import IO, Iterator, NamedTuple, Union

from .misc import decomment

__all__ = ["TBLScore", "TBLRow", "TBLData", "TBLIndex", "TBLDom"]


def read_tbl(file: Union[str, Path, IO[str]]) -> TBLData:
    """
    Read tbl file type.

    Parameters
    ----------
    file
        File path or file stream.
    """
    return TBLData(file)


TBLIndex = NamedTuple("TBLIndex", [("name", str), ("accession", str)])

TBLScore = NamedTuple("TBLScore", [("e_value", str), ("score", str), ("bias", str)])

TBLDom = NamedTuple(
    "TBLDom",
    [
        ("exp", str),
        ("reg", int),
        ("clu", int),
        ("ov", int),
        ("env", int),
        ("dom", int),
        ("rep", int),
        ("inc", int),
    ],
)

TBLRow = NamedTuple(
    "TBLRow",
    [
        ("target", TBLIndex),
        ("query", TBLIndex),
        ("full_sequence", TBLScore),
        ("best_1_domain", TBLScore),
        ("domain_numbers", TBLDom),
        ("description", str),
    ],
)


class TBLData:
    def __init__(self, file: Union[str, Path, IO[str]]):
        import csv

        if isinstance(file, str):
            file = Path(file)

        if isinstance(file, Path):
            file = open(file, "r")

        self._file = file
        self._reader = csv.reader(decomment(file), delimiter=" ", skipinitialspace=True)

    def close(self):
        """
        Close the associated stream.
        """
        self._file.close()

    def __iter__(self) -> Iterator[TBLRow]:
        for line in self._reader:
            yield TBLRow(
                TBLIndex(line[0], line[1]),
                TBLIndex(line[2], line[3]),
                TBLScore(*line[4:7]),
                TBLScore(*line[7:10]),
                TBLDom(line[10], *[int(i) for i in line[11:18]]),
                " ".join(line[18:]),
            )

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()
