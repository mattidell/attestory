"""Track 6 verification: explanation chains and the derive CLI (E15.1).

The walker is tested directly for the property that matters — a derived value
recurses through pin roles into the derived and human findings it stands on —
and the CLI is pinned against committed goldens via subprocess, proving the
report is deterministic and demoable.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

from packages.derivation.explanation import explain, index_derived, render_text

SCENARIO_DIR = Path("packages/sample_data/derivation/scenarios/first_slice")


class ExplanationWalker(unittest.TestCase):
    def _derived(self, symbol: str, value: str, pins: list[dict[str, str]], fid: str) -> dict[str, object]:
        return {"schema": "derived-finding.v1", "id": fid, "symbol": symbol,
                "value": value, "version": "v1", "pins": pins}

    def test_walk_recurses_derived_dependencies_and_stops_at_leaves(self) -> None:
        line1a = self._derived(
            "line1a", "42000",
            [{"role": "field-mapping", "id": "rule.wages", "version": "v1"},
             {"role": "input", "id": "f.w2", "version": "v1"},
             {"role": "operation-semantics", "id": "round", "version": "v1"}],
            "finding:derived:aaa",
        )
        line9 = self._derived(
            "line9", "42000",
            [{"role": "computation", "id": "rule.line9", "version": "v1"},
             {"role": "input", "id": "finding:derived:aaa", "version": "v1"}],
            "finding:derived:bbb",
        )
        derived = index_derived([line1a, line9])
        inputs = {"f.w2": {"symbol": "w2.box1", "value": "42000", "role": "input"}}
        node = explain("finding:derived:bbb", role="output", derived=derived, inputs=inputs)

        self.assertEqual(node.kind, "derived")
        self.assertEqual(node.produced_by["id"], "rule.line9")  # type: ignore[index]
        # its one dependency is the derived line1a, expanded
        child = node.children[0]
        self.assertEqual(child.kind, "derived")
        self.assertEqual(child.symbol, "line1a")
        self.assertEqual(child.produced_by["id"], "rule.wages")  # type: ignore[index]
        # which in turn reaches the human W-2 leaf and the round canon leaf
        kinds = {c.kind for c in child.children}
        self.assertIn("input", kinds)
        self.assertIn("operation-semantics", kinds)

    def test_render_text_is_stable_and_shows_producer(self) -> None:
        finding = self._derived(
            "line1a", "42000",
            [{"role": "field-mapping", "id": "rule.wages", "version": "v1"}],
            "finding:derived:aaa",
        )
        node = explain("finding:derived:aaa", role="output", derived=index_derived([finding]))
        text = render_text(node)
        self.assertIn("[output] line1a = 42000", text)
        self.assertIn("<- rule.wages", text)


class DeriveCliGoldens(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "packages.derivation.runners.derive",
             "--scenario", str(SCENARIO_DIR / "scenario.json"), *args],
            check=True, text=True, capture_output=True,
        )

    def test_json_report_matches_golden(self) -> None:
        got = json.loads(self._run("--json").stdout)
        expected = json.loads((SCENARIO_DIR / "expected" / "report.json").read_text("utf-8"))
        self.assertEqual(got, expected)

    def test_human_report_matches_golden(self) -> None:
        self.assertEqual(self._run().stdout, (SCENARIO_DIR / "expected" / "report.txt").read_text("utf-8"))

    def test_report_is_demoable(self) -> None:
        out = self._run().stdout
        self.assertIn("demo.form1040.line16 = 1559", out)
        self.assertIn("demo.form1040.line9 = 42000", out)
        # the chained derived-of-derived is visible in the tree
        self.assertIn("demo.form1040.line1a = 42000  <- demo.rule.wages-to-1040-line1a", out)


if __name__ == "__main__":
    unittest.main()
