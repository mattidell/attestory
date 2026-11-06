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
import json
import weakref
import threading
from bisect import bisect_left, insort
from collections import OrderedDict
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field, replace
from importlib.metadata import version
from typing import Any, NamedTuple

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
class EntityLifecycle:
    """Derived lifecycle for one entity citizen."""

    entity: dict[str, Any]
    status: str
    successor_id: str | None = None


@dataclass(frozen=True)
class KernelState:
    """The fold state of a workspace projection (grows by track)."""

    fact_types: dict[str, dict[str, Any]] = field(default_factory=dict)
    entities: dict[str, EntityLifecycle] = field(default_factory=dict)
    # Type ids retired by an adopted migration artifact. A later bundle
    # adoption that still lists one of these ids does not re-admit it.
    retired_fact_type_ids: frozenset[str] = field(default_factory=frozenset)
    # (fact_type_id, migration_artifact_id) for each retirement.
    retired_by: tuple[tuple[str, str], ...] = ()
    adopted_migrations: tuple[dict[str, Any], ...] = ()


def initial_state() -> KernelState:
    return KernelState()


# Successful value_schema checks only. The key is the canonical document, the
# jsonschema version, and the draft this function actually calls. An invalid
# schema is never stored, so the next fold checks it again and raises.
_VALUE_SCHEMA_DRAFT = "Draft202012"
_JSONSCHEMA_VERSION = version("jsonschema")
_VALUE_SCHEMA_CHECKS: OrderedDict[tuple[str, str, str], None] = OrderedDict()
_VALUE_SCHEMA_CHECKS_MAX = 4096


def _is_strict_json(value: object) -> bool:
    """True when ``value`` is exactly a JSON tree: dicts with string keys,
    lists, and JSON scalars. ``json.dumps`` writes a tuple like a list, but
    ``check_schema`` can accept one and reject the other, so a tree that is
    not strict JSON has no faithful text key."""
    if value is None or isinstance(value, (bool, str)):
        return True
    if isinstance(value, (int, float)):
        return type(value) in (int, float)
    if type(value) is list:
        return all(_is_strict_json(item) for item in value)
    if type(value) is dict:
        return all(
            type(key) is str and _is_strict_json(item) for key, item in value.items()
        )
    return False


def _value_schema_key(value_schema: object) -> tuple[str, str, str] | None:
    if not _is_strict_json(value_schema):
        return None
    try:
        canonical = json.dumps(
            value_schema,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError):
        return None
    return (canonical, _JSONSCHEMA_VERSION, _VALUE_SCHEMA_DRAFT)


def _check_value_schema(fact_type: dict[str, Any]) -> None:
    value_schema = fact_type["value_schema"]
    key = _value_schema_key(value_schema)
    if key is not None and key in _VALUE_SCHEMA_CHECKS:
        _VALUE_SCHEMA_CHECKS.move_to_end(key)
        return
    try:
        jsonschema.Draft202012Validator.check_schema(value_schema)
    except jsonschema.SchemaError as exc:
        raise FactModelError(
            f"fact type {fact_type['id']}: value_schema is not valid JSON Schema: "
            f"{exc.message}"
        ) from exc
    if key is not None:
        _VALUE_SCHEMA_CHECKS[key] = None
        if len(_VALUE_SCHEMA_CHECKS) > _VALUE_SCHEMA_CHECKS_MAX:
            _VALUE_SCHEMA_CHECKS.popitem(last=False)


def _validate_fact_type(fact_type: dict[str, Any], registry: SchemaRegistry) -> None:
    registry.validate_declared(fact_type)
    names = [key["name"] for key in fact_type["identity_keys"]]
    if len(names) != len(set(names)):
        raise FactModelError(
            f"fact type {fact_type['id']}: duplicate identity key names"
        )
    _check_value_schema(fact_type)


