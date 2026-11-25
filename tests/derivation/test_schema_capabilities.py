"""Structural completeness, AST anti-allowlist, and drift-fix guards for schema_capabilities."""

from __future__ import annotations

import ast
import copy
import json
import re
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DERIVATION_SCHEMA_DIR, DerivationSchemas, TAX_SCHEMA_DIR
from packages.derivation.package_validation import package_instance_checksum, validate_package
from packages.derivation.schema_capabilities import (
    ALL_EXECUTABLE_RULE_AND_ATTACHMENT_SCHEMAS,
    ALL_VALIDATION_GRAPH_SCHEMAS,
    ARTIFACT_PACKAGE_CAPABILITIES,
    ATTACHMENT_ADJUSTMENT_ROWS_EXECUTABLE_SCHEMAS,
    ATTACHMENT_ADJUSTMENT_ROWS_PROJECTION_SCHEMAS,
    ATTACHMENT_BFS_SCHEMAS,
    ATTACHMENT_CONDITIONAL_LIMITED_PART_SCHEMAS,
    ATTACHMENT_EAGER_ADJUSTMENT_REQUIRES_SCHEMAS,
    ATTACHMENT_EXECUTABLE_SCHEMAS,
    ATTACHMENT_EXCLUSIVE_SELECTION_SCHEMAS,
    ATTACHMENT_LEGACY_SINGLE_ROW_SET_SCHEMAS,
    ATTACHMENT_PROJECTION_ROW_SETS_SCHEMAS,
    ATTACHMENT_PROJECTION_SCHEMAS,
    ATTACHMENT_ROW_SET_SCHEMAS,
    ATTACHMENT_RULE_CAPABILITIES,
    PACKAGE_EXACT_ENTRYPOINT_SCHEMAS,
    PACKAGE_READER_ROLE_SCHEMAS,
    PACKAGE_UNIVERSE_GUARD_SCHEMAS,
    RULE_ARTIFACT_CAPABILITIES,
    RULE_ARTIFACT_SCHEMAS,
    RULE_DECLARED_REFS_OUTSIDE_REQUIRES,
    RULE_FIELD_REF_SCHEMAS,
    RULE_FIELD_REF_TOP_LEVEL_SCHEMAS,
    RULE_LINE2B_V9_SCHEMAS,
    RULE_LINK_COUNT_SCHEMAS,
    RULE_LINK_COVERAGE_SCHEMAS,
    RULE_READER_ROLE_SCHEMAS,
    RULE_REQUIRE_PAIRED_SCHEMAS,
    RULE_SHARED_KEY_COUNT_SCHEMAS,
    RULE_SUBJECT_OPTIONAL_SCHEMAS,
    RULE_SUBJECT_SCHEMAS,
    RULE_V2_RECORD_SCHEMAS,
    RULE_V13_SELECTION_SCHEMAS,
    RULE_VALIDATION_GRAPH_SCHEMAS,
    artifact_package_caps,
    attachment_rule_caps,
    rule_artifact_caps,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DERIVATION_DIR = REPO_ROOT / "packages" / "derivation"
_VERSIONED_SCHEMA_RE = re.compile(r"^(rule-artifact|attachment-rule|artifact-package)\.v\d+$")
_PREFIX_RE = re.compile(r"^(rule-artifact|attachment-rule|artifact-package)\.$")
_MANIFEST_ENTRY_RE = re.compile(r"^(rule-artifact|attachment-rule|artifact-package)\.v\d+(?=\.schema\.json$)")


def _extract_string_collection(node: ast.AST) -> list[str] | None:
    if isinstance(node, (ast.Set, ast.Tuple, ast.List)):
        values: list[str] = []
        for elt in node.elts:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                values.append(elt.value)
        return values
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "frozenset"
        and len(node.args) == 1
        and not node.keywords
    ):
        return _extract_string_collection(node.args[0])
    return None


