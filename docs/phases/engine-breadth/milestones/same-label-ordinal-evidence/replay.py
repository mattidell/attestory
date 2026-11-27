"""Compare the ordinal projection with the build's parent on the recorded and probe lists.

Run from the repository with Python. Use --workers for the parallel pool and
--part for an optional checkpoint dedicated to this candidate.
"""
from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Iterator
from contextlib import contextmanager
import copy
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from packages.derivation import presentation_projection as projection
from tools import recorded_replay as rr

PROJECTION_PATH = "packages/derivation/presentation_projection.py"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, check=True, capture_output=True, text=True, timeout=30,
    ).stdout


def _baseline_commit(candidate: str) -> str:
    prefix = "build(same-label-ordinal)"
    matches = _git("log", "--format=%H%x09%s", "--basic-regexp", f"--grep=^{prefix}", candidate)
    builds = [
        revision for revision, _, subject in (line.partition("\t") for line in matches.splitlines())
        if subject.startswith(prefix)
    ]
    if len(builds) != 1:
        raise ValueError(f"Expected one {prefix} commit in candidate history, found {len(builds)}")
    return _git("rev-parse", "--verify", f"{builds[0]}^").strip()


@lru_cache(maxsize=1)
def _probe() -> Any:
    path = HERE.parent / "same-label-members-evidence/probe.py"
    name = "slo_replay_members_probe"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _baseline_definitions(baseline: str) -> dict[str, Any]:
    source = _git("show", f"{baseline}:{PROJECTION_PATH}")
    names = frozenset(_probe()._changed_names((REPO / PROJECTION_PATH).read_text(), source))
    if names != {
        "_RosterMembers", "_closure_question_reasons", "_finalize_question_references",
        "_reasons_beside", "_validate_resolved", "_validate_question_groups",
    }:
        raise ValueError(f"Unexpected projection definitions differ from baseline: {sorted(names)}")
    namespace: dict[str, Any] = {"__name__": "slo_baseline_projection"}
    exec(compile(source, PROJECTION_PATH, "exec"), namespace)
    namespace.update({name: value for name, value in vars(projection).items()
                      if name not in names and not name.startswith("__")})
    return {name: namespace[name] for name in names}


@contextmanager
def _baseline_projection(baseline: str) -> Iterator[None]:
    replacement = _baseline_definitions(baseline)
    original = {name: getattr(projection, name) for name in replacement}
    vars(projection).update(replacement)
    try:
        yield
    finally:
        vars(projection).update(original)


def _snapshot(saved: dict[str, Any]) -> dict[str, Any]:
    if saved["outcome"] == "success":
        return rr.snapshot(saved["model"], saved["report"])
    return rr.failure_snapshot(saved["outcome"], saved["error"], saved["message"])


def _restore_member_reasons(
    before: dict[str, Any], after: dict[str, Any],
) -> tuple[dict[str, Any], Counter[str]] | None:
    """Reverse permitted edits only after checking the original reason content and multiplicity."""
    restored = copy.deepcopy(after)
    counts: Counter[str] = Counter()
    old_sections = {section["id"]: section["resolved"] for section in before["model"]["sections"]}
    for section in restored["model"]["sections"]:
        prior = old_sections.get(section["id"], {})
        resolved = section["resolved"]
        old = prior.get("reasons")
        new = resolved.get("reasons")
        if old == new:
            continue
        if not isinstance(old, list) or not isinstance(new, list):
            return None
        old_plain = [(index, reason) for index, reason in enumerate(old) if "memberLabel" not in reason]
        new_plain = [(index, reason) for index, reason in enumerate(new) if "memberLabel" not in reason]
        if old_plain != new_plain:
            return None
        old_members = [reason for reason in old if "memberLabel" in reason]
        new_members = [reason for reason in new if "memberLabel" in reason]
        ordinals = [reason["memberOrdinal"] for reason in new_members if "memberOrdinal" in reason]
        if not ordinals or any(type(ordinal) is not int or ordinal < 1 for ordinal in ordinals):
            return None
        stripped = [{k: v for k, v in reason.items() if k != "memberOrdinal"} for reason in new_members]
        if Counter(map(rr._encoded, old_members)) != Counter(map(rr._encoded, stripped)):
            return None
        counts["ordinals_added"] += len(ordinals)
        counts["lines_reordered"] += old_members != stripped
        resolved["reasons"] = old
    return restored, counts


