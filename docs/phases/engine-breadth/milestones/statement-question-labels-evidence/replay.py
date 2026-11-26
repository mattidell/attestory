"""Full-surface replay of the scratch design (P0 evidence for statement-question-labels).

Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/statement-question-labels-evidence/replay.py \
        --set recorded --shard 0/2 --out temp/statement-question-labels/replay-0.json

Each list runs twice in one worker process on published core v106 through the
real ``live_coordinate_run`` (``recorded_replay.snapshot_run``): first with the
pre-build projection, then with the P0 design applied to it. The two saved outputs
are compared by ``recorded_replay.classify_full`` (strict; any difference no
expectation names fails), with the expectations in ``replay_expectations.json``.

``--set recorded`` is the deduplicated recorded corpus (``recorded_lists``);
``--set cases`` is the relabelled synthetic cases of ``probe.CASES`` and
``probe.DROP_CASES``. ``--merge`` folds shard outputs into one summary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
for path in (str(REPO), str(HERE)):
    if path not in sys.path:
        sys.path.insert(0, path)

from tools import recorded_replay as rr  # noqa: E402
from packages.derivation import evaluator, live  # noqa: E402
from replay_baseline import baseline  # noqa: E402

EXPECT = HERE / "replay_expectations.json"


def save_pre_build(core: Any, acts: rr.Acts, run_id: str, *, scratch: bool = False) -> dict[str, Any]:
    from design import project_with_design

    projection = baseline("presentation_projection")
    def scratch_build(**kwargs: Any) -> dict[str, Any]:
        return project_with_design(projection, **kwargs)

    build = scratch_build if scratch else projection.build_presentation_model
    with (
        patch.object(live, "build_presentation_model", build),
        patch.object(evaluator, "_require_paired", baseline("evaluator")._require_paired),
    ):
        return rr.saved_output(core, acts, run_id)


class DesignCompare:
    """Picklable per-list callable: published projection, then the scratch design."""

    def __init__(self, expectations: list[dict[str, Any]], max_unexpected: int = 20) -> None:
        self.expectations = expectations
        self.max_unexpected = max_unexpected

    def __call__(self, key: str, acts: list[dict[str, Any]], cores: Any) -> dict[str, Any]:
        core = cores[0] if isinstance(cores, (list, tuple)) else cores
        run_id = "demo.sql." + hashlib.sha256(key.encode()).hexdigest()[:20]
        saved_a = save_pre_build(core, acts, run_id)
        saved_b = save_pre_build(core, acts, run_id, scratch=True)
        snap_a, snap_b = (rr.snapshot(saved["model"], saved["report"]) if saved["outcome"] == "success"
                          else rr.failure_snapshot(saved["outcome"], saved["error"], saved["message"])
                          for saved in (saved_a, saved_b))
        verdict = rr.classify_full(snap_a, snap_b, self.expectations)
        verdict["semantic"] = semantic_check(saved_a, saved_b)
        if not verdict["semantic"]["ok"] and verdict["class"] != "unexpected":
            verdict["class"] = "unexpected"
        unexpected = verdict.pop("unexpected")
        verdict["unexpected_total"] = len(unexpected)
        verdict["unexpected"] = unexpected[: self.max_unexpected]
        verdict["outcomes"] = [snap_a["outcome"], snap_b["outcome"]]
        verdict["records"] = [len(snap_a["records"]), len(snap_b["records"])]
        verdict["sha256"] = [rr.snapshot_sha256(snap_a), rr.snapshot_sha256(snap_b)]
        return verdict


def _statement_questions() -> set[str]:
    content = REPO / "packages/content/tax/2025"
    return {json.loads((content / name).read_text(encoding="utf-8"))["question"] for name in (
        "input-question.f1099b-box4.v2.json",
        "input-question.f1099b-statement-box4-withholding-reported.json",
        "input-question.f1099b-statement-box7-loss-not-allowed.json")}


def semantic_check(saved_a: dict[str, Any], saved_b: dict[str, Any]) -> dict[str, Any]:
    """What the design may change, checked on the saved models themselves.

    Holds when, on every page line: the design's reasons, with each run of
    per-statement question reasons that carry ``statementLabel`` folded back
    into the one unlabelled reason, equal the published reasons in order;
    every question reference names the same sentences; and the report rows are
    equal. Counts the lines and statements that gained a label.
    """
    out: dict[str, Any] = {"ok": True, "lines_labelled": 0, "labels": 0, "problems": []}
    if saved_a["outcome"] != "success" or saved_b["outcome"] != "success":
        out["ok"] = saved_a == saved_b
        if not out["ok"]:
            out["problems"].append("outcome differs")
        return out
    if saved_a["report"].get("dispositions") != saved_b["report"].get("dispositions"):
        out["ok"] = False
        out["problems"].append("report dispositions differ")
    questions = _statement_questions()
    sections_a = {s["id"]: s for s in saved_a["model"].get("sections") or []}
    sections_b = {s["id"]: s for s in saved_b["model"].get("sections") or []}
    if sections_a.keys() != sections_b.keys():
        out["ok"] = False
        out["problems"].append("section ids differ")
        return out
    for section_id, section_a in sections_a.items():
        res_a = section_a.get("resolved") or {}
        res_b = sections_b[section_id].get("resolved") or {}
        reasons_a = res_a.get("reasons") or []
        reasons_b = res_b.get("reasons") or []
        folded: list[dict[str, Any]] = []
        labelled = 0
        for reason in reasons_b:
            if reason.get("sentence") in questions and set(reason) == {"sentence", "statementLabel"}:
                labelled += 1
                plain = {"sentence": reason["sentence"]}
                if folded and folded[-1] == plain:
                    continue
                folded.append(plain)
            else:
                folded.append(reason)
        if folded != reasons_a:
            out["ok"] = False
            out["problems"].append(f"{section_id}: reasons do not fold back")
        if labelled:
            out["lines_labelled"] += 1
            out["labels"] += labelled
        def named(reasons: list[dict[str, Any]], indices: list[int]) -> list[str]:
            return sorted(reasons[i]["sentence"] if 0 <= i < len(reasons) else "(no reason)" for i in indices)

        refs_a = {ref["groupId"]: named(reasons_a, ref["reasonIndices"]) for ref in res_a.get("questionRefs") or []}
        refs_b = {ref["groupId"]: named(reasons_b, ref["reasonIndices"]) for ref in res_b.get("questionRefs") or []}
        if refs_a != refs_b:
            out["ok"] = False
            out["problems"].append(f"{section_id}: question references moved")
        rest_a = {k: v for k, v in res_a.items() if k not in {"reasons", "questionRefs"}}
        rest_b = {k: v for k, v in res_b.items() if k not in {"reasons", "questionRefs"}}
        if rest_a != rest_b or {k: v for k, v in section_a.items() if k != "resolved"} != {
                k: v for k, v in sections_b[section_id].items() if k != "resolved"}:
            out["ok"] = False
            out["problems"].append(f"{section_id}: other content differs")
    model_a = {k: v for k, v in saved_a["model"].items() if k != "sections"}
    model_b = {k: v for k, v in saved_b["model"].items() if k != "sections"}
    if model_a != model_b:
        out["ok"] = False
        out["problems"].append("model outside sections differs")
    out["problems"] = out["problems"][:10]
    return out


def semantic_controls(saved_a: dict[str, Any], saved_b: dict[str, Any]) -> dict[str, bool]:
    """Each mutation of a labelled design output that ``semantic_check`` must reject (True = rejected)."""
    import copy

    def first_labelled(model: dict[str, Any]) -> tuple[dict[str, Any], int] | None:
        # Prefer the line with the most reasons, so the other mutations have something to act on.
        ranked = sorted(model.get("sections") or [],
                        key=lambda section: -len((section.get("resolved") or {}).get("reasons") or []))
        for section in ranked:
            for index, reason in enumerate((section.get("resolved") or {}).get("reasons") or []):
                if "statementLabel" in reason and reason.get("sentence") in _statement_questions():
                    return section, index
        return None

    out: dict[str, bool] = {"unchanged_accepted": semantic_check(saved_a, saved_b)["ok"]}
    for name in ("drop_reason", "label_other_reason", "change_sentence", "move_reference"):
        mutated = copy.deepcopy(saved_b)
        found = first_labelled(mutated["model"])
        if found is None:
            continue
        section, index = found
        reasons = section["resolved"]["reasons"]
        if name == "drop_reason":
            # The only labelled reason of its sentence: dropping it drops the question.
            del reasons[index]
            if not reasons:
                del section["resolved"]["reasons"]
        elif name == "label_other_reason":
            other = next((r for r in reasons if r.get("sentence") not in _statement_questions()), None)
            if other is None:
                continue
            other["statementLabel"] = {"statement": "demo statement 9"}
        elif name == "change_sentence":
            reasons[index]["sentence"] = reasons[index]["sentence"] + " (demo)"
        elif name == "move_reference":
            refs = section["resolved"].get("questionRefs") or []
            if not refs:
                continue
            refs[0]["reasonIndices"] = [index]
        out[name + "_rejected"] = not semantic_check(saved_a, mutated)["ok"]
    return out


def chosen_lists(which: str) -> list[tuple[str, Any]]:
    if which == "recorded":
        return rr.recorded_lists()
    import probe

    return probe.case_lists()


def summarize(results: dict[str, Any], expectations: list[dict[str, Any]]) -> dict[str, Any]:
    classes = Counter(row["class"] for row in results.values())
    used = {index for row in results.values() for index in row.get("used", [])}
    by_attribute: dict[str, dict[str, Any]] = {}
    for key, row in results.items():
        for item in row["unexpected"]:
            slot = by_attribute.setdefault(
                f"{item['kind']}|{item['change']}|{re.sub(r'[0-9]+', 'N', item['attribute'])}", {"lists": set(), "samples": []})
            slot["lists"].add(key)
            if len(slot["samples"]) < 3:
                slot["samples"].append({"list": key, **item})
    return {
        "format": "statement-question-labels-replay.v1",
        "core": rr.core_fingerprint(rr.resolve_core("v106")),
        "lists": len(results),
        "classes": dict(sorted(classes.items())),
        "passing": sum(1 for row in results.values() if row["class"] != "unexpected"),
        "failing": sum(1 for row in results.values() if row["class"] == "unexpected"),
        "unexpected_differences": sum(row["unexpected_total"] for row in results.values()),
        "unexpected_by_kind_attribute": {
            name: {"lists": len(slot["lists"]), "samples": slot["samples"]} for name, slot in sorted(by_attribute.items())},
        "expectations_declared": len(expectations),
        "expectations_used": len(used),
        "unused_expectations": [spec.get("note") for index, spec in enumerate(expectations) if index not in used],
        "expected_by_note": dict(sorted(sum((Counter(row["expected_by_note"]) for row in results.values()), Counter()).items())),
        "outcomes": dict(sorted(Counter("/".join(row["outcomes"]) for row in results.values()).items())),
        "semantic_failures": sorted(key for key, row in results.items() if not row["semantic"]["ok"]),
        "lines_labelled": sum(row["semantic"]["lines_labelled"] for row in results.values()),
        "labelled_reasons": sum(row["semantic"]["labels"] for row in results.values()),
        "changed_lists": sorted(key for key, row in results.items() if row["class"] != "identical"),
        "failing_lists": {key: row["unexpected_total"] for key, row in sorted(results.items()) if row["class"] == "unexpected"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", choices=("recorded", "cases"), default="recorded")
    parser.add_argument("--shard", default="0/1")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--part", type=Path)
    parser.add_argument("--merge", nargs="*", type=Path)
    parser.add_argument("--controls", action="store_true", help="run the semantic-check mutation controls")
    args = parser.parse_args()
    if args.controls:
        import probe

        cases = dict(probe.case_lists())
        recorded = dict(rr.recorded_lists())
        chosen = {
            "two.late-statement": cases["two.late-statement"],
            "three.reported-s1.box7-s2-s3": cases["three.reported-s1.box7-s2-s3"],
            "relabelled v83/track0/s0/b4_two_statements_one_unanswered":
                probe.relabel(recorded["v83/track0/s0/b4_two_statements_one_unanswered"]),
        }
        core = rr.resolve_core("v106")
        controls: dict[str, Any] = {}
        for name, acts in chosen.items():
            saved_a = save_pre_build(core, acts, "demo.sql.controls")
            saved_b = save_pre_build(core, acts, "demo.sql.controls", scratch=True)
            controls[name] = semantic_controls(saved_a, saved_b)
        text = json.dumps(controls, indent=1) + "\n"
        rr._check_no_local_paths(text, "controls")
        (HERE / "replay_controls.json").write_text(text, encoding="utf-8")
        print(text)
        return
    expectations = json.loads(EXPECT.read_text(encoding="utf-8")) if EXPECT.exists() else []
    if args.merge:
        results: dict[str, Any] = {}
        for path in args.merge:
            results.update(json.loads(path.read_text(encoding="utf-8"))["results"])
        summary = summarize(results, expectations)
        text = json.dumps(summary, indent=1) + "\n"
        rr._check_no_local_paths(text, "summary")
        assert args.out is not None
        args.out.write_text(text, encoding="utf-8")
        print(json.dumps({k: summary[k] for k in ("lists", "classes", "passing", "failing",
                                                   "unexpected_differences", "expectations_used", "outcomes")}, indent=1))
        return
    index, total = (int(part) for part in args.shard.split("/"))
    lists = [item for position, item in enumerate(chosen_lists(args.set)) if position % total == index]
    results = rr.replay(lists, (rr.resolve_core("v106"),), DesignCompare(expectations),
                        workers=args.workers, part=args.part)
    assert args.out is not None
    args.out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps({"results": results}, indent=1) + "\n"
    rr._check_no_local_paths(text, "shard")
    args.out.write_text(text, encoding="utf-8")
    print(args.out.name, len(results), dict(Counter(row["class"] for row in results.values())))


if __name__ == "__main__":
    main()
