"""Rung-2 resolver mutations for SC-P1 affirmative-only enforcement.

PROTOTYPE ONLY (charter-repair1, checks 5-6). Self-contained: imports nothing
from ``packages/`` and never executes the production evaluator. It models the
*resolver boundary* that projects source-set closed membership from closure
findings plus an adopted mapping, for BOTH surviving authority shapes:

  Shape A  (it1, exhibit it1)  dedicated mapping citizen ``source-closure-mapping.v1``
  Shape B  (it2, exhibit it2)  ``closure_authority`` embedded in each collecting rule

Round 1 left SC-P1 enforcement *specified but unmeasured* (governance C1,
adversary A1): both papers assert current-true-only admission, but neither
demonstrates it against a value-inspecting boundary rather than a presence-only
adapter (the it4 defect). This module makes the boundary executable so the
false/absent/displaced/ambiguous/caller-injection cases are measured, and so a
presence-only *mutant* can be shown to die on the false-closure case.

The real seam this stands in for (grounding only, never imported):
``evaluator.py`` collect layer 2 tests ``source_set in env.closed_sets``;
``env.closed_sets`` is today a bare ``frozenset[str]`` supplied by the caller
(``runner.py`` RunContext.closed_sets, ``runners/derive.py`` scenario field).
This resolver is the design's replacement writer of that membership.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, dataclass
from typing import Callable, Optional, Union

# ---------------------------------------------------------------------------
# Shared domain (prototype shapes; NOT production schemas — check 6)
# ---------------------------------------------------------------------------

# An identity key is order-free so equality never depends on declaration order.
Identity = frozenset  # frozenset[tuple[str, str]]


@dataclass(frozen=True)
class ClosureFinding:
    """One closure attestation. ``value`` carries the attested payload exactly;
    only literal boolean ``True`` means *closed* (ADR-0011 decision 5)."""

    fact_type: str
    identity: Identity
    value: object
    finding_id: str
    version: str
    supersedes: Optional[str] = None  # finding_id this one displaces, or None


def current_findings(findings: list[ClosureFinding]) -> list[ClosureFinding]:
    """ADR-0010 currency: a finding is current iff nothing supersedes it.
    Currency is DERIVED here from the supersession edges, never stored."""
    superseded = {f.supersedes for f in findings if f.supersedes is not None}
    return [f for f in findings if f.finding_id not in superseded]


# Sentinel: more than one *current* match for one authority -> block, never pick.
AMBIGUOUS = object()

Admit = Callable[[str, Identity, list[ClosureFinding]],
                 Union[ClosureFinding, None, object]]


# ---------------------------------------------------------------------------
# The enforcement point, and its mutants
# ---------------------------------------------------------------------------

def admit_current_true(closure_fact_type: str, required_identity: Identity,
                       findings: list[ClosureFinding]):
    """Affirmative-only admission. Returns the EXACT admitting finding, or
    ``None`` (block), or ``AMBIGUOUS`` (block). This is the single site that
    inspects value; every other layer only routes its verdict."""
    matches = [
        f for f in current_findings(findings)
        if f.fact_type == closure_fact_type and f.identity == required_identity
    ]
    if len(matches) == 0:
        return None                       # absent, or displaced-only -> block
    if len(matches) > 1:
        return AMBIGUOUS                  # ambiguous current authority -> block
    f = matches[0]
    if f.value is True:                   # literal boolean true; not truthy
        return f
    return None                           # false / non-true -> block


def admit_presence_only(closure_fact_type, required_identity, findings):
    """MUTANT (the it4 defect): admits on presence of one current finding,
    NEVER inspecting value. Must die on the false-closure case."""
    matches = [
        f for f in current_findings(findings)
        if f.fact_type == closure_fact_type and f.identity == required_identity
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        return AMBIGUOUS
    return None


def admit_presence_any_history(closure_fact_type, required_identity, findings):
    """MUTANT (currency-blind): admits if ANY finding, even a superseded one,
    is literal true. Must die on the displaced-historical-true case."""
    matches = [
        f for f in findings                         # not current_findings
        if f.fact_type == closure_fact_type and f.identity == required_identity
    ]
    trues = [f for f in matches if f.value is True]
    return trues[-1] if trues else None


def admit_truthy(closure_fact_type, required_identity, findings):
    """MUTANT (loose value): admits on any truthy value (1, "true", ...),
    not literal ``True``. Dies on a truthy-but-not-True closure fixture."""
    matches = [
        f for f in current_findings(findings)
        if f.fact_type == closure_fact_type and f.identity == required_identity
    ]
    if len(matches) != 1:
        return AMBIGUOUS if len(matches) > 1 else None
    return matches[0] if matches[0].value else None


# ---------------------------------------------------------------------------
# Resolved membership: the SOLE, unaugmentable carrier (check 3)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ClosureAuthority:
    """Per admitted family: the exact finding + artifact for explanation pins."""

    source_family: str
    finding_id: str
    finding_version: str
    artifact_role: str      # "mapping-citizen" (A) | "adopted-rule" (B)
    artifact_id: str
    artifact_version: str


@dataclass(frozen=True)
class ResolvedMembership:
    """Frozen. ``closed_families`` is DERIVED from authority — there is no
    field, setter, or merge that lets a caller inject a bare family string."""

    authority: tuple  # tuple[ClosureAuthority, ...]

    @property
    def closed_families(self) -> frozenset:
        return frozenset(a.source_family for a in self.authority)

    def pin_for(self, source_family: str) -> Optional[ClosureAuthority]:
        for a in self.authority:
            if a.source_family == source_family:
                return a
        return None


def env_closed_sets(resolved: ResolvedMembership) -> frozenset:
    """The ONLY producer of evaluator layer-2 membership in this design. It
    takes no caller set: contrast production ``RunContext.closed_sets``, which
    is caller-supplied. Caller injection is thus unrepresentable here."""
    return resolved.closed_families


# ---------------------------------------------------------------------------
# Shape A — dedicated mapping citizen (exhibit it1)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MappingEntry:
    source_family: str
    closure_fact_type: str
    required_identity: Identity
    admit_when: str = "current-true"  # only value the v1 shape permits


@dataclass(frozen=True)
class MappingCitizen:
    artifact_id: str
    version: str
    entries: tuple  # tuple[MappingEntry, ...]


def resolve_A(mapping: MappingCitizen, findings: list[ClosureFinding],
              admit: Admit = admit_current_true) -> ResolvedMembership:
    # A6 stale-pin defect: two entries for one family are ambiguous authority.
    # Block the family entirely rather than let one pin overwrite the other.
    counts: dict[str, int] = {}
    for e in mapping.entries:
        counts[e.source_family] = counts.get(e.source_family, 0) + 1

    authorities: list[ClosureAuthority] = []
    for e in mapping.entries:
        if counts[e.source_family] > 1:
            continue                       # ambiguous mapping -> blocked
        if e.admit_when != "current-true":
            continue                       # only affirmative-only in v1
        got = admit(e.closure_fact_type, e.required_identity, findings)
        if got is None or got is AMBIGUOUS:
            continue
        authorities.append(ClosureAuthority(
            source_family=e.source_family,
            finding_id=got.finding_id, finding_version=got.version,
            artifact_role="mapping-citizen",
            artifact_id=mapping.artifact_id, artifact_version=mapping.version,
        ))
    return ResolvedMembership(authority=tuple(authorities))


# ---------------------------------------------------------------------------
# Shape B — embedded adopted-rule parameter (exhibit it2)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ClosureAuthorityParam:
    closure_fact_type: str
    required_identity: Identity
    admitted_value: object = True


@dataclass(frozen=True)
class CollectingRule:
    artifact_id: str
    version: str
    source_family: str
    member_fact_type: str
    closure_authority: ClosureAuthorityParam


def resolve_B(rules: list[CollectingRule], adopted_ids: frozenset,
              findings: list[ClosureFinding],
              admit: Admit = admit_current_true) -> ResolvedMembership:
    adopted = [r for r in rules if r.artifact_id in adopted_ids]  # predicate 1
    # Divergence guard: two adopted rules projecting one family are ambiguous.
    counts: dict[str, int] = {}
    for r in adopted:
        counts[r.source_family] = counts.get(r.source_family, 0) + 1

    authorities: list[ClosureAuthority] = []
    for r in adopted:
        if counts[r.source_family] > 1:
            continue                       # divergent duplicate rules -> block
        ca = r.closure_authority
        if ca.admitted_value is not True:  # only literal true admits in v1
            continue
        got = admit(ca.closure_fact_type, ca.required_identity, findings)
        if got is None or got is AMBIGUOUS:
            continue
        authorities.append(ClosureAuthority(
            source_family=r.source_family,
            finding_id=got.finding_id, finding_version=got.version,
            artifact_role="adopted-rule",
            artifact_id=r.artifact_id, artifact_version=r.version,
        ))
    return ResolvedMembership(authority=tuple(authorities))


__all__ = [
    "ClosureFinding", "current_findings", "AMBIGUOUS",
    "admit_current_true", "admit_presence_only",
    "admit_presence_any_history", "admit_truthy",
    "ClosureAuthority", "ResolvedMembership", "env_closed_sets",
    "MappingEntry", "MappingCitizen", "resolve_A",
    "ClosureAuthorityParam", "CollectingRule", "resolve_B",
    "FrozenInstanceError",
]
