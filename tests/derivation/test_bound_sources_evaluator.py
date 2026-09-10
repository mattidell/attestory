"""ADR-0074 Decision 2: bound_sources evaluator contract.

Reads only env.bound_sources, never env.sources; records the name on
AccessLog.bound_source_names and never on collects; empty or missing
raises DEPENDENCY_ABSENT. Environment.bound_sources is defaulted so the
five-positional pairing construction still works.
"""

from __future__ import annotations

import unittest
from decimal import Decimal

from packages.derivation.evaluator import (
    BLOCK_ABSENT,
    AccessLog,
    Environment,
    EvalBlocked,
    evaluate,
)
from packages.derivation.records import CURRENT_RECORD_SCHEMA
from packages.derivation.runner import RECORD_CODES
from packages.tax.pairing_consequences import _pairing_local_environment


class BoundSourcesEvaluator(unittest.TestCase):
    def _env(self, **overrides: object) -> Environment:
        kwargs: dict[str, object] = dict(
            symbols={},
            sources={},
            closed_sets=frozenset(),
            parameters={},
            canon={},
        )
        kwargs.update(overrides)
        return Environment(**kwargs)  # type: ignore[arg-type]

    def test_reads_bound_sources_not_sources(self) -> None:
        env = self._env(
            sources={"demo.allocation.amount": ["999"]},
            bound_sources={"demo.allocation.amount": ["300", "150"]},
        )
        access = AccessLog()
        result = evaluate(
            {"op": "bound_sources", "name": "demo.allocation.amount"},
            env,
            access,
        )
        self.assertEqual(result, [Decimal("300"), Decimal("150")])
        self.assertEqual(access.bound_source_names, {"demo.allocation.amount"})
        self.assertEqual(access.collects, set())

    def test_empty_or_missing_raises_dependency_absent(self) -> None:
        empty: dict[str, list[str]] = {}
        present_empty: dict[str, list[str]] = {"demo.allocation.amount": []}
        for bound in (empty, present_empty):
            with self.subTest(bound=bound):
                env = self._env(
                    sources={"demo.allocation.amount": ["450"]},
                    bound_sources=bound,
                )
                access = AccessLog()
                with self.assertRaises(EvalBlocked) as ctx:
                    evaluate(
                        {"op": "bound_sources", "name": "demo.allocation.amount"},
                        env,
                        access,
                    )
                self.assertEqual(ctx.exception.category, BLOCK_ABSENT)
                self.assertEqual(ctx.exception.missing, ["demo.allocation.amount"])
                self.assertEqual(access.collects, set())
                self.assertEqual(access.bound_source_names, {"demo.allocation.amount"})

    def test_add_flattens_bound_sources(self) -> None:
        env = self._env(bound_sources={"demo.allocation.amount": ["300", "150"]})
        access = AccessLog()
        result = evaluate(
            {
                "op": "add",
                "args": [{"op": "bound_sources", "name": "demo.allocation.amount"}],
            },
            env,
            access,
        )
        self.assertEqual(result, Decimal("450"))

    def test_five_positional_environment_still_constructs(self) -> None:
        env = Environment({}, {}, frozenset(), {}, {})
        self.assertEqual(env.bound_sources, {})
        access = AccessLog()
        with self.assertRaises(EvalBlocked) as ctx:
            evaluate(
                {"op": "bound_sources", "name": "demo.allocation.amount"},
                env,
                access,
            )
        self.assertEqual(ctx.exception.category, BLOCK_ABSENT)

    def test_pairing_five_positional_helper_still_constructs(self) -> None:
        # pairing_consequences.py 232: Environment(symbols, {}, frozenset(), parameters, canon)
        env = _pairing_local_environment(
            type("Binding", (), {"left_value": 1, "right_value": 2})(),
            run=None,
        )
        self.assertEqual(env.bound_sources, {})

    def test_record_codes_and_current_schema_include_v9(self) -> None:
        self.assertEqual(CURRENT_RECORD_SCHEMA, "derivation-record.v9")
        self.assertIn("NOMINEE_ALLOCATIONS_EXCEED_REPORT", RECORD_CODES)


if __name__ == "__main__":
    unittest.main()
