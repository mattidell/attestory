"""Finite review snapshots and guarded operations for mortgage borrowing claims."""
from __future__ import annotations

import copy
from typing import Any, Mapping

from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.f1098_statement_review import QUESTIONS as F1098_QUESTIONS
from packages.tax.mortgage_borrowing_recording import (
    BORROWING_KIND, STATEMENT_BOX1, _CLAIM_TYPES, _QUESTIONS,
    MortgageBorrowingRecordingRefused, clear_mortgage_borrowing_year_durably,
    current_mortgage_payment_comparison_support,
    correct_mortgage_borrowing_claim_durably, record_mortgage_borrowing_claim_durably,
    withdraw_mortgage_borrowing_claim_durably,
)


class MortgageBorrowingReviewRefused(ValueError):
    """The displayed mortgage borrowing snapshot is no longer current."""


_CHOICE_LABELS = {
    "continuing-borrowing": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"},
    "report-inclusion": {"affirmed": "Yes, this form includes it", "denied": "No, it does not", "cannot-tell": "I can't tell"},
    "payment-comparison": {"different-payments": "Yes, all payments are separate from the other report",
                           "copy-or-correction": "No, this is a copy or correction of the other report",
                           "cannot-tell": "I can't tell"},
    "other-secured-home-debt": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"},
    "owes-the-loan": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"},
    "no-one-else-owes-it": {"yes": "No one else owes it", "no": "Someone else owes it", "cannot-tell": "I can't tell"},
    "what-the-money-paid-for": {"bought-the-home": "It bought this home", "unrelated-personal-expense": "It paid an unrelated personal expense", "other": "Something else", "cannot-tell": "I can't tell"},
    "this-is-the-original-loan": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"},
    "mortgage-credit-certificate-received": {"received": "Yes", "not-received": "No", "cannot-tell": "I can't tell"},
}

_QUESTION_HELP = {
    "continuing-borrowing": "This asks whether the forms concern one borrowing you continued to owe when the company collecting payments changed. Whether it is the original loan or a refinance is a separate question.",
    "report-inclusion": "Answer for this exact Form 1098 only.",
    "payment-comparison": "Compare this exact report with the other exact report shown. All payments on both reports must be separate before they can be added; if any overlap or you cannot tell, do not affirm.",
    "annual-ceiling": "Give an amount you are confident the balance did not exceed at any point in 2025. It may be higher than the exact highest balance.",
    "other-secured-home-debt": "Do not count the named borrowing again here. This asks about other debt secured by your main home or a second home.",
    "owes-the-loan": F1098_QUESTIONS["owes-the-loan"]["help"],
    "no-one-else-owes-it": F1098_QUESTIONS["no-one-else-owes-it"]["help"],
    "what-the-money-paid-for": F1098_QUESTIONS["what-the-money-paid-for"]["help"],
    "this-is-the-original-loan": F1098_QUESTIONS["this-is-the-original-loan"]["help"],
    "mortgage-credit-certificate-received": F1098_QUESTIONS["mortgage-credit-certificate-received"]["help"],
}


