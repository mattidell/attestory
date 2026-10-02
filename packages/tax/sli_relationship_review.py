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
    FINANCING,
    SCHOOLING,
    STATEMENT_TYPE,
    RelationshipRecordingRefused,
    answer_relationship_claim_durably,
    correct_relationship_claim_durably,
    record_submission_durably,
    withdraw_relationship_claim_durably,
)

FORMAT = "experimental.sli-relationship-review.v1"
_ALLOWED = {"yes", "no", "cannot-tell", "unanswered"}


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


def _prepare_review_from_contents(contents: LogContents, registry: Any, *, review_id: str, shown_at: str,
                                  borrowing_refs: Sequence[str], schooling_fact_ids: Sequence[str],
                                  statement_fact_ids: Sequence[str]) -> dict[str, Any]:
    """Prepare cards from one immutable ActLog read."""
    if not review_id or not shown_at:
        raise RelationshipRecordingRefused("review identity and display time are required")
    state = project(contents.acts, registry)
    current_ids = compute_currency(state).current_finding_ids
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
        context["statement_correction"] = copy.deepcopy(statement_correction)
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

    This operation records the scope before appending the corrected box-1
    source. ``scope`` is ``amount-only``, ``inclusion-removed`` or
    ``inclusion-uncertain``. A pair is named only for the latter two cases.
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
                                  "corrected_box1_total": corrected_box1_total},
        )
        scope_result = record_submission_durably(log, submission, registry, expected_revision=revision)
        source_result = _append_statement_source_correction_durably(
            log, registry, statement_fact_id=statement_fact_id, corrected_total=corrected_box1_total,
            correction_id=source_correction_id, actor=actor, at=at, scope_evidence_id=evidence_id,
        )
        return {**scope_result, "source_correction": source_result,
                "revision": source_result["revision"], "state": source_result["state"],
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
                                  "corrected_box1_total": corrected_box1_total},
        )
        scope_result = record_submission_durably(log, submission, registry, expected_revision=revision)
        source_result = _append_statement_source_correction_durably(
            log, registry, statement_fact_id=statement_fact_id, corrected_total=corrected_box1_total,
            correction_id=source_correction_id, actor=actor, at=at,
            scope_evidence_id=evidence_id,
        )
        answer_id = f"{evidence_id}.affirmative"
        answer = dict(submission, submission_id=f"{submission_id}.affirmative", evidence_id=answer_id,
                      inclusion_response="yes")
        answer["recognition_context"] = copy.deepcopy(submission["recognition_context"])
        result = record_submission_durably(log, answer, registry,
                                           expected_revision=source_result["revision"])
        result["scope_evidence_id"] = scope_result["evidence_id"]
        result["source_correction"] = source_result
        result["revision"] = result["revision"]
        result["review"] = copy.deepcopy(submission["recognition_context"])
        return result
    if finding_id is None:
        raise RelationshipRecordingRefused("removed or uncertain inclusion requires its prior finding")
    response = "no" if scope == "inclusion-removed" else "cannot-tell"
    result = answer_review_claim(
        log, registry, finding_id=finding_id, review=review,
        borrowing_ref=borrowing_ref, schooling_fact_id=None,
        statement_fact_id=statement_fact_id, financing_response="unanswered",
        inclusion_response=response, actor=actor, at=at,
        submission_id=submission_id, evidence_id=evidence_id,
        statement_correction={"statement_fact_id": statement_fact_id,
                              "borrowing_ref": borrowing_ref, "scope": scope,
                              "source_correction_id": source_correction_id,
                              "corrected_box1_total": corrected_box1_total},
    )
    source_result = _append_statement_source_correction_durably(
        log, registry, statement_fact_id=statement_fact_id, corrected_total=corrected_box1_total,
        correction_id=source_correction_id, actor=actor, at=at,
        scope_evidence_id=evidence_id,
    )
    result["source_correction"] = source_result
    result["revision"] = source_result["revision"]
    result["state"] = source_result["state"]
    return result


def _append_statement_source_correction_durably(log: ActLog, registry: Any, *,
                                                statement_fact_id: str,
                                                corrected_total: int | float,
                                                correction_id: str, scope_evidence_id: str,
                                                actor: str, at: str) -> dict[str, Any]:
    """Append a same-identity corrected 1098-E box-1 source by normal admission."""
    contents = log.read()
    if contents.incomplete_tail is not None:
        raise RelationshipRecordingRefused("ActLog has an incomplete tail")
    state = project(contents.acts, registry)
    current_ids = compute_currency(state).current_finding_ids
    fact = facts_of(state.fact_state).get(statement_fact_id)
    current = [finding for finding_id, finding in state.findings.items()
               if finding_id in current_ids and finding.get("fact_id") == statement_fact_id]
    if fact is None or fact.fact_type_id != STATEMENT_TYPE or len(current) != 1:
        raise RelationshipRecordingRefused("statement correction must target one current 1098-E source")
    suffix = hashlib.sha256(correction_id.encode("utf-8")).hexdigest()[:20]
    source_evidence_id = f"demo.evidence.sli.statement-correction.{suffix}"
    contribution_id = f"demo.contribution.sli.statement-correction.{suffix}"
    finding_id = f"demo.finding.sli.statement-correction.{suffix}"
    if source_evidence_id in state.evidence or finding_id in state.findings:
        raise RelationshipRecordingRefused("source correction identity has already been used")
    revision = contents.revision
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
    staged = list(contents.acts) + [evidence_act]
    base = project(tuple(staged), registry)
    admission = apply_contribution_batch(base, contribution_act=contribution_act,
                                         successor_acts=[assertion], registry=registry,
                                         record_id=f"sli.statement-correction.record.{suffix}")
    if admission.terminal_record["phase"] != "completed":
        raise RelationshipRecordingRefused("corrected statement source failed contribution admission")
    committed = revision
    for item in (evidence_act, contribution_act, assertion):
        committed = log.append(item, expected_revision=committed)
    recovered = log.read()
    return {"statement_fact_id": statement_fact_id, "source_finding_id": finding_id,
            "source_evidence_id": source_evidence_id, "revision": recovered.revision,
            "state": project(recovered.acts, registry)}


def withdraw_review_claim(log: ActLog, registry: Any, *, finding_id: str,
                          actor: str, at: str) -> dict[str, Any]:
    """Withdraw one exact claim; its original review evidence remains in history."""
    return withdraw_relationship_claim_durably(
        log, registry, finding_id=finding_id, actor=actor, at=at,
    )
