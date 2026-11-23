"""Grouped closure admission and the covered-flag refusal.

v4 records one yes/no finding for every family it lists. no admits a family
only while that family has no current member. yes admits it until a later
added member. A covered sale with basis_reported_to_irs no is refused only
when the caller passes that family. v3 admission is the boolean-true rule.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

from packages.derivation.marshal import marshal_closure_authority
from packages.derivation.presentation_projection import (
    _closure_question_reasons,
    _line9_mixed_blocker_explanation,
    build_presentation_model,
)
from packages.kernel.findings import FindingState
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


def test_stale_line9_keeps_its_closure_question_beside_the_amount_check_explanation() -> None:
    family = "tax.us.2025.f1099b.noncovered-lt"
    transaction_type = "tax.us.2025.f1099b.noncovered-lt-txn"
    member_validation = family + ".member-validation"
    amount_check = transaction_type + ".amounts-check"
    subtotals = (
        "tax.us.2025.f1099b.noncovered-lt-proceeds-subtotal",
        "tax.us.2025.f1099b.noncovered-lt-basis-subtotal",
        "tax.us.2025.f1099b.noncovered-lt-adjustment-subtotal",
    )
    question = "Did you sell any securities whose basis was not reported to the IRS?"
    explanation = (
        "Schedule D line 9, column (h), has no value yet. It waits for your answers about sales "
        "whose basis was not reported to the IRS, or for a recorded long-term sale of that kind "
        "to pass its checks."
    )
    field = {
        "binds_symbol": "tax.us.2025.schedule-d.line-9",
        "dispositions": {"blocked": {"explain": explanation}},
    }
    row = {
        "artifact_id": "tax.us.2025.rule.schedule-d-line9",
        "disposition": "blocked",
        "code": "DEPENDENCY_ABSENT",
        "missing": [*subtotals, amount_check],
    }
    amount_check_row = {
        "disposition": "blocked",
        "code": "DEPENDENCY_INVALID",
        "missing": [transaction_type + "|broker=demo-broker,statement=demo-statement,transaction=demo-late,tax-year=2025"],
    }
    by_symbol = {
        **{
            subtotal: [{"disposition": "blocked", "code": "DEPENDENCY_ABSENT", "missing": [member_validation]}]
            for subtotal in subtotals
        },
        member_validation: [{"disposition": "blocked", "code": "SOURCE_SET_UNCLOSED", "missing": [family]}],
        amount_check: [amount_check_row],
    }
    mapping = {
        "schema": "source-closure-mapping.v3",
        "closure_question": question,
        "family": {"id": family, "version": "v1"},
    }

    mixed_explanation = _line9_mixed_blocker_explanation(
        field, row, by_symbol, ("tax.us.2025.package.core-calculations", "v91"),
    )
    transaction_leaf = amount_check_row["missing"][0]
    assert mixed_explanation == (explanation, transaction_leaf)
    assert _line9_mixed_blocker_explanation(
        field, row, by_symbol, ("tax.us.2025.package.core-calculations", "v90"),
    ) is None
    for version in ("v91", "v99", "v100"):
        assert _line9_mixed_blocker_explanation(
            field, row, by_symbol, ("tax.us.2025.package.core-calculations", version),
        ) == (explanation, transaction_leaf)
    assert _line9_mixed_blocker_explanation(
        field, row, by_symbol, ("demo.other.package", "v100"),
    ) is None
    assert _closure_question_reasons(
        row, resolved_members=[mapping], by_symbol=by_symbol, later_any_arm_refs=True,
    ) == []
    assert _closure_question_reasons(
        row,
        resolved_members=[mapping],
        by_symbol=by_symbol,
        later_any_arm_refs=True,
        partial_family=family,
        partial_leaf=transaction_leaf,
        partial_explanation=mixed_explanation[0],
    ) == [{"sentence": question}, {"sentence": explanation}]

    # Another reached blocker with no usable missing list cannot be hidden by
    # the valid closure path and known transaction-amount leaf.
    incomplete_sibling = "tax.us.2025.unclassified-blocker"
    row_with_incomplete_sibling = {**row, "missing": [*row["missing"], incomplete_sibling]}
    for incomplete in (
        {"disposition": "blocked", "code": "DEPENDENCY_INVALID"},
        {"disposition": "blocked", "code": "DEPENDENCY_INVALID", "missing": []},
    ):
        assert _closure_question_reasons(
            row_with_incomplete_sibling,
            resolved_members=[mapping],
            by_symbol={**by_symbol, incomplete_sibling: [incomplete]},
            later_any_arm_refs=True,
            partial_family=family,
            partial_leaf=transaction_leaf,
            partial_explanation=explanation,
        ) == []

    # A dependency cycle is also an unresolved shape, even if a sibling path
    # has already established the declared closure question.
    cycle_a = "tax.us.2025.unclassified-cycle-a"
    cycle_b = "tax.us.2025.unclassified-cycle-b"
    row_with_cycle = {**row, "missing": [*row["missing"], cycle_a]}
    cycle_rows = {
        cycle_a: [{"disposition": "blocked", "code": "DEPENDENCY_ABSENT", "missing": [cycle_b]}],
        cycle_b: [{"disposition": "blocked", "code": "DEPENDENCY_ABSENT", "missing": [cycle_a]}],
    }
    assert _closure_question_reasons(
        row_with_cycle,
        resolved_members=[mapping],
        by_symbol={**by_symbol, **cycle_rows},
        later_any_arm_refs=True,
        partial_family=family,
        partial_leaf=transaction_leaf,
        partial_explanation=explanation,
    ) == []

    wrong_field = {**field, "binds_symbol": "tax.us.2025.form1040.line-9"}
    assert _line9_mixed_blocker_explanation(
        wrong_field, row, by_symbol, ("tax.us.2025.package.core-calculations", "v91"),
    ) is None
    wrong_fact = {
        **by_symbol,
        amount_check: [{**amount_check_row, "missing": ["tax.us.2025.other-sale-txn|broker=demo-broker"]}],
    }
    assert _line9_mixed_blocker_explanation(
        field, row, wrong_fact, ("tax.us.2025.package.core-calculations", "v91"),
    ) is None
    second_transaction_leaf = transaction_type + "|broker=demo-other,statement=demo-statement,transaction=demo-second,tax-year=2025"
    multiple_transaction_facts = {
        **by_symbol,
        amount_check: [{**amount_check_row, "missing": [transaction_leaf, second_transaction_leaf]}],
    }
    assert _line9_mixed_blocker_explanation(
        field, row, multiple_transaction_facts,
        ("tax.us.2025.package.core-calculations", "v91"),
    ) is None
    assert _closure_question_reasons(
        row,
        resolved_members=[mapping],
        by_symbol=multiple_transaction_facts,
        later_any_arm_refs=True,
        partial_family=family,
        partial_leaf=transaction_leaf,
        partial_explanation=explanation,
    ) == []

    unanswered = {**row, "missing": list(subtotals)}
    assert _line9_mixed_blocker_explanation(
        field, unanswered, by_symbol, ("tax.us.2025.package.core-calculations", "v91"),
    ) is None
    assert _closure_question_reasons(
        unanswered, resolved_members=[mapping], by_symbol=by_symbol, later_any_arm_refs=True,
    ) == [{"sentence": question}]


def test_stale_line9_projection_uses_adopted_core_version_for_mixed_reason() -> None:
    family = "tax.us.2025.f1099b.noncovered-lt"
    transaction_type = "tax.us.2025.f1099b.noncovered-lt-txn"
    member_validation = family + ".member-validation"
    amount_check = transaction_type + ".amounts-check"
    subtotals = (
        "tax.us.2025.f1099b.noncovered-lt-proceeds-subtotal",
        "tax.us.2025.f1099b.noncovered-lt-basis-subtotal",
        "tax.us.2025.f1099b.noncovered-lt-adjustment-subtotal",
    )
    question = "Did you sell any securities whose basis was not reported to the IRS?"
    explanation = (
        "Schedule D line 9, column (h), has no value yet. It waits for your answers about sales "
        "whose basis was not reported to the IRS, or for a recorded long-term sale of that kind "
        "to pass its checks."
    )
    line9 = "tax.us.2025.schedule-d.line-9"
    rule_id = "tax.us.2025.rule.schedule-d-line9"
    transaction_leaf = transaction_type + "|broker=demo-broker,statement=demo-statement,transaction=demo-late,tax-year=2025"
    field = {
        "schema": "form-field.v3",
        "id": line9,
        "version": "v1",
        "form": {"authority": "IRS", "form_id": "1040-SCH-D", "tax_year": 2025, "jurisdiction": "US-federal"},
        "line": "9-h",
        "label": "Line 9 column (h)",
        "description": "Schedule D (2025) line 9 column (h).",
        "binds_symbol": line9,
        "citation": {"id": "tax.us.2025.citation.schedule-d.line-9", "version": "v1"},
        "dispositions": {"blocked": {"render": "", "explain": explanation, "codes": ["DEPENDENCY_ABSENT"]}},
    }
    rule = {
        "schema": "rule-artifact.v15",
        "id": rule_id,
        "version": "v3",
        "publishes": line9,
        "requires": [*subtotals, amount_check],
    }
    root = {
        "artifact_id": rule_id,
        "symbol": line9,
        "disposition": "blocked",
        "code": "DEPENDENCY_ABSENT",
        "missing": [*subtotals, amount_check],
    }
    subtotal_rows = [
        {
            "artifact_id": f"tax.us.2025.rule.demo-subtotal-{index}",
            "symbol": subtotal,
            "disposition": "blocked",
            "code": "DEPENDENCY_ABSENT",
            "missing": [member_validation],
        }
        for index, subtotal in enumerate(subtotals)
    ]
    validation = {
        "artifact_id": member_validation + ".synthesized",
        "symbol": member_validation,
        "disposition": "blocked",
        "code": "SOURCE_SET_UNCLOSED",
        "missing": [family],
    }
    amount_row = {
        "artifact_id": amount_check,
        "symbol": amount_check,
        "disposition": "blocked",
        "code": "DEPENDENCY_INVALID",
        "missing": [transaction_leaf],
    }
    mapping = {
        "schema": "source-closure-mapping.v3",
        "id": "tax.us.2025.closure-mapping.demo-noncovered-lt",
        "version": "v1",
        "closure_question": question,
        "family": {"id": family, "version": "v1"},
    }
    members: list[dict[str, Any]] = [field, rule, mapping]
    dispositions: list[dict[str, Any]] = [root, *subtotal_rows, validation, amount_row]

    def projected(version: str) -> list[dict[str, Any]]:
        model = build_presentation_model(
            run_id="demo.run.track1.line9",
            resolved_members=members,
            state=FindingState(),
            publications=[],
            dispositions=dispositions,
            adopted_package=("tax.us.2025.package.core-calculations", version),
        )
        return cast(list[dict[str, Any]], model["sections"][0]["resolved"].get("reasons", []))

    assert projected("v90") == []
    assert projected("v91") == [{"sentence": question}, {"sentence": explanation}]
    assert projected("v99") == [{"sentence": question}, {"sentence": explanation}]
