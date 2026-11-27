"""Run the v109 saved-surface comparison in fresh parallel shards."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from functools import cache
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import re
import subprocess
import sys
from types import ModuleType
from typing import Any
from unittest.mock import patch

import probe
from packages.derivation import live
from packages.kernel.facts import facts_of
from tests import evidence_loader
from tools import recorded_replay as rr

BASE = "c1d060d738cc83ab59adc0981092c0358bfcea50"
PROJECTION = "packages/derivation/presentation_projection.py"
RECORDED_TOTAL = 775
EXPECTED_GAIN = {"recorded": 2, "synthetic": 17}


@cache
def baseline_source() -> str:
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"],
                   cwd=probe.REPO, check=True, timeout=15)
    return subprocess.check_output(["git", "show", f"{BASE}:{PROJECTION}"],
                                   cwd=probe.REPO, text=True, timeout=15)


def scratch_source() -> str:
    """Extend only the projection in memory, using the actual ADR 0089 walk."""
    source = baseline_source()
    forms = {form.withholding: form.statement_kind for form in probe.FORMS.values()}
    changes = (
        ('        needs: Mapping[str, frozenset[str]],\n',
         '        needs: Mapping[str, frozenset[str]],\n'
         '        additional_kinds: Mapping[str, str],\n'),
        ('self._identity: dict[str, list[str]] = {}',
         'self._identity: dict[str, list[str]] = {}\n        self._additional_kinds = additional_kinds'),
        ('            entity_kinds=STATEMENT_QUESTION_ENTITY_KINDS, needs=STATEMENT_QUESTION_NEEDS,',
         '            entity_kinds=STATEMENT_QUESTION_ENTITY_KINDS, needs=STATEMENT_QUESTION_NEEDS,\n'
         f'            additional_kinds={forms!r} if adopted_package[1] == "v109" else {{}},'),
        ('            if (len(entity) == 1',
         '            statement_kind = self._additional_kinds.get(fact_type_id)\n'
         '            if statement_kind is not None:\n'
         '                expected = {"statement"} if statement_kind == "tax.us.ssa1099-statement" else {"payer", "statement"}\n'
         '                if ({key.get("name") for key in entity} == expected\n'
         '                        and {key.get("name") for key in identity} == expected | {"tax-year"}\n'
         '                        and any(key.get("name") == "statement" and key.get("entity_kind") == statement_kind\n'
         '                                for key in entity)\n'
         '                        and any(key.get("name") == "tax-year" and key.get("kind") == "literal"\n'
         '                                for key in identity)):\n'
         '                    self._identity[fact_type_id] = [str(key.get("name")) for key in identity]\n'
         '            if (len(entity) == 1'),
        ('            label = statement_label.get("statement")\n',
         '            if fact_type in statement_questions._additional_kinds:\n'
         '                statement_label.pop("lender", None)\n'
         '            label = statement_label.get("statement")\n'),
        ('    question_refs_out: list[dict[str, Any]] | None = None,\n',
         '    question_refs_out: list[dict[str, Any]] | None = None,\n'
         '    statement_reasons_out: dict[str, list[dict[str, Any]]] | None = None,\n'),
        ('        reasons = []\n        for text in sorted(sentences):',
         '        if statement_reasons_out is not None and statement_questions is not None:\n'
         '            for fact_type in statement_questions._additional_kinds:\n'
         '                sentence = input_questions.get(fact_type)\n'
         '                if sentence in labelled:\n'
         '                    statement_reasons_out[sentence] = labelled.pop(sentence)\n'
         '        reasons = []\n        for text in sorted(sentences):'),
        ('            "question_refs_out": row_question_candidates,',
         '            "question_refs_out": row_question_candidates,\n'
         '            "statement_reasons_out": additional_statement_reasons,'),
        ('        row_question_candidates: list[dict[str, Any]] = []',
         '        row_question_candidates: list[dict[str, Any]] = []\n'
         '        additional_statement_reasons: dict[str, list[dict[str, Any]]] = {}'),
        ('        if answer_sentences:\n            # Append the unlinked sentences',
         '''        if additional_statement_reasons:
            refs = resolved.get("questionRefs", ())
            linked = {index for ref in refs for index in ref["reasonIndices"]}
            indices = {}
            expanded = []
            for index, reason in enumerate(resolved["reasons"]):
                indices[index] = len(expanded)
                labels = additional_statement_reasons.get(reason["sentence"], ())
                if not labels or index in linked or set(reason) != {"sentence"}:
                    expanded.append(reason)
                if labels and set(reason) == {"sentence"}:
                    expanded.extend(labels)
            resolved["reasons"] = expanded
            for ref in refs:
                ref["reasonIndices"] = [indices[index] for index in ref["reasonIndices"]]
        if answer_sentences:
            # Append the unlinked sentences'''),
    )
    for old, new in changes:
        if source.count(old) != 1:
            raise ValueError(f"scratch projection anchor changed: {old}")
        source = source.replace(old, new, 1)
    return source


@cache
def projector(which: str) -> Any:
    source = baseline_source() if which == "base" else scratch_source()
    module = ModuleType(f"packages.derivation._statement_labels_forms_{which}")
    module.__file__ = str(probe.REPO / PROJECTION)
    sys.modules[module.__name__] = module
    exec(compile(source, PROJECTION, "exec"), vars(module))
    module.PresentationModelError = live.PresentationModelError
    return module.build_presentation_model


def expected_by_question(
    state: Any, current: frozenset[str], dispositions: list[dict],
) -> dict[str, list[dict]]:
    """Independent expectation from the report's actual read set.

    For the named line and bare missing type, use the listed, current input
    findings. Join their structured statement keys, then order the rendered
    reasons by recorded label and full answer identity. A same-label pair
    stays a pair. The scratch projector uses the evaluator's shared helper.
    """
    facts = facts_of(state.fact_state)
    by_text = {}
    for row in dispositions:
        if row["artifact_id"] != probe.LINE_25B or row.get("code") != "DEPENDENCY_ABSENT":
            continue
        rows = defaultdict(list)
        for pin in row.get("pins", []):
            if pin["role"] == "input" and pin["id"] in current:
                finding = state.findings.get(pin["id"], {})
                fact = facts.get(finding.get("fact_id"))
                if fact is not None:
                    rows[fact.fact_type_id].append(dict(fact.keys))
        for missing in row.get("missing", []):
            if missing not in probe.questions():
                continue
            form, text = probe.questions()[missing]
            covered = {keys["statement"] for keys in rows[missing]}
            targets = defaultdict(set)
            for fact_type in probe.FORMS[form].income:
                for keys in rows[fact_type]:
                    statement = keys["statement"]
                    if statement not in covered:
                        targets[statement].add(tuple(sorted(keys.items())))
            if not targets or any(len(keys) != 1 for keys in targets.values()):
                continue
            labelled = []
            for statement, keys in targets.items():
                lifecycle = state.fact_state.entities.get(statement)
                if lifecycle is None or lifecycle.status != "current" or not lifecycle.entity.get("label"):
                    break
                label = lifecycle.entity["label"]
                identity = next(iter(keys))
                labelled.append((label, identity, {
                    "sentence": text,
                    "statementLabel": {"statement": label, "taxYear": dict(identity)["tax-year"]},
                }))
            else:
                by_text[text] = [reason for _, _, reason in sorted(labelled)]
    return by_text


def run_pair(key: str, acts: rr.Acts, core: rr.ReplayCore) -> tuple[dict, dict, dict]:
    expected = {}

    def observe(**kwargs: Any) -> dict:
        expected.update(expected_by_question(kwargs["state"], kwargs["current_finding_ids"],
                                             kwargs["dispositions"]))
        return projector("base")(**kwargs)

    run_id = "demo.statement-labels-forms." + hashlib.sha256(key.encode()).hexdigest()[:20]
    with patch.object(live, "build_presentation_model", observe):
        before = rr.saved_output(core, acts, run_id)
    with patch.object(live, "build_presentation_model", projector("scratch")):
        after = rr.saved_output(core, acts, run_id)
    return before, after, expected


def expected_model(model: dict, by_text: dict) -> tuple[dict, Counter]:
    want = deepcopy(model)
    counts = Counter()
    for section in want["sections"]:
        resolved = section.get("resolved") or {}
        if not resolved.get("reasons"):
            continue
        refs = resolved.get("questionRefs", [])
        linked = {index for ref in refs for index in ref["reasonIndices"]}
        offsets = {}
        reasons = []
        for index, reason in enumerate(resolved["reasons"]):
            offsets[index] = len(reasons)
            additions = by_text.get(reason["sentence"], [])
            if additions and set(reason) == {"sentence"}:
                if index in linked:
                    reasons.append(reason)
                reasons.extend(additions)
                counts[reason["sentence"]] += len(additions)
            else:
                reasons.append(reason)
        resolved["reasons"] = reasons
        for ref in refs:
            ref["reasonIndices"] = [offsets[index] for index in ref["reasonIndices"]]
    return want, counts


def compare(before: dict, after: dict, by_text: dict) -> tuple[list[dict], Counter]:
    if before["outcome"] != "success" or after["outcome"] != "success":
        def snapshot(saved: dict) -> dict:
            if saved["outcome"] == "success":
                return rr.snapshot(saved["model"], saved["report"])
            return rr.failure_snapshot(saved["outcome"], saved["error"], saved["message"])

        return rr.diff_snapshots(snapshot(before), snapshot(after)), Counter()
    want, counts = expected_model(before["model"], by_text)
    # Use the exact, unnormalized model and report as the primary assertion.
    # The replay snapshot also classifies any failure across the saved surface.
    if rr._same(want, after["model"]) and rr._same(before["report"], after["report"]):
        return [], counts
    left = rr.snapshot(want, before["report"])
    right = rr.snapshot(after["model"], after["report"])
    differences = rr.diff_snapshots(left, right)
    return differences or [{"kind": "raw saved model or report mismatch"}], counts


def inventory(acts: rr.Acts, saved: dict) -> dict[str, dict]:
    forms = {form: {"introduced": len(probe.statement_entities(acts, form))} for form in probe.FORMS}
    if saved["outcome"] != "success":
        return forms
    model, report = saved["model"], saved["report"]
    for fact_type, (form, text) in probe.questions().items():
        rows = Counter()
        for row in report["dispositions"]:
            for name in row.get("missing", []):
                if name.partition("|")[0] == fact_type:
                    shape = "keyed" if "|" in name else "bare"
                    rows[f"{row['artifact_id']} / {row.get('code')} / {shape}"] += 1
        seen = Counter()
        for section in model["sections"]:
            resolved = section.get("resolved") or {}
            linked = {i for ref in resolved.get("questionRefs", []) for i in ref["reasonIndices"]}
            for index, reason in enumerate(resolved.get("reasons", [])):
                if reason["sentence"] == text:
                    seen[section["id"], bool(reason.get("statementLabel")), index in linked] += 1
        forms[form].update(
            missing_rows=dict(rows), reasons=sum(seen.values()),
            lines=sorted({line for line, _, _ in seen}),
            labelled=sum(n for (_, label, _), n in seen.items() if label),
            linked=sum(n for (_, _, link), n in seen.items() if link),
            groups=sum(g["answerTarget"]["factTypeId"] == fact_type for g in model.get("questionGroups", [])),
        )
    return forms


def line_reasons(saved: dict) -> list[dict]:
    line = next(s for s in saved["model"]["sections"] if s["id"].endswith("line-25b"))
    return line["resolved"]["reasons"]


def labelled_counts(model: dict) -> Counter:
    sentences = {sentence for _, sentence in probe.questions().values()}
    return Counter(
        reason["sentence"]
        for section in model["sections"]
        for reason in (section.get("resolved") or {}).get("reasons", [])
        if "statementLabel" in reason and reason["sentence"] in sentences
    )


def render_line_25b(before: dict, after: dict, text: str, labels: tuple[str, ...]) -> None:
    """Exercise the saved-page script for this line, including existing links."""
    checker = probe.HERE.parent / "page-plain-words-evidence/check_page_dom.mjs"
    page = probe.REPO / "packages/presentation/pages/citation-walk.v1.html"
    inputs = []
    for key, saved in (("before", before), ("after", after)):
        model = saved["model"]
        line = next(s for s in model["sections"] if s["id"].endswith("line-25b"))
        groups = {r["groupId"] for r in line["resolved"].get("questionRefs", [])}
        inputs.append(json.dumps({"key": key, "model": {
            **model, "sections": [line],
            "questionGroups": [g for g in model["questionGroups"] if g["id"] in groups],
        }}))
    run = subprocess.run(
        ["node", str(checker), str(page)], check=True, capture_output=True, text=True,
        input="\n".join(inputs), timeout=30, env={**os.environ, "PPW_CHECK_DETAIL": "1"},
    )
    output = json.loads(run.stdout)
    want = {"before": [], "after": list(labels)}
    for key, result in output.items():
        found = re.findall(r"(?m)^(demo [^:\n]+):\s*\n" + re.escape(text) + "$", result["first_read_text"])
        if found != want[key] or result["section_errors"]:
            raise ValueError(f"saved line 25b rendering differs for {key}: {found}")


def controls(key: str, before: dict, after: dict, by_text: dict) -> dict[str, str]:
    if key == "demo.int.two-missing":
        original = line_reasons(after)
        text = probe.questions()[probe.FORMS["int"].withholding][1]
        indices = [i for i, item in enumerate(original) if item["sentence"] == text]
        first, second = indices
        removed = deepcopy(after)
        line_reasons(removed)[first].pop("statementLabel")
        swapped = deepcopy(after)
        reasons = line_reasons(swapped)
        reasons[first], reasons[second] = reasons[second], reasons[first]
        variants = {"missing_label": removed, "swapped_labels": swapped}
    elif key == "demo.int.unclosed":
        added = deepcopy(after)
        section = next(s for s in added["model"]["sections"] if s["id"].endswith("line-25b"))
        text = probe.questions()[probe.FORMS["int"].withholding][1]
        section["resolved"].setdefault("reasons", []).append({
            "sentence": text, "statementLabel": {"statement": "demo Alpha", "taxYear": "2025"},
        })
        variants = {"spurious_label_on_closure_block": added}
    else:
        return {}
    out = {}
    for name, mutated in variants.items():
        differences, _ = compare(before, mutated, by_text)
        if not differences:
            raise ValueError(f"negative control passed: {name}")
        out[name] = "rejected"
    return out


def run_list(key: str, acts: rr.Acts, case: probe.Case | None, core: rr.ReplayCore) -> dict:
    before, after, by_text = run_pair(key, acts, core)
    differences, counts = compare(before, after, by_text)
    if differences:
        raise ValueError(f"{key}: {len(differences)} unexpected saved-surface differences: "
                         f"{[(d.get('identity'), d.get('attribute')) for d in differences[:4]]}")
    expected_labels = None
    dom_checked = False
    gain = Counter()
    if before["outcome"] == "success":
        gain = labelled_counts(after["model"])
        gain.subtract(labelled_counts(before["model"]))
        gain = Counter({text: count for text, count in gain.items() if count})
    if gain != counts:
        raise ValueError(f"{key}: actual label count drifted from the projected expansion")
    if case:
        if before["outcome"] != "success" or after["outcome"] != "success":
            raise ValueError(f"{key}: probe did not save on both projections: {before['outcome']}/{after['outcome']}")
        fact_type = probe.FORMS[case.form].withholding
        text = probe.questions()[fact_type][1]
        actual = defaultdict(list)
        for section in after["model"]["sections"]:
            for reason in (section.get("resolved") or {}).get("reasons", []):
                if reason["sentence"] == text and "statementLabel" in reason:
                    actual[section["id"]].append(reason["statementLabel"])
        expected_labels = [{"statement": label, "taxYear": "2025"} for label in case.labels]
        if (bool(actual) != bool(expected_labels)
                or any(reasons != expected_labels for reasons in actual.values())
                or (expected_labels and not any(line.endswith("line-25b") for line in actual))):
            raise ValueError(f"{key}: ordered labels do not match the hand-written case: {dict(actual)}")
        if key.endswith(".two-missing") or key == "demo.int.three-one-zero":
            render_line_25b(before, after, text, case.labels)
            dom_checked = True
    return {
        "outcome": before["outcome"], "forms": inventory(acts, before),
        "gain": dict(gain), "expected_labels": expected_labels, "dom_checked": dom_checked,
        "controls": controls(key, before, after, by_text),
    }


def run_shard(items: list[tuple[str, rr.Acts, probe.Case | None]], core: rr.ReplayCore) -> dict:
    return {key: run_list(key, acts, case, core) for key, acts, case in items}


def summarize(results: dict) -> dict:
    form_totals = {}
    for form, spec in probe.FORMS.items():
        text = probe.questions()[spec.withholding][1]
        observations = [r["forms"][form] for r in results.values()]
        missing = Counter()
        lines = Counter()
        for row in observations:
            missing.update(row.get("missing_rows", {}))
            lines.update(row.get("lines", []))
        form_totals[form] = {
            "introduced_statement_counts": dict(sorted(Counter(r["introduced"] for r in observations).items())),
            "successful_introduced_statement_counts": dict(sorted(Counter(
                r["forms"][form]["introduced"] for r in results.values() if r["outcome"] == "success"
            ).items())),
            "lists_with_question": sum(bool(r.get("reasons")) for r in observations),
            "plain_reasons": sum(r.get("reasons", 0) - r.get("labelled", 0) for r in observations),
            "labelled_reasons_before": sum(r.get("labelled", 0) for r in observations),
            "linked_reasons_before": sum(r.get("linked", 0) for r in observations),
            "question_groups_before": sum(r.get("groups", 0) for r in observations),
            "question_lines": dict(sorted(lines.items())),
            "missing_rows": dict(sorted(missing.items())),
            "lists_gaining_labels": sum(text in r["gain"] for r in results.values()),
            "labelled_reasons_added": sum(r["gain"].get(text, 0) for r in results.values()),
        }
    return {
        "lists": len(results), "passed": len(results), "unexpected_differences": 0,
        "outcomes": dict(sorted(Counter(r["outcome"] for r in results.values()).items())),
        "lists_gaining_labels": sum(bool(r["gain"]) for r in results.values()),
        "forms": form_totals,
    }


def require_gain_totals(summaries: dict[str, dict], *, cases_only: bool = False) -> None:
    for name, expected in EXPECTED_GAIN.items():
        if cases_only and name == "recorded":
            continue
        observed = summaries[name]["lists_gaining_labels"]
        if observed != expected:
            raise ValueError(f"{name}: expected {expected} lists gaining labels, got {observed}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases-only", action="store_true")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be positive")
    recorded = [] if args.cases_only else [(key, acts, None) for key, acts in rr.recorded_lists()]
    if not args.cases_only and len(recorded) != RECORDED_TOTAL:
        raise ValueError(f"recorded input count changed: {len(recorded)}")
    cases = [(key, case.acts, case) for key, case in probe.cases().items()]
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    items = recorded + cases
    if len({key for key, _, _ in items}) != len(items):
        raise ValueError("replay lists must have distinct keys")
    shards = min(len(items), 2 * args.workers)
    core = rr.resolve_core(probe.CORE)
    results = {}
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn")) as pool:
        pending = [pool.submit(run_shard, items[i::shards], core) for i in range(shards)]
        for part in as_completed(pending):
            results.update(part.result())
            print(f"{len(results)}/{len(items)} lists", file=sys.stderr, flush=True)
    if results.keys() != {key for key, _, _ in items}:
        raise ValueError("incomplete replay")
    controls_run = {name: outcome for result in results.values() for name, outcome in result["controls"].items()}
    if controls_run != {name: "rejected" for name in (
        "missing_label", "swapped_labels", "spurious_label_on_closure_block",
    )}:
        raise ValueError(f"missing failing controls: {controls_run}")
    case_results = {key: results[key] for key, _, _ in cases}
    corpus_results = {key: results[key] for key, _, _ in recorded}
    summaries = {"recorded": summarize(corpus_results), "synthetic": summarize(case_results)}
    require_gain_totals(summaries, cases_only=args.cases_only)
    out = {
        "baseline": BASE, "core": rr.core_fingerprint(core),
        "baseline_projection_sha256": hashlib.sha256(baseline_source().encode()).hexdigest(),
        "scratch_projection_sha256": hashlib.sha256(scratch_source().encode()).hexdigest(),
        "shards": shards, "workers": args.workers,
        **summaries,
        "case_labels_on_line_25b": {key: row["expected_labels"] for key, row in case_results.items()},
        "saved_page_dom_checks": [key for key, row in case_results.items() if row["dom_checked"]],
        "controls": controls_run,
    }
    rr._check_no_local_paths(json.dumps(out), "P0 replay summary")
    args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
