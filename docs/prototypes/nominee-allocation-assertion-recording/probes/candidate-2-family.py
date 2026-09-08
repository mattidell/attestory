"""Candidate 2 probe: adopted source-family route via act-member-transition.v3.

Exercises the committed kernel (packages/kernel/findings.py, horizons.py,
currency.py) plus the published source-family.v2 / family-horizon.v1 /
act-member-transition.v3 contracts. Synthetic demo.* identities only.
Does not modify packages/ or tests/.

Run from the repository root:

    PYTHONPATH=. python3 docs/prototypes/nominee-allocation-assertion-recording/probes/candidate-2-family.py
"""

from __future__ import annotations

from typing import Any

from packages.derivation.loader import DERIVATION_SCHEMA_DIR
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import (
    FindingModelError,
    _NO_CURRENT_VALUE,
    _current_value_for_fact,
    apply_act,
    initial_state,
)
from packages.kernel.horizons import HorizonModelError
from packages.kernel.schema_registry import (
    KERNEL_SCHEMA_DIR,
    SchemaRegistry,
    SchemaValidationError,
)

# ---------------------------------------------------------------------------
# Synthetic vocabulary
# ---------------------------------------------------------------------------

ACTOR = "demo.user.alex"
FACT_TYPE_ID = "demo.allocation.amount"
FACT_TYPE_GEN_ID = "demo.allocation.amount-instanced"
FAMILY = {"id": "demo.allocation.ordinary", "version": "v1"}
FAMILY_GEN = {"id": "demo.allocation.instanced", "version": "v1"}
SCOPE = {"tax-year": "2025", "subject": "demo.primary"}
REPORT_KIND = "demo.form1099int-report"
PERSON_KIND = "demo.person"
INSTANCE_KIND = "demo.allocation-instance"
REPORT_A = "demo.report.a"
REPORT_B = "demo.report.b"
OWNER_PAT = "demo.owner.pat"
OWNER_KIM = "demo.owner.kim"
PAYER = "demo.payer.alpha"

KEYS_REPORT_OWNER = ("report", "owner")
KEYS_REPORT_OWNER_INSTANCE = ("report", "owner", "instance")


def _fact_id(report: str, owner: str) -> str:
    return fact_id_for(
        FACT_TYPE_ID,
        (("report", report), ("owner", owner)),
    )


def _gen_fact_id(report: str, owner: str, instance: str) -> str:
    return fact_id_for(
        FACT_TYPE_GEN_ID,
        (("report", report), ("owner", owner), ("instance", instance)),
    )


def _act(index: int, kind: str, payload: dict[str, Any], actor: str = ACTOR) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.cand2.act.{index:03d}",
        "kind": kind,
        "actor": actor,
        "at": f"2026-09-05T14:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _entity(entity_id: str, kind: str, label: str) -> dict[str, Any]:
    return {"schema": "entity.v1", "id": entity_id, "kind": kind, "label": label}


def _finding(
    finding_id: str,
    fact_id: str,
    value: Any,
    *,
    basis: str = "attested",
) -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": basis,
        "evidence_ids": [],
    }


def _fact_type(type_id: str, title: str, identity_keys: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "fact-type.v1",
        "id": type_id,
        "title": title,
        "nature": "determinable",
        "identity_keys": identity_keys,
        "value_schema": {"type": "number"},
        "supersession": {"policy": "free"},
    }


def _bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v1",
        "id": "demo.allocation.vocabulary",
        "label": "Demo ordinary-allocation vocabulary (candidate 2 probe)",
        "fact_types": [
            _fact_type(
                FACT_TYPE_ID,
                "Ordinary allocation amount from one identified report to one named other person",
                [
                    {"name": "report", "kind": "entity", "entity_kind": REPORT_KIND},
                    {"name": "owner", "kind": "entity", "entity_kind": PERSON_KIND},
                ],
            ),
            _fact_type(
                FACT_TYPE_GEN_ID,
                "Ordinary allocation amount keyed also on an allocation instance (A11 diagnostic)",
                [
                    {"name": "report", "kind": "entity", "entity_kind": REPORT_KIND},
                    {"name": "owner", "kind": "entity", "entity_kind": PERSON_KIND},
                    {"name": "instance", "kind": "entity", "entity_kind": INSTANCE_KIND},
                ],
            ),
        ],
    }


def _family_body() -> dict[str, Any]:
    return {
        "id": FAMILY["id"],
        "version": FAMILY["version"],
        "title": "Ordinary allocation statements (candidate 2 recording-only probe)",
        "scope": {
            "tax_year": 2025,
            "jurisdiction": "us",
            "family": "demo-allocation",
        },
        "member_predicate": {"fact_type": FACT_TYPE_ID},
    }


def _family_v2(**extra: Any) -> dict[str, Any]:
    body = {"schema": "source-family.v2", **_family_body(), **extra}
    return body


def _transition_payload(
    *,
    family: dict[str, str],
    member: dict[str, Any],
    successor_id: str,
    predecessor: str,
) -> dict[str, Any]:
    return {
        "family": family,
        "scope": SCOPE,
        "member": member,
        "successor": {"id": successor_id, "predecessor": predecessor},
    }


