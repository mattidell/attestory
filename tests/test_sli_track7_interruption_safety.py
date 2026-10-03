"""Track 7: relationship saves that write several records survive interruption.

Plan sentence 6. Every relationship writer that appends more than one act is
interrupted after each of its acts, once with a torn last line and once with a
clean stop. The log is then recovered fresh and the whole return is run
through ``live_coordinate_run`` on both runners. The recovered line 21 and
per-statement standing are never more favorable than before the save, and the
recovered log holds none of the interrupted save. The next ordinary save then
works.

Commit ``e4a237db`` holds the first version of these cases, which ran each
writer to a crash at every act. Against the writers before Track 7 they
failed: partial saves, three more favorable line 21 results, and a torn line
that stranded the next save. Each writer now saves with one
``ActLog.append_batch``, so the sweep runs the writer once and replays its
batch with a crash after each act.

The readiness table is in
``docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track7-interruption-safety.md``.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator, Sequence
from unittest import mock

import pytest

from packages.derivation.loader import DerivationSchemas
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.findings import FindingModelError, project
from packages.tax import sli_relationship_review as review_mod
from packages.tax.loader import install_domain_scoped_supersession
from packages.tax.sli_relationship_recording import (
    RelationshipRecordingRefused,
    introduce_borrowing_reference_durably,
    record_borrowing_answer_durably,
)
import tests.test_sli_track4_support_chain as track4
import tests.test_sli_track5_worksheet_integration as t5
from tests.support import act as support_act

# Integration by construction: each case saves, interrupts, recovers fresh and
# runs the whole core calculations package on both runners.
pytestmark = pytest.mark.live

USER = t5.USER
AT = "2026-10-03T12:00:00Z"
LOAN_COST = "tax.us.2025.sli.loan-paid-only-school-costs"


class _Interrupted(Exception):
    """A simulated crash. No writer catches it."""


@contextmanager
def interrupt_at(line: Callable[[int], bool], *, torn: bool) -> Iterator[None]:
    """Crash while ``ActLog.append_batch`` writes a save's act lines.

    ``line(k)`` is asked before the k-th act line (from 0) is written; when it
    answers yes the process stops there, after half writing that line if
    ``torn``. The save's earlier lines are already written.
    """
    real_line = ActLog._write_pending_line
    written = 0

    def write(log: ActLog, handle: Any, data: bytes) -> None:
        nonlocal written
        if line(written):
            if torn:
                handle.write(data[: len(data) // 2])
                handle.flush()
            raise _Interrupted
        written += 1
        real_line(log, handle, data)

    with mock.patch.object(ActLog, "_write_pending_line", write):
        yield


class Result:
    """What the person would see: line 21 and each statement's standing."""

    def __init__(self, outcome: t5.Outcome) -> None:
        self.disposition = str(outcome.line21["disposition"])
        self.value = outcome.value()
        self.standing = t5.published(outcome.forward, t5.STANDING)

    def rank(self) -> float:
        """Higher is more favorable to the person: a deduction beats none."""
        if self.disposition == "blocked":
            return -1.0
        return float(self.value or 0)

    def __repr__(self) -> str:
        return f"Result({self.disposition}, {self.value}, {sorted(self.standing.values())})"