def apply_bundle_adoption(
    state: KernelState, payload: dict[str, Any], registry: SchemaRegistry
) -> KernelState:
    bundle = payload["bundle"]
    registry.validate_declared(bundle)
    fact_types = dict(state.fact_types)
    seen: set[str] = set()
    for fact_type in bundle["fact_types"]:
        _validate_fact_type(fact_type, registry)
        if fact_type["id"] in seen:
            raise FactModelError(
                f"bundle {bundle['id']}: duplicate fact type {fact_type['id']}"
            )
        seen.add(fact_type["id"])
        if fact_type["id"] in state.retired_fact_type_ids:
            # Retired by an adopted migration artifact. The bundle may
            # still list the id (a shared vocabulary that also carries
            # types this migration does not name); re-admission would
            # undo the supersession root.
            continue
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
    entities[entity["id"]] = EntityLifecycle(entity=entity, status="current")
    return replace(state, entities=entities)


def apply_entity_superseded(
    state: KernelState, payload: dict[str, Any], registry: SchemaRegistry
) -> KernelState:
    """Succession: the questions an entity brought leave current state with it.

    The facts individuated on the superseded entity — and the findings
    answering them — are displaced by recomputation (the lattice projects
    from current entities; currency walks the individuation edge). No
    finding is rewritten; history keeps everything.
    """
    entity_id = payload["entity_id"]
    entities = dict(state.entities)
    existing = entities.get(entity_id)
    if existing is None:
        raise FactModelError(f"unknown entity: {entity_id}")
    if existing.status != "current":
        raise FactModelError(f"entity is not current: {entity_id}")

    replacement = payload.get("replacement")
    successor_id: str | None = None
    if replacement is not None:
        registry.validate(ENTITY_SCHEMA, replacement)
        successor_id = replacement["id"]
        if successor_id == entity_id:
            raise FactModelError("replacement entity must have a new id")
        if successor_id in entities:
            raise FactModelError(f"entity already exists: {successor_id}")
        entities[successor_id] = EntityLifecycle(entity=replacement, status="current")

    entities[entity_id] = EntityLifecycle(
        entity=existing.entity,
        status="superseded",
        successor_id=successor_id,
    )
    return replace(state, entities=entities)


def apply_migration_adoption(
    state: KernelState, payload: dict[str, Any], registry: SchemaRegistry
) -> KernelState:
    """Take up a migration artifact as a direct supersession root.

    The named predecessor types leave current ``fact_types`` and are
    recorded as retired. Successor types must already be current —
    ordinary bundle adoption admits them; this act does not copy type
    bodies. Findings of the retired types become supersession roots in
    currency; this function does not walk edges and does not touch
    ``Fact.individuated_by``.
    """
    migration = payload["migration"]
    registry.validate_declared(migration)
    migration_id = migration["id"]
    if any(existing["id"] == migration_id for existing in state.adopted_migrations):
        raise FactModelError(f"migration already adopted: {migration_id}")
    pairs = migration["pairs"]
    predecessors = [pair["predecessor"] for pair in pairs]
    successors = [pair["successor"] for pair in pairs]
    if len(predecessors) != len(set(predecessors)):
        raise FactModelError(
            f"migration {migration_id}: predecessor list names an id more than once"
        )
    if len(successors) != len(set(successors)):
        raise FactModelError(
            f"migration {migration_id}: successor list names an id more than once"
        )
    overlap = set(predecessors) & set(successors)
    if overlap:
        raise FactModelError(
            f"migration {migration_id}: predecessor and successor sets overlap: "
            f"{sorted(overlap)}"
        )
    for successor_id in successors:
        if successor_id in state.retired_fact_type_ids:
            raise FactModelError(
                f"migration {migration_id}: successor type is retired: {successor_id}"
            )
        if successor_id not in state.fact_types:
            raise FactModelError(
                f"migration {migration_id}: successor type is not current: {successor_id}"
            )
    for predecessor_id in predecessors:
        if predecessor_id in state.retired_fact_type_ids:
            raise FactModelError(
                f"migration {migration_id}: predecessor type is already retired: "
                f"{predecessor_id}"
            )
    fact_types = dict(state.fact_types)
    for predecessor_id in predecessors:
        fact_types.pop(predecessor_id, None)
    return replace(
        state,
        fact_types=fact_types,
        retired_fact_type_ids=state.retired_fact_type_ids | frozenset(predecessors),
        retired_by=state.retired_by
        + tuple((predecessor_id, migration_id) for predecessor_id in predecessors),
        adopted_migrations=state.adopted_migrations + (migration,),
    )


