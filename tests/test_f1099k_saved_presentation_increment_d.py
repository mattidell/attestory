"""Tests for Increment D: presentation projection & review remediation (design Unit 4).

Validates:
1. Sourcing all current subjects from finding state and currency:
   - Sourcing iterates all current Box 1a subjects from finding state and currency.
   - Statements whose reason calculation blocked are projected into
     f1099kStatementExplanation with disposition="blocked", code, and missing.
2. Saved review Route 2 snapshot:
   - Multi-statement runs report the statement's own Box 1a gross amount in
     savedCalculation, not the return-level Schedule 1 total sum.
3. Decoupling local statement review status from aggregate top-entry block:
   - On a mixed pair (supported loss + unknown cost basis), the supported statement
     reports status "supported-loss" and its own Box 1a, even though Schedule 1
     top entry is blocked and the sibling statement is unresolved.
4. Legacy unkeyed presentation gating:
   - Unkeyed presentations are accepted only for single-statement workspaces at
     matching revisions; multi-statement workspaces refuse with recalculation-needed.
5. Structural validation of blocked explanation rows in presentation model.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.presentation_projection import (
    PresentationModelError,
    _f1099k_statement_explanation,
    _validate_f1099k_statement_explanation,
    build_presentation_model,
)
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.kernel.findings import project
from packages.tax.f1099k_statement_recording import (
    close_f1099k_family_durably,
    record_f1099k_statement_answers_durably,
    record_f1099k_statement_durably,
)
from packages.tax.f1099k_statement_review import (
    review_f1099k_statement_with_saved_presentation,
)
from packages.tax.loader import tax_registry
from tests.test_f1098_mortgage_interest_line12e_track2 import _load_fixture_adoption
from tests.test_f1099k_personal_item_sale_track1 import (
    CONTENT,
    RELEASE_DIR,
    ROOT,
    SCOPE,
    USER,
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
    payload["audit"] = {"note": "synthetic Form 1099-K v49 test"}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = USER
    return built


def _seed_workspace_v49(log: ActLog) -> None:
    seed_acts = _finish_acts_v49(_make_base_acts())
    log.append_batch(seed_acts, expected_revision=0)


class F1099KSavedPresentationIncrementDTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = tax_registry()
        self.temp = TemporaryDirectory(prefix="f1099k-inc-d-")
        self.addCleanup(self.temp.cleanup)
        self.ws_dir = Path(self.temp.name)
        self.capability = WorkspaceCapability(self.ws_dir)
        self.log = ActLog(self.ws_dir, self.registry)
        _seed_workspace_v49(self.log)
        self.records = RecordStream(self.ws_dir / "records", DerivationSchemas())

    def _run(self, run_id: str) -> Any:
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
            surface=SURFACE_V47,
            output_name=f"{run_id}.json",
        )

    def test_saved_projection_sources_all_current_subjects_including_blocked(self) -> None:
        """Finding F5 (hazard 2): current subjects whose reason blocked are projected as blocked rows."""
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
        close_f1099k_family_durably(
            self.log,
            self.registry,
            submission_id="sub.close",
            actor=USER,
            at="2026-10-16T12:04:00Z",
            expected_revision=self.log.read().revision,
        )

        outcome = self._run("run-all-subjects")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text("utf-8"))

        f1099k_expl = model.get("f1099kStatementExplanation")
        self.assertIsInstance(f1099k_expl, dict)
        self.assertIn(keys_a["statement"], f1099k_expl)
        self.assertIn(keys_b["statement"], f1099k_expl)

        expl_a = f1099k_expl[keys_a["statement"]]
        self.assertEqual(expl_a["reason"], "supported-loss")
        self.assertIsNotNone(expl_a["computation"])
        self.assertEqual(expl_a["statementKeys"]["statement"], keys_a["statement"])

        expl_b = f1099k_expl[keys_b["statement"]]
        self.assertEqual(expl_b["statementKeys"]["statement"], keys_b["statement"])

        # Also verify projection directly when a reason is blocked in dispositions
        blocked_disp_row = {
            "artifact_id": "tax.us.2025.rule.f1099k-statement-loss-reason",
            "symbol": f"tax.us.2025.f1099k.statement-loss-reason|payer={PAYER_B},statement={keys_b['statement']},tax-year=2025",
            "disposition": "blocked",
            "code": "DEPENDENCY_ABSENT",
            "missing": ["tax.us.2025.f1099k.purchase-cost"],
            "pins": [],
        }
        # Run _f1099k_statement_explanation directly with blocked disposition row for B
        matching_pubs = [
            p for p in (outcome.publications or ())
            if p.finding.get("symbol", "").startswith(f"tax.us.2025.f1099k.statement-loss-reason|payer={PAYER_A}")
        ]
        proj_expl = _f1099k_statement_explanation(
            resolved_members=[],
            state=project(self.log.read().acts, self.registry),
            publications=matching_pubs,
            publications_by_id={p.finding["id"]: p.finding for p in matching_pubs},
            dispositions=[blocked_disp_row],
        )
        self.assertIsNotNone(proj_expl)
        assert proj_expl is not None
        self.assertIn(keys_b["statement"], proj_expl)
        b_expl = proj_expl[keys_b["statement"]]
        self.assertEqual(b_expl["disposition"], "blocked")
        self.assertEqual(b_expl["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(b_expl["missing"], ["tax.us.2025.f1099k.purchase-cost"])
        self.assertIsNone(b_expl["computation"])
        self.assertEqual(b_expl["assumptions"], "none")

    def test_saved_review_route2_extracts_own_box1a(self) -> None:
        """Finding F5 (hazard 1, Route 2): savedCalculation carries own Box 1a, not the combined sum."""
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
        close_f1099k_family_durably(
            self.log,
            self.registry,
            submission_id="sub.close",
            actor=USER,
            at="2026-10-16T12:05:00Z",
            expected_revision=self.log.read().revision,
        )

        outcome = self._run("run-route2-own-box1a")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text("utf-8"))

        # Verify Schedule 1 top-entry is combined sum $1,340.00
        sec = next(s for s in model["sections"] if s["field"]["id"] == "tax.us.2025.schedule1.top-entry.form-field")
        self.assertEqual(float(sec["resolved"]["value"]), 1340.0)

        # Statement 1 review shows own Box 1a ($880.00)
        rev_a = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="rev.stmt.a",
            shown_at="2026-10-16T12:06:00Z",
            statement_keys=keys_a,
        )
        self.assertEqual(rev_a["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev_a["savedState"], "supported-loss")
        self.assertIsNotNone(rev_a["savedCalculation"])
        self.assertEqual(rev_a["savedCalculation"]["box1a"], 880.0)
        self.assertNotEqual(rev_a["savedCalculation"]["box1a"], 1340.0)

        # Statement 2 review shows own Box 1a ($460.00)
        rev_b = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="rev.stmt.b",
            shown_at="2026-10-16T12:06:00Z",
            statement_keys=keys_b,
        )
        self.assertEqual(rev_b["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev_b["savedState"], "supported-loss")
        self.assertIsNotNone(rev_b["savedCalculation"])
        self.assertEqual(rev_b["savedCalculation"]["box1a"], 460.0)
        self.assertNotEqual(rev_b["savedCalculation"]["box1a"], 1340.0)

    def test_saved_review_decouples_local_reason_from_aggregate_block(self) -> None:
        """Finding F5 (hazard 3): an aggregate blockage on Schedule 1 does not brand a supported sibling."""
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
        unknown_cost_answers = dict(SUPPORTED_ANSWERS_B)
        unknown_cost_answers["cost-basis-known"] = "cannot-tell"
        unknown_cost_answers["purchase-cost"] = 0.0
        unknown_cost_answers["lasting-improvements-or-adjustments"] = "no"

        ev_b = {q: f"ev.b.{q}" for q in unknown_cost_answers}

        record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=keys_b,
            answers=unknown_cost_answers,
            submission_id="sub.ans.b",
            evidence_ids=ev_b,
            actor=USER,
            at="2026-10-16T12:04:00Z",
            expected_revision=self.log.read().revision,
        )
        close_f1099k_family_durably(
            self.log,
            self.registry,
            submission_id="sub.close",
            actor=USER,
            at="2026-10-16T12:05:00Z",
            expected_revision=self.log.read().revision,
        )

        outcome = self._run("run-mixed-pair")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text("utf-8"))

        # Schedule 1 top entry is blocked
        sec = next(s for s in model["sections"] if s["field"]["id"] == "tax.us.2025.schedule1.top-entry.form-field")
        self.assertEqual(sec["resolved"]["disposition"], "blocked")

        # Statement 1 preserves local supported-loss status and own Box 1a
        rev_a = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="rev.stmt.a",
            shown_at="2026-10-16T12:06:00Z",
            statement_keys=keys_a,
        )
        self.assertEqual(rev_a["savedCalculationState"], "current-supported-loss")
        self.assertEqual(rev_a["savedState"], "supported-loss")
        self.assertIsNotNone(rev_a["savedCalculation"])
        self.assertEqual(rev_a["savedCalculation"]["box1a"], 880.0)
        self.assertIsNone(rev_a["savedUnresolvedExplanation"])

        # Statement 2 shows its published reason (cost-basis-unknown)
        rev_b = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="rev.stmt.b",
            shown_at="2026-10-16T12:06:00Z",
            statement_keys=keys_b,
        )
        self.assertEqual(rev_b["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(rev_b["savedState"], "actually-unresolved")
        self.assertIsNone(rev_b["savedCalculation"])
        self.assertIsNotNone(rev_b["savedUnresolvedExplanation"])
        self.assertEqual(rev_b["savedUnresolvedExplanation"]["reason"], "cost-basis-unknown")

    def test_legacy_unkeyed_presentation_gating(self) -> None:
        """Finding F5 (hazard 5): legacy unkeyed presentation is refused on multi-statement workspaces."""
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
        close_f1099k_family_durably(
            self.log,
            self.registry,
            submission_id="sub.close1",
            actor=USER,
            at="2026-10-16T12:03:00Z",
            expected_revision=self.log.read().revision,
        )

        outcome = self._run("run-single-for-legacy")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text("utf-8"))

        # Convert f1099kStatementExplanation to legacy unkeyed shape
        expl = model["f1099kStatementExplanation"][keys_a["statement"]]
        model["f1099kStatementExplanation"] = {
            "computation": expl["computation"],
            "assumptions": expl["assumptions"],
        }
        legacy_path = self.ws_dir / "legacy_presentation.json"
        legacy_path.write_text(json.dumps(model), encoding="utf-8")

        # 1. On single-statement workspace, legacy unkeyed presentation is accepted
        rev_single = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            legacy_path,
            self.records,
            review_id="rev.legacy.single",
            shown_at="2026-10-16T12:04:00Z",
            statement_keys=keys_a,
        )
        self.assertEqual(rev_single["savedCalculationState"], "current-supported-loss")

        # 2. Add second statement to workspace -> ActLog now has 2 current statements
        record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_B,
            statement_ref=STMT_B,
            box1a=460.0,
            box4=0.0,
            submission_id="sub.stmt.2",
            evidence_id="ev.stmt.2",
            actor=USER,
            at="2026-10-16T12:05:00Z",
            expected_revision=self.log.read().revision,
            close_family=False,
        )

        # Multiple statements with legacy unkeyed presentation refuses as recalculation-needed
        rev_multi = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            legacy_path,
            self.records,
            review_id="rev.legacy.multi",
            shown_at="2026-10-16T12:06:00Z",
            statement_keys=keys_a,
        )
        self.assertEqual(rev_multi["savedCalculationState"], "recalculation-needed")

    def test_validator_accepts_blocked_explanation_rows(self) -> None:
        """Validator accepts blocked explanation rows and rejects malformed fields."""
        valid_blocked = {
            "stmt.1": {
                "statementKeys": {"payer": "p", "statement": "s", "tax-year": "2025"},
                "disposition": "blocked",
                "code": "DEPENDENCY_ABSENT",
                "missing": ["tax.us.2025.f1099k.purchase-cost"],
                "computation": None,
                "assumptions": "none",
            }
        }
        _validate_f1099k_statement_explanation(valid_blocked)

        # Missing code
        invalid_code = copy.deepcopy(valid_blocked)
        del invalid_code["stmt.1"]["code"]
        with self.assertRaises(PresentationModelError):
            _validate_f1099k_statement_explanation(invalid_code)

        # Missing missing-dependencies list
        invalid_missing = copy.deepcopy(valid_blocked)
        del invalid_missing["stmt.1"]["missing"]
        with self.assertRaises(PresentationModelError):
            _validate_f1099k_statement_explanation(invalid_missing)
