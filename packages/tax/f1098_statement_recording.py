"""Bounded evidence-backed answers for one recorded Form 1098 statement.

This module records ordinary circumstances on the existing ``payer``,
``statement`` and ``tax-year`` identity. It has no calculation, package
adoption, or subject-change policy.
"""
from __future__ import annotations

import copy
import hashlib
from typing import AbstractSet, Any, Sequence

from packages.kernel.act_log import ActLog, ActLogError, LogContents
from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import apply_act, project
from packages.tax.loader import load_f1098_circumstances_bundle


BUNDLE_ID = "tax.us.2025.f1098-successor.vocabulary"
BUNDLE_VERSION = "v1"
SUPPORTED_BUNDLE_VERSIONS = frozenset({"v1", "v2"})
ANSWER_EVIDENCE_KIND = "tax.mortgage.f1098-statement-answer"
STATEMENT_BOX1 = "tax.us.2025.f1098.box1-mortgage-interest"
TIMING_QUESTIONS = frozenset({
    "loan-timing-relative-to-purchase",
    "loan-timing-relative-to-building-or-improving",
})
USE_QUESTION = "what-the-money-paid-for"
PERSONAL_EXPENSE = "unrelated-personal-expense"
ORDINARY_QUESTIONS = frozenset({
    "owns-the-home", "lives-there-most-of-the-time", "home-is-collateral", "owes-the-loan",
    "paid-the-interest", "no-one-else-owes-it", USE_QUESTION, "this-is-the-original-loan",
    "mortgage-credit-certificate-received",
})
V2_ORDINARY_QUESTIONS = (ORDINARY_QUESTIONS - {
    "owns-the-home", "lives-there-most-of-the-time",
}) | {"filing-unit-owns-home", "shared-main-home"}


def _questions_for_version(version: str) -> frozenset[str]:
    if version == "v1":
        return ORDINARY_QUESTIONS
    if version == "v2":
        return V2_ORDINARY_QUESTIONS
    raise F1098RecordingRefused("the adopted mortgage answer vocabulary is unsupported")


class F1098RecordingRefused(ValueError):
    """A reviewed answer operation cannot be admitted to the current log."""


def _require_provenance(submission_id: str, actor: str, at: str) -> None:
    if not all(isinstance(value, str) and value.strip() for value in (submission_id, actor, at)):
        raise F1098RecordingRefused("submission identity, actor and time are required")


def _token(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def _act(index: int, kind: str, payload: dict[str, Any], actor: str, at: str, suffix: str) -> dict[str, Any]:
    return {"schema": "act.v1", "act_id": f"f1098.answer.{suffix}.{index}", "kind": kind,
            "actor": actor, "at": at, "committed_against": index, "payload": payload}


def _current_finding(state: Any, fact_id: str, current_ids: AbstractSet[str]) -> tuple[str, dict[str, Any]] | None:
    rows = [(fid, row) for fid, row in state.findings.items()
            if fid in current_ids and row.get("fact_id") == fact_id]
    if len(rows) > 1:
        raise F1098RecordingRefused("more than one current finding exists for an answer")
    return rows[0] if rows else None


def _read_for_save(log: ActLog, expected_revision: int) -> LogContents:
    before = log.read()
    if before.incomplete_tail is not None:
        raise F1098RecordingRefused("ActLog has an incomplete tail")
    if before.revision != expected_revision:
        raise F1098RecordingRefused("reviewed ActLog revision changed before save")
    return before


def _adopted_bundle_version(staged: list[dict[str, Any]]) -> str | None:
    for row in reversed(staged):
        bundle = row.get("payload", {}).get("bundle", {}) if row.get("kind") == "bundle-adoption" else {}
        if bundle.get("id") == BUNDLE_ID:
            return bundle.get("version")
    return None


def _ensure_bundle(
    staged: list[dict[str, Any]], registry: Any, actor: str, at: str, suffix: str,
    requested_version: str | None = None,
) -> None:
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    adopted = _adopted_bundle_version(staged)
    version = adopted or requested_version or BUNDLE_VERSION
    if version not in SUPPORTED_BUNDLE_VERSIONS or (adopted is not None and requested_version not in (None, adopted)):
        raise F1098RecordingRefused("the selected mortgage answer vocabulary is unsupported or would downgrade adoption")
    selected_ownership = ("tax.us.2025.f1098.filing-unit-owns-home" if version == "v2"
                          else "tax.us.2025.f1098.owns-the-home")
    if selected_ownership in state.fact_state.fact_types:
        if adopted != version:
            raise F1098RecordingRefused("the selected mortgage answer vocabulary conflicts with current adoption")
        return
    bundle = load_f1098_circumstances_bundle(registry, version=version)
    if bundle.get("id") != BUNDLE_ID or bundle.get("version") != version:
        raise F1098RecordingRefused(f"the selected circumstance answer bundle {version} is unavailable")
    act = _act(len(staged), "bundle-adoption", {"bundle": bundle}, actor, at, suffix)
    staged.append(act)


def _require_selected_bundle(staged: list[dict[str, Any]]) -> None:
    latest = next((row.get("payload", {}).get("bundle", {}) for row in reversed(staged)
                   if row.get("kind") == "bundle-adoption" and
                   row.get("payload", {}).get("bundle", {}).get("id") == BUNDLE_ID), None)
    if latest is None or latest.get("version") not in SUPPORTED_BUNDLE_VERSIONS:
        raise F1098RecordingRefused("the current mortgage answer vocabulary is not an adopted supported version")


def _require_current_statement(state: Any, keys: dict[str, str]) -> None:
    current = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state, include_displaced=True)
    sources = [(fid, finding) for fid, finding in state.findings.items()
               if fid in current and finding.get("fact_id") in lattice
               and lattice[finding["fact_id"]].fact_type_id == STATEMENT_BOX1
               and dict(lattice[finding["fact_id"]].keys) == keys]
    if len(sources) != 1:
        raise F1098RecordingRefused("answer requires one exact current Form 1098 box 1 source")


