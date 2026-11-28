"""Box C/F question names through the saved output of live_coordinate_run."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from typing import Any, TypeVar
from unittest.mock import patch

import pytest

from packages.derivation.presentation_projection import (
    PresentationModelError,
    _SALE_ANSWER_SOURCES,
    _SALE_MEMBER_VALIDATION,
    _SaleQuestions,
    _SaleQuestionTrace,
    validate_presentation_model,
)
from packages.kernel.findings import FindingState
from tests import evidence_loader
from tools import recorded_replay as rr

EVIDENCE = (
    Path(__file__).resolve().parents[1]
    / "docs/phases/engine-breadth/milestones/sale-question-names-evidence"
)
PROBE = evidence_loader.load(EVIDENCE / "probe.py", "probe", owner=__name__)
evidence_loader.load(EVIDENCE / "scratch.py", "scratch", owner=__name__)
TRUSTED = evidence_loader.load(EVIDENCE / "trusted_inputs.py", "sale_names_p0_inputs", owner=__name__)
ALPHA, ZULU, PEER = PROBE.ALPHA, PROBE.ZULU, PROBE.PEER
PACKAGE = "tax.us.2025.package.core-calculations"
Json = dict[str, Any]
T = TypeVar("T")


def _saved(sales: tuple[Any, ...], name: str, core: str | rr.ReplayCore = PROBE.CORE) -> Json:
    result = rr.saved_output(core, PROBE.build_sales(sales), f"demo.sale-name-test.{name}")
    assert result["outcome"] == "success", result.get("message")
    return dict(result["model"])


def _line(model: Json, term: str) -> Json:
    suffix = ".schedule-d.line-" + {"st": "3", "lt": "10"}[term]
    return dict(next(section["resolved"] for section in model["sections"] if section["field"]["id"].endswith(suffix)))


def _ordered_names(line: Json) -> list[str]:
    return [reason["saleLabel"] for reason in line["reasons"] if "saleLabel" in reason]


@pytest.mark.parametrize("term", ["st", "lt"])
@pytest.mark.parametrize(("condition", "peer_condition"), [
    ("missing-proceeds", "good"), ("missing-basis", "good"), ("gain", "exceeds"),
])
@pytest.mark.parametrize("sale_count", [2, 3])
def test_box_c_and_f_questions_name_the_unanswered_sales(
    term: str, condition: str, peer_condition: str, sale_count: int,
) -> None:
    second = peer_condition if sale_count == 2 or condition == "gain" else condition
    sales = [PROBE.Sale(ZULU, term, condition), PROBE.Sale(ALPHA, term, second)]
    if sale_count == 3:
        sales.append(PROBE.Sale(PEER, term))
    model = _saved(tuple(sales), f"{term}.{condition}.{sale_count}")
    line = _line(model, term)
    if condition == "gain":
        expected = [ALPHA, ZULU]
        names = [reason for reason in line["reasons"] if "saleLabel" in reason]
        named_index = line["reasons"].index(names[0])
        assert line["reasons"][named_index - 1] == {"sentence": names[0]["sentence"]}
        refs = [ref for ref in line["questionRefs"] if ref["reasonIndices"] == [named_index - 1]]
        assert refs
        groups = {group["id"]: group for group in model["questionGroups"]}
        assert all(groups[ref["groupId"]]["question"] == names[0]["sentence"] for ref in refs)
    else:
        expected = [ZULU] if sale_count == 2 else [ALPHA, ZULU]
    assert _ordered_names(line) == expected


@pytest.mark.parametrize("peer", [None, ALPHA, ALPHA.lower(), "  demo  Alpha shares  "])
def test_single_sale_and_label_collisions_with_an_answered_peer_keep_generic_question(peer: str | None) -> None:
    sales: tuple[Any, ...] = (PROBE.Sale(ALPHA, condition="gain"),)
    if peer is not None:
        sales += (PROBE.Sale(peer, "lt"),)
    line = _line(_saved(sales, "single-or-collision"), "st")
    assert not _ordered_names(line)
    assert any("wash-sale loss disallowed do you enter" in reason["sentence"] for reason in line["reasons"])


@pytest.mark.parametrize("label", [" ", "\t", "demo.sfa.demo.sale-names.0.sale"])
def test_unusable_label_on_one_of_two_targets_keeps_generic_question(label: str) -> None:
    sales = (PROBE.Sale(label, condition="gain"), PROBE.Sale(ALPHA, condition="exceeds"))
    line = _line(_saved(sales, "missing-label"), "st")
    assert not _ordered_names(line)
    assert any("wash-sale loss disallowed do you enter" in reason["sentence"] for reason in line["reasons"])


def test_recorded_spacing_and_punctuation_are_preserved() -> None:
    label = "demo  Zulu & Sons"
    sales = (PROBE.Sale(label, condition="missing-basis"), PROBE.Sale(PEER))
    assert _ordered_names(_line(_saved(sales, "recorded-spacing"), "st")) == [label]


@pytest.mark.parametrize(
    ("key", "term"),
    [("demo.amounts-disagree", "st"), ("demo.long-amounts-disagree", "lt")],
)
def test_basis_consistency_keeps_existing_reason(key: str, term: str) -> None:
    result = rr.saved_output(PROBE.CORE, PROBE.build_sales(PROBE.cases()[key]), "demo.basis-consistency-" + term)
    assert result["outcome"] == "success", result.get("message")
    blocked, = [
        row for row in result["report"]["dispositions"]
        if row["artifact_id"].endswith(f".no1099b-{term}-txn.amounts-check")
    ]
    assert blocked["disposition"] == "blocked" and blocked["code"] == "DEPENDENCY_INVALID"
    line = _line(result["model"], term)
    reasons = [reason for reason in line["reasons"] if "basis" in reason["sentence"]]
    holding_period = {"st": "short-term", "lt": "long-term"}[term]
    assert reasons == [{
        "sentence": f"What is the basis of each {holding_period} sale you recorded without a Form 1099-B?",
    }]


def test_saved_sale_reason_cannot_be_a_question_reference() -> None:
    model = _saved(PROBE.cases()["demo.two-fixes"], "validator-link")
    line = _line(model, "st")
    index = next(i for i, reason in enumerate(line["reasons"]) if "saleLabel" in reason)
    sentence = line["reasons"][index]["sentence"]
    ref = next(item for item in line["questionRefs"] if any(
        line["reasons"][pos]["sentence"] == sentence for pos in item["reasonIndices"]
    ))
    ref["reasonIndices"] = [index]
    with pytest.raises(PresentationModelError, match="sale names cannot link"):
        validate_presentation_model(model)


def _without(item: Mapping[str, T], key: str) -> dict[str, T]:
    return {k: value for k, value in item.items() if k != key}


def _pin_changes(
    record: Mapping[str, Any], pin: Mapping[str, Any], replacement: Mapping[str, Any] | None = None,
) -> Json:
    return {**record, "pins": [
        item for old in record["pins"] for item in
        ([old] if old is not pin else [replacement] if replacement is not None else [])
    ]}


def _trusted_input_controls(
    walker: _SaleQuestions, traces: list[_SaleQuestionTrace], questions: Mapping[str, str],
    other: set[str], route: str, version: str,
) -> None:
    named = version != "v108"
    answer, row, leaf, declaration = traces[0]
    assert row is not None and walker.current_ids is not None
    source = _SALE_ANSWER_SOURCES[answer]
    family = source.removesuffix("-txn")
    source_id, finding = next((fid, walker.state.findings[fid]) for fid in walker.current_ids if
        walker.state.findings[fid]["fact_id"].startswith(source + "|sale=demo.sfa.demo.sale-names.0.sale,"))
    fact_id = finding["fact_id"]
    entity_id = dict(walker.facts[fact_id].keys)["sale"]
    assert walker.adopted_package == (PACKAGE, version)
    want = [ZULU] if route == "pairing" else [ALPHA, ZULU]
    exact = {questions[answer]: [{"sentence": questions[answer], "saleLabel": label} for label in want]}
    original = _SaleQuestions.reasons(walker, traces, questions, other)
    assert original == (exact if named else {})

    def check(
        name: str, *, new_traces: list[_SaleQuestionTrace] = traces, new_questions: Mapping[str, str] = questions,
        new_other: set[str] = other, **changes: Any,
    ) -> None:
        options: Json = dict(
            adopted_package=walker.adopted_package, state=walker.state, current_ids=walker.current_ids,
            members=walker.members, publications=walker.publications,
        )
        altered = _SaleQuestions(**(options | changes))
        assert altered.reasons(new_traces, new_questions, new_other) == {}, name

    def changed_row(name: str, updated: Mapping[str, Any] | None) -> None:
        check(name, new_traces=[(ft, updated, key, declared) for ft, _, key, declared in traces])

    def change_member(member_id: str, **updates: Any) -> list[Mapping[str, Any]]:
        return [({**m, **updates} if m.get("id") == member_id else m) for m in walker.members]

    def change_entity(**updates: Any) -> FindingState:
        state = walker.state.fact_state
        lifecycle = state.entities[entity_id]
        return replace(walker.state, fact_state=replace(state, entities={
            **state.entities, entity_id: replace(lifecycle, entity=updates.pop("entity", lifecycle.entity), **updates),
        }))

    check("missing currency", current_ids=None)
    check("source no longer current", current_ids=walker.current_ids - {source_id})
    check("unresolved current finding", current_ids=walker.current_ids | {"demo.unresolved"})
    check("wrong package", adopted_package=("demo.other.core", version))
    check("ambiguous witness", new_traces=[*traces, (answer, None, answer, None)])
    check("same wording from different cause", new_other={questions[answer]})
    check("missing question text", new_questions={})
    entity = walker.state.fact_state.entities[entity_id].entity
    check("wrong kind", state=change_entity(entity={**entity, "kind": "demo.wrong.kind"}))
    check("inactive entity", state=change_entity(status="superseded"))
    for label in (None, "\t  ", entity_id, "demo </script>"):
        replacement = _without(entity, "label") if label is None else {**entity, "label": label}
        check(f"unusable entity label {label!r}", state=change_entity(entity=replacement))
    for kind in (source, answer):
        state = walker.state.fact_state
        declaration_type = state.fact_types[kind]
        for identity in ([], [*declaration_type["identity_keys"], {"name": "demo.extra.key"}]):
            check("effective identity drift", state=replace(walker.state, fact_state=replace(state, fact_types={
                **state.fact_types, kind: {**declaration_type, "identity_keys": identity},
            })))
        declarations = [m for m in walker.members if any(item["id"] == kind for item in m.get("fact_types", ()))]
        assert declarations
        for member in declarations:
            check("adopted identity drift", members=change_member(member["id"], fact_types=[
                {**item, "identity_keys": []} if item["id"] == kind else item for item in member["fact_types"]
            ]))
        check("adopted identity removed", members=[
            {**member, "fact_types": [item for item in member["fact_types"] if item["id"] != kind]}
            if member in declarations else member for member in walker.members
        ])
    changed_row("missing row", None)
    changed_row("missing pins", _without(row, "pins"))
    core_pin = next(pin for pin in row["pins"] if pin["role"] == "adoption")
    changed_row("missing row core pin", _pin_changes(row, core_pin))
    changed_row("wrong row core version", _pin_changes(row, core_pin, {**core_pin, "version": "v999"}))
    changed_row("wrong disposition", {**row, "disposition": "published"})
    changed_row("wrong block code", {**row, "code": "DEMO_WRONG_CODE"})
    check("wrong leaf", new_traces=[(ft, row, "demo.wrong.leaf", d) for ft, row, _, d in traces])
    check("wrong source set", members=change_member(family, member_predicate={"fact_type": "demo.wrong.fact"}))
    check("missing source set", members=[m for m in walker.members if m.get("id") != family])
    if route == "pairing":
        rule = next(m for m in walker.members if m["id"] == row["artifact_id"])
        changed = deepcopy(rule["when"])
        changed["args"][0]["source_set"] = "demo.wrong.family"
        check("wrong guard source set", members=change_member(rule["id"], when=changed))
        check("inactive pairings", members=change_member(rule["id"], when={
            "op": "any", "args": [True, rule["when"]],
        }))
        check("unpinned rule version", members=change_member(rule["id"], version="v999"))
        family_pin = next(pin for pin in row["pins"] if pin["role"] == "package" and pin["id"] == family)
        changed_row("missing row source-set pin", _pin_changes(row, family_pin))
        source_pin = next(pin for pin in row["pins"] if pin["id"] == source_id)
        peer_pin = next(pin for pin in row["pins"] if
            walker.state.findings.get(pin["id"], {}).get("fact_id", "").startswith(answer + "|"))
        for pin in (source_pin, peer_pin):
            changed_row("missing pairing input", _pin_changes(row, pin))
            for change in ({"version": "v999"}, {"origin": "derived"}, {"id": "demo.unknown.pin"}):
                changed_row("invalid pairing input", _pin_changes(row, pin, {**pin, **change}))
    else:
        pid, result = next((fid, pub) for fid, pub in walker.publications.items()
                           if pub["symbol"] == family + _SALE_MEMBER_VALIDATION + "." + fact_id)
        check("missing validation publication", publications=_without(walker.publications, pid))
        check("changed validation publication version", publications={
            **walker.publications, pid: {**result, "version": "v999"},
        })
        for pin in result["pins"]:
            check("missing validation publication pin", publications={
                **walker.publications, pid: _pin_changes(result, pin),
            })
            check("bad validation publication pin", publications={
                **walker.publications, pid: _pin_changes(result, pin, {**pin, "version": "v999"}),
            })
        check("wrong validation member", publications={
            **walker.publications, pid: {**result, "value": {**result["value"], "member_fact_id": "demo.other"}},
        })
        check("unwitnessed validation code", publications={
            **walker.publications, pid: {**result, "value": {**result["value"], "violations": []}},
        })
        assert declaration is not None and leaf in row["missing"]
        assert all(declared is not None for _, _, _, declared in traces)
        check("wrong fixing question pin", new_traces=[
            (ft, row, code, {**(declared or {}), "fact_type": {"id": ft, "version": "v999"}})
            for ft, row, code, declared in traces
        ])


@pytest.mark.parametrize("version", ["v108", "v109", "v110"])
@pytest.mark.parametrize(("route", "key"), [("pairing", "demo.missing-basis"), ("fix", "demo.two-fixes")])
def test_trusted_inputs_fail_closed_on_each_core(tmp_path: Path, version: str, route: str, key: str) -> None:
    core = TRUSTED.successor(tmp_path) if version == "v110" else rr.resolve_core(version)
    seen: list[tuple[_SaleQuestions, list[_SaleQuestionTrace], Mapping[str, str], set[str]]] = []
    original = _SaleQuestions.reasons

    def observe(
        walker: _SaleQuestions, traces: Iterable[_SaleQuestionTrace], questions: Mapping[str, str], other: set[str],
    ) -> dict[str, list[dict[str, Any]]]:
        traces = list(traces)
        if traces and not seen:
            seen.append((walker, traces, questions, other))
        return original(walker, traces, questions, other)

    # Collect the older core's actual leaves while keeping its version gate
    # active during attribution and in each corrupt-input check.
    with patch.object(_SaleQuestions, "reasons", observe), patch.object(
        _SaleQuestions, "applies", lambda self, ft: ft in _SALE_ANSWER_SOURCES,
    ):
        model = _saved(PROBE.cases()[key], f"{version}.{route}", core)
    assert _ordered_names(_line(model, "st")) == (
        [] if version == "v108" else [ZULU] if route == "pairing" else [ALPHA, ZULU]
    )
    assert len(seen) == 1
    _trusted_input_controls(*seen[0], route, version)
