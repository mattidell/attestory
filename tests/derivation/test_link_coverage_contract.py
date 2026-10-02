"""Track 3 stage B1, amended by ADR 0075: declarative link_coverage contract.

Obligation 14 is schema and package acceptance. Obligation 17 is reusable
admission of the link type, and the sibling scalar binding that must stay
on today's marshal branch. No evaluator behaviour.
"""

from __future__ import annotations

import copy
import unittest
from typing import Any

from packages.derivation.live import _resolved_run_material
from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.package_validation import (
    package_instance_checksum,
    validate_package,
)
from packages.kernel.currency import CurrencyView
from packages.kernel.schema_registry import SchemaValidationError

SCOPE = {"tax_year": 2025, "jurisdiction": "us", "family": "demo-student-loan"}
LINKS = "demo.tax.statement-to-borrowing"
REDUCTIONS = "demo.tax.link-reduction"
OTHER_LINKS = "demo.tax.other-statement-to-borrowing"
OTHER_REDUCTIONS = "demo.tax.other-link-reduction"
BOX1 = "demo.tax.f1098e.box1-student-loan-interest"
PARAM_ID = "demo.param.no-link-reduction"
CITATION_ID = "demo.citation.statement-box-minus-reductions"
COVERAGE_ID = "demo.rule.statement-box-minus-reductions"
REDUCTION_RULE_ID = "demo.rule.link-reduction"
SIBLING = "demo.tax.sibling-scalar"
NAME_REUSED = "LINK_COVERAGE_NAME_REUSED"
INVALID = "LINK_COVERAGE_INVALID"


def _coverage() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v10",
        "id": COVERAGE_ID,
        "version": "v2",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [BOX1],
        "pins": [],
        "when": {
            "op": "compare",
            "cmp": "gt",
            "left": {"op": "ref", "name": BOX1},
            "right": 0,
        },
        "value": {
            "op": "subtract",
            "left": {"op": "ref", "name": BOX1},
            "right": {
                "op": "link_coverage",
                "links": LINKS,
                "reductions": REDUCTIONS,
                "empty": {"parameter": {"id": PARAM_ID, "version": "v1"}},
            },
        },
        "publishes": "demo.tax.statement-facing-amount",
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        "citations": [{"id": CITATION_ID, "version": "v1"}],
    }


def _reduction(
    *,
    rule_id: str = REDUCTION_RULE_ID,
    links: str = LINKS,
    reductions: str = REDUCTIONS,
) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v10",
        "id": rule_id,
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [],
        "pins": [],
        "when": True,
        "value": {"op": "ref", "name": links},
        "publishes": reductions,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }


def _parameter() -> dict[str, Any]:
    return {
        "schema": "parameter-declaration.v1",
        "id": PARAM_ID,
        "version": "v1",
        "scope": dict(SCOPE),
        "values": "0",
    }


def _fact_type(fact_id: str, title: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": title,
        "nature": "determinable",
        "identity_keys": [
            {"name": "statement", "kind": "literal", "values": ["demo-statement"]},
        ],
        "value_schema": {"type": "object"},
        "supersession": {"policy": "free"},
    }


def _citation() -> dict[str, Any]:
    return {
        "schema": "citation.v1",
        "id": CITATION_ID,
        "version": "v1",
        "authority": {
            "family": "irs-publication",
            "publication": "demo-970",
            "revision": "2025",
        },
    }


def _base_parts() -> list[tuple[dict[str, Any], str]]:
    return [
        (_coverage(), "computation"),
        (_reduction(), "computation"),
        (_parameter(), "parameter"),
        (_fact_type(LINKS, "Demo statement to borrowing link"), "fact-type"),
        (_citation(), "citation"),
    ]


