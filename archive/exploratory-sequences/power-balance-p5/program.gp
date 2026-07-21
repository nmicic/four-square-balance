\\ Power-balance record locations, p = 5: representable N = a^5+b^5+c^5+d^5
\\ (0 <= a <= b <= c <= d), scanned in increasing order; print N whenever
\\ g(N) = minmax(N) - lb(N) sets a new max, where minmax(N) is the least possible
\\ largest part d and lb(N) is the least m with 4*m^5 >= N.
lista(Nmax) = {
  my(p = 5, K = 1, L = List(), v, best = -1);
  while((K + 1)^p <= Nmax, K++);
  for(a = 0, K,
    my(pa = a^p); if(pa > Nmax, break);
    for(b = a, K,
      my(s2 = pa + b^p); if(s2 > Nmax, break);
      for(c = b, K,
        my(s3 = s2 + c^p); if(s3 > Nmax, break);
        for(d = c, K,
          my(s = s3 + d^p); if(s > Nmax, break);
          if(s, listput(L, s*(K + 1) + d))))));
  v = vecsort(Vec(L));
  for(i = 1, #v,
    if(i > 1 && v[i]\(K + 1) == v[i-1]\(K + 1), next);  \\ first pair per N has minimal d
    my(n = v[i]\(K + 1), dmin = v[i]%(K + 1), m = sqrtnint(n\4, p) + 1, g);
    while(4*m^p < n, m++); while(m > 1 && 4*(m - 1)^p >= n, m--);
    g = dmin - m;
    if(g > best, best = g; print1(n, ", ")));
  print();
}
lista(800000)   \\ bound of the archived b-file; raise for more records
