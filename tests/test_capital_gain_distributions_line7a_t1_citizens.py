"""Track 1 Capital-Gain Distributions / Line 7a: schema and content citizens (ADR-0050)."""

from __future__ import annotations

import hashlib
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

ROOT = Path("packages/sample_data/capital_gain_distributions_line7a_t1")
EXAMPLES = ROOT / "examples"
NEGATIVES = ROOT / "negatives"

COMPONENT_IDS = (
    "tax.us.2025.exception1.only-box2a-capital-gains",
    "tax.us.2025.exception1.no-capital-losses",
    "tax.us.2025.exception1.no-qof-deferral",
    "tax.us.2025.exception1.no-boxes-2b-2c-2d",
)

COMMITTED_CITIZENS = (
    "exception1.bundle.json",
    "schedule-d-required.conclusion-binding.json",
    "f1099div-box2a.bundle.json",
    "family.f1099div-2a.json",
    "closure-mapping.f1099div-2a.json",
    "dividend-universe.v2.json",
    "quantity.capital-gain-distributions.json",
    "citation.form1040.line-7a.json",
    "citation.form1040.line-7b.json",
    "form1040.line-7a.form-field.json",
    "form1040.line-7b.form-field.json",
)

HISTORICAL_BYTES = {
    "packages/content/tax/2025/dividend-universe.json": (
        "8e0b04bc0b5d813250f76ae48151c28a7a38d853e691c913a9cbe43a7214b037"
    ),
    "packages/content/tax/2025/f1099div.bundle.json": (
        "31783368886d228b3c6f1dfbaf889289fe4afbfc22b8188c384730935eaaf75f"
    ),
    "packages/content/tax/2025/qdcg.bundle.json": (
        "10cdca546eaedffccbcd11aa09e6f7637be890874f13a3cb2bd44b8f9f9876a0"
    ),
    "packages/schemas/derivation/dividend-universe.v1.schema.json": (
        "63f52279c298827e10f2b82884175a6c42d7851c65eb0655cdcfc2e687139feb"
    ),
    "packages/schemas/kernel/quantity-vocabulary.v2.schema.json": (
        "83588761674fe3d7b008fea5a00287b555357e0fccac9e728d6b9a23332b4a3a"
    ),
}


def load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TrackOneRegistry(unittest.TestCase):
    registry: ClassVar[SchemaRegistry]

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = SchemaRegistry([KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR, TAX_SCHEMA_DIR])


class NewSchemasPublished(TrackOneRegistry):
    def test_new_schema_ids_are_published(self) -> None:
        ids = set(self.registry.schema_ids())
        self.assertIn("dividend-universe.v2", ids)
        self.assertIn("checked-conclusion-binding.v1", ids)
        self.assertIn("quantity-vocabulary.v3", ids)

    def test_manifest_adds_only_new_filenames(self) -> None:
        der = load(DERIVATION_SCHEMA_DIR / "published.json")
        self.assertIn("dividend-universe.v2.schema.json", der)
        self.assertIn("checked-conclusion-binding.v1.schema.json", der)
        self.assertEqual(
            der["dividend-universe.v1.schema.json"],
            HISTORICAL_BYTES["packages/schemas/derivation/dividend-universe.v1.schema.json"],
        )
        ker = load(KERNEL_SCHEMA_DIR / "published.json")
        self.assertIn("quantity-vocabulary.v3.schema.json", ker)
        self.assertEqual(
            ker["quantity-vocabulary.v2.schema.json"],
            HISTORICAL_BYTES["packages/schemas/kernel/quantity-vocabulary.v2.schema.json"],
        )


class PositiveInstances(TrackOneRegistry):
    def test_sample_positives_for_new_schemas_validate(self) -> None:
        paths = sorted(EXAMPLES.glob("*.json"))
        self.assertEqual(len(paths), 3)
        for path in paths:
            with self.subTest(path=path.name):
                self.registry.validate_declared(load(path))

    def test_every_committed_track1_citizen_validates(self) -> None:
        for name in COMMITTED_CITIZENS:
            with self.subTest(name=name):
                citizen = load(TAX_CONTENT_DIR / name)
                self.registry.validate_declared(citizen)
                if name.endswith(".bundle.json"):
                    for fact_type in citizen["fact_types"]:
                        self.registry.validate_declared(fact_type)


