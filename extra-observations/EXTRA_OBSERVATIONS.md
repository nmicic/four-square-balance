# Extra observations on the power-balance family

*8 September 2026.*

The [family viewer](https://nmicic.github.io/four-square-balance/viz/power-balance/balance.html)
shows six sequences, one for each exponent p = 2..7. The four-square record
sequence [A396760](https://oeis.org/A396760) is the p = 2 member. The other
five use the same construction with p-th powers in place of squares.

This note lists all six sequences at the viewer bounds, then looks at the
p = 2 member: the shapes of its record tuples, its exact scaling law, and
which statements are proved and which are only observed. A last section
relates the four-square problem to three-square representability.

The script [verify_observations.py](verify_observations.py) rechecks every
bounded claim in this note with exact integer arithmetic. From the repo root:

```sh
python3 extra-observations/verify_observations.py
python3 extra-observations/verify_observations.py --full
```

Both commands need only the Python standard library and this checkout. The
script also runs by absolute path from another directory. A failed check exits
nonzero, also under `python3 -O`.

## One construction, six sequences

For each p, let R_p be the set of positive integers n with a representation

```text
n = a^p + b^p + c^p + d^p,    0 <= a <= b <= c <= d.
A_p(n) = the least possible largest root d;
L_p(n) = the least integer m with 4*m^p >= n;
g_p(n) = A_p(n) - L_p(n),    for n in R_p.
```

The sequence for p lists the n in R_p where g_p(n) exceeds its value at every
smaller member of R_p. The first record is 1, with gap 0, for every p. For
p = 2, every positive integer is in R_2 (Lagrange). For p >= 3 some integers
are missing; for example, 5 is not a sum of four nonnegative p-th powers. A
missing integer has no gap. It does not count as gap zero.

The bounds below are the ones in `balance.html`. The public viewer uses the
same bounds.

| p | Four summands | Viewer bound n <= | Representable positive integers | Records | Record gaps | Data |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 2 | Squares | 10,000 | 10,000 | 11 | 0,1,2,3,4,6,9,12,13,18,24 | [A396760 b-file](../sequences/gap-record-locations/b-file.txt) |
| 3 | Cubes | 300,000 | 193,625 | 25 | 0 through 24 | [p=3](../archive/exploratory-sequences/power-balance-p3/README.md) |
| 4 | Fourth powers | 500,000 | 17,236 | 8 | 0 through 7 | [p=4](../archive/exploratory-sequences/power-balance-p4/README.md) |
| 5 | Fifth powers | 800,000 | 2,806 | 4 | 0 through 3 | [p=5](../archive/exploratory-sequences/power-balance-p5/README.md) |
| 6 | Sixth powers | 9,000,000 | 2,498 | 3 | 0,1,2 | [p=6](../archive/exploratory-sequences/power-balance-p6/README.md) |
| 7 | Seventh powers | 40,000,000 | 1,472 | 3 | 0,1,2 | [p=7](../archive/exploratory-sequences/power-balance-p7/README.md) |

All record locations in these six rows:

```text
p=2:
1, 11, 53, 96, 224, 384, 896, 1536, 2816, 3584, 6144

p=3:
1, 27, 218, 731, 1331, 2745, 4913, 6862, 10648, 15627, 21954,
27016, 35938, 46658, 54896, 68956, 85186, 97338, 117650, 140700,
166377, 185195, 216002, 250050, 274642

p=4:
1, 256, 2401, 14641, 38416, 104976, 194481, 331776

p=5:
1, 3125, 59049, 371293

p=6:
1, 15625, 1000000

p=7:
1, 279936, 35831808
```

The p = 2 member has verified terms beyond 10,000: its b-file has 37 records
for n < 10^9. For p = 3..7 the viewer bounds equal the archived scan bounds.
These five members are exploratory and are not in the OEIS. The `shape.html`
viewer uses other bounds for p = 2, 3, 4 (12,000, 80,000, 600,000), so it
shows 12 records for p = 2 and 16 for p = 3.

The bounds grow with p because the powers grow faster. They are not equally
deep samples. The question is the same for every p: how far must the smallest
possible largest root exceed the equal-parts lower bound?

## The square member

For a positive integer n, write

```text
n = x^2 + y^2 + z^2 + w^2,    x >= y >= z >= w >= 0.
A(n) = the least possible largest root x;
L(n) = ceiling(sqrt(n/4));
g(n) = A(n) - L(n).
```

A(n) is [A122921](https://oeis.org/A122921). A396760 lists the n where g
first exceeds all earlier values. Where a tuple is shown below, it is the
lexicographically least one: minimize x, then y, then z. The gap depends only
on x, so this tie rule does not change the record sequence.

The [retained scan](../data/records_to_1e9_COMPLETE.txt) lists 37 records for
n < 10^9. In that range they are exactly the merge of

```text
1, 11, 53,
96*4^m, 224*4^m, 2816*4^m    (m >= 0).
```

| Claim | Status |
| --- | --- |
| The 96 and 2816 cores share one projected direction | Exact identity, proved below |
| Fixed-shape criterion x + w = y + z | Elementary theorem, proved below |
| The canonical tuple doubles for even inputs | Parity theorem, proved below |
| Infinitely many gap records | Follows from the scaling theorem |
| Three-square domain in (v2(n), u) coordinates | Legendre's theorem, restated below |
| No record families other than the three chains | Conjecture; open beyond the retained scan |
| Records for p = 4..7 are pure powers | Verified at the archived bounds only |

## Two record families share one projected direction

The three chains start at these canonical tuples. Dividing a tuple by its
largest common power of two gives its core:

| Record location | Canonical tuple | Core | Squared norm of core |
| ---: | --- | --- | ---: |
| 96 | (8,4,4,0) | (2,1,1,0) | 6 |
| 224 | (12,8,4,0) | (3,2,1,0) | 14 |
| 2816 | (40,24,24,8) | (5,3,3,1) | 44 |

A chain is named by its first record location, not by the norm of its core.
For example, 2816 = 8^2 * 44.

The [main viewer](../viz/index.html) removes the equal-coordinate component
with the Helmert map

```text
H(x,y,z,w) = ((x-y)/sqrt(2),
             (x+y-2z)/sqrt(6),
             (x+y+z-3w)/sqrt(12)).
```

H is linear and sends (1,1,1,1) to zero. The identity

```text
(5,3,3,1) - (1,1,1,1) = (4,2,2,0) = 2*(2,1,1,0)
```

gives

```text
H(5,3,3,1) = 2*H(2,1,1,0).
```

So the 96 core and the 2816 core lie on the same projected ray. The 224 core
does not: its Helmert numerators are (1,3,6), against (1,1,4) for the 96 core.
The three chains use only two ray directions in this view.

The 96 and 2816 chains are still different record families, with different
norms and gap values. The projection drops one coordinate, so a shared
projected direction does not mean a shared direction in four coordinates.

## Quaternion multiplication connects the cores

Read a tuple q = (x,y,z,w) as the quaternion x + y*i + z*j + w*k. The first
coordinate is the scalar part. This follows the sorted-root order used here,
not the scalar-last order sometimes used for rotations.

Define

```text
r = (1,1,1,1),
T(q) = canon(q*r),
canon(v) = the absolute values of the coordinates of v, sorted in descending order.
```

`canon` picks one representative of a signed-permutation orbit. It does not
search for a minimax representation of the resulting norm.

| Seed or core | q | Hamilton product q*r | T(q) |
| --- | --- | --- | --- |
| 1 | (1,0,0,0) | (1,1,1,1) | (1,1,1,1) |
| 11 | (3,1,1,0) | (1,5,3,3) | (5,3,3,1) |
| 53 | (6,3,2,2) | (-1,9,7,9) | (9,9,7,1) |
| 53, other minimax tuple | (6,4,1,0) | (1,11,3,9) | (11,9,3,1) |
| 96 | (2,1,1,0) | (0,4,2,2) | (4,2,2,0) |
| 224 | (3,2,1,0) | (0,6,2,4) | (6,4,2,0) |
| 2816 | (5,3,3,1) | (-2,10,6,6) | (10,6,6,2) |

The squared norm of a quaternion product is the product of the squared norms.
Since ||r||^2 = 4, every row multiplies the squared norm by four.

The 11 core maps to the 2816 core shape, from norm 11 to norm 44. Scaling by
8 then gives the canonical tuple at 2816. The three chain cores each map to
twice themselves. The two 53 tuples map to different shapes of norm 212, and
212 is not a record. Multiplication alone says nothing about minimax
optimality or records.

### A fixed-shape criterion

**For q = (x,y,z,w) with x >= y >= z >= w >= 0, T(q) = 2q if and only if
x + w = y + z.**

The product is

```text
q*r = (x-y-z-w, x+y+z-w, x-y+z+w, x+y-z+w).
```

If x + w = y + z, this becomes

```text
q*r = (-2w, 2x, 2z, 2y),
```

whose sorted absolute values are 2q.

Conversely, x+y+z-w is the largest absolute coordinate of the product. It is
at least the third and fourth coordinates because y >= w and z >= w, and those
two coordinates are nonnegative. It is at least the first coordinate and its
negative because y + z >= 0 and x >= w. If T(q) = 2q, this maximum equals 2x,
so x + w = y + z.

Equivalently, in (x-y, y-z, z-w) the first and last differences are equal.
The three chain cores have this symmetry. It is not a record criterion:
(1,1,0,0) satisfies it, and its norm 2 is not a record location.

The script computes the Hamilton product on its own and checks the criterion
on all 46,376 sorted nonnegative tuples with largest coordinate at most 30.

### Rotations

Scaling a tuple by a positive number does not change its unit quaternion.
Removing the diagonal component, or sorting absolute values, does change it
in general. For example, (2,1,1,0)/sqrt(6) and (5,3,3,1)/sqrt(44) are
different unit quaternions, although their Helmert images lie on one ray.
T(q) = 2q is a statement about shapes after `canon`. For the three chain
cores the raw product is a signed permutation of 2q, not 2q itself.

## Exact scaling of minimizers and gaps

For every p, doubling all four roots multiplies n by 2^p and doubles the
largest root, so A_p(2^p * n) <= 2*A_p(n). The odd part of n is unchanged.
Equality needs an argument that no better representation exists. For squares,
parity gives one.

**For every positive even n, A(4n) = 2A(n), and the canonical tuple doubles.**

4n is divisible by 8. Squares are 0 or 1 modulo 4, so a representation of 4n
has either zero or four odd coordinates. Four odd squares sum to 4 modulo 8,
so all four coordinates are even. Halving the coordinates is a bijection onto
the representations of n, and it preserves lexicographic order. This proves
the claim.

The claim also holds for non-records: 2 and 8 have tuples (1,1,0,0) and
(2,2,0,0), and neither is a record. For odd n, an all-odd representation can
beat the doubled tuple:

```text
11: (3,1,1,0)
44: (5,3,3,1), largest root 5, better than 6 in (6,2,2,0).
```

Whenever the minimizer doubles, the gaps satisfy

```text
g(4n) = 2*g(n) + e(n),
e(n) = 2*L(n) - L(4n), which is 0 or 1.
```

Here L(4n) = ceiling(2*sqrt(n/4)), and 2*ceiling(t) - ceiling(2t) is 0 or 1
for every real t. For example, g(224) = 4 and g(896) = 9: the tuple doubles,
but the gap need not.

The three chain bases 96, 224, 2816 are even, so the canonical tuples double
along each chain at every step. This does not show that the chain members
stay global records, or that no other family appears.

### There are infinitely many records

Exhaustive enumeration gives A(96) = 8. By the scaling theorem,

```text
g(96*4^m) = 8*2^m - ceiling(sqrt(24)*2^m).
```

Since 8 - sqrt(24) > 0, these gaps are unbounded. An unbounded function on
the positive integers has infinitely many strict running records. So A396760
is infinite, even without the three-chain conjecture.

## Minimax balance and geometric closeness differ

At n = 107, the canonical minimax tuple is (7,7,3,0). The representation
(8,5,3,3) has a larger maximum but lies closer to the equal-coordinate line.
For a tuple q of squared norm n, the squared distance to that line is

```text
n - (x+y+z+w)^2/4.
```

The coordinate sums are 17 and 19. So minimizing the largest root does not
minimize the distance to the diagonal. The script checks the minimax tuple by
exhaustive enumeration and compares the two sums in integers.

In the viewers, the projected position and the lean angle describe the shape
of the chosen minimax representation. The sequence statistic is still g(n).
Also, g(n) = 0 means the largest root equals the rounded lower bound; four
equal roots occur only when n = 4m^2.

## Record formation across the family

### The earliest possible location of a given gap

For p >= 2 and a target gap j >= 1, put

```text
alpha_p = 1 - 4^(-1/p),
D_j = ceiling(j/alpha_p).
```

If the minimal largest root at n is d, then n >= d^p, so

```text
g_p(n) <= d - ceiling(d/4^(1/p)) = floor(alpha_p * d).
```

So g_p(n) >= j needs d >= D_j, and then n >= D_j^p. The bound is attained
when D_j^p has no representation with a smaller largest root; its gap is then
exactly j. Another representation can prevent this, so the bound is not a
formula for the sequence.

**Every archived record after 1 for p = 4, 5, 6, 7 sits exactly at this
threshold.** For fourth powers, the first seven positive record gaps occur at
roots 4, 7, 11, 14, 18, 21, 24. This explains the pure-power prefixes at the
current bounds. It does not imply that they continue.

The script computes the thresholds with the integer test d - L_p(d^p) >= j,
so no irrational number is rounded.

### Cubes: the bound can fail

For cubes, the first possible location of gap 2 is 6^3 = 216. But

```text
216 = 5^3 + 4^3 + 3^3 + 0^3,
```

so its minimax root is 5, and with L_3(216) = 4 its gap is only 1. The next
record is

```text
218 = 6^3 + 1^3 + 1^3 + 0^3,
```

with minimax root 6, lower bound 4, and gap 2. The script computes all
representable integers through 218 to check both minima and the record.

The [power-family viewers](../viz/power-balance/index.html) show these
examples. Their bounds differ by page, so use the archived bounds above when
comparing with downloaded sequence data.

## Three-square representability and the four-square boundary

A three-square representation is a four-square representation with a zero
coordinate. So three-square representability is a boundary question for the
four-square shells above.

The sequence [A395008](https://oeis.org/A395008) uses the statistic

```text
s3(n) = min(x-z) over n = x^2 + y^2 + z^2,    x >= y >= z >= 0,
```

and lists the n where s3 sets a strict running record over representable
integers. Its first sixteen terms are

```text
1, 4, 10, 16, 37, 58, 64, 130, 148, 232, 256, 445, 520, 592, 928, 1024.
```

The data is in
[three-square-balance](https://github.com/nmicic/three-square-balance/tree/main/sequences/spread-record-locations).
The script here recomputes this prefix independently. Note that A395008 uses
three squares and the spread x-z, while p = 3 above uses four cubes and the
minimax gap.

### Legendre's condition in the coordinates n = 2^k * u

Write every positive integer as

```text
n = 2^k * u,    k = v2(n),    u odd.
```

Legendre's three-square theorem excludes exactly the integers 4^a * (8b+7).
In these coordinates:

```text
n is NOT a sum of three squares
    if and only if k is even and u mod 8 = 7.
```

For even k = 2a the odd part must be 8b+7; for odd k the forbidden form is
impossible. So the domain of s3 depends only on the parity of k and the
residue of u modulo 8.

| Odd part u modulo 8 | k even | k odd |
| ---: | --- | --- |
| 1, 3, 5 | Representable | Representable |
| 7 | Excluded | Representable |

Fix an odd u and look at u, 2u, 4u, 8u, ... If u mod 8 = 7, the terms
alternate between excluded and representable. For the other odd residues,
every term is representable. For example:

```text
u=7:
7       excluded
14      3^2 + 2^2 + 1^2
28      excluded
56      6^2 + 4^2 + 2^2
112     excluded
224     12^2 + 8^2 + 4^2
```

Multiplying n by four adds two to k and keeps the domain. Also, every
three-square representation of 4n has all coordinates even: three residues
from {0,1} sum to 0 modulo 4 only if all are 0. Halving and doubling are
inverse bijections, so

```text
s3(4n) = 2*s3(n)    for every representable n.
```

This does not decide which primitive integers set spread records.

### Lattice points on the sphere

A three-square representation is an integer point on the sphere
x^2 + y^2 + z^2 = n in R^3. Restricting to x >= y >= z >= 0 picks one point
per orbit under signs and permutations; minimizing x - z picks the smallest
spread among those points.

Four-square representations are integer points on a sphere in R^4. A
Legendre-excluded integer has no such point on the boundary of the
nonnegative orthant: every four-square representation of it has four positive
roots. The converse only says that a boundary point exists. The four-square
minimizer may still be interior. At 2816, the three-square representation
(48,16,16,0) exists, but the minimax tuple (40,24,24,8) has a smaller largest
root.

## What the script checks

Default run:

- Lists all six sequences at the `balance.html` bounds and checks the local
  viewer's exponent list and bounds against the table above.
- Prints and checks the seven seed transformations above.
- Checks the shared-ray identity with exact Helmert numerators.
- Checks the fixed-shape criterion and the norm identity on 46,376 tuples
  with largest coordinate at most 30.
- Enumerates canonical four-square tuples through 3,000, reproducing the nine
  record locations in that range and the core tuples.
- Checks tuple doubling and the gap formula for 375 even inputs, and the
  example at 107.
- Checks the cube example through 218, and that the retained record file
  matches the b-file.
- Enumerates three-square representations through 3,000, compares existence
  with the (v2(n), u mod 8) rule, checks s3(4n) = 2*s3(n) where both are in
  range, and reproduces the sixteen A395008 terms through 1,024.

The `--full` run also recomputes the four-square records through 20,000 and
every higher-power record at the archived bounds. It uses a different
algorithm: for each sum s of two p-th powers it stores the least possible
larger root M(s), then minimizes max(M(s), M(t)) over s + t = n. Every
four-root representation splits into two pairs, and replacing a pair by its
own minimizer cannot raise the maximum, so this computes A_p(n) exactly.

The results are compared with the committed b-files and record data. The
full run also checks every row of the 20,000-row gap table (tuple, minimal
largest root, gap, running record, spread), the representable counts in the
table above, the threshold observation for p = 4..7, and the three-square
checks through 20,000.

The script does not import the repository's minimax code and does not
derive its expected values from the three-chain conjecture. It writes no
files. Neither mode repeats the scan to 10^9 or proves that no further record
family exists.
