import json

MISSING = object()

def dump(v):
    if v is MISSING:
        return "<missing>"
    return json.dumps(v, separators=(",", ":"), sort_keys=True)

def diff(a, b, p=""):
    out = []
    if type(a) == dict and type(b) == dict:
        keys = set(a) | set(b)
        for k in keys:
            na = a.get(k, MISSING)
            nb = b.get(k, MISSING)
            np = k if p == "" else p + "." + k
            if na is MISSING or nb is MISSING:
                out.append((np, dump(na), dump(nb)))
            else:
                out += diff(na, nb, np)
    else:
        if a != b:
            out.append((p, dump(a), dump(b)))
    return out

a = json.loads(input())
b = json.loads(input())

ans = diff(a, b)
ans.sort(key=lambda x: x[0])

if not ans:
    print("No differences")
else:
    for p, x, y in ans:
        print(f"{p} : {x} -> {y}")