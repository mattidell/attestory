"""Track 5 verification for the v2 disposition ledger and scheduling parity."""

import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.records import RecordStream
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import InputFinding, RunContext, RunResult, run, run_and_record


ADOPTION = {"role": "adoption", "id": "demo.package.track5", "version": "v1"}
GOVERNANCE = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]


def _rule(rule_id: str, symbol: str, requires: list[str]) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v2",
        "id": rule_id,
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
        "role": "computation",
        "requires": requires,
        "pins": [{"role": "input", "id": name, "version": "v1", "origin": "assertion"} for name in requires],
        "when": True,
        "value": 1,
        "publishes": symbol,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": requires},
    }


class Track5Ledger(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.rules = [
            _rule("demo.rule.winner", "demo.output", ["demo.input"]),
            _rule("demo.rule.conflict-loser", "demo.output", ["demo.input"]),
            _rule("demo.rule.absent", "demo.absent-output", ["demo.missing"]),
        ]

    def context(self) -> RunContext:
        return RunContext(
            run_id="demo.track5.run",
            rules=self.rules,
            parameters={},
            canon={},
            inputs=[InputFinding("demo.input", 1, "finding.input", "input")],
            sources=[],
            adoption_pin=ADOPTION,
            governance_pins=GOVERNANCE,
        )

    def test_schedulers_share_total_v2_ledger_classification(self) -> None:
        forward = run(self.context(), self.schemas)
        reference = run_reference(self.context(), self.schemas)

        def rows(result: RunResult) -> dict[str, dict[str, Any]]:
            return {row["artifact_id"]: row for row in result.dispositions}

        self.assertEqual(rows(forward), rows(reference))
        ledger = rows(forward)
        self.assertEqual(set(ledger), {rule["id"] for rule in self.rules})
        self.assertEqual(ledger["demo.rule.winner"]["disposition"], "published")
        self.assertEqual(ledger["demo.rule.conflict-loser"]["disposition"], "inapplicable")
        self.assertEqual(ledger["demo.rule.conflict-loser"]["superseded_by"]["id"], "demo.rule.winner")
        self.assertEqual(ledger["demo.rule.absent"]["disposition"], "blocked")
        self.assertEqual(ledger["demo.rule.absent"]["missing"], ["demo.missing"])

    def test_run_and_record_writes_v2_ledger_without_second_blocked_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stream = RecordStream(Path(tmp) / "workspace", self.schemas)
            run_and_record(
                self.context(), self.schemas, stream,
                workspace_revision=4,
                adopted_packages={ADOPTION["id"]},
                start_record_id="demo.track5.start",
                completion_record_id="demo.track5.done",
            )
            closing = stream.standings()["demo.track5.run"].closing
            assert closing is not None
            self.assertEqual(closing["schema"], "derivation-record.v7")
            self.assertNotIn("blocked", closing)
            self.assertEqual({row["artifact_id"] for row in closing["dispositions"]}, {rule["id"] for rule in self.rules})
