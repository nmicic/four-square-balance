# Power-Balance Record Locations, p = 3 (Four Cubes)

**Status: exploratory, archived. Not an OEIS submission.**

This folder documents the p = 3 member of the power-balance family: the analogue,
for sums of four cubes, of the four-square balance-gap record locations
[A396760](https://oeis.org/A396760) (the p = 2 case, the active sequence of this
repository). It is retained for reference and reproducibility. If you use or
extend these terms, please reference this repository.

## Definition

For a representable integer N, write

    N = a^3 + b^3 + c^3 + d^3,   0 <= a <= b <= c <= d  (integers).

Let minmax(N) be the least possible largest part d over all such representations,
and let lb(N) be the least integer m with 4*m^3 >= N. The balance gap is

    g(N) = minmax(N) - lb(N).

a(n) is the n-th representable N, taken in increasing order, at which g(N) exceeds
all earlier values. Unlike p = 2 (Lagrange), for p >= 3 not every integer is a sum
of four p-th powers; records are taken over the representable N only.

## Terms

    1, 27, 218, 731, 1331, 2745, 4913, 6862, 10648, 15627, 21954, 27016, 35938,
    46658, 54896, 68956, 85186, 97338, 117650, 140700, 166377, 185195, 216002,
    250050, 274642

These 25 terms are complete for N <= 300000 (exhaustive scan); nothing is asserted
beyond that bound. The corresponding record gaps are 0, 1, 2, ..., 24: within the
scanned range every record raises the gap by exactly 1, unlike p = 2, where the
record gaps jump (0, 1, 2, 3, 4, 6, 9, ...).

## Files

- `b-file.txt` — the 25 verified terms, offset 1.
- `program.gp` — PARI/GP scanner: `lista(Nmax)` prints every record location <= Nmax.
- `../../exploratory-src/balance_records.py` — reference computation for the whole
  p = 2..7 family.
- `../../../viz/power-balance/` — interactive visualization of the family.
