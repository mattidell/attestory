"""A synthetic correction session over one saved student-loan line 21 result.

A person opens a correction session on a saved result, reviews one
borrowing's loan-cost answer, confirms a correction, and sees the return
recalculated beside the unchanged earlier result. The browser owns no
fact-writing authority: it submits a response through this session's small
JSON API; the session's only write is the reviewed recorder call through
``correct_borrowing_answer_review``, which writes through
``apply_contribution_batch`` the same as every other contribution. Nothing
here exposes a workspace locator through HTTP or in a response.

This is a parallel runtime and loopback server to ``entry_loop.py``'s
synthetic W-2 entry loop, not an edit to it. The W-2 entry loop's resolve,
build, seed and runtime classes are hard-wired to its own fixture; this
module is the equivalent set for the correction-session fixture
(``packages/sample_data/sli_correction_t1``). ``resolve_surface_artifact``
(``surface_resolver.py``) is reused unchanged, as the demonstrated plan
("Track 0 — readiness for implementation", H4) establishes it needs no
Node, schema, or ADR to serve a plain static page as an ADR-0049 surface
artifact.
"""

from __future__ import annotations

import json
import mimetypes
import shutil
import subprocess
from contextlib import AbstractContextManager
from datetime import datetime, timezone
from hmac import compare_digest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from secrets import token_urlsafe
from threading import Lock, Thread
from typing import Any, Mapping, Protocol, Sequence
from urllib.parse import urlsplit

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability, bootstrap_workspace
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface, Refusal
from packages.derivation.surface_resolver import ResolvedSurface, resolve_surface_artifact
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.loader import install_domain_scoped_supersession
from packages.tax.sli_relationship_recording import (
    BORROWING_QUESTIONS,
    FINANCING,
    FINANCING_DENIED,
    FINANCING_UNRESOLVED,
    FINANCING_WITHDRAWN,
    STATEMENT_INCLUSION,
    STATEMENT_INCLUSION_DENIED,
    STATEMENT_INCLUSION_UNRESOLVED,
    STATEMENT_INCLUSION_WITHDRAWN,
    RelationshipRecordingRefused,
)
from packages.tax.sli_relationship_review import (
    borrowing_recognition_clues,
    correct_borrowing_answer_review,
    prepare_borrowing_answer_review,
)

# The one supported question (plan, Track 0 step 2): "the supported question
# stays fixed to loan cost."
LOAN_COST_QUESTION = "loan-paid-only-school-costs"
LOAN_COST_FACT_TYPE = BORROWING_QUESTIONS[LOAN_COST_QUESTION]
# The other ordinary borrowing question (plan, Track 1 corrections,
# correction 4): a displayed enrollment answer is attributed the same way
# as a loan-cost answer.
ENROLL_FACT_TYPE = BORROWING_QUESTIONS["enrolled-at-least-half-time"]
# Every financing and statement-inclusion outcome (plan, Track 1 corrections,
# correction 2; R4 finding 3): each one is keyed by ``keys.borrowing`` exactly
# like the loan-cost and enroll answers above, so the same identity lookup
# resolves its displayed label. Never inferred from a count or a sentence.
_RELATIONSHIP_FACT_TYPES = frozenset({
    FINANCING, FINANCING_DENIED, FINANCING_WITHDRAWN, FINANCING_UNRESOLVED,
    STATEMENT_INCLUSION, STATEMENT_INCLUSION_DENIED, STATEMENT_INCLUSION_WITHDRAWN,
    STATEMENT_INCLUSION_UNRESOLVED,
})
_ATTRIBUTABLE_FACT_TYPES = (
    frozenset({LOAN_COST_FACT_TYPE, ENROLL_FACT_TYPE}) | _RELATIONSHIP_FACT_TYPES
)
_ALLOWED_RESPONSES = frozenset({"yes", "no", "cannot-tell"})

CORRECTION_FIXTURE = Path("packages/sample_data/sli_correction_t1")
SEED_LOG = CORRECTION_FIXTURE / "workspace" / "acts.jsonl"
SURFACE_CONTENT = CORRECTION_FIXTURE / "surface" / "content" / "app"
SURFACE_MANIFESTS = CORRECTION_FIXTURE / "surface" / "manifest"
SURFACE_REGISTRY = CORRECTION_FIXTURE / "surface" / "registry" / "published-surface-artifacts.json"
SURFACE_RELEASES = CORRECTION_FIXTURE / "surface" / "publication_surface" / "releases"
SURFACE_ADOPTION = CORRECTION_FIXTURE / "surface" / "adoptions" / "adopt-sli-correction-v1.json"

