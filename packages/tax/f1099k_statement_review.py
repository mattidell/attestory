"""Finite circumstance question and current-answer review for Form 1099-K personal item sales."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Mapping

from packages.derivation.presentation_projection import (
    PresentationModelError,
    validate_presentation_model,
)
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import project
from packages.tax.f1099k_statement_recording import (
    ALL_CIRCUMSTANCE_QUESTIONS,
    AMOUNT_QUESTIONS,
    CLOSURE_TYPE,
    F1099KAdoptionResolutionError,
    F1099KRecordingRefused,
    STATEMENT_BOX1A,
    STATEMENT_BOX4,
    _find_current_statement_findings,
    _normalize_question,
    answer_f1099k_statement_answer_durably,
    close_f1099k_family_durably,
    correct_f1099k_statement_answer_durably,
    f1099k_family_version_for_workspace,
    f1099k_family_version_from_package,
    record_f1099k_statement_answers_durably,
    retract_f1099k_statement_durably,
    withdraw_f1099k_statement_answer_durably,
)


class F1099KReviewRefused(ValueError):
    """A review operation cannot proceed because the log or snapshot is invalid or stale."""


QUESTIONS: dict[str, dict[str, Any]] = {
    "covers-only-single-item": {
        "question": "Does this Form 1099-K report payments from only this single item sale?",
        "help": "This route supports one Form 1099-K statement reporting payments from only a single personal item sale.",
        "kind": "categorical",
        "offered": ["yes", "no", "cannot-tell"],
        "labels": {
            "yes": "Yes, only this sale",
            "no": "No, includes other sales/transactions",
            "cannot-tell": "I can't tell",
        },
    },
    "acquired-by-purchase": {
        "question": "How did you acquire this item?",
        "help": "Cost basis rules require knowing how the property was acquired. This route supports purchased items.",
        "kind": "categorical",
        "offered": ["yes", "no", "cannot-tell"],
        "labels": {
            "yes": "I bought it",
            "no": "Acquired by gift, inheritance, or other means",
            "cannot-tell": "I can't tell",
        },
    },
    "primary-purpose-at-acquisition": {
        "question": "What was your main purpose when you acquired or held this item?",
        "help": "Losses on property held for investment or resale are governed by capital-loss or business rules.",
        "kind": "categorical",
        "offered": ["personal-use", "investment-or-profit", "resale-or-inventory", "cannot-tell"],
        "labels": {
            "personal-use": "Used it personally in my everyday life or household",
            "investment-or-profit": "Bought mainly as an investment or to make money",
            "resale-or-inventory": "Acquired or held for resale or as inventory",
            "cannot-tell": "I can't tell",
        },
    },
    "exclusive-personal-use": {
        "question": "Did you use this item exclusively for personal purposes without business or rental use?",
        "help": "Business or rental use is subject to depreciation recapture and cannot use this personal loss route.",
        "kind": "categorical",
        "offered": ["yes", "no", "cannot-tell"],
        "labels": {
            "yes": "Yes, solely personal use",
            "no": "No, used for business or rental",
            "cannot-tell": "I can't tell",
        },
    },
    "digital-asset-involvement": {
        "question": "Was this item a digital asset (such as cryptocurrency or NFT)?",
        "help": "Digital assets must be reported on Form 8949 and are outside the scope of this route.",
        "kind": "categorical",
        "offered": ["no", "yes", "cannot-tell"],
        "labels": {
            "no": "No",
            "yes": "Yes",
            "cannot-tell": "I can't tell",
        },
    },
    "agreed-item-price": {
        "question": "What was the agreed sale price paid by the buyer?",
        "help": "The agreed selling price before platform deductions or additions.",
        "kind": "amount",
        "offered": ["cannot-tell"],
        "labels": {
            "cannot-tell": "I can't tell",
        },
    },
    "shipping-arrangement": {
        "question": "How was shipping handled for this sale?",
        "help": "Identifies whether shipping was handled by the platform or paid directly by the seller.",
        "kind": "categorical",
        "offered": ["platform-pass-through", "seller-received-shipping", "none", "cannot-tell"],
        "labels": {
            "platform-pass-through": "Platform kept shipping / provided label",
            "seller-received-shipping": "I received shipping and bought label",
            "none": "No buyer shipping charged / local pickup",
            "cannot-tell": "I can't tell",
        },
    },
    "platform-fees": {
        "question": "What selling fees did the platform deduct?",
        "help": "Platform commission, payment processing, and transaction fees.",
        "kind": "amount",
        "offered": ["cannot-tell"],
        "labels": {
            "cannot-tell": "I can't tell",
        },
    },
    "seller-paid-shipping": {
        "question": "What did you pay to ship the item, including postage and shipping labels?",
        "help": "Include postage, shipping labels, and shipping costs you paid, including labels bought with shipping money you received from the buyer. Do not include shipping labels provided and kept by the platform.",
        "kind": "amount",
        "offered": ["cannot-tell"],
        "labels": {
            "cannot-tell": "I can't tell",
        },
    },
    "sales-tax-collected-by-platform": {
        "question": "What sales tax did the platform collect from the buyer?",
        "help": "Sales tax included in Box 1a that was collected and remitted by the platform.",
        "kind": "amount",
        "offered": ["cannot-tell"],
        "labels": {
            "cannot-tell": "I can't tell",
        },
    },
    "refund-amount": {
        "question": "Did you issue any refund to the buyer?",
        "help": "Refunds given back to the buyer that reduce the amount realized.",
        "kind": "amount",
        "offered": ["cannot-tell"],
        "labels": {
            "cannot-tell": "I can't tell",
        },
    },
    "buyer-paid-shipping": {
        "question": "What shipping did the buyer pay that was included in Box 1a?",
        "help": "Buyer-paid shipping charges included in the Box 1a gross amount, whether the platform kept the money or sent it to you.",
        "kind": "amount",
        "offered": ["cannot-tell"],
        "labels": {
            "cannot-tell": "I can't tell",
        },
    },
    "cost-basis-known": {
        "question": "Do you know what you originally paid to purchase the item?",
        "help": "You must know your cost basis to establish whether a sale resulted in a gain or loss.",
        "kind": "categorical",
        "offered": ["yes", "cannot-tell"],
        "labels": {
            "yes": "Yes, I know what I paid",
            "cannot-tell": "I can't tell",
        },
    },
    "purchase-cost": {
        "question": "What did you pay to purchase the item, including sales tax and delivery?",
        "help": "Original purchase price, sales tax, delivery charges, and initial installation.",
        "kind": "amount",
        "offered": ["cannot-tell"],
        "labels": {
            "cannot-tell": "I can't tell",
        },
    },
    "lasting-improvements-or-adjustments": {
        "question": "Did you make lasting improvements to the item, receive manufacturer rebates, or receive insurance/casualty payouts?",
        "help": "Capital improvements or basis adjustments under 26 U.S.C. § 1016.",
        "kind": "categorical",
        "offered": ["no", "yes", "cannot-tell"],
        "labels": {
            "no": "No",
            "yes": "Yes",
            "cannot-tell": "I can't tell",
        },
    },
}


def _format_label(question: str, value: Any) -> str:
    if value is None:
        return "Not answered"
    q_meta = QUESTIONS.get(question, {})
    if q_meta.get("kind") == "amount":
        if value == "cannot-tell":
            return "I can't tell"
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return f"${float(value):,.2f}"
        return str(value)
    labels = q_meta.get("labels", {})
    return str(labels.get(str(value), str(value)))


def prepare_f1099k_statement_review(
    log: ActLog,
    registry: Any,
    *,
    review_id: str,
    shown_at: str,
    statement_keys: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Take an immutable snapshot of one Form 1099-K statement and its circumstance answers."""
    review, _state = _prepare_f1099k_statement_review_impl(
        log, registry, review_id=review_id, shown_at=shown_at, statement_keys=statement_keys,
    )
    return review


