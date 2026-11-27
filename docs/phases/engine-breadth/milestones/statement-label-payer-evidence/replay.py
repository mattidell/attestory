"""Replay all recorded lists and explicit synthetic cases on core v109."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from dataclasses import dataclass
from functools import cache
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))

import scratch
from packages.derivation import live
from tests import evidence_loader
from tools import recorded_replay as rr

CORE = "v109"
FIELD = "statementPayerLabel"
STRUCTURAL_MISMATCH = "successful save differs structurally from the expected model or report"
STMT = "demo Statement"
ZULU = "demo Zulu Bank"
ALPHA = "demo Alpha Bank"
STATEMENT_KINDS = {
    scratch.B_SPEC[0], *(spec[0] for spec in scratch.WITHHOLDING.values()),
    "tax.us.ssa1099-statement",
}
FORM_KEYS = ("int", "div", "ira", "g", "ssa")
FORM_QUESTIONS = dict(zip(FORM_KEYS, (*scratch.WITHHOLDING, scratch.SSA), strict=True))


@dataclass(frozen=True)
class Case:
    acts: rr.Acts
    question: str
    ordered_names: tuple[str | None, ...]


def synthetic(recorded):
    forms = rr._module("payer_withholding_probe", HERE.parent / "statement-labels-forms-evidence/probe.py")
    sales = rr._module("payer_sale_probe", HERE.parent / "statement-question-labels-evidence/probe.py")
    out = {}

    def withhold(form, scenario, amounts, labels, names, expected):
        acts = forms.return_with_amounts(form, amounts)
        forms.label_statements(acts, form, labels)
        if form != "ssa":
            party_kind = scratch.WITHHOLDING[FORM_QUESTIONS[form]][1]
            by_id = {
                entity["id"]: entity for act in acts
                if (entity := act["payload"].get("entity")) and entity.get("kind") == party_kind
            }
            for entity, name in zip(list(by_id.values())[-len(names):], names, strict=True):
                entity["label"] = name
        out[f"demo.{form}.{scenario}"] = Case(forms.close_sale_scope(acts), FORM_QUESTIONS[form], expected)

    for form in FORM_KEYS:
        expected = (None, None) if form == "ssa" else (ZULU, ALPHA)
        withhold(form, "duplicate", (None, None), (STMT, STMT), (ZULU, ALPHA), expected)

    for scenario, labels, names, expected in (
        ("distinct-statements", (STMT, "demo Other"), (ZULU, ALPHA), (None, None)),
        ("near-statements", (STMT, "demo statement "), (ZULU, ALPHA), (None, None)),
        ("blank-payer", (STMT, STMT), (ZULU, " "), (None, None)),
        ("same-payer-label", (STMT, STMT), (ZULU, ZULU), (None, None)),
        ("near-payers", (STMT, STMT), (ZULU, " demo zulu  bank "), (None, None)),
        ("literal-payer", (STMT, STMT), ("demo  Zulu & Sons", ALPHA), ("demo  Zulu & Sons", ALPHA)),
    ):
        withhold("int", scenario, (None, None), labels, names, expected)
    withhold("int", "answered-peer", (None, 0.0), (STMT, STMT), (ZULU, ALPHA), (ZULU,))
    withhold("int", "all-answered", (0.0, 0.0), (STMT, STMT), (ZULU, ALPHA), ())

    for form, question in (("box4", scratch.BOX4), ("box7", scratch.BOX7)):
        for scenario, drops, labels, names, expected in (
            ("duplicate", (0, 1), (STMT, STMT), (ZULU, ALPHA), (ZULU, ALPHA)),
            ("answered-peer", (1,), (STMT, STMT), (ZULU, ALPHA), (ALPHA,)),
            ("same-broker-label", (0, 1), (STMT, STMT), (ZULU, ZULU), (None, None)),
            ("distinct-statements", (0, 1), (STMT, "demo Other"), (ZULU, ALPHA), (None, None)),
        ):
            acts = sales.drop_answers(recorded[sales.BASE2], ((question, drops),))
            statements = sales.statement_entities(acts)
            acts = sales.relabel(acts, dict(zip(statements, labels, strict=True)))
            brokers = {
                entity["id"]: entity for act in acts
                if (entity := act["payload"].get("entity")) and entity.get("kind") == scratch.BROKER
            }
            for entity, name in zip(brokers.values(), names, strict=True):
                entity["label"] = name
            out[f"demo.{form}.{scenario}"] = Case(acts, question, expected)
    return out


@cache
def question_texts():
    content = rr.resolve_core(CORE).content
    package = json.loads(rr.resolve_core(CORE).package_path.read_text())
    adopted = {(member["id"], member["version"]) for member in package["members"]
               if member["role"] == "input-question"}
    questions = {}
    for path in content.glob("input-question.*.json"):
        item = json.loads(path.read_text())
        if (item["id"], item["version"]) in adopted:
            questions[item["fact_type"]["id"]] = item["question"]
    return questions


def introduced_duplicates(acts):
    """Count distinct introduced IDs per exact label, before applying currency."""
    entities = {}
    for act in acts:
        entity = act["payload"].get("entity") or act["payload"].get("replacement")
        if entity and entity.get("kind") in STATEMENT_KINDS:
            entities[entity["id"]] = (entity["kind"], entity["label"])
    return sorted({kind for (kind, _), count in Counter(entities.values()).items() if count > 1})


def current_duplicates(state, current_ids):
    """Inventory current statement IDs with one of the form's source findings."""
    source_kinds = {
        source: kind
        for kind, _, types in (scratch.B_SPEC, *scratch.WITHHOLDING.values())
        for source in types
    }
    source_kinds[scratch.TAX + "ssa1099.box5-net-benefits"] = "tax.us.ssa1099-statement"
    entities = state.fact_state.entities
    groups = defaultdict(set)
    for finding_id in current_ids:
        fact_type, _, pairs = state.findings.get(finding_id, {}).get("fact_id", "").partition("|")
        if fact_type not in source_kinds:
            continue
        keys = dict(pair.split("=", 1) for pair in pairs.split(","))
        statement = keys.get("statement")
        entity = entities.get(statement)
        if entity and entity.status == "current" and entity.entity["kind"] == source_kinds[fact_type]:
            groups[entity.entity["kind"], keys["tax-year"], entity.entity["label"]].add(statement)
    return sorted({kind for (kind, _, _), ids in groups.items() if len(ids) > 1})


