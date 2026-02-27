def cycle(a,k):
    for i in range(k):
        for x in a:
            yield x

a=input().split()
k=int(input())

print(*cycle(a,k))