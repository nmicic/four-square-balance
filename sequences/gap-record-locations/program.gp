\\ Gap-record locations: numbers k where g(k) = A(k) - ceil(sqrt(k/4)) sets a new max.
A(n) = {
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

lista(N) = {
  my(best = -1);
  for(k = 1, N, my(g = A(k) - xmin(k));
    if(g > best, best = g; print1(k, ", ")));
  print();
}
lista(5000)   \\ raise the bound for more records (slow: definitional scan)
