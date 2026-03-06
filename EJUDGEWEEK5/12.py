import re

s = input()

nums = re.findall(r"\d{2,}", s)

print(" ".join(nums))