"""Synthetic Track 1A contract evidence for attachment-rule.v6."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import PackageValidation, package_instance_checksum, validate_package
from packages.derivation.runner import (
    ITEMIZATION_TIE_OUT_VIOLATION,
    InputFinding,
    RunContext,
    RunResult,
    SourceFact,
    run,
)
from packages.kernel.schema_registry import SchemaValidationError


ROOT = Path(__file__).resolve().parent.parent
V6_FIXTURE = ROOT / "packages/sample_data/schedule_b_interest_adjustments/schema/examples/attachment-rule.v6.json"
V2_FIXTURE = ROOT / "packages/sample_data/k1_interest_breadth/schema/examples/attachment-rule.v2.json"
V6_PACKAGE_FIXTURE = ROOT / "packages/sample_data/k1_interest_breadth/schema/examples/artifact-package.v6.json"
V11_PACKAGE_FIXTURE = ROOT / "packages/sample_data/schedule_b_interest_adjustments/schema/examples/artifact-package.v11.json"
V12_PACKAGE_FIXTURE = ROOT / "packages/sample_data/schedule_b_interest_adjustments/schema/examples/artifact-package.v12.json"


def _load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def _input(symbol: str, value: object) -> InputFinding:
    return InputFinding(symbol=symbol, value=value, finding_id=f"demo.finding.{symbol}", role="input")


def _package_corpus(attachment: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    """Build the small synthetic corpus admitted by the committed v11 fixture."""
    package = _load(V11_PACKAGE_FIXTURE)
    scope = attachment["scope"]
    corpus = {(attachment["id"], attachment["version"]): attachment}
    family_specs = {
        "demo.family.positive-interest": ("demo.interest.positive", "demo.interest.positive-subtotal"),
        "demo.family.nominee": ("demo.interest.nominee", "demo.interest.nominee-subtotal"),
        "demo.family.accrued-interest": ("demo.interest.accrued", "demo.interest.accrued-subtotal"),
        "demo.family.abp-adjustment": ("demo.interest.abp", "demo.interest.abp-subtotal"),
    }
    for member in package["members"]:
        member_id = member["id"]
        version = member["version"]
        schema = member["schema"]
        if schema == "source-family.v1":
            fact_type, subtotal = family_specs[member_id]
            citizen = {
                "schema": schema,
                "id": member_id,
                "version": version,
                "title": f"Synthetic source family {member_id}",
                "scope": scope,
                "closure_claim": "Synthetic closed class for package admission evidence.",
                "member_predicate": {"fact_type": fact_type},
                "authorizes_subtotal": subtotal,
            }
        elif schema == "fact-type.v2":
            value_schema: dict[str, Any] = (
                {"enum": ["yes", "no"]}
                if member_id == "demo.scheduleb.answer"
                else {"minimum": 0, "type": "number"}
            )
            citizen = {
                "schema": schema,
                "id": member_id,
                "version": version,
                "title": f"Synthetic fact type {member_id}",
                "nature": "determinable",
                "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
                "value_schema": value_schema,
                "supersession": {"policy": "free"},
            }
        elif schema == "citation.v1":
            citizen = {
                "schema": schema,
                "id": member_id,
                "version": version,
                "authority": {"family": "irs-instructions", "form_id": "demo-schedule-b", "tax_year": 2025},
            }
        elif schema == "parameter-declaration.v1":
            citizen = {"schema": schema, "id": member_id, "version": version, "scope": scope, "values": "0"}
        elif schema == "taxable-interest-composition.v1":
            citizen = {
                "schema": schema,
                "id": member_id,
                "version": version,
                "coextensiveness": "slot-bijection",
                "constituents": [{
                    "authorizes_subtotal": "demo.interest.positive-subtotal",
                    "source_family": {"id": "demo.family.positive-interest", "version": "v1"},
                }],
                "publishes": "demo.interest.taxable-total",
                "required_universe": {"claim": "Synthetic positive-interest composition."},
            }
        else:
            continue
        corpus[(member_id, version)] = citizen
    return corpus


def _package_result(attachment: dict[str, Any]) -> PackageValidation:
    package = _load(V11_PACKAGE_FIXTURE)
    return validate_package(package, _package_corpus(attachment), DerivationSchemas())


def _run(attachment: dict[str, Any], *, line_value: str = "60") -> RunResult:
    return run(
        RunContext(
        run_id="demo.attachment-v6",
            rules=[attachment],
            parameters={"demo.parameter.schedule-b-threshold": {"values": "0"}},
            canon={},
            inputs=[
                _input("demo.interest.taxable-total", line_value),
                _input("demo.interest.positive-subtotal", "100"),
                _input("demo.interest.nominee-subtotal", "25"),
                _input("demo.interest.accrued-subtotal", "10"),
                _input("demo.interest.abp-subtotal", "5"),
                _input("demo.scheduleb.answer", "yes"),
            ],
            sources=[
                SourceFact("demo.interest.positive", "100", "demo.row.positive"),
                SourceFact("demo.interest.nominee", "25", "demo.row.nominee"),
                SourceFact("demo.interest.accrued", "10", "demo.row.accrued"),
                SourceFact("demo.interest.abp", "5", "demo.row.abp"),
            ],
            adoption_pin={"role": "adoption", "id": "demo.adoption.v6", "version": "v1"},
            governance_pins=[],
        ),
        DerivationSchemas(),
    )


class AttachmentRuleV6Schema(unittest.TestCase):
    def test_positive_typed_adjustment_row_validates(self) -> None:
        DerivationSchemas().validate_declared(_load(V6_FIXTURE))

    def test_v2_fixture_remains_valid(self) -> None:
        DerivationSchemas().validate_declared(_load(V2_FIXTURE))

    def test_v6_fixture_remains_valid(self) -> None:
        DerivationSchemas().validate_declared(_load(V6_PACKAGE_FIXTURE))

    def test_v11_package_admits_v6_fixture(self) -> None:
        package = _load(V11_PACKAGE_FIXTURE)
        schemas = DerivationSchemas()
        schemas.validate_declared(package)
        self.assertEqual(package_instance_checksum(package), package["package_checksum"])
        result = _package_result(_load(V6_FIXTURE))
        self.assertTrue(result.ok, result.issues)

    def test_v12_package_admits_v6_fixture(self) -> None:
        package = _load(V12_PACKAGE_FIXTURE)
        schemas = DerivationSchemas()
        schemas.validate_declared(package)
        self.assertEqual(package_instance_checksum(package), package["package_checksum"])
        result = _package_result(_load(V6_FIXTURE))
        self.assertTrue(result.ok, result.issues)

    def test_invalid_adjustment_row_kind_is_rejected(self) -> None:
        malformed = _load(V6_FIXTURE)
        malformed["itemizations"][0]["adjustment_rows"][0]["kind"] = "unplanned_adjustment"
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(malformed)

    def test_each_adjustment_class_rejects_kind_label_and_authority_mutations(self) -> None:
        expected = (
            ("nominee_distribution", "Nominee Distribution", "demo.family.nominee"),
            ("accrued_interest", "Accrued Interest", "demo.family.accrued-interest"),
            ("abp_adjustment", "ABP Adjustment", "demo.family.abp-adjustment"),
        )
        for index, (kind, label, family) in enumerate(expected):
            next_kind, next_label, next_family = expected[(index + 1) % len(expected)]
            with self.subTest(kind=kind, mutation="label"):
                malformed = _load(V6_FIXTURE)
                row = malformed["itemizations"][0]["adjustment_rows"][index]
                row["label"] = next_label
                result = _package_result(malformed)
                self.assertIn("ATTACHMENT_ADJUSTMENT_LABEL_MISMATCH", {issue.code for issue in result.issues})
            with self.subTest(kind=kind, mutation="kind"):
                malformed = _load(V6_FIXTURE)
                row = malformed["itemizations"][0]["adjustment_rows"][index]
                row["kind"] = next_kind
                result = _package_result(malformed)
                codes = {issue.code for issue in result.issues}
                self.assertIn("ATTACHMENT_ADJUSTMENT_LABEL_MISMATCH", codes)
                self.assertIn("ATTACHMENT_ADJUSTMENT_AUTHORITY_MISMATCH", codes)
            with self.subTest(kind=kind, mutation="authority"):
                malformed = _load(V6_FIXTURE)
                row = malformed["itemizations"][0]["adjustment_rows"][index]
                row["rows"]["source_family"] = {"id": next_family, "version": "v1"}
                result = _package_result(malformed)
                self.assertIn("ATTACHMENT_ADJUSTMENT_AUTHORITY_MISMATCH", {issue.code for issue in result.issues})


class AttachmentRuleV6Runtime(unittest.TestCase):
    def test_positive_adjustment_row_is_subtracted_and_published(self) -> None:
        result = _run(_load(V6_FIXTURE))
        self.assertEqual(result.dispositions[0]["disposition"], "published")
        value = result.publications[0].finding["value"]
        self.assertEqual(value["itemizations"][0]["part_sum"], "60")
        self.assertEqual(
            [row["signed_sum"] for row in value["itemizations"][0]["adjustment_rows"]],
            ["-25", "-10", "-5"],
        )

    def test_whole_part_tie_out_failure_blocks_attachment(self) -> None:
        result = _run(copy.deepcopy(_load(V6_FIXTURE)), line_value="76")
        self.assertEqual(result.dispositions[0]["disposition"], "blocked")
        self.assertEqual(result.dispositions[0]["code"], ITEMIZATION_TIE_OUT_VIOLATION)


if __name__ == "__main__":
    unittest.main()
