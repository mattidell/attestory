"""Replay the exact ordered prompt-link additions against the ratified surface."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
from shutil import copytree
from tempfile import TemporaryDirectory
from unittest.mock import patch

from probe import (
    BASE, CORE, HERE, PROMPT, asking_positions, baseline_prompts, declarations, digest,
    producer_key, prompt_positions, summary_json,
)
import scratch
from packages.derivation import live
from tests import evidence_loader
from tools import recorded_replay as rr
from tools.package_successor import build_successor, load_corpus

OUTCOMES = {"success": 691, "error": 84}
ERROR_KEYS = "2767993ef1bce2c29eda8c07df82a0533d7180042ba34c387ed9636bf59d487b"


def preceding(directory, file="probe.py"):
    return rr._module("reason_links_" + directory.replace("-", "_"), HERE.parent / directory / file)


def synthetic():
    roster = preceding("eic-child-answers-evidence", "track1_probe.py")
    forms = preceding("statement-labels-forms-evidence")
    sales = preceding("sale-question-names-evidence")
    eic = preceding("eic-answer-questions-evidence")
    harness = rr._get_harness()
    cases = {
        "demo.roster.answered": roster.build("single/kid1/30000/-"),
        "demo.roster.eic": roster.build("single/kid2/30000/age@1+res@2"),
        "demo.roster.eic-same-question": roster.build("single/kid2/30000/age@1+age@2"),
        "demo.roster.relative": roster.build("single/parent2/30000/rel-tin@p1+rel-citizen@p2"),
        "demo.roster.other-dependent-child": roster.build("single/odckid2/30000/lived@2"),
        "demo.eic.unrecorded": eic.build("single/none/7000", "tpssn"),
        "demo.eic.negative-answer": eic.build("single/none/7000", "-"),
        "demo.family.unclosed": harness.opened(),
    }
    for key in ("two-fixes", "missing-basis", "amounts-disagree", "single-sale", "all-valid"):
        cases[f"demo.sale.{key}"] = sales.build_sales(sales.cases()["demo." + key])
    for form in ("int", "div", "ira", "g", "ssa"):
        case = forms.cases()[f"demo.{form}.two-missing"]
        cases[f"demo.withholding.{form}"] = case.acts
    cases["demo.withholding.same-label"] = forms.cases()["demo.int.same-label"].acts
    return cases


def successor(directory):
    base = rr.resolve_core(CORE)
    content = directory / "content"
    releases = directory / "releases"
    copytree(base.content, content)
    copytree(base.releases, releases)
    core = rr.ReplayCore("v110", "v108", "v108", content, releases, loader_from=CORE)
    corpus, _ = load_corpus(base.content)
    import json

    previous = json.loads(base.package_path.read_bytes())
    candidate = build_successor(
        previous, (base.content / f"published-packages.{base.registry}.json").read_bytes(),
        json.loads(base.release_path.read_bytes()), corpus,
        {"package_version": core.version, "release_version": core.release_version},
    )
    if json.loads(candidate.package)["members"] != previous["members"]:
        raise ValueError("successor changed the adopted members")
    core.package_path.write_bytes(candidate.package)
    (content / f"published-packages.{core.registry}.json").write_bytes(candidate.registry)
    core.release_path.write_bytes(candidate.release)
    return core


def compare(before, after, expected):
    if before["outcome"] != after["outcome"]:
        raise ValueError("outcome changed")
    if before["outcome"] != "success":
        left, right = (failure(result) for result in (before, after))
        if left != right:
            raise ValueError("failure changed")
        return
    if list(prompt_positions(after["model"]).items()) != list(expected.items()):
        raise ValueError("ordered prompt positions or producers differ")
    stripped = deepcopy(after["model"])
    for section in stripped["sections"]:
        resolved = section["resolved"]
        expected_indices = [i for i in range(len(resolved.get("reasons", ())))
                            if (section["id"], i) in expected or i in scratch.linked_positions(resolved)]
        if asking_positions(resolved) != expected_indices:
            raise ValueError("asking observer disagrees with ordered links")
        for reason in resolved.get("reasons", ()):
            reason.pop(PROMPT, None)
    if not rr._same(before["model"], stripped):
        raise ValueError("saved model differs beyond prompt links")
    if not rr._same(before["report"], after["report"]):
        raise ValueError("report changed")


def failure(result):
    return rr.failure_snapshot(result["outcome"], result["error"], result["message"])


def classify(model, expected, members, catalog):
    by_type, by_family = declarations(members)
    target_ids = defaultdict(set)
    for index, refs in zip((by_family, by_type), catalog[1:], strict=True):
        for subject, declarations_here in index.items():
            for member in declarations_here:
                target_ids[producer_key(member)].update(
                    ref["targetFactId"] for ref in refs.get(subject, ())
                )
    questions = Counter()
    causes = Counter()
    for section in model["sections"]:
        for i, reason in enumerate(section["resolved"].get("reasons", ())):
            refs = expected.get((section["id"], i))
            if refs is None:
                continue
            keys = [producer_key(ref) for ref in refs]
            questions.update(ref["id"] for ref in refs)
            question_ids = {ref["id"] for ref in refs}
            if "memberLabel" in reason:
                cause = "roster member"
            elif "saleLabel" in reason:
                cause = "sale label"
            elif "input-question.f1099b-box4" in question_ids or any(
                name.endswith(".input-question.f1099b-box4") for name in question_ids
            ):
                cause = "Form 1099-B box 4 amount"
            elif "statementLabel" in reason:
                cause = "other statement label"
            elif len(keys) != 1:
                cause = "several adopted declarations"
            elif not target_ids[keys[0]]:
                cause = "no catalogued answer fact"
            elif len(target_ids[keys[0]]) > 1:
                cause = "several catalogued targets"
            else:
                cause = "single catalogued target, no exact link"
            causes[cause] += 1
    return dict(causes), dict(questions)


def run_list(key, acts, core, is_synthetic):
    base, candidate = scratch.projectors()
    catalog = actual = None
    wanted = {}
    members = ()
    baseline_error = None
    before_rows = None
    baseline_model = None

    def remember_catalog(*args, **kwargs):
        nonlocal catalog
        catalog = original_catalog(*args, **kwargs)
        return catalog

    def project(**kwargs):
        nonlocal actual, members, wanted, baseline_model, before_rows, baseline_error
        original_rows = deepcopy(kwargs["dispositions"])
        try:
            with patch.object(base, "_question_group_catalog", remember_catalog):
                baseline_model = base.build_presentation_model(**kwargs)
        except Exception as exc:
            baseline_error = exc
            try:
                candidate.build_presentation_model(**kwargs)
            except Exception as candidate_exc:
                actual = {"outcome": "error", "error": type(candidate_exc).__name__, "message": str(candidate_exc)}
            else:
                actual = {"outcome": "success"}
            raise
        before_rows = original_rows
        members = kwargs["resolved_members"]
        wanted = baseline_prompts(baseline_model, members)
        return candidate.build_presentation_model(**kwargs)

    original_catalog = base._question_group_catalog
    with patch.object(live, "build_presentation_model", project):
        after = rr.saved_output(core, acts, "demo.reason-links." + digest(key)[:20])
    if baseline_error is not None:
        before, after = after, actual
    elif baseline_model is not None:
        report = dict(after.get("report", {}), dispositions=before_rows)
        before = {"outcome": "success", "model": baseline_model, "report": report}
    else:
        before = after  # the variants share the coordinator before projection
    if is_synthetic and before["outcome"] != "success":
        raise ValueError(f"{key}: synthetic baseline did not save ({before['error']})")
    try:
        compare(before, after, wanted)
    except ValueError as exc:
        if after.get("model") is not None:
            seen = prompt_positions(after["model"])
            missing = [ref["id"] for pos in wanted.keys() - seen.keys() for ref in wanted[pos]]
            extra = [ref["id"] for pos in seen.keys() - wanted.keys() for ref in seen[pos]]
            detail = f" missing={dict(Counter(missing))} extra={dict(Counter(extra))}"
        else:
            detail = f" candidate={after['outcome']}/{after.get('error')}"
            if is_synthetic:
                detail += f" {after.get('message')}"
        raise ValueError(f"{key}: {exc}{detail}") from exc
    row = {
        "key": key, "baseline_outcome": before["outcome"], "candidate_outcome": after["outcome"],
        "links": len(wanted), "ordered_links_sha256": digest([(s, i, refs) for (s, i), refs in wanted.items()]),
    }
    if before["outcome"] == "success":
        model = before["model"]
        row["causes"], row["questions"] = classify(model, wanted, members, catalog)
        row["existing_links"] = sum(len(scratch.linked_positions(s["resolved"])) for s in model["sections"])
    else:
        row["failure_sha256"] = digest(failure(before))
    return row


def run_shard(items):
    return [run_list(*item) for item in items]


def require_outcomes(rows, outcomes, error_keys):
    for field in ("baseline_outcome", "candidate_outcome"):
        if Counter(row[field] for row in rows) != outcomes:
            raise ValueError("outcome census differs")
        if error_keys is not None:
            import hashlib
            import json

            errors = sorted(row["key"] for row in rows if row[field] == "error")
            if hashlib.sha256(json.dumps(errors, separators=(",", ":")).encode()).hexdigest() != error_keys:
                raise ValueError("error set differs")


def summarize(rows, outcomes, error_keys=None):
    require_outcomes(rows, outcomes, error_keys)
    return {
        "lists": len(rows), "outcomes": outcomes, "error_keys_sha256": error_keys,
        "changed_lists": sum(row["links"] > 0 for row in rows),
        "links_added": sum(row["links"] for row in rows),
        "existing_links": sum(row.get("existing_links", 0) for row in rows),
        "causes": dict(sum((Counter(row.get("causes", {})) for row in rows), Counter())),
        "questions": dict(sum((Counter(row.get("questions", {})) for row in rows), Counter())),
        "ordered_links_sha256": digest([(r["key"], r["ordered_links_sha256"]) for r in rows]),
        "failure_details_sha256": digest([(r["key"], r["failure_sha256"]) for r in rows if "failure_sha256" in r]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=7)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cases-only", action="store_true")
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("workers must be positive")
    recorded = {} if args.cases_only else dict(rr.recorded_lists())
    demo = synthetic()
    if owner := evidence_loader.current_owner():
        evidence_loader.release(owner)
    with TemporaryDirectory() as directory:
        next_core = successor(Path(directory))
        work = [(key, acts, CORE, True) for key, acts in demo.items()]
        work.extend([
            ("demo.older-core", demo["demo.family.unclosed"], "v89", True),
            ("demo.successor-core", demo["demo.sale.two-fixes"], next_core, True),
        ])
        work.extend((key, acts, CORE, False) for key, acts in recorded.items())
        batches = args.workers * 3
        shards = [work[i::batches] for i in range(min(batches, len(work)))]
        by_key = {}
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            for result in as_completed([pool.submit(run_shard, shard) for shard in shards]):
                by_key.update((row["key"], row) for row in result.result())
                print(f"{len(by_key)}/{len(work)}", flush=True)
    if by_key.keys() != {key for key, _, _, _ in work}:
        raise ValueError("incomplete replay")
    recorded_rows, demo_rows = ([by_key[key] for key, _, _, flag in work if flag == wanted]
                                for wanted in (False, True))
    summary = {
        "baseline": BASE, "core": CORE, "registry": "v107", "release": "v107",
        "recorded": summarize(recorded_rows, OUTCOMES if recorded else {}, ERROR_KEYS if recorded else None),
        "synthetic": summarize(demo_rows, {"success": len(demo_rows)}),
        "synthetic_cases": {row["key"]: row for row in demo_rows},
    }
    args.out.write_text(summary_json(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
