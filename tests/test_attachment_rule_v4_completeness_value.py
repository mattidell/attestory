"""Focused schema/content/package tests for ADR-0055's attachment-rule.v4.

Hand-written positive and negative instances for the new `check: "value"`
required-answer shape, plus package_validation's equals-in-domain guard.
Behavioral coverage (attempt_attachment's value-check branch, actually
converging with the numeric route) lives in the coordinator goldens
(tests/test_schedule_d_covered_ltcg_8a_t2_coordinator.py); this module
covers the static shape only.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import validate_package

CONTENT = Path("packages/content/tax/2025")


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


class AttachmentRuleV4Shape(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.committed = _load("attachment.schedule-d.v2.json")

    def test_committed_schedule_d_v2_validates(self) -> None:
        self.schemas.validate_declared(self.committed)

    def test_presence_check_shape_unchanged(self) -> None:
        instance = copy.deepcopy(self.committed)
        instance["completeness"]["required_answers"] = [{
            "check": "presence",
            "fact_type": {"id": "tax.us.2025.schedule-d-boundary.no-short-term-transactions", "version": "v1"},
            "symbol": "tax.us.2025.schedule-d-boundary.no-short-term-transactions",
        }]
        self.schemas.validate_declared(instance)

    def test_value_check_requires_equals(self) -> None:
        instance = copy.deepcopy(self.committed)
        instance["completeness"]["required_answers"] = [{
            "check": "value",
            "fact_type": {"id": "tax.us.2025.schedule-d-boundary.no-short-term-transactions", "version": "v1"},
            "symbol": "tax.us.2025.schedule-d-boundary.no-short-term-transactions",
        }]
        with self.assertRaises(Exception):
            self.schemas.validate_declared(instance)

    def test_presence_check_rejects_equals(self) -> None:
        instance = copy.deepcopy(self.committed)
        instance["completeness"]["required_answers"] = [{
            "check": "presence",
            "equals": "yes",
            "fact_type": {"id": "tax.us.2025.schedule-d-boundary.no-short-term-transactions", "version": "v1"},
            "symbol": "tax.us.2025.schedule-d-boundary.no-short-term-transactions",
        }]
        with self.assertRaises(Exception):
            self.schemas.validate_declared(instance)

    def test_unknown_check_kind_rejects(self) -> None:
        instance = copy.deepcopy(self.committed)
        instance["completeness"]["required_answers"] = [{
            "check": "boolean",
            "fact_type": {"id": "tax.us.2025.schedule-d-boundary.no-short-term-transactions", "version": "v1"},
            "symbol": "tax.us.2025.schedule-d-boundary.no-short-term-transactions",
        }]
        with self.assertRaises(Exception):
            self.schemas.validate_declared(instance)

    def test_v3_attachment_still_validates_immutable(self) -> None:
        v1 = _load("attachment.schedule-d.json")
        self.schemas.validate_declared(v1)
        self.assertEqual(v1["schema"], "attachment-rule.v3")


class PackageValidationEqualsInDomain(unittest.TestCase):
    """A `check: "value"` answer's `equals` must be a value the fact type's
    own declared domain admits (ADR-0055 Decision 1's own-domain guard)."""

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.package = _load("package.core-calculations.v12.json")
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        import glob
        for f in glob.glob(str(CONTENT / "*.json")):
            try:
                d = json.loads(Path(f).read_text("utf-8"))
            except Exception:
                continue
            if isinstance(d, dict) and {"id", "version", "schema"} <= d.keys():
                corpus[(d["id"], d["version"])] = d
        self.corpus = corpus

    def test_committed_package_validates_clean(self) -> None:
        result = validate_package(self.package, self.corpus, self.schemas)
        self.assertTrue(result.ok, msg=str(result.issues))

    def test_equals_not_in_domain_rejected(self) -> None:
        corpus = dict(self.corpus)
        attachment = copy.deepcopy(corpus[("tax.us.2025.rule.attachment.schedule-d", "v2")])
        attachment["completeness"]["required_answers"][0]["equals"] = "maybe"
        corpus[("tax.us.2025.rule.attachment.schedule-d", "v2")] = attachment
        result = validate_package(self.package, corpus, self.schemas)
        codes = {issue.code for issue in result.issues}
        self.assertIn("ATTACHMENT_ANSWER_EQUALS_NOT_IN_DOMAIN", codes)


if __name__ == "__main__":
    unittest.main()
