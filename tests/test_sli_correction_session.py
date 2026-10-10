"""Track 1 -- the correction session: opening a saved line 21 result and
correcting one borrowing's loan-cost answer.

The first working example goes through the real recorder, review, and
``live_coordinate_run``, with saved presentations reread from disk; the
deciding checks throughout are finding ids, not message strings. The lighter
unit checks below (resolve outcomes, choice enumeration/dedup, admission,
the neighbor) use the fast ``tests.test_sli_track4_support_chain.Workspace``
fixture directly, without going through a live run, since they do not need
the full v42 production surface to demonstrate the behavior under test.
"""
from __future__ import annotations

import atexit
import json
import re
import shutil
import socket
import subprocess
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
from unittest import mock

import tests.test_sli_track1_combined_standing as T1
import tests.test_sli_track4_support_chain as T4
import tests.test_sli_track5_worksheet_integration as T5
import tests.test_sli_track17_relationship_applicability as track17
import packages.derivation.correction_session as correction_session_mod
from packages.derivation.correction_session import (
    CorrectionRuntime,
    CorrectionSessionServer,
    ENROLL_FACT_TYPE,
    LOAN_COST_FACT_TYPE,
    RUN_SCOPE,
    SCOPE_USER,
    build_correction_surface,
    core_calculations_surface,
    enumerate_choices,
    load_seed_acts,
    resolve_correction_surface,
    resolve_displayed_answer_to_target,
)
from packages.derivation.live import LiveCoordinatorOutcome, live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import Refusal
from packages.kernel.act_log import ActLog
from packages.kernel.contribution import ContributionBatchResult
from packages.kernel.facts import fact_id_for
from packages.tax import sli_relationship_review as review_mod
from packages.tax.loader import install_domain_scoped_supersession
from packages.tax.sli_relationship_recording import (
    BORROWING_ANSWER_EVIDENCE_KIND,
    RelationshipRecordingRefused,
    introduce_borrowing_reference_durably,
)

REPO = Path(__file__).resolve().parent.parent
_NODE = shutil.which("node")
_BROWSER = next(
    (
        str(path)
        for path in (
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
            Path("/usr/bin/google-chrome"),
            Path("/usr/bin/google-chrome-stable"),
            Path("/usr/bin/chromium"),
            Path("/usr/bin/chromium-browser"),
        )
        if path.is_file()
    ),
    None,
)


def _run_saved(work_dir: Path, acts: Any, run_id: str) -> Any:
    surface = core_calculations_surface(REPO)
    return live_coordinate_run(
        WorkspaceCapability(work_dir / "L"), repo_root=REPO, authoritative_acts=acts,
        workspace_revision=len(acts), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
        request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
        surface=surface, output_name=f"{run_id}.json",
    )


# Redacted refusal (plan, Track 1 corrections, correction 1). None of these
# patterns may appear in a refusal response: an act, record, finding or demo
# identifier; an ``sli.``/``tax.us.`` token; dict-like text (Python's own
# ``repr`` of a mapping, which is what an un-redacted terminal record would
# render as).
_FORBIDDEN_REFUSAL_PATTERNS = (
    re.compile(r"\bsli\."), re.compile(r"\btax\.us\."), re.compile(r"\bdemo\."),
    re.compile(r"[{}]"), re.compile(r"'[a-zA-Z_]+':"),
)


def _assert_redacted(testcase: unittest.TestCase, reason: Any) -> None:
    testcase.assertIsInstance(reason, str)
    for pattern in _FORBIDDEN_REFUSAL_PATTERNS:
        testcase.assertIsNone(pattern.search(reason), f"{pattern.pattern!r} matched {reason!r}")


# ---------------------------------------------------------------------------
# Track 1 corrections, correction 5 (R3 finding 6): shared initial live
# runs. Seven of this module's tests each ran their own, otherwise-identical
# initial saved-state computation over the committed correction_t1 fixture;
# only the subsequent choose/confirm step legitimately differed per test.
# Built once per test *process* (module-level, lazily, under a lock), and
# never written to: every test that uses it still writes through its own
# fresh ``CorrectionRuntime`` and its own temporary session workspace.
# Safe under ``-n auto`` -- each worker is a separate process with its own
# cache entry, and no test ever mutates the shared acts list or the shared
# presentation file.
# ---------------------------------------------------------------------------

_SHARED_SAVED_RUN_LOCK = threading.Lock()
_shared_saved_run_cache: dict[str, Any] = {}


def _shared_saved_run() -> tuple[Any, Any]:
    """The simple two-form fixture's initial saved run (Cedar/Autumn,
    Birch/Spring), shared by every test that only reads it."""
    with _SHARED_SAVED_RUN_LOCK:
        if "outcome" not in _shared_saved_run_cache:
            work_dir = TemporaryDirectory(prefix="sli-correction-shared-saved-")
            atexit.register(work_dir.cleanup)
            acts = load_seed_acts(REPO)
            outcome = _run_saved(Path(work_dir.name), acts, "demo.correction.test.shared")
            _shared_saved_run_cache["acts"] = acts
            _shared_saved_run_cache["outcome"] = outcome
        return _shared_saved_run_cache["acts"], _shared_saved_run_cache["outcome"]


class FirstWorkingExample(unittest.TestCase):
    """Two forms, one correction, one recalculation, the page served."""

    def test_choose_cedar_confirm_yes_to_no(self) -> None:
        acts, saved_outcome = _shared_saved_run()
        surface = core_calculations_surface(REPO)
        with TemporaryDirectory(prefix="sli-correction-session-") as session_dir:
            before_text = saved_outcome.presentation_path.read_text("utf-8")

            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO, surface=surface,
                run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=saved_outcome.presentation_path,
                saved_run_id="demo.correction.test.shared", seed_acts=acts,
            )

            state = runtime.state()
            choices = state["choices"]
            self.assertEqual(len(choices), 2)
            [cedar] = [c for c in choices.values()
                      if any(f.get("statement", "").startswith("2025 Form 1098-E from Cedar")
                             for f in c["forms"])]
            [birch] = [c for c in choices.values()
                      if any(f.get("statement", "").startswith("2025 Form 1098-E from Birch")
                             for f in c["forms"])]
            birch_finding_id_before = birch["finding_id"]

            # Serve the page over loopback and confirm it is reachable (the
            # page served, ADR-0049 surface artifact route, no Node needed).
            dist = build_correction_surface(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO)
            with CorrectionSessionServer(runtime, dist) as server:
                with urllib.request.urlopen(server.url, timeout=10) as response:
                    self.assertEqual(response.status, 200)
                    served_bytes = response.read()
            self.assertEqual(
                served_bytes,
                (REPO / "packages" / "sample_data" / "sli_correction_t1" /
                 "surface" / "content" / "app" / "index.html").read_bytes(),
            )

            chosen = runtime.choose(cedar["finding_id"])
            self.assertEqual(chosen["status"], "current")
            self.assertEqual(chosen["confirmation"]["current_answer"], "yes")
            token = chosen["token"]

            result = runtime.confirm(token, "no")
            self.assertEqual(result["outcome"], "saved-and-calculated")
            predecessor = result["predecessor_finding_id"]
            successor = result["successor_finding_id"]
            self.assertEqual(predecessor, cedar["finding_id"])
            self.assertNotEqual(predecessor, successor)

            rows_by_lender = {row["statementLabel"]["lender"]: row for row in result["line21_rows"]}
            cedar_row = rows_by_lender["Cedar Servicing"]
            birch_row = rows_by_lender["Birch Servicing"]

            # Cedar's new standing: the correction is reflected and blocks
            # the row.
            self.assertEqual(cedar_row["standing"], "loan-cost-no")
            self.assertEqual(cedar_row["support"], "not-supported")

            # Track 1 explanation parity: a named-by-reason row carries the
            # reason sentence the citation walk resolves from the saved
            # presentation's own line 21 section (``resolved.reasons``), by
            # the row's own ``status.reasonIndices`` -- never just the
            # index or the fact id. A supported row carries none.
            self.assertEqual(cedar_row["status"]["kind"], "named-by-reason")
            self.assertEqual(len(cedar_row["reasonSentences"]), 1)
            self.assertIn(
                "did not pay only for school costs", cedar_row["reasonSentences"][0])
            self.assertNotIn("reasonSentences", birch_row)

            loan_cost_now = next(
                item for item in cedar_row["account"]["said"]["current"]
                if item["factType"] == "tax.us.2025.sli.loan-paid-only-school-costs")
            self.assertEqual(loan_cost_now["findingId"], successor)
            self.assertEqual(loan_cost_now["response"], "no")
            history_ids = {item["findingId"] for item in cedar_row["account"]["said"]["history"]}
            self.assertIn(predecessor, history_ids)

            # Birch's findings and standing are unchanged.
            self.assertEqual(birch_row["standing"], "none")
            self.assertEqual(birch_row["support"], "plain-case-supported")
            birch_loan_cost_id = next(
                item["findingId"] for item in birch_row["basis"]["answers"]
                if item["factType"] == "tax.us.2025.sli.loan-paid-only-school-costs")
            self.assertEqual(birch_loan_cost_id, birch_finding_id_before)

            # The earlier presentation is byte-identical.
            self.assertEqual(saved_outcome.presentation_path.read_text("utf-8"), before_text)

            # The displayed (now-superseded) predecessor id resolves to the
            # successor as current, never silently retargeting.
            resolved_predecessor = runtime.resolve(predecessor)
            self.assertEqual(resolved_predecessor["status"], "superseded")
            self.assertEqual(resolved_predecessor["current_finding_id"], successor)
            resolved_successor = runtime.resolve(successor)
            self.assertEqual(resolved_successor["status"], "current")

            # Birch's own displayed id is still current and unaffected.
            new_state = runtime.state()
            birch_new = next(c for c in new_state["choices"].values()
                             if c["finding_id"] == birch_finding_id_before)
            self.assertEqual(birch_new["finding_id"], birch_finding_id_before)


