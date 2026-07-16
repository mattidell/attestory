"""Track 6 integration scenarios for the complete 2025 core package.

Each synthetic workspace names the same committed content fixture, proves
forward/reference parity, and pins the read-only derive CLI report. Together
they cover standard deduction selection, interest composition closure, and
the first tax-bracket crossing without any personal source material.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import run
from packages.derivation.runners.derive import _context, load_scenario


SCENARIOS = Path("packages/sample_data/tax/scenarios")
NAMES = (
    "single_standard_deduction",
    "mfj_standard_deduction",
    "standard_deduction_age_blind",
    "itemized_deduction_override",
    "unclosed_interest_composition",
    "tax_bracket_boundaries",
    "acm_a1_unpinned_content",
)


def _publications(result: Any) -> list[dict[str, Any]]:
    return sorted((publication.finding for publication in result.publications), key=lambda finding: finding["id"])


class Track6IntegrationScenarios(unittest.TestCase):
    maxDiff = None

    def _path(self, name: str) -> Path:
        return SCENARIOS / name / "scenario.json"

    def _cli(self, name: str) -> dict[str, Any]:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "packages.derivation.runners.derive",
                "--scenario",
                str(self._path(name)),
                "--json",
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        return cast(dict[str, Any], json.loads(completed.stdout))

    def test_all_scenarios_have_forward_reference_parity(self) -> None:
        schemas = DerivationSchemas()
        for name in NAMES:
            with self.subTest(scenario=name):
                context = _context(load_scenario(self._path(name)))
                forward = run(context, schemas)
                reference = run_reference(context, schemas)
                self.assertEqual(_publications(forward), _publications(reference))
                self.assertEqual(forward.blocked, reference.blocked)
                self.assertEqual(forward.stop_reason, reference.stop_reason)

    def test_cli_reports_match_committed_goldens(self) -> None:
        for name in NAMES:
            with self.subTest(scenario=name):
                golden = self._path(name).parent / "expected" / "report.json"
                self.assertEqual(self._cli(name), json.loads(golden.read_text("utf-8")))

    def test_scenarios_cover_the_declared_lifecycle_outcomes(self) -> None:
        expected = {
            "single_standard_deduction": {"tax.us.2025.tax.total-tax": "3968"},
            "mfj_standard_deduction": {"tax.us.2025.interest.taxable-total": "100", "tax.us.2025.tax.total-tax": "6748"},
            "standard_deduction_age_blind": {"demo.form1040.standard_deduction": "19000"},
            "itemized_deduction_override": {"tax.us.2025.deductions.total": "35000"},
            "tax_bracket_boundaries": {"tax.us.2025.income.taxable-income": "11601", "tax.us.2025.tax.total-tax": "1160"},
        }
        for name, symbols in expected.items():
            with self.subTest(scenario=name):
                report = self._cli(name)
                published = {entry["symbol"]: entry["value"] for entry in report["published"]}
                for symbol, value in symbols.items():
                    self.assertEqual(published[symbol], value)

        unclosed = self._cli("unclosed_interest_composition")
        blocked = {entry["artifact_id"]: entry["code"] for entry in unclosed["blocked"]}
        self.assertEqual(blocked["tax.us.2025.rule.non-form-interest-subtotal"], "SOURCE_SET_UNCLOSED")
        for rule_id in (
            "tax.us.2025.rule.form1040-line2b",
            "tax.us.2025.rule.form1040-line9",
            "tax.us.2025.rule.form1040-line11",
            "tax.us.2025.rule.form1040-line15",
            "tax.us.2025.rule.form1040-line16",
        ):
            self.assertEqual(blocked[rule_id], "DEPENDENCY_ABSENT")

    def test_acm_a1_projects_only_adopted_members(self) -> None:
        # Exclusive execution projection (ADR-0027 decision 7 / PMR-1): a
        # co-located rule that is not a package member must not reach any
        # execution surface. The scenario adopts the core package while a
        # sibling unpinned rule publishes tax.us.2025.unpinned_result; that
        # symbol must be absent from the report. Committed-golden equality is
        # asserted by test_cli_reports_match_committed_goldens (NAMES).
        report = self._cli("acm_a1_unpinned_content")
        published_symbols = {entry["symbol"] for entry in report["published"]}
        self.assertNotIn("tax.us.2025.unpinned_result", published_symbols)


if __name__ == "__main__":
    unittest.main()
