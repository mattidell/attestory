"""Serializable one-review input contract for student-loan relationships.

This experimental layer snapshots recognizable source cards and explicit
choices, then delegates durable claims to the ordinary Track 14 recorder.
It records no tax treatment or interest allocation.
"""
from __future__ import annotations

import copy
import hashlib
from collections.abc import Set as AbstractSet
from typing import Any, Sequence

from packages.kernel.act_log import ActLog, LogContents
from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import project
from packages.tax.sli_relationship_recording import (
    BORROWING_KIND,
    BORROWING_QUESTIONS,
    FINANCING,
    SCHOOLING,
    STATEMENT_TYPE,
    RelationshipRecordingRefused,
    _commit_save,
    _read_for_save,
    _stage_answer,
    answer_relationship_claim_durably,
    correct_borrowing_answer_durably,
    correct_relationship_claim_durably,
    record_borrowing_answer_durably,
    record_submission,
    record_submission_durably,
    withdraw_borrowing_answer_durably,
    withdraw_relationship_claim_durably,
)

FORMAT = "experimental.sli-relationship-review.v1"
_ALLOWED = {"yes", "no", "cannot-tell", "unanswered"}

BORROWING_ANSWER_FORMAT = "experimental.sli-borrowing-answer-review.v1"
# The two owner-approved ordinary questions (plan, owner decision 1). The
# person is never asked whether the loan is a qualified education loan.
BORROWING_PROPOSITIONS = {
    "loan-paid-only-school-costs": "This loan paid only for school costs.",
    "enrolled-at-least-half-time": (
        "During the schooling this loan paid for, the student was enrolled at least "
        "half-time in a degree or certificate program."),
}


def _unique_current_finding(state: Any, current_ids: AbstractSet[str], fact_id: str,
                            fact_type: str) -> tuple[str, dict[str, Any]]:
    fact = facts_of(state.fact_state).get(fact_id)
    if fact is None or fact.fact_type_id != fact_type:
        raise RelationshipRecordingRefused("review choice does not name the requested current fact type")
    found = [(finding_id, finding) for finding_id, finding in state.findings.items()
             if finding_id in current_ids and finding.get("fact_id") == fact_id]
    if len(found) != 1:
        raise RelationshipRecordingRefused("review choice has no unique current source finding")
    return found[0]


def prepare_review(log: ActLog, registry: Any, *, review_id: str, shown_at: str,
                   borrowing_refs: Sequence[str], schooling_fact_ids: Sequence[str],
                   statement_fact_ids: Sequence[str]) -> dict[str, Any]:
    """Snapshot current source cards for one review; never choose a candidate.

    Display descriptions and provenance come from the current ActLog projection.
    Internal IDs are included only as action addresses, not as the visible name.
    """
    contents = log.read()
    return _prepare_review_from_contents(contents, registry, review_id=review_id, shown_at=shown_at,
                                         borrowing_refs=borrowing_refs,
                                         schooling_fact_ids=schooling_fact_ids,
                                         statement_fact_ids=statement_fact_ids)


def _borrowing_cards(contents: LogContents, state: Any,
                     borrowing_refs: Sequence[str]) -> list[dict[str, Any]]:
    entities = state.fact_state.entities
    borrowing_cards: list[dict[str, Any]] = []
    for reference in borrowing_refs:
        lifecycle = entities.get(reference)
        if (lifecycle is None or lifecycle.status != "current" or
                lifecycle.entity.get("kind") != BORROWING_KIND):
            raise RelationshipRecordingRefused("review borrowing choice is missing or stale")
        origin = next((row for row in reversed(contents.acts)
                       if row.get("kind") == "entity-introduced" and
                       row.get("payload", {}).get("entity", {}).get("id") == reference), None)
        borrowing_cards.append({
            "choice_ref": reference,
            "shown_as": lifecycle.entity.get("label"),
            "recognition_clues": [],
            "support": [{"act_id": origin.get("act_id")}] if origin else [],
        })
    return borrowing_cards


