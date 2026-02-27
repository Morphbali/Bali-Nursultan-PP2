def p(n):
    for i in range(n+1):
        yield 2**i

n=int(input())

print(*p(n))