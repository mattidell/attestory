"""Replay published core v108 against v109 in one fresh parallel run.

The v108 run uses the projection from before the Track 1 build. The v109
run uses the current production path. The comparison requires the exact
ordered trailing explanations for current answers to questions on blocked
lines. The full saved model and report are compared, allowing the core
version move.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import multiprocessing
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import cache
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from packages.derivation import live  # noqa: E402
from tools import recorded_replay as rr  # noqa: E402

P = "tax.us.2025."
CORES = ("v108", "v109")
FOUR_ANSWERS = "probe/fails/single/15"
FOUR_ANSWER_ADDITIONS = 112
PROJECTION = "packages/derivation/presentation_projection.py"
REPLAY_FILES = (PROJECTION, "packages/tax/loader.py", "packages/derivation/loader.py",
                "packages/derivation/live.py", "packages/derivation/runner.py")


@cache
def baseline_ref() -> str:
    history = subprocess.check_output(
        ["git", "log", "--format=%H%x09%s", "HEAD"], cwd=REPO, text=True, timeout=30,
    )
    for row in history.splitlines():
        ref, _, subject = row.partition("\t")
        if subject.startswith("build(line16-next-step)"):
            return subprocess.check_output(
                ["git", "rev-parse", ref + "^"], cwd=REPO, text=True, timeout=30,
            ).strip()
    raise RuntimeError("Track 1 build commit is absent from history")


@cache
def baseline_projection_source() -> bytes:
    return subprocess.check_output(["git", "show", f"{baseline_ref()}:{PROJECTION}"], cwd=REPO, timeout=30)


@cache
def baseline_projector() -> Any:
    name = "packages.derivation._line16_replay_baseline"
    module = ModuleType(name)
    module.__file__ = str(REPO / PROJECTION)
    sys.modules[name] = module
    exec(compile(baseline_projection_source(), PROJECTION, "exec"), vars(module))
    return module.build_presentation_model


@cache
def _probe() -> Any:
    spec = importlib.util.spec_from_file_location("l16ns_probe_for_replay", HERE / "probe.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def explanations() -> dict[str, tuple[str, str, str]]:
    """Map each adopted sentence to its exact fact type pin and answer value."""
    core = rr.resolve_core("v109")
    package = json.loads(core.package_path.read_text(encoding="utf-8"))
    members = {(member["id"], member["version"]) for member in package["members"]
               if member["role"] == "answer-explanation"}
    declared = {}
    for path in core.content.glob("answer-explanation.exception1-*.json"):
        citizen = json.loads(path.read_text(encoding="utf-8"))
        if (citizen["id"], citizen["version"]) in members:
            pin = citizen["fact_type"]
            declared[citizen["explanation"]] = (pin["id"], pin["version"], citizen["value"])
    assert len(declared) == len(members) == 4
    return declared


def candidate_output(core: Any, acts: rr.Acts, run_id: str) -> tuple[dict, dict]:
    """Read current findings at the coordinator boundary, independently of the saved reasons."""
    answers: dict[str, list[tuple[str, Any]]] = defaultdict(list)
    fact_types = {pin[0] for pin in explanations().values()}
    projector = live.build_presentation_model

    def observe(**kwargs: Any) -> dict:
        state = kwargs["state"]
        for finding_id in kwargs["current_finding_ids"]:
            finding = state.findings.get(finding_id, {})
            fact_id = finding.get("fact_id", "")
            fact_type = fact_id.partition("|")[0]
            if fact_type in fact_types:
                version = state.fact_state.fact_types[fact_type]["version"]
                answers[fact_id].append((version, finding["value"]))
        return projector(**kwargs)

    with patch.object(live, "build_presentation_model", observe):
        return rr.saved_output(core, acts, run_id), answers


def version_expectation() -> rr.Expectation:
    return rr.version_change(P + "package.core-calculations", *CORES)


def reason_expectations(left: dict, right: dict, answers: dict) -> tuple[list[rr.Expectation], list[dict]]:
    if left["outcome"] != "success" or right["outcome"] != "success":
        return [], []
    model = left["model"]
    groups = {group["id"]: group["answerTarget"] for group in model.get("questionGroups", [])}
    candidate = {line["id"]: line["resolved"] for line in right["model"]["sections"]}
    specs = []
    mismatches = []
    sections = model["sections"]
    for line, label in zip(sections, rr._item_labels(sections), strict=True):
        resolved = line["resolved"]
        if resolved.get("disposition") != "blocked":
            continue
        before = resolved.get("reasons", [])
        current = set()
        for ref in resolved.get("questionRefs", []):
            target = groups[ref["groupId"]]
            findings = answers.get(target["factId"], [])
            if len(findings) == 1 and findings[0][0] == target["factTypeVersion"] and isinstance(findings[0][1], str):
                current.add((target["factTypeId"], target["factTypeVersion"], findings[0][1]))
        existing = {reason["sentence"] for reason in before}
        added = sorted(sentence for sentence, declaration in explanations().items()
                       if declaration in current and sentence not in existing)
        identity = f"sections[{label}]"
        expected = [*before, *({"sentence": sentence} for sentence in added)]
        after = candidate.get(line["id"], {}).get("reasons", [])
        if after != expected:
            mismatches.append({"kind": "page", "identity": identity, "attribute": "exact reason sequence",
                               "change": "mismatch", "before": expected, "after": after})
            continue
        for index, sentence in enumerate(added, start=len(before)):
            fact_type, _, _ = explanations()[sentence]
            slug = fact_type.removeprefix(P + "exception1.")
            reason_identity = re.escape(f"{identity}/resolved.reasons[[{index}]]")
            specs.append(rr.Expectation(("page",), "sentence", f"^{reason_identity}$",
                                        "added", after=sentence, note=f"answer-explanation:{slug}"))
        if added:
            specs.append(rr.Expectation(("page",), r"resolved\.reasons@order", f"^{re.escape(identity)}$", "changed",
                                        note="reasons order record of a line that gained an explanation"))
    return specs, mismatches


def snapshot(saved: dict) -> dict:
    if saved["outcome"] == "success":
        return rr.snapshot(saved["model"], saved["report"])
    return rr.failure_snapshot(saved["outcome"], saved["error"], saved["message"])


def compare(left: dict, right: dict, answers: dict) -> dict:
    reasons, mismatches = reason_expectations(left, right, answers)
    verdict = rr.classify_full(snapshot(left), snapshot(right), [version_expectation(), *reasons])
    if mismatches:
        verdict["class"] = "unexpected"
        verdict["unexpected"].extend(mismatches)
    verdict["outcomes"] = [left["outcome"], right["outcome"]]
    return verdict


def run_pair(key: str, acts: rr.Acts, cores: tuple) -> tuple[dict, dict, dict]:
    run_id = "demo.fsr." + hashlib.sha256(key.encode()).hexdigest()[:20]
    with patch.object(live, "build_presentation_model", baseline_projector()):
        left = rr.saved_output(cores[0], acts, run_id)
    right, answers = candidate_output(cores[1], acts, run_id)
    return left, right, answers


def replay_list(key: str, acts: rr.Acts, cores: tuple) -> dict:
    verdict = compare(*run_pair(key, acts, cores))
    if key == FOUR_ANSWERS:
        require_four_answer_additions(verdict)
    verdict["unexpected_total"] = len(verdict["unexpected"])
    verdict["unexpected"] = verdict["unexpected"][:3]
    return verdict


def replay_shard(items: list[tuple[str, rr.Acts]], cores: tuple) -> dict:
    return {key: replay_list(key, acts, cores) for key, acts in items}


def run_shards(items: list[tuple[str, rr.Acts]], cores: tuple, workers: int) -> tuple[dict, int]:
    shard_count = min(len(items), workers * 2)
    results = {}
    with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context("spawn")) as pool:
        shards = [pool.submit(replay_shard, items[index::shard_count], cores) for index in range(shard_count)]
        for shard in as_completed(shards):
            results.update(shard.result())
            print(f"[{len(results)}/{len(items)}] completed", file=sys.stderr, flush=True)
    return results, shard_count


def wrong_answer_control(cores: tuple) -> dict:
    key = "probe/control/c1-unanswered"
    acts = dict(("probe/" + key, acts) for key, acts in _probe().cases())[key]
    left, right, answers = run_pair(key, acts, cores)
    real = compare(left, right, answers)
    assert real["class"] == "expected_changes"
    c1 = P + "exception1.only-box2a-capital-gains"
    sentence = next(text for text, (fact_type, _, value) in explanations().items()
                    if (fact_type, value) == (c1, "no"))
    assert not any(fact_id.partition("|")[0] == c1 for fact_id in answers)
    mutated = copy.deepcopy(right)
    field = P + "form1040.line-16"
    line = next(line for line in mutated["model"]["sections"] if line["field"]["id"] == field)
    assert line["resolved"]["disposition"] == "blocked"
    line["resolved"].setdefault("reasons", []).append({"sentence": sentence})
    verdict = compare(left, mutated, answers)
    assert verdict["class"] == "unexpected"
    assert any(diff["attribute"] == "sentence" and diff["after"] == sentence for diff in verdict["unexpected"])
    return {"list": key, "field": field, "fact_type": c1, "injected_value": "no",
            "recorded_answer": None, "unmodified": real["class"], "mutated": verdict["class"],
            "unexpected_differences": len(verdict["unexpected"])}


def require_four_answer_additions(verdict: dict) -> int:
    additions = sum(count for note, count in verdict["expected_by_note"].items()
                    if note.startswith("answer-explanation:"))
    if additions != FOUR_ANSWER_ADDITIONS:
        verdict["class"] = "unexpected"
        verdict["unexpected"].append({"kind": "page", "identity": FOUR_ANSWERS, "attribute": "explanation count",
                                      "change": "mismatch", "before": FOUR_ANSWER_ADDITIONS, "after": additions})
    return additions


def explanation_sequence_controls(cores: tuple) -> dict:
    """Removing every explanation or reversing line 16's explanations must fail."""
    acts = dict(_probe().cases())[FOUR_ANSWERS.removeprefix("probe/")]
    left, right, answers = run_pair(FOUR_ANSWERS, acts, cores)
    real = compare(left, right, answers)
    additions = require_four_answer_additions(real)
    assert real["class"] == "expected_changes"
    missing = copy.deepcopy(right)
    approved = explanations()
    for line in missing["model"]["sections"]:
        resolved = line["resolved"]
        if "reasons" in resolved:
            resolved["reasons"] = [reason for reason in resolved["reasons"] if reason["sentence"] not in approved]
    reversed_line = copy.deepcopy(right)
    field = P + "form1040.line-16"
    line = next(line for line in reversed_line["model"]["sections"] if line["field"]["id"] == field)
    reasons = line["resolved"]["reasons"]
    assert all(reason["sentence"] in approved for reason in reasons[-4:])
    reasons[-4:] = reversed(reasons[-4:])
    results = {}
    for name, mutated in (("all_removed", missing), ("line16_reversed", reversed_line)):
        verdict = compare(left, mutated, answers)
        assert verdict["class"] == "unexpected"
        assert any(diff["attribute"] == "exact reason sequence" for diff in verdict["unexpected"])
        results[name] = verdict["class"]
    return {"list": FOUR_ANSWERS, "unmodified_additions": additions, **results}


