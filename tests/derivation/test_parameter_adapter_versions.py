from __future__ import annotations

import unittest
from typing import Any

from packages.derivation.evaluator import Environment, parameter_exact, parameter_unversioned
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.runner import RunContext, SourceFact, _Run
from packages.derivation.runners.derive import _context
from packages.derivation.runner import run
from packages.tax.pairing_consequences import (
    SUPPORTABILITY_TYPE,
    _evaluate_one_factory,
    _pairing_local_environment,
    supportability_by_pairing_fact_id,
)
from packages.tax.identity_association import ACQUISITION_FACT_TYPE, REPORT_FACT_TYPE
from packages.derivation.pairing_dispatch import PairingBinding


PARAMETER_ID = "demo.parameter.adapter-version"


def _parameter(version: str, value: str) -> dict[str, Any]:
    return {
        "schema": "parameter-declaration.v1",
        "id": PARAMETER_ID,
        "version": version,
        "values": value,
    }


def _context_scenario(
    parameters: list[dict[str, Any]],
    *,
    rules: list[dict[str, Any]] | None = None,
    fact_types: list[dict[str, Any]] | None = None,
    input_bindings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "run_id": "demo.adapter-version-run",
        "rules": rules or [],
        "parameters": parameters,
        "inputs": [],
        "sources": [],
        "adoption_pin": {"role": "adoption", "id": "demo.package", "version": "v1"},
        "governance_pins": [],
        "fact_types": fact_types or [],
        "input_bindings": input_bindings or [],
    }