def prepare_mortgage_borrowing_review(
    log: ActLog, registry: Any, *, review_id: str, shown_at: str,
    borrowing_ref: str | None = None,
) -> dict[str, Any]:
    """Show current borrowing claims and exact current Form 1098 subjects."""
    contents = log.read()
    if contents.incomplete_tail is not None:
        raise MortgageBorrowingReviewRefused("ActLog has an incomplete tail")
    state = project(tuple(copy.deepcopy(row) for row in contents.acts), registry)
    current = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state)
    borrowings = []
    for entity_id, lifecycle in sorted(state.fact_state.entities.items()):
        if lifecycle.status == "current" and lifecycle.entity.get("kind") == BORROWING_KIND:
            if borrowing_ref is None or entity_id == borrowing_ref:
                borrowings.append({"id": entity_id, "label": lifecycle.entity.get("label", entity_id)})
    if borrowing_ref is not None and not any(row["id"] == borrowing_ref for row in borrowings):
        raise MortgageBorrowingReviewRefused("selected borrowing is not a current mortgage reference")
    reports = []
    seen_sources: set[str] = set()
    for finding_id, finding in state.findings.items():
        if finding_id not in current:
            continue
        fact = lattice.get(str(finding.get("fact_id")))
        if fact is None or fact.fact_type_id != STATEMENT_BOX1 or fact.fact_id in seen_sources:
            continue
        seen_sources.add(fact.fact_id)
        keys = dict(fact.keys)
        payer = state.fact_state.entities.get(keys["payer"])
        statement = state.fact_state.entities.get(keys["statement"])
        local_answers = []
        for local_id, local_finding in state.findings.items():
            if local_id not in current:
                continue
            local_fact = lattice.get(str(local_finding.get("fact_id")))
            if local_fact is None or dict(local_fact.keys) != keys:
                continue
            prefix = "tax.us.2025.f1098."
            if not local_fact.fact_type_id.startswith(prefix):
                continue
            question_id = local_fact.fact_type_id.removeprefix(prefix)
            definition = F1098_QUESTIONS.get(question_id)
            if definition is not None:
                local_answers.append({"findingId": local_id, "factType": local_fact.fact_type_id,
                                      "question": definition["question"], "scope": "this exact Form 1098",
                                      "value": local_finding.get("value"),
                                      "label": definition["labels"].get(local_finding.get("value"), str(local_finding.get("value")))})
        reports.append({"keys": keys, "findingId": finding_id, "box1": finding.get("value"),
                        "payerLabel": payer.entity.get("label", keys["payer"]) if payer is not None else keys["payer"],
                        "statementLabel": statement.entity.get("label", keys["statement"]) if statement is not None else keys["statement"],
                        "localAnswers": sorted(local_answers, key=lambda row: row["factType"])})
    claims: list[dict[str, Any]] = []
    for finding_id, finding in state.findings.items():
        if finding_id not in current:
            continue
        fact = lattice.get(str(finding.get("fact_id")))
        if fact is None or fact.fact_type_id not in _CLAIM_TYPES:
            continue
        keys = dict(fact.keys)
        ref = keys.get("borrowing")
        if borrowing_ref is not None and ref != borrowing_ref:
            continue
        if ref is not None and not any(row["id"] == ref for row in borrowings):
            continue
        claim = next((name for name, question in _QUESTIONS.items()
                      if fact.fact_type_id == name or fact.fact_type_id in _claim_types_for_question(name)), None)
        if claim is None:
            continue
        claim_row = {"claim": claim, "question": _QUESTIONS[claim], "findingId": finding_id,
                     "factType": fact.fact_type_id, "keys": keys, "value": finding.get("value")}
        if claim == "payment-comparison":
            evidence_ids = finding.get("evidence_ids")
            evidence_row = state.evidence.get(evidence_ids[0]) if isinstance(evidence_ids, list) and len(evidence_ids) == 1 else None
            evidence = evidence_row.evidence if evidence_row is not None else {}
            content = evidence.get("content", {})
            if isinstance(content.get("peer_statement"), Mapping):
                claim_row["peerScope"] = dict(content["peer_statement"])
        claims.append(claim_row)
    questions = []
    for claim, wording in _QUESTIONS.items():
        question: dict[str, Any] = {
            "claim": claim, "question": wording, "help": _QUESTION_HELP[claim],
            "scope": "one exact report" if claim in {"report-inclusion", "payment-comparison"}
            else "the named borrowing for 2025; shared answers apply once across its linked reports",
        }
        if claim == "annual-ceiling":
            question.update({"inputKind": "nonnegative-number", "minimum": 0,
                             "unanswered": {"state": "absent", "value": None}})
        else:
            question.update({"inputKind": "choice", "choices": [
                {"value": value, "label": label} for value, label in _CHOICE_LABELS[claim].items()]})
        questions.append(question)
    answers = []
    for borrowing in borrowings:
        account_claims = [row for row in claims if row["keys"].get("borrowing") == borrowing["id"]]
        for claim in _QUESTIONS:
            if claim in {"report-inclusion", "payment-comparison"}:
                # ``state`` is still the projection of ``contents.acts``. This
                # review has not staged an act since that fold.
                pair_support = (current_mortgage_payment_comparison_support(
                                    contents.acts, registry, borrowing["id"], state=state)
                                if claim == "payment-comparison" else None)
                for report in reports:
                    report_keys = report["keys"]
                    if not isinstance(report_keys, Mapping):
                        raise MortgageBorrowingReviewRefused("current report identity is malformed")
                    keys = {**dict(report_keys), "borrowing": borrowing["id"]}
                    peer_keys = None
                    if claim == "payment-comparison" and pair_support is not None:
                        pair_reports = pair_support["reports"]
                        full_keys = {**dict(report_keys), "borrowing": borrowing["id"]}
                        own = next((item for item in pair_reports if item["keys"] == full_keys), None)
                        peer = next((item for item in pair_reports if item["keys"] != full_keys), None)
                        if own is None or peer is None:
                            continue
                        peer_keys = {key: peer["keys"][key] for key in ("payer", "statement", "tax-year")}
                    found = [row for row in account_claims if row["claim"] == claim and row["keys"] == keys]
                    if len(found) > 1:
                        raise MortgageBorrowingReviewRefused("multiple current outcomes for one exact report link")
                    answers.append({"claim": claim, "question": _QUESTIONS[claim], "scope": keys,
                                    "state": ("answered" if found else "absent") if claim != "payment-comparison" or pair_support is not None else ("stale" if found else "unavailable"),
                                    "findingId": found[0]["findingId"] if found else None,
                                    "value": found[0]["value"] if found else None,
                                    **({"peerScope": found[0].get("peerScope", peer_keys) if found else peer_keys,
                                        "comparisonSupport": pair_support}
                                       if claim == "payment-comparison" else {})})
            else:
                found = [row for row in account_claims if row["claim"] == claim]
                if len(found) > 1:
                    raise MortgageBorrowingReviewRefused(f"multiple current answers for borrowing claim {claim}")
                answers.append({"claim": claim, "question": _QUESTIONS[claim],
                                "scope": {"borrowing": borrowing["id"], "tax-year": "2025"},
                                "state": "answered" if found else "absent",
                                "findingId": found[0]["findingId"] if found else None,
                                "value": found[0]["value"] if found else None})
    return {"schema": "tax.mortgage-borrowing.review.v1", "reviewId": review_id,
            "shownAt": shown_at, "revision": contents.revision, "borrowings": borrowings,
            "reports": sorted(reports, key=lambda row: tuple(row["keys"][k] for k in ("payer", "statement", "tax-year"))),
            "questions": questions, "answers": answers, "claims": claims}


