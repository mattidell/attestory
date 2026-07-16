"""Track 3 verification: core tax calculations, standard deduction selectors, and tax progressive brackets.
"""

import json
import unittest
from pathlib import Path
from typing import Any, cast
from decimal import Decimal

from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.runner import InputFinding, RunContext, RunResult, SourceFact, run
from packages.derivation.reference_runner import run_reference
from packages.derivation.source_authority import ClosureFindingRecord
from packages.derivation.evaluator import EvalBlocked, BLOCK_INVALID, BLOCK_CATEGORICAL_DOMAIN_MISMATCH

CONTENT = Path("packages/content/tax/2025")


def _load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def _member_filename(member_id: str) -> str:
    suffix = member_id.replace("tax.us.2025.", "")
    if suffix == "rule.w2-box1-to-line1a":
        suffix = "rule.wages-line1a"
    elif suffix.endswith(".vocabulary"):
        suffix = suffix.replace(".vocabulary", ".bundle")
    elif suffix in {"f1099int.b1", "f1099int.b3", "f1099oid.b1", "non-form-interest"}:
        suffix = "family." + suffix.replace(".", "-")
    elif suffix == "form1040.line-1a":
        suffix = suffix + ".form-field"
    elif suffix == "form1040.line-2b":
        suffix = suffix + ".form-field"
    elif suffix == "form1040.line-9":
        suffix = suffix + ".form-field"
    elif suffix == "form1040.line-11":
        suffix = suffix + ".form-field"
    elif suffix == "form1040.line-12":
        suffix = suffix + ".form-field"
    elif suffix == "form1040.line-15":
        suffix = suffix + ".form-field"
    elif suffix == "form1040.line-16":
        suffix = suffix + ".form-field"
    return f"{suffix}.json"


