import hashlib

from hmmer import HMMER, example_filepath


def test_fetch():
    hmmfile = example_filepath("Pfam-A_24.hmm")
    hmm = HMMER(hmmfile)
    profiles = hmm.fetch(["PF01797.17", "PF03447.17"])

    hex = hashlib.sha256(profiles.encode()).hexdigest()
    assert hex == "ed84c32ad2714564960bf7393edd1d2e2937c1451a89d04d83760a6fb7eda833"