def _claim_types_for_question(claim: str) -> frozenset[str]:
    from packages.tax import mortgage_borrowing_recording as recording
    if claim in recording._RECOGNITION:
        return frozenset(recording._RECOGNITION[claim].values())
    if claim in recording._INCLUSION:
        return frozenset(recording._INCLUSION[claim].values())
    if claim == "payment-comparison":
        return frozenset(recording._PAYMENT_COMPARISON_OUTCOMES.values())
    if claim == "annual-ceiling":
        return frozenset({recording._CEILING})
    if claim == "other-secured-home-debt":
        return frozenset({recording._OTHER_DEBT})
    if claim in recording._SHARED:
        return frozenset({recording._SHARED[claim][0]})
    return frozenset()


def _revalidate(log: ActLog, registry: Any, review: Mapping[str, Any], borrowing_ref: str) -> dict[str, Any]:
    if review.get("schema") != "tax.mortgage-borrowing.review.v1":
        raise MortgageBorrowingReviewRefused("unsupported borrowing review snapshot")
    try:
        current = prepare_mortgage_borrowing_review(
            log, registry, review_id=str(review.get("reviewId", "revalidation")),
            shown_at=str(review.get("shownAt", "")))
    except MortgageBorrowingReviewRefused:
        raise
    if current["revision"] != review.get("revision"):
        raise MortgageBorrowingReviewRefused("reviewed ActLog revision changed before save")
    shown = review.get("borrowings")
    if not isinstance(shown, list) or not any(
        isinstance(row, Mapping) and row.get("id") == borrowing_ref for row in shown
    ):
        raise MortgageBorrowingReviewRefused("selected borrowing was not shown in this review")
    shown_ids = {row.get("id") for row in shown if isinstance(row, Mapping)}
    current["borrowings"] = [row for row in current["borrowings"] if row["id"] in shown_ids]
    current["claims"] = [row for row in current["claims"]
                         if row.get("keys", {}).get("borrowing") in shown_ids]
    current["answers"] = [row for row in current["answers"]
                          if row.get("scope", {}).get("borrowing") in shown_ids]
    for key in ("borrowings", "reports", "questions", "answers", "claims"):
        if current[key] != review.get(key):
            raise MortgageBorrowingReviewRefused("displayed borrowing review changed before save")
    return current


def record_mortgage_borrowing_review_answer(
    log: ActLog, registry: Any, review: Mapping[str, Any], *, claim: str, borrowing_ref: str,
    value: str | float | int, submission_id: str, evidence_id: str, actor: str, at: str,
    statement_keys: dict[str, str] | None = None, peer_statement_keys: dict[str, str] | None = None,
) -> dict[str, Any]:
    current = _revalidate(log, registry, review, borrowing_ref)
    if claim in {"report-inclusion", "payment-comparison"} and not any(
        isinstance(statement_keys, dict) and row["keys"] == statement_keys
        for row in current["reports"]
    ):
        raise MortgageBorrowingReviewRefused("report claim must select one exact current statement shown in this review")
    comparison_support = None
    if claim == "payment-comparison":
        answer = next((row for row in current["answers"] if row["claim"] == claim and
                       row["scope"].get("borrowing") == borrowing_ref and
                       row["scope"].get("payer") == (statement_keys or {}).get("payer") and
                       row["scope"].get("statement") == (statement_keys or {}).get("statement")), None)
        if answer is None or answer.get("state") == "unavailable" or answer.get("peerScope") != peer_statement_keys:
            raise MortgageBorrowingReviewRefused("payment comparison must select the exact displayed report pair")
        comparison_support = answer.get("comparisonSupport")
        if not isinstance(comparison_support, Mapping):
            raise MortgageBorrowingReviewRefused("payment comparison support is not current and complete")
    try:
        return record_mortgage_borrowing_claim_durably(
            log, registry, claim=claim, borrowing_ref=borrowing_ref, value=value,
            submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
            statement_keys=statement_keys, peer_statement_keys=peer_statement_keys,
            comparison_support=comparison_support, expected_revision=current["revision"])
    except MortgageBorrowingRecordingRefused as exc:
        raise MortgageBorrowingReviewRefused(str(exc)) from exc


