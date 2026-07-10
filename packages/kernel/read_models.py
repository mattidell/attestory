"""Derived read models for workspace inspection.

These projections are convenience views over the append-only act log.
They are discardable: rebuilding from committed acts must produce the
same bytes, and no read model is an authority source.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from packages.kernel.currency import compute_currency
from packages.kernel.facts import Fact, facts_of
from packages.kernel.findings import evidentiary_standing, project
from packages.kernel.schema_registry import SchemaRegistry


def _fact_to_json(fact: Fact, current_finding_id: str | None) -> dict[str, Any]:
    return {
        "fact_id": fact.fact_id,
        "fact_type_id": fact.fact_type_id,
        "nature": fact.nature,
        "keys": [
            {"name": name, "value": value}
            for name, value in fact.keys
        ],
        "individuated_by": list(fact.individuated_by),
        "current_finding_id": current_finding_id,
    }


def build_read_model(
    acts: tuple[dict[str, Any], ...],
    registry: SchemaRegistry,
) -> dict[str, Any]:
    """Build all Track 6 read views from committed acts."""
    state = project(acts, registry)
    currency = compute_currency(state)
    lattice = facts_of(state.fact_state)

    current_by_fact: dict[str, str] = {}
    history: dict[str, list[dict[str, Any]]] = {}
    for finding_id, finding in state.findings.items():
        is_current = finding_id in currency.current_finding_ids
        if is_current:
            current_by_fact[finding["fact_id"]] = finding_id
        history.setdefault(finding["fact_id"], []).append(
            {
                "finding_id": finding_id,
                "current": is_current,
                "basis": finding["basis"],
                "evidence_ids": list(finding["evidence_ids"]),
            }
        )

    standing = evidentiary_standing(state)
    current_findings = {
        finding_id: {
            "finding": standing[finding_id].finding,
            "evidence": [
                {
                    "evidence_id": ref.evidence_id,
                    "status": ref.status,
                    "successor_id": ref.successor_id,
                }
                for ref in standing[finding_id].evidence
            ],
        }
        for finding_id in sorted(currency.current_finding_ids)
    }

    facts = {
        fact_id: _fact_to_json(fact, current_by_fact.get(fact_id))
        for fact_id, fact in sorted(lattice.items())
    }

    open_fact_ids = [
        fact_id
        for fact_id in sorted(lattice)
        if fact_id not in current_by_fact
    ]

    return {
        "revision": len(acts),
        "current": {
            "finding_ids": sorted(currency.current_finding_ids),
            "evidence_ids": sorted(currency.current_evidence_ids),
            "findings": current_findings,
        },
        "facts": facts,
        "history_by_fact": {
            fact_id: entries for fact_id, entries in sorted(history.items())
        },
        "open_fact_ids": open_fact_ids,
    }


def current_state(
    acts: tuple[dict[str, Any], ...],
    registry: SchemaRegistry,
) -> dict[str, Any]:
    result = build_read_model(acts, registry)["current"]
    if not isinstance(result, dict):
        raise TypeError("current projection is not an object")
    return cast(dict[str, Any], result)


def fact_history(
    acts: tuple[dict[str, Any], ...],
    registry: SchemaRegistry,
) -> dict[str, Any]:
    result = build_read_model(acts, registry)["history_by_fact"]
    if not isinstance(result, dict):
        raise TypeError("history_by_fact projection is not an object")
    return cast(dict[str, Any], result)


def open_facts(
    acts: tuple[dict[str, Any], ...],
    registry: SchemaRegistry,
) -> list[str]:
    result = build_read_model(acts, registry)["open_fact_ids"]
    if not isinstance(result, list):
        raise TypeError("open_fact_ids projection is not a list")
    return [str(fact_id) for fact_id in result]


def write_projection(path: Path, projection: dict[str, Any]) -> None:
    """Write a deterministic cache file for containment-drill tests."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(projection, indent=2, sort_keys=True) + "\n",
        "utf-8",
    )


def read_projection(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("projection cache must contain a JSON object")
    return payload