def _prepare_f1099k_statement_review_impl(
    log: ActLog,
    registry: Any,
    *,
    review_id: str,
    shown_at: str,
    statement_keys: dict[str, str] | None = None,
) -> tuple[dict[str, Any], Any]:
    """Build the review snapshot; also return the state folded for it.

    ``prepare_f1099k_statement_review`` discards the state and keeps its own
    one-return signature. ``_revalidate`` uses this directly so the matching
    ``*_durably`` write in the same review-save operation can reuse the fold
    instead of re-projecting the same revision.
    """
    contents = log.read()
    if contents.incomplete_tail is not None:
        raise F1099KReviewRefused("ActLog has an incomplete tail")
    state = project(tuple(copy.deepcopy(row) for row in contents.acts), registry)
    current_ids = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state, include_displaced=True)

    statement_rows = _find_current_statement_findings(state)
    if not statement_rows:
        closure_matches = [
            (fid, f)
            for fid, f in state.findings.items()
            if fid in current_ids
            and f.get("fact_id") in lattice
            and lattice[f["fact_id"]].fact_type_id == CLOSURE_TYPE
            and f.get("value") is True
        ]
        if closure_matches:
            return {
                "schema": "tax.f1099k.statement-review.v1",
                "reviewId": review_id,
                "shownAt": shown_at,
                "revision": contents.revision,
                "closedEmpty": True,
                "statement": None,
                "questions": {},
            }, state
        raise F1099KReviewRefused("no Form 1099-K statement found to review")

    if statement_keys is not None:
        target = tuple(sorted(statement_keys.items()))
        matching = [row for row in statement_rows if tuple(sorted(row[2].items())) == target]
        if len(matching) != 1:
            raise F1099KReviewRefused(f"statement with keys {statement_keys} is not among current statements")
        box1a_fid, box1a_finding, keys = matching[0]
    else:
        if len(statement_rows) != 1:
            raise F1099KReviewRefused(
                "more than one Form 1099-K statement exists; specify statement_keys to select a statement"
            )
        box1a_fid, box1a_finding, keys = statement_rows[0]

    payer_entity = state.fact_state.entities.get(keys["payer"])
    statement_entity = state.fact_state.entities.get(keys["statement"])
    payer_label = payer_entity.entity["label"] if payer_entity else "Platform"
    stmt_label = statement_entity.entity["label"] if statement_entity else "Form 1099-K"

    # Box 4 finding
    box4_fact_id = fact_id_for(STATEMENT_BOX4, tuple(sorted(keys.items())))
    box4_match = [
        (fid, row) for fid, row in state.findings.items()
        if fid in current_ids and row.get("fact_id") == box4_fact_id
    ]
    box4_val = float(box4_match[0][1]["value"]) if box4_match else None
    box4_fid = box4_match[0][0] if box4_match else None

    # Circumstance answers
    answers: dict[str, dict[str, Any]] = {}
    for q in sorted(ALL_CIRCUMSTANCE_QUESTIONS):
        fact_id = fact_id_for(f"tax.us.2025.f1099k.{q}", tuple(sorted(keys.items())))
        found = [
            (fid, row) for fid, row in state.findings.items()
            if fid in current_ids and row.get("fact_id") == fact_id
        ]
        if len(found) > 1:
            raise F1099KReviewRefused(f"multiple current answers found for {q}")

        q_info = copy.deepcopy(QUESTIONS[q])
        if found:
            cur_fid, cur_row = found[0]
            val = cur_row["value"]
            answers[q] = {
                **q_info,
                "state": "answered",
                "finding_id": cur_fid,
                "answer": val,
                "label": _format_label(q, val),
            }
        else:
            answers[q] = {
                **q_info,
                "state": "absent",
                "finding_id": None,
                "answer": None,
                "label": "Not answered",
            }

    return {
        "schema": "tax.f1099k.statement-review.v1",
        "reviewId": review_id,
        "shownAt": shown_at,
        "revision": contents.revision,
        "statement": {
            "keys": keys,
            "payerLabel": payer_label,
            "statementLabel": stmt_label,
            "taxYear": keys["tax-year"],
            "box1a": box1a_finding["value"],
            "box1aFindingId": box1a_fid,
            "box4": box4_val,
            "box4FindingId": box4_fid,
        },
        "questions": answers,
    }, state


