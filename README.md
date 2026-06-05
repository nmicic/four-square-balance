# four-square-balance

This repository supports one object: the **gap-record locations** for the
canonical four-square balance gap.

For each positive integer n, write

    n = x^2 + y^2 + z^2 + w^2,   x >= y >= z >= w >= 0.

Let **A(n)** be the least possible largest part x among all such representations.
This is the existing OEIS sequence A122921. The associated lower bound is

    xmin(n) = ceiling(sqrt(n/4)),

since no representation can have all four parts below that value. The balance gap is

    g(n) = A(n) - xmin(n).

The sequence documented here is the list of numbers k where g(k) reaches a new
record value:

    1, 11, 53, 96, 224, 384, 896, 1536, 2816, 3584, ...

Exactly 37 record locations occur for k < 10^9. The last verified record below that
bound is 939524096, with g = 9250.

The sequence is distinct from A006431, the numbers with a unique partition into
four nonnegative squares: two observed chains overlap A006431, but 53 and the
2816*4^m chain do not, and A006431 contains many non-records.

## Main Sequence

- `sequences/gap-record-locations/` — definition, b-file, and a short PARI/GP
  scanner for the record locations.
- `data/records_to_1e9_COMPLETE.txt` — retained exact scan: the 37 record
  locations and their gap values for k < 10^9.
- `data/record_decompositions_verified.txt` — canonical decompositions for those
  37 verified records.

The observed structure is:

    1, 11, 53,
    96*4^m, 224*4^m, 2816*4^m     (m >= 0),

merged in increasing order. This reproduces all 37 verified record locations below
10^9. Beyond that bound it is a conjectural continuation, not a proved
completeness statement.

## Programs

- `src/foursquare.py` — pure-Python reference implementation of A(n) and the
  canonical decomposition.
- `src/foursquare.c` — faster exact C implementation of A(n), used for checks and
  larger scans.
- `src/records.gp` — PARI/GP definitions for the gap records: a direct scanner and
  the observed three-chain construction.
- `src/gen_records.py` — deterministic generator for the observed chain table; it
  marks rows as `exhaustive`, `scan-1e9`, or `chain-conj`.

Build and run the C checks:

    cd src
    make
    make check

On macOS, Apple clang may not support OpenMP by default. With Homebrew GCC, use:

    make CC=gcc-15 check

Run the PARI/GP record self-test:

    gp -q src/records.gp

## Visualization

`viz/index.html` visualizes the canonical four-square shapes, colored by balance
gap, with the verified gap-record rays highlighted. See `viz/README.md`.

When GitHub Pages is enabled, the visualization will be available at:

    https://nmicic.github.io/four-square-balance/viz/index.html

## Archive

`archive/` contains exploratory companion sequences and code that are not part of
the gap-record-location submission. They are kept for reproducibility context, but
the active repository surface is intentionally focused on the single sequence above.

## License

Apache-2.0. See `LICENSE`.