# Must match the seed fixture's own package-adoption act actor
# (``tests.test_sli_track4_support_chain.USER``), since
# ``select_current_adoption`` selects only that user's own adoption acts.
SCOPE_USER = "demo.user.filer"
RUN_SCOPE = {"jurisdiction": "us", "year": "2025"}

# The real, already-adopted v42 production surface (same fixture tests
# already run v42 against). No new package, release, or registry version is
# needed for this session (plan, Track 0 — readiness for implementation).
CORE_CONTENT = Path("packages/content/tax/2025")
CORE_RELEASE_DIR = Path(
    "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
)
CORE_V40_REGISTRY = CORE_CONTENT / "published-packages.v40.json"

_MAX_REQUEST_BYTES = 16_384


class CorrectionSessionError(RuntimeError):
    """A locator-free refusal suitable for the synthetic correction surface."""


def core_calculations_surface(repo_root: Path) -> PublicationSurface:
    """The adopted core-calculations surface this session recalculates against."""

    return PublicationSurface(
        repo_root / CORE_RELEASE_DIR, repo_root / CORE_V40_REGISTRY, repo_root / CORE_CONTENT,
    )


# ---------------------------------------------------------------------------
# The resolver: one displayed findingId to a current review target.
# ---------------------------------------------------------------------------


def resolve_displayed_answer_to_target(
    acts: Sequence[Mapping[str, Any]], registry: Any, finding_id: str,
) -> dict[str, Any]:
    """Classify one displayed ``findingId`` against the *current* workspace.

    The saved file contributes only the id; everything else is a fresh read
    of the current ActLog (plan, Track 0 step 2). Returns one of four
    outcomes: ``current``, ``superseded``, ``no-target``, ``not-a-target``.
    """
    state = project(tuple(dict(act) for act in acts), registry)
    current_ids = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state, include_displaced=True)
    return _classify_against_projection(state, current_ids, lattice, finding_id)


def _classify_against_projection(
    state: Any, current_ids: Any, lattice: Mapping[str, Any], finding_id: str,
) -> dict[str, Any]:
    """The resolver's classification, against an already-computed projection.

    Shared by ``resolve_displayed_answer_to_target`` (one id) and
    ``enumerate_choices`` (every candidate id in a saved presentation), so
    enumerating choices projects the current ActLog once rather than once
    per candidate.
    """
    finding = state.findings.get(finding_id)
    if finding is None:
        return {"status": "not-a-target",
                "reason": "no finding with this id exists in the current workspace"}
    fact = lattice.get(finding.get("fact_id", ""))
    if fact is None:
        return {"status": "not-a-target",
                "reason": "finding names a fact no longer in the current workspace"}
    if fact.fact_type_id != LOAN_COST_FACT_TYPE:
        return {"status": "not-a-target", "fact_type": fact.fact_type_id,
                "reason": "this finding is not the supported loan-cost answer; "
                          "it is not an editable target"}

    borrowing_ref = dict(fact.keys).get("borrowing")
    current_here = sorted(fid for fid, row in state.findings.items()
                          if fid in current_ids and row.get("fact_id") == fact.fact_id)
    if len(current_here) != 1:
        return {"status": "no-target", "borrowing_ref": borrowing_ref,
                "reason": "this borrowing has no current answer to this question; "
                          "there is nothing to correct"}
    [current_finding_id] = current_here
    if current_finding_id == finding_id:
        return {"status": "current", "borrowing_ref": borrowing_ref, "finding_id": finding_id}
    return {"status": "superseded", "borrowing_ref": borrowing_ref,
            "displayed_finding_id": finding_id, "current_finding_id": current_finding_id,
            "finding_id": current_finding_id,
            "reason": "a later correction already changed this borrowing's answer; "
                      "offering a review of the current answer, not the displayed one"}


