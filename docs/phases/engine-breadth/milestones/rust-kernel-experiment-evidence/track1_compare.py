"""Compare two Track 1 dumps list by list: python3 track1_compare.py <dump-a.json> <dump-b.json> [--ordered]

Prints how many lists are identical (result hash, page hash, error class and
message) and whether the validation error lists are identical. Exits 1 on any
difference. Package validation's issue order follows set iteration, so run
the validation comparison from dumps made with PYTHONHASHSEED=0
(``track1_dump.py <label> <scratch> --validation-only``).
"""
import json
import sys

a, b = (json.load(open(p)) for p in sys.argv[1:3])
la, lb = a.get("lists"), b.get("lists")
bad = 0
if la is not None and lb is not None:
    same = [k for k in la if k in lb and la[k] == lb[k]]
    diff = sorted(set(la) ^ set(lb)) + [k for k in la if k in lb and la[k] != lb[k]]
    print({"lists_identical": len(same), "lists_total": len(la), "different": diff[:10]})
    bad += len(diff)
va, vb = a.get("validation", a), b.get("validation", b)
def issues(v):
    return sorted(json.dumps(i, sort_keys=True) for i in v.get("issues", []))


same_v = {k: va[k] == vb[k] for k in va if isinstance(va[k], dict)}
same_multiset = {k: issues(va[k]) == issues(vb[k]) for k in va if isinstance(va[k], dict)}
print({"validation_identical_in_order": same_v, "validation_same_multiset_of_errors": same_multiset})
# Order is only comparable under one fixed PYTHONHASHSEED (the pristine code's
# issue order follows set iteration); the multiset must always agree.
bad += sum(not v for v in same_multiset.values())
if "--ordered" in sys.argv:
    bad += sum(not v for v in same_v.values())
sys.exit(1 if bad else 0)
