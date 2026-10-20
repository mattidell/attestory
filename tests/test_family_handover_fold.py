"""Focused kernel tests for family-version handover pure fold (Increment 1).

Covers:
- Admitted handover: retired predecessor chain key, active successor chain key,
  predecessor horizon citizen linked via cross-version predecessor, superseded
  entities and currency displacement of closure facts while retaining statements.
- Each atomic refusal: scope mismatch, identical version, family id mismatch,
  stale predecessor (wrong id or superseded), predecessor entity not current,
  ambiguous active authority (both-current), target already exists, reverse
  handover (target retired), reused successor horizon ID (in horizons or entities).
- Retired-chain refusals: genesis and member-transition on a retired chain key.
- Same-member correction after handover: ordinary assertion on retained statement
  updates statement value without touching successor horizon or resurrecting closure.
- Historical two-genesis log: projects cleanly on replay without raising.
"""

import dataclasses
from typing import Any
import pytest

from packages.kernel import facts, findings, horizons
from packages.kernel.currency import compute_currency
from packages.kernel.findings import FindingState, apply_act, project
from packages.kernel.horizons import HorizonModelError, chain_key
from packages.kernel.schema_registry import SchemaRegistry

STATEMENT_FACT_TYPE: dict[str, Any] = {
    "schema": "fact-type.v1",
    "id": "demo.statement.amount",
    "title": "Demo statement amount",
    "nature": "determinable",
    "identity_keys": [
        {"name": "payer", "kind": "literal", "values": ["p1", "p2"]},
        {"name": "statement", "kind": "literal", "values": ["s1", "s2"]},
        {"name": "year", "kind": "literal", "values": ["2025"]},
    ],
    "value_schema": {"type": "number"},
    "supersession": {"policy": "free"},
}

CLOSURE_FACT_TYPE: dict[str, Any] = {
    "schema": "fact-type.v1",
    "id": "demo.family.closure",
    "title": "Demo family closure",
    "nature": "determinable",
    "identity_keys": [
        {
            "name": "family-horizon",
            "kind": "entity",
            "entity_kind": "kernel.family-horizon",
        },
        {"name": "year", "kind": "literal", "values": ["2025"]},
    ],
    "value_schema": {"type": "boolean"},
    "supersession": {"policy": "free"},
}

FAMILY_V1 = {"id": "demo.sales", "version": "v1"}
FAMILY_V2 = {"id": "demo.sales", "version": "v2"}
FAMILY_V3 = {"id": "demo.sales", "version": "v3"}
SCOPE = {"subject": "s1"}


def make_act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"act-{index:03d}",
        "kind": kind,
        "actor": "user",
        "at": f"2026-10-19T10:{index:02d}:00Z",
        "committed_against": index,
        "payload": payload,
    }


def make_finding(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def setup_base_state(registry: SchemaRegistry) -> tuple[FindingState, tuple[dict[str, Any], ...]]:
    acts = (
        make_act(
            0,
            "bundle-adoption",
            {
                "bundle": {
                    "schema": "bundle.v1",
                    "id": "demo.bundle",
                    "label": "Demo bundle",
                    "fact_types": [STATEMENT_FACT_TYPE, CLOSURE_FACT_TYPE],
                }
            },
        ),
        make_act(
            1,
            "horizon-genesis",
            {"family": FAMILY_V1, "scope": SCOPE, "horizon_id": "demo.sales.v1.h0"},
        ),
        make_act(
            2,
            "assertion",
            {
                "finding": make_finding(
                    "finding-stmt-1",
                    "demo.statement.amount|payer=p1,statement=s1,year=2025",
                    1000,
                )
            },
        ),
        make_act(
            3,
            "assertion",
            {
                "finding": make_finding(
                    "finding-closure-v1",
                    "demo.family.closure|family-horizon=demo.sales.v1.h0,year=2025",
                    True,
                )
            },
        ),
    )
    state = project(acts, registry)
    return state, acts


def test_admitted_handover() -> None:
    registry = SchemaRegistry()
    state, base_acts = setup_base_state(registry)

    # Pre-handover assertions
    curr_before = compute_currency(state)
    assert "finding-stmt-1" in curr_before.current_finding_ids
    assert "finding-closure-v1" in curr_before.current_finding_ids
    assert state.horizon_state.current_by_chain[chain_key(FAMILY_V1, SCOPE)] == "demo.sales.v1.h0"
    assert chain_key(FAMILY_V1, SCOPE) not in state.horizon_state.retired_chains

    handover_act = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
        },
    )
    new_state = apply_act(state, handover_act, registry)

    # 1. Active chains updated: predecessor removed, successor added
    assert chain_key(FAMILY_V1, SCOPE) not in new_state.horizon_state.current_by_chain
    assert new_state.horizon_state.current_by_chain[chain_key(FAMILY_V2, SCOPE)] == "demo.sales.v2.h0"

    # 2. Remembered retirement recorded
    assert chain_key(FAMILY_V1, SCOPE) in new_state.horizon_state.retired_chains

    # 3. Horizon lifecycle updated
    pred_hl = new_state.horizon_state.horizons["demo.sales.v1.h0"]
    assert pred_hl.status == "superseded"
    assert pred_hl.successor_id == "demo.sales.v2.h0"
    succ_hl = new_state.horizon_state.horizons["demo.sales.v2.h0"]
    assert succ_hl.status == "current"
    assert succ_hl.horizon["predecessor"] == "demo.sales.v1.h0"

    # 4. Fact state entities updated
    pred_ent = new_state.fact_state.entities["demo.sales.v1.h0"]
    assert pred_ent.status == "superseded"
    assert pred_ent.successor_id == "demo.sales.v2.h0"
    succ_ent = new_state.fact_state.entities["demo.sales.v2.h0"]
    assert succ_ent.status == "current"

    # 5. Currency cascade: closure dropped, statement preserved
    curr_after = compute_currency(new_state)
    assert "finding-stmt-1" in curr_after.current_finding_ids
    assert "finding-closure-v1" in curr_after.displaced_finding_ids


