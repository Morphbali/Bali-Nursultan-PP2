import math

R=float(input())
x1,y1=map(float,input().split())
x2,y2=map(float,input().split())

d=math.hypot(x1-x2,y1-y2)

d1=math.hypot(x1,y1)
d2=math.hypot(x2,y2)

if d1>=R and d2>=R:
    h=abs(x1*y2-x2*y1)/d
    if h>=R:
        print(d)
    else:
        a=math.sqrt(d1*d1-R*R)
        b=math.sqrt(d2*d2-R*R)

        ang1=math.acos(R/d1)
        ang2=math.acos(R/d2)

        ang=math.acos((x1*x2+y1*y2)/(d1*d2))

        arc=R*(ang-ang1-ang2)

        print(a+b+arc)
else:
    print(d)