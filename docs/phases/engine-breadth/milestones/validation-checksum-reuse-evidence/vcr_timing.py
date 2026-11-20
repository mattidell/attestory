"""Paired, interleaved timing of the median and slowest recorded list, before and after.

Run (scratch outside the repository; base is a pristine export of the base
commit with this directory's vcr_*.py copied in at the same place):
  python3 vcr_timing.py workloads <scratch>
  python3 vcr_timing.py run <scratch>                # one process; prints JSON
  python3 vcr_timing.py paired <scratch> <base-tree> <rounds>

``workloads`` copies the median list, the slowest list and the base return
(warm-up) out of the shared materialization (scratch/lists.json) into
scratch/workloads.json. ``run`` is one process: a warm-up, then three
interleaved repetitions of median cold, median warm, slowest cold and
slowest warm. "cold" empties the member cache before the list (one list on
its own); "warm" keeps it from the previous list (every later list in a
worker, the test suite, CI). Both empty the validation memo first, as each
recorded list in a replay does. The per-cell figure is the median of the
three. ``paired`` alternates processes of the base tree and this tree, the
order flipped every round, so both see the same machine load; it writes
timing-paired.json beside this file.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vcr_common as vc  # noqa: E402

CELLS = ("median-cold", "median-warm", "slowest-cold", "slowest-warm")


def workloads(scratch: Path) -> None:
    body = json.loads((scratch / "lists.json").read_text("utf-8"))
    found = dict((key, acts) for key, acts in body["lists"])
    h = vc.rr._get_harness()
    out = {"median": [vc.MEDIAN, found[vc.MEDIAN]], "slowest": [vc.SLOWEST, found[vc.SLOWEST]],
           "warmup": ["demo.vcr.warmup", h.ccr.base_return()]}
    (scratch / "workloads.json").write_text(json.dumps(out), "utf-8")


def run(scratch: Path) -> dict[str, Any]:
    from packages.derivation import production_resolver as pr
    loads = json.loads((scratch / "workloads.json").read_text("utf-8"))
    core = vc.core()
    vc.release_evidence_owner()
    h = vc.rr._get_harness()

    def once(name: str, cold: bool) -> float:
        key, acts = loads[name]
        pr.clear_validation_memo()
        if cold:
            pr.clear_member_cache()
        t0 = time.perf_counter()
        finished = vc.wl.prepare(key, acts, core)
        vc.wl.run(key, finished, core)
        return time.perf_counter() - t0

    times: dict[str, list[float]] = {cell: [] for cell in CELLS}
    with h.loader_entries(core):
        once("warmup", False)
        for _ in range(3):
            for cell in CELLS:
                name, mode = cell.split("-")
                times[cell].append(once(name, mode == "cold"))
    return {cell: round(statistics.median(v), 4) for cell, v in times.items()}


def paired(scratch: Path, base: Path, rounds: int) -> None:
    trees = {"before": base / vc.HERE.relative_to(vc.REPO), "after": vc.HERE}
    results: dict[str, list[dict[str, float]]] = {"before": [], "after": []}
    for index in range(rounds):
        order = ("before", "after") if index % 2 == 0 else ("after", "before")
        for label in order:
            proc = subprocess.run([sys.executable, str(trees[label] / "vcr_timing.py"), "run", str(scratch)],
                                  cwd=str(trees[label]), capture_output=True, text=True, timeout=900,
                                  env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            if proc.returncode != 0:
                raise SystemExit(proc.stderr[-4000:])
            results[label].append(json.loads(proc.stdout.strip().splitlines()[-1]))
            print(label, results[label][-1], flush=True)
    summary: dict[str, Any] = {"rounds": rounds, "repetitions_per_round": 3, "core": vc.CORE,
                               "method": "alternating processes, order flipped each round; per round the median "
                                         "of three interleaved repetitions; figures are the median over rounds",
                               "per_round": results}
    for cell in CELLS:
        before = statistics.median(r[cell] for r in results["before"])
        after = statistics.median(r[cell] for r in results["after"])
        paired_ratio = statistics.median(a[cell] / b[cell] for a, b in zip(results["after"], results["before"]))
        summary[cell] = {"before_s": round(before, 4), "after_s": round(after, 4),
                         "change_pct": round(100 * (after - before) / before, 1),
                         "median_paired_change_pct": round(100 * (paired_ratio - 1), 1)}
    vc.write(vc.HERE / "timing-paired.json", summary)
    print(json.dumps({c: summary[c] for c in CELLS}, indent=1))


def main() -> None:
    command, scratch = sys.argv[1], Path(sys.argv[2]).resolve()
    assert vc.REPO not in scratch.parents
    if command == "workloads":
        workloads(scratch)
    elif command == "run":
        print(json.dumps(run(scratch)))
    else:
        paired(scratch, Path(sys.argv[3]).resolve(), int(sys.argv[4]))


if __name__ == "__main__":
    main()
