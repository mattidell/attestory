"""Full-surface replay: the repository projection against a scratch projection, on one core (same-label-members P0).

Run: python3 replay.py <scratch projection.py> [--core v107] [--workers N]
                       --part <part-file-outside-repo> [--out summary.json]

Every recorded list (``tools/recorded_replay.recorded_lists``) and every
``probe.py`` case runs in one shared ``recorded_replay.replay`` call whose
process pool holds the workers (shards are the pool's workers). For each list
the worker takes the full saved surface twice on the same core: once with the
repository's ``presentation_projection``, once with the changed definitions of
the scratch copy swapped in (``probe.scratch_projection``). The comparison is
``recorded_replay.classify_full`` with no expectations, so any difference on
any saved page field, attachment, explanation-graph node or report row fails
the list. The summary keeps recorded lists and probe lists apart: a recorded
list must be identical; a probe list's differences are listed by attribute so
the note can show they are reason entries only.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import recorded_replay as rr  # noqa: E402


def _probe() -> Any:
    name = "slm_p0_probe"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, HERE / "probe.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class ScratchCompare:
    """Picklable per-list function: repository projection, then scratch projection, strict."""

    def __init__(self, scratch: str, max_unexpected: int = 40) -> None:
        self.scratch = scratch
        self.max_unexpected = max_unexpected

    def __call__(self, key: str, acts: list, cores: tuple) -> dict:
        (core,) = cores
        run_id = "demo.fsr." + hashlib.sha256(key.encode()).hexdigest()[:20]
        snap_a = rr.snapshot_run(core, acts, run_id)
        with _probe().scratch_projection(Path(self.scratch)) as names:
            assert names, "the scratch projection changes nothing"
            snap_b = rr.snapshot_run(core, acts, run_id)
        verdict = rr.classify_full(snap_a, snap_b, [])
        unexpected = verdict.pop("unexpected")
        verdict["unexpected_total"] = len(unexpected)
        verdict["by_attribute"] = dict(Counter(f"{d['kind']}|{d['change']}|{re.sub(r'[0-9]+', 'N', d['attribute'])}"
                                               for d in unexpected))
        verdict["unexpected"] = unexpected[: self.max_unexpected]
        verdict["outcomes"] = [snap_a["outcome"], snap_b["outcome"]]
        verdict["records"] = [len(snap_a["records"]), len(snap_b["records"])]
        verdict["sha256"] = [rr.snapshot_sha256(snap_a), rr.snapshot_sha256(snap_b)]
        return verdict


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--core", default="v107")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--part", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--limit", type=int, default=None, help="first N recorded lists only (smoke test)")
    args = parser.parse_args()
    probe = _probe()
    core = rr.resolve_core(args.core)
    recorded = rr.recorded_lists()
    if args.limit is not None:
        recorded = recorded[: args.limit]
    probes = [(f"probe:{case}", probe.build(case, core.content)) for case in probe.CASES]
    started = time.monotonic()
    results = rr.replay([*recorded, *probes], (core,), ScratchCompare(str(args.scratch.resolve())),
                        workers=args.workers, part=args.part)
    recorded_keys = {key for key, _ in recorded}

    def part(keys: set[str]) -> dict[str, Any]:
        rows = {k: v for k, v in results.items() if k in keys}
        by_attribute: Counter = Counter()
        for row in rows.values():
            by_attribute.update(row.get("by_attribute", {}))
        return {
            "lists": len(rows),
            "classes": dict(sorted(Counter(r["class"] for r in rows.values()).items())),
            "identical": sum(1 for r in rows.values() if r["unexpected_total"] == 0),
            "differing": sum(1 for r in rows.values() if r["unexpected_total"]),
            "differences": sum(r["unexpected_total"] for r in rows.values()),
            "differences_by_kind_change_attribute": dict(sorted(by_attribute.items())),
            "outcomes": dict(sorted(Counter("/".join(r["outcomes"]) for r in rows.values()).items())),
            "differing_lists": {k: r["unexpected_total"] for k, r in sorted(rows.items()) if r["unexpected_total"]},
        }

    summary = {
        "format": "same-label-members-p0-replay.v1",
        "core": rr.core_fingerprint(core),
        "comparison": "repository presentation_projection vs scratch copy, same core, strict, no expectations",
        "swapped": probe._changed_names(Path(probe.projection.__file__).read_text(encoding="utf-8"),
                                        args.scratch.read_text(encoding="utf-8")),
        "wall_time_s": round(time.monotonic() - started, 1),
        "recorded": part(recorded_keys),
        "probe": part(set(results) - recorded_keys),
        "probe_samples": {k: results[k]["unexpected"][:4] for k in sorted(results) if k not in recorded_keys
                          and results[k]["unexpected_total"]},
    }
    text = json.dumps(summary, indent=1, sort_keys=True) + "\n"
    if args.out:
        rr._check_no_local_paths(text, str(args.out))
        args.out.write_text(text, encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("swapped", "wall_time_s", "recorded", "probe")}, indent=1)[:5000])


if __name__ == "__main__":
    main()
