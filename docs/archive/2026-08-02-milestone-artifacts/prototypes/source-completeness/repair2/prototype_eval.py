"""Rung-3 throwaway evaluator for SC-P1 end-to-end sole-writer enforcement.

PROTOTYPE ONLY (charter-repair2). A faithful COPY of the production two-layer
``collect`` check + aggregate + pin-building, wired ONLY to repair1's resolver
carrier. Imports nothing from ``packages/`` and never executes the production
runner/evaluator — it copies their behavior so the copy can be attacked.

Faithful-copy provenance (grounding only, not imported):
  * two-layer ``collect``   <- evaluator.py:107-119
  * ``add`` fold            <- evaluator.py:134
  * pin building            <- runner.py:143-154 (``pins_for``)

Declared deviations from production (charter check 1):
  1. The ``round``/rounding.convention wrapper is omitted; rounding never gates
     layer 2, so the collect result is summed directly. Immaterial to closure.
  2. Adoption/governance pins are omitted; they are not part of the closure
     question. Rule, member-input, and closure-authority pins are modeled.
  3. Closed membership is NOT a settable ``frozenset[str]`` field (production
     ``env.closed_sets``). It is DERIVED from a repair1 ``ResolvedMembership``.
     This is the design change under test — the sole-writer property — marked
     explicitly at ``Env.closed_families``.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field, fields
from decimal import Decimal

# Wire to repair1's resolver as the SOLE authority carrier (not re-implemented).
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "repair1")
)
import resolver  # noqa: E402  (repair1 module)

BLOCK_CLOSURE = "SOURCE_SET_NOT_CLOSED"  # mirrors evaluator.py BLOCK_CLOSURE


class EvalBlocked(Exception):
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class Pin:
    role: str
    id: str
    version: str


@dataclass(frozen=True)
class Env:
    """Everything a collect may read. Deliberately has NO ``closed_sets`` field:
    layer-2 membership is derived from ``resolved`` and cannot be caller-set."""

    # member fact name -> list of (decimal-string value, finding_id)
    sources: dict
    resolved: "resolver.ResolvedMembership"  # SOLE source of L2 membership

    @property
    def closed_families(self) -> frozenset:
        return resolver.env_closed_sets(self.resolved)


@dataclass
class Access:
    collects: set = field(default_factory=set)
    # repair1 explanation-defect fix: source_set -> ClosureAuthority (or None)
    closure_admits: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Publication:
    symbol: str
    value: Decimal
    pins: tuple


def _as_decimal(v) -> Decimal:
    if isinstance(v, bool):
        raise EvalBlocked("INVALID", [f"boolean {v}"])
    return Decimal(str(v))


def collect(node, env: Env, access: Access):
    """Faithful copy of evaluator.py:107-119. Layer 1: present members return
    their decimals (closure never consulted). Layer 2: an empty set is zero
    only if the declared ``source_set`` is in resolved membership; else block."""
    name = node["name"]
    access.collects.add(name)
    rows = env.sources.get(name, [])
    if not rows:
        source_set = node.get("source_set")
        members = env.closed_families                 # <- resolved, not caller
        if source_set is None or source_set not in members:
            raise EvalBlocked(BLOCK_CLOSURE, [source_set or name])
        # design addition: retain the exact admitting authority for pins
        access.closure_admits[source_set] = env.resolved.pin_for(source_set)
        return []
    return [_as_decimal(v) for (v, _fid) in rows]


def build_pins(rule, env: Env, access: Access) -> tuple:
    """Copy of pins_for's rule + collect-input pins, plus the repair1 closure
    pin. An empty-source zero pins the exact closure finding + its artifact; a
    present-member aggregate pins members only (no closure pin — it never ran)."""
    pins = [Pin("field-mapping", rule["id"], rule["version"])]
    for name in sorted(access.collects):
        for (_v, fid) in env.sources.get(name, []):
            pins.append(Pin("input", fid, "v1"))
    for source_set in sorted(access.closure_admits):
        auth = access.closure_admits[source_set]
        pins.append(Pin("closure-authority", auth.finding_id, auth.finding_version))
        pins.append(Pin(auth.artifact_role, auth.artifact_id, auth.artifact_version))
    return tuple(pins)


def run_rule(rule, env: Env) -> Publication:
    """collect -> sum -> publish. Raises EvalBlocked (no publication) if L2
    blocks. ``rule['value']`` is the collect node (round wrapper omitted)."""
    access = Access()
    values = collect(rule["value"], env, access)
    total = sum(values, Decimal(0))
    return Publication(rule["publishes"], total, build_pins(rule, env, access))


# ---------------------------------------------------------------------------
# End-to-end mutant: the caller-union smuggle that check 2 forbids
# ---------------------------------------------------------------------------

def run_rule_caller_union(rule, env: Env, caller_extra) -> Publication:
    """MUTANT: an alternate path that unions a caller-supplied family set into
    layer-2 membership. Must be killed by the injection case — it publishes a
    zero for a family that has NO resolved authority, where the faithful path
    blocks. (Its injected zero also carries no closure pin: unexplainable.)"""
    node = rule["value"]
    name = node["name"]
    rows = env.sources.get(name, [])
    if rows:
        return Publication(
            rule["publishes"],
            sum((_as_decimal(v) for (v, _f) in rows), Decimal(0)),
            (),
        )
    source_set = node.get("source_set")
    members = env.closed_families | frozenset(caller_extra)   # the smuggle
    if source_set is None or source_set not in members:
        raise EvalBlocked(BLOCK_CLOSURE, [source_set or name])
    return Publication(rule["publishes"], Decimal(0), ())     # injected zero


def env_field_names():
    """Helper for the 'no caller closed-set field' assertion."""
    return [f.name for f in fields(Env)]
