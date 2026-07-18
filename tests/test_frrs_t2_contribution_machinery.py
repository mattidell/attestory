"""Track 2 — Contribution Machinery (ADR-0032 / D2).

Synthetic in-repo fixtures only. Implements and kill-tests:
- contribution applicator + finding.v2 provenance admission
- contribution-record.v1 Article-14 process account
- runs-consume-facts MUST: run-request ≠ RunContext, marshal-only constructor,
  live-entrypoint reachability kill-test (7770000 ghost-id bypass closed)
- E14.2 static check (contribution not a rule dependency)
- negative goldens: any-order, correction-by-supersession, SC-R2
"""

from __future__ import annotations

import inspect
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.live import (
    RUN_REQUEST_SCHEMA,
    live_entrypoint_accepts_raw_inputs,
    live_run,
    validate_run_request,
)
from packages.derivation.loader import DerivationSchemas, load_canon, workspace_registry
from packages.derivation.marshal import marshal_run_context
from packages.derivation.package_validation import validate_package
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from packages.derivation.runners import derive as derive_fixture
from packages.kernel.act_log import ActLog
from packages.kernel.contribution import (
    ContributionError,
    apply_contribution_batch,
    started_contribution_record,
    terminal_contribution_record,
    validate_contribution_record,
)
from packages.kernel.currency import compute_currency
from packages.kernel.findings import FindingModelError, FindingState, apply_act, project
from packages.kernel.schema_registry import SchemaValidationError
from tests.support import act, demo_entity, demo_evidence, registry_with_demo_kinds


def _demo_bundle_w2() -> dict[str, Any]:
    return {
        "schema": "bundle.v1",
        "id": "demo.vocabulary.w2",
        "label": "Demo W-2 vocabulary (synthetic)",
        "fact_types": [
            {
                "schema": "fact-type.v1",
                "id": "demo.w2.box1",
                "title": "W-2 box 1 wages (synthetic)",
                "nature": "determinable",
                "identity_keys": [
                    {
                        "name": "employer",
                        "kind": "entity",
                        "entity_kind": "demo.employer",
                    },
                    {"name": "period", "kind": "literal", "values": ["2025"]},
                ],
                "value_schema": {"type": "number"},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v1",
                "id": "demo.interest.box1",
                "title": "1099-INT box 1 interest (synthetic)",
                "nature": "determinable",
                "identity_keys": [
                    {
                        "name": "payer",
                        "kind": "entity",
                        "entity_kind": "demo.payer",
                    },
                    {"name": "period", "kind": "literal", "values": ["2025"]},
                ],
                "value_schema": {"type": "number"},
                "supersession": {"policy": "free"},
            },
        ],
    }


def _fact_id(fact_type: str, key_name: str, entity_id: str) -> str:
    return f"{fact_type}|{key_name}={entity_id},period=2025"


def _finding_v2(
    finding_id: str,
    fact_id: str,
    value: Any,
    *,
    evidence_ids: list[str],
    contribution_id: str,
) -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "documentary",
        "evidence_ids": evidence_ids,
        "contribution_id": contribution_id,
    }


def _contribution(contribution_id: str, evidence_id: str) -> dict[str, Any]:
    return {
        "schema": "contribution.v1",
        "id": contribution_id,
        "evidence_id": evidence_id,
        "content": {"mode": "manual-entry", "synthetic": True},
    }


class ContributionMachineryFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self._tmp.name))
        self.schemas = DerivationSchemas()
        self.workspace_registry = workspace_registry()

    def opening_acts(self) -> list[dict[str, Any]]:
        return [
            act(0, "bundle-adoption", {"bundle": _demo_bundle_w2()}),
            act(
                1,
                "entity-introduced",
                {"entity": demo_entity("demo.employer-alpha", "Employer Alpha", "demo.employer")},
            ),
            act(
                2,
                "entity-introduced",
                {"entity": demo_entity("demo.payer-bank", "Bank Beta", "demo.payer")},
            ),
            act(
                3,
                "evidence-submitted",
                {
                    "evidence": demo_evidence(
                        "demo.evidence.w2-a", "Synthetic W-2", {"box1": 52000}
                    )
                },
            ),
            act(
                4,
                "evidence-submitted",
                {
                    "evidence": demo_evidence(
                        "demo.evidence.int-a", "Synthetic 1099-INT", {"box1": 120}
                    )
                },
            ),
        ]


