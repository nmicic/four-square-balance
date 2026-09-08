#!/usr/bin/env python3
"""Reproduce the bounded checks in EXTRA_OBSERVATIONS.md (standard library only).

    python3 extra-observations/verify_observations.py
    python3 extra-observations/verify_observations.py --full

The default lists all six power sequences and checks seed algebra and
three/four-square representations through 3000.
--full also reconstructs the archived power records, checks the dense four-square
table, and extends the three-square checks through 20000. Paths are relative to this repo;
no network, sibling checkout, generated files, or third-party packages are used.
Failures exit nonzero, including when Python runs with -O.
"""

import argparse
import ast
import csv
from math import isqrt
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SEEDS = (
    ("1", (1, 0, 0, 0), (1, 1, 1, 1)),
    ("11", (3, 1, 1, 0), (5, 3, 3, 1)),
    ("53", (6, 3, 2, 2), (9, 9, 7, 1)),
    ("53 alt", (6, 4, 1, 0), (11, 9, 3, 1)),
    ("96", (2, 1, 1, 0), (4, 2, 2, 0)),
    ("224", (3, 2, 1, 0), (6, 4, 2, 0)),
    ("2816", (5, 3, 3, 1), (10, 6, 6, 2)),
)
# p, complete search bound, positive representable count, record count
FAMILY = (
    (2, 20000, 20000, 13),
    (3, 300000, 193625, 25),
    (4, 500000, 17236, 8),
    (5, 800000, 2806, 4),
    (6, 9000000, 2498, 3),
    (7, 40000000, 1472, 3),
)
VIEWER_BOUNDS = {2: 10000, 3: 300000, 4: 500000, 5: 800000, 6: 9000000, 7: 40000000}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def norm2(q):
    return sum(a * a for a in q)


def qmul(a, b):
    """Hamilton product; the FIRST coordinate is the scalar component."""
    s, x, y, z = a
    t, u, v, w = b
    return (
        s * t - x * u - y * v - z * w,
        s * u + x * t + y * w - z * v,
        s * v - x * w + y * t + z * u,
        s * w + x * v - y * u + z * t,
    )


def canon(q):
    """Sort absolute coordinates; this is not a minimization over a norm shell."""
    return tuple(sorted(map(abs, q), reverse=True))


def helmert_numerators(q):
    """Exact numerators; denominators are sqrt(2), sqrt(6), sqrt(12)."""
    x, y, z, w = q
    return (x - y, x + y - 2 * z, x + y + z - 3 * w)


def lower_bound(n, p):
    """Least integer m with 4*m**p >= n, using integer arithmetic only."""
    lo, hi = 0, 1
    while 4 * hi**p < n:
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if 4 * mid**p >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo


def four_square_tuples(bound):
    """Independent exhaustive enumeration, keeping the least descending tuple."""
    best = {}
    for x in range(isqrt(bound) + 1):
        for y in range(x + 1):
            s2 = x * x + y * y
            if s2 > bound:
                break
            for z in range(y + 1):
                s3 = s2 + z * z
                if s3 > bound:
                    break
                for w in range(z + 1):
                    n = s3 + w * w
                    if n > bound:
                        break
                    q = (x, y, z, w)
                    if n not in best or q < best[n]:
                        best[n] = q
    require(len(best) == bound + 1, "four-square enumeration missed an integer")
    return best


def minimax_by_pairs(p, bound):
    """Minimize the largest root by combining two sums of two p-th powers.

    For each two-power sum s, retain its least possible largest root M(s).
    Combining s and t realizes max(M(s), M(t)). Minimizing that quantity
    for s+t=n is exact: every four-root representation splits into two pairs,
    and replacing either pair by its own minimizer cannot increase the maximum.
    Repeated roots, including zero, are allowed.
    """
    powers = []
    k = 0
    while k**p <= bound:
        powers.append(k**p)
        k += 1

    pair_min = {}
    for a, pa in enumerate(powers):
        for b in range(a, len(powers)):
            s = pa + powers[b]
            if s > bound:
                break
            if b < pair_min.get(s, len(powers)):
                pair_min[s] = b

    pairs = sorted(pair_min.items())
    best = {}
    for i, (s, a) in enumerate(pairs):
        for j in range(i, len(pairs)):
            t, b = pairs[j]
            n = s + t
            if n > bound:
                break
            d = max(a, b)
            if d < best.get(n, len(powers)):
                best[n] = d
    best.pop(0, None)
    return best