def _stage_answer(
    staged: list[dict[str, Any]], registry: Any, *, keys: dict[str, str], question: str,
    answer: str, actor: str, at: str, evidence_id: str, contribution_id: str,
    finding_id: str, target_finding_id: str | None, claim_id: str, suffix: str,
    base_state: Any = None,
) -> tuple[str, Any]:
    state = base_state if base_state is not None else project(tuple(copy.deepcopy(row) for row in staged), registry)
    if f"tax.us.2025.f1098.{question}" not in state.fact_state.fact_types:
        raise F1098RecordingRefused(f"question is not in the adopted circumstance bundle: {question}")
    fact_id = fact_id_for(f"tax.us.2025.f1098.{question}", tuple(sorted(keys.items())))
    evidence = {
        "schema": "evidence.v1", "id": evidence_id, "kind": ANSWER_EVIDENCE_KIND,
        "label": f"Recorded answer: {question}",
        "content": {"submission_id": claim_id, "statement": dict(keys), "question": question, "answer": answer,
                    "correction_target": target_finding_id},
    }
    evidence_act = _act(len(staged), "evidence-submitted", {"evidence": evidence}, actor, at, suffix)
    state = apply_act(state, evidence_act, registry)
    staged.append(evidence_act)
    contribution = {"schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
                    "content": {"mode": "manual-entry", "source": "f1098-statement-answer",
                                "claim_id": claim_id, "question": question}}
    contribution_act = _act(len(staged), "contribution", {"contribution": contribution}, actor, at, suffix)
    finding = {"schema": "finding.v2", "id": finding_id, "fact_id": fact_id, "value": answer,
               "basis": "attested", "evidence_ids": [evidence_id], "contribution_id": contribution_id}
    assertion_act = _act(len(staged) + 1, "assertion", {"finding": finding}, actor, at, suffix)
    if finding_id in state.findings:
        raise F1098RecordingRefused("submission or finding identity has already been used")
    admission = apply_contribution_batch(
        state, contribution_act=contribution_act, successor_acts=[assertion_act], registry=registry,
        record_id=f"f1098.answer.record.{suffix}", workspace_revision=len(staged),
    )
    if admission.terminal_record["phase"] != "completed":
        raise F1098RecordingRefused("answer contribution was not admitted")
    staged.extend((contribution_act, assertion_act))
    return fact_id, admission.state