class ChoicesEnumeration(unittest.TestCase):
    """Dedup by finding id, across both saved row shapes."""

    def test_shared_borrowing_two_forms_is_one_choice(self) -> None:
        ws = T4.Workspace()
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.link("statement-inclusion", "autumn", "birch")
            ws.answer("loan", "autumn", "yes")
            ws.answer("enroll", "autumn", "yes")
            acts = ws.acts()
            finding_id = ws.current_finding(T4.LOAN, (("borrowing", ws.borrowing["autumn"]),))
            presentation = {"line21Explanation": {"rows": [
                {"statementLabel": {"lender": "Cedar Servicing", "statement": "2025 Form 1098-E from Cedar"},
                 "basis": {"answers": [{"findingId": finding_id, "factType": T4.LOAN, "response": "yes"}]}},
                {"statementLabel": {"lender": "Birch Servicing", "statement": "2025 Form 1098-E from Birch"},
                 "account": {"said": {"current": [
                     {"findingId": finding_id, "factType": T4.LOAN, "response": "yes"}]}}},
            ]}}
            choices = enumerate_choices(presentation, acts, ws.registry)
            self.assertEqual(len(choices), 1)
            [entry] = list(choices.values())
            self.assertEqual(entry["finding_id"], finding_id)
            forms = {f["lender"] for f in entry["forms"]}
            self.assertEqual(forms, {"Cedar Servicing", "Birch Servicing"})

    def test_two_distinct_borrowings_stay_two_choices(self) -> None:
        ws = T4.Workspace()
        with ws.raw:
            ws.plain()  # autumn/autumn/cedar
            ws.link("financing", "spring", "spring")
            ws.link("statement-inclusion", "spring", "birch")
            ws.answer("loan", "spring", "yes")
            ws.answer("enroll", "spring", "yes")
            acts = ws.acts()
            autumn_id = ws.current_finding(T4.LOAN, (("borrowing", ws.borrowing["autumn"]),))
            spring_id = ws.current_finding(T4.LOAN, (("borrowing", ws.borrowing["spring"]),))
            presentation = {"line21Explanation": {"rows": [
                {"statementLabel": {"lender": "Cedar Servicing"},
                 "basis": {"answers": [{"findingId": autumn_id, "factType": T4.LOAN, "response": "yes"}]}},
                {"statementLabel": {"lender": "Birch Servicing"},
                 "basis": {"answers": [{"findingId": spring_id, "factType": T4.LOAN, "response": "yes"}]}},
            ]}}
            choices = enumerate_choices(presentation, acts, ws.registry)
            self.assertEqual(set(choices), {autumn_id, spring_id})

    def test_empty_presentation_yields_no_choices(self) -> None:
        ws = T4.Workspace()
        with ws.raw:
            acts = ws.acts()
        choices = enumerate_choices({"line21Explanation": {"rows": []}}, acts, ws.registry)
        self.assertEqual(choices, {})


class ResolveOutcomes(unittest.TestCase):
    """The resolver's four outcomes: current, superseded, no-target, not-a-target."""

    def test_current(self) -> None:
        ws = T4.Workspace()
        with ws.raw:
            ws.plain()
            acts = ws.acts()
            answer_id = ws.current_finding(T4.LOAN, (("borrowing", ws.borrowing["autumn"]),))
            result = resolve_displayed_answer_to_target(acts, ws.registry, answer_id)
            self.assertEqual(result["status"], "current")
            self.assertEqual(result["finding_id"], answer_id)
            self.assertEqual(result["borrowing_ref"], ws.borrowing["autumn"])

    def test_superseded_names_the_current_one(self) -> None:
        ws = T4.Workspace()
        with ws.raw:
            ws.plain()
            answer_id = ws.current_finding(T4.LOAN, (("borrowing", ws.borrowing["autumn"]),))
            review = review_mod.prepare_borrowing_answer_review(
                ws.log, ws.registry, review_id="demo.test.review.superseded",
                shown_at="2026-10-09T00:00:00Z", borrowing_refs=(ws.borrowing["autumn"],))
            corrected = review_mod.correct_borrowing_answer_review(
                ws.log, ws.registry, review, finding_id=answer_id, borrowing_ref=ws.borrowing["autumn"],
                question="loan-paid-only-school-costs", response="no", actor=T4.USER,
                at="2026-10-09T00:00:01Z", submission_id="demo.test.submission.superseded",
                evidence_id="demo.evidence.test.superseded")
            acts = ws.acts()
            result = resolve_displayed_answer_to_target(acts, ws.registry, answer_id)
            self.assertEqual(result["status"], "superseded")
            self.assertEqual(result["current_finding_id"], corrected["finding_id"])
            self.assertNotEqual(result["current_finding_id"], answer_id)

    def test_no_target_after_withdrawal(self) -> None:
        ws = T4.Workspace()
        with ws.raw:
            ws.plain()
            answer_id = ws.current_finding(T4.LOAN, (("borrowing", ws.borrowing["autumn"]),))
            review_mod.withdraw_borrowing_answer_review(
                ws.log, ws.registry, finding_id=answer_id, actor=T4.USER, at="2026-10-09T00:00:02Z")
            acts = ws.acts()
            result = resolve_displayed_answer_to_target(acts, ws.registry, answer_id)
            self.assertEqual(result["status"], "no-target")

    def test_box_witness_is_not_a_target(self) -> None:
        ws = T4.Workspace()
        with ws.raw:
            ws.plain()
            box1_id = ws.current_finding(T4.BOX1, ws.statement_keys["cedar"])
            acts = ws.acts()
            result = resolve_displayed_answer_to_target(acts, ws.registry, box1_id)
            self.assertEqual(result["status"], "not-a-target")


class Cancel(unittest.TestCase):
    def test_cancel_leaves_log_revision_unchanged(self) -> None:
        ws = T4.Workspace()
        with ws.raw:
            ws.plain()
            before_revision = ws.log.read().revision
            review_mod.prepare_borrowing_answer_review(
                ws.log, ws.registry, review_id="demo.test.review.cancel",
                shown_at="2026-10-09T00:00:00Z", borrowing_refs=(ws.borrowing["autumn"],))
            after_revision = ws.log.read().revision
            self.assertEqual(before_revision, after_revision)


class SurfaceArtifact(unittest.TestCase):
    def test_resolves_and_serves_bytes_equal_to_manifest_entry(self) -> None:
        resolved = resolve_correction_surface(REPO)
        self.assertEqual(resolved.entry_count, 1)
        with TemporaryDirectory(prefix="sli-correction-surface-") as tmp:
            capability = WorkspaceCapability(Path(tmp) / "L")
            dist = build_correction_surface(capability, repo_root=REPO)
            entrypoint = dist / resolved.manifest["entrypoint_html"]
            self.assertTrue(entrypoint.is_file())
            self.assertEqual(
                entrypoint.read_bytes(),
                (resolved.content_dir / resolved.manifest["entrypoint_html"]).read_bytes())