def _revalidate(log: ActLog, registry: Any, review: Mapping[str, Any]) -> tuple[dict[str, Any], Any]:
    """Refuse a stale review; return the refreshed review and its folded state.

    The state is the exact fold of the log revision just confirmed current,
    for the caller to pass into the matching ``*_durably`` write.
    """
    if review.get("closedEmpty"):
        current, state = _prepare_f1099k_statement_review_impl(
            log,
            registry,
            review_id=str(review.get("reviewId", "revalidation")),
            shown_at=str(review.get("shownAt", "")),
        )
        if current["revision"] != review.get("revision") or not current.get("closedEmpty"):
            raise F1099KReviewRefused("review is stale: closed-empty status or ActLog revision changed")
        return current, state
    statement_info = review.get("statement")
    if not isinstance(statement_info, dict) or "keys" not in statement_info:
        raise F1099KReviewRefused("review statement information is missing or malformed")
    keys = statement_info["keys"]
    current, state = _prepare_f1099k_statement_review_impl(
        log,
        registry,
        review_id=str(review.get("reviewId", "revalidation")),
        shown_at=str(review.get("shownAt", "")),
        statement_keys=keys,
    )
    if current["revision"] != review.get("revision") or current["statement"] != review.get("statement"):
        raise F1099KReviewRefused("review is stale: statement source or ActLog revision changed")
    if current["questions"] != review.get("questions"):
        raise F1099KReviewRefused("review is stale: current circumstance answer snapshot changed")
    return current, state


