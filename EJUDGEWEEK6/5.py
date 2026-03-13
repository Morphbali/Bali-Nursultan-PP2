s = input().lower()
print("Yes" if any(c in "aeiou" for c in s) else "No")