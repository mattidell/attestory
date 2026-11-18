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
        "dispositionNodes": {
            "demo.symbol.blocked": {"children": ["demo.missing.one"], "symbol": "demo.symbol.blocked",
                                    "records": [{"artifact_id": "demo.rule.blocked", "disposition": "blocked", "code": "DEPENDENCY_ABSENT"}]},
        },
        "sectionRoots": {"line-1": {"kind": "published", "root": 0}},
        "authorization": {"kind": "authorization", "status": "AUTHORIZATION_ABSENT"},
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


def _graph_value(m: dict[str, Any], r: dict[str, Any]) -> None:
    next(n for n in m["explanationGraph"]["nodes"].values() if n["kind"] == "input")["value"] = "no"


def _edge_target(m: dict[str, Any], r: dict[str, Any]) -> None:
    next(n for n in m["explanationGraph"]["nodes"].values() if n["kind"] == "derived")["edges"][0]["pin"]["version"] = "v9"


def _disposition_node(m: dict[str, Any], r: dict[str, Any]) -> None:
    m["dispositionNodes"]["demo.symbol.blocked"]["records"][0]["code"] = "demo.changed"


def _other_model_keys(m: dict[str, Any], r: dict[str, Any]) -> None:
    m["sectionRoots"]["line-1"]["root"] = 1
    m["authorization"]["status"] = "demo.changed"


@pytest.mark.parametrize(
    ("name", "mutate", "kind"),
    [
        ("graph node value", _graph_value, "graph"),
        ("graph edge pin", _edge_target, "graph"),
        ("disposition node record", _disposition_node, "model"),
        ("section roots and authorization", _other_model_keys, "model"),
    ],
)
def test_graph_and_other_model_keys_are_compared(name: str, mutate: Any, kind: str) -> None:
    result = _classify(mutate)
    assert result["class"] == "unexpected", name
    assert {d["kind"] for d in result["unexpected"]} == {kind}
    # the records exist in the snapshot: a snapshot that stops flattening them would not see the change
    model, report = _saved()
    assert {k for k, *_ in rr.snapshot(model, report)["records"]} >= {"graph", "model"}


@pytest.mark.parametrize(
    ("old", "new"),
    [(100, 100.0), (1, True), (0, False), (1.0, True), (100, "100"), (None, 0), ("", None)],
)
def test_values_compare_by_type_not_plain_equality(old: Any, new: Any) -> None:
    def set_value(m: dict[str, Any], value: Any) -> None:
        m["sections"][0]["resolved"]["value"] = value
        next(n for n in m["explanationGraph"]["nodes"].values() if n["kind"] == "input")["value"] = value

    model, report = _saved()
    set_value(model, old)
    changed = copy.deepcopy(model)
    set_value(changed, new)
    base, other = rr.snapshot(model, report), rr.snapshot(changed, report)
    result = rr.classify_full(base, other)
    assert result["class"] == "unexpected"
    assert {d["kind"] for d in result["unexpected"]} == {"page", "graph"}
    # an expectation is typed the same way: declaring 1 does not accept 1.0 or True
    right = [rr.Expectation(("page", "graph"), r"(?:resolved\.)?value", before=old, after=new)]
    wrong = [rr.Expectation(("page", "graph"), r"(?:resolved\.)?value", before=new, after=old)]
    assert rr.classify_full(base, other, right)["class"] == "expected_changes"
    assert rr.classify_full(base, other, wrong)["class"] == "unexpected"


def test_value_expectation_does_not_accept_an_equal_but_different_type() -> None:
    model, report = _saved()
    changed = copy.deepcopy(model)
    changed["sections"][0]["resolved"]["value"] = 100.0
    base, other = rr.snapshot(model, report), rr.snapshot(changed, report)
    assert rr.classify_full(base, other, [rr.Expectation(("page",), "resolved.value", before=100, after=100.0)])["class"] == "expected_changes"
    assert rr.classify_full(base, other, [rr.Expectation(("page",), "resolved.value", before=100, after=100)])["class"] == "unexpected"
    assert rr.classify_full(base, other, [rr.Expectation(("page",), "resolved.value", before=True, after=100.0)])["class"] == "unexpected"