def record_f1098_statement_answers_durably(
    log: ActLog, registry: Any, *, statement_keys: dict[str, str], answers: dict[str, str],
    submission_id: str, evidence_ids: dict[str, str], actor: str, at: str,
    expected_revision: int, bundle_version: str | None = None,
) -> dict[str, Any]:
    """Admit one initial nine-answer account (and optional relevant timing pair) atomically."""
    _require_provenance(submission_id, actor, at)
    before = _read_for_save(log, expected_revision)
    suffix = _token(submission_id)
    staged = list(copy.deepcopy(before.acts))
    _ensure_bundle(staged, registry, actor, at, suffix, bundle_version)
    _validate_answers(staged, registry, statement_keys, answers, evidence_ids, submission_id=submission_id)
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    _require_current_statement(state, statement_keys)
    current_ids = compute_currency(state).current_finding_ids
    for question in answers:
        fact_id = fact_id_for(f"tax.us.2025.f1098.{question}", tuple(sorted(statement_keys.items())))
        if _current_finding(state, fact_id, current_ids) is not None:
            raise F1098RecordingRefused(f"answer already exists for {question}; use correction")
    ids: list[str] = []
    for question, answer in answers.items():
        finding_id = f"f1098.answer.finding.{suffix}.{_token(question)}"
        contribution_id = f"f1098.answer.contribution.{suffix}.{_token(question)}"
        evidence_id = evidence_ids[question]
        _, current = _stage_answer(staged, registry, keys=statement_keys, question=question, answer=answer,
                      actor=actor, at=at, evidence_id=evidence_id, contribution_id=contribution_id,
                      finding_id=finding_id, target_finding_id=None, claim_id=submission_id, suffix=suffix,
                      base_state=state)
        state = current
        ids.append(finding_id)
    return _commit(log, registry, before, staged, actor=actor, at=at, suffix=suffix,
                   finding_ids=ids, expected_revision=expected_revision)


def _validate_answers(staged: list[dict[str, Any]], registry: Any, keys: dict[str, str],
                      answers: dict[str, str], evidence_ids: dict[str, str], *,
                      allow_partial: bool = False, submission_id: str) -> None:
    required_keys = {"payer", "statement", "tax-year"}
    if set(keys) != required_keys or not all(isinstance(v, str) and v for v in keys.values()):
        raise F1098RecordingRefused("statement identity must be payer, statement and tax-year")
    version = _adopted_bundle_version(staged) or BUNDLE_VERSION
    if version not in SUPPORTED_BUNDLE_VERSIONS:
        raise F1098RecordingRefused("the adopted mortgage answer vocabulary is unsupported")
    bundle = load_f1098_circumstances_bundle(registry, version=version)
    declarations = {item["id"]: item for item in bundle["fact_types"]}
    question_by_suffix = {fact_id.rsplit(".", 1)[-1]: fact_id for fact_id in declarations}
    expected = _questions_for_version(version)
    allowed = expected | TIMING_QUESTIONS
    if (not allow_partial and not expected.issubset(answers)) or set(answers) - allowed:
        raise F1098RecordingRefused("submission must contain the nine ordinary answers and only known questions")
    use = answers.get(USE_QUESTION)
    submitted_timing = set(answers) & TIMING_QUESTIONS
    if submitted_timing and not allow_partial and use != PERSONAL_EXPENSE:
        raise F1098RecordingRefused("new timing answers are accepted only with personal-expense use")
    if not isinstance(evidence_ids, dict) or set(evidence_ids) != set(answers):
        raise F1098RecordingRefused("each submitted answer needs its own evidence identity")
    all_ids = list(evidence_ids.values())
    if len(set(all_ids)) != len(all_ids) or any(not isinstance(v, str) or not v for v in all_ids):
        raise F1098RecordingRefused("evidence identities must be distinct nonempty strings")
    prior_evidence = [row.get("payload", {}).get("evidence", {}) for row in staged
                      if row.get("kind") == "evidence-submitted"]
    if any(item.get("id") in all_ids for item in prior_evidence):
        raise F1098RecordingRefused("evidence identity has already been used")
    if any(item.get("content", {}).get("submission_id") == submission_id for item in prior_evidence):
        raise F1098RecordingRefused("submission identity has already been used")
    if any(item.get("content", {}).get("request_id") == submission_id for item in prior_evidence):
        raise F1098RecordingRefused("submission identity has already been used")
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    for suffix, answer in answers.items():
        fact_type = declarations[question_by_suffix[suffix]]
        schema = fact_type["value_schema"]
        offered = schema.get("enum", [row.get("const") for row in schema.get("oneOf", [])])
        if answer == "not-asked" or answer not in offered:
            raise F1098RecordingRefused(f"answer is not an offered value for {suffix}")
        fact_id = fact_id_for(question_by_suffix[suffix], tuple(sorted(keys.items())))
        if fact_id not in facts_of(state.fact_state):
            raise F1098RecordingRefused(f"statement identity cannot form answer fact {suffix}")


