"""Focused tests for ActLog pre-persistence save fences and marshal containment (Increment 2).

Exercises:
- ActLog pre-save fold rejects:
  - stale predecessor handover
  - member transition naming a retired family version
  - third-version genesis when an active chain already exists in scope
  - reverse handover (downgrade to retired version)
- ActLog pre-save fold admits chained handover (v1 -> v2 -> v3)
- Old-engine read boundary: SchemaRegistry lacking act-family-handover raises ActLogCorruption on read()
- Historical two-genesis log stays readable via ActLog.read() and projectable via project()
- Marshal containment rule:
  - Refuses closure authority when multiple version chains are current in the same scope (SourceAuthorityError)
  - Admits exact adopted version when exactly one version chain is current (after handover)
  - Refuses when same version has multiple scopes
- Targeted pre-save fold scope: direct closure assertion against retired horizon is saved by ActLog, but fails later at project()
"""

from pathlib import Path
import json
import shutil
import tempfile
from typing import Any
import pytest

from packages.derivation.marshal import marshal_closure_authority
from packages.derivation.source_authority import SourceAuthorityError
from packages.kernel import facts, findings, horizons
from packages.kernel.act_log import ActLog, ActLogCorruption
from packages.kernel.currency import compute_currency
from packages.kernel.findings import FindingModelError, project
from packages.kernel.horizons import HorizonModelError, chain_key
from packages.kernel.schema_registry import (
    KERNEL_SCHEMA_DIR,
    SchemaRegistry,
    SchemaRegistryError,
    write_manifest,
)