def _package(
    parts: list[tuple[dict[str, Any], str]],
    *,
    bindings: list[dict[str, Any]] | None = None,
    entrypoints: list[dict[str, str]] | None = None,
    schema: str = "artifact-package.v31",
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": schema,
        "id": "demo.package.link-coverage",
        "version": "v2",
        "scope": dict(SCOPE),
        "admitted_schemas": sorted({citizen["schema"] for citizen, _role in parts}),
        "members": [
            {
                "role": role,
                "schema": citizen["schema"],
                "id": citizen["id"],
                "version": citizen["version"],
            }
            for citizen, role in parts
        ],
        "input_bindings": list(bindings or []),
        "entrypoints": entrypoints or [{"id": COVERAGE_ID, "version": "v2"}],
        "composition_obligations": [],
    }
    body["package_checksum"] = package_instance_checksum(body)
    return body


def _validate(
    parts: list[tuple[dict[str, Any], str]],
    **kwargs: Any,
) -> Any:
    package = _package(parts, **kwargs)
    corpus = {(citizen["id"], citizen["version"]): citizen for citizen, _role in parts}
    return validate_package(package, corpus, DerivationSchemas()), package


def _codes(result: Any) -> list[str]:
    return [issue.code for issue in result.issues]


class LinkCoverageSchemaAndPackage(unittest.TestCase):
    """Obligation 14, the validation half."""

    def test_worked_example_validates_against_v10(self) -> None:
        DerivationSchemas().validate_declared(_coverage())

    def test_v10_rejects_selection_and_aggregation(self) -> None:
        schemas = DerivationSchemas()
        for field in ("selection", "aggregation"):
            with self.subTest(field=field):
                rule = _coverage()
                rule[field] = {"mode": "exclusive_presence"}
                with self.assertRaises(SchemaValidationError):
                    schemas.validate_declared(rule)

    def test_v31_package_accepts_the_worked_example(self) -> None:
        result, _package_body = _validate(_base_parts())
        self.assertTrue(result.ok, result.issues)
        self.assertNotIn(NAME_REUSED, _codes(result))

    def test_v30_package_rejects_the_same_rule(self) -> None:
        result, _package_body = _validate(_base_parts(), schema="artifact-package.v30")
        self.assertFalse(result.ok)
        self.assertIn("PACKAGE_SCHEMA_INVALID", _codes(result))

    def test_node_in_when_is_rejected_and_is_not_name_reuse(self) -> None:
        parts = _base_parts()
        rule = parts[0][0]
        rule["when"] = copy.deepcopy(rule["value"]["right"])
        rule["value"] = {"op": "ref", "name": BOX1}
        result, _package_body = _validate(
            parts,
            entrypoints=[
                {"id": COVERAGE_ID, "version": "v2"},
                {"id": REDUCTION_RULE_ID, "version": "v1"},
            ],
        )
        self.assertFalse(result.ok)
        self.assertIn(INVALID, _codes(result))
        self.assertNotIn(NAME_REUSED, _codes(result))
        self.assertTrue(any("when" in issue.detail for issue in result.issues))

    def test_names_in_requires_are_accepted(self) -> None:
        for name in (LINKS, REDUCTIONS):
            with self.subTest(name=name):
                parts = _base_parts()
                parts[0][0]["requires"] = [BOX1, name]
                result, _package_body = _validate(parts)
                self.assertTrue(result.ok, result.issues)
                self.assertNotIn(NAME_REUSED, _codes(result))

    def test_unpublished_reductions_are_rejected(self) -> None:
        parts = _base_parts()
        rule = parts[0][0]
        rule["value"] = copy.deepcopy(rule["value"])
        rule["value"]["right"]["reductions"] = "demo.tax.no-such-reduction"
        result, _package_body = _validate(
            parts,
            entrypoints=[
                {"id": COVERAGE_ID, "version": "v2"},
                {"id": REDUCTION_RULE_ID, "version": "v1"},
            ],
        )
        self.assertFalse(result.ok)
        self.assertIn(INVALID, _codes(result))
        self.assertTrue(any("no-such-reduction" in issue.detail for issue in result.issues))

    def test_second_rule_with_different_strings_is_not_an_id_gate(self) -> None:
        other = _coverage()
        other["id"] = "demo.rule.other-statement-box"
        other["version"] = "v1"
        other["publishes"] = "demo.tax.other-statement-facing-amount"
        other["value"] = copy.deepcopy(other["value"])
        other["value"]["right"]["links"] = OTHER_LINKS
        other["value"]["right"]["reductions"] = OTHER_REDUCTIONS
        parts = _base_parts() + [
            (other, "computation"),
            (
                _reduction(
                    rule_id="demo.rule.other-link-reduction",
                    links=OTHER_LINKS,
                    reductions=OTHER_REDUCTIONS,
                ),
                "computation",
            ),
            (_fact_type(OTHER_LINKS, "Demo other statement to borrowing link"), "fact-type"),
        ]
        result, _package_body = _validate(
            parts,
            entrypoints=[
                {"id": COVERAGE_ID, "version": "v2"},
                {"id": other["id"], "version": "v1"},
            ],
        )
        self.assertTrue(result.ok, result.issues)

    def test_second_node_repeating_either_string_is_accepted(self) -> None:
        other = _coverage()
        other["id"] = "demo.rule.other-statement-box"
        other["version"] = "v1"
        other["publishes"] = "demo.tax.other-statement-facing-amount"
        parts = _base_parts() + [(other, "computation")]
        result, _package_body = _validate(
            parts,
            entrypoints=[
                {"id": COVERAGE_ID, "version": "v2"},
                {"id": other["id"], "version": "v1"},
            ],
        )
        self.assertTrue(result.ok, result.issues)
        self.assertNotIn(NAME_REUSED, _codes(result))


