"""Nominee-Allocation Assertion Recording, Track 2: recovery, join, coexistence.

Track 1 already persists through ``assert_nominee_allocation`` and
``retract_nominee_allocation``. Nothing here rebuilds that boundary or
re-proves that it persists. Every allocation below is written through those
named helpers onto a real ``ActLog``; recovery then discards in-memory state
and rebuilds from the committed log only.

The named synthetic workspace used for coexistence and neighbouring-surface
checks is ``demo.nominee-allocation.track2.coexistence``. Legacy artifacts
are committed and executable; tests admit them through ``bundle-adoption``.
Nothing here claims real-workspace or production-package adoption.

The milestone plan names no neighbouring surface beyond
``untranslated_source_findings`` and the legacy Schedule B nominee subtotal.
This file tests those two and does not invent a third.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_run_context
from packages.derivation.runner import RunContext, RunResult, run
from packages.kernel.act_log import ActLog
from packages.kernel.currency import CurrencyView, compute_currency
from packages.kernel.findings import project
from packages.tax import nominee_allocation_recording as nar
from packages.tax.coverage import untranslated_source_findings
from packages.tax.loader import TAX_CONTENT_DIR, load_nominee_allocation_bundle, tax_registry
from packages.tax.nominee_allocation_recovery import (
    NomineeAllocationInvariantError,
    NomineeAllocationRecoveryView,
    recover_nominee_allocations,
    unique_current_finding_id,
)
from packages.tax.report_statement_identity import (
    build_1099int_report_contribution,
    build_1099int_report_entity_acts,
    derive_1099int_box1_fact_id,
    derive_reported_payer_entity_id,
    derive_reported_statement_entity_id,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

PAYER = "Demo Savings Bank"
STMT_A = "demo-nominee-alloc-stmt-a"
YEAR = 2025

MATT = "demo.user.matt"
ALEX = "demo.user.alex"

PAT_ID = "demo.alloc.recipient.pat"
KIM_ID = "demo.alloc.recipient.kim"
PAT_LABEL = "Pat (allocation recipient)"
KIM_LABEL = "Kim (allocation recipient)"

BOX1_FAMILY_PREDECESSOR = "demo.nominee-alloc.int-b1.h0"
BOX1_FAMILY_SUCCESSOR = "demo.nominee-alloc.int-b1.h1"
REPORT_EVIDENCE_ID = "demo.evidence.nominee-alloc.report-copy"
LEGACY_EVIDENCE_ID = "demo.evidence.nominee-alloc.legacy-adjustment"

LEGACY_FACT_TYPE_ID = "tax.us.2025.scheduleb.adjustment.nominee.amount"
LEGACY_FAMILY_ID = "tax.us.2025.scheduleb.adjustment.nominee"
LEGACY_CLOSURE_TYPE_ID = "tax.us.2025.scheduleb.adjustment.nominee.source-closure"
LEGACY_INSTANCE_ID = "demo.track2.nominee.instance.0"
LEGACY_HORIZON_H0 = "demo.track2.nominee.h0"
LEGACY_HORIZON_H1 = "demo.track2.nominee.h1"
LEGACY_AMOUNT = 150.6
LEGACY_WORKSPACE_NAME = "demo.nominee-allocation.track2.coexistence"
LEGACY_SUBTOTAL_SYMBOL = "tax.us.2025.interest.scheduleb-nominee-subtotal"
LEGACY_ADOPTION_PIN = {
    "role": "adoption",
    "id": "demo.package.nominee-allocation.legacy-coexistence",
    "version": "v1",
}
LEGACY_GOVERNANCE_PINS = [
    {"role": "governance", "id": "governance.constitution", "version": "v1"}
]

NAMED_LEGACY_MEMBERS = (
    "family.scheduleb-adjustment.nominee.json",
    "closure-mapping.scheduleb-adjustment.nominee.json",
    "rule.scheduleb-adjustment.nominee-subtotal.json",
    "rule.attachment.schedule-b.v4.json",
    "rule.attachment.schedule-b.v5.json",
)


def _at(n: int) -> str:
    return f"2026-09-07T04:{n // 60:02d}:{n % 60:02d}Z"


class _Workspace:
    """A real ``ActLog`` over a temp directory. Production writes go through
    Track 1's named helpers; this class only bootstraps fixtures."""

    def __init__(self, tmp_root: Path, *, workspace_name: str = "demo.workspace") -> None:
        self.registry = tax_registry()
        self.allocation_bundle = load_nominee_allocation_bundle(self.registry)
        self.log = ActLog(tmp_root / workspace_name, self.registry)
        self.revision = 0

    def append(self, kind: str, payload: dict[str, Any], *, actor: str = "demo.workspace-boot") -> dict[str, Any]:
        self.revision = self.log.read().revision
        act = {
            "schema": "act.v1",
            "act_id": f"demo.boot-{self.revision:04d}-{kind}",
            "kind": kind,
            "actor": actor,
            "at": _at(self.revision),
            "committed_against": self.revision,
            "payload": payload,
        }
        self.revision = self.log.append(act, expected_revision=self.revision)
        return act

    def state(self) -> Any:
        return project(self.log.read().acts, self.registry)