class _StubRuntime:
    """Just enough of ``CorrectionRuntime`` to drive the HTTP admission path
    without the cost of a full workspace and live run."""

    def state(self) -> dict[str, Any]:
        return {"saved_run_id": "demo.stub", "line21_rows": [], "choices": {}}

    def choose(self, finding_id: str) -> dict[str, Any]:
        return {"status": "not-a-target", "reason": "stub"}

    def confirm(self, token: str, response: str) -> dict[str, Any]:
        from packages.derivation.correction_session import CorrectionSessionError
        raise CorrectionSessionError("correction-unknown-token")

    def cancel(self, token: str) -> dict[str, Any]:
        return {"outcome": "cancelled"}


class Admission(unittest.TestCase):
    def test_malformed_and_unknown_token_refused_without_echo(self) -> None:
        with TemporaryDirectory(prefix="sli-correction-admission-") as tmp:
            static_root = Path(tmp)
            (static_root / "index.html").write_text("<!doctype html><title>stub</title>", encoding="utf-8")
            with CorrectionSessionServer(_StubRuntime(), static_root) as server:
                root = server.url.rsplit("/", 1)[0]

                # Malformed JSON body.
                request = urllib.request.Request(
                    f"{root}/api/choose", data=b"not json",
                    headers={"Content-Type": "application/json"}, method="POST")
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    urllib.request.urlopen(request, timeout=10)
                self.assertEqual(caught.exception.code, 400)
                body = json.loads(caught.exception.read())
                self.assertNotIn("not json", json.dumps(body))

                # Unexpected extra key.
                request = urllib.request.Request(
                    f"{root}/api/choose",
                    data=json.dumps({"finding_id": "x", "extra": "y"}).encode("utf-8"),
                    headers={"Content-Type": "application/json"}, method="POST")
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    urllib.request.urlopen(request, timeout=10)
                self.assertEqual(caught.exception.code, 422)

                # Unknown token on confirm.
                request = urllib.request.Request(
                    f"{root}/api/confirm",
                    data=json.dumps({"token": "nope", "response": "no"}).encode("utf-8"),
                    headers={"Content-Type": "application/json"}, method="POST")
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    urllib.request.urlopen(request, timeout=10)
                self.assertEqual(caught.exception.code, 422)
                body = json.loads(caught.exception.read())
                self.assertNotIn("nope", json.dumps(body))


class Neighbor(unittest.TestCase):
    """``prepare_review``'s cards are unchanged."""

    def test_prepare_review_cards_still_carry_no_clues(self) -> None:
        ws = T4.Workspace()
        with ws.raw:
            ws.plain()
            review = review_mod.prepare_review(
                ws.log, ws.registry, review_id="demo.test.review.neighbor",
                shown_at="2026-10-09T00:00:00Z", borrowing_refs=tuple(ws.borrowing.values()),
                schooling_fact_ids=tuple(ws.school.values()), statement_fact_ids=tuple(ws.statement.values()))
            for card in review["borrowing_choices"]:
                self.assertEqual(card["recognition_clues"], [])


# ---------------------------------------------------------------------------
# Track 1 repair, defect 1: distinguishability across the relevant choices.
#
# ``CorrectionRuntime.choose`` prepares a review of the selected borrowing
# only (``borrowing_refs=(borrowing_ref,)``); the safeguard that compares a
# review's own ``borrowing_choices`` to each other then has nothing to
# compare against. The rule must live in the borrowing-answer review path in
# ``sli_relationship_review.py`` itself, checked against every current
# borrowing in the workspace, not merely the ones a caller chose to show.
# ---------------------------------------------------------------------------


class Repair1Distinguishability(unittest.TestCase):
    def test_choose_then_confirm_refuses_an_indistinguishable_pair(self) -> None:
        base_acts = load_seed_acts(REPO)
        schemas = DerivationSchemas()
        registry = install_domain_scoped_supersession(schemas.registry)
        with TemporaryDirectory(prefix="sli-correction-twin-seed-") as tmp:
            log = ActLog(Path(tmp) / "L", registry)
            for expected, row in enumerate(base_acts):
                log.append(dict(row), expected_revision=expected)
            introduce_borrowing_reference_durably(
                log, registry, reference_id="demo.correction.test.willow",
                description="Willow study loan", actor=SCOPE_USER, at="2026-10-09T00:00:00Z")
            review = review_mod.prepare_borrowing_answer_review(
                log, registry, review_id="demo.correction.test.willow.review",
                shown_at="2026-10-09T00:00:01Z", borrowing_refs=("demo.correction.test.willow",))
            saved = review_mod.save_borrowing_answer_review(
                log, registry, review, borrowing_ref="demo.correction.test.willow",
                question="loan-paid-only-school-costs", response="yes", actor=SCOPE_USER,
                at="2026-10-09T00:00:02Z", submission_id="demo.correction.test.willow.submission",
                evidence_id="demo.evidence.correction.test.willow")
            willow_finding_id = saved["finding_id"]
            # A second, unrelated borrowing with an identical label and no
            # relationships of its own -- identical to willow's own (empty)
            # clue set, and only ever introduced, never referenced by caller
            # input to ``choose``.
            introduce_borrowing_reference_durably(
                log, registry, reference_id="demo.correction.test.willow-twin",
                description="Willow study loan", actor=SCOPE_USER, at="2026-10-09T00:00:03Z")
            seed_acts = list(log.read().acts)

        with TemporaryDirectory(prefix="sli-correction-saved-") as saved_dir, \
                TemporaryDirectory(prefix="sli-correction-session-") as session_dir:
            presentation_path = Path(saved_dir) / "presentation.json"
            presentation_path.write_text(
                json.dumps({"line21Explanation": {"rows": []}}), encoding="utf-8")
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO,
                surface=core_calculations_surface(REPO), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=presentation_path,
                saved_run_id="demo.correction.test.willow-run", seed_acts=seed_acts,
            )
            before_revision = runtime._log.read().revision

            chosen = runtime.choose(willow_finding_id)
            if chosen.get("status") == "current":
                # Today's bug: choose narrowed the review to one card, so
                # nothing refuses the confirm either.
                result = runtime.confirm(chosen["token"], "no")
                self.assertNotEqual(result.get("outcome"), "saved-and-calculated")
                self.assertNotEqual(result.get("outcome"), "saved-not-calculated")

            after_revision = runtime._log.read().revision
            self.assertEqual(before_revision, after_revision)


def _twin_borrowing_seed_acts(label_a: str, label_b: str) -> tuple[list[dict[str, Any]], str]:
    """Two otherwise-identical (no relationships) borrowings, one with a
    saved loan-cost answer, seeded on top of the committed correction
    fixture. Returns the seed acts and the answered borrowing's findingId."""
    base_acts = load_seed_acts(REPO)
    schemas = DerivationSchemas()
    registry = install_domain_scoped_supersession(schemas.registry)
    with TemporaryDirectory(prefix="sli-correction-label-seed-") as tmp:
        log = ActLog(Path(tmp) / "L", registry)
        for expected, row in enumerate(base_acts):
            log.append(dict(row), expected_revision=expected)
        introduce_borrowing_reference_durably(
            log, registry, reference_id="demo.correction.test.sprout-a",
            description=label_a, actor=SCOPE_USER, at="2026-10-09T00:00:00Z")
        review = review_mod.prepare_borrowing_answer_review(
            log, registry, review_id="demo.correction.test.sprout-a.review",
            shown_at="2026-10-09T00:00:01Z", borrowing_refs=("demo.correction.test.sprout-a",))
        saved = review_mod.save_borrowing_answer_review(
            log, registry, review, borrowing_ref="demo.correction.test.sprout-a",
            question="loan-paid-only-school-costs", response="yes", actor=SCOPE_USER,
            at="2026-10-09T00:00:02Z", submission_id="demo.correction.test.sprout-a.submission",
            evidence_id="demo.evidence.correction.test.sprout-a")
        finding_id = str(saved["finding_id"])
        introduce_borrowing_reference_durably(
            log, registry, reference_id="demo.correction.test.sprout-b",
            description=label_b, actor=SCOPE_USER, at="2026-10-09T00:00:03Z")
        return list(log.read().acts), finding_id