def enumerate_choices(
    presentation: Mapping[str, Any], acts: Sequence[Mapping[str, Any]], registry: Any,
) -> dict[str, dict[str, Any]]:
    """One candidate correction choice per current loan-cost finding the
    saved presentation displays, deduplicated by finding id.

    Reads every ``account.said.current`` and ``basis.answers`` item in the
    saved presentation's line 21 rows and resolves each through the same
    classification the resolver above uses, keeping only current loan-cost
    answers (plan, Track 0 step 1). The same finding shown on two forms is
    one choice, with both forms recorded. The current ActLog is projected
    once for the whole enumeration, not once per candidate id.
    """
    state = project(tuple(dict(act) for act in acts), registry)
    current_ids = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state, include_displaced=True)

    explanation = presentation.get("line21Explanation") or {}
    choices: dict[str, dict[str, Any]] = {}
    for row in explanation.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        label = row.get("statementLabel")
        account = row.get("account") or {}
        basis = row.get("basis") or {}
        candidates: list[Any] = []
        said = account.get("said") if isinstance(account, dict) else None
        if isinstance(said, dict):
            candidates.extend(said.get("current", []) or [])
        if isinstance(basis, dict):
            candidates.extend(basis.get("answers", []) or [])
        for item in candidates:
            finding_id = item.get("findingId") if isinstance(item, dict) else None
            if not isinstance(finding_id, str):
                continue
            target = _classify_against_projection(state, current_ids, lattice, finding_id)
            if target.get("status") != "current":
                continue
            fid = target["finding_id"]
            entry = choices.setdefault(
                fid, {"finding_id": fid, "borrowing_ref": target["borrowing_ref"], "forms": []})
            if label is not None and label not in entry["forms"]:
                entry["forms"].append(label)
    return choices


def _attribute_borrowing_labels(
    rows: Sequence[Mapping[str, Any]], acts: Sequence[Mapping[str, Any]], registry: Any,
) -> list[dict[str, Any]]:
    """Resolve each displayed loan-cost or enrollment answer's borrowing
    label by identity (plan, Track 1 corrections, correction 4): findingId
    -> fact -> ``keys.borrowing`` -> that borrowing's current label. Never
    inferred from a count, a position, or a sentence.

    The lattice includes displaced facts, so a ``said.history`` item (a
    predecessor finding, now superseded) still resolves to its borrowing.
    Returns new row objects; ``rows`` and its nested items are never mutated
    in place.
    """
    state = project(tuple(dict(act) for act in acts), registry)
    lattice = facts_of(state.fact_state, include_displaced=True)
    entities = state.fact_state.entities

    def _borrowing_label(finding_id: object) -> str | None:
        if not isinstance(finding_id, str):
            return None
        finding = state.findings.get(finding_id)
        if not isinstance(finding, Mapping):
            return None
        fact = lattice.get(str(finding.get("fact_id", "")))
        if fact is None or fact.fact_type_id not in _ATTRIBUTABLE_FACT_TYPES:
            return None
        borrowing_ref = dict(fact.keys).get("borrowing")
        if not isinstance(borrowing_ref, str):
            return None
        lifecycle = entities.get(borrowing_ref)
        return lifecycle.entity.get("label") if lifecycle is not None else None

    def _annotate(item: Any) -> Any:
        if not isinstance(item, Mapping):
            return item
        label = _borrowing_label(item.get("findingId"))
        return {**item, "borrowingLabel": label} if label is not None else dict(item)

    annotated: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        new_row = dict(row)
        account = row.get("account")
        if isinstance(account, Mapping):
            said = account.get("said")
            if isinstance(said, Mapping):
                new_said = dict(said)
                for slot in ("current", "history"):
                    items = said.get(slot)
                    if isinstance(items, list):
                        new_said[slot] = [_annotate(item) for item in items]
                new_row["account"] = {**account, "said": new_said}
        basis = row.get("basis")
        if isinstance(basis, Mapping):
            answers = basis.get("answers")
            if isinstance(answers, list):
                new_row["basis"] = {**basis, "answers": [_annotate(item) for item in answers]}
        annotated.append(new_row)
    return annotated


# The saved presentation's own line 21 section id (``_section_id`` in
# ``presentation_projection.py``: ``f"line-{field['line']}"``), the same id
# the citation walk's ``renderLine21Explanation`` reads
# ``section.resolved.reasons`` from (``citation-walk.v1.html``).
_LINE21_SECTION_ID = "line-sch1-21"


def _line21_section_reasons(presentation: Mapping[str, Any]) -> list[Any]:
    """The line 21 section's own ``resolved.reasons`` list, by index -- the
    list every row's ``status.reasonIndices`` names into. Returns the raw
    reason mappings; the caller takes ``sentence`` only and drops the rest
    (plan, Track 1 explanation parity)."""
    sections = presentation.get("sections") if isinstance(presentation, Mapping) else None
    if not isinstance(sections, list):
        return []
    for section in sections:
        if isinstance(section, Mapping) and section.get("id") == _LINE21_SECTION_ID:
            resolved = section.get("resolved")
            reasons = resolved.get("reasons") if isinstance(resolved, Mapping) else None
            return list(reasons) if isinstance(reasons, list) else []
    return []