# ---------------------------------------------------------------------------
# Workspace fold
# ---------------------------------------------------------------------------


class Workspace:
    def __init__(self, registry: SchemaRegistry) -> None:
        self.registry = registry
        self.acts: list[dict[str, Any]] = []
        self.state = initial_state()

    def commit(self, kind: str, payload: dict[str, Any], actor: str = ACTOR) -> dict[str, Any]:
        act = _act(len(self.acts), kind, payload, actor)
        self.state = apply_act(self.state, act, self.registry)
        self.acts.append(act)
        return act

    def attempt(self, kind: str, payload: dict[str, Any], actor: str = ACTOR) -> dict[str, Any]:
        act = _act(len(self.acts), kind, payload, actor)
        try:
            new_state = apply_act(self.state, act, self.registry)
        except (FindingModelError, HorizonModelError, SchemaValidationError, KeyError) as exc:
            return {
                "accepted": False,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "act_kind": kind,
            }
        return {
            "accepted": True,
            "error_type": None,
            "error": None,
            "act_kind": kind,
            "new_withdrawn": sorted(new_state.withdrawn_fact_ids),
            "new_finding_ids": sorted(new_state.findings),
        }


def _current_findings(state) -> list[dict[str, Any]]:
    currency = compute_currency(state)
    return [
        state.findings[fid]
        for fid in sorted(currency.current_finding_ids)
        if state.findings[fid]["fact_id"].startswith(FACT_TYPE_ID + "|")
        or state.findings[fid]["fact_id"].startswith(FACT_TYPE_GEN_ID + "|")
    ]


def _current_for_fact(state, fact_id: str) -> list[dict[str, Any]]:
    currency = compute_currency(state)
    return [
        state.findings[fid]
        for fid in sorted(currency.current_finding_ids)
        if state.findings[fid]["fact_id"] == fact_id
    ]


def _join_act_for_finding(acts: list[dict[str, Any]], finding_id: str) -> dict[str, Any] | None:
    for act in acts:
        payload = act["payload"]
        finding = payload.get("finding")
        if finding is None:
            member = payload.get("member") or {}
            finding = member.get("finding")
        if finding is not None and finding.get("id") == finding_id:
            return {
                "act_id": act["act_id"],
                "kind": act["kind"],
                "actor": act["actor"],
                "at": act["at"],
                "committed_against": act["committed_against"],
            }
    return None


def _join_remove_act(acts: list[dict[str, Any]], fact_id: str) -> dict[str, Any] | None:
    for act in acts:
        if act["kind"] != "member-transition":
            continue
        member = act["payload"].get("member") or {}
        if member.get("action") == "remove" and member.get("fact_id") == fact_id:
            return {
                "act_id": act["act_id"],
                "kind": act["kind"],
                "actor": act["actor"],
                "at": act["at"],
                "committed_against": act["committed_against"],
                "successor": act["payload"]["successor"],
            }
    return None


def _current_horizon(state, family: dict[str, str]) -> str | None:
    for key, horizon_id in state.horizon_state.current_by_chain.items():
        if key[0] == family["id"] and key[1] == family["version"]:
            return horizon_id
    return None


def _current_value_repr(state, fact_id: str) -> str:
    value = _current_value_for_fact(state, fact_id)
    if value is _NO_CURRENT_VALUE:
        return "<NO_CURRENT_VALUE>"
    return repr(value)


def _emit(title: str, payload: Any) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)
    if isinstance(payload, str):
        print(payload)
        return
    # Stable, path-free dump.
    def _fmt(obj: Any, indent: int = 0) -> None:
        pad = "  " * indent
        if isinstance(obj, dict):
            for key in obj:
                value = obj[key]
                if isinstance(value, (dict, list)):
                    print(f"{pad}{key}:")
                    _fmt(value, indent + 1)
                else:
                    print(f"{pad}{key}: {value!r}")
        elif isinstance(obj, list):
            if not obj:
                print(f"{pad}[]")
                return
            for i, item in enumerate(obj):
                if isinstance(item, (dict, list)):
                    print(f"{pad}- [{i}]")
                    _fmt(item, indent + 1)
                else:
                    print(f"{pad}- {item!r}")
        else:
            print(f"{pad}{obj!r}")

    _fmt(payload)


def _validate(registry: SchemaRegistry, schema_id: str, instance: object) -> dict[str, Any]:
    try:
        registry.validate(schema_id, instance)
    except SchemaValidationError as exc:
        return {"ok": False, "schema": schema_id, "errors": list(exc.errors)}
    return {"ok": True, "schema": schema_id, "errors": []}


# ---------------------------------------------------------------------------
# Contract accounting (executed schema validation)
# ---------------------------------------------------------------------------