def correct_mortgage_borrowing_review_answer(
    log: ActLog, registry: Any, review: Mapping[str, Any], *, claim: str, borrowing_ref: str,
    finding_id: str, value: str | float | int, submission_id: str, evidence_id: str,
    actor: str, at: str, statement_keys: dict[str, str] | None = None,
    peer_statement_keys: dict[str, str] | None = None,
) -> dict[str, Any]:
    current = _revalidate(log, registry, review, borrowing_ref)
    matches = [row for row in current["claims"] if row["claim"] == claim and row["findingId"] == finding_id]
    if len(matches) != 1:
        raise MortgageBorrowingReviewRefused("correction must name one exact current displayed answer")
    if claim in {"report-inclusion", "payment-comparison"} and dict(matches[0]["keys"]) != {**(statement_keys or {}), "borrowing": borrowing_ref, "tax-year": "2025"}:
        raise MortgageBorrowingReviewRefused("correction scope differs from the displayed exact report")
    comparison_support = None
    if claim == "payment-comparison":
        answer = next((row for row in current["answers"] if row["claim"] == claim and
                       row["scope"].get("borrowing") == borrowing_ref and
                       row["scope"].get("payer") == (statement_keys or {}).get("payer") and
                       row["scope"].get("statement") == (statement_keys or {}).get("statement")), None)
        if answer is None or answer.get("peerScope") != peer_statement_keys:
            raise MortgageBorrowingReviewRefused("correction must keep the exact displayed report pair")
        comparison_support = answer.get("comparisonSupport")
    try:
        return correct_mortgage_borrowing_claim_durably(
            log, registry, finding_id=finding_id, claim=claim, borrowing_ref=borrowing_ref,
            value=value, submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
            statement_keys=statement_keys, peer_statement_keys=peer_statement_keys,
            comparison_support=comparison_support, expected_revision=current["revision"])
    except MortgageBorrowingRecordingRefused as exc:
        raise MortgageBorrowingReviewRefused(str(exc)) from exc


def withdraw_mortgage_borrowing_review_answer(
    log: ActLog, registry: Any, review: Mapping[str, Any], *, claim: str, borrowing_ref: str,
    finding_id: str, actor: str, at: str, statement_keys: dict[str, str] | None = None,
    submission_id: str | None = None, evidence_id: str | None = None,
) -> dict[str, Any]:
    current = _revalidate(log, registry, review, borrowing_ref)
    matches = [row for row in current["claims"] if row["claim"] == claim and row["findingId"] == finding_id]
    if len(matches) != 1:
        raise MortgageBorrowingReviewRefused("withdrawal must name one exact current displayed answer")
    peer_statement_keys = None
    if claim == "payment-comparison":
        displayed = next((row for row in current["answers"] if row["claim"] == claim and
                          row["findingId"] == finding_id), None)
        if displayed is None or not isinstance(displayed.get("peerScope"), Mapping):
            raise MortgageBorrowingReviewRefused("withdrawal must retain the exact displayed comparison pair")
        peer_statement_keys = dict(displayed["peerScope"])
    try:
        return withdraw_mortgage_borrowing_claim_durably(
            log, registry, finding_id=finding_id, claim=claim, borrowing_ref=borrowing_ref,
            actor=actor, at=at, statement_keys=statement_keys, peer_statement_keys=peer_statement_keys,
            submission_id=submission_id,
            evidence_id=evidence_id, expected_revision=current["revision"])
    except MortgageBorrowingRecordingRefused as exc:
        raise MortgageBorrowingReviewRefused(str(exc)) from exc


def clear_mortgage_borrowing_review_account(
    log: ActLog, registry: Any, review: Mapping[str, Any], *, borrowing_ref: str,
    actor: str, at: str,
) -> dict[str, Any]:
    current = _revalidate(log, registry, review, borrowing_ref)
    try:
        return clear_mortgage_borrowing_year_durably(
            log, registry, borrowing_ref=borrowing_ref, actor=actor, at=at,
            expected_revision=current["revision"])
    except MortgageBorrowingRecordingRefused as exc:
        raise MortgageBorrowingReviewRefused(str(exc)) from exc