class Correction1LabelsAsDisplayed(unittest.TestCase):
    """R3 finding 1: distinguishability must compare labels the way the
    page renders them -- whitespace runs collapsed, ends trimmed -- not as
    raw stored strings. Case stays significant."""

    def test_whitespace_only_label_difference_refuses(self) -> None:
        seed_acts, finding_id = _twin_borrowing_seed_acts(
            "Sprout study loan", "Sprout  study loan")
        with TemporaryDirectory(prefix="sli-correction-saved-") as saved_dir, \
                TemporaryDirectory(prefix="sli-correction-session-") as session_dir:
            presentation_path = Path(saved_dir) / "presentation.json"
            presentation_path.write_text(
                json.dumps({"line21Explanation": {"rows": []}}), encoding="utf-8")
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO,
                surface=core_calculations_surface(REPO), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=presentation_path,
                saved_run_id="demo.correction.test.whitespace-run", seed_acts=seed_acts,
            )
            before_revision = runtime._log.read().revision

            chosen = runtime.choose(finding_id)
            self.assertEqual(chosen.get("status"), "indistinguishable")

            after_revision = runtime._log.read().revision
            self.assertEqual(before_revision, after_revision)

    def test_case_difference_alone_stays_distinguishable(self) -> None:
        # Case is a genuine difference, not a display artifact: two labels
        # differing only in case must remain two distinguishable choices.
        seed_acts, finding_id = _twin_borrowing_seed_acts(
            "Sprout study loan", "sprout study loan")
        with TemporaryDirectory(prefix="sli-correction-saved-") as saved_dir, \
                TemporaryDirectory(prefix="sli-correction-session-") as session_dir:
            presentation_path = Path(saved_dir) / "presentation.json"
            presentation_path.write_text(
                json.dumps({"line21Explanation": {"rows": []}}), encoding="utf-8")
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO,
                surface=core_calculations_surface(REPO), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=presentation_path,
                saved_run_id="demo.correction.test.case-run", seed_acts=seed_acts,
            )
            chosen = runtime.choose(finding_id)
            self.assertEqual(chosen.get("status"), "current")


# ---------------------------------------------------------------------------
# Track 1 repair, defect 2: relationship meaning in clues.
#
# The production formatter rendered every financing outcome (affirmed,
# denied, withdrawn, unresolved) as "financed ...". Because the prepared
# and refreshed clue text was therefore equal, withdrawing the financing
# relationship after prepare saved: the as-shown revalidation had nothing
# visibly different to catch.
# ---------------------------------------------------------------------------


class Repair2RelationshipMeaning(unittest.TestCase):
    def test_financing_withdrawal_after_prepare_is_not_saved(self) -> None:
        acts, saved_outcome = _shared_saved_run()
        surface = core_calculations_surface(REPO)
        with TemporaryDirectory(prefix="sli-correction-session-") as session_dir:
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO, surface=surface,
                run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=saved_outcome.presentation_path,
                saved_run_id="demo.correction.test.shared", seed_acts=acts,
            )
            state = runtime.state()
            [cedar] = [c for c in state["choices"].values()
                      if any(f.get("statement", "").startswith("2025 Form 1098-E from Cedar")
                             for f in c["forms"])]
            chosen = runtime.choose(cedar["finding_id"])
            self.assertEqual(chosen["status"], "current")
            token = chosen["token"]
            self.assertIn("financed", " ".join(chosen["confirmation"]["recognition_clues"]))

            # Withdraw the financing relationship the prepared card's clue
            # showed as affirmed.
            financing_fact_id = fact_id_for(T4.FIN, (
                ("borrowing", cedar["borrowing_ref"]),
                ("period", "demo.track5.period.autumn24"),
                ("institution", "demo.track5.institution.river"),
                ("programme", "demo.track5.programme.bsc"),
            ))
            financing_finding_id = str(track17._current_source_finding(
                runtime._log.read().acts, runtime.registry, financing_fact_id)["id"])
            review_mod.withdraw_review_claim(
                runtime._log, runtime.registry, finding_id=financing_finding_id,
                actor=SCOPE_USER, at="2026-10-09T00:00:05Z")

            result = runtime.confirm(token, "no")
            self.assertEqual(result.get("outcome"), "not-saved")


# ---------------------------------------------------------------------------
# Track 1 corrections, correction 2 (R3 finding 3): defect 2's committed
# matrix. R3 found exactly one committed case (financing affirmed ->
# withdrawn, above) for what the charter asked to cover in full: every
# inclusion and financing outcome's fresh display, a stale confirmation
# after an outcome change for both relationship kinds, and the saved
# evidence's ``choices_shown`` carrying the plain-word outcome. These cases
# use a one-borrowing, one-relationship seed (not the full correction_t1
# fixture), since none of them reach recalculation: a fresh display never
# saves, and a stale confirmation is refused by the review API's own
# revalidation before the recorder is ever called.
# ---------------------------------------------------------------------------

_INCLUSION_PHRASES = {
    "affirmed": "included", "denied": "not included",
    "withdrawn": "inclusion withdrawn", "unresolved": "inclusion not yet known",
}
_FINANCING_PHRASES = {
    "affirmed": "financed", "denied": "did not finance",
    "withdrawn": "financing withdrawn for", "unresolved": "financing not yet known for",
}
_OUTCOME_RESPONSE = {"denied": "no", "unresolved": "cannot-tell"}  # "withdrawn" is a withdraw, not an answer


def _one_relationship_workspace(kind: str, outcome_name: str) -> dict[str, Any]:
    """One borrowing ('autumn'), one ``kind`` relationship at ``outcome_name``
    (affirmed/denied/withdrawn/unresolved), and a loan-cost 'yes' answer --
    enough for ``choose()`` to resolve a target and show a fresh card, and
    enough identity to mutate the same relationship later against the same
    log a ``CorrectionRuntime`` is built from."""
    ws = T4.Workspace()
    with ws.raw:
        target = "autumn" if kind == "financing" else "cedar"
        ws.link(kind, "autumn", target)
        if outcome_name != "affirmed":
            response = "withdrawn" if outcome_name == "withdrawn" else _OUTCOME_RESPONSE[outcome_name]
            ws.outcome(kind, "autumn", target, response)
        ws.answer("loan", "autumn", "yes")
        loan_finding_id = ws.current_finding(T4.LOAN, (("borrowing", ws.borrowing["autumn"]),))
        return {
            "acts": ws.acts(), "borrowing_ref": ws.borrowing["autumn"],
            "schooling_fact_id": ws.school["autumn"], "statement_fact_id": ws.statement["cedar"],
            "loan_finding_id": loan_finding_id,
        }


def _affirmed_relationship_workspace(kind: str) -> dict[str, Any]:
    """Like ``_one_relationship_workspace``, affirmed, plus the relationship
    claim's own findingId so a later test can change its outcome in place."""
    ws = T4.Workspace()
    with ws.raw:
        target = "autumn" if kind == "financing" else "cedar"
        ws.link(kind, "autumn", target)
        ws.answer("loan", "autumn", "yes")
        loan_finding_id = ws.current_finding(T4.LOAN, (("borrowing", ws.borrowing["autumn"]),))
        return {
            "acts": ws.acts(), "borrowing_ref": ws.borrowing["autumn"],
            "schooling_fact_id": ws.school["autumn"], "statement_fact_id": ws.statement["cedar"],
            "loan_finding_id": loan_finding_id, "claim_finding_id": ws.claims[(kind, "autumn", target)],
        }


def _empty_presentation_runtime(seed: dict[str, Any], *, run_label: str) -> tuple[Any, Any, Any]:
    """A ``CorrectionRuntime`` over ``seed['acts']`` with an empty saved
    presentation. The state/choose/confirm cases exercised here never read
    the saved presentation's rows, so an empty one keeps the case bounded
    to the backend under test. Returns the runtime and its two temp-dir
    context managers, which the caller must keep open for the runtime's life."""
    saved_dir = TemporaryDirectory(prefix="sli-correction-matrix-saved-")
    session_dir = TemporaryDirectory(prefix="sli-correction-matrix-session-")
    presentation_path = Path(saved_dir.name) / "presentation.json"
    presentation_path.write_text(json.dumps({"line21Explanation": {"rows": []}}), encoding="utf-8")
    runtime = CorrectionRuntime(
        WorkspaceCapability(Path(session_dir.name) / "L"), repo_root=REPO,
        surface=core_calculations_surface(REPO), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
        saved_presentation_path=presentation_path, saved_run_id=run_label, seed_acts=seed["acts"],
    )
    return runtime, saved_dir, session_dir