class TestContributionApplicator(ContributionMachineryFixture):
    def test_batch_produces_finding_v2_with_contribution_provenance(self) -> None:
        base = project(tuple(self.opening_acts()), self.registry)
        contribution_id = "demo.contribution.w2-a"
        evidence_id = "demo.evidence.w2-a"
        finding_id = "demo.finding.w2-box1-a"
        fact_id = _fact_id("demo.w2.box1", "employer", "demo.employer-alpha")

        contribution_act = act(
            5,
            "contribution",
            {"contribution": _contribution(contribution_id, evidence_id)},
        )
        assertion_act = act(
            6,
            "assertion",
            {
                "finding": _finding_v2(
                    finding_id,
                    fact_id,
                    52000,
                    evidence_ids=[evidence_id],
                    contribution_id=contribution_id,
                )
            },
        )
        result = apply_contribution_batch(
            base,
            contribution_act=contribution_act,
            successor_acts=[assertion_act],
            registry=self.registry,
            record_id="demo.crec.w2-a",
        )
        finding = result.state.findings[finding_id]
        self.assertEqual(finding["schema"], "finding.v2")
        self.assertEqual(finding["contribution_id"], contribution_id)
        self.assertIn(evidence_id, finding["evidence_ids"])
        self.assertNotIn("pins", finding)
        # Contribution pin is provenance-only: absent from pins.finding_ids.
        self.assertEqual(
            self.registry.get("finding.v2")["properties"]["contribution_id"]["type"],
            "string",
        )
        self.assertIn(contribution_id, result.state.contributions)
        self.assertEqual(result.terminal_record["phase"], "completed")
        self.assertEqual(result.terminal_record["stop_reason"], "completed")
        self.assertEqual(len(result.asserted), 1)

    def test_admission_rejects_contribution_evidence_not_in_finding_evidence_ids(
        self,
    ) -> None:
        base = project(tuple(self.opening_acts()), self.registry)
        contribution_act = act(
            5,
            "contribution",
            {
                "contribution": _contribution(
                    "demo.contribution.w2-a", "demo.evidence.w2-a"
                )
            },
        )
        bad_assertion = act(
            6,
            "assertion",
            {
                "finding": _finding_v2(
                    "demo.finding.bad",
                    _fact_id("demo.w2.box1", "employer", "demo.employer-alpha"),
                    52000,
                    # Evidence from a different document than the contribution.
                    evidence_ids=["demo.evidence.int-a"],
                    contribution_id="demo.contribution.w2-a",
                )
            },
        )
        with self.assertRaises(ContributionError) as ctx:
            apply_contribution_batch(
                base,
                contribution_act=contribution_act,
                successor_acts=[bad_assertion],
                registry=self.registry,
                record_id="demo.crec.bad",
            )
        self.assertIn("not a member of evidence_ids", str(ctx.exception))

    def test_act_log_admits_v2_assertion_payload(self) -> None:
        log = ActLog(Path(self._tmp.name) / "ws", self.workspace_registry)
        # Minimal valid acts through log: only contribution-related payload check.
        opening = self.opening_acts()
        for i, a in enumerate(opening):
            log.append(a, expected_revision=i)
        contribution_act = act(
            5,
            "contribution",
            {
                "contribution": _contribution(
                    "demo.contribution.w2-a", "demo.evidence.w2-a"
                )
            },
        )
        log.append(contribution_act, expected_revision=5)
        assertion_act = act(
            6,
            "assertion",
            {
                "finding": _finding_v2(
                    "demo.finding.w2-box1-a",
                    _fact_id("demo.w2.box1", "employer", "demo.employer-alpha"),
                    52000,
                    evidence_ids=["demo.evidence.w2-a"],
                    contribution_id="demo.contribution.w2-a",
                )
            },
        )
        log.append(assertion_act, expected_revision=6)
        contents = log.read()
        self.assertEqual(contents.revision, 7)
        self.assertEqual(contents.acts[-1]["payload"]["finding"]["schema"], "finding.v2")


