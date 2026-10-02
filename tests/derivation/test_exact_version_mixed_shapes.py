from __future__ import annotations

import unittest
from typing import Any

from packages.derivation.evaluator import (
    BLOCK_CATEGORICAL_DOMAIN_MISMATCH,
    BLOCK_INVALID,
    Environment,
    EvalBlocked,
    _validate_categorical_value,
)
from tests.derivation.test_exact_version_authority import _blocked
from tests.derivation.test_exact_version_authority import _finding  # type: ignore[attr-defined]
from tests.derivation.test_exact_version_authority import _for_both
from tests.derivation.test_exact_version_authority import _lattice_type  # type: ignore[attr-defined]
from tests.derivation.test_exact_version_authority import _ordinary_rule  # type: ignore[attr-defined]
from tests.derivation.test_exact_version_authority import _order
from tests.derivation.test_exact_version_authority import _package_fact_type  # type: ignore[attr-defined]
from tests.derivation.test_exact_version_authority import _publications  # type: ignore[attr-defined]
from tests.derivation.test_exact_version_authority import _run
from tests.derivation.test_exact_version_authority import _v11_rule  # type: ignore[attr-defined]
from tests.derivation.test_exact_version_authority import _with_schema


class MixedShapeExactVersion(unittest.TestCase):
    """A pinned scalar fact definition stays distinct from an enum sibling."""

    FACT = "demo.review.mixed-shape"
    ECHO = "demo.review.mixed-shape-echo"
    RULE = "demo.rule.mixed-shape"
    SUBJECT = "demo.review.mixed-shape-subject"

    def _comparison(self, version: str) -> dict[str, Any]:
        return {
            "op": "categorical_compare",
            "cmp": "eq",
            "left": {"op": "ref", "name": self.FACT},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": self.FACT, "version": version},
                "value": "12",
            },
        }

    def _fact_types(self, *, numeric_version: str) -> list[dict[str, Any]]:
        enum_version = "v2" if numeric_version == "v1" else "v1"
        numeric = _with_schema(self.FACT, numeric_version, {"type": "number"})
        categorical = _with_schema(
            self.FACT, enum_version,
            {"type": "string", "enum": ["12", "other"]},
        )
        return [numeric, categorical]

    def _input_binding(self, version: str) -> dict[str, Any]:
        return {
            "symbol": self.FACT,
            "fact_type": {"id": self.FACT, "version": version},
            "mode": "required",
        }

    def _ordinary_parts(self, *, numeric_version: str, v1_first: bool) -> list[tuple[dict[str, Any], str]]:
        rule = _ordinary_rule(
            rule_id=self.RULE,
            publishes=self.ECHO,
            value={"op": "ref", "name": self.FACT},
            requires=[self.FACT],
        )
        facts = self._fact_types(numeric_version=numeric_version)
        return [(rule, "computation")] + [
            (citizen, "fact-type")
            for citizen in _order(facts[0], facts[1], v1_first=v1_first)
        ]

    def _finding_map(self) -> dict[str, dict[str, Any]]:
        return {
            "demo.finding.mixed-shape": _finding(
                "demo.finding.mixed-shape", f"{self.FACT}|period=demo", 12,
            ),
        }

    def test_ordinary_numeric_binding_with_enum_sibling_both_orders(self) -> None:
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts = self._ordinary_parts(numeric_version="v1", v1_first=v1_first)

                def check(result: Any) -> None:
                    published = _publications(result)
                    self.assertEqual(published[self.ECHO]["value"], "12", result.dispositions)

                _for_both(
                    _run(
                        parts,
                        self._finding_map(),
                        bindings=[self._input_binding("v1")],
                    ),
                    check,
                )

    def test_ordinary_numeric_v2_binding_and_reverse_shape_both_orders(self) -> None:
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts = self._ordinary_parts(numeric_version="v2", v1_first=v1_first)

                def check(result: Any) -> None:
                    self.assertEqual(_publications(result)[self.ECHO]["value"], "12", result.dispositions)

                _for_both(
                    _run(
                        parts,
                        self._finding_map(),
                        bindings=[self._input_binding("v2")],
                    ),
                    check,
                )

    def test_declared_subject_uses_exact_numeric_version_both_orders(self) -> None:
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                rule = _v11_rule(
                    rule_id=self.RULE,
                    subject={"id": self.SUBJECT, "version": "v1"},
                    requires=[self.FACT],
                    value={"op": "ref", "name": self.FACT},
                    publishes=self.ECHO,
                    when=True,
                )
                subject_type = _package_fact_type(self.SUBJECT, ["who"])
                fact_types = self._fact_types(numeric_version="v1")
                parts = [(rule, "computation"), (subject_type, "fact-type")] + [
                    (citizen, "fact-type")
                    for citizen in _order(fact_types[0], fact_types[1], v1_first=v1_first)
                ]
                subject_fact_id = f"{self.SUBJECT}|who=demo-who"
                findings = self._finding_map() | {
                    "demo.finding.mixed-shape-subject": _finding(
                        "demo.finding.mixed-shape-subject", subject_fact_id, "demo-who",
                    ),
                }
                lattice = {
                    self.SUBJECT: _lattice_type(self.SUBJECT, (("who", ("demo-who",)),)),
                }
                symbol = f"{self.ECHO}|{subject_fact_id}"

                def check(result: Any) -> None:
                    self.assertEqual(_publications(result)[symbol]["value"], "12", result.dispositions)

                _for_both(
                    _run(
                        parts,
                        findings,
                        lattice,
                        bindings=[self._input_binding("v1")],
                    ),
                    check,
                )

    def test_enum_membership_is_checked_and_exact_absence_stays_blocked(self) -> None:
        env = Environment(
            {}, {}, frozenset(), {}, {},
            categorical_domains={
                f"{self.FACT}\x1fv2": ["12", "other"],
            },
            fact_type_versions={self.FACT: frozenset({"v1", "v2"})},
        )
        self.assertEqual(_validate_categorical_value(self.FACT, "12", env, "v2"), f"{self.FACT}\x1fv2")
        with self.assertRaises(EvalBlocked) as invalid:
            _validate_categorical_value(self.FACT, "invalid", env, "v2")
        self.assertEqual(invalid.exception.category, BLOCK_INVALID)
        with self.assertRaises(EvalBlocked) as missing:
            _validate_categorical_value(self.FACT, "12", env, "v3")
        self.assertEqual(missing.exception.category, BLOCK_CATEGORICAL_DOMAIN_MISMATCH)

    def test_cross_version_numeric_and_enum_never_compare_as_one_domain(self) -> None:
        rule = _ordinary_rule(
            rule_id=self.RULE,
            publishes=self.ECHO,
            requires=[self.FACT],
            value={
                "op": "categorical_compare",
                "cmp": "eq",
                "left": {"op": "ref", "name": self.FACT},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": self.FACT, "version": "v2"},
                    "value": "12",
                },
            },
        )
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                facts = self._fact_types(numeric_version="v1")
                parts = [(rule, "computation")] + [
                    (citizen, "fact-type")
                    for citizen in _order(facts[0], facts[1], v1_first=v1_first)
                ]

                def check(result: Any) -> None:
                    self.assertNotIn(self.ECHO, _publications(result))
                    blocked = _blocked(result, self.RULE)
                    self.assertTrue(blocked, result.dispositions)
                    self.assertEqual(blocked[0]["code"], BLOCK_CATEGORICAL_DOMAIN_MISMATCH)

                _for_both(
                    _run(parts, self._finding_map(), bindings=[self._input_binding("v1")]),
                    check,
                )

    def test_derived_categorical_ref_keeps_exact_type_with_scalar_and_enum_versions(self) -> None:
        producer = _ordinary_rule(
            rule_id="demo.rule.mixed-shape-derived-producer",
            publishes=self.FACT,
            value={"op": "category_literal", "fact_type": {"id": self.FACT, "version": "v2"}, "value": "12"},
        )
        consumer = _ordinary_rule(
            rule_id="demo.rule.mixed-shape-derived-consumer",
            publishes=self.ECHO,
            requires=[self.FACT],
            value=self._comparison("v2"),
        )
        parts = [(producer, "computation"), (consumer, "computation")] + [
            (fact, "fact-type") for fact in self._fact_types(numeric_version="v1")
        ]
        for run_result in _run(parts):
            self.assertEqual(_publications(run_result)[self.ECHO]["value"], "true", run_result.dispositions)

    def test_same_name_untyped_scalar_remains_ambiguous_with_scalar_and_enum_versions(self) -> None:
        producer = _ordinary_rule(
            rule_id="demo.rule.mixed-shape-untyped-producer",
            publishes=self.FACT,
            value="12",
        )
        consumer = _ordinary_rule(
            rule_id="demo.rule.mixed-shape-untyped-consumer",
            publishes=self.ECHO,
            requires=[self.FACT],
            value={
                "op": "categorical_compare",
                "cmp": "eq",
                "left": {"op": "ref", "name": self.FACT},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": self.FACT, "version": "v2"},
                    "value": "12",
                },
            },
        )
        fact_types = self._fact_types(numeric_version="v1")
        for v1_first in (True, False):
            parts = [(producer, "computation"), (consumer, "computation")] + [
                (fact, "fact-type") for fact in _order(fact_types[0], fact_types[1], v1_first=v1_first)
            ]
            for result in _run(parts):
                self.assertEqual(_publications(result)[self.FACT]["value"], "12")
                blocked = _blocked(result, consumer["id"])
                self.assertTrue(blocked, result.dispositions)
                self.assertEqual(blocked[0]["code"], BLOCK_CATEGORICAL_DOMAIN_MISMATCH)

    def test_same_name_untyped_scalar_keeps_one_version_compatibility(self) -> None:
        producer = _ordinary_rule(
            rule_id="demo.rule.mixed-shape-untyped-single-producer",
            publishes=self.FACT,
            value="12",
        )
        consumer = _ordinary_rule(
            rule_id="demo.rule.mixed-shape-untyped-single-consumer",
            publishes=self.ECHO,
            requires=[self.FACT],
            value={
                "op": "categorical_compare",
                "cmp": "eq",
                "left": {"op": "ref", "name": self.FACT},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": self.FACT, "version": "v2"},
                    "value": "12",
                },
            },
        )
        enum = _with_schema(self.FACT, "v2", {"type": "string", "enum": ["12", "other"]})
        parts = [(producer, "computation"), (consumer, "computation"), (enum, "fact-type")]
        for result in _run(parts):
            self.assertEqual(_publications(result)[self.ECHO]["value"], "true", result.dispositions)


if __name__ == "__main__":
    unittest.main()
