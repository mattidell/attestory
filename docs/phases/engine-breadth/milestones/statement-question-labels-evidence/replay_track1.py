"""Compare the pre-Track-1 evaluator and projection with the build on core v108."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import patch

from replay import EXPECT, HERE, chosen_lists, semantic_check, summarize

from packages.derivation import evaluator, live, presentation_projection
from tools import recorded_replay as rr

BASE = "9d3c2e2fa"
CORE = "v108"


@lru_cache(maxsize=2)
def baseline(name: str) -> ModuleType:
    # Load only historical code, while both runs resolve the same v108 content.
    source = subprocess.check_output(
        ["git", "show", f"{BASE}:packages/derivation/{name}.py"], timeout=15,
    )
    module = ModuleType(f"statement_labels_baseline_{name}")
    sys.modules[module.__name__] = module
    exec(compile(source, f"{BASE}:{name}.py", "exec"), vars(module))
    if name == "evaluator":
        vars(module)["EvalBlocked"] = evaluator.EvalBlocked
    else:
        vars(module)["PresentationModelError"] = presentation_projection.PresentationModelError
    return module


class Compare:
    def __init__(self, expectations: list[dict[str, Any]]) -> None:
        self.expectations = expectations

    def __call__(self, key: str, acts: rr.Acts, cores: tuple[Any, ...]) -> dict[str, Any]:
        run_id = "demo.sql." + hashlib.sha256(key.encode()).hexdigest()[:20]
        old_pairing = baseline("evaluator")._require_paired
        old_projection = baseline("presentation_projection").build_presentation_model
        with (
            patch.object(live, "build_presentation_model", old_projection),
            patch.object(evaluator, "_require_paired", old_pairing),
        ):
            before = rr.saved_output(cores[0], acts, run_id)
        after = rr.saved_output(cores[0], acts, run_id)
        snapshots = [
            rr.snapshot(saved["model"], saved["report"]) if saved["outcome"] == "success"
            else rr.failure_snapshot(saved["outcome"], saved["error"], saved["message"])
            for saved in (before, after)
        ]
        verdict = rr.classify_full(snapshots[0], snapshots[1], self.expectations)
        semantic = semantic_check(before, after)
        if before.get("report") != after.get("report"):
            semantic["ok"] = False
            semantic["problems"].append("saved reports differ")
        if not semantic["ok"]:
            verdict["class"] = "unexpected"
        unexpected = verdict["unexpected"]
        return {
            **verdict, "semantic": semantic, "unexpected_total": len(unexpected),
            "unexpected": unexpected[:20], "outcomes": [snap["outcome"] for snap in snapshots],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--part", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    recorded = chosen_lists("recorded")
    cases = chosen_lists("cases")
    expectations = json.loads(EXPECT.read_text(encoding="utf-8"))
    core = rr.resolve_core(CORE)
    results = rr.replay(recorded + cases, (core,), Compare(expectations), workers=args.workers, part=args.part)
    summaries = {}
    for name, inputs in (("recorded", recorded), ("cases", cases)):
        selected = {key: results[key] for key, _ in inputs}
        summary = summarize(selected, expectations)
        summary["core"] = rr.core_fingerprint(core)
        summary["problems"] = {key: row["semantic"]["problems"] for key, row in selected.items()
                               if not row["semantic"]["ok"]}
        summaries[name] = summary
        print(name, dict(Counter(row["class"] for row in selected.values())), flush=True)
    p0 = json.loads((HERE / "replay_summary.json").read_text(encoding="utf-8"))
    p0_changed = set(p0["changed_lists"])
    changed = set(summaries["recorded"]["changed_lists"])
    summaries["recorded"]["new_since_v106"] = sorted(changed - p0_changed)
    summaries["recorded"]["absent_since_v106"] = sorted(p0_changed - changed)
    output = json.dumps(summaries, indent=1) + "\n"
    rr._check_no_local_paths(output, "Track 1 replay summary")
    args.out.write_text(output, encoding="utf-8")
    if any(summary["failing"] for summary in summaries.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
