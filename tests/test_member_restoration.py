"""Real-act witness for restoring a removed source-family member.

Track 3R restores current membership only through the removing horizon's
validated lineage, while keeping earlier findings and their dependents ended.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.findings import FindingModelError, apply_act, project
from packages.kernel.horizons import HorizonModelError, current_horizon_id
from packages.derivation.loader import workspace_registry
from packages.derivation.projection import workspace_currency


FAMILY = {"id": "demo.restoration.family", "version": "v1"}
SCOPE = {"subject": "demo.subject"}
FACT_ID = "demo.restoration.amount|slip=demo.slip,year=2025"
MEMBER_FACT_TYPE = {
    "schema": "fact-type.v1",
    "id": "demo.restoration.amount",
    "title": "Demo source amount",
    "nature": "determinable",
    "identity_keys": [
        {"name": "slip", "kind": "entity", "entity_kind": "demo.slip"},
        {"name": "year", "kind": "literal", "values": ["2025"]},
    ],
    "value_schema": {"type": "number"},
    "supersession": {"policy": "free"},
}
CLOSURE_FACT_TYPE = {
    "schema": "fact-type.v1",
    "id": "demo.restoration.closure",
    "title": "Demo source-family closure",
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


def _base_acts(
    member_fact_type: dict[str, Any] = MEMBER_FACT_TYPE,
    additional_fact_types: tuple[dict[str, Any], ...] = (),
) -> list[dict[str, Any]]:
    bundle_schema = "bundle.v3" if member_fact_type.get("schema") == "fact-type.v3" else "bundle.v1"
    return [
        _act(
            0,
            "bundle-adoption",
            {
                "bundle": {
                    "schema": bundle_schema,
                    "id": "demo.restoration.bundle",
                    "label": "Demo restoration vocabulary",
                    "fact_types": [member_fact_type, CLOSURE_FACT_TYPE, *additional_fact_types],
                }
            },
        ),
        _act(
            1,
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": "demo.slip",
                    "kind": "demo.slip",
                    "label": "Demo slip",
                }
            },
        ),
        _act(
            2,
            "horizon-genesis",
            {"family": FAMILY, "scope": SCOPE, "horizon_id": "demo.h0"},
        ),
        _act(
            3,
            "assertion",
            {
                "finding": {
                    "schema": "finding.v1",
                    "id": "demo.closure.h0",
                    "fact_id": "demo.restoration.closure|family-horizon=demo.h0,year=2025",
                    "value": True,
                    "basis": "attested",
                    "evidence_ids": [],
                }
            },
        ),
    ]


def _append(log: ActLog, one_act: dict[str, Any]) -> int:
    return log.append(one_act, expected_revision=log.read().revision)


def _act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.restoration.act.{index}",
        "kind": kind,
        "actor": "demo.user",
        "at": f"2026-10-25T10:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _finding(finding_id: str, value: float) -> dict[str, Any]:
    return _finding_for(finding_id, FACT_ID, value)


def _finding_for(finding_id: str, fact_id: str, value: float) -> dict[str, Any]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def _transition(
    index: int, member: dict[str, Any], successor: str, predecessor: str
) -> dict[str, Any]:
    return _act(
        index,
        "member-transition",
        {
            "family": FAMILY,
            "scope": SCOPE,
            "member": member,
            "successor": {"id": successor, "predecessor": predecessor},
        },
    )


def test_fresh_same_fact_assertion_is_current_after_remove_and_readd(
    tmp_path: Any,
) -> None:
    registry = workspace_registry()
    registry.family_member_predicates.add("demo.restoration.amount")
    log = ActLog(tmp_path, registry, undeclared_test_log=True)
    revision = 0
    for one_act in _base_acts():
        revision = log.append(one_act, expected_revision=revision)
    revision = _append(log, _transition(
        4, {"action": "assert", "finding": _finding("demo.old", 100.0)},
        "demo.h1", "demo.h0",
    ))
    revision = _append(log, _act(5, "derived-publication", {
        "run_id": "demo.restoration.run.before-remove",
        "finding": {
            "schema": "derived-finding.v1",
            "id": "demo.derived.old-member",
            "symbol": "demo.restoration.result",
            "value": "100",
            "version": "v1",
            "pins": [
                {"role": "input", "id": "demo.old", "version": "v1"},
                {"role": "field-mapping", "id": "demo.restoration.map", "version": "v1"},
            ],
        },
    }))
    revision = _append(log, _transition(
        6, {"action": "remove", "fact_id": FACT_ID}, "demo.h2", "demo.h1",
    ))
    revision = _append(log, _transition(
        7, {"action": "assert", "finding": _finding("demo.fresh", 100.0)},
        "demo.h3", "demo.h2",
    ))
    acts = log.read().acts
    state = project(acts, registry)
    currency, derived_currency = workspace_currency(acts, registry)
    assert "demo.fresh" in state.findings
    assert "demo.old" in currency.displaced_finding_ids
    assert "demo.fresh" in currency.current_finding_ids
    assert "demo.closure.h0" in currency.displaced_finding_ids
    assert "demo.derived.old-member" in derived_currency.displaced_derived_ids
    assert current_horizon_id(state.horizon_state, FAMILY, SCOPE) == "demo.h3"


def test_equal_value_remove_readd_cycles_displace_every_older_finding(tmp_path: Any) -> None:
    registry = workspace_registry()
    registry.family_member_predicates.add("demo.restoration.amount")
    log = ActLog(tmp_path, registry, undeclared_test_log=True)
    for one_act in _base_acts():
        _append(log, one_act)

    prefixes: list[tuple[dict[str, Any], ...]] = [log.read().acts]
    incremental = project(prefixes[0], registry)
    transitions = [
        _transition(4, {"action": "assert", "finding": _finding("demo.first", 100.0)}, "demo.h1", "demo.h0"),
        _transition(5, {"action": "remove", "fact_id": FACT_ID}, "demo.h2", "demo.h1"),
        _transition(6, {"action": "assert", "finding": _finding("demo.second", 100.0)}, "demo.h3", "demo.h2"),
        _transition(7, {"action": "remove", "fact_id": FACT_ID}, "demo.h4", "demo.h3"),
        _transition(8, {"action": "assert", "finding": _finding("demo.third", 100.0)}, "demo.h5", "demo.h4"),
    ]
    for one_act in transitions:
        _append(log, one_act)
        acts = log.read().acts
        incremental = apply_act(incremental, one_act, registry)
        rebuilt = project(acts, registry)
        assert incremental == rebuilt
        assert compute_currency(incremental) == compute_currency(rebuilt)
        prefixes.append(acts)

    state = project(log.read().acts, registry)
    currency = compute_currency(state)
    assert current_horizon_id(state.horizon_state, FAMILY, SCOPE) == "demo.h5"
    assert FACT_ID not in state.withdrawn_fact_ids
    assert "demo.third" in currency.current_finding_ids
    assert {"demo.first", "demo.second"} <= currency.displaced_finding_ids
    assert "demo.closure.h0" in currency.displaced_finding_ids


def test_same_member_correction_after_restoration_does_not_advance_horizon(tmp_path: Any) -> None:
    registry = workspace_registry()
    registry.family_member_predicates.add("demo.restoration.amount")
    log = ActLog(tmp_path, registry, undeclared_test_log=True)
    for one_act in _base_acts():
        _append(log, one_act)
    for one_act in (
        _transition(4, {"action": "assert", "finding": _finding("demo.old", 100.0)}, "demo.h1", "demo.h0"),
        _transition(5, {"action": "remove", "fact_id": FACT_ID}, "demo.h2", "demo.h1"),
        _transition(6, {"action": "assert", "finding": _finding("demo.fresh", 100.0)}, "demo.h3", "demo.h2"),
    ):
        _append(log, one_act)

    horizon_before = current_horizon_id(project(log.read().acts, registry).horizon_state, FAMILY, SCOPE)
    correction = _act(7, "assertion", {"finding": _finding("demo.fresh.corrected", 101.0)})
    _append(log, correction)
    state = project(log.read().acts, registry)
    currency = compute_currency(state)
    assert current_horizon_id(state.horizon_state, FAMILY, SCOPE) == horizon_before == "demo.h3"
    assert "demo.fresh.corrected" in currency.current_finding_ids
    assert "demo.fresh" in currency.displaced_finding_ids


def test_reclassification_restores_removed_target_and_withdraws_current_source(tmp_path: Any) -> None:
    registry = workspace_registry()
    registry.family_member_predicates.add("demo.restoration.amount")
    log = ActLog(tmp_path, registry, undeclared_test_log=True)
    for one_act in _base_acts():
        _append(log, one_act)
    fact_b = "demo.restoration.amount|slip=demo.slip-b,year=2025"
    _append(log, _act(4, "entity-introduced", {
        "entity": {
            "schema": "entity.v1", "id": "demo.slip-b", "kind": "demo.slip", "label": "Demo slip B",
        },
    }))
    transitions = (
        _transition(5, {"action": "assert", "finding": _finding("demo.a.old", 100.0)}, "demo.h1", "demo.h0"),
        _transition(6, {"action": "assert", "finding": _finding_for("demo.b.current", fact_b, 200.0)}, "demo.h2", "demo.h1"),
        _transition(7, {"action": "remove", "fact_id": FACT_ID}, "demo.h3", "demo.h2"),
        _transition(8, {
            "action": "reclassify",
            "fact_id": fact_b,
            "finding": _finding("demo.a.restored", 100.0),
        }, "demo.h4", "demo.h3"),
    )
    for one_act in transitions:
        _append(log, one_act)

    state = project(log.read().acts, registry)
    currency = compute_currency(state)
    assert FACT_ID not in state.withdrawn_fact_ids
    assert fact_b in state.withdrawn_fact_ids
    assert "demo.a.old" in currency.displaced_finding_ids
    assert "demo.a.restored" in currency.current_finding_ids
    assert "demo.b.current" in currency.displaced_finding_ids
    assert current_horizon_id(state.horizon_state, FAMILY, SCOPE) == "demo.h4"


def _assert_absent_member_reclassification_rejected_atomically(
    log: ActLog, registry: Any, *, batch: bool
) -> None:
    before = log.read()
    before_bytes = log._path.read_bytes()
    before_state = project(before.acts, registry)
    before_currency = compute_currency(before_state)
    assert current_horizon_id(before_state.horizon_state, FAMILY, SCOPE) == "demo.h2"
    assert "demo.closure.h2" in before_currency.current_finding_ids
    assert FACT_ID in before_state.withdrawn_fact_ids
    same_fact_reclassify = _transition(
        before.revision,
        {"action": "reclassify", "fact_id": FACT_ID, "finding": _finding("demo.self-reclass", 100.0)},
        "demo.h3", "demo.h2",
    )
    try:
        if batch:
            log.append_batch((same_fact_reclassify,), expected_revision=before.revision)
        else:
            log.append(same_fact_reclassify, expected_revision=before.revision)
    except FindingModelError as exc:
        assert "already withdrawn" in str(exc)
    else:
        raise AssertionError("reclassification cannot remove a member that was already absent")
    assert log.read() == before
    assert log._path.read_bytes() == before_bytes
    after_state = project(log.read().acts, registry)
    assert after_state == before_state
    assert current_horizon_id(after_state.horizon_state, FAMILY, SCOPE) == "demo.h2"
    assert "demo.closure.h2" in compute_currency(after_state).current_finding_ids


def test_reclassifying_already_absent_same_fact_refuses_atomically_on_append(tmp_path: Any) -> None:
    log, registry, _acts = _removed_member_log(tmp_path)
    _assert_absent_member_reclassification_rejected_atomically(log, registry, batch=False)


def test_reclassifying_already_absent_same_fact_refuses_atomically_in_batch(tmp_path: Any) -> None:
    log, registry, _acts = _removed_member_log(tmp_path)
    _assert_absent_member_reclassification_rejected_atomically(log, registry, batch=True)


def test_removal_lineage_survives_family_version_handover(tmp_path: Any) -> None:
    registry = workspace_registry()
    registry.family_member_predicates.add("demo.restoration.amount")
    log = ActLog(tmp_path, registry, undeclared_test_log=True)
    for one_act in _base_acts():
        _append(log, one_act)
    _append(log, _transition(
        4, {"action": "assert", "finding": _finding("demo.old", 100.0)}, "demo.h1", "demo.h0",
    ))
    _append(log, _transition(5, {"action": "remove", "fact_id": FACT_ID}, "demo.h2", "demo.h1"))
    family_v2 = {"id": FAMILY["id"], "version": "v2"}
    _append(log, _act(6, "family-handover", {
        "predecessor": {"family": FAMILY, "scope": SCOPE, "horizon_id": "demo.h2"},
        "successor": {"family": family_v2, "scope": SCOPE, "horizon_id": "demo.v2.h0"},
    }))
    _append(log, _act(7, "member-transition", {
        "family": family_v2,
        "scope": SCOPE,
        "member": {"action": "assert", "finding": _finding("demo.after-handover", 100.0)},
        "successor": {"id": "demo.v2.h1", "predecessor": "demo.v2.h0"},
    }))
    state = project(log.read().acts, registry)
    currency = compute_currency(state)
    assert FACT_ID not in state.withdrawn_fact_ids
    assert "demo.after-handover" in currency.current_finding_ids
    assert "demo.old" in currency.displaced_finding_ids
    assert current_horizon_id(state.horizon_state, family_v2, SCOPE) == "demo.v2.h1"


def _removed_member_log(tmp_path: Any) -> tuple[ActLog, Any, list[dict[str, Any]]]:
    registry = workspace_registry()
    registry.family_member_predicates.add("demo.restoration.amount")
    log = ActLog(tmp_path, registry, undeclared_test_log=True)
    acts = _base_acts()
    for one_act in acts:
        _append(log, one_act)
    for one_act in (
        _transition(4, {"action": "assert", "finding": _finding("demo.old", 100.0)}, "demo.h1", "demo.h0"),
        _transition(5, {"action": "remove", "fact_id": FACT_ID}, "demo.h2", "demo.h1"),
    ):
        acts.append(one_act)
        _append(log, one_act)
    closure = _act(6, "assertion", {
        "finding": {
            "schema": "finding.v1",
            "id": "demo.closure.h2",
            "fact_id": "demo.restoration.closure|family-horizon=demo.h2,year=2025",
            "value": True,
            "basis": "attested",
            "evidence_ids": [],
        },
    })
    acts.append(closure)
    _append(log, closure)
    return log, registry, acts


def _unrelated_chain(
    which: str,
) -> tuple[dict[str, str], dict[str, str]]:
    if which == "family":
        return {"id": "demo.restoration.other-family", "version": "v1"}, SCOPE
    return FAMILY, {"subject": "demo.other-subject"}


def _independent_readd(
    index: int, family: dict[str, str], scope: dict[str, str]
) -> dict[str, Any]:
    return _act(
        index, "member-transition", {
            "family": family,
            "scope": scope,
            "member": {"action": "assert", "finding": _finding("demo.independent.readd", 100.0)},
            "successor": {"id": "demo.other.h1", "predecessor": "demo.other.h0"},
        },
    )


def test_new_readd_must_match_removal_family_lineage(tmp_path: Any) -> None:
    log, registry, _acts = _removed_member_log(tmp_path)
    family, scope = _unrelated_chain("family")
    genesis = _act(7, "horizon-genesis", {"family": family, "scope": scope, "horizon_id": "demo.other.h0"})
    _append(log, genesis)
    transition = _independent_readd(8, family, scope)
    before = log.read()
    before_bytes = log._path.read_bytes()
    try:
        log.append(transition, expected_revision=before.revision)
    except FindingModelError as exc:
        assert "recorded removal horizon" in str(exc)
    else:
        raise AssertionError("a new re-add under another family must be refused")
    assert log.read() == before
    assert log._path.read_bytes() == before_bytes


def test_new_readd_must_match_removal_scope_lineage(tmp_path: Any) -> None:
    log, _registry, _acts = _removed_member_log(tmp_path)
    family, scope = _unrelated_chain("scope")
    _append(log, _act(7, "horizon-genesis", {"family": family, "scope": scope, "horizon_id": "demo.other.h0"}))
    before = log.read()
    before_bytes = log._path.read_bytes()
    try:
        log.append(_independent_readd(8, family, scope), expected_revision=before.revision)
    except FindingModelError:
        pass
    else:
        raise AssertionError("a new re-add under another scope must be refused")
    assert log.read() == before
    assert log._path.read_bytes() == before_bytes


def test_batch_readd_wrong_chain_is_atomic(tmp_path: Any) -> None:
    log, _registry, _acts = _removed_member_log(tmp_path)
    family, scope = _unrelated_chain("family")
    before = log.read()
    before_bytes = log._path.read_bytes()
    genesis = _act(before.revision, "horizon-genesis", {
        "family": family, "scope": scope, "horizon_id": "demo.batch.other.h0",
    })
    transition = _act(before.revision + 1, "member-transition", {
        "family": family,
        "scope": scope,
        "member": {"action": "assert", "finding": _finding("demo.batch.readd", 100.0)},
        "successor": {"id": "demo.batch.other.h1", "predecessor": "demo.batch.other.h0"},
    })
    try:
        log.append_batch((genesis, transition), expected_revision=before.revision)
    except FindingModelError:
        pass
    else:
        raise AssertionError("a batch with cross-chain restoration must be refused")
    assert log.read() == before
    assert log._path.read_bytes() == before_bytes


def test_historical_cross_chain_readd_stays_ended_then_correct_lineage_restores(
    tmp_path: Any,
) -> None:
    _log, registry, acts = _removed_member_log(tmp_path)
    family, scope = _unrelated_chain("family")
    genesis = _act(7, "horizon-genesis", {
        "family": family, "scope": scope, "horizon_id": "demo.history.other.h0",
    })
    wrong_chain = _act(8, "member-transition", {
        "family": family,
        "scope": scope,
        "member": {"action": "assert", "finding": _finding("demo.historical.readd", 100.0)},
        "successor": {"id": "demo.history.other.h1", "predecessor": "demo.history.other.h0"},
    })
    acts.extend((genesis, wrong_chain))
    # This fixture models a previously admitted immutable history. The replay
    # reader accepts it; only new ActLog writes enforce the restoration guard.
    history_dir = Path(tmp_path) / "historical"
    history_dir.mkdir()
    historical = ActLog(history_dir, registry, undeclared_test_log=True)
    historical._path.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in acts))
    replay = historical.read()
    state = project(replay.acts, registry)
    currency = compute_currency(state)
    assert FACT_ID in state.withdrawn_fact_ids
    assert "demo.historical.readd" in state.findings
    assert "demo.historical.readd" in currency.displaced_finding_ids
    assert "demo.closure.h2" in currency.current_finding_ids
    incremental = project(replay.acts[:4], registry)
    for index, one_act in enumerate(replay.acts[4:], start=4):
        incremental = apply_act(incremental, one_act, registry)
        assert incremental == project(replay.acts[: index + 1], registry)

    correct = _transition(
        9, {"action": "assert", "finding": _finding("demo.correct.readd", 100.0)},
        "demo.h3", "demo.h2",
    )
    # Once loaded, a correct-lineage restoration is admitted through the
    # ordinary ActLog path; no second raw-history construction is needed.
    historical.append(correct, expected_revision=replay.revision)
    final_contents = historical.read()
    final = project(final_contents.acts, registry)
    final_currency = compute_currency(final)
    assert FACT_ID not in final.withdrawn_fact_ids
    assert FACT_ID in state.withdrawn_fact_ids  # prior immutable projection is unchanged
    assert "demo.correct.readd" in final_currency.current_finding_ids
    assert {"demo.old", "demo.historical.readd"} <= final_currency.displaced_finding_ids
    assert "demo.closure.h2" in final_currency.displaced_finding_ids
    incremental = project(final_contents.acts[:4], registry)
    for index, one_act in enumerate(final_contents.acts[4:], start=4):
        incremental = apply_act(incremental, one_act, registry)
        assert incremental == project(final_contents.acts[: index + 1], registry)


def test_reused_finding_id_and_invalid_fresh_assertion_are_atomic(tmp_path: Any) -> None:
    registry = workspace_registry()
    registry.family_member_predicates.add("demo.restoration.amount")
    log = ActLog(tmp_path, registry, undeclared_test_log=True)
    for one_act in _base_acts():
        _append(log, one_act)
    for one_act in (
        _transition(4, {"action": "assert", "finding": _finding("demo.old", 100.0)}, "demo.h1", "demo.h0"),
        _transition(5, {"action": "remove", "fact_id": FACT_ID}, "demo.h2", "demo.h1"),
    ):
        _append(log, one_act)

    before = log.read()
    reused_id = _transition(
        6, {"action": "assert", "finding": _finding("demo.old", 100.0)}, "demo.h3", "demo.h2",
    )
    try:
        log.append(reused_id, expected_revision=before.revision)
    except FindingModelError as exc:
        assert "finding already exists" in str(exc)
    else:
        raise AssertionError("restoration must not reuse an old finding identity")
    assert log.read() == before

    reused_horizon = _transition(
        6, {"action": "assert", "finding": _finding("demo.fresh", 100.0)}, "demo.h2", "demo.h2",
    )
    try:
        log.append(reused_horizon, expected_revision=before.revision)
    except HorizonModelError:
        pass
    else:
        raise AssertionError("a reused successor horizon must not restore membership")
    assert log.read() == before

    invalid = _finding("demo.invalid-evidence", 100.0)
    invalid["basis"] = "documentary"
    rejected = _transition(6, {"action": "assert", "finding": invalid}, "demo.h3", "demo.h2")
    try:
        log.append(rejected, expected_revision=before.revision)
    except FindingModelError as exc:
        assert "names no evidence" in str(exc)
    else:
        raise AssertionError("invalid fresh evidence must not restore membership")
    assert log.read() == before

    stale = _transition(
        6, {"action": "assert", "finding": _finding("demo.fresh", 100.0)}, "demo.h3", "demo.h1",
    )
    try:
        log.append(stale, expected_revision=before.revision)
    except HorizonModelError:
        pass
    else:
        raise AssertionError("a stale predecessor must not restore membership")
    assert log.read() == before


def test_locked_policy_still_blocks_reentry_after_removal(tmp_path: Any) -> None:
    registry = workspace_registry()
    registry.family_member_predicates.add("demo.restoration.amount")
    locked_type = {**MEMBER_FACT_TYPE, "schema": "fact-type.v3", "supersession": {"policy": "locked"}}
    state = project(tuple(_base_acts(locked_type)), registry)
    state = apply_act(state, _transition(
        4, {"action": "assert", "finding": _finding("demo.old", 100.0)}, "demo.h1", "demo.h0",
    ), registry)
    state = apply_act(state, _transition(
        5, {"action": "remove", "fact_id": FACT_ID}, "demo.h2", "demo.h1",
    ), registry)
    before = state
    try:
        apply_act(state, _transition(
            6, {"action": "assert", "finding": _finding("demo.fresh", 100.0)}, "demo.h3", "demo.h2",
        ), registry)
    except FindingModelError as exc:
        assert "locked" in str(exc)
    else:
        raise AssertionError("restoration must preserve the fact type's locked policy")
    assert state == before


def test_closed_on_attestation_policy_still_blocks_reentry(tmp_path: Any) -> None:
    registry = workspace_registry()
    registry.family_member_predicates.add("demo.restoration.amount")
    gate_type = {
        "schema": "fact-type.v1",
        "id": "demo.restoration.member-closure",
        "title": "Demo member closure gate",
        "nature": "determinable",
        "identity_keys": [
            {"name": "slip", "kind": "entity", "entity_kind": "demo.slip"},
            {"name": "year", "kind": "literal", "values": ["2025"]},
        ],
        "value_schema": {"type": "boolean"},
        "supersession": {"policy": "free"},
    }
    gated_type = {
        **MEMBER_FACT_TYPE,
        "schema": "fact-type.v3",
        "supersession": {
            "policy": "closed-on-attestation",
            "gate": {"fact_type": "demo.restoration.member-closure"},
        },
    }
    state = project(tuple(_base_acts(gated_type, (gate_type,))), registry)
    state = apply_act(state, _transition(
        4, {"action": "assert", "finding": _finding("demo.old", 100.0)}, "demo.h1", "demo.h0",
    ), registry)
    state = apply_act(state, _transition(
        5, {"action": "remove", "fact_id": FACT_ID}, "demo.h2", "demo.h1",
    ), registry)
    closure = _act(6, "assertion", {
        "finding": {
            "schema": "finding.v1",
            "id": "demo.closure.h2",
            "fact_id": "demo.restoration.member-closure|slip=demo.slip,year=2025",
            "value": True,
            "basis": "attested",
            "evidence_ids": [],
        },
    })
    state = apply_act(state, closure, registry)
    before = state
    try:
        apply_act(state, _transition(
            7, {"action": "assert", "finding": _finding("demo.fresh", 100.0)}, "demo.h3", "demo.h2",
        ), registry)
    except FindingModelError as exc:
        assert "closed-on-attestation" in str(exc)
    else:
        raise AssertionError("restoration must preserve an active closure gate")
    assert state == before
