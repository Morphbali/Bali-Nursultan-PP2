import json
import sys

def apply_patch(src, patch):
    for k, v in patch.items():
        if v is None:
            src.pop(k, None)
        else:
            if k in src and isinstance(src[k], dict) and isinstance(v, dict):
                apply_patch(src[k], v)
            else:
                src[k] = v
    return src

source = json.loads(sys.stdin.readline())
patch = json.loads(sys.stdin.readline())

result = apply_patch(source, patch)

print(json.dumps(result, sort_keys=True, separators=(",", ":")))