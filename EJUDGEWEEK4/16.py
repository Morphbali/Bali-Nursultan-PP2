from datetime import datetime,timedelta

def f(s):
    t,z=s.split(" UTC")
    d=datetime.strptime(t,"%Y-%m-%d %H:%M:%S")
    h,m=map(int,z.split(":"))
    return d-timedelta(hours=h,minutes=m)

a=f(input())
b=f(input())

print(int((b-a).total_seconds()))