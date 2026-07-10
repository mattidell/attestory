"""Fact types, entities, and the derived fact lattice.

Fact types arrive by bundle adoption; entities arrive by introduction
acts. Facts themselves are never stored: the lattice is a deterministic
projection over adopted fact types and current entities (Ontology §2 —
some facts arrive with the territory, others are individuated into
existence when the citizens they're keyed on appear). Because the
lattice is derived, there is no second store to fall out of sync
(Article 5), and displacement of a keyed-on citizen displaces its facts
by recomputation, not by write fan-out (Article 7).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field, replace
from typing import Any

import jsonschema

from packages.kernel.schema_registry import SchemaRegistry

BUNDLE_SCHEMA = "bundle.v1"
FACT_TYPE_SCHEMA = "fact-type.v1"
ENTITY_SCHEMA = "entity.v1"


class FactModelError(Exception):
    """An act's content is semantically inadmissible for the workspace."""


@dataclass(frozen=True)
class Fact:
    """A particular question as it applies to this workspace.

    Identity is the fact type plus its key bindings; the id is a
    canonical rendering of that identity, stable across projections.
    """

    fact_id: str
    fact_type_id: str
    nature: str
    keys: tuple[tuple[str, str], ...]
    individuated_by: tuple[str, ...]


@dataclass(frozen=True)
class KernelState:
    """The fold state of a workspace projection (grows by track)."""

    fact_types: dict[str, dict[str, Any]] = field(default_factory=dict)
    entities: dict[str, dict[str, Any]] = field(default_factory=dict)


def initial_state() -> KernelState:
    return KernelState()


def _validate_fact_type(fact_type: dict[str, Any], registry: SchemaRegistry) -> None:
    registry.validate(FACT_TYPE_SCHEMA, fact_type)
    names = [key["name"] for key in fact_type["identity_keys"]]
    if len(names) != len(set(names)):
        raise FactModelError(
            f"fact type {fact_type['id']}: duplicate identity key names"
        )
    try:
        jsonschema.Draft202012Validator.check_schema(fact_type["value_schema"])
    except jsonschema.SchemaError as exc:
        raise FactModelError(
            f"fact type {fact_type['id']}: value_schema is not valid JSON Schema: "
            f"{exc.message}"
        ) from exc


def apply_bundle_adoption(
    state: KernelState, payload: dict[str, Any], registry: SchemaRegistry
) -> KernelState:
    bundle = payload["bundle"]
    registry.validate(BUNDLE_SCHEMA, bundle)
    fact_types = dict(state.fact_types)
    seen: set[str] = set()
    for fact_type in bundle["fact_types"]:
        _validate_fact_type(fact_type, registry)
        if fact_type["id"] in seen:
            raise FactModelError(
                f"bundle {bundle['id']}: duplicate fact type {fact_type['id']}"
            )
        seen.add(fact_type["id"])
        # Re-adoption under a revised bundle supersedes the fact type;
        # the earlier declaration remains in the act history.
        fact_types[fact_type["id"]] = fact_type
    return replace(state, fact_types=fact_types)


def apply_entity_introduced(
    state: KernelState, payload: dict[str, Any], registry: SchemaRegistry
) -> KernelState:
    entity = payload["entity"]
    registry.validate(ENTITY_SCHEMA, entity)
    if entity["id"] in state.entities:
        raise FactModelError(f"entity already exists: {entity['id']}")
    entities = dict(state.entities)
    entities[entity["id"]] = entity
    return replace(state, entities=entities)


def _fact_id(fact_type_id: str, keys: tuple[tuple[str, str], ...]) -> str:
    bound = ",".join(f"{name}={value}" for name, value in keys)
    return f"{fact_type_id}|{bound}"


def facts_of(state: KernelState) -> dict[str, Fact]:
    """The derived fact lattice: every question the workspace holds.

    For each fact type, one fact exists per combination of key bindings:
    entity keys bind to each current entity of the declared kind,
    literal keys to each declared value. A fact type keyed on an entity
    kind with no current entities yields no facts yet — the questions
    arrive with the citizens they are about.
    """
    lattice: dict[str, Fact] = {}
    for fact_type in state.fact_types.values():
        per_key_bindings: list[list[tuple[str, str, str | None]]] = []
        for key in fact_type["identity_keys"]:
            bindings: list[tuple[str, str, str | None]] = []
            if key["kind"] == "entity":
                for entity_id, entity in sorted(state.entities.items()):
                    if entity["kind"] == key["entity_kind"]:
                        bindings.append((key["name"], entity_id, entity_id))
            else:
                for value in key["values"]:
                    bindings.append((key["name"], value, None))
            per_key_bindings.append(bindings)
        for combination in itertools.product(*per_key_bindings):
            keys = tuple((name, value) for name, value, _ in combination)
            individuated_by = tuple(
                entity_id for _, _, entity_id in combination if entity_id is not None
            )
            fact_id = _fact_id(fact_type["id"], keys)
            lattice[fact_id] = Fact(
                fact_id=fact_id,
                fact_type_id=fact_type["id"],
                nature=fact_type["nature"],
                keys=keys,
                individuated_by=individuated_by,
            )
    return lattice


_APPLIERS = {
    "bundle-adoption": apply_bundle_adoption,
    "entity-introduced": apply_entity_introduced,
}


def apply_act(
    state: KernelState, act: dict[str, Any], registry: SchemaRegistry
) -> KernelState:
    """Advance the fold by one act, validating semantic admissibility."""
    applier = _APPLIERS.get(act["kind"])
    if applier is None:
        raise FactModelError(f"no applier for act kind: {act['kind']}")
    return applier(state, act["payload"], registry)


def project(acts: tuple[dict[str, Any], ...], registry: SchemaRegistry) -> KernelState:
    state = initial_state()
    for act in acts:
        state = apply_act(state, act, registry)
    return state
