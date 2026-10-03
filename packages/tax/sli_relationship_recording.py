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
from packages.kernel.act_log import ActLog, ActLogError


FINANCING = "tax.us.2025.sli.financing-relationship"
STATEMENT_INCLUSION = "tax.us.2025.sli.statement-inclusion-relationship"
INCLUSION_UNRESOLVED = "demo.tax.2025.sli.statement-inclusion-unresolved"
SCHOOLING = "tax.us.2025.sli.schooling-situation"
BORROWING_KIND = "tax.us.student-loan-borrowing-reference"
STATEMENT_TYPE = "tax.us.2025.f1098e.box1-student-loan-interest"


class RelationshipRecordingRefused(ValueError):
    """The response cannot be bound to the exact current subjects supplied."""


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
    cited: list[str] = []
    for finding_id, row in state.findings.items():
        if not isinstance(finding_id, str) or not isinstance(row, dict):
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


def _record_submission(acts: list[dict[str, Any]], submission: dict[str, Any], registry: Any, *,
                      correction_of_finding_id: str | None = None) -> dict[str, Any]:
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
    for clause, kind in (("financing_response", "financing"),
                         ("inclusion_response", "statement-inclusion")):
        if responses[clause] != "yes":
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
            pairs = (("borrowing", borrowing),) + tuple((str(k), str(v)) for k, v in school.keys)
            value = "sli.financing.affirmed"
            claim_id = f"{submission_id}.financing"
        else:
            statement_id = references["statement_fact_id"]
            statement = lattice.get(statement_id) if isinstance(statement_id, str) else None
            if statement is None or statement.fact_type_id != STATEMENT_TYPE or statement_id not in active_facts:
                raise RelationshipRecordingRefused("current 1098-E box-1 source is missing or ambiguous")
            fact_type = STATEMENT_INCLUSION
            pairs = tuple((str(k), str(v)) for k, v in statement.keys) + (("borrowing", borrowing),)
            value = "sli.statement-inclusion.affirmed"
            claim_id = f"{submission_id}.statement-inclusion"
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
    acts[:] = staged
    return {"submission_id": submission_id, "evidence_id": evidence_id,
            "responses": responses, "claims": admitted}


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

    All semantic validation and contribution admission finish before the first
    append. The log remains the authority; the returned state is reprojected
    from a fresh read after the append sequence.
    """
    before = log.read()
    if expected_revision is not None and before.revision != expected_revision:
        raise RelationshipRecordingRefused("reviewed ActLog revision changed before recording")
    if before.incomplete_tail is not None:
        raise RelationshipRecordingRefused("ActLog has an incomplete tail")
    staged = [copy.deepcopy(row) for row in before.acts]
    result = record_submission(staged, submission, registry)
    additions = staged[len(before.acts):]
    revision = before.revision
    for index, item in enumerate(additions):
        append_revision = expected_revision if index == 0 and expected_revision is not None else revision
        try:
            revision = log.append(item, expected_revision=append_revision)
        except ActLogError as exc:
            if expected_revision is not None and index == 0 and "stale revision" in str(exc):
                raise RelationshipRecordingRefused("reviewed ActLog revision changed before first append") from exc
            raise
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
    """End support for one identified relationship claim and retain history."""
    before = log.read()
    state = project(before.acts, registry)
    suffix = hashlib.sha256(f"{finding_id}\0{at}\0withdraw".encode()).hexdigest()[:16]
    retraction = _relationship_retraction(state, finding_id, actor, at,
                                          f"sli.relationship.retract.{suffix}", before.revision,
                                          registry)
    revision = log.append(retraction, expected_revision=before.revision)
    recovered = log.read()
    return {"finding_id": finding_id, "retraction_act": retraction, "revision": revision,
            "state": project(recovered.acts, registry)}


def answer_relationship_claim_durably(log: ActLog, registry: Any, *, finding_id: str,
                                      submission: dict[str, Any], actor: str, at: str,
                                      expected_revision: int | None = None) -> dict[str, Any]:
    """Apply an identified no/cannot-tell answer to an affirmative claim.

    Retraction is the fail-closed transition: consumers stop seeing support
    before the answer evidence is appended. If the second append is refused or
    interrupted, the older affirmation remains historical but unusable.
    """
    before = log.read()
    if expected_revision is not None and before.revision != expected_revision:
        raise RelationshipRecordingRefused("reviewed ActLog revision changed before recording")
    if before.incomplete_tail is not None:
        raise RelationshipRecordingRefused("ActLog has an incomplete tail")
    state = project(before.acts, registry)
    current_ids = compute_currency(state).current_finding_ids
    predecessor = state.findings.get(finding_id)
    predecessor_fact = (facts_of(state.fact_state, include_displaced=True).get(predecessor["fact_id"])
                        if predecessor is not None else None)
    if (predecessor is not None and predecessor_fact is not None and
            predecessor_fact.fact_type_id == STATEMENT_INCLUSION and finding_id not in current_ids and
            submission.get("inclusion_response") == "no"):
        unresolved_fact_id = fact_id_for(INCLUSION_UNRESOLVED, tuple(predecessor_fact.keys))
        unresolved = [(fid, row) for fid, row in state.findings.items()
                      if fid in current_ids and row.get("fact_id") == unresolved_fact_id]
        if len(unresolved) == 1:
            return _answer_unresolved_inclusion_no_durably(
                log, registry, before=before, state=state, predecessor=finding_id,
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
    # Validate the complete answer before ending support. No validation failure
    # may strand the predecessor as retracted without a recordable answer.
    _record_submission([copy.deepcopy(row) for row in before.acts], submission, registry)
    suffix = hashlib.sha256(f"{finding_id}\0{at}\0answer".encode()).hexdigest()[:16]
    retraction = _relationship_retraction(state, finding_id, actor, at,
                                          f"sli.relationship.answer.{suffix}", before.revision,
                                          registry)
    revision = log.append(retraction, expected_revision=before.revision)
    try:
        result = record_submission_durably(log, dict(submission), registry, expected_revision=revision)
    except (ActLogError, RelationshipRecordingRefused) as exc:
        raise RelationshipRecordingRefused(
            "prior affirmation support is ended; the new answer was not saved"
        ) from exc
    if predecessor_fact.fact_type_id == STATEMENT_INCLUSION and submission.get("inclusion_response") == "cannot-tell":
        try:
            result["unresolved_status"] = _record_unresolved_inclusion_durably(
                log, registry, predecessor_fact=fact, evidence_id=str(submission["evidence_id"]),
                actor=actor, at=at, submission_id=str(submission["submission_id"]),
            )
        except (ActLogError, RelationshipRecordingRefused) as exc:
            raise RelationshipRecordingRefused(
                "cannot-tell answer evidence was saved, but its unresolved consumer status was not admitted"
            ) from exc
    recovered = log.read()
    result.update({"predecessor_finding_id": finding_id, "retraction_act": retraction,
                   "revision": recovered.revision, "state": project(recovered.acts, registry)})
    return result


def _answer_unresolved_inclusion_no_durably(log: ActLog, registry: Any, *, before: Any,
                                            state: Any, predecessor: str,
                                            predecessor_fact: Any, unresolved_finding_id: str,
                                            submission: dict[str, Any], actor: str,
                                            at: str) -> dict[str, Any]:
    """Save an exact-pair no and retire its current unresolved status."""
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
    # Validate the complete no answer before ending the current unresolved
    # state. This transition is fail closed if the answer append is interrupted.
    _record_submission([copy.deepcopy(row) for row in before.acts], submission, registry)
    suffix = hashlib.sha256(f"{unresolved_finding_id}\0{at}\0resolve-no".encode()).hexdigest()[:16]
    retraction = {"schema": "act.v1", "act_id": f"sli.relationship.resolve-unresolved-no.{suffix}",
                  "kind": "finding-retracted", "actor": actor, "at": at,
                  "committed_against": before.revision,
                  "payload": {"finding_id": unresolved_finding_id}}
    from packages.kernel.findings import apply_act
    apply_act(state, retraction, registry)
    revision = log.append(retraction, expected_revision=before.revision)
    try:
        saved = record_submission_durably(log, dict(submission), registry, expected_revision=revision)
    except (ActLogError, RelationshipRecordingRefused) as exc:
        raise RelationshipRecordingRefused(
            "unresolved status is ended; the new no answer was not saved"
        ) from exc
    recovered = log.read()
    saved.update({"predecessor_finding_id": predecessor, "unresolved_finding_id": unresolved_finding_id,
                  "retraction_act": retraction, "revision": recovered.revision,
                  "state": project(recovered.acts, registry)})
    return saved


def _record_unresolved_inclusion_durably(log: ActLog, registry: Any, *, predecessor_fact: Any,
                                         evidence_id: str, actor: str, at: str,
                                         submission_id: str) -> dict[str, Any]:
    """Admit an inspectable diagnostic status for one saved cannot-tell pair."""
    contents = log.read()
    if contents.incomplete_tail is not None:
        raise RelationshipRecordingRefused("ActLog has an incomplete tail")
    state = project(contents.acts, registry)
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
    contribution = _act(contents.revision, "contribution", {"contribution": {
        "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
        "content": {"mode": "manual-entry", "source": "relationship-cannot-tell",
                    "claim_id": f"{submission_id}.statement-inclusion-unresolved",
                    "response_field": "inclusion_response"},
    }}, actor, at, suffix)
    finding = {"schema": "finding.v2", "id": finding_id, "fact_id": fact_id,
               "value": "sli.statement-inclusion.unresolved", "basis": "attested",
               "evidence_ids": [evidence_id], "contribution_id": contribution_id}
    assertion = _act(contents.revision + 1, "assertion", {"finding": finding}, actor, at, suffix)
    admission = apply_contribution_batch(state, contribution_act=contribution,
                                         successor_acts=[assertion], registry=registry,
                                         record_id=f"sli.relationship.unresolved.record.{suffix}")
    if admission.terminal_record["phase"] != "completed":
        raise RelationshipRecordingRefused("unresolved inclusion status failed contribution admission")
    revision = contents.revision
    for item in (contribution, assertion):
        revision = log.append(item, expected_revision=revision)
    recovered = log.read()
    return {"fact_id": fact_id, "finding_id": finding_id, "revision": revision,
            "state": project(recovered.acts, registry)}


def correct_relationship_claim_durably(log: ActLog, registry: Any, *, finding_id: str,
                                        successor: dict[str, Any], actor: str, at: str,
                                        expected_revision: int | None = None) -> dict[str, Any]:
    """Retire one predecessor, then admit its explicitly affirmed successor.

    The successor is a complete ordinary submission. Other clause findings
    and their evidence remain current because the retraction names one finding.
    """
    before = log.read()
    if expected_revision is not None and before.revision != expected_revision:
        raise RelationshipRecordingRefused("reviewed ActLog revision changed before recording")
    if before.incomplete_tail is not None:
        raise RelationshipRecordingRefused("ActLog has an incomplete tail")
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
        from packages.kernel.findings import apply_act
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
    revision = before.revision
    for index, item in enumerate(staged[len(before.acts):]):
        append_revision = expected_revision if index == 0 and expected_revision is not None else revision
        try:
            revision = log.append(item, expected_revision=append_revision)
        except ActLogError as exc:
            if expected_revision is not None and index == 0 and "stale revision" in str(exc):
                raise RelationshipRecordingRefused("reviewed ActLog revision changed before first append") from exc
            raise
    recovered = log.read()
    result["predecessor_finding_id"] = finding_id
    result["retraction_act"] = retraction
    result["revision"] = revision
    result["state"] = project(recovered.acts, registry)
    return result