def _mutate_relationship_outcome(runtime: Any, *, kind: str, seed: dict[str, Any],
                                 new_outcome: str, serial: int) -> None:
    """Change the one relationship ``seed`` carries to ``new_outcome``,
    against the same log and registry the runtime already holds a held
    review against."""
    finding_id = seed["claim_finding_id"]
    if new_outcome == "withdrawn":
        review_mod.withdraw_review_claim(
            runtime._log, runtime.registry, finding_id=finding_id, actor=SCOPE_USER,
            at=f"2026-10-09T00:10:{serial:02d}Z")
        return
    response = _OUTCOME_RESPONSE[new_outcome]
    financing = kind == "financing"
    review = review_mod.prepare_review(
        runtime._log, runtime.registry, review_id=f"demo.correction.test.matrix.review.{serial}",
        shown_at=f"2026-10-09T00:11:{serial:02d}Z", borrowing_refs=(seed["borrowing_ref"],),
        schooling_fact_ids=(seed["schooling_fact_id"],) if financing else (),
        statement_fact_ids=(seed["statement_fact_id"],) if not financing else ())
    review_mod.answer_review_claim(
        runtime._log, runtime.registry, finding_id=finding_id, review=review,
        borrowing_ref=seed["borrowing_ref"],
        schooling_fact_id=seed["schooling_fact_id"] if financing else None,
        statement_fact_id=seed["statement_fact_id"] if not financing else None,
        financing_response=response if financing else "unanswered",
        inclusion_response=response if not financing else "unanswered",
        actor=SCOPE_USER, at=f"2026-10-09T00:12:{serial:02d}Z",
        submission_id=f"demo.correction.test.matrix.submission.{serial}",
        evidence_id=f"demo.evidence.correction.test.matrix.{serial}")


class Correction2FreshDisplay(unittest.TestCase):
    """Fresh display of every inclusion outcome and every financing outcome."""

    def test_every_outcome_shows_its_own_plain_word_phrase(self) -> None:
        cases = ([("statement-inclusion", name, phrase) for name, phrase in _INCLUSION_PHRASES.items()]
                 + [("financing", name, phrase) for name, phrase in _FINANCING_PHRASES.items()])
        for kind, outcome_name, phrase in cases:
            with self.subTest(kind=kind, outcome=outcome_name):
                seed = _one_relationship_workspace(kind, outcome_name)
                runtime, saved_dir, session_dir = _empty_presentation_runtime(
                    seed, run_label="demo.correction.test.fresh-display")
                with saved_dir, session_dir:
                    chosen = runtime.choose(seed["loan_finding_id"])
                    self.assertEqual(chosen.get("status"), "current")
                    clues = " ".join(chosen["confirmation"]["recognition_clues"])
                    self.assertIn(phrase, clues)


class Correction2StaleConfirmation(unittest.TestCase):
    """A stale confirmation after an outcome change, for inclusion and for
    financing, gives not-saved with the log revision unchanged."""

    def test_outcome_change_after_prepare_refuses_without_writing(self) -> None:
        cases = [(kind, outcome) for kind in ("statement-inclusion", "financing")
                 for outcome in ("denied", "unresolved", "withdrawn")]
        for serial, (kind, new_outcome) in enumerate(cases):
            with self.subTest(kind=kind, new_outcome=new_outcome):
                seed = _affirmed_relationship_workspace(kind)
                runtime, saved_dir, session_dir = _empty_presentation_runtime(
                    seed, run_label="demo.correction.test.stale-matrix")
                with saved_dir, session_dir:
                    chosen = runtime.choose(seed["loan_finding_id"])
                    self.assertEqual(chosen.get("status"), "current")
                    token = chosen["token"]

                    _mutate_relationship_outcome(runtime, kind=kind, seed=seed,
                                                 new_outcome=new_outcome, serial=serial)
                    revision_before_confirm = runtime._log.read().revision

                    result = runtime.confirm(token, "no")
                    self.assertEqual(result.get("outcome"), "not-saved")

                    revision_after_confirm = runtime._log.read().revision
                    self.assertEqual(revision_before_confirm, revision_after_confirm)


class Correction2SavedEvidenceCarriesOutcome(unittest.TestCase):
    """The saved evidence's ``choices_shown`` carries the plain-word outcome,
    for both relationship kinds."""

    def test_saved_choices_shown_carries_the_outcome_phrase(self) -> None:
        for kind, phrase in (("statement-inclusion", "included"), ("financing", "financed")):
            with self.subTest(kind=kind):
                seed = _one_relationship_workspace(kind, "affirmed")
                runtime, saved_dir, session_dir = _empty_presentation_runtime(
                    seed, run_label="demo.correction.test.evidence-matrix")
                with saved_dir, session_dir:
                    chosen = runtime.choose(seed["loan_finding_id"])
                    self.assertEqual(chosen.get("status"), "current")
                    result = runtime.confirm(chosen["token"], "no")
                    self.assertEqual(result.get("outcome"), "saved-not-calculated")

                    acts = runtime._log.read().acts
                    evidence_act = next(a for a in reversed(acts) if a.get("kind") == "evidence-submitted")
                    content = evidence_act["payload"]["evidence"]["content"]
                    [card] = content["recognition_context"]["choices_shown"]["borrowing_choices"]
                    self.assertIn(phrase, " ".join(card["recognition_clues"]))


# ---------------------------------------------------------------------------
# Track 1 corrections, correction 1 (R4 finding 4): redacted refusal.
#
# A ``RelationshipRecordingRefused`` carries the runtime's own internal
# wording -- sometimes an f-string over a terminal record. No exception
# text, act id, record, finding id, or demo identifier may ever reach a
# refusal response; ``choose``/``confirm`` classify the refusal and report
# one of a small, declared set of sentences instead.
# ---------------------------------------------------------------------------


class Correction1RedactedRefusal(unittest.TestCase):
    def test_indistinguishable_choice_is_redacted(self) -> None:
        seed_acts, finding_id = _twin_borrowing_seed_acts(
            "Sprout study loan", "Sprout study loan")
        with TemporaryDirectory(prefix="sli-correction-saved-") as saved_dir, \
                TemporaryDirectory(prefix="sli-correction-session-") as session_dir:
            presentation_path = Path(saved_dir) / "presentation.json"
            presentation_path.write_text(
                json.dumps({"line21Explanation": {"rows": []}}), encoding="utf-8")
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO,
                surface=core_calculations_surface(REPO), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=presentation_path,
                saved_run_id="demo.correction.test.redact-indistinguishable", seed_acts=seed_acts,
            )
            chosen = runtime.choose(finding_id)
            self.assertEqual(chosen.get("status"), "indistinguishable")
            self.assertEqual(
                chosen.get("reason"), correction_session_mod._REFUSAL_INDISTINGUISHABLE)
            _assert_redacted(self, chosen.get("reason"))

    def test_stale_confirmation_refusal_is_redacted(self) -> None:
        acts, saved_outcome = _shared_saved_run()
        surface = core_calculations_surface(REPO)
        with TemporaryDirectory(prefix="sli-correction-session-") as session_dir:
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO, surface=surface,
                run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=saved_outcome.presentation_path,
                saved_run_id="demo.correction.test.redact-stale", seed_acts=acts,
            )
            state = runtime.state()
            [cedar] = [c for c in state["choices"].values()
                      if any(f.get("statement", "").startswith("2025 Form 1098-E from Cedar")
                             for f in c["forms"])]
            chosen = runtime.choose(cedar["finding_id"])
            self.assertEqual(chosen["status"], "current")
            token = chosen["token"]

            financing_fact_id = fact_id_for(T4.FIN, (
                ("borrowing", cedar["borrowing_ref"]),
                ("period", "demo.track5.period.autumn24"),
                ("institution", "demo.track5.institution.river"),
                ("programme", "demo.track5.programme.bsc"),
            ))
            financing_finding_id = str(track17._current_source_finding(
                runtime._log.read().acts, runtime.registry, financing_fact_id)["id"])
            review_mod.withdraw_review_claim(
                runtime._log, runtime.registry, finding_id=financing_finding_id,
                actor=SCOPE_USER, at="2026-10-09T00:00:07Z")

            result = runtime.confirm(token, "no")
            self.assertEqual(result.get("outcome"), "not-saved")
            self.assertEqual(result.get("reason"), correction_session_mod._REFUSAL_SHOWN_CHANGED)
            _assert_redacted(self, result.get("reason"))

    def test_forced_admission_refusal_is_redacted(self) -> None:
        """A forced admission refusal: the recorder's own terminal record
        can carry act, finding and contribution identities
        (``sli_relationship_recording.py``'s last guard before the save).
        ``apply_contribution_batch`` never returns a non-completed phase in
        practice (an admission failure raises instead), so this forces the
        guard directly to prove the redaction holds even then."""
        seed = _one_relationship_workspace("statement-inclusion", "affirmed")
        runtime, saved_dir, session_dir = _empty_presentation_runtime(
            seed, run_label="demo.correction.test.redact-admission")
        with saved_dir, session_dir:
            chosen = runtime.choose(seed["loan_finding_id"])
            self.assertEqual(chosen.get("status"), "current")
            token = chosen["token"]

            fake_terminal = {
                "schema": "contribution-record.v1", "record_id": "sli.borrowing-answer.record.forced",
                "contribution_id": "sli.borrowing-answer.contribution.forced", "phase": "failed",
                "workspace_revision": 0, "stop_reason": "validation-failed", "facts_asserted": [],
            }
            fake_admission = ContributionBatchResult(
                state=cast(Any, None), started_record={}, terminal_record=fake_terminal)
            with mock.patch(
                "packages.tax.sli_relationship_recording.apply_contribution_batch",
                return_value=fake_admission,
            ):
                result = runtime.confirm(token, "no")
            self.assertEqual(result.get("outcome"), "not-saved")
            self.assertEqual(result.get("reason"), correction_session_mod._REFUSAL_OTHER)
            _assert_redacted(self, result.get("reason"))


