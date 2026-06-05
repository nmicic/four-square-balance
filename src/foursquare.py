#!/usr/bin/env python3
"""
foursquare.py -- canonical integer four-square decomposition (reference impl).

Every n >= 1 has n = x^2 + y^2 + z^2 + w^2 with integers x>=y>=z>=w>=0 (Lagrange).
A given n may admit several such ordered tuples; we pick ONE per mode:

  max       lexicographically GREATEST tuple. Top-heavy: one big square + scraps.
            Leading coord = floor(sqrt(n)) for ~84% of n. EXACT & FAST at any size.

  min       lexicographically SMALLEST tuple = the most "balanced" exact answer
            (minimizes the largest part first). EXACT but EXPENSIVE for large n:
            it is a closest-lattice-point-to-the-diagonal problem on the sphere
            of radius sqrt(n); the balanced corner is sparse, so naive climbing is
            infeasible past ~40-50 bits. Use only for small/medium n, or as the
            ground-truth checker. For large n use the C engine (../src/foursquare.c).

Pure standard library, no dependencies.

CLI:
  python foursquare.py <n> [--mode min|max]
  python foursquare.py --verify              # check all modes vs brute force
  python foursquare.py --csv FILE [--mode ...] [--col COLNAME] [--limit K]
                                             # FILE has a column of ints (dec or 0x hex)
"""
import math, sys, csv, time

# ---------- feasibility primitives ----------

def is_sum_of_three(m: int) -> bool:
    """Legendre: m is a sum of <=3 squares iff m is NOT of form 4^a*(8b+7)."""
    if m < 0:
        return False
    while m and m % 4 == 0:
        m //= 4
    return m % 8 != 7


# ---------- exact MAX (fast at any size) ----------
# self-contained two-square helpers (pure stdlib).
def _maybe2(m):
    if m < 0: return False
    if m % 4 == 3: return False
    return True
def _two_sq_cap(m, cap):
    out = []
    w = 0
    while w * w * 2 <= m:
        z2 = m - w * w
        z = math.isqrt(z2)
        if z * z == z2 and z <= cap:
            out.append((z, w))
        w += 1
    return sorted(out)


def canonical_max(n: int):
    if n == 0:
        return (0, 0, 0, 0)
    x = math.isqrt(n)
    while not is_sum_of_three(n - x * x):
        x -= 1
    r1 = n - x * x
    for y in range(min(x, math.isqrt(r1)), -1, -1):
        m = r1 - y * y
        if not _maybe2(m):
            continue
        reps = _two_sq_cap(m, y)
        if reps:
            z, w = reps[-1]
            return (x, y, z, w)
    raise RuntimeError("unreachable (Lagrange)")


# ---------- exact MIN (small/medium n; ground truth) ----------

def canonical_min_exact(n: int, time_budget: float = None):
    """Exact lexicographic-minimum. Box-scan, no factorization. Slow for large n."""
    if n == 0:
        return (0, 0, 0, 0)
    t0 = time.time()
    xmin = math.isqrt((n + 3) // 4)
    while xmin * xmin * 4 < n:
        xmin += 1
    for x in range(xmin, math.isqrt(n) + 1):
        r1 = n - x * x
        if not is_sum_of_three(r1):
            continue
        ylo = math.isqrt((r1 + 2) // 3)
        while ylo * ylo * 3 < r1:
            ylo += 1
        yhi = min(x, math.isqrt(r1))
        for y in range(ylo, yhi + 1):
            m = r1 - y * y
            zlo = math.isqrt((m + 1) // 2)
            while zlo * zlo * 2 < m:
                zlo += 1
            zhi = min(y, math.isqrt(m))
            for z in range(zlo, zhi + 1):
                w2 = m - z * z
                w = math.isqrt(w2)
                if w * w == w2 and w <= z:
                    return (x, y, z, w)
        if time_budget and time.time() - t0 > time_budget:
            raise TimeoutError(f"min exact exceeded {time_budget}s at x-climb {x - xmin}")
    raise RuntimeError("unreachable (Lagrange)")



def canonical(n: int, mode: str = "min", **kw):
    if mode == "min":
        return canonical_min_exact(n, kw.get("time_budget"))
    if mode == "max":
        return canonical_max(n)
    raise ValueError("mode must be min|max")


# ---------- brute-force ground truth (small n) ----------

def _all_sorted_reps(n):
    L = math.isqrt(n); out = []
    for a in range(L, -1, -1):
        for b in range(a, -1, -1):
            if a * a + b * b > n: continue
            for c in range(b, -1, -1):
                s = a * a + b * b + c * c
                if s > n: continue
                d2 = n - s; d = math.isqrt(d2)
                if d * d == d2 and d <= c: out.append((a, b, c, d))
    return out


def _verify():
    bad_max = [n for n in range(1, 5000) if canonical_max(n) != max(_all_sorted_reps(n))]
    bad_min = [n for n in range(1, 5000) if canonical_min_exact(n) != min(_all_sorted_reps(n))]
    print("max exact 1..4999 :", "OK" if not bad_max else f"FAIL {bad_max[:6]}")
    print("min exact 1..4999 :", "OK" if not bad_min else f"FAIL {bad_min[:6]}")


def _parse_int(s):
    s = s.strip()
    return int(s, 16) if s.lower().startswith("0x") else int(s)


def _run_csv(path, mode, col, limit):
    rows = list(csv.DictReader(open(path)))
    if col is None:
        # auto-pick a column that parses as int / hex
        for c in rows[0]:
            try:
                _parse_int(rows[0][c]); col = c; break
            except Exception:
                continue
    out = path.rsplit(".", 1)[0] + f".foursquare_{mode}.csv"
    t = time.time(); na = 0
    with open(out, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(list(rows[0].keys()) + ["n", "x", "y", "z", "w"])
        for row in rows[:limit] if limit else rows:
            n = _parse_int(row[col])
            try:
                r = canonical(n, mode)
            except TimeoutError:
                r = None
            if r is None:
                na += 1
                wr.writerow(list(row.values()) + [n, "NA", "NA", "NA", "NA"])
            else:
                assert sum(v * v for v in r) == n
                wr.writerow(list(row.values()) + [n, *r])
    print(f"wrote {out}  ({time.time()-t:.1f}s, NA={na})")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(0)
    if a[0] == "--verify":
        _verify()
    elif a[0] == "--csv":
        mode = a[a.index("--mode") + 1] if "--mode" in a else "max"
        col = a[a.index("--col") + 1] if "--col" in a else None
        limit = int(a[a.index("--limit") + 1]) if "--limit" in a else None
        _run_csv(a[1], mode, col, limit)
    else:
        mode = a[a.index("--mode") + 1] if "--mode" in a else "max"
        n = _parse_int(a[0])
        t = time.time(); r = canonical(n, mode); dt = (time.time() - t) * 1000
        print(f"n={n} ({n.bit_length()} bits) mode={mode} -> {r}  [{dt:.2f} ms]")
        if r: assert sum(v * v for v in r) == n