def reasons(section):
    return (section.get("resolved") or {}).get("reasons", [])


def for_question(section, text):
    return [index for index, reason in enumerate(reasons(section))
            if reason["sentence"] == text and reason.get("statementLabel", {}).get("statement")]


def expected_additions(model, case):
    if case is None:
        return {}
    text = question_texts()[case.question]
    expected = {}
    matching_sections = 0
    for section in model["sections"]:
        indices = for_question(section, text)
        if not indices:
            continue
        matching_sections += 1
        for index, name in zip(indices, case.ordered_names, strict=True):
            if name is not None:
                expected[section["id"], index] = name
    if bool(matching_sections) != bool(case.ordered_names):
        raise ValueError("synthetic case did not exercise the expected statement question")
    return expected


def check_model(before, after, expected):
    """Apply only the predetermined additions and compare every saved field."""
    want = deepcopy(before)
    for section in want["sections"]:
        for index, reason in enumerate(reasons(section)):
            name = expected.get((section["id"], index))
            if name is not None:
                reason[FIELD] = name
    # Check the exact names at their expected reason positions.
    actual = {(section["id"], index): reason[FIELD]
              for section in after["sections"]
              for index, reason in enumerate(reasons(section)) if FIELD in reason}
    if actual != expected:
        raise ValueError("exact names or positions differ from expectations")
    return want


