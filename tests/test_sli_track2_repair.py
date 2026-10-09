"""Track 2 repair: denial attribution scoped to its borrowing (defect 1),
and a corrected borrowing answer's history (defect 2), under v42.

Each case is run through ``live_coordinate_run`` with both runners, with the
saved presentation reloaded from disk, mirroring
``tests/test_sli_track2_explanation.py``. D1 and H1 fail on the pre-repair
explanation, which applied denial wording form-wide and collected history only
from borrowings in the slice being collected; that was shown separately and
is not re-run here.
"""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

import pytest

import tests.test_sli_track1_combined_standing as track1
import tests.test_sli_track2_explanation as track2
import tests.test_sli_track5_worksheet_integration as track5
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface

pytestmark = pytest.mark.live

DENIED = track2.DENIED
DENIAL = track2.DENIAL
ENROLL = "tax.us.2025.sli.enrolled-at-least-half-time"
LOAN = "tax.us.2025.sli.loan-paid-only-school-costs"
FINANCING = "tax.us.2025.sli.financing-relationship"


class _ModelShim:
    """Just enough of ``track5.Outcome`` for ``track2._row`` to read a model."""

    def __init__(self, model: dict[str, Any]) -> None:
        self.model = model


def _kind(row: dict[str, Any]) -> str:
    return str(row["account"]["used"]["kind"])


def _recorded(row: dict[str, Any]) -> list[dict[str, str]]:
    return list(row["account"]["recordedNotUsed"])


def _said(row: dict[str, Any], slot: str) -> list[dict[str, Any]]:
    return list(row["account"]["said"][slot])


def _by_fact_type(items: list[dict[str, Any]], fact_type: str) -> dict[str, Any]:
    matches = [item for item in items if item["factType"] == fact_type]
    if len(matches) != 1:
        raise AssertionError(f"expected exactly one {fact_type}, found {len(matches)}")
    return matches[0]


# ---------------------------------------------------------------------------
# Defect 1: Cedar has an affirmed-but-incomplete borrowing (Autumn, missing
# its enrollment answer) and a separately denied borrowing (Spring).
# ---------------------------------------------------------------------------


