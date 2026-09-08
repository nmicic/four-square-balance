# four-square-balance

This repository documents the **gap-record locations** for the
canonical four-square balance gap, published as OEIS [A396760](https://oeis.org/A396760).

[Open the interactive visualization](https://nmicic.github.io/four-square-balance/viz/index.html).

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
- `data/gap_table_1_20000.csv` — dense per-n companion table showing the
  canonical decomposition, gap, running gap record, and contextual spread for
  n = 1..20000.

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
- `src/gap_table.py` — generator for the dense per-n companion CSV
  `data/gap_table_1_20000.csv`.

Build and run the C checks:

    cd src
    make
    make check

On macOS, Apple clang may not support OpenMP by default. With Homebrew GCC, use:

    make CC=gcc-15 check

Run the PARI/GP record self-test:

    gp -q src/records.gp

## Visualization

`viz/index.html` visualizes the canonical four-square shapes in Helmert
shape-space, colored by balance gap, with the verified gap-record rays
highlighted:

[https://nmicic.github.io/four-square-balance/viz/index.html](https://nmicic.github.io/four-square-balance/viz/index.html)

See `viz/README.md`.

## Related Power-Balance Sequences

A396760 is the p = 2 member of a family using sums of four p-th powers.
The p = 3..7 members are exploratory and are not in the OEIS. Each has its
own terms, scan bound, and program.

For each exponent p, take the least possible largest root d over all
representations `n = a^p+b^p+c^p+d^p` with nonnegative integer roots. The gap
is d minus the least integer m with `4*m^p >= n`. The sequence lists the n
where this gap exceeds every earlier gap. For p >= 3, only representable
positive integers are considered.

| Exponent | Sequence | Scan bound | Records in that range |
| ---: | --- | ---: | ---: |
| 2 | [Four squares: A396760](sequences/gap-record-locations/README.md) | n < 10^9 | 37 |
| 3 | [Four cubes](archive/exploratory-sequences/power-balance-p3/README.md) | n <= 300000 | 25 |
| 4 | [Four fourth powers](archive/exploratory-sequences/power-balance-p4/README.md) | n <= 500000 | 8 |
| 5 | [Four fifth powers](archive/exploratory-sequences/power-balance-p5/README.md) | n <= 800000 | 4 |
| 6 | [Four sixth powers](archive/exploratory-sequences/power-balance-p6/README.md) | n <= 9000000 | 3 |
| 7 | [Four seventh powers](archive/exploratory-sequences/power-balance-p7/README.md) | n <= 40000000 | 3 |

[Explore all six sequences in the family viewer](https://nmicic.github.io/four-square-balance/viz/power-balance/balance.html).

## Extra Observations

[extra-observations/EXTRA_OBSERVATIONS.md](extra-observations/EXTRA_OBSERVATIONS.md)
lists all six sequences at the viewer bounds and gives short proofs for the
p = 2 member: the 96 and 2816 cores share one projected direction, the
canonical tuple doubles for even n, and the record sequence is infinite. It
also restates Legendre's three-square condition in `(v2(n), u)` form. The
bounded checks are reproduced by a standard-library Python script:

    python3 extra-observations/verify_observations.py
    python3 extra-observations/verify_observations.py --full

## Archive

`archive/` holds the p = 3..7 data and programs, and other exploratory
companion sequences and code. The family table above links to each
higher-power member. Only the p = 2 sequence is in the OEIS.

## License

Apache-2.0. See `LICENSE`.
