"""Run the recorded-replay CLI in the foreground and classify its part file.

Run: python3 <this-file> <scratch>/core.json
Keeps the original CLI part file beside core.json for Track 0 to reuse.
Lists are replayed exactly as tools.recorded_replay.recorded_lists emits them;
no scope, age, or blindness answers are added by this script.
"""
from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def sentences(pin: dict) -> set[str]:
    out = set(pin.get("questions") or [])
    for key in ("reasons", "blocked_reasons"):
        for values in (pin.get(key) or {}).values():
            out.update(values)
    return out


def computing(pin: dict) -> bool:
    # A numeric refund or balance-due line witnesses a computing return.
    return any(isinstance((pin.get("lines") or {}).get(name), (int, float))
               for name in ("form1040.line-34", "form1040.line-37"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", type=Path)
    parser.add_argument("--summarize-only", action="store_true")
    args = parser.parse_args()
    core = args.core.resolve()
    part = core.parent / "recorded-part.json"
    native = core.parent / "recorded-summary.json"
    clock = core.parent / "recorded-wall.json"
    workers = max(1, (os.cpu_count() or 2) - 1)
    spent = json.loads(clock.read_text()) if clock.exists() else []
    if not args.summarize_only:
        started = time.monotonic()
        try:
            subprocess.run([
                sys.executable, str(REPO / "tools/recorded_replay.py"), "neighbour", "v91", str(core),
                "--workers", str(workers), "--part", str(part), "--out", str(native),
            ], check=True, cwd=REPO)
        finally:
            spent.append(round(time.monotonic()-started, 3))
            clock.write_text(json.dumps(spent) + "\n")
    results = json.loads(part.read_text())["results"]
    counts = Counter(r["class"] for r in results.values())
    errors = Counter(r["pins"]["v91"].get("error") for r in results.values())
    by_set = {}
    baseline_computing = 0
    new_on_computing = []
    new_questions = Counter()
    changes = []
    for key, row in sorted(results.items()):
        by_set.setdefault(key.split("/", 1)[0], Counter())[row["class"]] += 1
        a, b = row["pins"]["v91"], row["pins"]["v92"]
        added = sorted(sentences(b) - sentences(a))
        new_questions.update(added)
        if computing(a):
            baseline_computing += 1
            if added:
                new_on_computing.append({"id": key, "added": added})
        if row["class"] != "identical":
            changes.append({"id": key, **{k: v for k, v in row.items() if k != "pins"}, "added_sentences": added})
    payload = {
        "baseline": "published core v91 / registry v89 / release v89",
        "successor": "scratch core v92 / registry v90 / release v90",
        "lists": "tools.recorded_replay.recorded_lists(); unmodified",
        "workers": workers, "distinct_lists": len(results), "live_runs": 2*len(results),
        "wall_time_s": round(sum(spent), 3), "invocations_s": spent,
        "counts": dict(counts), "by_set": {k: dict(v) for k, v in by_set.items()},
        "successful_coordinate_runs_per_core": errors.get(None, 0),
        "same_errors_per_core": {k: v for k, v in errors.items() if k is not None},
        "baseline_computing": baseline_computing,
        "computing_return_test": "a numeric Form 1040 line 34 or line 37 in the recorded-replay pin",
        "computing_newly_asked": new_on_computing,
        "computing_target_limit": "No unmodified recorded list has a numeric refund or balance due on v91; this test is unexercised by that set. See computing-neighbours.json.",
        "new_sentence_counts": dict(new_questions), "changes": changes,
        "classes": {key: row["class"] for key, row in sorted(results.items())},
        "part_file_kept": True,
    }
    spec = importlib.util.spec_from_file_location("l6b_rerun_probe", HERE / "probe.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.write_json(HERE / "rerun-output.json", payload)
    print(json.dumps({k: payload[k] for k in (
        "distinct_lists", "wall_time_s", "counts", "baseline_computing", "computing_newly_asked")}, indent=2))


if __name__ == "__main__":
    main()
