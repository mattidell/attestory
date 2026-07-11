"""Track 3 verification: paired derivation records, gate, and crash window.

Covers ADR-0008 as tested contracts:
- E14.1 paired records: a run is a started record plus a separate closing
  record; the stream is append-only and mis-pairings halt reads.
- E14.2 inapplicable-vs-unreached: a completed record names an evaluated-but
  -inapplicable rule with its guard result and pins, so it is distinguishable
  from a rule never reached (round-2 adversary attack 9).
- E6.1 interruption safety: exhaustive byte truncation of the stream yields a
  valid shorter stream at every cut; the orphan window is detectable and
  recovered by appending an `interrupted` record without mutating the start.
- Adoption gate: a run cannot start against an unadopted package.
"""

import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.records import (
    AdoptionError,
    RecordStream,
    RecordStreamCorruption,
    closing_record,
    recover_interrupted,
    start_run,
    started_record,
)

GOV_PINS = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]
ADOPTION_PIN = {"role": "adoption", "id": "demo.package.first-slice.2025", "version": "v1"}


def _completed(run_id: str, record_id: str) -> dict[str, Any]:
    return closing_record(
        record_id=record_id,
        run_id=run_id,
        phase="completed",
        workspace_revision=7,
        governance_pins=GOV_PINS,
        adoption_pin=ADOPTION_PIN,
        stop_reason="saturated",
        published=[{"symbol": "demo.form1040.line1a", "finding_id": "f.line1a", "act_id": "a.line1a"}],
        blocked=[],
        dispositions=[
            {"artifact_id": "demo.rule.wages-to-1040-line1a", "disposition": "published",
             "pins": [{"role": "input", "id": "f.w2box1", "version": "v1"}]},
            {"artifact_id": "demo.rule.tax-table-line16", "disposition": "inapplicable", "guard_result": False,
             "pins": [{"role": "input", "id": "f.line15", "version": "v1"}]},
        ],
    )


class RecordStreamFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.workspace = Path(self._tmp.name) / "workspace"
        self.stream = RecordStream(self.workspace, self.schemas)


class AdoptionGate(RecordStreamFixture):
    def test_unadopted_package_cannot_start_a_run(self) -> None:
        with self.assertRaises(AdoptionError):
            start_run(self.stream, record_id="r.start", run_id="run.1", workspace_revision=7,
                      governance_pins=GOV_PINS, adoption_pin=ADOPTION_PIN, adopted_packages=set())

    def test_adopted_package_starts_and_is_open(self) -> None:
        start_run(self.stream, record_id="r.start", run_id="run.1", workspace_revision=7,
                  governance_pins=GOV_PINS, adoption_pin=ADOPTION_PIN,
                  adopted_packages={"demo.package.first-slice.2025"})
        self.assertIn("run.1", self.stream.open_runs())


class Pairing(RecordStreamFixture):
    def test_completed_closes_the_run(self) -> None:
        self.stream.append(started_record(record_id="r.s", run_id="run.1", workspace_revision=7,
                                           governance_pins=GOV_PINS, adoption_pin=ADOPTION_PIN))
        self.stream.append(_completed("run.1", "r.c"))
        self.assertEqual(self.stream.open_runs(), {})

    def test_close_before_start_is_corruption(self) -> None:
        with self.assertRaises(RecordStreamCorruption):
            self.stream.append(_completed("run.404", "r.c"))

    def test_double_start_is_corruption(self) -> None:
        self.stream.append(started_record(record_id="r.s", run_id="run.1", workspace_revision=7,
                                          governance_pins=GOV_PINS, adoption_pin=ADOPTION_PIN))
        with self.assertRaises(RecordStreamCorruption):
            self.stream.append(started_record(record_id="r.s2", run_id="run.1", workspace_revision=7,
                                              governance_pins=GOV_PINS, adoption_pin=ADOPTION_PIN))


class InapplicableVsUnreached(RecordStreamFixture):
    def test_completed_record_distinguishes_inapplicable_from_unreached(self) -> None:
        record = _completed("run.1", "r.c")
        by_disposition = {d["disposition"]: d for d in record["dispositions"]}
        # The false-guard rule is recorded as inapplicable, with its guard
        # result and the pins it read — not silently omitted.
        self.assertIn("inapplicable", by_disposition)
        self.assertFalse(by_disposition["inapplicable"]["guard_result"])
        self.assertTrue(by_disposition["inapplicable"]["pins"])
        # A rule never reached appears nowhere in dispositions: the two
        # "nothings" are structurally different, so the record is not
        # signature-identical to an unsaturated snapshot (attack 9).
        named = {d["artifact_id"] for d in record["dispositions"]}
        self.assertNotIn("demo.rule.some-unreached-rule", named)


class InterruptionSafety(RecordStreamFixture):
    def setUp(self) -> None:
        super().setUp()
        self.stream.append(started_record(record_id="r.s", run_id="run.1", workspace_revision=7,
                                          governance_pins=GOV_PINS, adoption_pin=ADOPTION_PIN))
        self.stream.append(_completed("run.1", "r.c"))
        self.full_bytes = self.stream.path.read_bytes()
        self.line_ends = [i + 1 for i, b in enumerate(self.full_bytes) if b == ord("\n")]

    def _reload_truncated(self, cut: int) -> RecordStream:
        self.stream.path.write_bytes(self.full_bytes[:cut])
        return RecordStream(self.workspace, self.schemas)

    def test_every_byte_truncation_yields_a_valid_shorter_stream(self) -> None:
        for cut in range(len(self.full_bytes) + 1):
            with self.subTest(cut=cut):
                contents = self._reload_truncated(cut).read()
                committed = sum(1 for end in self.line_ends if end <= cut)
                self.assertEqual(len(contents.records), committed)
                mid_line = cut not in (0, *self.line_ends)
                self.assertEqual(contents.incomplete_tail is not None, mid_line)

    def test_crash_after_start_leaves_a_detectable_recoverable_open_run(self) -> None:
        # Cut just after the started record's newline: the start committed,
        # the completion never did. The run is detectably open and recovery
        # appends an interrupted close without touching the start record.
        cut = self.line_ends[0]
        stream = self._reload_truncated(cut)
        self.assertIn("run.1", stream.open_runs())
        start_before = stream.standings()["run.1"].start
        recover_interrupted(stream, "run.1", record_id="r.recovered")
        standing = stream.standings()["run.1"]
        self.assertFalse(standing.is_open)
        assert standing.closing is not None
        self.assertEqual(standing.closing["stop_reason"], "interrupted")
        self.assertEqual(standing.start, start_before)  # start never mutated

    def test_parseable_but_unterminated_tail_is_not_committed(self) -> None:
        cut = self.line_ends[-1] - 1
        contents = self._reload_truncated(cut).read()
        self.assertEqual(len(contents.records), 1)
        self.assertIsNotNone(contents.incomplete_tail)


if __name__ == "__main__":
    unittest.main()
