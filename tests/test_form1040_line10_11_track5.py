"""Track 5: Form 1040 line 10 / 11a / 11b succession.

Exercises ``tax.us.2025.rule.form1040-line10`` (mints
``tax.us.2025.income.line10-adjustments`` from complete Schedule 1 line 26,
mirroring ``rule.form1040-line8.json``'s thin-passthrough shape) and
``tax.us.2025.rule.form1040-line11`` version ``v2`` (the corrected AGI
producer: total income minus Schedule 1 line 26, directly -- not through
the new line-10 symbol, per Track 0 T0-8's settlement text and the
authority-lifecycle table's explicit dependency list for
``tax.us.2025.income.agi``), directly through the saturation runner's own
``RunContext``/``run`` entry point, mirroring Track 3/4's lightweight
non-kernel harness idiom.

See ``docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md``
T0-8 for the settled design this test proves.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.runner import InputFinding, RunContext, run

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"

LINE10_RULE_FILE = "rule.form1040-line10.json"
LINE11_V2_RULE_FILE = "rule.form1040-line11.v2.json"
LINE11_V1_RULE_FILE = "rule.form1040-line11.json"
LINE15_V2_RULE_FILE = "rule.form1040-line15.v2.json"

LINE10_SYMBOL = "tax.us.2025.income.line10-adjustments"
LINE26_SYMBOL = "tax.us.2025.schedule1.line26-total-adjustments"
TOTAL_INCOME_SYMBOL = "tax.us.2025.income.total-income"
AGI_SYMBOL = "tax.us.2025.income.agi"
TAXABLE_INCOME_SYMBOL = "tax.us.2025.income.taxable-income"

ADOPTION_PIN = {"role": "adoption", "id": "demo.package.form1040-line10-11.2025", "version": "v1"}
GOV_PINS = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)
        self.line10_rule = _load(LINE10_RULE_FILE)
        self.line11_v2_rule = _load(LINE11_V2_RULE_FILE)
        self.line11_v1_rule = _load(LINE11_V1_RULE_FILE)
        self.line15_v2_rule = _load(LINE15_V2_RULE_FILE)
        for rule in (self.line10_rule, self.line11_v2_rule, self.line11_v1_rule, self.line15_v2_rule):
            self.schemas.validate_declared(rule)
        self.parameters: dict[str, dict[str, Any]] = {}

    def _context(self, *, rules: list[dict[str, Any]], inputs: list[InputFinding]) -> RunContext:
        return RunContext(
            run_id="run.f1040.line10-11",
            rules=rules,
            parameters=self.parameters,
            canon=self.canon,
            inputs=inputs,
            sources=[],
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
        )

    def published(self, result: Any, symbol: str) -> str | None:
        for pub in result.publications:
            if pub.finding["symbol"] == symbol:
                return cast(str, pub.finding["value"])
        return None

    def blocked_entry(self, result: Any, artifact_id: str) -> dict[str, Any] | None:
        for entry in result.blocked:
            if entry["artifact_id"] == artifact_id:
                return cast(dict[str, Any], entry)
        return None

    def base_inputs(self, *, total_income: str, line26: str) -> list[InputFinding]:
        return [
            InputFinding("rounding.convention", "half_up", "f.f1040.rounding", "input"),
            InputFinding(TOTAL_INCOME_SYMBOL, total_income, "f.f1040.total-income", "input"),
            InputFinding(LINE26_SYMBOL, line26, "f.f1040.line26", "input"),
        ]


class Line10Cases(Fixture):
    """Line 10 mints its own Form-1040-scoped symbol from Schedule 1 line 26."""

    def test_line10_publishes_from_complete_line26(self) -> None:
        ctx = self._context(
            rules=[self.line10_rule],
            inputs=self.base_inputs(total_income="50000", line26="1000"),
        )
        result = run(ctx, self.schemas)
        self.assertIsNone(self.blocked_entry(result, self.line10_rule["id"]))
        self.assertEqual(self.published(result, LINE10_SYMBOL), "1000")

    def test_line10_zero_when_line26_zero(self) -> None:
        ctx = self._context(
            rules=[self.line10_rule],
            inputs=self.base_inputs(total_income="50000", line26="0"),
        )
        result = run(ctx, self.schemas)
        self.assertEqual(self.published(result, LINE10_SYMBOL), "0")

    def test_line10_blocks_when_line26_absent(self) -> None:
        ctx = self._context(
            rules=[self.line10_rule],
            inputs=[
                InputFinding("rounding.convention", "half_up", "f.f1040.rounding", "input"),
                InputFinding(TOTAL_INCOME_SYMBOL, "50000", "f.f1040.total-income", "input"),
            ],
        )
        result = run(ctx, self.schemas)
        blocked = self.blocked_entry(result, self.line10_rule["id"])
        self.assertIsNotNone(blocked)
        assert blocked is not None
        self.assertEqual(blocked["code"], "DEPENDENCY_ABSENT")
        self.assertIn(LINE26_SYMBOL, blocked["missing"])
        self.assertIsNone(self.published(result, LINE10_SYMBOL))


class AgiCases(Fixture):
    """(a) computed line 26 reduces AGI below total income."""

    def test_agi_reduced_by_line26_when_sli_active(self) -> None:
        ctx = self._context(
            rules=[self.line11_v2_rule],
            inputs=self.base_inputs(total_income="50000", line26="1000"),
        )
        result = run(ctx, self.schemas)
        self.assertIsNone(self.blocked_entry(result, self.line11_v2_rule["id"]))
        self.assertEqual(self.published(result, AGI_SYMBOL), "49000")

    def test_agi_equals_total_income_when_no_f1098e_activity(self) -> None:
        # (b) regression: line 26 = 0 (e.g. only Part I unemployment, or
        # nothing at all) must leave AGI exactly equal to total income,
        # matching v1's bare-passthrough behavior byte-for-byte.
        ctx = self._context(
            rules=[self.line11_v2_rule],
            inputs=self.base_inputs(total_income="72345", line26="0"),
        )
        result = run(ctx, self.schemas)
        self.assertEqual(self.published(result, AGI_SYMBOL), "72345")

        # Cross-check against v1's own bare passthrough directly: same
        # total-income input, same AGI symbol, same published value.
        ctx_v1 = self._context(
            rules=[self.line11_v1_rule],
            inputs=[
                InputFinding("rounding.convention", "half_up", "f.f1040.rounding", "input"),
                InputFinding(TOTAL_INCOME_SYMBOL, "72345", "f.f1040.total-income", "input"),
            ],
        )
        result_v1 = run(ctx_v1, self.schemas)
        self.assertEqual(self.published(result_v1, AGI_SYMBOL), "72345")
        self.assertEqual(self.published(result, AGI_SYMBOL), self.published(result_v1, AGI_SYMBOL))

    def test_agi_blocks_when_line26_absent(self) -> None:
        ctx = self._context(
            rules=[self.line11_v2_rule],
            inputs=[
                InputFinding("rounding.convention", "half_up", "f.f1040.rounding", "input"),
                InputFinding(TOTAL_INCOME_SYMBOL, "50000", "f.f1040.total-income", "input"),
            ],
        )
        result = run(ctx, self.schemas)
        blocked = self.blocked_entry(result, self.line11_v2_rule["id"])
        self.assertIsNotNone(blocked)
        assert blocked is not None
        self.assertEqual(blocked["code"], "DEPENDENCY_ABSENT")
        self.assertIn(LINE26_SYMBOL, blocked["missing"])
        self.assertIsNone(self.published(result, AGI_SYMBOL))

    def test_agi_blocks_when_total_income_absent(self) -> None:
        ctx = self._context(
            rules=[self.line11_v2_rule],
            inputs=[
                InputFinding("rounding.convention", "half_up", "f.f1040.rounding", "input"),
                InputFinding(LINE26_SYMBOL, "1000", "f.f1040.line26", "input"),
            ],
        )
        result = run(ctx, self.schemas)
        blocked = self.blocked_entry(result, self.line11_v2_rule["id"])
        self.assertIsNotNone(blocked)
        assert blocked is not None
        self.assertEqual(blocked["code"], "DEPENDENCY_ABSENT")
        self.assertIn(TOTAL_INCOME_SYMBOL, blocked["missing"])


class Line15UnaffectedCases(Fixture):
    """(c) rule.form1040-line15.v2 still fires correctly off the new AGI producer."""

    def test_taxable_income_computes_from_new_agi_producer(self) -> None:
        ctx = self._context(
            rules=[self.line11_v2_rule, self.line15_v2_rule],
            inputs=self.base_inputs(total_income="50000", line26="1000")
            + [InputFinding("tax.us.2025.deductions.line-14", "14600", "f.f1040.line14", "input")],
        )
        result = run(ctx, self.schemas)
        self.assertIsNone(self.blocked_entry(result, self.line11_v2_rule["id"]))
        self.assertIsNone(self.blocked_entry(result, self.line15_v2_rule["id"]))
        self.assertEqual(self.published(result, AGI_SYMBOL), "49000")
        self.assertEqual(self.published(result, TAXABLE_INCOME_SYMBOL), "34400")

    def test_taxable_income_clamps_at_zero_when_deduction_exceeds_agi(self) -> None:
        ctx = self._context(
            rules=[self.line11_v2_rule, self.line15_v2_rule],
            inputs=self.base_inputs(total_income="10000", line26="8000")
            + [InputFinding("tax.us.2025.deductions.line-14", "14600", "f.f1040.line14", "input")],
        )
        result = run(ctx, self.schemas)
        self.assertEqual(self.published(result, AGI_SYMBOL), "2000")
        self.assertEqual(self.published(result, TAXABLE_INCOME_SYMBOL), "0")


if __name__ == "__main__":
    unittest.main()
