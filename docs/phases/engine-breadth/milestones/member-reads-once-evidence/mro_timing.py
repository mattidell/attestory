"""Re-time every recorded list on core v96 (same method as rust-kernel-experiment track1_timing.py).

Run: python3 mro_timing.py <label> <scratch-outside-repo> [--mode warm|cold]
Parallel across cpu_count-1 spawn workers. Each list starts with an empty
validation memo. ``--mode cold`` also empties the member-file cache before every
list (the saving inside one list); ``--mode warm`` keeps it across the lists a
worker runs (a long-lived process: the test suite, CI). Before the cache exists
both modes are the same. Writes timing-<label>.json beside this file.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import statistics
import sys
import time

HERE = Path(__file__).resolve().parent
SIB = HERE.parent / "rust-kernel-experiment-evidence"


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        sys.modules[name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    return sys.modules[name]


wl = load("mro_timing_workload", SIB / "p0_workload.py")
rr = wl.rr
_WARM = False


def per_list(key, acts, core):  # type: ignore[no-untyped-def]
    global _WARM
    from packages.derivation import production_resolver as pr
    mode = os.environ.get("MRO_CACHE_MODE", "warm")
    clear_members = getattr(pr, "clear_member_cache", lambda: None)
    if not _WARM:
        wl.per_list("demo.rke.warmup", rr._get_harness().ccr.base_return(), core)
        _WARM = True
    pr.clear_validation_memo()
    if mode == "cold":
        clear_members()
    return wl.per_list(key, acts, core)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("label")
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--mode", choices=("warm", "cold"), default="warm")
    args = parser.parse_args()
    os.environ["MRO_CACHE_MODE"] = args.mode
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
    part = scratch / f"timing-part-{args.label}.json"
    t0 = time.monotonic()
    results = rr.replay(lists, core, per_list, workers=workers, part=part)
    wall = round(time.monotonic() - t0, 1)
    ok = {k: r for k, r in results.items() if r["outcome"] == "success"}
    ordered = sorted(results.items(), key=lambda kv: kv[1]["total_s"])
    totals = [r["total_s"] for _, r in ordered]
    okt = sorted(r["total_s"] for r in ok.values())
    body = {
        "label": args.label, "mode": args.mode, "workers": workers, "lists": len(results),
        "replay_wall_s": wall,
        "outcomes": {o: sum(r["outcome"] == o for r in results.values()) for o in ("success", "error", "refused")},
        "total_s_all_median": statistics.median(totals),
        "total_s_success_median": statistics.median(okt),
        "total_s_success_slowest": okt[-1],
        "total_s_sum_all": round(sum(totals), 1),
        "total_s_quartiles_all": statistics.quantiles(totals, n=4),
        "median_key": ordered[len(ordered) // 2][0], "slowest_key": ordered[-1][0],
        "per_list": {k: [r["outcome"], r["total_s"]] for k, r in sorted(results.items())},
    }
    wl.write(HERE / f"timing-{args.label}.json", body)
    print({k: v for k, v in body.items() if k != "per_list"})


if __name__ == "__main__":
    main()
