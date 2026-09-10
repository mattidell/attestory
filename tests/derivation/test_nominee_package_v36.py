"""ADR-0074: package.core-calculations v36 pins the nominee-reduction graph.

v35 bytes stay untouched. No source-family or source-closure-mapping is
added for tax.us.nominee-allocation.amount.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.package_validation import package_instance_checksum

CONTENT = Path(__file__).resolve().parents[2] / "packages" / "content" / "tax" / "2025"
ALLOCATION_TYPE = "tax.us.nominee-allocation.amount"
RULE_ID = "tax.us.2025.rule.interest.nominee-reduction"
REDUCTION_PREFIX = "tax.us.2025.interest.nominee-reduction"
REDUCTION_VOCAB = "tax.us.2025.interest.nominee-reduction.vocabulary"
ALLOCATION_VOCAB = "tax.us.nominee-allocation.vocabulary"
LEGACY_NOMINEE_AMOUNT = "tax.us.2025.scheduleb.adjustment.nominee.amount"
LINE2B_RULE_ID = "tax.us.2025.rule.form1040-line2b"
NOMINEE_SUBTOTAL_RULE_ID = "tax.us.2025.rule.scheduleb-adjustment.nominee-subtotal"
V35_CHECKSUM = "abda24c3aad1981fb4f9deb17e94484513251bfae8c5fa4be0e7cf7783283510"


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((CONTENT / name).read_text("utf-8"))
    return loaded


def _content_corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            value = json.loads(path.read_text("utf-8"))
        except Exception:
            continue
        if (
            isinstance(value, dict)
            and isinstance(value.get("id"), str)
            and isinstance(value.get("version"), str)
            and not ("citizens" in value and "packages" in value)
        ):
            corpus[(value["id"], value["version"])] = value
    return corpus


class NomineePackageV36(unittest.TestCase):
    def test_v35_bytes_and_catalog_checksum_untouched(self) -> None:
        v35 = _load("package.core-calculations.v35.json")
        self.assertEqual(v35["package_checksum"], V35_CHECKSUM)
        catalog = _load("published-packages.v31.json")
        v35_entry = next(
            e
            for e in catalog["packages"]
            if e["id"] == "tax.us.2025.package.core-calculations" and e["version"] == "v35"
        )
        self.assertEqual(v35_entry["checksum"], V35_CHECKSUM)

    def test_v36_is_artifact_package_v28_with_v8_admission(self) -> None:
        pkg = _load("package.core-calculations.v36.json")
        self.assertEqual(pkg["schema"], "artifact-package.v28")
        self.assertEqual(pkg["version"], "v36")
        self.assertEqual(pkg["package_checksum"], package_instance_checksum(pkg))
        self.assertIn("rule-artifact.v8", pkg["admitted_schemas"])

    def test_two_entrypoint_pins_and_required_members(self) -> None:
        pkg = _load("package.core-calculations.v36.json")
        member_ids = {m["id"] for m in pkg["members"]}
        entry_ids = {e["id"] for e in pkg["entrypoints"]}
        self.assertIn(RULE_ID, member_ids)
        self.assertIn(REDUCTION_VOCAB, member_ids)
        self.assertIn(ALLOCATION_VOCAB, member_ids)
        self.assertIn("tax.us.2025.citation.interest.nominee-reduction", member_ids)
        self.assertIn(RULE_ID, entry_ids)
        self.assertIn(REDUCTION_VOCAB, entry_ids)
        self.assertNotIn(ALLOCATION_VOCAB, entry_ids)

    def test_no_source_family_or_closure_mapping_for_allocation_type(self) -> None:
        pkg = _load("package.core-calculations.v36.json")
        corpus = _content_corpus()
        for member in pkg["members"]:
            citizen = corpus[(member["id"], member["version"])]
            schema = citizen.get("schema")
            if schema in {"source-family.v1", "source-family.v2"}:
                self.assertNotEqual(
                    citizen.get("member_predicate", {}).get("fact_type"),
                    ALLOCATION_TYPE,
                )
            if schema in {"source-closure-mapping.v1", "source-closure-mapping.v2"}:
                self.assertNotEqual(
                    citizen.get("member_fact_type", {}).get("id"),
                    ALLOCATION_TYPE,
                )

    def test_v36_does_not_claim_line2b_or_schedule_b_completeness(self) -> None:
        pkg = _load("package.core-calculations.v36.json")
        corpus = _content_corpus()
        for member in pkg["members"]:
            citizen = corpus[(member["id"], member["version"])]
            schema = str(citizen.get("schema") or "")
            blob = json.dumps(citizen)
            if schema.startswith("form-field"):
                self.assertNotEqual(citizen.get("binds_symbol"), REDUCTION_PREFIX)
                self.assertNotIn(REDUCTION_PREFIX, blob)
            if schema.startswith("attachment-rule"):
                self.assertNotIn(REDUCTION_PREFIX, blob)
            if citizen.get("id") == LINE2B_RULE_ID:
                self.assertNotIn(REDUCTION_PREFIX, citizen.get("requires", []))
                self.assertNotIn(REDUCTION_PREFIX, blob)

    def test_v36_nominee_rule_neither_consumes_nor_reinterprets_legacy_amount(self) -> None:
        rule = _load("rule.interest.nominee-reduction.json")
        blob = json.dumps(rule)
        self.assertNotIn(LEGACY_NOMINEE_AMOUNT, blob)
        self.assertNotIn(LEGACY_NOMINEE_AMOUNT, rule.get("requires", []))
        self.assertNotIn("accrued_interest_paid_to_seller", blob)
        bound_names = []

        def walk(node: Any) -> None:
            if isinstance(node, dict):
                if node.get("op") == "bound_sources":
                    bound_names.append(node.get("name"))
                if node.get("op") == "ref":
                    self.assertNotEqual(node.get("name"), LEGACY_NOMINEE_AMOUNT)
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(rule)
        self.assertEqual(set(bound_names), {ALLOCATION_TYPE})

    def test_v36_keeps_line2b_v6_and_legacy_nominee_subtotal_v1(self) -> None:
        v35 = _load("package.core-calculations.v35.json")
        v36 = _load("package.core-calculations.v36.json")

        def pin(pkg: dict[str, Any], citizen_id: str) -> dict[str, Any]:
            matches = [m for m in pkg["members"] if m["id"] == citizen_id]
            self.assertEqual(len(matches), 1, citizen_id)
            return cast(dict[str, Any], matches[0])

        self.assertEqual(pin(v35, LINE2B_RULE_ID)["version"], "v6")
        self.assertEqual(pin(v36, LINE2B_RULE_ID)["version"], "v6")
        self.assertEqual(pin(v35, NOMINEE_SUBTOTAL_RULE_ID)["version"], "v1")
        self.assertEqual(pin(v36, NOMINEE_SUBTOTAL_RULE_ID)["version"], "v1")


if __name__ == "__main__":
    unittest.main()
