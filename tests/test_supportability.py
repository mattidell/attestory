"""Seam 3 — Accrued-amount supportability as a pairing-scoped tax rule (ADR-0070).

Synthetic in-repo fixtures only. Proves the production adopted-rule citizen:

- one pairing whose accrued amount is at or under the associated report
  publishes ``true`` through the real ``run()`` loop;
- accrued exceeding the associated report blocks with
  ``ACCRUED_EXCEEDS_ASSOCIATED_REPORT``, and that named code survives to
  the schema-validated derivation-record.v8 ledger;
- an unrelated report of the same type is never consulted (masking);
- two acquisitions sharing one report evaluate independently, never
  cumulatively, even when their sum would exceed the report;
- a correction to either amount re-evaluates (derive, don't cache).

Source findings are marshaled through the real ``marshal_run_context``
collect path. The supportability rule is the committed
``rule-artifact.v7`` citizen and is invoked from ``_Run.attempt``, not as
a standalone function. Accrued amount is the ADR-0067 field-ref on the
acquisition object; the report is production box-1 (a scalar).
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.package_validation import (
    FIELD_REF_UNKNOWN_FIELD,
    check_field_ref_bindings,
)
from packages.derivation.records import RecordStream
from packages.derivation.runner import RunContext, RunResult, run, run_and_record
from packages.kernel.currency import CurrencyView
from packages.kernel.facts import fact_id_for
from packages.kernel.schema_registry import SchemaValidationError
from packages.tax.identity_association import (
    ACQUISITION_FACT_TYPE,
    ASSOCIATION_SYMBOL,
    REPORT_FACT_TYPE,
    associate,
)
from packages.tax.obligation_acquisition_mapping import (
    OBLIGATION_ACQUISITION_FACT_TYPE_ID,
    _CIRCUMSTANCE_VALUE_SCHEMA,
)
from packages.tax.supportability import (
    ACCRUED_EXCEEDS_ASSOCIATED_REPORT,
    ACQUISITION_FIELD,
    COLLECT_SOURCE_NAMES,
    PAIRING_TYPE,
    RULE_ID,
    SUPPORTABILITY_SYMBOL,
    load_rule,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "packages" / "sample_data" / "supportability"
BOX1_BUNDLE = (
    REPO_ROOT / "packages" / "content" / "tax" / "2025" / "f1099int.bundle.json"
)
RULE_CONTENT = (
    REPO_ROOT
    / "packages"
    / "content"
    / "tax"
    / "2025"
    / "rule.relationship.accrued-supported.json"
)

ADOPTION_PIN = {
    "role": "adoption",
    "id": "demo.package.supportability",
    "version": "v1",
}
GOVERNANCE_PINS = [
    {"role": "governance", "id": "governance.constitution", "version": "v1"}
]


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


def _marshal(findings: dict[str, dict[str, Any]], *, rules: list[dict[str, Any]] | None = None) -> RunContext:
    return marshal_run_context(
        run_id="demo.run.supportability",
        state=_State(findings),  # type: ignore[arg-type]
        currency=_currency(list(findings.keys())),
        rules=list(rules) if rules is not None else [load_rule()],
        parameters={},
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=list(GOVERNANCE_PINS),
        collect_source_names=list(COLLECT_SOURCE_NAMES),
    )


def _run(findings: dict[str, dict[str, Any]]) -> RunResult:
    return run(_marshal(findings), DerivationSchemas())


def _pin_ids(finding: dict[str, Any]) -> set[str]:
    return {p["id"] for p in finding["pins"]}


def _acquisition_fact_type() -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": ACQUISITION_FACT_TYPE,
        "version": "v1",
        "title": "Synthetic obligation-acquisition circumstance",
        "nature": "determinable",
        "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
        "value_schema": {
            "type": "object",
            "properties": dict(_CIRCUMSTANCE_VALUE_SCHEMA["properties"]),
            "required": list(_CIRCUMSTANCE_VALUE_SCHEMA["required"]),
        },
        "supersession": {"policy": "free"},
    }


class TestProductionSchemaIds(unittest.TestCase):
    def test_report_type_is_the_published_box1_fact_type(self) -> None:
        bundle = _load(BOX1_BUNDLE)
        ids = {ft["id"] for ft in bundle["fact_types"]}
        self.assertIn(REPORT_FACT_TYPE, ids)
        box1 = next(ft for ft in bundle["fact_types"] if ft["id"] == REPORT_FACT_TYPE)
        self.assertEqual(box1["value_schema"], {"type": "number"})

    def test_acquisition_type_is_seam6_circumstance(self) -> None:
        self.assertEqual(ACQUISITION_FACT_TYPE, OBLIGATION_ACQUISITION_FACT_TYPE_ID)

    def test_pairing_type_is_the_adr0068_association_symbol(self) -> None:
        self.assertEqual(PAIRING_TYPE, ASSOCIATION_SYMBOL)

    def test_committed_rule_is_the_loaded_citizen(self) -> None:
        rule = load_rule()
        self.assertEqual(rule, _load(RULE_CONTENT))
        self.assertEqual(rule["id"], RULE_ID)
        self.assertEqual(rule["schema"], "rule-artifact.v7")
        self.assertEqual(rule["publishes"], SUPPORTABILITY_SYMBOL)

    def test_fixture_fact_ids_compose_from_production_types(self) -> None:
        acq = _example("finding.v2.acquisition-supported.json")
        report = _example("finding.v2.box1-associated.json")
        pairing = _example("finding.v2.pairing-supported.json")
        self.assertEqual(
            acq["fact_id"],
            fact_id_for(
                ACQUISITION_FACT_TYPE,
                (
                    ("payer", "demo.payer.bank-a"),
                    ("reference", "DEMO-BOND-SUP"),
                    ("acquisition-year", "2025"),
                ),
            ),
        )
        self.assertEqual(
            report["fact_id"],
            fact_id_for(
                REPORT_FACT_TYPE,
                (
                    ("payer", "demo.payer.bank-a"),
                    ("statement", "demo.1099int-statement.associated"),
                    ("tax-year", "2025"),
                ),
            ),
        )
        self.assertEqual(
            pairing["fact_id"],
            fact_id_for(
                PAIRING_TYPE,
                (
                    ("left", "DEMO-BOND-SUP"),
                    ("right", "demo.1099int-statement.associated"),
                ),
            ),
        )
        self.assertEqual(pairing["value"]["left_fact_id"], acq["fact_id"])
        self.assertEqual(pairing["value"]["right_fact_id"], report["fact_id"])


class TestPayloadInstantiation(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = DerivationSchemas().registry

    def test_committed_rule_validates_as_rule_artifact_v7(self) -> None:
        rule = load_rule()
        self.registry.validate("rule-artifact.v7", rule)
        self.assertNotIn("literal", json.dumps(rule["value"]))
        left = rule["value"]["when"]["left"]
        self.assertEqual(left["op"], "ref")
        self.assertEqual(left["field"], ACQUISITION_FIELD)
        self.assertEqual(rule["value"]["else"], True)
        self.assertEqual(
            rule["value"]["then"],
            {"op": "block", "code": ACCRUED_EXCEEDS_ASSOCIATED_REPORT},
        )

    def test_literal_else_is_rejected_by_the_real_grammar(self) -> None:
        payload = _negative("rule-artifact.v7.literal-else.json")
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("rule-artifact.v7", payload)

    def test_positive_source_findings_validate_as_finding_v2(self) -> None:
        for name in (
            "finding.v2.acquisition-supported.json",
            "finding.v2.acquisition-sharing.json",
            "finding.v2.box1-associated.json",
            "finding.v2.box1-unrelated.json",
            "finding.v2.pairing-supported.json",
            "finding.v2.pairing-sharing.json",
        ):
            self.registry.validate("finding.v2", _example(name))

    def test_negative_exceeds_findings_validate_as_finding_v2(self) -> None:
        self.registry.validate(
            "finding.v2", _negative("finding.v2.acquisition-exceeds.json")
        )
        self.registry.validate(
            "finding.v2", _negative("finding.v2.pairing-exceeds.json")
        )

    def test_field_ref_is_accepted_against_the_circumstance_schema(self) -> None:
        issues = check_field_ref_bindings(
            load_rule(),
            {ACQUISITION_FACT_TYPE: _acquisition_fact_type()},
            {},
        )
        self.assertEqual(issues, [])

    def test_misspelled_field_fails_closed_at_load_time(self) -> None:
        rule = load_rule()
        rule["value"]["when"]["left"]["field"] = "accrued_interest_paid_to_seler"
        issues = check_field_ref_bindings(
            rule,
            {ACQUISITION_FACT_TYPE: _acquisition_fact_type()},
            {},
        )
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].code, FIELD_REF_UNKNOWN_FIELD)


class TestOnePairingPasses(unittest.TestCase):
    def test_run_publishes_true_for_a_supported_pairing(self) -> None:
        acq = _example("finding.v2.acquisition-supported.json")
        report = _example("finding.v2.box1-associated.json")
        pairing = _example("finding.v2.pairing-supported.json")
        result = _run({acq["id"]: acq, report["id"]: report, pairing["id"]: pairing})
        self.assertEqual(result.blocked, [])
        self.assertEqual(len(result.publications), 1)
        finding = result.publications[0].finding
        self.assertEqual(finding["schema"], "derived-finding.v2")
        self.assertEqual(
            finding["symbol"], f"{SUPPORTABILITY_SYMBOL}|{pairing['fact_id']}"
        )
        self.assertIs(finding["value"], True)
        pins = _pin_ids(finding)
        self.assertIn(acq["id"], pins)
        self.assertIn(report["id"], pins)
        self.assertIn(pairing["id"], pins)
        self.assertIn(RULE_ID, pins)
        published = [
            row for row in result.dispositions if row["disposition"] == "published"
        ]
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0]["artifact_id"], RULE_ID)


class TestAmountExceeds(unittest.TestCase):
    def test_run_blocks_with_the_named_code(self) -> None:
        acq = _negative("finding.v2.acquisition-exceeds.json")
        report = _example("finding.v2.box1-associated.json")
        pairing = _negative("finding.v2.pairing-exceeds.json")
        result = _run({acq["id"]: acq, report["id"]: report, pairing["id"]: pairing})
        self.assertEqual(result.publications, [])
        self.assertEqual(len(result.blocked), 1)
        self.assertEqual(result.blocked[0]["code"], ACCRUED_EXCEEDS_ASSOCIATED_REPORT)
        self.assertEqual(result.blocked[0]["artifact_id"], RULE_ID)
        blocked = [
            row for row in result.dispositions if row["disposition"] == "blocked"
        ]
        self.assertEqual(len(blocked), 1)
        self.assertEqual(blocked[0]["code"], ACCRUED_EXCEEDS_ASSOCIATED_REPORT)

    def test_named_code_survives_the_v8_ledger(self) -> None:
        acq = _negative("finding.v2.acquisition-exceeds.json")
        report = _example("finding.v2.box1-associated.json")
        pairing = _negative("finding.v2.pairing-exceeds.json")
        ctx = _marshal({acq["id"]: acq, report["id"]: report, pairing["id"]: pairing})
        schemas = DerivationSchemas()
        with tempfile.TemporaryDirectory() as tmp:
            stream = RecordStream(Path(tmp) / "workspace", schemas)
            result = run_and_record(
                ctx,
                schemas,
                stream,
                workspace_revision=1,
                adopted_packages={ADOPTION_PIN["id"]},
                start_record_id="demo.start.supportability",
                completion_record_id="demo.done.supportability",
            )
            closing = stream.standings()[ctx.run_id].closing
        assert closing is not None
        self.assertEqual(closing["schema"], "derivation-record.v8")
        self.assertEqual(result.blocked[0]["code"], ACCRUED_EXCEEDS_ASSOCIATED_REPORT)
        ledger = {row["artifact_id"]: row for row in closing["dispositions"]}
        self.assertEqual(ledger[RULE_ID]["disposition"], "blocked")
        self.assertEqual(ledger[RULE_ID]["code"], ACCRUED_EXCEEDS_ASSOCIATED_REPORT)
        self.assertNotEqual(ledger[RULE_ID]["code"], "DEPENDENCY_INVALID")


class TestMasking(unittest.TestCase):
    def test_unrelated_report_of_the_same_type_is_never_consulted(self) -> None:
        acq = _example("finding.v2.acquisition-supported.json")
        associated = _example("finding.v2.box1-associated.json")
        unrelated = _example("finding.v2.box1-unrelated.json")
        pairing = _example("finding.v2.pairing-supported.json")
        findings = {
            acq["id"]: acq,
            associated["id"]: associated,
            unrelated["id"]: unrelated,
            pairing["id"]: pairing,
        }
        ctx = _marshal(findings)
        report_sources = [s for s in ctx.sources if s.name == REPORT_FACT_TYPE]
        self.assertEqual(len(report_sources), 2)

        result = run(ctx, DerivationSchemas())
        self.assertEqual(result.blocked, [])
        self.assertEqual(len(result.publications), 1)
        finding = result.publications[0].finding
        self.assertIs(finding["value"], True)
        pins = _pin_ids(finding)
        self.assertIn(associated["id"], pins)
        self.assertNotIn(unrelated["id"], pins)
        self.assertIn(acq["id"], pins)
        self.assertIn(pairing["id"], pins)


class TestMultipleAcquisitions(unittest.TestCase):
    def test_each_pairing_evaluates_independently_not_cumulatively(self) -> None:
        """Two 600-accrued acquisitions against one 1000 report.

        Individually supportable even though the sum (1200) exceeds the
        report. Each finding pins only its own acquisition.
        """
        acq1 = _example("finding.v2.acquisition-supported.json")
        acq1 = dict(acq1)
        acq1["value"] = dict(acq1["value"])
        acq1["value"]["accrued_interest_paid_to_seller"] = 600.0
        acq2 = _example("finding.v2.acquisition-sharing.json")
        report = _example("finding.v2.box1-associated.json")
        pair1 = _example("finding.v2.pairing-supported.json")
        pair2 = _example("finding.v2.pairing-sharing.json")
        result = _run(
            {
                acq1["id"]: acq1,
                acq2["id"]: acq2,
                report["id"]: report,
                pair1["id"]: pair1,
                pair2["id"]: pair2,
            }
        )
        self.assertEqual(result.blocked, [])
        self.assertEqual(len(result.publications), 2)
        symbols = {pub.finding["symbol"] for pub in result.publications}
        self.assertEqual(
            symbols,
            {
                f"{SUPPORTABILITY_SYMBOL}|{pair1['fact_id']}",
                f"{SUPPORTABILITY_SYMBOL}|{pair2['fact_id']}",
            },
        )
        self.assertTrue(
            all(pub.finding["value"] is True for pub in result.publications)
        )
        for pub in result.publications:
            pins = _pin_ids(pub.finding)
            self.assertFalse({acq1["id"], acq2["id"]} <= pins)
            self.assertIn(report["id"], pins)
            self.assertTrue({acq1["id"], acq2["id"]} & pins)

    def test_one_exceeding_sibling_does_not_block_the_other(self) -> None:
        acq_ok = _example("finding.v2.acquisition-sharing.json")
        acq_bad = _negative("finding.v2.acquisition-exceeds.json")
        report = _example("finding.v2.box1-associated.json")
        pair_ok = _example("finding.v2.pairing-sharing.json")
        pair_bad = _negative("finding.v2.pairing-exceeds.json")
        result = _run(
            {
                acq_ok["id"]: acq_ok,
                acq_bad["id"]: acq_bad,
                report["id"]: report,
                pair_ok["id"]: pair_ok,
                pair_bad["id"]: pair_bad,
            }
        )
        self.assertEqual(len(result.publications), 1)
        self.assertEqual(len(result.blocked), 1)
        self.assertIs(result.publications[0].finding["value"], True)
        self.assertEqual(
            result.blocked[0]["code"], ACCRUED_EXCEEDS_ASSOCIATED_REPORT
        )
        published_pins = _pin_ids(result.publications[0].finding)
        self.assertIn(acq_ok["id"], published_pins)
        self.assertNotIn(acq_bad["id"], published_pins)


class TestCorrectionReevaluates(unittest.TestCase):
    def test_report_correction_changes_the_verdict(self) -> None:
        acq = _example("finding.v2.acquisition-supported.json")
        report = _example("finding.v2.box1-associated.json")
        pairing = _example("finding.v2.pairing-supported.json")
        before = _run({acq["id"]: acq, report["id"]: report, pairing["id"]: pairing})
        self.assertEqual(len(before.publications), 1)
        self.assertIs(before.publications[0].finding["value"], True)

        corrected = dict(report)
        corrected["id"] = "demo.finding.box1.associated-corrected"
        corrected["value"] = 100.0
        after = _run({acq["id"]: acq, corrected["id"]: corrected, pairing["id"]: pairing})
        self.assertEqual(after.publications, [])
        self.assertEqual(len(after.blocked), 1)
        self.assertEqual(after.blocked[0]["code"], ACCRUED_EXCEEDS_ASSOCIATED_REPORT)

    def test_acquisition_correction_changes_the_verdict(self) -> None:
        acq = _example("finding.v2.acquisition-supported.json")
        report = _example("finding.v2.box1-associated.json")
        pairing = _example("finding.v2.pairing-supported.json")
        before = _run({acq["id"]: acq, report["id"]: report, pairing["id"]: pairing})
        self.assertEqual(len(before.publications), 1)

        corrected = dict(acq)
        corrected["id"] = "demo.finding.acq.supported-corrected"
        value = dict(acq["value"])
        value["accrued_interest_paid_to_seller"] = 1500.0
        corrected["value"] = value
        after = _run(
            {corrected["id"]: corrected, report["id"]: report, pairing["id"]: pairing}
        )
        self.assertEqual(after.publications, [])
        self.assertEqual(after.blocked[0]["code"], ACCRUED_EXCEEDS_ASSOCIATED_REPORT)
        self.assertNotEqual(
            before.publications[0].finding["id"],
            after.blocked[0].get("pairing_fact_id"),
        )


class TestConsumesAssociationProducer(unittest.TestCase):
    def test_associate_publications_drive_supportability(self) -> None:
        """ADR-0068 publications are the pairing sources the rule consumes."""
        from packages.derivation.runner import SourceFact

        acq = _example("finding.v2.acquisition-supported.json")
        report = _example("finding.v2.box1-associated.json")
        assoc = associate(
            sources=_marshal(
                {acq["id"]: acq, report["id"]: report}, rules=[]
            ).sources,
            registry=DerivationSchemas().registry,
            adoption_pin=ADOPTION_PIN,
            reporting_year=2025,
        )
        self.assertEqual(len(assoc.publications), 1)
        pairing_pub = assoc.publications[0]
        pairing_source = SourceFact(
            name=PAIRING_TYPE,
            value=json.dumps(pairing_pub["value"], sort_keys=True),
            finding_id=pairing_pub["id"],
            fact_id=pairing_pub["id"],
        )
        ctx = _marshal({acq["id"]: acq, report["id"]: report})
        ctx = RunContext(
            run_id=ctx.run_id,
            rules=ctx.rules,
            parameters=ctx.parameters,
            canon=ctx.canon,
            inputs=list(ctx.inputs),
            sources=[*ctx.sources, pairing_source],
            adoption_pin=ctx.adoption_pin,
            governance_pins=list(ctx.governance_pins),
        )
        result = run(ctx, DerivationSchemas())
        self.assertEqual(result.blocked, [])
        self.assertEqual(len(result.publications), 1)
        self.assertIs(result.publications[0].finding["value"], True)
        pins = _pin_ids(result.publications[0].finding)
        self.assertIn(pairing_pub["id"], pins)
        self.assertIn(acq["id"], pins)
        self.assertIn(report["id"], pins)


class TestLiveCollectNames(unittest.TestCase):
    def test_resolved_run_material_collects_pairing_and_peer_types(self) -> None:
        from packages.derivation.live import _resolved_run_material

        class _Graph:
            resolved_members = (load_rule(),)
            package: dict[str, Any] = {"input_bindings": []}

        _, _, _, _, _, _, collect_names = _resolved_run_material(_Graph())
        for name in COLLECT_SOURCE_NAMES:
            self.assertIn(name, collect_names)


class TestAuthorizationIsOnThePairingEnvironment(unittest.TestCase):
    def test_run_environment_authorization_is_visible_to_evaluate_one(self) -> None:
        from packages.derivation.authorization import (
            STATUS_ADMITTED,
            AuthorizationResolution,
        )

        acq = _example("finding.v2.acquisition-supported.json")
        report = _example("finding.v2.box1-associated.json")
        pairing = _example("finding.v2.pairing-supported.json")
        admitted = AuthorizationResolution(STATUS_ADMITTED, "demo.auth.g1")
        ctx = _marshal({acq["id"]: acq, report["id"]: report, pairing["id"]: pairing})
        ctx = RunContext(
            run_id=ctx.run_id,
            rules=ctx.rules,
            parameters=ctx.parameters,
            canon=ctx.canon,
            inputs=list(ctx.inputs),
            sources=list(ctx.sources),
            adoption_pin=ctx.adoption_pin,
            governance_pins=list(ctx.governance_pins),
            authorization=admitted,
        )
        result = run(ctx, DerivationSchemas())
        self.assertEqual(len(result.publications), 1)
        self.assertIs(result.publications[0].finding["value"], True)


if __name__ == "__main__":
    unittest.main()