def compare_saved(before: dict[str, Any], after: dict[str, Any], *, probe: bool) -> dict[str, Any]:
    left, right = _snapshot(before), _snapshot(after)
    differences = rr.diff_snapshots(left, right)
    verdict: dict[str, Any] = {
        "class": "unexpected" if differences else "identical",
        "outcomes": [left["outcome"], right["outcome"]],
        "differences": len(differences),
    }
    if not differences or not probe or left["outcome"] != "success" or right["outcome"] != "success":
        return verdict
    restoration = _restore_member_reasons(before, after)
    if restoration is None:
        return verdict
    restored, counts = restoration
    if not rr.diff_snapshots(left, _snapshot(restored)):
        verdict.update({"class": "ordinals-and-order", **counts})
    return verdict


def report_value_control() -> dict[str, Any]:
    """A probe with an allowed ordinal and a forbidden change to its report."""
    reason = {"memberLabel": "Demo Sam", "sentence": "Demo member question"}
    before: dict[str, Any] = {
        "outcome": "success",
        "model": {"sections": [{"id": "demo.line", "resolved": {"reasons": [reason]}}]},
        "report": {"demo_value": 0},
    }
    after = copy.deepcopy(before)
    after["model"]["sections"][0]["resolved"]["reasons"][0]["memberOrdinal"] = 1
    after["report"]["demo_value"] = 1
    return compare_saved(before, after, probe=True)


def _compare(key: str, acts: rr.Acts, cores: tuple[Any, ...]) -> dict[str, Any]:
    core, _candidate, baseline = cores
    run_id = "demo.fsr." + sha256(key.encode()).hexdigest()[:20]
    with _baseline_projection(baseline):
        before = rr.saved_output(core, acts, run_id)
    after = rr.saved_output(core, acts, run_id)
    return compare_saved(before, after, probe=key.startswith("probe:"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--part", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    candidate = _git("rev-parse", "HEAD").strip()
    if (REPO / PROJECTION_PATH).read_text() != _git("show", f"{candidate}:{PROJECTION_PATH}"):
        raise ValueError("Commit the candidate projection before replaying it")
    baseline = _baseline_commit(candidate)
    control = report_value_control()
    if control["class"] != "unexpected":
        raise ValueError("The report-value control should fail")
    core = rr.resolve_core("v108")
    probe = _probe()
    recorded = rr.recorded_lists()
    probes = [(f"probe:{case}", probe.build(case, core.content)) for case in probe.CASES]
    if len(recorded) != 775 or len(probes) != 23:
        raise ValueError("Unexpected replay corpus size")
    # Keep checkpoints bound to both revisions as well as the core.
    rows = rr.replay([*recorded, *probes], (core, candidate, baseline), _compare,
                     workers=args.workers, part=args.part)
    identical = sorted(key for key, _ in recorded if rows[key]["class"] == "identical")
    probe_results = {key.removeprefix("probe:"): rows[key] for key, _ in probes}
    probe_classes = Counter(row["class"] for row in probe_results.values())
    if len(identical) != 775 or probe_classes != {"identical": 6, "ordinals-and-order": 17}:
        raise ValueError(f"Unexpected replay results: {len(identical)} recorded identical, probes {probe_classes}")
    summary = {
        "baseline": baseline,
        "candidate": candidate,
        "core": rr.core_fingerprint(core),
        "control_report_value": control,
        "recorded": {
            "identical": identical,
            "both_errors": sorted(key for key in identical if rows[key]["outcomes"] == ["error", "error"]),
        },
        "probes": probe_results,
    }
    output = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    rr._check_no_local_paths(output, str(args.out))
    args.out.write_text(output)
    print(f"{len(identical)} recorded identical, probes {dict(probe_classes)}, report-value control rejected")


if __name__ == "__main__":
    main()
