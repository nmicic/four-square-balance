\\ Minimal spread: s(n) = min over all four-square representations of (x - w),
\\ n = x^2+y^2+z^2+w^2 with x >= y >= z >= w >= 0. The tightest-cluster objective.
\\ NOTE: the minimum spread is NOT always attained at the smallest x, so the x-loop
\\ must climb past x = a(n) -- do not prune it the way a minimal-largest-part scan would.
sval(n) = {
  my(b = oo, root = sqrtint(n\4));
  forstep(w = root, 0, -1,
    if(4*w^2 > n, next);
    if(sqrtint((n+3)\4) - w >= b, break);
    my(r1 = n - w^2, xlo = sqrtint(r1\3)); while(3*xlo^2 < r1, xlo++);
    if(w > xlo, xlo = w);
    for(x = xlo, n,
      if(x - w >= b, break);
      my(m2 = r1 - x^2); if(m2 < 0, break);
      if(m2 > 2*x^2, next); if(m2 < 2*w^2, break);
      my(yhi = min(x, sqrtint(m2)), ylo = sqrtint(m2\2)); while(ylo^2*2 < m2, ylo++);
      for(y = ylo, yhi,
        my(z2 = m2 - y^2);
        if(issquare(z2), my(z = sqrtint(z2));
          if(z >= w && z <= y, b = x - w; break(2))))));
  b }

print(vector(40, n, sval(n)))