def _prepare_review_from_contents(contents: LogContents, registry: Any, *, review_id: str, shown_at: str,
                                  borrowing_refs: Sequence[str], schooling_fact_ids: Sequence[str],
                                  statement_fact_ids: Sequence[str]) -> dict[str, Any]:
    """Prepare cards from one immutable ActLog read."""
    if not review_id or not shown_at:
        raise RelationshipRecordingRefused("review identity and display time are required")
    state = project(contents.acts, registry)
    current_ids = compute_currency(state).current_finding_ids
    entities = state.fact_state.entities
    borrowing_cards = _borrowing_cards(contents, state, borrowing_refs)
    school_cards: list[dict[str, Any]] = []
    for fact_id in schooling_fact_ids:
        finding_id, finding = _unique_current_finding(state, current_ids, fact_id, SCHOOLING)
        fact = facts_of(state.fact_state)[fact_id]
        keys = dict(fact.keys)
        clue_labels = [entities[keys[name]].entity.get("label") for name in
                       ("period", "institution", "programme") if name in keys and keys[name] in entities]
        school_cards.append({
            "choice_ref": fact_id,
            "shown_as": finding.get("value"),
            "recognition_clues": clue_labels,
            "support": [{"finding_id": finding_id,
                         "evidence_ids": list(finding.get("evidence_ids", []))}],
        })
    statement_cards: list[dict[str, Any]] = []
    for fact_id in statement_fact_ids:
        finding_id, finding = _unique_current_finding(state, current_ids, fact_id, STATEMENT_TYPE)
        fact = facts_of(state.fact_state)[fact_id]
        keys = dict(fact.keys)
        statement_label = entities.get(keys.get("statement", ""))
        lender_label = entities.get(keys.get("lender", ""))
        year = keys.get("tax-year", "")
        statement_cards.append({
            "choice_ref": fact_id,
            "shown_as": str(statement_label.entity.get("label", "1098-E statement")) if statement_label else "1098-E statement",
            "tax_year": year,
            "issuer_as_printed": lender_label.entity.get("label") if lender_label else None,
            "box_1_reported_total": finding.get("value"),
            "recognition_clues": [],
            "support": [{"finding_id": finding_id,
                         "evidence_ids": list(finding.get("evidence_ids", []))}],
        })
    return {
        "format": FORMAT,
        "review_id": review_id,
        "shown_at": shown_at,
        "propositions": {
            "financing": "Some of this borrowing financed these studies.",
            "statement_inclusion": "This statement includes interest on this borrowing.",
        },
        "borrowing_choices": borrowing_cards,
        "schooling_choices": school_cards,
        "statement_choices": statement_cards,
        "selections": {"borrowing_ref": None, "schooling_fact_id": None,
                       "statement_fact_id": None},
        "responses": {"financing": "unanswered", "statement_inclusion": "unanswered"},
        "interest_portion": "not-requested",
    }


def _shown_statement_finding_id(review: dict[str, Any], statement_fact_id: str) -> str:
    """Return the exact box 1 finding the review showed for this statement."""
    for row in review.get("statement_choices", []):
        if row.get("choice_ref") != statement_fact_id:
            continue
        support = row.get("support")
        if (isinstance(support, list) and len(support) == 1 and isinstance(support[0], dict)
                and isinstance(support[0].get("finding_id"), str) and support[0]["finding_id"]):
            return str(support[0]["finding_id"])
    raise RelationshipRecordingRefused("review does not name the box 1 finding it showed")


def _choice_ref(review: dict[str, Any], collection: str, reference: Any) -> bool:
    return any(row.get("choice_ref") == reference for row in review.get(collection, []))


def _visible_card(card: dict[str, Any]) -> dict[str, Any]:
    """Return only information that could help the person tell cards apart."""
    return {key: value for key, value in card.items() if key not in {"choice_ref", "support"}}


def _require_distinguishable_selection(review: dict[str, Any], collection: str,
                                       reference: str | None) -> None:
    if reference is None:
        return
    selected = next((row for row in review.get(collection, [])
                     if row.get("choice_ref") == reference), None)
    if selected is None:
        raise RelationshipRecordingRefused("selected subject was not among the choices shown in this review")
    visible = _visible_card(selected)
    matching = [row for row in review.get(collection, []) if _visible_card(row) == visible]
    if len(matching) > 1:
        raise RelationshipRecordingRefused(
            "selected subject is indistinguishable from another displayed choice"
        )


def _revalidate_review(log: ActLog, registry: Any, review: dict[str, Any]) -> int:
    """Refuse a saved review whose displayed source snapshots are no longer current."""
    try:
        contents = log.read()
        refreshed = _prepare_review_from_contents(
            contents, registry, review_id=review["review_id"], shown_at=review["shown_at"],
            borrowing_refs=tuple(row["choice_ref"] for row in review["borrowing_choices"]),
            schooling_fact_ids=tuple(row["choice_ref"] for row in review["schooling_choices"]),
            statement_fact_ids=tuple(row["choice_ref"] for row in review["statement_choices"]),
        )
    except (KeyError, TypeError, RelationshipRecordingRefused) as exc:
        raise RelationshipRecordingRefused("reviewed choice is no longer current") from exc
    for name in ("format", "review_id", "shown_at", "propositions", "borrowing_choices",
                 "schooling_choices", "statement_choices", "selections", "responses",
                 "interest_portion"):
        if refreshed[name] != review.get(name):
            raise RelationshipRecordingRefused("prepared review changed; prepare a new review")
    return contents.revision


