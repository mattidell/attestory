"""P0 survey (itemization-cents): every rule in a core package that rounds a sum before
another rule reads it, the lines that read it, and the attachment row sets that tie out
against it. Static: reads packages/content only; never runs a return.

Usage: python3 survey.py [package path]   (default: core v65). Prints JSON.
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
DEFAULT = CONTENT / "package.core-calculations.v65.json"


def walk(n):
    if isinstance(n, dict):
        yield n
        for v in n.values():
            yield from walk(v)
    elif isinstance(n, list):
        for v in n:
            yield from walk(v)


def index():
    out = {}
    for f in glob.glob(str(CONTENT / "*.json")):
        try:
            j = json.loads(Path(f).read_text())
        except ValueError:
            continue
        if isinstance(j, dict) and "id" in j and "version" in j:
            out[(j["id"], j["version"])] = (Path(f).name, j)
    return out


def refs(node):
    return sorted({n["name"] for n in walk(node) if n.get("op") == "ref" and n["name"] != "rounding.convention"})


def collects(node):
    return sorted({(n["name"], n["source_set"]) for n in walk(node) if n.get("op") == "collect"})


def survey(package_path: Path = DEFAULT):
    pkg = json.loads(package_path.read_text())
    idx = index()
    members = [(m, idx[(m["id"], m["version"])][1]) for m in pkg["members"]]
    rules = [j for m, j in members if m["role"] == "computation" and "publishes" in j]
    by_symbol = {}
    for r in rules:
        by_symbol.setdefault(r["publishes"], []).append(r)
    fields = {j["binds_symbol"]: j["id"] for m, j in members if m["schema"].startswith("form-field") and "binds_symbol" in j}
    readers = {}
    for r in rules:
        body = {k: v for k, v in r.items() if k not in ("pins", "blocked", "citations", "notes")}
        for s in set(refs(body)) | set(r.get("requires") or []):
            readers.setdefault(s, set()).add(r["id"])

    # attachments: tie-out symbols and the row sets that tie against each subtotal
    attach = []
    tie_by_symbol = {}
    for m, j in members:
        if m["role"] != "attachment-rule":
            continue
        for part in j["itemizations"]:
            for rs in part["row_sets"]:
                tie_by_symbol.setdefault(rs["subtotal_symbol"], []).append({
                    "attachment": j["id"], "version": j["version"], "part": part["part_id"],
                    "family": rs["rows"].get("source_family", {}).get("id"),
                    "member": rs["rows"].get("member_fact_type", {}).get("id"),
                    "kind": "row_set"})
            for a in part.get("adjustment_rows", []):
                specs = [a] + [p for p in (a.get("selection") or {}).get("paths", [])]
                for sp in specs:
                    if "subtotal_symbol" in sp:
                        tie_by_symbol.setdefault(sp["subtotal_symbol"], []).append({
                            "attachment": j["id"], "version": j["version"], "part": part["part_id"],
                            "kind": "adjustment_row:" + a["kind"]})
            attach.append({"attachment": j["id"], "version": j["version"], "part": part["part_id"],
                           "line_symbol": part["tie_out"]["line_symbol"],
                           "positive_subtotals": part["tie_out"].get("positive_subtotals"),
                           "adjustment_subtotals": part["tie_out"].get("adjustment_subtotals")})

    rounders = []
    for r in rules:
        rounds = [n for n in walk(r.get("value")) if n.get("op") == "round"]
        if not rounds:
            continue
        inner = [n["value"] for n in rounds]
        kind = ("subtotal-of-collect" if any(collects(i) for i in inner)
                else "sum-of-refs" if any(i.get("op") == "add" and refs(i) for i in inner)
                else "round-of-ref" if any(i.get("op") == "ref" for i in inner) else "other")
        sym = r["publishes"]
        rounders.append({
            "rule": r["id"], "version": r["version"], "publishes": sym, "kind": kind,
            "round_count": len(rounds),
            "collects": [c for i in inner for c in collects(i)],
            "inner_refs": sorted({x for i in inner for x in refs(i)}),
            "read_by": sorted(readers.get(sym, [])),
            "ties_out_against": tie_by_symbol.get(sym, []),
            "ties_out_as_line": [a for a in attach if a["line_symbol"] == sym],
            "bound_field": fields.get(sym)})

    # subtotals that are NOT rounded but tie out (already carry cents)
    unrounded_tie = []
    rounded_syms = {x["publishes"] for x in rounders}
    for sym, rows in sorted(tie_by_symbol.items()):
        if sym not in rounded_syms:
            prod = by_symbol.get(sym, [])
            unrounded_tie.append({"symbol": sym, "rules": [(p["id"], p["version"]) for p in prod], "tie": rows})
    return {"package": f'{pkg["id"]} {pkg["version"]}', "rounders": rounders,
            "attachment_parts": attach, "tie_symbols_not_rounded": unrounded_tie}


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    print(json.dumps(survey(path), indent=1, sort_keys=True))
