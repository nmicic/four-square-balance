# Gap-Record Locations

a(n) is the n-th number k at which the balance gap

    g(k) = A122921(k) - ceiling(sqrt(k/4))

reaches a new record value over all smaller positive arguments.

Here A122921(k) is the least possible largest part x in a representation

    k = x^2 + y^2 + z^2 + w^2,   x >= y >= z >= w >= 0.

Since x >= ceiling(sqrt(k/4)) always, g(k) measures how far k is forced away from
four equal squares.

## Terms

1, 11, 53, 96, 224, 384, 896, 1536, 2816, 3584, 6144, 11264, 14336, 24576, 45056,
57344, 98304, 180224, 229376, 393216, 720896, 917504, 1572864, 2883584, 3670016,
6291456, 11534336, 14680064, 25165824, 46137344, 58720256, 100663296, 184549376,
234881024, 402653184, 738197504, 939524096

These 37 terms are complete for k < 10^9 by the retained exact scan in
`../../data/records_to_1e9_COMPLETE.txt`. The last verified record below 10^9 is
939524096, with g = 9250.

## b-file

`b-file.txt` has the 37 verified terms, offset 1.

## Program

`program.gp` is a direct PARI/GP scanner: `lista(N)` prints each k <= N where g(k)
exceeds all previous values.

For a reproducibility self-test and the observed chain construction, see
`../../src/records.gp`.

`../../loda/A396760.asm` is a [LODA](https://loda-lang.org) program for the same
terms: it stores a(1)..a(9) and applies the observed recurrence
a(n) = 4*a(n-3) for n >= 10, the three-chain structure below in recurrence
form. See `../../loda/README.md`.

## Observed Structure

The verified terms below 10^9 are reproduced by the initial records

    1, 11, 53

and the three interleaved chains

    96*4^m, 224*4^m, 2816*4^m     (m >= 0),

merged in increasing order.

This three-chain description is an observed formula through the retained scan. It
is used as a conjectural continuation beyond 10^9, but the b-file here contains
only verified terms below 10^9.

The corresponding canonical decompositions and gap values for the 37 verified
records are in `../../data/record_decompositions_verified.txt`.

## Relation To A006431

There is a partial overlap with A006431, the numbers with a unique partition into
four nonnegative squares, but the sequences are distinct. In the verified range,
1, 11, and the 96*4^m and 224*4^m chains overlap A006431; 53 and the 2816*4^m
chain do not. Conversely, A006431 contains many terms that are not gap-record
locations.
