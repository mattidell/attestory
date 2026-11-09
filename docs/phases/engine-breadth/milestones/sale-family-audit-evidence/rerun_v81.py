"""Run every return the core v81 test pins on v81 and on the scratch v82, and count what changes.

Evidence for docs/phases/engine-breadth/milestones/sale-family-audit.md (P0).
Reads the act lists ``export_v81_returns.py`` wrote (outside the repository)
and the scratch core ``prototype.py`` built, and runs each return through
``live_coordinate_run`` with ``audit_harness.py`` (loaded under a unique
module name; no other evidence module is imported):

- ``v81``: the published core;
- ``v82``: the scratch core, with the two new Form 1099-B questions (box 4,
  box 7) answered "no" when the return records a Form 1099-B sale (none of
  these synthetic returns has either box);
- ``v82_unanswered``: the scratch core with the new questions unanswered.

    python3 docs/phases/engine-breadth/milestones/sale-family-audit-evidence/rerun_v81.py <acts.json> <core.json> [workers] [tag names.json]

With ``tag`` and a JSON list of "group/name" keys, runs only those returns and
writes rerun-output-<tag>.json. Otherwise writes rerun-output.json beside this file: the v81 check against the
committed expectation table, and every difference between v81 and v82.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
OUT = HERE / "rerun-output.json"
EXPECTED = REPO / "tests/fixtures/code_b_sales_v81/expected.json"
HARNESS = "sale_family_audit_harness"
ACTS: dict[str, Any] = {}
SALE_FAMILIES = tuple(f"tax.us.2025.f1099b.{k}-{t}" for k in ("covered", "covered-w", "noncovered", "code-b")
                      for t in ("st", "lt"))


def harness() -> Any:
    module = sys.modules.get(HARNESS)
    if module is None:
        spec = importlib.util.spec_from_file_location(HARNESS, HERE / "audit_harness.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[HARNESS] = module
        spec.loader.exec_module(module)
    return module


def init(acts_path: str) -> None:
    ACTS.update(json.loads(Path(acts_path).read_text(encoding="utf-8")))


def records_1099b_sale(acts: list[dict[str, Any]]) -> bool:
    for act in acts:
        payload = act.get("payload") or {}
        if act.get("kind") == "member-transition" and (payload.get("family") or {}).get("id") in SALE_FAMILIES:
            return True
    return False


def execute(task: tuple[str, str, str, str]) -> tuple[str, str, str, dict[str, Any]]:
    group, name, variant, core_json = task
    h = harness()
    acts = ACTS[group][name]
    if variant == "v81":
        core = h.V81
    else:
        spec = json.loads(core_json)
        core = h.Core(spec["version"], spec["registry"], spec["release_version"], Path(spec["content"]),
                      Path(spec["releases"]), spec.get("loader_from"),
                  tuple(tuple(p) for p in spec.get("presence_pairs") or ()))
        if variant == "v82" and records_1099b_sale(acts):
            acts = h.answer(acts, core.content, box4="no", box7="no")
    return group, name, variant, h.run(core, acts, f"demo.sfa.rerun.{group}.{name}.{variant}")


def fixture_mismatch(expected: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Where this harness's v81 run disagrees with the committed table (lines and attachments)."""
    if "error" in result:
        return {} if "error" in expected else {"error": result["error"]}
    out: dict[str, Any] = {}
    for key, (disposition, value) in (expected.get("lines") or {}).items():
        got = (result.get("lines") or {}).get(key)
        want = disposition if value is None or "blocked" in str(disposition) else value
        if got != want:
            out[key] = [got, want]
    if (expected.get("attachments") or {}) != (result.get("attachments") or {}):
        out["attachments"] = [result.get("attachments"), expected.get("attachments")]
    return out


def difference(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in ("error", "stop", "attachments", "questions"):
        if a.get(key) != b.get(key):
            out[key] = [a.get(key), b.get(key)]
    lines = {k: [a.get("lines", {}).get(k), b.get("lines", {}).get(k)]
             for k in set(a.get("lines") or {}) | set(b.get("lines") or {})
             if (a.get("lines") or {}).get(k) != (b.get("lines") or {}).get(k)}
    if lines:
        out["lines"] = dict(sorted(lines.items()))
    rows_a = {r[0]: r[1:] for r in a.get("blocked") or []}
    rows_b = {r[0]: r[1:] for r in b.get("blocked") or []}
    rows = {k: [rows_a.get(k), rows_b.get(k)] for k in set(rows_a) | set(rows_b) if rows_a.get(k) != rows_b.get(k)}
    if rows:
        out["blocked_rows"] = dict(sorted(rows.items()))
    return out


def form1040(result: dict[str, Any]) -> list[Any]:
    lines = result.get("lines") or {}
    return [lines.get(f"form1040.line-{n}") for n in ("7a", "15", "16", "25b", "34", "37")]


def main() -> None:
    acts_path, core_path = sys.argv[1], sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    core_json = Path(core_path).read_text(encoding="utf-8")
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    names = [(g, n) for g in ("case", "v80", "neighbour") for n in sorted(expected[g])]
    out_path = OUT
    if len(sys.argv) > 5:
        only = set(json.loads(Path(sys.argv[5]).read_text(encoding="utf-8")))
        names = [(g, n) for g, n in names if f"{g}/{n}" in only]
        out_path = HERE / f"rerun-output-{sys.argv[4]}.json"
    tasks = [(g, n, v, core_json) for g, n in names for v in ("v81", "v82", "v82_unanswered")]
    results: dict[tuple[str, str], dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=workers, initializer=init, initargs=(acts_path,)) as pool:
        for group, name, variant, result in pool.map(execute, tasks, chunksize=2):
            results.setdefault((group, name), {})[variant] = result
            if len(results[(group, name)]) == 3:
                print(group, name, flush=True)
    report: dict[str, Any] = {"returns": len(names), "fixture_check": {}, "changed": {}, "unchanged": [],
                              "unanswered": {}}
    for group, name in names:
        runs = results[(group, name)]
        pinned = expected[group][name] if group == "case" else expected[group][name]["v81"]
        mismatch = fixture_mismatch(pinned, runs["v81"])
        if mismatch:
            report["fixture_check"][f"{group}/{name}"] = mismatch
        diff = difference(runs["v81"], runs["v82"])
        key = f"{group}/{name}"
        if diff:
            report["changed"][key] = {"form1040_v81": form1040(runs["v81"]), "form1040_v82": form1040(runs["v82"]),
                                      **diff}
        else:
            report["unchanged"].append(key)
        unanswered = runs["v82_unanswered"]
        report["unanswered"][key] = {"form1040": form1040(unanswered), "questions": unanswered.get("questions"),
                                     "line25b": (unanswered.get("lines") or {}).get("form1040.line-25b"),
                                     "sd16": (unanswered.get("lines") or {}).get("schedule-d.line-16")}
    report["summary"] = {"fixture_mismatches": len(report["fixture_check"]), "changed": len(report["changed"]),
                         "unchanged": len(report["unchanged"])}
    harness_module = harness()
    out_path.write_text(harness_module.scrub(json.dumps(report, indent=1, sort_keys=True)) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"]))


if __name__ == "__main__":
    main()
