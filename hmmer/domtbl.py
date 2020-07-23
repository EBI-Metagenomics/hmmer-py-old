from __future__ import annotations

from pathlib import Path
from typing import IO, Iterator, NamedTuple, Union

from ._misc import decomment

__all__ = [
    "DomTBLCoord",
    "DomTBLData",
    "DomTBLDomScore",
    "DomTBLIndex",
    "DomTBLRow",
    "DomTBLSeqScore",
]


def read_domtbl(file: Union[str, Path, IO[str]]) -> DomTBLData:
    """
    Read domtbl file type.

    Parameters
    ----------
    file
        File path or file stream.
    """
    return DomTBLData(file)


DomTBLIndex = NamedTuple(
    "DomTBLIndex", [("name", str), ("accession", str), ("length", int)]
)

DomTBLSeqScore = NamedTuple(
    "DomTBLSeqScore", [("e_value", str), ("score", str), ("bias", str)]
)

DomTBLDomScore = NamedTuple(
    "DomTBLDomScore",
    [
        ("id", int),
        ("size", int),
        ("c_value", str),
        ("i_value", str),
        ("score", str),
        ("bias", str),
    ],
)

DomTBLCoord = NamedTuple("DomTBLCoord", [("start", int), ("stop", int)])

DomTBLRow = NamedTuple(
    "DomTBLRow",
    [
        ("target", DomTBLIndex),
        ("query", DomTBLIndex),
        ("full_sequence", DomTBLSeqScore),
        ("domain", DomTBLDomScore),
        ("hmm_coord", DomTBLCoord),
        ("ali_coord", DomTBLCoord),
        ("env_coord", DomTBLCoord),
        ("acc", str),
        ("description", str),
    ],
)


class DomTBLData:
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

    def __iter__(self) -> Iterator[DomTBLRow]:
        for line in self._reader:
            yield DomTBLRow(
                DomTBLIndex(line[0], line[1], int(line[2])),
                DomTBLIndex(line[3], line[4], int(line[5])),
                DomTBLSeqScore(*line[6:9]),
                DomTBLDomScore(int(line[9]), int(line[10]), *line[11:15]),
                DomTBLCoord(int(line[15]), int(line[16])),
                DomTBLCoord(int(line[17]), int(line[18])),
                DomTBLCoord(int(line[19]), int(line[20])),
                line[21],
                " ".join(line[22:]),
            )

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()