def compare(before, after, expected):
    if before["outcome"] != after["outcome"]:
        raise ValueError(f"outcomes differ: {before['outcome']} versus {after['outcome']}")
    if before["outcome"] == "success":
        want = check_model(before["model"], after["model"], expected)
        if not rr._same(want, after["model"]) or not rr._same(before["report"], after["report"]):
            raise ValueError(STRUCTURAL_MISMATCH)
        return
    left, right = (rr.failure_snapshot(s["outcome"], s["error"], s["message"]) for s in (before, after))
    if left != right:
        raise ValueError("failure class or message differs")


def check_controls(key, before, after, expected, case):
    if key not in {"demo.int.duplicate", "demo.int.distinct-statements"}:
        return []
    mutations = {}
    if key == "demo.int.duplicate":
        section = next(s for s in after["model"]["sections"] if s["id"].endswith("line-25b"))
        i, j = for_question(section, question_texts()[case.question])
        mutations["removed_name"] = [(i, None)]
        mutations["swapped_names"] = [(i, ALPHA), (j, ZULU)]
    else:
        section = next(s for s in after["model"]["sections"] if s["id"].endswith("line-25b"))
        i, _ = for_question(section, question_texts()[case.question])
        mutations["added_name_to_distinct_statement"] = [(i, ALPHA)]
    detected = []
    for name, changes in mutations.items():
        changed = deepcopy(after)
        target = next(s for s in changed["model"]["sections"] if s["id"] == section["id"])
        for index, value in changes:
            reason = reasons(target)[index]
            if value is None:
                del reason[FIELD]
            else:
                reason[FIELD] = value
        try:
            compare(before, changed, expected)
        except ValueError as exc:
            if str(exc) != "exact names or positions differ from expectations":
                raise
            detected.append(name)
        else:
            raise ValueError(f"replay accepted mutation {name}")
    return detected


def check_dom(page, output, case, expected):
    model = output["model"]
    text = question_texts()[case.question]
    inputs, expected_lines = [], {}
    for section in model["sections"]:
        if not (indices := for_question(section, text)):
            continue
        key = section["id"]
        refs = {r["groupId"] for r in section["resolved"].get("questionRefs", [])}
        inputs.append(json.dumps({"key": key, "model": {
            **model, "sections": [section],
            "questionGroups": [g for g in model["questionGroups"] if g["id"] in refs],
        }}))
        expected_lines[key] = [
            reasons(section)[i]["statementLabel"]["statement"] + (", " + name if name else "") + ":"
            for i in indices for name in (expected.get((key, i)),)
        ]
    if not inputs:
        return
    checker = HERE.parent / "page-plain-words-evidence/check_page_dom.mjs"
    checked = subprocess.run(
        ["node", str(checker), str(page)], check=True, capture_output=True, text=True,
        input="\n".join(inputs) + "\n", timeout=30, env={**os.environ, "PPW_CHECK_DETAIL": "1"},
    )
    results = json.loads(checked.stdout)
    if results.keys() != expected_lines.keys():
        raise ValueError("DOM checker omitted a section")
    for key, result in results.items():
        lines = result["first_read_text"].splitlines()
        found = [lines[i - 1].rstrip() for i, line in enumerate(lines)
                 if line == text and i and lines[i - 1].rstrip().endswith(":")]
        if found != expected_lines[key] or result["section_errors"]:
            raise ValueError(f"wrong rendered question labels on {key}: {found!r}")


def run_list(key, acts, case, core, page):
    run_id = "demo.statement-label-payer." + hashlib.sha256(key.encode()).hexdigest()[:20]
    baseline, candidate = scratch.projectors()
    introduced = introduced_duplicates(acts)
    current = []

    def baseline_with_inventory(**kwargs):
        if introduced:
            current.extend(current_duplicates(kwargs["state"], kwargs["current_finding_ids"]))
        return baseline(**kwargs)

    with patch.object(live, "build_presentation_model", baseline_with_inventory):
        before = rr.saved_output(core, acts, run_id)
    with patch.object(live, "build_presentation_model", candidate):
        after = rr.saved_output(core, acts, run_id)
    if case is not None and before["outcome"] != "success":
        raise ValueError(f"{key}: baseline did not save: {before['message']}")
    expected = expected_additions(before["model"], case) if before["outcome"] == "success" else {}
    try:
        compare(before, after, expected)
    except ValueError as exc:
        if after["outcome"] == "error" and before["outcome"] == "success":
            raise ValueError(f"{key}: scratch failed: {after['message']}") from exc
        raise ValueError(f"{key}: {exc}") from exc
    controls = check_controls(key, before, after, expected, case)
    if case is not None:
        try:
            check_dom(page, after, case, expected)
        except ValueError as exc:
            raise ValueError(f"{key}: {exc}") from exc
    return {
        "outcome": before["outcome"], "names": len(expected), "controls": controls,
        "duplicates": introduced, "current_duplicates": current,
    }


