# Archive

This directory contains exploratory companion material from the same four-square
balance study. It is **not** part of the gap-record-location submission.

The active submission support files are:

- `../sequences/gap-record-locations/`
- `../data/records_to_1e9_COMPLETE.txt`
- `../data/record_decompositions_verified.txt`
- `../src/foursquare.c`
- `../src/foursquare.py`
- `../src/records.gp`
- `../src/gen_records.py`

Archived sequence folders are retained only so earlier computations remain
inspectable and reproducible.

## Power-balance family (p = 3..7)

`exploratory-sequences/power-balance-p3/` … `power-balance-p7/` document the
analogues of A396760 for sums of four p-th powers, p = 3..7 — same definition
with squares replaced by p-th powers, records taken over the representable N.
One folder per exponent (README.md, b-file.txt, program.gp). They are archived
here for reference and are **not** OEIS submissions; if you use or extend these
terms, please reference this repository.

- `exploratory-src/balance_records.py` — reference computation for the whole
  family p = 2..7 (the p = 2 run reproduces A396760).
- `../viz/power-balance/` — interactive visualization of the family.