def superseded_entity_ids(state: KernelState) -> frozenset[str]:
    return frozenset(
        entity_id
        for entity_id, lifecycle in state.entities.items()
        if lifecycle.status != "current"
    )


def _fact_id(fact_type_id: str, keys: tuple[tuple[str, str], ...]) -> str:
    bound = ",".join(f"{name}={value}" for name, value in keys)
    return f"{fact_type_id}|{bound}"


def fact_id_for(fact_type_id: str, keys: tuple[tuple[str, str], ...]) -> str:
    """Public composer for a fact id from a fact type and ordered key bindings.

    Exposed so callers outside this module (e.g. the ``closed-on-attestation``
    supersession-policy predicate in ``findings.py``) can project an
    already-answered fact's own key bindings onto another fact type's
    identity-key names without duplicating the id-rendering rule.
    """
    return _fact_id(fact_type_id, keys)


def _project_fact_lattice(
    state: KernelState, *, include_displaced: bool = False
) -> dict[str, Fact]:
    """Build one fact lattice from ``state``. No reuse."""
    lattice: dict[str, Fact] = {}
    for fact_type in state.fact_types.values():
        per_key_bindings: list[list[tuple[str, str, str | None]]] = []
        for key in fact_type["identity_keys"]:
            bindings: list[tuple[str, str, str | None]] = []
            if key["kind"] == "entity":
                for entity_id, lifecycle in sorted(state.entities.items()):
                    if lifecycle.entity["kind"] != key["entity_kind"]:
                        continue
                    if lifecycle.status != "current" and not include_displaced:
                        continue
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


class _HistoricalLatticeMemo:
    """Historical lattices for live fact states, keyed by object identity.

    Same boundary as ``_CurrentLatticeHolder``: a lattice is reused only
    when the ``KernelState`` is that object. ``KernelState`` is not
    hashable, so this is an id plus a weak reference rather than a
    ``WeakKeyDictionary``. The callback drops the entry when the state
    is collected, and lookup rejects a recycled id.
    """

    def __init__(self) -> None:
        self._entries: dict[
            int, tuple[weakref.ref[KernelState], dict[str, Fact]]
        ] = {}
        self._pending: dict[int, _HistoricalSnapshot] = {}

    def for_state(self, fact_state: KernelState) -> dict[str, Fact]:
        found = self._get(fact_state)
        if found is not None:
            return found
        pending = self._snapshot(fact_state)
        if pending is not None:
            index = pending.index()
            if (index is None or index.owner_thread != threading.get_ident()
                    or index.generation != pending.generation):
                index = _LatticeIndex(include_displaced=True)
                index.update(pending.metadata)
            lattice = _LatticeView(index, index.generation, pending.metadata).materialize()
            self._store(fact_state, lattice)
            return lattice
        lattice = _project_fact_lattice(fact_state, include_displaced=True)
        self._store(fact_state, lattice)
        return lattice

    def _get(self, fact_state: KernelState) -> dict[str, Fact] | None:
        entry = self._entries.get(id(fact_state))
        if entry is None:
            return None
        ref, lattice = entry
        if ref() is not fact_state:
            self._entries.pop(id(fact_state), None)
            return None
        return lattice

    def _store(self, fact_state: KernelState, lattice: dict[str, Fact]) -> None:
        ident = id(fact_state)
        self._pending.pop(ident, None)

        def _drop(
            ref: weakref.ref[KernelState], ident: int = ident
        ) -> None:
            current = self._entries.get(ident)
            if current is not None and current[0] is ref:
                self._entries.pop(ident, None)

        self._entries[ident] = (weakref.ref(fact_state, _drop), lattice)

    def _snapshot(self, state: KernelState) -> _HistoricalSnapshot | None:
        entry = self._pending.get(id(state))
        if entry is not None and entry.state() is not state:
            self._pending.pop(id(state), None)
            return None
        return entry

    def _remember(self, state: KernelState, view: _LatticeView) -> None:
        ident = id(state)

        def drop(ref: weakref.ref[KernelState]) -> None:
            current = self._pending.get(ident)
            if current is not None and current.state is ref:
                self._pending.pop(ident, None)

        self._pending[ident] = _HistoricalSnapshot(
            weakref.ref(state, drop), view.metadata, weakref.ref(view.index), view.generation
        )


