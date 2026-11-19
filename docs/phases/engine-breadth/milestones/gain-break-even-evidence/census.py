"""Summarize the gain-break-even P0 census records into census.json.

Input: the jsonl records gbe_census_plugin.py wrote during one pytest session
over every test file that names a sale family or Schedule D. Each record is
one live_coordinate_run call from a test, with the sales it carried.

A sale's path: covered (box A/D, lines 1a/8a; includes the older gain-only
covered-ltcg family), w (code W), codeb (code B), noncovered (box B/E), no1099b
(box C/F). Its shape: gain (column h > 0), even (h == 0), loss (h < 0).

For each (path, term, shape) the summary lists the distinct test functions
(file:line of the test frame) whose live run carried such a sale, the core
versions those runs adopted, and whether at least one run on core v96 reached
a published Schedule D line 16 (saturated, line 16 not blocked).

Run: python3 census.py <record prefix>   Writes census.json beside this file.
"""
from __future__ import annotations

import glob
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PATHS = ("covered", "w", "codeb", "noncovered", "no1099b")


def path_of(family: str) -> tuple[str, str]:
    m = re.match(r"^(f1099b|f8949)\.(covered-w|covered-ltcg|covered|noncovered|code-b|no1099b)(?:-(st|lt))?$", family)
    assert m, family
    kind = {"covered-w": "w", "covered-ltcg": "covered", "covered": "covered", "noncovered": "noncovered",
            "code-b": "codeb", "no1099b": "no1099b"}[m.group(2)]
    term = m.group(3) or "lt"
    return kind, term


def shape_of(h: float) -> str:
    return "gain" if h > 0.004 else "loss" if h < -0.004 else "even"


def test_frame(rec: dict[str, Any]) -> str:
    for frame in rec.get("caller") or []:
        if re.match(r"tests/test_[^/]+\.py:\d+$", frame):
            return frame
    return (rec.get("caller") or ["?"])[0]


def main() -> None:
    prefix = sys.argv[1]
    recs = [json.loads(line) for f in sorted(glob.glob(prefix + "*.jsonl")) for line in open(f, encoding="utf-8")]
    cells: dict[str, dict[str, Any]] = defaultdict(lambda: {"tests": {}, "cores": set(), "v96_line16_published": False,
                                                            "v96_runs": 0, "runs": 0})
    for rec in recs:
        published16 = (rec.get("stop") == "saturated" and "schedule-d.line-16" in (rec.get("pubs") or {})
                       and not any(b.startswith("schedule-d-line16") for b in rec.get("blocked") or []))
        seen = set()
        for sale in rec["sales"]:
            kind, term = path_of(sale["family"])
            # Long-term flag on the sale object decides the term where the family name has none.
            if sale.get("lt") in ("yes", "no") and sale["family"].endswith(("covered-ltcg",)):
                term = "lt" if sale["lt"] == "yes" else "st"
            key = f"{kind}/{term}/{shape_of(sale['h'])}"
            if key in seen:
                continue
            seen.add(key)
            cell = cells[key]
            cell["runs"] += 1
            cell["cores"].add(str(rec.get("core")))
            node = rec.get("test", "").split("::")
            test = test_frame(rec)
            entry = cell["tests"].setdefault(test, {"node": "::".join(node[:2]) if node else "", "cores": set(),
                                                    "line16_published": False, "single_path": True})
            entry["cores"].add(str(rec.get("core")))
            entry["line16_published"] |= published16
            entry["single_path"] &= len({path_of(s["family"]) for s in rec["sales"]}) == 1 and len(rec["sales"]) == 1
            if rec.get("core") == "v96":
                cell["v96_runs"] += 1
                cell["v96_line16_published"] |= published16
    grid: dict[str, Any] = {}
    for kind in PATHS:
        for term in ("st", "lt"):
            for shape in ("gain", "even", "loss"):
                key = f"{kind}/{term}/{shape}"
                cell = cells.get(key)
                if cell is None:
                    grid[key] = {"runs": 0, "tests": [], "test_functions": 0, "cores": [], "v96_runs": 0, "v96_line16_published": False}
                    continue
                tests = sorted(cell["tests"].items())
                grid[key] = {
                    "runs": cell["runs"], "v96_runs": cell["v96_runs"], "v96_line16_published": cell["v96_line16_published"],
                    "cores": sorted(cell["cores"], key=lambda v: (len(v), v)),
                    "test_functions": len(tests),
                    "tests": [{"at": t, "cores": sorted(e["cores"], key=lambda v: (len(v), v)),
                               "line16_published": e["line16_published"], "single_sale": e["single_path"]}
                              for t, e in tests],
                }
    gaps = sorted(k for k, v in grid.items() if not k.endswith("/loss") and not v["v96_line16_published"])
    body = {"records": len(recs), "test_files": len({r.get("test", "").split("::")[0] for r in recs}),
            "gaps_no_v96_published_run": gaps, "grid": grid}
    (HERE / "census.json").write_text(json.dumps(body, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"records": body["records"], "test_files": body["test_files"], "gaps": gaps}, indent=1))
    for key, v in grid.items():
        print(f"{key:24} runs={v['runs']:4} v96={v['v96_runs']:4} v96_l16={v['v96_line16_published']!s:5} cores={','.join(v['cores'])[:60]}")


if __name__ == "__main__":
    main()
