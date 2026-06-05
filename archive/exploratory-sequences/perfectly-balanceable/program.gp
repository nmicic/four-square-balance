\\ Perfectly balanceable: numbers k with A(k) == ceil(sqrt(k/4)) (balance gap 0).
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

isok(k) = A(k) == xmin(k);
print(select(isok, [1..200]))
