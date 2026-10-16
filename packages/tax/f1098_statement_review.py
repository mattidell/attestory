"""Finite question and current-answer review for one Form 1098 account."""
from __future__ import annotations

import copy
import json
from typing import Any, Mapping
from pathlib import Path

from packages.derivation.records import RecordStream
from packages.derivation.presentation_projection import PresentationModelError, validate_presentation_model
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import project
from packages.tax.f1098_statement_recording import (
    BUNDLE_ID, F1098RecordingRefused, _questions_for_version,
    STATEMENT_BOX1, TIMING_QUESTIONS, USE_QUESTION, _token,
    answer_f1098_statement_answer_durably, answer_f1098_statement_timing_durably,
    correct_f1098_statement_answer_durably,
    record_f1098_statement_answers_durably,
    withdraw_f1098_statement_answer_durably,
)
from packages.tax.loader import TAX_CONTENT_DIR, load_f1098_circumstances_bundle


class F1098ReviewRefused(ValueError):
    """A review does not describe one current, unambiguous statement."""


QUESTIONS: dict[str, dict[str, Any]] = {
    "owns-the-home": {"question": "Do you own this home?", "help": "This asks about an ownership interest in the home described by this statement.", "labels": {"yes": "Yes, I own it", "no": "No", "cannot-tell": "I can't tell"}},
    "lives-there-most-of-the-time": {"question": "Is this the home where you live most of the time?", "help": "This is about where you live most of the time, not a second-home election.", "labels": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"}},
    "filing-unit-owns-home": {"question": "Do you own this home, or does your spouse if you file jointly?", "help": "Either spouse's sole ownership can satisfy the ownership part for a joint return. This question does not decide whether the filing unit uses this as its main home.", "labels": {"yes": "I own this home, or my spouse does if we file jointly", "no": "I do not own this home, and neither does my spouse if we file jointly", "cannot-tell": "I can't tell whether I own this home, or whether my spouse owns it if we file jointly"}},
    "shared-main-home": {"question": "Is this the main home shared by your filing unit?", "help": "This asks whether this is the filing unit's shared main home. It does not treat either spouse's separate residence as sufficient by itself.", "labels": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"}},
    "home-is-collateral": {"question": "Is this home collateral for the loan?", "help": "The lender can take the home if the loan is not paid.", "labels": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"}},
    "owes-the-loan": {"question": "Do you or your spouse, if you file jointly, owe this loan?", "help": "Either spouse's obligation counts for a joint return.", "labels": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"}},
    "paid-the-interest": {"question": "Who paid the interest reported on this statement?", "help": "For a joint return, include either spouse. “No” means neither spouse paid any and nobody paid any for you. Someone else paying some or all, or your filing unit paying only part, is a separate outside-coverage answer.", "labels": {"yes": "My filing unit paid all of it", "paid-by-others-or-partial": "Someone else paid some or all, or my filing unit paid only part", "no": "Neither spouse paid any, and nobody paid any for us", "cannot-tell": "I can't tell"}},
    "no-one-else-owes-it": {"question": "Does anyone besides you or your spouse, if filing jointly, owe this loan with you?", "help": "A spouse is part of the filing unit, not someone else.", "labels": {"yes": "No one else owes it", "no": "Someone else owes it", "cannot-tell": "I can't tell"}},
    USE_QUESTION: {"question": "What did the borrowed money pay for?", "help": "Choose the account that best describes what happened; the application determines its tax meaning.", "labels": {"bought-the-home": "It bought this home", "unrelated-personal-expense": "It paid a personal expense unrelated to the home", "other": "Something else", "cannot-tell": "I can't tell"}},
    "this-is-the-original-loan": {"question": "Is this the original loan?", "help": "A purchase story alone does not establish that the loan was never refinanced.", "labels": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"}},
    "mortgage-credit-certificate-received": {"question": "Did you receive a mortgage credit certificate for this loan?", "help": "This route does not calculate the certificate credit.", "labels": {"received": "Yes", "not-received": "No", "cannot-tell": "I can't tell"}},
    "loan-timing-relative-to-purchase": {"question": "Was this loan taken out within 90 days before or after buying this home?", "help": "Use when the loan money was released. If an earlier written application could change your answer, choose “I can't tell.”", "labels": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"}},
    "loan-timing-relative-to-building-or-improving": {"question": "Was this loan taken out before you finished building or improving this home, or within 90 days after you finished?", "help": "Include unfinished or paused projects and preparation before physical work began. Use when the loan money was released. If an earlier written application could change your answer, choose “I can't tell.”", "labels": {"yes": "Yes", "no": "No", "cannot-tell": "I can't tell"}},
}


def prepare_f1098_statement_review(
    log: ActLog, registry: Any, *, review_id: str, shown_at: str, bundle_version: str | None = None,
) -> dict[str, Any]:
    """Take an immutable, recognizable snapshot of the unique current statement and answers."""
    contents = log.read()
    if contents.incomplete_tail is not None:
        raise F1098ReviewRefused("ActLog has an incomplete tail")
    state = project(tuple(copy.deepcopy(row) for row in contents.acts), registry)
    current_ids = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state, include_displaced=True)
    statement_rows: list[tuple[str, dict[str, Any]]] = []
    for finding_id, finding in state.findings.items():
        if finding_id not in current_ids:
            continue
        fact = lattice.get(finding.get("fact_id", ""))
        if fact is not None and fact.fact_type_id == STATEMENT_BOX1:
            statement_rows.append((finding_id, finding))
    if len(statement_rows) != 1:
        raise F1098ReviewRefused("the bounded review requires exactly one current Form 1098 box 1 statement")
    box1_finding_id, box1_finding = statement_rows[0]
    box1_fact = lattice[box1_finding["fact_id"]]
    keys = dict(box1_fact.keys)
    if set(keys) != {"payer", "statement", "tax-year"}:
        raise F1098ReviewRefused("current Form 1098 statement identity is incomplete")
    payer = state.fact_state.entities.get(keys["payer"])
    statement = state.fact_state.entities.get(keys["statement"])
    if payer is None or statement is None:
        raise F1098ReviewRefused("current Form 1098 statement entities are unavailable")
    adoption = _bundle_adoption(contents.acts)
    version = adoption["version"] if adoption is not None else (bundle_version or "v1")
    if version not in {"v1", "v2"}:
        raise F1098ReviewRefused("the current mortgage answer vocabulary adoption is unsupported")
    if adoption is not None and bundle_version not in (None, version):
        raise F1098ReviewRefused("the requested review vocabulary conflicts with current adoption")
    bundle = load_f1098_circumstances_bundle(registry, version=version)
    definitions = {row["id"]: row for row in bundle["fact_types"]}
    answers: dict[str, dict[str, Any]] = {}
    selected_questions = _questions_for_version(version)
    for question in sorted(selected_questions | TIMING_QUESTIONS):
        fact_id = fact_id_for(f"tax.us.2025.f1098.{question}", tuple(sorted(keys.items())))
        found = [(fid, row) for fid, row in state.findings.items()
                 if fid in current_ids and row.get("fact_id") == fact_id]
        if len(found) > 1:
            raise F1098ReviewRefused(f"multiple current answers for {question}")
        definition = definitions[f"tax.us.2025.f1098.{question}"]
        description_rows = definition.get("value_schema", {}).get("oneOf", [])
        content_labels = {row.get("const"): row.get("description") for row in description_rows
                          if isinstance(row, dict) and isinstance(row.get("const"), str)
                          and isinstance(row.get("description"), str)}
        labels = content_labels or QUESTIONS[question]["labels"]
        answers[question] = ({"state": "answered", "finding_id": found[0][0], "answer": found[0][1]["value"],
                              "label": labels.get(found[0][1]["value"], str(found[0][1]["value"]))}
                             if found else {"state": "absent", "finding_id": None, "answer": None, "label": "Not answered"})
    use = answers[USE_QUESTION]["answer"]
    timing_relevant = use == "unrelated-personal-expense"
    defaults = _timing_defaults(registry, version)
    for question in TIMING_QUESTIONS:
        answers[question]["relevance"] = "relevant" if timing_relevant else "retained-but-irrelevant"
        if answers[question]["state"] == "absent":
            answers[question]["defaultPolicy"] = {
                **defaults[question], "status": "declared" if adoption == {"id": BUNDLE_ID, "version": version}
                else "proposed-until-bundle-adoption",
            }
            answers[question]["label"] = "Not answered" if timing_relevant else "Not asked for this use"
    return {
        "schema": "tax.f1098.statement-review.v1", "reviewId": review_id, "shownAt": shown_at,
        "bundleVersion": version,
        "revision": contents.revision, "statement": {
            "keys": keys, "payerLabel": payer.entity["label"], "statementLabel": statement.entity["label"],
            "taxYear": keys["tax-year"], "box1": box1_finding["value"], "box1FindingId": box1_finding_id,
        },
        "questions": {q: {**QUESTIONS[q], **answers[q]} for q in sorted(answers)},
        "timingRelevant": timing_relevant, "bundleAdoption": adoption,
    }


def _bundle_adoption(acts: tuple[dict[str, Any], ...]) -> dict[str, Any] | None:
    for act in reversed(acts):
        bundle = act.get("payload", {}).get("bundle", {}) if act.get("kind") == "bundle-adoption" else {}
        if bundle.get("id") == BUNDLE_ID:
            return {"id": bundle["id"], "version": bundle["version"]}
    return None


def _timing_defaults(registry: Any, version: str = "v1") -> dict[str, dict[str, Any]]:
    bundle = load_f1098_circumstances_bundle(registry, version=version)
    declarations = {row["id"]: row for row in bundle["fact_types"]}
    result: dict[str, dict[str, Any]] = {}
    for question in TIMING_QUESTIONS:
        declaration = declarations[f"tax.us.2025.f1098.{question}"]
        ref = declaration["optional_default"]["parameter"]
        filename = ref["id"].removeprefix("tax.us.2025.parameter.")
        parameter = json.loads((TAX_CONTENT_DIR / f"parameter.{filename}.json").read_text("utf-8"))
        if parameter.get("id") != ref["id"] or parameter.get("version") != ref["version"]:
            raise F1098ReviewRefused(f"the selected default parameter {ref['id']}@{ref['version']} is unavailable")
        result[question] = {"parameterId": ref["id"], "parameterVersion": ref["version"],
                            "value": parameter["values"]}
    return result


def _revalidate(log: ActLog, registry: Any, review: Mapping[str, Any]) -> dict[str, Any]:
    selected_version = review.get("bundleVersion", "v1")
    if selected_version not in {"v1", "v2"}:
        raise F1098ReviewRefused("review has no supported selected vocabulary version")
    current = prepare_f1098_statement_review(log, registry,
                                            review_id=str(review.get("reviewId", "revalidation")),
                                            shown_at=str(review.get("shownAt", "")),
                                            bundle_version=str(selected_version))
    if current["revision"] != review.get("revision") or current["statement"] != review.get("statement"):
        raise F1098ReviewRefused("review is stale: statement source or revision changed")
    if current["questions"] != review.get("questions"):
        raise F1098ReviewRefused("review is stale: current answer snapshot changed")
    return current


def save_f1098_statement_review(log: ActLog, registry: Any, review: Mapping[str, Any], *,
                                answers: dict[str, str], submission_id: str,
                                evidence_ids: dict[str, str], actor: str, at: str,
                                bundle_version: str | None = None) -> dict[str, Any]:
    current = _revalidate(log, registry, review)
    selected_version = str(current["bundleVersion"])
    if bundle_version not in (None, selected_version):
        raise F1098ReviewRefused("save-time vocabulary conflicts with the reviewed question set")
    try:
        return record_f1098_statement_answers_durably(
            log, registry, statement_keys=current["statement"]["keys"], answers=answers,
            submission_id=submission_id, evidence_ids=evidence_ids, actor=actor, at=at,
            expected_revision=current["revision"], bundle_version=selected_version,
        )
    except F1098RecordingRefused as exc:
        raise F1098ReviewRefused(str(exc)) from exc


def correct_f1098_statement_review_answer(log: ActLog, registry: Any, review: Mapping[str, Any], *,
                                          question: str, answer: str, submission_id: str,
                                          evidence_id: str, actor: str, at: str) -> dict[str, Any]:
    current = _revalidate(log, registry, review)
    target = current["questions"].get(question)
    if not isinstance(target, dict) or target.get("state") != "answered":
        raise F1098ReviewRefused("correction requires one exact current answer from the review")
    if question in TIMING_QUESTIONS and target.get("relevance") != "relevant":
        raise F1098ReviewRefused("a retained timing answer cannot be corrected while it is irrelevant to the current use")
    try:
        return correct_f1098_statement_answer_durably(
            log, registry, statement_keys=current["statement"]["keys"], question=question, answer=answer,
            predecessor_finding_id=target["finding_id"], submission_id=submission_id, evidence_id=evidence_id,
            actor=actor, at=at, expected_revision=current["revision"],
        )
    except F1098RecordingRefused as exc:
        raise F1098ReviewRefused(str(exc)) from exc


def answer_f1098_statement_review_timing(log: ActLog, registry: Any, review: Mapping[str, Any], *,
                                         question: str, answer: str, submission_id: str,
                                         evidence_id: str, actor: str, at: str) -> dict[str, Any]:
    """Add one timing answer to a saved personal-expense account that left it absent."""
    current = _revalidate(log, registry, review)
    target = current["questions"].get(question)
    if question not in TIMING_QUESTIONS or not isinstance(target, dict) or target.get("state") != "absent":
        raise F1098ReviewRefused("add one timing answer only when that question is currently unanswered")
    if not current["timingRelevant"]:
        raise F1098ReviewRefused("timing questions are available only for personal-expense use")
    try:
        return answer_f1098_statement_timing_durably(
            log, registry, statement_keys=current["statement"]["keys"], question=question, answer=answer,
            submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
            expected_revision=current["revision"],
        )
    except F1098RecordingRefused as exc:
        raise F1098ReviewRefused(str(exc)) from exc


def answer_f1098_statement_review_question(log: ActLog, registry: Any, review: Mapping[str, Any], *,
                                           question: str, answer: str, submission_id: str,
                                           evidence_id: str, actor: str, at: str) -> dict[str, Any]:
    """Add one answer to an absent ordinary question or a timing answer after withdrawal."""
    current = _revalidate(log, registry, review)
    target = current["questions"].get(question)
    if not isinstance(target, dict) or target.get("state") != "absent":
        raise F1098ReviewRefused("answer requires a question that is currently unanswered")
    if question in TIMING_QUESTIONS and not current["timingRelevant"]:
        raise F1098ReviewRefused("timing questions are available only for personal-expense use")
    try:
        return answer_f1098_statement_answer_durably(
            log, registry, statement_keys=current["statement"]["keys"], question=question, answer=answer,
            submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
            expected_revision=current["revision"], bundle_version=str(current["bundleVersion"]),
        )
    except F1098RecordingRefused as exc:
        raise F1098ReviewRefused(str(exc)) from exc


def withdraw_f1098_statement_review_answers(log: ActLog, registry: Any, review: Mapping[str, Any], *,
                                            questions: list[str], submission_id: str,
                                            actor: str, at: str) -> dict[str, Any]:
    current = _revalidate(log, registry, review)
    if not questions or len(set(questions)) != len(questions):
        raise F1098ReviewRefused("withdrawal needs distinct question names")
    findings: list[str] = []
    for question in questions:
        row = current["questions"].get(question)
        if not isinstance(row, dict) or row.get("state") != "answered":
            raise F1098ReviewRefused(f"no current answer to withdraw for {question}")
        findings.append(row["finding_id"])
    try:
        return withdraw_f1098_statement_answer_durably(
            log, registry, current_findings=findings, submission_id=submission_id,
            actor=actor, at=at, expected_revision=current["revision"],
        )
    except F1098RecordingRefused as exc:
        raise F1098ReviewRefused(str(exc)) from exc


def associate_saved_run(presentation: Mapping[str, Any], records: RecordStream, current_revision: int) -> dict[str, Any]:
    """Associate a saved presentation only through its paired durable run record."""
    run_id = presentation.get("runId")
    if not isinstance(run_id, str) or not run_id:
        return {"state": "recalculation-needed", "reason": "saved presentation has no run identity"}
    contents = records.read()
    if contents.incomplete_tail is not None:
        return {"state": "recalculation-needed", "reason": "run record stream has an incomplete tail"}
    matches = [row for row in contents.records if row.get("run_id") == run_id and row.get("phase") == "completed"]
    if len(matches) != 1:
        return {"state": "recalculation-needed", "reason": "saved presentation has no unique completed run record"}
    run_revision = matches[0].get("workspace_revision")
    if not isinstance(run_revision, int) or run_revision != current_revision:
        return {"state": "recalculation-needed", "reason": "saved run was calculated from a different ActLog revision",
                "runRevision": run_revision, "currentRevision": current_revision, "runId": run_id}
    return {"state": "current", "runRevision": run_revision, "currentRevision": current_revision, "runId": run_id}


def review_f1098_statement_with_saved_presentation(
    log: ActLog, registry: Any, presentation_path: Path, records: RecordStream, *,
    review_id: str, shown_at: str,
) -> dict[str, Any]:
    """Reload the saved presentation and show it beside the freshly read account."""
    review = prepare_f1098_statement_review(log, registry, review_id=review_id, shown_at=shown_at)
    try:
        presentation = json.loads(presentation_path.read_text("utf-8"))
        if not isinstance(presentation, dict):
            raise PresentationModelError("saved presentation root must be an object")
        validate_presentation_model(presentation)
    except (OSError, json.JSONDecodeError, PresentationModelError) as exc:
        return {**review, "savedCalculation": None,
                "savedUnresolvedExplanation": None,
                "calculationAssociation": {"state": "recalculation-needed",
                                            "reason": f"saved presentation is unavailable or malformed: {exc}"}}
    association = associate_saved_run(presentation, records, review["revision"])
    explanation = presentation.get("mortgageInterestExplanation")
    current_run = association.get("state") == "current"
    has_explanation = isinstance(explanation, dict)
    expected_keys = review["statement"]["keys"]
    if isinstance(explanation, dict):
        account = explanation["accounts"][0]
        saved_keys = account["statementKeys"]
        if (saved_keys != {"payer": expected_keys["payer"], "statement": expected_keys["statement"],
                           "taxYear": expected_keys["tax-year"]} or
                account["reportedInterest"]["sourceFindingId"] != review["statement"]["box1FindingId"]):
            current_run = False
            association = {"state": "recalculation-needed", "reason": "saved mortgage account does not match the current statement"}
    unresolved: dict[str, Any] | None = None
    if current_run and not has_explanation:
        field = next((row for row in presentation["sections"]
                     if row["field"].get("id") == "tax.us.2025.form.f1098.residence-interest-unresolved"), None)
        if field is not None:
            expected_fact = fact_id_for("tax.us.2025.f1098.box1-mortgage-interest",
                                        tuple(sorted(expected_keys.items())))
            reasons = field["resolved"].get("reasons", [])
            matching = [reason for reason in reasons if isinstance(reason, dict)
                        and reason.get("factId") == expected_fact]
            if len(matching) == 1:
                unresolved = {"statementFactId": expected_fact,
                              "statementLabel": review["statement"]["statementLabel"],
                              "reasons": copy.deepcopy(matching)}
    return {**review,
            "savedCalculation": explanation if current_run and has_explanation else None,
            "savedUnresolvedExplanation": unresolved,
            "savedCalculationState": (
                "current-explanation" if current_run and has_explanation else
                "current-unresolved-explanation" if current_run and unresolved else
                "current-run-without-completed-mortgage-explanation" if current_run else
                "recalculation-needed"
            ),
            "calculationAssociation": association}
