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


class AttachmentCitizenSurface(TrackOneRegistry):
    """ADR-0036 decisions 1-5: the generic attachment rule citizen surface."""

    def test_generic_example_and_schedule_d_stub_are_schema_instances(self) -> None:
        for name in ("attachment-rule.v1.json", "attachment-rule.v1.schedule-d-stub.json"):
            with self.subTest(name=name):
                self.registry.validate_declared(load(EXAMPLES / name))

    def test_generalization_stub_shares_the_identical_schema_surface(self) -> None:
        # ADR-0036 decision 5: a second schedule is content only. Both examples
        # exercise the same closed key set; nothing on the citizen names a schedule.
        generic = load(EXAMPLES / "attachment-rule.v1.json")
        stub = load(EXAMPLES / "attachment-rule.v1.schedule-d-stub.json")
        self.assertEqual(set(generic), set(stub))
        schema_keys = set(self.registry.get("attachment-rule.v1")["properties"])
        self.assertEqual(set(generic), schema_keys)
        for key in schema_keys:
            self.assertNotIn("schedule", key)
            self.assertNotIn("part-iii", key)

    def test_completeness_value_read_before_presence_is_unrepresentable(self) -> None:
        with self.assertRaises(SchemaValidationError):
            self.registry.validate_declared(load(NEGATIVES / "attachment-rule.v1.value-before-presence.json"))

    def test_row_outside_the_declared_family_is_unrepresentable(self) -> None:
        with self.assertRaises(SchemaValidationError):
            self.registry.validate_declared(load(NEGATIVES / "attachment-rule.v1.row-outside-declared-family.json"))

    def test_rows_come_only_from_collect_members(self) -> None:
        attachment = load(EXAMPLES / "attachment-rule.v1.json")
        attachment["itemizations"][0]["rows"] = [
            {"finding_id": "demo.finding.literal-row", "value": "250.00"}
        ]
        with self.assertRaises(SchemaValidationError):
            self.registry.validate_declared(attachment)

    def test_threshold_comparison_is_pinned_strictly_greater_than(self) -> None:
        attachment = load(EXAMPLES / "attachment-rule.v1.json")
        attachment["requirement"]["comparison"] = "greater_than_or_equal"
        with self.assertRaises(SchemaValidationError):
            self.registry.validate_declared(attachment)

    def test_taxpayer_answer_pattern_pins_the_categorical_domain(self) -> None:
        answer = load(EXAMPLES / "fact-type.v2.taxpayer-answer.json")
        self.registry.validate_declared(answer)
        self.assertEqual(answer["value_schema"], {"enum": ["yes", "no"]})
        validator = jsonschema.Draft202012Validator(answer["value_schema"])
        self.assertEqual(list(validator.iter_errors("no")), [])
        for falsy in (False, True, "", 0, None):
            with self.subTest(value=falsy):
                self.assertTrue(list(validator.iter_errors(falsy)))

    def test_boolean_answer_negative_is_a_fact_type_instance_for_the_admission_guard(self) -> None:
        # fact-type.v2 legitimately admits boolean value schemas (closure
        # attestations), so this named negative is rejected at admission by
        # package validation, not by the fact-type schema.
        self.registry.validate_declared(load(NEGATIVES / "fact-type.v2.boolean-answer.json"))


