"""Nominee-Allocation Assertion Recording, Track 1: A0-A11 through the real
production content, producer, retraction helper, and ``ActLog``.

Track 0 (``docs/prototypes/nominee-allocation-assertion-recording/``)
established the identity and lifecycle mechanics by folding acts directly in
memory. Nothing here re-derives that contract or re-runs the candidate
comparison. This module proves the *production* surface: the real content
bundle (``packages/content/tax/2025/nominee-allocation.bundle.json``), the
real producer and retraction helper
(``packages.tax.nominee_allocation_recording``), and a real ``ActLog`` --
every assertion, correction, and retraction below goes through those named
helpers and a real workspace directory, never a hand-built act dict folded
directly.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Mapping

from packages.kernel.act_log import ActLog
from packages.kernel.contribution import ContributionError
from packages.kernel.currency import compute_currency
from packages.kernel.findings import (
    FindingModelError,
    _current_value_for_fact,
    _NO_CURRENT_VALUE,
    project,
)
from packages.tax import nominee_allocation_recording as nar
from packages.tax.loader import TAX_CONTENT_DIR, load_nominee_allocation_bundle, tax_registry
from packages.tax.report_statement_identity import (
    build_1099int_report_contribution,
    build_1099int_report_entity_acts,
    derive_1099int_box1_fact_id,
    derive_reported_payer_entity_id,
)

PAYER = "Demo Savings Bank"
STMT_A = "test-nominee-alloc-stmt-a"
STMT_B = "test-nominee-alloc-stmt-b"
YEAR = 2025
PRIOR_YEAR = 2024

MATT = "test-user-matt"
ALEX = "test-user-alex"

FAMILY_PREDECESSOR = "test.nominee-alloc.int-b1.h0"
FAMILY_SUCCESSOR = "test.nominee-alloc.int-b1.h1"

PAT_ID = "test.alloc.recipient.pat"
KIM_ID = "test.alloc.recipient.kim"

REPORT_EVIDENCE_ID = "test.evidence.nominee-alloc.report-copy"


def _at(n: int) -> str:
    return f"2026-09-07T02:{n // 60:02d}:{n % 60:02d}Z"


class _Workspace:
    """A real ``ActLog`` over a temp workspace, with a manual-append helper
    for bootstrap fixtures (bundle adoption, entity introduction, horizon
    genesis, evidence) -- everything downstream of that goes through the
    named production helpers in ``nominee_allocation_recording``, which
    manage their own revisions by reading the log."""

    def __init__(self, tmp_root: Path) -> None:
        self.registry = tax_registry()
        self.allocation_bundle = load_nominee_allocation_bundle(self.registry)
        self.log = ActLog(tmp_root / "workspace", self.registry)
        self.revision = 0

    def append(self, kind: str, payload: dict[str, Any], *, actor: str = "workspace-boot") -> dict[str, Any]:
        # Always read the log's own current revision rather than trusting a
        # cached counter: helpers in ``nominee_allocation_recording`` append
        # directly to the same real log and manage their own revisions, so
        # a cached counter here would go stale the moment one of them runs.
        self.revision = self.log.read().revision
        act = {
            "schema": "act.v1",
            "act_id": f"boot-{self.revision:04d}-{kind}",
            "kind": kind,
            "actor": actor,
            "at": _at(self.revision),
            "committed_against": self.revision,
            "payload": payload,
        }
        self.revision = self.log.append(act, expected_revision=self.revision)
        return act

    def state(self) -> Any:
        contents = self.log.read()
        return project(contents.acts, self.registry)


def _build_workspace(tmp_root: Path) -> _Workspace:
    ws = _Workspace(tmp_root)
    ws.append("bundle-adoption", {"bundle": ws.allocation_bundle})
    f1099int_bundle = json.loads((TAX_CONTENT_DIR / "f1099int.bundle.json").read_text("utf-8"))
    ws.append("bundle-adoption", {"bundle": f1099int_bundle})
    seen: set[str] = set()
    for stmt in (STMT_A, STMT_B):
        for entity_act in build_1099int_report_entity_acts(
            payer_name=PAYER, statement_reference=stmt, act_index=0
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
            "scope": {"tax-year": str(YEAR), "subject": "test.primary"},
            "horizon_id": FAMILY_PREDECESSOR,
        },
    )
    ws.append(
        "evidence-submitted",
        {
            "evidence": {
                "schema": "evidence.v1",
                "id": REPORT_EVIDENCE_ID,
                "kind": "test.report-1099int-copy",
                "label": "Synthetic Form 1099-INT copy",
                "content": {
                    "mode": nar.DOCUMENT_REPORT_EVIDENCE_MODE,
                    "synthetic": True,
                },
            }
        },
    )
    # Ordinary-language allocation evidence is submitted per answer event
    # below. Distinct assertions, corrections, and reassertions do not share
    # one generic interview record.
    return ws


def _contribute_box1_report(
    ws: _Workspace,
    *,
    statement_reference: str,
    amount: float,
    successor_id: str,
    finding_id: str,
) -> None:
    """Contribute one documentary box-1 report through a real, manually
    appended contribution + member-transition pair (mirrors the pattern
    ``tests.test_assertion_standing_integration`` uses -- a real ``ActLog``,
    never ``apply_contribution_batch``'s in-memory-only fold)."""
    built = build_1099int_report_contribution(
        payer_name=PAYER,
        statement_reference=statement_reference,
        tax_year=YEAR,
        amount=amount,
        scope={"tax-year": str(YEAR), "subject": "test.primary"},
        family_predecessor_id=FAMILY_PREDECESSOR,
        family_successor_id=successor_id,
        act_index=0,
        contribution_id=f"c.{finding_id}",
        evidence_id=REPORT_EVIDENCE_ID,
        finding_id=finding_id,
        committed_against=0,
    )
    ws.append(
        "contribution", built.contribution_act["payload"]
    )
    ws.append(
        "member-transition", built.member_transition_act["payload"]
    )


def _allocation_answers(
    *,
    statement_reference: str = STMT_A,
    tax_year: int = YEAR,
    recipient_id: str,
    amount: float,
    recipient_display_label: str | None = None,
) -> dict[str, Any]:
    answers: dict[str, Any] = {
        "circumstance": nar.ALLOCATION_CIRCUMSTANCE,
        "payer_name": PAYER,
        "statement_reference": statement_reference,
        "tax_year": tax_year,
        "recipient_id": recipient_id,
        "amount": amount,
    }
    if recipient_display_label is not None:
        answers["recipient_display_label"] = recipient_display_label
    return answers


def _ordinary_evidence_id(finding_id: str) -> str:
    return f"test.evidence.{finding_id}"


def _submit_evidence(
    ws: _Workspace,
    *,
    evidence_id: str,
    content: Mapping[str, Any],
    kind: str = "test.ordinary-allocation-interview",
    label: str = "Synthetic ordinary-language allocation interview",
) -> None:
    ws.append(
        "evidence-submitted",
        {
            "evidence": {
                "schema": "evidence.v1",
                "id": evidence_id,
                "kind": kind,
                "label": label,
                "content": content,
            }
        },
    )


def _submit_ordinary_allocation_evidence(
    ws: _Workspace, *, evidence_id: str, answers: Mapping[str, Any]
) -> None:
    """One submitted ordinary-language answer event.

    The evidence citizen retains the submitted answers; the finding remains
    the canonical proposition derived from them. Synthetic fixtures identify
    themselves here, on the evidence citizen, not in production contribution
    construction.
    """
    _submit_evidence(
        ws,
        evidence_id=evidence_id,
        content={
            "mode": nar.ORDINARY_LANGUAGE_EVIDENCE_MODE,
            "synthetic": True,
            "answers": dict(answers),
        },
    )


def _record(
    ws: _Workspace,
    *,
    answers: Mapping[str, Any],
    actor: str,
    at: str,
    evidence_id: str,
    contribution_id: str,
    finding_id: str,
    record_id: str,
    contribution_act_id: str,
    assertion_act_id: str,
) -> nar.NomineeAllocationAssertionResult:
    """Submit matching ordinary-language evidence, then persist the assertion."""
    _submit_ordinary_allocation_evidence(ws, evidence_id=evidence_id, answers=answers)
    return nar.assert_nominee_allocation(
        ws.log,
        ws.registry,
        answers=answers,
        actor=actor,
        at=at,
        evidence_id=evidence_id,
        contribution_id=contribution_id,
        finding_id=finding_id,
        record_id=record_id,
        contribution_act_id=contribution_act_id,
        assertion_act_id=assertion_act_id,
    )


class NomineeAllocationLifecycleTests(unittest.TestCase):
    """A2-A8, A11, join, and id-reuse-refused, in one real workspace,
    through the real producer and retraction helper only."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ws = _build_workspace(Path(self._tmp.name))
        _contribute_box1_report(
            self.ws,
            statement_reference=STMT_A,
            amount=1200.0,
            successor_id="test.nominee-alloc.int-b1.h1",
            finding_id="box1.a.first",
        )
        self.box1_a = derive_1099int_box1_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR
        )
        self.pat_a = nar.derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR, recipient_id=PAT_ID
        )
        self.kim_a = nar.derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR, recipient_id=KIM_ID
        )

    def test_a2_a3_one_then_several_recipients(self) -> None:
        r_pat = _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=450,
                                        recipient_display_label="Pat (allocation recipient)"),
            actor=MATT, at=_at(100),
            evidence_id=_ordinary_evidence_id("f.pat.1"), contribution_id="c.pat.1",
            finding_id="f.pat.1", record_id="r.pat.1",
            contribution_act_id="a.pat.1.contrib", assertion_act_id="a.pat.1.assert",
        )
        self.assertIsNotNone(r_pat.entity_act)
        self.assertEqual(r_pat.finding["fact_id"], self.pat_a)
        view = compute_currency(r_pat.state)
        self.assertIn("f.pat.1", view.current_finding_ids)

        r_kim = _record(
            self.ws,
            answers=_allocation_answers(recipient_id=KIM_ID, amount=150,
                                        recipient_display_label="Kim (allocation recipient)"),
            actor=MATT, at=_at(101),
            evidence_id=_ordinary_evidence_id("f.kim.1"), contribution_id="c.kim.1",
            finding_id="f.kim.1", record_id="r.kim.1",
            contribution_act_id="a.kim.1.contrib", assertion_act_id="a.kim.1.assert",
        )
        self.assertIsNotNone(r_kim.entity_act)
        self.assertNotEqual(self.pat_a, self.kim_a)
        view = compute_currency(r_kim.state)
        self.assertTrue({"f.pat.1", "f.kim.1"} <= view.current_finding_ids)

    def _assert_pat_and_kim(self) -> None:
        _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=300,
                                        recipient_display_label="Pat (allocation recipient)"),
            actor=MATT, at=_at(100),
            evidence_id=_ordinary_evidence_id("f.pat.1"), contribution_id="c.pat.1",
            finding_id="f.pat.1", record_id="r.pat.1",
            contribution_act_id="a.pat.1.contrib", assertion_act_id="a.pat.1.assert",
        )
        _record(
            self.ws,
            answers=_allocation_answers(recipient_id=KIM_ID, amount=150,
                                        recipient_display_label="Kim (allocation recipient)"),
            actor=MATT, at=_at(101),
            evidence_id=_ordinary_evidence_id("f.kim.1"), contribution_id="c.kim.1",
            finding_id="f.kim.1", record_id="r.kim.1",
            contribution_act_id="a.kim.1.contrib", assertion_act_id="a.kim.1.assert",
        )

    def test_a4_correction_leaves_the_other_recipient_the_same_record(self) -> None:
        self._assert_pat_and_kim()
        kim_before = dict(self.ws.state().findings["f.kim.1"])
        acts_before = self.ws.log.read().revision

        r_corr = _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=250),
            actor=MATT, at=_at(102),
            evidence_id=_ordinary_evidence_id("f.pat.2"), contribution_id="c.pat.2",
            finding_id="f.pat.2", record_id="r.pat.2",
            contribution_act_id="a.pat.2.contrib", assertion_act_id="a.pat.2.assert",
        )
        self.assertIsNone(r_corr.entity_act)  # existing recipient: no re-introduction
        self.assertEqual(
            r_corr.finding["evidence_ids"], [_ordinary_evidence_id("f.pat.2")]
        )
        self.assertNotEqual(
            r_corr.finding["evidence_ids"], [_ordinary_evidence_id("f.pat.1")]
        )
        kim_after = dict(r_corr.state.findings["f.kim.1"])
        self.assertEqual(kim_before, kim_after)  # same record, not merely equal value
        view = compute_currency(r_corr.state)
        self.assertIn("f.kim.1", view.current_finding_ids)
        # No act was written for Kim: Pat's correction appends its own
        # evidence-submitted act plus contribution and assertion (no entity
        # act either). The extra act is the distinct evidence citizen for
        # the changed amount, not a Kim write.
        acts_after = self.ws.log.read().revision
        self.assertEqual(acts_after - acts_before, 3)
        kinds_appended = [a["kind"] for a in self.ws.log.read().acts[acts_before:]]
        self.assertEqual(kinds_appended, ["evidence-submitted", "contribution", "assertion"])
        kim_carrying_acts = [
            a for a in self.ws.log.read().acts
            if a["kind"] == "assertion" and a["payload"]["finding"]["fact_id"] == self.kim_a
        ]
        self.assertEqual(len(kim_carrying_acts), 1)
        self.assertEqual(kim_carrying_acts[0]["act_id"], "a.kim.1.assert")

    def test_a4b_cross_actor_correction(self) -> None:
        self._assert_pat_and_kim()
        _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=250),
            actor=MATT, at=_at(102),
            evidence_id=_ordinary_evidence_id("f.pat.2"), contribution_id="c.pat.2",
            finding_id="f.pat.2", record_id="r.pat.2",
            contribution_act_id="a.pat.2.contrib", assertion_act_id="a.pat.2.assert",
        )
        r_alex = _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=275),
            actor=ALEX, at=_at(103),
            evidence_id=_ordinary_evidence_id("f.pat.alex"), contribution_id="c.pat.alex",
            finding_id="f.pat.alex", record_id="r.pat.alex",
            contribution_act_id="a.pat.alex.contrib", assertion_act_id="a.pat.alex.assert",
        )
        state = r_alex.state
        view = compute_currency(state)
        current_pat = [f for f in view.current_finding_ids if state.findings[f]["fact_id"] == self.pat_a]
        self.assertEqual(current_pat, ["f.pat.alex"])
        self.assertIn("f.pat.2", state.findings)  # Matt's finding: historical, still present
        self.assertEqual(r_alex.assertion_act["actor"], ALEX)
        self.assertEqual(
            state.findings["f.pat.2"]["evidence_ids"],
            [_ordinary_evidence_id("f.pat.2")],
        )
        self.assertEqual(
            r_alex.finding["evidence_ids"], [_ordinary_evidence_id("f.pat.alex")]
        )
        self.assertNotEqual(
            state.findings["f.pat.2"]["evidence_ids"],
            r_alex.finding["evidence_ids"],
        )

    def test_a5_two_statements_and_two_tax_years_stay_distinct(self) -> None:
        self._assert_pat_and_kim()
        pat_b = nar.derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT_B, tax_year=YEAR, recipient_id=PAT_ID
        )
        self.assertNotEqual(self.pat_a, pat_b)
        r_b = _record(
            self.ws,
            answers=_allocation_answers(statement_reference=STMT_B, recipient_id=PAT_ID, amount=999),
            actor=MATT, at=_at(104),
            evidence_id=_ordinary_evidence_id("f.pat.b"), contribution_id="c.pat.b",
            finding_id="f.pat.b", record_id="r.pat.b",
            contribution_act_id="a.pat.b.contrib", assertion_act_id="a.pat.b.assert",
        )
        view = compute_currency(r_b.state)
        self.assertIn("f.pat.1", view.current_finding_ids)  # statement A untouched

        pat_a_prior_year = nar.derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=PRIOR_YEAR, recipient_id=PAT_ID
        )
        self.assertNotEqual(self.pat_a, pat_a_prior_year)
        r_prior = _record(
            self.ws,
            answers=_allocation_answers(tax_year=PRIOR_YEAR, recipient_id=PAT_ID, amount=111),
            actor=MATT, at=_at(105),
            evidence_id=_ordinary_evidence_id("f.pat.prior"), contribution_id="c.pat.prior",
            finding_id="f.pat.prior", record_id="r.pat.prior",
            contribution_act_id="a.pat.prior.contrib", assertion_act_id="a.pat.prior.assert",
        )
        view = compute_currency(r_prior.state)
        self.assertIn("f.pat.1", view.current_finding_ids)  # 2025 statement A still current

    def test_a7_box1_correction_does_not_detach_the_allocation(self) -> None:
        self._assert_pat_and_kim()
        before = _current_value_for_fact(self.ws.state(), self.box1_a)
        self.ws.append(
            "assertion",
            {
                "finding": {
                    "schema": "finding.v2",
                    "id": "box1.a.correction",
                    "fact_id": self.box1_a,
                    "value": 1300.0,
                    "basis": "documentary",
                    "evidence_ids": [REPORT_EVIDENCE_ID],
                }
            },
            actor=MATT,
        )
        after = _current_value_for_fact(self.ws.state(), self.box1_a)
        self.assertNotEqual(before, after)
        self.assertEqual(
            derive_1099int_box1_fact_id(payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR),
            self.box1_a,
        )
        view = compute_currency(self.ws.state())
        self.assertIn("f.pat.1", view.current_finding_ids)

    def test_join_to_the_exact_current_box1_finding(self) -> None:
        self._assert_pat_and_kim()
        state = self.ws.state()
        view = compute_currency(state)
        current_box1 = [f for f in view.current_finding_ids if state.findings[f]["fact_id"] == self.box1_a]
        self.assertTrue(current_box1)
        self.assertIn(f"payer={derive_reported_payer_entity_id(PAYER)}", self.pat_a)
        self.assertIn(f"tax-year={YEAR}", self.pat_a)

    def test_a8_over_allocation_preserved_not_clamped(self) -> None:
        r_pat = _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=900,
                                        recipient_display_label="Pat (allocation recipient)"),
            actor=MATT, at=_at(100),
            evidence_id=_ordinary_evidence_id("f.pat.900"), contribution_id="c.pat.900",
            finding_id="f.pat.900", record_id="r.pat.900",
            contribution_act_id="a.pat.900.contrib", assertion_act_id="a.pat.900.assert",
        )
        r_kim = _record(
            self.ws,
            answers=_allocation_answers(recipient_id=KIM_ID, amount=900,
                                        recipient_display_label="Kim (allocation recipient)"),
            actor=MATT, at=_at(101),
            evidence_id=_ordinary_evidence_id("f.kim.900"), contribution_id="c.kim.900",
            finding_id="f.kim.900", record_id="r.kim.900",
            contribution_act_id="a.kim.900.contrib", assertion_act_id="a.kim.900.assert",
        )
        # 900 + 900 = 1800 exceeds the box-1 report's own 1200 -- both are
        # preserved; nothing here clamps or silently chooses an owner.
        view = compute_currency(r_kim.state)
        self.assertIn("f.pat.900", view.current_finding_ids)
        self.assertIn("f.kim.900", view.current_finding_ids)
        self.assertEqual(r_pat.finding["value"], 900)
        self.assertEqual(r_kim.finding["value"], 900)

    def test_a6_and_a11_cross_actor_retraction_then_reassert_same_fact_id(self) -> None:
        self._assert_pat_and_kim()
        r_corr = _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=250),
            actor=MATT, at=_at(102),
            evidence_id=_ordinary_evidence_id("f.pat.2"), contribution_id="c.pat.2",
            finding_id="f.pat.2", record_id="r.pat.2",
            contribution_act_id="a.pat.2.contrib", assertion_act_id="a.pat.2.assert",
        )
        self.assertIn("f.pat.2", compute_currency(r_corr.state).current_finding_ids)

        r_retract = nar.retract_nominee_allocation(
            self.ws.log, self.ws.registry,
            finding_id="f.pat.2", actor=ALEX, at=_at(103), act_id="a.pat.retract",
        )
        self.assertEqual(sorted(r_retract.retraction_act["payload"]), ["finding_id"])
        self.assertEqual(r_retract.retraction_act["actor"], ALEX)
        view = compute_currency(r_retract.state)
        current_pat = [f for f in view.current_finding_ids if r_retract.state.findings[f]["fact_id"] == self.pat_a]
        self.assertEqual(current_pat, [])
        # Matt's earlier findings remain historical, not erased.
        self.assertIn("f.pat.1", r_retract.state.findings)
        self.assertIn("f.pat.2", r_retract.state.findings)
        # No opposite proposition and no current value at all -- not zero.
        no_current = _current_value_for_fact(r_retract.state, self.pat_a)
        self.assertIs(no_current, _NO_CURRENT_VALUE)
        # Kim untouched throughout.
        self.assertIn("f.kim.1", view.current_finding_ids)

        r_reassert = _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=275),
            actor=MATT, at=_at(104),
            evidence_id=_ordinary_evidence_id("f.pat.3"), contribution_id="c.pat.3",
            finding_id="f.pat.3", record_id="r.pat.3",
            contribution_act_id="a.pat.3.contrib", assertion_act_id="a.pat.3.assert",
        )
        self.assertIsNone(r_reassert.entity_act)
        self.assertEqual(r_reassert.finding["fact_id"], self.pat_a)  # SAME fact id
        view = compute_currency(r_reassert.state)
        self.assertEqual(
            [f for f in view.current_finding_ids if r_reassert.state.findings[f]["fact_id"] == self.pat_a],
            ["f.pat.3"],
        )

        # Revival by re-using the retracted finding's id must still be refused.
        reuse_answers = _allocation_answers(recipient_id=PAT_ID, amount=250)
        reuse_evidence_id = _ordinary_evidence_id("f.pat.reuse")
        _submit_ordinary_allocation_evidence(
            self.ws, evidence_id=reuse_evidence_id, answers=reuse_answers
        )
        with self.assertRaises((FindingModelError, ContributionError)):
            nar.assert_nominee_allocation(
                self.ws.log, self.ws.registry,
                answers=reuse_answers,
                actor=MATT, at=_at(105),
                evidence_id=reuse_evidence_id, contribution_id="c.pat.reuse",
                finding_id="f.pat.2", record_id="r.pat.reuse",
                contribution_act_id="a.pat.reuse.contrib", assertion_act_id="a.pat.reuse.assert",
            )

    def test_attribution_recoverable_from_finding_and_from_retraction(self) -> None:
        self._assert_pat_and_kim()
        r_corr = _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=250),
            actor=MATT, at=_at(102),
            evidence_id=_ordinary_evidence_id("f.pat.2"), contribution_id="c.pat.2",
            finding_id="f.pat.2", record_id="r.pat.2",
            contribution_act_id="a.pat.2.contrib", assertion_act_id="a.pat.2.assert",
        )
        r_retract = nar.retract_nominee_allocation(
            self.ws.log, self.ws.registry,
            finding_id="f.pat.2", actor=ALEX, at=_at(103), act_id="a.pat.retract",
        )
        acts_by_id = {a["act_id"]: a for a in self.ws.log.read().acts}
        # finding id -> carrying act -> actor and time.
        carrying = next(
            a for a in acts_by_id.values()
            if a["kind"] == "assertion" and a["payload"]["finding"]["id"] == "f.pat.2"
        )
        self.assertEqual(carrying["actor"], MATT)
        self.assertEqual(carrying["at"], _at(102))
        # displacement reason -> the retracting act -> its own actor and time.
        view = compute_currency(r_retract.state)
        reasons = {r.kind: r.by for r in view.reasons["f.pat.2"]}
        self.assertIn("retraction", reasons)
        retracting_act = acts_by_id[reasons["retraction"]]
        self.assertEqual(retracting_act["actor"], ALEX)
        self.assertEqual(retracting_act["at"], _at(103))
        self.assertNotEqual(carrying["actor"], retracting_act["actor"])


class NomineeAllocationValueDomainTests(unittest.TestCase):
    """Deliverable 1's three value-domain consequences."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ws = _build_workspace(Path(self._tmp.name))
        _contribute_box1_report(
            self.ws, statement_reference=STMT_A, amount=1200.0,
            successor_id="test.nominee-alloc.int-b1.h1", finding_id="box1.a.first",
        )

    def test_a0_zero_or_absent_amount_writes_no_finding(self) -> None:
        with self.assertRaises(nar.NomineeAllocationInputError):
            nar.assert_nominee_allocation(
                self.ws.log, self.ws.registry,
                answers=_allocation_answers(recipient_id=PAT_ID, amount=0,
                                            recipient_display_label="Pat"),
                actor=MATT, at=_at(100),
                evidence_id=_ordinary_evidence_id("f.pat.zero"), contribution_id="c.pat.zero",
                finding_id="f.pat.zero", record_id="r.pat.zero",
                contribution_act_id="a.pat.zero.contrib", assertion_act_id="a.pat.zero.assert",
            )
        self.assertEqual(self.ws.log.read().revision, self.ws.revision)

    def test_correcting_to_zero_is_refused(self) -> None:
        _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=300,
                                        recipient_display_label="Pat"),
            actor=MATT, at=_at(100),
            evidence_id=_ordinary_evidence_id("f.pat.1"), contribution_id="c.pat.1",
            finding_id="f.pat.1", record_id="r.pat.1",
            contribution_act_id="a.pat.1.contrib", assertion_act_id="a.pat.1.assert",
        )
        revision_before = self.ws.log.read().revision
        with self.assertRaises(nar.NomineeAllocationInputError):
            nar.assert_nominee_allocation(
                self.ws.log, self.ws.registry,
                answers=_allocation_answers(recipient_id=PAT_ID, amount=0),
                actor=MATT, at=_at(101),
                evidence_id=_ordinary_evidence_id("f.pat.zero"), contribution_id="c.pat.zero",
                finding_id="f.pat.zero", record_id="r.pat.zero",
                contribution_act_id="a.pat.zero.contrib", assertion_act_id="a.pat.zero.assert",
            )
        self.assertEqual(self.ws.log.read().revision, revision_before)

    def test_removal_goes_through_retraction_where_correction_to_zero_failed(self) -> None:
        _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=300,
                                        recipient_display_label="Pat"),
            actor=MATT, at=_at(100),
            evidence_id=_ordinary_evidence_id("f.pat.1"), contribution_id="c.pat.1",
            finding_id="f.pat.1", record_id="r.pat.1",
            contribution_act_id="a.pat.1.contrib", assertion_act_id="a.pat.1.assert",
        )
        with self.assertRaises(nar.NomineeAllocationInputError):
            nar.assert_nominee_allocation(
                self.ws.log, self.ws.registry,
                answers=_allocation_answers(recipient_id=PAT_ID, amount=0),
                actor=MATT, at=_at(101),
                evidence_id=_ordinary_evidence_id("f.pat.zero"), contribution_id="c.pat.zero",
                finding_id="f.pat.zero", record_id="r.pat.zero",
                contribution_act_id="a.pat.zero.contrib", assertion_act_id="a.pat.zero.assert",
            )
        r_retract = nar.retract_nominee_allocation(
            self.ws.log, self.ws.registry,
            finding_id="f.pat.1", actor=MATT, at=_at(102), act_id="a.pat.retract",
        )
        pat_a = nar.derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR, recipient_id=PAT_ID
        )
        self.assertIs(_current_value_for_fact(r_retract.state, pat_a), _NO_CURRENT_VALUE)


