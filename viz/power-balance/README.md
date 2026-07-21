# Power-Balance Visualization (p = 2..7)

Two WebGL viewers that generalize the balance-gap construction of
[A396760](https://oeis.org/A396760) from squares (p = 2) to sums of four p-th
powers, p = 2..7. The p = 2 case is the active sequence of this repository; the
p >= 3 analogues are exploratory and their terms are archived in
`../../archive/exploratory-sequences/power-balance-p3/` … `power-balance-p7/`.

For a representable N = a^p + b^p + c^p + d^p (0 <= a <= b <= c <= d), the
most-balanced representation minimizes the largest part d. The balance gap

    g(N) = minmax(N) - lb(N),   lb(N) = least m with 4*m^p >= N,

measures how far N is forced away from four equal p-th powers; record locations
of g over the representable N form the sequence family shown here.

## Pages

- `index.html` — landing page linking the two viewers.
- `balance.html` — **the family.** Shells across exponents p = 2..7 in four
  synchronized 3-D shadows (one per dropped coordinate), the record holders
  flagged, each shell's constellation of integer points tinted from cool
  (balanced) to warm (forced). The strip along the bottom shows the whole family
  at once, one row per exponent.
- `shape.html` — **the trajectories.** Every representable number in the
  computed range places its most balanced arrangement on the unit shell;
  consecutive numbers join into a wandering line that hovers near the golden
  pole and is yanked toward the corner at the records. The ×2^p control scales the current number: the doubled parts always
  represent the scaled number, but the most-balanced shape usually changes —
  at p = 2 it is known to survive only along the record families
  (96·4^m, 224·4^m, 2816·4^m).

## Notes

- Both viewers load three.js (r128) from a CDN, so they need internet access —
  unlike the dependency-free main viewer `../index.html`.
- The record data for all exponents is computed in the page on load. Each page
  then re-checks its p = 2 records against the A396760 prefix
  (1, 11, 53, 96, 224, 384, 896, 1536, 2816, 3584, 6144) and logs the result to
  the browser console.
- The reference computation for the whole family is
  `../../archive/exploratory-src/balance_records.py`; per-exponent terms, bounds,
  and PARI/GP programs are in `../../archive/exploratory-sequences/`.

Like the main visualization, this is supporting material for the gap-record
sequence; it is not a separate sequence submission. Only the p = 2 case
(A396760) is an OEIS sequence.
