"""Synthetic recorded-horizon reducer; prototype evidence only."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


class Reject(ValueError):
    """An act cannot enter the synthetic authoritative record."""


Pair = tuple[str, str]
Edges = dict[str, dict[str, set[str]]]


@dataclass
class State:
    horizons: dict[str, tuple[Pair, str | None]] = field(default_factory=dict)
    current_horizon: dict[Pair, str] = field(default_factory=dict)
    closure_facts: dict[str, tuple[Pair, str]] = field(default_factory=dict)
    closure_findings: dict[str, str] = field(default_factory=dict)  # finding -> fact
    members: dict[tuple[Pair, str], bool] = field(default_factory=dict)
    zeroes: dict[str, str] = field(default_factory=dict)  # zero -> closure finding
    superseded_horizons: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class Currency:
    current: frozenset[str]
    displaced: frozenset[str]
    roots: frozenset[str]
    edges: dict[str, dict[str, frozenset[str]]]
    reasons: dict[str, tuple[tuple[str, str], ...]]


def _pair(act: Mapping[str, Any]) -> Pair:
    family, scope = act.get("family"), act.get("scope")
    if not isinstance(family, str) or not family or not isinstance(scope, str) or not scope:
        raise Reject("family and scope must be nonempty strings")
    if family == "GLOBAL":
        raise Reject("global horizon is forbidden")
    return family, scope


def _only(act: Mapping[str, Any], permitted: set[str]) -> None:
    unknown = set(act) - permitted
    if unknown:
        raise Reject(f"unknown/caller authority fields: {sorted(unknown)}")


def _validate_horizon(state: State, pair: Pair, horizon: Mapping[str, Any], previous: str | None) -> str:
    _only(horizon, {"id", "family", "scope", "previous"})
    ident = horizon.get("id")
    if not isinstance(ident, str) or not ident or ident in state.horizons:
        raise Reject("horizon id must be a new nonempty string")
    if (horizon.get("family"), horizon.get("scope")) != pair:
        raise Reject("horizon must preserve member-change family/scope")
    if horizon.get("previous") != previous:
        raise Reject("horizon previous must be the current family/scope horizon")
    return ident


def _new_horizon(state: State, pair: Pair, horizon: Mapping[str, Any], previous: str | None) -> str:
    ident = _validate_horizon(state, pair, horizon, previous)
    state.horizons[ident] = (pair, previous)
    state.current_horizon[pair] = ident
    state.closure_facts[f"C@{ident}"] = (pair, ident)
    if previous is not None:
        state.superseded_horizons.add(previous)
    return ident


def apply(state: State, act: Mapping[str, Any]) -> None:
    kind = act.get("kind")
    if kind == "open_family":
        _only(act, {"kind", "family", "scope", "horizon"})
        pair = _pair(act)
        if pair in state.current_horizon:
            raise Reject("family/scope already has a horizon")
        horizon = act.get("horizon")
        if not isinstance(horizon, Mapping):
            raise Reject("open_family needs an initial horizon")
        _new_horizon(state, pair, horizon, None)
        return

    if kind == "member_change":
        _only(act, {"kind", "family", "scope", "operation", "member", "relevant", "horizon"})
        pair = _pair(act)
        operation, member = act.get("operation"), act.get("member")
        if operation not in {"add", "value_correction", "predicate_change", "remove"}:
            raise Reject("unknown member operation")
        if not isinstance(member, str) or not member:
            raise Reject("member must be a nonempty string")
        key = pair, member
        was_present = key in state.members
        relevant = act.get("relevant")
        horizon = act.get("horizon")
        needs_horizon = operation != "value_correction"
        if needs_horizon != isinstance(horizon, Mapping):
            raise Reject("membership-changing transition requires exactly one horizon successor")
        if pair not in state.current_horizon:
            raise Reject("member change needs an open family")
        previous = state.current_horizon[pair]
        if isinstance(horizon, Mapping):
            # Validate the whole successor before changing membership: rejection
            # leaves neither half of this one complete transition in state.
            _validate_horizon(state, pair, horizon, previous)
        if operation == "add":
            if was_present or relevant is not True:
                raise Reject("add requires absent member and relevant=true")
            state.members[key] = True
        elif operation == "value_correction":
            if not was_present or relevant != state.members[key]:
                raise Reject("value correction must preserve existing membership predicate")
        elif operation == "predicate_change":
            if not was_present or not isinstance(relevant, bool) or relevant == state.members[key]:
                raise Reject("predicate change must change an existing boolean predicate")
            state.members[key] = relevant
        else:  # remove
            if not was_present or relevant is not None:
                raise Reject("remove requires existing member and no relevance value")
            del state.members[key]
        if isinstance(horizon, Mapping):
            _new_horizon(state, pair, horizon, previous)
        return

    if kind == "closure_attested":
        _only(act, {"kind", "id", "family", "scope", "horizon", "value"})
        pair = _pair(act)
        finding, horizon = act.get("id"), act.get("horizon")
        if not isinstance(finding, str) or finding in state.closure_findings:
            raise Reject("closure finding id must be new")
        if act.get("value") is not True:
            raise Reject("only literal true is affirmative closure")
        if state.current_horizon.get(pair) != horizon:
            raise Reject("closure must name the current, family-scoped horizon")
        state.closure_findings[finding] = f"C@{horizon}"
        return

    if kind == "run_zero":
        _only(act, {"kind", "id", "closure"})
        zero, closure = act.get("id"), act.get("closure")
        if not isinstance(zero, str) or zero in state.zeroes or closure not in state.closure_findings:
            raise Reject("zero needs a new id and an asserted closure")
        fact = state.closure_facts[state.closure_findings[closure]]
        if state.current_horizon.get(fact[0]) != fact[1]:
            raise Reject("cannot run against a stale closure fact")
        if any(member_pair == fact[0] and relevant for (member_pair, _), relevant in state.members.items()):
            raise Reject("current relevant member blocks empty-source zero")
        state.zeroes[zero] = closure
        return

    if kind == "derived_closure":
        raise Reject("closure authority must be asserted, never derived")
    raise Reject("unknown act kind")


def _edges(state: State) -> Edges:
    edges: Edges = {"individuation": {}, "derivation": {}}
    for finding, fact_id in state.closure_findings.items():
        _, horizon = state.closure_facts[fact_id]
        edges["individuation"].setdefault(horizon, set()).add(finding)
    for zero, closure in state.zeroes.items():
        edges["derivation"].setdefault(closure, set()).add(zero)
    return edges


def currency(state: State) -> Currency:
    """Derive currency from recorded successor roots and the two edge maps only."""
    edges = _edges(state)
    roots = set(state.superseded_horizons)
    displaced = set(roots)
    reasons: dict[str, list[tuple[str, str]]] = {}
    queue: deque[str] = deque(sorted(roots))
    while queue:
        source = queue.popleft()
        for edge_kind in ("individuation", "derivation"):
            for target in sorted(edges[edge_kind].get(source, set())):
                reasons.setdefault(target, []).append((edge_kind, source))
                if target not in displaced:
                    displaced.add(target)
                    queue.append(target)
    citizens = set(state.closure_findings) | set(state.zeroes)
    frozen_edges = {
        kind: {source: frozenset(targets) for source, targets in sources.items()}
        for kind, sources in edges.items()
    }
    return Currency(
        current=frozenset(citizens - displaced),
        displaced=frozenset(citizens & displaced),
        roots=frozenset(roots),
        edges=frozen_edges,
        reasons={target: tuple(value) for target, value in reasons.items()},
    )


def rebuild(acts: Iterable[Mapping[str, Any]]) -> State:
    state = State()
    for act in acts:
        apply(state, act)
    return state


def replay_check(acts: Iterable[Mapping[str, Any]]) -> list[Currency]:
    """After each accepted act, prove incremental currency equals full replay."""
    log = list(acts)
    incremental = State()
    result: list[Currency] = []
    for position, act in enumerate(log, start=1):
        apply(incremental, act)
        incremental_view = currency(incremental)
        rebuilt_view = currency(rebuild(log[:position]))
        if incremental_view != rebuilt_view:
            raise AssertionError(f"incremental/rebuild divergence at act {position}")
        result.append(incremental_view)
    return result