class LinkCoverageNameConfinement(unittest.TestCase):
    """Obligation 17: the link type may be named again, and the sibling binding holds."""

    def _with_rule(self, rule: dict[str, Any], *, role: str = "computation") -> Any:
        result, _package_body = _validate(
            _base_parts() + [(rule, role)],
            entrypoints=[
                {"id": COVERAGE_ID, "version": "v2"},
                {"id": rule["id"], "version": rule["version"]},
            ],
        )
        return result

    def test_v2_sibling_ref_of_either_string_is_accepted(self) -> None:
        """A rule-artifact.v2 ref of either string is not a name-reuse rejection."""
        for name in (LINKS, REDUCTIONS):
            for value in (
                {"op": "ref", "name": name},
                {"op": "compare", "cmp": "gt", "left": {"op": "ref", "name": name}, "right": 0},
            ):
                with self.subTest(name=name, value=value):
                    rule = _sibling_value(value)
                    rule["schema"] = "rule-artifact.v2"
                    result = self._with_rule(rule)
                    self.assertNotIn(NAME_REUSED, _codes(result))
                    self.assertTrue(result.ok, result.issues)

    def test_former_confined_uses_of_each_string_are_accepted(self) -> None:
        cases: list[tuple[str, str, dict[str, Any]]] = []
        for name in (LINKS, REDUCTIONS):
            cases.append((
                "requires",
                name,
                {
                    "schema": "rule-artifact.v10",
                    "id": "demo.rule.sibling-use",
                    "version": "v1",
                    "scope": dict(SCOPE),
                    "role": "computation",
                    "requires": [name],
                    "pins": [],
                    "when": True,
                    "value": 0,
                    "publishes": "demo.tax.sibling-output",
                    "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
                },
            ))
            cases.append((
                "ref",
                name,
                _sibling_value({"op": "ref", "name": name}),
            ))
            cases.append((
                "collect",
                name,
                _sibling_value({"op": "collect", "name": name, "source_set": "demo.family.unused"}),
            ))
            cases.append((
                "count",
                name,
                _sibling_value({"op": "count", "name": name, "source_set": "demo.family.unused"}),
            ))
            cases.append((
                "collect_categorical_all_equal",
                name,
                _sibling_value({
                    "op": "collect_categorical_all_equal",
                    "name": name,
                    "value": "demo-yes",
                }),
            ))
        reduction = _reduction()
        reduction["requires"] = [LINKS]
        cases.append(("reduction-rule-requires-links", LINKS, reduction))
        reduction_ref = _reduction()
        reduction_ref["value"] = {"op": "ref", "name": REDUCTIONS}
        cases.append(("reduction-rule-ref-reductions", REDUCTIONS, reduction_ref))

        for kind, name, rule in cases:
            with self.subTest(kind=kind, name=name):
                if rule["id"] == REDUCTION_RULE_ID:
                    parts = _base_parts()
                    parts[1] = (rule, "computation")
                    result, _package_body = _validate(parts)
                else:
                    result = self._with_rule(rule)
                self.assertNotIn(NAME_REUSED, _codes(result))
                self.assertTrue(result.ok, result.issues)

    def test_input_binding_of_the_link_type_is_accepted(self) -> None:
        for kind, binding in (
            ("symbol", {
                "symbol": LINKS,
                "fact_type": {"id": LINKS, "version": "v1"},
                "mode": "required",
            }),
            ("fact_type", {
                "symbol": "demo.symbol.other",
                "fact_type": {"id": LINKS, "version": "v1"},
                "mode": "required",
            }),
        ):
            with self.subTest(kind=kind):
                result, _package_body = _validate(_base_parts(), bindings=[binding])
                self.assertNotIn(NAME_REUSED, _codes(result))
                self.assertTrue(result.ok, result.issues)
        result, _package_body = _validate(
            _base_parts(),
            bindings=[{
                "symbol": "demo.symbol.other",
                "fact_type": {"id": REDUCTIONS, "version": "v1"},
                "mode": "required",
            }],
        )
        self.assertNotIn(NAME_REUSED, _codes(result))

    def test_attachment_symbols_are_not_name_reuse(self) -> None:
        for name in (LINKS, REDUCTIONS):
            for kind, attachment in _attachment_cases(name):
                with self.subTest(kind=kind, name=name):
                    result, _package_body = _validate(
                        _base_parts() + [(attachment, "attachment-rule")],
                        entrypoints=[
                            {"id": COVERAGE_ID, "version": "v2"},
                            {"id": attachment["id"], "version": "v1"},
                        ],
                    )
                    self.assertNotIn(NAME_REUSED, _codes(result))

    def test_reduction_rule_ref_of_links_and_publishes_are_accepted(self) -> None:
        result, _package_body = _validate(_base_parts())
        self.assertTrue(result.ok, result.issues)

    def test_resolved_run_material_emits_the_link_type_and_registers_neither_name(self) -> None:
        result, package = _validate(_base_parts())
        self.assertTrue(result.ok, result.issues)
        with_node = _resolved_run_material(_Graph(result.resolved_members, package))
        bare = _coverage()
        bare["value"] = {"op": "ref", "name": BOX1}
        bare["when"] = True
        without = _resolved_run_material(_Graph(
            [bare, _reduction(), _parameter(), _fact_type(LINKS, "Demo statement to borrowing link"), _citation()],
            {"input_bindings": []},
        ))
        only_when = _coverage()
        only_when["when"] = copy.deepcopy(only_when["value"]["right"])
        only_when["value"] = {"op": "ref", "name": BOX1}
        when_only = _resolved_run_material(_Graph([only_when], {"input_bindings": []}))

        self.assertEqual(with_node[2], [])
        self.assertNotIn(LINKS, with_node[6])
        self.assertNotIn(REDUCTIONS, with_node[6])
        self.assertEqual(with_node.emission_only_names, (LINKS,))
        self.assertNotIn(LINKS, without[6])
        self.assertNotIn(REDUCTIONS, without[6])
        self.assertEqual(without.emission_only_names, ())
        self.assertNotIn(LINKS, when_only[6])
        self.assertNotIn(REDUCTIONS, when_only[6])
        self.assertEqual(when_only.emission_only_names, ())

    def test_sibling_scalar_binding_is_unchanged_and_link_rows_are_sources(self) -> None:
        parts = _base_parts() + [(_fact_type(SIBLING, "Demo sibling scalar"), "fact-type")]
        bindings = [{
            "symbol": SIBLING,
            "fact_type": {"id": SIBLING, "version": "v1"},
            "mode": "required",
        }]
        result, package = _validate(
            parts,
            bindings=bindings,
            entrypoints=[
                {"id": COVERAGE_ID, "version": "v2"},
                {"id": SIBLING, "version": "v1"},
            ],
        )
        self.assertTrue(result.ok, result.issues)
        material = _resolved_run_material(_Graph(result.resolved_members, package))
        _rules, _parameters, families, _mappings, _fact_types, material_bindings, collect_names = material
        self.assertEqual(families, [])
        self.assertNotIn(LINKS, collect_names)
        self.assertNotIn(REDUCTIONS, collect_names)
        self.assertEqual(material.emission_only_names, (LINKS,))

        one = _marshal(collect_names, material_bindings, {
            "demo.finding.sibling.1": _finding(
                "demo.finding.sibling.1", f"{SIBLING}|statement=a", "demo-one",
            ),
            "demo.finding.link.1": _finding(
                "demo.finding.link.1", f"{LINKS}|statement=a", {"linked": "demo"},
            ),
        }, emission_only=list(material.emission_only_names))
        sibling_inputs = [item for item in one.inputs if item.symbol == SIBLING]
        self.assertEqual(len(sibling_inputs), 1)
        self.assertEqual(sibling_inputs[0].value, "demo-one")
        self.assertEqual(sibling_inputs[0].finding_id, "demo.finding.sibling.1")
        self.assertEqual([item.symbol for item in one.inputs if item.symbol in {LINKS, REDUCTIONS}], [])
        link_sources = [source for source in one.sources if source.name == LINKS]
        self.assertEqual([source.finding_id for source in link_sources], ["demo.finding.link.1"])

        several = _marshal(collect_names, material_bindings, {
            "demo.finding.sibling.2": _finding(
                "demo.finding.sibling.2", f"{SIBLING}|statement=b", "demo-agree",
            ),
            "demo.finding.sibling.1": _finding(
                "demo.finding.sibling.1", f"{SIBLING}|statement=a", "demo-agree",
            ),
        })
        agreed = [item for item in several.inputs if item.symbol == SIBLING]
        self.assertEqual(len(agreed), 1)
        self.assertEqual(agreed[0].value, "demo-agree")
        self.assertEqual(agreed[0].finding_id, "demo.finding.sibling.1")


