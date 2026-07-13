"""Source Completeness Track 4: 1099-INT box-1 content and B1 subtotal.

ADR-0015 statement-instance identity and ADR-0016 exact family meaning as
committed production content: the box-1 fact type keys on payer and
logical statement instance (never evidence), the family declaration and
adopted mapping validate as a pair, the one aggregation rule publishes
the B1 subtotal symbol only — no Form 1040 line-2b binding exists.
"""

import copy
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.package_validation import validate_package
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import InputFinding, RunContext, RunResult, SourceFact, run
from packages.derivation.source_authority import (
    SourceAuthorityError,
    audit_collect_authority,
)
from packages.kernel.schema_registry import SchemaRegistry, SchemaValidationError
from packages.tax import statements
from packages.tax.loader import (
    TAX_CONTENT_DIR,
    load_closure_mappings,
    load_f1099int_bundle,
    load_form_fields,
    load_source_families,
    tax_registry,
)

SCENARIOS = Path("packages/sample_data/tax/scenarios")
EXAMPLES = Path("packages/sample_data/tax/examples")

BOX1_FACT_TYPE = "tax.us.2025.f1099int.box1-interest"
CLOSURE_FACT_TYPE = "tax.us.2025.f1099int.b1.source-closure"
FAMILY_ID = "tax.us.2025.f1099int.b1"
RULE_ID = "tax.us.2025.rule.f1099int-b1-subtotal"
PACKAGE_ID = "tax.us.2025.package.interest-slice"
SUBTOTAL_SYMBOL = "tax.us.2025.interest.b1-subtotal"


