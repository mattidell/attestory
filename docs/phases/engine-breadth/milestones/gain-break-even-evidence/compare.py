"""Compare the gain-break-even P0 runs (runs.json) with hand values (hand.py).

Run: python3 compare.py   (after cases.py). Writes comparison.json beside this file.

Checked per run: Schedule D lines 1a, 1b, 2, 3, 6, 7, 8a, 8b, 9, 10, 13, 14,
15, 16 and Form 1040 lines 7a, 15, 16 on the saved page (value and a
published disposition); the Form 8949 part totals (columns d, e, g per box)
and whether Form 8949 is required; for a net gain on lines 15 and 16, the
worksheet lines the hand figures; no blocked rule, no open question, run
saturated. The four code W probes are checked against the ADR-0062 Decision 2
bound instead (blocked, not published).
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


hand = _load("gbe_p0_compare_hand", HERE / "hand.py")
# The case table only (cases.py would import the coordinator; read its literals instead).
_src = (HERE / "cases.py").read_text(encoding="utf-8")
_ns: dict[str, Any] = {"Any": Any}
exec(_src[_src.index("SPECS: dict"):_src.index("def column_h")], _ns)  # noqa: S102 - our own literal tables
SPECS, MIXED = _ns["SPECS"], _ns["MIXED"]

PAGE_LINES = tuple(f"schedule-d.line-{n}" for n in ("1a", "1b", "2", "3", "6", "7", "8a", "8b", "9", "10", "13", "14",
                                                   "15", "16")) + ("form1040.line-7a", "form1040.line-15",
                                                                   "form1040.line-16")
PUBLISHED_OK = ("published_value", "computed_zero", "closure_backed_zero")
WORKSHEET = {"line-3": None, "line-5": "qdcg-worksheet.line-5", "line-9": "qdcg-worksheet.line-9",
             "line-17": "qdcg-worksheet.line-17", "line-18": "qdcg-worksheet.line-18",
             "line-22": "qdcg-worksheet.line-22", "line-24": "qdcg-worksheet.line-24"}


def sales_of(key: str) -> list[tuple[str, str, dict[str, Any]]]:
    parts = key.split("/")
    if parts[0] == "mixed":
        return MIXED[parts[1]]
    path, term, shape, _status = parts
    return [(path, term, SPECS[(path, shape)])]


def main() -> None:
    runs = json.loads((HERE / "runs.json").read_text(encoding="utf-8"))["runs"]
    rows: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    probes: dict[str, Any] = {}
    for key, run in runs.items():
        status = key.split("/")[-1]
        if "/probe-" in key:
            blocked = run.get("blocked_rules") or []
            sd = run.get("lines", {}).get("schedule-d.line-16", {})
            probes[key] = {"stop": run.get("stop"), "error": run.get("error"), "message": run.get("message"),
                           "blocked_rules": blocked, "line16": sd, "line7a": run.get("lines", {}).get("form1040.line-7a"),
                           "questions": run.get("questions"),
                           "bound_held": bool(run.get("error") or blocked) and sd.get("disposition") not in ("published_value",)}
            if not probes[key]["bound_held"]:
                mismatches.append({"case": key, "line": "ADR-0062 Decision 2 bound", "engine": sd, "hand": "blocked"})
            continue
        want = hand.values(sales_of(key), status)
        row: dict[str, Any] = {"case": key, "tax_path": want["tax_path"], "checks": {}}
        if "error" in run or "refusal" in run:
            mismatches.append({"case": key, "line": "run", "engine": run.get("error") or run.get("refusal"), "hand": "saturated"})
            rows.append(row)
            continue
        for what, got, expected in (("stop", run.get("stop"), "saturated"), ("blocked_rules", run.get("blocked_rules"), []),
                                    ("questions", run.get("questions"), [])):
            if got != expected:
                mismatches.append({"case": key, "line": what, "engine": got, "hand": expected})
        for line in PAGE_LINES:
            got = run["lines"].get(line) or {}
            ok = got.get("value") == want[line] and got.get("disposition") in PUBLISHED_OK
            row["checks"][line] = {"engine": got.get("value"), "disposition": got.get("disposition"), "hand": want[line], "ok": ok}
            if not ok:
                mismatches.append({"case": key, "line": line, "engine": got, "hand": want[line]})
        f8949 = (run.get("attachment_parts") or {}).get("form8949") or {}
        got_parts = f8949.get("parts") or {}
        ok = got_parts == want["form8949_parts"]
        row["checks"]["form8949.parts"] = {"engine": got_parts, "hand": want["form8949_parts"], "ok": ok}
        if not ok:
            mismatches.append({"case": key, "line": "form8949.parts", "engine": got_parts, "hand": want["form8949_parts"]})
        page_required = run.get("attachments", {}).get("f8949")
        required = bool(f8949.get("required"))
        ok = required == want["form8949_required"]
        row["checks"]["form8949.required"] = {"engine": required, "page": page_required, "hand": want["form8949_required"], "ok": ok}
        if not ok:
            mismatches.append({"case": key, "line": "form8949.required", "engine": [required, page_required], "hand": want["form8949_required"]})
        sd_page = run.get("attachments", {}).get("schedule-d")
        row["checks"]["schedule-d.attachment"] = {"engine": sd_page, "hand": "published", "ok": sd_page == "published"}
        if sd_page != "published":
            mismatches.append({"case": key, "line": "schedule-d.attachment", "engine": sd_page, "hand": "published"})
        pref = run["published"].get("capital-gains.selected-preferential-base")
        want_pref = min(want["schedule-d.line-15"], want["schedule-d.line-16"]) if want["schedule-d.line-15"] > 0 else 0
        row["checks"]["preferential-base"] = {"engine": pref, "hand": want_pref, "ok": pref == want_pref}
        if pref != want_pref:
            mismatches.append({"case": key, "line": "preferential-base", "engine": pref, "hand": want_pref})
        if "qdcg" in want:
            for name, symbol in WORKSHEET.items():
                if symbol is None:
                    continue
                engine = run["published"].get(symbol)
                ok = engine is not None and abs(float(engine) - float(want["qdcg"][name])) < 0.005
                row["checks"]["qdcg." + name] = {"engine": engine, "hand": want["qdcg"][name], "ok": ok}
                if not ok:
                    mismatches.append({"case": key, "line": "qdcg." + name, "engine": engine, "hand": want["qdcg"][name]})
        row["engine_tax_path_published"] = sorted(s for s in run["published"] if s.startswith("qdcg-worksheet.")) != []
        rows.append(row)
    body = {
        "runs": len(runs),
        "checked_runs": len(rows),
        "checks": sum(len(r["checks"]) for r in rows),
        "mismatches": mismatches,
        "probes": probes,
        "rows": rows,
    }
    (HERE / "comparison.json").write_text(json.dumps(body, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: body[k] for k in ("runs", "checked_runs", "checks")}, indent=1))
    print("mismatches:", len(mismatches))
    for m in mismatches[:40]:
        print(" ", json.dumps(m)[:300])
    for k, p in probes.items():
        print("probe", k, json.dumps({x: p[x] for x in ("stop", "error", "blocked_rules", "bound_held")})[:400])


if __name__ == "__main__":
    main()