class NomineeAllocationScopeTests(unittest.TestCase):
    """A0/A1, A9/A10, and the scope guards named in the charter."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ws = _build_workspace(Path(self._tmp.name))
        _contribute_box1_report(
            self.ws, statement_reference=STMT_A, amount=1200.0,
            successor_id="test.nominee-alloc.int-b1.h1", finding_id="box1.a.first",
        )

    def test_a0_a1_unanswered_and_explicit_no_leave_no_durable_claim(self) -> None:
        """No call into this module at all is A0/A1's whole demonstration:
        there is no negative-fact producer here, and none should exist. The
        durable state after bootstrap carries no allocation finding of any
        kind for any recipient -- indistinguishable from a later retraction
        (T0-A artifact 2)."""
        state = self.ws.state()
        self.assertFalse(
            [f for f in state.findings.values() if f["fact_id"].startswith(nar.ALLOCATION_FACT_TYPE_ID)]
        )

    def test_a9_accrued_interest_answer_cannot_enter_the_producer(self) -> None:
        accrued_interest_shaped = {
            "circumstance": "accrued-interest-purchase",
            "payer_name": PAYER,
            "obligation_description": "10yr note",
            "acquisition_date": "2025-03-01",
            "accrued_interest_paid_to_seller": 42.0,
            "currency": "USD",
        }
        with self.assertRaises(nar.NomineeAllocationInputError):
            nar.validate_nominee_allocation_answers(accrued_interest_shaped)
        revision_before = self.ws.log.read().revision
        with self.assertRaises(nar.NomineeAllocationInputError):
            nar.assert_nominee_allocation(
                self.ws.log, self.ws.registry,
                answers=accrued_interest_shaped,
                actor=MATT, at=_at(100),
                evidence_id=_ordinary_evidence_id("f.accrued"), contribution_id="c.accrued",
                finding_id="f.accrued", record_id="r.accrued",
                contribution_act_id="a.accrued.contrib", assertion_act_id="a.accrued.assert",
            )
        self.assertEqual(self.ws.log.read().revision, revision_before)

    def test_matching_ordinary_language_evidence_is_accepted(self) -> None:
        answers = _allocation_answers(
            recipient_id=PAT_ID, amount=300, recipient_display_label="Pat"
        )
        evidence_id = _ordinary_evidence_id("f.pat.1")
        result = _record(
            self.ws,
            answers=answers,
            actor=MATT, at=_at(100),
            evidence_id=evidence_id, contribution_id="c.pat.1",
            finding_id="f.pat.1", record_id="r.pat.1",
            contribution_act_id="a.pat.1.contrib", assertion_act_id="a.pat.1.assert",
        )
        self.assertEqual(result.finding["evidence_ids"], [evidence_id])
        self.assertEqual(result.finding["value"], 300)
        self.assertEqual(result.finding["basis"], "attested")
        contribution_content = result.contribution_act["payload"]["contribution"]["content"]
        self.assertEqual(contribution_content["mode"], nar.ORDINARY_LANGUAGE_EVIDENCE_MODE)
        self.assertNotIn("synthetic", contribution_content)
        # Evidence retains the submitted answers; the finding is the
        # canonical proposition, not a copy of that payload.
        stored = self.ws.state().evidence[evidence_id].evidence["content"]
        self.assertEqual(stored["answers"]["amount"], 300)
        self.assertNotEqual(result.finding, stored["answers"])
        self.assertIn("f.pat.1", compute_currency(result.state).current_finding_ids)

    def test_report_copy_evidence_is_refused_as_sole_allocation_ground(self) -> None:
        revision_before = self.ws.log.read().revision
        with self.assertRaises(nar.NomineeAllocationInputError) as ctx:
            nar.assert_nominee_allocation(
                self.ws.log, self.ws.registry,
                answers=_allocation_answers(recipient_id=PAT_ID, amount=300,
                                            recipient_display_label="Pat"),
                actor=MATT, at=_at(100),
                evidence_id=REPORT_EVIDENCE_ID, contribution_id="c.pat.report-copy",
                finding_id="f.pat.report-copy", record_id="r.pat.report-copy",
                contribution_act_id="a.pat.report-copy.contrib",
                assertion_act_id="a.pat.report-copy.assert",
            )
        message = str(ctx.exception)
        self.assertIn("ordinary-language-entry", message)
        self.assertIn("document-report-entry", message)
        self.assertIn(REPORT_EVIDENCE_ID, message)
        self.assertEqual(self.ws.log.read().revision, revision_before)

    def test_absent_or_malformed_mode_is_refused(self) -> None:
        answers = _allocation_answers(
            recipient_id=PAT_ID, amount=300, recipient_display_label="Pat"
        )
        cases = (
            (
                "test.evidence.absent-mode",
                {"synthetic": True, "answers": dict(answers)},
            ),
            (
                "test.evidence.malformed-mode",
                {"mode": ["ordinary-language-entry"], "answers": dict(answers)},
            ),
            (
                "test.evidence.malformed-answers",
                {"mode": nar.ORDINARY_LANGUAGE_EVIDENCE_MODE, "answers": "not-an-object"},
            ),
        )
        for evidence_id, content in cases:
            with self.subTest(evidence_id=evidence_id):
                _submit_evidence(self.ws, evidence_id=evidence_id, content=content)
                revision_before = self.ws.log.read().revision
                with self.assertRaises(nar.NomineeAllocationInputError):
                    nar.assert_nominee_allocation(
                        self.ws.log, self.ws.registry,
                        answers=answers,
                        actor=MATT, at=_at(100),
                        evidence_id=evidence_id, contribution_id=f"c.{evidence_id}",
                        finding_id=f"f.{evidence_id}", record_id=f"r.{evidence_id}",
                        contribution_act_id=f"a.{evidence_id}.contrib",
                        assertion_act_id=f"a.{evidence_id}.assert",
                    )
                self.assertEqual(self.ws.log.read().revision, revision_before)

    def test_unrelated_mode_evidence_is_refused(self) -> None:
        answers = _allocation_answers(
            recipient_id=PAT_ID, amount=300, recipient_display_label="Pat"
        )
        evidence_id = "test.evidence.unrelated-mode"
        _submit_evidence(
            self.ws,
            evidence_id=evidence_id,
            content={
                "mode": "manual-entry",
                "synthetic": True,
                "answers": dict(answers),
            },
        )
        revision_before = self.ws.log.read().revision
        with self.assertRaises(nar.NomineeAllocationInputError) as ctx:
            nar.assert_nominee_allocation(
                self.ws.log, self.ws.registry,
                answers=answers,
                actor=MATT, at=_at(100),
                evidence_id=evidence_id, contribution_id="c.pat.unrelated",
                finding_id="f.pat.unrelated", record_id="r.pat.unrelated",
                contribution_act_id="a.pat.unrelated.contrib",
                assertion_act_id="a.pat.unrelated.assert",
            )
        self.assertIn("manual-entry", str(ctx.exception))
        self.assertEqual(self.ws.log.read().revision, revision_before)

    def test_evidence_answers_that_differ_from_the_requested_finding_are_refused(self) -> None:
        """Correspondence is load-bearing: same recipient, different amount."""
        requested = _allocation_answers(
            recipient_id=PAT_ID, amount=300, recipient_display_label="Pat"
        )
        recorded = dict(requested)
        recorded["amount"] = 250
        evidence_id = "test.evidence.mismatched-amount"
        _submit_ordinary_allocation_evidence(
            self.ws, evidence_id=evidence_id, answers=recorded
        )
        revision_before = self.ws.log.read().revision
        with self.assertRaises(nar.NomineeAllocationInputError) as ctx:
            nar.assert_nominee_allocation(
                self.ws.log, self.ws.registry,
                answers=requested,
                actor=MATT, at=_at(100),
                evidence_id=evidence_id, contribution_id="c.pat.mismatch",
                finding_id="f.pat.mismatch", record_id="r.pat.mismatch",
                contribution_act_id="a.pat.mismatch.contrib",
                assertion_act_id="a.pat.mismatch.assert",
            )
        self.assertIn("does not correspond", str(ctx.exception))
        self.assertIn("amount", str(ctx.exception))
        self.assertEqual(self.ws.log.read().revision, revision_before)

    def test_a10_erroneous_report_answer_is_not_captured(self) -> None:
        """Bounded per Track 0: no module owning erroneous-report routing
        exists anywhere in this repository. This proves only the negative --
        no nominee-allocation assertion is written -- and claims nothing
        about where such an answer belongs."""
        erroneous_report_shaped = {
            "circumstance": "erroneous-report",
            "report_fact_id": "tax.us.2025.f1099int.box1-interest|payer=Demo Savings Bank,"
                               "statement=Demo Savings Bank::statement::test-nominee-alloc-stmt-a,"
                               "tax-year=2025",
            "corrected_amount": 1000.0,
        }
        with self.assertRaises(nar.NomineeAllocationInputError):
            nar.validate_nominee_allocation_answers(erroneous_report_shaped)
        revision_before = self.ws.log.read().revision
        with self.assertRaises(nar.NomineeAllocationInputError):
            nar.assert_nominee_allocation(
                self.ws.log, self.ws.registry,
                answers=erroneous_report_shaped,
                actor=MATT, at=_at(100),
                evidence_id=_ordinary_evidence_id("f.erroneous"), contribution_id="c.erroneous",
                finding_id="f.erroneous", record_id="r.erroneous",
                contribution_act_id="a.erroneous.contrib", assertion_act_id="a.erroneous.assert",
            )
        self.assertEqual(self.ws.log.read().revision, revision_before)

    def test_retraction_helper_refuses_a_current_finding_of_another_fact_type(self) -> None:
        with self.assertRaises(nar.NomineeAllocationInputError):
            nar.retract_nominee_allocation(
                self.ws.log, self.ws.registry,
                finding_id="box1.a.first", actor=MATT, at=_at(100), act_id="a.wrong-type.retract",
            )
        self.assertEqual(self.ws.log.read().revision, self.ws.revision)

    def test_existing_recipient_correction_emits_no_second_entity_introduced_act(self) -> None:
        _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=300,
                                        recipient_display_label="Pat"),
            actor=MATT, at=_at(100),
            evidence_id=_ordinary_evidence_id("f.pat.1"), contribution_id="c.pat.1",
            finding_id="f.pat.1", record_id="r.pat.1",
            contribution_act_id="a.pat.1.contrib", assertion_act_id="a.pat.1.assert",
        )
        r_corr = _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=250),
            actor=MATT, at=_at(101),
            evidence_id=_ordinary_evidence_id("f.pat.2"), contribution_id="c.pat.2",
            finding_id="f.pat.2", record_id="r.pat.2",
            contribution_act_id="a.pat.2.contrib", assertion_act_id="a.pat.2.assert",
        )
        self.assertIsNone(r_corr.entity_act)
        entity_acts = [a for a in self.ws.log.read().acts if a["kind"] == "entity-introduced"]
        pat_intro = [a for a in entity_acts if a["payload"]["entity"]["id"] == PAT_ID]
        self.assertEqual(len(pat_intro), 1)

    def test_existing_recipient_with_a_display_label_is_refused_not_ignored(self) -> None:
        _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=300,
                                        recipient_display_label="Pat"),
            actor=MATT, at=_at(100),
            evidence_id=_ordinary_evidence_id("f.pat.1"), contribution_id="c.pat.1",
            finding_id="f.pat.1", record_id="r.pat.1",
            contribution_act_id="a.pat.1.contrib", assertion_act_id="a.pat.1.assert",
        )
        refused_answers = _allocation_answers(
            recipient_id=PAT_ID, amount=250, recipient_display_label="Patricia"
        )
        refused_evidence_id = _ordinary_evidence_id("f.pat.2")
        _submit_ordinary_allocation_evidence(
            self.ws, evidence_id=refused_evidence_id, answers=refused_answers
        )
        revision_before = self.ws.log.read().revision
        with self.assertRaises(nar.NomineeAllocationInputError):
            nar.assert_nominee_allocation(
                self.ws.log, self.ws.registry,
                answers=refused_answers,
                actor=MATT, at=_at(101),
                evidence_id=refused_evidence_id, contribution_id="c.pat.2",
                finding_id="f.pat.2", record_id="r.pat.2",
                contribution_act_id="a.pat.2.contrib", assertion_act_id="a.pat.2.assert",
            )
        self.assertEqual(self.ws.log.read().revision, revision_before)

    def test_new_recipient_present_after_reprojection_from_the_log(self) -> None:
        """The returned in-memory state is not evidence of persistence: the
        recipient must be visible after re-reading and re-projecting the
        committed log from a fresh start."""
        _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=300,
                                        recipient_display_label="Pat (allocation recipient)"),
            actor=MATT, at=_at(100),
            evidence_id=_ordinary_evidence_id("f.pat.1"), contribution_id="c.pat.1",
            finding_id="f.pat.1", record_id="r.pat.1",
            contribution_act_id="a.pat.1.contrib", assertion_act_id="a.pat.1.assert",
        )
        contents = self.ws.log.read()
        replayed = project(contents.acts, self.ws.registry)
        lifecycle = replayed.fact_state.entities.get(PAT_ID)
        assert lifecycle is not None, "recipient entity missing after log replay"
        self.assertEqual(lifecycle.status, "current")
        self.assertEqual(lifecycle.entity["kind"], nar.RECIPIENT_ENTITY_KIND)
        pat_a = nar.derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR, recipient_id=PAT_ID
        )
        self.assertEqual(_current_value_for_fact(replayed, pat_a), 300)


class NomineeAllocationRealPersistenceRoundTripTests(unittest.TestCase):
    """Deliverable 4's required real round-trip: assertion, correction, and
    retraction through their named production helpers, committed to a real
    ``ActLog``, then rebuilt from the log and checked through the current
    projection -- never the in-memory fold ``apply_contribution_batch``
    returns."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ws = _build_workspace(Path(self._tmp.name))
        _contribute_box1_report(
            self.ws, statement_reference=STMT_A, amount=1200.0,
            successor_id="test.nominee-alloc.int-b1.h1", finding_id="box1.a.first",
        )

    def test_round_trip_through_a_real_log(self) -> None:
        _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=300,
                                        recipient_display_label="Pat"),
            actor=MATT, at=_at(100),
            evidence_id=_ordinary_evidence_id("f.pat.1"), contribution_id="c.pat.1",
            finding_id="f.pat.1", record_id="r.pat.1",
            contribution_act_id="a.pat.1.contrib", assertion_act_id="a.pat.1.assert",
        )
        _record(
            self.ws,
            answers=_allocation_answers(recipient_id=PAT_ID, amount=250),
            actor=MATT, at=_at(101),
            evidence_id=_ordinary_evidence_id("f.pat.2"), contribution_id="c.pat.2",
            finding_id="f.pat.2", record_id="r.pat.2",
            contribution_act_id="a.pat.2.contrib", assertion_act_id="a.pat.2.assert",
        )
        nar.retract_nominee_allocation(
            self.ws.log, self.ws.registry,
            finding_id="f.pat.2", actor=ALEX, at=_at(102), act_id="a.pat.retract",
        )

        # Rebuild from a completely fresh read of the committed log.
        contents = self.ws.log.read()
        replayed = project(contents.acts, self.ws.registry)
        view = compute_currency(replayed)
        pat_a = nar.derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT_A, tax_year=YEAR, recipient_id=PAT_ID
        )
        current_pat = [f for f in view.current_finding_ids if replayed.findings[f]["fact_id"] == pat_a]
        self.assertEqual(current_pat, [])
        self.assertIs(_current_value_for_fact(replayed, pat_a), _NO_CURRENT_VALUE)
        self.assertIn("f.pat.1", replayed.findings)
        self.assertIn("f.pat.2", replayed.findings)


