"""Per-pairing rule dispatch driven by runtime pairing findings.

ADR-0070 Decision 2 and ADR-0071 Decision 2: a rule that must fire once per
ADR-0068 pairing finding cannot use ordinary ``attempt()`` (once per rule
id) and cannot use ``_evaluate_family_validation`` (static declared family,
no dereference of a fact id stored inside another finding's value).

This module is the production primitive both seams share. It iterates the
pairing ``SourceFact``s a run actually has (via ``collect_source_names`` /
marshal), resolves each peer by the pairing's pinned ``right_fact_id`` (and
the acquisition by ``left_fact_id``), and publishes exactly one finding per
pairing per rule id — never two in one loop iteration.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from packages.derivation.evaluator import EvalBlocked
from packages.derivation.loader import DerivationSchemas
from packages.derivation.runner import SourceFact, _content_id, _sorted_pins

DEPENDENCY_ABSENT = "DEPENDENCY_ABSENT"
DEPENDENCY_INVALID = "DEPENDENCY_INVALID"


@dataclass(frozen=True)
class PairingBinding:
    """One runtime pairing with both sides resolved by pinned fact id."""

    pairing: SourceFact
    pairing_value: dict[str, Any]
    left: SourceFact
    right: SourceFact
    left_value: Any
    right_value: Any

    @property
    def pairing_fact_id(self) -> str:
        return self.pairing.fact_id or self.pairing.finding_id

    @property
    def left_fact_id(self) -> str:
        return str(self.pairing_value["left_fact_id"])

    @property
    def right_fact_id(self) -> str:
        return str(self.pairing_value["right_fact_id"])


@dataclass(frozen=True)
class PairingPublish:
    """Evaluate-one outcome: publish this value as the pairing's finding."""

    value: Any
    extra_pins: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class PairingBlock:
    """Evaluate-one outcome: this pairing blocks; others still dispatch."""

    code: str
    missing: tuple[str, ...] = ()
    extra_pins: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class PairingScopedBlocked:
    pairing_fact_id: str
    code: str
    missing: tuple[str, ...]
    pins: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class PairingScopedResult:
    publications: tuple[dict[str, Any], ...]
    blocked: tuple[PairingScopedBlocked, ...]


def _decode(raw: Any) -> Any:
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    return raw


def _index_by_fact_id(sources: Sequence[SourceFact], type_name: str) -> dict[str, SourceFact]:
    """Index current sources of one type by identity-bearing fact id.

    Two current facts of the same type both appear; only the id a pairing
    actually names is ever looked up. This is the masking-prevention
    property ADR-0070 Decision 3 depends on.
    """
    return {s.fact_id: s for s in sources if s.name == type_name and s.fact_id}


def _input_pin(finding_id: str) -> dict[str, Any]:
    return {"role": "input", "id": finding_id, "version": "v1", "origin": "assertion"}


def evaluate_pairing_scoped_rule(
    *,
    sources: Sequence[SourceFact],
    pairing_type: str,
    left_type: str,
    right_type: str,
    rule_id: str,
    rule_version: str,
    rule_role: str = "computation",
    symbol_for: Callable[[PairingBinding], str],
    evaluate_one: Callable[[PairingBinding], PairingPublish | PairingBlock],
    extra_pins: Sequence[Mapping[str, Any]] = (),
    schemas: DerivationSchemas,
) -> PairingScopedResult:
    """Evaluate one rule once per current pairing finding.

    Driven by the runtime pairing sources a run actually has, not a static
    declared family. Resolves the acquisition and the peer by the pairing's
    own ``left_fact_id`` / ``right_fact_id``, never by a fact type's generic
    current binding. Appends at most one publication (or one blocked row)
    per pairing — never two in one iteration.
    """
    pairing_sources = [s for s in sources if s.name == pairing_type]
    left_by_fact_id = _index_by_fact_id(sources, left_type)
    right_by_fact_id = _index_by_fact_id(sources, right_type)
    rule_pin = {"role": rule_role, "id": rule_id, "version": rule_version}
    shared_pins = [dict(rule_pin), *(dict(p) for p in extra_pins)]

    publications: list[dict[str, Any]] = []
    blocked: list[PairingScopedBlocked] = []

    for pairing in pairing_sources:
        pairing_fact_id = pairing.fact_id or pairing.finding_id
        pairing_pin = _input_pin(pairing.finding_id)
        decoded = _decode(pairing.value)
        if not isinstance(decoded, dict):
            blocked.append(PairingScopedBlocked(
                pairing_fact_id=pairing_fact_id,
                code=DEPENDENCY_INVALID,
                missing=(pairing_fact_id,),
                pins=tuple(_sorted_pins([*shared_pins, pairing_pin])),
            ))
            continue

        left_fact_id = decoded.get("left_fact_id")
        right_fact_id = decoded.get("right_fact_id")
        if not isinstance(left_fact_id, str) or not isinstance(right_fact_id, str):
            blocked.append(PairingScopedBlocked(
                pairing_fact_id=pairing_fact_id,
                code=DEPENDENCY_INVALID,
                missing=(pairing_fact_id,),
                pins=tuple(_sorted_pins([*shared_pins, pairing_pin])),
            ))
            continue

        left = left_by_fact_id.get(left_fact_id)
        right = right_by_fact_id.get(right_fact_id)
        present_pins = [*shared_pins, pairing_pin]
        missing: list[str] = []
        if left is None:
            missing.append(left_fact_id)
        else:
            present_pins.append(_input_pin(left.finding_id))
        if right is None:
            missing.append(right_fact_id)
        else:
            present_pins.append(_input_pin(right.finding_id))
        if missing:
            blocked.append(PairingScopedBlocked(
                pairing_fact_id=pairing_fact_id,
                code=DEPENDENCY_ABSENT,
                missing=tuple(missing),
                pins=tuple(_sorted_pins(present_pins)),
            ))
            continue

        assert left is not None and right is not None  # missing check above exits first
        binding = PairingBinding(
            pairing=pairing,
            pairing_value=decoded,
            left=left,
            right=right,
            left_value=_decode(left.value),
            right_value=_decode(right.value),
        )
        try:
            outcome = evaluate_one(binding)
        except EvalBlocked as exc:
            blocked.append(PairingScopedBlocked(
                pairing_fact_id=pairing_fact_id,
                code=exc.category,
                missing=tuple(exc.missing),
                pins=tuple(_sorted_pins(present_pins)),
            ))
            continue

        if isinstance(outcome, PairingBlock):
            blocked.append(PairingScopedBlocked(
                pairing_fact_id=pairing_fact_id,
                code=outcome.code,
                missing=outcome.missing,
                pins=tuple(_sorted_pins([*present_pins, *outcome.extra_pins])),
            ))
            continue
        if not isinstance(outcome, PairingPublish):
            raise TypeError(
                f"evaluate_one must return PairingPublish or PairingBlock, "
                f"got {type(outcome)!r}"
            )

        pins = _sorted_pins([*present_pins, *outcome.extra_pins])
        symbol = symbol_for(binding)
        body = {"symbol": symbol, "value": outcome.value, "pins": pins}
        finding = {
            "schema": "derived-finding.v2",
            "id": _content_id("finding:derived:", body),
            "symbol": symbol,
            "value": outcome.value,
            "version": "v2",
            "pins": pins,
        }
        schemas.validate_declared(finding)
        # Exactly one append per pairing per rule id.
        publications.append(finding)

    return PairingScopedResult(
        publications=tuple(publications),
        blocked=tuple(blocked),
    )
