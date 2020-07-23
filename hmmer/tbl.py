import csv
from pathlib import Path
from typing import IO, List, NamedTuple, Union

from ._misc import decomment

__all__ = ["TBLScore", "TBLRow", "TBLIndex", "TBLDom", "read_tbl"]

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


def read_tbl(file: Union[str, Path, IO[str]]) -> List[TBLRow]:
    """
    Read tbl file type.

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
        row = TBLRow(
            TBLIndex(line[0], line[1]),
            TBLIndex(line[2], line[3]),
            TBLScore(*line[4:7]),
            TBLScore(*line[7:10]),
            TBLDom(line[10], *[int(i) for i in line[11:18]]),
            " ".join(line[18:]),
        )
        rows.append(row)

    if closeit:
        file.close()

    return rows
