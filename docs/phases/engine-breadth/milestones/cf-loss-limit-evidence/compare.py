"""Compare the cf-loss-limit P0 runs (runs.json) with hand values (hand.py) and the A/D control.

Run: python3 compare.py   (after cases.py). Writes comparison.json beside this file.

Sign convention: Schedule D line 21 is entered on the form in parentheses
(a loss); the engine publishes it as the positive amount of that loss (rule
schedule-d-line21 v1: 0 - line 16, capped by the parameter). The check is
engine == -hand. Every other line is signed on both sides.
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


hand = _load("cfl_p0_compare_hand", HERE / "hand.py")
LIMIT = {"married_filing_separately": 1500}
SHAPES = {"st": lambda loss: (-loss, 0), "lt": lambda loss: (0, -loss),
          "both": lambda loss: (-(loss - loss // 2), -(loss // 2))}
SIZES = {"below": lambda limit: limit // 2, "at": lambda limit: limit, "above": lambda limit: limit + 2000}
ROUTE_LINES = {"cf": ("schedule-d.line-3", "schedule-d.line-10"), "ad": ("schedule-d.line-1a", "schedule-d.line-8a")}
COMPARED = ("schedule-d.line-7", "schedule-d.line-15", "schedule-d.line-16", "schedule-d.line-21",
            "form1040.line-7a", "form1040.line-15")
PARITY_SKIP = {"schedule-d.line-1a", "schedule-d.line-3", "schedule-d.line-8a", "schedule-d.line-10"}


def main() -> None:
    runs = json.loads((HERE / "runs.json").read_text(encoding="utf-8"))["runs"]
    rows: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    for key, run in runs.items():
        route, shape, status, size = key.split("/")
        loss = SIZES[size](LIMIT.get(status, 3000))
        st, lt = SHAPES[shape](loss)
        want = hand.values(status, st, lt)
        assert run.get("stop") == "saturated" and not run.get("blocked_rules") and not run.get("questions"), key
        got = run["lines"]
        row: dict[str, Any] = {"case": key, "st": st, "lt": lt, "checks": {}}
        for line in COMPARED:
            engine = got[line]["value"]
            expected = -want[line] if line == "schedule-d.line-21" else want[line]
            ok = engine == expected and got[line]["disposition"] in ("published_value", "computed_zero")
            row["checks"][line] = {"engine": engine, "hand": want[line], "disposition": got[line]["disposition"], "ok": ok}
            if not ok:
                mismatches.append({"case": key, "line": line, "engine": engine, "hand": want[line]})
        # The sale lands on its own box line, and the other route's line is zero.
        own_st, own_lt = ROUTE_LINES[route]
        other = ROUTE_LINES["ad" if route == "cf" else "cf"]
        for line, expected in ((own_st, st), (own_lt, lt), (other[0], 0), (other[1], 0)):
            ok = got[line]["value"] == expected
            row["checks"][line] = {"engine": got[line]["value"], "hand": expected, "disposition": got[line]["disposition"], "ok": ok}
            if not ok:
                mismatches.append({"case": key, "line": line, "engine": got[line]["value"], "hand": expected})
        # 2026 carryover: hand value versus what the engine publishes (nothing, by ADR-0058/0060).
        row["carryover_2026_hand"] = {"short-term": want["carryover-2026.short-term"], "long-term": want["carryover-2026.long-term"]}
        row["carryover_2026_engine"] = None
        row["inbound_carryover_engine"] = run["carryover_published"]
        row["inbound_lines_6_14"] = [got["schedule-d.line-6"]["value"], got["schedule-d.line-14"]["value"]]
        row["page_carryover_mentions"] = run["page_carryover_mentions"]
        row["attachments"] = run["page_attachments"]
        rows.append(row)
    # C/F against the A/D control: every line except the box lines, plus dispositions and attachments.
    parity: list[dict[str, Any]] = []
    for key, run in runs.items():
        if not key.startswith("cf/"):
            continue
        control = runs["ad/" + key[3:]]
        diffs = [line for line in run["lines"] if line not in PARITY_SKIP and run["lines"][line] != control["lines"][line]]
        diffs += [k for k in ("carryover_published", "carry_or_2026_symbols", "page_carryover_mentions", "blocked_rules", "questions", "stop")
                  if run[k] != control[k]]
        attachment_diffs = {a: [run["page_attachments"].get(a), control["page_attachments"].get(a)]
                            for a in set(run["page_attachments"]) | set(control["page_attachments"])
                            if run["page_attachments"].get(a) != control["page_attachments"].get(a)}
        parity.append({"case": key[3:], "line_diffs": diffs, "attachment_diffs": attachment_diffs})
    carry_cases = sorted(r["case"] for r in rows if any(r["carryover_2026_hand"].values()))
    body = {
        "runs": len(runs),
        "checks": sum(len(r["checks"]) for r in rows),
        "mismatches": mismatches,
        "parity_line_diffs": [p for p in parity if p["line_diffs"]],
        "parity_attachment_diffs": sorted({json.dumps(p["attachment_diffs"], sort_keys=True) for p in parity}),
        "cases_with_hand_2026_carryover": carry_cases,
        "carry_or_2026_symbols_seen": sorted({x for r in runs.values() for x in r["carry_or_2026_symbols"]}),
        "rows": rows,
    }
    (HERE / "comparison.json").write_text(json.dumps(body, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: body[k] for k in ("runs", "checks", "mismatches", "parity_line_diffs", "parity_attachment_diffs", "carry_or_2026_symbols_seen")}, indent=1))
    print("hand 2026 carryover cases:", len(carry_cases))


if __name__ == "__main__":
    main()