def probe_family_contract(registry: SchemaRegistry) -> dict[str, Any]:
    missing = _family_v2()
    missing_result = _validate(registry, "source-family.v2", missing)

    empty_filled = _family_v2(closure_claim="", authorizes_subtotal="")
    empty_result = _validate(registry, "source-family.v2", empty_filled)

    hedge = _family_v2(
        closure_claim=(
            "No completeness about the world is claimed; this family only "
            "records ordinary allocation statements as they are made."
        ),
        authorizes_subtotal="this-recording-does-not-authorize-a-subtotal",
    )
    hedge_result = _validate(registry, "source-family.v2", hedge)

    tax_shaped = _family_v2(
        closure_claim=(
            "Every ordinary allocation of Form 1099-INT interest from an "
            "identified report to a named other person is recorded."
        ),
        authorizes_subtotal="demo.allocation.subtotal",
    )
    tax_shaped_result = _validate(registry, "source-family.v2", tax_shaped)

    required = registry.get("source-family.v2")["required"]

    transition_without_successor = {
        "family": FAMILY,
        "scope": SCOPE,
        "member": {"action": "remove", "fact_id": _fact_id(REPORT_A, OWNER_PAT)},
    }
    transition_missing = _validate(
        registry, "act-member-transition.v3", transition_without_successor
    )

    transition_complete = _transition_payload(
        family=FAMILY,
        member={"action": "remove", "fact_id": _fact_id(REPORT_A, OWNER_PAT)},
        successor_id="demo.horizon.ordinary.h-remove",
        predecessor="demo.horizon.ordinary.h0",
    )
    transition_ok = _validate(registry, "act-member-transition.v3", transition_complete)

    horizon_missing_pred = {
        "schema": "family-horizon.v1",
        "id": "demo.horizon.ordinary.h1",
        "family": FAMILY,
        "scope": SCOPE,
    }
    horizon_missing = _validate(registry, "family-horizon.v1", horizon_missing_pred)

    horizon_complete = {
        "schema": "family-horizon.v1",
        "id": "demo.horizon.ordinary.h1",
        "family": FAMILY,
        "scope": SCOPE,
        "predecessor": "demo.horizon.ordinary.h0",
    }
    horizon_ok = _validate(registry, "family-horizon.v1", horizon_complete)

    result = {
        "source_family_v2_required_fields": list(required),
        "missing_closure_and_subtotal": missing_result,
        "empty_string_closure_and_subtotal": empty_result,
        "hedged_recording_only_wording": hedge_result,
        "completeness_and_subtotal_wording": tax_shaped_result,
        "transition_missing_successor": transition_missing,
        "transition_with_successor": transition_ok,
        "horizon_missing_predecessor": horizon_missing,
        "horizon_with_predecessor": horizon_ok,
    }
    _emit("CONTRACT. source-family.v2 / act-member-transition.v3 / family-horizon.v1", result)
    return result


# ---------------------------------------------------------------------------
# Kernel lifecycle
# ---------------------------------------------------------------------------


def _open_ordinary(registry: SchemaRegistry) -> Workspace:
    ws = Workspace(registry)
    ws.commit("bundle-adoption", {"bundle": _bundle()})
    for entity_id, kind, label in (
        (REPORT_A, REPORT_KIND, f"Form 1099-INT report A from {PAYER}"),
        (REPORT_B, REPORT_KIND, f"Form 1099-INT report B from {PAYER}"),
        (OWNER_PAT, PERSON_KIND, "Pat (synthetic other person)"),
        (OWNER_KIM, PERSON_KIND, "Kim (synthetic other person)"),
    ):
        ws.commit("entity-introduced", {"entity": _entity(entity_id, kind, label)})
    ws.commit(
        "horizon-genesis",
        {"family": FAMILY, "scope": SCOPE, "horizon_id": "demo.horizon.ordinary.h0"},
    )
    return ws


def _add_member(
    ws: Workspace,
    *,
    finding_id: str,
    fact_id: str,
    value: Any,
    successor_id: str,
    predecessor: str,
    family: dict[str, str] = FAMILY,
) -> dict[str, Any]:
    return ws.commit(
        "member-transition",
        _transition_payload(
            family=family,
            member={"action": "assert", "finding": _finding(finding_id, fact_id, value)},
            successor_id=successor_id,
            predecessor=predecessor,
        ),
    )


def _remove_member(
    ws: Workspace,
    *,
    fact_id: str,
    successor_id: str,
    predecessor: str,
    family: dict[str, str] = FAMILY,
) -> dict[str, Any]:
    return ws.commit(
        "member-transition",
        _transition_payload(
            family=family,
            member={"action": "remove", "fact_id": fact_id},
            successor_id=successor_id,
            predecessor=predecessor,
        ),
    )


