"""Replay the pre-Track-1 projection and check v108 results against the P0 design."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any
from unittest.mock import patch

from replay import EXPECT, HERE, REPO, chosen_lists, semantic_check
from replay_baseline import baseline, baseline_ref

import design
import probe
from packages.derivation import evaluator, live
from tools import recorded_replay as rr

CORE = "v108"
EXPECTED_TOTALS = {"recorded": (775, 141), "cases": (18, 15)}
CONTROL_CASE = "two.amount.both"
CONTROL_NAMES = {"original_sentences_rejected", "swapped_labels_rejected"}


def reasons_by_line(model: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {section["id"]: (section.get("resolved") or {}).get("reasons", [])
            for section in model["sections"]}


def label_mismatches(expected: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    """Check each ordered reason, including its sentence, full label and duplicates."""
    want, got = reasons_by_line(expected), reasons_by_line(actual)
    return sorted(line for line in want.keys() | got.keys() if want.get(line) != got.get(line))


def negative_controls(before: dict[str, Any], after: dict[str, Any],
                      expected: dict[str, Any]) -> dict[str, bool]:
    """The old folding check accepts both mutations; the exact check rejects them."""
    swapped = deepcopy(after)
    for reasons in reasons_by_line(swapped["model"]).values():
        candidates = [reason for reason in reasons if "statementLabel" in reason]
        if (len(candidates) == 2 and candidates[0]["sentence"] == candidates[1]["sentence"]
                and candidates[0]["statementLabel"] != candidates[1]["statementLabel"]):
            first, second = candidates
            first["statementLabel"], second["statementLabel"] = second["statementLabel"], first["statementLabel"]
            break
    else:
        raise AssertionError("control case needs two distinct labels for one question")
    return {
        name: semantic_check(before, candidate)["ok"]
        and bool(label_mismatches(expected, candidate["model"]))
        for name, candidate in (("original_sentences_rejected", before), ("swapped_labels_rejected", swapped))
    }


class Compare:
    def __init__(self, expectations: list[dict[str, Any]], labelled_keys: set[str],
                 case_labels: dict[str, dict[str, list[str]]]) -> None:
        self.expectations = expectations
        self.labelled_keys = labelled_keys
        self.case_labels = case_labels

    def __call__(self, key: str, acts: rr.Acts, cores: tuple[Any, ...]) -> dict[str, Any]:
        run_id = "demo.sql." + hashlib.sha256(key.encode()).hexdigest()[:20]
        old_projection = baseline("presentation_projection")
        expected: dict[str, Any] | None = None
        should_label = key in self.labelled_keys

        def baseline_projection(**kwargs: Any) -> Any:
            nonlocal expected
            plain = old_projection.build_presentation_model(**kwargs)
            expected = plain
            if should_label:
                # P0 recomputes targets from current facts independently of the
                # built projection and runs on the pre-track walk.
                expected = design.project_with_design(old_projection, **kwargs)
            return plain

        with (
            patch.object(live, "build_presentation_model", baseline_projection),
            patch.object(evaluator, "_require_paired", baseline("evaluator")._require_paired),
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
        problems: list[str] = semantic["problems"]
        if before.get("report") != after.get("report"):
            problems.append("saved reports differ")
        controls = {}
        if before["outcome"] == after["outcome"] == "success" and expected is not None:
            mismatches = label_mismatches(expected, after["model"])
            if mismatches:
                problems.append(f"reason labels differ from P0 design on {len(mismatches)} lines")
            if key in self.case_labels:
                observed = probe.labels_by_fact(probe.observe(after["model"], after["report"]))
                if observed != self.case_labels[key]:
                    problems.append("case labels differ from the hand-written expectations")
            if key == CONTROL_CASE:
                controls = negative_controls(before, after, expected)
        if bool(semantic["labels"]) != should_label:
            problems.append("list label gain differs from the P0 expectation")
        unexpected = len(verdict["unexpected"])
        return {
            "class": "unexpected" if problems or verdict["class"] == "unexpected" else verdict["class"],
            "problems": problems,
            "unexpected": unexpected,
            "outcome": "/".join(snap["outcome"] for snap in snapshots),
            "lines_labelled": semantic["lines_labelled"],
            "labelled_reasons": semantic["labels"],
            "controls": controls,
        }


def compact(results: dict[str, Any]) -> dict[str, Any]:
    return {
        "lists": len(results),
        "passing": sum(row["class"] != "unexpected" for row in results.values()),
        "lists_gaining_labels": sum(row["labelled_reasons"] > 0 for row in results.values()),
        "lines_labelled": sum(row["lines_labelled"] for row in results.values()),
        "labelled_reasons": sum(row["labelled_reasons"] for row in results.values()),
        "unexpected_differences": sum(row["unexpected"] for row in results.values()),
        "semantic_failures": sum(bool(row["problems"]) for row in results.values()),
        "outcomes": dict(Counter(row["outcome"] for row in results.values())),
    }


def source_fingerprint() -> str:
    """Fingerprint the baseline, runner, transitive source files and replay inputs."""
    summary = HERE.relative_to(REPO) / "replay_track1_summary.json"
    files = subprocess.check_output(
        ["git", "ls-files", "-z", "--", "*.py", "*.sh", "*.js", "*.mjs",
         "packages", "tests/fixtures", "docs/phases/*/milestones/*.json",
         ":(exclude)archive", ":(exclude)docs/archive", ":(exclude)docs/governance",
         f":(exclude){summary.as_posix()}"],
        cwd=REPO, timeout=15,
    )
    digest = hashlib.sha256(baseline_ref().encode("ascii"))
    for name in sorted(set(files.split(b"\0")) - {b""}):
        digest.update(name + b"\0")
        digest.update(hashlib.sha256((REPO / os.fsdecode(name)).read_bytes()).digest())
    return digest.hexdigest()


def shard(index: int, total: int, workers: int) -> dict[str, Any]:
    inputs = {name: chosen_lists(name)[index::total] for name in EXPECTED_TOTALS}
    case_labels = {case["id"]: case["expect"] for case in probe.CASES}
    p0 = json.loads((HERE / "replay_summary.json").read_text(encoding="utf-8"))
    labelled_keys = set(p0["changed_lists"]) | {key for key, labels in case_labels.items() if labels}
    expectations = json.loads(EXPECT.read_text(encoding="utf-8"))
    results = rr.replay(inputs["recorded"] + inputs["cases"], (rr.resolve_core(CORE),),
                        Compare(expectations, labelled_keys, case_labels), workers=workers)
    failures = {key: {"problems": row["problems"], "unexpected_differences": row["unexpected"]}
                for key, row in results.items() if row["class"] == "unexpected"}
    return {
        "shard": [index, total],
        "sets": {name: compact({key: results[key] for key, _ in selected})
                 for name, selected in inputs.items()},
        "controls": results.get(CONTROL_CASE, {}).get("controls", {}),
        "failures": failures,
    }


def merge(parts: list[dict[str, Any]]) -> dict[str, Any]:
    if sorted(part["shard"] for part in parts) != [[i, len(parts)] for i in range(len(parts))]:
        raise ValueError("expected one fresh result for each shard")
    if any(part["failures"] for part in parts):
        raise ValueError("one or more replay shards failed")
    controls = {name: value for part in parts for name, value in part["controls"].items()}
    if controls.keys() != CONTROL_NAMES or not all(controls.values()):
        raise ValueError("negative controls did not reject both mutations")
    sets = {}
    for name, (total, labelled) in EXPECTED_TOTALS.items():
        rows = [part["sets"][name] for part in parts]
        combined = {key: sum(row[key] for row in rows) for key in rows[0] if key != "outcomes"}
        outcomes: Counter[str] = Counter()
        for row in rows:
            outcomes.update(row["outcomes"])
        if (combined["lists"] != total or combined["passing"] != total
                or combined["lists_gaining_labels"] != labelled):
            raise ValueError(f"{name}: wrong coverage or label count: {combined}")
        sets[name] = {**combined, "outcomes": dict(sorted(outcomes.items()))}
    return {"shards": len(parts), "sets": sets, "controls": controls}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--shard", help="zero-based shard index and total, e.g. 0/2")
    mode.add_argument("--merge", nargs="+", type=Path)
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    identity = {"core": rr.core_fingerprint(rr.resolve_core(CORE)),
                "source_sha256": source_fingerprint()}
    if args.merge:
        parts = [json.loads(path.read_text(encoding="utf-8")) for path in args.merge]
        if any(part["identity"] != identity for part in parts):
            raise ValueError("shards were produced with different core content or sources")
        payload = {"format": "statement-question-labels-track1-replay.v108",
                   "identity": identity, **merge(parts)}
    else:
        index, total = map(int, args.shard.split("/"))
        if not 0 <= index < total:
            parser.error("shard index must be between zero and total minus one")
        payload = {"identity": identity, **shard(index, total, args.workers)}
    output = json.dumps(payload, indent=2) + "\n"
    rr._check_no_local_paths(output, "Track 1 replay summary")
    args.out.write_text(output, encoding="utf-8")
    if payload.get("failures"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
