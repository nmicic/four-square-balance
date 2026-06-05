\\ All-prime decomposition: numbers k whose canonical four-square representation
\\ k = x^2+y^2+z^2+w^2 (x>=y>=z>=w>=0, minimizing x then y then z) has all parts prime.
minquad(k) = {
  my(x = sqrtint((k+3)\4)); while(4*x^2 < k, x++);
  while(1,
    my(r1 = k - x^2, ylo = sqrtint((r1+2)\3)); while(3*ylo^2 < r1, ylo++);
    for(y = ylo, min(x, sqrtint(r1)),
      my(m = r1 - y^2, zlo = sqrtint((m+1)\2)); while(2*zlo^2 < m, zlo++);
      for(z = zlo, min(y, sqrtint(m)),
        if(issquare(m - z^2), return([x, y, z, sqrtint(m - z^2)]))));
    x++)}

isok(k) = {my(t = minquad(k)); isprime(t[1]) && isprime(t[2]) && isprime(t[3]) && isprime(t[4]);}
print(select(isok, [1..200]))