# ---------------------------------------------------------------------------
# Track 1 repair, defect 3: honest outcomes when confirmation fails.
#
# Everything after the durable save must report saved-not-calculated, with
# the predecessor and successor ids; none of these may ever report
# not-saved. A token is consumed at save; a second confirm on the same
# token returns the recorded outcome, never a second save.
# ---------------------------------------------------------------------------


class Repair3HonestOutcomes(unittest.TestCase):
    def _runtime_with_token(self) -> tuple[Any, str, dict[str, Any]]:
        acts, saved_outcome = _shared_saved_run()
        surface = core_calculations_surface(REPO)
        session_dir = TemporaryDirectory(prefix="sli-correction-session-")
        self.addCleanup(session_dir.cleanup)
        runtime = CorrectionRuntime(
            WorkspaceCapability(Path(session_dir.name) / "L"), repo_root=REPO, surface=surface,
            run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
            saved_presentation_path=saved_outcome.presentation_path,
            saved_run_id="demo.correction.test.shared", seed_acts=acts,
        )
        state = runtime.state()
        [cedar] = [c for c in state["choices"].values()
                  if any(f.get("statement", "").startswith("2025 Form 1098-E from Cedar")
                         for f in c["forms"])]
        chosen = runtime.choose(cedar["finding_id"])
        self.assertEqual(chosen["status"], "current")
        return runtime, chosen["token"], cedar

    def test_calculation_refusal_reports_saved_not_calculated(self) -> None:
        runtime, token, _cedar = self._runtime_with_token()
        refusal = Refusal(reason="demo-refusal", detail="synthetic")
        fake = LiveCoordinatorOutcome(refusal=refusal, output_path=None, run_id="demo", presentation_path=None)
        with mock.patch.object(correction_session_mod, "live_coordinate_run", return_value=fake):
            result = runtime.confirm(token, "no")
        self.assertEqual(result.get("outcome"), "saved-not-calculated")
        self.assertIsNotNone(result.get("predecessor_finding_id"))
        self.assertIsNotNone(result.get("successor_finding_id"))

    def test_exception_in_live_coordinate_run_reports_saved_not_calculated(self) -> None:
        runtime, token, _cedar = self._runtime_with_token()
        with mock.patch.object(correction_session_mod, "live_coordinate_run",
                               side_effect=RuntimeError("synthetic recalculation failure")):
            result = runtime.confirm(token, "no")
        self.assertEqual(result.get("outcome"), "saved-not-calculated")
        self.assertNotEqual(result.get("outcome"), "not-saved")
        self.assertIsNotNone(result.get("predecessor_finding_id"))
        self.assertIsNotNone(result.get("successor_finding_id"))

    def test_presentation_read_failure_reports_saved_not_calculated(self) -> None:
        runtime, token, _cedar = self._runtime_with_token()
        bad_path = Path(runtime._repo_root) / "does-not-exist" / "presentation.json"
        fake = LiveCoordinatorOutcome(
            refusal=None, output_path=bad_path, run_id="demo", presentation_path=bad_path)
        with mock.patch.object(correction_session_mod, "live_coordinate_run", return_value=fake):
            result = runtime.confirm(token, "no")
        self.assertEqual(result.get("outcome"), "saved-not-calculated")
        self.assertNotEqual(result.get("outcome"), "not-saved")

    def test_second_confirm_on_same_token_returns_recorded_outcome(self) -> None:
        runtime, token, _cedar = self._runtime_with_token()
        first = runtime.confirm(token, "no")
        self.assertIn(first.get("outcome"), {"saved-and-calculated", "saved-not-calculated"})
        revision_after_first = runtime._log.read().revision

        second = runtime.confirm(token, "no")
        self.assertEqual(second.get("outcome"), first.get("outcome"))
        self.assertEqual(second.get("predecessor_finding_id"), first.get("predecessor_finding_id"))
        self.assertEqual(second.get("successor_finding_id"), first.get("successor_finding_id"))
        self.assertTrue(second.get("already_used"))

        revision_after_second = runtime._log.read().revision
        self.assertEqual(revision_after_first, revision_after_second)


# ---------------------------------------------------------------------------
# Track 1 corrections, correction 4 (R4 finding 7): one shared D1 run.
#
# D1 (``tests.test_sli_track2_repair._d1_populate``) is the Foreman's exact
# attribution gap: Cedar carries both Autumn (affirmed) and Spring (whose
# *inclusion* on Cedar is denied), so Cedar's own row already displays
# answers from two different borrowings side by side. Built once per test
# *process*, the same lock-guarded, lazily-built pattern ``_shared_saved_run``
# already established for the simple two-form fixture -- R4 found this D1
# run alone cost nearly as much as that fixture's entire prior module time,
# built fresh by a single test that never reused it.
# ---------------------------------------------------------------------------

_SHARED_D1_SAVED_RUN_LOCK = threading.Lock()
_shared_d1_saved_run_cache: dict[str, Any] = {}


def _d1_capture_full(ws: Any) -> dict[str, Any]:
    """``T2R._d1_capture``'s three ids, plus every other identity the
    correction-2 and correction-4 tests need, captured once while the D1
    act log is still live."""
    import tests.test_sli_track2_repair as T2R

    captured: dict[str, Any] = dict(T2R._d1_capture(ws))
    captured["autumn_ref"] = ws.borrowing["autumn"]
    captured["spring_loan_id"] = ws.current_finding(T4.LOAN, (("borrowing", ws.borrowing["spring"]),))
    captured["spring_enroll_id"] = ws.current_finding(T4.ENROLL, (("borrowing", ws.borrowing["spring"]),))
    captured["spring_financing_id"] = ws.current_finding(
        T4.FIN, (("borrowing", ws.borrowing["spring"]),) + T5.Return.SCHOOL_KEYS["spring"])
    captured["autumn_inclusion_id"] = ws.current_finding(
        T4.INCL, ws.statement_keys["cedar"] + (("borrowing", ws.borrowing["autumn"]),))
    return captured


def _shared_d1_saved_run() -> tuple[Any, dict[str, Any], Any]:
    """D1's initial saved run, shared by every test that only reads it."""
    with _SHARED_D1_SAVED_RUN_LOCK:
        if "outcome" not in _shared_d1_saved_run_cache:
            import tests.test_sli_track2_repair as T2R

            work_dir = TemporaryDirectory(prefix="sli-correction-shared-d1-")
            atexit.register(work_dir.cleanup)
            ws = T5.Return(wages=50000, amounts=T1.STANDARD)
            with ws.raw:
                T2R._d1_populate(ws)
                captured = _d1_capture_full(ws)
                T1.adopt_v42(ws)
                acts = ws.acts()
            outcome = _run_saved(Path(work_dir.name), acts, "demo.correction.test.d1")
            _shared_d1_saved_run_cache["acts"] = acts
            _shared_d1_saved_run_cache["captured"] = captured
            _shared_d1_saved_run_cache["outcome"] = outcome
        return (_shared_d1_saved_run_cache["acts"], _shared_d1_saved_run_cache["captured"],
                _shared_d1_saved_run_cache["outcome"])


