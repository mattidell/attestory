"""Tests for the full-surface snapshot, diff and strict classifier in tools/recorded_replay.py.

Fast tests use a small synthetic saved model and report.  The controls on one
real saved output run a live coordinate run and are marked live.
"""

from __future__ import annotations

import copy
import json
import pickle
from typing import Any

import pytest

from tools import recorded_replay as rr

FIELD = "demo.field.alpha"
OTHER = "demo.field.beta"
RULE = "demo.rule.alpha"


def _finding(fid: str, symbol: str, value: str, version: str) -> dict[str, Any]:
    return {
        "id": fid,
        "symbol": symbol,
        "value": value,
        "version": "v2",
        "pins": [
            {"id": "demo.package", "role": "adoption", "version": version},
            {"id": RULE, "role": "computation", "version": "v1"},
        ],
    }


def _saved(version: str = "v1", fid: str = "finding:derived:" + "a" * 24) -> tuple[dict[str, Any], dict[str, Any]]:
    node_key = f"derived:40:{fid}:v2"
    model = {
        "runId": "demo.run.one",
        "schema": "presentation.v1",
        "sections": [
            {
                "id": "line-1",
                "field": {
                    "id": FIELD, "label": "Line 1", "description": "Alpha description",
                    "dispositions": {"published_value": {"explain": "Alpha explained", "render": "{value}"},
                                     "blocked": {"explain": "Alpha blocked", "codes": ["DEPENDENCY_ABSENT"], "render": ""}},
                },
                "resolved": {"disposition": "published_value", "value": 100,
                             "act": {"finding": _finding(fid, "demo.symbol.alpha", "100", version), "run_id": "demo.run.one"}},
            },
            {
                "id": "line-2",
                "field": {"id": OTHER, "label": "Line 2", "description": "Beta description", "dispositions": {}},
                "resolved": {"disposition": "blocked", "activeCodes": ["DEPENDENCY_ABSENT"],
                             "reasons": [{"question_id": "demo.q.one", "text": "Is it so?"}]},
            },
        ],
        "attachments": [{"id": "demo.attachment", "title": "Attachment title", "resolved": {"disposition": "guard_inapplicable"}}],
        "explanationGraph": {
            "run_id": "demo.run.one",
            "nodes": {
                node_key: {"id": fid, "kind": "derived", "symbol": "demo.symbol.alpha", "value": "100", "version": "v2",
                           "produced_by": {"id": RULE, "role": "computation", "version": "v1"},
                           "edges": [{"pin": {"id": "demo.input", "role": "input", "version": "v1"}, "target": "input:1:demo.input:v1"}]},
                "input:1:demo.input:v1": {"id": "demo.input", "kind": "input", "value": "yes", "version": "v1", "edges": []},
            },
            "roots": [{"role": "output", "target": node_key}],
        },
        "dispositionNodes": {},
    }
    report = {
        "run_id": "demo.run.one",
        "stop_reason": "complete",
        "dispositions": [
            {"artifact_id": RULE, "symbol": "demo.symbol.alpha", "disposition": "published", "finding_id": fid,
             "act_id": "act:publication:" + "b" * 24, "pins": [{"id": "demo.package", "role": "adoption", "version": version}]},
            {"artifact_id": "demo.rule.blocked", "symbol": "demo.symbol.blocked", "disposition": "blocked",
             "code": "DEPENDENCY_ABSENT", "missing": ["demo.missing.one", "demo.missing.two"]},
        ],
    }
    return model, report


def _classify(mutate: Any, expectations: Any = ()) -> dict[str, Any]:
    model, report = _saved()
    base = rr.snapshot(model, report)
    changed_model, changed_report = copy.deepcopy(model), copy.deepcopy(report)
    mutate(changed_model, changed_report)
    return rr.classify_full(base, rr.snapshot(changed_model, changed_report), expectations)


def test_identical_snapshots_and_stable_hash() -> None:
    model, report = _saved()
    a, b = rr.snapshot(model, report), rr.snapshot(copy.deepcopy(model), copy.deepcopy(report))
    assert rr.diff_snapshots(a, b) == []
    assert rr.snapshot_sha256(a) == rr.snapshot_sha256(b)
    assert rr.classify_full(a, b)["class"] == "identical"


