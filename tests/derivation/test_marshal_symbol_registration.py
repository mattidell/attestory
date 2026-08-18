"""Track 4 Repair 2 regression: `marshal.py`'s hand-maintained
`rule-artifact`/`attachment-rule` version sets must match
`package_validation.py`'s registered sets exactly (ADR-0066 Track 2 legacy
demo-path fallback). If a version is under-registered here, a rule using
that version's declared-absence capability (a `when`/`value` reference
outside `requires`) passes content validation and then blocks at runtime
with a spurious `DEPENDENCY_ABSENT` instead of binding the value it names.

Exercises the real `marshal_run_context` production constructor over
projected record state — not `_rule_required_symbols` in isolation — so the
test proves the same code path a live run takes.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.marshal import marshal_run_context
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project
from tests.support import act, registry_with_demo_kinds


def _fact_type(identifier: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v1",
        "id": identifier,
        "title": f"Synthetic {identifier}",
        "nature": "determinable",
        "identity_keys": [{"name": "period", "kind": "literal", "values": ["2025"]}],
        "value_schema": {"type": "number"},
        "supersession": {"policy": "free"},
    }


class MarshalVersionRegistrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self._tmp.name))

    def _state_and_currency(self, symbol: str, value: Any) -> tuple[Any, Any]:
        acts = [
            act(0, "bundle-adoption", {"bundle": {
                "schema": "bundle.v1",
                "id": "demo.marshal-symbol-registration.bundle",
                "label": "Demo marshal symbol registration vocabulary",
                "fact_types": [_fact_type(symbol)],
            }}),
            act(1, "assertion", {"finding": {
                "schema": "finding.v1",
                "id": f"demo.finding.{symbol}",
                "fact_id": f"{symbol}|period=2025",
                "value": value,
                "basis": "attested",
                "evidence_ids": [],
            }}),
        ]
        state = project(tuple(acts), self.registry)
        currency = compute_currency(state)
        return state, currency

    def test_rule_artifact_v5_binds_a_ref_declared_outside_requires(self) -> None:
        # Defect 1: marshal.py:101 was missing "rule-artifact.v5" from the
        # set that walks `when`/`value` for declared-absence refs. Without
        # the fix, this symbol never reaches ctx.inputs and a v5 rule using
        # this capability blocks at runtime with DEPENDENCY_ABSENT instead
        # of binding the value.
        symbol = "demo.marshal-symbol-registration.outside-ref-v5"
        state, currency = self._state_and_currency(symbol, 42)
        rule = {
            "schema": "rule-artifact.v5",
            "id": "demo.rule.v5-outside-ref",
            "version": "v1",
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": {
                "op": "conditional_dependency_set",
                "condition": {"op": "literal", "arg": True},
                "members": [{"op": "ref", "name": symbol}],
            },
            "value": {"op": "ref", "name": symbol},
            "publishes": "demo.output.v5",
            "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [symbol]},
        }
        ctx = marshal_run_context(
            run_id="demo.run.marshal-v5",
            state=state,
            currency=currency,
            rules=[rule],
            parameters={},
            canon={},
            adoption_pin={"role": "adoption", "id": "demo.package", "version": "v1"},
            governance_pins=[],
        )
        self.assertEqual([i.symbol for i in ctx.inputs], [symbol])
        self.assertEqual(ctx.inputs[0].value, 42)

    def test_attachment_rule_v8_binds_a_required_answer_symbol(self) -> None:
        # Defect 1b: marshal.py:87/89's attachment-rule set stopped at v6,
        # missing "attachment-rule.v8" (Track 3's own new consumer schema).
        # Without the fix, a v8 attachment's required-answer symbol never
        # reaches ctx.inputs through this legacy fallback path.
        symbol = "demo.marshal-symbol-registration.required-answer-v8"
        state, currency = self._state_and_currency(symbol, 7)
        rule = {
            "schema": "attachment-rule.v8",
            "id": "demo.attachment.v8-required-answer",
            "version": "v1",
            "requirement": {"subtotals": []},
            "completeness": {
                "required_answers": [
                    {"symbol": symbol, "fact_type": {"id": symbol, "version": "v1"}, "check": "presence"}
                ]
            },
        }
        ctx = marshal_run_context(
            run_id="demo.run.marshal-v8",
            state=state,
            currency=currency,
            rules=[rule],
            parameters={},
            canon={},
            adoption_pin={"role": "adoption", "id": "demo.package", "version": "v1"},
            governance_pins=[],
        )
        self.assertEqual([i.symbol for i in ctx.inputs], [symbol])
        self.assertEqual(ctx.inputs[0].value, 7)


if __name__ == "__main__":
    unittest.main()
