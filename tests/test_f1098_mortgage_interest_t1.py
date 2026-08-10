"""Track 1 Form 1098 Mortgage Interest, Schedule A Line 8a: schema/content citizens (ADR-0052)."""

from __future__ import annotations

import unittest
import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from packages.derivation.evaluator import AccessLog, Environment, EvalBlocked, evaluate


AUTHORITY_FACTS = [
    "liable-and-paid",
    "qualified-main-home",
    "acquisition-debt-use",
    "no-balance-increase",
    "no-refinance",
    "single-mortgage-single-home",
    "not-shared-except-spouse",
    "no-mortgage-interest-credit"
]

class TestF1098MortgageInterestRule(unittest.TestCase):
    rule: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        with open("packages/content/tax/2025/rule.schedule-a-line8a.json") as f:
            cls.rule = json.load(f)["when"]

    def _env(self, box1_values: list[str], scope: dict[str, str] | None = None, closed: bool = True) -> Environment:
        symbols = {f"tax.us.2025.f1098.{a}": "yes" for a in AUTHORITY_FACTS}
        if scope:
            symbols.update(scope)

        closed_sets = frozenset(["tax.us.2025.f1098"]) if closed else frozenset()

        return Environment(
            symbols=symbols,
            sources={
                "tax.us.2025.f1098.box1-mortgage-interest": box1_values
            },
            closed_sets=closed_sets,
            parameters={},
            canon={},
            symbol_fact_types={f"tax.us.2025.f1098.{a}": f"tax.us.2025.f1098.{a}" for a in AUTHORITY_FACTS},
            categorical_domains={f"tax.us.2025.f1098.{a}": ["yes", "no"] for a in AUTHORITY_FACTS}
        )

    def test_single_f1098_in_scope_is_true(self) -> None:
        env = self._env(["15000.0"])
        self.assertTrue(evaluate(self.rule, env, AccessLog()))

    def test_multiple_f1098_blocks(self) -> None:
        env = self._env(["15000.0", "5000.0"])
        with self.assertRaisesRegex(EvalBlocked, "MULTIPLE_F1098_OUT_OF_SCOPE"):
            evaluate(self.rule, env, AccessLog())

    def test_zero_f1098_is_false(self) -> None:
        env = self._env([])
        self.assertFalse(evaluate(self.rule, env, AccessLog()))

    def test_out_of_scope_authority_is_false(self) -> None:
        env = self._env(["15000.0"], scope={"tax.us.2025.f1098.qualified-main-home": "no"})
        self.assertFalse(evaluate(self.rule, env, AccessLog()))

    def test_unclosed_f1098_blocks(self) -> None:
        env = self._env(["15000.0"], closed=False)
        with self.assertRaisesRegex(EvalBlocked, "SOURCE_SET_UNCLOSED"):
            evaluate(self.rule, env, AccessLog())

if __name__ == "__main__":
    unittest.main()
