import sympy as sp


for n in range(1,10+1):
    if sp.isprime(n) and n > 2:
        continue
    for i in range(1,n+1):
        if n%i != 0:
            continue
        
        j = n//i
        print(n,i,j)

