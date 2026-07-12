"""Source Completeness Track 1: contract schemas and payload instances.

Every committed positive validates against the *published* schema files;
every schema negative is an isolated single-defect instance the schema must
reject; every pair negative is schema-valid alone but rejected against its
pinned declaration; every admission negative is schema-valid by design and
awaits Track 2's atomic-admission rejection. Content assertions guard the
ratified ADR-0014/0016/0017 commitments schema validation cannot express.
"""

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DERIVATION_SCHEMA_DIR
from packages.derivation.source_authority import (
    SourceAuthorityError,
    validate_mapping_against_family,
)
from packages.kernel.schema_registry import (
    KERNEL_SCHEMA_DIR,
    SchemaRegistry,
    SchemaValidationError,
)

SAMPLE_ROOT = Path("packages/sample_data/source_authority")
EXAMPLES = SAMPLE_ROOT / "examples"
SCHEMA_NEGATIVES = SAMPLE_ROOT / "negatives" / "schema"
PAIR_NEGATIVES = SAMPLE_ROOT / "negatives" / "pair"
ADMISSION_NEGATIVES = SAMPLE_ROOT / "negatives" / "admission"

NEW_SCHEMAS = (
    "source-family.v1",
    "source-closure-mapping.v1",
    "family-horizon.v1",
    "act-member-transition.v1",
    "act-horizon-genesis.v1",
)


