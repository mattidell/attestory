"""Track 1 verification: W-2 vocabulary and form-field contract as published.

Every committed positive instance validates against the *published* schema
files; every committed negative is an isolated single-defect instance the
schema must reject. Content assertions guard the ratified ADR-0011/0012
commitments that schema validation alone cannot express (slip-keyed identity,
determinable closure, field/symbol distinctness).
"""

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.schema_registry import (
    SchemaRegistry,
    SchemaRegistryError,
    SchemaValidationError,
)
from packages.tax.loader import (
    FORM_FIELD_SCHEMA,
    TAX_CONTENT_DIR,
    TAX_SCHEMA_DIR,
    load_form_fields,
    load_w2_bundle,
    tax_registry,
)

SAMPLE_ROOT = Path("packages/sample_data/tax")
EXAMPLES = SAMPLE_ROOT / "examples"
NEGATIVES = SAMPLE_ROOT / "negatives"

LINE_1A_ID = "tax.us.2025.form1040.line-1a"
BOX1_FACT_TYPE = "tax.us.2025.w2.box1-wages"
CLOSURE_FACT_TYPE = "tax.us.2025.w2.source-closure"
DISPOSITIONS = (
    "published_value",
    "computed_zero",
    "closure_backed_zero",
    "blocked",
    "guard_inapplicable",
)


