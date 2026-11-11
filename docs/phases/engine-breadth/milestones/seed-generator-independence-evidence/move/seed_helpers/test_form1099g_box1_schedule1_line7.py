"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from seed_helpers.repo_root import repo_root

import json
from typing import Any
from typing import cast
from packages.tax.loader import TAX_CONTENT_DIR
from seed_helpers.test_capital_gain_distributions_line7a_t2_coordinator import _cgd_t2_acts

ROOT = repo_root()

CONTENT = TAX_CONTENT_DIR

FIXTURES = ROOT / "packages" / "sample_data" / "form1099g_box1_schedule1_line7"

USER = "demo.user.filer-1"

SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

BOX1_AMOUNT = "tax.us.2025.f1099g.box1-unemployment"

BOX1_CLOSURE = "tax.us.2025.f1099g.1.source-closure"

BOX1_FAMILY = "tax.us.2025.f1099g.1"

BOX4_AUTH = "tax.us.2025.f1099g.box4-federal-withholding-authority"

SCOPE_TOKENS = (
    "no-sch1-line1-taxable-refunds",
    "no-sch1-line2a-alimony",
    "no-sch1-line3-business",
    "no-sch1-line4-other-gains",
    "no-sch1-line5-rental",
    "no-sch1-line6-farm",
    "no-sch1-other-income",
    "no-unemployment-repayment",
    "no-f1099g-box2-state-refund",
    "no-f1099g-other-payment-classes",
)

def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))

