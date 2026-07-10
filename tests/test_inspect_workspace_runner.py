"""Inspection runner tests against committed kernel fixture goldens."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

FIXTURE = Path("packages/sample_data/kernel/demo_workspace")


class TestInspectWorkspaceRunner(unittest.TestCase):
    def _run_json(self, *args: str) -> object:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "packages.kernel.runners.inspect_workspace",
                "--workspace",
                str(FIXTURE),
                "--json",
                *args,
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        return json.loads(completed.stdout)

    def _expected(self, name: str) -> object:
        return json.loads((FIXTURE / "expected" / name).read_text("utf-8"))

    def test_runner_json_matches_read_model_golden(self) -> None:
        self.assertEqual(self._run_json(), self._expected("read-model.json"))

    def test_runner_current_view_matches_golden(self) -> None:
        self.assertEqual(
            self._run_json("--view", "current"),
            self._expected("current-state.json"),
        )

    def test_runner_history_view_matches_golden(self) -> None:
        self.assertEqual(
            self._run_json("--view", "history"),
            self._expected("fact-history.json"),
        )

    def test_runner_open_view_matches_golden(self) -> None:
        self.assertEqual(
            self._run_json("--view", "open"),
            self._expected("open-facts.json"),
        )

    def test_runner_human_view_is_read_only_and_demoable(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "packages.kernel.runners.inspect_workspace",
                "--workspace",
                str(FIXTURE),
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertIn("Revision: 5", completed.stdout)
        self.assertIn("finding-new", completed.stdout)
        self.assertIn("demo.rate-choice|period=2025", completed.stdout)


if __name__ == "__main__":
    unittest.main()