class _LatticeKey(NamedTuple):
    name: str
    entity_kind: str | None
    literals: tuple[str, ...] = ()


class _LatticeDeclaration(NamedTuple):
    map_id: str
    type_id: str
    nature: str
    keys: tuple[_LatticeKey, ...]


_LatticeMetadata = tuple[
    tuple[_LatticeDeclaration, ...], tuple[tuple[str, str], ...]
]
_Coordinate = str | int
_Position = tuple[_Coordinate, ...]
_Axes = tuple[tuple[_Coordinate, ...], ...]


def _lattice_metadata(state: KernelState, include_displaced: bool) -> _LatticeMetadata:
    """Copy construction inputs, including nested mutable declaration fields.

    No identity-only shortcut: callers can mutate nested dictionaries. These
    metadata scans are growing costs, distinct from changed-product work.
    """
    declarations = tuple(
        _LatticeDeclaration(map_id, ft["id"], ft["nature"], tuple(
            _LatticeKey(key["name"], key["entity_kind"]) if key["kind"] == "entity"
            else _LatticeKey(key["name"], None, tuple(key["values"]))
            for key in ft["identity_keys"]
        )) for map_id, ft in state.fact_types.items()
    )
    entities = tuple(sorted(
        (entity_id, lifecycle.entity["kind"])
        for entity_id, lifecycle in state.entities.items()
        if include_displaced or lifecycle.status == "current"
    ))
    return declarations, entities


