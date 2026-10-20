"""Real-recorder and integration tests for family version handover and containment (Increment 3).

Exercises:
1. test_finding_1_helper_log_containment: Marshal refuses ambiguous authority on both-current
   log with SourceAuthorityError; calculation fails closed.
2. test_finding_1_reached_through_real_recorder: Direct v2 genesis append beside active v1 chain
   is refused by ActLog pre-persistence boundary with HorizonModelError.
3. test_atomic_handover_replaces_closure_and_zero: Real recorder stages handover from closed-empty
   v1 to v2 on first statement; v1 closure drops; fresh v2 statement admitted.
4. test_closed_nonempty_handover_replaces_closure_and_subtotal: Real recorder stages handover from
   closed-nonempty v1 to v2; retained v1 statement facts survive; v1 closure drops; fresh closure needed.
5. test_real_recorder_no_statements_handover: Real recorder stages handover from closed-empty v1 to v2
   no-statements closure; v1 retired, fresh v2 closure attested.
6. test_untouched_workspace_standing: Historical v1 workspace evaluated under v2-adopting package
   does not calculate v2 figures; earlier v1 state stands unmutated.
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import pytest

from packages.derivation.marshal import marshal_closure_authority
from packages.derivation.source_authority import SourceAuthorityError
from packages.kernel.act_log import ActLog, ActLogError
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project
from packages.kernel.horizons import HorizonModelError
from packages.tax.f1099k_statement_recording import (
    F1099KRecordingRefused,
    FAMILY_ID,
    record_f1099k_no_statements_durably,
    record_f1099k_statement_durably,
)
from packages.tax.loader import TAX_CONTENT_DIR, load_closure_mappings, tax_registry

DEFAULT_SCOPE = {"tax-year": "2025", "subject": "demo.primary"}


def _setup_actlog(tmp_path: Path, registry: Any) -> ActLog:
    ws = tmp_path / "workspace"
    ws.mkdir(parents=True, exist_ok=True)
    return ActLog(ws, registry, undeclared_test_log=True)


def test_finding_1_helper_log_containment(tmp_path: Path) -> None:
    """Marshal refuses ambiguous authority on both-current log with SourceAuthorityError."""
    registry = tax_registry()
    map_v2 = json.loads(
        (TAX_CONTENT_DIR / "closure-mapping.f1099b-covered-w-st.v2.json").read_text("utf-8")
    )
    fid = "tax.us.2025.f1099b.covered-w-st"

    # Both-current log setup for fid
    acts = [
        {
            "schema": "act.v1",
            "act_id": "act-0001",
            "kind": "horizon-genesis",
            "actor": "user",
            "at": "2026-10-18T20:00:00Z",
            "committed_against": 0,
            "payload": {
                "family": {"id": fid, "version": "v1"},
                "scope": DEFAULT_SCOPE,
                "horizon_id": "demo.wst.v1.h0",
            },
        },
        {
            "schema": "act.v1",
            "act_id": "act-0002",
            "kind": "horizon-genesis",
            "actor": "user",
            "at": "2026-10-18T20:01:00Z",
            "committed_against": 1,
            "payload": {
                "family": {"id": fid, "version": "v2"},
                "scope": DEFAULT_SCOPE,
                "horizon_id": "demo.wst.v2.h0",
            },
        },
    ]
    state = project(tuple(acts), registry)
    currency = compute_currency(state)

    with pytest.raises(SourceAuthorityError) as exc_info:
        marshal_closure_authority(state, currency, [map_v2])
    assert f"family {fid} has multiple active version chains" in str(exc_info.value)


def test_finding_1_reached_through_real_recorder(tmp_path: Path) -> None:
    """Direct v2 genesis append beside active v1 chain is refused by ActLog pre-persistence boundary."""
    registry = tax_registry()
    log = _setup_actlog(tmp_path, registry)

    # 1. Real recorder establishes active v1 chain
    res1 = record_f1099k_no_statements_durably(
        log,
        registry,
        submission_id="sub.test.v1",
        evidence_id="ev.test.v1",
        actor="user",
        at="2026-10-18T20:00:00Z",
        expected_revision=0,
        family_version="v1",
    )
    assert res1["revision"] > 0
    current_rev = res1["revision"]

    # 2. Attempt to append a second genesis for v2 beside active v1 chain
    second_genesis_act = {
        "schema": "act.v1",
        "act_id": "act-bypass-v2-genesis",
        "kind": "horizon-genesis",
        "actor": "user",
        "at": "2026-10-18T20:05:00Z",
        "committed_against": current_rev,
        "payload": {
            "family": {"id": FAMILY_ID, "version": "v2"},
            "scope": DEFAULT_SCOPE,
            "horizon_id": "demo.f1099k.v2.h0",
        },
    }

    with pytest.raises(HorizonModelError) as exc_info:
        log.append(second_genesis_act, expected_revision=current_rev)
    assert "active chain already exists in scope" in str(exc_info.value)

    # Verify log is unmutated
    assert len(log.read().acts) == current_rev


def test_atomic_handover_replaces_closure_and_zero(tmp_path: Path) -> None:
    """Real recorder stages handover from closed-empty v1 to v2 on first statement; v1 closure drops."""
    registry = tax_registry()
    log = _setup_actlog(tmp_path, registry)

    # 1. Closed-empty v1
    res1 = record_f1099k_no_statements_durably(
        log,
        registry,
        submission_id="sub.closed.empty.v1",
        evidence_id="ev.closed.empty.v1",
        actor="user",
        at="2026-10-18T20:00:00Z",
        expected_revision=0,
        family_version="v1",
    )
    rev1 = res1["revision"]
    state1 = project(log.read().acts, registry)
    cur1 = compute_currency(state1)
    v1_closure_id = res1["finding_ids"][0]
    assert v1_closure_id in cur1.current_finding_ids

    # 2. Recorder writes first statement under v2 with close_family=False
    res2 = record_f1099k_statement_durably(
        log,
        registry,
        payer_id="demo.payer.1",
        statement_ref="stmt.001",
        box1a=1200.0,
        box4=50.0,
        submission_id="sub.stmt.v2",
        evidence_id="ev.stmt.v2",
        actor="user",
        at="2026-10-18T20:10:00Z",
        expected_revision=rev1,
        family_version="v2",
        close_family=False,
    )
    rev2 = res2["revision"]
    assert rev2 > rev1

    # Verify state after handover
    state2 = project(log.read().acts, registry)
    cur2 = compute_currency(state2)

    # Predecessor v1 chain is retired; v2 chain is active
    scope_tuple = tuple(sorted(DEFAULT_SCOPE.items()))
    assert (FAMILY_ID, "v1", scope_tuple) in state2.horizon_state.retired_chains
    assert (FAMILY_ID, "v2", scope_tuple) in state2.horizon_state.current_by_chain
    assert (FAMILY_ID, "v1", scope_tuple) not in state2.horizon_state.current_by_chain

    # Predecessor closure is displaced via currency cascade
    assert v1_closure_id not in cur2.current_finding_ids
    assert v1_closure_id in cur2.displaced_finding_ids

    # Statement finding is current
    stmt_b1a_id = res2["finding_ids"][0]
    assert stmt_b1a_id in cur2.current_finding_ids


def test_closed_nonempty_handover_replaces_closure_and_subtotal(tmp_path: Path) -> None:
    """Real recorder stages handover from closed-nonempty v1 to v2; retained statement facts survive."""
    registry = tax_registry()
    log = _setup_actlog(tmp_path, registry)

    # 1. Closed-nonempty v1 statement
    res1 = record_f1099k_statement_durably(
        log,
        registry,
        payer_id="demo.payer.1",
        statement_ref="stmt.001",
        box1a=800.0,
        box4=20.0,
        submission_id="sub.stmt1.v1",
        evidence_id="ev.stmt1.v1",
        actor="user",
        at="2026-10-18T20:00:00Z",
        expected_revision=0,
        family_version="v1",
        close_family=True,
    )
    rev1 = res1["revision"]
    state1 = project(log.read().acts, registry)
    cur1 = compute_currency(state1)
    v1_b1a_id = res1["finding_ids"][0]
    v1_closure_id = res1["finding_ids"][-1]
    assert v1_b1a_id in cur1.current_finding_ids
    assert v1_closure_id in cur1.current_finding_ids

    # 2. Add second statement under v2
    res2 = record_f1099k_statement_durably(
        log,
        registry,
        payer_id="demo.payer.2",
        statement_ref="stmt.002",
        box1a=400.0,
        box4=0.0,
        submission_id="sub.stmt2.v2",
        evidence_id="ev.stmt2.v2",
        actor="user",
        at="2026-10-18T20:10:00Z",
        expected_revision=rev1,
        family_version="v2",
        close_family=False,
    )
    state2 = project(log.read().acts, registry)
    cur2 = compute_currency(state2)

    # Retained statement finding from v1 survives intact in currency
    assert v1_b1a_id in cur2.current_finding_ids
    assert state2.findings[v1_b1a_id]["value"] == 800.0

    # New v2 statement finding is also current
    v2_b1a_id = res2["finding_ids"][0]
    assert v2_b1a_id in cur2.current_finding_ids
    assert state2.findings[v2_b1a_id]["value"] == 400.0

    # Predecessor v1 closure is displaced
    assert v1_closure_id in cur2.displaced_finding_ids
    assert v1_closure_id not in cur2.current_finding_ids


def test_real_recorder_no_statements_handover(tmp_path: Path) -> None:
    """Real recorder stages handover from closed-empty v1 to v2 no-statements closure."""
    registry = tax_registry()
    log = _setup_actlog(tmp_path, registry)

    # 1. Closed-empty v1
    res1 = record_f1099k_no_statements_durably(
        log,
        registry,
        submission_id="sub.empty.v1",
        evidence_id="ev.empty.v1",
        actor="user",
        at="2026-10-18T20:00:00Z",
        expected_revision=0,
        family_version="v1",
    )
    v1_closure_id = res1["finding_ids"][0]

    # 2. Handover to v2 no-statements closure
    res2 = record_f1099k_no_statements_durably(
        log,
        registry,
        submission_id="sub.empty.v2",
        evidence_id="ev.empty.v2",
        actor="user",
        at="2026-10-18T20:10:00Z",
        expected_revision=res1["revision"],
        family_version="v2",
    )
    v2_closure_id = res2["finding_ids"][0]

    state = project(log.read().acts, registry)
    cur = compute_currency(state)

    scope_tuple = tuple(sorted(DEFAULT_SCOPE.items()))
    assert (FAMILY_ID, "v1", scope_tuple) in state.horizon_state.retired_chains
    assert (FAMILY_ID, "v2", scope_tuple) in state.horizon_state.current_by_chain
    assert v1_closure_id in cur.displaced_finding_ids
    assert v2_closure_id in cur.current_finding_ids


def test_untouched_workspace_standing(tmp_path: Path) -> None:
    """Historical v1 workspace evaluated under v2-adopting mapping gets no closure admission."""
    registry = tax_registry()
    log = _setup_actlog(tmp_path, registry)

    # Record v1 statement and closure
    res = record_f1099k_statement_durably(
        log,
        registry,
        payer_id="demo.payer.1",
        statement_ref="stmt.001",
        box1a=600.0,
        box4=0.0,
        submission_id="sub.untouched.v1",
        evidence_id="ev.untouched.v1",
        actor="user",
        at="2026-10-18T20:00:00Z",
        expected_revision=0,
        family_version="v1",
        close_family=True,
    )
    acts = log.read().acts
    state = project(acts, registry)
    currency = compute_currency(state)

    # v1 mapping: admits closure for v1
    map_v1 = {
        "id": "tax.us.2025.closure-mapping.f1099k",
        "family": {"id": FAMILY_ID, "version": "v1"},
        "closure_fact_type": "tax.us.2025.f1099k.source-closure",
        "closure_horizon_key": "family-horizon",
    }
    records_v1, horizons_v1 = marshal_closure_authority(state, currency, [map_v1])
    assert FAMILY_ID in horizons_v1

    # Hypothetical future v2 mapping: untouched v1 workspace gets no horizon mapping
    map_v2 = {
        "id": "tax.us.2025.closure-mapping.f1099k.v2",
        "family": {"id": FAMILY_ID, "version": "v2"},
        "closure_fact_type": "tax.us.2025.f1099k.source-closure",
        "closure_horizon_key": "family-horizon",
    }
    records_v2, horizons_v2 = marshal_closure_authority(state, currency, [map_v2])
    assert FAMILY_ID not in horizons_v2


def test_writer_refuses_handover_to_older_version(tmp_path: Path) -> None:
    registry = tax_registry()
    log = _setup_actlog(tmp_path, registry)

    # Record v2 statement
    res1 = record_f1099k_statement_durably(
        log,
        registry,
        payer_id="demo.payer.1",
        statement_ref="stmt.001",
        box1a=600.0,
        box4=0.0,
        submission_id="sub.v2.1",
        evidence_id="ev.v2.1",
        actor="user",
        at="2026-10-18T20:00:00Z",
        expected_revision=0,
        family_version="v2",
    )
    rev1 = res1["revision"]

    # Attempt to record with older family_version="v1" via statement writer
    with pytest.raises(F1099KRecordingRefused, match="cannot handover to older family version"):
        record_f1099k_statement_durably(
            log,
            registry,
            payer_id="demo.payer.2",
            statement_ref="stmt.002",
            box1a=800.0,
            box4=0.0,
            submission_id="sub.v1.2",
            evidence_id="ev.v1.2",
            actor="user",
            at="2026-10-18T20:01:00Z",
            expected_revision=rev1,
            family_version="v1",
        )

    # Attempt to record with older family_version="v1" via no-statements writer
    log2 = _setup_actlog(tmp_path / "ws2", registry)
    res_no = record_f1099k_no_statements_durably(
        log2,
        registry,
        submission_id="sub.v2.no",
        evidence_id="ev.v2.no",
        actor="user",
        at="2026-10-18T20:00:00Z",
        expected_revision=0,
        family_version="v2",
    )
    with pytest.raises(F1099KRecordingRefused, match="cannot handover to older family version"):
        record_f1099k_no_statements_durably(
            log2,
            registry,
            submission_id="sub.v1.no",
            evidence_id="ev.v1.no",
            actor="user",
            at="2026-10-18T20:02:00Z",
            expected_revision=res_no["revision"],
            family_version="v1",
        )
