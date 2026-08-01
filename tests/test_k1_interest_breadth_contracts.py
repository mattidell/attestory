"""K1-C1/C2/C4/C5 contract evidence for Form-1065 K-1 box-5 breadth."""

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
from packages.kernel.schema_registry import SchemaValidationError
from packages.kernel.contribution import ContributionError, apply_contribution_batch
from packages.kernel.findings import apply_act, project
from tools import generate_k1_interest_breadth as generator


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "k1_interest_breadth"


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
        load_published_citizen_checksums(CONTENT / "published-packages.v4.json"),
    )


class IdentityAndSourceAdmission(unittest.TestCase):
    def test_k1_p1_p3_p4_and_k1_n4_identity_is_logical_not_evidence(self) -> None:
        """K1-P1 K1-P3 K1-P4 K1-N4: exact Form-1065 statement identity."""
        bundle = _load(CONTENT / "form1065-k1.bundle.json")
        amount = bundle["fact_types"][0]
        self.assertEqual(
            [key["name"] for key in amount["identity_keys"]],
            ["partnership", "k1-statement", "tax-year"],
        )
        self.assertEqual(amount["value_schema"], {"minimum": 0, "type": "number"})
        identity_text = json.dumps(amount["identity_keys"])
        for forbidden in ("evidence", "file", "upload", "document", "scan"):
            self.assertNotIn(forbidden, identity_text)

    def test_k1_n3_negative_amount_is_schema_invalid(self) -> None:
        """K1-N3: the member value schema rejects a negative contribution value."""
        bundle = _load(CONTENT / "form1065-k1.bundle.json")
        value_schema = bundle["fact_types"][0]["value_schema"]
        import jsonschema

        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(-1, value_schema)

    def test_k1_n3_n4_contribution_failures_are_atomic(self) -> None:
        """K1-N3 K1-N4: bad value or evidence-key identity lands no partial state."""
        from tests.test_k1_interest_breadth_integration import _act, _k1_acts

        registry = DerivationSchemas().registry
        base_acts = _k1_acts(k1_values=[])
        evidence_id = "demo.k1.evidence.invalid"
        evidence_act = _act(len(base_acts), "evidence-submitted", {"evidence": {
            "schema": "evidence.v1", "id": evidence_id,
            "kind": "demo.statement.form1065-k1", "label": "Synthetic invalid K-1",
            "content": {"value": -1},
        }})
        state = apply_act(project(tuple(base_acts), registry), evidence_act, registry)
        contribution_id = "demo.k1.contribution.invalid"
        contribution = _act(len(base_acts) + 1, "contribution", {"contribution": {
            "schema": "contribution.v1", "id": contribution_id,
            "evidence_id": evidence_id, "content": {"mode": "manual-entry", "synthetic": True},
        }})
        fact_ids = (
            "tax.us.2025.form1065-k1.box5-interest|partnership=demo.k1.partnership,k1-statement=demo.k1.statement.0,tax-year=2025",
            "tax.us.2025.form1065-k1.box5-interest|partnership=demo.k1.partnership,evidence=demo.k1.evidence.invalid,tax-year=2025",
        )
        for fact_id in fact_ids:
            with self.subTest(fact_id=fact_id):
                transition = _act(len(base_acts) + 2, "member-transition", {
                    "family": {"id": "tax.us.2025.form1065-k1.box5", "version": "v1"},
                    "scope": {"tax-year": "2025", "subject": "demo.primary"},
                    "member": {"action": "assert", "finding": {
                        "schema": "finding.v2", "id": "demo.k1.finding.invalid",
                        "fact_id": fact_id, "value": -1, "basis": "documentary",
                        "evidence_ids": [evidence_id], "contribution_id": contribution_id,
                    }},
                    "successor": {"id": "demo.k1.invalid.h1", "predecessor": "demo.k1.h0"},
                })
                with self.assertRaises(ContributionError) as raised:
                    apply_contribution_batch(
                        state, contribution_act=contribution, successor_acts=[transition],
                        registry=registry, record_id="demo.k1.invalid.batch",
                    )
                terminal = cast(dict[str, Any], getattr(raised.exception, "terminal_record"))
                self.assertEqual(terminal["facts_asserted"], [])
                self.assertNotIn(contribution_id, state.contributions)
                self.assertNotIn("demo.k1.finding.invalid", state.findings)


