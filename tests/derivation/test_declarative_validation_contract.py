"""ADR-0066 Track 2: the closed declarative-validation grammar, its
depth-bounded evaluator, explicit identity bindings, and the published
v2/v5/v8/v24 schema/example contract.
"""

import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.declarative_validation import (
    Evaluator,
    GrammarError,
    IdentityBindingError,
    MemberConstraintTooDeep,
    Violation,
    extract_bound_keys,
    extract_component,
    identity_tuple,
)
from packages.derivation.loader import DerivationSchemas
from packages.kernel.schema_registry import SchemaValidationError

SAMPLE_DIR = Path(__file__).resolve().parent.parent.parent / "packages" / "sample_data" / "declarative_validation_contract"


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((SAMPLE_DIR / name).read_text("utf-8")))


def _nested_all(depth: int) -> dict[str, Any]:
    """A predicate whose `all`/`args` nesting is exactly `depth` levels deep."""
    node: dict[str, Any] = {"op": "field_present", "field": "leaf"}
    for _ in range(depth - 1):
        node = {"op": "all", "args": [node]}
    return node


class TermEvaluationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ev = Evaluator()

    def test_field_present(self) -> None:
        self.assertEqual(self.ev.evaluate_term({"op": "field", "field": "x"}, {"x": "3"}), 3)

    def test_field_absent_uses_explicit_default(self) -> None:
        self.assertEqual(
            self.ev.evaluate_term({"op": "field", "field": "x", "default": 0}, {}), 0
        )

    def test_field_absent_without_default_raises(self) -> None:
        with self.assertRaises(GrammarError):
            self.ev.evaluate_term({"op": "field", "field": "x"}, {})

    def test_literal(self) -> None:
        self.assertEqual(self.ev.evaluate_term({"op": "literal", "arg": 5}, {}), 5)

    def test_add_subtract_floor_zero(self) -> None:
        term = {
            "op": "floor_zero",
            "value": {
                "op": "subtract",
                "left": {"op": "literal", "arg": 3},
                "right": {"op": "literal", "arg": 10},
            },
        }
        self.assertEqual(self.ev.evaluate_term(term, {}), 0)
        term_add = {"op": "add", "left": {"op": "literal", "arg": 2}, "right": {"op": "literal", "arg": 3}}
        self.assertEqual(self.ev.evaluate_term(term_add, {}), 5)

    def test_unknown_term_op_rejected(self) -> None:
        with self.assertRaises(GrammarError):
            self.ev.evaluate_term({"op": "multiply", "left": 1, "right": 2}, {})

    def test_boolean_is_not_a_numeric_value(self) -> None:
        with self.assertRaises(GrammarError):
            self.ev.evaluate_term({"op": "literal", "arg": True}, {})


class PredicateEvaluationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ev = Evaluator()

    def test_field_present_absent(self) -> None:
        self.assertTrue(self.ev.evaluate_predicate({"op": "field_present", "field": "a"}, {"a": 1}))
        self.assertFalse(self.ev.evaluate_predicate({"op": "field_present", "field": "a"}, {}))
        self.assertTrue(self.ev.evaluate_predicate({"op": "field_absent", "field": "a"}, {}))
        self.assertFalse(self.ev.evaluate_predicate({"op": "field_absent", "field": "a"}, {"a": 1}))

    def test_field_equals_not_equals(self) -> None:
        self.assertTrue(self.ev.evaluate_predicate({"op": "field_equals", "field": "a", "arg": "x"}, {"a": "x"}))
        self.assertFalse(self.ev.evaluate_predicate({"op": "field_equals", "field": "a", "arg": "x"}, {}))

    def test_field_equals_does_not_conflate_bool_and_numeric(self) -> None:
        # `Evaluator._dec` refuses to treat a bool as a numeric term for the
        # same reason: Python's `True == 1`/`False == 0` identity must not
        # smuggle meaning across types through the equality predicates.
        self.assertFalse(self.ev.evaluate_predicate({"op": "field_equals", "field": "flag", "arg": 1}, {"flag": True}))
        self.assertFalse(self.ev.evaluate_predicate({"op": "field_equals", "field": "flag", "arg": 0}, {"flag": False}))
        self.assertTrue(self.ev.evaluate_predicate({"op": "field_not_equals", "field": "flag", "arg": 1}, {"flag": True}))
        self.assertTrue(self.ev.evaluate_predicate({"op": "field_not_equals", "field": "flag", "arg": 0}, {"flag": False}))
        # Same-type comparisons are unaffected: bool-to-bool and
        # number-to-number equality still fire normally.
        self.assertTrue(self.ev.evaluate_predicate({"op": "field_equals", "field": "flag", "arg": True}, {"flag": True}))
        self.assertTrue(self.ev.evaluate_predicate({"op": "field_equals", "field": "n", "arg": 1}, {"n": 1}))

    def test_field_not_equals_is_false_when_absent(self) -> None:
        # ADR-0066: absent fields are true only for `field_absent`;
        # `field_not_equals` is false when absent, never vacuously true.
        self.assertFalse(self.ev.evaluate_predicate({"op": "field_not_equals", "field": "a", "arg": "x"}, {}))
        self.assertTrue(self.ev.evaluate_predicate({"op": "field_not_equals", "field": "a", "arg": "x"}, {"a": "y"}))
        self.assertFalse(self.ev.evaluate_predicate({"op": "field_not_equals", "field": "a", "arg": "x"}, {"a": "x"}))

    def test_compare_all_operators(self) -> None:
        left = {"op": "literal", "arg": 5}
        right = {"op": "literal", "arg": 3}
        for comparison, expected in (("gt", True), ("ge", True), ("lt", False), ("le", False), ("eq", False), ("ne", True)):
            pred = {"op": "compare", "left": left, "right": right, "comparison": comparison}
            self.assertEqual(self.ev.evaluate_predicate(pred, {}), expected, comparison)

    def test_all_and_any(self) -> None:
        true_pred = {"op": "field_present", "field": "a"}
        false_pred = {"op": "field_present", "field": "b"}
        member = {"a": 1}
        self.assertFalse(self.ev.evaluate_predicate({"op": "all", "args": [true_pred, false_pred]}, member))
        self.assertTrue(self.ev.evaluate_predicate({"op": "any", "args": [true_pred, false_pred]}, member))

    def test_unknown_predicate_op_and_not_rejected(self) -> None:
        with self.assertRaises(GrammarError):
            self.ev.evaluate_predicate({"op": "not", "arg": {"op": "field_present", "field": "a"}}, {})
        with self.assertRaises(GrammarError):
            self.ev.evaluate_predicate({"op": "regex", "field": "a", "pattern": ".*"}, {})

    def test_depth_six_evaluates_depth_seven_rejected(self) -> None:
        self.assertTrue(self.ev.evaluate_predicate(_nested_all(6), {"leaf": 1}))
        with self.assertRaises(MemberConstraintTooDeep):
            self.ev.evaluate_predicate(_nested_all(7), {"leaf": 1})

    def test_evaluate_member_names_constraint_id_code_and_meaning(self) -> None:
        constraints = [{
            "id": "c1", "block_code": "MISSING_ATTACHMENT", "meaning": "Attachment missing",
            "violated_when": {"op": "field_absent", "field": "some_field"},
        }]
        violations = self.ev.evaluate_member(constraints, {})
        self.assertEqual(violations, [Violation("c1", "MISSING_ATTACHMENT", "Attachment missing")])
        self.assertEqual(self.ev.evaluate_member(constraints, {"some_field": 1}), [])


class IdentityBindingTest(unittest.TestCase):
    def test_fact_id_bound_key(self) -> None:
        keys = extract_bound_keys("demo.fact.type|taxpayer=alice,statement=001")
        self.assertEqual(keys, {"taxpayer": "alice", "statement": "001"})
        value = extract_component(
            fact_id="demo.fact.type|taxpayer=alice,statement=001",
            member_value=None,
            component={"fact_id_bound_key": "taxpayer"},
        )
        self.assertEqual(value, "alice")

    def test_member_field(self) -> None:
        value = extract_component(
            fact_id="demo.fact.type|taxpayer=alice",
            member_value={"external_ref": "ref-1"},
            component={"member_field": "external_ref"},
        )
        self.assertEqual(value, "ref-1")

    def test_missing_fact_id_bound_key_fails_closed(self) -> None:
        with self.assertRaises(IdentityBindingError):
            extract_component(
                fact_id="demo.fact.type|statement=001",
                member_value=None,
                component={"fact_id_bound_key": "taxpayer"},
            )

    def test_missing_member_field_fails_closed(self) -> None:
        with self.assertRaises(IdentityBindingError):
            extract_component(
                fact_id="demo.fact.type|taxpayer=alice",
                member_value={},
                component={"member_field": "external_ref"},
            )
        with self.assertRaises(IdentityBindingError):
            extract_component(
                fact_id="demo.fact.type|taxpayer=alice",
                member_value=None,
                component={"member_field": "external_ref"},
            )

    def test_no_name_parsing_identity_works_regardless_of_naming(self) -> None:
        # Generic components never special-case tax/family/artifact names -
        # arbitrary non-tax-sounding ids and fields work identically.
        components = [{"fact_id_bound_key": "zzz"}, {"member_field": "qqq"}]
        ident = identity_tuple(
            fact_id="widget.thing|zzz=42", member_value={"qqq": "yes"}, components=components
        )
        self.assertEqual(ident, ("42", "yes"))

    def test_unsupported_component_shape_rejected(self) -> None:
        with self.assertRaises(IdentityBindingError):
            extract_component(fact_id="a|b=1", member_value={}, component={"nonsense": "x"})


