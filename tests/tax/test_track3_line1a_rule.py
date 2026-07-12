"""Track 3 verification: line-1a rule package and integration.

Boundary (milestone plan): nonempty present-source paths only. No
closure-backed empty-source publication, no downstream Form 1040 lines, no
new machinery — the rule/package are the only new content; the runner,
evaluator, reference runner, and explanation walker are exercised as
published.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.explanation import explain, index_derived
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.package_validation import validate_package
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import InputFinding, RunContext, RunResult, SourceFact, run
from packages.tax.loader import load_form_fields, tax_registry

CONTENT = Path("packages/content/tax/2025")
SCENARIOS = Path("packages/sample_data/tax/scenarios")

RULE_ID = "tax.us.2025.rule.w2-box1-to-line1a"
PACKAGE_ID = "tax.us.2025.package.first-tax-slice"
OUTPUT_SYMBOL = "tax.us.2025.wages.total-w2-box1"


def _load(path: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(path.read_text("utf-8"))
    return loaded


def _rule() -> dict[str, Any]:
    return _load(CONTENT / "rule.wages-line1a.json")


def _package() -> dict[str, Any]:
    return _load(CONTENT / "package.first-tax-slice.json")


class SchemaAuthority(unittest.TestCase):
    """The production rule/package validate against the *published* schemas."""

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def test_rule_validates_against_published_rule_artifact_schema(self) -> None:
        self.schemas.validate_declared(_rule())

    def test_package_validates_against_published_package_schema(self) -> None:
        self.schemas.validate_declared(_package())

    def test_rule_publishes_the_symbol_the_form_field_binds(self) -> None:
        rule = _rule()
        fields = load_form_fields(tax_registry())
        line_1a = fields["tax.us.2025.form1040.line-1a"]
        self.assertEqual(rule["publishes"], line_1a["binds_symbol"])
        self.assertEqual(rule["publishes"], OUTPUT_SYMBOL)


class PackageClosure(unittest.TestCase):
    """ADR-0006 decisions 6/7: the bounded package closes and owns its output."""

    def test_package_closes_with_only_existing_machinery_members(self) -> None:
        schemas = DerivationSchemas()
        corpus = {(_rule()["id"], _rule()["version"]): _rule()}
        result = validate_package(_package(), corpus, schemas)
        self.assertTrue(result.ok, msg=str(result.issues))
        self.assertEqual(result.output_owners[OUTPUT_SYMBOL], RULE_ID)

    def test_package_carries_exactly_the_line1a_rule_no_downstream_line(self) -> None:
        package = _package()
        self.assertEqual(len(package["members"]), 1)
        self.assertEqual(package["members"][0]["id"], RULE_ID)


class ScenarioFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)

    def _scenario(self, name: str) -> dict[str, Any]:
        return _load(SCENARIOS / name / "scenario.json")

    def _context(self, name: str) -> RunContext:
        scenario = self._scenario(name)
        return RunContext(
            run_id=scenario["run_id"],
            rules=scenario["rules"],
            parameters={p["id"]: p for p in scenario["parameters"]},
            canon=self.canon,
            inputs=[InputFinding(**i) for i in scenario["inputs"]],
            sources=[SourceFact(**s) for s in scenario["sources"]],
            closed_sets=frozenset(scenario.get("closed_sets", [])),
            adoption_pin=scenario["adoption_pin"],
            governance_pins=scenario["governance_pins"],
        )

    def _findings_blob(self, result: RunResult) -> str:
        findings = sorted((p.finding for p in result.publications), key=lambda f: f["symbol"])
        return json.dumps(findings, sort_keys=True, separators=(",", ":"))


class RunnerParityAndDeterminism(ScenarioFixture):
    SCENARIOS = ("single_w2", "two_w2_same_employer", "present_zero_w2")

    def test_forward_and_reference_runners_agree_on_every_scenario(self) -> None:
        for name in self.SCENARIOS:
            with self.subTest(scenario=name):
                ctx = self._context(name)
                primary = run(ctx, self.schemas)
                reference = run_reference(ctx, self.schemas)
                self.assertEqual(self._findings_blob(primary), self._findings_blob(reference))

    def test_runs_are_deterministic(self) -> None:
        ctx = self._context("single_w2")
        self.assertEqual(
            self._findings_blob(run(ctx, self.schemas)),
            self._findings_blob(run(ctx, self.schemas)),
        )

    def test_computed_values_match_expected_aggregation(self) -> None:
        expected = {"single_w2": "52000", "two_w2_same_employer": "60000", "present_zero_w2": "0"}
        for name, value in expected.items():
            with self.subTest(scenario=name):
                result = run(self._context(name), self.schemas)
                published = {p.finding["symbol"]: p.finding["value"] for p in result.publications}
                self.assertEqual(published[OUTPUT_SYMBOL], value)

    def test_present_zero_is_published_not_blocked(self) -> None:
        # ADR-0012: computed_zero, never a silent absence — and never
        # closure_backed_zero, since this rule never reads closure.
        result = run(self._context("present_zero_w2"), self.schemas)
        self.assertEqual(result.blocked, [])
        self.assertEqual(len(result.publications), 1)

    def test_two_slips_aggregate_into_one_published_finding(self) -> None:
        result = run(self._context("two_w2_same_employer"), self.schemas)
        self.assertEqual(len(result.publications), 1)
        pinned_inputs = [p for p in result.publications[0].finding["pins"] if p["role"] == "input"]
        pinned_ids = {p["id"] for p in pinned_inputs}
        self.assertIn("demo-finding-w2-alpha-1-box1", pinned_ids)
        self.assertIn("demo-finding-w2-alpha-2-box1", pinned_ids)


class ExplanationGoldens(ScenarioFixture):
    def test_nonzero_publication_explains_to_its_source_findings(self) -> None:
        result = run(self._context("single_w2"), self.schemas)
        derived = index_derived([p.finding for p in result.publications])
        finding_id = result.publications[0].finding["id"]
        node = explain(finding_id, role="output", derived=derived)
        self.assertEqual(node.symbol, OUTPUT_SYMBOL)
        self.assertEqual(node.produced_by["id"], RULE_ID)  # type: ignore[index]
        pinned_ids = {c.finding_id for c in node.children}
        self.assertIn("demo-finding-w2-alpha-1-box1", pinned_ids)

    def test_computed_zero_publication_explains_to_its_present_source(self) -> None:
        result = run(self._context("present_zero_w2"), self.schemas)
        derived = index_derived([p.finding for p in result.publications])
        finding_id = result.publications[0].finding["id"]
        node = explain(finding_id, role="output", derived=derived)
        self.assertEqual(node.value, "0")
        pinned_ids = {c.finding_id for c in node.children}
        self.assertIn("demo-finding-w2-alpha-1-box1", pinned_ids)


class DeriveCliGoldens(unittest.TestCase):
    def _run(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable, "-m", "packages.derivation.runners.derive",
                "--scenario", str(SCENARIOS / name / "scenario.json"), *args,
            ],
            check=True, text=True, capture_output=True,
        )

    def test_json_report_matches_golden_for_every_scenario(self) -> None:
        for name in ("single_w2", "two_w2_same_employer", "present_zero_w2"):
            with self.subTest(scenario=name):
                got = json.loads(self._run(name, "--json").stdout)
                expected = json.loads((SCENARIOS / name / "expected" / "report.json").read_text("utf-8"))
                self.assertEqual(got, expected)

    def test_human_report_matches_golden_for_every_scenario(self) -> None:
        for name in ("single_w2", "two_w2_same_employer", "present_zero_w2"):
            with self.subTest(scenario=name):
                got = self._run(name).stdout
                expected = (SCENARIOS / name / "expected" / "report.txt").read_text("utf-8")
                self.assertEqual(got, expected)

    def test_two_slip_report_shows_the_aggregated_total(self) -> None:
        out = self._run("two_w2_same_employer").stdout
        self.assertIn(f"{OUTPUT_SYMBOL} = 60000", out)


class DataSafety(unittest.TestCase):
    def test_committed_track3_content_and_scenarios_have_no_private_markers(self) -> None:
        forbidden = ("/Users/", "/private/", "local-data/", "uploads/")
        for root in (SCENARIOS, CONTENT):
            for path in Path(root).rglob("*"):
                if not path.is_file():
                    continue
                text = path.read_text("utf-8")
                with self.subTest(path=str(path)):
                    self.assertFalse(any(marker in text for marker in forbidden))


if __name__ == "__main__":
    unittest.main()
