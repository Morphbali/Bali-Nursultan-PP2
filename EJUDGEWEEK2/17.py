n = int(input())

freq = {}

for _ in range(n):
    num = input().strip()
    freq[num] = freq.get(num, 0) + 1

count = 0
for v in freq.values():
    if v == 3:
        count += 1

print(count)