class _AppendBudget:
    """Fail after ``succeeds`` successful ``ActLog.append`` calls.

    Bounded failure injection: the kernel has no transaction substrate, so
    this wrapper is the only way to observe a persisted prefix of the
    producer's multi-act sequence.
    """

    def __init__(self, log: ActLog, *, succeeds: int) -> None:
        self._log = log
        self._succeeds = succeeds
        self._seen = 0
        self._original = log.append

    def __enter__(self) -> "_AppendBudget":
        def _limited(act: dict[str, Any], expected_revision: int) -> int:
            if self._seen >= self._succeeds:
                raise RuntimeError(
                    f"injected interrupt after {self._succeeds} successful append(s)"
                )
            revision = self._original(act, expected_revision)
            self._seen += 1
            return revision

        self._log.append = _limited  # type: ignore[method-assign]
        return self

    def __exit__(self, *exc: object) -> None:
        self._log.append = self._original  # type: ignore[method-assign]


class NomineeAllocationInterruptedWriteTests(unittest.TestCase):
    """Hard gate: a persisted prefix is not a resumable retry."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ws = _build_workspace(Path(self._tmp.name))
        _contribute_box1_report(
            self.ws, statement_reference=STMT_A, amount=1200.0,
            successor_id="test.nominee-alloc.int-b1.h1", finding_id="box1.a.first",
        )

    def _new_recipient_kwargs(self) -> dict[str, Any]:
        answers = _allocation_answers(
            recipient_id=PAT_ID,
            amount=300,
            recipient_display_label="Pat (allocation recipient)",
        )
        evidence_id = _ordinary_evidence_id("f.pat.1")
        _submit_ordinary_allocation_evidence(
            self.ws, evidence_id=evidence_id, answers=answers
        )
        return {
            "answers": answers,
            "actor": MATT,
            "at": _at(100),
            "evidence_id": evidence_id,
            "contribution_id": "c.pat.1",
            "finding_id": "f.pat.1",
            "record_id": "r.pat.1",
            "contribution_act_id": "a.pat.1.contrib",
            "assertion_act_id": "a.pat.1.assert",
        }

    def test_retry_after_entity_prefix_fails_and_leaves_the_prefix(self) -> None:
        kwargs = self._new_recipient_kwargs()
        revision_before = self.ws.log.read().revision
        with self.assertRaisesRegex(RuntimeError, "injected interrupt after 1"):
            with _AppendBudget(self.ws.log, succeeds=1):
                nar.assert_nominee_allocation(self.ws.log, self.ws.registry, **kwargs)

        contents = self.ws.log.read()
        self.assertEqual(contents.revision, revision_before + 1)
        kinds = [act["kind"] for act in contents.acts[revision_before:]]
        self.assertEqual(kinds, ["entity-introduced"])
        entity = contents.acts[-1]["payload"]["entity"]
        self.assertEqual(entity["id"], PAT_ID)
        self.assertEqual(entity["kind"], nar.RECIPIENT_ENTITY_KIND)
        state = project(contents.acts, self.ws.registry)
        self.assertIsNotNone(state.fact_state.entities.get(PAT_ID))
        self.assertFalse(
            any(
                finding["id"] == "f.pat.1"
                for finding in state.findings.values()
            )
        )

        with self.assertRaises(nar.NomineeAllocationInputError) as ctx:
            nar.assert_nominee_allocation(self.ws.log, self.ws.registry, **kwargs)
        self.assertIn("already exists", str(ctx.exception))
        self.assertIn("display-name", str(ctx.exception))
        self.assertEqual(self.ws.log.read().revision, revision_before + 1)

    def test_retry_after_contribution_prefix_fails_and_leaves_the_prefix(self) -> None:
        kwargs = self._new_recipient_kwargs()
        revision_before = self.ws.log.read().revision
        with self.assertRaisesRegex(RuntimeError, "injected interrupt after 2"):
            with _AppendBudget(self.ws.log, succeeds=2):
                nar.assert_nominee_allocation(self.ws.log, self.ws.registry, **kwargs)

        contents = self.ws.log.read()
        self.assertEqual(contents.revision, revision_before + 2)
        kinds = [act["kind"] for act in contents.acts[revision_before:]]
        self.assertEqual(kinds, ["entity-introduced", "contribution"])
        self.assertEqual(
            contents.acts[-1]["payload"]["contribution"]["id"], "c.pat.1"
        )

        with self.assertRaises(nar.NomineeAllocationInputError) as ctx:
            nar.assert_nominee_allocation(self.ws.log, self.ws.registry, **kwargs)
        self.assertIn("already exists", str(ctx.exception))
        self.assertEqual(self.ws.log.read().revision, revision_before + 2)


class NomineeAllocationLegacyCoexistenceTests(unittest.TestCase):
    """The legacy nominee adjustment fact is unchanged and unconverted."""

    LEGACY_FACT_TYPE_ID = "tax.us.2025.scheduleb.adjustment.nominee.amount"

    def test_legacy_bundle_is_untouched_and_distinct_namespace(self) -> None:
        legacy_bundle = json.loads(
            (TAX_CONTENT_DIR / "scheduleb-adjustment.nominee.bundle.json").read_text("utf-8")
        )
        legacy_ids = {ft["id"] for ft in legacy_bundle["fact_types"]}
        self.assertIn(self.LEGACY_FACT_TYPE_ID, legacy_ids)
        allocation_bundle = json.loads(
            (TAX_CONTENT_DIR / "nominee-allocation.bundle.json").read_text("utf-8")
        )
        allocation_ids = {ft["id"] for ft in allocation_bundle["fact_types"]}
        self.assertFalse(legacy_ids & allocation_ids)
        self.assertNotIn(nar.ALLOCATION_FACT_TYPE_ID, legacy_ids)


class NomineeAllocationStructuralChecksTests(unittest.TestCase):
    """Structural checks -- reading declared shape, never searching text."""

    def test_published_fact_shape_carries_no_characterization_field(self) -> None:
        bundle = json.loads((TAX_CONTENT_DIR / "nominee-allocation.bundle.json").read_text("utf-8"))
        fact_type = next(
            ft for ft in bundle["fact_types"] if ft["id"] == nar.ALLOCATION_FACT_TYPE_ID
        )
        value_schema = fact_type["value_schema"]
        # The value schema is a bare number, not an object with fields at
        # all -- structurally, there is no field to carry a nominee
        # characterization, a Schedule B classification, or a reporting
        # conclusion.
        self.assertEqual(value_schema.get("type"), "number")
        self.assertNotIn("properties", value_schema)
        self.assertGreater(value_schema.get("exclusiveMinimum", -1), -1)

    def test_no_new_rule_consuming_the_allocation_fact_publishes_forbidden_symbols(self) -> None:
        """Track 1 publishes no rule and no derived symbol at all. This
        checks the honest, narrower structural claim the charter actually
        names: among every committed rule, none that *consumes* the new
        allocation fact type as an input also declares one of the two
        forbidden published symbols. (Those two symbols are already used
        elsewhere in the corpus by unrelated, pre-existing rules over
        pre-existing fact types -- a bare grep for the strings would
        wrongly flag those. This reads each rule's declared ``publishes``
        field and its declared input references structurally instead.)"""
        forbidden = {
            "tax.us.2025.interest.scheduleb-nominee-subtotal",
            "tax.us.2025.interest.taxable-total",
        }

        def references_allocation_fact(node: Any) -> bool:
            if isinstance(node, dict):
                if node.get("name") == nar.ALLOCATION_FACT_TYPE_ID:
                    return True
                return any(references_allocation_fact(v) for v in node.values())
            if isinstance(node, list):
                return any(references_allocation_fact(v) for v in node)
            return False

        offending: list[str] = []
        for path in TAX_CONTENT_DIR.glob("rule.*.json"):
            content = json.loads(path.read_text("utf-8"))
            if content.get("schema") != "rule-artifact.v2":
                continue
            if content.get("publishes") in forbidden and references_allocation_fact(
                content.get("value")
            ):
                offending.append(content["id"])
        self.assertEqual(offending, [])


if __name__ == "__main__":
    unittest.main()
