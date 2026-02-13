s = input().strip()

to_digit = {
    "ZER":"0","ONE":"1","TWO":"2","THR":"3","FOU":"4",
    "FIV":"5","SIX":"6","SEV":"7","EIG":"8","NIN":"9"
}
to_trip = {v:k for k,v in to_digit.items()}

pos = -1
op = ''
for i,c in enumerate(s):
    if c in '+-*':
        pos = i
        op = c
        break

left = s[:pos]
right = s[pos+1:]

def parse(numstr):
    return int(''.join(to_digit[numstr[i:i+3]] for i in range(0,len(numstr),3)))

a = parse(left)
b = parse(right)

if op == '+':
    res = a + b
elif op == '-':
    res = a - b
else:
    res = a * b

res_str = str(res)
print(''.join(to_trip[d] for d in res_str))
