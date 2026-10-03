"""Ordinary source recording for student-loan circumstance relationships.

This module records what a person explicitly connects. It has no tax result,
allocation, or document-proof semantics.
"""
from __future__ import annotations

import copy
import hashlib
from typing import Any, Sequence

from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import apply_act, project
from packages.kernel.act_log import ActLog, ActLogError, LogContents


FINANCING = "tax.us.2025.sli.financing-relationship"
STATEMENT_INCLUSION = "tax.us.2025.sli.statement-inclusion-relationship"
INCLUSION_UNRESOLVED = "demo.tax.2025.sli.statement-inclusion-unresolved"
SCHOOLING = "tax.us.2025.sli.schooling-situation"
BORROWING_KIND = "tax.us.student-loan-borrowing-reference"
STATEMENT_TYPE = "tax.us.2025.f1098e.box1-student-loan-interest"

# Relationship bundle v2: the two ordinary borrowing answers. Each is keyed by
# the borrowing alone; a second loan for the same schooling needs its own answer.
LOAN_COST = "tax.us.2025.sli.loan-paid-only-school-costs"
ENROLLMENT = "tax.us.2025.sli.enrolled-at-least-half-time"
BORROWING_QUESTIONS = {
    "loan-paid-only-school-costs": LOAN_COST,
    "enrolled-at-least-half-time": ENROLLMENT,
}
BORROWING_ANSWER_EVIDENCE_KIND = "tax.student-loan.borrowing-answer"
_BORROWING_RESPONSES = frozenset({"yes", "no", "cannot-tell"})

# Relationship bundle v2: what a person said about a link, other than yes. Each
# outcome is a current fact of its own pair so a rule can require it; a missing
# outcome then means genuine absence only. ``INCLUSION_UNRESOLVED`` above is
# the sample diagnostic type, still written for workspaces without v2.
STATEMENT_INCLUSION_UNRESOLVED = "tax.us.2025.sli.statement-inclusion-unresolved"
STATEMENT_INCLUSION_DENIED = "tax.us.2025.sli.statement-inclusion-denied"
STATEMENT_INCLUSION_WITHDRAWN = "tax.us.2025.sli.statement-inclusion-withdrawn"
FINANCING_UNRESOLVED = "tax.us.2025.sli.financing-unresolved"
FINANCING_DENIED = "tax.us.2025.sli.financing-denied"
FINANCING_WITHDRAWN = "tax.us.2025.sli.financing-withdrawn"
# A system marker that replay supplies in a run's sources (ADR 0077 Part 5),
# with its one value. Declared in bundle v2; no recorder writes it.
INCLUSION_APPLICABILITY_UNESTABLISHED = "tax.us.2025.sli.statement-inclusion-applicability-unestablished"
INCLUSION_APPLICABILITY_UNESTABLISHED_VALUE = "sli.statement-inclusion.applicability-unestablished"
# The person named a statement but could not tell which borrowing it covers.
# Keyed by the statement alone; ended by a later identified inclusion answer.
STATEMENT_INCLUSION_SCOPE_UNRESOLVED = "tax.us.2025.sli.statement-inclusion-scope-unresolved"
STATEMENT_INCLUSION_SCOPE_UNRESOLVED_VALUE = "sli.statement-inclusion.scope-unresolved"
LINK_OUTCOMES: dict[str, dict[str, tuple[str, str]]] = {
    FINANCING: {
        "cannot-tell": (FINANCING_UNRESOLVED, "sli.financing.unresolved"),
        "no": (FINANCING_DENIED, "sli.financing.denied"),
        "withdrawn": (FINANCING_WITHDRAWN, "sli.financing.withdrawn"),
    },
    STATEMENT_INCLUSION: {
        "cannot-tell": (STATEMENT_INCLUSION_UNRESOLVED, "sli.statement-inclusion.unresolved"),
        "no": (STATEMENT_INCLUSION_DENIED, "sli.statement-inclusion.denied"),
        "withdrawn": (STATEMENT_INCLUSION_WITHDRAWN, "sli.statement-inclusion.withdrawn"),
    },
}
WITHDRAWAL_EVIDENCE_KIND = "tax.student-loan.relationship-withdrawal"


class RelationshipRecordingRefused(ValueError):
    """The response cannot be bound to the exact current subjects supplied."""


def _commit_save(log: ActLog, before: LogContents, staged: Sequence[dict[str, Any]], *,
                 reviewed: bool = False) -> int:
    """Write one save's staged acts with one ``append_batch``: all, or none.

    Track 7: a save that writes several records leaves either the state
    before it or the whole save, never a part. ``staged`` is the log as read
    in ``before`` followed by the save's acts. ``reviewed`` names a save bound
    to a prepared review, whose log must not have moved since.
    """
    additions = list(staged[len(before.acts):])
    if not additions:
        return before.revision
    try:
        return log.append_batch(additions, expected_revision=before.revision)
    except ActLogError as exc:
        if reviewed and "stale revision" in str(exc):
            raise RelationshipRecordingRefused("reviewed ActLog revision changed before first append") from exc
        raise


def _read_for_save(log: ActLog, expected_revision: int | None) -> LogContents:
    """Read the log a save stages from; refuse a moved review or a torn tail."""
    before = log.read()
    if expected_revision is not None and before.revision != expected_revision:
        raise RelationshipRecordingRefused("reviewed ActLog revision changed before recording")
    if before.incomplete_tail is not None:
        raise RelationshipRecordingRefused("ActLog has an incomplete tail")
    return before


def _act(index: int, kind: str, payload: dict[str, Any], actor: str, at: str,
         suffix: str) -> dict[str, Any]:
    return {"schema": "act.v1", "act_id": f"sli.relationship.act.{suffix}.{index}", "kind": kind,
            "actor": actor, "at": at, "committed_against": index, "payload": payload}


def _current(acts: Sequence[dict[str, Any]], registry: Any) -> tuple[Any, Any, dict[str, dict[str, Any]], Any]:
    state = project(tuple(copy.deepcopy(row) for row in acts), registry)
    currency = compute_currency(state)
    current_ids = currency.current_finding_ids
    lattice = facts_of(state.fact_state)
    findings = {fid: row for fid, row in state.findings.items() if fid in current_ids}
    return state, currency, findings, lattice


_REVIEWED_CORRECTION_SCOPES = frozenset({
    "amount-only", "inclusion-added", "inclusion-removed", "inclusion-uncertain",
})


def _evidence_content(state: Any, evidence_id: object) -> dict[str, Any] | None:
    if not isinstance(evidence_id, str):
        return None
    lifecycle = state.evidence.get(evidence_id)
    if lifecycle is None:
        return None
    body = lifecycle.evidence if isinstance(getattr(lifecycle, "evidence", None), dict) else None
    if body is None:
        return None
    content = body.get("content")
    return content if isinstance(content, dict) else None


def _confirmed_statement_finding_id(state: Any, finding: dict[str, Any]) -> str | None:
    """Return the box-1 finding an inclusion was affirmed against, when recorded."""
    evidence_ids = finding.get("evidence_ids")
    if not isinstance(evidence_ids, list):
        return None
    for evidence_id in evidence_ids:
        content = _evidence_content(state, evidence_id)
        if content is None:
            continue
        confirmed = content.get("confirmed_statement_finding_id")
        if isinstance(confirmed, str) and confirmed:
            return confirmed
    return None


def _confirmed_statement_finding_at_admission(acts: Sequence[dict[str, Any]], registry: Any,
                                              inclusion_finding_id: str,
                                              statement_fact_id: str) -> str | None:
    """Tie an older inclusion to the box-1 finding current when it was admitted.

    Recorded evidence now stores the tie directly. Logs written before that
    field still resolve the same way: the statement finding that was current
    at the inclusion assertion. A later same-identity append does not inherit it.
    """
    for index, item in enumerate(acts):
        if item.get("kind") != "assertion":
            continue
        payload = item.get("payload")
        admitted = payload.get("finding") if isinstance(payload, dict) else None
        if not isinstance(admitted, dict) or admitted.get("id") != inclusion_finding_id:
            continue
        admitted_state = project(tuple(acts[:index + 1]), registry)
        admitted_current = compute_currency(admitted_state).current_finding_ids
        matches = [fid for fid, row in admitted_state.findings.items()
                   if isinstance(fid, str) and fid in admitted_current and isinstance(row, dict)
                   and row.get("fact_id") == statement_fact_id]
        if len(matches) == 1:
            return matches[0]
        return None
    return None


