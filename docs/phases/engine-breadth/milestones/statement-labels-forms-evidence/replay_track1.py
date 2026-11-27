"""Compare the built saved surface to its pre-build parent on core v109."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import cache
import hashlib
import json
import multiprocessing
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from typing import Any
from unittest.mock import patch

import probe
import replay as p0
from packages.derivation import live
from tests import evidence_loader
from tools import recorded_replay as rr

EXPECTED_TOTALS = {"recorded": (775, 2, 8), "synthetic": (23, 17, 168)}
EXPECTED_CONTROLS = {
    "missing_label": "rejected", "swapped_labels": "rejected",
    "spurious_label_on_closure_block": "rejected",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=probe.REPO, text=True, timeout=15).strip()


def build_and_parent() -> tuple[str, str]:
    prefix = "build(statement-labels-forms)"
    matches = git("log", "--format=%H%x09%s", f"--grep=^{prefix}", "HEAD")
    builds = [commit for line in matches.splitlines()
              for commit, _, subject in [line.partition("\t")] if subject.startswith(prefix)]
    if len(builds) != 1:
        raise ValueError(f"expected one statement-labels-forms build in HEAD history, found {len(builds)}")
    build = builds[0]
    return build, git("rev-parse", "--verify", f"{build}^")


@cache
def baseline_projection(parent: str) -> Any:
    source = git("show", f"{parent}:{p0.PROJECTION}")
    module = ModuleType("packages.derivation._withholding_statement_labels_baseline")
    sys.modules[module.__name__] = module
    exec(compile(source, p0.PROJECTION, "exec"), vars(module))
    module.PresentationModelError = live.PresentationModelError
    return module.build_presentation_model


def run_list(key: str, acts: rr.Acts, case: probe.Case | None, core: rr.ReplayCore, parent: str) -> dict:
    expected = {}

    def observe_baseline(**kwargs: Any) -> dict:
        expected.update(p0.expected_by_question(kwargs["state"], kwargs["current_finding_ids"],
                                                kwargs["dispositions"]))
        return baseline_projection(parent)(**kwargs)

    # Both saves use the same inputs, core and run id through the coordinator.
    run_id = "demo.statement-labels-forms." + hashlib.sha256(key.encode()).hexdigest()[:20]
    with patch.object(live, "build_presentation_model", observe_baseline):
        before = rr.saved_output(core, acts, run_id)
    after = rr.saved_output(core, acts, run_id)
    differences, counts = p0.compare(before, after, expected)
    if differences:
        raise ValueError(f"{key}: {len(differences)} unexpected saved-surface differences")

    gain = Counter()
    if after["outcome"] == "success":
        gain = p0.labelled_counts(after["model"])
        gain.subtract(p0.labelled_counts(before["model"]))
    if Counter({sentence: count for sentence, count in gain.items() if count}) != counts:
        raise ValueError(f"{key}: actual label count differs from the expected expansion")

    dom_checked = False
    if case is not None:
        if after["outcome"] != "success":
            raise ValueError(f"{key}: synthetic case did not save")
        sentence = probe.questions()[probe.FORMS[case.form].withholding][1]
        line = next(section["resolved"] for section in after["model"]["sections"]
                    if section["id"].endswith("line-25b"))
        actual = [reason["statementLabel"] for reason in line.get("reasons", [])
                  if reason["sentence"] == sentence and "statementLabel" in reason]
        want = [{"statement": label, "taxYear": "2025"} for label in case.labels]
        if actual != want:
            raise ValueError(f"{key}: ordered line 25b labels differ from the hand-written case")
        if key.endswith(".two-missing") or key in {
            "demo.int.single", "demo.int.three-one-zero", "demo.ssa.single",
        }:
            p0.render_line_25b(before, after, sentence, case.labels)
            dom_checked = True
    return {
        "outcome": after["outcome"],
        "labelled_reasons": sum(gain.values()),
        "dom_checked": dom_checked,
        "controls": p0.controls(key, before, after, expected),
    }


def run_shard(
    items: list[tuple[str, rr.Acts, probe.Case | None]], core: rr.ReplayCore, parent: str,
) -> dict:
    return {key: run_list(key, acts, case, core, parent) for key, acts, case in items}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=9)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be positive")
    build, parent = build_and_parent()
    baseline_projection(parent)  # Fail up front if the baseline cannot be loaded.
    recorded = [(key, acts, None) for key, acts in rr.recorded_lists()]
    synthetic = [(key, case.acts, case) for key, case in probe.cases().items()]
    if owner := evidence_loader.current_owner():
        evidence_loader.release(owner)
    items = recorded + synthetic
    keys = {key for key, _, _ in items}
    if len(keys) != len(items):
        raise ValueError("replay lists must have distinct keys")
    recorded_shards = min(len(recorded), 2 * args.workers - 1)
    shards = [synthetic, *(recorded[index::recorded_shards] for index in range(recorded_shards))]
    core = rr.resolve_core(probe.CORE)
    results = {}
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn")) as pool:
        pending = [pool.submit(run_shard, shard, core, parent) for shard in shards]
        for part in as_completed(pending):
            results.update(part.result())
            print(f"{len(results)}/{len(items)} lists", file=sys.stderr, flush=True)
    if results.keys() != keys:
        raise ValueError("incomplete replay")
    controls = {name: verdict for result in results.values() for name, verdict in result["controls"].items()}
    if controls != EXPECTED_CONTROLS:
        raise ValueError(f"missing failing controls: {controls}")

    totals = {}
    for name, corpus in (("recorded", recorded), ("synthetic", synthetic)):
        rows = [results[key] for key, _, _ in corpus]
        observed = (len(rows), sum(row["labelled_reasons"] > 0 for row in rows),
                    sum(row["labelled_reasons"] for row in rows))
        if observed != EXPECTED_TOTALS[name]:
            raise ValueError(f"{name}: expected lists, affected lists and labels {EXPECTED_TOTALS[name]}, got {observed}")
        totals[name] = {
            "lists": observed[0], "lists_gaining_labels": observed[1], "labelled_reasons": observed[2],
            "outcomes": dict(sorted(Counter(row["outcome"] for row in rows).items())),
        }
    summary = {
        "build": build, "baseline": parent, "core": probe.CORE,
        "shards": len(shards), "workers": args.workers, **totals, "unexpected_differences": 0,
        "dom_checks": sorted(key for key, row in results.items() if row["dom_checked"]),
        "controls": controls,
    }
    output = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    rr._check_no_local_paths(output, "Track 1 replay summary")
    args.out.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
