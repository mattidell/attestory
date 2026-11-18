"""Identity dump on core v96 after the member cache; compare with the committed baseline.

Run: python3 mro_dump.py <label> <scratch-outside-repo> [--validation-only]
Reuses rust-kernel-experiment's track1_dump.py per-list hashing (loaded by path)
and writes summary-<label>.json beside this file. The comparison target is
``per_list_digest`` in rust-kernel-experiment-evidence/track1-summary-baseline.json
(validation lists: run --validation-only with PYTHONHASHSEED=0 and compare to
track1-validation-baseline.json there).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
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


dump = load("mro_dump_sibling", SIB / "track1_dump.py")
wl, rr, _sha, _canon = dump.wl, dump.rr, dump._sha, dump._canon


def per_list(key, acts, core):  # type: ignore[no-untyped-def]
    return dump.per_list(key, acts, core)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("label")
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--validation-only", action="store_true")
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    assert wl.REPO not in scratch.parents
    scratch.mkdir(parents=True, exist_ok=True)
    validation = dump.validation_errors()
    vsum = {name: {"ok": v["ok"], "count": v["count"], "issues_digest": _sha(_canon(v["issues"])),
                   "output_owners_sha": v["output_owners_sha"], "resolved_members_sha": v["resolved_members_sha"]}
            for name, v in validation.items() if isinstance(v, dict) and "issues" in v}
    if args.validation_only:
        wl.write(HERE / f"validation-{args.label}.json",
                 {"label": args.label, "hashseed": os.environ.get("PYTHONHASHSEED"), "validation": vsum})
        print(json.dumps(vsum, indent=1))
        return
    lists = rr.recorded_lists()
    assert len(lists) == 775, len(lists)
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    core = rr.resolve_core(wl.CORE)
    workers = max(1, (os.cpu_count() or 2) - 1)
    t0 = time.monotonic()
    results = rr.replay(lists, core, per_list, workers=workers, part=scratch / f"dump-part-{args.label}.json")
    wall = round(time.monotonic() - t0, 1)
    (scratch / f"dump-{args.label}.json").write_text(json.dumps({"lists": results}, indent=1, sort_keys=True) + "\n")
    lines = [f"{k}\t{r['outcome']}\t{r.get('result_sha')}\t{r.get('page_sha')}\t{r.get('presentation_sha')}\t{r.get('error')}\t{r.get('message')}"
             for k, r in sorted(results.items())]
    baseline = json.loads((SIB / "track1-summary-baseline.json").read_text())
    digest = _sha("\n".join(lines).encode("utf-8"))
    summary = {
        "label": args.label, "core": core.version, "lists": len(results),
        "outcomes": {o: sum(r["outcome"] == o for r in results.values()) for o in ("success", "error", "refused")},
        "errors": sorted({r["error"] for r in results.values() if r["outcome"] == "error"}),
        "per_list_digest": digest,
        "baseline_per_list_digest": baseline["per_list_digest"],
        "equal_to_baseline": digest == baseline["per_list_digest"],
        "replay_wall_s": wall, "workers": workers,
    }
    wl.write(HERE / f"summary-{args.label}.json", summary)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