def _submission(review: dict[str, Any], *, borrowing_ref: str | None,
                schooling_fact_id: str | None, statement_fact_id: str | None,
                financing_response: str, inclusion_response: str,
                actor: str, at: str, submission_id: str, evidence_id: str,
                interest_portion_response: str = "unanswered",
                statement_correction: dict[str, Any] | None = None) -> dict[str, Any]:
    if review.get("format") != FORMAT or not review.get("review_id"):
        raise RelationshipRecordingRefused("unsupported or incomplete review object")
    if financing_response not in _ALLOWED or inclusion_response not in _ALLOWED:
        raise RelationshipRecordingRefused("each review clause requires an explicit response")
    if financing_response in {"yes", "no"} and (borrowing_ref is None or schooling_fact_id is None):
        raise RelationshipRecordingRefused("financing yes/no requires explicit borrowing and schooling selections")
    if inclusion_response in {"yes", "no"} and (borrowing_ref is None or statement_fact_id is None):
        raise RelationshipRecordingRefused("inclusion yes/no requires explicit borrowing and statement selections")
    for collection, reference in (("borrowing_choices", borrowing_ref),
                                  ("schooling_choices", schooling_fact_id),
                                  ("statement_choices", statement_fact_id)):
        if reference is not None and not _choice_ref(review, collection, reference):
            raise RelationshipRecordingRefused("selected subject was not among the choices shown in this review")
    # A nonempty address is itself a person selection for this input contract.
    # It cannot resolve equal visible cards, whatever answer is recorded.
    for collection, reference in (("borrowing_choices", borrowing_ref),
                                  ("schooling_choices", schooling_fact_id),
                                  ("statement_choices", statement_fact_id)):
        _require_distinguishable_selection(review, collection, reference)
    selections = {"borrowing_ref": borrowing_ref, "schooling_fact_id": schooling_fact_id,
                  "statement_fact_id": statement_fact_id}
    answer = {"financing": financing_response, "statement_inclusion": inclusion_response}
    context = {"format": FORMAT, "review_id": review["review_id"], "shown_at": review["shown_at"],
               "propositions": copy.deepcopy(review["propositions"]),
               "choices_shown": {name: copy.deepcopy(review[name]) for name in
                                  ("borrowing_choices", "schooling_choices", "statement_choices")},
               "selections": selections, "responses": answer,
               "interest_portion": "not-requested"}
    if statement_correction is not None:
        # Citing this evidence from the corrected box-1 finding refreshes
        # inclusion applicability onto that finding. Ordinary admission does not.
        correction = copy.deepcopy(statement_correction)
        correction["refreshes_inclusion_applicability"] = True
        context["statement_correction"] = correction
    return {
        "submission_id": submission_id, "evidence_id": evidence_id,
        "actor": actor, "at": at,
        "borrowing_ref": borrowing_ref, "schooling_fact_id": schooling_fact_id,
        "statement_fact_id": statement_fact_id,
        "financing_response": financing_response,
        "inclusion_response": inclusion_response,
        "interest_portion_response": interest_portion_response,
        "recognition_context": context,
    }


def save_review(log: ActLog, registry: Any, review: dict[str, Any], *,
                borrowing_ref: str | None, schooling_fact_id: str | None,
                statement_fact_id: str | None, financing_response: str,
                inclusion_response: str, actor: str, at: str,
                submission_id: str, evidence_id: str,
                interest_portion_response: str = "unanswered",
                statement_correction: dict[str, Any] | None = None) -> dict[str, Any]:
    """Save one person's review through the Track 14 durable contribution path."""
    reviewed_revision = _revalidate_review(log, registry, review)
    submission = _submission(
        review, borrowing_ref=borrowing_ref, schooling_fact_id=schooling_fact_id,
        statement_fact_id=statement_fact_id, financing_response=financing_response,
        inclusion_response=inclusion_response, actor=actor, at=at,
        submission_id=submission_id, evidence_id=evidence_id,
        interest_portion_response=interest_portion_response,
        statement_correction=statement_correction,
    )
    result = record_submission_durably(log, submission, registry, expected_revision=reviewed_revision)
    result["review"] = copy.deepcopy(submission["recognition_context"])
    return result


