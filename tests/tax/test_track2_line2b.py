"""Track 2 verification: Form 1040 Line 2b interest composition.

Verifies:
- Form 1040 Line 2b sums B1, B3, OID, and Non-Form interest subtotals.
- Line 2b blocks if any of the constituent interest source families is unclosed.
- Package validation passes for the interest-slice package.
- Parity between forward and reference runners.
"""

import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.package_validation import validate_package
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from packages.derivation.source_authority import ClosureFindingRecord

CONTENT = Path("packages/content/tax/2025")
LINE2B_SYMBOL = "tax.us.2025.interest.taxable-total"


def _load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def _member_filename(member_id: str) -> str:
    suffix = member_id.replace("tax.us.2025.", "")
    if suffix.endswith(".vocabulary"):
        suffix = suffix.replace(".vocabulary", ".bundle")
    elif suffix in {"f1099int.b1", "f1099int.b3", "f1099oid.b1", "non-form-interest"}:
        suffix = "family." + suffix.replace(".", "-")
    elif suffix == "form1040.line-2b":
        suffix = suffix + ".form-field"
    return f"{suffix}.json"


class TestLine2bInterestComposition(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)

        # Load all interest slice rules
        package = _load(CONTENT / "package.interest-slice.json")
        self.rules = []
        for member in package["members"]:
            if member["role"] == "computation":
                filename = _member_filename(member["id"])
                self.rules.append(_load(CONTENT / filename))

    def _context(
        self,
        sources: list[dict[str, Any]],
        findings: list[dict[str, Any]],
        closed_horizons: dict[str, str],
    ) -> RunContext:
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

        return RunContext(
            run_id="test-run-line2b",
            rules=self.rules,
            parameters={},
            canon=self.canon,
            inputs=[
                InputFinding(
                    finding_id="rounding-convention",
                    role="input",
                    symbol="rounding.convention",
                    value="half_up",
                )
            ],
            sources=[SourceFact(**s) for s in sources],
            adoption_pin={
                "id": "tax.us.2025.package.interest-slice",
                "role": "adoption",
                "version": "v1",
            },
            governance_pins=[
                {
                    "id": "governance.constitution",
                    "role": "governance",
                    "version": "v1",
                }
            ],
            family_declarations=families,
            closure_mappings=mappings,
            closure_findings=[ClosureFindingRecord(**f) for f in findings],
            current_horizons=closed_horizons,
        )

    def test_package_validation_passes(self) -> None:
        package = _load(CONTENT / "package.interest-slice.json")
        corpus = {}
        for member in package["members"]:
            filename = _member_filename(member["id"])
            corpus[(member["id"], member["version"])] = _load(CONTENT / filename)

        result = validate_package(package, corpus, self.schemas)
        self.assertTrue(result.ok, msg=str(result.issues))

    def test_all_closed_totals_correctly(self) -> None:
        sources = [
            # B1 interest
            {
                "finding_id": "demo-finding-b1-1",
                "name": "tax.us.2025.f1099int.box1-interest",
                "value": "10",
            },
            # B3 interest
            {
                "finding_id": "demo-finding-b3-1",
                "name": "tax.us.2025.f1099int.box3-interest",
                "value": "20",
            },
            # OID interest
            {
                "finding_id": "demo-finding-oid-1",
                "name": "tax.us.2025.f1099oid.box1-interest-oid",
                "value": "30",
            },
            # Non-form interest
            {
                "finding_id": "demo-finding-nf-1",
                "name": "tax.us.2025.non-form-interest.amount",
                "value": "5",
            },
        ]

        findings = [
            # Attestations of closure
            {
                "fact_type": "tax.us.2025.f1099int.b1.source-closure",
                "finding_id": "closure-b1",
                "horizon_id": "h-b1",
                "value": True,
            },
            {
                "fact_type": "tax.us.2025.f1099int.b3.source-closure",
                "finding_id": "closure-b3",
                "horizon_id": "h-b3",
                "value": True,
            },
            {
                "fact_type": "tax.us.2025.f1099oid.b1.source-closure",
                "finding_id": "closure-oid",
                "horizon_id": "h-oid",
                "value": True,
            },
            {
                "fact_type": "tax.us.2025.non-form-interest.source-closure",
                "finding_id": "closure-nf",
                "horizon_id": "h-nf",
                "value": True,
            },
        ]

        closed_horizons = {
            "tax.us.2025.f1099int.b1": "h-b1",
            "tax.us.2025.f1099int.b3": "h-b3",
            "tax.us.2025.f1099oid.b1": "h-oid",
            "tax.us.2025.non-form-interest": "h-nf",
        }

        ctx = self._context(sources, findings, closed_horizons)
        primary = run(ctx, self.schemas)
        reference = run_reference(ctx, self.schemas)

        # Check publications parity (B1, B3, OID, Non-form subtotals + Line 2b total = 5)
        self.assertEqual(len(primary.publications), 5)
        self.assertEqual(len(reference.publications), 5)

        published_primary = {
            p.finding["symbol"]: p.finding["value"] for p in primary.publications
        }
        published_reference = {
            p.finding["symbol"]: p.finding["value"] for p in reference.publications
        }

        self.assertEqual(published_primary[LINE2B_SYMBOL], "65")
        self.assertEqual(published_reference[LINE2B_SYMBOL], "65")

    def test_unclosed_source_blocks_line_2b(self) -> None:
        sources = [
            {
                "finding_id": "demo-finding-b1-1",
                "name": "tax.us.2025.f1099int.box1-interest",
                "value": "10",
            }
        ]

        # Only B1, B3, OID are closed; non-form is unclosed (no closure finding)
        findings = [
            {
                "fact_type": "tax.us.2025.f1099int.b1.source-closure",
                "finding_id": "closure-b1",
                "horizon_id": "h-b1",
                "value": True,
            },
            {
                "fact_type": "tax.us.2025.f1099int.b3.source-closure",
                "finding_id": "closure-b3",
                "horizon_id": "h-b3",
                "value": True,
            },
            {
                "fact_type": "tax.us.2025.f1099oid.b1.source-closure",
                "finding_id": "closure-oid",
                "horizon_id": "h-oid",
                "value": True,
            },
        ]

        closed_horizons = {
            "tax.us.2025.f1099int.b1": "h-b1",
            "tax.us.2025.f1099int.b3": "h-b3",
            "tax.us.2025.f1099oid.b1": "h-oid",
            "tax.us.2025.non-form-interest": "h-nf",
        }

        ctx = self._context(sources, findings, closed_horizons)
        primary = run(ctx, self.schemas)

        # Non-form subtotal blocks, and Line 2b also blocks because of require_closed on non-form-interest
        published_symbols = {p.finding["symbol"] for p in primary.publications}
        self.assertNotIn(LINE2B_SYMBOL, published_symbols)
        self.assertNotIn(
            "tax.us.2025.interest.non-form-subtotal", published_symbols
        )

        # Line 2b rule should be in blocked
        blocked_rules = {b["artifact_id"] for b in primary.blocked}
        self.assertIn("tax.us.2025.rule.form1040-line2b", blocked_rules)


if __name__ == "__main__":
    unittest.main()
