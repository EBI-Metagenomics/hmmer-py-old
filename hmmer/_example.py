import logging
from pathlib import Path

import pooch

from ._env import HMMER_CACHE_HOME

__all__ = ["example_filepath"]

pooch.get_logger().setLevel(logging.ERROR)

goodboy = pooch.create(
    path=HMMER_CACHE_HOME / "test_data",
    base_url="https://hmmer-py.s3.eu-west-2.amazonaws.com/",
    registry={
        "Pfam-A_24.hmm.gz": "32791a1b50837cbe1fca1376a3e1c45bc84b32dd4fe28c92fd276f3f2c3a15e3",
    },
)


def example_filepath(filename: str) -> Path:
    return Path(goodboy.fetch(filename + ".gz", processor=pooch.Decompress()))
