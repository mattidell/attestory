"""Durable recording for one explicitly identified mortgage borrowing.

This module records ordinary claims and exact report relationships. It makes
no loan match from labels or amounts and has no tax calculation behavior.
"""
from __future__ import annotations

import copy
import hashlib
import math
from typing import Any, Sequence

from packages.kernel.act_log import ActLog, LogContents
from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import apply_act, project
from packages.tax.loader import load_mortgage_borrowing_bundle

BUNDLE_ID = "tax.us.2025.mortgage-borrowing"
BUNDLE_VERSION = "v1"
BORROWING_KIND = "tax.us.mortgage-borrowing-reference"
STATEMENT_BOX1 = "tax.us.2025.f1098.box1-mortgage-interest"
WITHDRAWN = "withdrawn"

_RECOGNITION = {
    "continuing-borrowing": {
        "yes": "tax.us.2025.mortgage.continuing-borrowing",
        "no": "tax.us.2025.mortgage.continuing-borrowing-denied",
        "cannot-tell": "tax.us.2025.mortgage.continuing-borrowing-unresolved",
        WITHDRAWN: "tax.us.2025.mortgage.continuing-borrowing-withdrawn",
    },
}
_INCLUSION = {
    "report-inclusion": {
        "affirmed": "tax.us.2025.f1098.borrowing-inclusion",
        "denied": "tax.us.2025.f1098.borrowing-denied",
        "cannot-tell": "tax.us.2025.f1098.borrowing-unresolved",
        WITHDRAWN: "tax.us.2025.f1098.borrowing-withdrawn",
    },
}
_SHARED = {
    "owes-the-loan": ("tax.us.2025.mortgage.shared-owes-the-loan", {"yes", "no", "cannot-tell"}),
    "no-one-else-owes-it": ("tax.us.2025.mortgage.shared-no-one-else-owes-it", {"yes", "no", "cannot-tell"}),
    "what-the-money-paid-for": ("tax.us.2025.mortgage.shared-proceeds-use",
                                {"bought-the-home", "unrelated-personal-expense", "other", "cannot-tell"}),
    "this-is-the-original-loan": ("tax.us.2025.mortgage.shared-original-loan", {"yes", "no", "cannot-tell"}),
    "mortgage-credit-certificate-received": ("tax.us.2025.mortgage.shared-credit-certificate",
                                              {"received", "not-received", "cannot-tell"}),
}
_OTHER_DEBT = "tax.us.2025.mortgage.other-secured-home-debt"
_CEILING = "tax.us.2025.f1098.borrowing-year-ceiling"
_QUESTIONS = {
    "continuing-borrowing": "Is this one continuing original mortgage borrowing for 2025?",
    "report-inclusion": "Does this exact Form 1098 include interest for this borrowing?",
    "annual-ceiling": "What is the upper bound on this borrowing's highest balance during 2025?",
    "other-secured-home-debt": "Besides this borrowing, did you have any other mortgage or home-equity debt secured by either home in 2025?",
    "owes-the-loan": "Do you or your joint-filing spouse owe this borrowing?",
    "no-one-else-owes-it": "Does no one besides the joint-filing spouses owe this borrowing?",
    "what-the-money-paid-for": "What did the proceeds of this borrowing pay for?",
    "this-is-the-original-loan": "Is this the original loan rather than a refinance?",
    "mortgage-credit-certificate-received": "Was a mortgage credit certificate received for this borrowing?",
}
_RECOGNITION_TYPES = frozenset(t for outcomes in _RECOGNITION.values() for t in outcomes.values())
_INCLUSION_TYPES = frozenset(t for outcomes in _INCLUSION.values() for t in outcomes.values())
_SHARED_TYPES = frozenset(t for t, _ in _SHARED.values())
_CLAIM_TYPES = _RECOGNITION_TYPES | _INCLUSION_TYPES | _SHARED_TYPES | {_OTHER_DEBT, _CEILING}


class MortgageBorrowingRecordingRefused(ValueError):
    """A mortgage claim cannot be bound to the exact current subjects supplied."""