def save_f1099k_statement_review(
    log: ActLog,
    registry: Any,
    review: Mapping[str, Any],
    *,
    answers: dict[str, Any],
    submission_id: str,
    evidence_ids: dict[str, str],
    actor: str,
    at: str,
) -> dict[str, Any]:
    """Save initial circumstance answers after revalidating against the log."""
    current, state = _revalidate(log, registry, review)
    try:
        return record_f1099k_statement_answers_durably(
            log,
            registry,
            statement_keys=current["statement"]["keys"],
            answers=answers,
            submission_id=submission_id,
            evidence_ids=evidence_ids,
            actor=actor,
            at=at,
            expected_revision=current["revision"],
            _state=state,
        )
    except F1099KRecordingRefused as exc:
        raise F1099KReviewRefused(str(exc)) from exc


def correct_f1099k_statement_review_answer(
    log: ActLog,
    registry: Any,
    review: Mapping[str, Any],
    *,
    question: str,
    answer: Any,
    submission_id: str,
    evidence_id: str,
    actor: str,
    at: str,
) -> dict[str, Any]:
    """Correct one circumstance answer after revalidating against the log."""
    current, state = _revalidate(log, registry, review)
    norm_q = _normalize_question(question)
    target = current["questions"].get(norm_q)
    if not isinstance(target, dict) or target.get("state") != "answered":
        raise F1099KReviewRefused(f"correction requires an exact current answered question in review: {norm_q}")
    try:
        return correct_f1099k_statement_answer_durably(
            log,
            registry,
            statement_keys=current["statement"]["keys"],
            question=norm_q,
            answer=answer,
            predecessor_finding_id=target["finding_id"],
            submission_id=submission_id,
            evidence_id=evidence_id,
            actor=actor,
            at=at,
            expected_revision=current["revision"],
            _state=state,
        )
    except F1099KRecordingRefused as exc:
        raise F1099KReviewRefused(str(exc)) from exc


def answer_f1099k_statement_review_question(
    log: ActLog,
    registry: Any,
    review: Mapping[str, Any],
    *,
    question: str,
    answer: Any,
    submission_id: str,
    evidence_id: str,
    actor: str,
    at: str,
) -> dict[str, Any]:
    """Add one answer to a currently unanswered question after revalidating against the log."""
    current, state = _revalidate(log, registry, review)
    norm_q = _normalize_question(question)
    target = current["questions"].get(norm_q)
    if not isinstance(target, dict) or target.get("state") != "absent":
        raise F1099KReviewRefused(f"question {norm_q!r} is already answered; use correction instead")
    try:
        return answer_f1099k_statement_answer_durably(
            log,
            registry,
            statement_keys=current["statement"]["keys"],
            question=norm_q,
            answer=answer,
            submission_id=submission_id,
            evidence_id=evidence_id,
            actor=actor,
            at=at,
            expected_revision=current["revision"],
            _state=state,
        )
    except F1099KRecordingRefused as exc:
        raise F1099KReviewRefused(str(exc)) from exc


def withdraw_f1099k_statement_review_answers(
    log: ActLog,
    registry: Any,
    review: Mapping[str, Any],
    *,
    questions: list[str],
    submission_id: str,
    actor: str,
    at: str,
) -> dict[str, Any]:
    """Withdraw one or more answers after revalidating against the log."""
    current, state = _revalidate(log, registry, review)
    if not questions or len(set(questions)) != len(questions):
        raise F1099KReviewRefused("withdrawal requires distinct question names")
    finding_ids: list[str] = []
    for q in questions:
        norm_q = _normalize_question(q)
        target = current["questions"].get(norm_q)
        if not isinstance(target, dict) or target.get("state") != "answered":
            raise F1099KReviewRefused(f"no current answer to withdraw for {norm_q}")
        finding_ids.append(target["finding_id"])
    try:
        return withdraw_f1099k_statement_answer_durably(
            log,
            registry,
            current_findings=finding_ids,
            submission_id=submission_id,
            actor=actor,
            at=at,
            expected_revision=current["revision"],
            _state=state,
        )
    except F1099KRecordingRefused as exc:
        raise F1099KReviewRefused(str(exc)) from exc


