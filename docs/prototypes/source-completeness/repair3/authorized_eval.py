"""Repair pass 3: shape-A authority construction/invariant boundary.

PROTOTYPE ONLY (charter-repair3). A focused refinement over the repair1 resolver
and the repair2 throwaway evaluator. No production imports, edits, or execution.

Round-2 adversary finding (reviews/round-2-adversary.md): repair2 proved *sole
use* of the authority carrier but not *sole construction* — `ResolvedMembership`
and `ClosureAuthority` are public dataclasses and `Env` accepts any one, so a
caller can fabricate authority (fake finding + mapping) and publish a zero that
pins the fabrication. Frozen state prevents mutation, not construction.

This layer closes that boundary for **shape A only** (the selected shape; shape
B is rejected for rule-evolution outage and is not restored here).

**What the contract guarantees — and does not.** Python cannot make an object
un-constructible, so this is NOT language-level unforgeability. The guarantee is
*re-derivation*: the evaluator trusts an `AuthorizedMembership` only after
`validate_membership` re-runs shape-A resolution over the declared, pinned inputs
(the adopted mapping citizen + current closure findings) and confirms the carrier
equals that fresh resolver output exactly — same families, one per family, each
retained pin being the current literal-true finding under the declared mapping
version. A fabricated, duplicate, stale, or mapping-mismatched carrier cannot
equal fresh resolver output over real inputs, so it is rejected before any
publication. The sanctioned producer `authorize()` is the only construction path
a well-behaved caller uses; `validate_membership` is what makes any other path
safe.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "repair1"))
sys.path.insert(0, os.path.join(_HERE, "..", "repair2"))

import resolver as R           # noqa: E402  (repair1)
import prototype_eval as E     # noqa: E402  (repair2 two-layer collect + pins)


class AuthorityInvalid(Exception):
    """Raised when a presented carrier fails re-derivation validation."""


@dataclass(frozen=True)
class AuthorizedMembership:
    """The carrier the evaluator consumes. Duck-compatible with repair2 `Env`
    (`closed_families`, `pin_for`). Carries mapping provenance so it can be
    re-validated against declared inputs. Constructible by anyone — hence the
    mandatory `validate_membership` gate; construction alone confers no trust."""

    authorities: tuple            # tuple[R.ClosureAuthority, ...]
    mapping_id: str
    mapping_version: str

    @property
    def closed_families(self) -> frozenset:
        return frozenset(a.source_family for a in self.authorities)

    def pin_for(self, source_family: str):
        for a in self.authorities:
            if a.source_family == source_family:
                return a
        return None


def authorize(mapping: "R.MappingCitizen", findings) -> AuthorizedMembership:
    """Sole sanctioned construction path. Runs shape-A resolution (which already
    blocks duplicate mapping entries and admits only current literal-true) and
    stamps the mapping provenance onto the carrier."""
    resolved = R.resolve_A(mapping, findings)
    return AuthorizedMembership(resolved.authority, mapping.artifact_id, mapping.version)


def validate_membership(carrier: AuthorizedMembership,
                        mapping: "R.MappingCitizen", findings) -> None:
    """Mandatory gate. Re-derive from the declared inputs and require the carrier
    to match exactly; raise `AuthorityInvalid` otherwise. This is the whole
    boundary — it rejects fabricated, duplicate, stale, and mapping-mismatched
    carriers regardless of how they were constructed."""
    # Provenance: the carrier must name the mapping actually declared/pinned.
    if (carrier.mapping_id, carrier.mapping_version) != (mapping.artifact_id, mapping.version):
        raise AuthorityInvalid(
            f"carrier mapping provenance {carrier.mapping_id}@{carrier.mapping_version} "
            f"!= declared {mapping.artifact_id}@{mapping.version}")
    # One authority per family (order-independent).
    families = [a.source_family for a in carrier.authorities]
    if len(families) != len(set(families)):
        raise AuthorityInvalid("duplicate same-family authority in carrier")
    # Exact correspondence with fresh resolver output over the real findings.
    fresh = R.resolve_A(mapping, findings)
    if set(carrier.authorities) != set(fresh.authority):
        raise AuthorityInvalid(
            "carrier authority does not equal resolver output over declared inputs")


# ---------------------------------------------------------------------------
# Evaluator entry points
# ---------------------------------------------------------------------------

def run_rule_authorized(rule, sources, mapping, findings):
    """Production-shaped path: no external carrier at all. The evaluator builds
    authority itself from declared inputs, validates it, then runs the faithful
    two-layer collect. A caller has nothing to fabricate here."""
    carrier = authorize(mapping, findings)
    validate_membership(carrier, mapping, findings)
    return E.run_rule(rule, E.Env(sources, carrier))


def run_rule_with_carrier(rule, sources, carrier, mapping, findings):
    """Legacy-shaped path: an externally-supplied carrier is presented. The
    mandatory gate re-derives and rejects any carrier that is not exactly the
    resolver output; only then does it evaluate."""
    validate_membership(carrier, mapping, findings)
    return E.run_rule(rule, E.Env(sources, carrier))


def run_rule_trusting(rule, sources, carrier):
    """MUTANT (constructor bypass = the repair2 behavior): trusts a carrier
    without validation. Must be killed by the fabricated / duplicate cases —
    it publishes where the validated paths reject."""
    return E.run_rule(rule, E.Env(sources, carrier))