class ReconciledVocabularies(TrackOneRegistry):
    """ADR-0036 production conditions 1 and 3: the versioned vocabulary change."""

    def test_reconciled_record_and_walk_instances_validate(self) -> None:
        for name in ("derivation-record.v3.json", "npe-walk.v2.json"):
            with self.subTest(name=name):
                self.registry.validate_declared(load(EXAMPLES / name))

    def test_retired_open_code_is_rejected_by_the_reconciled_vocabularies(self) -> None:
        for name in ("derivation-record.v3.retired-open-code.json", "npe-walk.v2.retired-open-code.json"):
            with self.subTest(name=name):
                with self.assertRaises(SchemaValidationError):
                    self.registry.validate_declared(load(NEGATIVES / name))

    def test_form_field_v3_carries_the_emitted_code_and_the_head_line_2b_rides_it(self) -> None:
        # `load_form_fields` returns the head field, so this deliberately does
        # not pin a version number: the subject is that whichever line-2b
        # field is current is a form-field.v3 citizen carrying the reconciled
        # closure code. Successors move the number; they must not move that.
        line_2b = load_form_fields()["tax.us.2025.form1040.line-2b"]
        self.assertEqual(line_2b["schema"], "form-field.v3")
        codes = line_2b["dispositions"]["blocked"]["codes"]
        self.assertIn("SOURCE_SET_UNCLOSED", codes)
        self.assertNotIn("SOURCE_SET_OPEN", codes)

        # Compatibility assertions for the superseded generations, which stay
        # on disk untouched and must keep validating under the same schema.
        content = EXAMPLES.parent.parent.parent / "content/tax/2025"
        for version in ("v4", "v5"):
            with self.subTest(version=version):
                field = load(content / f"form1040.line-2b.form-field.{version}.json")
                self.assertEqual(field["schema"], "form-field.v3")
                self.assertEqual(field["version"], version)

    def test_the_runner_emission_is_the_reconciled_code(self) -> None:
        from packages.derivation.evaluator import BLOCK_CLOSURE

        self.assertEqual(BLOCK_CLOSURE, "SOURCE_SET_UNCLOSED")
        record_enum = self.registry.get("derivation-record.v3")["$defs"]["disposition"]["properties"]["code"]["enum"]
        walk_enum = self.registry.get("npe-walk.v2")["$defs"]["node"]["properties"]["code"]["enum"]
        for enum in (record_enum, walk_enum):
            self.assertIn(BLOCK_CLOSURE, enum)
            self.assertIn("ITEMIZATION_TIE_OUT_VIOLATION", enum)
            self.assertNotIn("SOURCE_SET_OPEN", enum)


def _demo_fact_type(fact_id: str, value_schema: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": f"Demo fact type {fact_id}",
        "nature": "determinable",
        "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
        "value_schema": value_schema,
        "supersession": {"policy": "free"},
    }


def _demo_family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": "demo.family.alpha",
        "version": "v1",
        "title": "Demo alpha statement items",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
        "closure_claim": "Every demo alpha statement item is recorded.",
        "member_predicate": {"fact_type": "demo.fact.alpha-item"},
        "authorizes_subtotal": "demo.alpha.subtotal",
    }


def _demo_collect_rule(*, name: str = "demo.fact.alpha-item", source_set: str = "demo.family.alpha",
                       value: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v2",
        "id": "demo.rule.alpha-subtotal",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
        "role": "computation",
        "requires": [],
        "pins": [],
        "when": True,
        "value": value if value is not None else {
            "op": "add",
            "args": [{"op": "collect", "name": name, "source_set": source_set}],
        },
        "publishes": "demo.alpha.subtotal",
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": []},
    }


def _demo_universe() -> dict[str, Any]:
    universe = load(EXAMPLES / "dividend-universe.v1.json")
    universe["scope"] = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"}
    return universe


def _demo_attachment() -> dict[str, Any]:
    return load(EXAMPLES / "attachment-rule.v1.json")