def _attach_line21_reason_sentences(
    rows: Sequence[Mapping[str, Any]], reasons: Sequence[Any],
) -> list[dict[str, Any]]:
    """Carry each named-by-reason row's reason sentences (``sentence`` only,
    identifiers dropped), resolved the same way the citation walk's
    ``renderLine21Explanation`` resolves ``status.reasonIndices`` against
    the line 21 section's ``resolved.reasons`` (plan, Track 1 explanation
    parity). A row whose index names no reason is refused, as the citation
    walk refuses it, rather than shown with nothing named. Returns new row
    objects; ``rows`` and its nested items are never mutated in place."""
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        new_row = dict(row)
        status = row.get("status")
        if isinstance(status, Mapping) and status.get("kind") == "named-by-reason":
            indices = status.get("reasonIndices")
            if not isinstance(indices, list) or not indices:
                raise CorrectionSessionError("correction-line21-reason-missing")
            sentences: list[str] = []
            for index in indices:
                reason = reasons[index] if isinstance(index, int) and 0 <= index < len(reasons) else None
                sentence = reason.get("sentence") if isinstance(reason, Mapping) else None
                if not isinstance(sentence, str) or not sentence:
                    raise CorrectionSessionError("correction-line21-reason-missing")
                sentences.append(sentence)
            new_row["reasonSentences"] = sentences
        out.append(new_row)
    return out


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Redacted refusal (plan, Track 1 corrections, correction 1; ADR 0051
# "redacted failure"). A ``RelationshipRecordingRefused`` carries the
# runtime's own internal wording -- a reason meant for logs, sometimes an
# f-string over a record. No exception text, act id, record, finding id, or
# demo identifier ever reaches a response. Each refusal is classified from
# its own reason, inspected only here, and reported as one of a small,
# declared set of person-facing sentences; the classifying text itself is
# never echoed.
# ---------------------------------------------------------------------------

_REFUSAL_INDISTINGUISHABLE = (
    "Two current borrowings would look the same. This choice cannot be reviewed on its own.")
_REFUSAL_SHOWN_CHANGED = (
    "What was shown in this review has changed since it was prepared. Nothing was saved.")
_REFUSAL_NOT_CURRENT = (
    "This is no longer the current answer to correct. Nothing was saved.")
_REFUSAL_OTHER = "This correction was not accepted. Nothing was saved."


def _classify_refusal(exc: RelationshipRecordingRefused) -> str:
    """Map a runtime refusal to one of four declared, person-facing
    sentences, by inspecting the refusal's own reason internally. The
    reason itself never reaches the return value."""
    reason = str(exc)
    if "indistinguishable" in reason:
        return _REFUSAL_INDISTINGUISHABLE
    if "no longer current" in reason or "prepared review changed" in reason:
        return _REFUSAL_SHOWN_CHANGED
    if "does not name this borrowing's current answer" in reason:
        return _REFUSAL_NOT_CURRENT
    return _REFUSAL_OTHER


# ---------------------------------------------------------------------------
# The correction runtime.
# ---------------------------------------------------------------------------


class CorrectionRuntime:
    """One synthetic, workspace-bound runtime: one ``ActLog`` and registry.

    Reads one saved presentation, which is never written, modified, or used
    as write authority. Its only write is the reviewed recorder call; a
    confirmed save is followed by one ``live_coordinate_run`` under an
    output name derived from the successor finding id, so the saved run's
    own output name can never collide with it.
    """

    def __init__(
        self,
        capability: WorkspaceCapability,
        *,
        repo_root: Path,
        surface: PublicationSurface,
        run_scope: Mapping[str, str],
        scope_user: str,
        saved_presentation_path: Path,
        saved_run_id: str,
        seed_acts: Sequence[Mapping[str, Any]] | None = None,
        schemas: DerivationSchemas | None = None,
    ) -> None:
        self._capability = capability
        self._repo_root = repo_root
        self._surface = surface
        self._run_scope = dict(run_scope)
        self._scope_user = scope_user
        self._schemas = schemas or DerivationSchemas()
        install_domain_scoped_supersession(self._schemas.registry)
        self._workspace = bootstrap_workspace(capability, repo_root=repo_root)
        self._log = ActLog(self._workspace.location, self._schemas.registry)
        self._lock = Lock()
        self._seed(seed_acts if seed_acts is not None else load_seed_acts(repo_root))
        try:
            self._saved_presentation: dict[str, Any] = json.loads(
                saved_presentation_path.read_text("utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise CorrectionSessionError("correction-saved-result-unavailable") from exc
        if not isinstance(self._saved_presentation, dict):
            raise CorrectionSessionError("correction-saved-result-invalid")
        self._saved_run_id = saved_run_id
        self._tokens: dict[str, dict[str, Any]] = {}
        # A token is consumed at save (plan, Track 1 repair, defect 3): once
        # ``confirm`` durably saves against a token, its outcome is recorded
        # here so a second confirm on the same token replays it rather than
        # attempting a second save.
        self._completed: dict[str, dict[str, Any]] = {}

    def _seed(self, seed_acts: Sequence[Mapping[str, Any]]) -> None:
        if self._log.read().revision:
            raise CorrectionSessionError("correction-workspace-not-empty")
        for expected, act in enumerate(seed_acts):
            body = dict(act)
            if body.get("committed_against") != expected:
                raise CorrectionSessionError("correction-fixture-invalid")
            self._log.append(body, expected_revision=expected)

    @property
    def registry(self) -> Any:
        return self._schemas.registry

    def state(self) -> dict[str, Any]:
        """The saved result's line 21 rows and the current correction choices."""
        with self._lock:
            acts = self._log.read().acts
            choices = enumerate_choices(self._saved_presentation, acts, self.registry)
            line21 = self._saved_presentation.get("line21Explanation") or {}
            rows = _attribute_borrowing_labels(line21.get("rows", []) or [], acts, self.registry)
            rows = _attach_line21_reason_sentences(rows, _line21_section_reasons(self._saved_presentation))
            working = line21.get("working") if isinstance(line21, dict) else None
            line21_value = working.get("value") if isinstance(working, dict) else None
            return {"saved_run_id": self._saved_run_id, "line21_rows": rows,
                    "line21_value": line21_value, "choices": choices}

    def resolve(self, finding_id: str) -> dict[str, Any]:
        """Classify one displayed finding id against the current workspace."""
        with self._lock:
            acts = self._log.read().acts
            return resolve_displayed_answer_to_target(acts, self.registry, finding_id)

    def choose(self, finding_id: str) -> dict[str, Any]:
        """Resolve one chosen answer and, for a current target, prepare a
        held review and confirmation under a fresh opaque token."""
        if not isinstance(finding_id, str) or not finding_id:
            raise CorrectionSessionError("correction-finding-id-invalid")
        with self._lock:
            contents = self._log.read()
            target = resolve_displayed_answer_to_target(contents.acts, self.registry, finding_id)
            status = target.get("status")
            if status not in {"current", "superseded"}:
                return {"status": status, "reason": target.get("reason")}
            target_finding_id = target["finding_id"]
            borrowing_ref = target["borrowing_ref"]
            state = project(contents.acts, self.registry)
            current_finding = state.findings.get(target_finding_id)
            if current_finding is None:
                return {"status": "no-target",
                        "reason": "this borrowing has no current answer to this question; "
                                  "there is nothing to correct"}
            current_response = current_finding.get("value")
            review_id = f"demo.correction.review.{token_urlsafe(16)}"
            try:
                review = prepare_borrowing_answer_review(
                    self._log, self.registry, review_id=review_id, shown_at=_now(),
                    borrowing_refs=(borrowing_ref,))
            except RelationshipRecordingRefused as exc:
                # The borrowing-answer review path itself refuses a selection
                # confusable with another current borrowing (plan, Track 1
                # repair, defect 1): an opaque id is never a recognition
                # clue, so nothing is prepared and nothing is written. The
                # reported reason is one of the declared redacted-refusal
                # sentences (plan, Track 1 corrections, correction 1), never
                # the runtime's own exception text.
                return {"status": "indistinguishable", "reason": _classify_refusal(exc)}
            matching_cards = [card for card in review["borrowing_choices"]
                              if card["choice_ref"] == borrowing_ref]
            if len(matching_cards) != 1:
                return {"status": "no-target",
                        "reason": "this borrowing is no longer a current choice"}
            [card] = matching_cards
            clues = borrowing_recognition_clues(contents, self.registry, borrowing_ref)
            forms_using_now = [form["statement"] for form in clues["forms"]
                               if form["inclusion"] == "affirmed"]
            confirmation = {
                "status": status,
                "borrowing_label": card["shown_as"],
                "recognition_clues": card["recognition_clues"],
                "question": review["propositions"][LOAN_COST_QUESTION],
                "current_answer": current_response,
                "forms_using_this_answer_now": forms_using_now,
                "disclaimer": "The effect on your return is known only after this "
                               "correction is recalculated.",
            }
            token = token_urlsafe(24)
            self._tokens[token] = {
                "review": review, "borrowing_ref": borrowing_ref, "question": LOAN_COST_QUESTION,
                "finding_id": target_finding_id, "confirmation": confirmation,
            }
            return {"status": status, "token": token, "confirmation": confirmation}

    def cancel(self, token: str) -> dict[str, Any]:
        """Discard the held token. Nothing is written."""
        with self._lock:
            self._tokens.pop(token, None)
            return {"outcome": "cancelled"}

    def confirm(self, token: str, response: str) -> dict[str, Any]:
        """Confirm the held review, save through the reviewed recorder call,
        then recalculate. Reports exactly one of three outcomes.

        A token is consumed at save (plan, Track 1 repair, defect 3): a
        second confirm on a token that already saved never attempts a
        second save. It replays the recorded outcome instead, marked
        ``already_used``. A refusal that happens *before* the save (the
        held review is stale) still reports ``not-saved`` and leaves the
        token free to be abandoned; nothing after the save may ever report
        ``not-saved`` -- a calculation refusal, an exception raised while
        recalculating, a presentation-model error, or a failure to read the
        new presentation back all report ``saved-not-calculated`` instead.
        """
        if response not in _ALLOWED_RESPONSES:
            raise CorrectionSessionError("correction-response-invalid")
        with self._lock:
            if isinstance(token, str) and token in self._completed:
                return {**self._completed[token], "already_used": True}
            prepared = self._tokens.get(token) if isinstance(token, str) else None
            if prepared is None:
                raise CorrectionSessionError("correction-unknown-token")
            self._tokens.pop(token, None)
            try:
                corrected = correct_borrowing_answer_review(
                    self._log, self.registry, prepared["review"], finding_id=prepared["finding_id"],
                    borrowing_ref=prepared["borrowing_ref"], question=prepared["question"],
                    response=response, actor=self._scope_user, at=_now(),
                    submission_id=f"demo.correction.submission.{token_urlsafe(16)}",
                    evidence_id=f"demo.evidence.correction.{token_urlsafe(16)}")
            except RelationshipRecordingRefused as exc:
                # A redacted refusal (plan, Track 1 corrections, correction
                # 1): the reported reason is one of the declared sentences
                # above, never the runtime's own exception text.
                return {"outcome": "not-saved", "reason": _classify_refusal(exc)}
            # The save is durable past this point: every failure below
            # reports saved-not-calculated, never not-saved, and the
            # recorded outcome is remembered against this token.
            predecessor = corrected.get("predecessor_finding_id")
            successor = corrected.get("finding_id")
            outcome = self._recalculate(predecessor, successor)
            self._completed[token] = outcome
            return outcome

    def _recalculate(self, predecessor: str | None, successor: str | None) -> dict[str, Any]:
        """Recalculate after a durable save; every failure here is honest
        about the save having happened (plan, Track 1 repair, defect 3)."""
        saved_not_calculated = {
            "outcome": "saved-not-calculated", "predecessor_finding_id": predecessor,
            "successor_finding_id": successor, "saved_run_id": self._saved_run_id,
        }
        contents = self._log.read()
        output_name = f"demo.correction.run.{successor}.json"
        try:
            run_outcome = live_coordinate_run(
                self._capability, repo_root=self._repo_root, authoritative_acts=contents.acts,
                workspace_revision=contents.revision, run_scope=self._run_scope,
                scope_user=self._scope_user, request={"schema": "run-request.v1"},
                run_id=f"demo.correction.run.{successor}", governance_pins=[],
                surface=self._surface, output_name=output_name, schemas=self._schemas)
        except Exception:
            # An exception raised while recalculating (ResidencyViolation or
            # otherwise) never surfaces past the save boundary.
            return saved_not_calculated
        if run_outcome.refusal is not None or run_outcome.presentation_path is None:
            return saved_not_calculated
        try:
            new_model = json.loads(run_outcome.presentation_path.read_text("utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return saved_not_calculated
        if not isinstance(new_model, dict):
            return saved_not_calculated
        line21 = new_model.get("line21Explanation") or {}
        rows = _attribute_borrowing_labels(line21.get("rows", []) or [], contents.acts, self.registry)
        rows = _attach_line21_reason_sentences(rows, _line21_section_reasons(new_model))
        working = line21.get("working") if isinstance(line21, dict) else None
        line21_value = working.get("value") if isinstance(working, dict) else None
        return {
            "outcome": "saved-and-calculated",
            "predecessor_finding_id": predecessor, "successor_finding_id": successor,
            "line21_rows": rows, "line21_value": line21_value, "saved_run_id": self._saved_run_id,
        }


# ---------------------------------------------------------------------------
# Fixture loading and the ADR-0049 surface artifact, hard-wired to the
# correction-session fixture (parallel to entry_loop.py's W-2 equivalents;
# none of this edits the W-2 entry loop).
# ---------------------------------------------------------------------------


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text("utf-8"))
    if not isinstance(value, dict):
        raise CorrectionSessionError("correction-fixture-invalid")
    return value


def load_seed_acts(repo_root: Path) -> list[dict[str, Any]]:
    """Read and validate the committed, newline-terminated seed act log."""
    path = repo_root / SEED_LOG
    try:
        raw = path.read_bytes()
    except OSError:
        raise CorrectionSessionError("correction-fixture-unavailable") from None
    if not raw.endswith(b"\n"):
        raise CorrectionSessionError("correction-fixture-invalid")
    acts: list[dict[str, Any]] = []
    try:
        for line in raw.splitlines():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError
            acts.append(value)
    except (json.JSONDecodeError, UnicodeError, ValueError):
        raise CorrectionSessionError("correction-fixture-invalid") from None
    return acts


def _surface_publication(repo_root: Path) -> PublicationSurface:
    root = repo_root / CORRECTION_FIXTURE / "surface"
    return PublicationSurface(
        release_dir=root / "publication_surface" / "releases",
        package_registry_path=root / "registry" / "published-surface-artifacts.json",
        member_dir=root / "manifest",
    )


def resolve_correction_surface(repo_root: Path) -> ResolvedSurface:
    """Resolve the correction page through the ADR-0049 surface artifact route."""
    adoption = _load_json(repo_root / SURFACE_ADOPTION)
    resolved = resolve_surface_artifact(
        [adoption], run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=SCOPE_USER,
        workspace_revision=1, surface=_surface_publication(repo_root),
        content_dir=repo_root / SURFACE_CONTENT)
    if isinstance(resolved, Refusal):
        raise CorrectionSessionError(f"correction-surface-refused:{resolved.reason}")
    return resolved


def build_correction_surface(
    capability: WorkspaceCapability, *, repo_root: Path, timeout_seconds: float = 60.0,
) -> Path:
    """Verify, copy, and (no-op) build the adopted surface inside the workspace."""
    workspace = bootstrap_workspace(capability, repo_root=repo_root)
    resolved = resolve_correction_surface(repo_root)
    build_root = workspace.live_output_path(Path(".correction-surface") / resolved.manifest["id"])
    if build_root.exists():
        raise CorrectionSessionError("correction-surface-build-target-exists")
    shutil.copytree(resolved.content_dir, build_root)
    command = str(resolved.manifest["build_command"]).split()
    try:
        result = subprocess.run(
            command, cwd=build_root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, timeout=timeout_seconds, check=False)
    except (OSError, subprocess.SubprocessError):
        raise CorrectionSessionError("correction-surface-build-failed") from None
    if result.returncode != 0:
        raise CorrectionSessionError("correction-surface-build-failed")
    entrypoint = build_root / str(resolved.manifest["entrypoint_html"])
    if not entrypoint.is_file():
        raise CorrectionSessionError("correction-surface-build-failed")
    return entrypoint.parent


# ---------------------------------------------------------------------------
# Loopback serving: a parallel server/handler pair to entry_loop.py's, since
# this session's routes (state / choose / confirm / cancel) differ from the
# W-2 entry loop's own (state / contributions). ``resolve_surface_artifact``
# above is reused unchanged; the HTTP mechanics below follow the same shape
# (route-scoped static serving, JSON admission, no caller-supplied locator)
# without editing the W-2 classes.
# ---------------------------------------------------------------------------


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


class CorrectionRuntimeLike(Protocol):
    """The shape the loopback server needs; duck-typed so a lighter test
    double can drive the HTTP admission path without a full ``CorrectionRuntime``."""

    def state(self) -> dict[str, Any]: ...

    def choose(self, finding_id: str) -> dict[str, Any]: ...

    def confirm(self, token: str, response: str) -> dict[str, Any]: ...

    def cancel(self, token: str) -> dict[str, Any]: ...


class _CorrectionHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, runtime: CorrectionRuntimeLike, static_root: Path, route: str) -> None:
        self.runtime = runtime
        self.static_root = static_root.resolve(strict=True)
        self.route = route.rstrip("/")
        super().__init__(("127.0.0.1", 0), _CorrectionRequestHandler)


class _CorrectionRequestHandler(BaseHTTPRequestHandler):
    server: _CorrectionHTTPServer

    def log_message(self, _format: str, *_args: object) -> None:
        return

    def _json(self, status: int, body: Mapping[str, Any]) -> None:
        encoded = _canonical_bytes(body)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def _target(self) -> tuple[str, str] | None:
        try:
            parsed = urlsplit(self.path)
        except ValueError:
            return None
        if parsed.query or parsed.fragment:
            return None
        prefix = f"{self.server.route}/"
        if not parsed.path.startswith(prefix):
            return None
        return parsed.path, parsed.path[len(prefix):]

    def _serve_static(self, relative: str) -> None:
        relative = relative or "index.html"
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            self.send_error(404)
            return
        candidate = (self.server.static_root / Path(*pure.parts)).resolve(strict=False)
        try:
            candidate.relative_to(self.server.static_root)
        except ValueError:
            self.send_error(404)
            return
        if not candidate.is_file():
            self.send_error(404)
            return
        try:
            body = candidate.read_bytes()
        except OSError:
            self.send_error(404)
            return
        mime = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; connect-src 'self'; "
            "img-src 'self' data:; object-src 'none'; base-uri 'none'",
        )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        target = self._target()
        if target is None:
            self.send_error(404)
            return
        _, relative = target
        if compare_digest(relative, "api/state"):
            self._json(200, self.server.runtime.state())
            return
        self._serve_static(relative)

    def _read_body(self) -> dict[str, Any] | None:
        if self.headers.get_content_type() != "application/json":
            return None
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return None
        if size <= 0 or size > _MAX_REQUEST_BYTES:
            return None
        try:
            body = json.loads(self.rfile.read(size))
        except (json.JSONDecodeError, UnicodeError, ValueError):
            return None
        return body if isinstance(body, dict) else None

    def do_POST(self) -> None:  # noqa: N802
        target = self._target()
        if target is None:
            self.send_error(404)
            return
        _, relative = target
        body = self._read_body()
        if body is None:
            self._json(400, {"error": "The request is invalid."})
            return
        try:
            if compare_digest(relative, "api/choose"):
                finding_id = body.get("finding_id")
                if set(body) != {"finding_id"} or not isinstance(finding_id, str) or not finding_id:
                    raise CorrectionSessionError("correction-request-invalid")
                result = self.server.runtime.choose(finding_id)
            elif compare_digest(relative, "api/confirm"):
                token = body.get("token")
                response = body.get("response")
                if (set(body) != {"token", "response"} or not isinstance(token, str)
                        or not token or not isinstance(response, str)):
                    raise CorrectionSessionError("correction-request-invalid")
                result = self.server.runtime.confirm(token, response)
            elif compare_digest(relative, "api/cancel"):
                token = body.get("token")
                if set(body) != {"token"} or not isinstance(token, str) or not token:
                    raise CorrectionSessionError("correction-request-invalid")
                result = self.server.runtime.cancel(token)
            else:
                self.send_error(404)
                return
        except CorrectionSessionError:
            self._json(422, {"error": "The request was not accepted. Nothing was changed."})
            return
        self._json(200, result)

    def do_HEAD(self) -> None:  # noqa: N802
        self.send_error(405)


class CorrectionSessionServer(AbstractContextManager["CorrectionSessionServer"]):
    """Owned loopback server for one synthetic correction runtime."""

    def __init__(self, runtime: CorrectionRuntimeLike, static_root: Path) -> None:
        route = f"/correction/{token_urlsafe(32)}"
        self._http = _CorrectionHTTPServer(runtime, static_root, route)
        self._thread = Thread(
            target=self._http.serve_forever, name="synthetic-correction-loopback", daemon=True)
        self._thread.start()
        self.url = f"http://127.0.0.1:{self._http.server_address[1]}{route}/index.html"
        self._closed = False

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._http.shutdown()
        finally:
            self._http.server_close()
        self._thread.join(timeout=3)
        if self._thread.is_alive():
            raise CorrectionSessionError("correction-server-teardown-failed")

    def __exit__(self, _type: Any, _value: Any, _traceback: Any) -> None:
        self.close()


__all__ = [
    "CORE_CONTENT",
    "CORE_RELEASE_DIR",
    "CORE_V40_REGISTRY",
    "CORRECTION_FIXTURE",
    "LOAN_COST_FACT_TYPE",
    "LOAN_COST_QUESTION",
    "RUN_SCOPE",
    "SCOPE_USER",
    "CorrectionRuntime",
    "CorrectionRuntimeLike",
    "CorrectionSessionError",
    "CorrectionSessionServer",
    "build_correction_surface",
    "core_calculations_surface",
    "enumerate_choices",
    "load_seed_acts",
    "resolve_correction_surface",
    "resolve_displayed_answer_to_target",
]