def _d1_populate(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    track1._link_complete(ws, "autumn", "autumn", "cedar", enroll=None)
    track1._link_complete(ws, "spring", "spring", "cedar")
    ws.outcome("statement-inclusion", "spring", "cedar", "no")
    track1._birch_old(ws)


def _d1b_populate(ws: track5.Return) -> None:
    """D1 with no Spring borrowing at all -- the control."""
    ws.old_answers("cedar")
    track1._link_complete(ws, "autumn", "autumn", "cedar", enroll=None)
    track1._birch_old(ws)


def _run_case(
    name: str, populate: Any, *, capture: Any = None,
) -> tuple[track5.Outcome, dict[str, dict[str, Any]], Any]:
    """Run one case. ``capture(ws)`` runs while the act log is still live, so a
    caller can resolve finding ids before ``ws.raw`` is torn down."""
    ws = track5.Return(wages=50000, amounts=track1.STANDARD)
    with ws.raw:
        populate(ws)
        captured = capture(ws) if capture is not None else None
        track1.adopt_v42(ws)
        outcome = track2._run(ws, name)
        rows = {statement: track2._row(outcome, ws, statement) for statement in track1.STANDARD}
        return outcome, rows, captured


def _d1_capture(ws: track5.Return) -> dict[str, str]:
    return {
        "spring_denial_id": ws.current_finding(
            "tax.us.2025.sli.statement-inclusion-denied",
            ws.statement_keys["cedar"] + (("borrowing", ws.borrowing["spring"]),),
        ),
        "autumn_loan_id": ws.current_finding(LOAN, (("borrowing", ws.borrowing["autumn"]),)),
        "autumn_financing_id": ws.current_finding(
            FINANCING, (("borrowing", ws.borrowing["autumn"]),) + track5.Return.SCHOOL_KEYS["autumn"],
        ),
    }


class Defect1DenialAttribution(unittest.TestCase):
    def test_d1_denial_wording_is_scoped_to_spring(self) -> None:
        outcome, rows, ids = _run_case("D1", _d1_populate, capture=_d1_capture)
        self.assertEqual(outcome.line21["value"], 2500)
        self.assertFalse(outcome.line21.get("reasons"))
        cedar, birch = rows["cedar"], rows["birch"]
        self.assertEqual(_kind(cedar), "older-yes-cover")

        spring_denial_id = ids["spring_denial_id"]
        autumn_loan_id = ids["autumn_loan_id"]
        autumn_financing_id = ids["autumn_financing_id"]

        current = _said(cedar, "current")
        current_by_id = {item["findingId"]: item for item in current}
        denial_item = _by_fact_type(current, DENIED)
        self.assertEqual(denial_item["findingId"], spring_denial_id)
        self.assertEqual(denial_item["proposition"], DENIAL)

        # Two borrowings both carry a loan-cost/financing answer; Autumn's
        # own findings (by identity, not by label) are the ones in current.
        self.assertIn(autumn_loan_id, current_by_id)
        self.assertEqual(current_by_id[autumn_loan_id]["factType"], LOAN)
        self.assertIn(autumn_financing_id, current_by_id)
        self.assertEqual(current_by_id[autumn_financing_id]["factType"], FINANCING)

        # The cover names Autumn's missing enrollment answer, not the denial.
        self.assertEqual(
            cedar["basis"]["standsInFor"],
            ["The older yes stands in for the missing enrollment answer."],
        )

        # Any "denied" wording in recordedNotUsed is on Spring's own entries only.
        recorded = _recorded(cedar)
        for item in recorded:
            self.assertIn("on a borrowing this form denied", item["text"])
        self.assertTrue(recorded)
        self.assertNotIn(autumn_loan_id, {item["findingId"] for item in recorded})
        self.assertNotIn(autumn_financing_id, {item["findingId"] for item in recorded})

        self.assertEqual(_kind(birch), "older-method")
        track2._quote(
            "D1",
            "D1 published 2500; cedar's denial wording stays on spring, autumn's missing "
            "enrollment is the cover; birch older-method",
        )

    def test_d1b_control_without_spring_matches_autumns_explanation(self) -> None:
        _outcome_d1, rows_d1, _ids_d1 = _run_case("D1", _d1_populate, capture=_d1_capture)
        outcome_b, rows_b, _ids_b = _run_case("D1b", _d1b_populate)
        self.assertEqual(outcome_b.line21["value"], 2500)
        cedar_d1, cedar_d1b = rows_d1["cedar"], rows_b["cedar"]
        self.assertEqual(cedar_d1["basis"]["standsInFor"], cedar_d1b["basis"]["standsInFor"])
        self.assertEqual(cedar_d1b["basis"]["standsInFor"], ["The older yes stands in for the missing enrollment answer."])
        self.assertEqual(_recorded(cedar_d1b), [])
        track2._quote("D1b", "D1b (no spring) published 2500; cedar's cover names the missing enrollment answer, same as D1; recorded none")


# ---------------------------------------------------------------------------
# Defect 2: a corrected borrowing answer must stay visible in history even
# though its statement's inclusion is unchanged and stays current.
# ---------------------------------------------------------------------------


def _h1_populate(ws: track5.Return) -> None:
    track1._k1(ws)


class Defect2CorrectedAnswerHistory(unittest.TestCase):
    def test_h1_corrected_enrollment_enters_history(self) -> None:
        ws = track5.Return(wages=50000, amounts=track1.STANDARD)
        with ws.raw:
            _h1_populate(ws)
            track1.adopt_v42(ws)
            original_yes_id = ws.current_finding(ENROLL, (("borrowing", ws.borrowing["autumn"]),))
            track1._correct_enrollment(ws)
            corrected_no_id = ws.current_finding(ENROLL, (("borrowing", ws.borrowing["autumn"]),))
            self.assertNotEqual(original_yes_id, corrected_no_id)
            outcome = track2._run(ws, "H1")
            cedar = track2._row(outcome, ws, "cedar")

        self.assertEqual(outcome.line21["disposition"], "blocked")
        self.assertEqual(cedar["account"]["used"]["combined"], "contradicts-enrollment-no")
        self.assertEqual(_kind(cedar), "nothing")

        current = _said(cedar, "current")
        history = _said(cedar, "history")
        current_ids = {item["findingId"] for item in current}
        history_ids = {item["findingId"] for item in history}

        self.assertIn(corrected_no_id, current_ids)
        self.assertNotIn(corrected_no_id, history_ids)
        self.assertIn(original_yes_id, history_ids)
        self.assertNotIn(original_yes_id, current_ids)

        history_enroll = _by_fact_type(history, ENROLL)
        self.assertEqual(history_enroll["response"], "yes")
        self.assertEqual(history_enroll["findingId"], original_yes_id)
        current_enroll = _by_fact_type(current, ENROLL)
        self.assertEqual(current_enroll["response"], "no")
        self.assertEqual(current_enroll["findingId"], corrected_no_id)

        # History holds no finding from an unrelated borrowing: only the
        # displaced enrollment answer was ever superseded here, so it is the
        # only history entry (loan-cost and financing stayed current and
        # unchanged, and there is no other borrowing on this form).
        self.assertEqual([item["findingId"] for item in history], [original_yes_id])
        track2._quote(
            "H1",
            "H1 blocked, contradicts-enrollment-no; cedar's displaced yes is history, the "
            "correction's no is current",
        )

    def test_h1_saved_presentation_is_not_rewritten_by_a_later_run(self) -> None:
        work = tempfile.mkdtemp(prefix="sli-track2repair-h1saved-")
        try:
            ws = track5.Return(wages=50000, amounts=track1.STANDARD)
            with ws.raw:
                _h1_populate(ws)
                track1.adopt_v42(ws)
                acts_before = tuple(ws.acts())
                capability = WorkspaceCapability(Path(work) / "workspace")
                surface = PublicationSurface(track5.RELEASE_DIR, track1.V40_REGISTRY, track5.CONTENT)
                before = live_coordinate_run(
                    capability, repo_root=track5.ROOT, authoritative_acts=acts_before,
                    workspace_revision=len(acts_before), run_scope=track5.SCOPE, scope_user=track5.USER,
                    request={"schema": "run-request.v1"}, run_id="demo.run.track2.h1-saved-before",
                    governance_pins=[], surface=surface, output_name="h1-before.json",
                )
                if before.refusal is not None or before.presentation_path is None:
                    raise AssertionError(f"H1-saved before: refused {before.refusal!r}")
                before_text = before.presentation_path.read_text("utf-8")
                before_model = json.loads(before_text)
                before_row = track2._row(cast(track5.Outcome, _ModelShim(before_model)), ws, "cedar")
                self.assertEqual(before_row["account"]["said"]["history"], [])
                before_enroll = _by_fact_type(_said(before_row, "current"), ENROLL)
                self.assertEqual(before_enroll["response"], "yes")

                track1._correct_enrollment(ws)
                acts_after = tuple(ws.acts())
                after = live_coordinate_run(
                    capability, repo_root=track5.ROOT, authoritative_acts=acts_after,
                    workspace_revision=len(acts_after), run_scope=track5.SCOPE, scope_user=track5.USER,
                    request={"schema": "run-request.v1"}, run_id="demo.run.track2.h1-saved-after",
                    governance_pins=[], surface=surface, output_name="h1-after.json",
                )
                if after.refusal is not None or after.presentation_path is None:
                    raise AssertionError(f"H1-saved after: refused {after.refusal!r}")

                reloaded_text = before.presentation_path.read_text("utf-8")
                self.assertEqual(reloaded_text, before_text)
                reloaded_model = json.loads(reloaded_text)
                reloaded_row = track2._row(cast(track5.Outcome, _ModelShim(reloaded_model)), ws, "cedar")
                self.assertEqual(reloaded_row["account"]["said"]["history"], [])
                reloaded_enroll = _by_fact_type(_said(reloaded_row, "current"), ENROLL)
                self.assertEqual(reloaded_enroll["response"], "yes")
        finally:
            shutil.rmtree(work, ignore_errors=True)

    def test_h2_unrelated_statements_borrowing_stays_out_of_cedars_account(self) -> None:
        def populate(ws: track5.Return) -> None:
            ws.old_answers("cedar")
            track1._link_complete(ws, "autumn", "autumn", "cedar")
            track1._link_complete(ws, "spring", "spring", "birch")
            ws.common_answers("birch")

        ws = track5.Return(wages=50000, amounts=track1.STANDARD)
        with ws.raw:
            populate(ws)
            track1.adopt_v42(ws)
            spring_enroll_id = ws.current_finding(ENROLL, (("borrowing", ws.borrowing["spring"]),))
            track1._correct_enrollment(ws)
            outcome = track2._run(ws, "H2")
            cedar = track2._row(outcome, ws, "cedar")
            birch = track2._row(outcome, ws, "birch")

        self.assertEqual(outcome.line21["disposition"], "blocked")
        self.assertEqual(cedar["account"]["used"]["combined"], "contradicts-enrollment-no")

        cedar_current_ids = {item["findingId"] for item in _said(cedar, "current")}
        cedar_history_ids = {item["findingId"] for item in _said(cedar, "history")}
        self.assertNotIn(spring_enroll_id, cedar_current_ids)
        self.assertNotIn(spring_enroll_id, cedar_history_ids)

        birch_current = _by_fact_type(_said(birch, "current"), ENROLL)
        self.assertEqual(birch_current["findingId"], spring_enroll_id)
        self.assertEqual(birch_current["response"], "yes")
        track2._quote(
            "H2",
            "H2 blocked on cedar's contradiction; birch keeps its own spring account, unaffected",
        )


if __name__ == "__main__":
    unittest.main()
