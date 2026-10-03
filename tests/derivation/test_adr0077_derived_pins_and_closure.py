"""ADR 0077 Part 3 derived pins on the record schemas, and the closure edges.

A run whose dispositions pin a per-subject entry as ``derived`` closes on
``derivation-record.v10``; every other record stays on v9 and every other
finding on ``derived-finding.v2``. The authorization-closure graph adds the
shared-key count's edge and the v13 selection's edges package validation
adds (Track 1b open question 3).
"""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.authorization_closure import build_dependency_edges, rule_scoped_closure
from packages.derivation.loader import DerivationSchemas
from packages.derivation.records import RecordStream
from packages.derivation.runner import run_and_record
from tests.derivation import adr0077_worksheet_fixture as fx
from tests.derivation.test_presence_selection_subject_reads import derived_pins, run_case


class DerivedPinRecords(unittest.TestCase):
    """Part 3 "Pins": derived-finding.v3 and derivation-record.v10 only when carried."""

    def _record(self, case: str) -> dict[str, Any]:
        ctx = fx.marshal(fx.parts(), fx.case_rows(case), run_id=f"demo.run.adr0077.{case}")
        schemas = DerivationSchemas()
        with tempfile.TemporaryDirectory() as directory:
            stream = RecordStream(Path(directory), schemas)
            run_and_record(
                ctx, schemas, stream, workspace_revision=0,
                adopted_packages={fx.ADOPTION_PIN["id"]},
                start_record_id=f"demo.record.{case}.start",
                completion_record_id=f"demo.record.{case}.close",
            )
            records = stream.read().records
        self.assertEqual(len(records), 2)
        return {"start": records[0], "close": records[1]}

    def test_a_run_with_a_derived_entry_pin_closes_on_v10(self) -> None:
        records = self._record("old-only")
        self.assertEqual(records["start"]["schema"], "derivation-record.v9")
        self.assertEqual(records["close"]["schema"], "derivation-record.v10")
        worksheet_rows = [row for row in records["close"]["dispositions"] if row["artifact_id"] == fx.WORKSHEET]
        self.assertEqual(len(derived_pins(worksheet_rows[0]["pins"])), 5)

    def test_a_run_without_one_stays_on_v9(self) -> None:
        records = self._record("closed-empty")
        self.assertEqual(records["close"]["schema"], "derivation-record.v9")

    def test_the_published_v9_and_v2_schemas_reject_a_derived_origin(self) -> None:
        forward, _reference = run_case(fx.case_rows("new-only"))
        finding = copy.deepcopy(fx.line21(forward)["finding"])
        finding["schema"] = "derived-finding.v2"
        finding["version"] = "v2"
        with self.assertRaises(Exception):
            DerivationSchemas().validate_declared(finding)


class AuthorizationClosureEdges(unittest.TestCase):
    """The closure graph keeps step with package validation (Track 1b open question 3)."""

    def _corpus(self) -> dict[str, dict[str, Any]]:
        return {citizen["id"]: citizen for citizen, _role in fx.parts()}

    def test_shared_key_count_reaches_its_counted_fact_type(self) -> None:
        edges = build_dependency_edges(self._corpus())
        self.assertIn(fx.FIN, edges[fx.COUNT_RULE])
        self.assertIn(fx.FIN, edges[fx.SUPPORT_RULE])

    def test_the_worksheet_reaches_its_declared_publishers_and_activity(self) -> None:
        corpus = self._corpus()
        reached = {member_id for member_id, _version in rule_scoped_closure({fx.WORKSHEET}, corpus)}
        for answer in fx.ANSWERS:
            self.assertIn(fx.STATUS_RULE[answer], reached)
            self.assertIn(answer, reached)
        for member in (fx.STATEMENT_RULE, fx.SUPPORT_RULE, fx.INCL, fx.FIN, fx.FAMILY):
            self.assertIn(member, reached)


if __name__ == "__main__":
    unittest.main()
