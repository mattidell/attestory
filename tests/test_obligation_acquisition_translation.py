"""Seam 6 — Ordinary input mapping.

Synthetic in-repo fixtures only. Proves:
- the structured ordinary-language answer set is closed (no tax
  classification can be smuggled through it, structurally, not just by
  naming convention);
- the mapper emits exactly one canonical circumstance fact, naming only
  ordinary quantities and identifying information;
- no question in the user-facing surface asks for a tax classification;
- contribution admission (the real `apply_contribution_batch` boundary,
  ADR-0032 D2) — not the mapper itself — is what makes the emitted fact
  real, and it still validates the mapper's output (evidence currentness,
  schema shape) rather than rubber-stamping it.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.contribution import ContributionError
from packages.kernel.findings import project
from packages.tax.obligation_acquisition_mapping import (
    ORDINARY_ANSWERS_SCHEMA,
    ORDINARY_QUESTIONS,
    OrdinaryInputError,
    build_obligation_acquisition_bundle,
    build_ordinary_acquisition_contribution,
    build_ordinary_acquisition_entity_acts,
    contribute_ordinary_acquisition,
    derive_obligation_acquisition_fact_id,
    map_ordinary_acquisition_answers,
    validate_ordinary_answers,
)
from tests.support import act, demo_evidence, registry_with_demo_kinds

_CLASSIFICATION_WORDS = (
    "taxable",
    "tax treatment",
    "adjustment",
    "deduct",
    "schedule b",
    "election",
    "classification",
    "exclusion",
    "basis",
)


def _valid_answers(**overrides: Any) -> dict[str, Any]:
    answers = {
        "payer_name": "Demo Municipal Authority",
        "obligation_description": "10-year municipal bond, series demo-2025",
        "obligation_reference": "demo-cusip-000111222",
        "acquisition_date": "2025-03-14",
        "accrued_interest_paid_to_seller": 42.5,
        "currency": "USD",
    }
    answers.update(overrides)
    return answers


class TestSubjectAndScope(unittest.TestCase):
    def test_emitted_value_names_exactly_the_ordinary_circumstance(self) -> None:
        finding = map_ordinary_acquisition_answers(
            _valid_answers(),
            finding_id="demo.finding.acq-a",
            evidence_id="demo.evidence.acq-a",
            contribution_id="demo.contribution.acq-a",
        )
        value = finding["value"]
        self.assertEqual(
            set(value.keys()),
            {
                "obligation",
                "acquisition_date",
                "accrued_interest_paid_to_seller",
                "currency",
                "reported_statement_reference",
                "confirmed_report_match",
            },
        )
        self.assertEqual(
            set(value["obligation"].keys()), {"payer_name", "description", "reference"}
        )
        self.assertEqual(finding["value"]["accrued_interest_paid_to_seller"], 42.5)
        self.assertEqual(finding["basis"], "attested")
        self.assertEqual(finding["schema"], "finding.v2")

    def test_no_question_asks_for_a_tax_classification(self) -> None:
        """Word-matching check for the classification words below, on
        whatever ordinary questions remain. The tax-year dimension is
        handled structurally instead: there is no tax-year-shaped question
        or answer field at all -- ``ORDINARY_ANSWERS_SCHEMA`` has no
        ``tax_year`` property and ``ORDINARY_QUESTIONS`` asks nothing about
        it. The semantic property (a run's reporting year, not a user
        answer, drives report selection) is proven directly and
        structurally in
        ``tests.test_identity_association.
        TestReportingYearIsRunScopeNotUserAnswer`` -- run the same
        acquisition answers against two different run-scope years and
        assert the association's result tracks the run scope, not the
        answer set.
        """
        self.assertTrue(ORDINARY_QUESTIONS)
        for field, prompt in ORDINARY_QUESTIONS:
            lowered = prompt.lower()
            for word in _CLASSIFICATION_WORDS:
                self.assertNotIn(
                    word,
                    lowered,
                    msg=f"question for {field!r} smuggles a classification word: {prompt!r}",
                )

    def test_schema_has_no_classification_field(self) -> None:
        properties = set(ORDINARY_ANSWERS_SCHEMA["properties"])
        for word in ("treatment", "classification", "election", "adjustment"):
            self.assertFalse(
                any(word in prop for prop in properties),
                msg=f"schema property set unexpectedly names {word!r}: {properties}",
            )


class TestStructuralClosure(unittest.TestCase):
    def test_extra_classification_field_is_rejected(self) -> None:
        answers = _valid_answers(tax_treatment="accrued-interest-reduction")
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)
        with self.assertRaises(OrdinaryInputError):
            map_ordinary_acquisition_answers(
                answers,
                finding_id="demo.finding.bad",
                evidence_id="demo.evidence.bad",
                contribution_id="demo.contribution.bad",
            )

    def test_missing_required_ordinary_field_is_rejected(self) -> None:
        answers = _valid_answers()
        del answers["acquisition_date"]
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)

    def test_malformed_date_is_rejected(self) -> None:
        answers = _valid_answers(acquisition_date="March 14 2025")
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)

    def test_negative_accrued_amount_is_rejected(self) -> None:
        answers = _valid_answers(accrued_interest_paid_to_seller=-1)
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)

    def test_non_usd_currency_is_rejected(self) -> None:
        answers = _valid_answers(currency="EUR")
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)

    def test_whitespace_only_payer_name_is_rejected(self) -> None:
        answers = _valid_answers(payer_name="   ")
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)
        with self.assertRaises(OrdinaryInputError):
            map_ordinary_acquisition_answers(
                answers,
                finding_id="demo.finding.bad-payer",
                evidence_id="demo.evidence.bad-payer",
                contribution_id="demo.contribution.bad-payer",
            )

    def test_future_acquisition_date_is_rejected(self) -> None:
        answers = _valid_answers(acquisition_date="2099-01-01")
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)

    def test_impossible_month_acquisition_date_is_rejected(self) -> None:
        """A lexically-shaped but calendrically impossible date (month 99)
        matches the schema's ``^\\d{4}-\\d{2}-\\d{2}$`` pattern but is not a
        real calendar date; it must be rejected through the real
        validation boundary, not merely at a bare schema check."""
        answers = _valid_answers(acquisition_date="2025-99-99")
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)
        with self.assertRaises(OrdinaryInputError):
            map_ordinary_acquisition_answers(
                answers,
                finding_id="demo.finding.bad-month",
                evidence_id="demo.evidence.bad-month",
                contribution_id="demo.contribution.bad-month",
            )

    def test_impossible_day_acquisition_date_is_rejected(self) -> None:
        """February 29 in a non-leap year is lexically well-shaped and
        individually valid-looking components, but not a real calendar
        date."""
        answers = _valid_answers(acquisition_date="2025-02-29")
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)
        with self.assertRaises(OrdinaryInputError):
            map_ordinary_acquisition_answers(
                answers,
                finding_id="demo.finding.bad-day",
                evidence_id="demo.evidence.bad-day",
                contribution_id="demo.contribution.bad-day",
            )


class TestIdentity(unittest.TestCase):
    def test_identity_rests_on_payer_and_reference_not_on_a_row(self) -> None:
        one = derive_obligation_acquisition_fact_id(
            payer_name="Demo Municipal Authority",
            obligation_reference="demo-cusip-000111222",
            obligation_description="10-year municipal bond, series demo-2025",
            acquisition_date="2025-03-14",
        )
        two = derive_obligation_acquisition_fact_id(
            payer_name="Demo Municipal Authority",
            obligation_reference="demo-cusip-333444555",
            obligation_description="10-year municipal bond, series demo-2025",
            acquisition_date="2025-03-14",
        )
        self.assertNotEqual(one, two)

    def test_missing_reference_still_derives_a_stable_id(self) -> None:
        answers = _valid_answers(obligation_reference=None)
        finding = map_ordinary_acquisition_answers(
            answers,
            finding_id="demo.finding.acq-noref",
            evidence_id="demo.evidence.acq-noref",
            contribution_id="demo.contribution.acq-noref",
        )
        self.assertIn("unreferenced", finding["fact_id"])
        self.assertIsNone(finding["value"]["obligation"]["reference"])


class TestConfirmationMustNameATarget(unittest.TestCase):
    """A ``confirmed_report_match: true`` confirmation must always name the
    report it confirms, uniformly at both tiers — whether or not a
    ``reported_statement_reference`` is present. The mapper fails closed
    rather than emitting that unscoped shape at either tier."""

    def test_coarse_tier_true_confirmation_with_no_target_is_rejected(self) -> None:
        answers = _valid_answers(confirmed_report_match=True)
        with self.assertRaises(OrdinaryInputError) as caught:
            map_ordinary_acquisition_answers(
                answers,
                finding_id="demo.finding.acq-unscoped",
                evidence_id="demo.evidence.acq-unscoped",
                contribution_id="demo.contribution.acq-unscoped",
            )
        self.assertIn("confirmed_report_match", str(caught.exception))

    def test_coarse_tier_true_confirmation_with_a_target_is_accepted(self) -> None:
        answers = _valid_answers(confirmed_report_match=True)
        finding = map_ordinary_acquisition_answers(
            answers,
            finding_id="demo.finding.acq-scoped",
            evidence_id="demo.evidence.acq-scoped",
            contribution_id="demo.contribution.acq-scoped",
            confirmed_report_fact_id="demo.report.named-target",
        )
        self.assertEqual(
            finding["value"]["confirmed_report_fact_id"], "demo.report.named-target"
        )

    def test_statement_narrowed_true_confirmation_with_no_target_is_rejected(
        self,
    ) -> None:
        """The strict (statement-narrowed) tier enforces the same
        exact-target rule as the coarse tier
        (``identity_association.associate``'s strict-tier branch now reads
        ``confirmed_report_fact_id`` too) — a confirmation naming a
        reported statement reference is not exempt from naming its
        target."""
        answers = _valid_answers(
            confirmed_report_match=True,
            reported_statement_reference="demo-statement-ref",
        )
        with self.assertRaises(OrdinaryInputError) as caught:
            map_ordinary_acquisition_answers(
                answers,
                finding_id="demo.finding.acq-statement-unscoped",
                evidence_id="demo.evidence.acq-statement-unscoped",
                contribution_id="demo.contribution.acq-statement-unscoped",
            )
        self.assertIn("confirmed_report_match", str(caught.exception))

    def test_statement_narrowed_true_confirmation_with_a_target_is_accepted(
        self,
    ) -> None:
        answers = _valid_answers(
            confirmed_report_match=True,
            reported_statement_reference="demo-statement-ref",
        )
        finding = map_ordinary_acquisition_answers(
            answers,
            finding_id="demo.finding.acq-statement-confirmed",
            evidence_id="demo.evidence.acq-statement-confirmed",
            contribution_id="demo.contribution.acq-statement-confirmed",
            confirmed_report_fact_id="demo.report.named-statement-target",
        )
        self.assertEqual(
            finding["value"]["confirmed_report_fact_id"],
            "demo.report.named-statement-target",
        )

    def test_false_confirmation_needs_no_target(self) -> None:
        answers = _valid_answers(confirmed_report_match=False)
        finding = map_ordinary_acquisition_answers(
            answers,
            finding_id="demo.finding.acq-unconfirmed",
            evidence_id="demo.evidence.acq-unconfirmed",
            contribution_id="demo.contribution.acq-unconfirmed",
        )
        self.assertNotIn("confirmed_report_fact_id", finding["value"])


class ContributionAdmissionFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self._tmp.name))

    def opening_acts(self, answers: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        resolved_answers = answers or _valid_answers()
        bundle = build_obligation_acquisition_bundle(resolved_answers)
        acts: list[dict[str, Any]] = [
            act(0, "bundle-adoption", {"bundle": bundle}),
            act(
                1,
                "evidence-submitted",
                {
                    "evidence": demo_evidence(
                        "demo.evidence.acq-a",
                        "Synthetic ordinary-language acquisition interview",
                        {"mode": "ordinary-language-entry", "synthetic": True},
                    )
                },
            ),
        ]
        # The mapper's identity now rests on entity-kind keys (payer,
        # obligation): the payer and obligation entities must be current
        # before an acquisition finding can name them, exactly as box-1
        # ingestion introduces its own payer/statement entities first.
        acts.extend(build_ordinary_acquisition_entity_acts(resolved_answers, act_index=2))
        return acts


class TestContributionAdmissionValidatesOutput(ContributionAdmissionFixture):
    def test_well_formed_answers_are_admitted_through_the_real_boundary(self) -> None:
        base = project(tuple(self.opening_acts()), self.registry)
        result = contribute_ordinary_acquisition(
            base,
            _valid_answers(),
            registry=self.registry,
            record_id="demo.crec.acq-a",
            act_index=4,
            contribution_id="demo.contribution.acq-a",
            evidence_id="demo.evidence.acq-a",
            finding_id="demo.finding.acq-a",
            committed_against=4,
        )
        self.assertEqual(result.terminal_record["phase"], "completed")
        finding = result.state.findings["demo.finding.acq-a"]
        self.assertEqual(finding["contribution_id"], "demo.contribution.acq-a")
        self.assertEqual(
            finding["value"]["accrued_interest_paid_to_seller"], 42.5
        )
        self.assertIn("demo.contribution.acq-a", result.state.contributions)

    def test_admission_rejects_a_contribution_whose_evidence_was_never_submitted(
        self,
    ) -> None:
        """Contribution admission genuinely validates — it is not a
        rubber stamp on whatever the mapper hands it."""
        base = project((), self.registry)  # no evidence-submitted act at all
        with self.assertRaises(ContributionError):
            contribute_ordinary_acquisition(
                base,
                _valid_answers(),
                registry=self.registry,
                record_id="demo.crec.acq-noevidence",
                act_index=1,
                contribution_id="demo.contribution.acq-noevidence",
                evidence_id="demo.evidence.does-not-exist",
                finding_id="demo.finding.acq-noevidence",
                committed_against=1,
            )

    def test_admission_rejects_a_finding_whose_evidence_is_not_the_contributions(
        self,
    ) -> None:
        base = project(
            tuple(
                self.opening_acts()
                + [
                    act(
                        4,
                        "evidence-submitted",
                        {
                            "evidence": demo_evidence(
                                "demo.evidence.other",
                                "A different synthetic document",
                                {"unrelated": True},
                            )
                        },
                    )
                ]
            ),
            self.registry,
        )
        built = build_ordinary_acquisition_contribution(
            _valid_answers(),
            act_index=5,
            contribution_id="demo.contribution.acq-mismatch",
            evidence_id="demo.evidence.acq-a",
            finding_id="demo.finding.acq-mismatch",
            committed_against=5,
        )
        # Tamper with the assertion's evidence after mapping, to prove the
        # contribution boundary — not the mapper — catches the mismatch.
        built.finding["evidence_ids"] = ["demo.evidence.other"]
        built.assertion_act["payload"]["finding"] = built.finding
        from packages.kernel.contribution import apply_contribution_batch

        with self.assertRaises(ContributionError):
            apply_contribution_batch(
                base,
                contribution_act=built.contribution_act,
                successor_acts=[built.assertion_act],
                registry=self.registry,
                record_id="demo.crec.acq-mismatch",
                workspace_revision=5,
            )


class TestNonFiniteNumbersRejectedBeforeAdmission(ContributionAdmissionFixture):
    """`inf`/`nan` for `accrued_interest_paid_to_seller` must be rejected
    before a finding or act is ever built, and must never reach
    contribution admission — not merely fail admission for some unrelated
    reason later."""

    def test_infinite_accrued_amount_is_rejected_before_admission(self) -> None:
        answers = _valid_answers(accrued_interest_paid_to_seller=float("inf"))
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)
        with self.assertRaises(OrdinaryInputError):
            map_ordinary_acquisition_answers(
                answers,
                finding_id="demo.finding.acq-inf",
                evidence_id="demo.evidence.acq-inf",
                contribution_id="demo.contribution.acq-inf",
            )
        base = project(tuple(self.opening_acts()), self.registry)
        with self.assertRaises(OrdinaryInputError):
            contribute_ordinary_acquisition(
                base,
                answers,
                registry=self.registry,
                record_id="demo.crec.acq-inf",
                act_index=2,
                contribution_id="demo.contribution.acq-inf",
                evidence_id="demo.evidence.acq-a",
                finding_id="demo.finding.acq-inf",
                committed_against=2,
            )
        self.assertNotIn("demo.contribution.acq-inf", base.contributions)
        self.assertNotIn("demo.finding.acq-inf", base.findings)

    def test_nan_accrued_amount_is_rejected_before_admission(self) -> None:
        answers = _valid_answers(accrued_interest_paid_to_seller=float("nan"))
        with self.assertRaises(OrdinaryInputError):
            validate_ordinary_answers(answers)
        with self.assertRaises(OrdinaryInputError):
            map_ordinary_acquisition_answers(
                answers,
                finding_id="demo.finding.acq-nan",
                evidence_id="demo.evidence.acq-nan",
                contribution_id="demo.contribution.acq-nan",
            )
        base = project(tuple(self.opening_acts()), self.registry)
        with self.assertRaises(OrdinaryInputError):
            contribute_ordinary_acquisition(
                base,
                answers,
                registry=self.registry,
                record_id="demo.crec.acq-nan",
                act_index=2,
                contribution_id="demo.contribution.acq-nan",
                evidence_id="demo.evidence.acq-a",
                finding_id="demo.finding.acq-nan",
                committed_against=2,
            )
        self.assertNotIn("demo.contribution.acq-nan", base.contributions)
        self.assertNotIn("demo.finding.acq-nan", base.findings)


class TestDataSafetySynthetic(unittest.TestCase):
    def test_fixtures_in_this_file_are_obviously_synthetic(self) -> None:
        answers = _valid_answers()
        self.assertTrue(answers["payer_name"].startswith("Demo"))
        self.assertIn("demo", answers["obligation_reference"])


if __name__ == "__main__":
    unittest.main()