def correct_review_claim(log: ActLog, registry: Any, *, finding_id: str,
                         review: dict[str, Any], borrowing_ref: str | None,
                         schooling_fact_id: str | None, statement_fact_id: str | None,
                         financing_response: str, inclusion_response: str,
                         actor: str, at: str, submission_id: str,
                         evidence_id: str) -> dict[str, Any]:
    """Correct exactly one predecessor using a newly reviewed explicit choice."""
    reviewed_revision = _revalidate_review(log, registry, review)
    successor = _submission(
        review, borrowing_ref=borrowing_ref, schooling_fact_id=schooling_fact_id,
        statement_fact_id=statement_fact_id, financing_response=financing_response,
        inclusion_response=inclusion_response, actor=actor, at=at,
        submission_id=submission_id, evidence_id=evidence_id,
    )
    return correct_relationship_claim_durably(
        log, registry, finding_id=finding_id, successor=successor, actor=actor, at=at,
        expected_revision=reviewed_revision,
    )


def answer_review_claim(log: ActLog, registry: Any, *, finding_id: str,
                        review: dict[str, Any], borrowing_ref: str | None,
                        schooling_fact_id: str | None, statement_fact_id: str | None,
                        financing_response: str, inclusion_response: str,
                        actor: str, at: str, submission_id: str,
                        evidence_id: str,
                        statement_correction: dict[str, Any] | None = None) -> dict[str, Any]:
    """Save a reviewed no/cannot-tell answer and end that pair's support."""
    reviewed_revision = _revalidate_review(log, registry, review)
    submission = _submission(
        review, borrowing_ref=borrowing_ref, schooling_fact_id=schooling_fact_id,
        statement_fact_id=statement_fact_id, financing_response=financing_response,
        inclusion_response=inclusion_response, actor=actor, at=at,
        submission_id=submission_id, evidence_id=evidence_id,
        statement_correction=statement_correction,
    )
    result = answer_relationship_claim_durably(
        log, registry, finding_id=finding_id, submission=submission,
        actor=actor, at=at, expected_revision=reviewed_revision,
    )
    result["review"] = copy.deepcopy(submission["recognition_context"])
    return result


