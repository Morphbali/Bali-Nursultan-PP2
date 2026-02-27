g=0
n=0

m=int(input())
for _ in range(m):
    s,x=input().split()
    x=int(x)
    if s=="global":
        g+=x
    elif s=="nonlocal":
        n+=x

print(g,n)