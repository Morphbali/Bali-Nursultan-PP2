import importlib

q=int(input())

for _ in range(q):
    m,a=input().split()
    try:
        mod=importlib.import_module(m)
    except Exception:
        print("MODULE_NOT_FOUND")
        continue

    if not hasattr(mod,a):
        print("ATTRIBUTE_NOT_FOUND")
        continue

    print("CALLABLE" if callable(getattr(mod,a)) else "VALUE")