def apply_statement_correction_review(log: ActLog, registry: Any, *, review: dict[str, Any],
                                      statement_fact_id: str, scope: str,
                                      borrowing_ref: str | None, finding_id: str | None,
                                      corrected_box1_total: int | float,
                                      source_correction_id: str,
                                      actor: str, at: str, submission_id: str,
                                      evidence_id: str) -> dict[str, Any]:
    """Record the known scope of one statement correction through one review.

    The scope answer and the corrected box-1 source are one save. ``scope`` is
    ``amount-only``, ``inclusion-added``, ``inclusion-removed`` or
    ``inclusion-uncertain``. A pair is named only when the correction changes
    inclusion. The scope evidence binds the box 1 finding the review saw, the
    corrected amount, and the correction identity. It authorizes one admitted
    finding: the successor of that finding, at that amount, carrying that
    correction identity. A later update that cites the same evidence is
    refused.

    Track 7: the scope evidence, any inclusion answer and the corrected source
    are written as one batch. An interruption leaves the statement and its
    loans as they were, or the whole correction; never a corrected amount with
    the earlier loans, or an earlier amount with only some of them.
    """
    if statement_fact_id not in {row.get("choice_ref") for row in review.get("statement_choices", [])}:
        raise RelationshipRecordingRefused("correction statement was not shown in the review")
    if scope not in {"amount-only", "inclusion-added", "inclusion-removed", "inclusion-uncertain"}:
        raise RelationshipRecordingRefused("unsupported statement correction scope")
    if isinstance(corrected_box1_total, bool) or not isinstance(corrected_box1_total, (int, float)) or corrected_box1_total < 0:
        raise RelationshipRecordingRefused("corrected box-1 total must be a nonnegative number")
    if not isinstance(source_correction_id, str) or not source_correction_id:
        raise RelationshipRecordingRefused("source correction identity is required")
    if scope == "amount-only":
        if borrowing_ref is not None or finding_id is not None:
            raise RelationshipRecordingRefused("amount-only correction cannot target an inclusion pair")
        revision = _revalidate_review(log, registry, review)
        submission = _submission(
            review, borrowing_ref=None, schooling_fact_id=None,
            statement_fact_id=statement_fact_id, financing_response="unanswered",
            inclusion_response="unanswered", actor=actor, at=at,
            submission_id=submission_id, evidence_id=evidence_id,
            statement_correction={"statement_fact_id": statement_fact_id, "scope": scope,
                                  "included_borrowings_changed": False,
                                  "source_correction_id": source_correction_id,
                                  "corrected_box1_total": corrected_box1_total,
                                  "reviewed_statement_finding_id": _shown_statement_finding_id(
                                      review, statement_fact_id)},
        )
        before = _read_for_save(log, revision)
        staged = [copy.deepcopy(row) for row in before.acts]
        scope_result = record_submission(staged, submission, registry)
        source = _stage_statement_source_correction(
            staged, registry, statement_fact_id=statement_fact_id, corrected_total=corrected_box1_total,
            correction_id=source_correction_id, actor=actor, at=at, scope_evidence_id=evidence_id,
        )
        committed, state = _commit_correction(log, registry, before, staged)
        return {**scope_result, "source_correction": {**source, "revision": committed, "state": state},
                "revision": committed, "state": state,
                "review": copy.deepcopy(submission["recognition_context"])}
    if borrowing_ref is None or borrowing_ref not in {row.get("choice_ref")
                                                       for row in review.get("borrowing_choices", [])}:
        raise RelationshipRecordingRefused("correction scope requires the identified borrowing")
    if scope == "inclusion-added":
        if finding_id is not None:
            raise RelationshipRecordingRefused("an added inclusion cannot target an existing affirmative finding")
        revision = _revalidate_review(log, registry, review)
        submission = _submission(
            review, borrowing_ref=borrowing_ref, schooling_fact_id=None,
            statement_fact_id=statement_fact_id, financing_response="unanswered",
            inclusion_response="unanswered", actor=actor, at=at,
            submission_id=submission_id, evidence_id=evidence_id,
            statement_correction={"statement_fact_id": statement_fact_id,
                                  "borrowing_ref": borrowing_ref, "scope": scope,
                                  "source_correction_id": source_correction_id,
                                  "corrected_box1_total": corrected_box1_total,
                                  "reviewed_statement_finding_id": _shown_statement_finding_id(
                                      review, statement_fact_id)},
        )
        before = _read_for_save(log, revision)
        staged = [copy.deepcopy(row) for row in before.acts]
        scope_result = record_submission(staged, submission, registry)
        source = _stage_statement_source_correction(
            staged, registry, statement_fact_id=statement_fact_id, corrected_total=corrected_box1_total,
            correction_id=source_correction_id, actor=actor, at=at,
            scope_evidence_id=evidence_id,
        )
        # The added pair is affirmed against the corrected source, in the same save.
        answer_id = f"{evidence_id}.affirmative"
        answer = dict(submission, submission_id=f"{submission_id}.affirmative", evidence_id=answer_id,
                      inclusion_response="yes")
        answer["recognition_context"] = copy.deepcopy(submission["recognition_context"])
        result = record_submission(staged, answer, registry)
        committed, state = _commit_correction(log, registry, before, staged)
        result["scope_evidence_id"] = scope_result["evidence_id"]
        result["source_correction"] = {**source, "revision": committed, "state": state}
        result["revision"] = committed
        result["state"] = state
        result["review"] = copy.deepcopy(submission["recognition_context"])
        return result
    if finding_id is None:
        raise RelationshipRecordingRefused("removed or uncertain inclusion requires its prior finding")
    response = "no" if scope == "inclusion-removed" else "cannot-tell"
    revision = _revalidate_review(log, registry, review)
    submission = _submission(
        review, borrowing_ref=borrowing_ref, schooling_fact_id=None,
        statement_fact_id=statement_fact_id, financing_response="unanswered",
        inclusion_response=response, actor=actor, at=at,
        submission_id=submission_id, evidence_id=evidence_id,
        statement_correction={"statement_fact_id": statement_fact_id,
                              "borrowing_ref": borrowing_ref, "scope": scope,
                              "source_correction_id": source_correction_id,
                              "corrected_box1_total": corrected_box1_total,
                              "reviewed_statement_finding_id": _shown_statement_finding_id(
                                  review, statement_fact_id)},
    )
    before = _read_for_save(log, revision)
    # The answer on the named pair, then the corrected source it scopes.
    result, staged = _stage_answer(before, registry, finding_id=finding_id, submission=submission,
                                   actor=actor, at=at)
    source = _stage_statement_source_correction(
        staged, registry, statement_fact_id=statement_fact_id, corrected_total=corrected_box1_total,
        correction_id=source_correction_id, actor=actor, at=at,
        scope_evidence_id=evidence_id,
    )
    committed, state = _commit_correction(log, registry, before, staged)
    result["review"] = copy.deepcopy(submission["recognition_context"])
    result["source_correction"] = {**source, "revision": committed, "state": state}
    result["revision"] = committed
    result["state"] = state
    return result


