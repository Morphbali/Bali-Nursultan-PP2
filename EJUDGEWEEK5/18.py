import re

s = input()
p = input()

pattern = re.escape(p)

matches = re.findall(pattern, s)

print(len(matches))