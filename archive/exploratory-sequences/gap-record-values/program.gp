\\ Gap-record values: the value g whenever g(k) = A(k) - ceil(sqrt(k/4)) sets a new max.
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
xmin(n) = my(x = sqrtint((n+3)\4)); while(4*x^2 < n, x++); x;

{
  my(best = -1);
  for(k = 1, 10^5, my(g = A(k) - xmin(k));     \\ raise the bound for more records
    if(g > best, best = g; print1(g, ", ")));
  print();
}