def _commit_correction(log: ActLog, registry: Any, before: LogContents,
                       staged: list[dict[str, Any]]) -> tuple[int, Any]:
    """Write one staged correction as one batch; return its revision and fresh state."""
    committed = _commit_save(log, before, staged, registry, reviewed=True)
    return committed, project(log.read().acts, registry)


def _amounts_equal(left: object, right: object) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return False
    return isinstance(left, (int, float)) and isinstance(right, (int, float)) and left == right


def _bound_scope_correction(state: Any, scope_evidence_id: str) -> dict[str, Any]:
    """Return the statement-correction object one scope evidence recorded."""
    lifecycle = state.evidence.get(scope_evidence_id)
    body = lifecycle.evidence if lifecycle is not None and isinstance(
        getattr(lifecycle, "evidence", None), dict) else None
    content = body.get("content") if isinstance(body, dict) else None
    context = content.get("recognition_context") if isinstance(content, dict) else None
    correction = context.get("statement_correction") if isinstance(context, dict) else None
    if body is None or body.get("kind") != "tax.student-loan.relationship-answer" or not isinstance(correction, dict):
        raise RelationshipRecordingRefused("scope evidence is not one reviewed statement correction")
    return correction


def _append_statement_source_correction_durably(log: ActLog, registry: Any, *,
                                                statement_fact_id: str,
                                                corrected_total: int | float,
                                                correction_id: str, scope_evidence_id: str,
                                                actor: str, at: str) -> dict[str, Any]:
    """Append the one box 1 finding a reviewed scope evidence authorizes.

    The evidence names the finding the review saw, the corrected amount, and
    the correction identity. This write is that successor or it is refused
    before any act is appended. A second write citing the same evidence is
    refused, including one that repeats the amount. The evidence, contribution
    and finding are one batch, so a refusal by the ADR 0077 Part 5 new-write
    step at the finding leaves nothing behind (Track 7, carried item 3).
    """
    before = _read_for_save(log, None)
    staged = [copy.deepcopy(row) for row in before.acts]
    source = _stage_statement_source_correction(
        staged, registry, statement_fact_id=statement_fact_id, corrected_total=corrected_total,
        correction_id=correction_id, scope_evidence_id=scope_evidence_id, actor=actor, at=at)
    committed = _commit_save(log, before, staged, registry)
    recovered = log.read()
    return {**source, "revision": committed, "state": project(recovered.acts, registry)}