def _act(index: int, kind: str, payload: dict[str, Any], actor: str, at: str, suffix: str) -> dict[str, Any]:
    return {"schema": "act.v1", "act_id": f"mortgage.borrowing.{suffix}.{index}", "kind": kind,
            "actor": actor, "at": at, "committed_against": index, "payload": payload}


def _read(log: ActLog, expected_revision: int | None) -> LogContents:
    before = log.read()
    if before.incomplete_tail is not None:
        raise MortgageBorrowingRecordingRefused("ActLog has an incomplete tail")
    if expected_revision is not None and before.revision != expected_revision:
        raise MortgageBorrowingRecordingRefused("reviewed ActLog revision changed before save")
    return before


def _adopt(staged: list[dict[str, Any]], registry: Any, actor: str, at: str, suffix: str) -> Any:
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    if all(fact_id in state.fact_state.fact_types for fact_id in _CLAIM_TYPES):
        return state
    bundle = load_mortgage_borrowing_bundle(registry)
    if bundle.get("id") != BUNDLE_ID or bundle.get("version") != BUNDLE_VERSION:
        raise MortgageBorrowingRecordingRefused("mortgage borrowing vocabulary is unavailable")
    item = _act(len(staged), "bundle-adoption", {"bundle": bundle}, actor, at, f"bundle.{suffix}")
    state = apply_act(state, item, registry)
    staged.append(item)
    return state


def _scoped_fact_id(state: Any, fact_type: str, keys: dict[str, str]) -> str:
    declared = state.fact_state.fact_types[fact_type]
    ordered = tuple((item["name"], keys[item["name"]]) for item in declared["identity_keys"])
    return fact_id_for(fact_type, ordered)


def _current_findings(state: Any, fact_types: frozenset[str], keys: dict[str, str]) -> list[str]:
    current = compute_currency(state).current_finding_ids
    wanted = {_scoped_fact_id(state, kind, keys) for kind in fact_types}
    return [finding_id for finding_id, finding in state.findings.items()
            if finding_id in current and finding.get("fact_id") in wanted]


def _validate_borrowing(state: Any, borrowing_ref: str) -> None:
    entity = state.fact_state.entities.get(borrowing_ref)
    if entity is None or entity.status != "current" or entity.entity.get("kind") != BORROWING_KIND:
        raise MortgageBorrowingRecordingRefused("borrowing reference is missing, ended, or wrong-kind")


def _validate_statement(state: Any, statement_keys: dict[str, str]) -> None:
    if set(statement_keys) != {"payer", "statement", "tax-year"} or statement_keys.get("tax-year") != "2025":
        raise MortgageBorrowingRecordingRefused("an exact 2025 Form 1098 identity is required")
    fact_id = _scoped_fact_id(state, STATEMENT_BOX1, statement_keys)
    current = compute_currency(state).current_finding_ids
    rows = [fid for fid, finding in state.findings.items() if fid in current and finding.get("fact_id") == fact_id]
    if len(rows) != 1:
        raise MortgageBorrowingRecordingRefused("report inclusion requires one exact current Form 1098 box 1 source")


def introduce_mortgage_borrowing_reference_durably(
    log: ActLog, registry: Any, *, reference_id: str, description: str, actor: str, at: str,
) -> dict[str, Any]:
    """Introduce an opaque mortgage-borrowing address; descriptions never match identities."""
    if not all(isinstance(value, str) and value.strip() for value in (reference_id, description, actor, at)):
        raise MortgageBorrowingRecordingRefused("reference, description, actor, and time are required")
    before = _read(log, None)
    state = project(before.acts, registry)
    if reference_id in state.fact_state.entities:
        raise MortgageBorrowingRecordingRefused("borrowing reference address has already been used")
    suffix = hashlib.sha256(reference_id.encode("utf-8")).hexdigest()[:16]
    item = _act(before.revision, "entity-introduced", {"entity": {
        "schema": "entity.v1", "id": reference_id, "kind": BORROWING_KIND, "label": description,
    }}, actor, at, f"reference.{suffix}")
    apply_act(state, item, registry)
    revision = log.append(item, expected_revision=before.revision)
    return {"reference_id": reference_id, "act": item, "revision": revision,
            "state": project(log.read().acts, registry)}


