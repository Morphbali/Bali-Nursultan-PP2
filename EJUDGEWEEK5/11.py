import re

s = input()

letters = re.findall(r"[A-Z]", s)

print(len(letters))