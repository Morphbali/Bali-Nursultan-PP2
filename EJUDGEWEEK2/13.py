x = int(input())

if x < 2:
    print("No")
else:
    prime = True
    i = 2
    while i * i <= x:
        if x % i == 0:
            prime = False
            break
        i += 1
    
    print("Yes" if prime else "No")