import json,re

J=json.loads(input())
q=int(input())

for _ in range(q):
    p=input().strip()
    cur=J
    ok=True
    for t in re.findall(r'[^.\[\]]+|\[\d+\]',p):
        if t[0]=='[':
            i=int(t[1:-1])
            if type(cur)!=list or i<0 or i>=len(cur):
                ok=False
                break
            cur=cur[i]
        else:
            if type(cur)!=dict or t not in cur:
                ok=False
                break
            cur=cur[t]
    print(json.dumps(cur,separators=(",",":")) if ok else "NOT_FOUND")