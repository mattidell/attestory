"""Track 5e exact category producer metadata on validated execution paths."""
from __future__ import annotations

import unittest
from typing import Any

from packages.derivation.evaluator import (
    AccessLog, BLOCK_CATEGORICAL_DOMAIN_MISMATCH, Environment, EvalBlocked, evaluate,
)
from tests.derivation.test_exact_version_authority import (
    DerivedCategoricalFallback,
    _blocked,
    _run,
)
from tests.derivation.test_exact_version_authority import _publications  # type: ignore[attr-defined]
from tests.derivation.test_exact_version_authority import _finding  # type: ignore[attr-defined]
from tests.derivation.test_exact_version_authority import _lattice_type  # type: ignore[attr-defined]
from tests.derivation.test_exact_version_authority import _v11_rule  # type: ignore[attr-defined]
from tests.derivation.test_exact_version_authority import _with_schema
from tests.derivation.test_exact_version_authority import _parameter
from tests.derivation.test_subject_declaration_live_path import _ordinary_rule
from tests.derivation.test_subject_declaration_live_path import _package_fact_type


class DerivedCategoryTypes(unittest.TestCase):
    def test_subject_result_may_retain_a_distinct_producer_category(self) -> None:
        source_type = "demo.subject.category-a"
        published_type = "demo.derived.category-b"
        source_fact = f"{source_type}|period=demo"
        published_symbol = f"{published_type}|{source_fact}"
        producer = _v11_rule(
            rule_id="demo.rule.category-a-to-b-symbol",
            subject={"id": source_type, "version": "v1"},
            publishes=published_type,
            value={
                "op": "category_literal",
                "fact_type": {"id": source_type, "version": "v1"},
                "value": "a-value",
            },
        )
        consumer_a = _v11_rule(
            rule_id="demo.rule.subject-b-reads-category-a",
            subject={"id": published_type, "version": "v1"},
            publishes="demo.derived.subject-b-accepts-a",
            value={
                "op": "categorical_compare", "cmp": "eq",
                "left": {"op": "ref", "name": published_type},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": source_type, "version": "v1"},
                    "value": "a-value",
                },
            },
        )
        consumer_b = _v11_rule(
            rule_id="demo.rule.subject-b-rejects-category-b",
            subject={"id": published_type, "version": "v1"},
            publishes="demo.derived.subject-b-rejects-b",
            value={
                "op": "categorical_compare", "cmp": "eq",
                "left": {"op": "ref", "name": published_type},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": published_type, "version": "v1"},
                    "value": "b-value",
                },
            },
        )
        ordinary_a = _ordinary_rule(
            rule_id="demo.rule.ordinary-b-reads-category-a",
            requires=[published_symbol],
            publishes="demo.derived.ordinary-b-accepts-a",
            value={
                "op": "categorical_compare", "cmp": "eq",
                "left": {"op": "ref", "name": published_symbol},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": source_type, "version": "v1"},
                    "value": "a-value",
                },
            },
        )
        ordinary_b = _ordinary_rule(
            rule_id="demo.rule.ordinary-b-rejects-category-b",
            requires=[published_symbol],
            publishes="demo.derived.ordinary-b-rejects-b",
            value={
                "op": "categorical_compare", "cmp": "eq",
                "left": {"op": "ref", "name": published_symbol},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": published_type, "version": "v1"},
                    "value": "b-value",
                },
            },
        )
        source = _with_schema(source_type, "v1", {"type": "string", "enum": ["a-value"]})
        destination = _with_schema(published_type, "v1", {"type": "string", "enum": ["b-value"]})
        parts = [(producer, "computation"), (consumer_a, "computation"),
                 (consumer_b, "computation"), (ordinary_a, "computation"),
                 (ordinary_b, "computation"), (source, "fact-type"),
                 (destination, "fact-type")]
        findings = {
            "demo.finding.category-a": _finding("demo.finding.category-a", source_fact, "a-value")
        }
        lattice = {source_type: _lattice_type(source_type, (("period", ("demo",)),))}

        for result in _run(parts, findings, lattice):
            published = _publications(result)
            producer_finding = published[published_symbol]
            accepted_symbol = f"demo.derived.subject-b-accepts-a|{source_fact}"
            self.assertIn(accepted_symbol, published, result.dispositions)
            self.assertEqual(published[accepted_symbol]["value"], "true", result.dispositions)
            self.assertIn(
                producer_finding["id"],
                {pin["id"] for pin in published[accepted_symbol]["pins"] if pin.get("role") == "input"},
            )
            ordinary_a_symbol = "demo.derived.ordinary-b-accepts-a"
            self.assertEqual(published[ordinary_a_symbol]["value"], "true", result.dispositions)
            self.assertIn(
                producer_finding["id"],
                {pin["id"] for pin in published[ordinary_a_symbol]["pins"] if pin.get("role") == "input"},
            )
            ordinary_b_rows = [
                row for row in result.dispositions
                if row.get("artifact_id") == "demo.rule.ordinary-b-rejects-category-b"
                and row.get("disposition") == "blocked"
            ]
            self.assertEqual(len(ordinary_b_rows), 1, result.dispositions)
            self.assertEqual(ordinary_b_rows[0].get("code"), "CATEGORICAL_DOMAIN_MISMATCH")
            self.assertIn(
                producer_finding["id"],
                {pin["id"] for pin in ordinary_b_rows[0]["pins"] if pin.get("role") == "input"},
            )
            rejected_symbol = f"demo.derived.subject-b-rejects-b|{source_fact}"
            rejected = [
                row for row in result.dispositions
                if row.get("artifact_id") == "demo.rule.subject-b-rejects-category-b"
                and row.get("disposition") == "blocked"
                and row.get("symbol") == rejected_symbol
            ]
            self.assertEqual(len(rejected), 1, result.dispositions)
            self.assertEqual(rejected[0].get("code"), "CATEGORICAL_DOMAIN_MISMATCH")
            self.assertIn(
                producer_finding["id"],
                {pin["id"] for pin in rejected[0]["pins"] if pin.get("role") == "input"},
            )

    def test_subject_result_type_reaches_all_consumer_routes(self) -> None:
        subject = "demo.subject.typed-source"
        joined_subject = "demo.subject.typed-joiner"
        result_type = "demo.derived.subject-result"
        subject_a = f"{subject}|who=a"
        subject_b = f"{subject}|who=b"
        join_a = f"{joined_subject}|who=a"
        join_b = f"{joined_subject}|who=b"
        result_a = f"{result_type}|{subject_a}"
        result_b = f"{result_type}|{subject_b}"

        producer = _v11_rule(
            rule_id="demo.rule.subject-result-producer",
            subject={"id": subject, "version": "v1"},
            publishes=result_type,
            value={
                "op": "choose",
                "when": {
                    "op": "categorical_compare", "cmp": "eq",
                    "left": {"op": "ref", "name": subject},
                    "right": {"op": "category_literal", "fact_type": {"id": subject, "version": "v1"}, "value": "a"},
                },
                "then": {"op": "category_literal", "fact_type": {"id": result_type, "version": "v1"}, "value": "yes"},
                "else": {"op": "category_literal", "fact_type": {"id": result_type, "version": "v2"}, "value": "no"},
            },
        )

        def compare_rule(rule_id: str, target: str, version: str, value: str, *, on_subject: bool) -> dict[str, Any]:
            return _v11_rule(
                rule_id=rule_id,
                subject={"id": target, "version": version if on_subject else "v1"},
                joined=None if on_subject else {"id": result_type, "version": version},
                direction=None if on_subject else "joined_contains_subject",
                requires=[] if on_subject else [result_type],
                publishes=f"{rule_id}.output",
                value={
                    "op": "categorical_compare", "cmp": "eq",
                    "left": {"op": "ref", "name": target if on_subject else result_type},
                    "right": {"op": "category_literal", "fact_type": {"id": result_type, "version": version}, "value": value},
                },
            )

        subject_a_match = _v11_rule(
            rule_id="demo.rule.subject-a-match",
            subject={"id": subject, "version": "v1"},
            publishes="demo.derived.subject-a-match",
            value={
                "op": "categorical_compare", "cmp": "eq",
                "left": {"op": "ref", "name": subject},
                "right": {"op": "category_literal", "fact_type": {"id": subject, "version": "v1"}, "value": "a"},
            },
        )
        subject_a_wrong_domain = _v11_rule(
            rule_id="demo.rule.subject-a-wrong-domain",
            subject={"id": subject, "version": "v1"},
            publishes="demo.derived.subject-a-wrong-domain",
            value={
                "op": "categorical_compare", "cmp": "eq",
                "left": {"op": "ref", "name": subject},
                "right": {"op": "category_literal", "fact_type": {"id": result_type, "version": "v1"}, "value": "yes"},
            },
        )
        subject_b_v1 = compare_rule("demo.rule.subject-b-v1", result_type, "v1", "yes", on_subject=True)
        subject_b_v2 = compare_rule("demo.rule.subject-b-v2", result_type, "v2", "no", on_subject=True)
        joined_v1 = compare_rule("demo.rule.joined-b-v1", joined_subject, "v1", "yes", on_subject=False)
        joined_v2 = compare_rule("demo.rule.joined-b-v2", joined_subject, "v2", "no", on_subject=False)

        exact_a = _ordinary_rule(
            rule_id="demo.rule.ordinary-exact-a", requires=[result_a],
            publishes="demo.derived.ordinary-exact-a",
            value={"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": result_a}, "right": {"op": "category_literal", "fact_type": {"id": result_type, "version": "v1"}, "value": "yes"}},
        )
        exact_b = _ordinary_rule(
            rule_id="demo.rule.ordinary-exact-b", requires=[result_b],
            publishes="demo.derived.ordinary-exact-b",
            value={"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": result_b}, "right": {"op": "category_literal", "fact_type": {"id": result_type, "version": "v2"}, "value": "no"}},
        )
        wrong_exact = _ordinary_rule(
            rule_id="demo.rule.ordinary-wrong-version", requires=[result_a],
            publishes="demo.derived.ordinary-wrong-version",
            value={"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": result_a}, "right": {"op": "category_literal", "fact_type": {"id": result_type, "version": "v2"}, "value": "no"}},
        )

        def typed_fact(fact_id: str, version: str, enum: list[str]) -> dict[str, Any]:
            fact = _package_fact_type(fact_id, ["who"], version=version)
            fact["identity_keys"][0]["values"] = ["a", "b"]
            fact["value_schema"] = {"type": "string", "enum": enum}
            return fact

        parts = [
            (producer, "computation"), (subject_a_match, "computation"),
            (subject_a_wrong_domain, "computation"), (subject_b_v1, "computation"),
            (subject_b_v2, "computation"), (joined_v1, "computation"),
            (joined_v2, "computation"), (exact_a, "computation"),
            (exact_b, "computation"), (wrong_exact, "computation"),
            (typed_fact(subject, "v1", ["a", "b"]), "fact-type"),
            (typed_fact(joined_subject, "v1", ["joined"]), "fact-type"),
            (typed_fact(result_type, "v1", ["yes"]), "fact-type"),
            (typed_fact(result_type, "v2", ["no"]), "fact-type"),
        ]
        facts = {
            "demo.finding.subject-a": _finding("demo.finding.subject-a", subject_a, "a"),
            "demo.finding.subject-b": _finding("demo.finding.subject-b", subject_b, "b"),
            "demo.finding.join-a": _finding("demo.finding.join-a", join_a, "joined"),
            "demo.finding.join-b": _finding("demo.finding.join-b", join_b, "joined"),
        }
        lattice = {
            subject: _lattice_type(subject, (("who", ("a", "b")),)),
            joined_subject: _lattice_type(joined_subject, (("who", ("a", "b")),)),
        }

        for result in _run(parts, facts, lattice):
            published = _publications(result)
            for symbol, expected in ((result_a, "yes"), (result_b, "no")):
                self.assertEqual(published[symbol]["value"], expected, result.dispositions)
            self.assertEqual(published["demo.derived.subject-a-match|" + subject_a]["value"], "true")
            self.assertEqual(published["demo.derived.subject-a-match|" + subject_b]["value"], "false")
            self.assertEqual(
                {pin["id"] for pin in published["demo.derived.subject-a-match|" + subject_a]["pins"] if pin.get("role") == "input"},
                {"demo.finding.subject-a"},
            )
            self.assertEqual(
                {pin["id"] for pin in published["demo.derived.subject-a-match|" + subject_b]["pins"] if pin.get("role") == "input"},
                {"demo.finding.subject-b"},
            )
            self.assertEqual(
                {row.get("code") for row in result.dispositions if row.get("artifact_id") == "demo.rule.subject-a-wrong-domain"},
                {"CATEGORICAL_DOMAIN_MISMATCH"},
            )

            actual_by_who = {"a": (result_a, "v1", "demo.finding.subject-a"), "b": (result_b, "v2", "demo.finding.subject-b")}
            for who, (source_symbol, version, source_finding_id) in actual_by_who.items():
                source_finding = published[source_symbol]
                subject_consumer = f"demo.rule.subject-b-{version}.output|{source_symbol.split('|', 1)[1]}"
                self.assertEqual(published[subject_consumer]["value"], "true", result.dispositions)
                self.assertIn(source_finding["id"], {pin["id"] for pin in published[subject_consumer]["pins"] if pin.get("role") == "input"})

                joined_consumer = f"demo.rule.joined-b-{version}.output|{join_a if who == 'a' else join_b}"
                self.assertEqual(published[joined_consumer]["value"], "true", result.dispositions)
                self.assertIn(source_finding["id"], {pin["id"] for pin in published[joined_consumer]["pins"] if pin.get("role") == "input"})

                ordinary_consumer = "demo.derived.ordinary-exact-a" if who == "a" else "demo.derived.ordinary-exact-b"
                self.assertEqual(published[ordinary_consumer]["value"], "true", result.dispositions)
                self.assertIn(source_finding["id"], {pin["id"] for pin in published[ordinary_consumer]["pins"] if pin.get("role") == "input"})
                self.assertIn(source_finding_id, {pin["id"] for pin in source_finding["pins"] if pin.get("role") == "input"})

            for rule_id, matching_subject, mismatching_subject in (
                ("demo.rule.subject-b-v1", subject_a, subject_b),
                ("demo.rule.subject-b-v2", subject_b, subject_a),
                ("demo.rule.joined-b-v1", join_a, join_b),
                ("demo.rule.joined-b-v2", join_b, join_a),
            ):
                expected_symbol = f"{rule_id}.output|{matching_subject}"
                self.assertEqual(published[expected_symbol]["value"], "true", result.dispositions)
                blocked_symbol = f"{rule_id}.output|{mismatching_subject}"
                blocked_rows = [
                    row for row in result.dispositions
                    if row.get("artifact_id") == rule_id
                    and row.get("disposition") == "blocked"
                    and row.get("symbol") == blocked_symbol
                ]
                self.assertEqual(len(blocked_rows), 1, result.dispositions)
                self.assertEqual(
                    blocked_rows[0].get("code"), "CATEGORICAL_DOMAIN_MISMATCH",
                    (rule_id, blocked_rows[0]),
                )
            self.assertEqual(
                [row.get("code") for row in result.dispositions if row.get("artifact_id") == "demo.rule.ordinary-wrong-version"],
                ["CATEGORICAL_DOMAIN_MISMATCH"],
            )

    def test_subject_keyed_sources_keep_each_subjects_exact_type(self) -> None:
        subject = "demo.derived.subject"
        output = "demo.derived.subject-output"
        final = "demo.derived.subject-final"
        producer = _v11_rule(
            rule_id="demo.rule.subject-type-producer",
            subject={"id": subject, "version": "v1"},
            value={"op": "choose", "when": {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": subject}, "right": {"op": "category_literal", "fact_type": {"id": subject, "version": "v1"}, "value": "a"}},
                   "then": {"op": "category_literal", "fact_type": {"id": output, "version": "v1"}, "value": "yes"},
                   "else": {"op": "category_literal", "fact_type": {"id": output, "version": "v2"}, "value": "no"}},
            publishes=output,
        )
        consumer = _v11_rule(
            rule_id="demo.rule.subject-type-consumer",
            subject={"id": subject, "version": "v1"},
            requires=[output],
            value={"op": "choose", "when": {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": subject}, "right": {"op": "category_literal", "fact_type": {"id": subject, "version": "v1"}, "value": "a"}},
                   "then": {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": output}, "right": {"op": "category_literal", "fact_type": {"id": output, "version": "v1"}, "value": "yes"}},
                   "else": {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": output}, "right": {"op": "category_literal", "fact_type": {"id": output, "version": "v2"}, "value": "no"}}},
            publishes=final,
        )
        keyed_a = f"{output}|{subject}|who=a"
        keyed_b = f"{output}|{subject}|who=b"
        ordinary_a = _ordinary_rule(
            rule_id="demo.rule.subject-type-exact-a",
            requires=[keyed_a], publishes="demo.derived.subject-exact-a",
            value={"op": "categorical_compare", "cmp": "eq",
                   "left": {"op": "ref", "name": keyed_a},
                   "right": {"op": "category_literal", "fact_type": {"id": output, "version": "v1"}, "value": "yes"}},
        )
        ordinary_b = _ordinary_rule(
            rule_id="demo.rule.subject-type-exact-b",
            requires=[keyed_b], publishes="demo.derived.subject-exact-b",
            value={"op": "categorical_compare", "cmp": "eq",
                   "left": {"op": "ref", "name": keyed_b},
                   "right": {"op": "category_literal", "fact_type": {"id": output, "version": "v2"}, "value": "no"}},
        )
        subject_type = _with_schema(subject, "v1", {"type": "string", "enum": ["a", "b"]})
        subject_type["identity_keys"] = [{"name": "who", "kind": "literal", "values": ["a", "b"]}]
        facts = [f"{subject}|who=a", f"{subject}|who=b"]
        findings = {
            f"demo.finding.subject-{who}": _finding(f"demo.finding.subject-{who}", fact, who)
            for who, fact in zip(("a", "b"), facts, strict=True)
        }
        lattice = {subject: _lattice_type(subject, (("who", ("a", "b")),))}
        parts = [(producer, "computation"), (consumer, "computation"), (ordinary_a, "computation"), (ordinary_b, "computation"), (subject_type, "fact-type"),
                 (_with_schema(output, "v1", {"type": "string", "enum": ["yes"]}), "fact-type"),
                 (_with_schema(output, "v2", {"type": "string", "enum": ["no"]}), "fact-type")]
        for result in _run(parts, findings, lattice):
            published = _publications(result)
            self.assertEqual(published.get(f"{final}|{facts[0]}", {}).get("value"), "true", result.dispositions)
            self.assertEqual(published.get(f"{final}|{facts[1]}", {}).get("value"), "true", result.dispositions)
            self.assertEqual(published.get("demo.derived.subject-exact-a", {}).get("value"), "true", result.dispositions)
            self.assertEqual(published.get("demo.derived.subject-exact-b", {}).get("value"), "true", result.dispositions)

    def test_selected_branch_types_follow_value_and_preserve_guard_pins(self) -> None:
        case = DerivedCategoricalFallback()
        for selected, expected_version, unselected_version in (
            (True, "v1", "v2"), (False, "v2", "v1"),
        ):
            parts = case._parts([("v1", ["yes"]), ("v2", ["no"])], v1_first=False)
            producer = parts[0][0]
            guard = "demo.derived.branch-guard"
            selected_ref = f"demo.derived.branch-{expected_version}"
            unselected_ref = f"demo.derived.branch-{unselected_version}"
            producer["requires"] = [guard, selected_ref, unselected_ref]
            producer["value"] = {
                "op": "choose",
                "when": {"op": "categorical_compare", "cmp": "eq",
                         "left": {"op": "ref", "name": guard},
                         "right": {"op": "category_literal", "fact_type": {"id": guard, "version": "v1"}, "value": "yes"}},
                "then": {"op": "ref", "name": selected_ref} if selected else {"op": "ref", "name": unselected_ref},
                "else": {"op": "ref", "name": unselected_ref} if selected else {"op": "ref", "name": selected_ref},
            }
            # The branch producers carry their exact version into the symbols
            # read by choose. The unused ref must never become a value pin.
            branch_ids = {"v1": f"demo.derived.branch-v1", "v2": f"demo.derived.branch-v2"}
            branch_rules = [
                (_ordinary_rule(
                    rule_id=f"demo.rule.branch-{version}", publishes=branch_ids[version],
                    value={"op": "category_literal", "fact_type": {"id": case.FACT, "version": version},
                           "value": "yes" if version == "v1" else "no"},
                ), "computation") for version in ("v1", "v2")
            ]
            guard_fact = _with_schema(guard, "v1", {"type": "string", "enum": ["yes", "no"]})
            bindings = [{"symbol": guard, "fact_type": {"id": guard, "version": "v1"}, "mode": "required"}]
            consumer = parts[1][0]
            consumer["value"]["right"]["fact_type"]["version"] = expected_version
            consumer["value"]["right"]["value"] = "yes" if selected else "no"

            def check(result: Any) -> None:
                published = _publications(result)
                self.assertIn("demo.tax.exact.derived-echo", published, result.dispositions)
                self.assertEqual(published["demo.tax.exact.derived-echo"]["value"], "true")
                producer_finding = published[case.FACT]
                consumer_finding = published["demo.tax.exact.derived-echo"]
                pins = producer_finding["pins"]
                selected_finding = published[selected_ref]
                unselected_finding = published[unselected_ref]
                self.assertIn(
                    {"role": "input", "id": "demo.finding.branch-guard", "version": "v1", "origin": "assertion"},
                    pins,
                )
                self.assertIn(
                    {"role": "input", "id": selected_finding["id"], "version": "v2", "origin": "assertion"},
                    pins,
                )
                self.assertNotIn(unselected_finding["id"], {pin["id"] for pin in pins})
                self.assertIn(
                    {"role": "input", "id": producer_finding["id"], "version": "v2", "origin": "assertion"},
                    consumer_finding["pins"],
                )

            package_parts = [(producer, "computation"), *branch_rules, (guard_fact, "fact-type"), *parts[1:]]
            for version in ("v1", "v2"):
                package_parts.append((_with_schema(branch_ids[version], "v1", {"type": "string", "enum": ["yes", "no"]}), "fact-type"))
            findings = {"demo.finding.branch-guard": _finding("demo.finding.branch-guard", f"{guard}|period=demo", "yes" if selected else "no")}
            for result in _run(package_parts, findings, bindings=bindings):
                check(result)

    def test_typed_input_copy_preserves_category_across_orders_and_runners(self) -> None:
        source = "demo.derived.input-source"
        output = "demo.derived.input-copy"
        echo = "demo.derived.input-echo"
        producer = _ordinary_rule(rule_id="demo.rule.input-copy", publishes=output,
                                  requires=[source], value={"op": "ref", "name": source})
        consumer = _ordinary_rule(rule_id="demo.rule.input-copy-consumer", publishes=echo,
                                  requires=[output], value={
                                      "op": "categorical_compare", "cmp": "eq",
                                      "left": {"op": "ref", "name": output},
                                      "right": {"op": "category_literal", "fact_type": {"id": source, "version": "v1"}, "value": "yes"},
                                  })
        fact_v1 = _with_schema(source, "v1", {"type": "string", "enum": ["yes", "no"]})
        fact_v2 = _with_schema(source, "v2", {"type": "number"})
        bindings = [{"symbol": source, "fact_type": {"id": source, "version": "v1"}, "mode": "required"}]
        finding = {"demo.finding.input-source": _finding("demo.finding.input-source", f"{source}|period=demo", "yes")}
        for v1_first in (True, False):
            ordered = ((fact_v1, "fact-type"), (fact_v2, "fact-type")) if v1_first else ((fact_v2, "fact-type"), (fact_v1, "fact-type"))
            parts = [(producer, "computation"), (consumer, "computation"),
                     *ordered]
            for result in _run(parts, finding, bindings=bindings):
                self.assertEqual(_publications(result)[output]["value"], "yes")
                input_copy_pins = [pin for pin in _publications(result)[output]["pins"] if pin.get("role") == "input"]
                self.assertEqual(input_copy_pins, [{"role": "input", "id": "demo.finding.input-source", "version": "v1", "origin": "assertion"}])
                self.assertIn(echo, _publications(result), result.dispositions)
                self.assertEqual(_publications(result)[echo]["value"], "true", result.dispositions)

    def test_typed_optional_default_copy_preserves_category_across_orders_and_runners(self) -> None:
        source = "demo.derived.default-source"
        output = "demo.derived.default-copy"
        echo = "demo.derived.default-echo"
        param = "demo.param.derived-default"
        fact_v1 = _with_schema(source, "v1", {"type": "string", "enum": ["yes", "no"]})
        fact_v1["optional_default"] = {"parameter": {"id": param, "version": "v1"}}
        fact_v2 = _with_schema(source, "v2", {"type": "number"})
        binding = {"symbol": source, "fact_type": {"id": source, "version": "v1"}, "mode": "optional_default"}
        producer = _ordinary_rule(rule_id="demo.rule.default-copy", publishes=output,
                                  requires=[source], value={"op": "ref", "name": source})
        consumer = _ordinary_rule(rule_id="demo.rule.default-copy-consumer", publishes=echo,
                                  requires=[output], value={
                                      "op": "categorical_compare", "cmp": "eq",
                                      "left": {"op": "ref", "name": output},
                                      "right": {"op": "category_literal", "fact_type": {"id": source, "version": "v1"}, "value": "yes"},
                                  })
        for v1_first in (True, False):
            ordered = ((fact_v1, "fact-type"), (fact_v2, "fact-type")) if v1_first else ((fact_v2, "fact-type"), (fact_v1, "fact-type"))
            parts = [(producer, "computation"), (consumer, "computation"), *ordered,
                     (_parameter(param, "v1", "yes"), "parameter"), (_parameter(param, "v2", "no"), "parameter")]
            for result in _run(parts, bindings=[binding]):
                self.assertEqual(_publications(result)[output]["value"], "yes")
                default_pin = next(pin for pin in _publications(result)[output]["pins"] if pin.get("role") == "input")
                self.assertEqual(default_pin["origin"], "declared_default")
                default_finding = next(pub.finding for pub in result.publications if pub.finding["id"] == default_pin["id"])
                self.assertEqual(
                    {(pin.get("id"), pin.get("version")) for pin in default_finding["pins"] if pin.get("role") == "parameter"},
                    {(param, "v1")},
                )
                self.assertNotIn((param, "v2"), {(pin.get("id"), pin.get("version")) for pin in default_finding["pins"] if pin.get("role") == "parameter"})
                self.assertIn(echo, _publications(result), result.dispositions)
                self.assertEqual(_publications(result)[echo]["value"], "true", result.dispositions)

    def test_unselected_invalid_branch_is_not_evaluated(self) -> None:
        case = DerivedCategoricalFallback()
        parts = case._parts([("v1", ["yes"]), ("v2", ["no"])], v1_first=True)
        parts[0][0]["value"] = {
            "op": "choose", "when": True,
            "then": {"op": "category_literal", "fact_type": {"id": case.FACT, "version": "v1"}, "value": "yes"},
            "else": {"op": "category_literal", "fact_type": {"id": case.FACT, "version": "v2"}, "value": "invalid"},
        }
        for result in _run(parts):
            self.assertEqual(_publications(result)[case.FACT]["value"], "yes")
            self.assertFalse(_blocked(result, case.PRODUCER), result.dispositions)

    def test_guard_category_does_not_type_numeric_or_boolean_results(self) -> None:
        guard = "demo.derived.typed-guard"
        number = "demo.derived.guard-number"
        boolean = "demo.derived.guard-boolean"
        guard_fact = _with_schema(guard, "v1", {"type": "string", "enum": ["yes", "no"]})
        number_rule = _ordinary_rule(
            rule_id="demo.rule.guard-number", requires=[guard], publishes=number, value=7,
        )
        number_rule["when"] = {
            "op": "categorical_compare", "cmp": "eq",
            "left": {"op": "ref", "name": guard},
            "right": {"op": "category_literal", "fact_type": {"id": guard, "version": "v1"}, "value": "yes"},
        }
        boolean_rule = _ordinary_rule(
            rule_id="demo.rule.guard-boolean", requires=[guard], publishes=boolean,
            value={"op": "categorical_compare", "cmp": "eq",
                   "left": {"op": "ref", "name": guard},
                   "right": {"op": "category_literal", "fact_type": {"id": guard, "version": "v1"}, "value": "yes"}},
        )
        consumers = [
            _ordinary_rule(rule_id=f"demo.rule.consume-{name}", requires=[name], publishes=f"demo.derived.bad-{name}", value={
                "op": "categorical_compare", "cmp": "eq",
                "left": {"op": "ref", "name": name},
                "right": {"op": "category_literal", "fact_type": {"id": guard, "version": "v1"}, "value": "yes"},
            }) for name in (number, boolean)
        ]
        parts = [(number_rule, "computation"), (boolean_rule, "computation"), *[(rule, "computation") for rule in consumers], (guard_fact, "fact-type")]
        finding = {"demo.finding.typed-guard": _finding("demo.finding.typed-guard", f"{guard}|period=demo", "yes")}
        bindings = [{"symbol": guard, "fact_type": {"id": guard, "version": "v1"}, "mode": "required"}]
        for result in _run(parts, finding, bindings=bindings):
            published = _publications(result)
            self.assertEqual(published[number]["value"], "7", result.dispositions)
            self.assertEqual(published[boolean]["value"], "true", result.dispositions)
            for rule in consumers:
                blocked = _blocked(result, rule["id"])
                self.assertTrue(blocked, result.dispositions)
                self.assertEqual(blocked[0]["code"], BLOCK_CATEGORICAL_DOMAIN_MISMATCH)

    def test_field_projection_does_not_inherit_parent_category(self) -> None:
        env = Environment(
            symbols={"demo.parent": {"label": "yes"}}, sources={}, closed_sets=frozenset(),
            parameters={}, canon={}, categorical_domains={
                "demo.category\x1fv1": ["yes"],
            }, symbol_result_fact_types={"demo.parent": ("demo.category", "v1")},
        )
        access = AccessLog()
        self.assertEqual(evaluate({"op": "ref", "name": "demo.parent", "field": "label"}, env, access), "yes")
        self.assertIsNone(access.result_fact_type)
        with self.assertRaises(EvalBlocked) as mismatch:
            evaluate({
                "op": "categorical_compare", "cmp": "eq",
                "left": {"op": "ref", "name": "demo.parent", "field": "label"},
                "right": {"op": "category_literal", "fact_type": {"id": "demo.category", "version": "v1"}, "value": "yes"},
            }, env, AccessLog())
        self.assertEqual(mismatch.exception.category, BLOCK_CATEGORICAL_DOMAIN_MISMATCH)