class RegistryCompletenessTests(unittest.TestCase):
    def test_capability_tables_cover_all_published_schemas(self) -> None:
        derivation_manifest = json.loads((DERIVATION_SCHEMA_DIR / "published.json").read_text("utf-8"))
        tax_manifest = json.loads((TAX_SCHEMA_DIR / "published.json").read_text("utf-8"))

        published: dict[str, set[str]] = {
            "rule-artifact": set(),
            "attachment-rule": set(),
            "artifact-package": set(),
        }
        for filename in [*derivation_manifest.keys(), *tax_manifest.keys()]:
            match = _MANIFEST_ENTRY_RE.match(filename)
            if match:
                schema_id = filename[: -len(".schema.json")]
                published[match.group(1)].add(schema_id)

        self.assertEqual(set(RULE_ARTIFACT_CAPABILITIES), published["rule-artifact"])
        self.assertEqual(set(ATTACHMENT_RULE_CAPABILITIES), published["attachment-rule"])
        self.assertEqual(set(ARTIFACT_PACKAGE_CAPABILITIES), published["artifact-package"])

        for key, rule_row in RULE_ARTIFACT_CAPABILITIES.items():
            self.assertEqual(rule_row.schema, key)
        for key, att_row in ATTACHMENT_RULE_CAPABILITIES.items():
            self.assertEqual(att_row.schema, key)
        for key, pkg_row in ARTIFACT_PACKAGE_CAPABILITIES.items():
            self.assertEqual(pkg_row.schema, key)

    def test_lookup_helpers_and_invariants(self) -> None:
        self.assertIsNone(rule_artifact_caps("attachment-rule.v1"))
        self.assertIsNone(rule_artifact_caps(None))
        self.assertIsNone(attachment_rule_caps("rule-artifact.v1"))
        self.assertIsNone(artifact_package_caps("artifact-package.v27"))

        for schema, row in ATTACHMENT_RULE_CAPABILITIES.items():
            with self.subTest(schema=schema):
                self.assertEqual(row.legacy_single_row_set, not row.uses_row_sets)
                if row.eager_adjustment_requires:
                    self.assertTrue(row.supports_adjustment_rows)
                if row.supports_adjustment_rows:
                    self.assertTrue(row.uses_row_sets)
                if row.supports_exclusive_adjustment_selection:
                    self.assertTrue(row.supports_adjustment_rows)
                if row.projection_reads_row_sets:
                    self.assertTrue(row.uses_row_sets)

        for schema, r_row in RULE_ARTIFACT_CAPABILITIES.items():
            with self.subTest(schema=schema):
                if r_row.subject_optional:
                    self.assertTrue(r_row.supports_subject_declaration)
                if r_row.supports_shared_key_count:
                    self.assertTrue(r_row.supports_v13_selection)

        for schema, p_row in ARTIFACT_PACKAGE_CAPABILITIES.items():
            with self.subTest(schema=schema):
                if p_row.enforces_reader_role:
                    self.assertTrue(p_row.exact_entrypoint_pins)

        self.assertIn("attachment-rule.v10", ATTACHMENT_PROJECTION_SCHEMAS)
        self.assertNotIn("attachment-rule.v10", ATTACHMENT_EXECUTABLE_SCHEMAS)
        self.assertEqual(
            ALL_VALIDATION_GRAPH_SCHEMAS,
            RULE_VALIDATION_GRAPH_SCHEMAS | ATTACHMENT_EXECUTABLE_SCHEMAS,
        )
        self.assertEqual(
            ALL_EXECUTABLE_RULE_AND_ATTACHMENT_SCHEMAS,
            RULE_ARTIFACT_SCHEMAS | ATTACHMENT_EXECUTABLE_SCHEMAS,
        )
        self.assertNotIn("rule-artifact.v12", RULE_VALIDATION_GRAPH_SCHEMAS)
        self.assertNotIn("artifact-package.v18", PACKAGE_UNIVERSE_GUARD_SCHEMAS)
        self.assertIn("attachment-rule.v8", ATTACHMENT_ADJUSTMENT_ROWS_EXECUTABLE_SCHEMAS)
        self.assertNotIn("attachment-rule.v11", ATTACHMENT_EAGER_ADJUSTMENT_REQUIRES_SCHEMAS)
        self.assertIn("attachment-rule.v12", ATTACHMENT_PROJECTION_ROW_SETS_SCHEMAS)
        self.assertNotIn("attachment-rule.v12", ATTACHMENT_ADJUSTMENT_ROWS_PROJECTION_SCHEMAS)
        self.assertIn("attachment-rule.v12", ATTACHMENT_BFS_SCHEMAS)
        self.assertIn("attachment-rule.v1", ATTACHMENT_LEGACY_SINGLE_ROW_SET_SCHEMAS)
        self.assertIn("attachment-rule.v2", ATTACHMENT_ROW_SET_SCHEMAS)
        self.assertIn("attachment-rule.v10", ATTACHMENT_ADJUSTMENT_ROWS_PROJECTION_SCHEMAS)
        self.assertIn("attachment-rule.v11", ATTACHMENT_EXCLUSIVE_SELECTION_SCHEMAS)
        self.assertIn("attachment-rule.v12", ATTACHMENT_CONDITIONAL_LIMITED_PART_SCHEMAS)
        self.assertIn("rule-artifact.v2", RULE_V2_RECORD_SCHEMAS)
        self.assertIn("rule-artifact.v3", RULE_DECLARED_REFS_OUTSIDE_REQUIRES)
        self.assertIn("rule-artifact.v7", RULE_FIELD_REF_SCHEMAS)
        self.assertIn("rule-artifact.v7", RULE_FIELD_REF_TOP_LEVEL_SCHEMAS)
        self.assertIn("rule-artifact.v9", RULE_LINE2B_V9_SCHEMAS)
        self.assertIn("rule-artifact.v10", RULE_LINK_COVERAGE_SCHEMAS)
        self.assertIn("rule-artifact.v11", RULE_SUBJECT_SCHEMAS)
        self.assertIn("rule-artifact.v13", RULE_SUBJECT_OPTIONAL_SCHEMAS)
        self.assertIn("rule-artifact.v12", RULE_LINK_COUNT_SCHEMAS)
        self.assertIn("rule-artifact.v12", RULE_READER_ROLE_SCHEMAS)
        self.assertIn("rule-artifact.v13", RULE_SHARED_KEY_COUNT_SCHEMAS)
        self.assertIn("rule-artifact.v13", RULE_V13_SELECTION_SCHEMAS)
        self.assertIn("rule-artifact.v15", RULE_REQUIRE_PAIRED_SCHEMAS)
        self.assertIn("artifact-package.v41", PACKAGE_EXACT_ENTRYPOINT_SCHEMAS)
        self.assertIn("artifact-package.v41", PACKAGE_READER_ROLE_SCHEMAS)


