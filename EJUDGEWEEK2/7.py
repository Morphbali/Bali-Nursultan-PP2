n = int(input())
arr = list(map(int, input().split()))

max_val = arr[0]
pos = 1

for i in range(1, n):
    if arr[i] > max_val:
        max_val = arr[i]
        pos = i + 1

print(pos)