def retract_f1099k_statement_review(
    log: ActLog,
    registry: Any,
    review: Mapping[str, Any],
    *,
    submission_id: str,
    actor: str,
    at: str,
    evidence_id: str | None = None,
) -> dict[str, Any]:
    """Retract (remove) the statement reviewed in the snapshot after revalidating against the log."""
    current, state = _revalidate(log, registry, review)
    stmt = current.get("statement")
    if not stmt or not isinstance(stmt, Mapping):
        raise F1099KReviewRefused("review does not have an active statement to remove")
    keys = stmt["keys"]
    try:
        return retract_f1099k_statement_durably(
            log,
            registry,
            submission_id=submission_id,
            statement_keys=keys,
            actor=actor,
            at=at,
            expected_revision=current["revision"],
            tax_year=keys.get("tax-year", "2025"),
            evidence_id=evidence_id,
            _state=state,
        )
    except F1099KRecordingRefused as exc:
        raise F1099KReviewRefused(str(exc)) from exc


def associate_saved_run(
    presentation: Mapping[str, Any],
    records: RecordStream,
    current_revision: int,
) -> dict[str, Any]:
    """Associate a saved presentation with the durable run record and current revision."""
    run_id = presentation.get("runId")
    if not isinstance(run_id, str) or not run_id:
        return {"state": "recalculation-needed", "reason": "saved presentation has no run identity"}
    contents = records.read()
    if contents.incomplete_tail is not None:
        return {"state": "recalculation-needed", "reason": "run record stream has an incomplete tail"}
    matches = [
        row for row in contents.records
        if row.get("run_id") == run_id and row.get("phase") == "completed"
    ]
    if len(matches) != 1:
        return {"state": "recalculation-needed", "reason": "saved presentation has no unique completed run record"}
    run_revision = matches[0].get("workspace_revision")
    if not isinstance(run_revision, int) or run_revision != current_revision:
        return {
            "state": "recalculation-needed",
            "reason": "saved run was calculated from a different ActLog revision",
            "runRevision": run_revision,
            "currentRevision": current_revision,
            "runId": run_id,
        }
    return {
        "state": "current",
        "runRevision": run_revision,
        "currentRevision": current_revision,
        "runId": run_id,
    }