def _claim_keys(claim: str, borrowing_ref: str, statement_keys: dict[str, str] | None) -> dict[str, str]:
    account = {"borrowing": borrowing_ref, "tax-year": "2025"}
    if claim == "report-inclusion":
        if statement_keys is None:
            raise MortgageBorrowingRecordingRefused("report inclusion requires exact report keys")
        return {**statement_keys, "borrowing": borrowing_ref}
    if claim not in {"continuing-borrowing", "annual-ceiling", "other-secured-home-debt", *_SHARED}:
        raise MortgageBorrowingRecordingRefused("unknown mortgage borrowing claim")
    return account


def _fact_type_and_value(claim: str, value: object) -> tuple[str, Any]:
    if claim in _RECOGNITION:
        fact_type = _RECOGNITION[claim].get(value) if isinstance(value, str) else None
        if fact_type:
            return fact_type, value
    elif claim in _INCLUSION:
        fact_type = _INCLUSION[claim].get(value) if isinstance(value, str) else None
        if fact_type:
            return fact_type, value
    elif claim == "annual-ceiling":
        if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value)) and value >= 0:
            return _CEILING, value
    elif claim == "other-secured-home-debt":
        if value in {"yes", "no", "cannot-tell"}:
            return _OTHER_DEBT, str(value)
    elif claim in _SHARED:
        fact_type, accepted = _SHARED[claim]
        if isinstance(value, str) and value in accepted:
            return fact_type, value
    raise MortgageBorrowingRecordingRefused("answer is outside the selected claim vocabulary")


def record_mortgage_borrowing_claim_durably(
    log: ActLog, registry: Any, *, claim: str, borrowing_ref: str, value: str | float | int,
    submission_id: str, evidence_id: str, actor: str, at: str,
    statement_keys: dict[str, str] | None = None, expected_revision: int | None = None,
) -> dict[str, Any]:
    """Record one explicit recognition, exact link, ceiling, other-debt, or shared answer."""
    return _save_claim(log, registry, claim=claim, borrowing_ref=borrowing_ref, value=value,
                       submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
                       statement_keys=statement_keys, expected_revision=expected_revision,
                       predecessor=None)


def correct_mortgage_borrowing_claim_durably(
    log: ActLog, registry: Any, *, finding_id: str, claim: str, borrowing_ref: str,
    value: str | float | int, submission_id: str, evidence_id: str, actor: str, at: str,
    statement_keys: dict[str, str] | None = None, expected_revision: int | None = None,
) -> dict[str, Any]:
    """Replace exactly one current claim of the named borrowing and scope."""
    return _save_claim(log, registry, claim=claim, borrowing_ref=borrowing_ref, value=value,
                       submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
                       statement_keys=statement_keys, expected_revision=expected_revision,
                       predecessor=finding_id)


def withdraw_mortgage_borrowing_claim_durably(
    log: ActLog, registry: Any, *, finding_id: str, claim: str, borrowing_ref: str,
    actor: str, at: str, statement_keys: dict[str, str] | None = None,
    submission_id: str | None = None, evidence_id: str | None = None,
    expected_revision: int | None = None,
) -> dict[str, Any]:
    """End one exact current claim; recognition/link withdrawal stays an explicit outcome."""
    if claim in {*_RECOGNITION, *_INCLUSION}:
        if submission_id is None or evidence_id is None:
            raise MortgageBorrowingRecordingRefused("withdrawal outcome requires fresh submission and evidence identities")
        return correct_mortgage_borrowing_claim_durably(
            log, registry, finding_id=finding_id, claim=claim, borrowing_ref=borrowing_ref,
            value=WITHDRAWN, submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
            statement_keys=statement_keys, expected_revision=expected_revision)
    if claim not in {"annual-ceiling", "other-secured-home-debt", *_SHARED}:
        raise MortgageBorrowingRecordingRefused("unknown mortgage claim")
    before = _read(log, expected_revision)
    state = project(before.acts, registry)
    _validate_borrowing(state, borrowing_ref)
    keys = _claim_keys(claim, borrowing_ref, statement_keys)
    fact_types = frozenset({_CEILING if claim == "annual-ceiling" else
                            _OTHER_DEBT if claim == "other-secured-home-debt" else _SHARED[claim][0]})
    if _current_findings(state, fact_types, keys) != [finding_id]:
        raise MortgageBorrowingRecordingRefused("withdrawal must name this exact current claim")
    suffix = hashlib.sha256(f"{finding_id}\0{at}\0withdraw".encode()).hexdigest()[:16]
    item = _act(before.revision, "finding-retracted", {"finding_id": finding_id}, actor, at,
                f"withdraw.{suffix}")
    apply_act(state, item, registry)
    revision = log.append(item, expected_revision=before.revision)
    return {"finding_id": finding_id, "retraction_act": item, "revision": revision,
            "state": project(log.read().acts, registry)}


