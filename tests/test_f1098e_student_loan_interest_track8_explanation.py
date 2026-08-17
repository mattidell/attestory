"""Track 8: the explanation walker over this milestone's own real pin chain.

Mirrors ``tests/derivation/test_explanation_cli.py``'s own subprocess-pinned
pattern exactly, but against the ``tools.generate_f1098e_track8_explanation_
golden`` CLI: ``tax.us.2025.income.agi`` for the below-floor scenario (single
Form 1098-E statement, full eligibility, MAGI below the phaseout floor),
walked from a real ``live_coordinate_run`` output via the already-shipped,
milestone-agnostic explanation walker (``packages/derivation/
explanation.py``) -- no new explanation machinery, just this milestone's own
proof of it.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GOLDEN_DIR = REPO / "packages" / "sample_data" / "f1098e_student_loan_interest_track6" / "explanation"


class ExplanationCliGoldens(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "tools.generate_f1098e_track8_explanation_golden", *args],
            check=True, text=True, capture_output=True, cwd=REPO,
        )

    def test_json_report_matches_golden(self) -> None:
        got = json.loads(self._run("--json").stdout)
        expected = json.loads((GOLDEN_DIR / "report.json").read_text("utf-8"))
        self.assertEqual(got, expected)

    def test_human_report_matches_golden(self) -> None:
        self.assertEqual(self._run().stdout, (GOLDEN_DIR / "report.txt").read_text("utf-8"))

    def test_report_recurses_through_the_route_own_pin_chain(self) -> None:
        out = self._run().stdout
        # AGI itself, produced by the successor line-11 rule.
        self.assertIn("tax.us.2025.income.agi = 47500  <- tax.us.2025.rule.form1040-line11", out)
        # Recurses through Schedule 1 line 26 (total adjustments) ...
        self.assertIn(
            "tax.us.2025.schedule1.line26-total-adjustments = 2500  <- tax.us.2025.rule.schedule1-line26",
            out,
        )
        # ... into the SLI worksheet's own published Schedule 1 line 21 ...
        self.assertIn(
            "tax.us.2025.schedule1.line21-sli-deduction = 2500  <- tax.us.2025.rule.sli-worksheet",
            out,
        )
        # ... down to the worksheet's own capped line-1 interest subtotal and
        # its MAGI phaseout parameters, not stopping short at an intermediate
        # node.
        self.assertIn(
            "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal = 3000"
            "  <- tax.us.2025.rule.sli-worksheet-line1-subtotal",
            out,
        )
        self.assertIn("[parameter] tax.us.2025.parameter.sli-magi-threshold", out)
        self.assertIn("[parameter] tax.us.2025.parameter.sli-magi-phase-range", out)
        self.assertIn("[parameter] tax.us.2025.parameter.sli-interest-cap", out)


if __name__ == "__main__":
    unittest.main()
