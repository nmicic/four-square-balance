# LODA Programs

This directory holds [LODA](https://loda-lang.org) assembly programs for the
OEIS sequences documented in this repository. LODA is a small assembly-like
language whose programs compute integer sequences; the community collection is
[loda-programs](https://github.com/loda-lang/loda-programs), where each program
lives at `oeis/<first three digits>/A<number>.asm`. The files here use the
same header format and are copied there unchanged.

| Program | Sequence | Terms checked |
| --- | --- | ---: |
| `A396760.asm` | [A396760](https://oeis.org/A396760), conjectured recurrence; submitted to LODA | 37 |
| `A396760-scan.asm` | A396760 computed directly from the definition; reference only | 17 |

## Which program is the definition, and which one was submitted

`A396760-scan.asm` is the program that matches the definition of A396760.
It is the LODA translation of the PARI program in the OEIS entry, which is
also `program.gp` in `sequences/gap-record-locations`: it scans
k = 1, 2, 3, ..., computes A122921(k) by searching for the least largest
part, and stops at the n-th gap record. It uses no conjecture. The only
additions are the ordering bounds 3*y^2 >= k - x^2 and
2*z^2 >= k - x^2 - y^2, which prune the search without changing what is
searched.

The scan is slow. Term 14 already needs about 8*10^7 LODA steps, term 15
exceeds LODA's default budget of 10^8 steps per term, and the 37th term lies
near 10^9, out of reach for any LODA scan. LODA validates a submitted program
by evaluating every listed term within that budget, so `loda submit` rejects
this file and `loda check` reports an error for it. Run it with the step limit
removed:

    loda eval loda/A396760-scan.asm -t 17 -c -1    # about one minute

The 17 terms it produced in that time match the b-file.

`A396760.asm` is the program submitted to LODA instead, because of that
load limitation. It stores a(1)..a(9) and applies the recurrence
a(n) = 4*a(n-3) for n >= 10, which is the three-chain structure
96*4^m, 224*4^m, 2816*4^m in recurrence form. That structure is stated as a
conjecture in the OEIS entry: it reproduces all 37 verified terms below 10^9
and is unproved beyond them. So the submitted program is a fast conjectural
formula, and the scan program is the definitional reference against which it
is checked. Should a later verified term contradict the recurrence, the
submitted program has to be corrected and the scan stays valid.

## Usage

Install [loda-cpp](https://github.com/loda-lang/loda-cpp) and run `loda setup`
once. Then, from the repository root:

    loda eval loda/A396760.asm -t 37      # print the first 37 terms
    loda check loda/A396760.asm           # compare with the OEIS b-file
    sh loda/check.sh                      # both checks for every program here

`loda/check.sh` also diffs each program's output against the b-file kept in
`sequences/`, so it works as a regression test when a program changes. For
the scan program it compares the first 14 terms only, which takes a few
seconds.
