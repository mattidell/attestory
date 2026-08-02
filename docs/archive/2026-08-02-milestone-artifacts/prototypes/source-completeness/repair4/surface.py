"""Repair pass 4: the single evaluation entry for SC-P1 shape A.

PROTOTYPE ONLY (charter-repair4). A self-contained *selected runtime surface*.
Its public API is exactly one function — ``compute`` — which takes the declared
inputs (rule, source rows, adopted shape-A mapping, closure findings), resolves
and validates authority **internally as one operation**, and then runs a faithful
copy of the production two-layer ``collect``. It accepts no external authority
carrier, closed-family set, raw environment, validator callback, or alternate
evaluator, and re-exports none.

Round-3 finding (reviews/round-3-adversary.md): repair3 *validated* carriers but
still exposed alternate callables (`run_rule_with_carrier`, `run_rule_trusting`,
the raw `Env`/evaluator) and accepted any duck-typed object with the carrier
methods. This pass removes every entry but one, so there is nowhere to hand in a
fabricated, duck-typed, duplicate, or stale authority.

**Not a security boundary.** Python privacy is a convention, not enforcement. The
contract this models is that the production surface *exposes and dispatches only*
this validated entry; the underscore-privates below are the internal steps of
that single operation, not alternate public paths. The tests reach into them
deliberately to show why they stay private — that is a test, not an API.

Faithful-copy provenance (grounding only, never imported from packages/):
two-layer ``collect`` <- evaluator.py:107-119; ``add`` fold <- evaluator.py:134;
pins <- runner.py:143-154. Same declared deviations as repair2 (round wrapper and
adoption/governance pins omitted; membership derived, never caller-set).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass as _dataclass
from decimal import Decimal as _Decimal

# Private import of repair1's shape-A resolution core. Underscore-aliased so it
# is not part of this module's public surface and cannot be reached as
# ``surface.resolver`` by a caller of this module.
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "repair1")
)
import resolver as _resolver  # noqa: E402

__all__ = ["compute"]

_BLOCK_CLOSURE = "SOURCE_SET_NOT_CLOSED"  # mirrors evaluator.py BLOCK_CLOSURE


class Blocked(Exception):
    """Raised when the two-layer check blocks; no publication occurs."""

    def __init__(self, detail):
        self.detail = detail
        super().__init__(f"{_BLOCK_CLOSURE}: {detail}")


@_dataclass(frozen=True)
class Pin:
    role: str
    id: str
    version: str


@_dataclass(frozen=True)
class Publication:
    symbol: str
    value: _Decimal
    pins: tuple


def _as_decimal(v) -> _Decimal:
    if isinstance(v, bool):
        raise Blocked([f"boolean {v}"])
    return _Decimal(str(v))


def _resolve_authority(mapping, findings) -> dict:
    """Internal shape-A resolution + validation as one step. ``resolve_A``
    already blocks duplicate mapping entries and admits only a current literal-
    true finding; keying by family guarantees one authority per family. There is
    no external carrier to fabricate — authority exists only as this output."""
    resolved = _resolver.resolve_A(mapping, findings)
    return {a.source_family: a for a in resolved.authority}


def _collect(node, source_rows, admitted, access):
    """Faithful copy of evaluator.py:107-119. Layer 1: present rows return their
    decimals (closure never consulted). Layer 2: an empty set is zero only if the
    declared ``source_set`` is in internally-resolved membership."""
    name = node["name"]
    access["collects"].add(name)
    rows = source_rows.get(name, [])
    if not rows:
        source_set = node.get("source_set")
        if source_set is None or source_set not in admitted:
            raise Blocked([source_set or name])
        access["closure_admits"][source_set] = admitted[source_set]
        return []
    return [_as_decimal(v) for (v, _fid) in rows]


def _pins(rule, source_rows, access) -> tuple:
    pins = [Pin("field-mapping", rule["id"], rule["version"])]
    for name in sorted(access["collects"]):
        for (_v, fid) in source_rows.get(name, []):
            pins.append(Pin("input", fid, "v1"))
    for source_set in sorted(access["closure_admits"]):
        a = access["closure_admits"][source_set]
        pins.append(Pin("closure-authority", a.finding_id, a.finding_version))
        pins.append(Pin(a.artifact_role, a.artifact_id, a.artifact_version))
    return tuple(pins)


def compute(rule, source_rows, mapping, findings) -> Publication:
    """THE one supported calculation entry.

    Parameters are the declared inputs only: ``rule`` (with a collect ``value``
    node), ``source_rows`` (member fact name -> list of (value, finding_id)),
    ``mapping`` (adopted shape-A mapping citizen), ``findings`` (closure findings).
    Authority is derived and consumed internally, immediately before the faithful
    two-layer check. No parameter accepts an authority object, carrier, closed set,
    environment, or evaluator. Raises ``Blocked`` (no publication) when layer 2
    blocks.
    """
    admitted = _resolve_authority(mapping, findings)
    access = {"collects": set(), "closure_admits": {}}
    values = _collect(rule["value"], source_rows, admitted, access)
    total = sum(values, _Decimal(0))
    return Publication(rule["publishes"], total, _pins(rule, source_rows, access))