def run_shard(items, core, page):
    return {key: run_list(key, acts, case, core, page) for key, acts, case in items}


def summarize(items, results, expected_lists):
    rows = [results[key] for key, _, _ in items]
    changed = sum(row["names"] > 0 for row in rows)
    if changed != expected_lists:
        raise ValueError(f"expected {expected_lists} changed lists, found {changed}")
    return {
        "lists": len(rows), "changed_lists": changed, "names_added": sum(row["names"] for row in rows),
        "outcomes": dict(Counter(row["outcome"] for row in rows)),
        "lists_with_introduced_duplicate_labels": dict(Counter(kind for row in rows for kind in row["duplicates"])),
        "saved_lists_with_current_duplicate_labels": dict(Counter(
            kind for row in rows if row["outcome"] == "success" for kind in row["current_duplicates"]
        )),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=9)
    parser.add_argument("--cases-only", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be positive")
    scratch.check_baseline()
    baseline, page = scratch.sources()
    scratch.projectors()
    all_recorded = dict(rr.recorded_lists())
    cases = synthetic(all_recorded)
    recorded = [] if args.cases_only else [(key, acts, None) for key, acts in all_recorded.items()]
    probes = [(key, case.acts, case) for key, case in cases.items()]
    if not args.cases_only and len(recorded) != 775:
        raise ValueError("recorded corpus count changed")
    if owner := evidence_loader.current_owner():
        evidence_loader.release(owner)
    core = rr.resolve_core(CORE)
    n = min(2 * args.workers - 1, len(recorded))
    shards = [[probe] for probe in probes] + [recorded[i::n] for i in range(n)]
    results = {}
    with tempfile.TemporaryDirectory() as scratch_dir:
        page_path = Path(scratch_dir) / "citation-walk.v1.html"
        page_path.write_text(scratch.scratch_page(page), encoding="utf-8")
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn")) as pool:
            futures = [pool.submit(run_shard, shard, core, page_path) for shard in shards]
            for future in as_completed(futures):
                try:
                    results.update(future.result())
                except Exception as exc:
                    print(f"Replay failed: {exc}", file=sys.stderr, flush=True)
                    if hasattr(pool, "terminate_workers"):
                        pool.terminate_workers()
                    raise
                print(f"{len(results)}/{len(recorded) + len(probes)} lists", file=sys.stderr, flush=True)
    if results.keys() != {key for key, _, _ in recorded + probes}:
        raise ValueError("incomplete replay")
    controls = sorted(control for result in results.values() for control in result["controls"])
    if controls != ["added_name_to_distinct_statement", "removed_name", "swapped_names"]:
        raise ValueError(f"incomplete controls: {controls}")
    summary = {
        "baseline": scratch.BASE, "core": CORE, "registry": core.registry, "release": core.release_version,
        "workers": args.workers, "shards": len(shards), "recorded": summarize(recorded, results, 0),
        "synthetic": summarize(probes, results, 10), "controls_rejected": controls,
        "synthetic_names_by_case": {key: results[key]["names"] for key in cases},
        "unexpected_differences": 0,
        "scratch_projection_sha256": hashlib.sha256(scratch.scratch_projection(baseline).encode()).hexdigest(),
        "scratch_page_sha256": hashlib.sha256(scratch.scratch_page(page).encode()).hexdigest(),
    }
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    rr._check_no_local_paths(encoded, "P0 replay summary")
    args.out.write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