def _save_claim(
    log: ActLog, registry: Any, *, claim: str, borrowing_ref: str, value: str | float | int,
    submission_id: str, evidence_id: str, actor: str, at: str,
    statement_keys: dict[str, str] | None, expected_revision: int | None,
    predecessor: str | None,
) -> dict[str, Any]:
    if not all(isinstance(item, str) and item.strip() for item in (submission_id, evidence_id, actor, at)):
        raise MortgageBorrowingRecordingRefused("submission, evidence, actor, and time are required")
    fact_type, stored_value = _fact_type_and_value(claim, value)
    keys = _claim_keys(claim, borrowing_ref, statement_keys)
    if claim == "report-inclusion" and (statement_keys is None or set(statement_keys) != {"payer", "statement", "tax-year"}):
        raise MortgageBorrowingRecordingRefused("report inclusion requires the exact payer, statement, and tax year")
    before = _read(log, expected_revision)
    staged = list(copy.deepcopy(before.acts))
    suffix = hashlib.sha256(f"{submission_id}\0{claim}\0{fact_type}".encode()).hexdigest()[:20]
    state = _adopt(staged, registry, actor, at, suffix)
    _validate_borrowing(state, borrowing_ref)
    if claim == "report-inclusion" and value != WITHDRAWN:
        assert statement_keys is not None
        _validate_statement(state, statement_keys)
    sibling_types = (_RECOGNITION_TYPES if claim == "continuing-borrowing" else
                     _INCLUSION_TYPES if claim == "report-inclusion" else frozenset({fact_type}))
    current = _current_findings(state, sibling_types, keys)
    if predecessor is None and current:
        raise MortgageBorrowingRecordingRefused("claim already has a current answer; correct or withdraw it")
    if predecessor is not None and current != [predecessor]:
        raise MortgageBorrowingRecordingRefused("correction must name this exact current claim")
    if evidence_id in state.evidence or any(
        getattr(item, "evidence", {}).get("content", {}).get("submission_id") == submission_id
        for item in state.evidence.values()
    ):
        raise MortgageBorrowingRecordingRefused("submission or evidence identity has already been used")
    finding_id = f"mortgage.borrowing.finding.{suffix}"
    contribution_id = f"mortgage.borrowing.contribution.{suffix}"
    if finding_id in state.findings:
        raise MortgageBorrowingRecordingRefused("submission identity has already been used")
    evidence = {"schema": "evidence.v1", "id": evidence_id, "kind": "tax.mortgage.borrowing-answer",
                "label": f"Mortgage borrowing claim: {claim}", "content": {
                    "submission_id": submission_id, "claim": claim, "value": stored_value,
                    "question": _QUESTIONS[claim],
                    "borrowing_ref": borrowing_ref, "tax_year": "2025",
                    "statement": copy.deepcopy(statement_keys), "correction_of_finding_id": predecessor,
                    "response_meaning": (
                        "no other obligor beyond the joint-filing spouses" if claim == "no-one-else-owes-it" and value == "yes"
                        else "an additional obligor exists" if claim == "no-one-else-owes-it" and value == "no"
                        else "upper bound on the borrowing's highest balance during 2025" if claim == "annual-ceiling"
                        else "other secured debt exists besides this exact borrowing" if claim == "other-secured-home-debt" and value == "yes"
                        else "no other secured debt besides this exact borrowing" if claim == "other-secured-home-debt" and value == "no"
                        else str(value)),
                }}
    contribution = {"schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
                    "content": {"mode": "manual-entry", "source": "mortgage-borrowing-claim", "claim": claim}}
    finding = {"schema": "finding.v2", "id": finding_id,
               "fact_id": _scoped_fact_id(state, fact_type, keys), "value": stored_value,
               "basis": "attested", "evidence_ids": [evidence_id], "contribution_id": contribution_id}
    if predecessor is not None:
        retraction = _act(len(staged), "finding-retracted", {"finding_id": predecessor}, actor, at,
                          f"retract.{suffix}")
        state = apply_act(state, retraction, registry)
        staged.append(retraction)
    evidence_act = _act(len(staged), "evidence-submitted", {"evidence": evidence}, actor, at, suffix)
    state = apply_act(state, evidence_act, registry)
    staged.append(evidence_act)
    contribution_act = _act(len(staged), "contribution", {"contribution": contribution}, actor, at, suffix)
    assertion_act = _act(len(staged) + 1, "assertion", {"finding": finding}, actor, at, suffix)
    admission = apply_contribution_batch(state, contribution_act=contribution_act,
                                         successor_acts=[assertion_act], registry=registry,
                                         record_id=f"mortgage.borrowing.record.{suffix}",
                                         workspace_revision=before.revision)
    if admission.terminal_record["phase"] != "completed":
        raise MortgageBorrowingRecordingRefused("mortgage claim contribution was not admitted")
    staged.extend((contribution_act, assertion_act))
    revision = log.append_batch(staged[len(before.acts):], expected_revision=before.revision)
    recovered = log.read()
    return {"claim": claim, "fact_type": fact_type, "finding_id": finding_id, "evidence_id": evidence_id,
            "predecessor_finding_id": predecessor, "revision": revision,
            "state": project(recovered.acts, registry)}


