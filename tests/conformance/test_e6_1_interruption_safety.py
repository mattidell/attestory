"""E6.1 (Atomicity) — Interruption safety.

Detection per the Engineering Constraints: kill each pipeline between
every pair of writes; the workspace must validate as incomplete-but-true
at every cut point. For the act log this is exhaustive truncation: the
log is cut at every byte offset, and every cut must yield a valid
prefix of committed acts — never an exception, never a partial act
admitted, never a repair.
"""

import tempfile
import unittest
from pathlib import Path

from packages.kernel.act_log import ActLog, ActLogCorruption
from tests.support import demo_note_act, registry_with_demo_kinds

ACT_COUNT = 4


class TestE61InterruptionSafety(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        root = Path(self._tmp.name)
        schema_dir = root / "schemas"
        schema_dir.mkdir()
        self.registry = registry_with_demo_kinds(schema_dir)
        self.workspace = root / "workspace"
        log = ActLog(self.workspace, self.registry)
        for i in range(ACT_COUNT):
            log.append(demo_note_act(i), expected_revision=i)
        self.full_bytes = log.path.read_bytes()
        self.line_ends = [
            i + 1 for i, b in enumerate(self.full_bytes) if b == ord("\n")
        ]

    def _reload_truncated(self, cut: int) -> ActLog:
        path = self.workspace / "acts.jsonl"
        path.write_bytes(self.full_bytes[:cut])
        return ActLog(self.workspace, self.registry)

    def test_every_byte_truncation_yields_a_valid_shorter_workspace(self) -> None:
        for cut in range(len(self.full_bytes) + 1):
            with self.subTest(cut=cut):
                contents = self._reload_truncated(cut).read()
                committed = sum(1 for end in self.line_ends if end <= cut)
                self.assertEqual(contents.revision, committed)
                for i, act in enumerate(contents.acts):
                    self.assertEqual(act["act_id"], f"demo-act-{i:03d}")
                mid_line = cut not in (0, *self.line_ends)
                self.assertEqual(contents.incomplete_tail is not None, mid_line)

    def test_parseable_but_unterminated_tail_is_not_committed(self) -> None:
        # Cut exactly at the end of the final JSON body, before its
        # newline: the bytes parse as an act, but the commit marker (the
        # newline) is absent. A log that admitted it would be committing
        # a write that never completed.
        cut = self.line_ends[-1] - 1
        contents = self._reload_truncated(cut).read()
        self.assertEqual(contents.revision, ACT_COUNT - 1)
        self.assertIsNotNone(contents.incomplete_tail)

    def test_mutation_corrupt_interior_line_is_an_error_not_a_repair(self) -> None:
        # Interruption can only ever damage the tail. Damage anywhere
        # else means the file misstates history, which must halt reads,
        # not be skipped over.
        lines = self.full_bytes.split(b"\n")
        lines[1] = lines[1][: len(lines[1]) // 2]
        (self.workspace / "acts.jsonl").write_bytes(b"\n".join(lines))
        with self.assertRaises(ActLogCorruption):
            ActLog(self.workspace, self.registry).read()

    def test_mutation_resequenced_history_is_an_error(self) -> None:
        # Deleting an interior line re-indexes later acts, so every
        # later act's committed_against revision no longer matches its
        # position: the record no longer supports its own pins.
        lines = self.full_bytes.split(b"\n")
        del lines[1]
        (self.workspace / "acts.jsonl").write_bytes(b"\n".join(lines))
        with self.assertRaises(ActLogCorruption):
            ActLog(self.workspace, self.registry).read()


if __name__ == "__main__":
    unittest.main()
