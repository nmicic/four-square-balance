# Structural notes on the four-square balance gap

Working notes on the gap-record-location sequence (A396760), recording two
structural observations about *why* the records look the way they do. These are
explanatory notes, not part of the verified evidence; the authoritative term data
remains the b-file and the retained 10^9 scan. Each claim below is labeled
**proved** or **observed/conjectural**.

Throughout, `A(n) = A122921(n)` is the least possible largest part `x` in
`n = x^2 + y^2 + z^2 + w^2` (`x >= y >= z >= w >= 0`), `xmin(n) = ceil(sqrt(n/4))`,
and the gap is `g(n) = A(n) - xmin(n)`.

## 1. Why doubling is conditional in four squares (proved)

The records cluster on `*4^m` chains, which raises the question: when does
`A(4n) = 2 A(n)`? There is a clean mod-4 answer.

If `4n = a^2 + b^2 + c^2 + d^2`, reduce mod 4. A square is `0 (mod 4)` if even and
`1 (mod 4)` if odd, so the sum is congruent to the **number of odd parts**. Since
`4n ≡ 0`, that count must be `≡ 0 (mod 4)`. With four parts it is therefore either
**0 (all even)** or **4 (all odd)**.

- **All even:** `a=2a', …` gives `n = a'^2 + b'^2 + c'^2 + d'^2`, a representation of
  `n` whose largest part is half. The best all-even representation of `4n` thus has
  largest part exactly `2 A(n)` — the "even lift."
- **All odd:** a genuinely different representation of `4n`, with its own minimal
  largest part `m_odd(4n)`.

Hence

    A(4n) = min( 2 A(n),  m_odd(4n) ),

and **doubling `A(4n) = 2 A(n)` holds iff no all-odd representation of `4n`
undercuts the even lift** (`m_odd(4n) >= 2 A(n)`).

The smallest failure is the cleanest: `4 = 1^2+1^2+1^2+1^2` is all-odd with largest
part `1 < 2 A(1) = 2`, so `A(4) = 1`, not `2`. The all-odd competitor — which exists
because four parts can carry four odd values — is exactly what makes doubling
conditional rather than automatic.

This also explains the **singleton** records `11` and `53` (no `*4^m` chain): their
doubling fails immediately because an all-odd representation wins one step up. For
`11`, `A(11) = 3` but `44 = 5^2+3^2+3^2+1^2` (all odd) gives `A(44) = 5 < 6`. For
`53`, `A(53) = 6` but `212 = 9^2+9^2+5^2+5^2` (all odd) gives `A(212) = 9 < 12`.
The record families are exactly the seeds where the all-odd competitor never wins
down the whole chain — which the retained scan confirms for every listed term.

## 2. The three families occupy only two shape-space directions (observed)

In the Helmert projection used by the visualization
(`s1=(x-y)/√2`, `s2=(x+y-2z)/√6`, `s3=(x+y+z-3w)/√12`, with the diagonal
`(1,1,1,1)` projected to the origin), each `*4^m` chain is a ray from the origin.
Dividing each family's canonical tuple by its largest common power of two —
equivalently dividing the norm by that power squared — gives a primitive **core**
shape per family:

    96   = 16 · 6,    core 6  = (2,1,1,0)
    224  = 16 · 14,   core 14 = (3,2,1,0)
    2816 = 64 · 44,   core 44 = (5,3,3,1)

Their Helmert unit directions are

    (2,1,1,0) -> (0.500, 0.289, 0.816)
    (5,3,3,1) -> (0.500, 0.289, 0.816)     <-- identical
    (3,2,1,0) -> (0.316, 0.548, 0.775)

So the `96` and `2816` families **coincide** as a single ray, while `224` is the
only geometrically distinct direction. The coincidence is exact, not numerical:

    (5,3,3,1) = 2·(2,1,1,0) + (1,1,1,1),

and the Helmert basis annihilates the cube `(1,1,1,1)`, so `2816`'s core projects
onto `96`'s direction at twice the radius. Geometrically the three chains are
**two rays**: the `(2,1,1,0)`-type "two equal middle parts, `w=0`" direction (96 &
2816), and the `(3,2,1,0)`-type **arithmetic-progression** direction with all parts
distinct and `w=0` (224).

## 3. The cores' odd parts run 3, 7, 11 (speculative)

The three cores carry odd parts

    6  = 2 · 3
    14 = 2 · 7
    44 = 4 · 11

i.e. odd core parts `3, 7, 11` — an arithmetic progression of step 4, all
`≡ 3 (mod 4)`. This is separate from the singleton record seeds `11` and `53`.
Whether a fourth family (a next odd core, e.g. near `15`) first appears beyond
`10^9` is open. This is a question for the exact scanner past the current `10^9`
bound, **not** something settled by the 37 known terms; it is recorded here only
as a direction to test, not a claim.

## Status

- Section 1 is a proof (the mod-4 congruence and the even-lift / all-odd split are
  elementary and exact); the statement that the listed families never lose the
  all-odd competition is checked term-by-term by the retained scan, not proved in
  general.
- Section 2 is an exact algebraic identity about the projection.
- Section 3 is an unverified pattern flagged for a future scan.