class SuccessorPackageContracts(unittest.TestCase):
    def setUp(self) -> None:
        self.package = _load(CONTENT / "package.core-calculations.v9.json")

    def assert_issue(self, package: dict[str, Any], code: str) -> None:
        result = _validate(package)
        self.assertFalse(result.ok)
        self.assertIn(code, {issue.code for issue in result.issues})

    def test_k1_p10_v9_graph_is_valid_and_v8_is_unchanged_input(self) -> None:
        """K1-P10: v9 validates while the generator emits no historical v8/v3 path."""
        self.assertTrue(_validate(self.package).ok)
        self.assertTrue(_validate(_load(CONTENT / "package.core-calculations.v8.json")).ok)
        emitted = {path.name for path in generator.render_content_files()}
        self.assertNotIn("package.core-calculations.v8.json", emitted)
        self.assertNotIn("published-packages.v3.json", emitted)

    def test_k1_n5_composition_family_subtotal_substitution_rejects(self) -> None:
        """K1-N5: package validation rejects a substituted composition slot."""
        corpus = _corpus()
        comp = copy.deepcopy(corpus[("tax.us.2025.interest-composition", "v2")])
        comp["constituents"][-1]["authorizes_subtotal"] = "tax.us.2025.interest.non-form-subtotal"
        corpus[(comp["id"], comp["version"])] = comp
        result = validate_package(self.package, corpus, DerivationSchemas())
        self.assertIn("COMPOSITION_FAMILY_SUBTOTAL_MISMATCH", {i.code for i in result.issues})

    def test_k1_n6_missing_closure_read_ref_or_pin_rejects(self) -> None:
        """K1-N6: every line-2b surface is bijective with composition v2."""
        base = _corpus()
        mutations: tuple[tuple[Callable[[dict[str, Any]], object], str], ...] = (
            (lambda rule: rule["when"]["args"].pop(), "COMPOSITION_CLOSURE_READS_MISMATCH"),
            (lambda rule: rule["value"]["args"].pop(), "COMPOSITION_VALUE_REFS_MISMATCH"),
            (lambda rule: rule["pins"].pop(), "COMPOSITION_INPUT_PINS_MISMATCH"),
        )
        for mutation, code in mutations:
            with self.subTest(code=code):
                corpus = copy.deepcopy(base)
                rule = corpus[("tax.us.2025.rule.form1040-line2b", "v2")]
                mutation(rule)
                result = validate_package(self.package, corpus, DerivationSchemas())
                self.assertIn(code, {i.code for i in result.issues})

    def test_k1_n12_mixed_successor_graph_rejects_both_older_fields(self) -> None:
        """K1-N12: v9 rejects line2b/attachment/field historical mixing."""
        replacements = (
            ("tax.us.2025.rule.form1040-line2b", "rule-artifact.v2", "v1"),
            ("tax.us.2025.rule.attachment.schedule-b", "attachment-rule.v1", "v1"),
            ("tax.us.2025.form1040.line-2b", "form-field.v2", "v1"),
            ("tax.us.2025.form1040.line-2b", "form-field.v3", "v2"),
        )
        for member_id, schema, version in replacements:
            with self.subTest(member_id=member_id, version=version):
                package = copy.deepcopy(self.package)
                member = next(m for m in package["members"] if m["id"] == member_id)
                member.update(schema=schema, version=version)
                self.assert_issue(package, "K1_SUCCESSOR_GRAPH_MIXED")


class ImmutableSuccessorSchemas(unittest.TestCase):
    def test_positive_examples_are_fully_schema_resolved(self) -> None:
        schemas = DerivationSchemas()
        for name in ("attachment-rule.v2.json", "artifact-package.v6.json"):
            schemas.validate_declared(_load(FIXTURES / "schema" / "examples" / name))

    def test_attachment_authority_is_required(self) -> None:
        instance = _load(FIXTURES / "schema" / "examples" / "attachment-rule.v2.json")
        del instance["itemizations"][0]["authority"]
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(instance)

    def test_isolated_successor_schema_negatives_reject(self) -> None:
        schemas = DerivationSchemas()
        negative_dir = FIXTURES / "schema" / "negatives"
        names = {
            "attachment-rule.v2.missing-authority.json",
            "attachment-rule.v2.empty-row-sets.json",
            "attachment-rule.v2.missing-subtotal.json",
            "attachment-rule.v2.wrong-collect-op.json",
            "artifact-package.v6.attachment-not-admitted.json",
            "artifact-package.v6.attachment-wrong-role.json",
        }
        self.assertEqual(names, {path.name for path in negative_dir.glob("*.json")})
        for name in sorted(names):
            with self.subTest(name=name), self.assertRaises(SchemaValidationError):
                schemas.validate_declared(_load(negative_dir / name))


if __name__ == "__main__":
    unittest.main()
