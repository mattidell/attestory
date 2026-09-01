"""derivation-record.v8: named pairing/supportability codes survive the ledger.

The identity-association, per-pairing and aggregate accrued-interest
supportability, and legacy/pairing migration seams each name a disposition
block code (ASSOCIATION_AMBIGUOUS, ACCRUED_EXCEEDS_ASSOCIATED_REPORT,
SUPPORTABILITY_NOT_ESTABLISHED, AGGREGATE_ACCRUED_EXCEEDS_REPORT,
ASSOCIATION_UNCONFIRMED, ASSOCIATION_MIGRATION_ADOPTION_REQUIRED) that must
reach the schema-validated disposition ledger instead of collapsing to
DEPENDENCY_INVALID at `_record_blocked`.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DERIVATION_SCHEMA_DIR, DerivationSchemas
from packages.derivation.records import CURRENT_RECORD_SCHEMA, RecordStream
from packages.derivation.runner import InputFinding, RunContext, run_and_record
from packages.kernel.schema_registry import SchemaRegistry, SchemaValidationError

NEW_RECORD_CODES = (
    "ASSOCIATION_AMBIGUOUS",
    "ACCRUED_EXCEEDS_ASSOCIATED_REPORT",
    "SUPPORTABILITY_NOT_ESTABLISHED",
    "AGGREGATE_ACCRUED_EXCEEDS_REPORT",
    "ASSOCIATION_UNCONFIRMED",
    "ASSOCIATION_MIGRATION_ADOPTION_REQUIRED",
)

ADOPTION = {"role": "adoption", "id": "demo.package.record-codes-v8", "version": "v1"}
GOVERNANCE = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]


def _blocking_rule(rule_id: str, symbol: str, code: str) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v6",
        "id": rule_id,
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
        "role": "computation",
        "requires": ["demo.input"],
        "pins": [{"role": "input", "id": "demo.input", "version": "v1", "origin": "assertion"}],
        "when": True,
        "value": {"op": "block", "code": code},
        "publishes": symbol,
        "blocked": {"code": code, "missing": []},
    }


def _closing_row(code: str) -> dict[str, Any]:
    return {
        "schema": "derivation-record.v8",
        "record_id": "demo.record.closing",
        "run_id": "demo.run",
        "phase": "completed",
        "workspace_revision": 1,
        "governance_pins": GOVERNANCE,
        "adoption_pin": ADOPTION,
        "stop_reason": "saturated",
        "dispositions": [
            {
                "artifact_id": "demo.rule.block",
                "disposition": "blocked",
                "pins": [],
                "code": code,
                "missing": ["demo.named"],
            }
        ],
    }


class DerivationRecordV8Schema(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = SchemaRegistry([DERIVATION_SCHEMA_DIR])

    def test_v8_is_current_and_v7_bytes_are_untouched(self) -> None:
        self.assertEqual(CURRENT_RECORD_SCHEMA, "derivation-record.v8")
        manifest = json.loads((DERIVATION_SCHEMA_DIR / "published.json").read_text("utf-8"))
        self.assertIn("derivation-record.v8.schema.json", manifest)
        self.assertEqual(
            manifest["derivation-record.v7.schema.json"],
            "7e00f5f7da9068fe246d4a9c07f0ecd496bac16d0858bf51de9b0e2231101572",
        )

    def test_v8_accepts_every_new_code(self) -> None:
        for code in NEW_RECORD_CODES:
            with self.subTest(code=code):
                self.registry.validate("derivation-record.v8", _closing_row(code))

    def test_v7_still_rejects_every_new_code(self) -> None:
        for code in NEW_RECORD_CODES:
            with self.subTest(code=code):
                row = _closing_row(code)
                row["schema"] = "derivation-record.v7"
                with self.assertRaises(SchemaValidationError):
                    self.registry.validate("derivation-record.v7", row)


class NamedCodesSurviveDispositionLedger(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def _run_blocking(self, code: str) -> dict[str, Any]:
        ctx = RunContext(
            run_id=f"demo.record-codes.{code}",
            rules=[_blocking_rule(f"demo.rule.{code}", f"demo.output.{code}", code)],
            parameters={},
            canon={},
            inputs=[InputFinding("demo.input", 1, "finding.input", "input")],
            sources=[],
            adoption_pin=ADOPTION,
            governance_pins=GOVERNANCE,
        )
        with tempfile.TemporaryDirectory() as tmp:
            stream = RecordStream(Path(tmp) / "workspace", self.schemas)
            result = run_and_record(
                ctx,
                self.schemas,
                stream,
                workspace_revision=1,
                adopted_packages={ADOPTION["id"]},
                start_record_id=f"demo.start.{code}",
                completion_record_id=f"demo.done.{code}",
            )
            closing = stream.standings()[ctx.run_id].closing
            assert closing is not None
            return {"result": result, "closing": closing}

    def test_each_new_code_survives_to_the_ledger(self) -> None:
        for code in NEW_RECORD_CODES:
            with self.subTest(code=code):
                observed = self._run_blocking(code)
                result = observed["result"]
                closing = observed["closing"]
                self.assertEqual(closing["schema"], CURRENT_RECORD_SCHEMA)
                blocked = {row["artifact_id"]: row for row in result.blocked}
                ledger = {row["artifact_id"]: row for row in closing["dispositions"]}
                artifact_id = f"demo.rule.{code}"
                self.assertEqual(blocked[artifact_id]["code"], code)
                self.assertEqual(ledger[artifact_id]["disposition"], "blocked")
                self.assertEqual(ledger[artifact_id]["code"], code)
                self.assertNotEqual(ledger[artifact_id]["code"], "DEPENDENCY_INVALID")

    def test_unknown_code_still_collapses_to_dependency_invalid(self) -> None:
        observed = self._run_blocking("NOT_A_RECORD_CODE")
        result = observed["result"]
        closing = observed["closing"]
        artifact_id = "demo.rule.NOT_A_RECORD_CODE"
        self.assertEqual(result.blocked[0]["code"], "NOT_A_RECORD_CODE")
        ledger = {row["artifact_id"]: row for row in closing["dispositions"]}
        self.assertEqual(ledger[artifact_id]["code"], "DEPENDENCY_INVALID")


if __name__ == "__main__":
    unittest.main()
