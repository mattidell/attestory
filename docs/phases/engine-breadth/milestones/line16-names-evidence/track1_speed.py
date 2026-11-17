"""Decision 11: paired live timings on 40 fixed recorded lists, speed first.

Run: python3 track1_speed.py <scratch-core.json>
The nine-worker pool is the only workload this agent runs during measurement.
Module preparation occurs before timing; no timing instrumentation is installed.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import statistics
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools import recorded_replay as rr

TARGETS = (
    "v82/m_2a_only_exc1_only2a_no/honest",
    "v82/m_empty_exc1_nolosses_no/honest",
    "v82/m_empty_exc1_only2a_no/honest",
    "v82/t4_s1_removed/honest",
)


def sample():
    lists = dict(rr.recorded_lists())
    chosen = []
    for group in ("v81", "v82", "v83", "v84", "v85"):
        candidates = sorted(key for key in lists if key.startswith(group + "/"))
        mandatory = list(TARGETS) if group == "v82" else []
        remaining = [key for key in candidates if key not in mandatory]
        count = 8 - len(mandatory)
        selected = mandatory + [remaining[round(i * (len(remaining) - 1) / (count - 1))] for i in range(count)]
        assert len(set(selected)) == 8
        chosen.extend((key, lists[key]) for key in sorted(selected))
    assert len(chosen) == 40 and set(TARGETS) <= {key for key, _ in chosen}
    return chosen


def worker(payload):
    index, key, acts, core_path = payload
    # Import and construct the shared harness before either timed core.
    rr._get_test().track0()
    cores = {"v94": rr.resolve_core("v94"), "successor": rr.resolve_core(Path(core_path))}
    order = ("v94", "successor") if index % 2 == 0 else ("successor", "v94")
    elapsed, hashes, errors = {}, {}, {}
    slug = key.replace("/", ".")
    for label in order:
        started = time.perf_counter()
        pin = rr.pin_run(cores[label], acts, "demo.l16.t1.speed." + label + "." + slug)
        elapsed[label] = time.perf_counter() - started
        hashes[label] = hashlib.sha256(json.dumps(pin, sort_keys=True).encode()).hexdigest()
        errors[label] = bool(pin.get("error"))
    return key, {"order": list(order), "elapsed_s": elapsed,
                 "ratio": elapsed["successor"] / elapsed["v94"],
                 "pin_sha256": hashes, "error_pin": errors,
                 "input_sha256": hashlib.sha256(json.dumps(acts, sort_keys=True).encode()).hexdigest()}


def main():
    assert len(sys.argv) == 2, "usage: track1_speed.py <scratch-core.json>"
    core = str(Path(sys.argv[1]).resolve())
    lists = sample()
    workers = max(1, (os.cpu_count() or 2) - 1)
    started = time.perf_counter()
    rows = {}
    tasks = [(i, key, acts, core) for i, (key, acts) in enumerate(lists)]
    with multiprocessing.get_context("spawn").Pool(workers) as pool:
        for key, row in pool.imap_unordered(worker, tasks):
            rows[key] = row
            if len(rows) % 5 == 0: print(f"speed pairs completed: {len(rows)}/40", flush=True)
    medians = {label: statistics.median(row["elapsed_s"][label] for row in rows.values()) for label in ("v94", "successor")}
    ratio = medians["successor"] / medians["v94"]
    body = {"item": 1, "verdict": "FAIL" if ratio > 1.10 else "PASS", "lists": len(rows),
        "sets": dict(Counter(key.split("/", 1)[0] for key in rows)), "all_four_targets_included": set(TARGETS) <= set(rows),
        "workers_each_core": workers, "timed_coordinate_runs": 80,
        "method": "Same fixed input in the same worker, cores back to back; 20 baseline-first and 20 successor-first pairs. No other job from this agent runs during the foreground pool. Shared harness imports are prepared before timing. Each list/core is timed once; per-core median is the median elapsed time per list across the 40 observations.",
        "per_list_median_s": medians, "median_ratio_successor_to_v94": ratio,
        "median_paired_ratio": statistics.median(row["ratio"] for row in rows.values()),
        "slowdown_percent": (ratio - 1) * 100, "stop_threshold_ratio": 1.10,
        "wall_time_s": time.perf_counter() - started,
        "cores": [rr.core_fingerprint(rr.resolve_core("v94")), rr.core_fingerprint(rr.resolve_core(Path(core)))],
        "rows": {key: rows[key] for key in sorted(rows)}}
    text = json.dumps(body, indent=2) + "\n"
    for marker in ("Users", "private", "tmp", "var"): assert "/" + marker + "/" not in text
    (HERE / "track1-speed.json").write_text(text)
    print(json.dumps({key: value for key, value in body.items() if key != "rows"}, indent=2), flush=True)


if __name__ == "__main__": main()
