# Data

This directory contains the evidence files for the gap-record-location sequence.

## records_to_1e9_COMPLETE.txt

The retained exact scan of the balance gap records for k < 10^9.

Columns:

    k gap

The file has 37 record rows after the header comments. The final verified record
below 10^9 is:

    939524096 9250

SHA-256:

    3bbad61d3895e054975635a65c91cc68f7f049f353198d07b26deeda1a25c81c

## record_decompositions_verified.txt

Canonical decompositions for the same 37 verified records.

Columns:

    idx k x y z w g status

where

    k = x^2 + y^2 + z^2 + w^2,
    x >= y >= z >= w >= 0,
    g = x - ceiling(sqrt(k/4)).

Status labels:

- `exhaustive` — covered by the independent exact scan through 10^7.
- `scan-1e9` — covered by the retained exact scan through 10^9.

No row in this file is conjectural.

## a122921_prefix_50.txt

The first 50 terms of A122921. This small fixture is used by `../src/Makefile` to
check that the C engine returns the expected minimal largest part on a fixed
prefix.

SHA-256:

    dc20a553f463cb31f080ece739cf5d8975fad3ca818e507d48c9ea47eea38b36

## sample.csv

A small strided visualization sample: every 100th n from n = 1 to n = 99901
(1000 rows).

Columns:

    n, x, y, z, w, gap, spread

Here `(x, y, z, w)` is the canonical minimal-largest-part decomposition, `gap` is
`x - ceiling(sqrt(n/4))`, and `spread` is `x - w` for this canonical tuple.

SHA-256:

    7fedb5790fe68ba1c1301497a524e5078d0f0938368b40e16bfcbc891b121523

The sample is included only for sanity checks and visualization. It is not needed
to verify the 37-term b-file.