def test_refusal_scope_mismatch() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    act = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": {"subject": "s1"},
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": {"subject": "s2"},
                "horizon_id": "demo.sales.v2.h0",
            },
        },
    )
    with pytest.raises(HorizonModelError, match="malformed handover payload"):
        apply_act(state, act, registry)


def test_refusal_identical_version() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    act = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h1",
            },
        },
    )
    with pytest.raises(HorizonModelError, match="malformed handover payload"):
        apply_act(state, act, registry)


def test_refusal_family_id_mismatch() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    act = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": {"id": "demo.other", "version": "v2"},
                "scope": SCOPE,
                "horizon_id": "demo.other.v2.h0",
            },
        },
    )
    with pytest.raises(HorizonModelError, match="malformed handover payload"):
        apply_act(state, act, registry)


def test_refusal_stale_predecessor_wrong_id() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    act = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.nonexistent",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
        },
    )
    with pytest.raises(HorizonModelError, match="predecessor horizon is not current"):
        apply_act(state, act, registry)


def test_refusal_stale_predecessor_superseded() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    handover1 = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
        },
    )
    state = apply_act(state, handover1, registry)

    # Attempting to handover from superseded v1.h0 to v3
    handover_stale = make_act(
        5,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V3,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v3.h0",
            },
        },
    )
    with pytest.raises(HorizonModelError, match="predecessor horizon is not current"):
        apply_act(state, handover_stale, registry)


def test_refusal_predecessor_entity_not_current() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    # Manually tamper fact_state.entities to mark predecessor entity superseded
    tampered_entities = dict(state.fact_state.entities)
    tampered_entities["demo.sales.v1.h0"] = facts.EntityLifecycle(
        entity=tampered_entities["demo.sales.v1.h0"].entity,
        status="superseded",
        successor_id="something",
    )
    tampered_state = dataclasses.replace(
        state,
        fact_state=dataclasses.replace(state.fact_state, entities=tampered_entities),
    )
    act = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
        },
    )
    with pytest.raises(HorizonModelError, match="predecessor horizon is not current"):
        apply_act(tampered_state, act, registry)


def test_refusal_ambiguous_authority_both_current() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    # Inject second current chain for same family and scope (both-current log)
    genesis_v2 = make_act(
        4,
        "horizon-genesis",
        {"family": FAMILY_V2, "scope": SCOPE, "horizon_id": "demo.sales.v2.h0"},
    )
    both_current_state = apply_act(state, genesis_v2, registry)

    # Attempting handover when multiple chains are current for this family/scope
    handover = make_act(
        5,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V3,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v3.h0",
            },
        },
    )
    with pytest.raises(
        HorizonModelError,
        match="successor chain already exists or ambiguous active authority",
    ):
        apply_act(both_current_state, handover, registry)


def test_refusal_target_already_exists() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    genesis_v2 = make_act(
        4,
        "horizon-genesis",
        {"family": FAMILY_V2, "scope": SCOPE, "horizon_id": "demo.sales.v2.h0"},
    )
    both_current_state = apply_act(state, genesis_v2, registry)

    # Attempting handover to a version that already has an active chain
    handover = make_act(
        5,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h1",
            },
        },
    )
    with pytest.raises(
        HorizonModelError,
        match="successor chain already exists or ambiguous active authority",
    ):
        apply_act(both_current_state, handover, registry)


def test_refusal_reverse_handover_downgrade() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    handover_forward = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
        },
    )
    state = apply_act(state, handover_forward, registry)

    # Reverse handover: v2 -> v1 (v1 is retired)
    handover_reverse = make_act(
        5,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
            "successor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h1",
            },
        },
    )
    with pytest.raises(HorizonModelError, match="successor chain is retired"):
        apply_act(state, handover_reverse, registry)