def test_hash_keyed_order_and_rendered_key_order_are_recorded_as_named_blind_spot_substitutes() -> None:
    model, report = _saved()
    derived = next(n for n in model["explanationGraph"]["nodes"].values() if n["kind"] == "derived")
    derived["edges"].append({"pin": {"id": "demo.a-input", "role": "input", "version": "v1"}, "target": "input:1:demo.input:v1"})
    snap = rr.snapshot(model, report)
    flags = {(k, a): v for k, i, a, v in snap["records"] if a.endswith("role-id-order")}
    assert flags[("graph", "edges-in-role-id-order")] is False  # ('input', 'demo.a-input') sorts before ('input', 'demo.input')
    assert flags[("page", "pins-in-role-id-order")] is True
    unsorted_pins = copy.deepcopy(model)
    unsorted_pins["sections"][0]["resolved"]["act"]["finding"]["pins"].reverse()
    flags = {(k, a): v for k, i, a, v in rr.snapshot(unsorted_pins, report)["records"] if a.endswith("role-id-order")}
    assert flags[("page", "pins-in-role-id-order")] is False

    def claims(order: list[str]) -> dict[str, Any]:
        m, r = _saved()
        m["mortgageBorrowingExplanation"] = {"recordedApplicableClaims": {k: {"value": 1} for k in order}}
        return rr.snapshot(m, r)

    assert rr.diff_snapshots(claims(["a", "b"]), claims(["a", "b"])) == []
    changed = rr.diff_snapshots(claims(["a", "b"]), claims(["b", "a"]))
    assert [d["attribute"] for d in changed] == ["mortgageBorrowingExplanation.recordedApplicableClaims@keys"]
    assert "mortgageBorrowingExplanation" in claims(["a"])["blocks"]


def test_local_paths_in_saved_strings_are_compared_not_masked() -> None:
    def labelled(path: str) -> dict[str, Any]:
        m, r = _saved()
        m["sections"][0]["field"]["label"] = "see " + "/" + "var/" + path
        return rr.snapshot(m, r)

    assert rr.classify_full(labelled("demo-a"), labelled("demo-b"))["class"] == "unexpected"


def test_generated_ids_outside_the_graph_and_rows_are_aliased_by_position() -> None:
    def with_block(first: str, second: str) -> dict[str, Any]:
        m, r = _saved()
        m["mortgageBorrowingExplanation"] = {"calculationChain": {"dispositions": [
            {"artifact_id": "demo.rule.one", "pins": [{"id": "finding:derived:" + first, "role": "input", "version": "v1"}]},
            {"artifact_id": "demo.rule.two", "pins": [{"id": "finding:derived:" + second, "role": "input", "version": "v1"}]},
        ]}}
        return rr.snapshot(m, r)

    same = rr.diff_snapshots(with_block("1" * 24, "2" * 24), with_block("3" * 24, "4" * 24))
    assert same == []
    assert "1" * 24 not in json.dumps(with_block("1" * 24, "2" * 24))
    # a changed version on such a pin is still a difference, on the aliased identity
    changed = with_block("3" * 24, "4" * 24)
    changed["records"] = [[k, i, a, "v2" if a == "version" and "demo.rule.two" in i else v] for k, i, a, v in changed["records"]]
    found = rr.diff_snapshots(with_block("1" * 24, "2" * 24), changed)
    assert len(found) == 1 and "demo.rule.two" in found[0]["identity"] and found[0]["attribute"] == "version"


