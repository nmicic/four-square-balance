# Power-Balance Record Locations, p = 7 (Four Seventh Powers)

**Status: exploratory, archived. Not an OEIS submission.**

This folder documents the p = 7 member of the power-balance family: the analogue,
for sums of four seventh powers, of the four-square balance-gap record locations
[A396760](https://oeis.org/A396760) (the p = 2 case, the active sequence of this
repository). It is retained for reference and reproducibility. If you use or
extend these terms, please reference this repository.

## Definition

For a representable integer N, write

    N = a^7 + b^7 + c^7 + d^7,   0 <= a <= b <= c <= d  (integers).

Let minmax(N) be the least possible largest part d over all such representations,
and let lb(N) be the least integer m with 4*m^7 >= N. The balance gap is

    g(N) = minmax(N) - lb(N).

a(n) is the n-th representable N, taken in increasing order, at which g(N) exceeds
all earlier values. Unlike p = 2 (Lagrange), for p >= 3 not every integer is a sum
of four p-th powers; records are taken over the representable N only.

## Terms

    1, 279936, 35831808

These 3 terms are complete for N <= 40000000 (exhaustive scan); nothing is asserted
beyond that bound. The corresponding record gaps are 0, 1, 2. Within the scanned
range every record location beyond 1 is itself a seventh power:

    279936 = 6^7, 35831808 = 12^7.

This is an observation about the scanned range only.

## Files

- `b-file.txt` — the 3 verified terms, offset 1.
- `program.gp` — PARI/GP scanner: `lista(Nmax)` prints every record location <= Nmax.
- `../../exploratory-src/balance_records.py` — reference computation for the whole
  p = 2..7 family.
- `../../../viz/power-balance/` — interactive visualization of the family.
