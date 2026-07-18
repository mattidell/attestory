"""Contribution machinery: manual-entry batches become provenance-bearing facts.

ADR-0032 (D2). A contribution is a first-class product event distinct from a
run. Manual entry produces finding.v2 facts through ordinary successor carrier
acts (assertion / member-transition); each finding may pin the contribution by
id. The contribution pin is provenance only — never a derivation edge.

This module coordinates a contribution batch over synthetic fixtures and
writes the Article-14 contribution-record process account (started → terminal).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from packages.kernel.findings import FindingModelError, FindingState, apply_act
from packages.kernel.schema_registry import SchemaRegistry, SchemaValidationError

CONTRIBUTION_RECORD_SCHEMA = "contribution-record.v1"
_SUCCESSOR_KINDS = frozenset({"assertion", "member-transition"})
_TERMINAL_PHASES = frozenset({"completed", "interrupted", "failed"})


class ContributionError(Exception):
    """A contribution batch is inadmissible or mis-structured."""


@dataclass(frozen=True)
class ContributionBatchResult:
    """Outcome of applying one contribution batch to projected state."""

    state: FindingState
    started_record: dict[str, Any]
    terminal_record: dict[str, Any]
    asserted: tuple[dict[str, str], ...] = field(default_factory=tuple)


def started_contribution_record(
    *,
    record_id: str,
    contribution_id: str,
    workspace_revision: int,
) -> dict[str, Any]:
    """Article-14 started account for a contribution process."""
    return {
        "schema": CONTRIBUTION_RECORD_SCHEMA,
        "record_id": record_id,
        "contribution_id": contribution_id,
        "phase": "started",
        "workspace_revision": workspace_revision,
    }


def terminal_contribution_record(
    *,
    record_id: str,
    contribution_id: str,
    workspace_revision: int,
    phase: str,
    stop_reason: str,
    facts_asserted: Sequence[dict[str, str]],
) -> dict[str, Any]:
    """Article-14 terminal account (completed / interrupted / failed)."""
    if phase not in _TERMINAL_PHASES:
        raise ContributionError(f"not a terminal phase: {phase}")
    return {
        "schema": CONTRIBUTION_RECORD_SCHEMA,
        "record_id": record_id,
        "contribution_id": contribution_id,
        "phase": phase,
        "workspace_revision": workspace_revision,
        "stop_reason": stop_reason,
        "facts_asserted": list(facts_asserted),
    }


def validate_contribution_record(
    record: dict[str, Any], registry: SchemaRegistry
) -> None:
    """Admit a contribution-record.v1 against the published schema."""
    registry.validate(CONTRIBUTION_RECORD_SCHEMA, record)


def _finding_from_act(act: dict[str, Any]) -> dict[str, Any] | None:
    kind = act["kind"]
    payload = act["payload"]
    if kind == "assertion":
        finding = payload.get("finding")
        return finding if isinstance(finding, dict) else None
    if kind == "member-transition":
        member = payload.get("member")
        if isinstance(member, dict) and member.get("action") in ("assert", "reclassify"):
            finding = member.get("finding")
            return finding if isinstance(finding, dict) else None
    return None


def apply_contribution_batch(
    state: FindingState,
    *,
    contribution_act: dict[str, Any],
    successor_acts: Sequence[dict[str, Any]],
    registry: SchemaRegistry,
    record_id: str,
    workspace_revision: int | None = None,
) -> ContributionBatchResult:
    """Apply one manual-entry contribution batch through successor carriers.

    Order is fixed by reference integrity, not by wizard sequence:

    1. Write the started process account.
    2. Apply the contribution act (anchors evidence + contribution id).
    3. Apply each successor carrier act (assertion / member-transition)
       producing finding.v2 facts that carry contribution_id.
    4. Write the terminal process account listing asserted facts.

    On any admission failure the started record is closed as ``failed`` and
    the exception is re-raised with the failed terminal record available on
    the exception as ``.terminal_record`` when callers need it; the returned
    path always yields a completed batch only when every act admits.
    """
    if contribution_act.get("kind") != "contribution":
        raise ContributionError(
            f"contribution batch requires kind 'contribution', got "
            f"{contribution_act.get('kind')!r}"
        )
    contribution = contribution_act["payload"]["contribution"]
    contribution_id = contribution["id"]
    revision = (
        workspace_revision
        if workspace_revision is not None
        else int(contribution_act["committed_against"])
    )
    started = started_contribution_record(
        record_id=f"{record_id}.started",
        contribution_id=contribution_id,
        workspace_revision=revision,
    )
    validate_contribution_record(started, registry)

    for act in successor_acts:
        kind = act.get("kind")
        if kind not in _SUCCESSOR_KINDS:
            raise ContributionError(
                f"successor act kind {kind!r} is not a contribution carrier "
                f"(expected assertion or member-transition)"
            )

    tentative = state
    asserted: list[dict[str, str]] = []
    try:
        tentative = apply_act(tentative, contribution_act, registry)
        for act in successor_acts:
            tentative = apply_act(tentative, act, registry)
            finding = _finding_from_act(act)
            if finding is not None:
                if finding.get("contribution_id") != contribution_id:
                    raise ContributionError(
                        f"finding {finding.get('id')!r} contribution_id "
                        f"{finding.get('contribution_id')!r} does not match "
                        f"batch contribution {contribution_id!r}"
                    )
                if "pins" in finding:
                    raise ContributionError(
                        f"finding {finding['id']}: contribution pin must stay "
                        f"out of pins (provenance only, no derivation edge)"
                    )
                asserted.append(
                    {
                        "fact_id": finding["fact_id"],
                        "finding_id": finding["id"],
                        "act_id": act["act_id"],
                    }
                )
    except (FindingModelError, SchemaValidationError, ContributionError) as exc:
        failed = terminal_contribution_record(
            record_id=f"{record_id}.terminal",
            contribution_id=contribution_id,
            workspace_revision=revision,
            phase="failed",
            stop_reason="validation-failed",
            facts_asserted=(),
        )
        try:
            validate_contribution_record(failed, registry)
        except SchemaValidationError:
            pass
        err = ContributionError(f"contribution batch failed: {exc}")
        setattr(err, "started_record", started)
        setattr(err, "terminal_record", failed)
        raise err from exc

    terminal = terminal_contribution_record(
        record_id=f"{record_id}.terminal",
        contribution_id=contribution_id,
        workspace_revision=revision + 1 + len(successor_acts),
        phase="completed",
        stop_reason="completed",
        facts_asserted=asserted,
    )
    validate_contribution_record(terminal, registry)
    return ContributionBatchResult(
        state=tentative,
        started_record=started,
        terminal_record=terminal,
        asserted=tuple(asserted),
    )
