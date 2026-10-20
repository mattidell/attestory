"""Acceptance test suite for Form 1099-K multiple statement personal item sales.

Validates the eleven concrete acceptance cases from connected-sale-design § 7
plus Candidate C closed-empty $0.00 on v2 and a gain/excluded statement beside
a supported loss:
1. Two supported personal losses (differing amounts: $880 + $460 -> $1,340.00 top entry, own Box 1a in review).
2. Two supported personal losses (identical amounts: $500 + $500 -> $1,000.00, distinct pins, no finding ID collision).
3. Mixed outcome (S1 supported loss $880, S2 cost-basis-unknown $460 -> top entry blocked, S1 review supported-loss, S2 review cost-basis-unknown).
4. Answer withdrawal (S1 & S2 initially supported, withdraw personal use on S2 -> S2 personal-use-unconfirmed, S1 remains supported-loss, top entry blocked).
5. Statement correction with amount mismatch (correct S1 to $900 with agreed price $800 -> unexplained-reconciliation-discrepancy, S2 unaffected, top entry blocked).
6. Atomic statement removal (S1 & S2 initially, remove S2 -> single statement return for S1 $880 once fresh closure attested).
7. Single-statement Form 1099-K invariant (zero regression; Form 1098 covered in unit-lane test_f1098_* modules).
8. v1 closed-empty workspace upgraded on first statement (v1 closed-empty -> handover to v2, fresh v2 closure required, top entry publishes $880 once closed).
9. v1 single-statement workspace upgraded on second statement (v1 single-statement -> handover to v2, fresh v2 closure required, top entry publishes $1,340 once closed).
10. Untouched v1 workspace under successor package (historical v1 presentation preserved at its historical revision; successor package without v1 admission blocks new run without invalidating historical saved run).
11. Stale older-version write refused (record_f1099k_statement_durably with family_version="v1" on v2 chain raises F1099KRecordingRefused).
12. Candidate C closed-empty $0.00 on v2 (no statements, attested v2 closure -> top entry publishes $0.00).
13. Gain or excluded statement beside supported loss (S1 supported loss $880, S2 unsupported gain $1,200 -> top entry blocked, S1 review preserves supported loss).

All cases run through the real recorder, save path, coordinator (no instrumented transport),
and reload the saved explanation from disk, observing identities, currency, and pins.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import unittest

from packages.derivation.live import LiveCoordinatorOutcome, live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.f1099k_statement_recording import (
    F1099KRecordingRefused,
    FAMILY_ID,
    STATEMENT_BOX1A,
    close_f1099k_family_durably,
    record_f1099k_no_statements_durably,
    record_f1099k_statement_answers_durably,
    record_f1099k_statement_durably,
    retract_f1099k_statement_durably,
    withdraw_f1099k_statement_answer_durably,
)
from packages.tax.f1099k_statement_review import (
    associate_saved_run,
    review_f1099k_statement_with_saved_presentation,
)
from packages.tax.loader import tax_registry
from tests.test_f1098_mortgage_interest_line12e_track2 import _load_fixture_adoption
from tests.test_f1099k_personal_item_sale_track1 import (
    CONTENT,
    RELEASE_DIR,
    ROOT,
    SCOPE,
    SURFACE,
    USER,
    _finish_acts,
    _make_base_acts,
)

PACKAGE_V49_PATH = CONTENT / "package.core-calculations.v49.json"
RELEASE_V47_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v47.json"
REGISTRY_V47_PATH = CONTENT / "published-packages.v47.json"
SURFACE_V47 = PublicationSurface(RELEASE_DIR, REGISTRY_V47_PATH, CONTENT)

PAYER_A = "demo.platform.a"
STMT_A = "demo.stmt.a"
PAYER_B = "demo.platform.b"
STMT_B = "demo.stmt.b"

TOP_ENTRY_FIELD_ID = "tax.us.2025.schedule1.top-entry.form-field"
UNRESOLVED_FIELD_ID = "tax.us.2025.form.f1099k.unresolved.form-field"

SUPPORTED_ANSWERS_A: dict[str, Any] = {
    "covers-only-single-item": "yes",
    "acquired-by-purchase": "yes",
    "primary-purpose-at-acquisition": "personal-use",
    "exclusive-personal-use": "yes",
    "digital-asset-involvement": "no",
    "agreed-item-price": 800.0,
    "shipping-arrangement": "platform-pass-through",
    "platform-fees": 80.0,
    "seller-paid-shipping": 0.0,
    "sales-tax-collected-by-platform": 56.0,
    "refund-amount": 0.0,
    "buyer-paid-shipping": 24.0,
    "cost-basis-known": "yes",
    "purchase-cost": 1000.0,
    "lasting-improvements-or-adjustments": "no",
}

SUPPORTED_ANSWERS_B: dict[str, Any] = {
    "covers-only-single-item": "yes",
    "acquired-by-purchase": "yes",
    "primary-purpose-at-acquisition": "personal-use",
    "exclusive-personal-use": "yes",
    "digital-asset-involvement": "no",
    "agreed-item-price": 460.0,
    "shipping-arrangement": "platform-pass-through",
    "platform-fees": 60.0,
    "seller-paid-shipping": 0.0,
    "sales-tax-collected-by-platform": 0.0,
    "refund-amount": 0.0,
    "buyer-paid-shipping": 0.0,
    "cost-basis-known": "yes",
    "purchase-cost": 600.0,
    "lasting-improvements-or-adjustments": "no",
}


def _finish_acts_v49(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    pkg_data = json.loads(PACKAGE_V49_PATH.read_text("utf-8"))
    pkg_csum = pkg_data["package_checksum"]
    rel_csum = hashlib.sha256(RELEASE_V47_PATH.read_bytes()).hexdigest()

    built = copy.deepcopy(acts)
    adoption = copy.deepcopy(_load_fixture_adoption())
    adoption["act_id"] = f"demo.f1099k.adopt.{len(built):03d}"
    adoption["committed_against"] = len(built)
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {"id": "tax.us.2025.package.core-calculations", "version": "v49", "checksum": pkg_csum}
    payload["release"] = {"id": "demo.release.sli-worksheet-integration.2025", "version": "v47", "checksum": rel_csum}
    payload["audit"] = {"note": "synthetic Form 1099-K v49 acceptance test"}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = USER
    return built


def _seed_workspace_v49(log: ActLog) -> None:
    seed_acts = _finish_acts_v49(_make_base_acts())
    log.append_batch(seed_acts, expected_revision=0)


def _seed_workspace_v48(log: ActLog) -> None:
    seed_acts = _finish_acts(_make_base_acts())
    log.append_batch(seed_acts, expected_revision=0)


class MultipleStatementSaleAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = tax_registry()
        self.temp = TemporaryDirectory(prefix="f1099k-acc-")
        self.addCleanup(self.temp.cleanup)
        self.ws_dir = Path(self.temp.name)
        self.capability = WorkspaceCapability(self.ws_dir)
        self.log = ActLog(self.ws_dir, self.registry)
        self.records = RecordStream(self.ws_dir / "records", DerivationSchemas())

    def _run(self, run_id: str, surface: PublicationSurface = SURFACE_V47) -> LiveCoordinatorOutcome:
        contents = self.log.read()
        return live_coordinate_run(
            self.capability,
            repo_root=ROOT,
            authoritative_acts=contents.acts,
            workspace_revision=contents.revision,
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name=f"{run_id}.json",
        )

    def test_case_01_two_supported_personal_losses_differing_amounts(self) -> None:
        """Case 1: Statement 1 ($880, loss) + Statement 2 ($460, loss) -> $1,340.00 top entry, own Box 1a in review."""
        _seed_workspace_v49(self.log)

        # 1. Record Statement 1
        res1 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_A,
            statement_ref=STMT_A,
            box1a=880.0,
            box4=0.0,
            submission_id="sub.stmt.1",
            evidence_id="ev.stmt.1",
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_a = res1["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=keys_a,
            answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.a",
            evidence_ids={q: f"ev.a.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=self.log.read().revision,
        )

        # 2. Record Statement 2
        res2 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_B,
            statement_ref=STMT_B,
            box1a=460.0,
            box4=0.0,
            submission_id="sub.stmt.2",
            evidence_id="ev.stmt.2",
            actor=USER,
            at="2026-10-16T12:03:00Z",
            expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_b = res2["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=keys_b,
            answers=SUPPORTED_ANSWERS_B,
            submission_id="sub.ans.b",
            evidence_ids={q: f"ev.b.{q}" for q in SUPPORTED_ANSWERS_B},
            actor=USER,
            at="2026-10-16T12:04:00Z",
            expected_revision=self.log.read().revision,
        )

        # 3. Close family
        close_res = close_f1099k_family_durably(
            self.log,
            self.registry,
            submission_id="sub.close",
            actor=USER,
            at="2026-10-16T12:05:00Z",
            expected_revision=self.log.read().revision,
        )

        # 4. Run live coordinator (no instrumented transport)
        outcome = self._run("run-case-01")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        # 5. Reload presentation model from disk
        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        top_sec = next(s for s in model["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(top_sec["resolved"]["disposition"], "published_value")
        self.assertEqual(float(top_sec["resolved"]["value"]), 1340.0)

        # Pins: top-entry rule directly pins the closure finding, subtotal, and both statements' reasons
        completed_record = list(self.records.read().records)[-1]
        top_disp = next(
            d for d in completed_record.get("dispositions", [])
            if d.get("symbol") == "tax.us.2025.schedule1.top-entry"
        )
        subtotal_disp = next(
            d for d in completed_record.get("dispositions", [])
            if d.get("symbol") == "tax.us.2025.f1099k.box1a-subtotal"
        )
        reason_disps = [
            d for d in completed_record.get("dispositions", [])
            if str(d.get("symbol", "")).startswith("tax.us.2025.f1099k.statement-loss-reason")
        ]
        self.assertEqual(len(reason_disps), 2)

        pinned_ids = {p["id"] for p in top_disp.get("pins", [])}
        self.assertIn(close_res["finding_ids"][0], pinned_ids)
        self.assertIn(subtotal_disp["finding_id"], pinned_ids)
        for rd in reason_disps:
            self.assertIn(rd["finding_id"], pinned_ids)

        # Presentation citation sites observe pins for both statements
        citation_leaves = [c["pinId"] for c in top_sec.get("citationSites", [])]
        self.assertIn(res1["finding_ids"][0], citation_leaves)
        self.assertIn(res2["finding_ids"][0], citation_leaves)

        # 6. Reload saved reviews from disk observing own Box 1a and supported-loss
        rev1 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="rev.stmt.1",
            shown_at="2026-10-16T12:06:00Z",
            statement_keys=keys_a,
        )
        self.assertEqual(rev1["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev1["savedState"], "supported-loss")
        self.assertIsNotNone(rev1["savedCalculation"])
        assert rev1["savedCalculation"] is not None
        self.assertEqual(rev1["savedCalculation"]["box1a"], 880.0)
        self.assertEqual(rev1["savedCalculation"]["reason"], "supported-loss")

        rev2 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="rev.stmt.2",
            shown_at="2026-10-16T12:07:00Z",
            statement_keys=keys_b,
        )
        self.assertEqual(rev2["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev2["savedState"], "supported-loss")
        self.assertIsNotNone(rev2["savedCalculation"])
        assert rev2["savedCalculation"] is not None
        self.assertEqual(rev2["savedCalculation"]["box1a"], 460.0)
        self.assertEqual(rev2["savedCalculation"]["reason"], "supported-loss")

        # Currency and identities
        state = project(self.log.read().acts, self.registry)
        cur = compute_currency(state)
        self.assertIn(res1["finding_ids"][0], cur.current_finding_ids)
        self.assertIn(res2["finding_ids"][0], cur.current_finding_ids)

    def test_case_02_two_supported_personal_losses_identical_amounts(self) -> None:
        """Case 2: Statement 1 ($500, loss) + Statement 2 ($500, loss) with identical answers -> $1,000.00, no collision."""
        _seed_workspace_v49(self.log)

        identical_answers_1 = {
            "covers-only-single-item": "yes",
            "acquired-by-purchase": "yes",
            "primary-purpose-at-acquisition": "personal-use",
            "exclusive-personal-use": "yes",
            "digital-asset-involvement": "no",
            "agreed-item-price": 500.0,
            "shipping-arrangement": "platform-pass-through",
            "platform-fees": 50.0,
            "seller-paid-shipping": 0.0,
            "sales-tax-collected-by-platform": 0.0,
            "refund-amount": 0.0,
            "buyer-paid-shipping": 0.0,
            "cost-basis-known": "yes",
            "purchase-cost": 800.0,
            "lasting-improvements-or-adjustments": "no",
        }
        identical_answers_2 = dict(identical_answers_1)

        res1 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_A,
            statement_ref=STMT_A,
            box1a=500.0,
            box4=0.0,
            submission_id="sub.stmt.id1",
            evidence_id="ev.stmt.id1",
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_a = res1["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=keys_a,
            answers=identical_answers_1,
            submission_id="sub.ans.id1",
            evidence_ids={q: f"ev.id1.{q}" for q in identical_answers_1},
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=self.log.read().revision,
        )

        res2 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_B,
            statement_ref=STMT_B,
            box1a=500.0,
            box4=0.0,
            submission_id="sub.stmt.id2",
            evidence_id="ev.stmt.id2",
            actor=USER,
            at="2026-10-16T12:03:00Z",
            expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_b = res2["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=keys_b,
            answers=identical_answers_2,
            submission_id="sub.ans.id2",
            evidence_ids={q: f"ev.id2.{q}" for q in identical_answers_2},
            actor=USER,
            at="2026-10-16T12:04:00Z",
            expected_revision=self.log.read().revision,
        )

        close_f1099k_family_durably(
            self.log,
            self.registry,
            submission_id="sub.close.id",
            actor=USER,
            at="2026-10-16T12:05:00Z",
            expected_revision=self.log.read().revision,
        )

        outcome = self._run("run-case-02")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        top_sec = next(s for s in model["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(float(top_sec["resolved"]["value"]), 1000.0)

        # Distinct statement IDs and no finding ID collisions
        self.assertNotEqual(keys_a["statement"], keys_b["statement"])
        self.assertNotEqual(res1["finding_ids"][0], res2["finding_ids"][0])

        # Separate pins and reviews reloaded from disk
        rev1 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.id1", shown_at="2026-10-16T12:06:00Z", statement_keys=keys_a,
        )
        rev2 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.id2", shown_at="2026-10-16T12:07:00Z", statement_keys=keys_b,
        )
        self.assertEqual(rev1["savedCalculation"]["box1a"], 500.0)
        self.assertEqual(rev2["savedCalculation"]["box1a"], 500.0)

    def test_case_03_mixed_outcome_one_supported_loss_one_unknown_cost_basis(self) -> None:
        """Case 3: S1 supported loss ($880) + S2 cost-basis-unknown ($460) -> top entry blocked, S1 review preserved."""
        _seed_workspace_v49(self.log)

        res1 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.stmt.m1", evidence_id="ev.stmt.m1",
            actor=USER, at="2026-10-16T12:01:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_a = res1["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_a, answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.m1", evidence_ids={q: f"ev.m1.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER, at="2026-10-16T12:02:00Z", expected_revision=self.log.read().revision,
        )

        res2 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_B, statement_ref=STMT_B,
            box1a=460.0, box4=0.0, submission_id="sub.stmt.m2", evidence_id="ev.stmt.m2",
            actor=USER, at="2026-10-16T12:03:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_b = res2["statement_keys"]
        unknown_cost_answers = dict(SUPPORTED_ANSWERS_B)
        unknown_cost_answers["cost-basis-known"] = "cannot-tell"
        unknown_cost_answers["purchase-cost"] = 0.0
        unknown_cost_answers["lasting-improvements-or-adjustments"] = "no"

        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_b, answers=unknown_cost_answers,
            submission_id="sub.ans.m2", evidence_ids={q: f"ev.m2.{q}" for q in unknown_cost_answers},
            actor=USER, at="2026-10-16T12:04:00Z", expected_revision=self.log.read().revision,
        )
        close_f1099k_family_durably(
            self.log, self.registry, submission_id="sub.close.m", actor=USER,
            at="2026-10-16T12:05:00Z", expected_revision=self.log.read().revision,
        )

        outcome = self._run("run-case-03")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        top_sec = next(s for s in model["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(top_sec["resolved"]["disposition"], "blocked")

        # Statement 1 review preserves local status supported-loss with own Box 1a
        rev1 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.m1", shown_at="2026-10-16T12:06:00Z", statement_keys=keys_a,
        )
        self.assertEqual(rev1["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev1["savedState"], "supported-loss")
        self.assertEqual(rev1["savedCalculation"]["box1a"], 880.0)

        # Statement 2 review shows its published reason cost-basis-unknown
        rev2 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.m2", shown_at="2026-10-16T12:07:00Z", statement_keys=keys_b,
        )
        self.assertEqual(rev2["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(rev2["savedState"], "actually-unresolved")
        self.assertIsNone(rev2["savedCalculation"])
        self.assertEqual(rev2["savedUnresolvedExplanation"]["reason"], "cost-basis-unknown")

    def test_case_04_answer_withdrawal_on_one_statement(self) -> None:
        """Case 4: S1 & S2 initially supported; withdraw personal use on S2 -> S2 personal-use-unconfirmed, top blocked."""
        _seed_workspace_v49(self.log)

        res1 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.stmt.w1", evidence_id="ev.stmt.w1",
            actor=USER, at="2026-10-16T12:01:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_a = res1["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_a, answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.w1", evidence_ids={q: f"ev.w1.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER, at="2026-10-16T12:02:00Z", expected_revision=self.log.read().revision,
        )

        res2 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_B, statement_ref=STMT_B,
            box1a=460.0, box4=0.0, submission_id="sub.stmt.w2", evidence_id="ev.stmt.w2",
            actor=USER, at="2026-10-16T12:03:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_b = res2["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_b, answers=SUPPORTED_ANSWERS_B,
            submission_id="sub.ans.w2", evidence_ids={q: f"ev.w2.{q}" for q in SUPPORTED_ANSWERS_B},
            actor=USER, at="2026-10-16T12:04:00Z", expected_revision=self.log.read().revision,
        )
        close_f1099k_family_durably(
            self.log, self.registry, submission_id="sub.close.w", actor=USER,
            at="2026-10-16T12:05:00Z", expected_revision=self.log.read().revision,
        )

        # Initial run: $1,340.00 published
        run1 = self._run("run-case-04-initial")
        self.assertIsNone(run1.refusal)

        # Taxpayer withdraws exclusive personal use on Statement 2
        state = project(self.log.read().acts, self.registry)
        q_fid = next(
            fid for fid, finding in state.findings.items()
            if "exclusive-personal-use" in finding["fact_id"]
            and keys_b["statement"] in finding["fact_id"]
        )
        withdraw_f1099k_statement_answer_durably(
            self.log,
            self.registry,
            current_findings=[q_fid],
            submission_id="sub.ans.w2.withdraw",
            actor=USER,
            at="2026-10-16T12:06:00Z",
            expected_revision=self.log.read().revision,
        )

        # Second run: S2 has personal use unconfirmed, top entry blocks
        run2 = self._run("run-case-04-withdrawn")
        self.assertIsNone(run2.refusal)
        assert run2.presentation_path is not None

        model = json.loads(run2.presentation_path.read_text("utf-8"))
        top_sec = next(s for s in model["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(top_sec["resolved"]["disposition"], "blocked")

        # Statement 1 review remains supported loss
        rev1 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, run2.presentation_path, self.records,
            review_id="rev.w1.after", shown_at="2026-10-16T12:07:00Z", statement_keys=keys_a,
        )
        self.assertEqual(rev1["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev1["savedState"], "supported-loss")
        self.assertEqual(rev1["savedCalculation"]["box1a"], 880.0)

        # Statement 2 review shows personal-use-unconfirmed
        rev2 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, run2.presentation_path, self.records,
            review_id="rev.w2.after", shown_at="2026-10-16T12:08:00Z", statement_keys=keys_b,
        )
        self.assertEqual(rev2["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(rev2["savedState"], "actually-unresolved")
        self.assertEqual(rev2["savedUnresolvedExplanation"]["reason"], "personal-use-unconfirmed")

    def test_case_05_statement_correction_with_amount_mismatch(self) -> None:
        """Case 5: Correct S1 to $900 with agreed price $800 -> unexplained-reconciliation-discrepancy, S2 unaffected."""
        _seed_workspace_v49(self.log)

        res1 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.stmt.c1", evidence_id="ev.stmt.c1",
            actor=USER, at="2026-10-16T12:01:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_a = res1["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_a, answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.c1", evidence_ids={q: f"ev.c1.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER, at="2026-10-16T12:02:00Z", expected_revision=self.log.read().revision,
        )

        res2 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_B, statement_ref=STMT_B,
            box1a=460.0, box4=0.0, submission_id="sub.stmt.c2", evidence_id="ev.stmt.c2",
            actor=USER, at="2026-10-16T12:03:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_b = res2["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_b, answers=SUPPORTED_ANSWERS_B,
            submission_id="sub.ans.c2", evidence_ids={q: f"ev.c2.{q}" for q in SUPPORTED_ANSWERS_B},
            actor=USER, at="2026-10-16T12:04:00Z", expected_revision=self.log.read().revision,
        )
        close_f1099k_family_durably(
            self.log, self.registry, submission_id="sub.close.c", actor=USER,
            at="2026-10-16T12:05:00Z", expected_revision=self.log.read().revision,
        )

        # Taxpayer records corrected Statement 1 ($900 Box 1a) without updating circumstance answers
        record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_A,
            statement_ref=STMT_A,
            box1a=900.0,
            box4=0.0,
            corrected=True,
            submission_id="sub.stmt.c1.corr",
            evidence_id="ev.stmt.c1.corr",
            actor=USER,
            at="2026-10-16T12:06:00Z",
            expected_revision=self.log.read().revision,
            close_family=False,
        )

        outcome = self._run("run-case-05-corrected")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        top_sec = next(s for s in model["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(top_sec["resolved"]["disposition"], "blocked")

        # Statement 1 evaluates to unexplained-reconciliation-discrepancy
        rev1 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.c1.after", shown_at="2026-10-16T12:07:00Z", statement_keys=keys_a,
        )
        self.assertEqual(rev1["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(rev1["savedState"], "actually-unresolved")
        self.assertEqual(rev1["savedUnresolvedExplanation"]["reason"], "unexplained-reconciliation-discrepancy")

        # Statement 2 stands unaffected
        rev2 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.c2.after", shown_at="2026-10-16T12:08:00Z", statement_keys=keys_b,
        )
        self.assertEqual(rev2["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev2["savedState"], "supported-loss")
        self.assertEqual(rev2["savedCalculation"]["box1a"], 460.0)

    def test_case_06_atomic_statement_removal(self) -> None:
        """Case 6: S1 & S2 initially; remove S2 -> single statement return for S1 $880 once fresh closure attested."""
        _seed_workspace_v49(self.log)

        res1 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.stmt.r1", evidence_id="ev.stmt.r1",
            actor=USER, at="2026-10-16T12:01:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_a = res1["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_a, answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.r1", evidence_ids={q: f"ev.r1.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER, at="2026-10-16T12:02:00Z", expected_revision=self.log.read().revision,
        )

        res2 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_B, statement_ref=STMT_B,
            box1a=460.0, box4=0.0, submission_id="sub.stmt.r2", evidence_id="ev.stmt.r2",
            actor=USER, at="2026-10-16T12:03:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_b = res2["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_b, answers=SUPPORTED_ANSWERS_B,
            submission_id="sub.ans.r2", evidence_ids={q: f"ev.r2.{q}" for q in SUPPORTED_ANSWERS_B},
            actor=USER, at="2026-10-16T12:04:00Z", expected_revision=self.log.read().revision,
        )
        close_f1099k_family_durably(
            self.log, self.registry, submission_id="sub.close.r", actor=USER,
            at="2026-10-16T12:05:00Z", expected_revision=self.log.read().revision,
        )

        # Remove Statement 2 atomically
        rem_res = retract_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_B,
            statement_ref=STMT_B,
            submission_id="sub.stmt.r2.remove",
            actor=USER,
            at="2026-10-16T12:06:00Z",
            expected_revision=self.log.read().revision,
        )

        # Attest fresh closure on the post-removal horizon
        close_f1099k_family_durably(
            self.log,
            self.registry,
            submission_id="sub.close.after_rm",
            evidence_id="ev.close.after.rm",
            actor=USER,
            at="2026-10-16T12:07:00Z",
            expected_revision=rem_res["revision"],
        )

        outcome = self._run("run-case-06-removed")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        top_sec = next(s for s in model["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(float(top_sec["resolved"]["value"]), 880.0)

        # S1 is the only statement in explanation
        f1099k_expl = model.get("f1099kStatementExplanation", {})
        self.assertIn(keys_a["statement"], f1099k_expl)
        self.assertNotIn(keys_b["statement"], f1099k_expl)

        # S1 review reloads cleanly
        rev1 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.r1.after", shown_at="2026-10-16T12:08:00Z", statement_keys=keys_a,
        )
        self.assertEqual(rev1["savedCalculation"]["box1a"], 880.0)

    def test_case_07_single_statement_f1099k_invariant(self) -> None:
        """Case 7: Single-statement Form 1099-K invariant (zero regressions in single-statement behavior).

        Form 1098 single-statement coverage is tested in the unit-lane mortgage modules:
        tests/test_f1098_circumstances_calculation.py,
        tests/test_f1098_circumstances_explanation.py,
        tests/test_f1098_circumstances_vocabulary.py.
        """
        _seed_workspace_v49(self.log)

        res1 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.stmt.s1", evidence_id="ev.stmt.s1",
            actor=USER, at="2026-10-16T12:01:00Z", expected_revision=self.log.read().revision,
            close_family=True,
        )
        keys_a = res1["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_a, answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.s1", evidence_ids={q: f"ev.s1.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER, at="2026-10-16T12:02:00Z", expected_revision=self.log.read().revision,
        )

        outcome = self._run("run-case-07-single")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        top_sec = next(s for s in model["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(float(top_sec["resolved"]["value"]), 880.0)

        rev1 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.s1", shown_at="2026-10-16T12:03:00Z", statement_keys=keys_a,
        )
        self.assertEqual(rev1["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev1["savedState"], "supported-loss")
        self.assertEqual(rev1["savedCalculation"]["box1a"], 880.0)

    def test_case_08_v1_closed_empty_workspace_upgraded_on_first_statement(self) -> None:
        """Case 8: v1 closed-empty chain -> record first statement under v2 -> handover staged, top entry publishes $880 once closed."""
        _seed_workspace_v49(self.log)

        # 1. Closed-empty v1
        res1 = record_f1099k_no_statements_durably(
            self.log, self.registry, submission_id="sub.closed.empty.v1",
            evidence_id="ev.closed.empty.v1", actor=USER, at="2026-10-16T12:01:00Z",
            expected_revision=self.log.read().revision, family_version="v1",
        )

        # 2. Record first statement under v2 with close_family=False
        res2 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.stmt.v2.first", evidence_id="ev.stmt.v2.first",
            actor=USER, at="2026-10-16T12:02:00Z", expected_revision=res1["revision"],
            family_version="v2", close_family=False,
        )
        keys_a = res2["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_a, answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.v2.first", evidence_ids={q: f"ev.v2.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER, at="2026-10-16T12:03:00Z", expected_revision=res2["revision"],
        )

        # Unclosed v2 horizon halts top entry
        run_unclosed = self._run("run-case-08-unclosed")
        self.assertIsNone(run_unclosed.refusal)
        assert run_unclosed.presentation_path is not None
        model_unclosed = json.loads(run_unclosed.presentation_path.read_text("utf-8"))
        top_unclosed = next(s for s in model_unclosed["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(top_unclosed["resolved"]["disposition"], "blocked")

        # Attest fresh closure for v2 horizon
        close_f1099k_family_durably(
            self.log, self.registry, submission_id="sub.close.v2", actor=USER,
            at="2026-10-16T12:04:00Z", expected_revision=self.log.read().revision,
        )

        # Now top entry publishes $880.00
        run_closed = self._run("run-case-08-closed")
        self.assertIsNone(run_closed.refusal)
        assert run_closed.presentation_path is not None
        model_closed = json.loads(run_closed.presentation_path.read_text("utf-8"))
        top_closed = next(s for s in model_closed["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(float(top_closed["resolved"]["value"]), 880.0)

    def test_case_09_v1_single_statement_workspace_upgraded_on_second_statement(self) -> None:
        """Case 9: v1 single-statement -> record second statement under v2 -> handover staged, top entry publishes $1,340 once closed."""
        _seed_workspace_v49(self.log)

        # 1. Closed v1 statement
        res1 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.stmt.v1.one", evidence_id="ev.stmt.v1.one",
            actor=USER, at="2026-10-16T12:01:00Z", expected_revision=self.log.read().revision,
            family_version="v1", close_family=True,
        )
        keys_a = res1["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_a, answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.v1.one", evidence_ids={q: f"ev.v1.one.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER, at="2026-10-16T12:02:00Z", expected_revision=self.log.read().revision,
        )

        # 2. Record second statement under v2
        res2 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_B, statement_ref=STMT_B,
            box1a=460.0, box4=0.0, submission_id="sub.stmt.v2.two", evidence_id="ev.stmt.v2.two",
            actor=USER, at="2026-10-16T12:03:00Z", expected_revision=self.log.read().revision,
            family_version="v2", close_family=False,
        )
        keys_b = res2["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_b, answers=SUPPORTED_ANSWERS_B,
            submission_id="sub.ans.v2.two", evidence_ids={q: f"ev.v2.two.{q}" for q in SUPPORTED_ANSWERS_B},
            actor=USER, at="2026-10-16T12:04:00Z", expected_revision=self.log.read().revision,
        )

        # Unclosed v2 halts top entry
        run_unclosed = self._run("run-case-09-unclosed")
        self.assertIsNone(run_unclosed.refusal)
        assert run_unclosed.presentation_path is not None
        model_unclosed = json.loads(run_unclosed.presentation_path.read_text("utf-8"))
        top_unclosed = next(s for s in model_unclosed["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(top_unclosed["resolved"]["disposition"], "blocked")

        # Attest fresh closure for v2 horizon
        close_f1099k_family_durably(
            self.log, self.registry, submission_id="sub.close.v2.two", actor=USER,
            at="2026-10-16T12:05:00Z", expected_revision=self.log.read().revision,
        )

        # Combined top entry publishes $1,340.00
        run_closed = self._run("run-case-09-closed")
        self.assertIsNone(run_closed.refusal)
        assert run_closed.presentation_path is not None
        model_closed = json.loads(run_closed.presentation_path.read_text("utf-8"))
        top_closed = next(s for s in model_closed["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(float(top_closed["resolved"]["value"]), 1340.0)

        # Both statements are retained in v2 review
        rev1 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, run_closed.presentation_path, self.records,
            review_id="rev.v2.one", shown_at="2026-10-16T12:06:00Z", statement_keys=keys_a,
        )
        rev2 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, run_closed.presentation_path, self.records,
            review_id="rev.v2.two", shown_at="2026-10-16T12:07:00Z", statement_keys=keys_b,
        )
        self.assertEqual(rev1["savedCalculation"]["box1a"], 880.0)
        self.assertEqual(rev2["savedCalculation"]["box1a"], 460.0)

    def test_case_10_untouched_v1_workspace_under_successor_package(self) -> None:
        """Case 10: Untouched v1 workspace under successor package preserves historical presentation; new run unclosed."""
        _seed_workspace_v48(self.log)

        # Record v1 statement and closure under v1 package
        res1 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.stmt.v1.hist", evidence_id="ev.stmt.v1.hist",
            actor=USER, at="2026-10-16T12:01:00Z", expected_revision=self.log.read().revision,
            family_version="v1", close_family=True,
        )
        keys_a = res1["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_a, answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.v1.hist", evidence_ids={q: f"ev.v1.hist.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER, at="2026-10-16T12:02:00Z", expected_revision=self.log.read().revision,
        )

        # Run under v1 surface (SURFACE = v46 release / v48 package)
        run_v1 = self._run("run-case-10-v1", surface=SURFACE)
        self.assertIsNone(run_v1.refusal)
        assert run_v1.presentation_path is not None
        v1_pres_path = run_v1.presentation_path
        hist_revision = self.log.read().revision

        # Verify historical presentation reloads cleanly
        rev_hist = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, v1_pres_path, self.records,
            review_id="rev.v1.hist", shown_at="2026-10-16T12:03:00Z", statement_keys=keys_a,
        )
        self.assertEqual(rev_hist["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev_hist["savedState"], "supported-loss")
        self.assertEqual(rev_hist["savedCalculation"]["box1a"], 880.0)

        # Now append package adoption act for successor package v49 without any workspace writes
        pkg_data = json.loads(PACKAGE_V49_PATH.read_text("utf-8"))
        pkg_csum = pkg_data["package_checksum"]
        rel_csum = hashlib.sha256(RELEASE_V47_PATH.read_bytes()).hexdigest()
        acts_now = list(self.log.read().acts)
        first_adoption = next(a for a in acts_now if a.get("kind") == "package-adoption")
        adoption = copy.deepcopy(_load_fixture_adoption())
        adoption["act_id"] = f"demo.f1099k.adopt.v49.{len(acts_now):03d}"
        adoption["committed_against"] = len(acts_now)
        payload = adoption["payload"]
        assert isinstance(payload, dict)
        payload["supersedes"] = first_adoption["act_id"]
        payload["revision"] = 49
        payload["package"] = {"id": "tax.us.2025.package.core-calculations", "version": "v49", "checksum": pkg_csum}
        payload["release"] = {"id": "demo.release.sli-worksheet-integration.2025", "version": "v47", "checksum": rel_csum}
        payload["audit"] = {"note": "successor package adoption"}
        self.log.append_batch([adoption], expected_revision=len(acts_now))

        # Run under successor surface (SURFACE_V47)
        # Successor mapping does not admit v1 closure, so Form 1099-K family is unclosed / blocks
        run_v2 = self._run("run-case-10-v2", surface=SURFACE_V47)
        self.assertIsNone(run_v2.refusal)
        assert run_v2.presentation_path is not None
        model_v2 = json.loads(run_v2.presentation_path.read_text("utf-8"))
        top_v2 = next(s for s in model_v2["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(top_v2["resolved"]["disposition"], "blocked")

        # The v1 closure and its saved presentation stay current at the historical revision,
        # readable through associate_saved_run
        model_v1 = json.loads(v1_pres_path.read_text("utf-8"))
        assoc_hist = associate_saved_run(model_v1, self.records, hist_revision)
        self.assertEqual(assoc_hist["state"], "current")

        # But against the advanced log revision under the successor package,
        # associate_saved_run reports recalculation-needed
        assoc_now = associate_saved_run(model_v1, self.records, self.log.read().revision)
        self.assertEqual(assoc_now["state"], "recalculation-needed")

    def test_case_11_stale_older_version_write_refused(self) -> None:
        """Case 11: Workspace has active v2 chain; write with family_version='v1' raises F1099KRecordingRefused."""
        _seed_workspace_v49(self.log)

        # Establish active v2 chain
        res1 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.stmt.v2.active", evidence_id="ev.stmt.v2.active",
            actor=USER, at="2026-10-16T12:01:00Z", expected_revision=self.log.read().revision,
            family_version="v2", close_family=True,
        )
        rev_before = self.log.read().revision

        # Attempt to record under older version v1
        with self.assertRaises(F1099KRecordingRefused) as ctx:
            record_f1099k_statement_durably(
                self.log, self.registry, payer_id=PAYER_B, statement_ref=STMT_B,
                box1a=460.0, box4=0.0, submission_id="sub.stmt.v1.stale", evidence_id="ev.stmt.v1.stale",
                actor=USER, at="2026-10-16T12:02:00Z", expected_revision=rev_before,
                family_version="v1", close_family=False,
            )
        self.assertIn("cannot handover to older family version", str(ctx.exception))
        # Log is completely unmutated
        self.assertEqual(self.log.read().revision, rev_before)

    def test_case_12_candidate_c_closed_empty_v2(self) -> None:
        """Case 12: Candidate C closed-empty $0.00 on v2 -> top entry publishes $0.00."""
        _seed_workspace_v49(self.log)

        record_f1099k_no_statements_durably(
            self.log, self.registry, submission_id="sub.closed.empty.v2",
            evidence_id="ev.closed.empty.v2", actor=USER, at="2026-10-16T12:01:00Z",
            expected_revision=self.log.read().revision, family_version="v2",
        )

        outcome = self._run("run-case-12-empty")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        top_sec = next(s for s in model["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertIn(top_sec["resolved"]["disposition"], ("closure_backed_zero", "published_zero", "published_value", "computed_zero"))
        self.assertEqual(float(top_sec["resolved"]["value"]), 0.0)

    def test_case_13_gain_or_excluded_statement_beside_supported_loss(self) -> None:
        """Case 13: Statement 1 (loss $880) + Statement 2 (unsupported gain $1,200) -> top entry blocked, S1 preserved."""
        _seed_workspace_v49(self.log)

        res1 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.stmt.g1", evidence_id="ev.stmt.g1",
            actor=USER, at="2026-10-16T12:01:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_a = res1["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_a, answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.g1", evidence_ids={q: f"ev.g1.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER, at="2026-10-16T12:02:00Z", expected_revision=self.log.read().revision,
        )

        # Statement 2: Box 1a $1,200, agreed price $1,200, platform fees $100, cost $800 -> Net proceeds $1,100 > cost $800 (gain)
        gain_answers = {
            "covers-only-single-item": "yes",
            "acquired-by-purchase": "yes",
            "primary-purpose-at-acquisition": "personal-use",
            "exclusive-personal-use": "yes",
            "digital-asset-involvement": "no",
            "agreed-item-price": 1200.0,
            "shipping-arrangement": "platform-pass-through",
            "platform-fees": 100.0,
            "seller-paid-shipping": 0.0,
            "sales-tax-collected-by-platform": 0.0,
            "refund-amount": 0.0,
            "buyer-paid-shipping": 0.0,
            "cost-basis-known": "yes",
            "purchase-cost": 800.0,
            "lasting-improvements-or-adjustments": "no",
        }
        res2 = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_B, statement_ref=STMT_B,
            box1a=1200.0, box4=0.0, submission_id="sub.stmt.g2", evidence_id="ev.stmt.g2",
            actor=USER, at="2026-10-16T12:03:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_b = res2["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=keys_b, answers=gain_answers,
            submission_id="sub.ans.g2", evidence_ids={q: f"ev.g2.{q}" for q in gain_answers},
            actor=USER, at="2026-10-16T12:04:00Z", expected_revision=self.log.read().revision,
        )
        close_f1099k_family_durably(
            self.log, self.registry, submission_id="sub.close.g", actor=USER,
            at="2026-10-16T12:05:00Z", expected_revision=self.log.read().revision,
        )

        outcome = self._run("run-case-13-gain")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        top_sec = next(s for s in model["sections"] if s["field"]["id"] == TOP_ENTRY_FIELD_ID)
        self.assertEqual(top_sec["resolved"]["disposition"], "blocked")

        # Statement 1 review preserves local status supported-loss with own Box 1a
        rev1 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.g1", shown_at="2026-10-16T12:06:00Z", statement_keys=keys_a,
        )
        self.assertEqual(rev1["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev1["savedState"], "supported-loss")
        self.assertEqual(rev1["savedCalculation"]["box1a"], 880.0)

        # Statement 2 review shows unsupported-gain
        rev2 = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.g2", shown_at="2026-10-16T12:07:00Z", statement_keys=keys_b,
        )
        self.assertEqual(rev2["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(rev2["savedState"], "actually-unresolved")
        self.assertIsNone(rev2["savedCalculation"])
        self.assertEqual(rev2["savedUnresolvedExplanation"]["reason"], "unsupported-gain")


if __name__ == "__main__":
    unittest.main()