def _load_content(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((TAX_CONTENT_DIR / name).read_text("utf-8"))
    return loaded


def _named_legacy_members() -> list[dict[str, Any]]:
    return [_load_content(name) for name in NAMED_LEGACY_MEMBERS]


def _build_workspace(
    tmp_root: Path,
    *,
    workspace_name: str = "demo.workspace",
    contribute_box1: bool = True,
    adopt_legacy: bool = False,
) -> _Workspace:
    ws = _Workspace(tmp_root, workspace_name=workspace_name)
    ws.append("bundle-adoption", {"bundle": ws.allocation_bundle})
    ws.append("bundle-adoption", {"bundle": _load_content("f1099int.bundle.json")})
    if adopt_legacy:
        ws.append(
            "bundle-adoption",
            {"bundle": _load_content("scheduleb-adjustment.nominee.bundle.json")},
        )
        ws.append(
            "bundle-adoption",
            {"bundle": _load_content("core_calculations.bundle.v2.json")},
        )
    seen: set[str] = set()
    for entity_act in build_1099int_report_entity_acts(
        payer_name=PAYER, statement_reference=STMT_A, act_index=0
    ):
        eid = entity_act["payload"]["entity"]["id"]
        if eid in seen:
            continue
        seen.add(eid)
        ws.append("entity-introduced", entity_act["payload"])
    ws.append(
        "horizon-genesis",
        {
            "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
            "scope": {"tax-year": str(YEAR), "subject": "demo.primary"},
            "horizon_id": BOX1_FAMILY_PREDECESSOR,
        },
    )
    ws.append(
        "evidence-submitted",
        {
            "evidence": {
                "schema": "evidence.v1",
                "id": REPORT_EVIDENCE_ID,
                "kind": "demo.report-1099int-copy",
                "label": "Synthetic Form 1099-INT copy",
                "content": {
                    "mode": nar.DOCUMENT_REPORT_EVIDENCE_MODE,
                    "synthetic": True,
                },
            }
        },
    )
    if contribute_box1:
        _contribute_box1_report(ws)
    if adopt_legacy:
        _contribute_legacy_nominee_adjustment(ws)
    return ws


def _contribute_box1_report(ws: _Workspace, *, amount: float = 1200.0) -> None:
    built = build_1099int_report_contribution(
        payer_name=PAYER,
        statement_reference=STMT_A,
        tax_year=YEAR,
        amount=amount,
        scope={"tax-year": str(YEAR), "subject": "demo.primary"},
        family_predecessor_id=BOX1_FAMILY_PREDECESSOR,
        family_successor_id=BOX1_FAMILY_SUCCESSOR,
        act_index=0,
        contribution_id="demo.c.box1.a",
        evidence_id=REPORT_EVIDENCE_ID,
        finding_id="demo.box1.a.first",
        committed_against=0,
    )
    ws.append("contribution", built.contribution_act["payload"])
    ws.append("member-transition", built.member_transition_act["payload"])


def _contribute_legacy_nominee_adjustment(ws: _Workspace) -> None:
    # The legacy Schedule B nominee adjustment is one submitted batch of its
    # own; it does not share evidence with the new per-event allocation
    # assertions recorded later in the same workspace.
    ws.append(
        "evidence-submitted",
        {
            "evidence": {
                "schema": "evidence.v1",
                "id": LEGACY_EVIDENCE_ID,
                "kind": "demo.ordinary-allocation-interview",
                "label": "Synthetic ordinary-language legacy nominee adjustment",
                "content": {
                    "mode": nar.ORDINARY_LANGUAGE_EVIDENCE_MODE,
                    "synthetic": True,
                },
            }
        },
    )
    ws.append(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": LEGACY_INSTANCE_ID,
                "kind": "tax.us.scheduleb-adjustment-instance",
                "label": "Synthetic Schedule B nominee adjustment instance",
            }
        },
    )
    ws.append(
        "horizon-genesis",
        {
            "family": {"id": LEGACY_FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": str(YEAR), "subject": "demo.primary"},
            "horizon_id": LEGACY_HORIZON_H0,
        },
    )
    legacy_fact_id = (
        f"{LEGACY_FACT_TYPE_ID}|tax-year={YEAR},adjustment-instance={LEGACY_INSTANCE_ID}"
    )
    finding = {
        "schema": "finding.v2",
        "id": "demo.legacy.nominee.amount",
        "fact_id": legacy_fact_id,
        "value": LEGACY_AMOUNT,
        "basis": "attested",
        "evidence_ids": [LEGACY_EVIDENCE_ID],
        "contribution_id": "demo.c.legacy.nominee",
    }
    ws.append(
        "contribution",
        {
            "contribution": {
                "schema": "contribution.v1",
                "id": "demo.c.legacy.nominee",
                "evidence_id": LEGACY_EVIDENCE_ID,
                "content": {"mode": "ordinary-language-entry", "synthetic": True},
            }
        },
    )
    ws.append(
        "member-transition",
        {
            "family": {"id": LEGACY_FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": str(YEAR), "subject": "demo.primary"},
            "member": {"action": "assert", "finding": finding},
            "successor": {"id": LEGACY_HORIZON_H1, "predecessor": LEGACY_HORIZON_H0},
        },
    )
    closure_fact_id = (
        f"{LEGACY_CLOSURE_TYPE_ID}|family-horizon={LEGACY_HORIZON_H1},tax-year={YEAR}"
    )
    ws.append(
        "contribution",
        {
            "contribution": {
                "schema": "contribution.v1",
                "id": "demo.c.legacy.closure",
                "evidence_id": LEGACY_EVIDENCE_ID,
                "content": {"mode": "ordinary-language-entry", "synthetic": True},
            }
        },
    )
    ws.append(
        "assertion",
        {
            "finding": {
                "schema": "finding.v2",
                "id": "demo.legacy.nominee.closure",
                "fact_id": closure_fact_id,
                "value": True,
                "basis": "attested",
                "evidence_ids": [LEGACY_EVIDENCE_ID],
                "contribution_id": "demo.c.legacy.closure",
            }
        },
    )
    ws.append(
        "assertion",
        {
            "finding": {
                "schema": "finding.v2",
                "id": "demo.legacy.rounding",
                "fact_id": f"rounding.convention|tax-year={YEAR}",
                "value": "half_up",
                "basis": "attested",
                "evidence_ids": [],
            }
        },
    )


def _allocation_answers(
    *,
    recipient_id: str,
    amount: float,
    recipient_display_label: str | None = None,
) -> dict[str, Any]:
    answers: dict[str, Any] = {
        "circumstance": nar.ALLOCATION_CIRCUMSTANCE,
        "payer_name": PAYER,
        "statement_reference": STMT_A,
        "tax_year": YEAR,
        "recipient_id": recipient_id,
        "amount": amount,
    }
    if recipient_display_label is not None:
        answers["recipient_display_label"] = recipient_display_label
    return answers


def _ordinary_evidence_id(finding_id: str) -> str:
    return f"demo.evidence.{finding_id}"


def _submit_ordinary_allocation_evidence(
    ws: _Workspace, *, evidence_id: str, answers: Mapping[str, Any]
) -> None:
    """One submitted ordinary-language answer event.

    Distinct assertions, corrections, and reassertions each get their own
    evidence citizen. The evidence retains the submitted answers; synthetic
    fixtures identify themselves here.
    """
    ws.append(
        "evidence-submitted",
        {
            "evidence": {
                "schema": "evidence.v1",
                "id": evidence_id,
                "kind": "demo.ordinary-allocation-interview",
                "label": "Synthetic ordinary-language allocation interview",
                "content": {
                    "mode": nar.ORDINARY_LANGUAGE_EVIDENCE_MODE,
                    "synthetic": True,
                    "answers": dict(answers),
                },
            }
        },
    )


def _assert_allocation(
    ws: _Workspace,
    *,
    recipient_id: str,
    amount: float,
    actor: str,
    at: str,
    finding_id: str,
    label: str | None = None,
) -> str:
    answers = _allocation_answers(
        recipient_id=recipient_id,
        amount=amount,
        recipient_display_label=label,
    )
    evidence_id = _ordinary_evidence_id(finding_id)
    _submit_ordinary_allocation_evidence(ws, evidence_id=evidence_id, answers=answers)
    nar.assert_nominee_allocation(
        ws.log,
        ws.registry,
        answers=answers,
        actor=actor,
        at=at,
        evidence_id=evidence_id,
        contribution_id=f"demo.c.{finding_id}",
        finding_id=finding_id,
        record_id=f"demo.r.{finding_id}",
        contribution_act_id=f"demo.a.{finding_id}.contrib",
        assertion_act_id=f"demo.a.{finding_id}.assert",
    )
    return evidence_id


def _recover(ws: _Workspace) -> NomineeAllocationRecoveryView:
    contents = ws.log.read()
    return recover_nominee_allocations(contents.acts, ws.registry)


def _execute_legacy_nominee_subtotal(
    state: Any,
) -> tuple[RunContext, RunResult]:
    """The committed nominee-subtotal through projection, marshalling, admission, and run.

    Uses the real ``FindingState`` (already projected from the committed log),
    ``marshal_run_context``, runner closure admission, and ``run()`` of the
    committed ``rule.scheduleb-adjustment.nominee-subtotal`` citizen. This is
    not expression arithmetic over a hand-built ``Environment``.
    """
    currency = compute_currency(state)
    rule = _load_content("rule.scheduleb-adjustment.nominee-subtotal.json")
    family = _load_content("family.scheduleb-adjustment.nominee.json")
    mapping = _load_content("closure-mapping.scheduleb-adjustment.nominee.json")
    bundle = _load_content("scheduleb-adjustment.nominee.bundle.json")
    ctx = marshal_run_context(
        run_id="demo.run.nominee-allocation.legacy-subtotal",
        state=state,
        currency=currency,
        rules=[rule],
        parameters={},
        canon=load_canon(DerivationSchemas()),
        adoption_pin=dict(LEGACY_ADOPTION_PIN),
        governance_pins=[dict(pin) for pin in LEGACY_GOVERNANCE_PINS],
        family_declarations=[family],
        closure_mappings=[mapping],
        fact_types=list(bundle["fact_types"]),
        collect_source_names=[LEGACY_FACT_TYPE_ID],
    )
    return ctx, run(ctx, DerivationSchemas())


def _published_legacy_subtotal(result: RunResult) -> Decimal:
    if result.blocked:
        raise AssertionError(f"legacy subtotal blocked: {result.blocked!r}")
    raw = result.symbols.get(LEGACY_SUBTOTAL_SYMBOL)
    if raw is None:
        raise AssertionError(
            f"legacy subtotal symbol missing; published={list(result.symbols)}"
        )
    return Decimal(str(raw))


def _legacy_dependency_set(result: RunResult) -> tuple[tuple[str, str, str], ...]:
    publications = [
        pub for pub in result.publications
        if pub.finding.get("symbol") == LEGACY_SUBTOTAL_SYMBOL
    ]
    if len(publications) != 1:
        raise AssertionError(
            f"expected one legacy-subtotal publication, got {len(publications)}"
        )
    pins = publications[0].finding.get("pins") or []
    return tuple(
        sorted(
            (str(pin.get("role")), str(pin.get("id")), str(pin.get("version")))
            for pin in pins
        )
    )


def _consumed_finding_ids(ctx: RunContext) -> frozenset[str]:
    from_inputs = {inp.finding_id for inp in ctx.inputs}
    from_sources = {source.finding_id for source in ctx.sources}
    return frozenset(from_inputs | from_sources)


class LogOnlyRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ws = _build_workspace(Path(self._tmp.name))
        _assert_allocation(
            self.ws,
            recipient_id=PAT_ID,
            amount=300,
            actor=MATT,
            at=_at(100),
            finding_id="demo.f.pat.1",
            label=PAT_LABEL,
        )
        _assert_allocation(
            self.ws,
            recipient_id=KIM_ID,
            amount=200,
            actor=MATT,
            at=_at(101),
            finding_id="demo.f.kim.1",
            label=KIM_LABEL,
        )

    def test_log_only_recovery_rebuilds_current_allocations_labels_attribution_and_join(self) -> None:
        log = self.ws.log
        registry = self.ws.registry
        expected_pat = nar.derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR, recipient_id=PAT_ID
        )
        expected_kim = nar.derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR, recipient_id=KIM_ID
        )
        expected_report = derive_1099int_box1_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR
        )
        # Discard in-memory workspace state. Recovery may use the committed
        # log only.
        del self.ws

        view = recover_nominee_allocations(log.read().acts, registry)
        by_recipient = {record.recipient_id: record for record in view.current}
        self.assertEqual(set(by_recipient), {PAT_ID, KIM_ID})

        pat = by_recipient[PAT_ID]
        self.assertEqual(pat.fact_id, expected_pat)
        self.assertEqual(pat.amount, 300)
        self.assertEqual(pat.recipient_display_label, PAT_LABEL)
        self.assertEqual(pat.payer_id, derive_reported_payer_entity_id(PAYER))
        self.assertEqual(
            pat.statement_id,
            derive_reported_statement_entity_id(
                payer_name=PAYER, statement_reference=STMT_A
            ),
        )
        self.assertEqual(pat.tax_year, str(YEAR))
        self.assertEqual(pat.current_finding_id, "demo.f.pat.1")
        self.assertEqual(pat.assertion_act_id, "demo.a.demo.f.pat.1.assert")
        self.assertEqual(pat.assertion_actor, MATT)
        self.assertEqual(pat.assertion_at, _at(100))
        self.assertEqual(pat.contribution_id, "demo.c.demo.f.pat.1")
        self.assertEqual(pat.evidence_ids, (_ordinary_evidence_id("demo.f.pat.1"),))
        self.assertEqual(pat.report_fact_id, expected_report)
        self.assertEqual(pat.current_report_finding_id, "demo.box1.a.first")
        self.assertFalse(hasattr(pat, "report_value"))

        kim = by_recipient[KIM_ID]
        self.assertEqual(kim.fact_id, expected_kim)
        self.assertEqual(kim.amount, 200)
        self.assertEqual(kim.recipient_display_label, KIM_LABEL)
        self.assertEqual(kim.current_finding_id, "demo.f.kim.1")
        self.assertEqual(kim.assertion_actor, MATT)
        self.assertEqual(kim.evidence_ids, (_ordinary_evidence_id("demo.f.kim.1"),))
        self.assertNotEqual(pat.evidence_ids, kim.evidence_ids)
        self.assertEqual(kim.report_fact_id, expected_report)
        self.assertEqual(kim.current_report_finding_id, "demo.box1.a.first")
        self.assertEqual(view.retracted, ())