def _snapshot(ws: Workspace, label: str) -> dict[str, Any]:
    currency = compute_currency(ws.state)
    current = _current_findings(ws.state)
    snap = {
        "label": label,
        "n_acts": len(ws.acts),
        "act_ids": [a["act_id"] for a in ws.acts],
        "withdrawn_fact_ids": sorted(ws.state.withdrawn_fact_ids),
        "all_finding_ids": sorted(ws.state.findings),
        "all_finding_values": {
            fid: {"fact_id": f["fact_id"], "value": f["value"], "basis": f["basis"]}
            for fid, f in sorted(ws.state.findings.items())
        },
        "current_finding_ids": sorted(currency.current_finding_ids),
        "displaced_finding_ids": sorted(currency.displaced_finding_ids),
        "current_allocations": [
            {
                "finding_id": f["id"],
                "fact_id": f["fact_id"],
                "value": f["value"],
                "supporting_act": _join_act_for_finding(ws.acts, f["id"]),
            }
            for f in current
        ],
        "current_horizon": _current_horizon(ws.state, FAMILY),
        "horizon_ids": sorted(ws.state.horizon_state.horizons),
        "pat_a_current_value": _current_value_repr(ws.state, _fact_id(REPORT_A, OWNER_PAT)),
        "kim_a_current_value": _current_value_repr(ws.state, _fact_id(REPORT_A, OWNER_KIM)),
        "pat_b_current_value": _current_value_repr(ws.state, _fact_id(REPORT_B, OWNER_PAT)),
    }
    _emit(f"SNAPSHOT. {label}", snap)
    return snap


