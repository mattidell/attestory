"""Track 1 verification: the ADR-0006 language as published, enforced schemas.

Every positive example validates; every mutation the prototypes showed the
schema failing to catch is rejected here. The central regression guarded is
it2's schema-never-loaded / no-per-op-constraint defect (round-2 legibility
L-4, adversary attack 2): an operation with absent operands, an unknown
operation, or a stray operand field must all fail validation against the
*published* schema, not a hand-rolled copy.
"""

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.schema_registry import SchemaValidationError
from packages.derivation.loader import (
    CANON_OPERATIONS,
    DERIVATION_RECORD_SCHEMA,
    OPERATION_SEMANTICS_SCHEMA,
    PACKAGE_SCHEMA,
    PUBLICATION_ACT_SCHEMA,
    RULE_ARTIFACT_SCHEMA,
    ROLE_VOCABULARY,
    DerivationSchemas,
    load_canon,
    role_vocabulary_report,
)

EXAMPLES = Path(__file__).resolve().parent.parent.parent / "packages" / "sample_data" / "derivation" / "examples"


def _example(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


class LanguageSchemaFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def assert_rejected(self, schema_id: str, instance: object) -> None:
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate(schema_id, instance)


class PositiveExamples(LanguageSchemaFixture):
    def test_all_committed_examples_validate(self) -> None:
        # Self-declaring citizens validate against the schema they name.
        for name in [
            "rule-artifact.wages-line1a.json",
            "rule-artifact.tax-table-line16.json",
            "parameter.standard-deduction.json",
            "artifact-package.json",
            "derivation-record.started.json",
            "derivation-record.completed.json",
        ]:
            with self.subTest(example=name):
                self.schemas.validate_declared(_example(name))

    def test_publication_act_payload_validates(self) -> None:
        # The act payload has no self-declaring `schema` field (the envelope
        # carries it), so it is validated by named schema. Per ADR-0009 it
        # carries a derived-finding.v1, whose role-bearing pins are the
        # lineage; the embedded finding is validated against its own schema.
        act = _example("act-derived-publication.json")
        self.schemas.validate(PUBLICATION_ACT_SCHEMA, act)
        self.schemas.validate_declared(act["finding"])

    def test_derived_finding_has_no_human_basis(self) -> None:
        # ADR-0009: a derived finding must not carry a human basis. The schema
        # forbids it (additionalProperties:false), so an injected basis fails.
        finding = _example("act-derived-publication.json")["finding"]
        finding["basis"] = "attested"
        self.assert_rejected("derived-finding.v1", finding)

    def test_derived_finding_requires_role_bearing_pins(self) -> None:
        finding = _example("act-derived-publication.json")["finding"]
        finding["pins"] = []  # a bare/empty lineage is rejected (ADR-0007 d3)
        self.assert_rejected("derived-finding.v1", finding)


class OperationVocabularyConstraints(LanguageSchemaFixture):
    """ADR-0006 decision 2 & 3: closed op enum with per-op required fields."""

    def _rule_with_value(self, value: object) -> dict[str, Any]:
        rule = _example("rule-artifact.wages-line1a.json")
        rule["value"] = value
        return rule

    def test_unknown_operation_rejected(self) -> None:
        self.assert_rejected(RULE_ARTIFACT_SCHEMA, self._rule_with_value({"op": "multiply", "args": [1, 2]}))

    def test_round_without_mode_rejected(self) -> None:
        self.assert_rejected(
            RULE_ARTIFACT_SCHEMA,
            self._rule_with_value({"op": "round", "value": 1, "stage": "final"}),
        )

    def test_round_without_stage_rejected(self) -> None:
        self.assert_rejected(
            RULE_ARTIFACT_SCHEMA,
            self._rule_with_value({"op": "round", "value": 1, "mode": {"op": "ref", "name": "rounding.convention"}}),
        )

    def test_compare_without_cmp_rejected(self) -> None:
        self.assert_rejected(
            RULE_ARTIFACT_SCHEMA,
            self._rule_with_value({"op": "compare", "left": 1, "right": 2}),
        )

    def test_ref_without_name_rejected(self) -> None:
        self.assert_rejected(RULE_ARTIFACT_SCHEMA, self._rule_with_value({"op": "ref"}))

    def test_subtract_missing_operand_rejected(self) -> None:
        self.assert_rejected(RULE_ARTIFACT_SCHEMA, self._rule_with_value({"op": "subtract", "left": 1}))

    def test_add_empty_args_rejected(self) -> None:
        self.assert_rejected(RULE_ARTIFACT_SCHEMA, self._rule_with_value({"op": "add", "args": []}))

    def test_stray_operand_field_rejected(self) -> None:
        # additionalProperties:false per op branch — a ref carrying `args` is
        # not a tolerated superset, it is malformed.
        self.assert_rejected(
            RULE_ARTIFACT_SCHEMA,
            self._rule_with_value({"op": "ref", "name": "x", "args": [1]}),
        )

    def test_range_lookup_requires_table_and_key_and_value(self) -> None:
        self.assert_rejected(
            RULE_ARTIFACT_SCHEMA,
            self._rule_with_value({"op": "range_lookup", "table_id": "t", "key": 1}),
        )

    def test_nested_operand_defect_rejected(self) -> None:
        # The grammar is recursive: a malformed inner operand fails the whole tree.
        self.assert_rejected(
            RULE_ARTIFACT_SCHEMA,
            self._rule_with_value({"op": "add", "args": [{"op": "ref"}]}),
        )

    def test_every_closed_operation_has_a_branch(self) -> None:
        # Guard against grammar drift: a schema-declared op that no branch
        # accepts would silently ban a legal operation.
        for op, minimal in {
            "ref": {"op": "ref", "name": "x"},
            "collect": {"op": "collect", "name": "x"},
            "parameter": {"op": "parameter", "parameter_id": "p"},
            "add": {"op": "add", "args": [1]},
            "subtract": {"op": "subtract", "left": 1, "right": 2},
            "max": {"op": "max", "args": [0, 1]},
            "compare": {"op": "compare", "left": 1, "right": 2, "cmp": "gt"},
            "all": {"op": "all", "args": [True]},
            "any": {"op": "any", "args": [True]},
            "not": {"op": "not", "value": True},
            "choose": {"op": "choose", "when": True, "then": 1, "else": 2},
            "range_lookup": {"op": "range_lookup", "table_id": "t", "key": 1, "value": 2},
            "bracket_fold": {"op": "bracket_fold", "table_id": "t", "key": 1, "value": 2},
            "round": {"op": "round", "value": 1, "mode": "half_up", "stage": "final"},
        }.items():
            with self.subTest(op=op):
                self.schemas.validate(RULE_ARTIFACT_SCHEMA, self._rule_with_value(minimal))


class RuleArtifactEnvelope(LanguageSchemaFixture):
    def test_bad_blocked_code_rejected(self) -> None:
        rule = _example("rule-artifact.wages-line1a.json")
        rule["blocked"]["code"] = "lowercase_code"
        self.assert_rejected(RULE_ARTIFACT_SCHEMA, rule)

    def test_bad_version_rejected(self) -> None:
        rule = _example("rule-artifact.wages-line1a.json")
        rule["version"] = "1.0"
        self.assert_rejected(RULE_ARTIFACT_SCHEMA, rule)

    def test_unknown_role_rejected(self) -> None:
        rule = _example("rule-artifact.wages-line1a.json")
        rule["role"] = "mapping"  # the prototype's divergent token (L-8)
        self.assert_rejected(RULE_ARTIFACT_SCHEMA, rule)

    def test_missing_publishes_rejected(self) -> None:
        rule = _example("rule-artifact.wages-line1a.json")
        del rule["publishes"]
        self.assert_rejected(RULE_ARTIFACT_SCHEMA, rule)


class OneRoleVocabulary(LanguageSchemaFixture):
    """ADR-0006 decision 9: one role vocabulary across all positions."""

    def test_all_role_enums_subset_of_master_vocabulary(self) -> None:
        report = role_vocabulary_report(self.schemas)
        self.assertTrue(report, "expected role enums in the schema set")
        for schema_id, tokens in report.items():
            with self.subTest(schema=schema_id):
                self.assertTrue(
                    tokens <= ROLE_VOCABULARY,
                    f"{schema_id} declares out-of-vocabulary roles: {sorted(tokens - ROLE_VOCABULARY)}",
                )

    def test_package_member_unknown_role_rejected(self) -> None:
        pkg = _example("artifact-package.json")
        pkg["members"][0]["role"] = "mapping"
        self.assert_rejected(PACKAGE_SCHEMA, pkg)


class DerivationRecordPhase(LanguageSchemaFixture):
    """ADR-0008 decisions 2 & 4: paired records, inapplicable-vs-unreached."""

    def test_started_must_not_carry_closing_fields(self) -> None:
        rec = _example("derivation-record.started.json")
        rec["stop_reason"] = "saturated"
        self.assert_rejected(DERIVATION_RECORD_SCHEMA, rec)

    def test_completed_requires_closing_fields(self) -> None:
        rec = _example("derivation-record.completed.json")
        del rec["stop_reason"]
        self.assert_rejected(DERIVATION_RECORD_SCHEMA, rec)

    def test_inapplicable_disposition_carries_guard_provenance(self) -> None:
        rec = _example("derivation-record.completed.json")
        dispositions = {d["disposition"]: d for d in rec["dispositions"]}
        self.assertIn("inapplicable", dispositions)
        self.assertIn("guard_result", dispositions["inapplicable"])
        self.assertTrue(dispositions["inapplicable"]["pins"])

    def test_bad_stop_reason_rejected(self) -> None:
        rec = _example("derivation-record.completed.json")
        rec["stop_reason"] = "started"  # a phase, never a stop reason
        self.assert_rejected(DERIVATION_RECORD_SCHEMA, rec)


class OperationSemanticsCanon(LanguageSchemaFixture):
    """ADR-0006 decision 4: versioned canon, structured and complete."""

    def test_canon_loads_and_covers_the_data_operations(self) -> None:
        canon = load_canon(self.schemas)
        self.assertEqual(set(canon), set(CANON_OPERATIONS))

    def test_round_spec_missing_tie_break_rejected(self) -> None:
        canon = load_canon(self.schemas)
        broken = copy.deepcopy(canon["round"])
        del broken["spec"]["tie_break"]
        self.assert_rejected(OPERATION_SEMANTICS_SCHEMA, broken)

    def test_range_lookup_unknown_boundary_rejected(self) -> None:
        canon = load_canon(self.schemas)
        broken = copy.deepcopy(canon["range_lookup"])
        broken["spec"]["boundary"] = "closed"
        self.assert_rejected(OPERATION_SEMANTICS_SCHEMA, broken)

    def test_missing_canon_operation_detected(self) -> None:
        import tempfile

        canon = load_canon(self.schemas)
        with tempfile.TemporaryDirectory() as tmp:
            only_round = Path(tmp) / "round.v1.json"
            only_round.write_text(json.dumps(canon["round"]), "utf-8")
            with self.assertRaises(SchemaValidationError):
                load_canon(self.schemas, canon_dir=Path(tmp))


if __name__ == "__main__":
    unittest.main()