class Correction4AttributionByIdentity(unittest.TestCase):
    """The saved model's ``said`` items deliberately omit which borrowing
    each answer belongs to (``presentation_projection._sli_collect_said``'s
    own docstring). The runtime recovers it by identity -- findingId ->
    fact -> keys.borrowing -> that borrowing's current label -- never by
    counting loans on the form, a position, or a sentence."""

    @staticmethod
    def _labels_by_finding_id(items: list[dict[str, Any]]) -> dict[str, Any]:
        return {item["findingId"]: item.get("borrowingLabel") for item in items
                if item.get("factType") in (LOAN_COST_FACT_TYPE, ENROLL_FACT_TYPE)}

    def test_d1_each_answer_carries_its_own_borrowing_before_and_after_correcting_autumn(self) -> None:
        acts, captured, saved_outcome = _shared_d1_saved_run()
        self.assertIsNone(saved_outcome.refusal)
        surface = core_calculations_surface(REPO)

        with TemporaryDirectory(prefix="sli-correction-d1-session-") as session_dir:
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO, surface=surface,
                run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=saved_outcome.presentation_path,
                saved_run_id="demo.correction.test.d1", seed_acts=acts,
            )

            # Before correcting: Cedar's row shows both Spring's and Autumn's
            # loan-cost/enrollment answers (Spring's denied inclusion still
            # leaves its own answers current and displayed, "recorded, not
            # used"). Each must carry its own borrowing's label.
            state = runtime.state()
            cedar_row = next(r for r in state["line21_rows"]
                             if r["statementLabel"]["lender"] == "Cedar Servicing")
            before_labels = self._labels_by_finding_id(cedar_row["account"]["said"]["current"])
            self.assertEqual(before_labels[captured["autumn_loan_id"]], "Autumn study loan")
            self.assertEqual(before_labels[captured["spring_loan_id"]], "Spring study loan")

            # Plan ("account-review-correction"), T0b claim 4: before the
            # correction, Cedar's "recorded, not used" entries name Spring's
            # own denied borrowing -- by finding id, the same identity basis
            # as every other displayed answer, never a count or a label.
            spring_loan_id = captured["spring_loan_id"]
            spring_enroll_id = captured["spring_enroll_id"]
            before_recorded = {item["findingId"] for item in cedar_row["account"]["recordedNotUsed"]}
            self.assertEqual(before_recorded, {spring_loan_id, spring_enroll_id})
            before_recorded_texts = {
                item["findingId"]: item["text"] for item in cedar_row["account"]["recordedNotUsed"]}
            self.assertIn("denied", before_recorded_texts[spring_loan_id])
            self.assertIn("denied", before_recorded_texts[spring_enroll_id])

            autumn_choice = next(c for c in state["choices"].values()
                                if c["borrowing_ref"] == captured["autumn_ref"])
            self.assertEqual(autumn_choice["finding_id"], captured["autumn_loan_id"])

            # Correct Autumn's loan-cost yes -> no.
            chosen = runtime.choose(autumn_choice["finding_id"])
            self.assertEqual(chosen["status"], "current")
            self.assertEqual(chosen["confirmation"]["borrowing_label"], "Autumn study loan")
            result = runtime.confirm(chosen["token"], "no")
            self.assertEqual(result["outcome"], "saved-and-calculated")

            # After correcting: the new current Autumn answer, its displaced
            # predecessor (history), and Spring's untouched answers must each
            # still carry the right borrowing -- including the displaced one.
            after_cedar_row = next(r for r in result["line21_rows"]
                                   if r["statementLabel"]["lender"] == "Cedar Servicing")
            after_said = after_cedar_row["account"]["said"]
            after_current = self._labels_by_finding_id(after_said["current"])
            after_history = self._labels_by_finding_id(after_said["history"])

            successor_id = result["successor_finding_id"]
            predecessor_id = result["predecessor_finding_id"]
            self.assertEqual(predecessor_id, captured["autumn_loan_id"])
            self.assertEqual(after_current[successor_id], "Autumn study loan")
            self.assertEqual(after_history[predecessor_id], "Autumn study loan")

            # Spring's own loan-cost answer is untouched and still
            # correctly attributed, never relabelled as Autumn's.
            self.assertEqual(after_current[spring_loan_id], "Spring study loan")

            # After correcting Autumn directly, Cedar's whole form now
            # contradicts (the newer no beats the older-yes cover) and
            # blocks -- a different "recorded, not used" entry follows from
            # that new model, not the pre-correction one. The row is now
            # named by a reason, and this runtime carries that reason's
            # sentence the same way the earlier (unblocked) rows carry none.
            self.assertEqual(after_cedar_row["status"]["kind"], "named-by-reason")
            self.assertEqual(len(after_cedar_row["reasonSentences"]), 1)
            after_recorded = after_cedar_row["account"]["recordedNotUsed"]
            self.assertEqual(len(after_recorded), 1)
            self.assertEqual(after_recorded[0]["text"], "Recorded, not used. Older yes on this form.")


# ---------------------------------------------------------------------------
# Track 1 corrections, correction 2 (R4 finding 3): relationship answers
# attributed by identity. Financing and statement-inclusion items are keyed
# by ``keys.borrowing`` exactly like loan-cost/enroll, so the same identity
# lookup resolves their displayed label too -- tested on the D1 state
# (reused from the shared fixture above) and on a borrowing shared by two
# forms.
# ---------------------------------------------------------------------------


class Correction2RelationshipAttribution(unittest.TestCase):
    def test_d1_financing_and_inclusion_items_carry_their_borrowing_label(self) -> None:
        acts, captured, saved_outcome = _shared_d1_saved_run()
        surface = core_calculations_surface(REPO)
        with TemporaryDirectory(prefix="sli-correction-d1-session-") as session_dir:
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO, surface=surface,
                run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=saved_outcome.presentation_path,
                saved_run_id="demo.correction.test.d1", seed_acts=acts,
            )
            state = runtime.state()
            cedar_row = next(r for r in state["line21_rows"]
                             if r["statementLabel"]["lender"] == "Cedar Servicing")
            current = cedar_row["account"]["said"]["current"]
            labels = {item["findingId"]: item.get("borrowingLabel") for item in current}

            # Two financing-relationship items (Autumn and Spring, both
            # affirmed) and one statement-inclusion-affirmed/-denied pair
            # (Autumn affirmed, Spring denied) -- R4 finding 3's exact gap.
            self.assertEqual(labels[captured["autumn_financing_id"]], "Autumn study loan")
            self.assertEqual(labels[captured["spring_financing_id"]], "Spring study loan")
            self.assertEqual(labels[captured["autumn_inclusion_id"]], "Autumn study loan")
            self.assertEqual(labels[captured["spring_denial_id"]], "Spring study loan")

    def test_shared_borrowing_across_two_forms_carries_its_label_on_both(self) -> None:
        ws = T4.Workspace()
        with ws.raw:
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.link("statement-inclusion", "autumn", "birch")
            acts = ws.acts()
            cedar_inclusion_id = ws.current_finding(
                T4.INCL, ws.statement_keys["cedar"] + (("borrowing", ws.borrowing["autumn"]),))
            birch_inclusion_id = ws.current_finding(
                T4.INCL, ws.statement_keys["birch"] + (("borrowing", ws.borrowing["autumn"]),))
            registry = ws.registry

        rows = [
            {"account": {"said": {"current": [
                {"findingId": cedar_inclusion_id, "factType": T4.INCL, "response": "yes"}],
                "history": []}}},
            {"account": {"said": {"current": [
                {"findingId": birch_inclusion_id, "factType": T4.INCL, "response": "yes"}],
                "history": []}}},
        ]
        annotated = correction_session_mod._attribute_borrowing_labels(rows, acts, registry)
        for row in annotated:
            [item] = row["account"]["said"]["current"]
            self.assertEqual(item["borrowingLabel"], "Autumn study loan")


# ---------------------------------------------------------------------------
# Visible-interaction evidence, kept separate from the backend and
# transport evidence above. This surface's page is a plain static HTML/JS
# file with a no-op build command (H4), so unlike the W-2 entry loop's
# compiled client this needs no vendored Node tree -- only Node itself and
# a local Chrome/Chromium to drive it.
# ---------------------------------------------------------------------------


class _StaleAfterChooseRuntime(CorrectionRuntime):
    """Test-only (Track 1 corrections, correction 3): after the first
    successful ``choose()`` -- the confirmation already computed and about
    to be returned, correctly reflecting the pre-change state -- withdraw
    the Cedar/Autumn financing relationship the confirmation's own clue
    showed as affirmed, synchronously and server-side, before the HTTP
    response is sent back. The browser sees a correct confirmation; by the
    time it submits confirm(), the workspace has already changed. This
    models "a financing change after the confirmation is shown" without any
    timing coordination with the browser subprocess."""

    _mutated = False
    revision_after_mutation: int | None = None

    def choose(self, finding_id: str) -> dict[str, Any]:
        result = super().choose(finding_id)
        if not self._mutated and result.get("status") == "current":
            self._mutated = True
            borrowing_ref = self.resolve(finding_id)["borrowing_ref"]
            financing_fact_id = fact_id_for(T4.FIN, (
                ("borrowing", borrowing_ref),
                ("period", "demo.track5.period.autumn24"),
                ("institution", "demo.track5.institution.river"),
                ("programme", "demo.track5.programme.bsc"),
            ))
            financing_finding_id = str(track17._current_source_finding(
                self._log.read().acts, self.registry, financing_fact_id)["id"])
            review_mod.withdraw_review_claim(
                self._log, self.registry, finding_id=financing_finding_id,
                actor=SCOPE_USER, at="2026-10-09T00:20:00Z")
            self.revision_after_mutation = self._log.read().revision
        return result


