"""Track 7: ``ActLog.append_batch`` commits several acts as one save, or none.

A save that writes several records must not leave a part of itself behind. The
batch validates every act, checks revisions and identities, and runs the ADR
0077 Part 5 new-write step on each act against the acts staged before it, all
before anything is written. It then writes the log plus the new lines to a
pending file and renames it over the log. An interruption before the rename
leaves the log byte for byte as it was.
"""

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

from packages.kernel.act_log import ActLog, ActLogError
from packages.kernel.schema_registry import SchemaValidationError
from tests.support import demo_note_act, registry_with_demo_kinds


class _Interrupted(Exception):
    """A simulated crash; nothing in the writer catches it."""


class BatchFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        root = Path(self._tmp.name)
        schema_dir = root / "schemas"
        schema_dir.mkdir()
        self.registry = registry_with_demo_kinds(schema_dir)
        self.workspace = root / "workspace"
        self.log = ActLog(self.workspace, self.registry, undeclared_test_log=True)
        for index in range(2):
            self.log.append(demo_note_act(index), expected_revision=index)
        self.before = self.log.path.read_bytes()

    def _batch(self, start: int, count: int) -> list[dict[str, Any]]:
        return [demo_note_act(start + offset) for offset in range(count)]


class AppendBatch(BatchFixture):
    def test_a_batch_commits_every_act_in_order(self) -> None:
        revision = self.log.append_batch(self._batch(2, 3), expected_revision=2)
        self.assertEqual(revision, 5)
        contents = ActLog(self.workspace, self.registry, read_only=True).read()
        self.assertEqual([act["act_id"] for act in contents.acts],
                         [f"demo-act-{index:03d}" for index in range(5)])
        self.assertIsNone(contents.incomplete_tail)
        # The committed prefix is byte-identical: the log only grew.
        self.assertTrue(self.log.path.read_bytes().startswith(self.before))

    def test_the_bytes_match_one_append_per_act(self) -> None:
        other = ActLog(Path(self._tmp.name) / "other", self.registry, undeclared_test_log=True)
        for index in range(5):
            other.append(demo_note_act(index), expected_revision=index)
        self.log.append_batch(self._batch(2, 3), expected_revision=2)
        self.assertEqual(self.log.path.read_bytes(), other.path.read_bytes())

    def test_an_interruption_at_any_point_leaves_the_log_as_it_was(self) -> None:
        batch = self._batch(2, 3)
        for lines in range(len(batch)):
            for torn in (False, True):
                with self.subTest(lines=lines, torn=torn):
                    self.log.path.write_bytes(self.before)
                    real = ActLog._write_pending_line
                    written = 0

                    def crash(log: ActLog, handle: Any, line: bytes) -> None:
                        nonlocal written
                        if written >= lines:
                            if torn:
                                handle.write(line[: len(line) // 2])
                                handle.flush()
                            raise _Interrupted
                        written += 1
                        real(log, handle, line)

                    with mock.patch.object(ActLog, "_write_pending_line", crash), \
                            self.assertRaises(_Interrupted):
                        self.log.append_batch(batch, expected_revision=2)
                    self.assertEqual(self.log.path.read_bytes(), self.before)
                    contents = ActLog(self.workspace, self.registry, read_only=True).read()
                    self.assertEqual(contents.revision, 2)
                    self.assertIsNone(contents.incomplete_tail)

    def test_a_crash_after_every_line_but_before_the_rename_leaves_the_log_as_it_was(self) -> None:
        with mock.patch("packages.kernel.act_log.os.replace", side_effect=_Interrupted), \
                self.assertRaises(_Interrupted):
            self.log.append_batch(self._batch(2, 3), expected_revision=2)
        self.assertEqual(self.log.path.read_bytes(), self.before)

    def test_a_leftover_pending_file_does_not_affect_the_next_save(self) -> None:
        with mock.patch("packages.kernel.act_log.os.replace", side_effect=_Interrupted), \
                self.assertRaises(_Interrupted):
            self.log.append_batch(self._batch(2, 3), expected_revision=2)
        self.assertEqual(self.log.read().revision, 2)
        self.assertEqual(self.log.append_batch(self._batch(2, 2), expected_revision=2), 4)
        self.assertEqual(self.log.read().revision, 4)
        self.assertEqual(self.log.append(demo_note_act(4), expected_revision=4), 5)

    def test_any_invalid_act_refuses_the_whole_batch(self) -> None:
        batch = self._batch(2, 3)
        batch[2]["payload"] = {"text": ""}
        with self.assertRaises(SchemaValidationError):
            self.log.append_batch(batch, expected_revision=2)
        self.assertEqual(self.log.path.read_bytes(), self.before)

    def test_revision_sequence_and_identity_are_checked_before_writing(self) -> None:
        cases: dict[str, tuple[list[dict[str, Any]], int, str]] = {}
        stale = self._batch(2, 2)
        cases["stale"] = (stale, 1, "stale revision")
        gap = self._batch(2, 2)
        gap[1]["committed_against"] = 5
        cases["gap"] = (gap, 2, "commits against revision")
        duplicate = self._batch(2, 2)
        duplicate[1]["act_id"] = "demo-act-000"
        cases["duplicate in log"] = (duplicate, 2, "duplicate act_id")
        twice = self._batch(2, 2)
        twice[1]["act_id"] = twice[0]["act_id"]
        cases["duplicate in batch"] = (twice, 2, "duplicate act_id")
        cases["empty"] = ([], 2, "no acts")
        for name, (batch, expected, message) in cases.items():
            with self.subTest(name):
                with self.assertRaisesRegex(ActLogError, message):
                    self.log.append_batch(batch, expected_revision=expected)
                self.assertEqual(self.log.path.read_bytes(), self.before)

    def test_an_uncommitted_tail_is_refused_not_written_onto(self) -> None:
        line = json.dumps(demo_note_act(2), sort_keys=True, separators=(",", ":")).encode()
        with self.log.path.open("ab") as handle:
            handle.write(line[:20])
        torn = self.log.path.read_bytes()
        with self.assertRaisesRegex(ActLogError, "uncommitted"):
            self.log.append_batch(self._batch(2, 1), expected_revision=2)
        self.assertEqual(self.log.path.read_bytes(), torn)

    def test_a_read_only_log_refuses(self) -> None:
        reader = ActLog(self.workspace, self.registry, read_only=True)
        with self.assertRaisesRegex(ActLogError, "read-only"):
            reader.append_batch(self._batch(2, 1), expected_revision=2)
        self.assertEqual(self.log.path.read_bytes(), self.before)

    def test_a_log_changed_during_the_save_is_refused(self) -> None:
        real = ActLog._write_pending_line
        intruded = False

        def intrude(log: ActLog, handle: Any, line: bytes) -> None:
            nonlocal intruded
            if not intruded:
                intruded = True
                ActLog(self.workspace, self.registry, undeclared_test_log=True).append(
                    demo_note_act(2), expected_revision=2)
            real(log, handle, line)

        with mock.patch.object(ActLog, "_write_pending_line", intrude), \
                self.assertRaisesRegex(ActLogError, "changed during the save"):
            self.log.append_batch(self._batch(2, 2), expected_revision=2)
        self.assertEqual(self.log.read().revision, 3)

    def test_a_first_batch_creates_the_log(self) -> None:
        fresh = ActLog(Path(self._tmp.name) / "fresh", self.registry, undeclared_test_log=True)
        self.assertEqual(fresh.append_batch(self._batch(0, 2), expected_revision=0), 2)
        self.assertEqual(fresh.read().revision, 2)


if __name__ == "__main__":
    unittest.main()