def records_from_minima(minima, p):
    records, high = [], -1
    for n, largest in sorted(minima.items()):
        if n == 0:
            continue
        gap = largest - lower_bound(n, p)
        if gap > high:
            records.append((n, gap))
            high = gap
    return records


def read_pairs(path):
    rows = []
    for line in path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split()
        require(len(fields) == 2, f"expected two columns in {path}")
        rows.append(tuple(map(int, fields)))
    require(bool(rows), f"empty data file: {path}")
    return rows


def read_bfile(path):
    rows = read_pairs(path)
    require([i for i, _ in rows] == list(range(1, len(rows) + 1)),
            f"nonconsecutive b-file indices: {path}")
    return [n for _, n in rows]


def retained_records():
    records = read_pairs(ROOT / "data/records_to_1e9_COMPLETE.txt")
    terms = read_bfile(ROOT / "sequences/gap-record-locations/b-file.txt")
    require([n for n, _ in records] == terms, "retained records differ from b-file")
    require(all(a[0] < b[0] and a[1] < b[1]
                for a, b in zip(records, records[1:])),
            "retained record locations and gaps must increase strictly")
    return records


def check_catalogue(retained):
    viewer = (ROOT / "viz/power-balance/balance.html").read_text()
    for name, expected in (("CFGP", VIEWER_BOUNDS), ("PLIST", list(VIEWER_BOUNDS))):
        match = re.search(r"\bconst\s+" + name + r"\s*=\s*([^;]+);", viewer)
        require(match is not None, f"missing viewer configuration {name}")
        require(ast.literal_eval(match.group(1)) == expected,
                f"viewer configuration {name} differs from this catalogue")

    print("All six sequences at balance.html bounds (committed terms; --full recomputes them):")
    for p, _, _, expected_records in FAMILY:
        bound = VIEWER_BOUNDS[p]
        if p == 2:
            terms = [n for n, _ in retained if n <= bound]
            expected_records = 11
        else:
            terms = read_bfile(ROOT / f"archive/exploratory-sequences/power-balance-p{p}/b-file.txt")
        require(len(terms) == expected_records, f"catalogue record count mismatch for p={p}")
        require(all(1 <= n <= bound for n in terms), f"catalogue term outside bound for p={p}")
        require(all(a < b for a, b in zip(terms, terms[1:])),
                f"catalogue terms not increasing for p={p}")
        print(f"  p={p}, n<={bound:,}: " + ", ".join(map(str, terms)))
    print("PASS: all six catalogue prefixes and local viewer configuration")


def two_adic_parts(n):
    require(n > 0, "odd-core decomposition requires a positive integer")
    k = (n & -n).bit_length() - 1
    return k, n >> k


def legendre_allowed(n):
    k, u = two_adic_parts(n)
    return not (k % 2 == 0 and u % 8 == 7)


def three_square_spreads(bound):
    """Enumerate triples independently of the Legendre predicate."""
    best = {}
    for x in range(isqrt(bound) + 1):
        for y in range(x + 1):
            s2 = x * x + y * y
            if s2 > bound:
                break
            for z in range(y + 1):
                n = s2 + z * z
                if n > bound:
                    break
                spread = x - z
                if n not in best or spread < best[n]:
                    best[n] = spread
    best.pop(0, None)
    return best


def check_three_squares(bound):
    best = three_square_spreads(bound)
    for n in range(1, bound + 1):
        k, u = two_adic_parts(n)
        require(n == (1 << k) * u and u % 2 == 1, f"odd-core factorization failed at {n}")
        require((n in best) == legendre_allowed(n), f"Legendre/domain mismatch at {n}")
    checked = 0
    for n, spread in best.items():
        if 4 * n <= bound:
            require(best[4 * n] == 2 * spread, f"three-square spread scaling failed at {n}")
            checked += 1
    for k in range(6):
        n = 7 * 2**k
        require((n in best) == (k % 2 == 1), f"odd-core 7 alternation failed at {n}")
    for n, q in ((14, (3, 2, 1)), (56, (6, 4, 2)), (224, (12, 8, 4))):
        require(norm2(q) == n and best[n] == q[0] - q[-1],
                f"three-square witness or spread failed at {n}")
    prefix, high = [], -1
    for n, spread in sorted(best.items()):
        if n > 1024:
            break
        if spread > high:
            prefix.append(n)
            high = spread
    require(prefix == [1, 4, 10, 16, 37, 58, 64, 130, 148, 232, 256, 445,
                       520, 592, 928, 1024], "displayed A395008 prefix mismatch")
    print(f"PASS: Legendre predicate versus independent triples through {bound:,}; "
          f"{len(best):,} representable, {checked:,} exact spread-scaling checks")
    print("PASS: all 16 displayed A395008 spread-record locations through 1,024")


