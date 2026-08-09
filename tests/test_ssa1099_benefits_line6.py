"""Track 1: bounded Form SSA-1099 ordinary-benefits source boundary."""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path
from typing import Any

from packages.derivation.source_authority import audit_collect_authority
from packages.tax.ssa_benefits import (
    SSA_CLOSURE_FACT_TYPE,
    SSA_FAMILY_ID,
    SSA_MAPPING_ID,
    SSA_MEMBER_FACT_TYPE,
    FamilyClosure,
    SsaBenefitsError,
    SsaBenefitsStatement,
    current_statements,
    publish_subtotal,
)
from packages.tax.loader import (
    TAX_CONTENT_DIR,
    load_closure_mappings,
    load_source_families,
    tax_registry,
)


CONTENT = TAX_CONTENT_DIR
FIXTURES = Path("packages/sample_data/ssa1099_benefits_line6/source-boundary-fixtures.json")


def statement(
    ref: str = "demo.claim.1",
    *,
    payer: str = "demo.payer.ssa",
    subject: str = "taxpayer",
    statement_kind: str = "ssa-1099",
    box3: int | float | None = 1200,
    box4: int | float | None = 0,
    box5: int | float | None = 1200,
    box6: int | float | None = None,
    lump_sum_election: bool | None = False,
    corrected: bool = False,
) -> SsaBenefitsStatement:
    return SsaBenefitsStatement(
        payer_id=payer,
        tax_year=2025,
        statement_ref=ref,
        subject=subject,
        statement_kind=statement_kind,
        box3=box3,
        box4=box4,
        box5=box5,
        box6=box6,
        lump_sum_election=lump_sum_election,
        finding_id=f"demo.finding.{ref}",
        corrected=corrected,
    )


def closure(horizon: str = "demo.ssa.h0", attested: bool = True) -> FamilyClosure:
    return FamilyClosure(SSA_FAMILY_ID, "v1", horizon, attested)


class ContentContracts(unittest.TestCase):
    def load(self, name: str) -> dict[str, Any]:
        return json.loads((CONTENT / name).read_text("utf-8"))

    def test_all_track1_citizens_validate_against_published_schemas(self) -> None:
        registry = tax_registry()
        for name in (
            "ssa1099.bundle.json",
            "family.ssa1099-benefits.json",
            "closure-mapping.ssa1099-benefits.json",
            "rule.ssa1099-benefits-subtotal.json",
            "citation.ssa1099.box3.json",
            "citation.ssa1099.box4.json",
            "citation.ssa1099.box5.json",
            "citation.ssa1099.box6.json",
            "citation.ssa1099.statement-kind.json",
            "citation.ssa1099.lump-sum-election.json",
        ):
            with self.subTest(name=name):
                registry.validate_declared(self.load(name))

    def test_mapping_pins_the_exact_adopted_family_and_member(self) -> None:
        families = load_source_families()
        mappings = load_closure_mappings()
        family = families[SSA_FAMILY_ID]
        mapping = mappings[SSA_MAPPING_ID]
        self.assertEqual(mapping["family"], {"id": SSA_FAMILY_ID, "version": "v1"})
        self.assertEqual(mapping["member_fact_type"], {"id": SSA_MEMBER_FACT_TYPE, "version": "v1"})
        self.assertEqual(mapping["closure_fact_type"], {"id": SSA_CLOSURE_FACT_TYPE, "version": "v1"})
        audit_collect_authority(
            [self.load("rule.ssa1099-benefits-subtotal.json")],
            [mapping],
            [family],
        )

    def test_no_line6_form_field_or_worksheet_content_yet(self) -> None:
        # Track 1 stops at the source-side subtotal; line 6a/6b, the
        # worksheet, and presentation are Track 2's job.
        self.assertFalse(list(CONTENT.glob("form1040.line-6*")))
        self.assertFalse(list(CONTENT.glob("*worksheet*")))

    def test_synthetic_fixture_covers_positive_lifecycle_and_blocked_cases(self) -> None:
        fixture = json.loads(FIXTURES.read_text("utf-8"))
        self.assertTrue(fixture["positive"]["id"].startswith("demo."))
        self.assertEqual(fixture["positive"]["subject"], "taxpayer")
        self.assertEqual(fixture["spouse"]["subject"], "spouse")
        self.assertTrue(fixture["correction"]["successor"]["corrected"])
        self.assertEqual(len(fixture["blocked"]), 7)
        self.assertTrue(all(item["id"].startswith("demo.") for item in fixture["blocked"]))


