x1,y1=map(float,input().split())
x2,y2=map(float,input().split())

if abs(y1+y2)<1e-12:
    x=x1
else:
    t=y1/(y1+y2)
    x=x1+t*(x2-x1)

print(f"{x:.10f} {0.0:.10f}")