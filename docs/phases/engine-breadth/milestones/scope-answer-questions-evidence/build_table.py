"""Render the per-fact audit table (P0) from groups.py, probe-output.json, probe-flip-output.json and
probe-extra-output.json. Run from anywhere: ``python3 build_table.py`` prints markdown to stdout."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(HERE))
from groups import GROUPS  # noqa: E402

held = {c["root"]: c["lines_held"] for c in json.loads((HERE / "probe-output.json").read_text())["cases"]}
flip = {c["root"]: c for c in json.loads((HERE / "probe-flip-output.json").read_text())["cases"]}
extra = json.loads((HERE / "probe-extra-output.json").read_text())["cases"]


def effect(root):
    c = flip.get(root)
    if root == "f1098-scope.no-mortgage-statement":
        e = [x for x in extra if x["root"] == root][0]
        return f"false: {len(e['changed'])} lines change (no statement is recorded, so the statement path computes the same)"
    if not c or c["status"] != "ran":
        return "not run"
    ch = c["changed"]
    blocked = [k for k, v in ch.items() if v["flipped"]["disposition"] == "blocked"]
    guard = [k for k, v in ch.items() if v["flipped"]["disposition"] == "guard_inapplicable"]
    valued = [k for k, v in ch.items() if v["flipped"]["disposition"] not in ("blocked", "guard_inapplicable")]
    parts = []
    if blocked:
        parts.append(f"{len(blocked)} lines blocked")
    if guard:
        parts.append("not computed: " + ", ".join(guard))
    if valued:
        parts.append("values change: " + ", ".join(
            f"{k} {ch[k]['as_built']['value']}->{ch[k]['flipped']['value']}" for k in valued[:3]) + ("..." if len(valued) > 3 else ""))
    return f"{c['flipped_value']}: " + ("; ".join(parts) if parts else "no line changes on this return")


def lines(root):
    h = held[root]
    names = [x["section"].replace("line-", "") for x in h]
    return f"{len(h)}: " + ", ".join(names[:5]) + (", ..." if len(names) > 5 else "")


if not (len(sys.argv) > 1 and sys.argv[1] == "groups"):
    print("| Q | Fact (tax.us.2025.) | Lines held when withheld | Non-baseline value: effect | Question yes records | Question no records |")
    print("| --- | --- | --- | --- | --- | --- |")
    for gid, text, members, kind in GROUPS:
        for fact, pol in members:
            if pol == "choice":
                continue
            yes_ = {"pos": "yes", "abs": "no"}[pol]
            no_ = {"pos": "no", "abs": "yes"}[pol]
            if fact.startswith("f1098"):
                yes_, no_ = "false", "true"
            if kind == "absence":
                yes_ = "not determined (some member is \"no\"; outside the supported class)"
            if kind == "conjunction":
                no_ = "not determined (some member is \"no\"; outside the supported class)"
            print(f"| {gid} | {fact} | {lines(fact)} | {effect(fact)} | {yes_} | {no_} |")



if len(sys.argv) > 1 and sys.argv[1] == "groups":
    from groups import META
    print("| Q | Question (yes = present) | Facts it settles | Asked when | What the rules do with the values |")
    print("| --- | --- | --- | --- | --- |")
    for gid, text, members, kind in GROUPS:
        asked, rules = META[gid]
        facts_ = ", ".join(m[0] for m in members)
        print(f"| {gid} | {text} | {facts_} | {asked} | {rules} |")
