import math

R=float(input())
x1,y1=map(float,input().split())
x2,y2=map(float,input().split())

dx,dy=x2-x1,y2-y1
L=math.hypot(dx,dy)

if L==0.0:
    ans=0.0
else:
    a=dx*dx+dy*dy
    b=2*(x1*dx+y1*dy)
    c=x1*x1+y1*y1-R*R
    d=b*b-4*a*c
    if d<0:
        ans=0.0
    else:
        s=math.sqrt(max(0.0,d))
        t1=(-b-s)/(2*a)
        t2=(-b+s)/(2*a)
        lo=min(t1,t2)
        hi=max(t1,t2)
        lo=max(0.0,lo)
        hi=min(1.0,hi)
        ans=max(0.0,hi-lo)*L

print(f"{ans:.10f}")