class AdmissionCases(unittest.TestCase):
    def test_p1_one_statement_publishes_exact_subtotal(self) -> None:
        result = publish_subtotal([statement()], closure=closure())
        self.assertEqual(result.value, Decimal("1200"))
        self.assertEqual(result.statement_refs, ("demo.claim.1",))

    def test_p2_distinct_statements_aggregate_once(self) -> None:
        result = publish_subtotal(
            [
                statement("demo.claim.1", box3=700, box5=700),
                statement("demo.claim.2", box3=300, box5=300),
            ],
            closure=closure(),
        )
        self.assertEqual(result.value, Decimal("1000"))
        self.assertEqual(result.statement_refs, ("demo.claim.1", "demo.claim.2"))

    def test_p2b_taxpayer_and_spouse_remain_distinct_and_aggregate(self) -> None:
        result = publish_subtotal(
            [
                statement("demo.claim.taxpayer.1", subject="taxpayer", box3=12000, box5=12000),
                statement("demo.claim.spouse.1", subject="spouse", box3=9000, box5=9000, box6=0),
            ],
            closure=closure(),
        )
        self.assertEqual(result.value, Decimal("21000"))
        self.assertEqual(result.statement_refs, ("demo.claim.spouse.1", "demo.claim.taxpayer.1"))

    def test_p3_same_statement_correction_replaces_prior_value(self) -> None:
        current = current_statements([
            statement(box3=1000, box5=1000),
            statement(box3=1250, box5=1250, corrected=True),
        ])
        self.assertEqual(len(current), 1)
        self.assertEqual(current[0].box3, 1250)
        result = publish_subtotal(
            [statement(box3=1000, box5=1000), statement(box3=1250, box5=1250, corrected=True)],
            closure=closure(),
        )
        self.assertEqual(result.value, Decimal("1250"))

    def test_p3b_duplicate_original_or_conflicting_correction_blocks(self) -> None:
        with self.assertRaises(SsaBenefitsError):
            current_statements([statement(), statement()])
        with self.assertRaises(Exception):
            current_statements([statement(ref="demo.claim.never-seen", corrected=True)])

    def test_p4_affirmative_closed_empty_publishes_zero(self) -> None:
        result = publish_subtotal([], closure=closure(), closure_finding_id="demo.closure.true")
        self.assertEqual(result.value, Decimal(0))
        self.assertEqual(result.horizon_id, "demo.ssa.h0")
        self.assertEqual(result.closure_finding_id, "demo.closure.true")

    def test_p5_box5_equals_box3_minus_box4_including_zero(self) -> None:
        result = publish_subtotal(
            [statement(box3=500, box4=500, box5=0)], closure=closure()
        )
        self.assertEqual(result.value, Decimal("0"))

    def test_n1_box_reconciliation_mismatch_blocks(self) -> None:
        for bad in (
            statement(box3=1000, box4=0, box5=900),
            statement(box3=1000, box4=1200, box5=-200),
            statement(box5=None),
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(SsaBenefitsError):
                    current_statements([bad])

    def test_n2_repayment_greater_than_benefits_blocks(self) -> None:
        with self.assertRaises(SsaBenefitsError):
            current_statements([statement(box3=500, box4=700, box5=-200)])

    def test_n3_non_ordinary_statement_kind_blocks(self) -> None:
        for kind in ("rrb-1099", "ssa-1042s", "foreign-social-benefit"):
            with self.subTest(kind=kind):
                with self.assertRaises(SsaBenefitsError):
                    current_statements([statement(statement_kind=kind)])

    def test_n4_another_taxpayer_subject_blocks(self) -> None:
        for subject in ("dependent", "other-taxpayer", ""):
            with self.subTest(subject=subject):
                with self.assertRaises(SsaBenefitsError):
                    current_statements([statement(subject=subject)])

    def test_n5_lump_sum_election_blocks(self) -> None:
        with self.assertRaisesRegex(SsaBenefitsError, "lump-sum"):
            current_statements([statement(lump_sum_election=True)])
        with self.assertRaises(SsaBenefitsError):
            current_statements([statement(lump_sum_election=None)])

    def test_n6_positive_box6_withholding_blocks(self) -> None:
        with self.assertRaisesRegex(SsaBenefitsError, "box 6"):
            current_statements([statement(box6=150)])

    def test_n7_missing_false_stale_or_duplicate_closure_blocks_empty_zero(self) -> None:
        for bad_closure, horizon in (
            (None, "demo.ssa.h0"),
            (closure(attested=False), "demo.ssa.h0"),
            (closure(horizon="demo.ssa.old"), "demo.ssa.h0"),
        ):
            with self.subTest(bad_closure=bad_closure):
                with self.assertRaises(SsaBenefitsError):
                    publish_subtotal([], closure=bad_closure, current_horizon_id=horizon)
        with self.assertRaises(SsaBenefitsError):
            publish_subtotal([statement(), statement()], closure=closure())


if __name__ == "__main__":
    unittest.main()
