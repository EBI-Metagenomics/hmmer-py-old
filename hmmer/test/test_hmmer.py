import hashlib

from hmmer import HMMER, example_filepath


def test_fetch():
    hmmfile = example_filepath("Pfam-A_24.hmm")
    hmm = HMMER(hmmfile)
    profiles = hmm.fetch(["PF01797.17", "PF03447.17"])

    hex = hashlib.sha256(profiles.encode()).hexdigest()
    assert hex == "1d869020a903c80da47eec0464b91b3e48aa095996e2f0df44e41e9e0e7bd6aa"
