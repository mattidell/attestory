"""Check current, answered wage returns beside the unmodified recorded replay.

Run: python3 <this-file> <scratch>/core.json
Checks every page field's disposition and value, and every reason sentence.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("l6b_computing_probe", HERE / "probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = probe
spec.loader.exec_module(probe)
from tools import recorded_replay as rr


def page(result: dict) -> dict:
    assert result["outcome"] == "success"
    states, reasons = {}, {}
    for section in result["model"]["sections"]:
        field, resolved = section["field"], section["resolved"]
        fid = field["id"].removeprefix(probe.P)
        states[fid] = [resolved.get("disposition"), resolved.get("value")]
        sentences = [r["sentence"] for r in resolved.get("reasons", [])]
        if sentences:
            reasons[fid] = sentences
    return {"states": states, "reasons": reasons, "stop": result["report"].get("stop_reason")}


def worker(task: tuple) -> dict:
    key, acts, path = task
    a = page(probe.run(acts, "demo.l6b.computing.v91." + key))
    b = page(probe.run(acts, "demo.l6b.computing.v92." + key, rr.resolve_core(path)))
    changed = [f for f in a["states"] if a["states"][f] != b["states"].get(f)]
    added = {f: [s for s in ss if s not in a["reasons"].get(f, [])]
             for f, ss in b["reasons"].items() if ss != a["reasons"].get(f, [])}
    return {"id": key, "changed_fields": changed, "added_reasons": added,
            "stop_v91": a["stop"], "stop_v92": b["stop"],
            "line6b": a["states"].get("form1040.line-6b"),
            "line34": a["states"].get("form1040.line-34"),
            "line37": a["states"].get("form1040.line-37"),
            "question_field_changes": sorted(added)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    h = probe.harness()
    tasks = []
    for status in probe.STATUSES:
        for benefits in (False, True):
            acts = probe.base(status, benefits=benefits)
            if status == "married_filing_separately":
                h._add(acts, "bundle-adoption", {"bundle": json.loads(
                    (probe.CONTENT / "core_calculations.bundle.v4.json").read_text())})
                acts = h.say(h.renumber(acts), probe.P + "standard-deduction.spouse-separate-condition", False, "l6b.computing.condition")
            key = status.replace("married_filing_", "") + (".ssa" if benefits else ".no-ssa")
            tasks.append((key, acts, str(args.core.resolve())))
            if status == "married_filing_separately" and not benefits:
                tasks.append((key + ".living-unanswered", h.strip(acts, probe.P + "mfs-lived-apart-all-year"), str(args.core.resolve())))
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    workers = max(1, (os.cpu_count() or 2) - 1)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(worker, tasks))
    output = {"workers": workers, "wall_time_s": round(time.monotonic()-started, 3), "cases": results}
    probe.write_json(HERE / "computing-neighbours.json", output)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
