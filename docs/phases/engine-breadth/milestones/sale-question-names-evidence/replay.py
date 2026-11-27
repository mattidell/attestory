"""Run the P0 exact full-surface replay, including rejected mutations."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from unittest.mock import patch

from probe import ALPHA, CORE, HERE, P, SALE_ENTITY, SALE_TYPES, ZULU, build_sales, cases, questions
import scratch
from packages.derivation import live
from tests import evidence_loader
from tools import recorded_replay as rr

LABEL = "saleLabel"
BEFORE = "v108"
EXPECTED = {
    "demo.two-fixes": {"st.adjustment": (ALPHA, ZULU)},
    "demo.three-with-peer": {"lt.adjustment": (ALPHA, ZULU)},
    "demo.mixed-terms": {"st.adjustment": (ZULU,), "lt.adjustment": (ALPHA,)},
    "demo.missing-adjustment": {"st.basis": (ZULU,)},
    "demo.missing-basis": {"st.basis": (ZULU,)},
    "demo.missing-proceeds": {"st.proceeds": (ZULU,)},
    "demo.long-missing-basis": {"lt.basis": (ZULU,)},
    "demo.long-missing-proceeds": {"lt.proceeds": (ALPHA, ZULU)},
    "demo.long-amounts-disagree": {"lt.basis": (ZULU,)},
    "demo.amounts-disagree": {"st.basis": (ALPHA, ZULU)},
    "demo.holding-period": {},
    "demo.blank-label": {"st.adjustment": ()},
    "demo.repeated-label": {"st.adjustment": ()},
    "demo.near-labels": {"st.adjustment": ()},
    "demo.id-label": {"st.adjustment": ()},
    "demo.repeated-with-peer": {"st.adjustment": ()},
    "demo.all-valid": {},
    "demo.single-sale": {"st.adjustment": ()},
    "demo.older-core": {"st.adjustment": ()},
}
EXPECTED_CHANGED = {"recorded": 0, "synthetic": 10}


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
    if before["outcome"] != "success":
        left, right = (rr.failure_snapshot(s["outcome"], s["error"], s["message"]) for s in (before, after))
        if left != right:
            raise ValueError("failure details changed")
        return 0
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


def check_dom(page, model, want):
    expected, inputs = {}, []
    for section in want["sections"]:
        prefixes = [f"{r[LABEL]}:" for r in reasons(section) if LABEL in r]
        if not prefixes:
            continue
        key = section["id"]
        rendered_section = next(s for s in model["sections"] if s["id"] == key)
        refs = {ref["groupId"] for ref in rendered_section["resolved"].get("questionRefs", ())}
        inputs.append(json.dumps({"key": key, "model": {
            **model, "sections": [rendered_section],
            "questionGroups": [group for group in model["questionGroups"] if group["id"] in refs],
        }}))
        expected[key] = prefixes
    if not expected:
        return 0
    helper = HERE.parent / "page-plain-words-evidence/check_page_dom.mjs"
    finished = subprocess.run(
        ["node", str(helper), str(page)], input="\n".join(inputs) + "\n", check=True, text=True,
        capture_output=True, timeout=30, env={**os.environ, "PPW_CHECK_DETAIL": "1"},
    )
    observed = json.loads(finished.stdout)
    if observed.keys() != expected.keys():
        raise ValueError("DOM probe did not render all named sections")
    for key, result in observed.items():
        lines = result["first_read_text"].splitlines()
        prefixes = [line.rstrip() for line in lines if line.startswith("demo ") and line.rstrip().endswith(":")]
        if prefixes != expected[key] or result["section_errors"]:
            raise ValueError(f"wrong rendered sale names on {key}: {prefixes!r}")
    return len(observed)


def historical_sales(acts):
    observed = set()
    for act in acts:
        payload = act["payload"]
        finding = (payload.get("member") or {}).get("finding") or payload.get("finding") or {}
        kind, _, identity = finding.get("fact_id", "").partition("|")
        if kind in SALE_TYPES:
            observed.add(identity)
    return len(observed)


def current_sales(kwargs):
    ids = set()
    labels = []
    state = kwargs["state"]
    for fid in kwargs["current_finding_ids"]:
        kind, _, keys = state.findings.get(fid, {}).get("fact_id", "").partition("|")
        if kind not in SALE_TYPES:
            continue
        entity_id = dict(pair.split("=", 1) for pair in keys.split(","))["sale"]
        if entity_id in ids:
            continue
        ids.add(entity_id)
        entity = state.fact_state.entities.get(entity_id)
        if entity and entity.status == "current" and entity.entity.get("kind") == SALE_ENTITY:
            label = entity.entity.get("label")
            labels.append(label if isinstance(label, str) and label.strip() and label != entity_id else "")
        else:
            labels.append("")
    nonempty = [" ".join(label.split()).casefold() for label in labels if label]
    return len(ids), "" in labels, len(nonempty) != len(set(nonempty))


def run_list(key, acts, is_synthetic, page):
    base, candidate = scratch.projectors()
    texts = {}
    counts = ()
    core = BEFORE if key == "demo.older-core" else CORE

    def inventory(**kwargs):
        nonlocal counts
        counts = current_sales(kwargs)
        for fact_type, text in questions(kwargs["resolved_members"]).items():
            source, _, kind = fact_type.rpartition(".")
            texts[f"{SALE_TYPES[source]}.{kind}"] = text
        return base.build_presentation_model(**kwargs)

    digest = hashlib.sha256(key.encode()).hexdigest()[:20]
    run_id = "demo.sale-names.replay." + digest
    with patch.object(live, "build_presentation_model", inventory):
        before = rr.saved_output(core, acts, run_id)
    with patch.object(live, "build_presentation_model", candidate.build_presentation_model):
        after = rr.saved_output(core, acts, run_id)
    if is_synthetic and before["outcome"] != "success":
        raise ValueError(f"{key}: baseline did not save: {before['message']}")
    want, seen = None, {}
    try:
        if before["outcome"] == "success":
            want, seen = expected_model(before["model"], texts, EXPECTED[key] if is_synthetic else None)
        names = compare(before, after, want)
        rejected = controls(key, before, after, want)
        rendered = check_dom(page, after["model"], want) if is_synthetic else 0
    except ValueError as exc:
        error = after["message"] if before["outcome"] == "success" and after["outcome"] != "success" else ""
        actual = names_at_positions(after["model"]) if after["outcome"] == "success" else {}
        raise ValueError(f"{key}: {exc} {error} ({len(actual)} actual names)") from exc
    return {
        "outcome": before["outcome"], "names": names, "controls": rejected, "dom_sections": rendered,
        "questions": dict(seen), "historical_sales": historical_sales(acts), "current_sales": counts,
    }


def run_shard(items, page):
    return {key: run_list(key, acts, synthetic, page) for key, acts, synthetic in items}


def summarize(rows, expected):
    saves = [r for r in rows if r["outcome"] == "success"]
    return {
        "lists": len(rows), "outcomes": dict(Counter(r["outcome"] for r in rows)),
        "changed_lists": require_changed(rows, expected), "names_added": sum(r["names"] for r in rows),
        "recorded_sale_counts": dict(Counter(r["historical_sales"] for r in rows)),
        "saved_current_sale_counts": dict(Counter(r["current_sales"][0] for r in saves)),
        "saved_with_missing_labels": sum(r["current_sales"][1] for r in saves),
        "saved_with_repeated_labels": sum(r["current_sales"][2] for r in saves),
        "lists_by_question": dict(Counter(q for r in saves for q in r["questions"])),
        "reason_counts_by_question": dict(sum((Counter(r["questions"]) for r in saves), Counter())),
        "named_dom_sections": sum(r["dom_sections"] for r in rows),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--cases-only", action="store_true")
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("workers must be positive")
    projection, page = scratch.sources()
    known_cases = cases()
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
    with TemporaryDirectory() as directory:
        page_path = Path(directory) / "citation-walk.v1.html"
        page_path.write_text(scratch.scratch_page(page), encoding="utf-8")
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(run_shard, shard, page_path) for shard in shards]
            for future in as_completed(futures):
                try:
                    results.update(future.result())
                except BaseException:
                    pool.terminate_workers()
                    raise
                print(f"{len(results)}/{len(recorded) + len(synthetic)}", flush=True)
    if results.keys() != {key for key, _, _ in synthetic + recorded}:
        raise ValueError("incomplete replay")
    summary = {
        "baseline": scratch.BASE, "core": CORE, "registry": "v107", "release": "v107",
        "workers": args.workers, "shards": len(shards),
        "recorded": summarize([results[key] for key, _, _ in recorded], EXPECTED_CHANGED["recorded"]),
        "synthetic": summarize([results[key] for key, _, _ in synthetic], EXPECTED_CHANGED["synthetic"]),
        "synthetic_cases": {key: results[key] for key, _, _ in synthetic},
        "controls_rejected": sorted(name for result in results.values() for name in result["controls"]),
        "unexpected_differences": 0,
        "scratch_projection_sha256": hashlib.sha256(scratch.scratch_projection(projection).encode()).hexdigest(),
        "scratch_page_sha256": hashlib.sha256(scratch.scratch_page(page).encode()).hexdigest(),
    }
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    rr._check_no_local_paths(encoded, "P0 sale-name replay summary")
    args.out.write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