class ExceptionOneComponents(TrackOneRegistry):
    def test_four_components_have_yes_no_domain_no_default_free_supersession(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "exception1.bundle.json")
        by_id = {ft["id"]: ft for ft in bundle["fact_types"]}
        for fact_id in COMPONENT_IDS:
            with self.subTest(fact_id=fact_id):
                ft = by_id[fact_id]
                self.assertEqual(ft["value_schema"], {"enum": ["yes", "no"]})
                self.assertNotIn("optional_default", ft)
                self.assertEqual(ft["supersession"], {"policy": "free"})
                self.assertEqual(ft["identity_keys"], [
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]}
                ])

    def test_component_value_schema_rejects_non_yes_no_values(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "exception1.bundle.json")
        by_id = {ft["id"]: ft for ft in bundle["fact_types"]}
        for fact_id in COMPONENT_IDS:
            validator = jsonschema.Draft202012Validator(by_id[fact_id]["value_schema"])
            with self.subTest(fact_id=fact_id):
                self.assertEqual(list(validator.iter_errors("yes")), [])
                self.assertEqual(list(validator.iter_errors("no")), [])
                self.assertTrue(list(validator.iter_errors(True)))
                self.assertTrue(list(validator.iter_errors(False)))
                self.assertTrue(list(validator.iter_errors("maybe")))
                self.assertTrue(list(validator.iter_errors(None)))

    def test_components_are_distinct_from_checked_conclusion(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "exception1.bundle.json")
        ids = {ft["id"] for ft in bundle["fact_types"]}
        self.assertIn("tax.us.2025.schedule-d-required.conclusion", ids)
        self.assertTrue(set(COMPONENT_IDS).isdisjoint({"tax.us.2025.schedule-d-required.conclusion"}))
        self.assertNotIn("tax.us.2025.schedule-d-required", ids)


class CheckedConclusionBinding(TrackOneRegistry):
    def test_committed_binding_pins_c1_through_c4_and_truth_table(self) -> None:
        binding = load(TAX_CONTENT_DIR / "schedule-d-required.conclusion-binding.json")
        self.registry.validate_declared(binding)
        self.assertEqual(binding["publishes"], "tax.us.2025.schedule-d-required.conclusion")
        self.assertEqual(
            binding["conclusion_fact_type"],
            {"id": "tax.us.2025.schedule-d-required.conclusion", "version": "v1"},
        )
        aliases = [row["alias"] for row in binding["components"]]
        self.assertEqual(sorted(aliases), ["C1", "C2", "C3", "C4"])
        by_alias = {row["alias"]: row["fact_type"]["id"] for row in binding["components"]}
        self.assertEqual(by_alias["C1"], COMPONENT_IDS[0])
        self.assertEqual(by_alias["C2"], COMPONENT_IDS[1])
        self.assertEqual(by_alias["C3"], COMPONENT_IDS[2])
        self.assertEqual(by_alias["C4"], COMPONENT_IDS[3])
        self.assertEqual(
            binding["truth_table"]["all_present_all_yes"],
            {"conclusion": "no", "direct_route": "eligible"},
        )
        self.assertEqual(
            binding["truth_table"]["all_present_any_no"],
            {"conclusion": "yes", "direct_route": "guard_inapplicable"},
        )
        self.assertEqual(
            binding["truth_table"]["any_missing"],
            {
                "conclusion": "unpublished",
                "disposition": "blocked",
                "code": "DEPENDENCY_ABSENT",
                "name_missing": "every_missing_component",
            },
        )
        self.assertEqual(
            binding["direct_pin_boundary"]["conclusion_pins"],
            "exactly_the_current_component_findings",
        )
        self.assertTrue(
            binding["direct_pin_boundary"][
                "historical_contributed_schedule_d_required_is_not_direct_route_authority"
            ]
        )


