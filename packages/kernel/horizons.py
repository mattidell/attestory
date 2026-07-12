"""Family membership horizons: recorded succession per family and scope.

ADR-0017: each versioned source-family declaration and scope has an
ordinary recorded membership-horizon citizen with explicit succession.
This module owns the horizon chain fold — genesis, transition
validation, and succession — as pure functions over immutable state.

The kernel does not know family member predicates (those are adopted
derivation-family content), so it cannot detect a membership change
smuggled through an ordinary assertion; routing membership changes
through transition acts is the contract of the layers that consume the
adopted declaration. What the kernel does enforce is the chain itself:
one genesis per family/scope, successors only from the current
predecessor, and succession ids never reused — so a replayed, future,
or wrong-predecessor successor rejects atomically.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

from packages.kernel.schema_registry import SchemaRegistry

HORIZON_SCHEMA = "family-horizon.v1"

# Horizons project into the fact lattice as citizens of this entity
# kind, so closure fact types key on them with ordinary entity keys and
# succession feeds the existing individuation root set (ADR-0017
# decision 5) — no third edge, no new key kind.
HORIZON_ENTITY_KIND = "kernel.family-horizon"

ChainKey = tuple[str, str, tuple[tuple[str, str], ...]]


class HorizonModelError(Exception):
    """A horizon act is semantically inadmissible; nothing takes effect."""


@dataclass(frozen=True)
class HorizonLifecycle:
    """Derived lifecycle for one recorded horizon citizen."""

    horizon: dict[str, Any]
    status: str
    successor_id: str | None = None


@dataclass(frozen=True)
class HorizonState:
    """Fold state for every horizon chain in the workspace."""

    horizons: dict[str, HorizonLifecycle] = field(default_factory=dict)
    current_by_chain: dict[ChainKey, str] = field(default_factory=dict)


def initial_state() -> HorizonState:
    return HorizonState()


def chain_key(family: dict[str, str], scope: dict[str, str]) -> ChainKey:
    return (family["id"], family["version"], tuple(sorted(scope.items())))


def current_horizon_id(
    state: HorizonState, family: dict[str, str], scope: dict[str, str]
) -> str | None:
    return state.current_by_chain.get(chain_key(family, scope))


def superseded_horizon_ids(state: HorizonState) -> frozenset[str]:
    """Supersession roots accumulate: a superseded horizon never returns."""
    return frozenset(
        horizon_id
        for horizon_id, lifecycle in state.horizons.items()
        if lifecycle.status != "current"
    )


def _validated_citizen(
    horizon_id: str,
    family: dict[str, str],
    scope: dict[str, str],
    predecessor: str | None,
    registry: SchemaRegistry,
) -> dict[str, Any]:
    citizen: dict[str, Any] = {
        "schema": HORIZON_SCHEMA,
        "id": horizon_id,
        "family": dict(family),
        "scope": dict(scope),
        "predecessor": predecessor,
    }
    registry.validate(HORIZON_SCHEMA, citizen)
    return citizen


def apply_genesis(
    state: HorizonState, payload: dict[str, Any], registry: SchemaRegistry
) -> HorizonState:
    """Establish the initial horizon for a family/scope with no chain yet."""
    key = chain_key(payload["family"], payload["scope"])
    if key in state.current_by_chain:
        raise HorizonModelError(
            f"family {payload['family']['id']} {payload['family']['version']} "
            "already has a horizon chain in this scope; genesis is not repeatable"
        )
    horizon_id = payload["horizon_id"]
    if horizon_id in state.horizons:
        raise HorizonModelError(f"horizon id already recorded: {horizon_id}")
    citizen = _validated_citizen(
        horizon_id, payload["family"], payload["scope"], None, registry
    )
    horizons = dict(state.horizons)
    horizons[horizon_id] = HorizonLifecycle(horizon=citizen, status="current")
    chains = dict(state.current_by_chain)
    chains[key] = horizon_id
    return replace(state, horizons=horizons, current_by_chain=chains)


def apply_transition(
    state: HorizonState, payload: dict[str, Any], registry: SchemaRegistry
) -> tuple[HorizonState, str]:
    """Advance one chain by exactly one successor; returns the predecessor id.

    Rejections cover the recorded admission-negative corpus: no chain
    (genesis missing), a successor id already recorded (replayed), and a
    predecessor that is not the chain's current horizon — whether it is a
    real superseded horizon (wrong predecessor) or was never recorded at
    all (future predecessor). The caller composes this with the member
    half; a raise here means neither half takes effect.
    """
    key = chain_key(payload["family"], payload["scope"])
    current = state.current_by_chain.get(key)
    if current is None:
        raise HorizonModelError(
            f"no horizon chain exists for family {payload['family']['id']} "
            f"{payload['family']['version']} in this scope; genesis is required first"
        )
    successor = payload["successor"]
    if successor["id"] in state.horizons:
        raise HorizonModelError(
            f"replayed successor: horizon id already recorded: {successor['id']}"
        )
    named = successor["predecessor"]
    if named != current:
        if named in state.horizons:
            raise HorizonModelError(
                f"wrong predecessor: {named} is superseded; the current "
                f"horizon is {current}"
            )
        raise HorizonModelError(
            f"unknown predecessor: {named} is not recorded for this chain; "
            f"the current horizon is {current}"
        )
    citizen = _validated_citizen(
        successor["id"], payload["family"], payload["scope"], current, registry
    )
    horizons = dict(state.horizons)
    predecessor_lifecycle = horizons[current]
    horizons[current] = HorizonLifecycle(
        horizon=predecessor_lifecycle.horizon,
        status="superseded",
        successor_id=successor["id"],
    )
    horizons[successor["id"]] = HorizonLifecycle(horizon=citizen, status="current")
    chains = dict(state.current_by_chain)
    chains[key] = successor["id"]
    return replace(state, horizons=horizons, current_by_chain=chains), current
