\\ Minimal largest part: a(n) = least x with n = x^2+y^2+z^2+w^2, x>=y>=z>=w>=0.
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

print(vector(24, n, A(n)))
