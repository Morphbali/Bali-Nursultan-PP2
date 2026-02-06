n, l, r = map(int, input().split())
a = list(map(int, input().split()))

a[l-1:r] = reversed(a[l-1:r])

print(*a)