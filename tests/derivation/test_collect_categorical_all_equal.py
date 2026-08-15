"""Track 6b repair (f1098e-student-loan-interest-agi): `collect_categorical_all_equal`.

Direct evaluator-level tests, mirroring `tests/derivation/test_multiply_divide.py`'s
`evaluate()`-against-a-hand-built-`Environment` pattern.

This op is the corpus's collect-based universal test over a per-member
categorical witness (e.g. "no member of a multi-statement family answers
'no'"), added because `collect` force-coerces every row to `Decimal`
(`_as_decimal`) and cannot read a "yes"/"no" row, and because an unkeyed
`ref` reads exactly one arbitrarily-chosen current finding for a multi-member
fact type (`packages/derivation/marshal.py`'s `matches[0]` binding), never
every member. `collect_categorical_all_equal` reads every row and requires
all of them to equal the expected category before returning `True`.
"""

from __future__ import annotations

import unittest

from packages.derivation.evaluator import (
    BLOCK_ABSENT,
    BLOCK_INVALID,
    AccessLog,
    Environment,
    EvalBlocked,
    evaluate,
)

FACT_TYPE = "tax.us.2025.f1098e.no-related-person-interest"


def _env(sources: dict[str, list[str]] | None = None, *, categorical_domains: dict[str, list[str]] | None = None) -> Environment:
    return Environment(
        symbols={},
        sources=sources or {},
        closed_sets=frozenset(),
        parameters={},
        canon={},
        categorical_domains=categorical_domains or {FACT_TYPE: ["yes", "no"]},
    )


def _expr(name: str = FACT_TYPE, value: str = "yes") -> dict[str, object]:
    return {
        "op": "collect_categorical_all_equal",
        "name": name,
        "value": {
            "op": "category_literal",
            "fact_type": {"id": FACT_TYPE, "version": "v1"},
            "value": value,
        },
    }


class CollectCategoricalAllEqual(unittest.TestCase):
    def test_single_member_all_yes_is_true(self) -> None:
        env = _env({FACT_TYPE: ["yes"]})
        self.assertTrue(evaluate(_expr(), env, AccessLog()))

    def test_multiple_members_all_yes_is_true(self) -> None:
        env = _env({FACT_TYPE: ["yes", "yes", "yes"]})
        self.assertTrue(evaluate(_expr(), env, AccessLog()))

    def test_one_member_no_makes_it_false_regardless_of_order(self) -> None:
        # The order the rows happen to be marshalled in must not matter --
        # this is exactly the correctness property the order-dependent
        # unkeyed-ref defect (path (j)) lacked.
        env_first = _env({FACT_TYPE: ["no", "yes", "yes"]})
        env_last = _env({FACT_TYPE: ["yes", "yes", "no"]})
        self.assertFalse(evaluate(_expr(), env_first, AccessLog()))
        self.assertFalse(evaluate(_expr(), env_last, AccessLog()))

    def test_absent_source_blocks_dependency_absent(self) -> None:
        env = _env({})
        with self.assertRaises(EvalBlocked) as ctx:
            evaluate(_expr(), env, AccessLog())
        self.assertEqual(ctx.exception.category, BLOCK_ABSENT)
        self.assertEqual(ctx.exception.missing, [FACT_TYPE])

    def test_out_of_domain_row_blocks_invalid(self) -> None:
        env = _env({FACT_TYPE: ["yes", "maybe"]})
        with self.assertRaises(EvalBlocked) as ctx:
            evaluate(_expr(), env, AccessLog())
        self.assertEqual(ctx.exception.category, BLOCK_INVALID)

    def test_records_collect_access_for_pinning(self) -> None:
        env = _env({FACT_TYPE: ["yes"]})
        access = AccessLog()
        evaluate(_expr(), env, access)
        self.assertIn(FACT_TYPE, access.collects)
        self.assertNotIn(FACT_TYPE, access.refs)


if __name__ == "__main__":
    unittest.main()
