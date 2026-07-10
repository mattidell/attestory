"""Kernel fixture safety and golden consistency tests."""

import json
import unittest
from pathlib import Path

from packages.kernel.read_models import build_read_model
from packages.kernel.schema_registry import SchemaRegistry

FIXTURE_ROOT = Path("packages/sample_data/kernel")
WORKSPACE = FIXTURE_ROOT / "demo_workspace"


class TestKernelFixtures(unittest.TestCase):
    def test_fixture_workspace_rebuilds_expected_golden(self) -> None:
        acts = [
            json.loads(line)
            for line in (WORKSPACE / "acts.jsonl").read_text("utf-8").splitlines()
        ]
        model = build_read_model(tuple(acts), SchemaRegistry())
        expected = json.loads(
            (WORKSPACE / "expected" / "read-model.json").read_text("utf-8")
        )
        self.assertEqual(model, expected)

    def test_committed_kernel_fixtures_have_no_absolute_local_paths(self) -> None:
        forbidden = ("/Users/", "/private/", "local-data/", "uploads/")
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text("utf-8")
            with self.subTest(path=str(path)):
                self.assertFalse(any(marker in text for marker in forbidden))


if __name__ == "__main__":
    unittest.main()
