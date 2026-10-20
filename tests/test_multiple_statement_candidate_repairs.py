"""Regressions for multiple-statement circumstances candidate repairs.

Covers the four reproduced candidate defects:
1. Re-recording a removed statement is refused and log is unchanged;
2. Colliding statement pair keeps two explanations and each review returns its own;
3. Populated v1 workspace on v49 re-attestation records handover + fresh closure in one save;
4. Supported-loss statement beside a blocking sibling keeps local result without 'entered' wording.
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
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import project
from packages.tax.f1099k_statement_recording import (
    CLOSURE_TYPE,
    FAMILY_ID,
    STATEMENT_BOX1A,
    F1099KRecordingRefused,
    _token,
    close_f1099k_family_durably,
    record_f1099k_statement_answers_durably,
    record_f1099k_statement_durably,
    retract_f1099k_statement_durably,
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
    **SUPPORTED_ANSWERS_A,
    "agreed-item-price": 460.0,
    "platform-fees": 60.0,
    "sales-tax-collected-by-platform": 0.0,
    "buyer-paid-shipping": 0.0,
    "purchase-cost": 600.0,
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


class MultipleStatementCandidateRepairsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = tax_registry()
        self.temp = TemporaryDirectory(prefix="multiple-statement-repairs-")
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

    def test_defect1_re_record_after_removal_is_refused_and_log_unchanged(self) -> None:
        """Defect 1 regression: re-record after removal is refused before writing and log is unchanged."""
        # Record Statement A
        res_a = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_A,
            statement_ref=STMT_A,
            box1a=880.0,
            box4=0.0,
            submission_id="sub.stmt.a",
            evidence_id="ev.stmt.a",
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_a = res_a["statement_keys"]
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

        # Durably retract (remove) Statement A
        retract_f1099k_statement_durably(
            self.log,
            self.registry,
            statement_keys=keys_a,
            submission_id="sub.rm.a",
            evidence_id="ev.rm.a",
            actor=USER,
            at="2026-10-16T12:04:00Z",
            expected_revision=self.log.read().revision,
        )

        # Snapshot log state after removal
        log_after_removal = self.log.read()
        snapshot_acts = copy.deepcopy(log_after_removal.acts)
        snapshot_revision = log_after_removal.revision

        # Verify Box 1a finding is displaced by withdrawal root
        state_after_rm = project(tuple(copy.deepcopy(row) for row in snapshot_acts), self.registry)
        fact_b1a_id = fact_id_for(STATEMENT_BOX1A, tuple(sorted(keys_a.items())))
        self.assertIn(fact_b1a_id, state_after_rm.withdrawn_fact_ids)
        current_fids = compute_currency(state_after_rm).current_finding_ids
        current_b1a = [
            fid for fid, f in state_after_rm.findings.items()
            if f.get("fact_id") == fact_b1a_id and fid in current_fids
        ]
        self.assertEqual(current_b1a, [])

        # Attempt to re-record Statement A with fresh submission and evidence IDs
        with self.assertRaises(F1099KRecordingRefused) as ctx:
            record_f1099k_statement_durably(
                self.log,
                self.registry,
                payer_id=PAYER_A,
                statement_ref=STMT_A,
                box1a=880.0,
                box4=0.0,
                submission_id="sub.stmt.a.fresh",
                evidence_id="ev.stmt.a.fresh",
                actor=USER,
                at="2026-10-16T12:05:00Z",
                expected_revision=snapshot_revision,
                close_family=False,
            )

        # Assert named refusal reason
        self.assertIn("was removed and cannot be recorded again under the same identity", str(ctx.exception))
        self.assertIn(PAYER_A, str(ctx.exception))
        self.assertIn(STMT_A, str(ctx.exception))

        # Assert log is completely unchanged
        fresh_log = self.log.read()
        self.assertEqual(fresh_log.revision, snapshot_revision)
        self.assertEqual(fresh_log.acts, snapshot_acts)

    def test_defect2_colliding_pair_keeps_two_explanations_and_each_review_returns_its_own(self) -> None:
        """Defect 2 regression: colliding statement entity IDs keep two distinct explanations and reviews."""
        # Statement 1: payer demo.platform with ref 2025.loan -> entity stmt.demo.platform.2025.2025.loan
        payer_1 = "demo.platform"
        ref_1 = "2025.loan"
        res1 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=payer_1,
            statement_ref=ref_1,
            box1a=880.0,
            box4=0.0,
            submission_id="sub.stmt.coll.1",
            evidence_id="ev.stmt.coll.1",
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_1 = res1["statement_keys"]
        self.assertEqual(keys_1["statement"], "stmt.demo.platform.2025.2025.loan")
        self.assertEqual(keys_1["payer"], payer_1)

        record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=keys_1,
            answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.ans.coll.1",
            evidence_ids={q: f"ev.c1.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=self.log.read().revision,
        )

        # Statement 2: payer demo.platform.2025 with ref loan -> entity stmt.demo.platform.2025.2025.loan
        payer_2 = "demo.platform.2025"
        ref_2 = "loan"
        res2 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=payer_2,
            statement_ref=ref_2,
            box1a=460.0,
            box4=0.0,
            submission_id="sub.stmt.coll.2",
            evidence_id="ev.stmt.coll.2",
            actor=USER,
            at="2026-10-16T12:03:00Z",
            expected_revision=self.log.read().revision,
            close_family=False,
        )
        keys_2 = res2["statement_keys"]
        self.assertEqual(keys_2["statement"], "stmt.demo.platform.2025.2025.loan")
        self.assertEqual(keys_2["payer"], payer_2)
        # Identical statement entity ID, but distinct full identity keys:
        self.assertEqual(keys_1["statement"], keys_2["statement"])
        self.assertNotEqual(keys_1["payer"], keys_2["payer"])

        unknown_cost_answers = dict(SUPPORTED_ANSWERS_A)
        unknown_cost_answers["agreed-item-price"] = 460.0
        unknown_cost_answers["cost-basis-known"] = "cannot-tell"
        unknown_cost_answers["purchase-cost"] = "cannot-tell"
        record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=keys_2,
            answers=unknown_cost_answers,
            submission_id="sub.ans.coll.2",
            evidence_ids={q: f"ev.c2.{q}" for q in unknown_cost_answers},
            actor=USER,
            at="2026-10-16T12:04:00Z",
            expected_revision=self.log.read().revision,
        )

        close_f1099k_family_durably(
            self.log,
            self.registry,
            submission_id="sub.close.coll",
            actor=USER,
            at="2026-10-16T12:05:00Z",
            expected_revision=self.log.read().revision,
        )

        outcome = self._run("run-colliding-pair")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text("utf-8"))

        # 1. Assert finding currentness and exact statement identities
        state = project(tuple(copy.deepcopy(row) for row in self.log.read().acts), self.registry)
        current_fids = compute_currency(state).current_finding_ids
        lattice = facts_of(state.fact_state)
        b1a_facts = {
            f["fact_id"]: f["value"]
            for fid, f in state.findings.items()
            if fid in current_fids and f.get("fact_id") in lattice and lattice[f["fact_id"]].fact_type_id == STATEMENT_BOX1A
        }
        fact1_id = fact_id_for(STATEMENT_BOX1A, tuple(sorted(keys_1.items())))
        fact2_id = fact_id_for(STATEMENT_BOX1A, tuple(sorted(keys_2.items())))
        self.assertIn(fact1_id, b1a_facts)
        self.assertIn(fact2_id, b1a_facts)
        self.assertEqual(b1a_facts[fact1_id], 880.0)
        self.assertEqual(b1a_facts[fact2_id], 460.0)

        # 2. Assert top entry disposition: blocked because S2 is cost-basis-unknown
        top_sec = next(s for s in model["sections"] if s["field"]["id"] == "tax.us.2025.schedule1.top-entry.form-field")
        self.assertEqual(top_sec["resolved"]["disposition"], "blocked")

        # 3. Assert saved explanations: the colliding pair keeps TWO explanations with their own reasons
        f1099k_expl = model.get("f1099kStatementExplanation")
        self.assertIsInstance(f1099k_expl, dict)
        self.assertEqual(len(f1099k_expl), 2)

        self.assertEqual(
            sorted(tuple(sorted(v["statementKeys"].items())) for v in f1099k_expl.values()),
            sorted([tuple(sorted(keys_1.items())), tuple(sorted(keys_2.items()))]),
        )
        expls_by_payer = {
            v["statementKeys"]["payer"]: v
            for v in f1099k_expl.values()
            if isinstance(v, dict) and "statementKeys" in v
        }
        self.assertIn(payer_1, expls_by_payer)
        self.assertIn(payer_2, expls_by_payer)
        self.assertEqual(expls_by_payer[payer_1]["reason"], "supported-loss")
        self.assertEqual(expls_by_payer[payer_2]["reason"], "cost-basis-unknown")

        # 4. Assert review reader lookup returns each statement's own explanation
        rev_1 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="rev.coll.1",
            shown_at="2026-10-16T12:06:00Z",
            statement_keys=keys_1,
        )
        self.assertEqual(rev_1["savedCalculationState"], "current-supported-loss")
        self.assertIsNotNone(rev_1["savedCalculation"])
        self.assertEqual(rev_1["savedCalculation"]["box1a"], 880.0)
        self.assertEqual(rev_1["savedCalculation"]["reason"], "supported-loss")
        self.assertIsNone(rev_1["savedUnresolvedExplanation"])

        rev_2 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="rev.coll.2",
            shown_at="2026-10-16T12:07:00Z",
            statement_keys=keys_2,
        )
        self.assertEqual(rev_2["savedCalculationState"], "current-unresolved-explanation")
        self.assertIsNone(rev_2["savedCalculation"])
        self.assertIsNotNone(rev_2["savedUnresolvedExplanation"])
        self.assertEqual(rev_2["savedUnresolvedExplanation"]["reason"], "cost-basis-unknown")
        self.assertEqual(rev_2["savedUnresolvedExplanation"]["statementKeys"], keys_2)
        self.assertEqual(rev_1["statement"]["keys"], keys_1)
        self.assertEqual(rev_2["statement"]["keys"], keys_2)
        # The blocking reason names the second statement's full keys, so only it carries the sentence
        own_reasons = rev_2["savedUnresolvedExplanation"]["reasons"]
        self.assertEqual(len(own_reasons), 1)
        self.assertIn(f"payer={payer_2},", own_reasons[0]["factId"])
        self.assertEqual(rev_2["savedUnresolvedExplanation"]["reasonSentences"], [own_reasons[0]["sentence"]])

        # 5. The reader never substitutes a differently keyed statement: with only the
        # first statement's explanation on disk, the second statement reads none of it.
        model_only_1 = copy.deepcopy(model)
        model_only_1["f1099kStatementExplanation"] = {
            k: v for k, v in f1099k_expl.items() if v["statementKeys"] == keys_1
        }
        self.assertEqual(len(model_only_1["f1099kStatementExplanation"]), 1)
        only_1_path = outcome.presentation_path.with_name("only-first-explanation.json")
        only_1_path.write_text(json.dumps(model_only_1), "utf-8")
        rev_2_sub = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            only_1_path,
            self.records,
            review_id="rev.coll.2.sub",
            shown_at="2026-10-16T12:08:00Z",
            statement_keys=keys_2,
        )
        self.assertNotEqual(rev_2_sub["savedCalculationState"], "current-supported-loss")
        self.assertIsNone(rev_2_sub["savedCalculation"])
        saved_unres_2 = rev_2_sub["savedUnresolvedExplanation"]
        self.assertIsNotNone(saved_unres_2)
        self.assertNotIn("reason", saved_unres_2)
        self.assertIsNone(saved_unres_2["computation"])



def _top_section(model: dict[str, Any]) -> dict[str, Any]:
    return next(sec for sec in model["sections"] if sec["field"]["id"] == TOP_ENTRY_FIELD_ID)


def _adopt_v49_later(log: ActLog) -> None:
    """Append the successor package adoption to a workspace that was populated on v1."""
    pkg_csum = json.loads(PACKAGE_V49_PATH.read_text("utf-8"))["package_checksum"]
    rel_csum = hashlib.sha256(RELEASE_V47_PATH.read_bytes()).hexdigest()
    acts_now = list(log.read().acts)
    first_adoption = next(a for a in acts_now if a.get("kind") == "package-adoption")
    adoption = copy.deepcopy(_load_fixture_adoption())
    adoption["act_id"] = f"demo.f1099k.adopt.v49.{len(acts_now):03d}"
    adoption["committed_against"] = len(acts_now)
    adoption["actor"] = USER
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["supersedes"] = first_adoption["act_id"]
    payload["revision"] = 49
    payload["package"] = {"id": "tax.us.2025.package.core-calculations", "version": "v49", "checksum": pkg_csum}
    payload["release"] = {"id": "demo.release.sli-worksheet-integration.2025", "version": "v47", "checksum": rel_csum}
    payload["audit"] = {"note": "successor package adoption"}
    log.append_batch([adoption], expected_revision=len(acts_now))


class ReattestationAfterAdoptionTests(unittest.TestCase):
    """Defect 3: a populated v1 workspace adopted onto v49 re-attests completeness."""

    def setUp(self) -> None:
        self.registry = tax_registry()
        self.temp = TemporaryDirectory(prefix="multiple-statement-reattest-")
        self.addCleanup(self.temp.cleanup)
        self.ws_dir = Path(self.temp.name)
        self.capability = WorkspaceCapability(self.ws_dir)
        self.log = ActLog(self.ws_dir, self.registry)
        self.log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        res_a = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.v1.a", evidence_id="ev.v1.a",
            actor=USER, at="2026-10-16T12:01:00Z", expected_revision=self.log.read().revision,
            family_version="v1", close_family=False,
        )
        self.keys_a = res_a["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=self.keys_a, answers=SUPPORTED_ANSWERS_A,
            submission_id="sub.v1.ans.a", evidence_ids={q: f"ev.v1.a.{q}" for q in SUPPORTED_ANSWERS_A},
            actor=USER, at="2026-10-16T12:02:00Z", expected_revision=self.log.read().revision,
        )
        res_b = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_B, statement_ref=STMT_B,
            box1a=460.0, box4=0.0, submission_id="sub.v1.b", evidence_id="ev.v1.b",
            actor=USER, at="2026-10-16T12:03:00Z", expected_revision=self.log.read().revision,
            family_version="v1", close_family=True,
        )
        self.keys_b = res_b["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=self.keys_b, answers=SUPPORTED_ANSWERS_B,
            submission_id="sub.v1.ans.b", evidence_ids={q: f"ev.v1.b.{q}" for q in SUPPORTED_ANSWERS_B},
            actor=USER, at="2026-10-16T12:04:00Z", expected_revision=self.log.read().revision,
        )
        self.old_closure_fids = self._closure_finding_ids()
        self.assertEqual(len(self.old_closure_fids), 1)
        self.assertEqual(self._chain()[0], "v1")
        _adopt_v49_later(self.log)

    def _state(self) -> Any:
        return project(tuple(copy.deepcopy(row) for row in self.log.read().acts), self.registry)

    def _chain(self) -> tuple[str, str]:
        scope = tuple(sorted({"tax-year": "2025", "subject": "demo.primary"}.items()))
        for (fid, ver, sc), horizon in self._state().horizon_state.current_by_chain.items():
            if fid == FAMILY_ID and sc == scope:
                return ver, horizon
        raise AssertionError("no current family chain")

    def _closure_finding_ids(self) -> list[str]:
        state = self._state()
        return [fid for fid, f in state.findings.items() if f["fact_id"].startswith(f"{CLOSURE_TYPE}|")]

    def _current_ids(self) -> Any:
        return compute_currency(self._state()).current_finding_ids

    def _current_b1a(self) -> dict[tuple[tuple[str, str], ...], float]:
        state = self._state()
        current = self._current_ids()
        lattice = facts_of(state.fact_state)
        return {
            tuple(sorted(lattice[f["fact_id"]].keys)): f["value"]
            for fid, f in state.findings.items()
            if fid in current and f.get("fact_id") in lattice
            and lattice[f["fact_id"]].fact_type_id == STATEMENT_BOX1A
        }

    def _run(self, run_id: str) -> Any:
        contents = self.log.read()
        return live_coordinate_run(
            self.capability, repo_root=ROOT, authoritative_acts=contents.acts,
            workspace_revision=contents.revision, run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=SURFACE_V47, output_name=f"{run_id}.json",
        )

    def _assert_one_batch_handover_and_fresh_closure(
        self, rev_before: int, result: dict[str, Any], submission_id: str, evidence_id: str,
    ) -> None:
        contents = self.log.read()
        new_acts = contents.acts[rev_before:]
        self.assertEqual(result["revision"], contents.revision)
        token = _token(submission_id)
        # one save: every new act belongs to this submission's batch
        self.assertTrue(all(f".{token}." in a["act_id"] for a in new_acts), [a["act_id"] for a in new_acts])
        handovers = [a for a in new_acts if a["kind"] == "family-handover"]
        self.assertEqual(len(handovers), 1)
        payload = handovers[0]["payload"]
        self.assertEqual(payload["predecessor"]["family"], {"id": FAMILY_ID, "version": "v1"})
        self.assertEqual(payload["successor"]["family"], {"id": FAMILY_ID, "version": "v2"})
        old_horizon = payload["predecessor"]["horizon_id"]
        new_horizon = payload["successor"]["horizon_id"]
        self.assertNotEqual(old_horizon, new_horizon)
        # the handover precedes the closure assertion in the same batch
        closure_acts = [
            a for a in new_acts
            if a["kind"] == "assertion" and a["payload"]["finding"]["fact_id"].startswith(f"{CLOSURE_TYPE}|")
        ]
        self.assertEqual(len(closure_acts), 1)
        self.assertLess(new_acts.index(handovers[0]), new_acts.index(closure_acts[0]))
        closure = closure_acts[0]["payload"]["finding"]
        self.assertEqual(closure["fact_id"], f"{CLOSURE_TYPE}|family-horizon={new_horizon},tax-year=2025")
        self.assertIs(closure["value"], True)
        # the closure is the person's new answer: fresh evidence, not the old closure copied
        self.assertEqual(closure["evidence_ids"], [evidence_id])
        # chain moved to the successor horizon at v2
        self.assertEqual(self._chain(), ("v2", new_horizon))
        current = self._current_ids()
        self.assertIn(closure["id"], current)
        for old_fid in self.old_closure_fids:
            self.assertNotIn(old_fid, current)
        # exactly one current closure, and both statements stay current with their exact keys
        self.assertEqual([fid for fid in self._closure_finding_ids() if fid in current], [closure["id"]])
        self.assertEqual(
            self._current_b1a(),
            {tuple(sorted(self.keys_a.items())): 880.0, tuple(sorted(self.keys_b.items())): 460.0},
        )

    def test_defect3_before_reattestation_adopted_workspace_does_not_publish(self) -> None:
        outcome = self._run("run-reattest-before")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        self.assertEqual(_top_section(model)["resolved"]["disposition"], "blocked")
        self.assertEqual(self._chain()[0], "v1")

    def test_defect3_close_family_stages_handover_and_fresh_closure_in_one_save(self) -> None:
        rev_before = self.log.read().revision
        result = close_f1099k_family_durably(
            self.log, self.registry, submission_id="sub.reattest", evidence_id="ev.reattest",
            actor=USER, at="2026-10-16T12:10:00Z", expected_revision=rev_before,
        )
        self._assert_one_batch_handover_and_fresh_closure(rev_before, result, "sub.reattest", "ev.reattest")

        outcome = self._run("run-reattest-after")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        top = _top_section(model)
        self.assertNotEqual(top["resolved"]["disposition"], "blocked")
        self.assertEqual(float(top["resolved"]["value"]), 1340.0)

    def test_defect3_close_family_without_newer_adoption_still_targets_current_chain(self) -> None:
        """Passing the current chain version targets that chain and stages no handover."""
        rev_before = self.log.read().revision
        old_horizon = self._chain()[1]
        with self.assertRaises(F1099KRecordingRefused) as ctx:
            close_f1099k_family_durably(
                self.log, self.registry, submission_id="sub.reattest.v1", evidence_id="ev.reattest.v1",
                actor=USER, at="2026-10-16T12:10:00Z", expected_revision=rev_before, family_version="v1",
            )
        self.assertIn(f"family closure already recorded for horizon {old_horizon}", str(ctx.exception))
        self.assertEqual(self.log.read().revision, rev_before)

    def test_defect3_correction_with_close_family_takes_the_same_route(self) -> None:
        rev_before = self.log.read().revision
        result = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.corr.a", evidence_id="ev.corr.a",
            actor=USER, at="2026-10-16T12:10:00Z", expected_revision=rev_before,
            corrected=True, close_family=True,
        )
        self.assertEqual(result["statement_keys"], self.keys_a)
        self._assert_one_batch_handover_and_fresh_closure(rev_before, result, "sub.corr.a", "ev.corr.a")

        outcome = self._run("run-reattest-corrected")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        top = _top_section(model)
        self.assertNotEqual(top["resolved"]["disposition"], "blocked")
        self.assertEqual(float(top["resolved"]["value"]), 1340.0)

    def test_defect3_older_requested_version_is_refused_on_both_closure_routes(self) -> None:
        # Re-attest so the chain is on v2, then ask both closure routes for v1.
        close_f1099k_family_durably(
            self.log, self.registry, submission_id="sub.reattest.v2", evidence_id="ev.reattest.v2",
            actor=USER, at="2026-10-16T12:10:00Z", expected_revision=self.log.read().revision,
        )
        self.assertEqual(self._chain()[0], "v2")
        before = self.log.read()

        with self.assertRaises(F1099KRecordingRefused) as ctx:
            close_f1099k_family_durably(
                self.log, self.registry, submission_id="sub.close.v1", evidence_id="ev.close.v1",
                actor=USER, at="2026-10-16T12:20:00Z", expected_revision=before.revision,
                family_version="v1",
            )
        self.assertIn("cannot handover to older family version", str(ctx.exception))

        with self.assertRaises(F1099KRecordingRefused) as ctx:
            record_f1099k_statement_durably(
                self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
                box1a=880.0, box4=0.0, submission_id="sub.corr.v1", evidence_id="ev.corr.v1",
                actor=USER, at="2026-10-16T12:21:00Z", expected_revision=before.revision,
                corrected=True, close_family=True, family_version="v1",
            )
        self.assertIn("cannot handover to older family version", str(ctx.exception))

        after = self.log.read()
        self.assertEqual(after.revision, before.revision)
        self.assertEqual(after.acts, before.acts)

    def test_defect3_correction_without_close_family_attests_nothing(self) -> None:
        rev_before = self.log.read().revision
        record_f1099k_statement_durably(
            self.log, self.registry, payer_id=PAYER_A, statement_ref=STMT_A,
            box1a=880.0, box4=0.0, submission_id="sub.corr.nc", evidence_id="ev.corr.nc",
            actor=USER, at="2026-10-16T12:10:00Z", expected_revision=rev_before,
            corrected=True, close_family=False,
        )
        new_acts = self.log.read().acts[rev_before:]
        self.assertEqual([a for a in new_acts if a["kind"] == "family-handover"], [])
        self.assertEqual(self._chain()[0], "v1")
        # no fresh closure was invented: the only closure is the v1 one
        self.assertEqual(self._closure_finding_ids(), self.old_closure_fids)


class LocalResultVersusReturnEntryTests(unittest.TestCase):
    """Defect 4: a local supported loss is kept, but only a published top entry says 'entered'."""

    def setUp(self) -> None:
        self.registry = tax_registry()
        self.temp = TemporaryDirectory(prefix="multiple-statement-local-entry-")
        self.addCleanup(self.temp.cleanup)
        self.ws_dir = Path(self.temp.name)
        self.capability = WorkspaceCapability(self.ws_dir)
        self.log = ActLog(self.ws_dir, self.registry)
        _seed_workspace_v49(self.log)
        self.records = RecordStream(self.ws_dir / "records", DerivationSchemas())

    def _record(self, payer: str, ref: str, box1a: float, answers: dict[str, Any], tag: str, minute: int) -> dict[str, str]:
        res = record_f1099k_statement_durably(
            self.log, self.registry, payer_id=payer, statement_ref=ref,
            box1a=box1a, box4=0.0, submission_id=f"sub.stmt.{tag}", evidence_id=f"ev.stmt.{tag}",
            actor=USER, at=f"2026-10-16T12:{minute:02d}:00Z", expected_revision=self.log.read().revision,
            close_family=False,
        )
        record_f1099k_statement_answers_durably(
            self.log, self.registry, statement_keys=res["statement_keys"], answers=answers,
            submission_id=f"sub.ans.{tag}", evidence_ids={q: f"ev.{tag}.{q}" for q in answers},
            actor=USER, at=f"2026-10-16T12:{minute + 1:02d}:00Z", expected_revision=self.log.read().revision,
        )
        keys: dict[str, str] = res["statement_keys"]
        return keys

    def _close_and_run(self, run_id: str) -> tuple[Any, dict[str, Any]]:
        close_f1099k_family_durably(
            self.log, self.registry, submission_id=f"sub.close.{run_id}", actor=USER,
            at="2026-10-16T12:20:00Z", expected_revision=self.log.read().revision,
        )
        contents = self.log.read()
        outcome = live_coordinate_run(
            self.capability, repo_root=ROOT, authoritative_acts=contents.acts,
            workspace_revision=contents.revision, run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=SURFACE_V47, output_name=f"{run_id}.json",
        )
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        return outcome, json.loads(outcome.presentation_path.read_text("utf-8"))

    def _current_b1a_values(self) -> dict[tuple[tuple[str, str], ...], float]:
        state = project(tuple(copy.deepcopy(row) for row in self.log.read().acts), self.registry)
        current = compute_currency(state).current_finding_ids
        lattice = facts_of(state.fact_state)
        return {
            tuple(sorted(lattice[f["fact_id"]].keys)): f["value"]
            for fid, f in state.findings.items()
            if fid in current and f.get("fact_id") in lattice
            and lattice[f["fact_id"]].fact_type_id == STATEMENT_BOX1A
        }

    def test_defect4_supported_loss_beside_blocking_sibling_keeps_result_without_entered_wording(self) -> None:
        keys_a = self._record(PAYER_A, STMT_A, 880.0, SUPPORTED_ANSWERS_A, "a", 1)
        unknown_cost = {**SUPPORTED_ANSWERS_B, "cost-basis-known": "cannot-tell", "purchase-cost": "cannot-tell"}
        keys_b = self._record(PAYER_B, STMT_B, 460.0, unknown_cost, "b", 3)
        outcome, model = self._close_and_run("run-local-vs-entry")

        # both statements are current with their exact full keys and own amounts
        self.assertEqual(
            self._current_b1a_values(),
            {tuple(sorted(keys_a.items())): 880.0, tuple(sorted(keys_b.items())): 460.0},
        )
        # the published top-entry disposition is blocked and publishes no value
        top = _top_section(model)["resolved"]
        self.assertEqual(top["disposition"], "blocked")
        self.assertNotIn("value", top)

        # the saved explanations keep each statement's local reason
        expl = {
            tuple(sorted(v["statementKeys"].items())): v
            for v in model["f1099kStatementExplanation"].values()
        }
        self.assertEqual(expl[tuple(sorted(keys_a.items()))]["reason"], "supported-loss")
        self.assertEqual(expl[tuple(sorted(keys_b.items()))]["reason"], "cost-basis-unknown")

        # the reloaded review keeps the supported loss but does not say it was entered
        rev_a = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.local.a", shown_at="2026-10-16T12:30:00Z", statement_keys=keys_a,
        )
        self.assertEqual(rev_a["savedCalculationState"], "current-supported-loss")
        saved = rev_a["savedCalculation"]
        self.assertEqual(saved["status"], "supported-loss")
        self.assertEqual(saved["reason"], "supported-loss")
        self.assertEqual(saved["box1a"], 880.0)
        self.assertEqual(saved["topEntryDisposition"], "blocked")
        self.assertNotIn("entered", saved["sentence"].lower())
        self.assertIn("has not been added", saved["sentence"])
        self.assertEqual(rev_a["statement"]["keys"], keys_a)

        rev_b = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.local.b", shown_at="2026-10-16T12:31:00Z", statement_keys=keys_b,
        )
        self.assertEqual(rev_b["savedCalculationState"], "current-unresolved-explanation")
        self.assertIsNone(rev_b["savedCalculation"])

    def test_defect4_published_top_entry_still_says_entered(self) -> None:
        keys_a = self._record(PAYER_A, STMT_A, 880.0, SUPPORTED_ANSWERS_A, "a", 1)
        keys_b = self._record(PAYER_B, STMT_B, 460.0, SUPPORTED_ANSWERS_B, "b", 3)
        outcome, model = self._close_and_run("run-local-and-entry")

        self.assertEqual(
            self._current_b1a_values(),
            {tuple(sorted(keys_a.items())): 880.0, tuple(sorted(keys_b.items())): 460.0},
        )
        top = _top_section(model)["resolved"]
        self.assertEqual(top["disposition"], "published_value")
        self.assertEqual(float(top["value"]), 1340.0)

        rev_a = review_f1099k_statement_with_saved_presentation(
            self.log, self.registry, outcome.presentation_path, self.records,
            review_id="rev.entry.a", shown_at="2026-10-16T12:30:00Z", statement_keys=keys_a,
        )
        saved = rev_a["savedCalculation"]
        self.assertEqual(saved["box1a"], 880.0)
        self.assertEqual(saved["topEntryDisposition"], "published_value")
        self.assertIn("entered at the top of Schedule 1", saved["sentence"])