def _amounts_equal(left: object, right: object) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return False
    return isinstance(left, (int, float)) and isinstance(right, (int, float)) and left == right


def _predecessor_statement_finding_id(acts: Sequence[dict[str, Any]], registry: Any, finding_id: str,
                                      statement_fact_id: str) -> str | None:
    """Return the box 1 finding current just before this finding was asserted."""
    for index, item in enumerate(acts):
        if item.get("kind") != "assertion":
            continue
        payload = item.get("payload")
        admitted = payload.get("finding") if isinstance(payload, dict) else None
        if not isinstance(admitted, dict) or admitted.get("id") != finding_id:
            continue
        prior = project(tuple(acts[:index]), registry)
        prior_current = compute_currency(prior).current_finding_ids
        matches = [fid for fid, row in prior.findings.items()
                   if isinstance(fid, str) and fid in prior_current and isinstance(row, dict)
                   and row.get("fact_id") == statement_fact_id]
        if len(matches) == 1:
            return matches[0]
        return None
    return None


def _cited_source_correction_id(state: Any, finding: dict[str, Any]) -> str | None:
    """Return the one corrected-statement correction id this finding cites."""
    evidence_ids = finding.get("evidence_ids")
    if not isinstance(evidence_ids, list):
        return None
    found: str | None = None
    for evidence_id in evidence_ids:
        if not isinstance(evidence_id, str):
            continue
        lifecycle = state.evidence.get(evidence_id)
        body = lifecycle.evidence if lifecycle is not None and isinstance(
            getattr(lifecycle, "evidence", None), dict) else None
        if not isinstance(body, dict) or body.get("kind") != "tax.form-1098e-corrected-statement-source":
            continue
        content = body.get("content")
        correction_id = content.get("source_correction_id") if isinstance(content, dict) else None
        if not isinstance(correction_id, str) or not correction_id:
            return None
        if found is not None:
            return None
        found = correction_id
    return found


def _finding_ids_citing(state: Any, evidence_id: str) -> list[str]:
    """Box 1 findings that cite ``evidence_id``.

    Single use counts box 1 findings only: the inclusion-uncertain route's own
    unresolved status cites the same answer evidence and does not use it up.
    """
    cited: list[str] = []
    all_facts = facts_of(state.fact_state, include_displaced=True)
    for finding_id, row in state.findings.items():
        if not isinstance(finding_id, str) or not isinstance(row, dict):
            continue
        fact = all_facts.get(row.get("fact_id", ""))
        if fact is None or fact.fact_type_id != STATEMENT_TYPE:
            continue
        evidence_ids = row.get("evidence_ids")
        if isinstance(evidence_ids, list) and evidence_id in evidence_ids:
            cited.append(finding_id)
    return cited


def _reviewed_correction_refreshes(state: Any, statement_finding: dict[str, Any],
                                   statement_fact_id: str, *,
                                   acts: Sequence[dict[str, Any]], registry: Any) -> bool:
    """Refresh only the one finding a scope evidence binds.

    The evidence kind is ``tax.student-loan.relationship-answer``. It must
    name the box 1 finding the review saw, the corrected amount, and the
    correction identity. The current finding must be that amount, cite that
    correction identity, and be the successor of the finding the review saw.
    The same evidence authorizes no second finding. Statement identity, an
    allowed scope, and a refresh flag are not enough.
    """
    evidence_ids = statement_finding.get("evidence_ids")
    finding_id = statement_finding.get("id")
    if not isinstance(evidence_ids, list) or not isinstance(finding_id, str):
        return False
    for evidence_id in evidence_ids:
        if not isinstance(evidence_id, str):
            continue
        lifecycle = state.evidence.get(evidence_id)
        body = lifecycle.evidence if lifecycle is not None and isinstance(
            getattr(lifecycle, "evidence", None), dict) else None
        if not isinstance(body, dict) or body.get("kind") != "tax.student-loan.relationship-answer":
            continue
        content = body.get("content")
        if not isinstance(content, dict):
            continue
        context = content.get("recognition_context")
        if not isinstance(context, dict):
            continue
        correction = context.get("statement_correction")
        if not isinstance(correction, dict):
            continue
        if correction.get("statement_fact_id") != statement_fact_id:
            continue
        if correction.get("scope") not in _REVIEWED_CORRECTION_SCOPES:
            continue
        if correction.get("refreshes_inclusion_applicability") is not True:
            continue
        reviewed_id = correction.get("reviewed_statement_finding_id")
        bound_correction_id = correction.get("source_correction_id")
        if not isinstance(reviewed_id, str) or not reviewed_id:
            continue
        if not isinstance(bound_correction_id, str) or not bound_correction_id:
            continue
        if not _amounts_equal(statement_finding.get("value"), correction.get("corrected_box1_total")):
            continue
        if _cited_source_correction_id(state, statement_finding) != bound_correction_id:
            continue
        if _predecessor_statement_finding_id(acts, registry, finding_id, statement_fact_id) != reviewed_id:
            continue
        if _finding_ids_citing(state, evidence_id) != [finding_id]:
            continue
        return True
    return False


def _inclusion_applies_to_current_statement(state: Any, current_ids: Any, finding: dict[str, Any],
                                            statement_fact_id: str, *,
                                            acts: Sequence[dict[str, Any]], registry: Any,
                                            inclusion_finding_id: str) -> bool:
    """An inclusion applies only to the statement finding it was confirmed against.

    The reviewed correction route refreshes that tie only when the current
    box-1 finding is the one finding bound to the scope evidence: successor
    of the finding the review saw, at the corrected amount, with that
    correction identity. Citing the evidence id is not enough. Missing or
    ambiguous current box-1 support fails closed.
    """
    current_sources = [(source_id, source) for source_id, source in state.findings.items()
                       if source_id in current_ids and isinstance(source, dict)
                       and source.get("fact_id") == statement_fact_id]
    if len(current_sources) != 1:
        return False
    source_id, source_finding = current_sources[0]
    confirmed = _confirmed_statement_finding_id(state, finding)
    if confirmed is None:
        confirmed = _confirmed_statement_finding_at_admission(
            acts, registry, inclusion_finding_id, statement_fact_id)
    if confirmed == source_id:
        return True
    return _reviewed_correction_refreshes(
        state, source_finding, statement_fact_id, acts=acts, registry=registry)


def current_claim_applicability(acts: Sequence[dict[str, Any]], registry: Any) -> list[dict[str, str]]:
    """Project current claims against their exact current source subjects.

    This is an opt-in source-use guard, not a tax result or automatic engine
    hold. Consumers must explicitly call it and act on unresolved rows. Missing
    or changed source identity leaves the claim's finding history intact but
    returns ``unresolved-applicability``; it never follows labels or retargets.

    A statement inclusion is tied to the box-1 finding it was affirmed against.
    It stays applicable when that finding is still current, or when the current
    box-1 finding is the one successor bound to reviewed scope evidence. It
    does not follow an ordinary same-identity box-1 append, or a later update
    that cites evidence bound to a different correction.
    """
    state, currency, _findings, lattice = _current(acts, registry)
    current_ids = currency.current_finding_ids
    results: list[dict[str, str]] = []
    for finding_id in sorted(current_ids):
        finding = state.findings.get(finding_id)
        fact = lattice.get(finding.get("fact_id")) if finding is not None else None
        if fact is None or fact.fact_type_id not in {FINANCING, STATEMENT_INCLUSION}:
            continue
        if not isinstance(finding, dict):
            continue
        keys = tuple((key, value) for key, value in fact.keys if key != "borrowing")
        source_type = SCHOOLING if fact.fact_type_id == FINANCING else STATEMENT_TYPE
        source_fact_id = fact_id_for(source_type, keys)
        if fact.fact_type_id == STATEMENT_INCLUSION:
            applicable = _inclusion_applies_to_current_statement(
                state, current_ids, finding, source_fact_id, acts=acts, registry=registry,
                inclusion_finding_id=finding_id)
        else:
            applicable = any(source_id in current_ids and source.get("fact_id") == source_fact_id
                             for source_id, source in state.findings.items())
        results.append({"finding_id": finding_id, "relationship_type": fact.fact_type_id,
                        "source_fact_id": source_fact_id,
                        "applicability": "current" if applicable else "unresolved-applicability"})
    return results


def link_outcomes_adopted(state: Any) -> bool:
    """True when this workspace adopted relationship bundle v2's link outcomes.

    Workspaces that adopted only v1 record as before: no outcome facts.
    """
    return STATEMENT_INCLUSION_SCOPE_UNRESOLVED in state.fact_state.fact_types and all(
        fact_type in state.fact_state.fact_types
        for outcomes in LINK_OUTCOMES.values() for fact_type, _value in outcomes.values())