class MissingReportJoinTests(unittest.TestCase):
    def test_allocation_current_with_no_current_box1_finding_stays_recoverable(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = _build_workspace(Path(tmp.name), contribute_box1=False)
        _assert_allocation(
            ws,
            recipient_id=PAT_ID,
            amount=300,
            actor=MATT,
            at=_at(100),
            finding_id="demo.f.pat.1",
            label=PAT_LABEL,
        )
        view = _recover(ws)
        self.assertEqual(len(view.current), 1)
        record = view.current[0]
        expected_report = derive_1099int_box1_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR
        )
        self.assertEqual(record.report_fact_id, expected_report)
        self.assertIsNone(record.current_report_finding_id)
        self.assertEqual(record.amount, 300)
        self.assertEqual(record.recipient_display_label, PAT_LABEL)
        self.assertEqual(record.assertion_actor, MATT)
        self.assertFalse(hasattr(record, "report_value"))
        # No successful current-value join is reported: the box-1 finding
        # is absent, and recovery does not substitute a historical value.
        state = project(ws.log.read().acts, ws.registry)
        currency = compute_currency(state)
        box1_current = [
            fid
            for fid in currency.current_finding_ids
            if state.findings[fid]["fact_id"] == expected_report
        ]
        self.assertEqual(box1_current, [])


