"""ADR 0077 Part 5: the new-write step in ``ActLog.append`` and its registry condition.

Every case drives the real recorder and a real ``ActLog`` over a registry that
carries the Part 5 declaration, then reads the log back through a fresh
``ActLog``. A *bypassing writer* is a test-only ``ActLog`` over a registry with
no declaration; it stands for a log written before the step existed. Replay of
such a log (cases 19-21) is the second half of Track 1e and is not tested here.
"""
from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

from packages.derivation.loader import DerivationSchemas, workspace_registry
from packages.kernel import act_log as act_log_module
from packages.kernel.act_log import ActLog, ActLogError
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import (
    FindingModelError,
    declares_new_write_invariants,
    enforce_new_write_invariants,
    project,
)
from packages.kernel.schema_registry import SchemaRegistry
from packages.tax.loader import (
    domain_scoped_supersession_declarations,
    install_domain_companion_presence,
    install_domain_scoped_supersession,
    tax_registry,
)
from packages.tax.sli_relationship_recording import (
    SCHOOLING,
    RelationshipRecordingRefused,
    current_claim_applicability,
    introduce_borrowing_reference_durably,
    record_submission_durably,
    withdraw_relationship_claim_durably,
)
from packages.tax.sli_relationship_review import (
    _append_statement_source_correction_durably,
    apply_statement_correction_review,
    prepare_review,
)
import tests.test_sli_correction_entry_enforcement as track6
import tests.test_sli_relationship_recording as track14

ROOT = Path(__file__).resolve().parents[1]
USER = "demo.user.filer"
SOURCE_TYPE = "tax.us.2025.f1098e.box1-student-loan-interest"
DEPENDENT_TYPE = "tax.us.2025.sli.statement-inclusion-relationship"


def _bypass(log: ActLog) -> ActLog:
    """A test-only writer over a registry without the declaration (case 20's bare registry)."""
    return ActLog(log.path.parent, DerivationSchemas().registry, undeclared_test_log=True)


def _fresh_acts(log: ActLog, registry: Any) -> tuple[dict[str, Any], ...]:
    return ActLog(log.path.parent, registry).read().acts


def _box1(acts: tuple[dict[str, Any], ...], registry: Any, statement: str) -> list[tuple[str, Any]]:
    state = project(acts, registry)
    current = compute_currency(state).current_finding_ids
    return [(fid, row["value"]) for fid, row in state.findings.items()
            if fid in current and row.get("fact_id") == statement]


def _box1_history(acts: tuple[dict[str, Any], ...], registry: Any, statement: str) -> list[Any]:
    return [row["value"] for row in project(acts, registry).findings.values()
            if row.get("fact_id") == statement]


def _applicability(acts: tuple[dict[str, Any], ...], registry: Any, finding_id: str) -> str:
    rows = {row["finding_id"]: row for row in current_claim_applicability(acts, registry)}
    return rows[finding_id]["applicability"]


def _statement_keys(log: ActLog, registry: Any, statement: str) -> tuple[tuple[str, str], ...]:
    return tuple(facts_of(project(log.read().acts, registry).fact_state)[statement].keys)


def _retract(log: ActLog, finding_id: str, label: str) -> None:
    revision = log.read().revision
    log.append({"schema": "act.v1", "act_id": f"demo.part5.retract.{label}",
                "kind": "finding-retracted", "actor": USER, "at": "2026-10-02T13:00:00Z",
                "committed_against": revision, "payload": {"finding_id": finding_id}},
               expected_revision=revision)


def _assertion_acts(log: ActLog) -> set[str]:
    return {item["payload"]["finding"]["id"] for item in log.read().acts if item["kind"] == "assertion"}


