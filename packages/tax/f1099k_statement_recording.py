"""Bounded evidence-backed answers and statements for Form 1099-K personal item sales.

This module provides durable operations to:
1. Record one Form 1099-K statement (Box 1a, Box 4, and payer and statement
   identity under packages.tax.statements) as a member of the tax.us.2025.f1099k
   family;
2. Record "I received no Form 1099-K for 2025" as the family closure at the current
   horizon;
3. Answer each circumstance question with its offered choices only (categorical
   choices, or amounts as non-negative numbers or "cannot-tell"; "not-asked" is
   refused);
4. Correct an answer, superseding it with history kept;
5. Withdraw an answer, returning the question to unanswered ("not-asked") and its
   own stop.

Multiple statements are recorded normally without artificial single-statement
refusals; the adopted rules handle multiple statements via an explicit named stop.
A statement recorded after a "no Form 1099-K" closure advances the family horizon,
letting the earlier closure cease counting.
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
from packages.kernel.horizons import current_horizon_id
from packages.tax.loader import (
    load_f1099k_bundle,
    load_f1099k_circumstances_bundle,
)
from packages.tax.statements import (
    StatementIdentityError,
    StatementKey,
    classify_assertion,
    statement_entity_id,
    statement_key,
)

BUNDLE_ID = "tax.us.2025.f1099k.vocabulary"
BUNDLE_VERSION = "v1"
CIRCUMSTANCES_BUNDLE_ID = "tax.us.2025.f1099k-circumstances.vocabulary"
CIRCUMSTANCES_BUNDLE_VERSION = "v1"

FAMILY_ID = "tax.us.2025.f1099k"
FAMILY_VERSION = "v1"


def _version_number(version: str) -> int:
    if version.startswith("v") and version[1:].isdigit():
        return int(version[1:])
    raise ValueError(f"unrecognized version format: {version!r}")


DEFAULT_FAMILY_SCOPE: dict[str, str] = {"tax-year": "2025", "subject": "demo.primary"}

CLOSURE_TYPE = "tax.us.2025.f1099k.source-closure"
STATEMENT_BOX1A = "tax.us.2025.f1099k.box1a-gross-amount"
STATEMENT_BOX4 = "tax.us.2025.f1099k.box4-federal-withholding"
STATEMENT_REASON = "tax.us.2025.f1099k.statement-loss-reason"

PAYER_ENTITY_KIND = "tax.us.1099k-platform"
STATEMENT_ENTITY_KIND = "tax.us.1099k-statement"

ANSWER_EVIDENCE_KIND = "tax.personal-item-sale.f1099k-statement-answer"
STATEMENT_EVIDENCE_KIND = "tax.personal-item-sale.f1099k-statement-document"
CLOSURE_EVIDENCE_KIND = "tax.personal-item-sale.f1099k-family-closure"

CATEGORICAL_QUESTIONS: dict[str, frozenset[str]] = {
    "covers-only-single-item": frozenset({"yes", "no", "cannot-tell"}),
    "acquired-by-purchase": frozenset({"yes", "no", "cannot-tell"}),
    "primary-purpose-at-acquisition": frozenset({
        "personal-use", "investment-or-profit", "resale-or-inventory", "cannot-tell",
    }),
    "exclusive-personal-use": frozenset({"yes", "no", "cannot-tell"}),
    "digital-asset-involvement": frozenset({"no", "yes", "cannot-tell"}),
    "shipping-arrangement": frozenset({
        "platform-pass-through", "seller-received-shipping", "none", "cannot-tell",
    }),
    "cost-basis-known": frozenset({"yes", "cannot-tell"}),
    "lasting-improvements-or-adjustments": frozenset({"no", "yes", "cannot-tell"}),
}

AMOUNT_QUESTIONS: frozenset[str] = frozenset({
    "agreed-item-price",
    "platform-fees",
    "seller-paid-shipping",
    "sales-tax-collected-by-platform",
    "refund-amount",
    "buyer-paid-shipping",
    "purchase-cost",
})

ALL_CIRCUMSTANCE_QUESTIONS: frozenset[str] = (
    frozenset(CATEGORICAL_QUESTIONS.keys()) | AMOUNT_QUESTIONS
)


class F1099KRecordingRefused(ValueError):
    """A Form 1099-K statement or answer operation cannot be admitted to the current log."""


def _require_provenance(submission_id: str, actor: str, at: str) -> None:
    if not all(isinstance(val, str) and val.strip() for val in (submission_id, actor, at)):
        raise F1099KRecordingRefused("submission identity, actor, and timestamp are required non-empty strings")


def _token(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def _act(
    index: int,
    kind: str,
    payload: dict[str, Any],
    actor: str,
    at: str,
    suffix: str,
) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"f1099k.{suffix}.{index}",
        "kind": kind,
        "actor": actor,
        "at": at,
        "committed_against": index,
        "payload": payload,
    }


def _read_for_save(log: ActLog, expected_revision: int) -> LogContents:
    before = log.read()
    if before.incomplete_tail is not None:
        raise F1099KRecordingRefused("ActLog has an incomplete tail")
    if before.revision != expected_revision:
        raise F1099KRecordingRefused(
            f"reviewed ActLog revision changed before save: expected {expected_revision}, got {before.revision}"
        )
    return before


def _commit(
    log: ActLog,
    registry: Any,
    before: LogContents,
    staged: list[dict[str, Any]],
    *,
    actor: str,
    at: str,
    suffix: str,
    finding_ids: Sequence[str],
    expected_revision: int,
) -> dict[str, Any]:
    additions = staged[len(before.acts):]
    try:
        revision = log.append_batch(additions, expected_revision=expected_revision)
    except ActLogError as exc:
        raise F1099KRecordingRefused(f"atomic answer save refused: {exc}") from exc
    fresh = log.read()
    return {
        "revision": revision,
        "finding_ids": list(finding_ids),
        "state": project(fresh.acts, registry),
        "actor": actor,
        "at": at,
    }


def _ensure_bundles(
    staged: list[dict[str, Any]],
    registry: Any,
    actor: str,
    at: str,
    suffix: str,
) -> None:
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    if STATEMENT_BOX1A not in state.fact_state.fact_types:
        bundle = load_f1099k_bundle(registry)
        act = _act(len(staged), "bundle-adoption", {"bundle": bundle}, actor, at, f"{suffix}.b1")
        staged.append(act)
        state = apply_act(state, act, registry)
    if "tax.us.2025.f1099k.covers-only-single-item" not in state.fact_state.fact_types:
        circ_bundle = load_f1099k_circumstances_bundle(registry)
        act = _act(len(staged), "bundle-adoption", {"bundle": circ_bundle}, actor, at, f"{suffix}.b2")
        staged.append(act)


def _normalize_question(name: str) -> str:
    return name.removeprefix("tax.us.2025.f1099k.")


def _validate_answer_value(question: str, value: Any) -> None:
    if value == "not-asked":
        raise F1099KRecordingRefused(f"'not-asked' is a default sentinel and cannot be recorded for {question}")
    if question in CATEGORICAL_QUESTIONS:
        allowed = CATEGORICAL_QUESTIONS[question]
        if value not in allowed:
            raise F1099KRecordingRefused(
                f"answer {value!r} is not an offered choice for {question} (offered: {sorted(allowed)})"
            )
    elif question in AMOUNT_QUESTIONS:
        if value == "cannot-tell":
            return
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise F1099KRecordingRefused(
                f"answer for amount question {question} must be a non-negative number or 'cannot-tell', got {value!r}"
            )
    else:
        raise F1099KRecordingRefused(f"question {question!r} is not part of the Form 1099-K circumstance vocabulary")


def _validate_statement_keys(keys: dict[str, str]) -> None:
    required = {"payer", "statement", "tax-year"}
    if set(keys) != required or not all(isinstance(v, str) and v.strip() for v in keys.values()):
        raise F1099KRecordingRefused("statement identity must contain non-empty payer, statement, and tax-year")


def _find_current_statement_findings(state: Any) -> list[tuple[str, dict[str, Any], dict[str, str]]]:
    """Return [(finding_id, finding, keys_dict)] for all current Box 1a findings."""
    current = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state, include_displaced=True)
    results = []
    for fid, finding in state.findings.items():
        if fid in current and finding.get("fact_id") in lattice:
            fact = lattice[finding["fact_id"]]
            if fact.fact_type_id == STATEMENT_BOX1A:
                results.append((fid, finding, dict(fact.keys)))
    return results


def _require_statement_exists(state: Any, statement_keys: dict[str, str]) -> tuple[str, dict[str, Any]]:
    stmts = _find_current_statement_findings(state)
    target = tuple(sorted(statement_keys.items()))
    for fid, finding, keys in stmts:
        if tuple(sorted(keys.items())) == target:
            return fid, finding
    raise F1099KRecordingRefused(f"statement with keys {statement_keys} is not a current Form 1099-K statement")


def _current_finding(state: Any, fact_id: str, current_ids: AbstractSet[str]) -> tuple[str, dict[str, Any]] | None:
    rows = [
        (fid, row) for fid, row in state.findings.items()
        if fid in current_ids and row.get("fact_id") == fact_id
    ]
    if len(rows) > 1:
        raise F1099KRecordingRefused("more than one current finding exists for an answer")
    return rows[0] if rows else None


def _check_evidence_ids(
    evidence_ids: Sequence[str] | dict[str, str],
    submission_id: str,
    staged: list[dict[str, Any]],
) -> None:
    id_list = list(evidence_ids.values()) if isinstance(evidence_ids, dict) else list(evidence_ids)
    if len(set(id_list)) != len(id_list) or any(not isinstance(v, str) or not v.strip() for v in id_list):
        raise F1099KRecordingRefused("evidence identities must be distinct non-empty strings")
    prior_evidence = [
        row.get("payload", {}).get("evidence", {})
        for row in staged
        if row.get("kind") == "evidence-submitted"
    ]
    if any(item.get("id") in id_list for item in prior_evidence):
        raise F1099KRecordingRefused("evidence identity has already been used")
    if any(
        item.get("content", {}).get("submission_id") == submission_id
        or item.get("content", {}).get("request_id") == submission_id
        for item in prior_evidence
    ):
        raise F1099KRecordingRefused(f"submission identity {submission_id!r} has already been used")


def _stage_answer(
    staged: list[dict[str, Any]],
    registry: Any,
    *,
    keys: dict[str, str],
    question: str,
    answer: Any,
    actor: str,
    at: str,
    evidence_id: str,
    contribution_id: str,
    finding_id: str,
    target_finding_id: str | None,
    claim_id: str,
    suffix: str,
    base_state: Any = None,
) -> tuple[str, Any]:
    norm_q = _normalize_question(question)
    _validate_answer_value(norm_q, answer)
    state = base_state if base_state is not None else project(tuple(copy.deepcopy(row) for row in staged), registry)
    full_fact_type = f"tax.us.2025.f1099k.{norm_q}"
    if full_fact_type not in state.fact_state.fact_types:
        raise F1099KRecordingRefused(f"question is not in the adopted circumstance bundle: {norm_q}")
    fact_id = fact_id_for(full_fact_type, tuple(sorted(keys.items())))
    evidence = {
        "schema": "evidence.v1",
        "id": evidence_id,
        "kind": ANSWER_EVIDENCE_KIND,
        "label": f"Recorded Form 1099-K answer: {norm_q}",
        "content": {
            "submission_id": claim_id,
            "statement": dict(keys),
            "question": norm_q,
            "answer": answer,
            "correction_target": target_finding_id,
        },
    }
    evidence_act = _act(len(staged), "evidence-submitted", {"evidence": evidence}, actor, at, suffix)
    state = apply_act(state, evidence_act, registry)
    staged.append(evidence_act)

    contribution = {
        "schema": "contribution.v1",
        "id": contribution_id,
        "evidence_id": evidence_id,
        "content": {
            "mode": "manual-entry",
            "source": "f1099k-statement-answer",
            "claim_id": claim_id,
            "question": norm_q,
        },
    }
    contribution_act = _act(len(staged), "contribution", {"contribution": contribution}, actor, at, suffix)
    finding = {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": answer,
        "basis": "attested",
        "evidence_ids": [evidence_id],
        "contribution_id": contribution_id,
    }
    assertion_act = _act(len(staged) + 1, "assertion", {"finding": finding}, actor, at, suffix)
    if finding_id in state.findings:
        raise F1099KRecordingRefused("submission or finding identity has already been used")
    admission = apply_contribution_batch(
        state,
        contribution_act=contribution_act,
        successor_acts=[assertion_act],
        registry=registry,
        record_id=f"f1099k.answer.record.{suffix}",
        workspace_revision=len(staged),
    )
    if admission.terminal_record["phase"] != "completed":
        raise F1099KRecordingRefused("answer contribution was not admitted")
    staged.extend((contribution_act, assertion_act))
    return fact_id, admission.state


def record_f1099k_statement_durably(
    log: ActLog,
    registry: Any,
    *,
    payer_id: str,
    statement_ref: str,
    box1a: float,
    box4: float,
    submission_id: str,
    evidence_id: str,
    actor: str,
    at: str,
    expected_revision: int,
    tax_year: str = "2025",
    payer_label: str = "Synthetic platform",
    statement_label: str = "Synthetic Form 1099-K",
    corrected: bool = False,
    close_family: bool = True,
    family_scope: dict[str, str] | None = None,
    answers: dict[str, Any] | None = None,
    answer_evidence_ids: dict[str, str] | None = None,
    family_version: str = FAMILY_VERSION,
) -> dict[str, Any]:
    """Record one Form 1099-K statement as a member of the tax.us.2025.f1099k family."""
    _require_provenance(submission_id, actor, at)
    before = _read_for_save(log, expected_revision)

    if not isinstance(box1a, (int, float)) or isinstance(box1a, bool) or box1a < 0:
        raise F1099KRecordingRefused("box1a gross amount must be a non-negative number")
    if not isinstance(box4, (int, float)) or isinstance(box4, bool) or box4 < 0:
        raise F1099KRecordingRefused("box4 withholding amount must be a non-negative number")

    try:
        stmt_sameness_key = statement_key(payer_id=payer_id, tax_year=tax_year, payer_ref=statement_ref)
    except StatementIdentityError as exc:
        raise F1099KRecordingRefused(str(exc)) from exc

    stmt_entity = statement_entity_id(stmt_sameness_key)
    statement_keys = {"payer": payer_id, "statement": stmt_entity, "tax-year": tax_year}
    _validate_statement_keys(statement_keys)

    suffix = _token(submission_id)
    staged = list(copy.deepcopy(before.acts))
    _ensure_bundles(staged, registry, actor, at, suffix)
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)

    current_stmts = _find_current_statement_findings(state)
    recorded_keys = frozenset(
        StatementKey(
            keys["payer"],
            keys["tax-year"],
            keys["statement"].split(f"stmt.{keys['payer']}.{keys['tax-year']}.")[-1],
        )
        for _, _, keys in current_stmts
    )
    try:
        classification = classify_assertion(stmt_sameness_key, recorded_keys, corrected=corrected)
    except StatementIdentityError as exc:
        raise F1099KRecordingRefused(str(exc)) from exc

    if classification == "duplicate":
        raise F1099KRecordingRefused(
            f"statement {statement_ref!r} from {payer_id!r} has already been recorded; use corrected=True for a correction"
        )

    all_evidence = [evidence_id]
    if answer_evidence_ids:
        all_evidence.extend(answer_evidence_ids.values())
    _check_evidence_ids(all_evidence, submission_id, staged)

    scope = dict(family_scope or DEFAULT_FAMILY_SCOPE)
    family_ref = {"id": FAMILY_ID, "version": family_version}
    finding_ids: list[str] = []

    if classification == "new-original":
        if payer_id not in state.fact_state.entities:
            payer_act = _act(
                len(staged),
                "entity-introduced",
                {"entity": {"schema": "entity.v1", "id": payer_id, "kind": PAYER_ENTITY_KIND, "label": payer_label}},
                actor, at, f"{suffix}.payer",
            )
            state = apply_act(state, payer_act, registry)
            staged.append(payer_act)

        if stmt_entity not in state.fact_state.entities:
            statement_act = _act(
                len(staged),
                "entity-introduced",
                {"entity": {"schema": "entity.v1", "id": stmt_entity, "kind": STATEMENT_ENTITY_KIND, "label": statement_label}},
                actor, at, f"{suffix}.stmt",
            )
            state = apply_act(state, statement_act, registry)
            staged.append(statement_act)

        scope_tuple = tuple(sorted(scope.items()))
        active_chain: tuple[str, str] | None = None
        for (c_fid, c_ver, c_scope), h_id in state.horizon_state.current_by_chain.items():
            if c_fid == FAMILY_ID and c_scope == scope_tuple:
                active_chain = (c_ver, h_id)
                break

        if active_chain is None:
            h_count = 0
            genesis_h = f"demo.f1099k.h{h_count}"
            while genesis_h in state.horizon_state.horizons:
                h_count += 1
                genesis_h = f"demo.f1099k.h{h_count}"
            genesis_act = _act(
                len(staged),
                "horizon-genesis",
                {"family": family_ref, "scope": scope, "horizon_id": genesis_h},
                actor, at, f"{suffix}.genesis",
            )
            state = apply_act(state, genesis_act, registry)
            staged.append(genesis_act)
            pred_h = genesis_h
        else:
            cur_ver, cur_h = active_chain
            if cur_ver != family_version:
                if _version_number(cur_ver) > _version_number(family_version):
                    raise F1099KRecordingRefused(
                        f"cannot handover to older family version: current chain is {cur_ver}, writer requested {family_version}"
                    )
                h_count = len(state.horizon_state.horizons)
                handover_succ_h = f"demo.f1099k.h{h_count}"
                while handover_succ_h in state.horizon_state.horizons:
                    h_count += 1
                    handover_succ_h = f"demo.f1099k.h{h_count}"
                handover_act = _act(
                    len(staged),
                    "family-handover",
                    {
                        "predecessor": {
                            "family": {"id": FAMILY_ID, "version": cur_ver},
                            "scope": scope,
                            "horizon_id": cur_h,
                        },
                        "successor": {
                            "family": family_ref,
                            "scope": scope,
                            "horizon_id": handover_succ_h,
                        },
                    },
                    actor, at, f"{suffix}.handover",
                )
                state = apply_act(state, handover_act, registry)
                staged.append(handover_act)
                pred_h = handover_succ_h
            else:
                pred_h = cur_h

        h_count = len(state.horizon_state.horizons)
        succ_h = f"demo.f1099k.h{h_count}"
        while succ_h in state.horizon_state.horizons:
            h_count += 1
            succ_h = f"demo.f1099k.h{h_count}"

        stmt_evidence = {
            "schema": "evidence.v1",
            "id": evidence_id,
            "kind": STATEMENT_EVIDENCE_KIND,
            "label": f"Form 1099-K statement from {payer_label}",
            "content": {
                "submission_id": submission_id,
                "statement": statement_keys,
                "box1a": box1a,
                "box4": box4,
            },
        }
        stmt_ev_act = _act(len(staged), "evidence-submitted", {"evidence": stmt_evidence}, actor, at, f"{suffix}.doc_ev")
        state = apply_act(state, stmt_ev_act, registry)
        staged.append(stmt_ev_act)

        contrib_id = f"f1099k.statement.contrib.{suffix}"
        contrib = {
            "schema": "contribution.v1",
            "id": contrib_id,
            "evidence_id": evidence_id,
            "content": {
                "mode": "document-report-entry",
                "source": "f1099k-statement",
                "statement": statement_keys,
            },
        }
        contrib_act = _act(len(staged), "contribution", {"contribution": contrib}, actor, at, f"{suffix}.doc_cb")

        finding_b1a_id = f"f1099k.b1a.finding.{suffix}"
        fact_b1a_id = fact_id_for(STATEMENT_BOX1A, tuple(sorted(statement_keys.items())))
        finding_b1a = {
            "schema": "finding.v2",
            "id": finding_b1a_id,
            "fact_id": fact_b1a_id,
            "value": float(box1a),
            "basis": "documentary",
            "evidence_ids": [evidence_id],
            "contribution_id": contrib_id,
        }
        member_transition_act = _act(
            len(staged) + 1,
            "member-transition",
            {
                "family": family_ref,
                "scope": scope,
                "member": {"action": "assert", "finding": finding_b1a},
                "successor": {"id": succ_h, "predecessor": pred_h},
            },
            actor, at, f"{suffix}.mt",
        )
        finding_ids.append(finding_b1a_id)

        finding_b4_id = f"f1099k.b4.finding.{suffix}"
        fact_b4_id = fact_id_for(STATEMENT_BOX4, tuple(sorted(statement_keys.items())))
        finding_b4 = {
            "schema": "finding.v2",
            "id": finding_b4_id,
            "fact_id": fact_b4_id,
            "value": float(box4),
            "basis": "documentary",
            "evidence_ids": [evidence_id],
            "contribution_id": contrib_id,
        }
        assertion_b4_act = _act(len(staged) + 2, "assertion", {"finding": finding_b4}, actor, at, f"{suffix}.b4")
        finding_ids.append(finding_b4_id)

        successor_acts: list[dict[str, Any]] = [member_transition_act, assertion_b4_act]

        if close_family:
            closure_finding_id = f"f1099k.closure.finding.{suffix}"
            closure_fact_id = f"{CLOSURE_TYPE}|family-horizon={succ_h},tax-year={tax_year}"
            finding_closure = {
                "schema": "finding.v2",
                "id": closure_finding_id,
                "fact_id": closure_fact_id,
                "value": True,
                "basis": "attested",
                "evidence_ids": [evidence_id],
                "contribution_id": contrib_id,
            }
            closure_act = _act(len(staged) + 3, "assertion", {"finding": finding_closure}, actor, at, f"{suffix}.closure")
            successor_acts.append(closure_act)
            finding_ids.append(closure_finding_id)

        admission = apply_contribution_batch(
            state,
            contribution_act=contrib_act,
            successor_acts=successor_acts,
            registry=registry,
            record_id=f"f1099k.statement.record.{suffix}",
            workspace_revision=len(staged),
        )
        if admission.terminal_record["phase"] != "completed":
            raise F1099KRecordingRefused(f"statement contribution admission refused: {admission.terminal_record}")
        staged.append(contrib_act)
        staged.extend(successor_acts)
        state = admission.state
    else:
        # Correction of existing statement
        stmt_evidence = {
            "schema": "evidence.v1",
            "id": evidence_id,
            "kind": STATEMENT_EVIDENCE_KIND,
            "label": f"Corrected Form 1099-K statement from {payer_label}",
            "content": {
                "submission_id": submission_id,
                "statement": statement_keys,
                "box1a": box1a,
                "box4": box4,
                "correction": True,
            },
        }
        stmt_ev_act = _act(len(staged), "evidence-submitted", {"evidence": stmt_evidence}, actor, at, f"{suffix}.corr_ev")
        state = apply_act(state, stmt_ev_act, registry)
        staged.append(stmt_ev_act)

        contrib_id = f"f1099k.statement.contrib.{suffix}"
        contrib = {
            "schema": "contribution.v1",
            "id": contrib_id,
            "evidence_id": evidence_id,
            "content": {
                "mode": "document-report-entry",
                "source": "f1099k-statement-correction",
                "statement": statement_keys,
            },
        }
        contrib_act = _act(len(staged), "contribution", {"contribution": contrib}, actor, at, f"{suffix}.corr_cb")

        finding_b1a_id = f"f1099k.b1a.finding.{suffix}"
        fact_b1a_id = fact_id_for(STATEMENT_BOX1A, tuple(sorted(statement_keys.items())))
        finding_b1a = {
            "schema": "finding.v2",
            "id": finding_b1a_id,
            "fact_id": fact_b1a_id,
            "value": float(box1a),
            "basis": "documentary",
            "evidence_ids": [evidence_id],
            "contribution_id": contrib_id,
        }
        assertion_b1a_act = _act(len(staged) + 1, "assertion", {"finding": finding_b1a}, actor, at, f"{suffix}.corr_b1a")
        finding_ids.append(finding_b1a_id)

        finding_b4_id = f"f1099k.b4.finding.{suffix}"
        fact_b4_id = fact_id_for(STATEMENT_BOX4, tuple(sorted(statement_keys.items())))
        finding_b4 = {
            "schema": "finding.v2",
            "id": finding_b4_id,
            "fact_id": fact_b4_id,
            "value": float(box4),
            "basis": "documentary",
            "evidence_ids": [evidence_id],
            "contribution_id": contrib_id,
        }
        assertion_b4_act = _act(len(staged) + 2, "assertion", {"finding": finding_b4}, actor, at, f"{suffix}.corr_b4")
        finding_ids.append(finding_b4_id)

        corr_successor_acts = [assertion_b1a_act, assertion_b4_act]

        cur_h = current_horizon_id(state.horizon_state, family=family_ref, scope=scope)
        if close_family and cur_h is not None:
            closure_fact_id = f"{CLOSURE_TYPE}|family-horizon={cur_h},tax-year={tax_year}"
            current_ids = compute_currency(state).current_finding_ids
            existing_closure = _current_finding(state, closure_fact_id, current_ids)
            if existing_closure is None:
                closure_finding_id = f"f1099k.closure.finding.{suffix}"
                finding_closure = {
                    "schema": "finding.v2",
                    "id": closure_finding_id,
                    "fact_id": closure_fact_id,
                    "value": True,
                    "basis": "attested",
                    "evidence_ids": [evidence_id],
                    "contribution_id": contrib_id,
                }
                closure_act = _act(len(staged) + 3, "assertion", {"finding": finding_closure}, actor, at, f"{suffix}.closure")
                corr_successor_acts.append(closure_act)
                finding_ids.append(closure_finding_id)

        admission = apply_contribution_batch(
            state,
            contribution_act=contrib_act,
            successor_acts=corr_successor_acts,
            registry=registry,
            record_id=f"f1099k.statement.record.{suffix}",
            workspace_revision=len(staged),
        )
        if admission.terminal_record["phase"] != "completed":
            raise F1099KRecordingRefused(f"statement correction admission refused: {admission.terminal_record}")
        staged.append(contrib_act)
        staged.extend(corr_successor_acts)
        state = admission.state

    if answers:
        norm_answers = {_normalize_question(k): v for k, v in answers.items()}
        for q, a in norm_answers.items():
            _validate_answer_value(q, a)
        ans_ev_ids = {
            _normalize_question(k): v for k, v in (answer_evidence_ids or {}).items()
        }
        if set(ans_ev_ids) != set(norm_answers):
            raise F1099KRecordingRefused("each submitted answer requires its own evidence identity")
        for q, a in norm_answers.items():
            ans_fid = f"f1099k.answer.finding.{suffix}.{_token(q)}"
            ans_cid = f"f1099k.answer.contrib.{suffix}.{_token(q)}"
            ev_id = ans_ev_ids[q]
            _, state = _stage_answer(
                staged, registry, keys=statement_keys, question=q, answer=a,
                actor=actor, at=at, evidence_id=ev_id, contribution_id=ans_cid,
                finding_id=ans_fid, target_finding_id=None, claim_id=submission_id,
                suffix=suffix, base_state=state,
            )
            finding_ids.append(ans_fid)

    committed = _commit(
        log, registry, before, staged, actor=actor, at=at,
        suffix=suffix, finding_ids=finding_ids, expected_revision=expected_revision,
    )
    committed["statement_keys"] = statement_keys
    return committed


def record_f1099k_no_statements_durably(
    log: ActLog,
    registry: Any,
    *,
    submission_id: str,
    evidence_id: str,
    actor: str,
    at: str,
    expected_revision: int,
    tax_year: str = "2025",
    family_scope: dict[str, str] | None = None,
    family_version: str = FAMILY_VERSION,
) -> dict[str, Any]:
    """Record 'I received no Form 1099-K for 2025' as family closure at the current horizon."""
    _require_provenance(submission_id, actor, at)
    before = _read_for_save(log, expected_revision)
    suffix = _token(submission_id)
    staged = list(copy.deepcopy(before.acts))
    _ensure_bundles(staged, registry, actor, at, suffix)
    _check_evidence_ids([evidence_id], submission_id, staged)
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)

    current_stmts = _find_current_statement_findings(state)
    if current_stmts:
        raise F1099KRecordingRefused(
            "cannot record 'no Form 1099-K' closure when Form 1099-K statements are currently recorded"
        )

    scope = dict(family_scope or DEFAULT_FAMILY_SCOPE)
    family_ref = {"id": FAMILY_ID, "version": family_version}
    scope_tuple = tuple(sorted(scope.items()))
    active_chain: tuple[str, str] | None = None
    for (c_fid, c_ver, c_scope), h_id in state.horizon_state.current_by_chain.items():
        if c_fid == FAMILY_ID and c_scope == scope_tuple:
            active_chain = (c_ver, h_id)
            break

    if active_chain is None:
        h_count = 0
        genesis_h = f"demo.f1099k.h{h_count}"
        while genesis_h in state.horizon_state.horizons:
            h_count += 1
            genesis_h = f"demo.f1099k.h{h_count}"
        genesis_act = _act(
            len(staged),
            "horizon-genesis",
            {"family": family_ref, "scope": scope, "horizon_id": genesis_h},
            actor, at, f"{suffix}.genesis",
        )
        state = apply_act(state, genesis_act, registry)
        staged.append(genesis_act)
        target_h = genesis_h
    else:
        cur_ver, cur_h = active_chain
        if cur_ver != family_version:
            if _version_number(cur_ver) > _version_number(family_version):
                raise F1099KRecordingRefused(
                    f"cannot handover to older family version: current chain is {cur_ver}, writer requested {family_version}"
                )
            h_count = len(state.horizon_state.horizons)
            handover_succ_h = f"demo.f1099k.h{h_count}"
            while handover_succ_h in state.horizon_state.horizons:
                h_count += 1
                handover_succ_h = f"demo.f1099k.h{h_count}"
            handover_act = _act(
                len(staged),
                "family-handover",
                {
                    "predecessor": {
                        "family": {"id": FAMILY_ID, "version": cur_ver},
                        "scope": scope,
                        "horizon_id": cur_h,
                    },
                    "successor": {
                        "family": family_ref,
                        "scope": scope,
                        "horizon_id": handover_succ_h,
                    },
                },
                actor, at, f"{suffix}.handover",
            )
            state = apply_act(state, handover_act, registry)
            staged.append(handover_act)
            target_h = handover_succ_h
        else:
            target_h = cur_h

    closure_fact_id = f"{CLOSURE_TYPE}|family-horizon={target_h},tax-year={tax_year}"
    current_fids = compute_currency(state).current_finding_ids
    existing_closure = [
        fid for fid, f in state.findings.items()
        if f["fact_id"] == closure_fact_id and fid in current_fids
    ]
    if existing_closure:
        raise F1099KRecordingRefused(
            f"family closure already recorded for horizon {target_h}"
        )

    evidence = {
        "schema": "evidence.v1",
        "id": evidence_id,
        "kind": CLOSURE_EVIDENCE_KIND,
        "label": "No Form 1099-K received for 2025",
        "content": {
            "submission_id": submission_id,
            "closure_horizon": target_h,
            "tax_year": tax_year,
            "statement_count": 0,
        },
    }
    evidence_act = _act(len(staged), "evidence-submitted", {"evidence": evidence}, actor, at, f"{suffix}.no_stmt_ev")
    state = apply_act(state, evidence_act, registry)
    staged.append(evidence_act)

    contrib_id = f"f1099k.closure.contrib.{suffix}"
    contrib = {
        "schema": "contribution.v1",
        "id": contrib_id,
        "evidence_id": evidence_id,
        "content": {
            "mode": "manual-entry",
            "source": "f1099k-no-statements-closure",
        },
    }
    contrib_act = _act(len(staged), "contribution", {"contribution": contrib}, actor, at, f"{suffix}.no_stmt_cb")

    closure_finding_id = f"f1099k.closure.finding.{suffix}"
    closure_fact_id = f"{CLOSURE_TYPE}|family-horizon={target_h},tax-year={tax_year}"
    finding = {
        "schema": "finding.v2",
        "id": closure_finding_id,
        "fact_id": closure_fact_id,
        "value": True,
        "basis": "attested",
        "evidence_ids": [evidence_id],
        "contribution_id": contrib_id,
    }
    assertion_act = _act(len(staged) + 1, "assertion", {"finding": finding}, actor, at, f"{suffix}.no_stmt_as")
    admission = apply_contribution_batch(
        state,
        contribution_act=contrib_act,
        successor_acts=[assertion_act],
        registry=registry,
        record_id=f"f1099k.no_statement.record.{suffix}",
        workspace_revision=len(staged),
    )
    if admission.terminal_record["phase"] != "completed":
        raise F1099KRecordingRefused(f"closure contribution was not admitted: {admission.terminal_record}")
    staged.extend((contrib_act, assertion_act))

    committed = _commit(
        log, registry, before, staged, actor=actor, at=at,
        suffix=suffix, finding_ids=[closure_finding_id], expected_revision=expected_revision,
    )
    committed["horizon"] = target_h
    return committed


def record_f1099k_statement_answers_durably(
    log: ActLog,
    registry: Any,
    *,
    statement_keys: dict[str, str],
    answers: dict[str, Any],
    submission_id: str,
    evidence_ids: dict[str, str],
    actor: str,
    at: str,
    expected_revision: int,
    allow_partial: bool = False,
) -> dict[str, Any]:
    """Record initial circumstance answers for one Form 1099-K statement atomically."""
    _require_provenance(submission_id, actor, at)
    _validate_statement_keys(statement_keys)
    before = _read_for_save(log, expected_revision)
    suffix = _token(submission_id)
    staged = list(copy.deepcopy(before.acts))
    _ensure_bundles(staged, registry, actor, at, suffix)

    norm_answers = {_normalize_question(k): v for k, v in answers.items()}
    norm_evidence = {_normalize_question(k): v for k, v in evidence_ids.items()}

    if not allow_partial:
        missing = ALL_CIRCUMSTANCE_QUESTIONS - set(norm_answers)
        if missing:
            raise F1099KRecordingRefused(
                f"full initial submission must contain all 15 circumstance answers; missing: {sorted(missing)}"
            )

    extra = set(norm_answers) - ALL_CIRCUMSTANCE_QUESTIONS
    if extra:
        raise F1099KRecordingRefused(f"unexpected questions in submission: {sorted(extra)}")

    if set(norm_answers) != set(norm_evidence):
        raise F1099KRecordingRefused("each submitted answer must have a matching evidence identity")
    _check_evidence_ids(norm_evidence, submission_id, staged)

    for q, a in norm_answers.items():
        _validate_answer_value(q, a)

    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    _require_statement_exists(state, statement_keys)
    current_ids = compute_currency(state).current_finding_ids

    # Verify no current answer already exists for any question being submitted
    for q in norm_answers:
        fid = fact_id_for(f"tax.us.2025.f1099k.{q}", tuple(sorted(statement_keys.items())))
        if _current_finding(state, fid, current_ids) is not None:
            raise F1099KRecordingRefused(f"answer already exists for {q}; use correction")

    finding_ids: list[str] = []
    for q, a in norm_answers.items():
        finding_id = f"f1099k.answer.finding.{suffix}.{_token(q)}"
        contribution_id = f"f1099k.answer.contrib.{suffix}.{_token(q)}"
        ev_id = norm_evidence[q]
        _, state = _stage_answer(
            staged, registry, keys=statement_keys, question=q, answer=a,
            actor=actor, at=at, evidence_id=ev_id, contribution_id=contribution_id,
            finding_id=finding_id, target_finding_id=None, claim_id=submission_id,
            suffix=suffix, base_state=state,
        )
        finding_ids.append(finding_id)

    return _commit(
        log, registry, before, staged, actor=actor, at=at,
        suffix=suffix, finding_ids=finding_ids, expected_revision=expected_revision,
    )


def answer_f1099k_statement_answer_durably(
    log: ActLog,
    registry: Any,
    *,
    statement_keys: dict[str, str],
    question: str,
    answer: Any,
    submission_id: str,
    evidence_id: str,
    actor: str,
    at: str,
    expected_revision: int,
) -> dict[str, Any]:
    """Record one absent circumstance answer for a statement."""
    norm_q = _normalize_question(question)
    return record_f1099k_statement_answers_durably(
        log,
        registry,
        statement_keys=statement_keys,
        answers={norm_q: answer},
        submission_id=submission_id,
        evidence_ids={norm_q: evidence_id},
        actor=actor,
        at=at,
        expected_revision=expected_revision,
        allow_partial=True,
    )


def correct_f1099k_statement_answer_durably(
    log: ActLog,
    registry: Any,
    *,
    statement_keys: dict[str, str],
    question: str,
    answer: Any,
    predecessor_finding_id: str,
    submission_id: str,
    evidence_id: str,
    actor: str,
    at: str,
    expected_revision: int,
) -> dict[str, Any]:
    """Replace one current answer with new evidence on the same fact identity."""
    _require_provenance(submission_id, actor, at)
    _validate_statement_keys(statement_keys)
    norm_q = _normalize_question(question)
    _validate_answer_value(norm_q, answer)
    before = _read_for_save(log, expected_revision)
    suffix = _token(submission_id)
    staged = list(copy.deepcopy(before.acts))
    _ensure_bundles(staged, registry, actor, at, suffix)
    _check_evidence_ids([evidence_id], submission_id, staged)

    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    _require_statement_exists(state, statement_keys)
    current_ids = compute_currency(state).current_finding_ids
    fact_id = fact_id_for(f"tax.us.2025.f1099k.{norm_q}", tuple(sorted(statement_keys.items())))
    current = _current_finding(state, fact_id, current_ids)
    if current is None or current[0] != predecessor_finding_id:
        raise F1099KRecordingRefused("correction target is not the exact current answer shown")

    finding_id = f"f1099k.answer.finding.{suffix}.{_token(norm_q)}"
    contribution_id = f"f1099k.answer.contrib.{suffix}.{_token(norm_q)}"
    _, state = _stage_answer(
        staged, registry, keys=statement_keys, question=norm_q, answer=answer,
        actor=actor, at=at, evidence_id=evidence_id, contribution_id=contribution_id,
        finding_id=finding_id, target_finding_id=predecessor_finding_id,
        claim_id=submission_id, suffix=suffix, base_state=state,
    )
    return _commit(
        log, registry, before, staged, actor=actor, at=at,
        suffix=suffix, finding_ids=[finding_id], expected_revision=expected_revision,
    )


def withdraw_f1099k_statement_answer_durably(
    log: ActLog,
    registry: Any,
    *,
    current_findings: Sequence[str],
    submission_id: str,
    actor: str,
    at: str,
    expected_revision: int,
) -> dict[str, Any]:
    """End current answer support without a replacement or an opposite answer."""
    _require_provenance(submission_id, actor, at)
    before = _read_for_save(log, expected_revision)
    if not current_findings or len(set(current_findings)) != len(current_findings):
        raise F1099KRecordingRefused("withdrawal must name distinct non-empty current findings")

    staged = list(copy.deepcopy(before.acts))
    state = project(tuple(copy.deepcopy(row) for row in staged), registry)
    current_ids = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state, include_displaced=True)

    allowed_fact_types = {f"tax.us.2025.f1099k.{q}" for q in ALL_CIRCUMSTANCE_QUESTIONS}
    for finding_id in current_findings:
        if finding_id not in current_ids:
            raise F1099KRecordingRefused(f"withdrawal target is no longer current: {finding_id}")
        finding = state.findings[finding_id]
        fact = lattice.get(finding.get("fact_id", ""))
        if fact is None or fact.fact_type_id not in allowed_fact_types:
            raise F1099KRecordingRefused(f"withdrawal target is not a Form 1099-K circumstance answer: {finding_id}")

    _check_evidence_ids([], submission_id, staged)
    suffix = _token(submission_id)
    evidence = {
        "schema": "evidence.v1",
        "id": f"f1099k.withdrawal.evidence.{suffix}",
        "kind": ANSWER_EVIDENCE_KIND,
        "label": "Recorded Form 1099-K answer withdrawal",
        "content": {
            "request_id": submission_id,
            "target_finding_ids": list(current_findings),
        },
    }
    evidence_act = _act(len(staged), "evidence-submitted", {"evidence": evidence}, actor, at, suffix)
    state = apply_act(state, evidence_act, registry)
    staged.append(evidence_act)

    for finding_id in current_findings:
        act = _act(len(staged), "finding-retracted", {"finding_id": finding_id}, actor, at, suffix)
        state = apply_act(state, act, registry)
        staged.append(act)

    return _commit(
        log, registry, before, staged, actor=actor, at=at,
        suffix=suffix, finding_ids=[], expected_revision=expected_revision,
    )
