"""Act log unit tests: append discipline and strict reading."""

import tempfile
import unittest
from pathlib import Path

from packages.kernel.act_log import ActLog, ActLogError
from packages.kernel.schema_registry import SchemaRegistryError, SchemaValidationError
from tests.support import demo_note_act, registry_with_demo_kinds


class ActLogFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        root = Path(self._tmp.name)
        schema_dir = root / "schemas"
        schema_dir.mkdir()
        self.registry = registry_with_demo_kinds(schema_dir)
        self.workspace = root / "workspace"
        self.log = ActLog(self.workspace, self.registry)


class TestAppend(ActLogFixture):
    def test_append_and_read_round_trip(self) -> None:
        for i in range(3):
            new_revision = self.log.append(demo_note_act(i), expected_revision=i)
            self.assertEqual(new_revision, i + 1)
        contents = self.log.read()
        self.assertEqual(contents.revision, 3)
        self.assertIsNone(contents.incomplete_tail)
        self.assertEqual([a["act_id"] for a in contents.acts],
                         ["demo-act-000", "demo-act-001", "demo-act-002"])

    def test_stale_expected_revision_is_rejected(self) -> None:
        self.log.append(demo_note_act(0), expected_revision=0)
        with self.assertRaises(ActLogError) as ctx:
            self.log.append(demo_note_act(0), expected_revision=0)
        self.assertIn("stale revision", str(ctx.exception))

    def test_wrong_committed_against_is_rejected(self) -> None:
        act = demo_note_act(0)
        act["committed_against"] = 5
        with self.assertRaises(ActLogError):
            self.log.append(act, expected_revision=0)

    def test_duplicate_act_id_is_rejected(self) -> None:
        self.log.append(demo_note_act(0), expected_revision=0)
        duplicate = demo_note_act(1)
        duplicate["act_id"] = "demo-act-000"
        with self.assertRaises(ActLogError) as ctx:
            self.log.append(duplicate, expected_revision=1)
        self.assertIn("duplicate", str(ctx.exception))

    def test_invalid_envelope_is_rejected_before_write(self) -> None:
        act = demo_note_act(0)
        del act["actor"]
        with self.assertRaises(SchemaValidationError):
            self.log.append(act, expected_revision=0)
        self.assertFalse(self.log.path.exists())

    def test_invalid_payload_is_rejected_before_write(self) -> None:
        act = demo_note_act(0)
        act["payload"] = {"text": ""}
        with self.assertRaises(SchemaValidationError):
            self.log.append(act, expected_revision=0)
        self.assertFalse(self.log.path.exists())

    def test_unknown_act_kind_is_rejected(self) -> None:
        act = demo_note_act(0)
        act["kind"] = "demo-unregistered"
        with self.assertRaises(SchemaRegistryError):
            self.log.append(act, expected_revision=0)

    def test_empty_workspace_reads_as_revision_zero(self) -> None:
        contents = self.log.read()
        self.assertEqual(contents.revision, 0)
        self.assertEqual(contents.acts, ())


if __name__ == "__main__":
    unittest.main()