class TestContributionRecord(ContributionMachineryFixture):
    def test_started_and_terminal_records_admit(self) -> None:
        started = started_contribution_record(
            record_id="demo.crec.1.started",
            contribution_id="demo.contribution.w2-a",
            workspace_revision=5,
        )
        validate_contribution_record(started, self.registry)
        self.workspace_registry.validate("contribution-record.v1", started)

        terminal = terminal_contribution_record(
            record_id="demo.crec.1.terminal",
            contribution_id="demo.contribution.w2-a",
            workspace_revision=7,
            phase="completed",
            stop_reason="completed",
            facts_asserted=[
                {
                    "fact_id": _fact_id(
                        "demo.w2.box1", "employer", "demo.employer-alpha"
                    ),
                    "finding_id": "demo.finding.w2-box1-a",
                    "act_id": "demo-act-006",
                }
            ],
        )
        validate_contribution_record(terminal, self.registry)
        self.workspace_registry.validate("contribution-record.v1", terminal)

    def test_started_record_rejects_terminal_fields(self) -> None:
        bad = {
            "schema": "contribution-record.v1",
            "record_id": "demo.crec.bad",
            "contribution_id": "demo.contribution.w2-a",
            "phase": "started",
            "workspace_revision": 0,
            "stop_reason": "completed",
        }
        with self.assertRaises(SchemaValidationError):
            validate_contribution_record(bad, self.registry)