def review_f1099k_statement_with_saved_presentation(
    log: ActLog,
    registry: Any,
    presentation_path: Path,
    records: RecordStream,
    *,
    review_id: str,
    shown_at: str,
    statement_keys: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Reload the saved presentation and show calculation or unresolved explanation beside the review."""
    review = prepare_f1099k_statement_review(
        log, registry, review_id=review_id, shown_at=shown_at, statement_keys=statement_keys,
    )
    try:
        presentation = json.loads(presentation_path.read_text("utf-8"))
        if not isinstance(presentation, dict):
            raise PresentationModelError("saved presentation root must be an object")
        validate_presentation_model(presentation)
    except (OSError, json.JSONDecodeError, PresentationModelError) as exc:
        return {
            **review,
            "savedCalculation": None,
            "savedUnresolvedExplanation": None,
            "calculationAssociation": {
                "state": "recalculation-needed",
                "reason": f"saved presentation is unavailable or malformed: {exc}",
            },
            "savedCalculationState": "recalculation-needed",
        }

    association = associate_saved_run(presentation, records, review["revision"])
    is_current = association.get("state") == "current"

    if not is_current:
        return {
            **review,
            "savedCalculation": None,
            "savedUnresolvedExplanation": None,
            "calculationAssociation": association,
            "savedCalculationState": "recalculation-needed",
        }

    sections = presentation.get("sections", [])
    top_entry_field = next(
        (s for s in sections if (s.get("field") or {}).get("id") == "tax.us.2025.schedule1.top-entry.form-field"),
        None,
    )
    unresolved_field = next(
        (s for s in sections if (s.get("field") or {}).get("id") == "tax.us.2025.form.f1099k.unresolved.form-field"),
        None,
    )

    top_disp = ((top_entry_field or {}).get("resolved") or {}).get("disposition") if top_entry_field else None
    top_val = ((top_entry_field or {}).get("resolved") or {}).get("value") if top_entry_field else None

    unres_resolved = (unresolved_field or {}).get("resolved") or {} if unresolved_field else {}
    unres_disp = unres_resolved.get("disposition") if unresolved_field else None
    reasons = unres_resolved.get("reasons", []) if unresolved_field else []
    f1099k_expl = presentation.get("f1099kStatementExplanation")
    is_legacy_unkeyed = (
        isinstance(f1099k_expl, Mapping)
        and "computation" in f1099k_expl
        and "assumptions" in f1099k_expl
    )
    if is_legacy_unkeyed:
        contents = log.read()
        cur_state = project(tuple(copy.deepcopy(row) for row in contents.acts), registry)
        current_stmts = _find_current_statement_findings(cur_state)
        if len(current_stmts) > 1:
            return {
                **review,
                "savedCalculation": None,
                "savedUnresolvedExplanation": None,
                "calculationAssociation": {
                    "state": "recalculation-needed",
                    "reason": "legacy unkeyed presentation incompatible with multiple statements",
                },
                "savedCalculationState": "recalculation-needed",
            }

    stmt_info = review.get("statement") or {}
    stmt_keys = stmt_info.get("keys", {})
    # An explanation belongs to this statement only when its recorded statementKeys
    # equal the statement's full keys exactly. Entry keys and entity ids are never
    # used to pick an explanation, since distinct statements can share an entity id.
    # The one remaining read is the legacy unkeyed single-statement shape.
    target_expl: Mapping[str, Any] | None = None
    if isinstance(f1099k_expl, Mapping):
        if is_legacy_unkeyed:
            target_expl = f1099k_expl
        else:
            exact = [
                v for v in f1099k_expl.values()
                if isinstance(v, Mapping) and v.get("statementKeys") == stmt_keys
            ]
            if len(exact) == 1:
                target_expl = exact[0]

    comp = target_expl.get("computation") if target_expl is not None else None
    assumptions = target_expl.get("assumptions", "none") if target_expl is not None else "none"

    # Missing output: no top-entry or reason result in the saved run; this is not reported as either supported or unresolved
    if top_entry_field is None and unresolved_field is None:
        saved_missing = {
            "status": "missing-output",
            "sentence": "No Form 1099-K top-entry or reason result was produced by the saved run.",
            "statementKeys": stmt_keys,
            "assumptions": assumptions,
            "computation": comp,
        }
        return {
            **review,
            "savedCalculation": None,
            "savedUnresolvedExplanation": None,
            "savedMissingOutput": saved_missing,
            "calculationAssociation": association,
            "savedCalculationState": "current-missing-output",
            "savedState": "missing-output",
        }

    # 1. Closed-empty zero: the person said no Form 1099-K, so there is no statement and a $0 entry
    if review.get("closedEmpty") or review.get("statement") is None:
        if (
            top_disp in ("published_value", "published", "closure_backed_zero", "computed_zero")
            and float(top_val or 0) == 0.0
            and unres_disp != "blocked"
        ):
            closure_explain = (
                ((top_entry_field or {}).get("field") or {}).get("dispositions", {}).get("closure_backed_zero", {}).get("explain")
                or ((top_entry_field or {}).get("field") or {}).get("dispositions", {}).get(top_disp or "", {}).get("explain")
                or "No Form 1099-K statements were received for 2025."
            )
            saved_calc = {
                "status": "closed-empty-zero",
                "box1a": 0.0,
                "sentence": closure_explain,
                "fieldId": "tax.us.2025.schedule1.top-entry.form-field",
                "assumptions": "none",
                "computation": None,
            }
            return {
                **review,
                "savedCalculation": saved_calc,
                "savedUnresolvedExplanation": None,
                "savedMissingOutput": None,
                "calculationAssociation": association,
                "savedCalculationState": "current-closed-empty-zero",
                "savedState": "closed-empty-zero",
            }

    # 2. Supported loss (Route 2 snapshot: statement's own box1a from review snapshot)
    local_reason = target_expl.get("reason") if target_expl is not None else None
    is_supported_loss = (
        local_reason == "supported-loss"
        or (
            local_reason is None
            and top_disp in ("published_value", "published", "computed_zero")
            and top_val is not None
            and unres_disp != "blocked"
            and not reasons
        )
    )
    if is_supported_loss:
        # The statement's own result is local. Whether its Box 1a was entered on
        # Schedule 1 is the published top-entry disposition's answer, not the local
        # reason's: a blocked or missing top entry means nothing was entered.
        top_entered = top_disp in ("published_value", "published", "computed_zero") and top_val is not None
        if top_entered:
            top_explain = (
                ((top_entry_field or {}).get("field") or {}).get("dispositions", {}).get("published_value", {}).get("explain", "")
                or "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."
            )
        else:
            top_explain = (
                "This sale resulted in a nondeductible personal loss. The Schedule 1 top entry for Form 1099-K "
                "is not resolved, so this statement's Box 1a gross amount has not been added to it."
            )
        own_box1a = float(stmt_info.get("box1a", top_val or 0.0))
        saved_calc = {
            "status": "supported-loss",
            "reason": "supported-loss",
            "box1a": own_box1a,
            "sentence": top_explain,
            "fieldId": "tax.us.2025.schedule1.top-entry.form-field",
            "topEntryDisposition": top_disp,
            "assumptions": assumptions,
            "computation": comp,
        }
        return {
            **review,
            "savedCalculation": saved_calc,
            "savedUnresolvedExplanation": None,
            "savedMissingOutput": None,
            "calculationAssociation": association,
            "savedCalculationState": "current-supported-loss",
            "savedState": "supported-loss",
        }

    # 3. Actually unresolved: a named stop with its reason sentence and the income sentence
    is_unresolved = (
        (target_expl is not None and (target_expl.get("reason") != "supported-loss" or target_expl.get("disposition") == "blocked"))
        or unres_disp == "blocked"
        or len(reasons) > 0
    )
    if is_unresolved:
        # A reason names a statement by the full identity keys carried in its fact
        # id. Match those keys exactly; never by entity id or display label, and
        # never fall back to another statement's reasons. A reason whose fact id
        # names no statement is return-level and applies to every statement.
        own_key_segment = fact_id_for(STATEMENT_BOX1A, tuple(sorted(stmt_keys.items()))).partition("|")[2]

        def _reason_applies(reason: Any) -> bool:
            if not isinstance(reason, dict):
                return False
            reason_fact_id = reason.get("factId")
            if not reason_fact_id:
                return True
            segment = str(reason_fact_id).partition("|")[2]
            if not any(token.startswith("statement=") for token in segment.split(",")):
                return True
            return segment == own_key_segment

        matching_reasons = [r for r in reasons if _reason_applies(r)]

        reason_sentences = [r["sentence"] for r in matching_reasons if isinstance(r, dict) and "sentence" in r]
        unres_explain = (
            ((unresolved_field or {}).get("field") or {}).get("dispositions", {}).get("blocked", {}).get("explain", "")
            or "This Form 1099-K statement requires further review."
        )
        saved_unres: dict[str, Any] = {
            "status": "unresolved",
            "statementKeys": stmt_keys,
            "incomeSentence": unres_explain,
            "reasons": copy.deepcopy(matching_reasons),
            "reasonSentences": reason_sentences,
            "fieldId": "tax.us.2025.form.f1099k.unresolved.form-field",
            "assumptions": assumptions,
            "computation": comp,
        }
        if target_expl is not None:
            if "reason" in target_expl:
                saved_unres["reason"] = target_expl["reason"]
            if target_expl.get("disposition") == "blocked":
                saved_unres["code"] = target_expl.get("code")
                saved_unres["missing"] = target_expl.get("missing")
        return {
            **review,
            "savedCalculation": None,
            "savedUnresolvedExplanation": saved_unres,
            "savedMissingOutput": None,
            "calculationAssociation": association,
            "savedCalculationState": "current-unresolved-explanation",
            "savedState": "actually-unresolved",
        }

    # 4. Missing output: no top-entry or reason result in the saved run; this is not reported as either supported or unresolved
    saved_missing = {
        "status": "missing-output",
        "sentence": "No Form 1099-K top-entry or reason result in the saved run.",
        "assumptions": assumptions,
        "computation": comp,
    }
    return {
        **review,
        "savedCalculation": None,
        "savedUnresolvedExplanation": None,
        "savedMissingOutput": saved_missing,
        "calculationAssociation": association,
        "savedCalculationState": "current-missing-output",
        "savedState": "missing-output",
    }
