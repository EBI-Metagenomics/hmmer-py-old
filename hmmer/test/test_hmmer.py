import hashlib

from hmmer import HMMER, example_filepath


def test_fetch():
    hmmfile = example_filepath("Pfam-A_24.hmm")
    hmm = HMMER(hmmfile)
    profiles = hmm.fetch(["PF01797.17", "PF03447.17"])

    hex = hashlib.sha256(profiles.encode()).hexdigest()
    assert hex == "f9ac45bb2cea5c0d610a6fe6f3a707246b4cc69926d66f07d67bd1346be06ded"
