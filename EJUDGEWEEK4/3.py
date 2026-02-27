def d(n):
    for i in range(0, n+1, 12):
        yield i

n=int(input())
for x in d(n):
    print(x,end=" ")