STATEMENT_FACT_TYPE: dict[str, Any] = {
    "schema": "fact-type.v1",
    "id": "demo.sales.amount",
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
    "id": "demo.sales.closure",
    "title": "Demo sales closure",
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

BUNDLE: dict[str, Any] = {
    "schema": "bundle.v1",
    "id": "demo.sales.bundle",
    "label": "Demo sales bundle",
    "fact_types": [STATEMENT_FACT_TYPE, CLOSURE_FACT_TYPE],
}

FAMILY_V1 = {"id": "demo.sales", "version": "v1"}
FAMILY_V2 = {"id": "demo.sales", "version": "v2"}
FAMILY_V3 = {"id": "demo.sales", "version": "v3"}
SCOPE = {"subject": "s1"}


def make_act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"act-{index:04d}",
        "kind": kind,
        "actor": "user",
        "at": f"2026-10-19T10:{index % 60:02d}:00Z",
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


def setup_log_with_v1_and_handover(tmp_path: Path, registry: SchemaRegistry) -> tuple[ActLog, Path]:
    ws = tmp_path / "workspace"
    log = ActLog(ws, registry, undeclared_test_log=True)
    log.append(make_act(0, "bundle-adoption", {"bundle": BUNDLE}), expected_revision=0)
    log.append(
        make_act(
            1,
            "horizon-genesis",
            {"family": FAMILY_V1, "scope": SCOPE, "horizon_id": "demo.sales.v1.h0"},
        ),
        expected_revision=1,
    )
    log.append(
        make_act(
            2,
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
        ),
        expected_revision=2,
    )
    return log, ws


def test_actlog_save_stale_predecessor_handover_refused(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    log, _ = setup_log_with_v1_and_handover(tmp_path, registry)

    # Handover naming superseded v1.h0 to v3
    stale_handover = make_act(
        3,
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
        log.append(stale_handover, expected_revision=3)

    # Disk log unmutated
    assert log.read().revision == 3


def test_actlog_save_post_retirement_transition_refused(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    log, _ = setup_log_with_v1_and_handover(tmp_path, registry)

    transition_v1 = make_act(
        3,
        "member-transition",
        {
            "family": FAMILY_V1,
            "scope": SCOPE,
            "member": {
                "action": "assert",
                "finding": make_finding(
                    "f-stmt-1",
                    "demo.sales.amount|payer=p1,statement=s1,year=2025",
                    100,
                ),
            },
            "successor": {
                "id": "demo.sales.v1.h1",
                "predecessor": "demo.sales.v1.h0",
            },
        },
    )
    with pytest.raises(HorizonModelError, match="family version is retired"):
        log.append(transition_v1, expected_revision=3)

    assert log.read().revision == 3


def test_actlog_save_third_version_genesis_refused(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    log, _ = setup_log_with_v1_and_handover(tmp_path, registry)

    # v2 is active; attempting genesis for v3 in same scope
    genesis_v3 = make_act(
        3,
        "horizon-genesis",
        {"family": FAMILY_V3, "scope": SCOPE, "horizon_id": "demo.sales.v3.h0"},
    )
    with pytest.raises(HorizonModelError, match="active chain already exists in scope"):
        log.append(genesis_v3, expected_revision=3)

    assert log.read().revision == 3


def test_actlog_save_batch_second_genesis_refused(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    ws = tmp_path / "workspace"
    log = ActLog(ws, registry, undeclared_test_log=True)
    acts = [
        make_act(0, "bundle-adoption", {"bundle": BUNDLE}),
        make_act(
            1,
            "horizon-genesis",
            {"family": FAMILY_V1, "scope": SCOPE, "horizon_id": "demo.sales.v1.h0"},
        ),
        # Second genesis beside active v1 in same batch
        make_act(
            2,
            "horizon-genesis",
            {"family": FAMILY_V2, "scope": SCOPE, "horizon_id": "demo.sales.v2.h0"},
        ),
    ]
    with pytest.raises(HorizonModelError, match="active chain already exists in scope"):
        log.append_batch(acts, expected_revision=0)

    # All-or-none: nothing written
    assert not (ws / "acts.jsonl").exists() or log.read().revision == 0


def test_actlog_save_reverse_handover_downgrade_refused(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    log, _ = setup_log_with_v1_and_handover(tmp_path, registry)

    reverse_handover = make_act(
        3,
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
        log.append(reverse_handover, expected_revision=3)

    assert log.read().revision == 3


def test_actlog_save_chained_handover_succeeds(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    log, _ = setup_log_with_v1_and_handover(tmp_path, registry)

    handover_v2_to_v3 = make_act(
        3,
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
    rev = log.append(handover_v2_to_v3, expected_revision=3)
    assert rev == 4

    contents = log.read()
    assert contents.revision == 4
    state = project(contents.acts, registry)
    assert chain_key(FAMILY_V1, SCOPE) in state.horizon_state.retired_chains
    assert chain_key(FAMILY_V2, SCOPE) in state.horizon_state.retired_chains
    assert state.horizon_state.current_by_chain[chain_key(FAMILY_V3, SCOPE)] == "demo.sales.v3.h0"


def test_actlog_old_engine_read_boundary(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    log, ws = setup_log_with_v1_and_handover(tmp_path, registry)

    # Create an old engine schema registry lacking act-family-handover.v1
    old_schemas_dir = tmp_path / "old_schemas"
    old_schemas_dir.mkdir(parents=True, exist_ok=True)
    for p in KERNEL_SCHEMA_DIR.glob("*.schema.json"):
        if p.name != "act-family-handover.v1.schema.json":
            shutil.copy(p, old_schemas_dir / p.name)
    write_manifest(old_schemas_dir)
    old_registry = SchemaRegistry(old_schemas_dir)

    old_engine_log = ActLog(ws, old_registry, undeclared_test_log=True)
    with pytest.raises((ActLogCorruption, SchemaRegistryError)):
        old_engine_log.read()


def test_actlog_historical_two_genesis_log_stays_readable(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    ws = tmp_path / "workspace"
    ws.mkdir(parents=True, exist_ok=True)
    log_file = ws / "acts.jsonl"

    acts = [
        make_act(0, "bundle-adoption", {"bundle": BUNDLE}),
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
    ]
    lines = [json.dumps(a, sort_keys=True, separators=(",", ":")) for a in acts]
    log_file.write_text("\n".join(lines) + "\n", "utf-8")

    log = ActLog(ws, registry, undeclared_test_log=True)
    contents = log.read()
    assert contents.revision == 3
    state = project(contents.acts, registry)
    assert state.horizon_state.current_by_chain[chain_key(FAMILY_V1, SCOPE)] == "demo.sales.v1.h0"
    assert state.horizon_state.current_by_chain[chain_key(FAMILY_V2, SCOPE)] == "demo.sales.v2.h0"


def test_marshal_containment_refuses_both_current_log(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    acts = (
        make_act(0, "bundle-adoption", {"bundle": BUNDLE}),
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
                    "f.closure.v1",
                    "demo.sales.closure|family-horizon=demo.sales.v1.h0,year=2025",
                    True,
                )
            },
        ),
        make_act(
            3,
            "horizon-genesis",
            {"family": FAMILY_V2, "scope": SCOPE, "horizon_id": "demo.sales.v2.h0"},
        ),
        make_act(
            4,
            "assertion",
            {
                "finding": make_finding(
                    "f.closure.v2",
                    "demo.sales.closure|family-horizon=demo.sales.v2.h0,year=2025",
                    True,
                )
            },
        ),
    )
    state = project(acts, registry)
    currency = compute_currency(state)

    mapping_v2 = {
        "family": {"id": "demo.sales", "version": "v2"},
        "closure_fact_type": "demo.sales.closure",
        "closure_horizon_key": "family-horizon",
    }
    with pytest.raises(
        SourceAuthorityError, match="family demo.sales has multiple active version chains"
    ):
        marshal_closure_authority(state, currency, [mapping_v2])


def test_marshal_containment_admits_exact_version_after_handover(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    log, _ = setup_log_with_v1_and_handover(tmp_path, registry)
    state = project(log.read().acts, registry)
    currency = compute_currency(state)

    mapping_v2 = {
        "family": {"id": "demo.sales", "version": "v2"},
        "closure_fact_type": "demo.sales.closure",
        "closure_horizon_key": "family-horizon",
    }
    records, horizons_map = marshal_closure_authority(state, currency, [mapping_v2])
    assert horizons_map == {"demo.sales": "demo.sales.v2.h0"}


def test_marshal_multiple_scopes_same_version_refused(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    acts = (
        make_act(0, "bundle-adoption", {"bundle": BUNDLE}),
        make_act(
            1,
            "horizon-genesis",
            {"family": FAMILY_V2, "scope": {"subject": "s1"}, "horizon_id": "demo.sales.v2.h0.s1"},
        ),
        make_act(
            2,
            "horizon-genesis",
            {"family": FAMILY_V2, "scope": {"subject": "s2"}, "horizon_id": "demo.sales.v2.h0.s2"},
        ),
    )
    state = project(acts, registry)
    currency = compute_currency(state)

    mapping_v2 = {
        "family": {"id": "demo.sales", "version": "v2"},
        "closure_fact_type": "demo.sales.closure",
        "closure_horizon_key": "family-horizon",
    }
    with pytest.raises(
        SourceAuthorityError, match="family demo.sales has horizon chains in multiple scopes"
    ):
        marshal_closure_authority(state, currency, [mapping_v2])


def test_actlog_save_direct_closure_assertion_saved_then_fails_at_project(tmp_path: Path) -> None:
    registry = SchemaRegistry()
    log, _ = setup_log_with_v1_and_handover(tmp_path, registry)

    # Direct closure assertion against retired/superseded v1.h0
    closure_assertion = make_act(
        3,
        "assertion",
        {
            "finding": make_finding(
                "f-closure-v1-stale",
                "demo.sales.closure|family-horizon=demo.sales.v1.h0,year=2025",
                True,
            )
        },
    )
    # The pre-save fold covers lifecycle kinds only, so assertion is persisted
    rev = log.append(closure_assertion, expected_revision=3)
    assert rev == 4

    # But project() refuses it when resolving against the lattice (FindingModelError)
    with pytest.raises(FindingModelError):
        project(log.read().acts, registry)