def summarize(results: dict, cores: tuple, controls: dict) -> dict:
    classes = Counter(row["class"] for row in results.values())
    return {
        "format": "line16-next-step-track1-replay.v1",
        "cores": [rr.core_fingerprint(core) for core in cores],
        "baseline_projection_sha256": hashlib.sha256(baseline_projection_source()).hexdigest(),
        "candidate_code_sha256": {p: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for p in REPLAY_FILES},
        "lists": len(results),
        "recorded_lists": sum(not key.startswith("probe/") for key in results),
        "probe_lists": sum(key.startswith("probe/") for key in results),
        "classes": dict(sorted(classes.items())),
        "passing": len(results) - classes["unexpected"],
        "failing": classes["unexpected"],
        "unexpected_differences": sum(row["unexpected_total"] for row in results.values()),
        "expected_by_note": dict(sorted(sum((Counter(row["expected_by_note"]) for row in results.values()), Counter()).items())),
        "lists_with_added_explanations": sorted(key for key, row in results.items()
                                                if any(n.startswith("answer-explanation:") for n in row["expected_by_note"])),
        "unexpected_lists": {key: row["unexpected"] for key, row in results.items() if row["unexpected"]},
        **controls,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    subset = parser.add_mutually_exclusive_group()
    subset.add_argument("--only-probe", action="store_true")
    subset.add_argument("--controls", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be positive")
    cores = tuple(rr.resolve_core(c) for c in CORES)
    controls = {"wrong_answer_control": wrong_answer_control(cores),
                "explanation_sequence_controls": explanation_sequence_controls(cores)}
    if args.controls:
        body = controls
    else:
        probe = [("probe/" + key, acts) for key, acts in _probe().cases()]
        chosen = probe if args.only_probe else rr.recorded_lists() + probe
        if len({key for key, _ in chosen}) != len(chosen):
            raise ValueError("replay list keys are not unique")
        results, shard_count = run_shards(chosen, cores, args.workers)
        body = summarize(results, cores, controls)
        body.update(workers=args.workers, shards=shard_count)
    text = json.dumps(body, indent=2, ensure_ascii=False) + "\n"
    rr._check_no_local_paths(text, "replay summary")
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return int(bool(body.get("unexpected_lists")))


if __name__ == "__main__":
    raise SystemExit(main())
