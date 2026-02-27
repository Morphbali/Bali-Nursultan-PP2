from datetime import datetime, timedelta, timezone

def parse(s):
    d, z = s.split()
    y, m, day = map(int, d.split("-"))
    sign = 1 if z[3] == "+" else -1
    hh, mm = map(int, z[4:].split(":"))
    tz = timezone(sign * timedelta(hours=hh, minutes=mm))
    return datetime(y, m, day, 0, 0, 0, tzinfo=tz)

def leap(y):
    return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)

def bday(year, m, d, tz):
    if m == 2 and d == 29 and not leap(year):
        d = 28
    return datetime(year, m, d, 0, 0, 0, tzinfo=tz)

birth = parse(input())
now = parse(input())

bm, bd = birth.month, birth.day
btz = birth.tzinfo

now_utc = now.astimezone(timezone.utc)
cand_utc = bday(now.year, bm, bd, btz).astimezone(timezone.utc)

if cand_utc < now_utc:
    cand_utc = bday(now.year + 1, bm, bd, btz).astimezone(timezone.utc)

delta = int((cand_utc - now_utc).total_seconds())

print(0 if delta == 0 else (delta + 86400 - 1) // 86400)