def _commit(log: ActLog, registry: Any, before: LogContents, staged: list[dict[str, Any]], *,
            actor: str, at: str, suffix: str, finding_ids: Sequence[str],
            expected_revision: int) -> dict[str, Any]:
    additions = staged[len(before.acts):]
    try:
        revision = log.append_batch(additions, expected_revision=expected_revision)
    except ActLogError as exc:
        raise F1098RecordingRefused(f"atomic answer save refused: {exc}") from exc
    fresh = log.read()
    return {"revision": revision, "finding_ids": list(finding_ids),
            "state": project(fresh.acts, registry), "actor": actor, "at": at}


def correct_f1098_statement_answer_durably(
    log: ActLog, registry: Any, *, statement_keys: dict[str, str], question: str, answer: str,
    predecessor_finding_id: str, submission_id: str, evidence_id: str, actor: str, at: str,
    expected_revision: int,
) -> dict[str, Any]:
    """Replace one exact current answer with new evidence on the same fact identity."""
    _require_provenance(submission_id, actor, at)
    before = _read_for_save(log, expected_revision)
    suffix = _token(submission_id)
    staged = list(copy.deepcopy(before.acts))
    _ensure_bundle(staged, registry, actor, at, suffix)
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    _require_current_statement(state, statement_keys)
    current_ids = compute_currency(state).current_finding_ids
    question_id = f"tax.us.2025.f1098.{question}"
    version = _adopted_bundle_version(staged) or BUNDLE_VERSION
    if question not in _questions_for_version(version) | TIMING_QUESTIONS:
        raise F1098RecordingRefused("question is not part of the selected Form 1098 answer set")
    fact_id = fact_id_for(question_id, tuple(sorted(statement_keys.items())))
    current = _current_finding(state, fact_id, current_ids)
    if current is None or current[0] != predecessor_finding_id:
        raise F1098RecordingRefused("correction target is not the exact current answer shown")
    if question in TIMING_QUESTIONS:
        use_fact_id = fact_id_for(f"tax.us.2025.f1098.{USE_QUESTION}", tuple(sorted(statement_keys.items())))
        use = _current_finding(state, use_fact_id, current_ids)
        if use is None or use[1].get("value") != PERSONAL_EXPENSE:
            raise F1098RecordingRefused("timing answers can be corrected only while personal-expense use is current")
    _validate_answers(staged, registry, statement_keys, {question: answer}, {question: evidence_id},
                      allow_partial=True, submission_id=submission_id)
    finding_id = f"f1098.answer.finding.{suffix}.{_token(question)}"
    contribution_id = f"f1098.answer.contribution.{suffix}.{_token(question)}"
    _, _ = _stage_answer(staged, registry, keys=statement_keys, question=question, answer=answer, actor=actor, at=at,
                  evidence_id=evidence_id, contribution_id=contribution_id, finding_id=finding_id,
                  target_finding_id=predecessor_finding_id, claim_id=submission_id, suffix=suffix,
                  base_state=state)
    return _commit(log, registry, before, staged, actor=actor, at=at, suffix=suffix,
                   finding_ids=[finding_id], expected_revision=expected_revision)


def answer_f1098_statement_answer_durably(
    log: ActLog, registry: Any, *, statement_keys: dict[str, str], question: str, answer: str,
    submission_id: str, evidence_id: str, actor: str, at: str, expected_revision: int,
    bundle_version: str | None = None,
) -> dict[str, Any]:
    """Record one absent ordinary or timing answer as a new finding."""
    _require_provenance(submission_id, actor, at)
    before = _read_for_save(log, expected_revision)
    suffix = _token(submission_id)
    staged = list(copy.deepcopy(before.acts))
    _ensure_bundle(staged, registry, actor, at, suffix, bundle_version)
    version = _adopted_bundle_version(staged) or BUNDLE_VERSION
    if question not in _questions_for_version(version) | TIMING_QUESTIONS:
        raise F1098RecordingRefused("question is not part of the selected Form 1098 answer set")
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    _require_current_statement(state, statement_keys)
    keys = tuple(sorted(statement_keys.items()))
    use_id = fact_id_for(f"tax.us.2025.f1098.{USE_QUESTION}", keys)
    timing_id = fact_id_for(f"tax.us.2025.f1098.{question}", keys)
    current_ids = compute_currency(state).current_finding_ids
    use_finding = _current_finding(state, use_id, current_ids)
    if question in TIMING_QUESTIONS and (use_finding is None or use_finding[1]["value"] != PERSONAL_EXPENSE):
        raise F1098RecordingRefused("timing answers can be added only while personal-expense use is current")
    if _current_finding(state, timing_id, current_ids) is not None:
        raise F1098RecordingRefused("timing answer is already current; use correction")
    _validate_answers(staged, registry, statement_keys, {question: answer}, {question: evidence_id},
                      allow_partial=True, submission_id=submission_id)
    finding_id = f"f1098.answer.finding.{suffix}.{_token(question)}"
    contribution_id = f"f1098.answer.contribution.{suffix}.{_token(question)}"
    _, _ = _stage_answer(staged, registry, keys=statement_keys, question=question, answer=answer, actor=actor, at=at,
                         evidence_id=evidence_id, contribution_id=contribution_id, finding_id=finding_id,
                         target_finding_id=None, claim_id=submission_id, suffix=suffix, base_state=state)
    return _commit(log, registry, before, staged, actor=actor, at=at, suffix=suffix,
                   finding_ids=[finding_id], expected_revision=expected_revision)