def _sibling_value(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v10",
        "id": "demo.rule.sibling-use",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [],
        "pins": [],
        "when": True,
        "value": value,
        "publishes": "demo.tax.sibling-output",
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }


def _attachment_shell(*, attachment_id: str, schema: str, requirement: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": schema,
        "id": attachment_id,
        "version": "v1",
        "title": "Demo attachment naming a confined symbol",
        "scope": dict(SCOPE),
        "attachment": {
            "authority": "DEMO",
            "form_id": "SCHX",
            "tax_year": 2025,
            "jurisdiction": "us",
        },
        "publishes": "demo.attachment.confined.disposition",
        "requirement": requirement,
        "itemizations": [],
        "completeness": {
            "required_answers": [{
                "symbol": "demo.answer.harmless",
                "fact_type": {"id": LINKS, "version": "v1"},
                "check": "presence",
            }],
        },
    }


def _attachment_cases(name: str) -> list[tuple[str, dict[str, Any]]]:
    pin = {"id": PARAM_ID, "version": "v1"}
    citation = {"id": CITATION_ID, "version": "v1"}
    subtotals = _attachment_shell(
        attachment_id="demo.rule.attachment.subtotals",
        schema="attachment-rule.v1",
        requirement={
            "subtotals": [name],
            "threshold_parameter": pin,
            "comparison": "strictly_greater_than",
            "citation": citation,
        },
    )
    answer = _attachment_shell(
        attachment_id="demo.rule.attachment.answer",
        schema="attachment-rule.v1",
        requirement={
            "subtotals": ["demo.attach.harmless.subtotal"],
            "threshold_parameter": pin,
            "comparison": "strictly_greater_than",
            "citation": citation,
        },
    )
    answer["completeness"]["required_answers"][0]["symbol"] = name
    branch = _attachment_shell(
        attachment_id="demo.rule.attachment.branch",
        schema="attachment-rule.v1",
        requirement={
            "subtotals": ["demo.attach.harmless.subtotal"],
            "threshold_parameter": pin,
            "comparison": "strictly_greater_than",
            "citation": citation,
        },
    )
    branch["completeness"]["branch_requirements"] = [{
        "when_answer": {"symbol": name, "equals": "yes"},
        "adds_required": [{
            "symbol": "demo.answer.added",
            "fact_type": {"id": LINKS, "version": "v1"},
            "check": "presence",
        }],
    }]
    added = _attachment_shell(
        attachment_id="demo.rule.attachment.added",
        schema="attachment-rule.v1",
        requirement={
            "subtotals": ["demo.attach.harmless.subtotal"],
            "threshold_parameter": pin,
            "comparison": "strictly_greater_than",
            "citation": citation,
        },
    )
    added["completeness"]["branch_requirements"] = [{
        "when_answer": {"symbol": "demo.answer.harmless", "equals": "yes"},
        "adds_required": [{
            "symbol": name,
            "fact_type": {"id": LINKS, "version": "v1"},
            "check": "presence",
        }],
    }]
    trigger = _attachment_shell(
        attachment_id="demo.rule.attachment.trigger",
        schema="attachment-rule.v11",
        requirement={
            "kind": "any_trigger",
            "triggers": [{
                "subtotals": [name],
                "threshold_parameter": pin,
                "comparison": "strictly_greater_than",
                "citation": citation,
            }],
        },
    )
    return [
        ("requirement.subtotals", subtotals),
        ("completeness answer", answer),
        ("branch when_answer", branch),
        ("branch adds_required", added),
        ("trigger subtotals", trigger),
    ]


