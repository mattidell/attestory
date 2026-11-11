"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from seed_helpers.repo_root import repo_root

import json
from typing import cast

REPO = repo_root()

CONTENT = REPO / "packages" / "content" / "tax" / "2025"

T3 = REPO / "packages" / "sample_data" / "frrs_t3"

USER = "demo.user.filer-1"

C1 = "tax.us.2025.exception1.only-box2a-capital-gains"

C2 = "tax.us.2025.exception1.no-capital-losses"

C3 = "tax.us.2025.exception1.no-qof-deferral"

C4 = "tax.us.2025.exception1.no-boxes-2b-2c-2d"

CG_DIST = "tax.us.2025.capital-gain-distributions"

def _act(name: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads((T3 / "adoptions" / name).read_text("utf-8")))

def _live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.cgd.t2.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-07-30T00:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }

def _attested(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }

def _cgd_t2_acts(
    *,
    wages: float = 90000,
    box1a: float | None = 600,
    box1b: float | None = 0,
    box2a: float | None = 1500,
    close_2a: bool = True,
    components: dict[str, str | None] | None = None,
    cg_dist: str | None = "yes",
    multi_payer_box2a: list[float] | None = None,
    c4_successor: str | None = None,
) -> list[dict[str, object]]:
    if components is None:
        components = {"C1": "yes", "C2": "yes", "C3": "yes", "C4": "yes"}
    acts: list[dict[str, object]] = []

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_live_act(len(acts), kind, payload))

    for name in (
        "w2.bundle.v3.json",
        "f1099int.bundle.json",
        "interest_composition.bundle.json",
        "core_calculations.bundle.v2.json",
        "f1099div.bundle.v2.json",
        "f1099div-box2a.bundle.json",
        "exception1.bundle.json",
        "qdcg.bundle.json",
    ):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text())})

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.employer", "kind": "tax.us.employer", "label": "Synthetic employer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.w2", "kind": "tax.us.w2-slip", "label": "Synthetic W-2"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.payer", "kind": "tax.us.dividend-payer", "label": "Synthetic payer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.stmt", "kind": "tax.us.1099div-statement", "label": "Synthetic 1099-DIV"}})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = (
        ("tax.us.2025.w2", "v2", "demo.cgd.t2.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.cgd.t2.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.cgd.t2.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.cgd.t2.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.cgd.t2.nonform.h0"),
        ("tax.us.2025.f1099div.1a", "v1", "demo.cgd.t2.div1a.h0"),
        ("tax.us.2025.f1099div.1b", "v1", "demo.cgd.t2.div1b.h0"),
        ("tax.us.2025.f1099div.2a", "v1", "demo.cgd.t2.div2a.h0"),
    )
    for family_id, version, horizon_id in families:
        add("horizon-genesis", {"family": {"id": family_id, "version": version}, "scope": scope, "horizon_id": horizon_id})

    w2_horizon = "demo.cgd.t2.w2.h0"
    if wages:
        add("member-transition", {
            "family": {"id": "tax.us.2025.w2", "version": "v2"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.cgd.t2.finding.wages",
                "tax.us.2025.w2.box1-wages|employer=demo.cgd.t2.employer,w2-slip=demo.cgd.t2.w2,tax-year=2025",
                wages,
            )},
            "successor": {"id": "demo.cgd.t2.w2.h1", "predecessor": w2_horizon},
        })
        w2_horizon = "demo.cgd.t2.w2.h1"

    def _div_member(fact_type: str, family_id: str, predecessor: str, successor: str, value: float, finding_id: str) -> None:
        add("member-transition", {
            "family": {"id": family_id, "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                finding_id,
                f"{fact_type}|payer=demo.cgd.t2.payer,statement=demo.cgd.t2.stmt,tax-year=2025",
                value,
            )},
            "successor": {"id": successor, "predecessor": predecessor},
        })

    div1a_horizon = "demo.cgd.t2.div1a.h0"
    if box1a is not None:
        _div_member(
            "tax.us.2025.f1099div.box1a-ordinary", "tax.us.2025.f1099div.1a",
            div1a_horizon, "demo.cgd.t2.div1a.h1", box1a, "demo.cgd.t2.finding.box1a",
        )
        div1a_horizon = "demo.cgd.t2.div1a.h1"

    div1b_horizon = "demo.cgd.t2.div1b.h0"
    if box1b is not None and box1b != 0:
        _div_member(
            "tax.us.2025.f1099div.box1b-qualified", "tax.us.2025.f1099div.1b",
            div1b_horizon, "demo.cgd.t2.div1b.h1", box1b, "demo.cgd.t2.finding.box1b",
        )
        div1b_horizon = "demo.cgd.t2.div1b.h1"

    div2a_horizon = "demo.cgd.t2.div2a.h0"
    if multi_payer_box2a is not None:
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.payer-b", "kind": "tax.us.dividend-payer", "label": "Payer B"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.stmt-b", "kind": "tax.us.1099div-statement", "label": "Stmt B"}})
        pairs = [
            ("demo.cgd.t2.payer", "demo.cgd.t2.stmt"),
            ("demo.cgd.t2.payer-b", "demo.cgd.t2.stmt-b"),
        ]
        for i, amount in enumerate(multi_payer_box2a):
            payer, stmt = pairs[i]
            succ = f"demo.cgd.t2.div2a.h{i + 1}"
            add("member-transition", {
                "family": {"id": "tax.us.2025.f1099div.2a", "version": "v1"},
                "scope": scope,
                "member": {"action": "assert", "finding": _attested(
                    f"demo.cgd.t2.finding.box2a.{i}",
                    f"tax.us.2025.f1099div.box2a-capital-gain-distribution|payer={payer},statement={stmt},tax-year=2025",
                    amount,
                )},
                "successor": {"id": succ, "predecessor": div2a_horizon},
            })
            div2a_horizon = succ
    elif box2a is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099div.2a", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.cgd.t2.finding.box2a",
                "tax.us.2025.f1099div.box2a-capital-gain-distribution|payer=demo.cgd.t2.payer,statement=demo.cgd.t2.stmt,tax-year=2025",
                box2a,
            )},
            "successor": {"id": "demo.cgd.t2.div2a.h1", "predecessor": div2a_horizon},
        })
        div2a_horizon = "demo.cgd.t2.div2a.h1"

    add("assertion", {"finding": _attested("demo.cgd.t2.finding.rounding", "rounding.convention|tax-year=2025", "half_up")})
    add("assertion", {"finding": _attested("demo.cgd.t2.finding.status", "tax.us.2025.filing-status|tax-year=2025", "single")})

    component_facts = {
        "C1": (C1, "demo.cgd.t2.finding.c1"),
        "C2": (C2, "demo.cgd.t2.finding.c2"),
        "C3": (C3, "demo.cgd.t2.finding.c3"),
        "C4": (C4, "demo.cgd.t2.finding.c4"),
    }
    for alias, value in components.items():
        if value is None:
            continue
        fact_type, fid = component_facts[alias]
        add("assertion", {"finding": _attested(fid, f"{fact_type}|tax-year=2025", value)})
    if c4_successor is not None:
        add("assertion", {"finding": _attested(
            "demo.cgd.t2.finding.c4.v2", f"{C4}|tax-year=2025", c4_successor,
        )})

    if cg_dist is not None:
        add("assertion", {"finding": _attested("demo.cgd.t2.finding.cg-dist", f"{CG_DIST}|tax-year=2025", cg_dist)})

    closures = [
        ("demo.cgd.t2.closure.w2", "tax.us.2025.w2.source-closure", w2_horizon),
        ("demo.cgd.t2.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure", "demo.cgd.t2.int-b1.h0"),
        ("demo.cgd.t2.closure.int-b3", "tax.us.2025.f1099int.b3.source-closure", "demo.cgd.t2.int-b3.h0"),
        ("demo.cgd.t2.closure.oid-b1", "tax.us.2025.f1099oid.b1.source-closure", "demo.cgd.t2.oid-b1.h0"),
        ("demo.cgd.t2.closure.nonform", "tax.us.2025.non-form-interest.source-closure", "demo.cgd.t2.nonform.h0"),
        ("demo.cgd.t2.closure.div1a", "tax.us.2025.f1099div.1a.source-closure", div1a_horizon),
        ("demo.cgd.t2.closure.div1b", "tax.us.2025.f1099div.1b.source-closure", div1b_horizon),
    ]
    if close_2a:
        closures.append(("demo.cgd.t2.closure.div2a", "tax.us.2025.f1099div.2a.source-closure", div2a_horizon))
    for finding_id, fact_type, horizon_id in closures:
        add("assertion", {"finding": _attested(finding_id, f"{fact_type}|family-horizon={horizon_id},tax-year=2025", True)})

    adoption = _act("adopt-core-v7-current.json")
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts
