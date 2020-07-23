import csv
from pathlib import Path
from typing import IO, List, NamedTuple, Union

from ._misc import decomment

__all__ = [
    "DomTBLCoord",
    "DomTBLDomScore",
    "DomTBLIndex",
    "DomTBLRow",
    "DomTBLSeqScore",
    "read_domtbl",
]

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


def read_domtbl(file: Union[str, Path, IO[str]]) -> List[DomTBLRow]:
    """
    Read domtbl file type.

    Parameters
    ----------
    file
        File path or file stream.
    """
    closeit = False
    if isinstance(file, str):
        file = Path(file)

    if isinstance(file, Path):
        file = open(file, "r")
        closeit = True

    rows = []
    for line in csv.reader(decomment(file), delimiter=" ", skipinitialspace=True):
        row = DomTBLRow(
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
        rows.append(row)

    if closeit:
        file.close()

    return rows
