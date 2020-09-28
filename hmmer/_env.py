import os
from pathlib import Path

from appdirs import user_cache_dir

__all__ = ["HMMER_CACHE_HOME"]

HMMER_CACHE_HOME = Path(
    os.environ.get(
        "HMMER_CACHE_HOME",
        default=Path(user_cache_dir("hmmer-py", "EBI-Metagenomics")),
    )
)


HMMER_CACHE_HOME.mkdir(parents=True, exist_ok=True)
(HMMER_CACHE_HOME / "test_data").mkdir(parents=True, exist_ok=True)
