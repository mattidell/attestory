"""Replay the landed Track 1 projection against its parent on one shared run."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import cache
import hashlib
import json
import multiprocessing
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from unittest.mock import patch

import replay as p0
from packages.derivation import live
from tests import evidence_loader
from tools import recorded_replay as rr
from tools.sale_page_observation import _labeled_reason_text

PROJECTION = "packages/derivation/presentation_projection.py"
PAGE = "packages/presentation/pages/citation-walk.v1.html"
EXPECTED_CONTROLS = ["added_name_to_distinct_statement", "removed_name", "swapped_names"]
EXPECTED_RECORDED = 775
EXPECTED_SYNTHETIC = 21
EXPECTED_SYNTHETIC_NAMES = 174
EXPECTED_DOM_CHECKS = 20


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=p0.REPO, text=True, timeout=20).strip()


def build_and_parent() -> tuple[str, str]:
    prefix = "build(statement-label-payer)"
    history = git("log", "--format=%H%x09%s", f"--grep=^{prefix}", "HEAD")
    builds = [commit for line in history.splitlines()
              for commit, _, subject in [line.partition("\t")] if subject.startswith(prefix)]
    if len(builds) != 1:
        raise ValueError(f"expected one {prefix} commit in HEAD history, found {len(builds)}")
    build = builds[0]
    return build, git("rev-parse", "--verify", f"{build}^")


@cache
def baseline_projection(parent: str):
    source = git("show", f"{parent}:{PROJECTION}")
    module = ModuleType("packages.derivation._statement_label_payer_baseline")
    sys.modules[module.__name__] = module
    exec(compile(source, PROJECTION, "exec"), vars(module))
    module.PresentationModelError = live.PresentationModelError
    return module.build_presentation_model


def check_observer(model, expected):
    for section in model["sections"]:
        for index, reason in enumerate(p0.reasons(section)):
            name = expected.get((section["id"], index))
            if name is None:
                continue
            label = reason["statementLabel"]["statement"]
            want = f"{label}, {name}: {reason['sentence']}"
            if _labeled_reason_text(reason) != want:
                raise ValueError("observed prefix differs from the expected text")


def run_list(key, acts, case, core, parent):
    baseline = baseline_projection(parent)
    introduced = p0.introduced_duplicates(acts)
    current = []

    def baseline_with_inventory(**kwargs):
        if introduced:
            current.extend(p0.current_duplicates(kwargs["state"], kwargs["current_finding_ids"]))
        return baseline(**kwargs)

    run_id = "demo.statement-payer-track1." + hashlib.sha256(key.encode()).hexdigest()[:20]
    with patch.object(live, "build_presentation_model", baseline_with_inventory):
        before = rr.saved_output(core, acts, run_id)
    after = rr.saved_output(core, acts, run_id)
    try:
        if case is not None and before["outcome"] != "success":
            raise ValueError("baseline did not save the synthetic case")
        expected = p0.expected_additions(before["model"], case) if before["outcome"] == "success" else {}
        p0.compare(before, after, expected)
        controls = p0.check_controls(key, before, after, expected, case)
        if case is not None:
            p0.check_dom(p0.REPO / PAGE, after, case, expected)
            check_observer(after["model"], expected)
    except ValueError as exc:
        raise ValueError(f"{key}: {exc}") from exc
    return {
        "outcome": before["outcome"], "names": len(expected), "controls": controls,
        "duplicates": introduced, "current_duplicates": current, "dom_checked": bool(case and case.ordered_names),
    }


def run_shard(items, core, parent):
    return {key: run_list(key, acts, case, core, parent) for key, acts, case in items}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=9)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be positive")
    build, parent = build_and_parent()
    baseline_projection(parent)
    all_recorded = dict(rr.recorded_lists())
    cases = p0.synthetic(all_recorded)
    recorded = [(key, acts, None) for key, acts in all_recorded.items()]
    probes = [(key, case.acts, case) for key, case in cases.items()]
    if (len(recorded), len(probes)) != (EXPECTED_RECORDED, EXPECTED_SYNTHETIC):
        raise ValueError("replay corpus count changed")
    if owner := evidence_loader.current_owner():
        evidence_loader.release(owner)
    core = rr.resolve_core(p0.CORE)
    n = min(2 * args.workers - 1, len(recorded))
    shards = [[probe] for probe in probes] + [recorded[i::n] for i in range(n)]
    results = {}
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn")) as pool:
        futures = [pool.submit(run_shard, shard, core, parent) for shard in shards]
        for future in as_completed(futures):
            try:
                results.update(future.result())
            except Exception:
                if hasattr(pool, "terminate_workers"):
                    pool.terminate_workers()
                raise
            print(f"{len(results)}/{len(recorded) + len(probes)} lists", file=sys.stderr, flush=True)
    if results.keys() != {key for key, _, _ in recorded + probes}:
        raise ValueError("incomplete replay")
    controls = sorted(control for result in results.values() for control in result["controls"])
    if controls != EXPECTED_CONTROLS:
        raise ValueError(f"incomplete controls: {controls}")
    synthetic = p0.summarize(probes, results, 10)
    dom_checks = sum(result["dom_checked"] for result in results.values())
    if synthetic["names_added"] != EXPECTED_SYNTHETIC_NAMES or dom_checks != EXPECTED_DOM_CHECKS:
        raise ValueError("synthetic additions or DOM checks differ from the expected totals")
    summary = {
        "build": build, "baseline": parent, "core": p0.CORE,
        "registry": core.registry, "release": core.release_version,
        "workers": args.workers, "shards": len(shards), "recorded": p0.summarize(recorded, results, 0),
        "synthetic": synthetic, "controls_rejected": controls, "synthetic_dom_checks": dom_checks,
        "synthetic_names_by_case": {key: results[key]["names"] for key in cases},
        "unexpected_differences": 0,
    }
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    rr._check_no_local_paths(encoded, "Track 1 replay summary")
    args.out.write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
