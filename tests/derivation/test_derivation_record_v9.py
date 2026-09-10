"""ADR-0074 Decision 3h: derivation-record.v9 schema-test table.

v8 bytes stay untouched. Nothing emits NOMINEE_ALLOCATIONS_EXCEED_REPORT
against v8. The third inapplicable form is legal only for the nominee
rule, with no_groups_selected: true and the unsuffixed publishes prefix.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DERIVATION_SCHEMA_DIR
from packages.kernel.schema_registry import SchemaRegistry, SchemaValidationError
from packages.tax.report_statement_identity import derive_1099int_box1_fact_id

EXAMPLES = (
    Path(__file__).resolve().parents[2]
    / "packages"
    / "sample_data"
    / "derivation"
    / "examples"
)

V8_CHECKSUM = "0e9acba1857b27ab4ae7a8827d1f36388b2e2e677b80299e886de6c1ca8dd3ca"
NOMINEE_RULE = "tax.us.2025.rule.interest.nominee-reduction"
NOMINEE_PREFIX = "tax.us.2025.interest.nominee-reduction"
GOVERNANCE = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]
ADOPTION = {"role": "adoption", "id": "demo.package.record-v9", "version": "v1"}


def _example(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


def _closing(row: dict[str, Any], *, schema: str = "derivation-record.v9") -> dict[str, Any]:
    return {
        "schema": schema,
        "record_id": "demo.record.closing",
        "run_id": "demo.run",
        "phase": "completed",
        "workspace_revision": 1,
        "governance_pins": GOVERNANCE,
        "adoption_pin": ADOPTION,
        "stop_reason": "saturated",
        "dispositions": [row],
    }


def _p1_row() -> dict[str, Any]:
    return {
        "artifact_id": NOMINEE_RULE,
        "disposition": "inapplicable",
        "no_groups_selected": True,
        "symbol": NOMINEE_PREFIX,
        "pins": [],
    }


class DerivationRecordV9Schema(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = SchemaRegistry([DERIVATION_SCHEMA_DIR])

    def assert_valid(self, instance: dict[str, Any]) -> None:
        self.registry.validate(instance["schema"], instance)

    def assert_rejected(self, instance: dict[str, Any]) -> None:
        with self.assertRaises(SchemaValidationError):
            self.registry.validate(instance["schema"], instance)

    def test_v8_manifest_entry_unchanged_and_v9_published(self) -> None:
        manifest = json.loads((DERIVATION_SCHEMA_DIR / "published.json").read_text("utf-8"))
        self.assertIn("derivation-record.v9.schema.json", manifest)
        self.assertEqual(manifest["derivation-record.v8.schema.json"], V8_CHECKSUM)

    def test_committed_over_allocation_instance_validates(self) -> None:
        instance = _example("derivation-record.v9.nominee-over-allocation.json")
        self.registry.validate_declared(instance)

    def test_committed_c0_instance_validates(self) -> None:
        instance = _example("derivation-record.v9.nominee-c0.json")
        self.registry.validate_declared(instance)

    def test_over_allocation_symbol_uses_derived_report_fact_id(self) -> None:
        instance = _example("derivation-record.v9.nominee-over-allocation.json")
        report_fact_id = derive_1099int_box1_fact_id(
            payer_name="demo.payer.a",
            statement_reference="demo.stmt.a",
            tax_year=2025,
        )
        expected = f"{NOMINEE_PREFIX}|{report_fact_id}"
        self.assertEqual(instance["dispositions"][0]["symbol"], expected)

    def test_p1_no_groups_selected_row_validates(self) -> None:
        self.assert_valid(_closing(_p1_row()))

    def test_n1_other_artifact_id_rejected(self) -> None:
        row = _p1_row()
        row["artifact_id"] = "tax.us.2025.rule.interest.other"
        self.assert_rejected(_closing(row))

    def test_n2_published_or_blocked_disposition_rejected(self) -> None:
        for disposition in ("published", "blocked"):
            with self.subTest(disposition=disposition):
                row = _p1_row()
                row["disposition"] = disposition
                self.assert_rejected(_closing(row))

    def test_n3_no_groups_selected_false_rejected(self) -> None:
        row = _p1_row()
        row["no_groups_selected"] = False
        self.assert_rejected(_closing(row))

    def test_n3b_inapplicable_with_no_evidence_form_rejected(self) -> None:
        row = {
            "artifact_id": NOMINEE_RULE,
            "disposition": "inapplicable",
            "pins": [],
        }
        self.assert_rejected(_closing(row))

    def test_n4_symbol_missing_rejected(self) -> None:
        row = _p1_row()
        del row["symbol"]
        self.assert_rejected(_closing(row))

    def test_n5_suffixed_or_wrong_symbol_rejected(self) -> None:
        for symbol in (
            f"{NOMINEE_PREFIX}|demo.report",
            "tax.us.2025.interest.other",
        ):
            with self.subTest(symbol=symbol):
                row = _p1_row()
                row["symbol"] = symbol
                self.assert_rejected(_closing(row))

    def test_n6_third_form_plus_forbidden_fields_rejected(self) -> None:
        extras: dict[str, Any] = {
            "guard_result": False,
            "superseded_by": {"role": "citation", "id": "demo.citation.other", "version": "v1"},
            "code": "DEPENDENCY_ABSENT",
            "finding_id": "demo.finding.x",
            "act_id": "demo.act.x",
        }
        for key, value in extras.items():
            with self.subTest(field=key):
                row = _p1_row()
                row[key] = value
                self.assert_rejected(_closing(row))

    def test_p2_existing_blocked_row_without_symbol_still_valid(self) -> None:
        row = {
            "artifact_id": "demo.rule.block",
            "disposition": "blocked",
            "code": "DEPENDENCY_ABSENT",
            "missing": ["demo.named"],
            "pins": [],
        }
        self.assert_valid(_closing(row))

    def test_p3_existing_guard_result_inapplicable_without_symbol_still_valid(self) -> None:
        row = {
            "artifact_id": "demo.rule.other",
            "disposition": "inapplicable",
            "guard_result": False,
            "pins": [],
        }
        self.assert_valid(_closing(row))

    def test_p4_existing_superseded_by_inapplicable_without_symbol_still_valid(self) -> None:
        row = {
            "artifact_id": "demo.rule.other",
            "disposition": "inapplicable",
            "superseded_by": {
                "role": "citation",
                "id": "demo.citation.successor",
                "version": "v1",
            },
            "pins": [],
        }
        self.assert_valid(_closing(row))

    def test_p5_published_row_with_symbol_still_valid_and_symbol_required(self) -> None:
        row = {
            "artifact_id": "demo.rule.publish",
            "disposition": "published",
            "finding_id": "demo.finding.out",
            "act_id": "demo.act.pub",
            "symbol": "demo.output",
            "pins": [],
        }
        self.assert_valid(_closing(row))
        missing_symbol = copy.deepcopy(row)
        del missing_symbol["symbol"]
        self.assert_rejected(_closing(missing_symbol))

    def test_v8_still_rejects_new_code_and_no_groups_form(self) -> None:
        over = _example("derivation-record.v9.nominee-over-allocation.json")
        over["schema"] = "derivation-record.v8"
        self.assert_rejected(over)
        c0 = _example("derivation-record.v9.nominee-c0.json")
        c0["schema"] = "derivation-record.v8"
        self.assert_rejected(c0)


if __name__ == "__main__":
    unittest.main()