class Box2aSourcePath(TrackOneRegistry):
    def test_member_identity_follows_1099div_statement_pattern(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "f1099div-box2a.bundle.json")
        member = next(
            ft
            for ft in bundle["fact_types"]
            if ft["id"] == "tax.us.2025.f1099div.box2a-capital-gain-distribution"
        )
        keys = {k["name"]: k for k in member["identity_keys"]}
        self.assertEqual(keys["payer"]["entity_kind"], "tax.us.dividend-payer")
        self.assertEqual(keys["statement"]["entity_kind"], "tax.us.1099div-statement")
        self.assertEqual(keys["tax-year"]["values"], ["2025"])
        self.assertTrue(member["source_amount"])
        self.assertEqual(
            member["quantity"],
            {"id": "tax.us.2025.quantity.capital-gain-distributions", "version": "v1"},
        )
        self.assertEqual(member["supersession"], {"policy": "free"})

    def test_family_and_closure_mapping_load_through_production_loader(self) -> None:
        families = load_source_families(self.registry)
        mappings = load_closure_mappings(self.registry)
        family = families["tax.us.2025.f1099div.2a"]
        mapping = mappings["tax.us.2025.closure-mapping.f1099div-2a"]
        self.assertEqual(
            family["member_predicate"]["fact_type"],
            "tax.us.2025.f1099div.box2a-capital-gain-distribution",
        )
        self.assertEqual(family["authorizes_subtotal"], "tax.us.2025.dividends.2a-subtotal")
        self.assertEqual(mapping["family"], {"id": "tax.us.2025.f1099div.2a", "version": "v1"})
        self.assertEqual(
            mapping["member_fact_type"],
            {"id": "tax.us.2025.f1099div.box2a-capital-gain-distribution", "version": "v1"},
        )
        self.assertEqual(
            mapping["closure_fact_type"],
            {"id": "tax.us.2025.f1099div.2a.source-closure", "version": "v1"},
        )
        self.assertEqual(mapping["closure_horizon_key"], "family-horizon")
        self.assertEqual(mapping["admits_symbol"], "tax.us.2025.dividends.2a-subtotal")
        self.assertEqual(mapping["admission"], {"condition": "current-literal-true"})
        claim = family["closure_claim"].lower()
        self.assertIn("box 2a", claim)
        # Claim explicitly excludes line-7a completeness (does not assert it).
        self.assertIn("line 7a completeness", claim)
        self.assertTrue(
            "says nothing" in claim or "never" in claim or "not" in claim,
            "closure claim must exclude line-7a completeness, not assert it",
        )

    def test_historical_1a_1b_families_unchanged(self) -> None:
        families = load_source_families(self.registry)
        self.assertEqual(
            families["tax.us.2025.f1099div.1a"]["member_predicate"]["fact_type"],
            "tax.us.2025.f1099div.box1a-ordinary",
        )
        self.assertEqual(
            families["tax.us.2025.f1099div.1b"]["member_predicate"]["fact_type"],
            "tax.us.2025.f1099div.box1b-qualified",
        )


class SuccessorUniverseAndResidual(TrackOneRegistry):
    def test_successor_universe_composable_set_and_residual(self) -> None:
        universe = load(TAX_CONTENT_DIR / "dividend-universe.v2.json")
        self.registry.validate_declared(universe)
        self.assertEqual(universe["id"], "tax.us.2025.dividend-universe")
        self.assertEqual(universe["version"], "v2")
        boxes = {entry["box"]: entry["family"]["id"] for entry in universe["composable_boxes"]}
        self.assertEqual(
            boxes,
            {
                "1a": "tax.us.2025.f1099div.1a",
                "1b": "tax.us.2025.f1099div.1b",
                "2a": "tax.us.2025.f1099div.2a",
            },
        )
        self.assertEqual(set(universe["recorded_non_composable_boxes"]), {"3", "5", "7", "12"})
        self.assertNotIn("2a", universe["recorded_non_composable_boxes"])
        self.assertEqual(
            universe["recorded_boxes_fact_type"],
            {"id": "tax.us.2025.f1099div.recorded-boxes", "version": "v2"},
        )
        self.assertEqual(
            universe["capital_gain_signal"],
            {
                "box": "2a",
                "signal": "CAPITAL_GAIN_DISTRIBUTION_RECORDED",
                "source": "current_successor_family_member",
            },
        )

    def test_residual_recorded_boxes_v2_omits_2a(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "f1099div-box2a.bundle.json")
        residual = next(
            ft
            for ft in bundle["fact_types"]
            if ft["id"] == "tax.us.2025.f1099div.recorded-boxes" and ft["version"] == "v2"
        )
        props = residual["value_schema"]["properties"]
        self.assertEqual(set(props), {"3", "5", "7", "12"})
        self.assertNotIn("2a", props)
        validator = jsonschema.Draft202012Validator(residual["value_schema"])
        ok = {"3": None, "5": None, "7": None, "12": None}
        self.assertEqual(list(validator.iter_errors(ok)), [])
        with_2a = {"2a": 1.0, "3": None, "5": None, "7": None, "12": None}
        self.assertTrue(list(validator.iter_errors(with_2a)))