def _link_pairs(relation_type: str, borrowing: str, source_keys: Sequence[tuple[Any, Any]]) -> tuple[tuple[str, str], ...]:
    """Identity bindings of one link, in the relationship type's key order."""
    source = tuple((str(key), str(value)) for key, value in source_keys)
    if relation_type == FINANCING:
        return (("borrowing", borrowing),) + source
    return source + (("borrowing", borrowing),)


def _current_link_outcomes(state: Any, current_ids: Any, relation_type: str,
                           pairs: tuple[tuple[str, str], ...]) -> list[tuple[str, str]]:
    """Current outcome findings of one link pair, as (finding id, fact id)."""
    fact_ids = {fact_id_for(fact_type, pairs) for fact_type, _value in LINK_OUTCOMES[relation_type].values()}
    return sorted((finding_id, row["fact_id"]) for finding_id, row in state.findings.items()
                  if finding_id in current_ids and isinstance(row, dict) and row.get("fact_id") in fact_ids)


def _stage_link_outcome(staged: list[dict[str, Any]], registry: Any, *, relation_type: str, outcome: str,
                        pairs: tuple[tuple[str, str], ...], evidence_id: str, actor: str, at: str,
                        claim_id: str, response_field: str, seed: str,
                        fact_type_value: tuple[str, str] | None = None) -> dict[str, str]:
    """Stage one outcome assertion citing ``evidence_id``, already staged."""
    fact_type, value = fact_type_value or LINK_OUTCOMES[relation_type][outcome]
    fact_id = fact_id_for(fact_type, pairs)
    suffix = hashlib.sha256(f"{seed}\0{fact_type}".encode("utf-8")).hexdigest()[:24]
    contribution_id = f"sli.relationship.outcome.contribution.{suffix}"
    finding_id = f"sli.relationship.outcome.finding.{suffix}"
    contribution = _act(len(staged), "contribution", {"contribution": {
        "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
        "content": {"mode": "manual-entry", "source": f"relationship-{outcome}",
                    "claim_id": claim_id, "response_field": response_field},
    }}, actor, at, suffix)
    finding = {"schema": "finding.v2", "id": finding_id, "fact_id": fact_id, "value": value,
               "basis": "attested", "evidence_ids": [evidence_id], "contribution_id": contribution_id}
    assertion = _act(len(staged) + 1, "assertion", {"finding": finding}, actor, at, suffix)
    base = project(tuple(copy.deepcopy(row) for row in staged), registry)
    if finding_id in base.findings:
        raise RelationshipRecordingRefused("submission identity has already been used")
    result = apply_contribution_batch(base, contribution_act=contribution, successor_acts=[assertion],
                                      registry=registry, record_id=f"sli.relationship.outcome.record.{suffix}")
    if result.terminal_record["phase"] != "completed":
        raise RelationshipRecordingRefused(f"link outcome admission refused: {result.terminal_record}")
    staged.extend((contribution, assertion))
    return {"fact_type": fact_type, "fact_id": fact_id, "finding_id": finding_id,
            "value": value, "evidence_id": evidence_id}


def _stage_retractions(staged: list[dict[str, Any]], registry: Any, finding_ids: Sequence[str], *,
                       actor: str, at: str, seed: str) -> list[dict[str, Any]]:
    """Stage one retraction per finding, after everything already staged."""
    retractions: list[dict[str, Any]] = []
    if not finding_ids:
        return retractions
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    for finding_id in finding_ids:
        suffix = hashlib.sha256(f"{seed}\0{finding_id}".encode("utf-8")).hexdigest()[:16]
        retraction = {"schema": "act.v1", "act_id": f"sli.relationship.end-outcome.{suffix}",
                      "kind": "finding-retracted", "actor": actor, "at": at,
                      "committed_against": len(staged), "payload": {"finding_id": finding_id}}
        apply_act(state, retraction, registry)
        staged.append(retraction)
        retractions.append(retraction)
    return retractions