def answer_f1098_statement_timing_durably(
    log: ActLog, registry: Any, *, statement_keys: dict[str, str], question: str, answer: str,
    submission_id: str, evidence_id: str, actor: str, at: str, expected_revision: int,
) -> dict[str, Any]:
    """Compatibility spelling for the two timing questions."""
    if question not in TIMING_QUESTIONS:
        raise F1098RecordingRefused("only one of the two timing questions may be added by this operation")
    return answer_f1098_statement_answer_durably(
        log, registry, statement_keys=statement_keys, question=question, answer=answer,
        submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
        expected_revision=expected_revision,
    )


def withdraw_f1098_statement_answer_durably(
    log: ActLog, registry: Any, *, current_findings: Sequence[str], submission_id: str,
    actor: str, at: str, expected_revision: int,
) -> dict[str, Any]:
    """End current answer support without a replacement or an opposite answer."""
    _require_provenance(submission_id, actor, at)
    before = _read_for_save(log, expected_revision)
    if not current_findings or len(set(current_findings)) != len(current_findings):
        raise F1098RecordingRefused("withdrawal must name distinct current findings")
    staged = list(copy.deepcopy(before.acts))
    _require_selected_bundle(staged)
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    current_ids = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state, include_displaced=True)
    exact_sources = [(fid, row) for fid, row in state.findings.items() if fid in current_ids
                     and row.get("fact_id") in lattice and lattice[row["fact_id"]].fact_type_id == STATEMENT_BOX1]
    if len(exact_sources) != 1:
        raise F1098RecordingRefused("withdrawal requires one exact current Form 1098 box 1 source")
    source_keys = dict(lattice[exact_sources[0][1]["fact_id"]].keys)
    version = _adopted_bundle_version(staged) or BUNDLE_VERSION
    allowed_fact_types = {f"tax.us.2025.f1098.{q}" for q in _questions_for_version(version) | TIMING_QUESTIONS}
    for finding_id in current_findings:
        if finding_id not in current_ids:
            raise F1098RecordingRefused("withdrawal target is no longer current")
        finding = state.findings[finding_id]
        fact = lattice.get(finding.get("fact_id", ""))
        if (fact is None or fact.fact_type_id not in allowed_fact_types or
                dict(fact.keys) != source_keys):
            raise F1098RecordingRefused("withdrawal target is not an answer on the exact current statement")
    prior_evidence = [row.get("payload", {}).get("evidence", {}) for row in staged
                      if row.get("kind") == "evidence-submitted"]
    if any(item.get("content", {}).get("submission_id") == submission_id or
           item.get("content", {}).get("request_id") == submission_id for item in prior_evidence):
        raise F1098RecordingRefused("submission identity has already been used")
    suffix = _token(submission_id)
    evidence = {"schema": "evidence.v1", "id": f"f1098.withdrawal.{suffix}",
                "kind": ANSWER_EVIDENCE_KIND, "label": "Recorded answer withdrawal",
                "content": {"request_id": submission_id, "statement": source_keys,
                            "target_finding_ids": list(current_findings)}}
    evidence_act = _act(len(staged), "evidence-submitted", {"evidence": evidence}, actor, at, suffix)
    state = apply_act(state, evidence_act, registry)
    staged.append(evidence_act)
    for finding_id in current_findings:
        act = _act(len(staged), "finding-retracted", {"finding_id": finding_id}, actor, at, suffix)
        # Apply against the projected state before staging so ADR-0073 refusal is surfaced now.
        state = apply_act(state, act, registry)
        staged.append(act)
    return _commit(log, registry, before, staged, actor=actor, at=at, suffix=suffix,
                   finding_ids=[], expected_revision=expected_revision)
