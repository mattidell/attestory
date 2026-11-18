"""P0 step 1: time every recorded list on published core v96 and pick workloads.

Run: python3 p0_timing.py <scratch-outside-repo>
Parallel across cpu_count-1 spawn workers (tools/recorded_replay.replay), so
per-list times carry contention; the chosen lists are re-timed alone by
p0_profile.py. Writes p0-timing.json next to this file.
"""
from __future__ import annotations

import argparse
import json
import importlib.util
import os
from pathlib import Path
import statistics
import sys
import time

HERE = Path(__file__).resolve().parent


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        sys.modules[name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    return sys.modules[name]


wl = load("rke_p0_workload", HERE / "p0_workload.py")
rr = wl.rr


_WARM = False


def per_list(key, acts, core):  # type: ignore[no-untyped-def]
    """Warm each worker once (imports, schema and package loads) before timing."""
    global _WARM
    if not _WARM:
        wl.per_list("demo.rke.warmup", rr._get_harness().ccr.base_return(), core)
        _WARM = True
    return wl.per_list(key, acts, core)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--limit", type=int, default=None,
                        help="run at most this many pending lists this invocation (resumable)")
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    assert wl.REPO not in scratch.parents
    scratch.mkdir(parents=True, exist_ok=True)
    lists = rr.recorded_lists()
    assert len(lists) == 775
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    core = rr.resolve_core(wl.CORE)
    workers = max(1, (os.cpu_count() or 2) - 1)
    part = scratch / "timing-part.json"
    done = set(json.loads(part.read_text())["results"]) if part.exists() else set()
    pending = [(k, a) for k, a in lists if k not in done][: args.limit]
    t0 = time.monotonic()
    rr.replay(pending, core, per_list, workers=workers, part=part)
    wall_log = scratch / "timing-walls.json"
    walls = json.loads(wall_log.read_text()) if wall_log.exists() else []
    walls.append({"lists": len(pending), "replay_wall_s": round(time.monotonic() - t0, 1)})
    wall_log.write_text(json.dumps(walls))
    results = json.loads(part.read_text())["results"]
    if len(results) < len(lists):
        print({"done": len(results), "of": len(lists)})
        return
    replay_wall = sum(w["replay_wall_s"] for w in walls)
    ok = {k: r for k, r in results.items() if r["outcome"] == "success"}
    ordered = sorted(results.items(), key=lambda kv: kv[1]["total_s"])
    totals = [r["total_s"] for _, r in ordered]
    median_key = ordered[len(ordered) // 2][0]
    slowest_key = ordered[-1][0]
    def stats(field: str, rows: dict) -> dict:  # type: ignore[type-arg]
        vals = [r[field] for r in rows.values() if field in r]
        return {"min": min(vals), "median": statistics.median(vals), "max": max(vals),
                "sum": round(sum(vals), 2)}
    body = {
        "core": {"version": core.version, "registry": core.registry, "release": core.release_version},
        "workers": workers, "lists": len(results),
        "replay_wall_s": round(replay_wall, 1), "invocations": walls,
        "outcomes": {o: sum(r["outcome"] == o for r in results.values()) for o in ("success", "error", "refused")},
        "errors": sorted({r.get("error") for r in results.values() if r["outcome"] == "error"}),
        "stage_seconds_success": {f: stats(f, ok) for f in ("prep_s", "run_s", "render_s", "total_s")},
        "size_success": {f: stats(f, ok) for f in ("acts", "assertions", "distinct_asserted_facts", "rows", "publications")},
        "chosen": {"median": median_key, "slowest": slowest_key,
                   "rule": "sort all 775 lists by total_s (prep + live_coordinate_run + page render) under parallel replay; median is index 387, slowest is the last"},
        "top10": [[k, r["total_s"], r.get("acts")] for k, r in ordered[-10:]],
        "per_list": {k: [r["outcome"], r["total_s"], r.get("run_s"), r.get("acts"), r.get("assertions")]
                     for k, r in sorted(results.items())},
        "per_list_fields": ["outcome", "total_s", "run_s", "acts", "assertions"],
        "total_s_quartiles": statistics.quantiles(totals, n=4),
    }
    wl.write(HERE / "p0-timing.json", body)
    print({k: body[k] for k in ("replay_wall_s", "outcomes", "chosen", "top10")})


if __name__ == "__main__":
    main()