class _LatticeProduct:
    """Combination records for one declaration, including overwritten ids.

    Each axis has only string entity ids or only integer literal positions;
    positions within one product therefore have a total lexicographic order.
    First position owns insertion order; last position owns the winning Fact.
    """

    def __init__(self, declaration: _LatticeDeclaration, axes: _Axes) -> None:
        self.declaration = declaration
        self.axes = axes
        self.by_combination: dict[_Position, str] = {}
        self.by_id: dict[str, tuple[list[_Position], dict[_Position, Fact]]] = {}
        for combination in itertools.product(*axes):
            self._add(combination)

    def _add(self, combination: _Position) -> None:
        keys: list[tuple[str, str]] = []
        owners: list[str] = []
        for key, token in zip(self.declaration.keys, combination):
            if key.entity_kind is not None:
                assert isinstance(token, str)
                keys.append((key.name, token))
                owners.append(token)
            else:
                assert isinstance(token, int)
                keys.append((key.name, key.literals[token]))
        bindings = tuple(keys)
        fact_id = _fact_id(self.declaration.type_id, bindings)
        fact = Fact(fact_id, self.declaration.type_id, self.declaration.nature,
                    bindings, tuple(owners))
        positions, rows = self.by_id.setdefault(fact_id, ([], {}))
        insort(positions, combination)
        rows[combination] = fact
        self.by_combination[combination] = fact_id

    def _remove(self, combination: _Position) -> None:
        fact_id = self.by_combination.pop(combination)
        positions, rows = self.by_id[fact_id]
        positions.pop(bisect_left(positions, combination))
        del rows[combination]
        if not positions:
            del self.by_id[fact_id]

    def update_axes(self, axes: _Axes) -> None:
        removed = [set(old)-set(new) for old, new in zip(self.axes, axes)]
        added = [set(new)-set(old) for old, new in zip(self.axes, axes)]
        # First changed axis owns a combination, so multi-axis changes produce
        # disjoint slices even when several keys use the same entity kind.
        for axis, values in enumerate(removed):
            if values:
                slices = [tuple(v for v in old if v not in removed[i]) if i < axis
                          else tuple(v for v in old if v in values) if i == axis else old
                          for i, old in enumerate(self.axes)]
                for combination in itertools.product(*slices):
                    self._remove(combination)
        for axis, values in enumerate(added):
            if values:
                slices = [tuple(v for v in new if v not in added[i]) if i < axis
                          else tuple(v for v in new if v in values) if i == axis else new
                          for i, new in enumerate(axes)]
                for combination in itertools.product(*slices):
                    self._add(combination)
        self.axes = axes

    def get(self, fact_id: str) -> Fact | None:
        found = self.by_id.get(fact_id)
        return None if found is None else found[1][found[0][-1]]

    def ordered(self) -> Iterator[tuple[str, Fact]]:
        for fact_id, (positions, rows) in sorted(self.by_id.items(), key=lambda item: item[1][0][0]):
            yield fact_id, rows[positions[-1]]


class _LatticeIndex:
    """Projection-local delta construction; never owns a public dictionary."""

    def __init__(self, include_displaced: bool = False) -> None:
        self.include_displaced = include_displaced
        self.metadata: _LatticeMetadata | None = None
        self.parts: dict[str, _LatticeProduct] = {}
        self.by_type_id: dict[str, list[_LatticeProduct]] = {}
        self.generation = 0
        self.owner_thread = threading.get_ident()

    def view(self, state: KernelState) -> _LatticeView:
        return self.view_metadata(_lattice_metadata(state, self.include_displaced))

    def view_metadata(self, metadata: _LatticeMetadata) -> _LatticeView:
        if metadata != self.metadata:
            self.update(metadata)
        return _LatticeView(self, self.generation, metadata)

    def update(self, metadata: _LatticeMetadata) -> None:
        declarations, entities = metadata
        by_kind: dict[str, list[str]] = {}
        for entity_id, kind in entities:
            by_kind.setdefault(kind, []).append(entity_id)
        parts: dict[str, _LatticeProduct] = {}
        for declaration in declarations:
            axes: _Axes = tuple(
                tuple(by_kind.get(key.entity_kind, ())) if key.entity_kind is not None
                else tuple(range(len(key.literals))) for key in declaration.keys
            )
            prior = self.parts.get(declaration.map_id)
            if prior is None or prior.declaration != declaration:
                prior = _LatticeProduct(declaration, axes)
            elif prior.axes != axes:
                prior.update_axes(axes)
            parts[declaration.map_id] = prior
        self.parts = parts
        self.by_type_id = {}
        for part in parts.values():
            self.by_type_id.setdefault(part.declaration.type_id, []).append(part)
        self.metadata = metadata
        self.generation += 1


