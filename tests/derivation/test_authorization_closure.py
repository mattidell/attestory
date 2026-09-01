"""Rule-scoped re-authorization boundary (ADR-0069 Decision 5 / SA-P2)."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.authorization_closure import (
    package_boundary_digest,
    rule_scoped_closure,
)

CONTENT = Path(__file__).resolve().parents[2] / "packages" / "content" / "tax" / "2025"


def _corpus() -> dict[str, dict[str, Any]]:
    """Synthetic corpus in production schema shapes. No interest-vertical content."""
    return {
        "demo.rule.ordinary-subtotal": {
            "id": "demo.rule.ordinary-subtotal",
            "version": "v1",
            "schema": "rule-artifact.v3",
            "requires": ["demo.scale.convention"],
            "publishes": "demo.ordinary.subtotal",
            "composition": {"id": "demo.composition.slots", "version": "v1"},
            "citations": [{"id": "demo.citation.base", "version": "v1"}],
            "when": True,
            "value": {
                "op": "round",
                "mode": {"op": "ref", "name": "demo.scale.convention"},
                "value": {
                    "op": "add",
                    "args": [
                        {
                            "op": "collect",
                            "source_set": "demo.family.ordinary",
                            "name": "demo.fact.ordinary",
                        }
                    ],
                },
            },
        },
        "demo.scale.convention": {
            "id": "demo.scale.convention",
            "version": "v1",
            "schema": "rule-artifact.v3",
            "publishes": "demo.scale.convention",
            "requires": [],
            "when": True,
            "value": {"op": "literal", "value": "half-up"},
        },
        "demo.family.ordinary": {
            "id": "demo.family.ordinary",
            "version": "v1",
            "schema": "source-family.v1",
            "member_predicate": {"fact_type": "demo.fact.ordinary"},
        },
        "demo.bundle.ordinary": {
            "id": "demo.bundle.ordinary",
            "version": "v1",
            "schema": "bundle.v2",
            "fact_types": [
                {
                    "id": "demo.fact.ordinary",
                    "version": "v1",
                    "quantity": {"id": "demo.quantity.ordinary", "version": "v1"},
                    "optional_default": {
                        "parameter": {"id": "demo.parameter.threshold", "version": "v1"}
                    },
                }
            ],
        },
        "demo.quantity.ordinary": {
            "id": "demo.quantity.ordinary",
            "version": "v1",
            "schema": "quantity-vocabulary.v7",
            "quantities": ["ordinary"],
        },
        "demo.parameter.threshold": {
            "id": "demo.parameter.threshold",
            "version": "v1",
            "schema": "parameter-declaration.v1",
            "values": "0",
        },
        "demo.mapping.ordinary": {
            "id": "demo.mapping.ordinary",
            "version": "v1",
            "schema": "source-closure-mapping.v2",
            "member_fact_type": {"id": "demo.fact.ordinary", "version": "v1"},
            "closure_fact_type": {"id": "demo.fact.ordinary-closure", "version": "v1"},
        },
        "demo.composition.slots": {
            "id": "demo.composition.slots",
            "version": "v1",
            "schema": "taxable-interest-composition.v1",
            "constituents": [
                {
                    "source_family": {"id": "demo.family.ordinary", "version": "v1"},
                    "authorizes_subtotal": "demo.ordinary.subtotal",
                }
            ],
        },
        "demo.citation.base": {
            "id": "demo.citation.base",
            "version": "v1",
            "schema": "citation.v1",
        },
        "demo.field.line": {
            "id": "demo.field.line",
            "version": "v1",
            "schema": "form-field.v2",
            "binds_symbol": "demo.ordinary.subtotal",
            "citation": {"id": "demo.citation.base", "version": "v1"},
        },
        "demo.attachment.schedule": {
            "id": "demo.attachment.schedule",
            "version": "v1",
            "schema": "attachment-rule.v6",
            "itemizations": [
                {
                    "authority": {
                        "kind": "composition",
                        "composition": {"id": "demo.composition.slots", "version": "v1"},
                    },
                    "row_sets": [
                        {
                            "rows": {
                                "source_family": {"id": "demo.family.ordinary", "version": "v1"},
                                "member_fact_type": {"id": "demo.fact.ordinary", "version": "v1"},
                            }
                        }
                    ],
                    "adjustment_rows": [],
                }
            ],
            "completeness": {
                "required_answers": [
                    {"fact_type": {"id": "demo.parameter.threshold", "version": "v1"}}
                ]
            },
            "requirement": {
                "subtotals": ["demo.ordinary.subtotal"],
                "citation": {"id": "demo.citation.base", "version": "v1"},
                "threshold_parameter": {"id": "demo.parameter.threshold", "version": "v1"},
            },
        },
        "demo.role.canon": {
            "id": "demo.role.canon",
            "version": "v1",
            "schema": "role-canon.v1",
        },
        "demo.family.v2": {
            "id": "demo.family.v2",
            "version": "v1",
            "schema": "source-family.v2",
            "member_predicate": {"fact_type": "demo.fact.v2"},
        },
        "demo.bundle.v2": {
            "id": "demo.bundle.v2",
            "version": "v1",
            "schema": "bundle.v2",
            "fact_types": [{"id": "demo.fact.v2", "version": "v1"}],
        },
        "demo.rule.v2-collect": {
            "id": "demo.rule.v2-collect",
            "version": "v1",
            "schema": "rule-artifact.v3",
            "requires": [],
            "publishes": "demo.v2.subtotal",
            "when": True,
            "value": {
                "op": "collect",
                "source_set": "demo.family.v2",
                "name": "demo.fact.v2",
            },
        },
    }


ROOT = {"demo.rule.ordinary-subtotal"}


class RuleScopedClosure(unittest.TestCase):
    def test_closure_includes_bfs_kinds_and_excludes_unrelated(self) -> None:
        corpus = _corpus()
        closure_ids = {cid for cid, _ver in rule_scoped_closure(ROOT, corpus)}
        self.assertEqual(
            closure_ids,
            {
                "demo.rule.ordinary-subtotal",
                "demo.scale.convention",
                "demo.family.ordinary",
                "demo.bundle.ordinary",
                "demo.quantity.ordinary",
                "demo.parameter.threshold",
                "demo.mapping.ordinary",
                "demo.composition.slots",
                "demo.citation.base",
                "demo.role.canon",
            },
        )
        self.assertNotIn("demo.field.line", closure_ids)
        self.assertNotIn("demo.attachment.schedule", closure_ids)
        self.assertNotIn("demo.rule.v2-collect", closure_ids)

    def test_form_field_root_reaches_producing_rule(self) -> None:
        corpus = _corpus()
        closure_ids = {cid for cid, _ver in rule_scoped_closure({"demo.field.line"}, corpus)}
        self.assertIn("demo.rule.ordinary-subtotal", closure_ids)
        self.assertIn("demo.citation.base", closure_ids)

    def test_attachment_rule_root_reaches_composition_and_family(self) -> None:
        corpus = _corpus()
        closure_ids = {
            cid for cid, _ver in rule_scoped_closure({"demo.attachment.schedule"}, corpus)
        }
        self.assertIn("demo.composition.slots", closure_ids)
        self.assertIn("demo.family.ordinary", closure_ids)
        self.assertIn("demo.rule.ordinary-subtotal", closure_ids)

    def test_source_family_v2_collect_is_an_edge(self) -> None:
        corpus = _corpus()
        closure_ids = {
            cid for cid, _ver in rule_scoped_closure({"demo.rule.v2-collect"}, corpus)
        }
        self.assertIn("demo.family.v2", closure_ids)
        self.assertIn("demo.bundle.v2", closure_ids)

    def test_counterexample_a_unrelated_addition_does_not_force_reauth(self) -> None:
        corpus_before = _corpus()
        digest_before = package_boundary_digest(ROOT, corpus_before)
        corpus_after = copy.deepcopy(corpus_before)
        corpus_after["demo.rule.unrelated-subtotal"] = {
            "id": "demo.rule.unrelated-subtotal",
            "version": "v1",
            "schema": "rule-artifact.v3",
            "requires": [],
            "publishes": "demo.unrelated.subtotal",
            "when": True,
            "value": {
                "op": "collect",
                "source_set": "demo.family.unrelated",
                "name": "demo.fact.unrelated",
            },
        }
        corpus_after["demo.family.unrelated"] = {
            "id": "demo.family.unrelated",
            "version": "v1",
            "schema": "source-family.v1",
            "member_predicate": {"fact_type": "demo.fact.unrelated"},
        }
        corpus_after["demo.bundle.unrelated"] = {
            "id": "demo.bundle.unrelated",
            "version": "v1",
            "schema": "bundle.v2",
            "fact_types": [{"id": "demo.fact.unrelated", "version": "v1"}],
        }
        digest_after = package_boundary_digest(ROOT, corpus_after)
        self.assertEqual(digest_after, digest_before)

    def test_counterexample_b_depended_on_rule_edit_forces_reauth(self) -> None:
        corpus_before = _corpus()
        digest_before = package_boundary_digest(ROOT, corpus_before)
        corpus_after = copy.deepcopy(corpus_before)
        corpus_after["demo.scale.convention"]["version"] = "v2"
        corpus_after["demo.scale.convention"]["value"] = {"op": "literal", "value": "half-even"}
        digest_after = package_boundary_digest(ROOT, corpus_after)
        self.assertNotEqual(digest_after, digest_before)

    def test_content_edit_without_version_bump_also_forces_reauth(self) -> None:
        corpus_before = _corpus()
        digest_before = package_boundary_digest(ROOT, corpus_before)
        corpus_after = copy.deepcopy(corpus_before)
        corpus_after["demo.scale.convention"]["value"] = {"op": "literal", "value": "down"}
        self.assertNotEqual(package_boundary_digest(ROOT, corpus_after), digest_before)


def _load_2025_citizens() -> dict[str, dict[str, Any]]:
    corpus: dict[str, dict[str, Any]] = {}
    for path in sorted(CONTENT.glob("*.json")):
        try:
            data = json.loads(path.read_text("utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        schema = data.get("schema")
        citizen_id = data.get("id")
        if not isinstance(schema, str) or not isinstance(citizen_id, str):
            continue
        if schema.startswith("artifact-package.") or schema.startswith("release-registry."):
            continue
        corpus[citizen_id] = data
    return corpus


class ProductionContentStructures(unittest.TestCase):
    def test_wages_line1a_closure_on_real_2025_citizens(self) -> None:
        corpus = _load_2025_citizens()
        root = "tax.us.2025.rule.w2-box1-to-line1a"
        self.assertIn(root, corpus)
        closure_ids = {cid for cid, _ver in rule_scoped_closure({root}, corpus)}
        self.assertIn(root, closure_ids)
        self.assertIn("tax.us.2025.w2", closure_ids)
        self.assertIn("tax.us.2025.w2-vocabulary", closure_ids)
        self.assertIn("tax.us.2025.quantity.wages", closure_ids)
        self.assertIn("tax.us.2025.closure-mapping.w2", closure_ids)
        self.assertNotIn("tax.us.2025.f1099div.1a", closure_ids)
        digest = package_boundary_digest({root}, corpus)
        self.assertEqual(len(digest), 64)
        self.assertTrue(all(ch in "0123456789abcdef" for ch in digest))


if __name__ == "__main__":
    unittest.main()