def _stage_statement_source_correction(staged: list[dict[str, Any]], registry: Any, *,
                                       statement_fact_id: str, corrected_total: int | float,
                                       correction_id: str, scope_evidence_id: str,
                                       actor: str, at: str) -> dict[str, Any]:
    """Stage the bound box 1 successor after the acts already in ``staged``."""
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    current_ids = compute_currency(state).current_finding_ids
    fact = facts_of(state.fact_state).get(statement_fact_id)
    current = [(finding_id, finding) for finding_id, finding in state.findings.items()
               if finding_id in current_ids and finding.get("fact_id") == statement_fact_id]
    if fact is None or fact.fact_type_id != STATEMENT_TYPE or len(current) != 1:
        raise RelationshipRecordingRefused("statement correction must target one current 1098-E source")
    correction = _bound_scope_correction(state, scope_evidence_id)
    if correction.get("statement_fact_id") != statement_fact_id:
        raise RelationshipRecordingRefused("scope evidence names a different statement")
    if correction.get("scope") not in {"amount-only", "inclusion-added", "inclusion-removed", "inclusion-uncertain"}:
        raise RelationshipRecordingRefused("scope evidence has no reviewed correction scope")
    if correction.get("refreshes_inclusion_applicability") is not True:
        raise RelationshipRecordingRefused("scope evidence does not refresh inclusion applicability")
    if correction.get("source_correction_id") != correction_id:
        raise RelationshipRecordingRefused("scope evidence is bound to a different correction")
    if not _amounts_equal(correction.get("corrected_box1_total"), corrected_total):
        raise RelationshipRecordingRefused("scope evidence is bound to a different corrected amount")
    reviewed_finding_id = correction.get("reviewed_statement_finding_id")
    if not isinstance(reviewed_finding_id, str) or not reviewed_finding_id:
        raise RelationshipRecordingRefused("scope evidence does not name the box 1 finding the review saw")
    if current[0][0] != reviewed_finding_id:
        raise RelationshipRecordingRefused("box 1 finding changed since the review")
    # Single use counts box 1 findings only. The inclusion-uncertain route's
    # own unresolved status cites the same answer evidence; it is not a box 1
    # finding, so it does not use up the authorization.
    all_facts = facts_of(state.fact_state, include_displaced=True)
    already_authorized = [
        finding_id for finding_id, finding in state.findings.items()
        if isinstance(finding, dict) and scope_evidence_id in (finding.get("evidence_ids") or [])
        and getattr(all_facts.get(finding.get("fact_id", "")), "fact_type_id", None) == STATEMENT_TYPE
    ]
    if already_authorized:
        raise RelationshipRecordingRefused("scope evidence already authorizes one finding")
    suffix = hashlib.sha256(correction_id.encode("utf-8")).hexdigest()[:20]
    source_evidence_id = f"demo.evidence.sli.statement-correction.{suffix}"
    contribution_id = f"demo.contribution.sli.statement-correction.{suffix}"
    finding_id = f"demo.finding.sli.statement-correction.{suffix}"
    if source_evidence_id in state.evidence or finding_id in state.findings:
        raise RelationshipRecordingRefused("source correction identity has already been used")
    revision = len(staged)
    evidence = {"schema": "evidence.v1", "id": source_evidence_id,
                "kind": "tax.form-1098e-corrected-statement-source",
                "label": "Corrected Form 1098-E box-1 source",
                "content": {"source_correction_id": correction_id}}
    evidence_act = {"schema": "act.v1", "act_id": f"sli.statement-correction.evidence.{suffix}",
                    "kind": "evidence-submitted", "actor": actor, "at": at,
                    "committed_against": revision, "payload": {"evidence": evidence}}
    contribution_act = {"schema": "act.v1", "act_id": f"sli.statement-correction.contribution.{suffix}",
                        "kind": "contribution", "actor": actor, "at": at,
                        "committed_against": revision + 1,
                        "payload": {"contribution": {"schema": "contribution.v1", "id": contribution_id,
                                                       "evidence_id": source_evidence_id,
                                                       "content": {"mode": "manual-entry",
                                                                   "source": "corrected-form-1098e"}}}}
    finding = {"schema": "finding.v2", "id": finding_id, "fact_id": statement_fact_id,
               "value": corrected_total, "basis": "attested",
               "evidence_ids": [source_evidence_id, scope_evidence_id],
               "contribution_id": contribution_id}
    assertion = {"schema": "act.v1", "act_id": f"sli.statement-correction.assertion.{suffix}",
                 "kind": "assertion", "actor": actor, "at": at,
                 "committed_against": revision + 2, "payload": {"finding": finding}}
    base = project(tuple(copy.deepcopy(row) for row in (*staged, evidence_act)), registry)
    admission = apply_contribution_batch(base, contribution_act=contribution_act,
                                         successor_acts=[assertion], registry=registry,
                                         record_id=f"sli.statement-correction.record.{suffix}")
    if admission.terminal_record["phase"] != "completed":
        raise RelationshipRecordingRefused("corrected statement source failed contribution admission")
    staged.extend((evidence_act, contribution_act, assertion))
    return {"statement_fact_id": statement_fact_id, "source_finding_id": finding_id,
            "source_evidence_id": source_evidence_id}


def withdraw_review_claim(log: ActLog, registry: Any, *, finding_id: str,
                          actor: str, at: str) -> dict[str, Any]:
    """Withdraw one exact claim; its original review evidence remains in history."""
    return withdraw_relationship_claim_durably(
        log, registry, finding_id=finding_id, actor=actor, at=at,
    )


def prepare_borrowing_answer_review(log: ActLog, registry: Any, *, review_id: str, shown_at: str,
                                    borrowing_refs: Sequence[str]) -> dict[str, Any]:
    """Snapshot borrowing cards and the two ordinary questions for one review.

    The person answers each question for one identified loan; this never
    chooses a loan for them. Answers start ``unanswered``.
    """
    contents = log.read()
    return _prepare_borrowing_answer_review_from_contents(
        contents, registry, review_id=review_id, shown_at=shown_at, borrowing_refs=borrowing_refs)