class RegisteredSchemaContractTest(unittest.TestCase):
    """Every handwritten v2/v5/v8/v24 synthetic example must validate through
    the real published registry (not a hand-rolled JSON Schema check)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = DerivationSchemas()

    def test_every_sample_citizen_validates_declared(self) -> None:
        for path in sorted(SAMPLE_DIR.glob("*.json")):
            citizen = json.loads(path.read_text("utf-8"))
            self.schemas.validate_declared(citizen)

    def test_successor_with_only_predecessor_fields_validates(self) -> None:
        # source-family.v2 with none of its additive fields present still
        # validates - the new contract is strictly additive over v1.
        minimal = {
            "schema": "source-family.v2",
            "id": "declarativevalidation.demo-minimal-family",
            "version": "v1",
            "title": "Minimal",
            "closure_claim": "All minimal members",
            "member_predicate": {"fact_type": "declarativevalidation.demo-minimal.member"},
            "scope": {"tax_year": 2025, "jurisdiction": "us", "family": "declarativevalidation.demo-family"},
            "authorizes_subtotal": "demo.minimal-subtotal",
        }
        self.schemas.validate_declared(minimal)

        minimal_rule = {
            "schema": "rule-artifact.v5",
            "id": "declarativevalidation.demo-minimal-rule",
            "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "us", "family": "declarativevalidation.demo-family"},
            "role": "computation",
            "publishes": "demo.minimal-output",
            "requires": [],
            "pins": [],
            "when": True,
            "value": 1,
            "blocked": {"code": "NONE", "missing": []},
        }
        self.schemas.validate_declared(minimal_rule)

    def test_unknown_predicate_form_is_schema_rejected(self) -> None:
        family = json.loads((SAMPLE_DIR / "source-family.declarativevalidation.demo-family.v1.json").read_text())
        family = dict(family)
        family["member_constraints"] = [{
            "id": "bad", "block_code": "BAD", "meaning": "bad",
            "violated_when": {"op": "not", "arg": {"op": "field_present", "field": "x"}},
        }]
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(family)

    def test_unknown_term_form_is_schema_rejected(self) -> None:
        family = json.loads((SAMPLE_DIR / "source-family.declarativevalidation.demo-family.v1.json").read_text())
        family = dict(family)
        family["member_constraints"] = [{
            "id": "bad", "block_code": "BAD", "meaning": "bad",
            "violated_when": {
                "op": "compare", "comparison": "gt",
                "left": {"op": "multiply", "left": {"op": "literal", "arg": 1}, "right": {"op": "literal", "arg": 2}},
                "right": {"op": "literal", "arg": 0},
            },
        }]
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(family)


class EvaluateConstraintsDeadCodeRemovedTest(unittest.TestCase):
    """Defect 3: `evaluate_constraints` was a second, unused API returning
    `list[dict[str, str]]` for what `evaluate_member` already returns as
    `list[Violation]` — no caller anywhere but its own now-deleted test."""

    def test_evaluate_constraints_no_longer_exists_on_the_module(self) -> None:
        import packages.derivation.declarative_validation as declarative_validation
        self.assertFalse(hasattr(declarative_validation, "evaluate_constraints"))

    def test_evaluate_constraints_not_referenced_anywhere_in_the_repo(self) -> None:
        import subprocess
        root = Path(__file__).resolve().parents[2]
        this_file = Path(__file__).resolve()
        result = subprocess.run(
            [
                "grep", "-rl", "--include=*.py", "evaluate_constraints",
                str(root / "packages"), str(root / "tools"), str(root / "tests"),
            ],
            capture_output=True, text=True,
        )
        matches = {Path(line) for line in result.stdout.splitlines()}
        # Only this test file's own reference to the symbol name is expected;
        # exclude it from the assertion since the test itself must name the
        # deleted symbol to check for its absence.
        matches.discard(this_file)
        self.assertEqual(matches, set())


if __name__ == "__main__":
    unittest.main()