class TestRunsConsumeFacts(ContributionMachineryFixture):
    def test_run_request_is_not_run_context(self) -> None:
        request = {"schema": RUN_REQUEST_SCHEMA}
        validate_run_request(request, self.schemas)
        # Distinct types / shapes: closing the request does not close RunContext.
        self.assertNotEqual(RUN_REQUEST_SCHEMA, "RunContext")
        self.assertTrue(hasattr(RunContext, "__dataclass_fields__"))
        request_fields = set(request)
        context_fields = set(RunContext.__dataclass_fields__)
        self.assertNotEqual(request_fields, context_fields)
        # Closed request admits no value-bearing member.
        with self.assertRaises(SchemaValidationError):
            validate_run_request(
                {"schema": RUN_REQUEST_SCHEMA, "inputs": [{"value": 7770000}]},
                self.schemas,
            )

    def test_marshal_only_constructor_builds_from_record_state(self) -> None:
        base = project(tuple(self.opening_acts()), self.registry)
        contribution_id = "demo.contribution.w2-a"
        result = apply_contribution_batch(
            base,
            contribution_act=act(
                5,
                "contribution",
                {
                    "contribution": _contribution(
                        contribution_id, "demo.evidence.w2-a"
                    )
                },
            ),
            successor_acts=[
                act(
                    6,
                    "assertion",
                    {
                        "finding": _finding_v2(
                            "demo.finding.w2-box1-a",
                            _fact_id(
                                "demo.w2.box1", "employer", "demo.employer-alpha"
                            ),
                            52000,
                            evidence_ids=["demo.evidence.w2-a"],
                            contribution_id=contribution_id,
                        )
                    },
                )
            ],
            registry=self.registry,
            record_id="demo.crec.marshal",
        )
        currency = compute_currency(result.state)
        ctx = marshal_run_context(
            run_id="demo.run.marshal",
            state=result.state,
            currency=currency,
            rules=[
                {
                    "schema": "rule-artifact.v1",
                    "id": "demo.rule.passthrough",
                    "version": "v1",
                    "role": "computation",
                    "requires": ["demo.w2.box1"],
                    "pins": [],
                    "when": True,
                    "value": {"op": "ref", "name": "demo.w2.box1"},
                    "publishes": "demo.form.line1a",
                    "blocked": {"code": "DEPENDENCY_ABSENT", "missing": ["demo.w2.box1"]},
                }
            ],
            parameters={},
            canon=load_canon(self.schemas),
            adoption_pin={
                "role": "adoption",
                "id": "demo.package.t2",
                "version": "v1",
            },
            governance_pins=[
                {"role": "governance", "id": "governance.constitution", "version": "v1"}
            ],
        )
        self.assertIsInstance(ctx, RunContext)
        self.assertEqual(len(ctx.inputs), 1)
        self.assertEqual(ctx.inputs[0].finding_id, "demo.finding.w2-box1-a")
        self.assertEqual(ctx.inputs[0].value, 52000)
        # Constructor signature has no inputs=/sources= injection surface.
        sig = inspect.signature(marshal_run_context)
        self.assertNotIn("inputs", sig.parameters)
        self.assertNotIn("sources", sig.parameters)

    def test_kill_test_hand_assembled_input_unreachable_from_live_run(self) -> None:
        """ADR-0032 Decision 3 kill-test: the 7770000 ghost-id bypass fails.

        The adversary published 7770000 via directly-constructed RunContext /
        InputFinding. The live entrypoint must make that path structurally
        unreachable — not merely policy-discouraged.
        """
        # Structural: live_run accepts no raw-input parameters.
        self.assertFalse(live_entrypoint_accepts_raw_inputs())
        sig = inspect.signature(live_run)
        for forbidden in ("inputs", "sources", "raw_inputs", "scenario"):
            self.assertNotIn(forbidden, sig.parameters)

        # Attempt the adversary construction against the live entrypoint.
        ghost_inputs = [
            InputFinding(
                symbol="demo.w2.box1",
                value=7770000,
                finding_id="GHOST-w2-in-no-record",
                role="input",
            )
        ]
        with self.assertRaises(TypeError):
            live_run(  # type: ignore[call-arg]
                {"schema": RUN_REQUEST_SCHEMA},
                run_id="demo.run.attack",
                state=FindingState(),
                currency=compute_currency(FindingState()),
                rules=[],
                parameters={},
                canon={},
                adoption_pin={"role": "adoption", "id": "demo.pkg", "version": "v1"},
                governance_pins=[],
                schemas=self.schemas,
                inputs=ghost_inputs,
            )

        # Fixture adapter path still exists (production-fenced) and can assemble
        # raw inputs — that is intentional and must not be reachable from live.
        self.assertTrue(derive_fixture.FIXTURE_ADAPTER_ONLY)
        fixture_ctx = derive_fixture._context(
            {
                "run_id": "demo.run.fixture-ghost",
                "rules": [],
                "parameters": [],
                "inputs": [
                    {
                        "symbol": "demo.w2.box1",
                        "value": 7770000,
                        "finding_id": "GHOST-w2-in-no-record",
                        "role": "input",
                    }
                ],
                "sources": [
                    {
                        "name": "demo.w2.box1",
                        "value": "7770000",
                        "finding_id": "GHOST-source",
                    }
                ],
                "adoption_pin": {
                    "role": "adoption",
                    "id": "demo.pkg",
                    "version": "v1",
                },
                "governance_pins": [
                    {
                        "role": "governance",
                        "id": "governance.constitution",
                        "version": "v1",
                    }
                ],
            }
        )
        self.assertEqual(fixture_ctx.inputs[0].value, 7770000)

        # Live path over empty record state yields no ghost value in context.
        live_ctx = marshal_run_context(
            run_id="demo.run.live-empty",
            state=FindingState(),
            currency=compute_currency(FindingState()),
            rules=[],
            parameters={},
            canon={},
            adoption_pin={"role": "adoption", "id": "demo.pkg", "version": "v1"},
            governance_pins=[],
        )
        self.assertEqual(live_ctx.inputs, [])
        self.assertEqual(live_ctx.sources, [])
        self.assertNotIn(7770000, [i.value for i in live_ctx.inputs])


