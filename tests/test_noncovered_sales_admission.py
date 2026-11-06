"""Grouped closure admission and the covered-flag refusal.

v4 records one yes/no finding for every family it lists. no admits a family
only while that family has no current member. yes admits it until a later
added member. A covered sale with basis_reported_to_irs no is refused only
when the caller passes that family. v3 admission is the boolean-true rule.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from packages.derivation.marshal import marshal_closure_authority
from packages.derivation.presentation_projection import _closure_question_reasons
from packages.derivation.source_authority import (
    ClosureFindingRecord,
    covered_flag_block,
    families_refused_for_unreported_basis,
    group_member_counts,
    resolve_closure_admissions,
    stale_group_families,
)
from packages.kernel.currency import CurrencyView
from packages.kernel.findings import FindingState
from packages.tax.loader import (
    COVERED_FLAG_REFUSAL_CODE,
    COVERED_FLAG_REFUSAL_SENTENCE,
)

SHARED = "demo.ns.t1.noncovered-sold.source-closure"
LT = "demo.ns.t1.noncovered-lt"
ST = "demo.ns.t1.noncovered-st"
LT_MEMBER = "demo.ns.t1.noncovered-lt-txn"
ST_MEMBER = "demo.ns.t1.noncovered-st-txn"
WASH = "A wash-sale disallowance is recorded on a sale that is not a loss."


def _declaration(family_id: str, member: str) -> dict[str, Any]:
    return {
        "id": family_id,
        "version": "v1",
        "member_predicate": {"fact_type": member},
        "authorizes_subtotal": family_id + ".subtotal",
    }


def _group() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v4",
        "id": "demo.ns.t1.mapping.noncovered",
        "version": "v1",
        "closure_fact_type": {"id": SHARED, "version": "v1"},
        "closure_question": "Did you sell any securities whose basis was not reported to the IRS?",
        "admission": {"no": "closed-empty", "yes": "until-later-member"},
        "families": [
            {
                "family": {"id": LT, "version": "v1"},
                "member_fact_type": {"id": LT_MEMBER, "version": "v1"},
                "admits_symbol": LT + ".subtotal",
            },
            {
                "family": {"id": ST, "version": "v1"},
                "member_fact_type": {"id": ST_MEMBER, "version": "v1"},
                "admits_symbol": ST + ".subtotal",
            },
        ],
    }


def _declarations() -> list[dict[str, Any]]:
    return [_declaration(LT, LT_MEMBER), _declaration(ST, ST_MEMBER)]


def _horizons() -> dict[str, str]:
    return {LT: "demo.ns.t1.lt.h0", ST: "demo.ns.t1.st.h0"}


def _answer(value: str) -> ClosureFindingRecord:
    return ClosureFindingRecord("demo.ns.t1.answer", SHARED, "", value)


def _admit(
    value: str,
    *,
    counts: dict[str, int] | None = None,
    acts: list[dict[str, Any]] | None = None,
) -> set[str]:
    admitted = resolve_closure_admissions(
        [_group()],
        _declarations(),
        [_answer(value)],
        _horizons(),
        member_counts=counts or {},
        acts=acts or [],
    )
    return set(admitted)


def _source(name: str) -> SimpleNamespace:
    return SimpleNamespace(name=name)


def test_no_with_zero_members_admits_each_listed_family() -> None:
    assert _admit("no") == {LT, ST}


def test_no_with_a_member_does_not_admit_that_family() -> None:
    assert _admit("no", counts={LT: 1, ST: 0}) == {ST}


def test_yes_admits_each_listed_family() -> None:
    assert _admit("yes") == {LT, ST}


def test_a_recorded_member_transition_strips_only_that_family() -> None:
    acts = [
        {"kind": "assertion", "payload": {"finding": {"fact_id": SHARED + "|tax-year=2025"}}},
        {
            "kind": "member-transition",
            "payload": {"family": {"id": LT}, "member": {"action": "assert"}},
        },
    ]
    assert stale_group_families(acts, [_group()]) == frozenset({LT})
    assert _admit("yes", acts=acts) == {ST}


def test_a_later_added_member_strips_only_that_family() -> None:
    acts = [
        {"kind": "assertion", "payload": {"finding": {"fact_id": SHARED + "|tax-year=2025"}}},
        {
            "kind": "member-transition",
            "payload": {"action": "assert", "family": {"id": LT}},
        },
    ]
    assert stale_group_families(acts, [_group()]) == frozenset({LT})
    assert _admit("yes", acts=acts) == {ST}


def test_a_later_answer_admits_the_family_again() -> None:
    acts = [
        {"kind": "assertion", "payload": {"finding": {"fact_id": SHARED + "|tax-year=2025"}}},
        {
            "kind": "member-transition",
            "payload": {"action": "assert", "family": {"id": LT}},
        },
        {"kind": "assertion", "payload": {"finding": {"fact_id": SHARED + "|tax-year=2025"}}},
    ]
    assert stale_group_families(acts, [_group()]) == frozenset()
    assert _admit("yes", acts=acts) == {LT, ST}


def test_yes_then_no_with_a_member_admits_only_the_empty_family() -> None:
    assert _admit("no", counts={LT: 1}) == {ST}


def test_a_removal_does_not_strip_the_answer() -> None:
    acts = [
        {"kind": "assertion", "payload": {"finding": {"fact_id": SHARED + "|tax-year=2025"}}},
        {
            "kind": "member-transition",
            "payload": {"action": "remove", "family": {"id": LT}},
        },
    ]
    assert _admit("yes", acts=acts) == {LT, ST}


def test_two_current_answers_admit_nothing() -> None:
    admitted = resolve_closure_admissions(
        [_group()],
        _declarations(),
        [_answer("yes"), ClosureFindingRecord("demo.ns.t1.answer-2", SHARED, "", "yes")],
        _horizons(),
    )
    assert admitted == {}


def test_other_values_admit_nothing() -> None:
    assert _admit("maybe") == set()


def test_v3_still_requires_boolean_true_on_its_horizon() -> None:
    mapping: dict[str, Any] = {
        "schema": "source-closure-mapping.v3",
        "id": "demo.ns.t1.mapping.covered-lt",
        "version": "v1",
        "family": {"id": "demo.ns.t1.covered-lt", "version": "v1"},
        "member_fact_type": "demo.ns.t1.covered-lt-txn",
        "closure_fact_type": "demo.ns.t1.covered-lt.source-closure",
        "admits_symbol": "demo.ns.t1.covered-lt.subtotal",
        "closure_horizon_key": "horizon",
    }
    declaration = _declaration("demo.ns.t1.covered-lt", "demo.ns.t1.covered-lt-txn")
    declaration["authorizes_subtotal"] = "demo.ns.t1.covered-lt.subtotal"
    horizons = {"demo.ns.t1.covered-lt": "demo.ns.t1.covered.h0"}
    true = ClosureFindingRecord("demo.ns.t1.covered.answer", mapping["closure_fact_type"], "demo.ns.t1.covered.h0", True)
    admitted = resolve_closure_admissions(
        [mapping], [declaration], [true], horizons, member_counts={LT: 4}, acts=[{"kind": "assertion"}],
    )
    assert set(admitted) == {"demo.ns.t1.covered-lt"}
    text = ClosureFindingRecord("demo.ns.t1.covered.answer", mapping["closure_fact_type"], "demo.ns.t1.covered.h0", "yes")
    assert resolve_closure_admissions([mapping], [declaration], [text], horizons) == {}


def test_the_shared_answer_is_recorded_once() -> None:
    state = FindingState(findings={
        "demo.ns.t1.answer": {
            "fact_id": SHARED + "|tax-year=2025",
            "value": "no",
        }
    })
    currency = CurrencyView(
        current_finding_ids=frozenset({"demo.ns.t1.answer"}),
        displaced_finding_ids=frozenset(),
        current_evidence_ids=frozenset(),
        displaced_evidence_ids=frozenset(),
    )
    second = dict(_group())
    second["id"] = "demo.ns.t1.mapping.noncovered.again"
    records, _horizons_out = marshal_closure_authority(state, currency, [_group(), second])
    assert [(record.fact_type, record.finding_id, record.horizon_id, record.value) for record in records] == [
        (SHARED, "demo.ns.t1.answer", "", "no"),
    ]


def test_member_counts_follow_the_listed_fact_type() -> None:
    counts = group_member_counts([_group()], [_source(LT_MEMBER), _source(LT_MEMBER), _source(ST_MEMBER)])
    assert counts == {LT: 2, ST: 1}


def test_covered_flag_no_drops_admission_and_names_the_token() -> None:
    mapping: dict[str, Any] = {
        "schema": "source-closure-mapping.v3",
        "id": "demo.ns.t1.mapping.covered-lt",
        "version": "v1",
        "family": {"id": "tax.us.2025.f1099b.covered-lt", "version": "v1"},
        "member_fact_type": "tax.us.2025.f1099b.covered-lt-txn",
        "closure_fact_type": "demo.ns.t1.covered-lt.source-closure",
        "admits_symbol": "demo.ns.t1.covered-lt.subtotal",
    }
    declaration = _declaration("tax.us.2025.f1099b.covered-lt", "tax.us.2025.f1099b.covered-lt-txn")
    declaration["authorizes_subtotal"] = "demo.ns.t1.covered-lt.subtotal"
    finding = ClosureFindingRecord("demo.ns.t1.covered.answer", mapping["closure_fact_type"], "h0", True)
    source = SimpleNamespace(
        name="tax.us.2025.f1099b.covered-lt-txn",
        value='{"basis_reported_to_irs": "no", "proceeds": "4100", "basis": "100"}',
    )
    objects = {"tax.us.2025.f1099b.covered-lt-txn": "tax.us.2025.f1099b.covered-lt"}
    refused = families_refused_for_unreported_basis([source], objects)
    assert refused == frozenset({"tax.us.2025.f1099b.covered-lt"})
    admitted = resolve_closure_admissions(
        [mapping],
        [declaration],
        [finding],
        {"tax.us.2025.f1099b.covered-lt": "h0"},
        refused_families=refused,
    )
    assert admitted == {}
    code, missing = covered_flag_block(
        "SOURCE_SET_UNCLOSED",
        ["tax.us.2025.f1099b.covered-lt", "tax.us.2025.schedule-d.line-15"],
        refused,
        COVERED_FLAG_REFUSAL_CODE,
    )
    assert code == "DEPENDENCY_INVALID"
    assert missing == [COVERED_FLAG_REFUSAL_CODE, "tax.us.2025.schedule-d.line-15"]


def test_a_reported_basis_does_not_refuse_the_family() -> None:
    source = SimpleNamespace(
        name="tax.us.2025.f1099b.covered-lt-txn",
        value={"basis_reported_to_irs": "yes"},
    )
    refused = families_refused_for_unreported_basis(
        [source],
        {"tax.us.2025.f1099b.covered-lt-txn": "tax.us.2025.f1099b.covered-lt"},
    )
    assert refused == frozenset()


def test_the_refusal_sentence_is_shown_and_a_constraint_meaning_fills_an_empty_reason() -> None:
    flag_row = {
        "disposition": "blocked",
        "code": "DEPENDENCY_INVALID",
        "missing": [COVERED_FLAG_REFUSAL_CODE],
    }
    reasons = _closure_question_reasons(
        flag_row,
        resolved_members=[],
        by_symbol={},
        refusal_sentence=COVERED_FLAG_REFUSAL_SENTENCE,
        refusal_token=COVERED_FLAG_REFUSAL_CODE,
    )
    assert reasons == [{"sentence": COVERED_FLAG_REFUSAL_SENTENCE}]

    line = {
        "disposition": "blocked",
        "code": "DEPENDENCY_ABSENT",
        "missing": ["demo.ns.t1.noncovered-lt-proceeds-subtotal"],
    }
    validation = {
        "disposition": "blocked",
        "code": "DEPENDENCY_INVALID",
        "missing": ["CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"],
    }
    subtotal = {
        "disposition": "blocked",
        "code": "DEPENDENCY_ABSENT",
        "missing": ["demo.ns.t1.noncovered-lt.member-validation"],
    }
    members = [{
        "schema": "source-family.v2",
        "member_constraints": [
            {"block_code": "CODE_W_ON_GAIN", "meaning": WASH},
            {"block_code": "ADJUSTMENT_EXCEEDS_LOSS", "meaning": "The disallowance is larger than the loss."},
        ],
    }]
    filled = _closure_question_reasons(
        line,
        resolved_members=members,
        by_symbol={
            "demo.ns.t1.noncovered-lt-proceeds-subtotal": [subtotal],
            "demo.ns.t1.noncovered-lt.member-validation": [validation],
        },
        constraint_meanings={
            "CODE_W_ON_GAIN": WASH,
            "ADJUSTMENT_EXCEEDS_LOSS": "The disallowance is larger than the loss.",
        },
    )
    assert [reason["sentence"] for reason in filled] == [
        WASH,
        "The disallowance is larger than the loss.",
    ]
    assert _closure_question_reasons(
        line,
        resolved_members=members,
        by_symbol={
            "demo.ns.t1.noncovered-lt-proceeds-subtotal": [subtotal],
            "demo.ns.t1.noncovered-lt.member-validation": [validation],
        },
    ) == []