def clear_mortgage_borrowing_year_durably(
    log: ActLog, registry: Any, *, borrowing_ref: str, actor: str, at: str,
    expected_revision: int,
) -> dict[str, Any]:
    """Explicitly end current 2025 recognition, link, ceiling, and five shared answers atomically."""
    if not all(isinstance(value, str) and value.strip() for value in (borrowing_ref, actor, at)):
        raise MortgageBorrowingRecordingRefused("borrowing reference, actor, and time are required")
    before = _read(log, expected_revision)
    state = project(before.acts, registry)
    _validate_borrowing(state, borrowing_ref)
    current = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state, include_displaced=True)
    target_ids: list[str] = []
    for finding_id, row in state.findings.items():
        if finding_id not in current:
            continue
        fact = lattice.get(row.get("fact_id", ""))
        if fact is None or fact.fact_type_id not in (_RECOGNITION_TYPES | _INCLUSION_TYPES | _SHARED_TYPES | {_CEILING}):
            continue
        if dict(fact.keys).get("borrowing") == borrowing_ref and dict(fact.keys).get("tax-year") == "2025":
            target_ids.append(finding_id)
    staged = list(copy.deepcopy(before.acts))
    for finding_id in sorted(target_ids):
        suffix = hashlib.sha256(f"{borrowing_ref}\0{finding_id}\0{at}".encode()).hexdigest()[:16]
        item = _act(len(staged), "finding-retracted", {"finding_id": finding_id}, actor, at, f"clear.{suffix}")
        state = apply_act(state, item, registry)
        staged.append(item)
    revision = log.append_batch(staged[len(before.acts):], expected_revision=before.revision)
    recovered = log.read()
    return {"borrowing_ref": borrowing_ref, "ended_finding_ids": sorted(target_ids),
            "revision": revision, "state": project(recovered.acts, registry)}
