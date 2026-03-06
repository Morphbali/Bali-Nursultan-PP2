import re

s = input()

m = re.search(r"\S+@\S+\.\S+", s)

if m:
    print(m.group(0))
else:
    print("No email")