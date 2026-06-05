#!/usr/bin/env python3
"""Emit the four-square balance table as CSV for n = 1..N.

Columns: n,x,y,z,w,gap,spread
  (x,y,z,w) = canonical (most balanced) decomposition, x>=y>=z>=w>=0
  gap       = x - ceil(sqrt(n/4))
  spread    = x - w

Uses the exact 'min' mode of foursquare.py (minimal largest part). Exact but
expensive for large n; meant for small/medium prefixes and visualization samples,
not for reproducing the retained 10^9 record scan.

Usage: python gen_table.py N > table.csv
"""
import sys, math
from foursquare import canonical


def xmin(n):
    x = math.isqrt((n + 3) // 4)
    while 4 * x * x < n:
        x += 1
    return x


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    print("n,x,y,z,w,gap,spread")
    for n in range(1, N + 1):
        x, y, z, w = canonical(n, "min")
        print(f"{n},{x},{y},{z},{w},{x - xmin(n)},{x - w}")


if __name__ == "__main__":
    main()
