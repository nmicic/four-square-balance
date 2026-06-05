/* records.gp -- the two PARI/GP variations for the balance-gap record sequence.
 *
 * Run:  gp -q src/records.gp
 *
 * VARIATION 1 (DEFINITIONAL): from first principles. A(k) climbs the largest part
 *   until the remainder is a sum of three squares all <= the cap (Legendre test),
 *   exactly the sequence definition. It reproduces the sequence from its definition,
 *   no pattern assumed. Slow (scans).
 *
 * VARIATION 2 (CONSTRUCTIVE / CLOSED FORM): after the seeds 1,11,53 the observed
 *   record chains start at 96, 224, and 2816 and then follow n -> 4n. Both the
 *   decomposition and gap are then closed-form; no search. Fast; matches Variation 1
 *   on the scanned range. Beyond the retained scan, completeness is conjectural.
 */

/* ---- shared definitional pieces ---- */
A(n) = {                                   \\ minimal possible largest part x
  my(x = sqrtint((n+3)\4)); while(4*x^2 < n, x++);
  while(1,
    my(r1 = n - x^2);
    if(r1 == 0, return(x));
    forstep(y = min(x, sqrtint(r1)), 0, -1,
      my(m = r1 - y^2);
      for(z = 0, min(y, sqrtint(m)),
        if(issquare(m - z^2) && sqrtint(m - z^2) <= y, return(x))));
    x++)}
xmin(n) = {my(x = sqrtint((n+3)\4)); while(4*x^2 < n, x++); x};
gap(n)  = A(n) - xmin(n);

/* ===== VARIATION 1 -- definitional record scan (the submission %o) ===== */
recordsDef(N) = {                          \\ locations where gap reaches a new max, k<=N
  my(best = -1, loc = List(), val = List());
  for(k = 1, N,
    my(g = gap(k));
    if(g > best, best = g; listput(loc, k); listput(val, g)));
  [Vec(loc), Vec(val)];
}

/* ===== VARIATION 2 -- constructive / closed form (the pattern) ===== */
/* chains, indexed by m >= 0:
 *   96*4^m   = 6*4^(m+2):  x = 8*2^m
 *   224*4^m  = 14*4^(m+2): x = 12*2^m
 *   2816*4^m = 11*4^(m+4): x = 40*2^m
 * gap is closed form: x - ceil(sqrt(n/4)).  */
csqrt(c, p) = {my(v = c << (2*p), r = sqrtint(v)); if(r^2 == v, r, r + 1)};  \\ ceil(sqrt(c)*2^p)
recordsClosed(B) = {                       \\ all records with n <= B, as [n, x, g] rows
  my(L = List([[1,1,0],[11,3,1],[53,6,2]]));
  my(j = 2); while(6*4^j  <= B, listput(L, [6*4^j,  2^(j+1),   2^(j+1)   - csqrt(6, j-1)]); j++);
  j = 2;     while(14*4^j <= B, listput(L, [14*4^j, 3*2^j,     3*2^j     - csqrt(14, j-1)]); j++);
  j = 4;     while(11*4^j <= B, listput(L, [11*4^j, 5*2^(j-1), 5*2^(j-1) - csqrt(11, j-1)]); j++);
  vecsort(Vec(L), 1);                      \\ sort rows by n
}

/* ---- self-test: the two variations must agree on the scanned range ---- */
{
  my(B = 2*10^4);   \\ demo bound: definitional A() is the honest (slow) from-definition
                    \\ program, not a fast scanner; 13 records here is enough to show the
                    \\ two variations agree. The chain continuation below is conjectural
                    \\ outside the retained scan.
  my(d = recordsDef(B));
  my(locD = d[1], valD = d[2]);
  my(c = recordsClosed(B));
  my(locC = vector(#c, i, c[i][1]), valC = vector(#c, i, c[i][3]));
  print("Variation 1 (definitional) locations <= ", B, ":");
  print("  ", locD);
  print("Variation 1 gap values:");
  print("  ", valD);
  print("Variation 2 (closed form) locations <= ", B, ":");
  print("  ", locC);
  if(locD == locC && valD == valC,
     print("AGREE: definitional == closed form on 1..", B, " (", #locD, " records)"),
     print("*** DISAGREE ***"));
  \\ conjectural continuation: exact chain arithmetic, but completeness beyond
  \\ the retained scan is not proved here.
  print("\nConjectural three-chain continuation to 10^12 (n  x  g):");
  my(e = recordsClosed(10^12));
  for(i = 1, #e, print("  ", e[i]));
}