class NoScatteredAllowlistAstTests(unittest.TestCase):
    def test_no_scattered_schema_version_collections_in_derivation(self) -> None:
        multi_version_offenders: list[str] = []
        equality_offenders: list[str] = []
        prefix_offenders: list[str] = []
        allowed_prefixes = {("packages/derivation/presentation_projection.py", "attachment-rule.")}

        for py_path in sorted(DERIVATION_DIR.rglob("*.py")):
            rel = str(py_path.relative_to(REPO_ROOT))
            if rel == "packages/derivation/schema_capabilities.py":
                continue
            tree = ast.parse(py_path.read_text("utf-8"), filename=rel)
            for node in ast.walk(tree):
                vals = _extract_string_collection(node)
                if vals is not None:
                    matched = [v for v in vals if _VERSIONED_SCHEMA_RE.match(v)]
                    if len(matched) >= 2:
                        multi_version_offenders.append(
                            f"{rel}:{getattr(node, 'lineno', '?')} ({len(matched)} items: {matched[:3]})"
                        )
                if isinstance(node, ast.Compare):
                    for op, comp in zip(node.ops, node.comparators):
                        if isinstance(op, (ast.Eq, ast.NotEq)) and isinstance(comp, ast.Constant):
                            if isinstance(comp.value, str) and _VERSIONED_SCHEMA_RE.match(comp.value):
                                equality_offenders.append(f"{rel}:{node.lineno} ({comp.value})")
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "startswith"
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                    and _PREFIX_RE.match(node.args[0].value)
                ):
                    if (rel, node.args[0].value) not in allowed_prefixes:
                        prefix_offenders.append(f"{rel}:{node.lineno} ({node.args[0].value})")

        self.assertEqual(multi_version_offenders, [])
        self.assertEqual(equality_offenders, [])
        self.assertEqual(prefix_offenders, [])


class DriftFixesRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    @staticmethod
    def _minimal_package(
        package_schema: str,
        rule: dict[str, Any],
        *,
        entrypoints: list[dict[str, str]] | None = None,
    ) -> tuple[dict[str, Any], dict[tuple[str, str], dict[str, Any]]]:
        package: dict[str, Any] = {
            "schema": package_schema,
            "id": "demo.package.drift-fix",
            "version": "v2",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
            "admitted_schemas": [rule["schema"]],
            "members": [{"role": rule.get("role", "computation"), "schema": rule["schema"], "id": rule["id"], "version": rule["version"]}],
            "input_bindings": [],
            "entrypoints": entrypoints if entrypoints is not None else [{"id": rule["id"], "version": rule["version"]}],
            "composition_obligations": [],
        }
        package["package_checksum"] = package_instance_checksum(package)
        return package, {(rule["id"], rule["version"]): rule}

    def test_reader_role_issues_enforced_on_v41_through_v43(self) -> None:
        rule: dict[str, Any] = {
            "schema": "rule-artifact.v13",
            "id": "demo.rule.linenote-bad",
            "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
            "role": "computation",
            "requires": ["demo.input"],
            "pins": [{"role": "input", "id": "demo.input", "version": "v1", "origin": "assertion"}],
            "when": True,
            "value": {"op": "ref", "name": "demo.input"},
            "publishes": "demo.output",
            "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
            "reader_role": "statement-amount",
            "lineNote": "not valid on statement-amount",
        }
        for pkg_schema in ("artifact-package.v41", "artifact-package.v42", "artifact-package.v43"):
            with self.subTest(pkg_schema=pkg_schema):
                pkg, corpus = self._minimal_package(pkg_schema, rule)
                result = validate_package(pkg, corpus, self.schemas)
                self.assertFalse(result.ok)
                self.assertIn("READER_ROLE_TEXT_INVALID", [i.code for i in result.issues])

    def test_exact_entrypoint_pins_enforced_on_omitted_v20_plus_packages(self) -> None:
        rule: dict[str, Any] = {
            "schema": "rule-artifact.v8",
            "id": "demo.rule.entrypoint-check",
            "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": True,
            "value": 1,
            "publishes": "demo.output",
            "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        }
        for pkg_schema in (
            "artifact-package.v28",
            "artifact-package.v32",
            "artifact-package.v33",
            "artifact-package.v34",
            "artifact-package.v41",
            "artifact-package.v42",
            "artifact-package.v43",
        ):
            with self.subTest(pkg_schema=pkg_schema, case="version_mismatch"):
                pkg, corpus = self._minimal_package(
                    pkg_schema,
                    rule,
                    entrypoints=[{"id": rule["id"], "version": "v999"}],
                )
                result = validate_package(pkg, corpus, self.schemas)
                self.assertIn("ENTRYPOINT_VERSION_MISMATCH", [i.code for i in result.issues])
            with self.subTest(pkg_schema=pkg_schema, case="dangling"):
                pkg, corpus = self._minimal_package(
                    pkg_schema,
                    rule,
                    entrypoints=[{"id": "demo.missing.entrypoint", "version": "v1"}],
                )
                result = validate_package(pkg, corpus, self.schemas)
                self.assertIn("ENTRYPOINT_DANGLING", [i.code for i in result.issues])

    def test_check_10c_subtractive_positive_basis_admits_attachment_rule_v8(self) -> None:
        scope = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"}
        fact_pos = {
            "schema": "fact-type.v2",
            "id": "demo.fact.pos",
            "version": "v1",
            "title": "Demo positive",
            "nature": "determinable",
            "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
            "value_schema": {"type": "number"},
            "supersession": {"policy": "free"},
        }
        fact_adj = copy.deepcopy(fact_pos)
        fact_adj["id"] = "demo.fact.adj"
        fact_ans = {
            "schema": "fact-type.v2",
            "id": "demo.fact.ans",
            "version": "v1",
            "title": "Demo answer",
            "nature": "determinable",
            "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
            "value_schema": {"type": "string", "enum": ["yes", "no"]},
            "supersession": {"policy": "free"},
        }
        bundle = {
            "schema": "bundle.v2",
            "id": "demo.bundle",
            "version": "v1",
            "scope": scope,
            "fact_types": [fact_pos, fact_adj, fact_ans],
        }
        fam_pos = {
            "schema": "source-family.v1",
            "id": "demo.family.pos",
            "version": "v1",
            "scope": scope,
            "member_predicate": {"fact_type": "demo.fact.pos"},
            "authorizes_subtotal": "demo.pos.subtotal",
        }
        fam_adj = {
            "schema": "source-family.v1",
            "id": "demo.family.nominee",
            "version": "v1",
            "scope": scope,
            "member_predicate": {"fact_type": "demo.fact.adj"},
            "authorizes_subtotal": "demo.adj.subtotal",
        }
        comp = {
            "schema": "taxable-interest-composition.v1",
            "id": "demo.comp",
            "version": "v1",
            "scope": scope,
            "publishes": "tax.us.2025.interest.positive-total",
            "constituents": [
                {"source_family": {"id": "demo.family.pos", "version": "v1"}, "authorizes_subtotal": "demo.pos.subtotal"}
            ],
        }
        param = {"schema": "parameter-declaration.v1", "id": "demo.param", "version": "v1", "scope": scope, "values": "0"}
        cite = {"schema": "citation.v1", "id": "demo.cite", "version": "v1", "scope": scope, "authority": "IRS", "title": "Demo"}
        rule_pos = {
            "schema": "rule-artifact.v2",
            "id": "demo.rule.pos",
            "version": "v1",
            "scope": scope,
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": True,
            "value": 1,
            "publishes": "demo.pos.subtotal",
            "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        }
        rule_adj = copy.deepcopy(rule_pos)
        rule_adj["id"] = "demo.rule.adj"
        rule_adj["publishes"] = "demo.adj.subtotal"
        rule_taxable = copy.deepcopy(rule_pos)
        rule_taxable["id"] = "demo.rule.taxable"
        rule_taxable["publishes"] = "tax.us.2025.interest.taxable-total"
        att_v8: dict[str, Any] = {
            "schema": "attachment-rule.v8",
            "id": "demo.att.v8",
            "version": "v1",
            "title": "Demo v8",
            "scope": scope,
            "attachment": {"authority": "IRS", "form_id": "1040", "tax_year": 2025, "jurisdiction": "US-federal"},
            "publishes": "demo.att.pub",
            "requirement": {
                "subtotals": ["demo.pos.subtotal"],
                "threshold_parameter": {"id": "demo.param", "version": "v1"},
                "comparison": "strictly_greater_than",
                "citation": {"id": "demo.cite", "version": "v1"},
            },
            "completeness": {
                "required_answers": [
                    {"check": "presence", "fact_type": {"id": "demo.fact.ans", "version": "v1"}, "symbol": "demo.fact.ans"}
                ]
            },
            "itemizations": [
                {
                    "part_id": "part-i",
                    "label": "Part I",
                    "authority": {"kind": "composition", "composition": {"id": "demo.comp", "version": "v1"}},
                    "row_sets": [
                        {
                            "rows": {
                                "op": "collect_members",
                                "member_fact_type": {"id": "demo.fact.pos", "version": "v1"},
                                "source_family": {"id": "demo.family.pos", "version": "v1"},
                            },
                            "subtotal_symbol": "demo.pos.subtotal",
                        }
                    ],
                    "adjustment_rows": [
                        {
                            "kind": "nominee_distribution",
                            "label": "Nominee Distribution",
                            "sign": "negative",
                            "rows": {
                                "op": "collect_members",
                                "member_fact_type": {"id": "demo.fact.adj", "version": "v1"},
                                "source_family": {"id": "demo.family.nominee", "version": "v1"},
                            },
                            "subtotal_symbol": "demo.adj.subtotal",
                        }
                    ],
                    "tie_out": {
                        "line_symbol": "tax.us.2025.interest.taxable-total",
                        "operation": "subtract",
                        "positive_subtotals": ["demo.pos.subtotal"],
                        "adjustment_subtotals": ["demo.adj.subtotal"],
                    },
                }
            ],
        }
        members_and_roles: list[tuple[dict[str, Any], str]] = [
            (bundle, "fact-type-bundle"),
            (fam_pos, "source-family"),
            (fam_adj, "source-family"),
            (comp, "composition"),
            (param, "parameter"),
            (cite, "citation"),
            (rule_pos, "computation"),
            (rule_adj, "computation"),
            (rule_taxable, "computation"),
            (att_v8, "attachment-rule"),
        ]
        package: dict[str, Any] = {
            "schema": "artifact-package.v24",
            "id": "demo.package.v8-subtractive",
            "version": "v1",
            "scope": scope,
            "admitted_schemas": sorted({c["schema"] for c, _ in members_and_roles}),
            "members": [
                {"role": role, "schema": c["schema"], "id": c["id"], "version": c["version"]}
                for c, role in members_and_roles
            ],
            "input_bindings": [],
            "entrypoints": [{"id": "demo.att.v8", "version": "v1"}],
            "composition_obligations": [],
        }
        package["package_checksum"] = package_instance_checksum(package)
        corpus = {(c["id"], c["version"]): c for c, _ in members_and_roles}
        result = validate_package(package, corpus, self.schemas)
        self.assertNotIn("ATTACHMENT_LINE_AUTHORITY_MISMATCH", [i.code for i in result.issues])