def _record_submission(acts: list[dict[str, Any]], submission: dict[str, Any], registry: Any, *,
                      correction_of_finding_id: str | None = None,
                      answering_finding_id: str | None = None) -> dict[str, Any]:
    """Persist one answer and independently admit affirmative clauses.

    Submission fields: ``submission_id``, ``evidence_id``, ``actor``, ``at``,
    ``borrowing_ref``, ``schooling_fact_id``, ``statement_fact_id``,
    ``financing_response`` and ``inclusion_response``. Responses are yes/no/
    cannot-tell/unanswered. Only yes creates a claim finding. Stable opaque
    borrowing references must already identify current borrowing entities;
    this function never resolves them from labels, lenders, amounts or order.
    """
    allowed = {"yes", "no", "cannot-tell", "unanswered"}
    responses = {name: submission.get(name) for name in ("financing_response", "inclusion_response")}
    if any(value not in allowed for value in responses.values()):
        raise RelationshipRecordingRefused("each clause requires an explicit response state")
    portion_response = submission.get("interest_portion_response", "unanswered")
    if portion_response not in {"unknown", "unanswered"}:
        raise RelationshipRecordingRefused("portion status here may only be unknown or unanswered")
    required = ("submission_id", "evidence_id", "actor", "at")
    if any(not isinstance(submission.get(key), str) or not submission[key] for key in required):
        raise RelationshipRecordingRefused("submission identity and caller provenance are required")
    submission_id = submission["submission_id"]
    if "correction_of_finding_id" in submission:
        raise RelationshipRecordingRefused("correction predecessor is assigned by the correction operation")
    evidence_id = submission["evidence_id"]
    state, currency, findings, lattice = _current(acts, registry)
    active_facts = {row["fact_id"] for row in findings.values()}
    if evidence_id in state.evidence:
        raise RelationshipRecordingRefused("evidence identity has already been used")
    if any(isinstance(lifecycle.evidence.get("content"), dict) and
           lifecycle.evidence["content"].get("submission_id") == submission_id
           for lifecycle in state.evidence.values()):
        raise RelationshipRecordingRefused("submission identity has already been used")

    # Preserve every response, including unresolved choices, as source evidence.
    reference_names = ("borrowing_ref", "schooling_fact_id", "statement_fact_id")
    references = {key: submission.get(key) for key in reference_names}
    confirmed_statement_finding_id: str | None = None
    if responses["inclusion_response"] == "yes" and isinstance(references["statement_fact_id"], str):
        statement_matches = [fid for fid, row in findings.items()
                             if row.get("fact_id") == references["statement_fact_id"]]
        if len(statement_matches) == 1:
            confirmed_statement_finding_id = statement_matches[0]
    evidence_content: dict[str, Any] = {
        "submission_id": submission_id,
        "responses": responses,
        "interest_portion_response": portion_response,
        "references": references,
        "recognition_context": copy.deepcopy(submission.get("recognition_context", {})),
        "correction_of_finding_id": correction_of_finding_id,
    }
    if confirmed_statement_finding_id is not None:
        evidence_content["confirmed_statement_finding_id"] = confirmed_statement_finding_id
    evidence = {"schema": "evidence.v1", "id": evidence_id, "kind": "tax.student-loan.relationship-answer",
                "label": "Student loan relationship answers", "content": evidence_content}
    staged = list(acts)
    act_suffix = hashlib.sha256(submission_id.encode("utf-8")).hexdigest()[:16]
    staged.append(_act(len(staged), "evidence-submitted", {"evidence": evidence},
                       submission["actor"], submission["at"], act_suffix))

    admitted: dict[str, dict[str, str]] = {}
    outcomes: dict[str, dict[str, str]] = {}
    ending: list[str] = []
    record_outcomes = link_outcomes_adopted(state)
    current_ids = currency.current_finding_ids
    for clause, kind in (("financing_response", "financing"),
                         ("inclusion_response", "statement-inclusion")):
        response = responses[clause]
        relation_type = FINANCING if kind == "financing" else STATEMENT_INCLUSION
        source_name = "schooling_fact_id" if kind == "financing" else "statement_fact_id"
        if (record_outcomes and kind == "statement-inclusion" and response == "cannot-tell"
                and not isinstance(references["borrowing_ref"], str)
                and isinstance(references["statement_fact_id"], str)):
            # The person named the statement but cannot tell which loan it
            # covers: keep that doubt on the statement, never pick a loan.
            doubted = lattice.get(references["statement_fact_id"])
            if (doubted is None or doubted.fact_type_id != STATEMENT_TYPE
                    or references["statement_fact_id"] not in active_facts):
                raise RelationshipRecordingRefused("current 1098-E box-1 source is missing or ambiguous")
            outcomes["statement-scope"] = _stage_link_outcome(
                staged, registry, relation_type=STATEMENT_INCLUSION, outcome="cannot-tell",
                pairs=tuple((str(k), str(v)) for k, v in doubted.keys), evidence_id=evidence_id,
                actor=submission["actor"], at=submission["at"],
                claim_id=f"{submission_id}.statement-inclusion-scope", response_field=clause,
                seed=f"{submission_id}\0statement-scope",
                fact_type_value=(STATEMENT_INCLUSION_SCOPE_UNRESOLVED,
                                 STATEMENT_INCLUSION_SCOPE_UNRESOLVED_VALUE))
            continue
        if response in {"no", "cannot-tell"}:
            # An identified no or cannot-tell is recorded as its own current
            # outcome; without both references there is no pair to key.
            if not record_outcomes or not isinstance(references["borrowing_ref"], str) or \
                    not isinstance(references[source_name], str):
                continue
        elif response != "yes":
            continue
        borrowing = references["borrowing_ref"]
        if not isinstance(borrowing, str):
            raise RelationshipRecordingRefused("affirmative clause has no identified borrowing")
        entity_lifecycle = state.fact_state.entities.get(borrowing)
        if entity_lifecycle is None or entity_lifecycle.status != "current" or entity_lifecycle.entity.get("kind") != BORROWING_KIND:
            raise RelationshipRecordingRefused("borrowing reference is missing, stale, or wrong-kind")
        if kind == "financing":
            school_id = references["schooling_fact_id"]
            school = lattice.get(school_id) if isinstance(school_id, str) else None
            if school is None or school.fact_type_id != SCHOOLING or school_id not in active_facts:
                raise RelationshipRecordingRefused("schooling situation is missing, stale, or ambiguous")
            fact_type = FINANCING
            pairs = _link_pairs(FINANCING, borrowing, school.keys)
            value = "sli.financing.affirmed"
            claim_id = f"{submission_id}.financing"
        else:
            statement_id = references["statement_fact_id"]
            statement = lattice.get(statement_id) if isinstance(statement_id, str) else None
            if statement is None or statement.fact_type_id != STATEMENT_TYPE or statement_id not in active_facts:
                raise RelationshipRecordingRefused("current 1098-E box-1 source is missing or ambiguous")
            fact_type = STATEMENT_INCLUSION
            pairs = _link_pairs(STATEMENT_INCLUSION, borrowing, statement.keys)
            value = "sli.statement-inclusion.affirmed"
            claim_id = f"{submission_id}.statement-inclusion"
        prior_outcomes = (_current_link_outcomes(state, current_ids, relation_type, pairs)
                          if record_outcomes else [])
        if record_outcomes and kind == "statement-inclusion":
            # An identified answer on this statement ends its unkeyed doubt.
            doubt = fact_id_for(STATEMENT_INCLUSION_SCOPE_UNRESOLVED,
                                tuple(pair for pair in pairs if pair[0] != "borrowing"))
            ending.extend(fid for fid, row in findings.items() if row.get("fact_id") == doubt)
        if response != "yes":
            affirmed = [fid for fid, row in findings.items() if row.get("fact_id") == fact_id_for(fact_type, pairs)]
            if any(fid != answering_finding_id for fid in affirmed):
                raise RelationshipRecordingRefused(
                    f"this {kind} link is currently affirmed; answer that affirmation instead")
            written = _stage_link_outcome(
                staged, registry, relation_type=relation_type, outcome=response, pairs=pairs,
                evidence_id=evidence_id, actor=submission["actor"], at=submission["at"],
                claim_id=f"{claim_id}-{response}", response_field=clause, seed=f"{submission_id}\0{kind}")
            outcomes[kind] = written
            # The same outcome again is an ordinary correction of that fact;
            # a different earlier outcome on this pair ends after this write.
            ending.extend(fid for fid, prior_fact in prior_outcomes if prior_fact != written["fact_id"])
            continue
        ending.extend(fid for fid, _prior_fact in prior_outcomes)
        fact_id = fact_id_for(fact_type, pairs)
        if fact_id in active_facts:
            raise RelationshipRecordingRefused(f"active {kind} identity already has support")
        suffix = hashlib.sha256(f"{submission_id}\0{kind}".encode()).hexdigest()[:24]
        contribution_id = f"sli.relationship.contribution.{suffix}"
        finding_id = f"sli.relationship.finding.{suffix}"
        contribution = _act(len(staged), "contribution", {"contribution": {
            "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
            "content": {"mode": "manual-entry", "source": "ordinary-relationship-answer",
                        "claim_id": claim_id, "response_field": clause},
        }}, submission["actor"], submission["at"], suffix)
        finding = {"schema": "finding.v2", "id": finding_id, "fact_id": fact_id,
                   "value": value, "basis": "attested", "evidence_ids": [evidence_id],
                   "contribution_id": contribution_id}
        assertion = _act(len(staged) + 1, "assertion", {"finding": finding},
                         submission["actor"], submission["at"], suffix)
        base = project(tuple(copy.deepcopy(row) for row in staged), registry)
        result = apply_contribution_batch(base, contribution_act=contribution,
                                          successor_acts=[assertion], registry=registry,
                                          record_id=f"sli.relationship.record.{suffix}")
        if result.terminal_record["phase"] != "completed":
            raise RelationshipRecordingRefused(f"ordinary contribution admission refused: {result.terminal_record}")
        staged.extend((contribution, assertion))
        admitted[kind] = {"claim_id": claim_id, "fact_id": fact_id,
                          "finding_id": finding_id, "evidence_id": evidence_id}
    # Earlier outcomes end only after the new standing is staged, so an
    # interrupted save leaves the pair with both, never with neither.
    ended = _stage_retractions(staged, registry, sorted(set(ending)), actor=submission["actor"],
                               at=submission["at"], seed=submission_id)
    acts[:] = staged
    recorded: dict[str, Any] = {"submission_id": submission_id, "evidence_id": evidence_id,
                                "responses": responses, "claims": admitted}
    if record_outcomes:
        recorded["outcomes"] = outcomes
        recorded["ended_outcome_finding_ids"] = [row["payload"]["finding_id"] for row in ended]
    return recorded


def record_submission(acts: list[dict[str, Any]], submission: dict[str, Any], registry: Any) -> dict[str, Any]:
    """Record a normal answer; callers cannot supply correction lineage."""
    return _record_submission(acts, submission, registry)


def introduce_borrowing_reference_durably(log: ActLog, registry: Any, *, reference_id: str,
                                          description: str, actor: str, at: str) -> dict[str, Any]:
    """Introduce one person-distinguished borrowing subject with an opaque id.

    The caller owns the opaque address and supplies the person's description.
    Repeated descriptions are allowed under separate addresses; the function
    never merges or resolves subjects from labels, lenders, values, or order.
    """
    if not all(isinstance(value, str) and value for value in (reference_id, description, actor, at)):
        raise RelationshipRecordingRefused("borrowing reference, description, actor, and time are required")
    before = log.read()
    state = project(before.acts, registry)
    existing = state.fact_state.entities.get(reference_id)
    if existing is not None:
        raise RelationshipRecordingRefused("borrowing reference address has already been used")
    suffix = hashlib.sha256(reference_id.encode("utf-8")).hexdigest()[:16]
    item = {"schema": "act.v1", "act_id": f"sli.borrowing.reference.{suffix}",
            "kind": "entity-introduced", "actor": actor, "at": at,
            "committed_against": before.revision,
            "payload": {"entity": {"schema": "entity.v1", "id": reference_id,
                                     "kind": BORROWING_KIND, "label": description}}}
    apply_act(state, item, registry)
    revision = log.append(item, expected_revision=before.revision)
    recovered = project(log.read().acts, registry)
    return {"reference_id": reference_id, "act": item, "revision": revision, "state": recovered}


def record_submission_durably(log: ActLog, submission: dict[str, Any], registry: Any, *,
                             expected_revision: int | None = None) -> dict[str, Any]:
    """Admit one submission, append its acts, and return a fresh projection.

    All semantic validation and contribution admission finish before anything
    is written, and the save's acts are written as one batch. The log remains
    the authority; the returned state is reprojected from a fresh read.
    """
    before = _read_for_save(log, expected_revision)
    staged = [copy.deepcopy(row) for row in before.acts]
    result = record_submission(staged, submission, registry)
    revision = _commit_save(log, before, staged, reviewed=expected_revision is not None)
    recovered = log.read()
    state = project(recovered.acts, registry)
    result["revision"] = revision
    result["state"] = state
    return result


