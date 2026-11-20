"""Count and time every citizen checksum on one recorded list (published core v100).

Run (one process per call):
  python3 vcr_measure.py median|slowest <label>
Writes measure-<label>-<workload>.json beside this file.

The process warms up on the base return first (imports, schemas, the member
cache), then runs the workload twice: "warm" keeps the member cache from the
warm-up (every list after a worker's first, the test suite, CI) and "cold"
empties it first. Both start with an empty validation memo, as a fresh list
does. ``citizen_checksum`` is wrapped where production code looks it up (the
resolver module and the validator module) and each call is attributed to its
calling function and line; the wrapper's own time is included in the seconds.
A third, unwrapped run gives the wall time the shares are taken of.
"""
from __future__ import annotations

import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vcr_common as vc  # noqa: E402


def run_once(key: str, acts: list[dict[str, Any]], core: Any, cold: bool) -> float:
    from packages.derivation import production_resolver as pr
    pr.clear_validation_memo()
    if cold:
        pr.clear_member_cache()
    t0 = time.perf_counter()
    finished = vc.wl.prepare(key, acts, core)
    vc.wl.run(key, finished, core)
    return time.perf_counter() - t0


def instrumented(key: str, acts: list[dict[str, Any]], core: Any, cold: bool) -> dict[str, Any]:
    from packages.derivation import package_validation as pv
    from packages.derivation import production_resolver as pr
    calls: dict[str, int] = defaultdict(int)
    secs: dict[str, float] = defaultdict(float)
    timed: dict[str, list[float]] = {"_validation_memo_key": [0.0, 0], "validate_package": [0.0, 0]}
    real = pv.citizen_checksum

    def counted(citizen: Any) -> str:
        frame = sys._getframe(1)
        site = f"{Path(frame.f_code.co_filename).name}:{frame.f_lineno} {frame.f_code.co_name}"
        t = time.perf_counter()
        try:
            return real(citizen)
        finally:
            secs[site] += time.perf_counter() - t
            calls[site] += 1

    def timer(module: Any, name: str) -> Any:
        original = getattr(module, name)

        def wrapper(*a: Any, **k: Any) -> Any:
            t = time.perf_counter()
            try:
                return original(*a, **k)
            finally:
                timed[name][0] += time.perf_counter() - t
                timed[name][1] += 1
        return original, wrapper

    saved = [(pr, "citizen_checksum", getattr(pr, "citizen_checksum")), (pv, "citizen_checksum", real)]
    setattr(pr, "citizen_checksum", counted)
    setattr(pv, "citizen_checksum", counted)
    for name in ("_validation_memo_key", "validate_package"):
        original, wrapper = timer(pr, name)
        saved.append((pr, name, original))
        setattr(pr, name, wrapper)
    try:
        total = run_once(key, acts, core, cold)
    finally:
        for module, name, original in saved:
            setattr(module, name, original)
    return {
        "instrumented_total_s": round(total, 4),
        "citizen_checksum_calls": dict(sorted(calls.items())),
        "citizen_checksum_s": {k: round(v, 4) for k, v in sorted(secs.items())},
        "citizen_checksum_calls_total": sum(calls.values()),
        "citizen_checksum_s_total": round(sum(secs.values()), 4),
        "inclusive_s": {k: {"calls": int(v[1]), "s": round(v[0], 4)} for k, v in timed.items()},
    }


def main() -> None:
    name, label = sys.argv[1], sys.argv[2]
    core = vc.core()
    vc.release_evidence_owner()
    key, acts = vc.workload(name)
    h = vc.rr._get_harness()
    body: dict[str, Any] = {"workload": name, "list": key, "core": vc.CORE, "label": label}
    with h.loader_entries(core):
        run_once("demo.vcr.warmup", h.ccr.base_return(), core, cold=False)
        for mode in ("warm", "cold"):
            plain = run_once(key, acts, core, cold=(mode == "cold"))
            run_once("demo.vcr.warmup", h.ccr.base_return(), core, cold=False)
            measured = instrumented(key, acts, core, cold=(mode == "cold"))
            measured["uninstrumented_total_s"] = round(plain, 4)
            measured["checksum_share_of_uninstrumented"] = round(measured["citizen_checksum_s_total"] / plain, 4)
            body[mode] = measured
            run_once("demo.vcr.warmup", h.ccr.base_return(), core, cold=False)
    vc.write(vc.HERE / f"measure-{label}-{name}.json", body)
    print({m: {k: body[m][k] for k in ("uninstrumented_total_s", "citizen_checksum_calls_total",
                                        "citizen_checksum_s_total", "checksum_share_of_uninstrumented")}
           for m in ("warm", "cold")})


if __name__ == "__main__":
    main()
