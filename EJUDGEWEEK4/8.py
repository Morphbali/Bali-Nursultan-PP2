def primes(n):
    for i in range(2,n+1):
        ok=True
        for j in range(2,i):
            if i%j==0:
                ok=False
        if ok:
            yield i

n=int(input())

print(*primes(n))