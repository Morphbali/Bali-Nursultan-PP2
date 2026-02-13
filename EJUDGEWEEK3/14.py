n = int(input())
arr = list(map(int, input().split()))
q = int(input())

for _ in range(q):
    parts = input().split()
    op = parts[0]
    
    if op == "add":
        x = int(parts[1])
        f = lambda a, x=x: a + x
    elif op == "multiply":
        x = int(parts[1])
        f = lambda a, x=x: a * x
    elif op == "power":
        x = int(parts[1])
        f = lambda a, x=x: a ** x
    else:
        f = lambda a: abs(a)
    
    arr = list(map(f, arr))

print(*arr)