class RegistryCondition(unittest.TestCase):
    """The acceptance condition: no production ActLog over a registry without the declaration."""

    def test_bare_kernel_registry_construction_fails_loudly(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaisesRegex(ActLogError, "new-write declaration"):
                ActLog(Path(raw), SchemaRegistry())

    def test_derivation_and_workspace_registries_without_install_fail_loudly(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            for registry in (DerivationSchemas().registry, workspace_registry()):
                with self.assertRaisesRegex(ActLogError, "new-write declaration"):
                    ActLog(Path(raw), registry)

    def test_tax_registry_and_live_install_carry_the_declaration(self) -> None:
        expected = domain_scoped_supersession_declarations()
        self.assertEqual(len(expected), 1)
        self.assertEqual(expected[0]["source_fact_type"], SOURCE_TYPE)
        self.assertEqual(expected[0]["dependent_fact_type"], DEPENDENT_TYPE)
        self.assertEqual(expected[0]["dependent_keys_not_identifying_source"], ["borrowing"])
        self.assertEqual(expected[0]["reviewed_scope"]["binds"],
                         ["reviewed_statement_finding_id", "corrected_box1_total", "source_correction_id"])
        reg = tax_registry()
        self.assertEqual(reg.scoped_supersession_declarations, expected)  # type: ignore[attr-defined]
        live = install_domain_companion_presence(DerivationSchemas().registry)
        self.assertEqual(live.scoped_supersession_declarations, expected)  # type: ignore[attr-defined]
        install_domain_companion_presence(live)
        self.assertEqual(live.scoped_supersession_declarations, expected)  # type: ignore[attr-defined]
        with tempfile.TemporaryDirectory() as raw:
            ActLog(Path(raw), reg)
            ActLog(Path(raw), live)

    def test_entry_loop_log_carries_the_declaration(self) -> None:
        from packages.derivation.entry_loop import SyntheticW2EntryRuntime
        from packages.derivation.live_workspace import WorkspaceCapability
        with tempfile.TemporaryDirectory() as raw:
            runtime = SyntheticW2EntryRuntime(WorkspaceCapability(Path(raw) / "L"), repo_root=ROOT)
            self.assertEqual(runtime._log.registry.scoped_supersession_declarations,  # type: ignore[attr-defined]
                             domain_scoped_supersession_declarations())

    def test_malformed_declaration_fails_loudly(self) -> None:
        registry = DerivationSchemas().registry
        registry.scoped_supersession_declarations = [  # type: ignore[attr-defined]
            {"source_fact_type": SOURCE_TYPE, "dependent_fact_type": DEPENDENT_TYPE}]
        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaisesRegex(ActLogError, "new-write declaration"):
                ActLog(Path(raw), registry)
        registry.scoped_supersession_declarations = []  # type: ignore[attr-defined]
        self.assertFalse(declares_new_write_invariants(registry))

    def test_declaration_removed_after_construction_refuses_append(self) -> None:
        raw, log, registry, refs = track14.OrdinaryRelationshipRecording()._workspace()
        with raw:
            saved = registry.scoped_supersession_declarations
            registry.scoped_supersession_declarations = []
            try:
                keys = _statement_keys(log, registry, refs["statement"])
                revision = log.read().revision
                with self.assertRaisesRegex(ActLogError, "new-write declaration"):
                    track14._append_source(log, registry, SOURCE_TYPE, keys, 1410.0, "part5-removed")
                self.assertEqual(log.read().revision, revision)
            finally:
                registry.scoped_supersession_declarations = saved

    def test_read_only_log_reads_and_never_writes(self) -> None:
        raw, log, registry, _refs = track14.OrdinaryRelationshipRecording()._workspace()
        with raw:
            reader = ActLog(log.path.parent, DerivationSchemas().registry, read_only=True)
            self.assertEqual(reader.read().revision, log.read().revision)
            with self.assertRaisesRegex(ActLogError, "read-only"):
                reader.append(log.read().acts[0], expected_revision=log.read().revision)

    def test_test_only_opt_out_is_explicit_and_unused_in_packages(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            ActLog(Path(raw), SchemaRegistry(), undeclared_test_log=True)
        offenders: list[str] = []
        for path in sorted((ROOT / "packages").rglob("*.py")):
            tree = ast.parse(path.read_text("utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and getattr(node.func, "id", getattr(node.func, "attr", None)) == "ActLog":
                    if any(kw.arg == "undeclared_test_log" for kw in node.keywords):
                        offenders.append(f"{path.relative_to(ROOT)}:{node.lineno}")
        self.assertEqual(offenders, [])

    def test_production_constructions_are_declared_or_read_only(self) -> None:
        sites: list[str] = []
        for path in sorted((ROOT / "packages").rglob("*.py")):
            tree = ast.parse(path.read_text("utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "ActLog":
                    read_only = any(kw.arg == "read_only" for kw in node.keywords)
                    sites.append(f"{path.relative_to(ROOT)}:{'read-only' if read_only else 'write'}")
        self.assertEqual(sorted(sites), [
            "packages/derivation/entry_loop.py:write",
            "packages/kernel/runners/inspect_workspace.py:read-only",
        ])


class NewWriteStepBoundary(unittest.TestCase):
    """Where the step runs, and where it never runs."""

    def test_project_and_read_never_run_the_step_and_append_does(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            with mock.patch.object(act_log_module, "enforce_new_write_invariants",
                                   wraps=enforce_new_write_invariants) as step:
                acts = ActLog(log.path.parent, registry).read().acts
                project(acts, registry)
                current_claim_applicability(acts, registry)
                self.assertEqual(step.call_count, 0)
                keys = _statement_keys(log, registry, refs["statement"])
                with self.assertRaises(FindingModelError):
                    track14._append_source(log, registry, SOURCE_TYPE, keys, 1800.0, "part5-boundary")
                self.assertEqual(step.call_count, 1)

    def test_member_transition_assert_is_checked(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            state = project(log.read().acts, registry)
            finding = {"schema": "finding.v2", "id": "demo.finding.part5.member", "fact_id": refs["statement"],
                       "value": 1800.0, "basis": "attested", "evidence_ids": []}
            for action in ("assert", "reclassify"):
                item = {"schema": "act.v1", "act_id": f"demo.part5.member.{action}", "kind": "member-transition",
                        "actor": USER, "at": "2026-10-02T13:00:00Z", "committed_against": 0,
                        "payload": {"member": {"action": action, "finding": finding}}}
                with self.assertRaisesRegex(FindingModelError, "scoped supersession violated"):
                    enforce_new_write_invariants(state, item, registry)
            remove = {"schema": "act.v1", "act_id": "demo.part5.member.remove", "kind": "member-transition",
                      "actor": USER, "at": "2026-10-02T13:00:00Z", "committed_against": 0,
                      "payload": {"member": {"action": "remove", "fact_id": refs["statement"]}}}
            enforce_new_write_invariants(state, remove, registry)

    def test_refusal_message_names_each_dependent_in_fact_id_order(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            second = "demo.part5.borrowing.winter"
            introduce_borrowing_reference_durably(log, registry, reference_id=second,
                                                  description="Winter borrowing", actor=USER,
                                                  at="2026-10-02T12:01:00Z")
            other = record_submission_durably(log, {
                "submission_id": "demo.part5.submission.second", "evidence_id": "demo.evidence.part5.second",
                "actor": USER, "at": "2026-10-02T12:01:30Z", "borrowing_ref": second,
                "schooling_fact_id": refs["school"], "statement_fact_id": refs["statement"],
                "financing_response": "unanswered", "inclusion_response": "yes",
            }, registry)
            dependents = sorted([refs["inclusion_fact_id"], other["claims"]["statement-inclusion"]["fact_id"]])
            keys = _statement_keys(log, registry, refs["statement"])
            with self.assertRaises(FindingModelError) as caught:
                track14._append_source(log, registry, SOURCE_TYPE, keys, 1800.0, "part5-two")
            clauses = "; ".join(f"while {dep} is current and names that source" for dep in dependents)
            self.assertEqual(
                str(caught.exception),
                f"scoped supersession violated: new finding demo.finding.track14.part5-two of "
                f"{refs['statement']} {clauses}; the new finding is not the one successor bound by "
                f"reviewed-scope evidence for that source; rejected, not recorded",
            )


class Part5Cases(unittest.TestCase):
    """ADR 0077 Part 5, "The implementation track executes these cases", items 1-18 and 20."""

    def test_case_1_reviewed_amount_only_is_admitted_through_the_step(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            with mock.patch.object(act_log_module, "enforce_new_write_invariants",
                                   wraps=enforce_new_write_invariants) as step:
                track6._reviewed_correction(log, registry, refs, scope="amount-only", amount=1775.0,
                                            correction_id="demo.part5.case1", borrowing_ref=None,
                                            finding_id=None, suffix="part5-case1")
                self.assertGreater(step.call_count, 0)
            acts = _fresh_acts(log, registry)
            self.assertEqual([value for _fid, value in _box1(acts, registry, refs["statement"])], [1775.0])
            self.assertEqual(set(_box1_history(acts, registry, refs["statement"])), {1250.0, 1775.0})
            self.assertEqual(_applicability(acts, registry, refs["inclusion_finding_id"]), "current")

    def test_case_2_reviewed_removal_answers_first_then_admits_the_source(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            track6._reviewed_correction(log, registry, refs, scope="inclusion-removed", amount=1660.0,
                                        correction_id="demo.part5.case2", borrowing_ref=refs["borrowing"],
                                        finding_id=refs["inclusion_finding_id"], suffix="part5-case2")
            acts = _fresh_acts(log, registry)
            state = project(acts, registry)
            self.assertEqual([value for _fid, value in _box1(acts, registry, refs["statement"])], [1660.0])
            self.assertNotIn(refs["inclusion_finding_id"], compute_currency(state).current_finding_ids)
            self.assertEqual(state.evidence["demo.evidence.track6.inclusion"].evidence["content"]
                             ["responses"]["inclusion_response"], "yes")

    def test_case_3_direct_append_is_refused_and_not_recorded(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            before = _box1(log.read().acts, registry, refs["statement"])
            keys = _statement_keys(log, registry, refs["statement"])
            with self.assertRaisesRegex(FindingModelError, "rejected, not recorded"):
                track14._append_source(log, registry, SOURCE_TYPE, keys, 1800.0, "part5-case3")
            acts = _fresh_acts(log, registry)
            self.assertNotIn("demo.finding.track14.part5-case3", _assertion_acts(log))
            self.assertEqual(_box1(acts, registry, refs["statement"]), before)
            self.assertNotIn(1800.0, _box1_history(acts, registry, refs["statement"]))
            self.assertEqual(_applicability(acts, registry, refs["inclusion_finding_id"]), "current")

    def test_case_4_no_claims_writes_an_identical_log_with_and_without_the_step(self) -> None:
        logs: list[bytes] = []
        for declared in (True, False):
            raw, log, registry, refs = track14.OrdinaryRelationshipRecording()._workspace()
            with raw:
                writer = log if declared else _bypass(log)
                self.assertEqual(declares_new_write_invariants(registry), True)
                keys = _statement_keys(log, registry, refs["statement"])
                track14._append_source(writer, registry, SOURCE_TYPE, keys, 1410.0, "part5-case4")
                acts = _fresh_acts(log, registry)
                self.assertEqual([value for _fid, value in _box1(acts, registry, refs["statement"])], [1410.0])
                logs.append(log.path.read_bytes())
        self.assertEqual(logs[0], logs[1])

    def test_case_5_touched_append_refused_beside_an_unrelated_inclusion(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            other_fact = track6._append_other_statement(log, registry)
            other = record_submission_durably(log, {
                "submission_id": "demo.part5.submission.other", "evidence_id": "demo.evidence.part5.other",
                "actor": USER, "at": "2026-10-02T12:02:00Z", "borrowing_ref": refs["borrowing"],
                "schooling_fact_id": refs["school"], "statement_fact_id": other_fact,
                "financing_response": "unanswered", "inclusion_response": "yes",
            }, registry)
            other_id = other["claims"]["statement-inclusion"]["finding_id"]
            other_before = _box1(log.read().acts, registry, other_fact)
            keys = _statement_keys(log, registry, refs["statement"])
            with self.assertRaises(FindingModelError):
                track14._append_source(log, registry, SOURCE_TYPE, keys, 1800.0, "part5-case5")
            acts = _fresh_acts(log, registry)
            self.assertEqual(_applicability(acts, registry, refs["inclusion_finding_id"]), "current")
            self.assertEqual(_applicability(acts, registry, other_id), "current")
            self.assertEqual(_box1(acts, registry, other_fact), other_before)

    def test_case_7_reviewed_correction_after_a_refused_direct_append(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            keys = _statement_keys(log, registry, refs["statement"])
            with self.assertRaises(FindingModelError):
                track14._append_source(log, registry, SOURCE_TYPE, keys, 1800.0, "part5-case7")
            track6._reviewed_correction(log, registry, refs, scope="amount-only", amount=1900.0,
                                        correction_id="demo.part5.case7", borrowing_ref=None,
                                        finding_id=None, suffix="part5-case7")
            acts = _fresh_acts(log, registry)
            self.assertEqual(set(_box1_history(acts, registry, refs["statement"])), {1250.0, 1900.0})
            self.assertEqual(_applicability(acts, registry, refs["inclusion_finding_id"]), "current")

    def test_case_8_first_box1_of_a_fact_id_is_admitted_while_another_inclusion_is_current(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            other_fact = track6._append_other_statement(log, registry)
            acts = _fresh_acts(log, registry)
            self.assertEqual([value for _fid, value in _box1(acts, registry, other_fact)], [900.0])
            self.assertEqual(_applicability(acts, registry, refs["inclusion_finding_id"]), "current")

    def test_case_8_first_box1_is_refused_when_a_current_dependent_already_names_it(self) -> None:
        """No prior finding is not an exemption: the dependent decides, after a retraction too."""
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            original = _box1(log.read().acts, registry, refs["statement"])[0][0]
            _retract(log, original, "case8")
            self.assertEqual(_box1(log.read().acts, registry, refs["statement"]), [])
            keys = _statement_keys(log, registry, refs["statement"])
            with self.assertRaises(FindingModelError):
                track14._append_source(log, registry, SOURCE_TYPE, keys, 1500.0, "part5-case8-after")

    def test_case_9_retraction_of_box1_is_admitted(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            original = _box1(log.read().acts, registry, refs["statement"])[0][0]
            revision = log.read().revision
            _retract(log, original, "case9")
            self.assertEqual(log.read().revision, revision + 1)
            acts = _fresh_acts(log, registry)
            self.assertEqual(_box1(acts, registry, refs["statement"]), [])
            self.assertIn(original, project(acts, registry).retracted_finding_ids)

    def test_case_10_unrelated_fact_type_corrections_are_admitted(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            school_keys = tuple(facts_of(project(log.read().acts, registry).fact_state)[refs["school"]].keys)
            track14._append_source(log, registry, SCHOOLING, school_keys,
                                   "Riverside College, BSc, autumn 2024 (corrected)", "part5-case10-school")
            financing = record_submission_durably(log, {
                "submission_id": "demo.part5.submission.financing",
                "evidence_id": "demo.evidence.part5.financing",
                "actor": USER, "at": "2026-10-02T12:03:00Z", "borrowing_ref": refs["borrowing"],
                "schooling_fact_id": refs["school"], "statement_fact_id": refs["statement"],
                "financing_response": "yes", "inclusion_response": "unanswered",
            }, registry)
            acts = _fresh_acts(log, registry)
            state = project(acts, registry)
            current = compute_currency(state).current_finding_ids
            self.assertIn("demo.finding.track14.part5-case10-school", current)
            self.assertIn(financing["claims"]["financing"]["finding_id"], current)
            self.assertEqual(_applicability(acts, registry, refs["inclusion_finding_id"]), "current")

    def test_case_11_withdrawal_then_same_identity_append_is_admitted(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            withdraw_relationship_claim_durably(log, registry, finding_id=refs["inclusion_finding_id"],
                                                actor=USER, at="2026-10-02T12:04:00Z")
            keys = _statement_keys(log, registry, refs["statement"])
            track14._append_source(log, registry, SOURCE_TYPE, keys, 1800.0, "part5-case11")
            acts = _fresh_acts(log, registry)
            self.assertEqual([value for _fid, value in _box1(acts, registry, refs["statement"])], [1800.0])

    def test_case_12_scope_evidence_for_a_different_statement_is_refused(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            other_fact = track6._append_other_statement(log, registry)
            original = _box1(log.read().acts, registry, refs["statement"])[0][0]
            scope_id = "demo.evidence.part5.case12-scope"
            track6._submit_scope_evidence(log, evidence_id=scope_id, statement_fact_id=other_fact,
                                          reviewed_statement_finding_id=original, corrected_total=1888.0,
                                          correction_id="demo.part5.case12")
            with self.assertRaisesRegex(FindingModelError, "scoped supersession violated"):
                track6._smuggle_box1_citing_scope(log, registry, statement_fact_id=refs["statement"],
                                                  value=1888.0, label="part5-case12",
                                                  scope_evidence_id=scope_id,
                                                  source_correction_id="demo.part5.case12")
            self.assertNotIn("demo.finding.track1a3.part5-case12", _assertion_acts(log))

    def test_case_13_retract_then_assert_is_refused_without_the_bound_successor(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            original = _box1(log.read().acts, registry, refs["statement"])[0][0]
            scope_id = "demo.evidence.part5.case13-scope"
            track6._submit_scope_evidence(log, evidence_id=scope_id, statement_fact_id=refs["statement"],
                                          reviewed_statement_finding_id=original, corrected_total=1500.0,
                                          correction_id="demo.part5.case13")
            _retract(log, original, "case13")
            keys = _statement_keys(log, registry, refs["statement"])
            with self.assertRaises(FindingModelError):
                track14._append_source(log, registry, SOURCE_TYPE, keys, 1500.0, "part5-case13-direct")
            # Even a finding that cites scope evidence for ``original`` is refused: the
            # binding requires its predecessor to be the one current box 1 finding, and
            # after the retraction there is none. The way back is the next test.
            with self.assertRaises(FindingModelError):
                track6._smuggle_box1_citing_scope(log, registry, statement_fact_id=refs["statement"],
                                                  value=1500.0, label="part5-case13-bound",
                                                  scope_evidence_id=scope_id,
                                                  source_correction_id="demo.part5.case13")
            acts = _fresh_acts(log, registry)
            self.assertEqual(_box1(acts, registry, refs["statement"]), [])
            self.assertNotIn(1500.0, _box1_history(acts, registry, refs["statement"]))

    def test_case_13_way_back_withdraw_enter_box1_then_confirm_again(self) -> None:
        """After a retraction: withdraw the inclusion, enter box 1, confirm the inclusion again."""
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            original = _box1(log.read().acts, registry, refs["statement"])[0][0]
            _retract(log, original, "case13-way-back")
            keys = _statement_keys(log, registry, refs["statement"])
            with self.assertRaises(FindingModelError):
                track14._append_source(log, registry, SOURCE_TYPE, keys, 1500.0, "part5-case13-early")
            withdraw_relationship_claim_durably(log, registry, finding_id=refs["inclusion_finding_id"],
                                                actor=USER, at="2026-10-02T13:01:00Z")
            track14._append_source(log, registry, SOURCE_TYPE, keys, 1500.0, "part5-case13-reentered")
            again = record_submission_durably(log, {
                "submission_id": "demo.part5.submission.case13-again",
                "evidence_id": "demo.evidence.part5.case13-again",
                "actor": USER, "at": "2026-10-02T13:02:00Z", "borrowing_ref": refs["borrowing"],
                "schooling_fact_id": refs["school"], "statement_fact_id": refs["statement"],
                "financing_response": "unanswered", "inclusion_response": "yes",
            }, registry)
            reconfirmed = again["claims"]["statement-inclusion"]
            acts = _fresh_acts(log, registry)
            state = project(acts, registry)
            current = compute_currency(state).current_finding_ids
            self.assertEqual(_box1(acts, registry, refs["statement"]),
                             [("demo.finding.track14.part5-case13-reentered", 1500.0)])
            self.assertEqual(reconfirmed["fact_id"], refs["inclusion_fact_id"])
            self.assertNotEqual(reconfirmed["finding_id"], refs["inclusion_finding_id"])
            self.assertIn(reconfirmed["finding_id"], current)
            self.assertNotIn(refs["inclusion_finding_id"], current)
            self.assertIn(refs["inclusion_finding_id"], state.findings)
            self.assertEqual(_applicability(acts, registry, reconfirmed["finding_id"]), "current")

    def test_bound_successor_written_without_the_recorder_is_admitted(self) -> None:
        """The step admits the one bound successor whoever writes it; the binding decides."""
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            original = _box1(log.read().acts, registry, refs["statement"])[0][0]
            scope_id = "demo.evidence.part5.direct-bound-scope"
            track6._submit_scope_evidence(log, evidence_id=scope_id, statement_fact_id=refs["statement"],
                                          reviewed_statement_finding_id=original, corrected_total=1888.0,
                                          correction_id="demo.part5.direct-bound")
            track6._smuggle_box1_citing_scope(log, registry, statement_fact_id=refs["statement"],
                                              value=1888.0, label="part5-direct-bound",
                                              scope_evidence_id=scope_id,
                                              source_correction_id="demo.part5.direct-bound")
            acts = _fresh_acts(log, registry)
            self.assertEqual([value for _fid, value in _box1(acts, registry, refs["statement"])], [1888.0])
            self.assertEqual(_applicability(acts, registry, refs["inclusion_finding_id"]), "current")
            # A boolean amount, a wrong correction id, or a missing binding field each fails closed.
            for label, total, correction, value in (
                ("bool", True, "demo.part5.bool", 1.0),
                ("wrong-id", 1999.0, "demo.part5.wrong-id", 1999.0),
            ):
                current = _box1(log.read().acts, registry, refs["statement"])[0][0]
                bad_scope = f"demo.evidence.part5.{label}-scope"
                track6._submit_scope_evidence(log, evidence_id=bad_scope, statement_fact_id=refs["statement"],
                                              reviewed_statement_finding_id=current, corrected_total=total,
                                              correction_id=correction)
                with self.assertRaises(FindingModelError):
                    track6._smuggle_box1_citing_scope(
                        log, registry, statement_fact_id=refs["statement"], value=value,
                        label=f"part5-{label}", scope_evidence_id=bad_scope,
                        source_correction_id=correction if label != "wrong-id" else "demo.part5.other-id")

    def test_case_14_reuse_after_reviewed_1775_is_refused_by_recorder_and_step(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            scope_id = "demo.evidence.track6.part5-case14"
            track6._reviewed_correction(log, registry, refs, scope="amount-only", amount=1775.0,
                                        correction_id="demo.part5.case14", borrowing_ref=None,
                                        finding_id=None, suffix="part5-case14")
            revision = log.read().revision
            with self.assertRaises(RelationshipRecordingRefused):
                _append_statement_source_correction_durably(
                    log, registry, statement_fact_id=refs["statement"], corrected_total=2900.0,
                    correction_id="demo.part5.case14-2900", scope_evidence_id=scope_id,
                    actor=USER, at="2026-10-02T12:06:00Z")
            self.assertEqual(log.read().revision, revision)
            with self.assertRaisesRegex(FindingModelError, "scoped supersession violated"):
                track6._smuggle_box1_citing_scope(log, registry, statement_fact_id=refs["statement"],
                                                  value=2900.0, label="part5-case14-smuggle",
                                                  scope_evidence_id=scope_id,
                                                  source_correction_id="demo.part5.case14-2900")
            kinds = [item["kind"] for item in log.read().acts[revision:]]
            self.assertEqual(kinds, ["evidence-submitted", "contribution"])
            acts = _fresh_acts(log, registry)
            self.assertEqual([value for _fid, value in _box1(acts, registry, refs["statement"])], [1775.0])
            self.assertEqual(_applicability(acts, registry, refs["inclusion_finding_id"]), "current")

    def test_case_15_same_amount_reuse_is_refused_by_recorder_and_step(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            scope_id = "demo.evidence.track6.part5-case15"
            track6._reviewed_correction(log, registry, refs, scope="amount-only", amount=1775.0,
                                        correction_id="demo.part5.case15", borrowing_ref=None,
                                        finding_id=None, suffix="part5-case15")
            with self.assertRaises(RelationshipRecordingRefused):
                _append_statement_source_correction_durably(
                    log, registry, statement_fact_id=refs["statement"], corrected_total=1775.0,
                    correction_id="demo.part5.case15-again", scope_evidence_id=scope_id,
                    actor=USER, at="2026-10-02T12:06:00Z")
            with self.assertRaises(FindingModelError):
                track6._smuggle_box1_citing_scope(log, registry, statement_fact_id=refs["statement"],
                                                  value=1775.0, label="part5-case15-smuggle",
                                                  scope_evidence_id=scope_id,
                                                  source_correction_id="demo.part5.case15")
            acts = _fresh_acts(log, registry)
            self.assertEqual(len(_box1(acts, registry, refs["statement"])), 1)
            self.assertEqual(_applicability(acts, registry, refs["inclusion_finding_id"]), "current")

    def test_case_16_review_against_a_changed_box1_is_refused_by_recorder_and_step(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            original = _box1(log.read().acts, registry, refs["statement"])[0][0]
            review = prepare_review(
                log, registry, review_id="demo.part5.review.case16", shown_at="2026-10-02T12:05:00Z",
                borrowing_refs=(refs["borrowing"],), schooling_fact_ids=(refs["school"],),
                statement_fact_ids=(refs["statement"],))
            keys = _statement_keys(log, registry, refs["statement"])
            with self.assertRaises(FindingModelError):
                track14._append_source(log, registry, SOURCE_TYPE, keys, 1640.0, "part5-case16-step")
            # Only a bypassing writer can change box 1 under a current inclusion.
            track14._append_source(_bypass(log), registry, SOURCE_TYPE, keys, 1640.0, "part5-case16")
            revision = log.read().revision
            with self.assertRaises(RelationshipRecordingRefused):
                apply_statement_correction_review(
                    log, registry, review=review, statement_fact_id=refs["statement"], scope="amount-only",
                    borrowing_ref=None, finding_id=None, corrected_box1_total=1775.0,
                    source_correction_id="demo.part5.case16", actor=USER, at="2026-10-02T12:05:01Z",
                    submission_id="demo.part5.submission.case16", evidence_id="demo.evidence.part5.case16")
            self.assertEqual(log.read().revision, revision)
            scope_id = "demo.evidence.part5.case16-scope"
            track6._submit_scope_evidence(log, evidence_id=scope_id, statement_fact_id=refs["statement"],
                                          reviewed_statement_finding_id=original, corrected_total=1775.0,
                                          correction_id="demo.part5.case16")
            with self.assertRaises(FindingModelError):
                track6._smuggle_box1_citing_scope(log, registry, statement_fact_id=refs["statement"],
                                                  value=1775.0, label="part5-case16-successor",
                                                  scope_evidence_id=scope_id,
                                                  source_correction_id="demo.part5.case16")
            acts = _fresh_acts(log, registry)
            self.assertEqual([value for _fid, value in _box1(acts, registry, refs["statement"])], [1640.0])

    def test_case_17_reviewed_id_not_the_predecessor_is_refused_by_the_step(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            scope_id = "demo.evidence.part5.case17-scope"
            track6._submit_scope_evidence(log, evidence_id=scope_id, statement_fact_id=refs["statement"],
                                          reviewed_statement_finding_id="demo.finding.not-the-reviewed-box1",
                                          corrected_total=1888.0, correction_id="demo.part5.case17")
            with self.assertRaises(FindingModelError):
                track6._smuggle_box1_citing_scope(log, registry, statement_fact_id=refs["statement"],
                                                  value=1888.0, label="part5-case17",
                                                  scope_evidence_id=scope_id,
                                                  source_correction_id="demo.part5.case17")
            self.assertEqual(_applicability(_fresh_acts(log, registry), registry,
                                            refs["inclusion_finding_id"]), "current")

    def test_case_18_wrong_kind_is_refused_by_recorder_and_step(self) -> None:
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            original = _box1(log.read().acts, registry, refs["statement"])[0][0]
            scope_id = "demo.evidence.part5.case18-scope"
            track6._submit_scope_evidence(log, evidence_id=scope_id, statement_fact_id=refs["statement"],
                                          reviewed_statement_finding_id=original, corrected_total=1888.0,
                                          correction_id="demo.part5.case18", kind="tax.other-answer")
            with self.assertRaises(RelationshipRecordingRefused):
                _append_statement_source_correction_durably(
                    log, registry, statement_fact_id=refs["statement"], corrected_total=1888.0,
                    correction_id="demo.part5.case18", scope_evidence_id=scope_id,
                    actor=USER, at="2026-10-02T12:06:00Z")
            with self.assertRaises(FindingModelError):
                track6._smuggle_box1_citing_scope(log, registry, statement_fact_id=refs["statement"],
                                                  value=1888.0, label="part5-case18",
                                                  scope_evidence_id=scope_id,
                                                  source_correction_id="demo.part5.case18")

    def test_case_20_bypassing_writers_persist_the_write(self) -> None:
        """A raw line and a test-only bare-registry log both put the write in the log."""
        raw, log, registry, refs = track6._affirmed_inclusion()
        with raw:
            keys = _statement_keys(log, registry, refs["statement"])
            track14._append_source(_bypass(log), registry, SOURCE_TYPE, keys, 1800.0, "part5-case20")
            acts = _fresh_acts(log, registry)
            self.assertEqual([value for _fid, value in _box1(acts, registry, refs["statement"])], [1800.0])
            self.assertEqual(_applicability(acts, registry, refs["inclusion_finding_id"]),
                             "unresolved-applicability")


class DeclarationInstall(unittest.TestCase):
    def test_install_is_idempotent_and_a_fresh_copy(self) -> None:
        registry = DerivationSchemas().registry
        install_domain_scoped_supersession(registry)
        install_domain_scoped_supersession(registry)
        declared = registry.scoped_supersession_declarations  # type: ignore[attr-defined]
        self.assertEqual(declared, domain_scoped_supersession_declarations())
        declared[0]["source_fact_type"] = "demo.mutated"
        self.assertEqual(domain_scoped_supersession_declarations()[0]["source_fact_type"], SOURCE_TYPE)


if __name__ == "__main__":
    unittest.main()