def _load(path: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(path.read_text("utf-8"))
    return loaded


class VocabularyContract(unittest.TestCase):
    """ADR-0015: statement-keyed identity; ADR-0017: horizon-keyed closure."""

    registry: SchemaRegistry
    fact_types: dict[str, dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = tax_registry()
        cls.fact_types = {
            ft["id"]: ft for ft in load_f1099int_bundle(cls.registry)["fact_types"]
        }

    def test_bundle_carries_exactly_the_two_fact_types(self) -> None:
        self.assertEqual(
            sorted(self.fact_types), sorted([BOX1_FACT_TYPE, CLOSURE_FACT_TYPE])
        )

    def test_box1_identity_is_payer_statement_year_never_evidence(self) -> None:
        keys = {k["name"]: k for k in self.fact_types[BOX1_FACT_TYPE]["identity_keys"]}
        self.assertEqual(sorted(keys), ["payer", "statement", "tax-year"])
        self.assertEqual(keys["payer"]["entity_kind"], "tax.us.interest-payer")
        self.assertEqual(keys["statement"]["entity_kind"], "tax.us.1099int-statement")
        self.assertEqual(
            keys["tax-year"], {"name": "tax-year", "kind": "literal", "values": ["2025"]}
        )

    def test_closure_is_keyed_on_the_family_horizon(self) -> None:
        closure = self.fact_types[CLOSURE_FACT_TYPE]
        keys = {k["name"]: k for k in closure["identity_keys"]}
        self.assertEqual(keys["family-horizon"]["entity_kind"], "kernel.family-horizon")
        self.assertEqual(closure["nature"], "determinable")
        self.assertEqual(closure["value_schema"], {"type": "boolean"})

    def test_evidence_key_kind_has_no_schema_branch(self) -> None:
        box1 = copy.deepcopy(self.fact_types[BOX1_FACT_TYPE])
        box1["identity_keys"].append(
            {"name": "upload", "kind": "evidence", "evidence_kind": "tax.us.1099int-upload"}
        )
        with self.assertRaises(SchemaValidationError):
            self.registry.validate_declared(box1)

    def test_two_same_payer_statement_instances_are_distinct_entities(self) -> None:
        one = _load(EXAMPLES / "entity.1099int-stmt-alpha-1.json")
        two = _load(EXAMPLES / "entity.1099int-stmt-alpha-2.json")
        self.assertEqual(one["kind"], two["kind"])
        self.assertNotEqual(one["id"], two["id"])


class FamilyAndMapping(unittest.TestCase):
    """ADR-0014/0016 as committed, pair-validated adopted content."""

    def test_family_and_mapping_load_as_a_valid_pair(self) -> None:
        families = load_source_families()
        mappings = load_closure_mappings()
        self.assertIn(FAMILY_ID, families)
        mapping = next(m for m in mappings.values() if m["family"]["id"] == FAMILY_ID)
        self.assertEqual(mapping["member_fact_type"], BOX1_FACT_TYPE)
        self.assertEqual(mapping["closure_fact_type"], CLOSURE_FACT_TYPE)
        self.assertEqual(mapping["admits_symbol"], SUBTOTAL_SYMBOL)

    def test_the_exact_claim_says_box1_only(self) -> None:
        family = load_source_families()[FAMILY_ID]
        self.assertIn("box 1 only", family["closure_claim"])
        self.assertIn("line 2b", family["closure_claim"])
        self.assertEqual(family["authorizes_subtotal"], SUBTOTAL_SYMBOL)

    def test_rule_collects_the_family_and_publishes_its_subtotal(self) -> None:
        rule = _load(TAX_CONTENT_DIR / "rule.f1099int-b1-subtotal.json")
        families = load_source_families()
        mappings = list(load_closure_mappings().values())
        audit_collect_authority([rule], mappings, list(families.values()))
        self.assertEqual(rule["publishes"], SUBTOTAL_SYMBOL)
        self.assertEqual(rule["role"], "computation")

    def test_a_broadened_rule_fails_the_authority_audit(self) -> None:
        rule = _load(TAX_CONTENT_DIR / "rule.f1099int-b1-subtotal.json")
        rule["publishes"] = "tax.us.2025.interest.total-taxable"
        with self.assertRaisesRegex(SourceAuthorityError, "authorizes only"):
            audit_collect_authority(
                [rule],
                list(load_closure_mappings().values()),
                list(load_source_families().values()),
            )

    def test_no_form_field_binds_the_b1_subtotal(self) -> None:
        # ADR-0016 decision 5 / milestone non-goal: no line-2b citizen.
        for field in load_form_fields().values():
            self.assertNotEqual(field["binds_symbol"], SUBTOTAL_SYMBOL)


class StatementMechanics(unittest.TestCase):
    """ADR-0015 decision 5: deterministic sameness without evidence keys."""

    def key(self, ref: str) -> statements.StatementKey:
        return statements.statement_key("demo-payer-bank-alpha", "2025", ref)

    def test_two_same_payer_returns_are_distinct_new_originals(self) -> None:
        recorded = frozenset({self.key("a")})
        self.assertEqual(
            statements.classify_assertion(self.key("b"), recorded, corrected=False),
            statements.NEW_ORIGINAL,
        )

    def test_replayed_same_return_is_a_rejected_duplicate(self) -> None:
        recorded = frozenset({self.key("a")})
        self.assertEqual(
            statements.classify_assertion(self.key("a"), recorded, corrected=False),
            statements.DUPLICATE,
        )

    def test_corrected_copy_of_recorded_return_is_a_correction(self) -> None:
        recorded = frozenset({self.key("a")})
        self.assertEqual(
            statements.classify_assertion(self.key("a"), recorded, corrected=True),
            statements.CORRECTION,
        )

    def test_correction_without_a_target_is_rejected(self) -> None:
        with self.assertRaisesRegex(statements.StatementIdentityError, "must correct"):
            statements.classify_assertion(self.key("a"), frozenset(), corrected=True)

    def test_evidence_flavored_reference_is_rejected(self) -> None:
        for ref in ("upload-3", "scan.2025.pdf", "document-7", "evidence:9"):
            with self.subTest(ref=ref):
                with self.assertRaises(statements.StatementIdentityError):
                    self.key(ref)

    def test_payer_account_keying_would_collide_the_two_slip_case(self) -> None:
        # The ADR-0015 rejected alternative, reproduced: keying on payer
        # (or payer+account) alone merges two same-account returns that
        # the statement key keeps distinct.
        first, second = self.key("a"), self.key("b")
        self.assertNotEqual(first, second)
        payer_account_key = (first.payer_id, first.tax_year)
        self.assertEqual(payer_account_key, (second.payer_id, second.tax_year))

    def test_statement_entity_ids_are_deterministic(self) -> None:
        self.assertEqual(
            statements.statement_entity_id(self.key("a")),
            "stmt.demo-payer-bank-alpha.2025.a",
        )
        example = _load(EXAMPLES / "entity.1099int-stmt-alpha-1.json")
        self.assertEqual(example["id"], statements.statement_entity_id(self.key("a")))


class PackageClosure(unittest.TestCase):
    def test_interest_package_closes_and_owns_its_symbol(self) -> None:
        schemas = DerivationSchemas()
        rule = _load(TAX_CONTENT_DIR / "rule.f1099int-b1-subtotal.json")
        package = _load(TAX_CONTENT_DIR / "package.interest-slice.json")
        result = validate_package(package, {(rule["id"], rule["version"]): rule}, schemas)
        self.assertTrue(result.ok, msg=str(result.issues))
        self.assertEqual(result.output_owners[SUBTOTAL_SYMBOL], RULE_ID)


class ScenarioRuns(unittest.TestCase):
    NAMES = ("single_1099int", "two_1099int_same_payer", "present_zero_1099int")

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)

    def _context(self, name: str) -> RunContext:
        scenario = _load(SCENARIOS / name / "scenario.json")
        return RunContext(
            run_id=scenario["run_id"],
            rules=scenario["rules"],
            parameters={p["id"]: p for p in scenario["parameters"]},
            canon=self.canon,
            inputs=[InputFinding(**i) for i in scenario["inputs"]],
            sources=[SourceFact(**s) for s in scenario["sources"]],
            adoption_pin=scenario["adoption_pin"],
            governance_pins=scenario["governance_pins"],
        )

    def _blob(self, result: RunResult) -> str:
        findings = sorted((p.finding for p in result.publications), key=lambda f: f["symbol"])
        return json.dumps(findings, sort_keys=True, separators=(",", ":"))

    def test_values_and_two_runner_parity(self) -> None:
        expected = {
            "single_1099int": "120",
            "two_1099int_same_payer": "155",
            "present_zero_1099int": "0",
        }
        for name, value in expected.items():
            with self.subTest(scenario=name):
                ctx = self._context(name)
                primary = run(ctx, self.schemas)
                published = {p.finding["symbol"]: p.finding["value"] for p in primary.publications}
                self.assertEqual(published[SUBTOTAL_SYMBOL], value)
                self.assertEqual(self._blob(primary), self._blob(run_reference(ctx, self.schemas)))

    def test_present_computed_zero_pins_its_source_never_closure(self) -> None:
        result = run(self._context("present_zero_1099int"), self.schemas)
        self.assertEqual(result.blocked, [])
        finding = result.publications[0].finding
        pinned = {p["id"] for p in finding["pins"]}
        self.assertIn("demo-finding-1099int-alpha-a-box1", pinned)
        for pin_id in pinned:
            self.assertNotIn("closure", pin_id)
            self.assertNotIn(FAMILY_ID, {pin_id})

    def test_cli_goldens_are_stable(self) -> None:
        for name in self.NAMES:
            with self.subTest(scenario=name):
                expected_text = (SCENARIOS / name / "expected" / "report.txt").read_text("utf-8")
                completed = subprocess.run(
                    [sys.executable, "-m", "packages.derivation.runners.derive",
                     "--scenario", str(SCENARIOS / name / "scenario.json")],
                    capture_output=True, text=True, check=True,
                )
                self.assertEqual(completed.stdout, expected_text)


class DataSafety(unittest.TestCase):
    def test_no_private_markers_or_account_identifiers(self) -> None:
        # Interest fixtures are a natural leak surface for real-looking
        # account numbers: forbid long digit runs alongside path markers.
        # Hex lookarounds exempt content-addressed hash ids, whose digit
        # runs sit inside longer hexadecimal strings.
        forbidden = ("/Users/", "/private/", "local-data/", "uploads/")
        digit_run = re.compile(r"(?<![0-9a-f])\d{6,}(?![0-9a-f])")
        roots = [TAX_CONTENT_DIR, EXAMPLES, SCENARIOS]
        for root in roots:
            for path in Path(root).rglob("*"):
                if not path.is_file():
                    continue
                text = path.read_text("utf-8")
                with self.subTest(path=str(path)):
                    self.assertFalse(any(marker in text for marker in forbidden))
                    self.assertIsNone(digit_run.search(text.replace("2025", "")))


if __name__ == "__main__":
    unittest.main()