class InterruptedSaves(unittest.TestCase):
    """One test per writer: sweep every act, torn and clean."""

    _results: dict[str, Result] = {}

    def _result(self, ws: t5.Return, tag: str) -> Result:
        acts = ws.acts()
        key = hashlib.sha256(json.dumps(acts, sort_keys=True).encode("utf-8")).hexdigest()
        if key not in self._results:
            self._results[key] = Result(t5.run_live(acts, f"demo.run.track7.{tag}"))
        return self._results[key]

    def _assert_not_more_favorable(self, after: Result, before: Result) -> None:
        self.assertLessEqual(after.rank(), before.rank(), f"{after} is more favorable than {before}")
        for statement, standing in after.standing.items():
            if standing == "none":
                self.assertEqual(before.standing.get(statement), "none",
                                 f"{statement} became supported: {after} after {before}")

    def sweep(self, ws: t5.Return, save: Callable[[t5.Return], Any], *, expected: str | int,
              tag: str) -> None:
        """Interrupt ``save`` after each of its acts, recover, then save once more.

        The writer runs once, crashing while it writes its last act with a
        torn line. Its save must be exactly one ``append_batch``. That batch
        is then committed again from the same starting log with a crash after
        each act, torn and clean. Every recovery must hold none of the save,
        and its line 21 and standing must be no more favorable than before.
        The next ordinary save must then work. ``expected`` is the completed
        save's line 21: a value, or ``"blocked"``.
        """
        with ws.raw:
            before_bytes = ws.log.path.read_bytes()
            before_acts = ws.acts()
            serial, claims = ws._serial, dict(ws.claims)
            before = self._result(ws, f"{tag}.before")

            batches: list[list[dict[str, Any]]] = []
            real_batch = ActLog.append_batch
            last = {"line": -1}

            def spy(log: ActLog, items: Sequence[dict[str, Any]], expected_revision: int) -> int:
                batches.append([dict(item) for item in items])
                last["line"] = len(items) - 1
                return real_batch(log, items, expected_revision)

            def single_append(log: ActLog, act: dict[str, Any], expected_revision: int) -> int:
                raise AssertionError(f"the save appended a single act: {act['kind']}")

            # 1. The writer itself, crashing at its last act with a torn line.
            with mock.patch.object(ActLog, "append_batch", spy), \
                    mock.patch.object(ActLog, "append", single_append), \
                    interrupt_at(lambda k: k == last["line"], torn=True), \
                    self.assertRaises(_Interrupted):
                save(ws)
            self.assertEqual(len(batches), 1, "a save is one batch")
            [items] = batches
            self.assertGreater(len(items), 1, "the save wrote one act; nothing to interrupt")
            self.assertEqual(ws.acts(), before_acts)

            # 2. The same save, interrupted after each act, torn and clean.
            for after in range(len(items)):
                for torn in (True, False):
                    with self.subTest(after_acts=after, torn=torn):
                        ws.log.path.write_bytes(before_bytes)
                        with interrupt_at(lambda k: k == after, torn=torn), self.assertRaises(_Interrupted):
                            ActLog(ws.log.path.parent, ws.registry).append_batch(
                                items, expected_revision=len(before_acts))
                        recovered = ActLog(ws.log.path.parent, ws.registry).read()
                        self.assertIsNone(recovered.incomplete_tail)
                        # All or nothing: the interrupted save left none of itself.
                        self.assertEqual(recovered.acts, before_acts)
                        self._assert_not_more_favorable(self._result(ws, f"{tag}.{after}"), before)

            # 3. The next ordinary save, from the recovered log (a pending file
            # from the crash may still sit beside it).
            ws.log.path.write_bytes(before_bytes)
            ws._serial, ws.claims = serial, dict(claims)
            save(ws)
            done = self._result(ws, f"{tag}.done")
            if expected == "blocked":
                self.assertEqual(done.disposition, "blocked", done)
            else:
                self.assertEqual((done.disposition, done.value), ("published_value", expected), done)

    # -- record_submission_durably ------------------------------------------

    def test_one_save_with_both_links(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.answer("loan", "autumn", "yes")
        ws.answer("enroll", "autumn", "yes")
        ws.common_answers("cedar")

        def save(ws: t5.Return) -> None:
            name = ws._name("both-links")
            review_mod.save_review(
                ws.log, ws.registry, ws._review(name), borrowing_ref=ws.borrowing["autumn"],
                schooling_fact_id=ws.school["autumn"], statement_fact_id=ws.statement["cedar"],
                financing_response="yes", inclusion_response="yes", actor=USER, at=AT,
                submission_id=f"demo.track7.submission.{name}", evidence_id=f"demo.evidence.track7.{name}")

        self.sweep(ws, save, expected=1500, tag="both-links")

    def test_yes_after_a_withdrawn_link(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.plain()
        ws.outcome("statement-inclusion", "autumn", "cedar", "withdrawn")
        self.sweep(ws, lambda ws: ws.link("statement-inclusion", "autumn", "cedar", "yes"),
                   expected=1500, tag="yes-after-withdrawn")

    # -- answers on an affirmed link ----------------------------------------

    def test_no_on_the_statement_link(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.plain()
        self.sweep(ws, lambda ws: ws.outcome("statement-inclusion", "autumn", "cedar", "no"),
                   expected="blocked", tag="inclusion-no")

    def test_no_on_the_financing_link(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.plain()
        self.sweep(ws, lambda ws: ws.outcome("financing", "autumn", "autumn", "no"),
                   expected="blocked", tag="financing-no")

    def test_cannot_tell_on_the_statement_link(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.plain()
        self.sweep(ws, lambda ws: ws.outcome("statement-inclusion", "autumn", "cedar", "cannot-tell"),
                   expected="blocked", tag="inclusion-cannot-tell")

    def test_withdrawing_the_statement_link(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.plain()
        self.sweep(ws, lambda ws: ws.outcome("statement-inclusion", "autumn", "cedar", "withdrawn"),
                   expected="blocked", tag="inclusion-withdrawn")

    def test_correcting_the_only_link_beside_old_answers(self) -> None:
        # Both paths present blocks. The corrected link keeps the new path
        # present; an interruption that dropped it would let the old path deduct.
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.old_answers("cedar")
        ws.link("statement-inclusion", "autumn", "cedar")

        def save(ws: t5.Return) -> None:
            name = ws._name("correct-link")
            review_mod.correct_review_claim(
                ws.log, ws.registry, finding_id=ws.claims[("statement-inclusion", "autumn", "cedar")],
                review=ws._review(name), borrowing_ref=ws.borrowing["spring"], schooling_fact_id=None,
                statement_fact_id=ws.statement["cedar"], financing_response="unanswered",
                inclusion_response="yes", actor=USER, at=AT,
                submission_id=f"demo.track7.submission.{name}", evidence_id=f"demo.evidence.track7.{name}")

        self.sweep(ws, save, expected="blocked", tag="correct-link")

    # -- the two borrowing answers ------------------------------------------

    def test_answering_a_borrowing_question(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.link("financing", "autumn", "autumn")
        ws.link("statement-inclusion", "autumn", "cedar")
        ws.answer("loan", "autumn", "yes")
        ws.common_answers("cedar")
        self.sweep(ws, lambda ws: ws.answer("enroll", "autumn", "yes"), expected=1500, tag="answer")

    def test_correcting_a_borrowing_answer(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.plain()
        answer = ws.current_finding(LOAN_COST, (("borrowing", ws.borrowing["autumn"]),))

        def save(ws: t5.Return) -> None:
            name = ws._name("correct-answer")
            review = review_mod.prepare_borrowing_answer_review(
                ws.log, ws.registry, review_id=f"demo.track7.review.{name}", shown_at=AT,
                borrowing_refs=tuple(ws.borrowing.values()))
            review_mod.correct_borrowing_answer_review(
                ws.log, ws.registry, review, finding_id=answer, borrowing_ref=ws.borrowing["autumn"],
                question="loan-paid-only-school-costs", response="no", actor=USER, at=AT,
                submission_id=f"demo.track7.submission.{name}", evidence_id=f"demo.evidence.track7.{name}")

        self.sweep(ws, save, expected="blocked", tag="correct-answer")

    def test_first_answer_in_a_v1_workspace_adopts_bundle_v2(self) -> None:
        # Carried item 1: a workspace set up before the two questions existed
        # adopts relationship bundle v2 in the same save as its first answer.
        ws = t5.Return(amounts={"cedar": 1500.0}, bundle_version="v1")
        ws.link("financing", "autumn", "autumn")
        ws.link("statement-inclusion", "autumn", "cedar")
        ws.common_answers("cedar")
        # The deduction still waits for the second answer.
        self.sweep(ws, lambda ws: ws.answer("loan", "autumn", "yes"), expected="blocked", tag="v1-adopt")

    # -- the reviewed statement correction ----------------------------------

    def _correction(self, ws: t5.Return, *, scope: str, borrowing: str | None, amount: float) -> None:
        name = ws._name(f"correction-{scope}")
        finding = (ws.claims[("statement-inclusion", borrowing, "cedar")]
                   if scope in {"inclusion-removed", "inclusion-uncertain"} and borrowing else None)
        review_mod.apply_statement_correction_review(
            ws.log, ws.registry, review=ws._review(name), statement_fact_id=ws.statement["cedar"],
            scope=scope, borrowing_ref=ws.borrowing[borrowing] if borrowing else None, finding_id=finding,
            corrected_box1_total=amount, source_correction_id=f"demo.track7.correction.{name}",
            actor=USER, at=AT, submission_id=f"demo.track7.submission.{name}",
            evidence_id=f"demo.evidence.track7.{name}")

    def test_amount_only_correction(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.plain()
        self.sweep(ws, lambda ws: self._correction(ws, scope="amount-only", borrowing=None, amount=1000.0),
                   expected=1000, tag="amount-only")

    def test_correction_adding_a_loan(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.plain()
        self.sweep(ws, lambda ws: self._correction(ws, scope="inclusion-added", borrowing="spring", amount=2200.0),
                   expected="blocked", tag="inclusion-added")

    def test_correction_removing_a_loan(self) -> None:
        ws = t5.Return(amounts={"cedar": 2200.0})
        ws.plain()
        ws.link("financing", "spring", "spring")
        ws.link("statement-inclusion", "spring", "cedar")
        ws.answer("loan", "spring", "yes")
        ws.answer("enroll", "spring", "yes")
        self.sweep(ws, lambda ws: self._correction(ws, scope="inclusion-removed", borrowing="autumn", amount=1500.0),
                   expected=1500, tag="inclusion-removed")

    def test_correction_with_an_uncertain_loan(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0})
        ws.plain()
        self.sweep(ws, lambda ws: self._correction(ws, scope="inclusion-uncertain", borrowing="autumn",
                                                   amount=1400.0),
                   expected="blocked", tag="inclusion-uncertain")

    # -- the v1 answer path (carried item 2) --------------------------------

    def test_v1_no_on_the_statement_link(self) -> None:
        # The v1 path ends the affirmation and saves the answer in one write.
        ws = t5.Return(amounts={"cedar": 1500.0}, bundle_version="v1")
        ws.link("financing", "autumn", "autumn")
        ws.link("statement-inclusion", "autumn", "cedar")
        ws.common_answers("cedar")
        self.sweep(ws, lambda ws: ws.outcome("statement-inclusion", "autumn", "cedar", "no"),
                   expected="blocked", tag="v1-no")


class BundleAdoption(unittest.TestCase):
    """Carried item 1: adopt relationship bundle v2 on the first borrowing answer."""

    def test_a_v1_workspace_records_its_answers_and_deducts(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0}, bundle_version="v1")
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.common_answers("cedar")
            before = len(ws.acts())
            ws.answer("loan", "autumn", "yes")
            added = ws.acts()[before:]
            # One save: the adoption first, then the answer's three acts.
            self.assertEqual([row["kind"] for row in added],
                             ["bundle-adoption", "evidence-submitted", "contribution", "assertion"])
            self.assertEqual(added[0]["payload"]["bundle"]["version"], "v2")
            ws.answer("enroll", "autumn", "yes")
            # Bundle v2 is adopted once.
            adoptions = [row for row in ws.acts() if row["kind"] == "bundle-adoption"
                         and row["payload"]["bundle"]["id"] == "tax.us.2025.sli-relationship-source"]
            self.assertEqual([row["payload"]["bundle"]["version"] for row in adoptions], ["v1", "v2"])
            outcome = t5.run_live(ws.acts(), "demo.run.track7.v1-adopted")
            self.assertEqual(outcome.value(), 1500)

    def test_v1_history_with_an_ended_link_is_refused_with_a_reason(self) -> None:
        # v1 kept no current fact for a withdrawal, a no or a cannot-tell. Under
        # v2 those would block or keep the new path present; adopting v2 over
        # them would read them as never said. The save is refused instead.
        for outcome in ("withdrawn", "no"):
            with self.subTest(outcome=outcome):
                ws = t5.Return(amounts={"cedar": 1500.0}, bundle_version="v1")
                with ws.raw:
                    ws.link("statement-inclusion", "autumn", "cedar")
                    ws.link("statement-inclusion", "spring", "cedar")
                    ws.outcome("statement-inclusion", "spring", "cedar", outcome)
                    before = ws.log.path.read_bytes()
                    with self.assertRaisesRegex(RelationshipRecordingRefused, "before relationship bundle v2"):
                        ws.answer("loan", "autumn", "yes")
                    self.assertEqual(ws.log.path.read_bytes(), before)

    def test_a_workspace_without_the_relationship_bundle_is_not_given_one(self) -> None:
        # Nothing to upgrade: a workspace that never adopted the relationship
        # vocabulary keeps refusing the borrowing questions.
        registry = install_domain_scoped_supersession(DerivationSchemas().registry)
        with tempfile.TemporaryDirectory() as raw:
            log = ActLog(Path(raw) / "workspace", registry)
            log.append(support_act(0, "bundle-adoption", {"bundle": track4._load("f1098e.bundle.json")}),
                       expected_revision=0)
            introduce_borrowing_reference_durably(log, registry, reference_id="demo.track7.borrowing",
                                                  description="Study loan", actor=USER, at=AT)
            before = log.path.read_bytes()
            with self.assertRaisesRegex(RelationshipRecordingRefused, "not adopted"):
                record_borrowing_answer_durably(
                    log, registry, question="loan-paid-only-school-costs",
                    borrowing_ref="demo.track7.borrowing", response="yes",
                    submission_id="demo.track7.submission.bare", evidence_id="demo.evidence.track7.bare",
                    actor=USER, at=AT)
            self.assertEqual(log.path.read_bytes(), before)


class NewWriteRefusalLeavesNothing(unittest.TestCase):
    """Carried item 3: a refusal by the ADR 0077 Part 5 step leaves no act."""

    def test_a_correction_refused_at_its_box1_act_writes_nothing(self) -> None:
        ws = track4.Workspace()
        with ws.raw:
            ws.link("statement-inclusion", "autumn", "cedar")
            name = ws._name("scope")
            review = ws._review(name)
            shown = review_mod._shown_statement_finding_id(review, ws.statement["cedar"])
            review_mod.save_review(
                ws.log, ws.registry, review, borrowing_ref=None, schooling_fact_id=None,
                statement_fact_id=ws.statement["cedar"], financing_response="unanswered",
                inclusion_response="unanswered", actor=USER, at=AT,
                submission_id=f"demo.track7.submission.{name}", evidence_id=f"demo.evidence.track7.{name}",
                statement_correction={"statement_fact_id": ws.statement["cedar"], "scope": "amount-only",
                                      "included_borrowings_changed": False,
                                      "source_correction_id": "demo.track7.correction.scope",
                                      "corrected_box1_total": 1300.0,
                                      "reviewed_statement_finding_id": shown})
            before = ws.log.path.read_bytes()
            # The recorder's own amount check is bypassed, so only the new-write
            # step sees that 1999 is not the amount the review bound.
            with mock.patch.object(review_mod, "_amounts_equal", return_value=True), \
                    self.assertRaisesRegex(FindingModelError, "scoped supersession violated"):
                review_mod._append_statement_source_correction_durably(
                    ws.log, ws.registry, statement_fact_id=ws.statement["cedar"], corrected_total=1999.0,
                    correction_id="demo.track7.correction.scope",
                    scope_evidence_id=f"demo.evidence.track7.{name}", actor=USER, at=AT)
            self.assertEqual(ws.log.path.read_bytes(), before)
            # The bound correction is still available and is admitted.
            review_mod._append_statement_source_correction_durably(
                ws.log, ws.registry, statement_fact_id=ws.statement["cedar"], corrected_total=1300.0,
                correction_id="demo.track7.correction.scope",
                scope_evidence_id=f"demo.evidence.track7.{name}", actor=USER, at=AT)
            state = project(ws.acts(), ws.registry)
            current = compute_currency(state).current_finding_ids
            values = [row["value"] for fid, row in state.findings.items()
                      if fid in current and row.get("fact_id") == ws.statement["cedar"]]
            self.assertEqual(values, [1300.0])


class NoClaimWorkspace(unittest.TestCase):
    def test_a_workspace_with_no_relationship_claims_is_unchanged(self) -> None:
        # Old answers only: written act by act through ActLog.append as before,
        # never through a batch, and line 21 is the v38 result.
        ws = t5.Return(amounts={"cedar": 1500.0})
        with ws.raw, mock.patch.object(ActLog, "append_batch", side_effect=AssertionError("batch used"),
                                       create=True):
            before = len(ws.acts())
            ws.old_answers("cedar")
            self.assertEqual(len(ws.acts()), before + 15)
            self.assertFalse((ws.log.path.parent / "acts.jsonl.pending").exists())
            outcome = t5.run_live(ws.acts(), "demo.run.track7.no-claims")
            self.assertEqual((outcome.line21["disposition"], outcome.value()), ("published_value", 1500))


if __name__ == "__main__":
    unittest.main()
