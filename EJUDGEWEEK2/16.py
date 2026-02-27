n = int(input())
a = list(map(int, input()))

seen = set()

for x in a:
    if x in seen:
        print("NO")
    else:
        print("YES")
        seen.add(x)