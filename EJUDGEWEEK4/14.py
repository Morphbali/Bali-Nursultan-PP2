from datetime import datetime, timedelta, timezone

def read():
    d, z = input().split()
    y, m, day = map(int, d.split("-"))
    s = 1 if z[3] == "+" else -1
    h, mi = map(int, z[4:].split(":"))
    tz = timezone(s * timedelta(hours=h, minutes=mi))
    return datetime(y, m, day, 0, 0, 0, tzinfo=tz)

a = read().astimezone(timezone.utc)
b = read().astimezone(timezone.utc)

print(abs(int((a - b).total_seconds())) // 86400)