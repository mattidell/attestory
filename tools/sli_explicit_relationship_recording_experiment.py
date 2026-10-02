"""Synthetic Track 13 recorder over the existing Track 10 source declarations."""
from __future__ import annotations

import copy
import hashlib
from typing import Any, cast

from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import project
from tests.support import act, demo_evidence
from tests.test_sli_track10_saved_account_evidence import FINANCE, MEMBERSHIP, SCHOOL


class RecordingRefused(ValueError):
    """The explicit claim cannot be validated against current source facts."""


def record_explicit_claim(acts: list[dict[str, Any]], claim: dict[str, Any], registry: Any) -> dict[str, str] | None:
    """Validate and ordinarily admit one affirmative supplied relationship claim.

    Claims have claim_id, kind, attestation, evidence_id and references. Financing
    references name a borrowing entity and exact schooling fact. Membership
    references name a borrowing entity and exact box-1 statement fact and scope.
    """
    if claim.get("attestation") is not True:
        return None
    claim_id_value = claim.get("claim_id")
    evidence_id_value = claim.get("evidence_id")
    refs = claim.get("references")
    if not all(isinstance(value, str) and value.startswith("demo.") for value in
               (claim_id_value, evidence_id_value)) or not isinstance(refs, dict):
        raise RecordingRefused("claim and evidence identities must be explicit synthetic addresses")
    claim_id = cast(str, claim_id_value)
    evidence_id = cast(str, evidence_id_value)
    kind = claim.get("kind")
    if kind not in {"financing", "statement-membership"}:
        raise RecordingRefused("unknown relationship claim kind")
    if kind == "statement-membership" and claim.get("scope") != "named-statement":
        raise RecordingRefused("statement membership requires named-statement scope")

    state = project(tuple(copy.deepcopy(row) for row in acts), registry)
    currency = __import__("packages.kernel.currency", fromlist=["compute_currency"]).compute_currency(state)
    lattice = facts_of(state.fact_state)
    current = {finding["fact_id"]: finding for finding_id, finding in state.findings.items()
               if finding_id in currency.current_finding_ids}
    current_finding_rows = [state.findings[finding_id] for finding_id in currency.current_finding_ids
                            if finding_id in state.findings]
    for active in current_finding_rows:
        active_evidence_ids = active.get("evidence_ids", [])
        if evidence_id in active_evidence_ids:
            raise RecordingRefused("evidence identity is already active")
        for active_evidence_id in active_evidence_ids:
            lifecycle = state.evidence.get(active_evidence_id)
            evidence = lifecycle.evidence if lifecycle is not None else {}
            content = evidence.get("content", {})
            if isinstance(content, dict) and content.get("claim_id") == claim_id:
                raise RecordingRefused("claim ID is already active")
    borrowing_value = refs.get("borrowing")
    if not isinstance(borrowing_value, str):
        raise RecordingRefused("borrowing referent is missing or stale")
    borrowing = borrowing_value
    borrowing_lifecycle = state.fact_state.entities.get(borrowing)
    if (borrowing_lifecycle is None or borrowing_lifecycle.status != "current" or
            borrowing_lifecycle.entity.get("kind") != "demo.sli-borrowing"):
        raise RecordingRefused("borrowing referent is missing or stale")
    if kind == "financing":
        school_id = refs.get("schooling_fact_id")
        school = lattice.get(school_id) if isinstance(school_id, str) else None
        if school is None or school.fact_type_id != SCHOOL or school_id not in current:
            raise RecordingRefused("schooling referent is missing, stale, or wrong-kind")
        school_keys = {str(key): str(value) for key, value in school.keys}
        fact_type = FINANCE
        pairs = (("borrowing", borrowing),) + tuple(school_keys.items())
        value = "demo.financing.observed"
        detail = f"Synthetic supplied claim {claim_id}: borrowing {borrowing} financed the exact referenced schooling circumstance."
    else:
        statement_id = refs.get("statement_fact_id")
        statement = lattice.get(statement_id) if isinstance(statement_id, str) else None
        if statement is None or statement_id not in current or statement.fact_type_id != "tax.us.2025.f1098e.box1-student-loan-interest":
            raise RecordingRefused("statement referent is missing, stale, or wrong-kind")
        if not isinstance(refs.get("borrowing"), str):
            raise RecordingRefused("borrowing referent is missing")
        fact_type = MEMBERSHIP
        pairs = tuple((str(key), str(value)) for key, value in statement.keys) + (("borrowing", borrowing),)
        value = "demo.membership.observed"
        detail = f"Synthetic supplied claim {claim_id}: borrowing {borrowing} is associated with the named statement only."
    fact_id = fact_id_for(fact_type, pairs)
    if any(row.get("fact_id") == fact_id and fid in currency.current_finding_ids
           for fid, row in state.findings.items()):
        raise RecordingRefused("ambiguous duplicate active relationship identity")

    revision_key = hashlib.sha256(f"{claim_id}\0{evidence_id}".encode("utf-8")).hexdigest()[:20]
    finding_id = f"demo.finding.sli.track13.{revision_key}"
    contribution_id = f"demo.contribution.sli.track13.{revision_key}"
    staged = list(acts)
    evidence_content = {"claim_id": claim_id, "kind": kind, "attestation": True,
                        "references": copy.deepcopy(refs), "assertion": detail}
    if kind == "statement-membership":
        evidence_content["scope"] = "named-statement"
    staged.append(act(len(staged), "evidence-submitted", {"evidence": demo_evidence(
        evidence_id, "Synthetic explicit relationship assertion", evidence_content)}))
    contribution = act(len(staged), "contribution", {"contribution": {
        "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
        "content": {"mode": "manual-entry", "synthetic": True},
    }})
    finding = {"schema": "finding.v2", "id": finding_id, "fact_id": fact_id,
               "value": value, "basis": "attested", "evidence_ids": [evidence_id],
               "contribution_id": contribution_id}
    assertion = act(len(staged) + 1, "assertion", {"finding": finding})
    base = project(tuple(copy.deepcopy(row) for row in staged), registry)
    admitted = apply_contribution_batch(base, contribution_act=contribution, successor_acts=[assertion],
                                        registry=registry, record_id=f"demo.contribution-record.{claim_id}")
    if admitted.terminal_record["phase"] != "completed":
        raise RecordingRefused(f"ordinary contribution admission refused: {admitted.terminal_record}")
    staged.extend((contribution, assertion))
    acts[:] = staged
    return {"claim_id": claim_id, "fact_id": fact_id, "finding_id": finding_id,
            "evidence_id": evidence_id, "contribution_id": contribution_id}