def check_seed_algebra():
    r = (1, 1, 1, 1)
    print("Seed transformations: first coordinate scalar; T(q) = canon(q*r)")
    for label, q, expected in SEEDS:
        raw = qmul(q, r)
        require(canon(raw) == expected, f"incorrect transform for seed {label}")
        require(norm2(raw) == 4 * norm2(q), f"incorrect norm for seed {label}")
        print(f"  {label:>6}: {q} -> raw {raw} -> {expected}")

    a, b = (2, 1, 1, 0), (5, 3, 3, 1)
    require(tuple(bi - 1 for bi in b) == tuple(2 * ai for ai in a),
            "diagonal-collapse identity failed")
    require(helmert_numerators(r) == (0, 0, 0), "diagonal projection failed")
    require(helmert_numerators(b) == tuple(2 * v for v in helmert_numerators(a)),
            "shared Helmert ray identity failed")
    require(helmert_numerators((3, 2, 1, 0)) == (1, 3, 6),
            "224 core projection failed")
    print("PASS: shared ray, H(5,3,3,1) = 2*H(2,1,1,0)")

    count = 0
    for x in range(31):
        for y in range(x + 1):
            for z in range(y + 1):
                for w in range(z + 1):
                    q = (x, y, z, w)
                    raw = qmul(q, r)
                    fixed = canon(raw) == tuple(2 * v for v in q)
                    require(fixed == (x + w == y + z), f"criterion failed at {q}")
                    require(norm2(raw) == 4 * norm2(q), f"norm failed at {q}")
                    count += 1
    print(f"PASS: fixed-shape criterion and norm identity on {count:,} tuples (max <= 30)")


