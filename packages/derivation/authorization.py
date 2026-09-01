"""Standing workspace authorization: out-of-kernel act-log fold (ADR-0069).

Compose-over (ADR-0010): this fold reads the shared act log and ignores every
kind it does not own. In particular ``member-transition`` and ``assertion``
never touch standing authorization — that is the property that makes it
standing. Kernel ``entity-superseded`` is a subscribed displacement root
(Decision 4); grant and end kinds are this family's own.

Taxpayer/year mismatch is classified unconditionally on ``(subject_id,
tax_year)`` with no boundary-digest co-requirement (Decision 3). A grant
whose subject entity has been superseded is inert; the successor does not
inherit it.

A ``calculation-scope-declaration`` act (Decision 5/9) names the rule
id(s) a workspace's calculation actually composes for one ``(subject_id,
tax_year)``. This is an out-of-kernel act-log entry, not a kernel-projected
fact: it is never a ``Finding``, never addressable from ``env.sources`` or
any rule's ``when``/``value`` expression, and no tax computation reads it.
Production always resolves and executes every adopted-package entrypoint
(there is no run-request field able to select one calculation, ADR-0032
Decision 3), so the declaration cannot narrow the re-authorization boundary
below what the run actually executes and publishes -- it can only widen it
(``resolve_for_composition`` unions the declared rule ids into the
actually-executed root). Aligning the boundary with the actually-published
result is required so that a reader of the resolved authorization can trust
it describes the same scope as the run's output. The scope citizen is
``workspace-calculation-scope.v1`` (``act-calculation-scope-declaration.v1``
wraps it).

No edits to ``packages/kernel/findings.py`` ``KERNEL_ACT_KINDS`` / ``_APPLIERS``.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Iterable, Mapping

from packages.derivation.authorization_closure import package_boundary_digest

GRANT_ACT_KIND = "calculation-authorization"
END_ACT_KIND = "calculation-authorization-end"
ENTITY_SUPERSEDED_KIND = "entity-superseded"
# ADR-0069 Decision 5/9: names the specific rule(s) a workspace's
# calculation actually composes, as an out-of-kernel act-log entry -- not a
# kernel-projected fact (run-request.v1 is deliberately closed, ADR-0032
# Decision 3, and cannot carry this). The nested-citizen schema is
# workspace-calculation-scope.v1.
SCOPE_ACT_KIND = "calculation-scope-declaration"

STATUS_ADMITTED = "admitted"
STATUS_ABSENT = "AUTHORIZATION_ABSENT"
STATUS_SUSPENDED = "AUTHORIZATION_SUSPENDED"
STATUS_WITHDRAWN = "AUTHORIZATION_WITHDRAWN"
STATUS_TAXPAYER_MISMATCH = "AUTHORIZATION_TAXPAYER_MISMATCH"
STATUS_YEAR_MISMATCH = "AUTHORIZATION_YEAR_MISMATCH"
STATUS_STALE = "AUTHORIZATION_STALE"
STATUS_UNIVERSE_SUPERSEDED = "AUTHORIZATION_UNIVERSE_SUPERSEDED"
STATUS_SUBJECT_SUPERSEDED = "AUTHORIZATION_SUBJECT_SUPERSEDED"


@dataclass(frozen=True)
class Grant:
    id: str
    subject_id: str
    tax_year: str
    universe_id: str
    supersedes: str | None = None


@dataclass(frozen=True)
class AuthorizationState:
    grants: dict[str, Grant] = field(default_factory=dict)
    current_by_key: dict[tuple[str, str], str] = field(default_factory=dict)
    ended: dict[str, str] = field(default_factory=dict)
    superseded_subjects: dict[str, str | None] = field(default_factory=dict)
    # ADR-0069 Decision 5 successor: latest declared calculation-scope rule
    # ids by (subject_id, tax_year). A later declaration at the same key
    # replaces the prior one -- this is descriptive state, not a grant with
    # a supersession chain or an end act.
    scope_by_key: dict[tuple[str, str], frozenset[str]] = field(default_factory=dict)


@dataclass(frozen=True)
class AuthorizationResolution:
    """Fail-closed admission result for one (subject, year, universe) read."""

    status: str
    grant_id: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    @property
    def admitted(self) -> bool:
        return self.status == STATUS_ADMITTED


def initial_state() -> AuthorizationState:
    return AuthorizationState()


def _apply_grant(state: AuthorizationState, payload: Mapping[str, Any]) -> AuthorizationState:
    citizen = payload["authorization"]
    grant = Grant(
        id=citizen["id"],
        subject_id=citizen["subject_id"],
        tax_year=str(citizen["tax_year"]),
        universe_id=citizen["universe_id"],
        supersedes=citizen.get("supersedes"),
    )
    grants = dict(state.grants)
    grants[grant.id] = grant
    current_by_key = dict(state.current_by_key)
    current_by_key[(grant.subject_id, grant.tax_year)] = grant.id
    return replace(state, grants=grants, current_by_key=current_by_key)


def _apply_end(state: AuthorizationState, payload: Mapping[str, Any]) -> AuthorizationState:
    ended = dict(state.ended)
    ended[payload["authorization_id"]] = payload["ending"]
    return replace(state, ended=ended)


def _apply_entity_superseded(
    state: AuthorizationState, payload: Mapping[str, Any]
) -> AuthorizationState:
    """Taxpayer-entity supersession as a displacement root (ADR-0069 Decision 4).

    Reads the real kernel ``entity-superseded`` kind off the shared log.
    The successor entity does not inherit the grant.
    """
    entity_id = payload["entity_id"]
    replacement = payload.get("replacement")
    successor_id: str | None = None
    if isinstance(replacement, dict):
        raw = replacement.get("id")
        if isinstance(raw, str):
            successor_id = raw
    superseded = dict(state.superseded_subjects)
    superseded[entity_id] = successor_id
    return replace(state, superseded_subjects=superseded)


def _apply_scope_declaration(
    state: AuthorizationState, payload: Mapping[str, Any]
) -> AuthorizationState:
    """Latest calculation-scope declaration wins at (subject_id, tax_year).

    ADR-0069 Decision 5/9 successor: widens the entrypoint-set rooting of
    the re-authorization boundary with the rule id(s) the workspace's
    calculation actually declares as composed, when a declaration exists --
    it never replaces or narrows that root (resolve_for_composition unions
    it in). Reads only the generic subject_id/tax_year/rule_ids fields
    shared by both the current (v2) and superseded (v1) nested-citizen
    schemas.
    """
    citizen = payload["scope"]
    key = (citizen["subject_id"], str(citizen["tax_year"]))
    rule_ids = frozenset(citizen["rule_ids"])
    scope_by_key = dict(state.scope_by_key)
    scope_by_key[key] = rule_ids
    return replace(state, scope_by_key=scope_by_key)


_APPLIERS = {
    GRANT_ACT_KIND: _apply_grant,
    END_ACT_KIND: _apply_end,
    ENTITY_SUPERSEDED_KIND: _apply_entity_superseded,
    SCOPE_ACT_KIND: _apply_scope_declaration,
}


def project(acts: Iterable[Mapping[str, Any]]) -> AuthorizationState:
    """ADR-0010 compose-over: ignore every act kind this fold does not own."""
    state = initial_state()
    for act in acts:
        applier = _APPLIERS.get(act["kind"])
        if applier is None:
            continue
        state = applier(state, act["payload"])
    return state


def _live_current(
    state: AuthorizationState,
) -> list[tuple[str, str, str]]:
    """Current (subject, year, grant_id) triples, excluding ended grants.

    Sorted by grant id so mismatch classification is deterministic.
    """
    live: list[tuple[str, str, str]] = []
    for (subject_id, tax_year), grant_id in state.current_by_key.items():
        if grant_id in state.ended:
            continue
        live.append((subject_id, tax_year, grant_id))
    live.sort(key=lambda item: item[2])
    return live


def resolve(
    state: AuthorizationState,
    subject_id: str,
    tax_year: str,
    universe_id: str,
    named_authorization_id: str | None = None,
) -> AuthorizationResolution:
    """Fail-closed admission.

    Precedence, once a named-id stale check has passed:

    1. exact-key ended grant → suspended / withdrawn (distinct from absence)
    2. exact-key subject entity superseded → AUTHORIZATION_SUBJECT_SUPERSEDED
    3. exact-key universe digest drift → AUTHORIZATION_UNIVERSE_SUPERSEDED
    4. exact-key match → admitted
    5. no exact key: year mismatch (same subject, any live year) before
       taxpayer mismatch (same year, any live other subject) — never gated
       on ``universe_id`` matching (Decision 3)
    6. else absence
    """
    if named_authorization_id is not None:
        current_id = state.current_by_key.get((subject_id, tax_year))
        if current_id != named_authorization_id or named_authorization_id not in state.grants:
            return AuthorizationResolution(STATUS_STALE, named_authorization_id)

    grant_id = state.current_by_key.get((subject_id, tax_year))
    if grant_id is not None:
        grant = state.grants[grant_id]
        if grant_id in state.ended:
            ending = state.ended[grant_id]
            status = STATUS_SUSPENDED if ending == "suspend" else STATUS_WITHDRAWN
            return AuthorizationResolution(status, grant_id)
        if grant.subject_id in state.superseded_subjects:
            return AuthorizationResolution(
                STATUS_SUBJECT_SUPERSEDED,
                grant_id,
                {
                    "superseded_subject": grant.subject_id,
                    "successor": state.superseded_subjects[grant.subject_id],
                },
            )
        if grant.universe_id != universe_id:
            return AuthorizationResolution(
                STATUS_UNIVERSE_SUPERSEDED,
                grant_id,
                {"expected": grant.universe_id, "actual": universe_id},
            )
        return AuthorizationResolution(STATUS_ADMITTED, grant_id)

    live = _live_current(state)
    for other_subject, other_year, other_id in live:
        if other_subject == subject_id and other_year != tax_year:
            return AuthorizationResolution(
                STATUS_YEAR_MISMATCH,
                other_id,
                {"expected_year": other_year, "actual_year": tax_year},
            )
    for other_subject, other_year, other_id in live:
        if other_year == tax_year and other_subject != subject_id:
            return AuthorizationResolution(
                STATUS_TAXPAYER_MISMATCH,
                other_id,
                {"expected_subject": other_subject, "actual_subject": subject_id},
            )
    return AuthorizationResolution(STATUS_ABSENT)


def resolve_for_composition(
    acts: Iterable[Mapping[str, Any]],
    *,
    subject_id: str,
    tax_year: str,
    root_rule_ids: set[str],
    corpus: Mapping[str, dict[str, Any]],
    named_authorization_id: str | None = None,
    package: Mapping[str, Any] | None = None,
) -> AuthorizationResolution:
    """Fold the log and admit against the composed rule(s)' current closure.

    ``root_rule_ids`` is the set of entrypoints this run actually resolved
    and is about to execute and publish -- it is never optional and never
    replaced. A ``calculation-scope-declaration`` act, when one exists for
    this exact ``(subject_id, tax_year)``, can only *widen* the boundary
    (union in its named rule ids); it can never narrow it below what the
    run actually executes.

    Production resolves and publishes every adopted-package entrypoint
    regardless of any declared scope (there is no run-request field able to
    select one calculation, ADR-0032 Decision 3), so a declaration that
    *omitted* an entrypoint the run still executed must never let the
    reauthorization boundary under-cover the actual presented result --
    a run must never be able to publish a newly added calculation outside
    the declared scope while reporting the authorization as current. Until
    a caller exists that actually narrows *execution* to a declared scope
    (not merely its own reachability), the declared scope cannot narrow the
    *authorization* boundary either: every entrypoint the run actually
    executes and publishes is always in the boundary.
    """
    state = project(acts)
    declared = state.scope_by_key.get((subject_id, str(tax_year)))
    effective_root_rule_ids = set(root_rule_ids) | (set(declared) if declared is not None else set())
    universe_id = package_boundary_digest(effective_root_rule_ids, corpus, package=package)
    return resolve(
        state,
        subject_id,
        str(tax_year),
        universe_id,
        named_authorization_id,
    )


def bind_authorization(env: Any, resolution: AuthorizationResolution) -> Any:
    """Return ``env`` with ``authorization`` set. Does not change tax reads."""
    return replace(env, authorization=resolution)


def authorization_provenance(resolution: AuthorizationResolution) -> dict[str, Any]:
    """Run-explanation payload for the resolved disposition.

    Not a derived-finding pin: published pin-role enums
    (``derived-finding.v2``, ``derivation-record.v7``) have no authorization
    token, and this seam does not publish a schema successor to add one.
    Follow-on: a ``derivation-record.v8`` field (and optionally a
    ``derived-finding.v3`` pin role) may persist this object. Until then,
    ``Environment.authorization`` plus this helper is how the disposition
    reaches run explanation.

    Integration-checkpoint follow-on: exhaustive-total admission for the
    interest path consults this resolution so a suspended grant blocks
    currentness without changing tax semantics. This module does not wire
    that consumer.
    """
    return {
        "kind": "authorization",
        "role": "authorization",
        "status": resolution.status,
        "grant_id": resolution.grant_id,
        "detail": dict(resolution.detail),
        "admitted": resolution.admitted,
    }
