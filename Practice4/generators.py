#1
def squares(n):
    for i in range(1,n+1):
        yield i*i

n=int(input())
for x in squares(n):
    print(x)

#2
def even(n):
    for i in range(0,n+1,2):
        yield i

n=int(input())
print(*even(n),sep=",")
#3
def f(n):
    for i in range(n+1):
        if i%12==0:
            yield i

n=int(input())
print(*f(n))
#4
def squares(a,b):
    for i in range(a,b+1):
        yield i*i

a,b=map(int,input().split())

for x in squares(a,b):
    print(x)