def _load(path: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(path.read_text("utf-8"))
    return loaded


class TaxRegistryFixture(unittest.TestCase):
    registry: SchemaRegistry

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = tax_registry()

    def assert_rejected(self, instance: dict[str, Any]) -> None:
        with self.assertRaises(SchemaValidationError):
            self.registry.validate_declared(instance)


class RegistryIntegrity(TaxRegistryFixture):
    def test_combined_registry_spans_kernel_and_tax_families(self) -> None:
        ids = self.registry.schema_ids()
        self.assertIn(FORM_FIELD_SCHEMA, ids)
        self.assertIn("fact-type.v1", ids)
        self.assertIn("bundle.v1", ids)
        self.assertIn("entity.v1", ids)

    def test_mutated_published_tax_schema_is_a_registry_defect(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mutated = Path(tmp) / "tax"
            shutil.copytree(TAX_SCHEMA_DIR, mutated)
            schema_path = mutated / "form-field.v1.schema.json"
            document = json.loads(schema_path.read_text("utf-8"))
            document["additionalProperties"] = True
            schema_path.write_text(json.dumps(document), "utf-8")
            with self.assertRaises(SchemaRegistryError):
                SchemaRegistry(mutated)


class PositiveInstances(TaxRegistryFixture):
    def test_all_committed_examples_validate(self) -> None:
        paths = sorted(EXAMPLES.glob("*.json"))
        self.assertTrue(paths, "expected committed positive examples")
        for path in paths:
            with self.subTest(example=path.name):
                self.registry.validate_declared(_load(path))

    def test_production_content_loads_and_validates(self) -> None:
        load_w2_bundle(self.registry)
        fields = load_form_fields(self.registry)
        self.assertIn(LINE_1A_ID, fields)


class CommittedNegatives(TaxRegistryFixture):
    def test_every_committed_negative_is_rejected(self) -> None:
        paths = sorted(NEGATIVES.glob("*.json"))
        self.assertTrue(paths, "expected committed negative instances")
        for path in paths:
            with self.subTest(negative=path.name):
                self.assert_rejected(_load(path))


class FormFieldContract(TaxRegistryFixture):
    """ADR-0012: five dispositions, immutable versioned content, no stored state."""

    def line_1a(self) -> dict[str, Any]:
        return load_form_fields(self.registry)[LINE_1A_ID]

    def test_line_1a_carries_all_five_disposition_instructions(self) -> None:
        field = self.line_1a()
        self.assertEqual(tuple(sorted(field["dispositions"])), tuple(sorted(DISPOSITIONS)))

    def test_field_is_distinct_from_its_output_symbol(self) -> None:
        field = self.line_1a()
        self.assertNotEqual(field["id"], field["binds_symbol"])
        # The symbol is form-agnostic presentation-side binding: the rule
        # publishes it without knowing which official fields render it.
        self.assertNotIn("form1040", field["binds_symbol"])

    def test_line_1a_names_the_official_2025_locator(self) -> None:
        field = self.line_1a()
        self.assertEqual(field["form"]["authority"], "IRS")
        self.assertEqual(field["form"]["form_id"], "1040")
        self.assertEqual(field["form"]["tax_year"], 2025)
        self.assertEqual(field["line"], "1a")

    def test_zero_dispositions_share_glyph_but_never_explanation(self) -> None:
        d = self.line_1a()["dispositions"]
        self.assertEqual(d["computed_zero"]["render"], d["closure_backed_zero"]["render"])
        self.assertNotEqual(d["computed_zero"]["explain"], d["closure_backed_zero"]["explain"])

    def test_each_missing_disposition_is_rejected(self) -> None:
        for name in DISPOSITIONS:
            field = self.line_1a()
            del field["dispositions"][name]
            with self.subTest(disposition=name):
                self.assert_rejected(field)

    def test_undeclared_disposition_class_is_rejected(self) -> None:
        field = self.line_1a()
        field["dispositions"]["blocked_unclosed"] = {"render": "", "explain": "prototype vocabulary"}
        self.assert_rejected(field)

    def test_stored_rendered_state_is_rejected(self) -> None:
        field = self.line_1a()
        field["current_disposition"] = "published_value"
        self.assert_rejected(field)


class W2Vocabulary(TaxRegistryFixture):
    """ADR-0011: slip-keyed wage identity and determinable affirmative closure."""

    def fact_types(self) -> dict[str, dict[str, Any]]:
        bundle = load_w2_bundle(self.registry)
        return {ft["id"]: ft for ft in bundle["fact_types"]}

    def test_bundle_carries_exactly_the_track1_fact_types(self) -> None:
        self.assertEqual(
            sorted(self.fact_types()), sorted([BOX1_FACT_TYPE, CLOSURE_FACT_TYPE])
        )

    def test_box1_identity_is_employer_slip_and_year_never_evidence(self) -> None:
        keys = {k["name"]: k for k in self.fact_types()[BOX1_FACT_TYPE]["identity_keys"]}
        self.assertEqual(sorted(keys), ["employer", "tax-year", "w2-slip"])
        self.assertEqual(keys["employer"]["kind"], "entity")
        self.assertEqual(keys["w2-slip"]["kind"], "entity")
        self.assertEqual(keys["w2-slip"]["entity_kind"], "tax.us.w2-slip")
        self.assertEqual(keys["tax-year"], {"name": "tax-year", "kind": "literal", "values": ["2025"]})

    def test_two_same_employer_slips_are_distinct_entities(self) -> None:
        slip_1 = _load(EXAMPLES / "entity.w2-slip-alpha-1.json")
        slip_2 = _load(EXAMPLES / "entity.w2-slip-alpha-2.json")
        self.assertEqual(slip_1["kind"], slip_2["kind"])
        self.assertNotEqual(slip_1["id"], slip_2["id"])

    def test_closure_is_determinable_boolean_not_elective(self) -> None:
        closure = self.fact_types()[CLOSURE_FACT_TYPE]
        self.assertEqual(closure["nature"], "determinable")
        self.assertEqual(closure["value_schema"], {"type": "boolean"})

    def test_evidence_key_kind_has_no_schema_branch(self) -> None:
        # Article 1 / E1.1: the published key kinds are entity and literal;
        # a source-flavor key must fail the oneOf outright.
        box1 = copy.deepcopy(self.fact_types()[BOX1_FACT_TYPE])
        box1["identity_keys"].append(
            {"name": "upload", "kind": "evidence", "evidence_kind": "tax.us.w2-upload"}
        )
        self.assert_rejected(box1)


class DataSafety(unittest.TestCase):
    def test_committed_tax_files_have_no_private_markers(self) -> None:
        forbidden = ("/Users/", "/private/", "local-data/", "uploads/")
        for root in (SAMPLE_ROOT, TAX_CONTENT_DIR, TAX_SCHEMA_DIR):
            for path in Path(root).rglob("*"):
                if not path.is_file():
                    continue
                text = path.read_text("utf-8")
                with self.subTest(path=str(path)):
                    self.assertFalse(any(marker in text for marker in forbidden))


if __name__ == "__main__":
    unittest.main()
