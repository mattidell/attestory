"""Track 1 Dividends and Schedule B Slice: schema citizens (ADR-0035/0036)."""

import json
import unittest
from pathlib import Path
from typing import Any, ClassVar, cast

import jsonschema

from packages.derivation.loader import DERIVATION_SCHEMA_DIR
from packages.kernel.schema_registry import KERNEL_SCHEMA_DIR, SchemaRegistry, SchemaValidationError
from packages.tax.loader import (
    TAX_CONTENT_DIR,
    TAX_SCHEMA_DIR,
    load_closure_mappings,
    load_form_fields,
    load_source_families,
)

ROOT = Path("packages/sample_data/dsbs_t1")
EXAMPLES = ROOT / "examples"
NEGATIVES = ROOT / "negatives"

DIV_CONTENT = (
    "f1099div.bundle.json",
    "family.f1099div-1a.json",
    "family.f1099div-1b.json",
    "closure-mapping.f1099div-1a.json",
    "closure-mapping.f1099div-1b.json",
    "quantity.ordinary-dividends.json",
    "quantity.qualified-dividends.json",
)


def load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


class TrackOneRegistry(unittest.TestCase):
    registry: ClassVar[SchemaRegistry]

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = SchemaRegistry([KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR, TAX_SCHEMA_DIR])


class DividendStatementAndFamilyCitizens(TrackOneRegistry):
    """ADR-0035 decisions 1-2: statement identity, two independent per-box families."""

    def test_every_committed_dividend_citizen_is_a_published_schema_instance(self) -> None:
        for name in DIV_CONTENT:
            with self.subTest(name=name):
                self.registry.validate_declared(load(TAX_CONTENT_DIR / name))

    def test_bundle_fact_types_validate_individually(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "f1099div.bundle.json")
        self.assertEqual(len(bundle["fact_types"]), 5)
        for fact_type in bundle["fact_types"]:
            with self.subTest(fact_type=fact_type["id"]):
                self.registry.validate_declared(fact_type)

    def test_statement_identity_follows_the_adr_0015_pattern(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "f1099div.bundle.json")
        by_id = {ft["id"]: ft for ft in bundle["fact_types"]}
        for fact_id in (
            "tax.us.2025.f1099div.box1a-ordinary",
            "tax.us.2025.f1099div.box1b-qualified",
            "tax.us.2025.f1099div.recorded-boxes",
        ):
            with self.subTest(fact_id=fact_id):
                keys = {k["name"]: k for k in by_id[fact_id]["identity_keys"]}
                self.assertEqual(keys["payer"]["entity_kind"], "tax.us.dividend-payer")
                self.assertEqual(keys["statement"]["entity_kind"], "tax.us.1099div-statement")
                self.assertEqual(keys["tax-year"]["values"], ["2025"])

    def test_families_are_independent_and_loader_admits_them(self) -> None:
        families = load_source_families()
        mappings = load_closure_mappings()
        subtotals = {}
        for family_id in ("tax.us.2025.f1099div.1a", "tax.us.2025.f1099div.1b"):
            with self.subTest(family_id=family_id):
                self.assertIn(family_id, families)
                mapping = mappings[f"tax.us.2025.closure-mapping.f1099div-{family_id.rsplit('.', 1)[1]}"]
                self.assertEqual(mapping["family"]["id"], family_id)
                self.assertEqual(mapping["closure_horizon_key"], "family-horizon")
                subtotals[family_id] = families[family_id]["authorizes_subtotal"]
        # Two independent authorized subtotals: neither family can stand in for the other.
        self.assertEqual(len(set(subtotals.values())), 2)

    def test_recorded_boxes_value_schema_admits_declared_absence_only(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "f1099div.bundle.json")
        recorded = next(
            ft for ft in bundle["fact_types"] if ft["id"] == "tax.us.2025.f1099div.recorded-boxes"
        )
        validator = jsonschema.Draft202012Validator(recorded["value_schema"])
        declared_all_absent = {"2a": None, "3": None, "5": None, "7": None, "12": None}
        self.assertEqual(list(validator.iter_errors(declared_all_absent)), [])
        box_2a_present = {"2a": 125.5, "3": None, "5": None, "7": None, "12": None}
        self.assertEqual(list(validator.iter_errors(box_2a_present)), [])
        with self.subTest(negative="undeclared box"):
            self.assertTrue(list(validator.iter_errors({**declared_all_absent, "9": 10})))
        with self.subTest(negative="missing declared box is never assumed absent"):
            self.assertTrue(list(validator.iter_errors({"2a": None, "3": None, "5": None, "7": None})))
        with self.subTest(negative="composable box smuggled into the recorded surface"):
            self.assertTrue(list(validator.iter_errors({**declared_all_absent, "1a": 100})))


class DividendUniverseCitizen(TrackOneRegistry):
    """ADR-0035 decision 3: the declared dividend universe."""

    def test_committed_universe_and_example_are_schema_instances(self) -> None:
        for path in (TAX_CONTENT_DIR / "dividend-universe.json", EXAMPLES / "dividend-universe.v1.json"):
            with self.subTest(path=path.name):
                self.registry.validate_declared(load(path))

    def test_named_negatives_are_rejected(self) -> None:
        for name in (
            "dividend-universe.v1.composable-without-family.json",
            "dividend-universe.v1.box-in-both-sets.json",
            "dividend-universe.v1.undeclared-box.json",
        ):
            with self.subTest(name=name):
                with self.assertRaises(SchemaValidationError):
                    self.registry.validate_declared(load(NEGATIVES / name))

    def test_duplicated_composable_box_cannot_displace_the_other(self) -> None:
        universe = load(EXAMPLES / "dividend-universe.v1.json")
        universe["composable_boxes"] = [
            {"box": "1a", "family": {"id": "demo.family.div-1a", "version": "v1"}},
            {"box": "1a", "family": {"id": "demo.family.div-1a-again", "version": "v1"}},
        ]
        with self.assertRaises(SchemaValidationError):
            self.registry.validate_declared(universe)

    def test_committed_universe_pins_resolve_to_committed_citizens(self) -> None:
        universe = load(TAX_CONTENT_DIR / "dividend-universe.json")
        families = load_source_families()
        bound = {entry["box"]: entry["family"]["id"] for entry in universe["composable_boxes"]}
        self.assertEqual(bound, {"1a": "tax.us.2025.f1099div.1a", "1b": "tax.us.2025.f1099div.1b"})
        for family_id in bound.values():
            self.assertIn(family_id, families)
        bundle = load(TAX_CONTENT_DIR / "f1099div.bundle.json")
        fact_ids = {ft["id"] for ft in bundle["fact_types"]}
        self.assertIn(universe["recorded_boxes_fact_type"]["id"], fact_ids)
        self.assertEqual(
            universe["capital_gain_signal"],
            {"box": "2a", "signal": "CAPITAL_GAIN_DISTRIBUTION_RECORDED"},
        )


if __name__ == "__main__":
    unittest.main()
