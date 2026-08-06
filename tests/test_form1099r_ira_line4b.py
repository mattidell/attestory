"""Track 1: bounded Form 1099-R IRA-family source-to-line-4b boundary."""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path
from typing import Any, cast

from packages.derivation.source_authority import audit_collect_authority
from packages.tax.ira_distributions import (
    IRA_CLOSURE_FACT_TYPE,
    IRA_FAMILY_ID,
    IRA_MAPPING_ID,
    IRA_MEMBER_FACT_TYPE,
    IraDistributionError,
    IraDistributionStatement,
    FamilyClosure,
    current_statements,
    publish_line4b,
)
from packages.tax.loader import TAX_CONTENT_DIR, load_closure_mappings, load_source_families, tax_registry


CONTENT = TAX_CONTENT_DIR


def statement(
    ref: str = "demo.stmt.1",
    *,
    payer: str = "demo.payer.alpha",
    box1: int | float = 1200,
    box2a: int | float | None = 1200,
    indicator: str = "traditional",
    codes: tuple[str, ...] = ("7",),
    box2b_not_determined: bool | None = False,
    corrected: bool = False,
) -> IraDistributionStatement:
    return IraDistributionStatement(
        payer_id=payer,
        tax_year=2025,
        statement_ref=ref,
        ira_indicator=indicator,
        distribution_codes=codes,
        box1=box1,
        box2a=box2a,
        box2b_not_determined=box2b_not_determined,
        finding_id=f"demo.finding.{ref}",
        corrected=corrected,
    )


def closure(horizon: str = "demo.ira.h0", attested: bool = True) -> FamilyClosure:
    return FamilyClosure(IRA_FAMILY_ID, "v1", horizon, attested)


class ContentContracts(unittest.TestCase):
    def load(self, name: str) -> dict[str, Any]:
        return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))

    def test_all_track1_citizens_validate_against_published_schemas(self) -> None:
        registry = tax_registry()
        for name in (
            "f1099r-ira.bundle.json",
            "family.f1099r-ira-fully-taxable.json",
            "closure-mapping.f1099r-ira-fully-taxable.json",
            "rule.f1099r-ira-fully-taxable-subtotal.json",
            "form1040.line-4b.form-field.json",
            "citation.f1099r.box1.json",
            "citation.f1099r.box2a.json",
            "citation.f1099r.box2b.json",
            "citation.f1099r.indicator.json",
            "citation.f1099r.distribution-code.json",
            "citation.form1040.line-4b.json",
        ):
            with self.subTest(name=name):
                registry.validate_declared(self.load(name))

    def test_mapping_pins_the_exact_adopted_family_and_member(self) -> None:
        families = load_source_families()
        mappings = load_closure_mappings()
        family = families[IRA_FAMILY_ID]
        mapping = mappings[IRA_MAPPING_ID]
        self.assertEqual(mapping["family"], {"id": IRA_FAMILY_ID, "version": "v1"})
        self.assertEqual(mapping["member_fact_type"], {"id": IRA_MEMBER_FACT_TYPE, "version": "v1"})
        self.assertEqual(mapping["closure_fact_type"], {"id": IRA_CLOSURE_FACT_TYPE, "version": "v1"})
        audit_collect_authority(
            [self.load("rule.f1099r-ira-fully-taxable-subtotal.json")],
            [mapping],
            [family],
        )

    def test_line4b_is_the_only_new_form1040_field(self) -> None:
        field = self.load("form1040.line-4b.form-field.json")
        self.assertEqual(field["line"], "4b")
        self.assertNotIn("line-4a", field["id"])
        self.assertFalse(list(CONTENT.glob("form1040.line-4a*")))
        self.assertEqual(field["citation"], {"id": "tax.us.2025.citation.form1040.line-4b", "version": "v1"})

    def test_synthetic_fixture_covers_positive_lifecycle_and_blocked_cases(self) -> None:
        fixture = json.loads(
            (Path("packages/sample_data/form1099r_ira_line4b/source-boundary-fixtures.json")).read_text("utf-8")
        )
        self.assertTrue(fixture["positive"]["id"].startswith("demo."))
        self.assertTrue(fixture["correction"]["successor"]["corrected"])
        self.assertEqual(len(fixture["blocked"]), 4)
        self.assertTrue(all(item["id"].startswith("demo.") for item in fixture["blocked"]))


class AdmissionCases(unittest.TestCase):
    def test_p1_one_statement_publishes_exact_line4b(self) -> None:
        result = publish_line4b([statement()], closure=closure())
        self.assertEqual(result.value, Decimal("1200"))
        self.assertIsNone(result.line4a)
        self.assertEqual(result.statement_refs, ("demo.stmt.1",))

    def test_p2_distinct_statements_aggregate_once(self) -> None:
        result = publish_line4b(
            [statement("demo.stmt.1", box1=700, box2a=700), statement("demo.stmt.2", box1=300, box2a=300)],
            closure=closure(),
        )
        self.assertEqual(result.value, Decimal("1000"))
        self.assertEqual(result.statement_refs, ("demo.stmt.1", "demo.stmt.2"))

    def test_p3_same_statement_correction_replaces_prior_value(self) -> None:
        current = current_statements([
            statement(box1=1000, box2a=1000),
            statement(box1=1250, box2a=1250, corrected=True),
        ])
        self.assertEqual(len(current), 1)
        self.assertEqual(current[0].box1, 1250)
        result = publish_line4b(
            [statement(box1=1000, box2a=1000), statement(box1=1250, box2a=1250, corrected=True)],
            closure=closure(),
        )
        self.assertEqual(result.value, Decimal("1250"))

    def test_p4_affirmative_closed_empty_publishes_zero(self) -> None:
        result = publish_line4b([], closure=closure(), closure_finding_id="demo.closure.true")
        self.assertEqual(result.value, Decimal(0))
        self.assertIsNone(result.line4a)
        self.assertEqual(result.horizon_id, "demo.ira.h0")
        self.assertEqual(result.closure_finding_id, "demo.closure.true")

    def test_n1_missing_or_mismatched_taxable_amount_witness_blocks(self) -> None:
        for bad in (
            statement(box2a=None),
            statement(box1=1000, box2a=900),
            statement(box2b_not_determined=True),
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(IraDistributionError):
                    current_statements([bad])

    def test_n2_non_ira_or_non_normal_code_blocks(self) -> None:
        for bad in (
            statement(indicator="roth"),
            statement(codes=("7", "B")),
            statement(codes=("1",)),
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(IraDistributionError):
                    current_statements([bad])

    def test_n3_special_treatment_is_not_inferred(self) -> None:
        for code in (("2",), ("G",), ("Q",), ("J",)):
            with self.subTest(code=code):
                with self.assertRaisesRegex(IraDistributionError, "code 7"):
                    current_statements([statement(codes=code)])

    def test_n4_missing_false_stale_or_duplicate_closure_blocks_empty_zero(self) -> None:
        for bad_closure, horizon in (
            (None, "demo.ira.h0"),
            (closure(attested=False), "demo.ira.h0"),
            (closure(horizon="demo.ira.old"), "demo.ira.h0"),
        ):
            with self.subTest(bad_closure=bad_closure):
                with self.assertRaises(IraDistributionError):
                    publish_line4b([], closure=bad_closure, current_horizon_id=horizon)
        with self.assertRaises(IraDistributionError):
            publish_line4b([statement(), statement()], closure=closure())


if __name__ == "__main__":
    unittest.main()