class ParameterAdapterVersions(unittest.TestCase):
    def test_fixture_context_preserves_both_versions_in_both_orders(self) -> None:
        for parameters in (
            [_parameter("v1", "1"), _parameter("v2", "2")],
            [_parameter("v2", "2"), _parameter("v1", "1")],
        ):
            with self.subTest(versions=[item["version"] for item in parameters]):
                ctx = _context(_context_scenario(parameters))
                self.assertEqual(
                    parameter_exact(ctx.parameters, PARAMETER_ID, "v1", ctx.parameter_index),
                    _parameter("v1", "1"),
                )
                self.assertEqual(
                    parameter_exact(ctx.parameters, PARAMETER_ID, "v2", ctx.parameter_index),
                    _parameter("v2", "2"),
                )
                self.assertIsNone(
                    parameter_exact(ctx.parameters, PARAMETER_ID, "v3", ctx.parameter_index)
                )
                self.assertIsNone(
                    parameter_unversioned(ctx.parameters, PARAMETER_ID, ctx.parameter_index)
                )

    def test_pairing_environment_transports_index_and_blocks_ambiguous_parameter(self) -> None:
        pairing = SourceFact("demo.pairing", "{}", "demo.finding.pairing", "demo.fact.pairing")
        left = SourceFact("demo.left", "1", "demo.finding.left", "demo.fact.left")
        right = SourceFact("demo.right", "1", "demo.finding.right", "demo.fact.right")
        binding = PairingBinding(
            pairing=pairing,
            pairing_value={"left_fact_id": "demo.fact.left", "right_fact_id": "demo.fact.right"},
            left=left,
            right=right,
            left_value="1",
            right_value="1",
        )
        for parameters in (
            [_parameter("v1", "1"), _parameter("v2", "2")],
            [_parameter("v2", "2"), _parameter("v1", "1")],
        ):
            with self.subTest(versions=[item["version"] for item in parameters]):
                fixture_ctx = _context(_context_scenario(parameters))
                run_ctx = RunContext(
                    run_id=fixture_ctx.run_id,
                    rules=[],
                    parameters=fixture_ctx.parameters,
                    canon=load_canon(DerivationSchemas()),
                    inputs=[],
                    sources=[],
                    adoption_pin=fixture_ctx.adoption_pin,
                    governance_pins=[],
                    parameter_index=fixture_ctx.parameter_index,
                )
                run = _Run(run_ctx, DerivationSchemas())
                env = _pairing_local_environment(binding, run=run)
                self.assertEqual(
                    parameter_exact(env.parameters, PARAMETER_ID, "v2", env.parameter_index),
                    _parameter("v2", "2"),
                )
                self.assertIsNone(parameter_exact(env.parameters, PARAMETER_ID, "v3", env.parameter_index))
                self.assertIsNone(parameter_unversioned(env.parameters, PARAMETER_ID, env.parameter_index))
                self.assertEqual(env.sources, {})
                self.assertEqual(set(env.symbols), {ACQUISITION_FACT_TYPE, REPORT_FACT_TYPE})
                supportability = SourceFact(
                    SUPPORTABILITY_TYPE, "true", "demo.finding.supportable",
                    binding.pairing_fact_id,
                )
                evaluate_one = _evaluate_one_factory(
                    supportability_by_pairing_fact_id([supportability]),
                    value_expr={"op": "parameter", "parameter_id": PARAMETER_ID},
                    run=run,
                )
                outcome = evaluate_one(binding)
                self.assertEqual(getattr(outcome, "code", None), "DEPENDENCY_INVALID")
                self.assertFalse(
                    any(pin.get("role") == "parameter" for pin in getattr(outcome, "extra_pins", ()))
                )

    def test_pairing_factory_reads_and_pins_single_version_parameter(self) -> None:
        pairing = SourceFact("demo.pairing", "{}", "demo.finding.pairing", "demo.fact.pairing")
        left = SourceFact("demo.left", "1", "demo.finding.left", "demo.fact.left")
        right = SourceFact("demo.right", "1", "demo.finding.right", "demo.fact.right")
        binding = PairingBinding(
            pairing=pairing,
            pairing_value={"left_fact_id": "demo.fact.left", "right_fact_id": "demo.fact.right"},
            left=left,
            right=right,
            left_value="1",
            right_value="1",
        )
        fixture_ctx = _context(_context_scenario([_parameter("v1", "1")]))
        run = _Run(
            RunContext(
                run_id=fixture_ctx.run_id,
                rules=[],
                parameters=fixture_ctx.parameters,
                canon=load_canon(DerivationSchemas()),
                inputs=[],
                sources=[],
                adoption_pin=fixture_ctx.adoption_pin,
                governance_pins=[],
                parameter_index=fixture_ctx.parameter_index,
            ),
            DerivationSchemas(),
        )
        supportability = SourceFact(
            SUPPORTABILITY_TYPE, "true", "demo.finding.supportable", binding.pairing_fact_id,
        )
        outcome = _evaluate_one_factory(
            supportability_by_pairing_fact_id([supportability]),
            value_expr={"op": "parameter", "parameter_id": PARAMETER_ID},
            run=run,
        )(binding)
        self.assertEqual(getattr(outcome, "value", None), "1")
        self.assertIn(
            {"role": "parameter", "id": PARAMETER_ID, "version": "v1"},
            getattr(outcome, "extra_pins", ()),
        )

    def test_hand_built_environment_and_single_version_fixture_remain_supported(self) -> None:
        citizen = _parameter("v1", "1")
        env = Environment({}, {}, frozenset(), {PARAMETER_ID: citizen}, {})
        self.assertEqual(parameter_exact(env.parameters, PARAMETER_ID, "v1", env.parameter_index), citizen)
        ctx = _context(_context_scenario([citizen]))
        self.assertEqual(ctx.parameters[PARAMETER_ID], citizen)
        self.assertEqual(ctx.parameter_index[PARAMETER_ID], {"v1": citizen})

    def test_fixture_runner_reads_and_pins_exact_optional_default_both_orders(self) -> None:
        fact_id = "demo.fact.fixture-parameter"
        echo_id = "demo.fact.fixture-parameter-echo"
        rule = {
            "schema": "rule-artifact.v6",
            "id": "demo.rule.fixture-parameter-echo",
            "version": "v1",
            "role": "computation",
            "requires": [fact_id],
            "pins": [],
            "when": True,
            "value": {"op": "ref", "name": fact_id},
            "publishes": echo_id,
            "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        }
        fact_type = {
            "schema": "fact-type.v2",
            "id": fact_id,
            "version": "v1",
            "value_schema": {"type": "string"},
            "optional_default": {
                "parameter": {"id": PARAMETER_ID, "version": "v1"},
            },
        }
        binding = {
            "symbol": fact_id,
            "fact_type": {"id": fact_id, "version": "v1"},
            "mode": "optional_default",
        }
        for parameters in (
            [_parameter("v1", "from-v1"), _parameter("v2", "from-v2")],
            [_parameter("v2", "from-v2"), _parameter("v1", "from-v1")],
        ):
            with self.subTest(versions=[item["version"] for item in parameters]):
                ctx = _context(
                    _context_scenario(
                        parameters,
                        rules=[rule],
                        fact_types=[fact_type],
                        input_bindings=[binding],
                    )
                )
                result = run(ctx, DerivationSchemas())
                finding = next(
                    pub.finding for pub in result.publications if pub.finding["symbol"] == echo_id
                )
                self.assertEqual(finding["value"], "from-v1")
                default_pin = next(
                    pin for pin in finding["pins"]
                    if pin.get("origin") == "declared_default"
                )
                default_finding = next(
                    pub.finding for pub in result.publications
                    if pub.finding["id"] == default_pin["id"]
                )
                self.assertEqual(default_finding["value"], "from-v1")
                self.assertIn(
                    {"role": "parameter", "id": PARAMETER_ID, "version": "v1"},
                    default_finding["pins"],
                )
                self.assertNotIn(
                    {"role": "parameter", "id": PARAMETER_ID, "version": "v2"},
                    default_finding["pins"],
                )

    def test_fixture_runner_does_not_select_ambiguous_unversioned_parameter(self) -> None:
        echo_id = "demo.fact.fixture-parameter-unversioned"
        rule = {
            "schema": "rule-artifact.v6",
            "id": "demo.rule.fixture-parameter-unversioned",
            "version": "v1",
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": True,
            "value": {"op": "parameter", "parameter_id": PARAMETER_ID},
            "publishes": echo_id,
            "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        }
        ctx = _context(
            _context_scenario(
                [_parameter("v1", "1"), _parameter("v2", "2")],
                rules=[rule],
            )
        )
        result = run(ctx, DerivationSchemas())
        self.assertFalse(any(pub.finding["symbol"] == echo_id for pub in result.publications))
        self.assertTrue(
            any(row.get("artifact_id") == rule["id"] and row.get("code") == "DEPENDENCY_INVALID" for row in result.dispositions),
            result.dispositions,
        )


if __name__ == "__main__":
    unittest.main()