def probe_lifecycle(registry: SchemaRegistry) -> dict[str, Any]:
    pat_a = _fact_id(REPORT_A, OWNER_PAT)
    kim_a = _fact_id(REPORT_A, OWNER_KIM)
    pat_b = _fact_id(REPORT_B, OWNER_PAT)
    results: dict[str, Any] = {
        "fact_ids": {"pat_a": pat_a, "kim_a": kim_a, "pat_b": pat_b},
    }

    ws = _open_ordinary(registry)

    # --- SC-R1 on first entry: plain assertion must be refused ---
    scr1_first = ws.attempt(
        "assertion",
        {"finding": _finding("demo.finding.pat.a.illicit-plain", pat_a, 450)},
    )
    results["SC-R1_plain_assertion_before_membership"] = scr1_first
    _emit("CLAIM. SC-R1 first entry (plain assertion of never-member fact)", scr1_first)

    # --- A2: one owner records via member-transition ---
    add_pat = _add_member(
        ws,
        finding_id="demo.finding.pat.a.v1",
        fact_id=pat_a,
        value=450,
        successor_id="demo.horizon.ordinary.h1",
        predecessor="demo.horizon.ordinary.h0",
    )
    snap_a2 = _snapshot(ws, "A2 after Pat $450 on report A")
    a2_current = snap_a2["current_allocations"]
    a2_pass = (
        len(a2_current) == 1
        and a2_current[0]["fact_id"] == pat_a
        and a2_current[0]["value"] == 450
        and a2_current[0]["supporting_act"]["actor"] == ACTOR
        and a2_current[0]["supporting_act"]["kind"] == "member-transition"
        and REPORT_A in a2_current[0]["fact_id"]
        and REPORT_B not in a2_current[0]["fact_id"]
        and snap_a2["pat_a_current_value"] == "450"
        and snap_a2["kim_a_current_value"] == "<NO_CURRENT_VALUE>"
    )
    results["A2"] = {
        "status": "PASS" if a2_pass else "FAIL",
        "add_act_id": add_pat["act_id"],
        "current_allocations": a2_current,
        "pat_a_current_value": snap_a2["pat_a_current_value"],
    }
    _emit("A2 result", results["A2"])

    # --- A3: add Kim; correct Pat 450 -> 300 so the A3 amounts match the plan ---
    add_kim = _add_member(
        ws,
        finding_id="demo.finding.kim.a.v1",
        fact_id=kim_a,
        value=150,
        successor_id="demo.horizon.ordinary.h2",
        predecessor="demo.horizon.ordinary.h1",
    )
    kim_finding_obj = ws.state.findings["demo.finding.kim.a.v1"]
    kim_python_id_before = id(kim_finding_obj)
    kim_revision_before = _join_act_for_finding(ws.acts, "demo.finding.kim.a.v1")

    # Same-member correction of Pat belongs on the ordinary assertion path (SC-R2).
    scr2 = ws.attempt(
        "member-transition",
        _transition_payload(
            family=FAMILY,
            member={
                "action": "assert",
                "finding": _finding("demo.finding.pat.a.illicit-transition-corr", pat_a, 300),
            },
            successor_id="demo.horizon.ordinary.h-scr2",
            predecessor="demo.horizon.ordinary.h2",
        ),
    )
    results["SC-R2_same_member_via_transition"] = scr2
    _emit("CLAIM. SC-R2 same-member correction via member-transition", scr2)

    corr_pat_300 = ws.commit(
        "assertion",
        {"finding": _finding("demo.finding.pat.a.v2", pat_a, 300)},
    )
    snap_a3 = _snapshot(ws, "A3 Pat $300 and Kim $150 on report A")
    a3_facts = sorted(f["fact_id"] for f in snap_a3["current_allocations"])
    a3_values = {f["fact_id"]: f["value"] for f in snap_a3["current_allocations"]}
    a3_pass = (
        a3_facts == sorted([pat_a, kim_a])
        and a3_values[pat_a] == 300
        and a3_values[kim_a] == 150
        and snap_a3["current_horizon"] == "demo.horizon.ordinary.h2"
        # Correction of Pat did not mint a horizon (assertion path).
        and corr_pat_300["kind"] == "assertion"
    )
    results["A3"] = {
        "status": "PASS" if a3_pass else "FAIL",
        "current_allocations": snap_a3["current_allocations"],
        "distinct_fact_ids": a3_facts,
        "kim_add_act_id": add_kim["act_id"],
        "pat_correction_act_id": corr_pat_300["act_id"],
        "horizon_unchanged_by_pat_value_correction": snap_a3["current_horizon"],
    }
    _emit("A3 result", results["A3"])

    # --- A4: correct Pat 300 -> 250; Kim record identity must not change ---
    corr_pat_250 = ws.commit(
        "assertion",
        {"finding": _finding("demo.finding.pat.a.v3", pat_a, 250)},
    )
    snap_a4 = _snapshot(ws, "A4 after Pat corrected to $250")
    kim_after = ws.state.findings.get("demo.finding.kim.a.v1")
    kim_python_id_after = id(kim_after) if kim_after is not None else None
    kim_revision_after = _join_act_for_finding(ws.acts, "demo.finding.kim.a.v1")
    acts_on_kim = [
        a["act_id"]
        for a in ws.acts
        if _join_act_for_finding([a], "demo.finding.kim.a.v1") is not None
        or (
            a["kind"] == "member-transition"
            and (a["payload"].get("member") or {}).get("fact_id") == kim_a
        )
    ]
    kim_current = _current_for_fact(ws.state, kim_a)
    a4_pass = (
        kim_after is kim_finding_obj
        and kim_python_id_before == kim_python_id_after
        and kim_revision_before == kim_revision_after
        and len(kim_current) == 1
        and kim_current[0]["id"] == "demo.finding.kim.a.v1"
        and kim_current[0]["value"] == 150
        and acts_on_kim == [add_kim["act_id"]]
        and corr_pat_250["act_id"] not in acts_on_kim
        and snap_a4["pat_a_current_value"] == "250"
    )
    results["A4"] = {
        "status": "PASS" if a4_pass else "FAIL",
        "kim_finding_id_before": "demo.finding.kim.a.v1",
        "kim_finding_id_after": kim_after["id"] if kim_after else None,
        "kim_python_id_before": kim_python_id_before,
        "kim_python_id_after": kim_python_id_after,
        "kim_same_object": kim_after is kim_finding_obj,
        "kim_supporting_act_before": kim_revision_before,
        "kim_supporting_act_after": kim_revision_after,
        "acts_whose_payload_names_kim_finding_or_fact": acts_on_kim,
        "pat_new_finding_id": "demo.finding.pat.a.v3",
        "pat_new_act_id": corr_pat_250["act_id"],
        "pat_prior_finding_still_stored": "demo.finding.pat.a.v2" in ws.state.findings,
        "pat_prior_finding_current": "demo.finding.pat.a.v2"
        in compute_currency(ws.state).current_finding_ids,
    }
    _emit("A4 result (record identity, not value equality)", results["A4"])

    # --- A5: report B shares the payer; allocation on A must not attach to B ---
    snap_a5 = snap_a4
    current_fact_ids = [f["fact_id"] for f in snap_a5["current_allocations"]]
    a5_pass = (
        pat_b not in current_fact_ids
        and all(REPORT_B not in fid for fid in current_fact_ids)
        and all(REPORT_A in fid for fid in current_fact_ids)
        and snap_a5["pat_b_current_value"] == "<NO_CURRENT_VALUE>"
        and pat_a != pat_b
    )
    results["A5"] = {
        "status": "PASS" if a5_pass else "FAIL",
        "pat_a_fact_id": pat_a,
        "pat_b_fact_id": pat_b,
        "ids_differ": pat_a != pat_b,
        "current_fact_ids": current_fact_ids,
        "pat_b_current_value": snap_a5["pat_b_current_value"],
        "report_b_entity_present": REPORT_B in ws.state.fact_state.entities,
    }
    _emit("A5 result", results["A5"])

    withdrawn_before_a6 = frozenset(ws.state.withdrawn_fact_ids)
    findings_before_a6 = dict(ws.state.findings)
    pat_values_before = [
        f["value"]
        for f in ws.state.findings.values()
        if f["fact_id"] == pat_a
    ]

    # --- A6: withdraw Pat ---
    remove_pat = _remove_member(
        ws,
        fact_id=pat_a,
        successor_id="demo.horizon.ordinary.h3",
        predecessor="demo.horizon.ordinary.h2",
    )
    snap_a6 = _snapshot(ws, "A6 after withdrawing Pat on report A")
    pat_findings_after = [
        {"id": f["id"], "value": f["value"], "basis": f["basis"]}
        for f in ws.state.findings.values()
        if f["fact_id"] == pat_a
    ]
    authored_zero_or_false = [
        f
        for f in pat_findings_after
        if f["value"] in (0, 0.0, False, "false")
    ]
    history_deleted = any(
        fid not in ws.state.findings for fid in findings_before_a6
    )
    kim_still = _current_for_fact(ws.state, kim_a)
    remove_join = _join_remove_act(ws.acts, pat_a)
    a6_pass = (
        snap_a6["pat_a_current_value"] == "<NO_CURRENT_VALUE>"
        and pat_a in ws.state.withdrawn_fact_ids
        and not authored_zero_or_false
        and not history_deleted
        and all(fid in ws.state.findings for fid in findings_before_a6)
        and pat_values_before == [f["value"] for f in pat_findings_after]
        and len(kim_still) == 1
        and kim_still[0]["id"] == "demo.finding.kim.a.v1"
        and kim_still[0] is kim_finding_obj
        and remove_join is not None
        and remove_join["actor"] == ACTOR
        and withdrawn_before_a6.issubset(ws.state.withdrawn_fact_ids)
        and pat_a not in withdrawn_before_a6
    )
    results["A6"] = {
        "status": "PASS" if a6_pass else "FAIL",
        "remove_act": remove_join,
        "withdrawn_fact_ids_before": sorted(withdrawn_before_a6),
        "withdrawn_fact_ids_after": sorted(ws.state.withdrawn_fact_ids),
        "pat_findings_still_stored": pat_findings_after,
        "authored_zero_or_false_or_opposite": authored_zero_or_false,
        "history_deleted": history_deleted,
        "pat_a_current_value": snap_a6["pat_a_current_value"],
        "kim_current_finding_id": kim_still[0]["id"] if kim_still else None,
        "kim_same_object_after_withdraw": bool(kim_still) and kim_still[0] is kim_finding_obj,
        "remove_did_not_write_a_finding": "finding"
        not in (remove_pat["payload"].get("member") or {}),
    }
    _emit("A6 result", results["A6"])

    # --- Kernel claims, executed on this state ---
    withdrawn_ids = set(ws.state.withdrawn_fact_ids)
    current_value_pat = _current_value_for_fact(ws.state, pat_a)
    current_value_kim = _current_value_for_fact(ws.state, kim_a)
    # Unconditional: every withdrawn id has no current value, including ones
    # that still have stored findings.
    withdrawn_current_values = {
        fid: _current_value_repr(ws.state, fid) for fid in sorted(withdrawn_ids)
    }

    results["CLAIM_monotonic_union_at_A6"] = {
        "before": sorted(withdrawn_before_a6),
        "after": sorted(ws.state.withdrawn_fact_ids),
        "grew_by_union_with_pat_a": ws.state.withdrawn_fact_ids
        == withdrawn_before_a6 | {pat_a},
        "nothing_subtracted": withdrawn_before_a6.issubset(ws.state.withdrawn_fact_ids),
    }
    results["CLAIM_current_value_for_withdrawn"] = {
        "pat_a_is_sentinel": current_value_pat is _NO_CURRENT_VALUE,
        "kim_a_is_150": current_value_kim == 150,
        "every_withdrawn_id": withdrawn_current_values,
    }

    second_remove = ws.attempt(
        "member-transition",
        _transition_payload(
            family=FAMILY,
            member={"action": "remove", "fact_id": pat_a},
            successor_id="demo.horizon.ordinary.h-second-remove",
            predecessor="demo.horizon.ordinary.h3",
        ),
    )
    results["CLAIM_second_withdrawal_of_same_id"] = second_remove
    _emit("CLAIM. second remove of the same withdrawn fact id", second_remove)

    # --- A11 attempts ---
    a11_plain = ws.attempt(
        "assertion",
        {"finding": _finding("demo.finding.pat.a.v4-plain", pat_a, 250)},
    )
    results["A11_path_plain_assertion_same_fact_id"] = a11_plain
    _emit("A11 path 1. plain assertion of withdrawn (report, owner) fact id", a11_plain)

    a11_transition = ws.attempt(
        "member-transition",
        _transition_payload(
            family=FAMILY,
            member={
                "action": "assert",
                "finding": _finding("demo.finding.pat.a.v4-transition", pat_a, 250),
            },
            successor_id="demo.horizon.ordinary.h4",
            predecessor="demo.horizon.ordinary.h3",
        ),
    )
    results["A11_path_member_transition_same_fact_id"] = a11_transition
    _emit(
        "A11 path 2. member-transition assert of withdrawn (report, owner) fact id",
        a11_transition,
    )

    # If the transition write was accepted, fold it in so we can observe
    # currency and monotonicity on the resulting state. A11 asks whether
    # the proposition can become *current* again, not merely whether a
    # finding dict can be stored.
    a11_after_write: dict[str, Any] | None = None
    if a11_transition.get("accepted"):
        write_act = ws.commit(
            "member-transition",
            _transition_payload(
                family=FAMILY,
                member={
                    "action": "assert",
                    "finding": _finding("demo.finding.pat.a.v4-transition", pat_a, 250),
                },
                successor_id="demo.horizon.ordinary.h4",
                predecessor="demo.horizon.ordinary.h3",
            ),
        )
        snap_a11 = _snapshot(ws, "A11 after member-transition re-assert of SAME fact id")
        a11_after_write = {
            "write_act_id": write_act["act_id"],
            "new_finding_stored": "demo.finding.pat.a.v4-transition" in ws.state.findings,
            "new_finding_value": ws.state.findings.get(
                "demo.finding.pat.a.v4-transition", {}
            ).get("value"),
            "pat_a_still_in_withdrawn_fact_ids": pat_a in ws.state.withdrawn_fact_ids,
            "withdrawn_fact_ids": sorted(ws.state.withdrawn_fact_ids),
            "pat_a_current_value": snap_a11["pat_a_current_value"],
            "new_finding_in_current": "demo.finding.pat.a.v4-transition"
            in compute_currency(ws.state).current_finding_ids,
            "new_finding_in_displaced": "demo.finding.pat.a.v4-transition"
            in compute_currency(ws.state).displaced_finding_ids,
            "current_allocations": snap_a11["current_allocations"],
        }
        results["A11_after_same_id_write"] = a11_after_write
        _emit("A11 path 2b. state after the same-id write was folded", a11_after_write)

    same_id_became_current = (
        a11_after_write is not None
        and a11_after_write["pat_a_current_value"] != "<NO_CURRENT_VALUE>"
        and a11_after_write["new_finding_in_current"]
    )
    results["A11"] = {
        "status": "PASS" if same_id_became_current else "FAIL",
        "plain_assertion_accepted": bool(a11_plain.get("accepted")),
        "member_transition_write_accepted": bool(a11_transition.get("accepted")),
        "same_fact_id_became_current": same_id_became_current,
        "note": (
            "A11 on this route with the same (report, owner) fact id is the "
            "only identity that preserves A4's per-owner key. See diagnostic "
            "workspace for a different-fact-id alternative."
        ),
    }
    _emit("A11 result", results["A11"])
    _emit("CLAIM. monotonic withdrawn_fact_ids", results["CLAIM_monotonic_union_at_A6"])
    _emit(
        "CLAIM. _current_value_for_fact on withdrawn ids",
        results["CLAIM_current_value_for_withdrawn"],
    )

    results["history_attribution_coupling"] = {
        "findings_retained_ids": sorted(ws.state.findings),
        "acts_retained_ids": [a["act_id"] for a in ws.acts],
        "horizon_chain": [
            {
                "id": hid,
                "status": ws.state.horizon_state.horizons[hid].status,
                "predecessor": ws.state.horizon_state.horizons[hid].horizon["predecessor"],
                "successor_id": ws.state.horizon_state.horizons[hid].successor_id,
            }
            for hid in sorted(ws.state.horizon_state.horizons)
        ],
        "attribution_join": (
            "finding.id -> act.payload.finding.id (assertion) or "
            "act.payload.member.finding.id (member-transition assert); "
            "actor and at live on the act envelope, not the finding. "
            "Withdrawal authorship is the member-transition remove act "
            "joined by payload.member.fact_id."
        ),
        "owners_share_one_horizon_chain": True,
        "current_horizon_after_pat_withdraw_or_reassert": _current_horizon(
            ws.state, FAMILY
        ),
        "kim_fact_id_never_equals_pat_fact_id": kim_a != pat_a,
    }
    _emit("History, attribution, coupling", results["history_attribution_coupling"])
    return results


