#!/usr/bin/env python3
"""
Balance-gap records for representations of N as a sum of four p-th powers.

For each representable N = a^p + b^p + c^p + d^p (a<=b<=c<=d, nonneg integers),
let minMax(N) = the smallest possible largest part d over all representations,
and lb(N) = the smallest integer m with 4*m^p >= N (the "perfectly balanced" part).
The balance gap is g(N) = minMax(N) - lb(N): how far N is forced away from
four equal p-th powers. Record positions of g are the sequence family.

p=2 reproduces OEIS A396760 (asserted below against the known prefix). The
p=3..7 results are documented in ../exploratory-sequences/power-balance-p{3..7}/;
only p=2 is an OEIS sequence.
"""

def lb_int(n, p):
    m = int(round((n/4) ** (1.0/p)))
    while 4 * (m ** p) < n: m += 1
    while m > 0 and 4 * ((m-1) ** p) >= n: m -= 1
    return m

def records(p, Nmax):
    K = 1
    while (K+1) ** p <= Nmax: K += 1
    pw = [m ** p for m in range(K+1)]
    minMax = {}
    for a in range(K+1):
        pa = pw[a]
        if pa > Nmax: break
        for b in range(a, K+1):
            s2 = pa + pw[b]
            if s2 > Nmax: break
            for c in range(b, K+1):
                s3 = s2 + pw[c]
                if s3 > Nmax: break
                for d in range(c, K+1):
                    s = s3 + pw[d]
                    if s > Nmax: break
                    if s not in minMax or d < minMax[s]:
                        minMax[s] = d
    recs, rec = [], -1
    for n in sorted(minMax):
        if n < 1: continue
        g = minMax[n] - lb_int(n, p)
        if g > rec:
            rec = g
            recs.append((n, g))
    return recs

if __name__ == "__main__":
    A396760 = [1, 11, 53, 96, 224, 384, 896, 1536, 2816, 3584, 6144]
    CFG = {2: 10000, 3: 300000, 4: 500000, 5: 800000, 6: 9000000, 7: 40000000}
    for p, Nmax in CFG.items():
        rs = records(p, Nmax)
        if p == 2:
            assert [n for n, _ in rs] == A396760, "p=2 self-check vs A396760 failed"
        print(f"# balance-gap records, p={p}, search bound Nmax={Nmax}")
        print("# columns: N gap")
        for n, g in rs:
            print(f"{n} {g}")