class TestCoreTaxConditions(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)

        package = _load(CONTENT / "package.core-calculations.json")
        self.rules = []
        for member in package["members"]:
            if member["role"] == "computation":
                filename = _member_filename(member["id"])
                self.rules.append(_load(CONTENT / filename))

        # Load fact types
        bundles = [
            _load(CONTENT / "core_calculations.bundle.json"),
            _load(CONTENT / "interest_composition.bundle.json"),
            _load(CONTENT / "w2.bundle.json"),
        ]
        self.fact_types = []
        for b in bundles:
            self.fact_types.extend(b["fact_types"])

        self.input_bindings = package["input_bindings"]

        # Load parameters
        self.parameters = {
            "demo.parameter.standard-deduction-base.2025": _load(CONTENT / "parameter.standard-deduction-base.json"),
            "demo.parameter.additional-deduction-rate.2025": _load(CONTENT / "parameter.additional-deduction-rate.json"),
            "demo.parameter.tax-brackets.2025": _load(CONTENT / "parameter.tax-brackets.json"),
            "tax.us.2025.parameter.default-false": _load(CONTENT / "parameter.default-false.json"),
            "tax.us.2025.parameter.default-zero": _load(CONTENT / "parameter.default-zero.json"),
        }

    def _context(
        self,
        filing_status: str,
        taxpayer_over_65: bool | None,
        taxpayer_blind: bool | None,
        wages: str,
        spouse_over_65: bool | None = None,
        spouse_blind: bool | None = None,
        itemized_deductions: str | None = None,
    ) -> RunContext:
        inputs = [
            InputFinding(finding_id="rounding-convention", role="input", symbol="rounding.convention", value="half_up"),
            InputFinding(finding_id="filing-status", role="input", symbol="filing_status", value=filing_status),
        ]

        if taxpayer_over_65 is not None:
            inputs.append(InputFinding(finding_id="tp-over-65", role="input", symbol="taxpayer_over_65", value=taxpayer_over_65))
        if taxpayer_blind is not None:
            inputs.append(InputFinding(finding_id="tp-blind", role="input", symbol="taxpayer_blind", value=taxpayer_blind))
        if spouse_over_65 is not None:
            inputs.append(InputFinding(finding_id="sp-over-65", role="input", symbol="spouse_over_65", value=spouse_over_65))
        if spouse_blind is not None:
            inputs.append(InputFinding(finding_id="sp-blind", role="input", symbol="spouse_blind", value=spouse_blind))
        if itemized_deductions is not None:
            inputs.append(InputFinding(finding_id="itemized-ded", role="input", symbol="tax.us.2025.deductions.itemized", value=Decimal(itemized_deductions)))

        # Close all interest families as empty
        mappings = [
            _load(CONTENT / "closure-mapping.f1099int-b1.json"),
            _load(CONTENT / "closure-mapping.f1099int-b3.json"),
            _load(CONTENT / "closure-mapping.f1099oid-b1.json"),
            _load(CONTENT / "closure-mapping.non-form-interest.json"),
        ]
        families = [
            _load(CONTENT / "family.f1099int-b1.json"),
            _load(CONTENT / "family.f1099int-b3.json"),
            _load(CONTENT / "family.f1099oid-b1.json"),
            _load(CONTENT / "family.non-form-interest.json"),
        ]
        findings = [
            {"fact_type": "tax.us.2025.f1099int.b1.source-closure", "finding_id": "c-b1", "horizon_id": "hb1", "value": True},
            {"fact_type": "tax.us.2025.f1099int.b3.source-closure", "finding_id": "c-b3", "horizon_id": "hb3", "value": True},
            {"fact_type": "tax.us.2025.f1099oid.b1.source-closure", "finding_id": "c-oid", "horizon_id": "hoid", "value": True},
            {"fact_type": "tax.us.2025.non-form-interest.source-closure", "finding_id": "c-nf", "horizon_id": "hnf", "value": True}
        ]
        horizons = {
            "tax.us.2025.f1099int.b1": "hb1",
            "tax.us.2025.f1099int.b3": "hb3",
            "tax.us.2025.f1099oid.b1": "hoid",
            "tax.us.2025.non-form-interest": "hnf"
        }

        # Wages sources
        sources = [
            SourceFact(finding_id="w-wages", name="tax.us.2025.w2.box1-wages", value=wages)
        ]

        return RunContext(
            run_id="test-run-track3",
            rules=self.rules,
            parameters=self.parameters,
            canon=self.canon,
            inputs=inputs,
            sources=sources,
            adoption_pin={
                "id": "tax.us.2025.package.core-calculations",
                "role": "adoption",
                "version": "v1"
            },
            governance_pins=[
                {
                    "id": "governance.constitution",
                    "role": "governance",
                    "version": "v1"
                }
            ],
            family_declarations=families,
            closure_mappings=mappings,
            closure_findings=[
            ClosureFindingRecord(
                fact_type=str(f["fact_type"]),
                finding_id=str(f["finding_id"]),
                horizon_id=str(f["horizon_id"]),
                value=bool(f["value"])
            ) for f in findings
        ],
            current_horizons=horizons,
            fact_types=self.fact_types,
            input_bindings=self.input_bindings
        )

    def test_single_filer_standard_deduction_and_tax(self) -> None:
        # wages = 50000, filing_status = single, standard deduction = 15000 (defaulted demographics)
        # taxable income = 35000
        # tax brackets:
        # 11600 * 0.10 = 1160
        # (35000 - 11600) * 0.12 = 23400 * 0.12 = 2808
        # total tax = 3968
        ctx = self._context("single", None, None, "50000")
        result = run(ctx, self.schemas)

        published = {p.finding["symbol"]: p.finding["value"] for p in result.publications}
        self.assertEqual(published["demo.form1040.standard_deduction"], "15000")
        self.assertEqual(published["tax.us.2025.deductions.total"], "15000")
        self.assertEqual(published["tax.us.2025.income.taxable-income"], "35000")
        self.assertEqual(published["tax.us.2025.tax.total-tax"], "3968")

        # Test reference runner parity
        result_ref = run_reference(ctx, self.schemas)
        published_ref = {p.finding["symbol"]: p.finding["value"] for p in result_ref.publications}
        self.assertEqual(published, published_ref)

    def test_mfj_filer_with_spouse_age_addition(self) -> None:
        # wages = 120000, status = mfj, spouse over 65 = True
        # standard deduction = 30000 + 1550 = 31550
        # taxable income = 120000 - 31550 = 88450
        # tax:
        # 23200 * 0.10 = 2320
        # (88450 - 23200) * 0.12 = 65250 * 0.12 = 7830
        # total tax = 10150
        ctx = self._context("married_filing_jointly", None, None, "120000", spouse_over_65=True)
        result = run(ctx, self.schemas)

        published = {p.finding["symbol"]: p.finding["value"] for p in result.publications}
        self.assertEqual(published["demo.form1040.standard_deduction"], "31550")
        self.assertEqual(published["tax.us.2025.deductions.total"], "31550")
        self.assertEqual(published["tax.us.2025.income.taxable-income"], "88450")
        self.assertEqual(published["tax.us.2025.tax.total-tax"], "10150")

    def test_single_over_65_and_blind(self) -> None:
        # wages = 50000, single, over 65 = True, blind = True
        # standard deduction = 15000 + 2000 + 2000 = 19000
        # taxable income = 31000
        ctx = self._context("single", True, True, "50000")
        result = run(ctx, self.schemas)

        published = {p.finding["symbol"]: p.finding["value"] for p in result.publications}
        self.assertEqual(published["demo.form1040.standard_deduction"], "19000")
        self.assertEqual(published["tax.us.2025.income.taxable-income"], "31000")

    def test_itemized_deductions_override(self) -> None:
        # wages = 120000, MFJ, itemized = 35000 (overrides standard of 30000)
        # taxable income = 120000 - 35000 = 85000
        ctx = self._context("married_filing_jointly", None, None, "120000", itemized_deductions="35000")
        result = run(ctx, self.schemas)

        published = {p.finding["symbol"]: p.finding["value"] for p in result.publications}
        self.assertEqual(published["demo.form1040.standard_deduction"], "30000")
        self.assertEqual(published["tax.us.2025.deductions.total"], "35000")
        self.assertEqual(published["tax.us.2025.income.taxable-income"], "85000")

    def test_categorical_validation_invalid_enum(self) -> None:
        # Asserting an invalid filing status enum should fail validation or run-time check
        ctx = self._context("divorced", None, None, "50000")
        result = run(ctx, self.schemas)
        # Verify it blocks on DEPENDENCY_INVALID
        blocked_status = next((b for b in result.blocked if b["artifact_id"] == "tax.us.2025.rule.form1040-standard-deduction"), None)
        self.assertIsNotNone(blocked_status)
        assert blocked_status is not None
        self.assertEqual(blocked_status["code"], BLOCK_INVALID)

    def test_categorical_validation_domain_mismatch(self) -> None:
        # Run categorical compare on mismatched domains
        # We construct a context with a rule comparing filing_status to a category literal of another domain
        bad_rule = {
            "schema": "rule-artifact.v2",
            "id": "demo.rule.bad-compare",
            "version": "v1",
            "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
            "role": "computation",
            "requires": ["filing_status"],
            "pins": [{"role": "input", "id": "tax.us.2025.filing-status", "version": "v1", "origin": "assertion"}],
            "when": True,
            "value": {
                "op": "categorical_compare",
                "cmp": "eq",
                "left": { "op": "ref", "name": "filing_status" },
                "right": {
                    "op": "category_literal",
                    "fact_type": { "id": "tax.us.2025.taxpayer-over-65", "version": "v1" },
                    "value": "single"
                }
            },
            "publishes": "demo.bad-compare-out",
            "blocked": { "code": "DEPENDENCY_ABSENT", "missing": ["filing_status"] }
        }
        
        ctx = self._context("single", None, None, "50000")
        # Swap rules to only run bad rule
        ctx = RunContext(
            run_id=ctx.run_id,
            rules=[bad_rule],
            parameters=ctx.parameters,
            canon=ctx.canon,
            inputs=ctx.inputs,
            sources=ctx.sources,
            adoption_pin=ctx.adoption_pin,
            governance_pins=ctx.governance_pins,
            family_declarations=ctx.family_declarations,
            closure_mappings=ctx.closure_mappings,
            closure_findings=ctx.closure_findings,
            current_horizons=ctx.current_horizons,
            fact_types=ctx.fact_types,
            input_bindings=ctx.input_bindings
        )
        result = run(ctx, self.schemas)
        blocked_status = next((b for b in result.blocked if b["artifact_id"] == "demo.rule.bad-compare"), None)
        self.assertIsNotNone(blocked_status)
        assert blocked_status is not None
        self.assertEqual(blocked_status["code"], BLOCK_CATEGORICAL_DOMAIN_MISMATCH)


if __name__ == "__main__":
    unittest.main()