def check_examples(retained):
    bound = 3000
    best = four_square_tuples(bound)
    expected = {
        1: (1, 0, 0, 0), 2: (1, 1, 0, 0), 8: (2, 2, 0, 0),
        11: (3, 1, 1, 0), 44: (5, 3, 3, 1), 53: (6, 3, 2, 2),
        96: (8, 4, 4, 0), 107: (7, 7, 3, 0),
        224: (12, 8, 4, 0), 896: (24, 16, 8, 0), 2816: (40, 24, 24, 8),
    }
    for n, q in expected.items():
        require(best[n] == q, f"canonical tuple mismatch at {n}")
    for n, factor, core in ((96, 4, (2, 1, 1, 0)),
                            (224, 4, (3, 2, 1, 0)),
                            (2816, 8, (5, 3, 3, 1))):
        require(best[n] == tuple(factor * v for v in core), f"core mismatch at {n}")

    minima = {n: q[0] for n, q in best.items()}
    records = records_from_minima(minima, 2)
    require(records == [row for row in retained if row[0] <= bound],
            f"record prefix mismatch through {bound}")
    require(2 not in {n for n, _ in records}, "norm 2 unexpectedly a record")
    print(f"PASS: {len(records)} four-square records through {bound:,}, including the seed witnesses")

    def gap(n):
        return best[n][0] - lower_bound(n, 2)

    checked = 0
    for n in range(2, bound // 4 + 1, 2):
        require(best[4 * n] == tuple(2 * v for v in best[n]),
                f"even-input tuple doubling failed at {n}")
        correction = 2 * lower_bound(n, 2) - lower_bound(4 * n, 2)
        require(correction in (0, 1), f"ceiling correction failed at {n}")
        require(gap(4 * n) == 2 * gap(n) + correction,
                f"gap scaling failed at {n}")
        checked += 1
    require(gap(224) == 4 and gap(896) == 9, "rounding example failed")
    require(best[44][0] < 2 * best[11][0], "all-odd competitor example failed")
    print(f"PASS: even-input scaling on {checked} inputs; g(224)=4, g(896)=9")

    boundary = (48, 16, 16, 0)
    require(norm2(boundary) == 2816 and boundary[0] > best[2816][0],
            "three-square boundary versus four-square minimax example failed")
    for n, q in best.items():
        if n > 0 and not legendre_allowed(n):
            require(q[-1] > 0, f"Legendre-excluded norm has a boundary tuple at {n}")
    print("PASS: Legendre-excluded minimizers are interior; 2816 has a suboptimal boundary witness")

    alternative = (8, 5, 3, 3)
    require(norm2(alternative) == 107 and sum(alternative) > sum(best[107]),
            "minimax versus distance-to-diagonal example failed")
    print("PASS: n=107 distinguishes minimax from distance to the diagonal")

    cubes = minimax_by_pairs(3, 218)
    require(5 not in cubes, "5 unexpectedly representable by four nonnegative cubes")
    require(sum(v**3 for v in (5, 4, 3, 0)) == 216, "216 cube witness failed")
    require(sum(v**3 for v in (6, 1, 1, 0)) == 218, "218 cube witness failed")
    require(cubes[216] == 5 and cubes[218] == 6, "cube minimax example failed")
    require(lower_bound(216, 3) == lower_bound(218, 3) == 4,
            "cube lower-bound example failed")
    require(records_from_minima(cubes, 3) == [(1, 0), (27, 1), (218, 2)],
            "cube record prefix failed")
    print("PASS: cube gap 2 is delayed from 216 to 218")


def earliest_thresholds(p, bound):
    """First possible n for each gap, computed without irrational arithmetic.

    These are a bound, not a record generator: alternative representations
    can prevent a pure power from attaining its putative gap.
    """
    result, high, d = [(1, 0)], 0, 1
    while d**p <= bound:
        gap = d - lower_bound(d**p, p)
        if gap > high:
            result.append((d**p, gap))
            high = gap
        d += 1
    return result


def check_dense_table(minima):
    path = ROOT / "data/gap_table_1_20000.csv"
    count, high, index = 0, -1, 0
    with path.open(newline="") as stream:
        rows = csv.DictReader(line for line in stream if not line.lstrip().startswith("#"))
        for count, row in enumerate(rows, 1):
            n = int(row["n"])
            require(n == count and n in minima, f"unexpected dense-table index {n}")
            q = tuple(int(row[c]) for c in ("x", "y", "z", "w"))
            require(q == canon(q) and norm2(q) == n, f"invalid dense-table tuple at {n}")
            require(q[0] == minima[n], f"dense-table maximum is not minimal at {n}")
            gap = minima[n] - lower_bound(n, 2)
            is_record = gap > high
            if is_record:
                high, index = gap, index + 1
            require(int(row["gap"]) == gap and int(row["best_so_far"]) == high,
                    f"incorrect dense-table gap or running maximum at {n}")
            require(int(row["is_record"]) == int(is_record), f"incorrect record flag at {n}")
            require(row["record_index"] == (str(index) if is_record else ""),
                    f"incorrect record index at {n}")
            require(int(row["spread"]) == q[0] - q[3], f"incorrect contextual spread at {n}")
    require(count == 20000, f"expected 20000 dense-table rows, got {count}")
    print(f"PASS: all {count:,} dense-table representations, minimax values, gaps, and record fields")


def check_full(retained):
    print("Full independent pair-sum checks (over representable positive integers):", flush=True)
    for p, bound, expected_representable, expected_records in FAMILY:
        minima = minimax_by_pairs(p, bound)
        records = records_from_minima(minima, p)
        require(len(minima) == expected_representable, f"representability count mismatch for p={p}")
        require(len(records) == expected_records, f"record count mismatch for p={p}")
        if p == 2:
            require(records == [row for row in retained if row[0] <= bound],
                    "independent four-square record prefix mismatch")
            check_dense_table(minima)
            prefix = [row for row in records if row[0] <= VIEWER_BOUNDS[p]]
            require(len(prefix) == 11 and [g for _, g in prefix] == [0, 1, 2, 3, 4, 6, 9, 12, 13, 18, 24],
                    "square viewer catalogue gaps mismatch")
            require(sum(n <= VIEWER_BOUNDS[p] for n in minima) == 10000,
                    "square viewer representability count mismatch")
        else:
            path = ROOT / f"archive/exploratory-sequences/power-balance-p{p}/b-file.txt"
            require([n for n, _ in records] == read_bfile(path), f"archived b-file mismatch for p={p}")
            require([g for _, g in records] == list(range(len(records))),
                    f"record gaps are not consecutive for p={p} in the archived range")
        if p >= 4:
            require(records == earliest_thresholds(p, bound),
                    f"pure-power records do not attain the earliest thresholds for p={p}")
        print(f"PASS: p={p}, n<={bound:,}, {len(minima):,} representable, "
              f"{len(records)} records, last gap {records[-1][1]}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help="reproduce archived bounds, the 20000-row table, and three squares through 20000")
    args = parser.parse_args()
    retained = retained_records()
    check_catalogue(retained)
    check_three_squares(20000 if args.full else 3000)
    check_seed_algebra()
    check_examples(retained)
    if args.full:
        check_full(retained)
    print("PASS: all requested checks. Finite scans do not prove record-chain completeness.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
