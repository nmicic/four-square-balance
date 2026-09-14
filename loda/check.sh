#!/bin/sh
# Verify the LODA programs in this directory.
#
# For each program listed in PROGRAMS the script
#   1. runs `loda check`, which compares the program with the OEIS b-file
#      (downloaded into ~/loda/seqs on first use), and
#   2. evaluates the program and diffs the output against the b-file kept in
#      this repository.
#
# Requires loda-cpp (https://loda-lang.org) after `loda setup`.

set -e
cd "$(dirname "$0")/.."
PATH="$PATH:$HOME/loda/bin"
export PATH

# A-number  repository b-file
PROGRAMS="
A396760 sequences/gap-record-locations/b-file.txt
"

# Slow definitional scans: file name, repository b-file, terms to compare.
# These exceed LODA's default step budget, so they are only evaluated with the
# step limit removed and compared with the leading terms of the b-file.
SCANS="
A396760-scan sequences/gap-record-locations/b-file.txt 14
"

status=0
for entry in $(echo "$PROGRAMS" | tr ' ' ':'); do
    id=${entry%%:*}
    bfile=${entry#*:}
    asm="loda/$id.asm"
    terms=$(grep -c '^[0-9]' "$bfile")
    printf '%s: loda check ... ' "$id"
    if loda check "$asm" >/dev/null 2>&1; then
        printf 'ok; repository b-file (%s terms) ... ' "$terms"
    else
        printf 'FAILED; repository b-file (%s terms) ... ' "$terms"
        status=1
    fi
    if loda eval "$asm" -t "$terms" -b 2>/dev/null | diff -q - "$bfile" >/dev/null; then
        echo ok
    else
        echo FAILED
        status=1
    fi
done
for entry in $(echo "$SCANS" | tr ' ' ':'); do
    name=${entry%%:*}
    rest=${entry#*:}
    bfile=${rest%%:*}
    terms=${rest#*:}
    asm="loda/$name.asm"
    printf '%s: first %s terms of the repository b-file ... ' "$name" "$terms"
    got=$(loda eval "$asm" -t "$terms" -b -c -1 2>/dev/null)
    want=$(head -n "$terms" "$bfile")
    if [ -n "$got" ] && [ "$got" = "$want" ]; then
        echo ok
    else
        echo FAILED
        status=1
    fi
done
exit $status