def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.ug.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-08-05T12:{index // 60:02d}:{index % 60:02d}Z",
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

def _scope_id(token: str) -> str:
    return f"tax.us.2025.schedule1-part1-scope.{token}"

def _ug_acts(
    *,
    box1_values: list[float] | None = None,
    box4_values: list[object] | None = None,
    close_box1: bool = True,
    scope: dict[str, str] | None = None,
    wages: float = 90000,
    box1a: float | None = 0,
    box1b: float | None = 0,
    box2a: float | None = None,
    include_box4: bool = True,
    same_payer_two_statements: bool = False,
    wash_sale_version: str = "v1",
) -> list[dict[str, object]]:
    """Build a production-shaped act log on the v20 route with box-1 facts."""
    box1_values = [2500.0] if box1_values is None else box1_values
    if box4_values is None:
        box4_values = [None] * max(1, len(box1_values) if box1_values else 1)
    scope_vals = {token: "yes" for token in SCOPE_TOKENS}
    if scope:
        scope_vals.update(scope)

    acts = _cgd_t2_acts(
        wages=wages,
        box1a=box1a if box1a else None,
        box1b=box1b if box1b else 0,
        box2a=box2a,
        close_2a=True,
        cg_dist="no" if box2a is None else "yes",
        components={"C1": "yes", "C2": "yes", "C3": "yes", "C4": "yes"},
    )
    acts.pop()  # drop historical package adoption

    # Residual-free box2a vocabulary for exclusive package graph (same as box-12 tests).
    for act in acts:
        if act["kind"] == "bundle-adoption":
            payload = cast(dict[str, object], act["payload"])
            bundle = cast(dict[str, Any], payload.get("bundle") or {})
            if bundle.get("id") == "tax.us.2025.f1099div.box2a.vocabulary":
                payload["bundle"] = _load("f1099div-box2a.bundle.v2.json")

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("f1099g-box1.bundle.json")})
    add("bundle-adoption", {"bundle": _load("schedule1-part1-scope.bundle.json")})
    # Close remaining interest-composition v4 families and Schedule B adjustment
    # families closed-empty so taxable-interest (and thus line 9) can publish on
    # the current core package graph.
    for name in (
        "form1065-k1.bundle.json",
        "f1099int-b10.bundle.json",
        "f1099oid-b5.bundle.json",
        "f1099int-box8.bundle.json",
        "scheduleb.bundle.json",
        "scheduleb-adjustment.nominee.bundle.json",
        "scheduleb-adjustment.accrued-interest.bundle.json",
        "scheduleb-adjustment.abp-adjustment.bundle.json",
        "f1099b-covered-st.bundle.json",
        "f1099b-covered-lt.bundle.json",
        "f1099b-covered-st-scalars.bundle.json",
        "f1099b-covered-lt-scalars.bundle.json",
        "f1099b-covered-w-st.bundle.json",
        "f1099b-covered-w-lt.bundle.json",
        "f1099b-covered-w-st-scalars.bundle.json",
        "f1099b-covered-w-lt-scalars.bundle.json",
        "schedule-d-boundary.bundle.json",
    ):
        add("bundle-adoption", {"bundle": _load(name)})

    # Closed-empty interest-composition remainder + Schedule B adjustments +
    # covered ST/LT families so line 7a / line 9 can publish alongside line 8.
    closed_empty: tuple[tuple[str, str, str], ...] = (
        (
            "tax.us.2025.form1065-k1.box5",
            "demo.ug.k1.h0",
            "tax.us.2025.form1065-k1.box5.source-closure",
        ),
        (
            "tax.us.2025.f1099int.b10",
            "demo.ug.int-b10.h0",
            "tax.us.2025.f1099int.b10.source-closure",
        ),
        (
            "tax.us.2025.f1099oid.b5",
            "demo.ug.oid-b5.h0",
            "tax.us.2025.f1099oid.b5.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.nominee",
            "demo.ug.sb-nom.h0",
            "tax.us.2025.scheduleb.adjustment.nominee.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.accrued-interest",
            "demo.ug.sb-acc.h0",
            "tax.us.2025.scheduleb.adjustment.accrued-interest.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.abp-adjustment",
            "demo.ug.sb-abp.h0",
            "tax.us.2025.scheduleb.adjustment.abp-adjustment.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-st",
            "demo.ug.st.h0",
            "tax.us.2025.f1099b.covered-st.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-st-proceeds",
            "demo.ug.st-p.h0",
            "tax.us.2025.f1099b.covered-st-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-st-basis",
            "demo.ug.st-b.h0",
            "tax.us.2025.f1099b.covered-st-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-lt",
            "demo.ug.lt.h0",
            "tax.us.2025.f1099b.covered-lt.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-lt-proceeds",
            "demo.ug.lt-p.h0",
            "tax.us.2025.f1099b.covered-lt-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-lt-basis",
            "demo.ug.lt-b.h0",
            "tax.us.2025.f1099b.covered-lt-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099int.b8",
            "demo.ug.int-b8.h0",
            "tax.us.2025.f1099int.b8.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st",
            "demo.ug.wst.h0",
            "tax.us.2025.f1099b.covered-w-st.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-proceeds",
            "demo.ug.wst-p.h0",
            "tax.us.2025.f1099b.covered-w-st-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-basis",
            "demo.ug.wst-b.h0",
            "tax.us.2025.f1099b.covered-w-st-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-adjustment",
            "demo.ug.wst-a.h0",
            "tax.us.2025.f1099b.covered-w-st-adjustment.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt",
            "demo.ug.wlt.h0",
            "tax.us.2025.f1099b.covered-w-lt.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-proceeds",
            "demo.ug.wlt-p.h0",
            "tax.us.2025.f1099b.covered-w-lt-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-basis",
            "demo.ug.wlt-b.h0",
            "tax.us.2025.f1099b.covered-w-lt-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-adjustment",
            "demo.ug.wlt-a.h0",
            "tax.us.2025.f1099b.covered-w-lt-adjustment.source-closure",
        ),
    )
    wash_sale_prefixes = (
        "tax.us.2025.f1099b.covered-w-st",
        "tax.us.2025.f1099b.covered-w-lt",
    )
    for family_id, horizon_id, closure_type in closed_empty:
        fver = wash_sale_version if family_id.startswith(wash_sale_prefixes) else "v1"
        add(
            "horizon-genesis",
            {
                "family": {"id": family_id, "version": fver},
                "scope": SCOPE_KEY,
                "horizon_id": horizon_id,
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ug.closure.{horizon_id}",
                    f"{closure_type}|family-horizon={horizon_id},tax-year=2025",
                    True,
                )
            },
        )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.ug.scheduleb.foreign-account",
                "tax.us.2025.scheduleb.foreign-account|tax-year=2025",
                "no",
            )
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.ug.scheduleb.foreign-trust",
                "tax.us.2025.scheduleb.foreign-trust|tax-year=2025",
                "no",
            )
        },
    )
    for token in (
        "no-inbound-capital-loss-carryovers",
        "no-form8949-sources",
        "no-other-schedule-d-sources",
        "no-lines-18-19-sources",
        "no-1099da-or-qof",
    ):
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ug.sd-boundary.{token}",
                    f"tax.us.2025.schedule-d-boundary.{token}|tax-year=2025",
                    "yes",
                )
            },
        )

    n_members = max(len(box1_values), 1)
    payers_stmts: list[tuple[str, str]] = []
    if same_payer_two_statements and n_members >= 2:
        payer = "demo.ug.payer.shared"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": payer,
                    "kind": "tax.us.unemployment-payer",
                    "label": "Synthetic shared unemployment agency",
                }
            },
        )
        for index in range(n_members):
            stmt = f"demo.ug.stmt.{index}"
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": stmt,
                        "kind": "tax.us.1099g-statement",
                        "label": f"Synthetic 1099-G statement {index}",
                    }
                },
            )
            payers_stmts.append((payer, stmt))
    else:
        for index in range(n_members):
            payer = f"demo.ug.payer.{index}"
            stmt = f"demo.ug.stmt.{index}"
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": payer,
                        "kind": "tax.us.unemployment-payer",
                        "label": f"Synthetic unemployment agency {index}",
                    }
                },
            )
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": stmt,
                        "kind": "tax.us.1099g-statement",
                        "label": f"Synthetic 1099-G statement {index}",
                    }
                },
            )
            payers_stmts.append((payer, stmt))

    add(
        "horizon-genesis",
        {
            "family": {"id": BOX1_FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": "demo.ug.h0",
        },
    )
    horizon = "demo.ug.h0"
    for index, amount in enumerate(box1_values):
        payer, stmt = payers_stmts[index]
        if include_box4:
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.ug.finding.box4.{index}",
                        f"{BOX4_AUTH}|payer={payer},statement={stmt},tax-year=2025",
                        box4_values[index] if index < len(box4_values) else None,
                    )
                },
            )
        next_horizon = f"demo.ug.h{index + 1}"
        add(
            "member-transition",
            {
                "family": {"id": BOX1_FAMILY, "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        f"demo.ug.finding.box1.{index}",
                        f"{BOX1_AMOUNT}|payer={payer},statement={stmt},tax-year=2025",
                        amount,
                    ),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            },
        )
        horizon = next_horizon

    if close_box1:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ug.closure.box1",
                    f"{BOX1_CLOSURE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    for token, value in scope_vals.items():
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ug.scope.{token}",
                    f"{_scope_id(token)}|tax-year=2025",
                    value,
                )
            },
        )

    adoption = cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / "adopt-core-v20-current.json").read_text("utf-8")),
    )
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts
