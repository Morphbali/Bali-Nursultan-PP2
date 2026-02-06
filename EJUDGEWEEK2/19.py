n = int(input())
cnt = {}

for _ in range(n):
    s, k = input().split()
    k = int(k)
    cnt[s] = cnt.get(s, 0) + k

for name in sorted(cnt):
    print(name, cnt[name])