def _prepare_borrowing_answer_review_from_contents(contents: LogContents, registry: Any, *,
                                                   review_id: str, shown_at: str,
                                                   borrowing_refs: Sequence[str]) -> dict[str, Any]:
    if not review_id or not shown_at:
        raise RelationshipRecordingRefused("review identity and display time are required")
    state = project(contents.acts, registry)
    return {
        "format": BORROWING_ANSWER_FORMAT,
        "review_id": review_id,
        "shown_at": shown_at,
        "propositions": dict(BORROWING_PROPOSITIONS),
        "borrowing_choices": _borrowing_cards(contents, state, borrowing_refs),
        "selections": {"borrowing_ref": None},
        "responses": {question: "unanswered" for question in BORROWING_PROPOSITIONS},
    }


def _revalidate_borrowing_answer_review(log: ActLog, registry: Any, review: dict[str, Any]) -> int:
    """Refuse a saved borrowing review whose cards or questions are no longer current."""
    if review.get("format") != BORROWING_ANSWER_FORMAT or not review.get("review_id"):
        raise RelationshipRecordingRefused("unsupported or incomplete review object")
    try:
        contents = log.read()
        refreshed = _prepare_borrowing_answer_review_from_contents(
            contents, registry, review_id=review["review_id"], shown_at=review["shown_at"],
            borrowing_refs=tuple(row["choice_ref"] for row in review["borrowing_choices"]),
        )
    except (KeyError, TypeError, RelationshipRecordingRefused) as exc:
        raise RelationshipRecordingRefused("reviewed choice is no longer current") from exc
    for name in ("format", "review_id", "shown_at", "propositions", "borrowing_choices",
                 "selections", "responses"):
        if refreshed[name] != review.get(name):
            raise RelationshipRecordingRefused("prepared review changed; prepare a new review")
    return contents.revision


def _borrowing_answer_context(review: dict[str, Any], *, borrowing_ref: str, question: str,
                              response: str) -> dict[str, Any]:
    if question not in BORROWING_QUESTIONS:
        raise RelationshipRecordingRefused("unknown borrowing question")
    if not _choice_ref(review, "borrowing_choices", borrowing_ref):
        raise RelationshipRecordingRefused("selected subject was not among the choices shown in this review")
    _require_distinguishable_selection(review, "borrowing_choices", borrowing_ref)
    return {"format": BORROWING_ANSWER_FORMAT, "review_id": review["review_id"],
            "shown_at": review["shown_at"], "question": question,
            "proposition": review["propositions"][question],
            "choices_shown": {"borrowing_choices": copy.deepcopy(review["borrowing_choices"])},
            "selections": {"borrowing_ref": borrowing_ref}, "response": response}


def save_borrowing_answer_review(log: ActLog, registry: Any, review: dict[str, Any], *,
                                 borrowing_ref: str, question: str, response: str,
                                 actor: str, at: str, submission_id: str,
                                 evidence_id: str) -> dict[str, Any]:
    """Save one person's answer to one of the two ordinary questions for one loan."""
    reviewed_revision = _revalidate_borrowing_answer_review(log, registry, review)
    context = _borrowing_answer_context(review, borrowing_ref=borrowing_ref, question=question,
                                        response=response)
    result = record_borrowing_answer_durably(
        log, registry, question=question, borrowing_ref=borrowing_ref, response=response,
        submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
        recognition_context=context, expected_revision=reviewed_revision)
    result["review"] = copy.deepcopy(context)
    return result


def correct_borrowing_answer_review(log: ActLog, registry: Any, review: dict[str, Any], *,
                                    finding_id: str, borrowing_ref: str, question: str,
                                    response: str, actor: str, at: str, submission_id: str,
                                    evidence_id: str) -> dict[str, Any]:
    """Replace one loan's current answer to one question with a newly reviewed answer."""
    reviewed_revision = _revalidate_borrowing_answer_review(log, registry, review)
    context = _borrowing_answer_context(review, borrowing_ref=borrowing_ref, question=question,
                                        response=response)
    result = correct_borrowing_answer_durably(
        log, registry, finding_id=finding_id, question=question, borrowing_ref=borrowing_ref,
        response=response, submission_id=submission_id, evidence_id=evidence_id, actor=actor,
        at=at, recognition_context=context, expected_revision=reviewed_revision)
    result["review"] = copy.deepcopy(context)
    return result


def withdraw_borrowing_answer_review(log: ActLog, registry: Any, *, finding_id: str,
                                     actor: str, at: str) -> dict[str, Any]:
    """Withdraw one loan's answer; its evidence remains in history."""
    return withdraw_borrowing_answer_durably(log, registry, finding_id=finding_id, actor=actor, at=at)