def probe_instanced_a11(registry: SchemaRegistry) -> dict[str, Any]:
    """Diagnostic: can A11 succeed if identity is (report, owner, instance)?"""
    registry.family_member_predicates.add(FACT_TYPE_GEN_ID)
    ws = Workspace(registry)
    ws.commit("bundle-adoption", {"bundle": _bundle()})
    inst_1 = "demo.allocation.instance.1"
    inst_2 = "demo.allocation.instance.2"
    inst_kim = "demo.allocation.instance.kim"
    for entity_id, kind, label in (
        (REPORT_A, REPORT_KIND, f"Form 1099-INT report A from {PAYER}"),
        (OWNER_PAT, PERSON_KIND, "Pat (synthetic other person)"),
        (OWNER_KIM, PERSON_KIND, "Kim (synthetic other person)"),
        (inst_1, INSTANCE_KIND, "Pat allocation instance 1"),
        (inst_2, INSTANCE_KIND, "Pat allocation instance 2"),
        (inst_kim, INSTANCE_KIND, "Kim allocation instance 1"),
    ):
        ws.commit("entity-introduced", {"entity": _entity(entity_id, kind, label)})
    ws.commit(
        "horizon-genesis",
        {
            "family": FAMILY_GEN,
            "scope": SCOPE,
            "horizon_id": "demo.horizon.instanced.h0",
        },
    )
    pat_1 = _gen_fact_id(REPORT_A, OWNER_PAT, inst_1)
    pat_2 = _gen_fact_id(REPORT_A, OWNER_PAT, inst_2)
    kim_1 = _gen_fact_id(REPORT_A, OWNER_KIM, inst_kim)
    _add_member(
        ws,
        finding_id="demo.finding.gen.pat.1",
        fact_id=pat_1,
        value=300,
        successor_id="demo.horizon.instanced.h1",
        predecessor="demo.horizon.instanced.h0",
        family=FAMILY_GEN,
    )
    _add_member(
        ws,
        finding_id="demo.finding.gen.kim.1",
        fact_id=kim_1,
        value=150,
        successor_id="demo.horizon.instanced.h2",
        predecessor="demo.horizon.instanced.h1",
        family=FAMILY_GEN,
    )
    kim_obj = ws.state.findings["demo.finding.gen.kim.1"]
    ws.commit(
        "assertion",
        {"finding": _finding("demo.finding.gen.pat.1.corr", pat_1, 250)},
    )
    kim_after_corr = ws.state.findings["demo.finding.gen.kim.1"]
    _remove_member(
        ws,
        fact_id=pat_1,
        successor_id="demo.horizon.instanced.h3",
        predecessor="demo.horizon.instanced.h2",
        family=FAMILY_GEN,
    )
    _add_member(
        ws,
        finding_id="demo.finding.gen.pat.2",
        fact_id=pat_2,
        value=250,
        successor_id="demo.horizon.instanced.h4",
        predecessor="demo.horizon.instanced.h3",
        family=FAMILY_GEN,
    )
    currency = compute_currency(ws.state)
    current = [
        {
            "finding_id": ws.state.findings[fid]["id"],
            "fact_id": ws.state.findings[fid]["fact_id"],
            "value": ws.state.findings[fid]["value"],
        }
        for fid in sorted(currency.current_finding_ids)
        if ws.state.findings[fid]["fact_id"].startswith(FACT_TYPE_GEN_ID + "|")
    ]
    result = {
        "pat_instance_1_fact_id": pat_1,
        "pat_instance_2_fact_id": pat_2,
        "kim_instance_1_fact_id": kim_1,
        "fact_ids_differ": pat_1 != pat_2,
        "kim_same_object_after_pat_correction": kim_after_corr is kim_obj,
        "pat_1_withdrawn": pat_1 in ws.state.withdrawn_fact_ids,
        "pat_2_withdrawn": pat_2 in ws.state.withdrawn_fact_ids,
        "pat_1_current_value": _current_value_repr(ws.state, pat_1),
        "pat_2_current_value": _current_value_repr(ws.state, pat_2),
        "kim_current_value": _current_value_repr(ws.state, kim_1),
        "current_instanced_allocations": current,
        "per_owner_identity_is_no_longer_report_plus_owner": True,
        "two_pat_fact_ids_exist_for_same_report_and_owner": True,
    }
    _emit("A11 diagnostic. instanced identity (report, owner, instance)", result)
    return result


