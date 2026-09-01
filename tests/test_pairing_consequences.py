"""Seam 5 — two pairing-scoped consequence rules (ADR-0071).

Synthetic in-repo fixtures only. Proves the production rules:

- two separate rule-artifact.v7 citizens, each dispatched via
  ``evaluate_pairing_scoped_rule``, not one rule appending twice;
- both gated on an ADR-0070 supportability verdict of True for the same
  pairing (Seam 3 producer may still be landing; this consumes the
  accepted finding shape);
- independent succession: superseding one rule's version leaves the
  other rule's finding for the same pairing byte-identical;
- correction displacement through real ``derivation_edges`` /
  ``compute_currency`` / ``displacement_closure``;
- neither fact type is keyed to a Schedule B form-row entity;
- both rules fire from ``runner.run`` / ``attempt()`` rather than as
  standalone functions nobody calls.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from typing import Any

from packages.derivation.authorization import AuthorizationResolution, STATUS_SUSPENDED
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_run_context
from packages.derivation.projection import derivation_edges
from packages.derivation.records import RecordStream
from packages.derivation.runner import RunContext, SourceFact, run, run_and_record
from packages.kernel.currency import CurrencyView, compute_currency, displacement_closure
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import FindingState
from packages.kernel import facts as kernel_facts
from packages.kernel.schema_registry import SchemaValidationError
from packages.tax.identity_association import (
    ACQUISITION_FACT_TYPE,
    ASSOCIATION_SYMBOL,
    REPORT_FACT_TYPE,
)
from packages.tax.pairing_consequences import (
    ACQUISITION_FIELD,
    AGGREGATE_ACCRUED_EXCEEDS_REPORT,
    AGGREGATE_SUPPORTABILITY_RULE_ID,
    AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX,
    BASIS_CITATION_ID,
    BASIS_RULE_ID,
    BASIS_SYMBOL_PREFIX,
    CURRENT_YEAR_CITATION_ID,
    CURRENT_YEAR_RULE_ID,
    CURRENT_YEAR_SUBTOTAL_RULE_ID,
    CURRENT_YEAR_SUBTOTAL_SYMBOL,
    CURRENT_YEAR_SYMBOL_PREFIX,
    PAIRING_TYPE,
    SUPPORTABILITY_NOT_ESTABLISHED,
    SUPPORTABILITY_TYPE,
    evaluate_basis_consequence,
    evaluate_current_year_adjustment,
    is_pairing_scoped_consequence_rule,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT = REPO_ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = REPO_ROOT / "packages" / "sample_data" / "pairing_consequences"
ASSOC_FIXTURES = REPO_ROOT / "packages" / "sample_data" / "identity_association"
INCUMBENT_BUNDLE = CONTENT / "scheduleb-adjustment.accrued-interest.bundle.json"

ADOPTION_PIN = {
    "role": "adoption",
    "id": "demo.package.pairing-consequences",
    "version": "v1",
}
GOVERNANCE = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]


class _HorizonState:
    def __init__(self) -> None:
        self.current_by_chain: dict[tuple[str, str, str], str] = {}


class _State:
    def __init__(self, findings: dict[str, dict[str, Any]]) -> None:
        self.findings = findings
        self.horizon_state = _HorizonState()


def _load(path: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return loaded


def _example(name: str) -> dict[str, Any]:
    return _load(FIXTURES / "examples" / name)


def _assoc_example(name: str) -> dict[str, Any]:
    return _load(ASSOC_FIXTURES / "examples" / name)


def _negative(name: str) -> dict[str, Any]:
    return _load(FIXTURES / "negatives" / name)


def _currency(finding_ids: list[str]) -> CurrencyView:
    ids = frozenset(finding_ids)
    return CurrencyView(
        current_finding_ids=ids,
        displaced_finding_ids=frozenset(),
        current_evidence_ids=frozenset(),
        displaced_evidence_ids=frozenset(),
    )


def _content_rule(rule_id: str) -> dict[str, Any]:
    if rule_id == CURRENT_YEAR_RULE_ID:
        return _load(CONTENT / "rule.interest.current-year-adjustment.pairing-scoped.json")
    if rule_id == BASIS_RULE_ID:
        return _load(CONTENT / "rule.basis.item-level-consequence.pairing-scoped.json")
    raise KeyError(rule_id)


def _pairing_fact_id(left_ref: str, right_statement: str) -> str:
    return fact_id_for(PAIRING_TYPE, (("left", left_ref), ("right", right_statement)))


def _supportability_source(pairing_fact_id: str, *, finding_id: str, value: Any = True) -> SourceFact:
    encoded = value if isinstance(value, str) else json.dumps(value)
    return SourceFact(
        name=SUPPORTABILITY_TYPE,
        value=encoded,
        finding_id=finding_id,
        fact_id=pairing_fact_id,
    )


def _sources_for(
    findings: dict[str, dict[str, Any]],
    *,
    rules: list[dict[str, Any]] | None = None,
    collect: list[str] | None = None,
) -> RunContext:
    return marshal_run_context(
        run_id="demo.run.pairing-consequences",
        state=_State(findings),  # type: ignore[arg-type]
        currency=_currency(list(findings)),
        rules=list(rules or []),
        parameters={},
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE,
        collect_source_names=collect
        or [ACQUISITION_FACT_TYPE, REPORT_FACT_TYPE, PAIRING_TYPE],
    )


def _one_pairing_findings() -> dict[str, dict[str, Any]]:
    a1 = _assoc_example("finding.v2.acquisition-a1.json")
    r1 = _assoc_example("finding.v2.box1-s1.json")
    pair = _example("finding.v2.pairing-a1-s1.json")
    return {a1["id"]: a1, r1["id"]: r1, pair["id"]: pair}


def _ctx_with_supportability(
    findings: dict[str, dict[str, Any]],
    *,
    rules: list[dict[str, Any]] | None = None,
    supportability_value: Any = True,
    supportability_finding_id: str = "demo.finding.supportability.a1-s1",
) -> RunContext:
    ctx = _sources_for(findings, rules=rules)
    pair = next(s for s in ctx.sources if s.name == PAIRING_TYPE)
    extra = _supportability_source(
        pair.fact_id or pair.finding_id,
        finding_id=supportability_finding_id,
        value=supportability_value,
    )
    return replace(ctx, sources=list(ctx.sources) + [extra])


def _pin_ids(finding: dict[str, Any]) -> set[tuple[str, str]]:
    return {(p["role"], p["id"]) for p in finding["pins"]}


class TestContentCitizens(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.registry = self.schemas.registry

    def test_both_rules_validate_as_rule_artifact_v7(self) -> None:
        for rule_id in (CURRENT_YEAR_RULE_ID, BASIS_RULE_ID):
            with self.subTest(rule_id=rule_id):
                rule = _content_rule(rule_id)
                self.registry.validate("rule-artifact.v7", rule)
                self.assertTrue(is_pairing_scoped_consequence_rule(rule))
                self.assertEqual(rule["schema"], "rule-artifact.v7")
                self.assertEqual(rule["blocked"]["code"], SUPPORTABILITY_NOT_ESTABLISHED)

    def test_rules_are_distinct_artifacts(self) -> None:
        cy = _content_rule(CURRENT_YEAR_RULE_ID)
        basis = _content_rule(BASIS_RULE_ID)
        self.assertNotEqual(cy["id"], basis["id"])
        self.assertNotEqual(cy["publishes"], basis["publishes"])
        self.assertNotEqual(cy["citations"][0]["id"], basis["citations"][0]["id"])

    def test_fact_types_are_keyed_to_the_pairing_not_a_form_row(self) -> None:
        bundle = _load(CONTENT / "pairing-scoped-consequences.bundle.json")
        self.registry.validate("bundle.v2", bundle)
        incumbent = _load(INCUMBENT_BUNDLE)
        incumbent_kinds = {
            key.get("entity_kind")
            for ft in incumbent["fact_types"]
            for key in ft["identity_keys"]
        }
        self.assertIn("tax.us.scheduleb-adjustment-instance", incumbent_kinds)
        for ft in bundle["fact_types"]:
            self.registry.validate("fact-type.v2", ft)
            kinds = [key.get("entity_kind") for key in ft["identity_keys"] if key["kind"] == "entity"]
            self.assertEqual(kinds, ["tax.us.acquisition-report-pairing"])
            self.assertNotIn("tax.us.scheduleb-adjustment-instance", kinds)
            self.assertNotIn("adjustment-instance", [key["name"] for key in ft["identity_keys"]])

    def test_runtime_symbol_prefixes_literally_equal_the_declared_fact_type_ids(
        self,
    ) -> None:
        """Declared consequence fact types must match published findings.

        The published bundle names the two consequence fact types with a
        ``.pairing-scoped`` suffix; the runtime symbol prefix a
        pairing-scoped publication actually carries (everything before the
        ``|`` pairing-fact-id separator) must be exactly that declared id,
        not merely something recognizable as related to it.
        """
        bundle = _load(CONTENT / "pairing-scoped-consequences.bundle.json")
        declared_ids = {ft["id"] for ft in bundle["fact_types"]}
        self.assertIn(CURRENT_YEAR_SYMBOL_PREFIX, declared_ids)
        self.assertIn(BASIS_SYMBOL_PREFIX, declared_ids)

        ctx = _ctx_with_supportability(_one_pairing_findings())
        cy = evaluate_current_year_adjustment(
            sources=ctx.sources, extra_pins=[ADOPTION_PIN], schemas=self.schemas
        ).publications[0]
        basis = evaluate_basis_consequence(
            sources=ctx.sources, extra_pins=[ADOPTION_PIN], schemas=self.schemas
        ).publications[0]
        cy_prefix, _, _ = cy["symbol"].partition("|")
        basis_prefix, _, _ = basis["symbol"].partition("|")
        self.assertEqual(cy_prefix, CURRENT_YEAR_SYMBOL_PREFIX)
        self.assertEqual(basis_prefix, BASIS_SYMBOL_PREFIX)
        self.assertIn(cy_prefix, declared_ids)
        self.assertIn(basis_prefix, declared_ids)

    def test_basis_citation_is_distinct_from_schedule_b(self) -> None:
        citation = _load(CONTENT / "citation.basis-adjustment.accrued-interest.json")
        self.registry.validate("citation.v1", citation)
        self.assertEqual(citation["id"], BASIS_CITATION_ID)
        self.assertNotEqual(citation["id"], CURRENT_YEAR_CITATION_ID)


class TestPayloadInstantiation(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = DerivationSchemas().registry

    def test_positive_derived_findings_validate(self) -> None:
        for name in (
            "derived-finding.v2.current-year-adjustment.json",
            "derived-finding.v2.basis-consequence.json",
        ):
            payload = _example(name)
            self.registry.validate("derived-finding.v2", payload)
            roles = {p["role"] for p in payload["pins"]}
            self.assertIn("computation", roles)
            self.assertIn("citation", roles)
            self.assertIn("input", roles)

    def test_input_pin_without_origin_is_rejected(self) -> None:
        payload = _negative("derived-finding.v2.input-without-origin.json")
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("derived-finding.v2", payload)

    def test_positive_pairing_and_supportability_findings_validate(self) -> None:
        for name in (
            "finding.v2.pairing-a1-s1.json",
            "finding.v2.supportability-a1-s1.json",
        ):
            self.registry.validate("finding.v2", _example(name))


class TestTwoRulesOnePairing(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.findings = _one_pairing_findings()
        self.ctx = _ctx_with_supportability(self.findings)
        self.pair = _example("finding.v2.pairing-a1-s1.json")
        self.a1 = _assoc_example("finding.v2.acquisition-a1.json")
        self.r1 = _assoc_example("finding.v2.box1-s1.json")

    def test_each_rule_publishes_one_finding_with_own_identity(self) -> None:
        cy = evaluate_current_year_adjustment(
            sources=self.ctx.sources, extra_pins=[ADOPTION_PIN], schemas=self.schemas
        )
        basis = evaluate_basis_consequence(
            sources=self.ctx.sources, extra_pins=[ADOPTION_PIN], schemas=self.schemas
        )
        self.assertEqual(cy.blocked, ())
        self.assertEqual(basis.blocked, ())
        self.assertEqual(len(cy.publications), 1)
        self.assertEqual(len(basis.publications), 1)
        cy_finding = cy.publications[0]
        basis_finding = basis.publications[0]
        self.assertNotEqual(cy_finding["id"], basis_finding["id"])
        self.assertNotEqual(cy_finding["symbol"], basis_finding["symbol"])
        self.assertTrue(cy_finding["symbol"].startswith(CURRENT_YEAR_SYMBOL_PREFIX + "|"))
        self.assertTrue(basis_finding["symbol"].startswith(BASIS_SYMBOL_PREFIX + "|"))

        cy_rule = next(p for p in cy_finding["pins"] if p["role"] == "computation")
        basis_rule = next(p for p in basis_finding["pins"] if p["role"] == "computation")
        self.assertEqual(cy_rule["id"], CURRENT_YEAR_RULE_ID)
        self.assertEqual(basis_rule["id"], BASIS_RULE_ID)
        self.assertNotEqual(cy_rule["id"], basis_rule["id"])

        expected_inputs = {
            self.a1["id"],
            self.r1["id"],
            self.pair["id"],
            "demo.finding.supportability.a1-s1",
        }
        for finding, citation_id in (
            (cy_finding, CURRENT_YEAR_CITATION_ID),
            (basis_finding, BASIS_CITATION_ID),
        ):
            input_ids = {p["id"] for p in finding["pins"] if p["role"] == "input"}
            self.assertTrue(expected_inputs <= input_ids, input_ids)
            citations = [p for p in finding["pins"] if p["role"] == "citation"]
            self.assertEqual(len(citations), 1)
            self.assertEqual(citations[0]["id"], citation_id)
        self.assertEqual(cy_finding["value"], "42.0")
        self.assertEqual(basis_finding["value"], "42.0")
        self.assertEqual(self.a1["value"][ACQUISITION_FIELD], 42.0)


class TestSupportabilityGate(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.findings = _one_pairing_findings()

    def test_missing_verdict_blocks_both_rules(self) -> None:
        ctx = _sources_for(self.findings)
        cy = evaluate_current_year_adjustment(
            sources=ctx.sources, extra_pins=[ADOPTION_PIN], schemas=self.schemas
        )
        basis = evaluate_basis_consequence(
            sources=ctx.sources, extra_pins=[ADOPTION_PIN], schemas=self.schemas
        )
        self.assertEqual(cy.publications, ())
        self.assertEqual(basis.publications, ())
        self.assertEqual(len(cy.blocked), 1)
        self.assertEqual(len(basis.blocked), 1)
        self.assertEqual(cy.blocked[0].code, SUPPORTABILITY_NOT_ESTABLISHED)
        self.assertEqual(basis.blocked[0].code, SUPPORTABILITY_NOT_ESTABLISHED)

    def test_false_verdict_blocks_both_rules(self) -> None:
        ctx = _ctx_with_supportability(self.findings, supportability_value=False)
        cy = evaluate_current_year_adjustment(
            sources=ctx.sources, extra_pins=[ADOPTION_PIN], schemas=self.schemas
        )
        self.assertEqual(cy.publications, ())
        self.assertEqual(cy.blocked[0].code, SUPPORTABILITY_NOT_ESTABLISHED)


class TestIndependentSuccession(unittest.TestCase):
    def test_superseding_basis_leaves_current_year_byte_identical(self) -> None:
        schemas = DerivationSchemas()
        ctx = _ctx_with_supportability(_one_pairing_findings())
        cy_before = evaluate_current_year_adjustment(
            sources=ctx.sources, extra_pins=[ADOPTION_PIN], schemas=schemas
        ).publications[0]
        basis_v1 = evaluate_basis_consequence(
            sources=ctx.sources,
            rule_version="v1",
            extra_pins=[ADOPTION_PIN],
            schemas=schemas,
        ).publications[0]
        basis_v2 = evaluate_basis_consequence(
            sources=ctx.sources,
            rule_version="v2",
            extra_pins=[ADOPTION_PIN],
            schemas=schemas,
        ).publications[0]
        self.assertNotEqual(basis_v1["id"], basis_v2["id"])
        basis_pin_v2 = next(p for p in basis_v2["pins"] if p["role"] == "computation")
        self.assertEqual(basis_pin_v2["version"], "v2")

        cy_after = evaluate_current_year_adjustment(
            sources=ctx.sources, extra_pins=[ADOPTION_PIN], schemas=schemas
        ).publications[0]
        self.assertEqual(cy_after["id"], cy_before["id"])
        self.assertEqual(cy_after, cy_before)
        cy_pin = next(p for p in cy_after["pins"] if p["role"] == "computation")
        self.assertEqual(cy_pin["id"], CURRENT_YEAR_RULE_ID)
        self.assertEqual(cy_pin["version"], "v1")


class TestCorrectionDisplacement(unittest.TestCase):
    def test_shared_pins_displace_both_consequences_via_real_machinery(self) -> None:
        schemas = DerivationSchemas()
        findings = _one_pairing_findings()
        ctx = _ctx_with_supportability(findings)
        a1 = findings["demo.finding.acq.a1"]
        r1 = findings["demo.finding.box1.s1"]
        pair = findings["demo.finding.pair.a1-s1"]

        cy = evaluate_current_year_adjustment(
            sources=ctx.sources, extra_pins=[ADOPTION_PIN], schemas=schemas
        ).publications[0]
        basis = evaluate_basis_consequence(
            sources=ctx.sources, extra_pins=[ADOPTION_PIN], schemas=schemas
        ).publications[0]

        supportability_finding: dict[str, Any] = {
            "schema": "derived-finding.v2",
            "id": "demo.finding.supportability.a1-s1",
            "symbol": f"{SUPPORTABILITY_TYPE}|{pair['fact_id']}",
            "value": True,
            "version": "v2",
            "pins": [
                {
                    "role": "input",
                    "id": a1["id"],
                    "version": "v1",
                    "origin": "assertion",
                },
                {
                    "role": "input",
                    "id": r1["id"],
                    "version": "v1",
                    "origin": "assertion",
                },
                {
                    "role": "input",
                    "id": pair["id"],
                    "version": "v1",
                    "origin": "assertion",
                },
            ],
        }
        derived_all = {
            supportability_finding["id"]: supportability_finding,
            cy["id"]: cy,
            basis["id"]: basis,
        }
        edges = derivation_edges(derived_all)
        self.assertIn(cy["id"], edges[a1["id"]])
        self.assertIn(basis["id"], edges[a1["id"]])
        self.assertIn(cy["id"], edges[pair["id"]])
        self.assertIn(basis["id"], edges[pair["id"]])
        self.assertIn(supportability_finding["id"], edges[r1["id"]])
        self.assertEqual(
            {cy["id"], basis["id"]},
            edges[supportability_finding["id"]],
        )

        kernel_findings = {
            a1["id"]: {"id": a1["id"], "fact_id": a1["fact_id"], "value": a1["value"]},
            r1["id"]: {"id": r1["id"], "fact_id": r1["fact_id"], "value": r1["value"]},
            pair["id"]: {
                "id": pair["id"],
                "fact_id": pair["fact_id"],
                "value": pair["value"],
            },
        }
        initial = FindingState(
            fact_state=kernel_facts.initial_state(), findings=kernel_findings
        )
        self.assertEqual(compute_currency(initial).displaced_finding_ids, frozenset())

        for corrected_id, fact_id, new_value in (
            (a1["id"], a1["fact_id"], {**a1["value"], ACQUISITION_FIELD: 50.0}),
            (r1["id"], r1["fact_id"], 600.0),
            (pair["id"], pair["fact_id"], pair["value"]),
        ):
            with self.subTest(corrected=corrected_id):
                corrected = dict(kernel_findings)
                successor = f"{corrected_id}-corrected"
                corrected[successor] = {
                    "id": successor,
                    "fact_id": fact_id,
                    "value": new_value,
                }
                currency = compute_currency(
                    FindingState(
                        fact_state=kernel_facts.initial_state(), findings=corrected
                    )
                )
                self.assertIn(corrected_id, currency.displaced_finding_ids)
                closure, _ = displacement_closure(
                    set(currency.displaced_finding_ids), {"derivation": edges}
                )
                self.assertIn(cy["id"], closure)
                self.assertIn(basis["id"], closure)
                if corrected_id == r1["id"]:
                    self.assertIn(supportability_finding["id"], closure)


class TestRunnerWiring(unittest.TestCase):
    def test_run_dispatches_both_rules_from_attempt(self) -> None:
        schemas = DerivationSchemas()
        rules = [_content_rule(CURRENT_YEAR_RULE_ID), _content_rule(BASIS_RULE_ID)]
        ctx = _ctx_with_supportability(_one_pairing_findings(), rules=rules)
        result = run(ctx, schemas)
        symbols = {pub.finding["symbol"] for pub in result.publications}
        self.assertEqual(len(result.publications), 2)
        self.assertTrue(any(s.startswith(CURRENT_YEAR_SYMBOL_PREFIX + "|") for s in symbols))
        self.assertTrue(any(s.startswith(BASIS_SYMBOL_PREFIX + "|") for s in symbols))
        self.assertIn(CURRENT_YEAR_RULE_ID, {d["artifact_id"] for d in result.dispositions})
        self.assertIn(BASIS_RULE_ID, {d["artifact_id"] for d in result.dispositions})
        published = [d for d in result.dispositions if d["disposition"] == "published"]
        self.assertEqual(len(published), 2)
        self.assertEqual(result.blocked, [])

    def test_missing_supportability_survives_v8_ledger(self) -> None:
        schemas = DerivationSchemas()
        rules = [_content_rule(CURRENT_YEAR_RULE_ID)]
        ctx = _sources_for(_one_pairing_findings(), rules=rules)
        with tempfile.TemporaryDirectory() as tmp:
            stream = RecordStream(Path(tmp) / "workspace", schemas)
            result = run_and_record(
                ctx,
                schemas,
                stream,
                workspace_revision=1,
                adopted_packages={ADOPTION_PIN["id"]},
                start_record_id="demo.start.supportability-missing",
                completion_record_id="demo.done.supportability-missing",
            )
            closing = stream.standings()[ctx.run_id].closing
        assert closing is not None
        self.assertEqual(closing["schema"], "derivation-record.v8")
        self.assertEqual(result.blocked[0]["code"], SUPPORTABILITY_NOT_ESTABLISHED)
        ledger = {row["artifact_id"]: row for row in closing["dispositions"]}
        self.assertEqual(ledger[CURRENT_YEAR_RULE_ID]["code"], SUPPORTABILITY_NOT_ESTABLISHED)
        self.assertNotEqual(ledger[CURRENT_YEAR_RULE_ID]["code"], "DEPENDENCY_INVALID")

    def test_suspended_authorization_is_on_env_and_does_not_bypass_attempt(self) -> None:
        schemas = DerivationSchemas()
        rules = [_content_rule(CURRENT_YEAR_RULE_ID)]
        ctx = _ctx_with_supportability(_one_pairing_findings(), rules=rules)
        ctx = replace(
            ctx, authorization=AuthorizationResolution(STATUS_SUSPENDED, "demo.auth.g1")
        )
        result = run(ctx, schemas)
        self.assertEqual(len(result.publications), 1)
        assert ctx.authorization is not None
        self.assertEqual(ctx.authorization.status, STATUS_SUSPENDED)
        self.assertFalse(ctx.authorization.admitted)


class TestDeclaredExpressionControlsExecution(unittest.TestCase):
    """A successor rule citizen whose ``value`` is a genuinely
    different, schema-valid expression must genuinely change what
    ``dispatch_consequence_on_run`` (called from real ``_Run.attempt`` via
    ``run()``) publishes -- not silently keep publishing the old hardcoded
    number. This exercises the real production dispatch path
    (``TestRunnerWiring``'s own pattern: a loaded ``rule-artifact.v7``
    content citizen run through ``run(ctx, schemas)``), not a second,
    hand-rolled evaluator.
    """

    def test_successor_basis_rule_expression_changes_the_published_value(self) -> None:
        schemas = DerivationSchemas()
        ctx = _ctx_with_supportability(_one_pairing_findings())

        incumbent_rule = _content_rule(BASIS_RULE_ID)
        self.assertEqual(
            incumbent_rule["value"],
            {"op": "ref", "name": ACQUISITION_FACT_TYPE, "field": ACQUISITION_FIELD},
        )

        # A schema-valid successor expression that computes something
        # genuinely different from the incumbent (double the accrued
        # amount) -- arithmetic rather than a differently-typed field, so
        # the result stays numeric.
        successor_rule = dict(incumbent_rule)
        successor_rule["version"] = "v2"
        successor_rule["value"] = {
            "op": "multiply",
            "left": {"op": "ref", "name": ACQUISITION_FACT_TYPE, "field": ACQUISITION_FIELD},
            "right": 2,
        }
        self.registry_validate_or_skip(schemas, successor_rule)

        result = run(replace(ctx, rules=[successor_rule]), schemas)
        self.assertEqual(result.blocked, [])
        self.assertEqual(len(result.publications), 1)
        published = result.publications[0].finding
        self.assertTrue(published["symbol"].startswith(BASIS_SYMBOL_PREFIX + "|"))

        # Not the old hardcoded 42.0 -- the new declared expression's own
        # answer, 84.0.
        self.assertEqual(Decimal(str(published["value"])), Decimal("84.0"))
        self.assertNotEqual(Decimal(str(published["value"])), Decimal("42.0"))

        computation_pin = next(p for p in published["pins"] if p["role"] == "computation")
        self.assertEqual(computation_pin["id"], BASIS_RULE_ID)
        self.assertEqual(computation_pin["version"], "v2")

    def registry_validate_or_skip(self, schemas: DerivationSchemas, rule: dict[str, Any]) -> None:
        # The rule-artifact.v7 schema constrains the closed op vocabulary,
        # not specific op combinations; a "multiply" value is exactly as
        # schema-valid as the incumbent "ref" value.  Validate here so a
        # future schema change that would reject this shape fails loudly
        # in this test rather than masking the defect this test targets.
        schemas.registry.validate("rule-artifact.v7", rule)


def _enc(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list, bool)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def _src(name: str, value: Any, finding_id: str, fact_id: str) -> SourceFact:
    return SourceFact(name=name, value=_enc(value), finding_id=finding_id, fact_id=fact_id)


class TestAggregateSupportability(unittest.TestCase):
    """Aggregate supportability.

    ADR-0070 Decision 4's per-pairing check stays exactly as accepted: two
    acquisitions genuinely associated with the same report each get their
    own independent supportability verdict, evaluated against the report's
    full amount. This suite proves the *separate*, additive aggregate layer
    that closes the gap the per-pairing check cannot see by design: a
    combined claim against one specific report exceeding that report.
    """

    def _shared_report_sources(
        self, *, accrued_1: float, accrued_2: float, report_amount: float
    ) -> list[SourceFact]:
        return [
            _src(
                ACQUISITION_FACT_TYPE,
                {"accrued_interest_paid_to_seller": accrued_1},
                "demo.finding.acq.g1",
                "demo.fact.acq.g1",
            ),
            _src(
                ACQUISITION_FACT_TYPE,
                {"accrued_interest_paid_to_seller": accrued_2},
                "demo.finding.acq.g2",
                "demo.fact.acq.g2",
            ),
            _src(REPORT_FACT_TYPE, report_amount, "demo.finding.box1.shared", "demo.fact.box1.shared"),
            _src(
                PAIRING_TYPE,
                {"left_fact_id": "demo.fact.acq.g1", "right_fact_id": "demo.fact.box1.shared"},
                "demo.finding.pair.g1",
                "demo.fact.pair.g1",
            ),
            _src(
                PAIRING_TYPE,
                {"left_fact_id": "demo.fact.acq.g2", "right_fact_id": "demo.fact.box1.shared"},
                "demo.finding.pair.g2",
                "demo.fact.pair.g2",
            ),
            _src(SUPPORTABILITY_TYPE, True, "demo.finding.support.g1", "demo.fact.pair.g1"),
            _src(SUPPORTABILITY_TYPE, True, "demo.finding.support.g2", "demo.fact.pair.g2"),
        ]

    def _unrelated_report_sources(self, *, accrued: float, report_amount: float) -> list[SourceFact]:
        return [
            _src(
                ACQUISITION_FACT_TYPE,
                {"accrued_interest_paid_to_seller": accrued},
                "demo.finding.acq.u",
                "demo.fact.acq.u",
            ),
            _src(REPORT_FACT_TYPE, report_amount, "demo.finding.box1.unrelated", "demo.fact.box1.unrelated"),
            _src(
                PAIRING_TYPE,
                {"left_fact_id": "demo.fact.acq.u", "right_fact_id": "demo.fact.box1.unrelated"},
                "demo.finding.pair.u",
                "demo.fact.pair.u",
            ),
            _src(SUPPORTABILITY_TYPE, True, "demo.finding.support.u", "demo.fact.pair.u"),
        ]

    def _rules(self, *, with_subtotal: bool = False) -> list[dict[str, Any]]:
        rules = [
            _content_rule(CURRENT_YEAR_RULE_ID),
            _load(CONTENT / "rule.interest.current-year-adjustment.aggregate-supportability.json"),
        ]
        if with_subtotal:
            rules.append(_load(CONTENT / "rule.interest.current-year-adjustment-subtotal.json"))
        return rules

    def _ctx(self, sources: list[SourceFact], *, with_subtotal: bool = False) -> RunContext:
        return RunContext(
            run_id="demo.run.aggregate-supportability",
            rules=self._rules(with_subtotal=with_subtotal),
            parameters={},
            canon={},
            inputs=[],
            sources=sources,
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
        )

    def test_shared_report_exceeded_by_combined_claim(self) -> None:
        """Detecting the combined over-claim does not establish the
        excluded remainder is "correct" — the blocked group's individual
        findings are retracted (not left "published"), and the subtotal
        itself blocks rather than presenting a different confident number.

        Report 500, two acquisitions of 300 each genuinely associated to
        it (both individually pass 300<=500), one unrelated report of 200.
        Without the aggregate check: box-1 subtotal 700, adjustment
        subtotal 600, taxable total 100, with no block -- this must not
        happen silently. The subtotal must never quietly publish 50
        (excluding the blocked group) and call it correct, either.
        """
        schemas = DerivationSchemas()
        sources = self._shared_report_sources(
            accrued_1=300.0, accrued_2=300.0, report_amount=500.0
        ) + self._unrelated_report_sources(accrued=50.0, report_amount=200.0)
        ctx = self._ctx(sources, with_subtotal=True)
        result = run(ctx, schemas)

        # Each pairing's own per-pairing verdict still passes individually
        # (ADR-0070 Decision 4 is not reopened) at evaluation time, but the
        # blocked group's two 300-accrued findings are retracted from
        # ordinary publication: only the unrelated report's
        # 50-accrued finding remains presented as ordinarily supported.
        cy = [
            pub.finding
            for pub in result.publications
            if str(pub.finding.get("symbol", "")).startswith(CURRENT_YEAR_SYMBOL_PREFIX + "|")
        ]
        self.assertEqual(len(cy), 1)
        self.assertEqual(Decimal(str(cy[0]["value"])), Decimal("50.0"))

        # The retracted findings' own disposition rows are rewritten from
        # published to blocked, named with the aggregate check's own code —
        # not silently dropped, not left falsely "published".
        retracted = [
            row
            for row in result.dispositions
            if row.get("artifact_id") == CURRENT_YEAR_RULE_ID
            and row.get("disposition") == "blocked"
        ]
        self.assertEqual(len(retracted), 2)
        for row in retracted:
            self.assertEqual(row["code"], AGGREGATE_ACCRUED_EXCEEDS_REPORT)
            self.assertEqual(row["missing"], ["demo.fact.box1.shared"])

        # The aggregate check blocks the shared-report group and nothing else.
        aggregate_blocks = [
            row for row in result.blocked
            if row["artifact_id"] == AGGREGATE_SUPPORTABILITY_RULE_ID
        ]
        self.assertEqual(len(aggregate_blocks), 1)
        self.assertEqual(aggregate_blocks[0]["code"], AGGREGATE_ACCRUED_EXCEEDS_REPORT)
        self.assertEqual(aggregate_blocks[0]["missing"], ["demo.fact.box1.shared"])

        # The unrelated report's own aggregate group still publishes True.
        aggregate_publications = [
            pub.finding
            for pub in result.publications
            if str(pub.finding.get("symbol", "")).startswith(
                AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX + "|"
            )
        ]
        self.assertEqual(len(aggregate_publications), 1)
        self.assertEqual(
            aggregate_publications[0]["symbol"],
            f"{AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX}|demo.fact.box1.unrelated",
        )
        self.assertIs(aggregate_publications[0]["value"], True)

        # The subtotal must not quietly publish 50 and call it correct: it
        # blocks,
        # named with the exact report still unresolved, and propagates
        # through the ordinary missing-dependency mechanism rather than a
        # new mechanism.
        self.assertNotIn(
            CURRENT_YEAR_SUBTOTAL_SYMBOL,
            {pub.finding.get("symbol") for pub in result.publications},
        )
        subtotal_blocks = [
            row for row in result.blocked
            if row["artifact_id"] == CURRENT_YEAR_SUBTOTAL_RULE_ID
        ]
        self.assertEqual(len(subtotal_blocks), 1)
        self.assertEqual(subtotal_blocks[0]["code"], AGGREGATE_ACCRUED_EXCEEDS_REPORT)
        self.assertEqual(subtotal_blocks[0]["missing"], ["demo.fact.box1.shared"])
        self.assertTrue(
            any(
                d["artifact_id"] == AGGREGATE_SUPPORTABILITY_RULE_ID
                and d["disposition"] == "blocked"
                and d.get("code") == AGGREGATE_ACCRUED_EXCEEDS_REPORT
                for d in result.dispositions
            )
        )
        self.assertTrue(
            any(
                d["artifact_id"] == CURRENT_YEAR_SUBTOTAL_RULE_ID
                and d["disposition"] == "blocked"
                and d.get("code") == AGGREGATE_ACCRUED_EXCEEDS_REPORT
                for d in result.dispositions
            )
        )

    def test_named_code_survives_the_v9_ledger(self) -> None:
        schemas = DerivationSchemas()
        sources = self._shared_report_sources(
            accrued_1=300.0, accrued_2=300.0, report_amount=500.0
        )
        ctx = self._ctx(sources)
        with tempfile.TemporaryDirectory() as tmp:
            stream = RecordStream(Path(tmp) / "workspace", schemas)
            result = run_and_record(
                ctx,
                schemas,
                stream,
                workspace_revision=1,
                adopted_packages={ADOPTION_PIN["id"]},
                start_record_id="demo.start.aggregate",
                completion_record_id="demo.done.aggregate",
            )
            closing = stream.standings()[ctx.run_id].closing
        assert closing is not None
        self.assertEqual(closing["schema"], "derivation-record.v8")
        ledger = [
            row for row in closing["dispositions"]
            if row["artifact_id"] == AGGREGATE_SUPPORTABILITY_RULE_ID
        ]
        self.assertEqual(len(ledger), 1)
        self.assertEqual(ledger[0]["disposition"], "blocked")
        self.assertEqual(ledger[0]["code"], AGGREGATE_ACCRUED_EXCEEDS_REPORT)
        self.assertNotEqual(ledger[0]["code"], "DEPENDENCY_INVALID")
        self.assertEqual(result.blocked[0]["code"], AGGREGATE_ACCRUED_EXCEEDS_REPORT)

    def test_combined_claim_at_or_under_report_is_not_blocked(self) -> None:
        """Two 200-accrued acquisitions against one 500 report: 400<=500.

        Must not be blocked; both individual pairings and the aggregate
        check publish. Matches ADR-0070's continued-valid per-pairing case
        at the aggregate layer too.
        """
        schemas = DerivationSchemas()
        sources = self._shared_report_sources(
            accrued_1=200.0, accrued_2=200.0, report_amount=500.0
        )
        ctx = self._ctx(sources, with_subtotal=True)
        result = run(ctx, schemas)

        self.assertEqual(
            [row for row in result.blocked if row["artifact_id"] == AGGREGATE_SUPPORTABILITY_RULE_ID],
            [],
        )
        aggregate_publications = [
            pub.finding
            for pub in result.publications
            if str(pub.finding.get("symbol", "")).startswith(
                AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX + "|"
            )
        ]
        self.assertEqual(len(aggregate_publications), 1)
        self.assertIs(aggregate_publications[0]["value"], True)

        subtotal = next(
            pub.finding for pub in result.publications
            if pub.finding.get("symbol") == CURRENT_YEAR_SUBTOTAL_SYMBOL
        )
        self.assertEqual(Decimal(str(subtotal["value"])), Decimal("400.0"))

    def test_aggregate_rule_absent_does_not_change_isolation_test_behavior(self) -> None:
        """An isolation test that omits the aggregate rule stays unaffected."""
        schemas = DerivationSchemas()
        sources = self._shared_report_sources(
            accrued_1=300.0, accrued_2=300.0, report_amount=500.0
        )
        ctx = RunContext(
            run_id="demo.run.no-aggregate-rule",
            rules=[_content_rule(CURRENT_YEAR_RULE_ID)],
            parameters={},
            canon={},
            inputs=[],
            sources=sources,
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
        )
        result = run(ctx, schemas)
        cy = [
            pub.finding
            for pub in result.publications
            if str(pub.finding.get("symbol", "")).startswith(CURRENT_YEAR_SYMBOL_PREFIX + "|")
        ]
        self.assertEqual(len(cy), 2)
        self.assertEqual(result.blocked, [])


class TestDependencyPinFidelity(unittest.TestCase):
    """A pairing-scoped rule's declared expression controls the published
    number, and the evaluator's own ``AccessLog`` must be consulted so a
    parameter, table, or operation-semantics dependency the expression
    actually read always appears as a pin -- never silently discarded. The
    parameter case plus the companion operation-semantics case, run through
    the real production dispatch path (``dispatch_consequence_on_run`` via
    ``run(ctx, schemas)``), not a hand-rolled evaluator.
    """

    PARAMETER_ID = "demo.parameter.pairing-value"

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.ctx = _ctx_with_supportability(_one_pairing_findings())
        self.incumbent_rule = _content_rule(BASIS_RULE_ID)

    def _successor(self, *, value_expr: dict[str, Any], version: str = "v2") -> dict[str, Any]:
        rule = dict(self.incumbent_rule)
        rule["version"] = version
        rule["value"] = value_expr
        self.schemas.registry.validate("rule-artifact.v7", rule)
        return rule

    def test_parameter_dependency_is_published_and_pinned(self) -> None:
        """A declared parameter reference."""
        successor = self._successor(
            value_expr={"op": "parameter", "parameter_id": self.PARAMETER_ID}
        )
        ctx = replace(
            self.ctx,
            rules=[successor],
            parameters={self.PARAMETER_ID: {"version": "v1", "values": 77}},
        )
        result = run(ctx, self.schemas)
        self.assertEqual(result.blocked, [])
        self.assertEqual(len(result.publications), 1)
        published = result.publications[0].finding

        self.assertEqual(Decimal(str(published["value"])), Decimal("77"))

        # The parameter the declared expression actually read is an exact
        # pin, never silently discarded.
        parameter_pins = [p for p in published["pins"] if p["role"] == "parameter"]
        self.assertEqual(
            [(p["id"], p["version"]) for p in parameter_pins],
            [(self.PARAMETER_ID, "v1")],
        )

    def test_parameter_correction_changes_the_published_pin_and_value(self) -> None:
        """Superseding the parameter's own version changes what's published
        and pinned -- the truthful form of "currency" available for a
        provenance-class dependency.

        ``packages/derivation/projection.py``'s ``derivation_edges`` (ADR-0010
        decision 4) deliberately excludes ``parameter``/``operation-semantics``/
        ``adoption``/``governance`` pins from the kernel displacement-closure
        walk: "changing a parameter version is a re-adoption, not a correction
        of a finding this derived value stood on." Parameters are not kernel
        findings with a fact id in this codebase (``RunContext.parameters`` is
        a plain versioned mapping the caller supplies, never fact-log
        tracked), so there is no kernel finding to correct and no
        ``compute_currency``/``displacement_closure`` edge to walk for this
        pin class -- unlike the acquisition/report/pairing/supportability
        input pins, which are real kernel-findings and are proven to displace
        in ``TestCorrectionDisplacement`` and again below in
        ``test_input_class_pins_still_displace_when_value_also_depends_on_a_parameter``.
        What a parameter *does* get, now that it is truthfully pinned, is
        exact version fidelity: a different adopted parameter version
        produces a genuinely different published finding (different value,
        different pin, different finding id) rather than silently keeping
        the old number under the old, now-stale pin.
        """
        successor = self._successor(
            value_expr={"op": "parameter", "parameter_id": self.PARAMETER_ID}
        )
        before_ctx = replace(
            self.ctx,
            rules=[successor],
            parameters={self.PARAMETER_ID: {"version": "v1", "values": 77}},
        )
        before = run(before_ctx, self.schemas).publications[0].finding

        after_ctx = replace(
            self.ctx,
            rules=[successor],
            parameters={self.PARAMETER_ID: {"version": "v2", "values": 90}},
        )
        after = run(after_ctx, self.schemas).publications[0].finding

        self.assertEqual(Decimal(str(before["value"])), Decimal("77"))
        self.assertEqual(Decimal(str(after["value"])), Decimal("90"))
        before_param = next(p for p in before["pins"] if p["role"] == "parameter")
        after_param = next(p for p in after["pins"] if p["role"] == "parameter")
        self.assertEqual(before_param["version"], "v1")
        self.assertEqual(after_param["version"], "v2")
        self.assertNotEqual(before["id"], after["id"])

    def test_operation_semantics_dependency_is_published_and_pinned(self) -> None:
        """A ``round`` op exercises ``AccessLog.operations`` the same way an
        ordinary rule's declared expression does; this must pin the exact
        adopted operation-semantics canon version, not silently drop it.
        """
        canon = load_canon(self.schemas)
        successor = self._successor(
            value_expr={
                "op": "round",
                "mode": "half_up",
                "value": {"op": "ref", "name": ACQUISITION_FACT_TYPE, "field": ACQUISITION_FIELD},
            }
        )
        ctx = replace(self.ctx, rules=[successor], canon=canon)
        result = run(ctx, self.schemas)
        self.assertEqual(result.blocked, [])
        self.assertEqual(len(result.publications), 1)
        published = result.publications[0].finding

        self.assertEqual(Decimal(str(published["value"])), Decimal("42"))
        op_pins = [p for p in published["pins"] if p["role"] == "operation-semantics"]
        self.assertEqual(
            [(p["id"], p["version"]) for p in op_pins],
            [("round", canon["round"]["version"])],
        )

    def test_input_class_pins_still_displace_when_value_also_depends_on_a_parameter(
        self,
    ) -> None:
        """The real ADR-0010 displacement mechanism.

        A successor rule whose value reads both a parameter (provenance-only,
        proven above) and the pairing's own acquisition input (via ``ref``,
        access-log ``refs``) still gets the acquisition/report/pairing/
        supportability input pins unconditionally (``pairing_dispatch``'s
        ``present_pins``), and correcting one of
        those real kernel findings still displaces this successor's
        published finding to non-current through the exact same
        ``derivation_edges`` / ``compute_currency`` / ``displacement_closure``
        chain ``TestCorrectionDisplacement`` already proves for the
        incumbent rule.
        """
        successor = self._successor(
            value_expr={
                "op": "add",
                "args": [
                    {"op": "ref", "name": ACQUISITION_FACT_TYPE, "field": ACQUISITION_FIELD},
                    {"op": "parameter", "parameter_id": self.PARAMETER_ID},
                ],
            }
        )
        ctx = replace(
            self.ctx,
            rules=[successor],
            parameters={self.PARAMETER_ID: {"version": "v1", "values": 8}},
        )
        result = run(ctx, self.schemas)
        self.assertEqual(result.blocked, [])
        basis = result.publications[0].finding
        self.assertEqual(Decimal(str(basis["value"])), Decimal("50"))  # 42 + 8

        parameter_pins = [p for p in basis["pins"] if p["role"] == "parameter"]
        self.assertEqual(
            [(p["id"], p["version"]) for p in parameter_pins],
            [(self.PARAMETER_ID, "v1")],
        )

        a1 = _assoc_example("finding.v2.acquisition-a1.json")
        r1 = _assoc_example("finding.v2.box1-s1.json")
        pair = _example("finding.v2.pairing-a1-s1.json")
        supportability_finding: dict[str, Any] = {
            "schema": "derived-finding.v2",
            "id": "demo.finding.supportability.a1-s1",
            "symbol": f"{SUPPORTABILITY_TYPE}|{pair['fact_id']}",
            "value": True,
            "version": "v2",
            "pins": [
                {"role": "input", "id": a1["id"], "version": "v1", "origin": "assertion"},
                {"role": "input", "id": r1["id"], "version": "v1", "origin": "assertion"},
                {"role": "input", "id": pair["id"], "version": "v1", "origin": "assertion"},
            ],
        }
        derived_all = {
            supportability_finding["id"]: supportability_finding,
            basis["id"]: basis,
        }
        edges = derivation_edges(derived_all)
        self.assertIn(basis["id"], edges[a1["id"]])
        self.assertIn(basis["id"], edges[pair["id"]])

        kernel_findings = {
            a1["id"]: {"id": a1["id"], "fact_id": a1["fact_id"], "value": a1["value"]},
        }
        corrected = dict(kernel_findings)
        corrected["demo.finding.acq.a1-corrected"] = {
            "id": "demo.finding.acq.a1-corrected",
            "fact_id": a1["fact_id"],
            "value": {**a1["value"], ACQUISITION_FIELD: 999.0},
        }
        currency = compute_currency(
            FindingState(fact_state=kernel_facts.initial_state(), findings=corrected)
        )
        self.assertIn(a1["id"], currency.displaced_finding_ids)
        closure, _ = displacement_closure(
            set(currency.displaced_finding_ids), {"derivation": edges}
        )
        self.assertIn(basis["id"], closure)


if __name__ == "__main__":
    unittest.main()
