from io import StringIO

import pytest

from hmmer import read_domtbl, read_tbl

_tbl_content = """#                                                               --- full sequence ---- --- best 1 domain ---- --- domain number estimation ----
# target name        accession  query name           accession    E-value  score  bias   E-value  score  bias   exp reg clu  ov env dom rep inc description of target
#------------------- ---------- -------------------- ---------- --------- ------ ----- --------- ------ -----   --- --- --- --- --- --- --- --- ---------------------
item2                -          Octapeptide          PF03373.14   1.2e-07   19.5   3.5   1.2e-07   19.5   3.5   1.0   1   0   0   1   1   1   1 Description one two three
item3                -          Octapeptide          PF03373.14   1.2e-07   19.5   3.5   1.2e-07   19.5   3.5   1.0   1   0   0   1   1   1   1 -
#
# Program:         hmmsearch
# Version:         3.2.1 (June 2018)
# Pipeline mode:   SEARCH
# Query file:      tmp/database.hmm
# Target file:     tmp/amino.fasta
# Option settings: hmmsearch -A tmp/db_hits --tblout tmp/db_tblout tmp/database.hmm tmp/amino.fasta
# Current dir:     /Users/horta/code/nmm-py
# Date:            Fri Jan 10 12:41:26 2020
# [ok]
"""

_domtbl_content = """#                                                                                   --- full sequence --- -------------- this domain -------------   hmm coord   ali coord   env coord
# target name        accession   tlen query name                  accession   qlen   E-value  score  bias   #  of  c-Evalue  i-Evalue  score  bias  from    to  from    to  from    to  acc description of target
#------------------- ---------- -----        -------------------- ---------- ----- --------- ------ ----- --- --- --------- --------- ------ ----- ----- ----- ----- ----- ----- ----- ---- ---------------------
Leader_Thr           PF08254.12    22 AE014075.1:190-252|amino|11 -             21   5.3e-10   38.8  17.5   1   1     3e-14   5.5e-10   38.8  17.5     1    22     1    21     1    21 0.99 Threonine leader peptide
Y1_Tnp               PF01797.17   121 AE014075.1:534-908|amino|11 -            125   8.3e-25   87.2   0.0   1   1     5e-29   9.2e-25   87.1   0.0    19   121     2   102     1   102 0.94 Transposase IS200 like
Homoserine_dh        PF00742.20   173 AE014075.1:985-3507|amino|11 -            841   1.5e-49  168.2   0.0   1   1     2e-52   7.3e-49  166.0   0.0     1   173   635   832   635   832 0.92 Homoserine dehydrogenase
AA_kinase            PF00696.29   241 AE014075.1:985-3507|amino|11 -            841   1.9e-46  158.7   0.3   1   1   1.6e-49   5.7e-46  157.1   0.1     3   241    23   305    21   305 0.87 Amino acid kinase family
NAD_binding_3        PF03447.17   117 AE014075.1:985-3507|amino|11 -            841   5.9e-34  117.3   0.0   1   1   4.6e-37   1.7e-33  115.8   0.0     1   116   493   626   493   627 0.97 Homoserine dehydrogenase, NAD binding domain
ACT_7                PF13840.7     65 AE014075.1:985-3507|amino|11 -            841   4.5e-19   68.0   1.3   1   2   4.7e-11   1.7e-07   30.9   0.0     5    63   335   395   333   397 0.90 ACT domain
ACT_7                PF13840.7     65 AE014075.1:985-3507|amino|11 -            841   4.5e-19   68.0   1.3   2   2     2e-12   7.2e-09   35.3   0.3     3    61   414   474   412   478 0.92 ACT domain
ACT                  PF01842.26    67 AE014075.1:985-3507|amino|11 -            841   1.8e-17   62.8   0.3   1   2   2.3e-11   8.2e-08   31.9   0.0     6    61   345   397   341   402 0.91 ACT domain
#
# Program:         hmmscan
# Version:         3.3 (Nov 2019)
# Pipeline mode:   SCAN
# Query file:      AE014075.1_amino.fasta
# Target file:     Pfam-A.hmm
# Option settings: hmmscan --domtblout domtblout.txt --cut_ga Pfam-A.hmm AE014075.1_amino.fasta
# Current dir:     /Users/horta/code/iseq/scripts
# Date:            Wed Jul  8 17:21:50 2020
# [ok]
"""


def test_tbl():
    tbl = iter(read_tbl(StringIO(_tbl_content)))
    row = next(tbl)

    assert row.target.name == "item2"
    assert row.target.accession == "-"
    assert row.query.name == "Octapeptide"
    assert row.query.accession == "PF03373.14"
    assert row.full_sequence.e_value == "1.2e-07"
    assert row.full_sequence.score == "19.5"
    assert row.full_sequence.bias == "3.5"
    assert row.best_1_domain.e_value == "1.2e-07"
    assert row.best_1_domain.score == "19.5"
    assert row.best_1_domain.bias == "3.5"
    assert row.domain_numbers.exp == "1.0"
    assert row.domain_numbers.reg == 1
    assert row.domain_numbers.clu == 0
    assert row.domain_numbers.ov == 0
    assert row.domain_numbers.env == 1
    assert row.domain_numbers.dom == 1
    assert row.domain_numbers.rep == 1
    assert row.domain_numbers.inc == 1
    assert row.description == "Description one two three"

    row = next(tbl)

    assert row.target.name == "item3"
    assert row.target.accession == "-"
    assert row.query.name == "Octapeptide"
    assert row.query.accession == "PF03373.14"
    assert row.full_sequence.e_value == "1.2e-07"
    assert row.full_sequence.score == "19.5"
    assert row.full_sequence.bias == "3.5"
    assert row.best_1_domain.e_value == "1.2e-07"
    assert row.best_1_domain.score == "19.5"
    assert row.best_1_domain.bias == "3.5"
    assert row.domain_numbers.exp == "1.0"
    assert row.domain_numbers.reg == 1
    assert row.domain_numbers.clu == 0
    assert row.domain_numbers.ov == 0
    assert row.domain_numbers.env == 1
    assert row.domain_numbers.dom == 1
    assert row.domain_numbers.rep == 1
    assert row.domain_numbers.inc == 1
    assert row.description == "-"

    with pytest.raises(StopIteration):
        next(tbl)


def test_domtbl():
    tbl = iter(read_domtbl(StringIO(_domtbl_content)))
    row = next(tbl)

    assert row.target.name == "Leader_Thr"
    assert row.target.accession == "PF08254.12"
    assert row.target.length == 22
    assert row.query.name == "AE014075.1:190-252|amino|11"
    assert row.query.accession == "-"
    assert row.query.length == 21
    assert row.full_sequence.e_value == "5.3e-10"
    assert row.full_sequence.score == "38.8"
    assert row.full_sequence.bias == "17.5"
    assert row.domain.id == 1
    assert row.domain.size == 1
    assert row.domain.c_value == "3e-14"
    assert row.domain.i_value == "5.5e-10"
    assert row.domain.score == "38.8"
    assert row.domain.bias == "17.5"
    assert row.hmm_coord.start == 1
    assert row.hmm_coord.stop == 22
    assert row.ali_coord.start == 1
    assert row.ali_coord.stop == 21
    assert row.env_coord.start == 1
    assert row.env_coord.stop == 21
    assert row.acc == "0.99"
    assert row.description == "Threonine leader peptide"

    row = next(tbl)
    assert row.target.name == "Y1_Tnp"

    assert len(list(read_domtbl(StringIO(_domtbl_content)))) == 8