class TestE142ContributionDependency(ContributionMachineryFixture):
    def test_package_validation_rejects_contribution_member(self) -> None:
        """Executed golden: a package member that is a contribution is rejected."""
        package = {
            "schema": "artifact-package.v1",
            "id": "demo.package.e142",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "demo",
            },
            "members": [
                {
                    "role": "parameter",
                    "id": "demo.contribution.as-dep",
                    "version": "v1",
                }
            ],
        }
        corpus: dict[tuple[str, str], dict[str, Any]] = {
            ("demo.contribution.as-dep", "v1"): {
                "schema": "contribution.v1",
                "id": "demo.contribution.as-dep",
                "evidence_id": "demo.evidence.w2-a",
                "content": {},
            }
        }
        result = validate_package(package, corpus, self.schemas)
        self.assertFalse(result.ok)
        codes = {issue.code for issue in result.issues}
        self.assertIn(
            "E14_2_FORBIDDEN_DEPENDENCY",
            codes,
            msg=f"expected E14.2 rejection, got: {result.issues}",
        )

    def test_package_validation_rejects_rule_pin_to_contribution(self) -> None:
        """Executed golden: a rule pin naming a contribution is rejected."""
        rule: dict[str, Any] = {
            "schema": "rule-artifact.v2",
            "id": "demo.rule.with-contribution-dep",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "demo",
            },
            "role": "computation",
            "requires": ["demo.w2.box1"],
            "pins": [
                {
                    "role": "input",
                    "id": "demo.contribution.as-dep",
                    "version": "v1",
                    "origin": "assertion",
                }
            ],
            "when": True,
            "value": {"op": "ref", "name": "demo.w2.box1"},
            "publishes": "demo.form.line1a",
            "blocked": {"code": "DEPENDENCY_ABSENT", "missing": ["demo.w2.box1"]},
        }
        package = {
            "schema": "artifact-package.v2",
            "id": "demo.package.e142-pin",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "demo",
            },
            "admitted_schemas": ["rule-artifact.v2"],
            "members": [
                {
                    "role": "computation",
                    "schema": "rule-artifact.v2",
                    "id": "demo.rule.with-contribution-dep",
                    "version": "v1",
                }
            ],
            "input_bindings": [],
            "entrypoints": [
                {"id": "demo.rule.with-contribution-dep", "version": "v1"}
            ],
            "composition_obligations": [],
            "package_checksum": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
        }
        corpus: dict[tuple[str, str], dict[str, Any]] = {
            ("demo.rule.with-contribution-dep", "v1"): rule,
            # Contribution is in the corpus so the pin target resolves, but is
            # not a package member — only the pin-target E14.2 path fires.
            ("demo.contribution.as-dep", "v1"): {
                "schema": "contribution.v1",
                "id": "demo.contribution.as-dep",
                "evidence_id": "demo.evidence.w2-a",
                "content": {},
            },
        }
        result = validate_package(package, corpus, self.schemas)
        self.assertFalse(result.ok)
        pin_issues = [
            i for i in result.issues if i.code == "E14_2_FORBIDDEN_DEPENDENCY"
        ]
        self.assertTrue(
            pin_issues,
            msg=f"expected pin-target E14.2 rejection, got: {result.issues}",
        )
        self.assertTrue(
            any("rule pin" in i.detail for i in pin_issues),
            msg=f"expected rule-pin detail, got: {pin_issues}",
        )


