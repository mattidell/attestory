"""Run the reproduction lists on the scratch successor; retain actual reasons.

Run: python3 <this-file> <scratch>/core.json
Only newly added combined-absence cases need an additional baseline run.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("l6b_check_probe", HERE / "probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = probe
spec.loader.exec_module(probe)
from tools import recorded_replay as rr


def worker(task: tuple) -> dict:
    row, baseline, core_path = task
    if baseline is None:
        baseline = probe.worker(row)
    try:
        result = probe.view(probe.run(row["acts"], "demo.l6b.prototype." + row["id"],
            rr.resolve_core(core_path), reconfirm=row["vary"] not in {"ssa-open", "no-benefits-open"}))
    except Exception as exc:
        import re
        result = {"outcome": "error", "error": type(exc).__name__,
                  "message": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))[:600]}
    a, b = baseline.get("sections", []), result.get("sections", [])
    def value_pin(sections: list) -> list:
        return [{k: v for k, v in s.items() if k != "reasons"} for s in sections]
    same_state = (baseline["outcome"] == result["outcome"] and value_pin(a) == value_pin(b)
                  and baseline.get("worksheet_rows") == result.get("worksheet_rows")
                  and baseline.get("blocked") == result.get("blocked")
                  and baseline.get("error") == result.get("error"))
    reasons_changed = [s["reasons"] for s in a] != [s["reasons"] for s in b]
    return {"id": row["id"], "baseline": baseline, "prototype": result,
            "class": ("numbers_identical_sentences_changed" if reasons_changed else "identical")
                if same_state else "unexpected_state_change"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    old = json.loads((HERE / "probe-output.json").read_text())
    baseline = {r["id"]: r for r in old["cases"]}
    tasks = [(r, baseline.get(r["id"]), str(args.core.resolve())) for r in probe.cases()]
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    workers = max(1, (os.cpu_count() or 2) - 1)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        rows = []
        for i, result in enumerate(pool.map(worker, tasks), 1):
            rows.append(result)
            if i % 25 == 0 or i == len(tasks):
                print(f"[{i}/{len(tasks)}] {result['id']}: {result['class']}", flush=True)
    for row in rows:
        baseline[row["id"]] = row["baseline"]
    old["cases"] = list(baseline.values())
    probe.write_json(HERE / "probe-output.json", old)
    counts = dict(Counter(r["class"] for r in rows))
    unanswered_blocks = [r["id"] for r in rows if any(
        s["disposition"] == "blocked" and not s["reasons"] for s in r["prototype"].get("sections", []))]
    result = {"workers": workers, "wall_time_s": round(time.monotonic()-started, 3),
              "cases": len(rows), "counts": counts, "unexplained_blocks": unanswered_blocks,
              "results": [{k: v for k, v in r.items() if k != "baseline"} for r in rows]}
    probe.write_json(HERE / "prototype-output.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "results"}, indent=2))
    assert not unanswered_blocks
    assert not counts.get("unexpected_state_change")


if __name__ == "__main__":
    main()
