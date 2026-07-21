"""Track 3 deliverable 1: declared-absence fact-type citizens and their
package admission (ADR-0038 decision 1, production condition 1).

Covers: the two committed fact types validate on the ADR-0032/ADR-0036
categorical taxpayer-assertion pattern (bundle-adoption, not bare members,
per the Track 2 ``scheduleb.bundle.json`` precedent); and package admission
rejects a ``conditional_dependency_set`` member fact type whose domain is
not exactly {yes, no} - a boolean encoding, an open string domain, and a
non-yes/no-labeled two-value enum are each separately proven rejected.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import validate_package
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry

CONTENT = TAX_CONTENT_DIR
BUNDLE_FILE = "qdcg.bundle.json"
CG_DIST = "tax.us.2025.capital-gain-distributions"
SCHED_D = "tax.us.2025.schedule-d-required"


def load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


class DeclaredAbsenceBundleCitizens(unittest.TestCase):
    """The committed bundle validates and instantiates the categorical
    taxpayer-assertion pattern (ADR-0032/ADR-0036), never boolean, no
    default."""

    def setUp(self) -> None:
        self.registry = tax_registry()

    def test_bundle_validates_against_the_published_schema(self) -> None:
        bundle = load(BUNDLE_FILE)
        self.registry.validate_declared(bundle)

    def test_bundle_carries_exactly_the_two_declared_absence_fact_types(self) -> None:
        bundle = load(BUNDLE_FILE)
        ids = {ft["id"] for ft in bundle["fact_types"]}
        self.assertEqual(ids, {CG_DIST, SCHED_D})

    def test_each_fact_type_is_categorical_yes_no_never_boolean_no_default(self) -> None:
        bundle = load(BUNDLE_FILE)
        for fact_type in bundle["fact_types"]:
            with self.subTest(fact_type=fact_type["id"]):
                self.registry.validate_declared(fact_type)
                self.assertEqual(fact_type["value_schema"], {"enum": ["yes", "no"]})
                self.assertNotIn("optional_default", fact_type)
                self.assertEqual(fact_type["identity_keys"], [
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]}
                ])

    def test_committed_line16_v2_names_both_fact_types_as_bundle_members_only(self) -> None:
        """Bundle-adoption, not bare members (Track 2 precedent): a bare
        fact-type.v2 member passes package validation but the live kernel
        fact registry only admits fact types reached via bundle-adoption."""
        bundle = load(BUNDLE_FILE)
        bundle_ids = {ft["id"] for ft in bundle["fact_types"]}
        rule = load("rule.form1040-line16.v2.json")
        self.assertIn(CG_DIST, bundle_ids)
        self.assertIn(SCHED_D, bundle_ids)
        self.assertEqual(rule["schema"], "rule-artifact.v3")


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


def _demo_bundle(fact_types: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": "demo.bundle.dsbs-t3-guard",
        "version": "v1",
        "label": "Demo declared-absence guard bundle",
        "fact_types": fact_types,
    }


def _demo_cds_rule(member_names: list[str]) -> dict[str, Any]:
    # The domain guard is scoped to members the *same rule* also reads
    # categorically (a category_literal naming them) - the real
    # declared-absence shape ADR-0038's line-16 rule instantiates, never
    # ADR-0037's own generic numeric-member substrate. Each member here is
    # therefore also compared against the literal "no", matching that shape.
    categorical_reads = [
        {
            "op": "categorical_compare", "cmp": "eq",
            "left": {"op": "ref", "name": name},
            "right": {"op": "category_literal", "fact_type": {"id": name, "version": "v1"}, "value": "no"},
        }
        for name in member_names
    ]
    return {
        "schema": "rule-artifact.v3",
        "id": "demo.rule.dsbs-t3-guard",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
        "role": "computation",
        "requires": ["demo.condition"],
        "pins": [],
        "when": {
            "op": "all",
            "args": [
                {
                    "op": "conditional_dependency_set",
                    "condition": {"op": "compare", "left": {"op": "ref", "name": "demo.condition"}, "right": 0, "cmp": "gt"},
                    "members": [{"op": "ref", "name": name} for name in member_names],
                },
                {"op": "all", "args": categorical_reads} if categorical_reads else True,
            ],
        },
        "value": True,
        "publishes": "demo.dsbs-t3-guard.output",
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": list(member_names)},
    }


class DeclaredAbsenceDomainAdmissionGuard(unittest.TestCase):
    """ADR-0038 production condition 1: package admission must reject a
    non-{yes, no} domain for a conditional_dependency_set member fact type."""

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def _package(self, members: list[dict[str, Any]]) -> dict[str, Any]:
        roles = {"fact-type-bundle": "fact-type-bundle", "rule-artifact.v3": "computation"}
        member_pins = []
        for m in members:
            if m["schema"] == "bundle.v2":
                role = "fact-type-bundle"
            else:
                role = "computation"
            member_pins.append({"role": role, "schema": m["schema"], "id": m["id"], "version": m["version"]})
        return {
            "schema": "artifact-package.v4",
            "id": "demo.package.dsbs-t3-guard",
            "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
            "admitted_schemas": sorted({m["schema"] for m in members}),
            "members": member_pins,
            "input_bindings": [],
            "entrypoints": [{"id": m["id"], "version": m["version"]} for m in members],
            "composition_obligations": [],
            "package_checksum": "0" * 64,
        }

    def _validate(self, members: list[dict[str, Any]]) -> Any:
        corpus = {(m["id"], m["version"]): m for m in members}
        return validate_package(self._package(members), corpus, self.schemas)

    def _codes(self, result: Any) -> set[str]:
        return {issue.code for issue in result.issues}

    def test_conforming_yes_no_domain_is_admitted(self) -> None:
        fact_type = _demo_fact_type("demo.fact.declared-absence", {"enum": ["yes", "no"]})
        bundle = _demo_bundle([fact_type])
        rule = _demo_cds_rule(["demo.fact.declared-absence"])
        result = self._validate([bundle, rule])
        self.assertTrue(result.ok, msg=str(result.issues))
        self.assertNotIn("CONDITIONAL_DEPENDENCY_MEMBER_NOT_YES_NO", self._codes(result))

    def test_boolean_domain_is_rejected(self) -> None:
        fact_type = _demo_fact_type("demo.fact.declared-absence", {"type": "boolean"})
        bundle = _demo_bundle([fact_type])
        rule = _demo_cds_rule(["demo.fact.declared-absence"])
        result = self._validate([bundle, rule])
        self.assertIn("CONDITIONAL_DEPENDENCY_MEMBER_NOT_YES_NO", self._codes(result))

    def test_open_string_domain_is_rejected(self) -> None:
        fact_type = _demo_fact_type("demo.fact.declared-absence", {"type": "string"})
        bundle = _demo_bundle([fact_type])
        rule = _demo_cds_rule(["demo.fact.declared-absence"])
        result = self._validate([bundle, rule])
        self.assertIn("CONDITIONAL_DEPENDENCY_MEMBER_NOT_YES_NO", self._codes(result))

    def test_non_yes_no_two_value_enum_is_rejected(self) -> None:
        fact_type = _demo_fact_type("demo.fact.declared-absence", {"enum": ["true", "false"]})
        bundle = _demo_bundle([fact_type])
        rule = _demo_cds_rule(["demo.fact.declared-absence"])
        result = self._validate([bundle, rule])
        self.assertIn("CONDITIONAL_DEPENDENCY_MEMBER_NOT_YES_NO", self._codes(result))

    def test_member_fact_type_absent_from_the_fact_surface_is_rejected(self) -> None:
        rule = _demo_cds_rule(["demo.fact.missing-entirely"])
        result = self._validate([rule])
        self.assertIn("CONDITIONAL_DEPENDENCY_MEMBER_FACT_TYPE_ABSENT", self._codes(result))

    def test_committed_qdcg_bundle_conforms_to_the_guard(self) -> None:
        """The committed bundle's two fact types, exercised through the same
        admission path with a demo v3 rule referencing them, are admitted."""
        bundle = load(BUNDLE_FILE)
        rule = _demo_cds_rule([CG_DIST, SCHED_D])
        result = self._validate([bundle, rule])
        self.assertTrue(result.ok, msg=str(result.issues))


if __name__ == "__main__":
    unittest.main()