def test_refusal_reused_successor_horizon_id() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    # Successor horizon id is already in state.horizons / state.fact_state.entities
    act = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",  # reused id
            },
        },
    )
    with pytest.raises(HorizonModelError, match="horizon id already recorded"):
        apply_act(state, act, registry)


def test_refusal_genesis_on_retired_chain() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    handover = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
        },
    )
    state = apply_act(state, handover, registry)

    # Genesis on retired v1 chain
    genesis_v1 = make_act(
        5,
        "horizon-genesis",
        {"family": FAMILY_V1, "scope": SCOPE, "horizon_id": "demo.sales.v1.h1"},
    )
    with pytest.raises(HorizonModelError, match="family version is retired"):
        apply_act(state, genesis_v1, registry)


def test_refusal_transition_on_retired_chain() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    handover = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
        },
    )
    state = apply_act(state, handover, registry)

    # Member transition naming retired v1
    transition_v1 = make_act(
        5,
        "member-transition",
        {
            "family": FAMILY_V1,
            "scope": SCOPE,
            "member": {
                "action": "assert",
                "finding": make_finding(
                    "finding-stmt-2",
                    "demo.statement.amount|payer=p2,statement=s2,year=2025",
                    2000,
                ),
            },
            "successor": {
                "id": "demo.sales.v1.h1",
                "predecessor": "demo.sales.v1.h0",
            },
        },
    )
    with pytest.raises(HorizonModelError, match="family version is retired"):
        apply_act(state, transition_v1, registry)


def test_same_member_correction_after_handover() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    handover = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
        },
    )
    state = apply_act(state, handover, registry)

    # Ordinary assertion updating the same statement fact value (Case 1 in proposal)
    correction = make_act(
        5,
        "assertion",
        {
            "finding": make_finding(
                "finding-stmt-1-corr",
                "demo.statement.amount|payer=p1,statement=s1,year=2025",
                1500,
            )
        },
    )
    state = apply_act(state, correction, registry)

    curr = compute_currency(state)
    assert "finding-stmt-1-corr" in curr.current_finding_ids
    assert "finding-stmt-1" in curr.displaced_finding_ids
    assert "finding-closure-v1" in curr.displaced_finding_ids
    assert state.horizon_state.horizons["demo.sales.v2.h0"].status == "current"


def test_chained_handover_v1_to_v2_to_v3() -> None:
    registry = SchemaRegistry()
    state, _ = setup_base_state(registry)
    handover1 = make_act(
        4,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V1,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v1.h0",
            },
            "successor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
        },
    )
    state = apply_act(state, handover1, registry)

    handover2 = make_act(
        5,
        "family-handover",
        {
            "predecessor": {
                "family": FAMILY_V2,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v2.h0",
            },
            "successor": {
                "family": FAMILY_V3,
                "scope": SCOPE,
                "horizon_id": "demo.sales.v3.h0",
            },
        },
    )
    state = apply_act(state, handover2, registry)

    # Both v1 and v2 retired; v3 current
    assert chain_key(FAMILY_V1, SCOPE) in state.horizon_state.retired_chains
    assert chain_key(FAMILY_V2, SCOPE) in state.horizon_state.retired_chains
    assert state.horizon_state.current_by_chain[chain_key(FAMILY_V3, SCOPE)] == "demo.sales.v3.h0"
    assert state.horizon_state.horizons["demo.sales.v3.h0"].horizon["predecessor"] == "demo.sales.v2.h0"


def test_historical_two_genesis_log_projects() -> None:
    """Historical log with two genesis acts must project without error on replay."""
    registry = SchemaRegistry()
    acts = (
        make_act(
            0,
            "bundle-adoption",
            {
                "bundle": {
                    "schema": "bundle.v1",
                    "id": "demo.bundle",
                    "label": "Demo bundle",
                    "fact_types": [STATEMENT_FACT_TYPE, CLOSURE_FACT_TYPE],
                }
            },
        ),
        make_act(
            1,
            "horizon-genesis",
            {"family": FAMILY_V1, "scope": SCOPE, "horizon_id": "demo.sales.v1.h0"},
        ),
        make_act(
            2,
            "horizon-genesis",
            {"family": FAMILY_V2, "scope": SCOPE, "horizon_id": "demo.sales.v2.h0"},
        ),
    )
    state = project(acts, registry)
    # Replay admitted both genesis acts into current_by_chain
    assert state.horizon_state.current_by_chain[chain_key(FAMILY_V1, SCOPE)] == "demo.sales.v1.h0"
    assert state.horizon_state.current_by_chain[chain_key(FAMILY_V2, SCOPE)] == "demo.sales.v2.h0"