def _load(path: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(path.read_text("utf-8"))
    return loaded


def _payload_schema_for(path: Path) -> str:
    """Negative payload files name their schema by filename prefix."""
    return path.name.split(".")[0] + ".v1"


class ContractRegistryFixture(unittest.TestCase):
    registry: SchemaRegistry

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = SchemaRegistry([KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR])

    def validate_act(self, act: dict[str, Any]) -> None:
        """An act validates as envelope plus kind-named payload schema."""
        self.registry.validate_declared(act)
        self.registry.validate(f"act-{act['kind']}.v1", act["payload"])


class RegistryIntegrity(ContractRegistryFixture):
    def test_new_contract_schemas_are_published(self) -> None:
        ids = self.registry.schema_ids()
        for schema_id in NEW_SCHEMAS:
            self.assertIn(schema_id, ids)

    def test_new_schema_files_are_in_the_immutable_manifests(self) -> None:
        kernel = _load(KERNEL_SCHEMA_DIR / "published.json")
        derivation = _load(DERIVATION_SCHEMA_DIR / "published.json")
        self.assertIn("family-horizon.v1.schema.json", kernel)
        self.assertIn("act-member-transition.v1.schema.json", kernel)
        self.assertIn("act-horizon-genesis.v1.schema.json", kernel)
        self.assertIn("source-family.v1.schema.json", derivation)
        self.assertIn("source-closure-mapping.v1.schema.json", derivation)


class PositiveInstances(ContractRegistryFixture):
    def test_all_committed_examples_validate(self) -> None:
        paths = sorted(EXAMPLES.glob("*.json"))
        self.assertTrue(paths, "expected committed positive examples")
        for path in paths:
            instance = _load(path)
            with self.subTest(example=path.name):
                if instance.get("schema") == "act.v1":
                    self.validate_act(instance)
                else:
                    self.registry.validate_declared(instance)

    def test_embedded_member_finding_validates_whole(self) -> None:
        act = _load(EXAMPLES / "act.member-transition.assert.json")
        self.registry.validate_declared(act["payload"]["member"]["finding"])

    def test_mapping_pair_validates_against_its_declaration(self) -> None:
        mapping = _load(EXAMPLES / "source-closure-mapping.w2-box1.json")
        family = _load(EXAMPLES / "source-family.w2-box1.json")
        validate_mapping_against_family(mapping, family)


class SuccessionShape(ContractRegistryFixture):
    """ADR-0017: explicit succession, genesis-only null, one shared scope."""

    def test_genesis_horizon_has_null_predecessor(self) -> None:
        genesis = _load(EXAMPLES / "family-horizon.genesis.json")
        self.assertIsNone(genesis["predecessor"])

    def test_successor_names_the_genesis_horizon(self) -> None:
        genesis = _load(EXAMPLES / "family-horizon.genesis.json")
        successor = _load(EXAMPLES / "family-horizon.successor.json")
        self.assertEqual(successor["predecessor"], genesis["id"])
        self.assertEqual(successor["family"], genesis["family"])
        self.assertEqual(successor["scope"], genesis["scope"])

    def test_transition_scope_binds_both_halves_once(self) -> None:
        # The successor carries no family/scope of its own: a differently
        # scoped successor is unrepresentable, not merely rejected.
        act = _load(EXAMPLES / "act.member-transition.assert.json")
        self.assertEqual(sorted(act["payload"]["successor"]), ["id", "predecessor"])

    def test_same_member_correction_is_an_ordinary_assertion(self) -> None:
        # ADR-0017 decision 4: a value correction that does not change
        # predicate membership never advances the horizon, so it travels
        # as kind "assertion" with no successor anywhere in the payload.
        act = _load(EXAMPLES / "act.assertion.same-member-correction.json")
        self.assertEqual(act["kind"], "assertion")
        self.assertNotIn("successor", act["payload"])
        original = _load(EXAMPLES / "act.member-transition.assert.json")
        self.assertEqual(
            act["payload"]["finding"]["fact_id"],
            original["payload"]["member"]["finding"]["fact_id"],
        )


class SchemaNegatives(ContractRegistryFixture):
    def test_every_schema_negative_is_rejected(self) -> None:
        paths = sorted(SCHEMA_NEGATIVES.glob("*.json"))
        self.assertTrue(paths, "expected committed schema negatives")
        for path in paths:
            with self.subTest(negative=path.name):
                with self.assertRaises(SchemaValidationError):
                    self.registry.validate(_payload_schema_for(path), _load(path))

    def test_member_action_branches_do_not_blend(self) -> None:
        # A member that mixes assert and remove fields fails every oneOf
        # branch: per-action required/closed fields are live constraints.
        payload = _load(EXAMPLES / "act.member-transition.assert.json")["payload"]
        blended = copy.deepcopy(payload)
        blended["member"]["fact_id"] = "fact.tax.us.2025.w2.box1-wages.employer-alpha.slip-1"
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("act-member-transition.v1", blended)

    def test_truthy_admission_has_no_schema_branch(self) -> None:
        # ADR-0014 decision 3: the admission vocabulary is closed at one
        # affirmative condition; no truthy or presence-only variant exists.
        mapping = _load(EXAMPLES / "source-closure-mapping.w2-box1.json")
        mapping["admission"]["condition"] = "current-truthy"
        with self.assertRaises(SchemaValidationError):
            self.registry.validate_declared(mapping)


class PairNegatives(ContractRegistryFixture):
    """Schema-valid alone; rejected against the pinned declaration."""

    def test_pair_negatives_are_schema_valid_alone(self) -> None:
        for path in sorted(PAIR_NEGATIVES.glob("*.json")):
            with self.subTest(negative=path.name):
                self.registry.validate_declared(_load(path))

    def test_claim_predicate_mismatch_is_rejected(self) -> None:
        mapping = _load(PAIR_NEGATIVES / "source-closure-mapping.mismatched-member.json")
        family = _load(EXAMPLES / "source-family.w2-box1.json")
        with self.assertRaisesRegex(SourceAuthorityError, "claim/predicate mismatch"):
            validate_mapping_against_family(mapping, family)

    def test_narrow_subtotal_substitution_is_rejected(self) -> None:
        mapping = _load(PAIR_NEGATIVES / "source-closure-mapping.broader-symbol.json")
        family = _load(EXAMPLES / "source-family.w2-box1.json")
        with self.assertRaisesRegex(SourceAuthorityError, "narrow-subtotal"):
            validate_mapping_against_family(mapping, family)

    def test_wrong_declaration_pin_is_rejected(self) -> None:
        mapping = _load(EXAMPLES / "source-closure-mapping.w2-box1.json")
        family = _load(EXAMPLES / "source-family.w2-box1.json")
        family = copy.deepcopy(family)
        family["version"] = "v2"
        with self.assertRaisesRegex(SourceAuthorityError, "pins family"):
            validate_mapping_against_family(mapping, family)


class AdmissionNegatives(ContractRegistryFixture):
    """Track 2's rejection corpus: each is schema-valid by design."""

    def test_every_admission_negative_is_schema_valid(self) -> None:
        paths = sorted(ADMISSION_NEGATIVES.glob("*.json"))
        self.assertTrue(paths, "expected committed admission negatives")
        for path in paths:
            with self.subTest(negative=path.name):
                self.validate_act(_load(path))


class DataSafety(unittest.TestCase):
    def test_committed_files_have_no_private_markers(self) -> None:
        forbidden = ("/Users/", "/private/", "local-data/", "uploads/")
        for path in SAMPLE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text("utf-8")
            with self.subTest(path=str(path)):
                self.assertFalse(any(marker in text for marker in forbidden))


if __name__ == "__main__":
    unittest.main()