class DuplicateCurrentReportTests(unittest.TestCase):
    def test_more_than_one_current_box1_finding_is_refused_not_picked(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = _build_workspace(Path(tmp.name))
        _assert_allocation(
            ws,
            recipient_id=PAT_ID,
            amount=300,
            actor=MATT,
            at=_at(100),
            finding_id="demo.f.pat.1",
            label=PAT_LABEL,
        )
        state = project(ws.log.read().acts, ws.registry)
        report_fact_id = derive_1099int_box1_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR
        )
        original = unique_current_finding_id(report_fact_id, state, compute_currency(state))
        self.assertEqual(original, "demo.box1.a.first")

        duplicate_finding = dict(state.findings["demo.box1.a.first"])
        duplicate_finding["id"] = "demo.box1.a.duplicate"
        duplicated_state = replace(
            state,
            findings={**state.findings, "demo.box1.a.duplicate": duplicate_finding},
        )
        # Standing is still defined by a CurrencyView: this case is the
        # invariant the join must refuse if that view ever names two current
        # findings for one box-1 fact identity. compute_currency itself
        # displaces a later same-fact finding, so the refusal cannot be
        # reached through a well-formed log; the join still must not pick.
        two_current = CurrencyView(
            current_finding_ids=frozenset({"demo.box1.a.first", "demo.box1.a.duplicate"}),
            displaced_finding_ids=frozenset(),
            current_evidence_ids=frozenset(),
            displaced_evidence_ids=frozenset(),
        )
        with self.assertRaises(NomineeAllocationInvariantError) as ctx:
            unique_current_finding_id(report_fact_id, duplicated_state, two_current)
        message = str(ctx.exception)
        self.assertIn(report_fact_id, message)
        self.assertIn("demo.box1.a.first", message)
        self.assertIn("demo.box1.a.duplicate", message)
        self.assertIn("refusing rather than picking one", message)