class TestAnyOrderEquivalence(ContributionMachineryFixture):
    def _apply_w2(self, state: FindingState, index: int) -> FindingState:
        cid = "demo.contribution.w2-a"
        eid = "demo.evidence.w2-a"
        return apply_contribution_batch(
            state,
            contribution_act=act(
                index,
                "contribution",
                {"contribution": _contribution(cid, eid)},
            ),
            successor_acts=[
                act(
                    index + 1,
                    "assertion",
                    {
                        "finding": _finding_v2(
                            "demo.finding.w2-box1-a",
                            _fact_id(
                                "demo.w2.box1", "employer", "demo.employer-alpha"
                            ),
                            52000,
                            evidence_ids=[eid],
                            contribution_id=cid,
                        )
                    },
                )
            ],
            registry=self.registry,
            record_id="demo.crec.w2",
            workspace_revision=index,
        ).state

    def _apply_int(self, state: FindingState, index: int) -> FindingState:
        cid = "demo.contribution.int-a"
        eid = "demo.evidence.int-a"
        return apply_contribution_batch(
            state,
            contribution_act=act(
                index,
                "contribution",
                {"contribution": _contribution(cid, eid)},
            ),
            successor_acts=[
                act(
                    index + 1,
                    "assertion",
                    {
                        "finding": _finding_v2(
                            "demo.finding.int-box1-a",
                            _fact_id("demo.interest.box1", "payer", "demo.payer-bank"),
                            120,
                            evidence_ids=[eid],
                            contribution_id=cid,
                        )
                    },
                )
            ],
            registry=self.registry,
            record_id="demo.crec.int",
            workspace_revision=index,
        ).state

    def test_independent_batches_commute(self) -> None:
        base = project(tuple(self.opening_acts()), self.registry)
        # Order A: W-2 then 1099-INT
        a = self._apply_int(self._apply_w2(base, 5), 7)
        # Order B: 1099-INT then W-2
        b = self._apply_w2(self._apply_int(base, 5), 7)

        currency_a = compute_currency(a)
        currency_b = compute_currency(b)
        self.assertEqual(
            set(currency_a.current_finding_ids), set(currency_b.current_finding_ids)
        )
        current_values_a = {
            fid: a.findings[fid]["value"] for fid in currency_a.current_finding_ids
        }
        current_values_b = {
            fid: b.findings[fid]["value"] for fid in currency_b.current_finding_ids
        }
        self.assertEqual(current_values_a, current_values_b)
        self.assertEqual(set(a.contributions), set(b.contributions))
        self.assertEqual(
            {fid: a.findings[fid]["fact_id"] for fid in a.findings},
            {fid: b.findings[fid]["fact_id"] for fid in b.findings},
        )


class TestCorrectionBySupersession(ContributionMachineryFixture):
    def test_correction_supersedes_without_horizon_advance(self) -> None:
        base = project(tuple(self.opening_acts()), self.registry)
        fact_id = _fact_id("demo.w2.box1", "employer", "demo.employer-alpha")
        first = apply_contribution_batch(
            base,
            contribution_act=act(
                5,
                "contribution",
                {
                    "contribution": _contribution(
                        "demo.contribution.w2-a", "demo.evidence.w2-a"
                    )
                },
            ),
            successor_acts=[
                act(
                    6,
                    "assertion",
                    {
                        "finding": _finding_v2(
                            "demo.finding.w2-box1-a",
                            fact_id,
                            52000,
                            evidence_ids=["demo.evidence.w2-a"],
                            contribution_id="demo.contribution.w2-a",
                        )
                    },
                )
            ],
            registry=self.registry,
            record_id="demo.crec.first",
        )
        # Correcting contribution: new evidence + new contribution + plain assertion.
        state = first.state
        state = apply_act(
            state,
            act(
                7,
                "evidence-submitted",
                {
                    "evidence": demo_evidence(
                        "demo.evidence.w2-a-corr",
                        "Synthetic W-2 correction",
                        {"box1": 53000},
                    )
                },
            ),
            self.registry,
        )
        corrected = apply_contribution_batch(
            state,
            contribution_act=act(
                8,
                "contribution",
                {
                    "contribution": _contribution(
                        "demo.contribution.w2-a-corr", "demo.evidence.w2-a-corr"
                    )
                },
            ),
            successor_acts=[
                act(
                    9,
                    "assertion",
                    {
                        "finding": _finding_v2(
                            "demo.finding.w2-box1-a-corr",
                            fact_id,
                            53000,
                            evidence_ids=["demo.evidence.w2-a-corr"],
                            contribution_id="demo.contribution.w2-a-corr",
                        )
                    },
                )
            ],
            registry=self.registry,
            record_id="demo.crec.corr",
        )
        # Both findings remain on the record (no edit / withdrawal).
        self.assertIn("demo.finding.w2-box1-a", corrected.state.findings)
        self.assertIn("demo.finding.w2-box1-a-corr", corrected.state.findings)
        currency = compute_currency(corrected.state)
        self.assertIn("demo.finding.w2-box1-a-corr", currency.current_finding_ids)
        self.assertIn("demo.finding.w2-box1-a", currency.displaced_finding_ids)
        # Family horizon does not advance — no member-transition was used.
        self.assertEqual(corrected.state.horizon_state.current_by_chain, {})
        self.assertEqual(first.state.horizon_state.current_by_chain, {})


