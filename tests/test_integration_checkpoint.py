"""Integration checkpoint: six seams compose on one real run.

Synthetic in-repo fixtures only. Ordinary facts enter through Seam 6's
``contribute_ordinary_acquisition`` (the real contribution/admission
boundary). Documentary box-1 facts use the production Form 1099-INT fact
type. Evaluation goes through ``runner.run`` / ``_execute`` — the same
saturation loop ``execute_marshaled`` uses — so identity association,
supportability, both pairing-scoped consequences, and the line-2b
successor aggregator are the production modules, not a test-only harness.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from typing import Any

from packages.derivation.authorization import (
    STATUS_ADMITTED,
    STATUS_SUSPENDED,
    AuthorizationResolution,
)
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_run_context
from packages.derivation.runner import InputFinding, RunResult, run
from packages.derivation.source_authority import ClosureFindingRecord
from packages.kernel.currency import CurrencyView
from packages.kernel.findings import project
from packages.tax.identity_association import (
    ACQUISITION_FACT_TYPE,
    ASSOCIATION_AMBIGUOUS,
    ASSOCIATION_SYMBOL,
    REPORT_FACT_TYPE,
)
from packages.tax.obligation_acquisition_mapping import (
    ORDINARY_QUESTIONS,
    OrdinaryInputError,
    build_obligation_acquisition_bundle,
    build_ordinary_acquisition_entity_acts,
    contribute_ordinary_acquisition,
    validate_ordinary_answers,
)
from packages.tax.pairing_consequences import (
    BASIS_RULE_ID,
    BASIS_SYMBOL_PREFIX,
    CURRENT_YEAR_RULE_ID,
    CURRENT_YEAR_SUBTOTAL_RULE_ID,
    CURRENT_YEAR_SUBTOTAL_SYMBOL,
    CURRENT_YEAR_SYMBOL_PREFIX,
    PAIRING_TYPE,
    SUPPORTABILITY_TYPE,
)
from packages.tax.supportability import (
    ACCRUED_EXCEEDS_ASSOCIATED_REPORT,
    RULE_ID as SUPPORTABILITY_RULE_ID,
    SUPPORTABILITY_SYMBOL,
    load_rule as load_supportability_rule,
)
from tests.support import act, demo_evidence, registry_with_demo_kinds

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"

ADOPTION_PIN = {
    "role": "adoption",
    "id": "demo.package.integration-checkpoint",
    "version": "v1",
}
GOVERNANCE = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]

_FAMILY_FILES = (
    "family.f1099int-b1.json",
    "family.f1099int-b3.json",
    "family.f1099oid-b1.json",
    "family.non-form-interest.json",
    "family.form1065-k1-box5.json",
    "family.f1099int-b10.json",
    "family.f1099oid-b5.json",
    "family.scheduleb-adjustment.nominee.json",
    "family.scheduleb-adjustment.accrued-interest.json",
    "family.scheduleb-adjustment.abp-adjustment.json",
)
_MAPPING_FILES = (
    "closure-mapping.f1099int-b1.json",
    "closure-mapping.f1099int-b3.json",
    "closure-mapping.f1099oid-b1.json",
    "closure-mapping.non-form-interest.json",
    "closure-mapping.form1065-k1-box5.json",
    "closure-mapping.f1099int-b10.json",
    "closure-mapping.f1099oid-b5.json",
    "closure-mapping.scheduleb-adjustment.nominee.json",
    "closure-mapping.scheduleb-adjustment.accrued-interest.json",
    "closure-mapping.scheduleb-adjustment.abp-adjustment.json",
)
_SUBTOTAL_RULE_FILES = (
    "rule.f1099int-b1-subtotal.json",
    "rule.f1099int-b3-subtotal.json",
    "rule.f1099oid-subtotal.json",
    "rule.non-form-interest-subtotal.json",
    "rule.form1065-k1-box5-subtotal.json",
    "rule.f1099int-b10-subtotal.json",
    "rule.f1099oid-b5-subtotal.json",
    "rule.scheduleb-adjustment.nominee-subtotal.json",
    "rule.scheduleb-adjustment.accrued-interest-subtotal.json",
    "rule.scheduleb-adjustment.abp-adjustment-subtotal.json",
)


def _load(path: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return loaded


def _content(name: str) -> dict[str, Any]:
    return _load(CONTENT / name)


def _answers(**overrides: Any) -> dict[str, Any]:
    answers = {
        "payer_name": "demo.payer.bank-a",
        "obligation_description": "synthetic municipal bond series demo-2025",
        "obligation_reference": "DEMO-BOND-T2",
        "acquisition_date": "2025-03-14",
        "accrued_interest_paid_to_seller": 42.0,
        "currency": "USD",
        # A single same-payer/year
        # report is never silently associated. These fixtures are not
        # testing the confirmation semantics itself (see the dedicated
        # T5/T8 cases below), so they carry the explicit user confirmation
        # a real interaction would have collected.
        "confirmed_report_match": True,
    }
    answers.update(overrides)
    return answers


def _report(
    *,
    statement: str = "demo.1099int-statement.t2",
    amount: float = 500.0,
    finding_id: str = "demo.finding.box1.t2",
) -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": (
            f"{REPORT_FACT_TYPE}|payer=demo.payer.bank-a,"
            f"statement={statement},tax-year=2025"
        ),
        "value": amount,
        "basis": "documentary",
        "evidence_ids": [f"demo.evidence.{finding_id}"],
    }


def _box8(*, finding_id: str = "demo.finding.box8.t9") -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": (
            "tax.us.2025.f1099int.box8-tax-exempt-interest|"
            "payer=demo.payer.bank-a,"
            "statement=demo.1099int-statement.t9,tax-year=2025"
        ),
        "value": 75.0,
        "basis": "documentary",
        "evidence_ids": [f"demo.evidence.{finding_id}"],
    }


def _rounding() -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": "demo.finding.rounding",
        "fact_id": "rounding.convention|tax-year=2025",
        "value": "half_up",
        "basis": "attested",
        "evidence_ids": [],
    }


def _currency(finding_ids: list[str]) -> CurrencyView:
    ids = frozenset(finding_ids)
    return CurrencyView(
        current_finding_ids=ids,
        displaced_finding_ids=frozenset(),
        current_evidence_ids=frozenset(),
        displaced_evidence_ids=frozenset(),
    )


class _HorizonState:
    def __init__(self) -> None:
        self.current_by_chain: dict[tuple[str, str, str], str] = {}


class _State:
    def __init__(self, findings: dict[str, dict[str, Any]]) -> None:
        self.findings = findings
        self.horizon_state = _HorizonState()


def _seam_rules() -> list[dict[str, Any]]:
    return [
        load_supportability_rule(),
        _content("rule.interest.current-year-adjustment.pairing-scoped.json"),
        _content("rule.basis.item-level-consequence.pairing-scoped.json"),
        _content("rule.interest.current-year-adjustment.aggregate-supportability.json"),
        _content("rule.interest.current-year-adjustment-subtotal.json"),
    ]


def _collect_names() -> list[str]:
    return [
        ACQUISITION_FACT_TYPE,
        REPORT_FACT_TYPE,
        ASSOCIATION_SYMBOL,
        SUPPORTABILITY_TYPE,
        CURRENT_YEAR_SYMBOL_PREFIX,
        "tax.us.2025.f1099int.box1-interest",
        "tax.us.2025.f1099int.box3-interest",
        "tax.us.2025.f1099oid.box1-interest-oid",
        "tax.us.2025.non-form-interest.amount",
        "tax.us.2025.form1065-k1.box5-interest",
        "tax.us.2025.f1099int.box10-market-discount",
        "tax.us.2025.f1099oid.box5-market-discount",
        "tax.us.2025.scheduleb.adjustment.nominee.amount",
        "tax.us.2025.scheduleb.adjustment.accrued-interest.amount",
        "tax.us.2025.scheduleb.adjustment.abp-adjustment.amount",
    ]


# A ``confirmed_report_match: true`` confirmation always requires a named
# ``confirmed_report_fact_id``, uniformly at both tiers. Every test below
# that leaves the default ``_answers()`` confirmation in place pairs it, by
# default, with ``_report()``'s own default fact id — the single report id
# nearly every T1-T9 fixture actually associates with. A test that
# genuinely exercises the statement-narrowed tier against a *different*
# report must override this default explicitly (see
# ``_findings_for``/``_admit_acquisition``'s own ``confirmed_report_fact_id``
# parameter) — this value is only ever inert for ambiguous/no-candidate
# scenarios, which never reach the target check at all.
_DEFAULT_CONFIRMED_REPORT_FACT_ID = (
    f"{REPORT_FACT_TYPE}|payer=demo.payer.bank-a,"
    "statement=demo.1099int-statement.t2,tax-year=2025"
)


def _admit_acquisition(
    answers: dict[str, Any],
    *,
    finding_id: str,
    confirmed_report_fact_id: str | None = _DEFAULT_CONFIRMED_REPORT_FACT_ID,
) -> dict[str, Any]:
    tmp = tempfile.TemporaryDirectory()
    try:
        registry = registry_with_demo_kinds(Path(tmp.name))
        bundle = build_obligation_acquisition_bundle(answers)
        opening = [
            act(0, "bundle-adoption", {"bundle": bundle}),
            act(
                1,
                "evidence-submitted",
                {
                    "evidence": demo_evidence(
                        "demo.evidence.acq",
                        "Synthetic ordinary-language acquisition interview",
                        {"mode": "ordinary-language-entry", "synthetic": True},
                    )
                },
            ),
        ]
        opening.extend(build_ordinary_acquisition_entity_acts(answers, act_index=2))
        base = project(tuple(opening), registry)
        result = contribute_ordinary_acquisition(
            base,
            answers,
            registry=registry,
            record_id="demo.crec.acq",
            act_index=4,
            contribution_id="demo.contribution.acq",
            evidence_id="demo.evidence.acq",
            finding_id=finding_id,
            confirmed_report_fact_id=confirmed_report_fact_id,
            committed_against=4,
        )
        return result.state.findings[finding_id]
    finally:
        tmp.cleanup()


def _findings_for(
    *,
    answers: dict[str, Any] | None,
    reports: list[dict[str, Any]],
    extra: list[dict[str, Any]] | None = None,
    acquisition_id: str = "demo.finding.acq.t2",
    confirmed_report_fact_id: str | None = _DEFAULT_CONFIRMED_REPORT_FACT_ID,
) -> dict[str, dict[str, Any]]:
    findings: dict[str, dict[str, Any]] = {_rounding()["id"]: _rounding()}
    if answers is not None:
        acq = _admit_acquisition(
            answers,
            finding_id=acquisition_id,
            confirmed_report_fact_id=confirmed_report_fact_id,
        )
        findings[acq["id"]] = acq
    for report in reports:
        findings[report["id"]] = report
    for item in extra or ():
        findings[item["id"]] = item
    return findings


def _run(
    findings: dict[str, dict[str, Any]],
    *,
    rules: list[dict[str, Any]] | None = None,
    authorization: AuthorizationResolution | None = None,
    with_line2b: bool = False,
    reporting_year: int | None = 2025,
) -> RunResult:
    chosen = list(rules if rules is not None else _seam_rules())
    families = [_content(name) for name in _FAMILY_FILES] if with_line2b else []
    mappings = [_content(name) for name in _MAPPING_FILES] if with_line2b else []
    if with_line2b:
        chosen.extend(_content(name) for name in _SUBTOTAL_RULE_FILES)
        chosen.append(_content("rule.form1040-line2b.v5.json"))
    closures: list[ClosureFindingRecord] = []
    horizons: dict[str, str] = {}
    if with_line2b:
        for mapping in mappings:
            family_id = mapping["family"]["id"]
            horizon = f"demo.h.{family_id}"
            horizons[family_id] = horizon
            closure_type = mapping["closure_fact_type"]["id"]
            closures.append(
                ClosureFindingRecord(
                    finding_id=f"demo.closure.{family_id}",
                    fact_type=closure_type,
                    horizon_id=horizon,
                    value=True,
                )
            )
    ctx = marshal_run_context(
        run_id="demo.run.integration-checkpoint",
        state=_State(findings),  # type: ignore[arg-type]
        currency=_currency(list(findings)),
        rules=chosen,
        parameters={},
        canon=load_canon(DerivationSchemas()) if with_line2b else {},
        adoption_pin=ADOPTION_PIN,
        governance_pins=list(GOVERNANCE),
        collect_source_names=_collect_names(),
        family_declarations=families,
        closure_mappings=mappings,
        authorization=authorization,
        reporting_year=reporting_year,
    )
    if with_line2b:
        ctx = replace(ctx, closure_findings=closures, current_horizons=horizons)
        extra_inputs = [
            inp for inp in ctx.inputs if inp.symbol == "rounding.convention"
        ]
        if not extra_inputs:
            ctx = replace(
                ctx,
                inputs=list(ctx.inputs)
                + [
                    InputFinding(
                        "rounding.convention", "half_up", "demo.finding.rounding", "input"
                    )
                ],
            )
    return run(ctx, DerivationSchemas())


def _pubs_by_prefix(result: Any, prefix: str) -> list[dict[str, Any]]:
    return [
        pub.finding
        for pub in result.publications
        if str(pub.finding.get("symbol", "")).startswith(prefix)
    ]


def _pairing_values(result: Any) -> list[dict[str, Any]]:
    return [finding["value"] for finding in _pubs_by_prefix(result, ASSOCIATION_SYMBOL)]


class TestT1ThroughT9(unittest.TestCase):
    def test_t1_fully_includible_report_survives_without_adjustment(self) -> None:
        report = _report()
        result = _run(_findings_for(answers=None, reports=[report]))
        self.assertEqual(_pairing_values(result), [])
        self.assertEqual(_pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|"), [])
        self.assertEqual(_pubs_by_prefix(result, BASIS_SYMBOL_PREFIX + "|"), [])
        self.assertFalse(
            any(row.get("code") == ASSOCIATION_AMBIGUOUS for row in result.blocked)
        )

    def test_t2_accrued_treatment_publishes_both_consequences(self) -> None:
        report = _report()
        result = _run(_findings_for(answers=_answers(), reports=[report]))
        pairings = _pairing_values(result)
        self.assertEqual(len(pairings), 1)
        self.assertEqual(pairings[0]["right_fact_id"], report["fact_id"])
        cy = _pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|")
        basis = _pubs_by_prefix(result, BASIS_SYMBOL_PREFIX + "|")
        self.assertEqual(len(cy), 1)
        self.assertEqual(len(basis), 1)
        self.assertEqual(cy[0]["value"], "42.0")
        self.assertEqual(basis[0]["value"], "42.0")
        self.assertNotEqual(cy[0]["id"], basis[0]["id"])
        support = _pubs_by_prefix(result, SUPPORTABILITY_SYMBOL + "|")
        self.assertEqual(len(support), 1)
        self.assertIs(support[0]["value"], True)

    def test_t3_missing_ordinary_answer_is_named_and_not_defaulted(self) -> None:
        incomplete = _answers()
        del incomplete["accrued_interest_paid_to_seller"]
        with self.assertRaises(OrdinaryInputError) as caught:
            validate_ordinary_answers(incomplete)
        self.assertIn("accrued_interest_paid_to_seller", str(caught.exception))
        question_fields = {field for field, _prompt in ORDINARY_QUESTIONS}
        self.assertIn("accrued_interest_paid_to_seller", question_fields)
        result = _run(_findings_for(answers=None, reports=[_report()]))
        self.assertEqual(_pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|"), [])

    def test_t4_ordinary_fact_without_report_invents_no_return_contribution(self) -> None:
        result = _run(_findings_for(answers=_answers(), reports=[]))
        self.assertEqual(_pairing_values(result), [])
        self.assertEqual(_pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|"), [])
        self.assertEqual(_pubs_by_prefix(result, BASIS_SYMBOL_PREFIX + "|"), [])

    def test_t5_ambiguous_association_refuses_silently_matching(self) -> None:
        r1 = _report(statement="demo.1099int-statement.t5a", finding_id="demo.finding.box1.t5a")
        r2 = _report(
            statement="demo.1099int-statement.t5b",
            finding_id="demo.finding.box1.t5b",
            amount=600.0,
        )
        result = _run(_findings_for(answers=_answers(), reports=[r1, r2]))
        self.assertEqual(_pairing_values(result), [])
        self.assertTrue(
            any(row.get("code") == ASSOCIATION_AMBIGUOUS for row in result.blocked)
        )
        self.assertEqual(_pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|"), [])

    def test_t6_document_correction_displaces_dependents_not_association(self) -> None:
        answers = _answers()
        original = _report(amount=500.0, finding_id="demo.finding.box1.t6a")
        before = _run(_findings_for(answers=answers, reports=[original]))
        corrected = _report(amount=400.0, finding_id="demo.finding.box1.t6b")
        after = _run(_findings_for(answers=answers, reports=[corrected]))
        self.assertEqual(
            _pairing_values(before)[0]["left_fact_id"],
            _pairing_values(after)[0]["left_fact_id"],
        )
        self.assertEqual(
            _pairing_values(before)[0]["right_fact_id"],
            _pairing_values(after)[0]["right_fact_id"],
        )
        self.assertNotEqual(
            _pubs_by_prefix(before, SUPPORTABILITY_SYMBOL + "|")[0]["id"],
            _pubs_by_prefix(after, SUPPORTABILITY_SYMBOL + "|")[0]["id"],
        )
        self.assertNotEqual(
            _pubs_by_prefix(before, CURRENT_YEAR_SYMBOL_PREFIX + "|")[0]["id"],
            _pubs_by_prefix(after, CURRENT_YEAR_SYMBOL_PREFIX + "|")[0]["id"],
        )
        self.assertEqual(
            _pubs_by_prefix(after, CURRENT_YEAR_SYMBOL_PREFIX + "|")[0]["value"], "42.0"
        )

    def test_t7_circumstance_correction_changes_tax_not_the_report(self) -> None:
        report = _report()
        before = _run(_findings_for(answers=_answers(), reports=[report]))
        after = _run(
            _findings_for(
                answers=_answers(accrued_interest_paid_to_seller=18.0),
                reports=[report],
            )
        )
        self.assertEqual(_pairing_values(before)[0]["right_fact_id"], report["fact_id"])
        self.assertEqual(_pairing_values(after)[0]["right_fact_id"], report["fact_id"])
        self.assertEqual(
            _pubs_by_prefix(before, CURRENT_YEAR_SYMBOL_PREFIX + "|")[0]["value"], "42.0"
        )
        self.assertEqual(
            _pubs_by_prefix(after, CURRENT_YEAR_SYMBOL_PREFIX + "|")[0]["value"], "18.0"
        )

    def test_t8_same_payer_two_reports_surface_as_association_ambiguous(self) -> None:
        """ADR-0068 Decision 3: join is payer+year; statement-level selection is not closed."""
        a1 = _answers(obligation_reference="DEMO-BOND-T8A")
        r1 = _report(statement="demo.1099int-statement.t8a", finding_id="demo.finding.box1.t8a")
        r2 = _report(
            statement="demo.1099int-statement.t8b",
            finding_id="demo.finding.box1.t8b",
            amount=300.0,
        )
        findings = _findings_for(
            answers=a1, reports=[r1, r2], acquisition_id="demo.finding.acq.t8a"
        )
        second = _admit_acquisition(
            _answers(obligation_reference="DEMO-BOND-T8B", accrued_interest_paid_to_seller=10.0),
            finding_id="demo.finding.acq.t8b",
        )
        findings[second["id"]] = second
        result = _run(findings)
        self.assertEqual(_pairing_values(result), [])
        self.assertGreaterEqual(
            sum(1 for row in result.blocked if row.get("code") == ASSOCIATION_AMBIGUOUS),
            1,
        )

    def test_t8_statement_reference_selects_the_specific_report(self) -> None:
        """Genuine item selection among two candidate reports.

        Two real, distinct ``tax.us.1099int-statement`` entities from the
        same payer/year. The acquisition names a reported statement
        reference resolving to exactly one of them, *and* confirms the
        match: a statement reference alone only narrows which report is a
        candidate — a statement
        can aggregate several obligations, so the match alone is not
        evidence of *obligation* correspondence. The person's own
        ``confirmed_report_match`` attestation is what the
        mechanism actually associates on; it selects that specific report
        — not a refusal — and publishes the adjustment computed against
        its amount, not the other statement's.
        """
        from packages.tax.obligation_acquisition_mapping import (
            derive_reported_statement_entity_id,
        )

        statement_c = derive_reported_statement_entity_id(
            payer_name="demo.payer.bank-a",
            reported_statement_reference="ACCOUNT-REF-T8C",
        )
        assert statement_c is not None
        r1 = _report(
            statement=statement_c,
            finding_id="demo.finding.box1.t8c",
            amount=250.0,
        )
        r2 = _report(
            statement="demo.1099int-statement.t8d",
            finding_id="demo.finding.box1.t8d",
            amount=900.0,
        )
        a1 = _answers(
            obligation_reference="DEMO-BOND-T8C",
            reported_statement_reference="ACCOUNT-REF-T8C",
            confirmed_report_match=True,
        )
        result = _run(
            _findings_for(
                answers=a1,
                reports=[r1, r2],
                acquisition_id="demo.finding.acq.t8c",
                confirmed_report_fact_id=r1["fact_id"],
            )
        )
        pairings = _pairing_values(result)
        self.assertEqual(len(pairings), 1)
        self.assertEqual(pairings[0]["right_fact_id"], r1["fact_id"])
        cy = _pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|")
        self.assertEqual(len(cy), 1)
        self.assertEqual(cy[0]["value"], "42.0")
        self.assertFalse(
            any(row.get("code") == ASSOCIATION_AMBIGUOUS for row in result.blocked)
        )
        self.assertFalse(
            any(row.get("code") == "ASSOCIATION_UNCONFIRMED" for row in result.blocked)
        )

    def test_t1_unconfirmed_coarse_candidate_refuses(self) -> None:
        """An unconfirmed coarse-tier candidate must never auto-associate.

        An acquisition referencing ``DEMO-BOND-NOT-REPRESENTED-BY-REPORT``
        (no statement reference, no confirmation) against one same-payer/
        year report with a *different* statement identity must refuse
        ``ASSOCIATION_UNCONFIRMED`` and
        publish neither a pairing nor an adjustment.
        """
        a1 = _answers(
            obligation_reference="DEMO-BOND-NOT-REPRESENTED-BY-REPORT",
            confirmed_report_match=False,
        )
        report = _report(
            statement="demo.1099int-statement.unrelated-to-t1-adversary",
            finding_id="demo.finding.box1.t1-adversary",
        )
        result = _run(
            _findings_for(
                answers=a1, reports=[report], acquisition_id="demo.finding.acq.t1-adversary"
            )
        )
        self.assertEqual(_pairing_values(result), [])
        self.assertEqual(_pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|"), [])
        self.assertEqual(_pubs_by_prefix(result, BASIS_SYMBOL_PREFIX + "|"), [])
        self.assertTrue(
            any(row.get("code") == "ASSOCIATION_UNCONFIRMED" for row in result.blocked)
        )

    def test_t9_unsupported_neighbor_is_not_silently_translated(self) -> None:
        result = _run(
            _findings_for(answers=_answers(), reports=[], extra=[_box8()])
        )
        self.assertEqual(_pairing_values(result), [])
        self.assertEqual(_pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|"), [])
        self.assertFalse(
            any(
                "box8" in str(pub.finding.get("symbol", ""))
                for pub in result.publications
            )
        )


class TestCrossSeamClaims(unittest.TestCase):
    def test_document_correction_displaces_dependents_not_unrelated(self) -> None:
        answers = _answers()
        original = _report(amount=500.0)
        before = _run(_findings_for(answers=answers, reports=[original]))
        too_small = _report(amount=10.0, finding_id="demo.finding.box1.corrected")
        after = _run(_findings_for(answers=answers, reports=[too_small]))
        self.assertEqual(_pairing_values(before)[0]["left_fact_id"], _pairing_values(after)[0]["left_fact_id"])
        self.assertEqual(_pubs_by_prefix(before, CURRENT_YEAR_SYMBOL_PREFIX + "|")[0]["value"], "42.0")
        self.assertEqual(_pubs_by_prefix(after, CURRENT_YEAR_SYMBOL_PREFIX + "|"), [])
        self.assertTrue(
            any(row.get("code") == ACCRUED_EXCEEDS_ASSOCIATED_REPORT for row in after.blocked)
        )
        self.assertFalse(
            any(row.get("code") == ASSOCIATION_AMBIGUOUS for row in after.blocked)
        )

    def test_acquisition_correction_displaces_dependents_not_the_report(self) -> None:
        report = _report()
        before = _run(_findings_for(answers=_answers(), reports=[report]))
        after = _run(
            _findings_for(
                answers=_answers(accrued_interest_paid_to_seller=600.0),
                reports=[report],
            )
        )
        self.assertEqual(_pairing_values(after)[0]["right_fact_id"], report["fact_id"])
        self.assertEqual(_pubs_by_prefix(before, BASIS_SYMBOL_PREFIX + "|")[0]["value"], "42.0")
        self.assertEqual(_pubs_by_prefix(after, BASIS_SYMBOL_PREFIX + "|"), [])
        self.assertTrue(
            any(row.get("code") == ACCRUED_EXCEEDS_ASSOCIATED_REPORT for row in after.blocked)
        )

    def test_suspended_authorization_does_not_change_tax_semantics(self) -> None:
        findings = _findings_for(answers=_answers(), reports=[_report()])
        admitted = _run(
            findings,
            authorization=AuthorizationResolution(STATUS_ADMITTED, "demo.auth.g1"),
        )
        suspended = _run(
            findings,
            authorization=AuthorizationResolution(STATUS_SUSPENDED, "demo.auth.g1"),
        )
        self.assertTrue(admitted.current)
        self.assertFalse(suspended.current)
        self.assertEqual(admitted.authorization_status, STATUS_ADMITTED)
        self.assertEqual(suspended.authorization_status, STATUS_SUSPENDED)
        tax_admitted = [
            (pub.finding["symbol"], pub.finding["value"])
            for pub in admitted.publications
        ]
        tax_suspended = [
            (pub.finding["symbol"], pub.finding["value"])
            for pub in suspended.publications
        ]
        self.assertEqual(tax_admitted, tax_suspended)
        self.assertEqual(admitted.blocked, suspended.blocked)

    def test_seam5_reads_real_pairing_supportability_and_field_ref_interfaces(self) -> None:
        result = _run(_findings_for(answers=_answers(), reports=[_report()]))
        support = _pubs_by_prefix(result, SUPPORTABILITY_SYMBOL + "|")[0]
        cy = _pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|")[0]
        pairing = _pubs_by_prefix(result, ASSOCIATION_SYMBOL + "|")[0]
        pin_ids = {pin["id"] for pin in cy["pins"]}
        self.assertIn(pairing["id"], pin_ids)
        self.assertIn(support["id"], pin_ids)
        self.assertIn(CURRENT_YEAR_RULE_ID, pin_ids)
        self.assertIs(support["value"], True)
        self.assertEqual(cy["value"], "42.0")
        # Seam 1: the adopted supportability citizen is the field-ref rule.
        rule = load_supportability_rule()
        self.assertEqual(rule["id"], SUPPORTABILITY_RULE_ID)
        self.assertEqual(rule["value"]["when"]["left"]["op"], "ref")
        self.assertEqual(
            rule["value"]["when"]["left"]["field"], "accrued_interest_paid_to_seller"
        )
        self.assertEqual(rule["value"]["when"]["left"]["name"], ACQUISITION_FACT_TYPE)


class TestAggregateSupportabilityAcrossASharedReport(unittest.TestCase):
    """Aggregate supportability, live pipeline.

    A matching statement
    only narrows *which* report an acquisition's attestation targets, so
    both acquisitions here also confirm the match explicitly
    (``confirmed_report_match: True``) — one report of 500, two
    acquisitions of 300 each genuinely associated to it via a shared
    reported-statement reference plus an explicit confirmation, one
    unrelated report of 200. The per-pairing check alone would let box-1
    subtotal 700, adjustment subtotal 600, taxable total 100, through with
    no block. The
    aggregate check must catch the combined 600 claim against the 500
    report and the run must not silently reach 100.
    """

    def test_shared_statement_two_acquisitions_exceed_the_report(self) -> None:
        from packages.tax.obligation_acquisition_mapping import (
            derive_reported_statement_entity_id,
        )
        from packages.tax.pairing_consequences import (
            AGGREGATE_ACCRUED_EXCEEDS_REPORT,
            AGGREGATE_SUPPORTABILITY_RULE_ID,
        )

        statement = derive_reported_statement_entity_id(
            payer_name="demo.payer.bank-a",
            reported_statement_reference="ACCOUNT-REF-AGG",
        )
        assert statement is not None
        report_main = _report(
            statement=statement, finding_id="demo.finding.box1.agg-main", amount=500.0
        )
        report_unrelated = _report(
            statement="demo.1099int-statement.agg-unrelated",
            finding_id="demo.finding.box1.agg-unrelated",
            amount=200.0,
        )
        acq_a = _admit_acquisition(
            _answers(
                obligation_reference="DEMO-BOND-AGG-A",
                reported_statement_reference="ACCOUNT-REF-AGG",
                accrued_interest_paid_to_seller=300.0,
                confirmed_report_match=True,
            ),
            finding_id="demo.finding.acq.agg-a",
            confirmed_report_fact_id=report_main["fact_id"],
        )
        acq_b = _admit_acquisition(
            _answers(
                obligation_reference="DEMO-BOND-AGG-B",
                reported_statement_reference="ACCOUNT-REF-AGG",
                accrued_interest_paid_to_seller=300.0,
                confirmed_report_match=True,
            ),
            finding_id="demo.finding.acq.agg-b",
            confirmed_report_fact_id=report_main["fact_id"],
        )
        findings = {
            _rounding()["id"]: _rounding(),
            acq_a["id"]: acq_a,
            acq_b["id"]: acq_b,
            report_main["id"]: report_main,
            report_unrelated["id"]: report_unrelated,
        }
        result = _run(findings, with_line2b=True)

        # Both acquisitions genuinely associate to the shared report --
        # ADR-0068's evidenced statement match, not a payer+year guess.
        pairings = _pairing_values(result)
        self.assertEqual(len(pairings), 2)
        self.assertTrue(all(p["right_fact_id"] == report_main["fact_id"] for p in pairings))
        self.assertEqual(
            {p["left_fact_id"] for p in pairings},
            {acq_a["fact_id"], acq_b["fact_id"]},
        )

        # Each per-pairing supportability/current-year verdict still passes
        # independently at evaluation time (ADR-0070 Decision 4 is not
        # reopened): 300<=500 twice. Both are
        # retracted from ordinary publication because their shared report
        # group is aggregate-blocked -- detecting the combined over-claim
        # does not establish either finding is still ordinarily supported.
        cy = _pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|")
        self.assertEqual(cy, [])
        retracted = [
            row
            for row in result.dispositions
            if row.get("artifact_id") == CURRENT_YEAR_RULE_ID
            and row.get("disposition") == "blocked"
        ]
        self.assertEqual(len(retracted), 2)
        for row in retracted:
            self.assertEqual(row["code"], AGGREGATE_ACCRUED_EXCEEDS_REPORT)
            self.assertEqual(row["missing"], [report_main["fact_id"]])
        self.assertFalse(
            any(row.get("code") == ACCRUED_EXCEEDS_ASSOCIATED_REPORT for row in result.blocked)
        )

        # The aggregate check catches the combined 600 claim against the
        # specific 500 report and blocks it -- not the whole run, not the
        # unrelated report.
        aggregate_blocks = [
            row for row in result.blocked
            if row["artifact_id"] == AGGREGATE_SUPPORTABILITY_RULE_ID
        ]
        self.assertEqual(len(aggregate_blocks), 1)
        self.assertEqual(aggregate_blocks[0]["code"], AGGREGATE_ACCRUED_EXCEEDS_REPORT)
        self.assertEqual(aggregate_blocks[0]["missing"], [report_main["fact_id"]])

        # The subtotal must not silently publish 0 and
        # let line-2b present a different, confidently-computed taxable
        # total (an overstated "correct" $700). An
        # unresolved combined over-claim blocks the subtotal itself, named
        # with the same code, and that block propagates upward through the
        # ordinary missing-dependency mechanism: line-2b (and therefore
        # taxable-total) never reaches a plain, confidently-presented
        # number while the report-500 group is unresolved.
        self.assertNotIn(CURRENT_YEAR_SUBTOTAL_SYMBOL, result.symbols)
        subtotal_blocks = [
            row for row in result.blocked
            if row["artifact_id"] == CURRENT_YEAR_SUBTOTAL_RULE_ID
        ]
        self.assertEqual(len(subtotal_blocks), 1)
        self.assertEqual(subtotal_blocks[0]["code"], AGGREGATE_ACCRUED_EXCEEDS_REPORT)
        self.assertEqual(subtotal_blocks[0]["missing"], [report_main["fact_id"]])
        self.assertNotIn("tax.us.2025.interest.taxable-total", result.symbols)
        line2b_blocks = [
            row for row in result.blocked
            if row["artifact_id"] == "tax.us.2025.rule.form1040-line2b"
        ]
        self.assertEqual(len(line2b_blocks), 1)
        self.assertIn(CURRENT_YEAR_SUBTOTAL_SYMBOL, line2b_blocks[0]["missing"])


class TestLine2bProjection(unittest.TestCase):
    def test_t1_fully_includible_reaches_taxable_total(self) -> None:
        result = _run(
            _findings_for(answers=None, reports=[_report(amount=500.0)]),
            with_line2b=True,
        )
        self.assertIn("tax.us.2025.interest.taxable-total", result.symbols)
        self.assertEqual(Decimal(str(result.symbols["tax.us.2025.interest.taxable-total"])), Decimal("500"))
        self.assertEqual(result.symbols.get(CURRENT_YEAR_SUBTOTAL_SYMBOL), "0")

    def test_t2_current_year_adjustment_reduces_line2b(self) -> None:
        result = _run(
            _findings_for(answers=_answers(), reports=[_report(amount=500.0)]),
            with_line2b=True,
        )
        self.assertEqual(result.symbols.get(CURRENT_YEAR_SUBTOTAL_SYMBOL), "42.0")
        self.assertEqual(
            Decimal(str(result.symbols["tax.us.2025.interest.taxable-total"])),
            Decimal("458"),
        )
        self.assertIn(CURRENT_YEAR_SUBTOTAL_RULE_ID, {d["artifact_id"] for d in result.dispositions})
        self.assertIn(
            "tax.us.2025.rule.form1040-line2b",
            {d["artifact_id"] for d in result.dispositions if d["disposition"] == "published"},
        )


if __name__ == "__main__":
    unittest.main()