def test_snapshot_holds_every_field_row_and_sentence() -> None:
    model, report = _saved()
    records = {(k, i, a): v for k, i, a, v in rr.snapshot(model, report)["records"]}
    assert records[("page", "sections[line-1]", "resolved.value")] == 100
    assert records[("page", f"sections[line-1]/field={FIELD}", "dispositions.blocked.explain")] == "Alpha blocked"
    assert records[("page", "sections[line-2]", "resolved.reasons@order")] == ["[0]"]
    assert records[("row", f"dispositions[{RULE}|demo.symbol.alpha]", "disposition")] == "published"
    assert records[("row", "dispositions[demo.rule.blocked|demo.symbol.blocked]", "missing")] == ["demo.missing.one", "demo.missing.two"]
    assert records[("attachment", "attachments[demo.attachment]", "title")] == "Attachment title"


def test_generated_ids_runs_and_paths_are_masked_not_compared() -> None:
    other_id = "finding:derived:" + "c" * 24
    model, report = _saved(fid=other_id)
    text = json.dumps(rr.snapshot(model, report))
    assert other_id not in text and "demo.run.one" not in text
    original = rr.snapshot(*_saved())
    assert rr.diff_snapshots(original, rr.snapshot(model, report)) == []
    failure = rr.failure_snapshot("error", "SomeError", "failed at " + "/" + "Users/x/y.json now")
    assert "/" + "Users" not in json.dumps(failure) and "<path>" in json.dumps(failure)


@pytest.mark.parametrize(
    ("name", "mutate", "attribute"),
    [
        ("field value", lambda m, r: m["sections"][0]["resolved"].__setitem__("value", 101), "resolved.value"),
        ("value type", lambda m, r: m["sections"][0]["resolved"].__setitem__("value", True), "resolved.value"),
        ("row code", lambda m, r: r["dispositions"][1].__setitem__("code", "demo.changed"), "code"),
        ("row disposition", lambda m, r: r["dispositions"][0].__setitem__("disposition", "inapplicable"), "disposition"),
        ("page disposition", lambda m, r: m["sections"][1]["resolved"].__setitem__("disposition", "published_value"), "resolved.disposition"),
        ("missing name", lambda m, r: r["dispositions"][1]["missing"].__setitem__(0, "demo.other"), "missing"),
        ("question", lambda m, r: m["sections"][1]["resolved"]["reasons"][0].__setitem__("text", "Is it not?"), "text"),
        ("sentence", lambda m, r: m["sections"][0]["field"].__setitem__("description", "Changed"), "description"),
        ("categorical render", lambda m, r: m["sections"][0]["field"]["dispositions"]["published_value"].__setitem__("render", "x"), "dispositions.published_value.render"),
        ("attachment title", lambda m, r: m["attachments"][0].__setitem__("title", "New"), "title"),
        ("report key", lambda m, r: r.__setitem__("stop_reason", "other"), "stop_reason"),
    ],
)
def test_unexpected_changes_fail(name: str, mutate: Any, attribute: str) -> None:
    result = _classify(mutate)
    assert result["class"] == "unexpected", name
    assert any(attribute in d["attribute"] or attribute in d["identity"] for d in result["unexpected"])


def test_added_and_removed_fields_and_rows_fail() -> None:
    def add_field(m: dict[str, Any], r: dict[str, Any]) -> None:
        extra = copy.deepcopy(m["sections"][0])
        extra["id"] = "line-extra"
        m["sections"].append(extra)

    def remove_field(m: dict[str, Any], r: dict[str, Any]) -> None:
        m["sections"].pop()

    def add_row(m: dict[str, Any], r: dict[str, Any]) -> None:
        r["dispositions"].append({"artifact_id": "demo.extra", "disposition": "blocked"})

    def remove_row(m: dict[str, Any], r: dict[str, Any]) -> None:
        r["dispositions"].pop()

    def reorder(m: dict[str, Any], r: dict[str, Any]) -> None:
        m["sections"].reverse()

    assert {d["change"] for d in _classify(add_field)["unexpected"]} >= {"added"}
    assert {d["change"] for d in _classify(remove_field)["unexpected"]} >= {"removed"}
    assert _classify(add_row)["class"] == "unexpected"
    assert _classify(remove_row)["class"] == "unexpected"
    reordered = _classify(reorder)
    assert reordered["class"] == "unexpected" and reordered["unexpected"][0]["attribute"] == "sections@order"