def main() -> int:
    registry = SchemaRegistry([KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR])
    # Mirror packages/tax/loader.py:tax_registry — an adopted family's
    # member_predicate fact type is what arms SC-R1.
    registry.family_member_predicates.add(FACT_TYPE_ID)

    print("CANDIDATE 2 PROBE")
    print("route: adopted source family + act-member-transition.v3")
    print(f"actor: {ACTOR}")
    print(f"family: {FAMILY['id']} {FAMILY['version']}")
    print(f"member fact type: {FACT_TYPE_ID}")
    print("identities: demo.* only")

    contract = probe_family_contract(registry)
    life = probe_lifecycle(registry)
    instanced = probe_instanced_a11(registry)

    print()
    print("=" * 72)
    print("CASE STATUS SUMMARY")
    print("=" * 72)
    for case in ("A2", "A3", "A4", "A5", "A6", "A11"):
        print(f"{case}: {life[case]['status']}")
    print(
        "SC-R1 first entry refused:",
        not life["SC-R1_plain_assertion_before_membership"]["accepted"],
        life["SC-R1_plain_assertion_before_membership"]["error"],
    )
    print(
        "SC-R1 after withdraw refused:",
        not life["A11_path_plain_assertion_same_fact_id"]["accepted"],
        life["A11_path_plain_assertion_same_fact_id"]["error"],
    )
    print(
        "monotonic union at A6:",
        life["CLAIM_monotonic_union_at_A6"]["grew_by_union_with_pat_a"],
    )
    print(
        "withdrawn fact has no current value:",
        life["CLAIM_current_value_for_withdrawn"]["pat_a_is_sentinel"],
    )
    print(
        "source-family.v2 required:",
        contract["source_family_v2_required_fields"],
    )
    print(
        "family missing closure/subtotal ok?:",
        contract["missing_closure_and_subtotal"]["ok"],
        contract["missing_closure_and_subtotal"]["errors"],
    )
    print(
        "hedged recording-only wording schema-ok?:",
        contract["hedged_recording_only_wording"]["ok"],
    )
    print(
        "instanced A11 pat_2 current value:",
        instanced["pat_2_current_value"],
    )
    print(
        "instanced A11 pat_1 current value:",
        instanced["pat_1_current_value"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
