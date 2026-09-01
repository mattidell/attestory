"""Environment and explanation wiring for standing authorization (ADR-0069)."""

from __future__ import annotations

import unittest
from decimal import Decimal

from packages.derivation.authorization import (
    STATUS_ADMITTED,
    STATUS_SUSPENDED,
    AuthorizationResolution,
    authorization_provenance,
    bind_authorization,
    project,
    resolve,
)
from packages.derivation.authorization_closure import package_boundary_digest
from packages.derivation.evaluator import AccessLog, Environment, evaluate
from packages.derivation.explanation import explain
from packages.derivation.loader import DerivationSchemas
from packages.derivation.runner import InputFinding, RunContext, SourceFact, _Run
from tests.derivation.test_authorization_closure import ROOT, _corpus
from tests.derivation.test_authorization_fold import _end, _grant


def _env(authorization: AuthorizationResolution | None = None) -> Environment:
    return Environment(
        symbols={"demo.scale.convention": "half_up"},
        sources={"demo.fact.ordinary": ["10"]},
        closed_sets=frozenset({"demo.family.ordinary"}),
        parameters={},
        canon={},
        authorization=authorization,
    )


class EnvironmentWiring(unittest.TestCase):
    def test_evaluate_does_not_consult_authorization(self) -> None:
        suspended = AuthorizationResolution(STATUS_SUSPENDED, "demo.auth.g1")
        env = _env(suspended)
        result = evaluate({"op": "add", "args": ["1", "2"]}, env, AccessLog())
        self.assertEqual(result, Decimal("3"))
        self.assertIs(env.authorization, suspended)
        self.assertFalse(suspended.admitted)

    def test_bind_authorization_replaces_disposition(self) -> None:
        env = _env()
        self.assertIsNone(env.authorization)
        admitted = AuthorizationResolution(STATUS_ADMITTED, "demo.auth.g1")
        bound = bind_authorization(env, admitted)
        self.assertEqual(bound.authorization, admitted)
        self.assertIsNone(env.authorization)

    def test_runner_env_exposes_run_context_authorization(self) -> None:
        admitted = AuthorizationResolution(STATUS_ADMITTED, "demo.auth.g1")
        ctx = RunContext(
            run_id="demo.run.1",
            rules=[],
            parameters={},
            canon={},
            inputs=[InputFinding("demo.scale.convention", "half_up", "demo.f.scale", "input")],
            sources=[SourceFact("demo.fact.ordinary", "10", "demo.f.ordinary")],
            adoption_pin={"role": "adoption", "id": "demo.package", "version": "v1"},
            governance_pins=[{"role": "governance", "id": "demo.gov", "version": "v1"}],
            authorization=admitted,
        )
        env = _Run(ctx, DerivationSchemas()).env()
        self.assertEqual(env.authorization, admitted)


class ExplanationProvenance(unittest.TestCase):
    def test_provenance_helper_and_explain_child(self) -> None:
        corpus = _corpus()
        universe = package_boundary_digest(ROOT, corpus)
        resolution = resolve(
            project((_grant("demo.auth.g1", "demo.subject.a", "2025", universe),)),
            "demo.subject.a",
            "2025",
            universe,
        )
        payload = authorization_provenance(resolution)
        self.assertEqual(payload["kind"], "authorization")
        self.assertEqual(payload["status"], STATUS_ADMITTED)
        self.assertTrue(payload["admitted"])
        self.assertEqual(payload["grant_id"], "demo.auth.g1")

        derived = {
            "demo.finding.output": {
                "id": "demo.finding.output",
                "symbol": "demo.ordinary.subtotal",
                "value": "10",
                "version": "v2",
                "pins": [
                    {"role": "computation", "id": "demo.rule.ordinary-subtotal", "version": "v1"},
                    {"role": "input", "id": "demo.finding.input", "version": "v1", "origin": "assertion"},
                ],
            }
        }
        node = explain(
            "demo.finding.output",
            role="output",
            derived=derived,
            authorization=resolution,
        )
        auth_children = [child for child in node.children if child.role == "authorization"]
        self.assertEqual(len(auth_children), 1)
        self.assertEqual(auth_children[0].kind, "authorization")
        self.assertEqual(auth_children[0].value, STATUS_ADMITTED)
        self.assertEqual(auth_children[0].finding_id, "demo.auth.g1")

        nested_auth = [
            grandchild
            for child in node.children
            for grandchild in child.children
            if grandchild.role == "authorization"
        ]
        self.assertEqual(nested_auth, [])

    def test_explain_without_authorization_is_unchanged(self) -> None:
        derived = {
            "demo.finding.output": {
                "id": "demo.finding.output",
                "symbol": "demo.ordinary.subtotal",
                "value": "10",
                "version": "v2",
                "pins": [{"role": "computation", "id": "demo.rule.ordinary-subtotal", "version": "v1"}],
            }
        }
        node = explain("demo.finding.output", role="output", derived=derived)
        self.assertFalse(any(child.role == "authorization" for child in node.children))


class SuspendedProvenance(unittest.TestCase):
    def test_suspended_disposition_reaches_explanation(self) -> None:
        corpus = _corpus()
        universe = package_boundary_digest(ROOT, corpus)
        resolution = resolve(
            project(
                (
                    _grant("demo.auth.g1", "demo.subject.a", "2025", universe),
                    _end("demo.auth.g1", "suspend"),
                )
            ),
            "demo.subject.a",
            "2025",
            universe,
        )
        self.assertEqual(resolution.status, STATUS_SUSPENDED)
        derived = {
            "demo.finding.output": {
                "id": "demo.finding.output",
                "symbol": "demo.ordinary.subtotal",
                "value": "10",
                "version": "v2",
                "pins": [{"role": "computation", "id": "demo.rule.ordinary-subtotal", "version": "v1"}],
            }
        }
        node = explain(
            "demo.finding.output",
            role="output",
            derived=derived,
            authorization=resolution,
        )
        auth = next(child for child in node.children if child.role == "authorization")
        self.assertEqual(auth.value, STATUS_SUSPENDED)


if __name__ == "__main__":
    unittest.main()