def _relationship_retraction(state: Any, finding_id: str, actor: str, at: str,
                              act_id: str, revision: int, registry: Any) -> dict[str, Any]:
    finding = state.findings.get(finding_id)
    if finding is None:
        raise RelationshipRecordingRefused("relationship claim finding is missing")
    fact = facts_of(state.fact_state, include_displaced=True).get(finding["fact_id"])
    if fact is None or fact.fact_type_id not in {FINANCING, STATEMENT_INCLUSION}:
        raise RelationshipRecordingRefused("named finding is not a relationship claim")
    retraction = {"schema": "act.v1", "act_id": act_id, "kind": "finding-retracted",
                  "actor": actor, "at": at, "committed_against": revision,
                  "payload": {"finding_id": finding_id}}
    apply_act(state, retraction, registry)
    return retraction


def withdraw_relationship_claim_durably(log: ActLog, registry: Any, *, finding_id: str,
                                         actor: str, at: str) -> dict[str, Any]:
    """End support for one identified relationship claim and retain history.

    With relationship bundle v2 adopted, the withdrawal is also recorded as
    the pair's current withdrawn outcome, in the same save that ends the
    affirmation. The save is written as one batch, so an interruption leaves
    either the affirmation or the withdrawal, never part of both.
    """
    before = log.read()
    state = project(before.acts, registry)
    if link_outcomes_adopted(state):
        return _withdraw_with_outcome_durably(log, registry, before=before, state=state,
                                              finding_id=finding_id, actor=actor, at=at)
    suffix = hashlib.sha256(f"{finding_id}\0{at}\0withdraw".encode()).hexdigest()[:16]
    retraction = _relationship_retraction(state, finding_id, actor, at,
                                          f"sli.relationship.retract.{suffix}", before.revision,
                                          registry)
    revision = log.append(retraction, expected_revision=before.revision)
    recovered = log.read()
    return {"finding_id": finding_id, "retraction_act": retraction, "revision": revision,
            "state": project(recovered.acts, registry)}


def _withdraw_with_outcome_durably(log: ActLog, registry: Any, *, before: Any, state: Any,
                                   finding_id: str, actor: str, at: str) -> dict[str, Any]:
    if before.incomplete_tail is not None:
        raise RelationshipRecordingRefused("ActLog has an incomplete tail")
    finding = state.findings.get(finding_id)
    if finding is None:
        raise RelationshipRecordingRefused("relationship claim finding is missing")
    fact = facts_of(state.fact_state, include_displaced=True).get(finding["fact_id"])
    if fact is None or fact.fact_type_id not in {FINANCING, STATEMENT_INCLUSION}:
        raise RelationshipRecordingRefused("named finding is not a relationship claim")
    current_ids = compute_currency(state).current_finding_ids
    if finding_id not in current_ids:
        raise RelationshipRecordingRefused("named relationship claim is not current")
    pairs = tuple((str(key), str(value)) for key, value in fact.keys)
    suffix = hashlib.sha256(f"{finding_id}\0{at}\0withdraw".encode()).hexdigest()[:16]
    evidence_id = f"sli.relationship.withdrawal.evidence.{suffix}"
    if evidence_id in state.evidence:
        raise RelationshipRecordingRefused("this withdrawal has already been recorded")
    evidence = {"schema": "evidence.v1", "id": evidence_id, "kind": WITHDRAWAL_EVIDENCE_KIND,
                "label": "Student loan relationship withdrawal",
                "content": {"withdrawn_finding_id": finding_id, "relationship_type": fact.fact_type_id,
                            "fact_id": finding["fact_id"]}}
    staged = [copy.deepcopy(row) for row in before.acts]
    staged.append(_act(len(staged), "evidence-submitted", {"evidence": evidence}, actor, at, suffix))
    written = _stage_link_outcome(
        staged, registry, relation_type=fact.fact_type_id, outcome="withdrawn", pairs=pairs,
        evidence_id=evidence_id, actor=actor, at=at, claim_id=f"{finding_id}.withdrawn",
        response_field="withdrawal", seed=f"{finding_id}\0{at}\0withdraw")
    prior = [fid for fid, prior_fact in _current_link_outcomes(state, current_ids, fact.fact_type_id, pairs)
             if prior_fact != written["fact_id"]]
    _stage_retractions(staged, registry, prior, actor=actor, at=at, seed=f"{finding_id}\0{at}\0withdraw")
    working = project(tuple(copy.deepcopy(row) for row in staged), registry)
    retraction = _relationship_retraction(working, finding_id, actor, at,
                                          f"sli.relationship.retract.{suffix}", len(staged), registry)
    staged.append(retraction)
    # One batch: the withdrawn outcome and the end of the affirmation together.
    revision = _commit_save(log, before, staged)
    recovered = log.read()
    return {"finding_id": finding_id, "retraction_act": retraction, "revision": revision,
            "outcome": written, "state": project(recovered.acts, registry)}


def answer_relationship_claim_durably(log: ActLog, registry: Any, *, finding_id: str,
                                      submission: dict[str, Any], actor: str, at: str,
                                      expected_revision: int | None = None) -> dict[str, Any]:
    """Apply an identified no/cannot-tell answer to an affirmative claim.

    Without relationship bundle v2, the affirmation ends and the answer
    evidence is saved; cannot-tell also admits the sample unresolved status.
    With v2 adopted, the answer is recorded as the pair's current outcome
    (denied or unresolved) and the affirmation ends; see
    ``_stage_answer_with_outcome``. Either way the save is one batch: an
    interruption leaves the affirmation as it was, or the whole answer.
    """
    before = _read_for_save(log, expected_revision)
    result, staged = _stage_answer(before, registry, finding_id=finding_id, submission=submission,
                                   actor=actor, at=at)
    revision = _commit_save(log, before, staged, reviewed=expected_revision is not None)
    recovered = log.read()
    result.update({"revision": revision, "state": project(recovered.acts, registry)})
    return result