def test_run_full_reports_every_unused_expectation_by_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    model, report = _saved("v1")
    new_model, new_report = _saved("v2")
    snaps = {"core-a": rr.snapshot(model, report), "core-b": rr.snapshot(new_model, new_report)}
    monkeypatch.setattr(rr, "resolve_core", lambda core: core)
    monkeypatch.setattr(rr, "snapshot_run", lambda core, acts, run_id: snaps[core])
    monkeypatch.setattr(rr, "recorded_lists", lambda: [("demo/one", []), ("demo/two", [])])
    monkeypatch.setattr(
        rr, "replay", lambda lists, cores, per_list, workers=None, part=None: {k: per_list(k, a, tuple(cores)) for k, a in lists},
    )
    used = rr.version_change("demo.package", "v1", "v2")
    unused_text = rr.text_change(FIELD, "description", "never saved", "never seen")
    unused_version = rr.version_change("demo.absent", "v1", "v2")
    summary = rr.run_full("core-a", "core-b", [used, unused_text, unused_version])
    assert summary["classes"] == {"expected_changes": 2}
    assert summary["expectations_declared"] == 3 and summary["expectations_used"] == 1
    listed = summary["unused_expectations"]
    assert [row["note"] for row in listed] == [unused_text.note, unused_version.note]
    assert listed[0]["attribute"] == "description" and listed[0]["before"] == "never saved"
    assert listed[1]["identity"] == rr._id_pattern("demo.absent") and listed[1]["after"] == "v2"
    assert summary["optional_blocks_reached"] == {}
    # an expectation list that is all used reports nothing unused
    assert rr.run_full("core-a", "core-b", [used])["unused_expectations"] == []


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
    for name in ("changed_graph_node_value", "changed_disposition_node", "changed_section_root", "changed_authorization"):
        assert verdicts[name]["available"] and verdicts[name]["ok"], name
    assert not verdicts["changed_explanation_block_note"]["available"]  # no recorded list reaches the block
    again = rr.saved_output("v96", harness.opened(), "demo.fsr.test")
    assert rr.diff_snapshots(rr.snapshot(saved["model"], saved["report"]), rr.snapshot(again["model"], again["report"])) == []


def mortgage_explanation_acts() -> list[dict[str, Any]]:
    """Synthetic demo.* act list (two Form 1098 statements on one borrowing) that produces the
    mortgage borrowing explanation block.

    The connected-borrowing case of the mortgage calculation tests is built with its own
    recorder; its package adoption is dropped, so a core's adoption is the only one.
    """
    from unittest import mock

    from tests import test_mortgage_borrowing_calculation as mortgage

    captured: list[list[dict[str, Any]]] = []
    real = getattr(mortgage, "live_coordinate_run")

    def spy(*args: Any, **kwargs: Any) -> Any:
        captured.append(copy.deepcopy(list(kwargs["authoritative_acts"])))
        return real(*args, **kwargs)

    with mock.patch.object(mortgage, "live_coordinate_run", spy):
        mortgage._run_connected_case()
    acts = [row for row in captured[-1] if row["kind"] != "package-adoption"]
    for index, row in enumerate(acts):
        row["committed_against"] = index
    return acts


@pytest.mark.live
def test_mortgage_explanation_block_is_snapshotted_and_its_notes_are_controlled() -> None:
    acts = mortgage_explanation_acts()
    assert all(row["actor"] == "demo.user.filer-1" for row in acts)
    for core in ("v95", "v96"):
        saved = rr.saved_output(core, acts, "demo.fsr.mortgage")
        assert saved["outcome"] == "success", core
        assert "mortgageBorrowingExplanation" in saved["model"]
        snap = rr.snapshot(saved["model"], saved["report"])
        assert "mortgageBorrowingExplanation" in snap["blocks"]
        notes = [r for r in snap["records"] if r[0] == "model" and r[2] == "notes"
                 and r[1].startswith("mortgageBorrowingExplanation.calculationChain.resolvedContent[")]
        assert len(notes) >= 15 and all(isinstance(r[3], str) and r[3] for r in notes)
    verdicts = rr.run_controls(saved["model"], saved["report"])
    assert verdicts["changed_explanation_block_note"]["available"] and verdicts["changed_explanation_block_note"]["ok"]
    assert verdicts["changed_explanation_block_note"]["class"] == "unexpected"
    assert verdicts["expected_explanation_block_note"]["ok"]
    assert verdicts["expected_explanation_block_note"]["class"] == "expected_changes"
    # a changed notes text that was not declared, and one declared for another citizen, both fail
    base = rr.snapshot(saved["model"], saved["report"])
    changed = copy.deepcopy(saved["model"])
    member = rr._first_explanation_note(changed)
    assert member is not None
    before = member["notes"]
    member["notes"] = before + " demo.reworded"
    other = rr.snapshot(changed, saved["report"])
    named = rr.text_change(member["id"], "notes", before, before + " demo.reworded")
    assert rr.classify_full(base, other, [named])["class"] == "expected_changes"
    stranger = rr.text_change("tax.us.2025.rule.f1098-line8a-other", "notes", before, before + " demo.reworded")
    assert rr.classify_full(base, other, [stranger])["class"] == "unexpected"