class _Graph:
    def __init__(self, members: list[dict[str, Any]], package: dict[str, Any]) -> None:
        self.resolved_members = members
        self.package = package


class _State:
    def __init__(self, findings: dict[str, dict[str, Any]]) -> None:
        self.findings = findings
        self.horizon_state = type("Horizon", (), {"current_by_chain": {}})()


def _finding(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {"id": finding_id, "fact_id": fact_id, "value": value, "basis": "attested"}


def _marshal(
    collect_names: list[str],
    bindings: list[dict[str, Any]],
    findings: dict[str, dict[str, Any]],
    *,
    emission_only: list[str] | None = None,
    rules: list[dict[str, Any]] | None = None,
) -> Any:
    return marshal_run_context(
        run_id="demo.run.link-coverage",
        state=_State(findings),  # type: ignore[arg-type]
        currency=CurrencyView(
            current_finding_ids=frozenset(findings),
            displaced_finding_ids=frozenset(),
            current_evidence_ids=frozenset(),
            displaced_evidence_ids=frozenset(),
        ),
        rules=list(rules or []),
        parameters={},
        canon={},
        adoption_pin={"role": "adoption", "id": "demo.package.link-coverage", "version": "v2"},
        governance_pins=[],
        input_bindings=bindings,
        collect_source_names=collect_names,
        emission_only_source_names=list(emission_only or []),
    )