class Line7FormAndCitation(TrackOneRegistry):
    def test_line_7a_and_7b_form_fields_load_through_production_loader(self) -> None:
        fields = load_form_fields(self.registry)
        line_7a = fields["tax.us.2025.form1040.line-7a"]
        line_7b = fields["tax.us.2025.form1040.line-7b"]
        self.assertEqual(line_7a["schema"], "form-field.v3")
        self.assertEqual(line_7b["schema"], "form-field.v3")
        self.assertEqual(line_7a["line"], "7a")
        self.assertEqual(line_7b["line"], "7b")
        self.assertEqual(line_7a["binds_symbol"], "tax.us.2025.capital-gains.line7a-total")
        self.assertEqual(line_7b["binds_symbol"], "tax.us.2025.schedule-d-required.conclusion")
        self.assertEqual(
            line_7a["citation"],
            {"id": "tax.us.2025.citation.form1040.line-7a", "version": "v1"},
        )
        self.assertEqual(
            line_7b["citation"],
            {"id": "tax.us.2025.citation.form1040.line-7b", "version": "v1"},
        )

    def test_line_7b_citation_identity_and_cardinality(self) -> None:
        citation = load(TAX_CONTENT_DIR / "citation.form1040.line-7b.json")
        self.registry.validate_declared(citation)
        self.assertEqual(citation["id"], "tax.us.2025.citation.form1040.line-7b")
        self.assertEqual(citation["version"], "v1")
        self.assertEqual(
            citation["authority"],
            {"family": "irs-instructions", "form_id": "1040", "tax_year": 2025},
        )
        line_7b = load(TAX_CONTENT_DIR / "form1040.line-7b.form-field.json")
        # Exactly one citation pin object (not an array; not absent; exact identity).
        self.assertIsInstance(line_7b["citation"], dict)
        self.assertEqual(
            line_7b["citation"],
            {"id": "tax.us.2025.citation.form1040.line-7b", "version": "v1"},
        )
        self.assertIn("If Exception 1 applies", line_7b["description"])
        self.assertIn("Schedule D not required", line_7b["description"])


class NamedNegatives(TrackOneRegistry):
    SCHEMA_NEGATIVES = (
        "checked-conclusion-binding.v1.incomplete-components.json",
        "checked-conclusion-binding.v1.incorrect-truth-table.json",
        "source-family.v1.box2a-invalid-member.json",
        "source-closure-mapping.v2.box2a-invalid-admission.json",
        "dividend-universe.v2.residual-includes-2a.json",
        "dividend-universe.v2.missing-composable-2a.json",
        "form-field.v3.line-7b-multi-citation.json",
    )

    def test_schema_negatives_reject(self) -> None:
        for name in self.SCHEMA_NEGATIVES:
            with self.subTest(name=name):
                with self.assertRaises(SchemaValidationError):
                    self.registry.validate_declared(load(NEGATIVES / name))

    def test_boolean_component_domain_is_not_the_accepted_yes_no_contract(self) -> None:
        # The fact-type schema admits arbitrary value_schema objects; the accepted
        # component contract is the {yes, no} enum on the committed citizens. This
        # named negative records a boolean domain shape that must not be used.
        negative = load(NEGATIVES / "fact-type.v2.exception1-boolean-domain.json")
        self.registry.validate_declared(negative)
        self.assertEqual(negative["value_schema"], {"type": "boolean"})
        bundle = load(TAX_CONTENT_DIR / "exception1.bundle.json")
        for ft in bundle["fact_types"]:
            if ft["id"] in COMPONENT_IDS:
                self.assertEqual(ft["value_schema"], {"enum": ["yes", "no"]})

    def test_line_7b_wrong_citation_identity_is_not_the_committed_pin(self) -> None:
        negative = load(NEGATIVES / "form-field.v3.line-7b-wrong-citation-id.json")
        self.registry.validate_declared(negative)
        committed = load(TAX_CONTENT_DIR / "form1040.line-7b.form-field.json")
        self.assertNotEqual(negative["citation"]["id"], committed["citation"]["id"])
        self.assertEqual(
            committed["citation"]["id"],
            "tax.us.2025.citation.form1040.line-7b",
        )


class HistoricalImmutability(TrackOneRegistry):
    def test_historical_content_and_schemas_are_byte_for_byte_unchanged(self) -> None:
        for path, digest in HISTORICAL_BYTES.items():
            with self.subTest(path=path):
                self.assertEqual(sha256_file(Path(path)), digest)

    def test_historical_dividend_universe_v1_still_validates(self) -> None:
        universe = load(TAX_CONTENT_DIR / "dividend-universe.json")
        self.assertEqual(universe["schema"], "dividend-universe.v1")
        self.assertEqual(universe["version"], "v1")
        self.registry.validate_declared(universe)
        self.assertEqual(
            {entry["box"] for entry in universe["composable_boxes"]},
            {"1a", "1b"},
        )
        self.assertIn("2a", universe["recorded_non_composable_boxes"])

    def test_historical_recorded_boxes_v1_still_carries_2a(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "f1099div.bundle.json")
        recorded = next(
            ft for ft in bundle["fact_types"] if ft["id"] == "tax.us.2025.f1099div.recorded-boxes"
        )
        self.assertEqual(recorded["version"], "v1")
        self.assertIn("2a", recorded["value_schema"]["properties"])


if __name__ == "__main__":
    unittest.main()