def test_expected_sentence_passes_and_is_bounded() -> None:
    def change(m: dict[str, Any], r: dict[str, Any]) -> None:
        m["sections"][0]["field"]["dispositions"]["blocked"]["explain"] = "New blocked sentence"

    expect = rr.text_change(FIELD, "dispositions.blocked.explain", "Alpha blocked", "New blocked sentence")
    assert _classify(change, [expect])["class"] == "expected_changes"
    # the same sentence declared for another citizen, attribute or wording does not pass
    assert _classify(change, [rr.text_change(OTHER, "dispositions.blocked.explain", "Alpha blocked", "New blocked sentence")])["class"] == "unexpected"
    assert _classify(change, [rr.text_change(FIELD, "dispositions.published_value.explain", "Alpha blocked", "New blocked sentence")])["class"] == "unexpected"
    assert _classify(change, [rr.text_change(FIELD, "dispositions.blocked.explain", "Alpha blocked", "Other wording")])["class"] == "unexpected"

    def change_two(m: dict[str, Any], r: dict[str, Any]) -> None:
        change(m, r)
        m["sections"][0]["resolved"]["value"] = 5

    partial = _classify(change_two, [expect])
    assert partial["class"] == "unexpected" and len(partial["unexpected"]) == 1


def test_version_change_expectation_covers_only_the_named_move() -> None:
    model, report = _saved("v1")
    new_model, new_report = _saved("v2")
    base, successor = rr.snapshot(model, report), rr.snapshot(new_model, new_report)
    assert rr.classify_full(base, successor)["class"] == "unexpected"
    assert rr.classify_full(base, successor, [rr.version_change("demo.package", "v1", "v2")])["class"] == "expected_changes"
    assert rr.classify_full(base, successor, [rr.version_change("demo.package", "v1", "v3")])["class"] == "unexpected"
    assert rr.classify_full(base, successor, [rr.version_change("demo.package-other", "v1", "v2")])["class"] == "unexpected"


def test_expectation_must_name_kind_and_attribute_and_is_picklable() -> None:
    with pytest.raises(ValueError):
        rr.Expectation((), "x")
    with pytest.raises(ValueError):
        rr.Expectation(("page",), "")
    spec = rr.text_change(FIELD, "description", "a", "b")
    assert pickle.loads(pickle.dumps(spec)) == spec
    assert rr.Expectation(("page",), "title").kind == ("page",)
    compare = rr.FullSurfaceCompare([spec])
    assert pickle.loads(pickle.dumps(compare)).expectations == [spec]


def test_failure_snapshots_compare_class_and_message() -> None:
    a = rr.failure_snapshot("error", "FindingModelError", "same")
    assert rr.classify_full(a, rr.failure_snapshot("error", "FindingModelError", "same"))["class"] == "identical"
    assert rr.classify_full(a, rr.failure_snapshot("error", "FindingModelError", "different"))["class"] == "unexpected"
    success = rr.snapshot(*_saved())
    kinds = {d["kind"] for d in rr.diff_snapshots(a, success)}
    assert "outcome" in kinds


def test_pin_classify_is_unchanged() -> None:
    assert rr.classify({"lines": {"a": 1}}, {"lines": {"a": 1}})["class"] == "identical"
    assert rr.classify({"lines": {"a": 1}}, {"lines": {"a": 2}})["class"] == "numbers_changed"
    assert rr.classify({"questions": ["x"]}, {"questions": ["y"]})["class"] == "numbers_identical_sentences_changed"


@pytest.mark.live
def test_controls_on_one_real_saved_output() -> None:
    harness = rr._get_harness()
    saved = rr.saved_output("v96", harness.opened(), "demo.fsr.test")
    assert saved["outcome"] == "success"
    verdicts = rr.run_controls(saved["model"], saved["report"])
    assert verdicts["changed_field_value"]["ok"]
    assert verdicts["changed_unwatched_row_code"]["ok"]
    assert verdicts["removed_field"]["ok"] and verdicts["added_field"]["ok"]
    assert verdicts["changed_page_disposition"]["ok"] and verdicts["changed_row_disposition"]["ok"]
    assert verdicts["unexpected_sentence"]["ok"]
    assert verdicts["expected_sentence"]["must"] == "accept" and verdicts["expected_sentence"]["ok"]
    again = rr.saved_output("v96", harness.opened(), "demo.fsr.test")
    assert rr.diff_snapshots(rr.snapshot(saved["model"], saved["report"]), rr.snapshot(again["model"], again["report"])) == []