_ORIGINAL_DO_POST = correction_session_mod._CorrectionRequestHandler.do_POST


def _do_post_dropping_first_confirm_response(self: Any) -> None:
    """Test-only (Track 1 corrections, correction 3): let the real
    ``confirm()`` run and durably save server-side, exactly as it would for
    any other request, then drop the TCP connection before any response
    byte is written. This is a genuine transport-level failure -- the
    browser's fetch() call rejects -- not an HTTP error status, and it only
    ever fires for the first ``/api/confirm`` request this handler class
    sees; every other request (including a second confirm, if the page
    were to send one) is served normally."""
    target = self._target()
    if (target is not None and target[1] == "api/confirm"
            and not getattr(self.server, "_confirm_response_dropped", False)):
        self.server._confirm_response_dropped = True
        body = self._read_body()
        if isinstance(body, dict):
            token, response = body.get("token"), body.get("response")
            if isinstance(token, str) and isinstance(response, str):
                try:
                    self.server.runtime.confirm(token, response)
                except correction_session_mod.CorrectionSessionError:
                    pass
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.close_connection = True
        return
    _ORIGINAL_DO_POST(self)


@unittest.skipUnless(_NODE and _BROWSER, "needs Node and a local Chrome/Chromium")
class BrowserIntegration(unittest.TestCase):
    def test_choose_confirm_calculated_shows_before_and_after_explanation(self) -> None:
        assert _NODE is not None
        acts, saved_outcome = _shared_saved_run()
        surface = core_calculations_surface(REPO)
        with TemporaryDirectory(prefix="sli-correction-session-") as session_dir:
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO, surface=surface,
                run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=saved_outcome.presentation_path,
                saved_run_id="demo.correction.test.shared", seed_acts=acts,
            )
            dist = build_correction_surface(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO)
            with CorrectionSessionServer(runtime, dist) as server:
                result = subprocess.run(
                    [_NODE, str(REPO / "tests" / "helpers" / "correction_browser_client.mjs"), server.url],
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, timeout=90, check=False,
                )
            self.assertEqual(result.returncode, 0, result.stderr)
            observed = json.loads(result.stdout)
            self.assertEqual(observed, {
                "complete": True,
                "beforeShowsRecordedAnswer": True,
                "clueShown": True,
                "afterShowsCurrentAndHistory": True,
                "afterShowsLine21Value": True,
                "earlierResultUnchangedAfter": True,
                "afterShowsReasonSentence": True,
                "afterShowsWhatItAssumed": True,
                "afterShowsRecordedNotUsed": True,
                "noLeakedCodePatternsBefore": True,
                "noLeakedCodePatternsAfter": True,
                "leakedCodePatterns": [],
            })

    def test_indistinguishable_choice_is_refused_with_nothing_saved(self) -> None:
        """R3 finding 4, path 2: an indistinguishable choice, which the
        served page shows as refused, with nothing saved."""
        assert _NODE is not None
        seed_acts, finding_id = _twin_borrowing_seed_acts(
            "Sprout study loan", "Sprout study loan")
        with TemporaryDirectory(prefix="sli-correction-session-") as session_dir, \
                TemporaryDirectory(prefix="sli-correction-saved-") as saved_dir:
            presentation_path = Path(saved_dir) / "presentation.json"
            presentation_path.write_text(json.dumps({"line21Explanation": {"rows": [
                {"statementLabel": {"lender": "Demo Lender", "statement": "Demo statement"},
                 "basis": {"answers": [{"findingId": finding_id,
                                        "factType": LOAN_COST_FACT_TYPE, "response": "yes"}]}},
            ]}}), encoding="utf-8")
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO,
                surface=core_calculations_surface(REPO), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=presentation_path, saved_run_id="demo.correction.test.twin",
                seed_acts=seed_acts,
            )
            before_revision = runtime._log.read().revision
            dist = build_correction_surface(WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO)
            with CorrectionSessionServer(runtime, dist) as server:
                result = subprocess.run(
                    [_NODE, str(REPO / "tests" / "helpers" / "correction_browser_client.mjs"),
                     server.url, "indistinguishable"],
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, timeout=90, check=False,
                )
            self.assertEqual(result.returncode, 0, result.stderr)
            observed = json.loads(result.stdout)
            self.assertEqual(observed, {
                "complete": True,
                "errorShown": True,
                "confirmationStayedHidden": True,
                "outcomeStayedHidden": True,
            })
            after_revision = runtime._log.read().revision
            self.assertEqual(before_revision, after_revision)

    def test_financing_change_after_confirmation_shown_is_not_saved(self) -> None:
        """R3 finding 4, path 3: a financing change after the confirmation
        is shown, which the served page shows as not saved."""
        assert _NODE is not None
        acts, saved_outcome = _shared_saved_run()
        surface = core_calculations_surface(REPO)
        with TemporaryDirectory(prefix="sli-correction-session-") as session_dir:
            runtime = _StaleAfterChooseRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO, surface=surface,
                run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=saved_outcome.presentation_path,
                saved_run_id="demo.correction.test.shared", seed_acts=acts,
            )
            dist = build_correction_surface(WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO)
            with CorrectionSessionServer(runtime, dist) as server:
                result = subprocess.run(
                    [_NODE, str(REPO / "tests" / "helpers" / "correction_browser_client.mjs"),
                     server.url, "stale-financing"],
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, timeout=90, check=False,
                )
            self.assertEqual(result.returncode, 0, result.stderr)
            observed = json.loads(result.stdout)
            self.assertTrue(observed.get("outcomeShowsNotSaved"))
            self.assertIn("Not saved", observed.get("titleText", ""))
            self.assertIsNotNone(runtime.revision_after_mutation)
            self.assertEqual(runtime.revision_after_mutation, runtime._log.read().revision)

    def test_unconfirmed_response_reloads_state_and_never_resubmits(self) -> None:
        """R3 finding 4, path 4: an unconfirmed response. The server's
        confirm response fails at the transport level; the page must say it
        could not confirm, reload the state, and not resubmit."""
        assert _NODE is not None
        acts, saved_outcome = _shared_saved_run()
        surface = core_calculations_surface(REPO)
        with TemporaryDirectory(prefix="sli-correction-session-") as session_dir:
            runtime = CorrectionRuntime(
                WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO, surface=surface,
                run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                saved_presentation_path=saved_outcome.presentation_path,
                saved_run_id="demo.correction.test.shared", seed_acts=acts,
            )
            dist = build_correction_surface(WorkspaceCapability(Path(session_dir) / "L"), repo_root=REPO)
            with mock.patch.object(correction_session_mod._CorrectionRequestHandler, "do_POST",
                                   _do_post_dropping_first_confirm_response):
                with CorrectionSessionServer(runtime, dist) as server:
                    result = subprocess.run(
                        [_NODE, str(REPO / "tests" / "helpers" / "correction_browser_client.mjs"),
                         server.url, "unconfirmed"],
                        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        text=True, timeout=90, check=False,
                    )
            self.assertEqual(result.returncode, 0, result.stderr)
            observed = json.loads(result.stdout)
            self.assertTrue(observed.get("titleMentionsCouldNotConfirm"))
            self.assertTrue(observed.get("reloadedStateShown"))

            # Exactly one correction act exists: the one the dropped
            # request's server-side confirm() actually saved. The page
            # never resubmitted, so there is no second one. (The seed
            # fixture's own original borrowing answers share the same
            # evidence kind, so a correction is told apart by carrying a
            # non-null ``correction_of_finding_id``, not by its kind alone.)
            acts_after = runtime._log.read().acts
            correction_evidence = [
                a for a in acts_after if a.get("kind") == "evidence-submitted"
                and a.get("payload", {}).get("evidence", {}).get("kind") == BORROWING_ANSWER_EVIDENCE_KIND
                and a.get("payload", {}).get("evidence", {}).get("content", {}).get(
                    "correction_of_finding_id") is not None
            ]
            self.assertEqual(len(correction_evidence), 1)


if __name__ == "__main__":
    unittest.main()