class TestSCR2SameMemberTransition(ContributionMachineryFixture):
    def test_same_member_correction_via_member_transition_rejects(self) -> None:
        """SC-R2: same-member value correction through member-transition rejects."""
        base_acts = self.opening_acts()
        # Horizon genesis + first member transition establishing membership.
        family = {"id": "demo.family.w2", "version": "v1"}
        scope = {"subject": "demo-subject", "tax-year": "2025"}
        # Register family member predicate so SC-R1 would also bind; for SC-R2
        # membership is established by a prior finding on the fact.
        self.registry.family_member_predicates.add("demo.w2.box1")

        state = project(tuple(base_acts), self.registry)
        state = apply_act(
            state,
            act(
                5,
                "horizon-genesis",
                {
                    "family": family,
                    "scope": scope,
                    "horizon_id": "demo.horizon.w2.h0",
                },
            ),
            self.registry,
        )
        # Contribution so finding.v2 may pin it.
        state = apply_act(
            state,
            act(
                6,
                "contribution",
                {
                    "contribution": _contribution(
                        "demo.contribution.w2-a", "demo.evidence.w2-a"
                    )
                },
            ),
            self.registry,
        )
        fact_id = _fact_id("demo.w2.box1", "employer", "demo.employer-alpha")
        state = apply_act(
            state,
            act(
                7,
                "member-transition",
                {
                    "family": family,
                    "scope": scope,
                    "member": {
                        "action": "assert",
                        "finding": _finding_v2(
                            "demo.finding.w2-box1-a",
                            fact_id,
                            52000,
                            evidence_ids=["demo.evidence.w2-a"],
                            contribution_id="demo.contribution.w2-a",
                        ),
                    },
                    "successor": {
                        "id": "demo.horizon.w2.h1",
                        "predecessor": "demo.horizon.w2.h0",
                    },
                },
            ),
            self.registry,
        )
        # Same-member correction attempted via member-transition (SC-R2).
        with self.assertRaisesRegex(FindingModelError, "already in the family"):
            apply_act(
                state,
                act(
                    8,
                    "member-transition",
                    {
                        "family": family,
                        "scope": scope,
                        "member": {
                            "action": "assert",
                            "finding": _finding_v2(
                                "demo.finding.w2-box1-a-corr",
                                fact_id,
                                53000,
                                evidence_ids=["demo.evidence.w2-a"],
                                contribution_id="demo.contribution.w2-a",
                            ),
                        },
                        "successor": {
                            "id": "demo.horizon.w2.h2",
                            "predecessor": "demo.horizon.w2.h1",
                        },
                    },
                ),
                self.registry,
            )


class TestSchemaWiring(ContributionMachineryFixture):
    def test_seven_track1_citizens_registered(self) -> None:
        required = {
            "act-contribution.v1",
            "contribution.v1",
            "contribution-record.v1",
            "finding.v2",
            "act-assertion.v2",
            "act-member-transition.v2",
            "run-request.v1",
        }
        ids = set(self.workspace_registry.schema_ids())
        missing = required - ids
        self.assertEqual(missing, set(), msg=f"missing registry citizens: {missing}")


class TestDataSafetySynthetic(unittest.TestCase):
    def test_track2_fixtures_are_synthetic(self) -> None:
        root = Path("packages/sample_data/frrs_t2")
        markers = ("/Users/", "/private/", "local-data/", "uploads/")
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text("utf-8")
            for marker in markers:
                self.assertNotIn(marker, text, msg=f"{path} contains {marker}")
            # Identifiers must be demo.* synthetic in JSON fixtures.
            if path.suffix == ".json":
                data = json.loads(text)
                blob = json.dumps(data)
                self.assertIn("demo.", blob)


if __name__ == "__main__":
    unittest.main()
