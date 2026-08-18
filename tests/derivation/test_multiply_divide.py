"""Track 1 (f1098e-student-loan-interest-agi): `multiply`/`divide` operators.

Direct evaluator-level tests, mirroring `tests/test_f1098_mortgage_interest_t1.py`'s
`evaluate()`-against-a-hand-built-`Environment` pattern. `multiply` mirrors
`subtract`'s left/right shape exactly; `divide` adds a `min_decimal_places`
precision floor and a `rounding` mode drawn from `_ROUND_MODES`, and blocks
`DEPENDENCY_INVALID` on a zero divisor rather than raising or producing
Infinity (T0-4/T0-9).
"""

from __future__ import annotations

import unittest
from decimal import Decimal

from packages.derivation.evaluator import (
    BLOCK_INVALID,
    AccessLog,
    Environment,
    EvalBlocked,
    evaluate,
)


def _env(symbols: dict[str, object] | None = None) -> Environment:
    return Environment(
        symbols=symbols or {},
        sources={},
        closed_sets=frozenset(),
        parameters={},
        canon={},
    )


class MultiplyOperator(unittest.TestCase):
    def test_multiplies_two_literals(self) -> None:
        expr = {"op": "multiply", "left": "1500.00", "right": "0.674"}
        self.assertEqual(evaluate(expr, _env(), AccessLog()), Decimal("1500.00") * Decimal("0.674"))

    def test_multiplies_refs(self) -> None:
        env = _env({"a": "40.0", "b": "3"})
        expr = {"op": "multiply", "left": {"op": "ref", "name": "a"}, "right": {"op": "ref", "name": "b"}}
        self.assertEqual(evaluate(expr, env, AccessLog()), Decimal("120.0"))

    def test_zero_operand_yields_zero(self) -> None:
        expr = {"op": "multiply", "left": "0", "right": "12345.67"}
        self.assertEqual(evaluate(expr, _env(), AccessLog()), Decimal("0"))


class DivideOperator(unittest.TestCase):
    def test_divides_two_literals(self) -> None:
        expr = {
            "op": "divide",
            "left": "10",
            "right": "4",
            "min_decimal_places": 2,
            "rounding": "half_up",
        }
        self.assertEqual(evaluate(expr, _env(), AccessLog()), Decimal("2.50"))

    def test_zero_divisor_blocks_dependency_invalid(self) -> None:
        expr = {
            "op": "divide",
            "left": "1500",
            "right": "0",
            "min_decimal_places": 3,
            "rounding": "half_up",
        }
        with self.assertRaises(EvalBlocked) as ctx:
            evaluate(expr, _env(), AccessLog())
        self.assertEqual(ctx.exception.category, BLOCK_INVALID)

    def test_min_decimal_places_worksheet_line7_shape(self) -> None:
        # i1040gi p.99 worksheet line 7: MAGI-excess divided by $15,000
        # ($30,000 MFJ), rounded to at least three decimal places. Track 1
        # proves only the primitive's precision floor, not the cap.
        expr = {
            "op": "divide",
            "left": {"op": "ref", "name": "excess"},
            "right": "15000",
            "min_decimal_places": 3,
            "rounding": "half_up",
        }
        env = _env({"excess": "2000"})
        self.assertEqual(evaluate(expr, env, AccessLog()), Decimal("0.133"))

    def test_min_decimal_places_floor_extends_exact_ratio(self) -> None:
        # A ratio that terminates before the floor is still padded to it.
        expr = {
            "op": "divide",
            "left": "1",
            "right": "4",
            "min_decimal_places": 5,
            "rounding": "half_up",
        }
        self.assertEqual(evaluate(expr, _env(), AccessLog()), Decimal("0.25000"))

    def test_rounding_mode_half_even_applies(self) -> None:
        expr = {
            "op": "divide",
            "left": "0.125",
            "right": "1",
            "min_decimal_places": 2,
            "rounding": "half_even",
        }
        self.assertEqual(evaluate(expr, _env(), AccessLog()), Decimal("0.12"))

    def test_unknown_rounding_mode_blocks_dependency_invalid(self) -> None:
        expr = {
            "op": "divide",
            "left": "1",
            "right": "2",
            "min_decimal_places": 2,
            "rounding": "banker",
        }
        with self.assertRaises(EvalBlocked) as ctx:
            evaluate(expr, _env(), AccessLog())
        self.assertEqual(ctx.exception.category, BLOCK_INVALID)


if __name__ == "__main__":
    unittest.main()