class _LatticeView(Mapping[str, Fact]):
    """Private lookup view; materialization is always a fresh ordered dict."""

    def __init__(self, index: _LatticeIndex, generation: int, metadata: _LatticeMetadata) -> None:
        self.index = index
        self.generation = generation
        self.metadata = metadata
        self._snapshot: _LatticeIndex | None = None

    def _index(self) -> _LatticeIndex:
        if self.index.generation == self.generation:
            return self.index
        if self._snapshot is None:
            self._snapshot = _LatticeIndex(self.index.include_displaced)
            self._snapshot.update(self.metadata)
        return self._snapshot

    def __getitem__(self, fact_id: str) -> Fact:
        # Published type-id patterns exclude '|'; entity ids remain opaque.
        parts = self._index().by_type_id.get(fact_id.split("|", 1)[0], ())
        for part in reversed(parts):
            row = part.get(fact_id)
            if row is not None:
                return row
        raise KeyError(fact_id)

    def __iter__(self) -> Iterator[str]:
        return iter(self.materialize())

    def __len__(self) -> int:
        index = self._index()
        # Admitted types have unique ids; tolerate duplicate nested mutations
        # defensively without claiming malformed states as admitted contracts.
        if any(len(parts) > 1 for parts in index.by_type_id.values()):
            return len(self.materialize())
        return sum(len(part.by_id) for part in index.parts.values())

    def materialize(self) -> dict[str, Fact]:
        result: dict[str, Fact] = {}
        for part in self._index().parts.values():
            result.update(part.ordered())
        return result


@dataclass(frozen=True)
class _HistoricalSnapshot:
    state: weakref.ref[KernelState]
    metadata: _LatticeMetadata
    index: weakref.ref[_LatticeIndex]
    generation: int


class _ReplayLattices:
    def __init__(self) -> None:
        self.owner_thread = threading.get_ident()
        self.current = _LatticeIndex()
        self.historical = _LatticeIndex(include_displaced=True)


_REPLAY_LATTICES: ContextVar[_ReplayLattices | None] = ContextVar("replay_lattices", default=None)


@contextmanager
def _replay_lattices() -> Iterator[None]:
    """Nested calls own independent indexes; exceptions restore the caller."""
    token = _REPLAY_LATTICES.set(_ReplayLattices())
    try:
        yield
    finally:
        _REPLAY_LATTICES.reset(token)


def _active_lattices() -> _ReplayLattices | None:
    replay = _REPLAY_LATTICES.get()
    if replay is not None and replay.owner_thread == threading.get_ident():
        return replay
    return None


def _current_lattice_for_replay(state: KernelState) -> Mapping[str, Fact] | None:
    replay = _active_lattices()
    return None if replay is None else replay.current.view(state)


def _historical_lattice_for_currency(state: KernelState) -> Mapping[str, Fact]:
    replay = _active_lattices()
    if replay is None:
        return facts_of(state, include_displaced=True)
    existing = _HISTORICAL_LATTICES._get(state)
    if existing is not None:
        return existing
    pending = _HISTORICAL_LATTICES._snapshot(state)
    if pending is not None:
        return replay.historical.view_metadata(pending.metadata)
    view = replay.historical.view(state)
    # Preserve the incumbent's first-read snapshot side effect, even if the
    # caller later mutates the retained state's nested declarations/entities.
    _HISTORICAL_LATTICES._remember(state, view)
    return view


_HISTORICAL_LATTICES = _HistoricalLatticeMemo()


def facts_of(state: KernelState, *, include_displaced: bool = False) -> dict[str, Fact]:
    """The derived fact lattice: every question the workspace holds.

    For each fact type, one fact exists per combination of key bindings:
    entity keys bind to each current entity of the declared kind,
    literal keys to each declared value. A fact type keyed on an entity
    kind with no current entities yields no facts yet — the questions
    arrive with the citizens they are about, and leave current state
    when those citizens are superseded (``include_displaced=True``
    projects the full historical lattice, which currency uses to walk
    individuation edges).

    The historical projection is reused for the lifetime of that exact
    ``KernelState`` object. The current projection is not: callers that
    need it across finding acts keep their own holder.
    """
    if include_displaced:
        return _HISTORICAL_LATTICES.for_state(state)
    return _project_fact_lattice(state, include_displaced=False)


_APPLIERS = {
    "bundle-adoption": apply_bundle_adoption,
    "entity-introduced": apply_entity_introduced,
    "entity-superseded": apply_entity_superseded,
    "migration-adoption": apply_migration_adoption,
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
