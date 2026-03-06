import re

with open("raw.txt", encoding="utf-8") as f:
    text = f.read()

prices = re.findall(r"\d[\d\s]*,\d{2}", text)

date_time = re.search(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text)

payment = re.search(r"Банковская карта", text)

total = re.search(r"ИТОГО:\s*\n?([\d\s]+,\d{2})", text)

items = re.findall(r"\d+\.\s*\n([^\n]+)", text)

print("Items:")
for i in items:
    print("-", i)

print("\nPrices:")
for p in prices:
    print(p)

if total:
    print("\nTotal:", total.group(1))

if date_time:
    print("Date and Time:", date_time.group())

if payment:
    print("Payment Method: Card")