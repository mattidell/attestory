"""Replay the landed sale-name projector and page against its build parent."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from functools import cache
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from unittest.mock import patch

from probe import ALPHA, CORE, HERE, SALE_TYPES, ZULU, Sale, build_sales, cases, questions
from packages.derivation import live
from tests import evidence_loader
from tools import recorded_replay as rr
from tools.sale_page_observation import _expected_blocked_reason_texts

LABEL = "saleLabel"
BUILD_SUBJECT = "build(sale-question-names)"
PROJECTION = "packages/derivation/presentation_projection.py"
PAGE = HERE.parents[4] / "packages/presentation/pages/citation-walk.v1.html"
BEFORE = "v108"
EXPECTED = {
    "demo.two-fixes": {"st.adjustment": (ALPHA, ZULU)},
    "demo.three-with-peer": {"lt.adjustment": (ALPHA, ZULU)},
    "demo.mixed-terms": {"st.adjustment": (ZULU,), "lt.adjustment": (ALPHA,)},
    "demo.missing-adjustment": {"st.basis": ()},
    "demo.missing-basis": {"st.basis": (ZULU,)},
    "demo.missing-proceeds": {"st.proceeds": (ZULU,)},
    "demo.long-missing-basis": {"lt.basis": (ZULU,)},
    "demo.long-missing-proceeds": {"lt.proceeds": (ALPHA, ZULU)},
    "demo.long-amounts-disagree": {"lt.basis": ()},
    "demo.amounts-disagree": {"st.basis": ()},
    "demo.holding-period": {},
    "demo.blank-label": {"st.adjustment": ()},
    "demo.repeated-label": {"st.adjustment": ()},
    "demo.near-labels": {"st.adjustment": ()},
    "demo.id-label": {"st.adjustment": ()},
    "demo.repeated-with-peer": {"st.adjustment": ()},
    "demo.all-valid": {},
    "demo.single-sale": {"st.adjustment": ()},
    "demo.older-core": {"st.adjustment": ()},
    "demo.nfc-collision": {"st.basis": ()},
    "demo.format-collision": {"st.basis": ()},
    "demo.combining-only": {"st.adjustment": ()},
}
UNICODE_CASES = {
    "demo.nfc-collision": (Sale("demo Café", "st", "missing-basis"), Sale("demo Cafe\u0301", "lt")),
    "demo.format-collision": (Sale("demo Café", "st", "missing-basis"), Sale("demo Ca\u200bfé", "lt")),
    "demo.combining-only": (Sale("\u034f", condition="gain"), Sale(ALPHA, condition="exceeds")),
}
EXPECTED_CHANGED = {"recorded": 0, "synthetic": 7}
# The landed baseline census was recorded by P0 and the Track 1 build replay.
EXPECTED_OUTCOMES = {"recorded": {"success": 691, "error": 84}, "synthetic": {"success": 22}}
# The 84 case keys agree in member-reads-once timing-before and line16-names
# Track 1 evidence. Hash the sorted keys so a swap cannot preserve the census.
RECORDED_ERROR_KEYS_SHA256 = "2767993ef1bce2c29eda8c07df82a0533d7180042ba34c387ed9636bf59d487b"


def git(*args):
    return subprocess.check_output(
        ["git", *args], cwd=HERE.parents[4], timeout=30, text=True,
    ).strip()


@cache
def baseline():
    builds = [
        commit for line in git("log", "--format=%H%x09%s", "HEAD").splitlines()
        for commit, subject in [line.split("\t", 1)]
        if subject.startswith(BUILD_SUBJECT)
    ]
    if len(builds) != 1:
        raise ValueError("expected one sale-question-names build in HEAD history")
    return git("rev-parse", builds[0] + "^")


@cache
def baseline_projector():
    module = ModuleType("packages.derivation.sale_names_replay_baseline")
    module.__package__ = "packages.derivation"
    sys.modules[module.__name__] = module
    source = git("show", f"{baseline()}:{PROJECTION}")
    exec(compile(source, PROJECTION, "exec"), module.__dict__)
    return module.build_presentation_model


def reasons(section):
    return section["resolved"].get("reasons", ())


def names_at_positions(model):
    return {
        (section["id"], index): (reason["sentence"], reason[LABEL])
        for section in model["sections"] for index, reason in enumerate(reasons(section))
        if LABEL in reason
    }


def expected_model(model, texts, expectation):
    """Rebuild the precise intended model from baseline and fixed case names."""
    want = deepcopy(model)
    by_sentence = {sentence: key for key, sentence in texts.items()}
    seen = Counter()
    for section in want["sections"]:
        resolved = section["resolved"]
        if "reasons" not in resolved:
            continue
        refs = resolved.get("questionRefs", ())
        linked = {index for ref in refs for index in ref["reasonIndices"]}
        positions, updated = {}, []
        for index, reason in enumerate(resolved["reasons"]):
            positions[index] = len(updated)
            sentence = reason["sentence"]
            key = by_sentence.get(sentence)
            if key is not None:
                seen[key] += 1
            added = (expectation or {}).get(key, ())
            if not added or index in linked:
                updated.append(reason)
            if added:
                if set(reason) != {"sentence"}:
                    raise ValueError("expected plain baseline reason")
                updated.extend({"sentence": sentence, LABEL: name} for name in added)
        resolved["reasons"] = updated
        for ref in refs:
            ref["reasonIndices"] = [positions[index] for index in ref["reasonIndices"]]
    if expectation is not None and dict(seen) != dict.fromkeys(expectation, 32):
        raise ValueError(f"unexpected synthetic question inventory: {dict(seen)}")
    return want, seen


def compare(before, after, want):
    if before["outcome"] != after["outcome"]:
        raise ValueError("outcome changed")
    if before["outcome"] not in {"success", "error", "refused"}:
        raise ValueError("unknown outcome")
    if before["outcome"] != "success":
        left, right = (rr.failure_snapshot(s["outcome"], s["error"], s["message"]) for s in (before, after))
        if left != right:
            raise ValueError("failure details changed")
        return 0
    if want is None:
        raise ValueError("successful baseline lacks an expected model")
    expected_names = names_at_positions(want)
    if names_at_positions(after["model"]) != expected_names:
        raise ValueError("sale names or their reason positions changed")
    if (not rr._same(want, after["model"])
            or not rr._same(before["report"], after["report"])):
        raise ValueError("saved model or report changed beyond the expected names")
    return len(expected_names)


def require_changed(rows, expected):
    count = sum(row["names"] > 0 for row in rows)
    if count != expected:
        raise ValueError("changed-list total differs")
    return count


def reject(name, action, message):
    try:
        action()
    except ValueError as exc:
        if str(exc) != message:
            raise
        return name
    raise ValueError(f"control accepted: {name}")


def controls(key, before, after, want):
    out = []

    def attempt(name, mutation, message):
        broken = deepcopy(after)
        mutation(broken)
        out.append(reject(name, lambda: compare(before, broken, want), message))

    names_error = "sale names or their reason positions changed"
    surface_error = "saved model or report changed beyond the expected names"
    if key in {"demo.two-fixes", "demo.missing-basis", "demo.repeated-label"}:
        named_section = next(s for s in after["model"]["sections"] if reasons(s) and (
            any(LABEL in r for r in reasons(s)) if key != "demo.repeated-label"
            else any("wash-sale loss disallowed do you enter" in r["sentence"] for r in reasons(s))
        ))
        idx = after["model"]["sections"].index(named_section)

        def at(saved):
            return saved["model"]["sections"][idx]["resolved"]

        names = [i for i, reason in enumerate(reasons(named_section)) if LABEL in reason]
        if key == "demo.two-fixes":
            first, second = names
            attempt("removed_name", lambda s: at(s)["reasons"][first].pop(LABEL), names_error)
            attempt("removed_named_reason", lambda s: at(s)["reasons"].pop(first), names_error)

            def swap(saved):
                left, right = (at(saved)["reasons"][i] for i in names)
                left[LABEL], right[LABEL] = right[LABEL], left[LABEL]

            attempt("swapped_names", swap, names_error)
            attempt("moved_question_ref", lambda s: at(s)["questionRefs"][0]["reasonIndices"].__setitem__(0, second),
                    surface_error)
        elif key == "demo.missing-basis":
            attempt("wrong_unlinked_name", lambda s: at(s)["reasons"][names[0]].__setitem__(LABEL, ALPHA),
                    names_error)
            attempt("changed_block_code_beside_name", lambda s: at(s)["activeCodes"].append("DEPENDENCY_INVALID"),
                    surface_error)
            attempt("changed_report_beside_name", lambda s: s["report"].__setitem__("demo-control", True),
                    surface_error)
        else:
            i = next(i for i, reason in enumerate(reasons(named_section))
                     if "wash-sale loss disallowed do you enter" in reason["sentence"])
            attempt("added_name_to_repeated_sale", lambda s: at(s)["reasons"][i].__setitem__(LABEL, ZULU),
                    names_error)
            attempt("changed_unnamed_model", lambda s: s["model"].__setitem__("demo-control", True), surface_error)
            attempt("changed_unnamed_report", lambda s: s["report"].__setitem__("demo-control", True), surface_error)
    if key == "demo.all-valid":
        attempt("changed_outcome", lambda s: s.__setitem__("outcome", "error"), "outcome changed")
        out.append(reject("wrong_changed_list_total", lambda: require_changed([{"names": 1}], 0),
                          "changed-list total differs"))
    if key == "v81/v80/v80_mixed_abcf":
        if before["outcome"] != "error":
            raise ValueError("recorded failure control requires an error")
        attempt("changed_failure_class", lambda s: s.__setitem__("error", "DemoChangedError"),
                "failure details changed")
        attempt("changed_failure_message", lambda s: s.__setitem__("message", "demo changed error"),
                "failure details changed")
    return out


def observe_dom(page, model):
    helper = HERE.parent / "page-plain-words-evidence/check_page_dom.mjs"
    request = json.dumps({"key": "saved-page", "model": model}) + "\n"
    finished = subprocess.run(
        ["node", str(helper), str(page)], input=request, check=True, text=True,
        capture_output=True, timeout=30, env={**os.environ, "PPW_CHECK_BLOCKED_REASONS": "1"},
    )
    return json.loads(finished.stdout)["saved-page"]


def expected_dom(model):
    expected = {}
    for section in model["sections"]:
        texts = _expected_blocked_reason_texts(model, section["resolved"])
        pairs = [
            {"text": text, "sale_prefixes": [f"{r[LABEL]}: "] if LABEL in r else []}
            for text, r in zip(texts, reasons(section), strict=True)
        ]
        expected[section["id"]] = {
            "reasons": pairs,
            "sale_prefixes": [prefix for pair in pairs for prefix in pair["sale_prefixes"]],
            "errors": 0,
        }
    return expected


def check_dom(observed, want):
    if observed.keys() != want.keys():
        raise ValueError("DOM probe did not render every section")
    for key, expected in want.items():
        if observed[key] != expected:
            raise ValueError(f"blocked reason DOM differs on {key}")
    return len(want), sum(bool(section["sale_prefixes"]) for section in want.values())


def dom_controls(key, page, model, want):
    def mutated(name, mutate):
        broken = deepcopy(model)
        mutate(broken)
        return reject(name, lambda: check_dom(observe_dom(page, broken), want), f"blocked reason DOM differs on {section_id}")

    if key == "demo.single-sale":
        expected_section = next(s for s in model["sections"] if s["field"]["id"].endswith(".schedule-d.line-3"))
        section_id = expected_section["id"]

        def generic_reason(broken):
            section = next(s for s in broken["sections"] if s["id"] == section_id)
            resolved = section["resolved"]
            linked = {i for ref in resolved.get("questionRefs", ()) for i in ref["reasonIndices"]}
            return next(reason for i, reason in enumerate(resolved["reasons"]) if i not in linked)

        checked = [mutated("dom_spurious_single_sale_prefix", lambda broken: generic_reason(broken).update({LABEL: ZULU}))]
        for label in ("\ufeff", "\u2003\u200b", "\u034f", "\u0301", "\u115f"):
            blank = deepcopy(model)
            generic_reason(blank)[LABEL] = label
            check_dom(observe_dom(page, blank), want)
        return checked
    if key == "demo.missing-basis":
        section_id = next(s["id"] for s in model["sections"] if any(LABEL in r for r in reasons(s)))

        def wrong_question(broken):
            section = next(s for s in broken["sections"] if s["id"] == section_id)
            reason = next(r for r in reasons(section) if LABEL in r)
            reason["sentence"] = "Demo unrelated question?"

        return [mutated("dom_prefix_beside_wrong_question", wrong_question)]
    return []


def run_list(key, acts, is_synthetic, page):
    base = baseline_projector()
    texts = {}
    core = BEFORE if key == "demo.older-core" else CORE

    def inventory(**kwargs):
        for fact_type, text in questions(kwargs["resolved_members"]).items():
            source, _, kind = fact_type.rpartition(".")
            texts[f"{SALE_TYPES[source]}.{kind}"] = text
        return base(**kwargs)

    digest = hashlib.sha256(key.encode()).hexdigest()[:20]
    run_id = "demo.sale-names.replay." + digest
    with patch.object(live, "build_presentation_model", inventory):
        before = rr.saved_output(core, acts, run_id)
    after = rr.saved_output(core, acts, run_id)
    if is_synthetic and before["outcome"] != "success":
        raise ValueError(f"{key}: baseline did not save: {before['message']}")
    want = None
    try:
        if before["outcome"] == "success":
            want, _ = expected_model(before["model"], texts, EXPECTED[key] if is_synthetic else None)
        names = compare(before, after, want)
        rejected = controls(key, before, after, want)
        rendered = named = 0
        if want is not None:
            expected = expected_dom(want)
            rendered, named = check_dom(observe_dom(page, after["model"]), expected)
            rejected.extend(dom_controls(key, page, after["model"], expected))
    except ValueError as exc:
        error = after["message"] if before["outcome"] == "success" and after["outcome"] != "success" else ""
        actual = names_at_positions(after["model"]) if after["outcome"] == "success" else {}
        raise ValueError(f"{key}: {exc} {error} ({len(actual)} actual names)") from exc
    return {
        "key": key, "baseline_outcome": before["outcome"], "candidate_outcome": after["outcome"],
        "names": names, "controls": rejected, "dom_sections": rendered, "named_dom_sections": named,
    }


def run_shard(items, page):
    return {key: run_list(key, acts, synthetic, page) for key, acts, synthetic in items}


def error_keys_sha256(rows, outcome_field):
    keys = sorted(row["key"] for row in rows if row[outcome_field] == "error")
    return hashlib.sha256(json.dumps(keys, separators=(",", ":")).encode()).hexdigest()


def require_outcomes(rows, expected, expected_error_keys=None):
    baseline = Counter(row["baseline_outcome"] for row in rows)
    candidate = Counter(row["candidate_outcome"] for row in rows)
    if baseline != expected or candidate != baseline:
        raise ValueError(f"outcome census differs from the landed baseline: {dict(sorted(baseline.items()))}, {dict(sorted(candidate.items()))}")
    if expected_error_keys is not None and any(
        error_keys_sha256(rows, field) != expected_error_keys
        for field in ("baseline_outcome", "candidate_outcome")
    ):
        raise ValueError("error cases differ from the landed baseline")
    return dict(baseline), dict(candidate)


def census_controls(rows, expected, expected_error_keys, *, compare_saved=compare):
    broken = deepcopy(rows)
    previously_saved = next(row for row in broken if row["baseline_outcome"] == "success")
    # compare() alone accepts identical errors on both sides.
    setup_error = {"outcome": "error", "error": "DemoSetupError", "message": "demo setup failed"}
    previously_saved["names"] = compare_saved(setup_error, setup_error, None)
    previously_saved.update(baseline_outcome="error", candidate_outcome="error")
    wrong = dict(expected)
    wrong["success"] -= 1
    wrong["error"] += 1
    quoted = dict(sorted(wrong.items()))
    rejected = [reject(
        "same_setup_error_replaces_recorded_save", lambda: require_outcomes(broken, expected, expected_error_keys),
        f"outcome census differs from the landed baseline: {quoted}, {quoted}",
    )]
    previously_errored = next(row for row in broken if row is not previously_saved and row["baseline_outcome"] == "error")
    previously_errored.update(baseline_outcome="success", candidate_outcome="success")
    rejected.append(reject(
        "recorded_save_and_error_swap_with_same_census", lambda: require_outcomes(broken, expected, expected_error_keys),
        "error cases differ from the landed baseline",
    ))
    return rejected


def summarize(rows, expected_changed, expected_outcomes, expected_error_keys=None):
    baseline, candidate = require_outcomes(rows, expected_outcomes, expected_error_keys)
    return {
        "lists": len(rows), "baseline_outcomes": baseline, "outcomes": candidate,
        "changed_lists": require_changed(rows, expected_changed), "names_added": sum(r["names"] for r in rows),
        "dom_sections": sum(r["dom_sections"] for r in rows),
        "named_dom_sections": sum(r["named_dom_sections"] for r in rows),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--cases-only", action="store_true")
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("workers must be positive")
    baseline()
    known_cases = cases() | UNICODE_CASES
    known_cases["demo.older-core"] = known_cases["demo.two-fixes"]
    if EXPECTED.keys() != known_cases.keys():
        raise ValueError("synthetic inventory and expectations disagree")
    synthetic = [(key, build_sales(data), True) for key, data in known_cases.items()]
    recorded = [] if args.cases_only else [(key, acts, False) for key, acts in rr.recorded_lists()]
    if not args.cases_only and len(recorded) != 775:
        raise ValueError("recorded inventory count changed")
    if owner := evidence_loader.current_owner():
        evidence_loader.release(owner)
    batches = args.workers * 3
    shards = [[test] for test in synthetic] + [recorded[i::batches] for i in range(min(batches, len(recorded)))]
    results = {}
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_shard, shard, PAGE) for shard in shards]
        for future in as_completed(futures, timeout=1800):
            try:
                results.update(future.result())
            except BaseException:
                if hasattr(pool, "terminate_workers"):
                    pool.terminate_workers()
                else:
                    for pending in futures:
                        pending.cancel()
                raise
            print(f"{len(results)}/{len(recorded) + len(synthetic)}", flush=True)
    if results.keys() != {key for key, _, _ in synthetic + recorded}:
        raise ValueError("incomplete replay")
    recorded_rows = [results[key] for key, _, _ in recorded]
    synthetic_rows = [results[key] for key, _, _ in synthetic]
    recorded_census = {} if args.cases_only else EXPECTED_OUTCOMES["recorded"]
    recorded_errors = None if args.cases_only else RECORDED_ERROR_KEYS_SHA256
    recorded_summary = summarize(recorded_rows, EXPECTED_CHANGED["recorded"], recorded_census, recorded_errors)
    if recorded_errors is not None:
        recorded_summary["error_keys_sha256"] = error_keys_sha256(recorded_rows, "baseline_outcome")
    synthetic_summary = summarize(synthetic_rows, EXPECTED_CHANGED["synthetic"], EXPECTED_OUTCOMES["synthetic"])
    rejected = [name for result in results.values() for name in result["controls"]]
    if recorded_rows:
        rejected.extend(census_controls(recorded_rows, recorded_census, recorded_errors))
    summary = {
        "baseline": "parent of the build(sale-question-names) commit in HEAD history", "core": CORE, "registry": "v107", "release": "v107",
        "workers": args.workers, "shards": len(shards),
        "recorded": recorded_summary,
        "synthetic": synthetic_summary,
        "controls_rejected": sorted(rejected),
        "unexpected_differences": 0,
    }
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    rr._check_no_local_paths(encoded, "Track 1 sale-name replay summary")
    args.out.write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