def _stage_answer(before: LogContents, registry: Any, *, finding_id: str, submission: dict[str, Any],
                  actor: str, at: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Stage an identified no/cannot-tell answer; return its result and the staged log."""
    state = project(before.acts, registry)
    current_ids = compute_currency(state).current_finding_ids
    predecessor = state.findings.get(finding_id)
    predecessor_fact = (facts_of(state.fact_state, include_displaced=True).get(predecessor["fact_id"])
                        if predecessor is not None else None)
    if (link_outcomes_adopted(state) and predecessor_fact is not None and
            predecessor_fact.fact_type_id in {FINANCING, STATEMENT_INCLUSION}):
        return _stage_answer_with_outcome(
            before, registry, state=state, current_ids=current_ids, finding_id=finding_id,
            predecessor_fact=predecessor_fact, submission=submission, actor=actor, at=at)
    if (predecessor is not None and predecessor_fact is not None and
            predecessor_fact.fact_type_id == STATEMENT_INCLUSION and finding_id not in current_ids and
            submission.get("inclusion_response") == "no"):
        unresolved_fact_id = fact_id_for(INCLUSION_UNRESOLVED, tuple(predecessor_fact.keys))
        unresolved = [(fid, row) for fid, row in state.findings.items()
                      if fid in current_ids and row.get("fact_id") == unresolved_fact_id]
        if len(unresolved) == 1:
            return _stage_unresolved_inclusion_no(
                before, registry, state=state, predecessor=finding_id,
                predecessor_fact=predecessor_fact, unresolved_finding_id=unresolved[0][0],
                submission=submission, actor=actor, at=at,
            )
    if predecessor is None or finding_id not in current_ids or predecessor_fact is None:
        raise RelationshipRecordingRefused("named relationship claim is not current")
    if predecessor_fact.fact_type_id not in {FINANCING, STATEMENT_INCLUSION}:
        raise RelationshipRecordingRefused("named finding is not a relationship claim")
    answer_key = "financing_response" if predecessor_fact.fact_type_id == FINANCING else "inclusion_response"
    if submission.get(answer_key) not in {"no", "cannot-tell"}:
        raise RelationshipRecordingRefused("answer must be no or cannot-tell for the named relationship")
    fact = facts_of(state.fact_state, include_displaced=True)[predecessor["fact_id"]]
    refs = {"borrowing_ref": submission.get("borrowing_ref"),
            "schooling_fact_id": submission.get("schooling_fact_id"),
            "statement_fact_id": submission.get("statement_fact_id")}
    relation_borrowing = dict(fact.keys).get("borrowing")
    relation_source = fact_id_for(SCHOOLING if predecessor_fact.fact_type_id == FINANCING else STATEMENT_TYPE,
                                  tuple((key, value) for key, value in fact.keys if key != "borrowing"))
    submitted_source = refs["schooling_fact_id"] if predecessor_fact.fact_type_id == FINANCING else refs["statement_fact_id"]
    if refs["borrowing_ref"] != relation_borrowing or submitted_source != relation_source:
        raise RelationshipRecordingRefused("answer does not identify the exact predecessor pair")
    active_facts = {row["fact_id"] for row in _current(before.acts, registry)[2].values()}
    if relation_source not in active_facts:
        raise RelationshipRecordingRefused("answer target source is no longer current")
    if submission.get("actor") != actor or submission.get("at") != at:
        raise RelationshipRecordingRefused("answer provenance must match caller-supplied actor and time")
    if (predecessor_fact.fact_type_id == STATEMENT_INCLUSION and
            submission.get("inclusion_response") == "cannot-tell" and
            INCLUSION_UNRESOLVED not in state.fact_state.fact_types):
        raise RelationshipRecordingRefused(
            "unresolved inclusion diagnostic bundle is not adopted in this workspace"
        )
    # The retraction, the answer and any unresolved status are one save, so
    # no failure can strand the predecessor as retracted without its answer.
    staged = [copy.deepcopy(row) for row in before.acts]
    suffix = hashlib.sha256(f"{finding_id}\0{at}\0answer".encode()).hexdigest()[:16]
    retraction = _relationship_retraction(state, finding_id, actor, at,
                                          f"sli.relationship.answer.{suffix}", len(staged),
                                          registry)
    staged.append(retraction)
    result = _record_submission(staged, dict(submission), registry)
    if predecessor_fact.fact_type_id == STATEMENT_INCLUSION and submission.get("inclusion_response") == "cannot-tell":
        result["unresolved_status"] = _stage_unresolved_inclusion(
            staged, registry, predecessor_fact=fact, evidence_id=str(submission["evidence_id"]),
            actor=actor, at=at, submission_id=str(submission["submission_id"]),
        )
    result.update({"predecessor_finding_id": finding_id, "retraction_act": retraction})
    return result, staged


def _stage_answer_with_outcome(before: LogContents, registry: Any, *, state: Any, current_ids: Any,
                               finding_id: str, predecessor_fact: Any, submission: dict[str, Any],
                               actor: str, at: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Stage a no or cannot-tell on one exact pair as its current outcome.

    A current affirmation ends in the same save that records the outcome.
    A pair whose affirmation already ended (an earlier outcome is current)
    records the new outcome and ends the earlier one in the same save.
    """
    relation_type = predecessor_fact.fact_type_id
    answer_key = "financing_response" if relation_type == FINANCING else "inclusion_response"
    response = submission.get(answer_key)
    if response not in {"no", "cannot-tell"}:
        raise RelationshipRecordingRefused("answer must be no or cannot-tell for the named relationship")
    pairs = tuple((str(key), str(value)) for key, value in predecessor_fact.keys)
    relation_borrowing = dict(pairs).get("borrowing")
    relation_source = fact_id_for(SCHOOLING if relation_type == FINANCING else STATEMENT_TYPE,
                                  tuple((key, value) for key, value in pairs if key != "borrowing"))
    submitted_source = submission.get("schooling_fact_id" if relation_type == FINANCING else "statement_fact_id")
    if submission.get("borrowing_ref") != relation_borrowing or submitted_source != relation_source:
        raise RelationshipRecordingRefused("answer does not identify the exact predecessor pair")
    if not any(fid in current_ids and row.get("fact_id") == relation_source
               for fid, row in state.findings.items()):
        raise RelationshipRecordingRefused("answer target source is no longer current")
    if submission.get("actor") != actor or submission.get("at") != at:
        raise RelationshipRecordingRefused("answer provenance must match caller-supplied actor and time")
    staged = [copy.deepcopy(row) for row in before.acts]
    if finding_id not in current_ids:
        if not _current_link_outcomes(state, current_ids, relation_type, pairs):
            raise RelationshipRecordingRefused("named relationship claim is not current")
        result = _record_submission(staged, submission, registry)
        retraction = None
    else:
        result = _record_submission(staged, submission, registry, answering_finding_id=finding_id)
        working = project(tuple(copy.deepcopy(row) for row in staged), registry)
        suffix = hashlib.sha256(f"{finding_id}\0{at}\0answer".encode()).hexdigest()[:16]
        retraction = _relationship_retraction(working, finding_id, actor, at,
                                              f"sli.relationship.answer.{suffix}", len(staged), registry)
        staged.append(retraction)
    result.update({"predecessor_finding_id": finding_id, "retraction_act": retraction})
    return result, staged


def _stage_unresolved_inclusion_no(before: LogContents, registry: Any, *, state: Any, predecessor: str,
                                   predecessor_fact: Any, unresolved_finding_id: str,
                                   submission: dict[str, Any], actor: str,
                                   at: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Stage an exact-pair no that retires its current sample unresolved status."""
    inclusion_fact_id = fact_id_for(STATEMENT_INCLUSION, tuple(predecessor_fact.keys))
    fact = facts_of(state.fact_state, include_displaced=True)[inclusion_fact_id]
    refs = {"borrowing_ref": submission.get("borrowing_ref"),
            "statement_fact_id": submission.get("statement_fact_id")}
    relation_borrowing = dict(fact.keys).get("borrowing")
    relation_source = fact_id_for(STATEMENT_TYPE,
                                  tuple((key, value) for key, value in fact.keys if key != "borrowing"))
    if refs["borrowing_ref"] != relation_borrowing or refs["statement_fact_id"] != relation_source:
        raise RelationshipRecordingRefused("answer does not identify the exact unresolved predecessor pair")
    current_ids = compute_currency(state).current_finding_ids
    if not any(fid in current_ids and finding.get("fact_id") == relation_source
               for fid, finding in state.findings.items()):
        raise RelationshipRecordingRefused("answer target source is no longer current")
    if submission.get("actor") != actor or submission.get("at") != at:
        raise RelationshipRecordingRefused("answer provenance must match caller-supplied actor and time")
    staged = [copy.deepcopy(row) for row in before.acts]
    suffix = hashlib.sha256(f"{unresolved_finding_id}\0{at}\0resolve-no".encode()).hexdigest()[:16]
    retraction = {"schema": "act.v1", "act_id": f"sli.relationship.resolve-unresolved-no.{suffix}",
                  "kind": "finding-retracted", "actor": actor, "at": at,
                  "committed_against": len(staged),
                  "payload": {"finding_id": unresolved_finding_id}}
    apply_act(state, retraction, registry)
    staged.append(retraction)
    saved = _record_submission(staged, dict(submission), registry)
    saved.update({"predecessor_finding_id": predecessor, "unresolved_finding_id": unresolved_finding_id,
                  "retraction_act": retraction})
    return saved, staged


def _stage_unresolved_inclusion(staged: list[dict[str, Any]], registry: Any, *, predecessor_fact: Any,
                                evidence_id: str, actor: str, at: str,
                                submission_id: str) -> dict[str, Any]:
    """Stage an inspectable diagnostic status for one cannot-tell pair."""
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    if INCLUSION_UNRESOLVED not in state.fact_state.fact_types:
        raise RelationshipRecordingRefused("unresolved inclusion diagnostic bundle is not adopted")
    fact_id = fact_id_for(INCLUSION_UNRESOLVED, tuple(predecessor_fact.keys))
    current_ids = compute_currency(state).current_finding_ids
    current_rows = [row for finding_id, row in state.findings.items()
                    if finding_id in current_ids and row.get("fact_id") == fact_id]
    if current_rows:
        raise RelationshipRecordingRefused("an unresolved status already exists for this inclusion pair")
    suffix = hashlib.sha256(f"{submission_id}\0unresolved-inclusion".encode("utf-8")).hexdigest()[:24]
    contribution_id = f"sli.relationship.unresolved.contribution.{suffix}"
    finding_id = f"sli.relationship.unresolved.finding.{suffix}"
    contribution = _act(len(staged), "contribution", {"contribution": {
        "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
        "content": {"mode": "manual-entry", "source": "relationship-cannot-tell",
                    "claim_id": f"{submission_id}.statement-inclusion-unresolved",
                    "response_field": "inclusion_response"},
    }}, actor, at, suffix)
    finding = {"schema": "finding.v2", "id": finding_id, "fact_id": fact_id,
               "value": "sli.statement-inclusion.unresolved", "basis": "attested",
               "evidence_ids": [evidence_id], "contribution_id": contribution_id}
    assertion = _act(len(staged) + 1, "assertion", {"finding": finding}, actor, at, suffix)
    admission = apply_contribution_batch(state, contribution_act=contribution,
                                         successor_acts=[assertion], registry=registry,
                                         record_id=f"sli.relationship.unresolved.record.{suffix}")
    if admission.terminal_record["phase"] != "completed":
        raise RelationshipRecordingRefused("unresolved inclusion status failed contribution admission")
    staged.extend((contribution, assertion))
    return {"fact_id": fact_id, "finding_id": finding_id}


def correct_relationship_claim_durably(log: ActLog, registry: Any, *, finding_id: str,
                                        successor: dict[str, Any], actor: str, at: str,
                                        expected_revision: int | None = None) -> dict[str, Any]:
    """Retire one predecessor and admit its explicitly affirmed successor, in one save.

    The successor is a complete ordinary submission. Other clause findings
    and their evidence remain current because the retraction names one finding.
    """
    before = _read_for_save(log, expected_revision)
    state = project(before.acts, registry)
    predecessor = state.findings.get(finding_id)
    predecessor_fact = (facts_of(state.fact_state, include_displaced=True).get(predecessor["fact_id"])
                        if predecessor is not None else None)
    if predecessor_fact is None or predecessor_fact.fact_type_id not in {FINANCING, STATEMENT_INCLUSION}:
        raise RelationshipRecordingRefused("named finding is not a current relationship claim")
    response_key = "financing_response" if predecessor_fact.fact_type_id == FINANCING else "inclusion_response"
    other_key = "inclusion_response" if response_key == "financing_response" else "financing_response"
    if successor.get(response_key) != "yes" or successor.get(other_key) == "yes":
        raise RelationshipRecordingRefused("correction must affirm exactly the predecessor's relationship kind")
    if successor.get("actor") != actor or successor.get("at") != at:
        raise RelationshipRecordingRefused("correction provenance must match caller-supplied actor and time")
    current_ids = compute_currency(state).current_finding_ids
    if (finding_id not in current_ids and link_outcomes_adopted(state) and _current_link_outcomes(
            state, current_ids, predecessor_fact.fact_type_id,
            tuple((str(key), str(value)) for key, value in predecessor_fact.keys))):
        # The affirmation already ended with a recorded outcome. The successor
        # yes is admitted first; the outcome it replaces ends after it.
        staged = [copy.deepcopy(row) for row in before.acts]
        result = _record_submission(staged, successor, registry, correction_of_finding_id=finding_id)
        revision = _commit_save(log, before, staged, reviewed=expected_revision is not None)
        recovered = log.read()
        result.update({"predecessor_finding_id": finding_id, "retraction_act": None,
                       "revision": revision, "state": project(recovered.acts, registry)})
        return result
    if finding_id not in current_ids:
        if predecessor_fact.fact_type_id != STATEMENT_INCLUSION:
            raise RelationshipRecordingRefused("named relationship claim is not current")
        unresolved_id = fact_id_for(INCLUSION_UNRESOLVED, tuple(predecessor_fact.keys))
        unresolved = [(fid, row) for fid, row in state.findings.items()
                      if fid in current_ids and row.get("fact_id") == unresolved_id]
        if len(unresolved) != 1:
            raise RelationshipRecordingRefused("named relationship claim is not current")
        suffix = hashlib.sha256(f"{finding_id}\0{at}\0resolve-yes".encode()).hexdigest()[:16]
        unresolved_finding_id = unresolved[0][0]
        retraction = {"schema": "act.v1", "act_id": f"sli.relationship.resolve-unresolved.{suffix}",
                      "kind": "finding-retracted", "actor": actor, "at": at,
                      "committed_against": before.revision,
                      "payload": {"finding_id": unresolved_finding_id}}
        apply_act(state, retraction, registry)
        predecessor_retraction = None
    else:
        suffix = hashlib.sha256(f"{finding_id}\0{at}\0correct".encode()).hexdigest()[:16]
        retraction = _relationship_retraction(state, finding_id, actor, at,
                                              f"sli.relationship.correct.{suffix}", before.revision,
                                              registry)
        predecessor_retraction = retraction
    staged = [copy.deepcopy(row) for row in before.acts]
    if predecessor_retraction is not None:
        staged.append(predecessor_retraction)
    else:
        staged.append(retraction)
    result = _record_submission(staged, successor, registry, correction_of_finding_id=finding_id)
    # The predecessor ends and its successor is admitted in one save.
    revision = _commit_save(log, before, staged, reviewed=expected_revision is not None)
    recovered = log.read()
    result["predecessor_finding_id"] = finding_id
    result["retraction_act"] = retraction
    result["revision"] = revision
    result["state"] = project(recovered.acts, registry)
    return result


def _borrowing_answer_target(state: Any, question: object, borrowing_ref: object,
                             response: object) -> tuple[str, str]:
    """Validate one ordinary borrowing answer and return its fact type and id."""
    fact_type = BORROWING_QUESTIONS.get(question) if isinstance(question, str) else None
    if fact_type is None:
        raise RelationshipRecordingRefused("unknown borrowing question")
    if response not in _BORROWING_RESPONSES:
        raise RelationshipRecordingRefused("a borrowing answer must be yes, no, or cannot-tell")
    if fact_type not in state.fact_state.fact_types:
        raise RelationshipRecordingRefused(
            "borrowing answer vocabulary (relationship bundle v2) is not adopted in this workspace")
    entity = state.fact_state.entities.get(borrowing_ref) if isinstance(borrowing_ref, str) else None
    if entity is None or entity.status != "current" or entity.entity.get("kind") != BORROWING_KIND:
        raise RelationshipRecordingRefused("borrowing reference is missing, stale, or wrong-kind")
    return fact_type, fact_id_for(fact_type, (("borrowing", str(borrowing_ref)),))


def _record_borrowing_answer_durably(log: ActLog, registry: Any, *, question: str, borrowing_ref: str,
                                     response: str, submission_id: str, evidence_id: str,
                                     actor: str, at: str, recognition_context: dict[str, Any] | None,
                                     expected_revision: int | None,
                                     correction_of_finding_id: str | None) -> dict[str, Any]:
    if not all(isinstance(value, str) and value for value in (submission_id, evidence_id, actor, at)):
        raise RelationshipRecordingRefused("submission identity and caller provenance are required")
    before = _read_for_save(log, expected_revision)
    staged = [copy.deepcopy(row) for row in before.acts]
    adoption = _stage_relationship_v2_adoption(staged, registry, question=question, actor=actor, at=at)
    state, _currency, findings, _lattice = _current(staged, registry)
    fact_type, fact_id = _borrowing_answer_target(state, question, borrowing_ref, response)
    current = [finding_id for finding_id, row in findings.items() if row.get("fact_id") == fact_id]
    if correction_of_finding_id is None and current:
        raise RelationshipRecordingRefused(
            "this borrowing already has a current answer to this question; correct or withdraw it")
    if correction_of_finding_id is not None and current != [correction_of_finding_id]:
        raise RelationshipRecordingRefused("correction does not name this borrowing's current answer")
    if evidence_id in state.evidence:
        raise RelationshipRecordingRefused("evidence identity has already been used")
    if any(isinstance(lifecycle.evidence.get("content"), dict) and
           lifecycle.evidence["content"].get("submission_id") == submission_id
           for lifecycle in state.evidence.values()):
        raise RelationshipRecordingRefused("submission identity has already been used")
    evidence = {"schema": "evidence.v1", "id": evidence_id, "kind": BORROWING_ANSWER_EVIDENCE_KIND,
                "label": "Student loan borrowing answer",
                "content": {"submission_id": submission_id, "question": question, "response": response,
                            "borrowing_ref": borrowing_ref,
                            "recognition_context": copy.deepcopy(recognition_context or {}),
                            "correction_of_finding_id": correction_of_finding_id}}
    suffix = hashlib.sha256(f"{submission_id}\0{question}".encode("utf-8")).hexdigest()[:24]
    contribution_id = f"sli.borrowing-answer.contribution.{suffix}"
    finding_id = f"sli.borrowing-answer.finding.{suffix}"
    if finding_id in state.findings:
        raise RelationshipRecordingRefused("submission identity has already been used")
    revision = len(staged)
    evidence_act = _act(revision, "evidence-submitted", {"evidence": evidence}, actor, at, suffix)
    contribution = _act(revision + 1, "contribution", {"contribution": {
        "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
        "content": {"mode": "manual-entry", "source": "ordinary-borrowing-answer",
                    "question": question},
    }}, actor, at, suffix)
    finding = {"schema": "finding.v2", "id": finding_id, "fact_id": fact_id, "value": response,
               "basis": "attested", "evidence_ids": [evidence_id], "contribution_id": contribution_id}
    assertion = _act(revision + 2, "assertion", {"finding": finding}, actor, at, suffix)
    base = project(tuple(copy.deepcopy(row) for row in (*staged, evidence_act)), registry)
    admission = apply_contribution_batch(base, contribution_act=contribution, successor_acts=[assertion],
                                         registry=registry,
                                         record_id=f"sli.borrowing-answer.record.{suffix}")
    if admission.terminal_record["phase"] != "completed":
        raise RelationshipRecordingRefused(f"ordinary contribution admission refused: {admission.terminal_record}")
    staged.extend((evidence_act, contribution, assertion))
    # One save: the bundle adoption (if any), the evidence and the answer.
    committed = _commit_save(log, before, staged, reviewed=True)
    recovered = log.read()
    return {"submission_id": submission_id, "question": question, "fact_type": fact_type,
            "fact_id": fact_id, "finding_id": finding_id, "evidence_id": evidence_id,
            "response": response, "predecessor_finding_id": correction_of_finding_id,
            "adopted_bundle_version": adoption,
            "revision": committed, "state": project(recovered.acts, registry)}


RELATIONSHIP_BUNDLE_ID = "tax.us.2025.sli-relationship-source"


def _stage_relationship_v2_adoption(staged: list[dict[str, Any]], registry: Any, *, question: str,
                                    actor: str, at: str) -> str | None:
    """Stage the adoption of relationship bundle v2 before a first borrowing answer.

    Track 7, carried item 1. A workspace that adopted only relationship bundle
    v1 cannot hold the two borrowing answers. When the person first answers
    one, the same save adopts v2 first. Nothing else is staged, and a
    workspace that never adopted the relationship vocabulary is left alone.

    v1 kept no current fact for a link answered no or cannot tell, or
    withdrawn. Under v2 such an answer blocks the statement or keeps the
    loan-link path present; adopted over a v1 history, it would read as never
    said. That history is refused with a reason instead of adopted.
    """
    fact_type = BORROWING_QUESTIONS.get(question)
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    fact_types = state.fact_state.fact_types
    if fact_type is None or fact_type in fact_types:
        return None
    if FINANCING not in fact_types or STATEMENT_INCLUSION not in fact_types:
        return None
    if _v1_link_answers_without_a_current_fact(state):
        raise RelationshipRecordingRefused(
            "this workspace recorded a link answer of no, cannot tell or a withdrawal before relationship "
            "bundle v2; v2 has no record of those answers, so it is not adopted automatically and the "
            "borrowing questions cannot be saved here yet")
    from packages.tax.loader import load_sli_relationship_source_bundle

    bundle = load_sli_relationship_source_bundle()
    suffix = hashlib.sha256(f"{bundle['id']}\0{bundle['version']}\0{len(staged)}".encode("utf-8")).hexdigest()[:16]
    adoption = {"schema": "act.v1", "act_id": f"sli.relationship.bundle-adoption.{suffix}",
                "kind": "bundle-adoption", "actor": actor, "at": at, "committed_against": len(staged),
                "payload": {"bundle": bundle}}
    apply_act(state, adoption, registry)
    staged.append(adoption)
    return str(bundle["version"])


def _v1_link_answers_without_a_current_fact(state: Any) -> bool:
    """True when a v1-era link answer left nothing current that v2 could read.

    That is a recorded no or cannot-tell on either link, or a link claim that
    ended without a correction naming it (a withdrawal or an answer).
    """
    corrected: set[str] = set()
    for lifecycle in state.evidence.values():
        body = getattr(lifecycle, "evidence", None)
        if not isinstance(body, dict) or body.get("kind") != "tax.student-loan.relationship-answer":
            continue
        content = body.get("content")
        if not isinstance(content, dict):
            continue
        responses = content.get("responses")
        if isinstance(responses, dict) and any(
                responses.get(name) in {"no", "cannot-tell"}
                for name in ("financing_response", "inclusion_response")):
            return True
        predecessor = content.get("correction_of_finding_id")
        if isinstance(predecessor, str):
            corrected.add(predecessor)
    current_ids = compute_currency(state).current_finding_ids
    all_facts = facts_of(state.fact_state, include_displaced=True)
    for finding_id, row in state.findings.items():
        if not isinstance(row, dict) or finding_id in current_ids or finding_id in corrected:
            continue
        fact = all_facts.get(row.get("fact_id", ""))
        if fact is not None and fact.fact_type_id in {FINANCING, STATEMENT_INCLUSION}:
            return True
    return False


def record_borrowing_answer_durably(log: ActLog, registry: Any, *, question: str, borrowing_ref: str,
                                    response: str, submission_id: str, evidence_id: str,
                                    actor: str, at: str,
                                    recognition_context: dict[str, Any] | None = None,
                                    expected_revision: int | None = None) -> dict[str, Any]:
    """Record one ordinary answer about one identified borrowing.

    ``question`` is ``loan-paid-only-school-costs`` or
    ``enrolled-at-least-half-time``; ``response`` is yes, no or cannot-tell.
    The answer is its own fact with its own evidence. A borrowing that
    already has a current answer to the question is refused: correct or
    withdraw that answer instead. Nothing here draws a tax conclusion. In a
    workspace with only relationship bundle v1, the same save adopts v2 first.
    """
    return _record_borrowing_answer_durably(
        log, registry, question=question, borrowing_ref=borrowing_ref, response=response,
        submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
        recognition_context=recognition_context, expected_revision=expected_revision,
        correction_of_finding_id=None)


def correct_borrowing_answer_durably(log: ActLog, registry: Any, *, finding_id: str, question: str,
                                     borrowing_ref: str, response: str, submission_id: str,
                                     evidence_id: str, actor: str, at: str,
                                     recognition_context: dict[str, Any] | None = None,
                                     expected_revision: int | None = None) -> dict[str, Any]:
    """Replace one borrowing's current answer; the earlier answer stays in history.

    The successor is a new finding of the same fact, so the kernel's ordinary
    correction displaces the predecessor. ``finding_id`` must be that
    borrowing's current answer to ``question``.
    """
    return _record_borrowing_answer_durably(
        log, registry, question=question, borrowing_ref=borrowing_ref, response=response,
        submission_id=submission_id, evidence_id=evidence_id, actor=actor, at=at,
        recognition_context=recognition_context, expected_revision=expected_revision,
        correction_of_finding_id=finding_id)


def withdraw_borrowing_answer_durably(log: ActLog, registry: Any, *, finding_id: str,
                                      actor: str, at: str) -> dict[str, Any]:
    """End one current borrowing answer; it becomes a missing answer, not a no."""
    before = log.read()
    if before.incomplete_tail is not None:
        raise RelationshipRecordingRefused("ActLog has an incomplete tail")
    state = project(before.acts, registry)
    finding = state.findings.get(finding_id)
    fact = (facts_of(state.fact_state, include_displaced=True).get(finding["fact_id"])
            if finding is not None else None)
    if fact is None or fact.fact_type_id not in set(BORROWING_QUESTIONS.values()):
        raise RelationshipRecordingRefused("named finding is not a borrowing answer")
    if finding_id not in compute_currency(state).current_finding_ids:
        raise RelationshipRecordingRefused("named borrowing answer is not current")
    suffix = hashlib.sha256(f"{finding_id}\0{at}\0withdraw-answer".encode()).hexdigest()[:16]
    retraction = {"schema": "act.v1", "act_id": f"sli.borrowing-answer.retract.{suffix}",
                  "kind": "finding-retracted", "actor": actor, "at": at,
                  "committed_against": before.revision, "payload": {"finding_id": finding_id}}
    apply_act(state, retraction, registry)
    revision = log.append(retraction, expected_revision=before.revision)
    recovered = log.read()
    return {"finding_id": finding_id, "retraction_act": retraction, "revision": revision,
            "state": project(recovered.acts, registry)}
