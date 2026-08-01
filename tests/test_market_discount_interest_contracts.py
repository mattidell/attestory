"""MD-C1/C2/C4/C5 contract evidence for payer-reported market-discount interest."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any, Callable, cast

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    PackageValidation,
    load_published_citizen_checksums,
    validate_package,
)
from packages.kernel.contribution import ContributionError, apply_contribution_batch
from packages.kernel.findings import apply_act, project
from tools import generate_market_discount_interest as generator


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"


def _load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def _corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        value = _load(path)
        if isinstance(value.get("id"), str) and isinstance(value.get("version"), str):
            corpus[(value["id"], value["version"])] = value
    return corpus


def _validate(
    package: dict[str, Any],
    corpus: dict[tuple[str, str], dict[str, Any]] | None = None,
) -> PackageValidation:
    return validate_package(
        package,
        corpus or _corpus(),
        DerivationSchemas(),
        load_published_citizen_checksums(CONTENT / "published-packages.v5.json"),
    )


class IdentityAndSourceAdmission(unittest.TestCase):
    def test_md_c1_identity_is_logical_not_evidence(self) -> None:
        """MD-C1: both families key on tax year + payer + logical statement."""
        for bundle_name, fact_index in (
            ("f1099int-b10.bundle.json", 0),
            ("f1099oid-b5.bundle.json", 0),
        ):
            with self.subTest(bundle_name=bundle_name):
                bundle = _load(CONTENT / bundle_name)
                amount = bundle["fact_types"][fact_index]
                self.assertEqual(
                    [key["name"] for key in amount["identity_keys"]],
                    ["payer", "statement", "tax-year"],
                )
                self.assertEqual(amount["value_schema"], {"minimum": 0, "type": "number"})
                identity_text = json.dumps(amount["identity_keys"])
                for forbidden in ("evidence", "file", "upload", "document", "scan"):
                    self.assertNotIn(forbidden, identity_text)

    def test_md_n3_negative_amount_is_schema_invalid(self) -> None:
        """MD-N3: both families reject a negative contribution value atomically."""
        import jsonschema

        for bundle_name in ("f1099int-b10.bundle.json", "f1099oid-b5.bundle.json"):
            with self.subTest(bundle_name=bundle_name):
                bundle = _load(CONTENT / bundle_name)
                value_schema = bundle["fact_types"][0]["value_schema"]
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(-1, value_schema)

    def test_md_n3_n4_contribution_failures_are_atomic(self) -> None:
        """MD-N3 MD-N4: bad value or evidence-key identity lands no partial state."""
        from tests.test_market_discount_interest_integration import _act, _md_acts

        registry = DerivationSchemas().registry
        base_acts = _md_acts(b10_values=[])
        evidence_id = "demo.md.evidence.invalid"
        evidence_act = _act(len(base_acts), "evidence-submitted", {"evidence": {
            "schema": "evidence.v1", "id": evidence_id,
            "kind": "demo.statement.f1099int-b10", "label": "Synthetic invalid box-10 statement",
            "content": {"value": -1},
        }})
        state = apply_act(project(tuple(base_acts), registry), evidence_act, registry)
        contribution_id = "demo.md.contribution.invalid"
        contribution = _act(len(base_acts) + 1, "contribution", {"contribution": {
            "schema": "contribution.v1", "id": contribution_id,
            "evidence_id": evidence_id, "content": {"mode": "manual-entry", "synthetic": True},
        }})
        fact_ids = (
            "tax.us.2025.f1099int.box10-market-discount|payer=demo.md.payer,statement=demo.md.b10.stmt.0,tax-year=2025",
            "tax.us.2025.f1099int.box10-market-discount|payer=demo.md.payer,evidence=demo.md.evidence.invalid,tax-year=2025",
        )
        for fact_id in fact_ids:
            with self.subTest(fact_id=fact_id):
                transition = _act(len(base_acts) + 2, "member-transition", {
                    "family": {"id": "tax.us.2025.f1099int.b10", "version": "v1"},
                    "scope": {"tax-year": "2025", "subject": "demo.primary"},
                    "member": {"action": "assert", "finding": {
                        "schema": "finding.v2", "id": "demo.md.finding.invalid",
                        "fact_id": fact_id, "value": -1, "basis": "documentary",
                        "evidence_ids": [evidence_id], "contribution_id": contribution_id,
                    }},
                    "successor": {"id": "demo.md.invalid.h1", "predecessor": "demo.md.b10.h0"},
                })
                with self.assertRaises(ContributionError) as raised:
                    apply_contribution_batch(
                        state, contribution_act=contribution, successor_acts=[transition],
                        registry=registry, record_id="demo.md.invalid.batch",
                    )
                terminal = cast(dict[str, Any], getattr(raised.exception, "terminal_record"))
                self.assertEqual(terminal["facts_asserted"], [])
                self.assertNotIn(contribution_id, state.contributions)
                self.assertNotIn("demo.md.finding.invalid", state.findings)


class SuccessorPackageContracts(unittest.TestCase):
    def setUp(self) -> None:
        self.package = _load(CONTENT / "package.core-calculations.v10.json")

    def assert_issue(self, package: dict[str, Any], code: str) -> None:
        result = _validate(package)
        self.assertFalse(result.ok)
        self.assertIn(code, {issue.code for issue in result.issues})

    def test_md_p10_v10_graph_is_valid_and_v9_is_unchanged_input(self) -> None:
        """MD-P10: v10 validates while the generator emits no historical v9/v4 path."""
        self.assertTrue(_validate(self.package).ok)
        self.assertTrue(_validate(_load(CONTENT / "package.core-calculations.v9.json")).ok)
        emitted = set(generator.render_content_files())
        self.assertNotIn("package.core-calculations.v9.json", emitted)
        self.assertNotIn("published-packages.v4.json", emitted)

    def test_md_n5_composition_family_subtotal_substitution_rejects(self) -> None:
        """MD-N5: package validation rejects a substituted composition slot."""
        corpus = _corpus()
        comp = copy.deepcopy(corpus[("tax.us.2025.interest-composition", "v3")])
        comp["constituents"][-1]["authorizes_subtotal"] = "tax.us.2025.interest.b10-market-discount-subtotal"
        corpus[(comp["id"], comp["version"])] = comp
        result = validate_package(self.package, corpus, DerivationSchemas())
        self.assertIn("COMPOSITION_FAMILY_SUBTOTAL_MISMATCH", {i.code for i in result.issues})

    def test_md_n5_composition_omitted_slot_rejects(self) -> None:
        """MD-N5: omitting a market-discount slot breaks the seven-family bijection."""
        corpus = _corpus()
        comp = copy.deepcopy(corpus[("tax.us.2025.interest-composition", "v3")])
        comp["constituents"].pop()
        corpus[(comp["id"], comp["version"])] = comp
        result = validate_package(self.package, corpus, DerivationSchemas())
        self.assertIn("COMPOSITION_SLOT_BIJECTION_MISMATCH", {i.code for i in result.issues})

    def test_md_n6_missing_closure_read_ref_or_pin_rejects(self) -> None:
        """MD-N6: every line-2b surface is bijective with composition v3."""
        base = _corpus()
        mutations: tuple[tuple[Callable[[dict[str, Any]], object], str], ...] = (
            (lambda rule: rule["when"]["args"].pop(), "COMPOSITION_CLOSURE_READS_MISMATCH"),
            (lambda rule: rule["value"]["args"].pop(), "COMPOSITION_VALUE_REFS_MISMATCH"),
            (lambda rule: rule["pins"].pop(), "COMPOSITION_INPUT_PINS_MISMATCH"),
        )
        for mutation, code in mutations:
            with self.subTest(code=code):
                corpus = copy.deepcopy(base)
                rule = corpus[("tax.us.2025.rule.form1040-line2b", "v3")]
                mutation(rule)
                result = validate_package(self.package, corpus, DerivationSchemas())
                self.assertIn(code, {i.code for i in result.issues})

    def test_md_n10_mixed_successor_graph_rejects_older_fields(self) -> None:
        """MD-N10: v10 rejects composition/line2b/attachment/field version mixing."""
        replacements = (
            ("tax.us.2025.interest-composition", "taxable-interest-composition.v1", "v2"),
            ("tax.us.2025.rule.form1040-line2b", "rule-artifact.v3", "v2"),
            ("tax.us.2025.form1040.line-2b", "form-field.v3", "v3"),
            ("tax.us.2025.rule.attachment.schedule-b", "attachment-rule.v2", "v2"),
        )
        for member_id, schema, version in replacements:
            with self.subTest(member_id=member_id, version=version):
                package = copy.deepcopy(self.package)
                member = next(m for m in package["members"] if m["id"] == member_id)
                member.update(schema=schema, version=version)
                result = _validate(package)
                self.assertFalse(result.ok)
                self.assertTrue(
                    any(
                        issue.code
                        in {
                            "COMPOSITION_SLOT_BIJECTION_MISMATCH",
                            "COMPOSITION_FAMILY_SUBTOTAL_MISMATCH",
                            "COMPOSITION_PIN_MISMATCH",
                            "COMPOSITION_VALUE_REFS_MISMATCH",
                            "COMPOSITION_CLOSURE_READS_MISMATCH",
                            "COMPOSITION_INPUT_PINS_MISMATCH",
                            "ATTACHMENT_COMPOSITION_BIJECTION_MISMATCH",
                            "ATTACHMENT_COMPOSITION_ABSENT",
                            "MEMBER_SCHEMA_INVALID",
                            "MD_SUCCESSOR_GRAPH_MIXED",
                        }
                        for issue in result.issues
                    ),
                    result.issues,
                )


if __name__ == "__main__":
    unittest.main()