class AdmissionGuards(unittest.TestCase):
    """ADR-0035 runtime universe guard and ADR-0036 presence-encoding guard."""

    def setUp(self) -> None:
        from packages.derivation.loader import DerivationSchemas

        self.schemas = DerivationSchemas()

    def _members(self) -> list[dict[str, Any]]:
        return [
            _demo_fact_type("demo.fact.alpha-item", {"type": "number"}),
            _demo_fact_type("demo.fact.answer-first", {"enum": ["yes", "no"]}),
            _demo_fact_type("demo.fact.answer-second", {"enum": ["yes", "no"]}),
            _demo_fact_type("demo.fact.answer-first-detail", {"enum": ["demo-country-a", "demo-country-b"]}),
            _demo_family(),
            _demo_collect_rule(),
            _demo_universe(),
            _demo_attachment(),
        ]

    def _package(self, members: list[dict[str, Any]]) -> dict[str, Any]:
        roles = {
            "fact-type.v2": "fact-type",
            "source-family.v1": "source-family",
            "rule-artifact.v2": "computation",
            "dividend-universe.v1": "dividend-universe",
            "attachment-rule.v1": "attachment-rule",
        }
        return {
            "schema": "artifact-package.v4",
            "id": "demo.package.dsbs-guards",
            "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
            "admitted_schemas": sorted({m["schema"] for m in members}),
            "members": [
                {"role": roles[m["schema"]], "schema": m["schema"], "id": m["id"], "version": m["version"]}
                for m in members
            ],
            "input_bindings": [],
            "entrypoints": [{"id": m["id"], "version": m["version"]} for m in members],
            "composition_obligations": [],
            "package_checksum": "0" * 64,
        }

    def _validate(self, members: list[dict[str, Any]]) -> Any:
        from packages.derivation.package_validation import validate_package

        corpus = {(m["id"], m["version"]): m for m in members}
        return validate_package(self._package(members), corpus, self.schemas)

    def _codes(self, result: Any) -> set[str]:
        return {issue.code for issue in result.issues}

    def test_conforming_package_is_admitted_by_both_guards(self) -> None:
        result = self._validate(self._members())
        self.assertTrue(result.ok, msg=str(result.issues))

    def test_collect_against_an_undeclared_source_set_is_rejected(self) -> None:
        members = [m for m in self._members() if m["schema"] != "source-family.v1"]
        result = self._validate(members)
        self.assertIn("COLLECT_TARGET_NOT_FAMILY", self._codes(result))

    def test_collect_of_a_non_member_fact_type_is_rejected(self) -> None:
        members = self._members()
        members = [
            _demo_collect_rule(name="demo.fact.answer-first") if m["schema"] == "rule-artifact.v2" else m
            for m in members
        ]
        result = self._validate(members)
        self.assertIn("COLLECT_TARGET_NOT_FAMILY", self._codes(result))

    def test_rule_consuming_recorded_non_composable_content_is_rejected(self) -> None:
        members = self._members()
        recorded_id = _demo_universe()["recorded_boxes_fact_type"]["id"]
        ref_rule = _demo_collect_rule(value={
            "op": "add",
            "args": [
                {"op": "collect", "name": "demo.fact.alpha-item", "source_set": "demo.family.alpha"},
                {"op": "ref", "name": recorded_id},
            ],
        })
        members = [ref_rule if m["schema"] == "rule-artifact.v2" else m for m in members]
        result = self._validate(members)
        self.assertIn("RECORDED_NON_COMPOSABLE_INPUT", self._codes(result))

    def test_boolean_part_iii_answer_fact_type_is_rejected(self) -> None:
        members = self._members()
        boolean_answer = load(NEGATIVES / "fact-type.v2.boolean-answer.json")
        members = [boolean_answer if m["id"] == "demo.fact.answer-first" else m for m in members]
        result = self._validate(members)
        self.assertIn("ATTACHMENT_ANSWER_NOT_CATEGORICAL", self._codes(result))

    def test_otherwise_falsy_categorical_answer_domain_is_rejected(self) -> None:
        members = self._members()
        falsy = _demo_fact_type("demo.fact.answer-first", {"enum": ["yes", ""]})
        members = [falsy if m["id"] == "demo.fact.answer-first" else m for m in members]
        result = self._validate(members)
        self.assertIn("ATTACHMENT_ANSWER_NOT_CATEGORICAL", self._codes(result))

    def test_answer_fact_type_missing_from_the_fact_surface_is_rejected(self) -> None:
        members = [m for m in self._members() if m["id"] != "demo.fact.answer-second"]
        result = self._validate(members)
        self.assertIn("ATTACHMENT_ANSWER_FACT_TYPE_ABSENT", self._codes(result))

    def test_published_pre_adr_0035_package_generations_stay_exempt(self) -> None:
        # The collect-target half binds artifact-package.v3 onward; the
        # committed v1/v2 instances keep their recorded issue surfaces.
        from packages.derivation.package_validation import validate_package

        members = [m for m in self._members() if m["schema"] in {"fact-type.v2", "rule-artifact.v2"}]
        package = self._package(members)
        package["schema"] = "artifact-package.v2"
        corpus = {(m["id"], m["version"]): m for m in members}
        result = validate_package(package, corpus, self.schemas)
        self.assertNotIn("COLLECT_TARGET_NOT_FAMILY", self._codes(result))


if __name__ == "__main__":
    unittest.main()