class AttributionTests(unittest.TestCase):
    def test_a6_a11_recovers_current_and_historical_with_distinct_actors(self) -> None:
        """Assert, retract under a different actor, then assert again.

        Recovery must show the new current assertion AND the historical
        retracted assertion, with assertion and retraction actors separately
        recoverable and distinct. Nothing may claim the original actor recanted.
        """
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = _build_workspace(Path(tmp.name))
        _assert_allocation(
            ws,
            recipient_id=PAT_ID,
            amount=300,
            actor=MATT,
            at=_at(100),
            finding_id="demo.f.pat.1",
            label=PAT_LABEL,
        )
        _assert_allocation(
            ws,
            recipient_id=KIM_ID,
            amount=200,
            actor=MATT,
            at=_at(101),
            finding_id="demo.f.kim.1",
            label=KIM_LABEL,
        )
        nar.retract_nominee_allocation(
            ws.log,
            ws.registry,
            finding_id="demo.f.pat.1",
            actor=ALEX,
            at=_at(102),
            act_id="demo.a.pat.retract",
        )
        _assert_allocation(
            ws,
            recipient_id=PAT_ID,
            amount=275,
            actor=MATT,
            at=_at(103),
            finding_id="demo.f.pat.2",
        )

        view = _recover(ws)
        by_recipient = {record.recipient_id: record for record in view.current}
        self.assertEqual(set(by_recipient), {PAT_ID, KIM_ID})

        current_pat = by_recipient[PAT_ID]
        self.assertEqual(current_pat.amount, 275)
        self.assertEqual(current_pat.current_finding_id, "demo.f.pat.2")
        self.assertEqual(current_pat.assertion_act_id, "demo.a.demo.f.pat.2.assert")
        self.assertEqual(current_pat.assertion_actor, MATT)
        self.assertEqual(current_pat.assertion_at, _at(103))
        self.assertEqual(current_pat.contribution_id, "demo.c.demo.f.pat.2")
        self.assertEqual(current_pat.evidence_ids, (_ordinary_evidence_id("demo.f.pat.2"),))
        self.assertEqual(current_pat.recipient_display_label, PAT_LABEL)

        kim = by_recipient[KIM_ID]
        self.assertEqual(kim.assertion_actor, MATT)
        self.assertEqual(kim.current_finding_id, "demo.f.kim.1")

        self.assertEqual(len(view.retracted), 1)
        retracted = view.retracted[0]
        self.assertEqual(retracted.finding_id, "demo.f.pat.1")
        self.assertEqual(retracted.fact_id, current_pat.fact_id)
        self.assertEqual(retracted.payer_id, current_pat.payer_id)
        self.assertEqual(retracted.statement_id, current_pat.statement_id)
        self.assertEqual(retracted.tax_year, current_pat.tax_year)
        self.assertEqual(retracted.recipient_id, PAT_ID)
        self.assertEqual(retracted.recipient_display_label, PAT_LABEL)
        self.assertEqual(retracted.amount, 300)
        self.assertEqual(retracted.assertion_act_id, "demo.a.demo.f.pat.1.assert")
        self.assertEqual(retracted.assertion_actor, MATT)
        self.assertEqual(retracted.assertion_at, _at(100))
        self.assertEqual(retracted.contribution_id, "demo.c.demo.f.pat.1")
        self.assertEqual(retracted.evidence_ids, (_ordinary_evidence_id("demo.f.pat.1"),))
        self.assertNotEqual(current_pat.evidence_ids, retracted.evidence_ids)
        self.assertEqual(retracted.retraction_act_id, "demo.a.pat.retract")
        self.assertEqual(retracted.retraction_actor, ALEX)
        self.assertEqual(retracted.retraction_at, _at(102))
        self.assertEqual(retracted.report_fact_id, current_pat.report_fact_id)
        self.assertEqual(
            retracted.current_report_finding_id, current_pat.current_report_finding_id
        )
        self.assertEqual(retracted.current_report_finding_id, "demo.box1.a.first")
        self.assertNotEqual(retracted.assertion_actor, retracted.retraction_actor)
        self.assertNotEqual(MATT, ALEX)
        self.assertFalse(hasattr(retracted, "recanted"))
        self.assertFalse(hasattr(retracted, "original_actor_recanted"))
        # The later current assertion is a new act; the retracted assertion
        # remains Matt's. Alex ended current support. Nothing equates those.
        self.assertEqual(current_pat.assertion_actor, MATT)
        self.assertNotEqual(current_pat.assertion_act_id, retracted.assertion_act_id)

    def test_correction_and_cross_actor_cases_retain_distinct_evidence_ids(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = _build_workspace(Path(tmp.name))
        initial_evidence = _assert_allocation(
            ws,
            recipient_id=PAT_ID,
            amount=300,
            actor=MATT,
            at=_at(100),
            finding_id="demo.f.pat.1",
            label=PAT_LABEL,
        )
        correction_evidence = _assert_allocation(
            ws,
            recipient_id=PAT_ID,
            amount=250,
            actor=MATT,
            at=_at(101),
            finding_id="demo.f.pat.2",
        )
        cross_actor_evidence = _assert_allocation(
            ws,
            recipient_id=PAT_ID,
            amount=275,
            actor=ALEX,
            at=_at(102),
            finding_id="demo.f.pat.alex",
        )
        self.assertNotEqual(initial_evidence, correction_evidence)
        self.assertNotEqual(correction_evidence, cross_actor_evidence)
        self.assertNotEqual(initial_evidence, cross_actor_evidence)

        view = _recover(ws)
        self.assertEqual(len(view.current), 1)
        current = view.current[0]
        self.assertEqual(current.current_finding_id, "demo.f.pat.alex")
        self.assertEqual(current.assertion_actor, ALEX)
        self.assertEqual(current.amount, 275)
        self.assertEqual(current.evidence_ids, (cross_actor_evidence,))
        self.assertNotEqual(current.evidence_ids, (initial_evidence,))
        self.assertNotEqual(current.evidence_ids, (correction_evidence,))

        state = project(ws.log.read().acts, ws.registry)
        self.assertEqual(
            tuple(state.findings["demo.f.pat.1"]["evidence_ids"]),
            (initial_evidence,),
        )
        self.assertEqual(
            tuple(state.findings["demo.f.pat.2"]["evidence_ids"]),
            (correction_evidence,),
        )
        self.assertEqual(
            tuple(state.findings["demo.f.pat.alex"]["evidence_ids"]),
            (cross_actor_evidence,),
        )


class LegacyCoexistenceTests(unittest.TestCase):
    """Execution in the named synthetic workspace, plus a structural check
    scoped to what this track introduced — not a universal negative over
    every historical artifact."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ws = _build_workspace(
            Path(self._tmp.name),
            workspace_name=LEGACY_WORKSPACE_NAME,
            adopt_legacy=True,
        )

    def test_legacy_adjustment_and_allocation_coexist_with_unchanged_subtotal(self) -> None:
        before_state = project(self.ws.log.read().acts, self.ws.registry)
        before_ctx, before_result = _execute_legacy_nominee_subtotal(before_state)
        before_subtotal = _published_legacy_subtotal(before_result)
        before_deps = _legacy_dependency_set(before_result)
        before_consumed = _consumed_finding_ids(before_ctx)
        self.assertEqual(before_subtotal, Decimal("151"))
        self.assertIn("demo.legacy.nominee.amount", before_consumed)
        legacy_finding = before_state.findings["demo.legacy.nominee.amount"]
        self.assertEqual(legacy_finding["value"], LEGACY_AMOUNT)

        _assert_allocation(
            self.ws,
            recipient_id=PAT_ID,
            amount=300,
            actor=MATT,
            at=_at(100),
            finding_id="demo.f.pat.1",
            label=PAT_LABEL,
        )

        after_acts = self.ws.log.read().acts
        after_state = project(after_acts, self.ws.registry)
        after_currency = compute_currency(after_state)
        after_ctx, after_result = _execute_legacy_nominee_subtotal(after_state)
        after_subtotal = _published_legacy_subtotal(after_result)
        after_deps = _legacy_dependency_set(after_result)
        after_consumed = _consumed_finding_ids(after_ctx)

        self.assertEqual(after_subtotal, before_subtotal)
        self.assertEqual(after_subtotal, Decimal("151"))
        self.assertEqual(after_deps, before_deps)
        self.assertEqual(
            after_state.findings["demo.legacy.nominee.amount"]["value"],
            LEGACY_AMOUNT,
        )
        self.assertEqual(
            after_state.findings["demo.legacy.nominee.amount"],
            legacy_finding,
        )
        recovered = recover_nominee_allocations(after_acts, self.ws.registry)
        self.assertEqual(len(recovered.current), 1)
        self.assertEqual(recovered.current[0].amount, 300)
        self.assertIn("demo.legacy.nominee.amount", after_currency.current_finding_ids)
        self.assertIn("demo.f.pat.1", after_currency.current_finding_ids)
        # The new allocation is neither consumed as a collect source or
        # input nor pinned as a dependency of the legacy subtotal.
        self.assertNotIn("demo.f.pat.1", after_consumed)
        self.assertNotIn(
            ("input", "demo.f.pat.1", "v1"),
            after_deps,
        )
        allocation_fact_id = recovered.current[0].fact_id
        self.assertFalse(
            any(source.fact_id == allocation_fact_id for source in after_ctx.sources)
        )

    def test_this_track_introduces_no_conversion_edge_between_the_two_fact_types(self) -> None:
        production = Path(
            REPO_ROOT / "packages" / "tax" / "nominee_allocation_recovery.py"
        ).read_text("utf-8")
        self.assertNotIn("migration-artifact", production)
        self.assertNotIn("act-migration-adoption", production)
        self.assertNotIn('"predecessor"', production)
        self.assertNotIn('"successor"', production)

        _assert_allocation(
            self.ws,
            recipient_id=PAT_ID,
            amount=300,
            actor=MATT,
            at=_at(100),
            finding_id="demo.f.pat.1",
            label=PAT_LABEL,
        )
        state = project(self.ws.log.read().acts, self.ws.registry)
        pairs = [
            (pair.get("predecessor"), pair.get("successor"))
            for migration in state.fact_state.adopted_migrations
            for pair in migration.get("pairs", ())
        ]
        forbidden = {
            (LEGACY_FACT_TYPE_ID, nar.ALLOCATION_FACT_TYPE_ID),
            (nar.ALLOCATION_FACT_TYPE_ID, LEGACY_FACT_TYPE_ID),
        }
        self.assertEqual(set(pairs) & forbidden, set())
        self.assertEqual(state.fact_state.adopted_migrations, ())


class NeighbouringSurfaceTests(unittest.TestCase):
    """Named surfaces only: ``untranslated_source_findings`` and the legacy
    nominee subtotal. The milestone plan names none beyond these."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.members = _named_legacy_members()
        self.ws = _build_workspace(
            Path(self._tmp.name),
            workspace_name=LEGACY_WORKSPACE_NAME,
            adopt_legacy=True,
        )

    def test_allocation_does_not_surface_as_an_untranslated_source_finding(self) -> None:
        _assert_allocation(
            self.ws,
            recipient_id=PAT_ID,
            amount=300,
            actor=MATT,
            at=_at(100),
            finding_id="demo.f.pat.1",
            label=PAT_LABEL,
        )
        state = project(self.ws.log.read().acts, self.ws.registry)
        untranslated = untranslated_source_findings(state, self.members)
        allocation_hits = [
            item
            for item in untranslated
            if item.fact_type_id == nar.ALLOCATION_FACT_TYPE_ID
            or item.finding_id == "demo.f.pat.1"
            or item.fact_id.startswith(f"{nar.ALLOCATION_FACT_TYPE_ID}|")
        ]
        self.assertEqual(allocation_hits, [])
        self.assertIn("demo.f.pat.1", compute_currency(state).current_finding_ids)

    def test_named_surfaces_are_unchanged_when_no_allocation_exists(self) -> None:
        state = project(self.ws.log.read().acts, self.ws.registry)
        _baseline_ctx, baseline_result = _execute_legacy_nominee_subtotal(state)
        baseline_subtotal = _published_legacy_subtotal(baseline_result)
        baseline_deps = _legacy_dependency_set(baseline_result)
        baseline_untranslated = [
            (item.fact_type_id, item.finding_id, item.fact_id, item.value)
            for item in untranslated_source_findings(state, self.members)
        ]
        self.assertEqual(baseline_subtotal, Decimal("151"))
        self.assertNotIn(
            nar.ALLOCATION_FACT_TYPE_ID,
            {item[0] for item in baseline_untranslated},
        )

        # No allocation is recorded. Re-read the same committed log: the
        # named surfaces stay exactly as they were.
        reread_state = project(self.ws.log.read().acts, self.ws.registry)
        _reread_ctx, reread_result = _execute_legacy_nominee_subtotal(reread_state)
        self.assertEqual(
            _published_legacy_subtotal(reread_result),
            baseline_subtotal,
        )
        self.assertEqual(_legacy_dependency_set(reread_result), baseline_deps)
        self.assertEqual(
            [
                (item.fact_type_id, item.finding_id, item.fact_id, item.value)
                for item in untranslated_source_findings(reread_state, self.members)
            ],
            baseline_untranslated,
        )


class RemainingCoordinatorWorkTests(unittest.TestCase):
    def test_no_coordinator_work_remains(self) -> None:
        """Track 1 already persists on ``apply_contribution_batch`` and the
        bounded retraction helper. Track 2 recovery is a log read. No
        remaining coordinator work is named, and none is added."""
        import packages.tax.nominee_allocation_recovery as recovery

        self.assertFalse(hasattr(recovery, "assert_nominee_allocation"))
        self.assertFalse(hasattr(recovery, "retract_nominee_allocation"))
        self.assertFalse(hasattr(recovery, "contribute_nominee_allocation"))
        self.assertFalse(hasattr(recovery, "apply_nominee_allocation_batch"))
        self.assertTrue(hasattr(recovery, "recover_nominee_allocations"))
        self.assertIn(
            "Remaining coordinator work (Track 2 deliverable 4): none.",
            recovery.__doc__ or "",
        )


if __name__ == "__main__":
    unittest.main()
