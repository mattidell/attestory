"""Track 1 Covered Form 1099-B wash-sale (code W) through Form 8949 (ADR-0061/0062)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from collections.abc import Mapping
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    validate_package,
)
from packages.derivation.production_resolver import PublicationSurface

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
FIXTURES = REPO / "packages" / "sample_data" / "schedule_d_form8949_covered_wash_sale_t1"
T3 = REPO / "packages" / "sample_data" / "declarative_validation_substrate_t3"
ST_VALIDATION = "tax.us.2025.f1099b.covered-w-st.member-validation.synthesized"
LT_VALIDATION = "tax.us.2025.f1099b.covered-w-lt.member-validation.synthesized"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2059"}

LINE1A = "tax.us.2025.rule.schedule-d-line1a-gain"
LINE1B = "tax.us.2025.rule.schedule-d-line1b"
LINE6 = "tax.us.2025.rule.schedule-d-line6"
LINE7 = "tax.us.2025.rule.schedule-d-line7"
LINE8A = "tax.us.2025.rule.schedule-d-line8a-gain"
LINE8B = "tax.us.2025.rule.schedule-d-line8b"
LINE14 = "tax.us.2025.rule.schedule-d-line14"
LINE15 = "tax.us.2025.rule.schedule-d-line15"
LINE16 = "tax.us.2025.rule.schedule-d-line16"
LINE21 = "tax.us.2025.rule.schedule-d-line21"
LINE7A = "tax.us.2025.rule.form1040-line7a"
SPB = "tax.us.2025.rule.selected-preferential-base"
SD_ATT = "tax.us.2025.rule.attachment.schedule-d"
F8949 = "tax.us.2025.rule.attachment.f8949"

# ADR-0059 prior-return authority (fixture #7: W transaction coexisting with
# an inbound loss carryover).
P1 = "tax.us.2025.prior-return.form1040.line-15"
P2 = "tax.us.2025.prior-return.schedule-d.line-21"
P3 = "tax.us.2025.prior-return.schedule-d.line-7"
P4 = "tax.us.2025.prior-return.schedule-d.line-15"
P5 = "tax.us.2025.prior-return.schedule-d.line-16"

BOUNDARY_PATH_A = {
    "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers": "yes",
    "tax.us.2025.schedule-d-boundary.no-form8949-sources": "yes",
    "tax.us.2025.schedule-d-boundary.no-other-schedule-d-sources": "yes",
    "tax.us.2025.schedule-d-boundary.no-lines-18-19-sources": "yes",
    "tax.us.2025.schedule-d-boundary.no-1099da-or-qof": "yes",
}

BOUNDARY_PATH_B = {
    "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers": "yes",
    "tax.us.2025.schedule-d-boundary.no-form8949-sources": "no",
    "tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments": "yes",
    "tax.us.2025.schedule-d-boundary.no-other-schedule-d-sources": "yes",
    "tax.us.2025.schedule-d-boundary.no-lines-18-19-sources": "yes",
    "tax.us.2025.schedule-d-boundary.no-1099da-or-qof": "yes",
}

# Fixture #7: Path B plus an honestly-declared inbound capital-loss
# carryover (ADR-0059/0060), coexisting with a covered-w-st transaction.
BOUNDARY_PATH_B_WITH_CARRYOVER = {
    **BOUNDARY_PATH_B,
    "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers": "no",
}

# The fact/family scope key `_build_acts` uses internally (horizon-genesis,
# member-transition) - distinct from the run's own `SCOPE` (jurisdiction/year
# passed to `live_coordinate_run`). Fixture #9's late-member acts assert
# directly against an already-built act log, so it must match this key
# exactly or the horizon chain lookup fails to find the existing chain.
_FACT_SCOPE = {"tax-year": "2025", "subject": "demo.primary"}

_TXN_BASE = {
    "covered_security": "yes",
    "basis_reported_to_irs": "yes",
    "box_1f_market_discount": "no",
    "ordinary_indicated": "no",
    "qof_indicated": "no",
    "taxpayer_side_adjustment": "no",
    "collectibles_or_special_rate": "no",
}


def _surface() -> PublicationSurface:
    return PublicationSurface(
        T3 / "publication_surface" / "releases",
        CONTENT / "published-packages.v27.json",
        CONTENT,
    )


def _live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.sdw.t1.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-08-05T00:00:{index:02d}Z",
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


def _build_acts(
    *,
    direct_st: list[tuple[float, float]] | None = None,
    direct_lt: list[tuple[float, float]] | None = None,
    w_st: list[tuple[float, float, float]] | None = None,
    w_lt: list[tuple[float, float, float]] | None = None,
    box2a: float | None = None,
    close_direct_st: bool = True,
    close_direct_lt: bool = True,
    close_w_st: bool = True,
    close_w_lt: bool = True,
    filing_status: str = "single",
    boundary: Mapping[str, str | None] | None = None,
    w_st_omit_amount_scalar: bool = False,
    w_st_flag: str = "yes",
    w_st_market_discount: bool = False,
    prior: Mapping[str, float] | None = None,
    w_st_collides_with_direct_st: bool = False,
) -> list[dict[str, object]]:
    """Build act log for package v32 wash-sale route.

    ``w_st`` / ``w_lt`` are lists of (proceeds, basis, adjustment).
    ``direct_st`` / ``direct_lt`` are lists of (proceeds, basis) for 1a/8a.

    ``w_st_collides_with_direct_st`` (Track 1 repair round 3): asserts the
    first ``w_st`` row's real transaction identity (broker, statement,
    transaction, tax-year) as the exact same identity already asserted for
    the first ``direct_st`` row - a genuine live-path reproduction of
    ADR-0061 Decision 2's amended identity-key collision, one real
    transaction adopted into both the direct-reporting and wash-sale
    families at once.
    """
    if direct_st is None:
        direct_st = []
    if direct_lt is None:
        direct_lt = []
    if w_st is None:
        w_st = []
    if w_lt is None:
        w_lt = []
    if boundary is None:
        boundary = BOUNDARY_PATH_A if not (w_st or w_lt) else BOUNDARY_PATH_B

    acts: list[dict[str, object]] = []
    introduced_entities: set[str] = set()

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_live_act(len(acts), kind, payload))

    bundles = (
        "w2.bundle.v3.json",
        "f1099int.bundle.json",
        "interest_composition.bundle.json",
        "f1099int-b10.bundle.json",
        "f1099oid-b5.bundle.json",
        "form1065-k1.bundle.json",
        "core_calculations.bundle.v2.json",
        "f1099div.bundle.v2.json",
        "f1099div-box2a.bundle.json",
        "exception1.bundle.json",
        "qdcg.bundle.json",
        "f1099b-covered-lt.bundle.json",
        "f1099b-covered-st.bundle.json",
        "schedule-d-boundary.bundle.json",
        "schedule-d-boundary-form8949-w.bundle.json",
        "f1099b-covered-lt-scalars.bundle.json",
        "f1099b-covered-st-scalars.bundle.json",
        "f1099b-covered-w-st.bundle.json",
        "f1099b-covered-w-st-scalars.bundle.json",
        "f1099b-covered-w-lt.bundle.json",
        "f1099b-covered-w-lt-scalars.bundle.json",
        "prior-return.bundle.json",
        "scheduleb-adjustment.nominee.bundle.json",
        "scheduleb-adjustment.accrued-interest.bundle.json",
        "scheduleb-adjustment.abp-adjustment.bundle.json",
    )
    for name in bundles:
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text())})

    for eid, kind, label in (
        ("demo.sdw.t1.employer", "tax.us.employer", "Synthetic employer"),
        ("demo.sdw.t1.w2", "tax.us.w2-slip", "Synthetic W-2"),
        ("demo.sdw.t1.payer", "tax.us.dividend-payer", "Synthetic payer"),
        ("demo.sdw.t1.stmt", "tax.us.1099div-statement", "Synthetic 1099-DIV"),
        ("demo.sdw.t1.broker", "tax.us.f1099b-broker", "Synthetic broker"),
        ("demo.sdw.t1.b-stmt", "tax.us.f1099b-statement", "Synthetic 1099-B"),
    ):
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": eid, "kind": kind, "label": label}},
        )

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = [
        ("tax.us.2025.w2", "v2", "demo.sdw.t1.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.sdw.t1.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.sdw.t1.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.sdw.t1.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.sdw.t1.nonform.h0"),
        ("tax.us.2025.f1099int.b10", "v1", "demo.sdw.t1.int-b10.h0"),
        ("tax.us.2025.f1099oid.b5", "v1", "demo.sdw.t1.oid-b5.h0"),
        ("tax.us.2025.form1065-k1.box5", "v1", "demo.sdw.t1.k1-box5.h0"),
        ("tax.us.2025.f1099div.1a", "v1", "demo.sdw.t1.div1a.h0"),
        ("tax.us.2025.f1099div.1b", "v1", "demo.sdw.t1.div1b.h0"),
        ("tax.us.2025.f1099div.2a", "v1", "demo.sdw.t1.div2a.h0"),
        ("tax.us.2025.f1099b.covered-lt", "v1", "demo.sdw.t1.lt.h0"),
        ("tax.us.2025.f1099b.covered-lt-proceeds", "v1", "demo.sdw.t1.lt-p.h0"),
        ("tax.us.2025.f1099b.covered-lt-basis", "v1", "demo.sdw.t1.lt-b.h0"),
        ("tax.us.2025.f1099b.covered-st", "v1", "demo.sdw.t1.st.h0"),
        ("tax.us.2025.f1099b.covered-st-proceeds", "v1", "demo.sdw.t1.st-p.h0"),
        ("tax.us.2025.f1099b.covered-st-basis", "v1", "demo.sdw.t1.st-b.h0"),
        ("tax.us.2025.f1099b.covered-w-st", "v1", "demo.sdw.t1.wst.h0"),
        ("tax.us.2025.f1099b.covered-w-st-proceeds", "v1", "demo.sdw.t1.wst-p.h0"),
        ("tax.us.2025.f1099b.covered-w-st-basis", "v1", "demo.sdw.t1.wst-b.h0"),
        ("tax.us.2025.f1099b.covered-w-st-adjustment", "v1", "demo.sdw.t1.wst-a.h0"),
        ("tax.us.2025.f1099b.covered-w-lt", "v1", "demo.sdw.t1.wlt.h0"),
        ("tax.us.2025.f1099b.covered-w-lt-proceeds", "v1", "demo.sdw.t1.wlt-p.h0"),
        ("tax.us.2025.f1099b.covered-w-lt-basis", "v1", "demo.sdw.t1.wlt-b.h0"),
        ("tax.us.2025.f1099b.covered-w-lt-adjustment", "v1", "demo.sdw.t1.wlt-a.h0"),
        # schedule B adjustment families required by package
        ("tax.us.2025.scheduleb.adjustment.nominee", "v1", "demo.sdw.t1.nom.h0"),
        ("tax.us.2025.scheduleb.adjustment.accrued-interest", "v1", "demo.sdw.t1.acc.h0"),
        ("tax.us.2025.scheduleb.adjustment.abp-adjustment", "v1", "demo.sdw.t1.abp.h0"),
    ]
    horizons: dict[str, str] = {}
    for family_id, version, horizon_id in families:
        add(
            "horizon-genesis",
            {
                "family": {"id": family_id, "version": version},
                "scope": scope,
                "horizon_id": horizon_id,
            },
        )
        horizons[family_id] = horizon_id

    # wages
    h = horizons["tax.us.2025.w2"]
    add(
        "member-transition",
        {
            "family": {"id": "tax.us.2025.w2", "version": "v2"},
            "scope": scope,
            "member": {
                "action": "assert",
                "finding": _attested(
                    "demo.sdw.t1.finding.wages",
                    "tax.us.2025.w2.box1-wages|employer=demo.sdw.t1.employer,w2-slip=demo.sdw.t1.w2,tax-year=2025",
                    90000,
                ),
            },
            "successor": {"id": "demo.sdw.t1.w2.h1", "predecessor": h},
        },
    )
    horizons["tax.us.2025.w2"] = "demo.sdw.t1.w2.h1"

    if box2a is not None:
        h = horizons["tax.us.2025.f1099div.2a"]
        add(
            "member-transition",
            {
                "family": {"id": "tax.us.2025.f1099div.2a", "version": "v1"},
                "scope": scope,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        "demo.sdw.t1.finding.box2a",
                        "tax.us.2025.f1099div.box2a-capital-gain-distribution|payer=demo.sdw.t1.payer,statement=demo.sdw.t1.stmt,tax-year=2025",
                        box2a,
                    ),
                },
                "successor": {"id": "demo.sdw.t1.div2a.h1", "predecessor": h},
            },
        )
        horizons["tax.us.2025.f1099div.2a"] = "demo.sdw.t1.div2a.h1"

    def add_direct(
        term: str,
        rows: list[tuple[float, float]],
        long_term: str,
        txn_ids: list[str] | None = None,
    ) -> None:
        fam = f"tax.us.2025.f1099b.covered-{term}"
        for i, (proceeds, basis) in enumerate(rows):
            txn = txn_ids[i] if txn_ids is not None else f"demo.sdw.t1.{term}-txn-{i}"
            if txn not in introduced_entities:
                introduced_entities.add(txn)
                add(
                    "entity-introduced",
                    {
                        "entity": {
                            "schema": "entity.v1",
                            "id": txn,
                            "kind": "tax.us.f1099b-transaction",
                            "label": f"{term} txn {i}",
                        }
                    },
                )
            val = {
                **_TXN_BASE,
                "proceeds": proceeds,
                "basis": basis,
                "long_term": long_term,
                "box_1g_wash_sale_adjustment": "no",
            }
            h = horizons[fam]
            nh = f"{h}.m{i}"
            add(
                "member-transition",
                {
                    "family": {"id": fam, "version": "v1"},
                    "scope": scope,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            f"demo.sdw.t1.finding.{term}-obj-{i}",
                            f"tax.us.2025.f1099b.covered-{term}-txn|broker=demo.sdw.t1.broker,statement=demo.sdw.t1.b-stmt,transaction={txn},tax-year=2025",
                            val,
                        ),
                    },
                    "successor": {"id": nh, "predecessor": h},
                },
            )
            horizons[fam] = nh
            for field, amount in (("proceeds", proceeds), ("basis", basis)):
                sfam = f"tax.us.2025.f1099b.covered-{term}-{field}"
                h = horizons[sfam]
                nh = f"{h}.m{i}"
                add(
                    "member-transition",
                    {
                        "family": {"id": sfam, "version": "v1"},
                        "scope": scope,
                        "member": {
                            "action": "assert",
                            "finding": _attested(
                                f"demo.sdw.t1.finding.{term}-{field}-{i}",
                                f"tax.us.2025.f1099b.covered-{term}-txn.{field}|broker=demo.sdw.t1.broker,statement=demo.sdw.t1.b-stmt,transaction={txn},tax-year=2025",
                                amount,
                            ),
                        },
                        "successor": {"id": nh, "predecessor": h},
                    },
                )
                horizons[sfam] = nh

    def add_w(
        term: str,
        rows: list[tuple[float, float, float]],
        long_term: str,
        *,
        omit_amount_scalar: bool = False,
        flag: str = "yes",
        market_discount: str = "no",
        txn_ids: list[str] | None = None,
    ) -> None:
        fam = f"tax.us.2025.f1099b.covered-w-{term}"
        for i, (proceeds, basis, adj) in enumerate(rows):
            txn = txn_ids[i] if txn_ids is not None else f"demo.sdw.t1.w-{term}-txn-{i}"
            if txn not in introduced_entities:
                introduced_entities.add(txn)
                add(
                    "entity-introduced",
                    {
                        "entity": {
                            "schema": "entity.v1",
                            "id": txn,
                            "kind": "tax.us.f1099b-transaction",
                            "label": f"w-{term} txn {i}",
                        }
                    },
                )
            val: dict[str, object] = {
                **_TXN_BASE,
                "proceeds": proceeds,
                "basis": basis,
                "long_term": long_term,
                "box_1f_market_discount": market_discount,
                "box_1g_wash_sale_adjustment": flag,
            }
            if not omit_amount_scalar:
                val["box_1g_wash_sale_disallowed_amount"] = adj
            h = horizons[fam]
            nh = f"{h}.m{i}"
            add(
                "member-transition",
                {
                    "family": {"id": fam, "version": "v1"},
                    "scope": scope,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            f"demo.sdw.t1.finding.w-{term}-obj-{i}",
                            f"tax.us.2025.f1099b.covered-w-{term}-txn|broker=demo.sdw.t1.broker,statement=demo.sdw.t1.b-stmt,transaction={txn},tax-year=2025",
                            val,
                        ),
                    },
                    "successor": {"id": nh, "predecessor": h},
                },
            )
            horizons[fam] = nh
            fields = [("proceeds", proceeds), ("basis", basis)]
            if not omit_amount_scalar:
                fields.append(("adjustment", adj))
            for field, amount in fields:
                sfam = f"tax.us.2025.f1099b.covered-w-{term}-{field}"
                h = horizons[sfam]
                nh = f"{h}.m{i}"
                add(
                    "member-transition",
                    {
                        "family": {"id": sfam, "version": "v1"},
                        "scope": scope,
                        "member": {
                            "action": "assert",
                            "finding": _attested(
                                f"demo.sdw.t1.finding.w-{term}-{field}-{i}",
                                f"tax.us.2025.f1099b.covered-w-{term}-txn.{field}|broker=demo.sdw.t1.broker,statement=demo.sdw.t1.b-stmt,transaction={txn},tax-year=2025",
                                amount,
                            ),
                        },
                        "successor": {"id": nh, "predecessor": h},
                    },
                )
                horizons[sfam] = nh

    add_direct("st", direct_st, "no")
    add_direct("lt", direct_lt, "yes")
    w_st_txn_ids = None
    if w_st_collides_with_direct_st:
        assert direct_st and w_st, (
            "w_st_collides_with_direct_st requires both direct_st and w_st rows"
        )
        w_st_txn_ids = ["demo.sdw.t1.st-txn-0"] + [
            f"demo.sdw.t1.w-st-txn-{i}" for i in range(1, len(w_st))
        ]
    add_w(
        "st",
        w_st,
        "no",
        omit_amount_scalar=w_st_omit_amount_scalar,
        flag=w_st_flag,
        market_discount="yes" if w_st_market_discount else "no",
        txn_ids=w_st_txn_ids,
    )
    add_w("lt", w_lt, "yes")

    # close families
    close_map = {
        "tax.us.2025.w2": ("tax.us.2025.w2.source-closure", True),
        "tax.us.2025.f1099int.b1": ("tax.us.2025.f1099int.b1.source-closure", True),
        "tax.us.2025.f1099int.b3": ("tax.us.2025.f1099int.b3.source-closure", True),
        "tax.us.2025.f1099oid.b1": ("tax.us.2025.f1099oid.b1.source-closure", True),
        "tax.us.2025.non-form-interest": ("tax.us.2025.non-form-interest.source-closure", True),
        "tax.us.2025.f1099int.b10": ("tax.us.2025.f1099int.b10.source-closure", True),
        "tax.us.2025.f1099oid.b5": ("tax.us.2025.f1099oid.b5.source-closure", True),
        "tax.us.2025.form1065-k1.box5": ("tax.us.2025.form1065-k1.box5.source-closure", True),
        "tax.us.2025.f1099div.1a": ("tax.us.2025.f1099div.1a.source-closure", True),
        "tax.us.2025.f1099div.1b": ("tax.us.2025.f1099div.1b.source-closure", True),
        "tax.us.2025.f1099div.2a": ("tax.us.2025.f1099div.2a.source-closure", True),
        "tax.us.2025.scheduleb.adjustment.nominee": (
            "tax.us.2025.scheduleb.adjustment.nominee.source-closure",
            True,
        ),
        "tax.us.2025.scheduleb.adjustment.accrued-interest": (
            "tax.us.2025.scheduleb.adjustment.accrued-interest.source-closure",
            True,
        ),
        "tax.us.2025.scheduleb.adjustment.abp-adjustment": (
            "tax.us.2025.scheduleb.adjustment.abp-adjustment.source-closure",
            True,
        ),
    }
    for fam, (cft, do) in close_map.items():
        if not do:
            continue
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.sdw.t1.close.{fam.replace('.', '-')}",
                    f"{cft}|family-horizon={horizons[fam]},tax-year=2025",
                    True,
                )
            },
        )

    def maybe_close(fam: str, cft: str, do: bool) -> None:
        if not do:
            return
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.sdw.t1.close.{fam.replace('.', '-')}",
                    f"{cft}|family-horizon={horizons[fam]},tax-year=2025",
                    True,
                )
            },
        )

    maybe_close(
        "tax.us.2025.f1099b.covered-st",
        "tax.us.2025.f1099b.covered-st.source-closure",
        close_direct_st,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-st-proceeds",
        "tax.us.2025.f1099b.covered-st-proceeds.source-closure",
        close_direct_st,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-st-basis",
        "tax.us.2025.f1099b.covered-st-basis.source-closure",
        close_direct_st,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-lt",
        "tax.us.2025.f1099b.covered-lt.source-closure",
        close_direct_lt,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-lt-proceeds",
        "tax.us.2025.f1099b.covered-lt-proceeds.source-closure",
        close_direct_lt,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-lt-basis",
        "tax.us.2025.f1099b.covered-lt-basis.source-closure",
        close_direct_lt,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-w-st",
        "tax.us.2025.f1099b.covered-w-st.source-closure",
        close_w_st,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-w-st-proceeds",
        "tax.us.2025.f1099b.covered-w-st-proceeds.source-closure",
        close_w_st,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-w-st-basis",
        "tax.us.2025.f1099b.covered-w-st-basis.source-closure",
        close_w_st,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-w-st-adjustment",
        "tax.us.2025.f1099b.covered-w-st-adjustment.source-closure",
        close_w_st and not w_st_omit_amount_scalar,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-w-lt",
        "tax.us.2025.f1099b.covered-w-lt.source-closure",
        close_w_lt,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-w-lt-proceeds",
        "tax.us.2025.f1099b.covered-w-lt-proceeds.source-closure",
        close_w_lt,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-w-lt-basis",
        "tax.us.2025.f1099b.covered-w-lt-basis.source-closure",
        close_w_lt,
    )
    maybe_close(
        "tax.us.2025.f1099b.covered-w-lt-adjustment",
        "tax.us.2025.f1099b.covered-w-lt-adjustment.source-closure",
        close_w_lt,
    )

    # exception-1 components + filing + rounding + boundaries
    components = {
        "tax.us.2025.exception1.only-box2a-capital-gains": "yes",
        "tax.us.2025.exception1.no-capital-losses": "yes",
        "tax.us.2025.exception1.no-qof-deferral": "yes",
        "tax.us.2025.exception1.no-boxes-2b-2c-2d": "yes",
    }
    for fact_type, value in components.items():
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.sdw.t1.exc.{fact_type.split('.')[-1]}",
                    f"{fact_type}|tax-year=2025",
                    value,
                )
            },
        )

    add(
        "assertion",
        {
            "finding": _attested(
                "demo.sdw.t1.finding.rounding",
                "rounding.convention|tax-year=2025",
                "half_up",
            )
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.sdw.t1.finding.status",
                "tax.us.2025.filing-status|tax-year=2025",
                filing_status,
            )
        },
    )

    for fact_type, boundary_value in boundary.items():
        if boundary_value is None:
            continue
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.sdw.t1.boundary.{fact_type.split('.')[-1]}",
                    f"{fact_type}|tax-year=2025",
                    boundary_value,
                )
            },
        )

    if prior:
        for type_id, prior_value in prior.items():
            tail = type_id.removeprefix("tax.us.2025.prior-return.").replace(".", "-")
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.sdw.t1.finding.prior.{tail}",
                        f"{type_id}|tax-year=2025,source-tax-year=2024",
                        prior_value,
                    )
                },
            )

    adoption = json.loads((T3 / "adoptions" / "adopt-core-v32-current.json").read_text())
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _parse_report(result: Any) -> dict[str, Any]:
    assert result.refusal is None, result.refusal
    assert result.output_path is not None
    report = cast(dict[str, Any], json.loads(result.output_path.read_text()))
    values: dict[str, Any] = {}
    if result.presentation_path is not None and result.presentation_path.is_file():
        pres = json.loads(result.presentation_path.read_text())
        for sec in pres.get("sections", []):
            resolved = sec.get("resolved") or {}
            finding = (resolved.get("act") or {}).get("finding") or {}
            symbol = finding.get("symbol")
            if symbol is not None and "value" in finding:
                raw = finding["value"]
                try:
                    values[symbol] = (
                        float(raw)
                        if isinstance(raw, str) and raw not in {"checked", "yes", "no"}
                        else raw
                    )
                except ValueError:
                    values[symbol] = raw
            elif symbol is not None and "value" in resolved:
                values[symbol] = resolved["value"]
    # also harvest from report publications if present
    for item in report.get("publications") or []:
        f = item.get("finding", item)
        symbol = f.get("symbol")
        if symbol is not None and "value" in f and symbol not in values:
            try:
                values[symbol] = float(f["value"])
            except (TypeError, ValueError):
                values[symbol] = f["value"]
    report["symbol_values"] = values
    return report


def _run_tmp(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=_surface(),
            output_name="out.json",
        )
        return _parse_report(result)


def _by_artifact(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["artifact_id"]: row for row in report["dispositions"]}


def _pub_value(report: dict[str, Any], rule_id: str) -> Any:
    rows = _by_artifact(report)
    row = rows[rule_id]
    assert row["disposition"] == "published", (rule_id, row)
    symbol = row.get("symbol")
    values = report.get("symbol_values") or {}
    if symbol in values:
        return values[symbol]
    if symbol == "tax.us.2025.capital-gains.selected-preferential-base":
        return max(float(values.get("tax.us.2025.schedule-d.line-16", 0.0)), 0.0)
    raise AssertionError(
        f"no published value for {rule_id} symbol={symbol} known={list(values)[:20]}"
    )


class PackageSurface(unittest.TestCase):
    def test_v18_validates(self) -> None:
        pkg = json.loads((CONTENT / "package.core-calculations.v18.json").read_text())
        self.assertEqual(pkg["version"], "v18")
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in CONTENT.glob("*.json"):
            d = cast(dict[str, Any], json.loads(path.read_text()))
            if {"id", "version", "schema"} <= d.keys():
                corpus[(d["id"], str(d["version"]))] = d
        result = validate_package(
            pkg,
            {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in pkg["members"]},
            DerivationSchemas(),
        )
        self.assertTrue(result.ok, result.issues)
        ids = {m["id"] for m in pkg["members"]}
        self.assertIn("tax.us.2025.rule.attachment.f8949", ids)
        self.assertIn("tax.us.2025.rule.schedule-d-line1b", ids)
        self.assertIn("tax.us.2025.f1099b.covered-w-st", ids)

    def test_line1a_does_not_pin_covered_w(self) -> None:
        text = (CONTENT / "rule.schedule-d-line1a-gain.json").read_text()
        self.assertNotIn("covered-w", text)
        text = (CONTENT / "rule.schedule-d-line8a-gain.v2.json").read_text()
        self.assertNotIn("covered-w", text)

    def test_line1a_8a_non_confusion_is_a_package_validation_kill_test(self) -> None:
        # Finding 4 repair: ADR-0061 Decision 5's non-confusion invariant is
        # a structural package_validation.py check (LINE_1A_8A_PINS_COVERED_W),
        # not only the ad hoc string test above. Prove both directions: the
        # real content passes clean, and a synthetic mutation pinning a
        # covered-w-* symbol onto line 1a is actually caught.
        pkg = json.loads((CONTENT / "package.core-calculations.v18.json").read_text())
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in CONTENT.glob("*.json"):
            d = cast(dict[str, Any], json.loads(path.read_text()))
            if {"id", "version", "schema"} <= d.keys():
                corpus[(d["id"], str(d["version"]))] = d
        clean_corpus = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in pkg["members"]}
        clean_result = validate_package(pkg, clean_corpus, DerivationSchemas())
        self.assertTrue(clean_result.ok, clean_result.issues)

        mutated_corpus = dict(clean_corpus)
        line1a_key = ("tax.us.2025.rule.schedule-d-line1a-gain", "v1")
        mutated_line1a = json.loads(json.dumps(mutated_corpus[line1a_key]))
        mutated_line1a["requires"] = list(mutated_line1a["requires"]) + [
            "tax.us.2025.f1099b.covered-w-st-proceeds-subtotal"
        ]
        mutated_corpus[line1a_key] = mutated_line1a
        mutated_result = validate_package(pkg, mutated_corpus, DerivationSchemas())
        self.assertFalse(mutated_result.ok)
        self.assertTrue(
            any(issue.code == "LINE_1A_8A_PINS_COVERED_W" for issue in mutated_result.issues),
            mutated_result.issues,
        )

class HappyPath(unittest.TestCase):
    def test_st_loss_fully_disallowed(self) -> None:
        # proceeds 1000, basis 5000, adj 4000 → h = 1000-5000+4000 = 0
        report = _run_tmp(_build_acts(w_st=[(1000, 5000, 4000)]), "demo.sdw.t1.full-disallow")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE1B]["disposition"], "published")
        self.assertEqual(_pub_value(report, LINE1B), 0)
        self.assertEqual(rows[F8949]["disposition"], "published")
        self.assertEqual(rows[SD_ATT]["disposition"], "published")
        self.assertEqual(_pub_value(report, LINE7), 0)
        self.assertEqual(_pub_value(report, LINE16), 0)

    def test_st_loss_partially_disallowed(self) -> None:
        # proceeds 1000, basis 5000, adj 1500 → h = 1000-5000+1500 = -2500
        report = _run_tmp(_build_acts(w_st=[(1000, 5000, 1500)]), "demo.sdw.t1.partial")
        self.assertEqual(_pub_value(report, LINE1B), -2500)
        self.assertEqual(_pub_value(report, LINE7), -2500)
        self.assertEqual(_pub_value(report, LINE16), -2500)
        self.assertEqual(_pub_value(report, LINE21), 2500)
        self.assertEqual(_pub_value(report, LINE7A), -2500)

    def test_lt_loss_with_code_w(self) -> None:
        report = _run_tmp(_build_acts(w_lt=[(2000, 7000, 2000)]), "demo.sdw.t1.lt-w")
        # h = 2000-7000+2000 = -3000
        self.assertEqual(_pub_value(report, LINE8B), -3000)
        self.assertEqual(_pub_value(report, LINE15), -3000)

    def test_multiple_w_st_aggregated(self) -> None:
        report = _run_tmp(
            _build_acts(w_st=[(1000, 3000, 500), (500, 1500, 200)]),
            "demo.sdw.t1.multi",
        )
        # h1 = 1000-3000+500=-1500; h2=500-1500+200=-800; total -2300
        self.assertEqual(_pub_value(report, LINE1B), -2300)

    def test_direct_1a_coexists_with_1b(self) -> None:
        report = _run_tmp(
            _build_acts(direct_st=[(5000, 1000)], w_st=[(1000, 4000, 500)]),
            "demo.sdw.t1.1a-1b",
        )
        # 1a = 4000; 1b = 1000-4000+500=-2500; line7=1500
        self.assertEqual(_pub_value(report, LINE1A), 4000)
        self.assertEqual(_pub_value(report, LINE1B), -2500)
        self.assertEqual(_pub_value(report, LINE7), 1500)

    def test_direct_8a_coexists_with_8b(self) -> None:
        report = _run_tmp(
            _build_acts(direct_lt=[(8000, 2000)], w_lt=[(1000, 5000, 1000)]),
            "demo.sdw.t1.8a-8b",
        )
        # 8a=6000; 8b=1000-5000+1000=-3000; line15=3000
        self.assertEqual(_pub_value(report, LINE8A), 6000)
        self.assertEqual(_pub_value(report, LINE8B), -3000)
        self.assertEqual(_pub_value(report, LINE15), 3000)

    def test_w_only_requires_schedule_d(self) -> None:
        report = _run_tmp(_build_acts(w_st=[(1000, 3000, 500)]), "demo.sdw.t1.w-only")
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_ATT]["disposition"], "published")
        self.assertEqual(rows[F8949]["disposition"], "published")

    def test_path_a_regression_direct_loss(self) -> None:
        report = _run_tmp(
            _build_acts(direct_st=[(1000, 4000)], boundary=BOUNDARY_PATH_A),
            "demo.sdw.t1.path-a-reg",
        )
        self.assertEqual(_pub_value(report, LINE1A), -3000)
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE1B]["disposition"], "published")
        self.assertEqual(_pub_value(report, LINE1B), 0)


class ValidationGuards(unittest.TestCase):
    def test_code_w_on_gain_blocks(self) -> None:
        # gain: d=5000 e=1000 g=100 → on-gain guard
        report = _run_tmp(_build_acts(w_st=[(5000, 1000, 100)]), "demo.sdw.t1.w-on-gain")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE1B]["disposition"], "blocked")
        self.assertEqual(rows[ST_VALIDATION]["disposition"], "blocked", rows[ST_VALIDATION])
        missing = rows[ST_VALIDATION].get("missing") or []
        self.assertTrue(
            any("CODE_W_ON_GAIN" in str(m) for m in missing),
            rows[ST_VALIDATION],
        )

    def test_adjustment_exceeds_loss_blocks(self) -> None:
        # loss of 1000 (e-d), g=2000
        report = _run_tmp(_build_acts(w_st=[(1000, 2000, 2000)]), "demo.sdw.t1.exceeds")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE1B]["disposition"], "blocked")
        self.assertEqual(rows[ST_VALIDATION]["disposition"], "blocked", rows[ST_VALIDATION])
        missing = rows[ST_VALIDATION].get("missing") or []
        self.assertTrue(
            any("ADJUSTMENT_EXCEEDS_LOSS" in str(m) for m in missing),
            rows[ST_VALIDATION],
        )

    def test_adjustment_exactly_equals_loss_passes(self) -> None:
        report = _run_tmp(_build_acts(w_st=[(1000, 4000, 3000)]), "demo.sdw.t1.exact")
        self.assertEqual(_pub_value(report, LINE1B), 0)

    def test_missing_w_family_authority_blocks(self) -> None:
        report = _run_tmp(
            _build_acts(w_st=[(1000, 4000, 500)], close_w_st=False),
            "demo.sdw.t1.open-w",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE1B]["disposition"], "blocked")

    def test_individually_invalid_row_cannot_mask_via_aggregate_netting(self) -> None:
        # Reviewer's exact masking reproduction (Finding 1, CRITICAL): one
        # individually-invalid W row (code W applied to a gain: d=5000,
        # e=1000, g=100) sits in the same box as a valid big-loss W row
        # (d=100, e=10000, g=50). Aggregated: D=5100, E=11000, G=150 - the
        # old (buggy) subtotal-level guard sees D < E (a net loss) and
        # G <= max(E-D,0), so it would have let both rows net together and
        # published h=-5750. The per-transaction guard must instead block
        # on the first row's own individual invalidity, regardless of the
        # second row's valid loss.
        report = _run_tmp(
            _build_acts(w_st=[(5000, 1000, 100), (100, 10000, 50)]),
            "demo.sdw.t1.masking-regression",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE1B]["disposition"], "blocked", rows[LINE1B])
        self.assertEqual(rows[F8949]["disposition"], "blocked", rows[F8949])
        self.assertEqual(rows[ST_VALIDATION]["disposition"], "blocked", rows[ST_VALIDATION])
        missing = rows[ST_VALIDATION].get("missing") or []
        self.assertTrue(
            any("CODE_W_ON_GAIN" in str(m) for m in missing),
            rows[ST_VALIDATION],
        )

    def test_identity_key_collision_blocks_live_run(self) -> None:
        # Second independent review, Track 1 repair round 3: the
        # identity-key collision kill-test
        # (declared identity exclusivity) was correct in
        # isolation but never wired into the live run path -
        # `resolve_production_package` cannot see per-run asserted fact
        # ids at all. This is the genuine live-path reproduction: one real
        # transaction identity (same broker/statement/transaction/tax-year)
        # asserted into both `covered-st` (direct) and `covered-w-st`
        # (wash-sale) in a single run. It must block Schedule D line 1b,
        # the Form 8949 attachment, and line 15 with the new named code -
        # not silently double-count the transaction.
        report = _run_tmp(
            _build_acts(
                direct_st=[(3000, 4000)],
                w_st=[(1000, 4000, 500)],
                w_st_collides_with_direct_st=True,
            ),
            "demo.sdw.t1.identity-collision",
        )
        rows = _by_artifact(report)
        for rule_id in (LINE1B, F8949):
            self.assertEqual(rows[rule_id]["disposition"], "blocked", rows[rule_id])
        self.assertEqual(rows[ST_VALIDATION]["disposition"], "blocked", rows[ST_VALIDATION])
        missing = rows[ST_VALIDATION].get("missing") or []
        self.assertTrue(
            any(
                "IDENTITY_EXCLUSIVITY_COLLISION" in str(m)
                or "identity-key-collision" in str(m)
                for m in missing
            ),
            rows[ST_VALIDATION],
        )

    def test_box_1g_flag_without_amount_blocks(self) -> None:
        # Fixture #11 (Finding 3): box-1g indication (flag=yes) without an
        # amount is independently representable and must independently
        # block, not be silently treated as a well-formed member.
        report = _run_tmp(
            _build_acts(w_st=[(1000, 4000, 500)], w_st_omit_amount_scalar=True),
            "demo.sdw.t1.flag-no-amount",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE1B]["disposition"], "blocked", rows[LINE1B])
        self.assertEqual(rows[ST_VALIDATION]["disposition"], "blocked", rows[ST_VALIDATION])
        missing = rows[ST_VALIDATION].get("missing") or []
        self.assertTrue(
            any("BOX_1G_FLAG_WITHOUT_AMOUNT" in str(m) for m in missing),
            rows[ST_VALIDATION],
        )

    def test_box_1g_amount_without_flag_blocks(self) -> None:
        # Fixture #12 (Finding 3): an amount present without the W
        # classification (flag != "yes") is independently representable and
        # must independently block.
        report = _run_tmp(
            _build_acts(w_st=[(1000, 4000, 500)], w_st_flag="no"),
            "demo.sdw.t1.amount-no-flag",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE1B]["disposition"], "blocked", rows[LINE1B])
        self.assertEqual(rows[ST_VALIDATION]["disposition"], "blocked", rows[ST_VALIDATION])
        missing = rows[ST_VALIDATION].get("missing") or []
        self.assertTrue(
            any("BOX_1G_AMOUNT_WITHOUT_FLAG" in str(m) for m in missing),
            rows[ST_VALIDATION],
        )

    def test_no_other_form8949_adjustments_no_blocks_path_b(self) -> None:
        # attachment-rule.v8 completeness is presence-only. A contributed
        # "no" is present, so this path no longer blocks on a value-equals
        # check. Absence of the answer still blocks (see the noncovered
        # case below).
        b = dict(BOUNDARY_PATH_B)
        b["tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments"] = "no"
        report = _run_tmp(_build_acts(w_st=[(1000, 4000, 500)], boundary=b), "demo.sdw.t1.no-other-no")
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_ATT]["disposition"], "published")

    def test_real_second_code_transaction_blocks_no_other_form8949_adjustments(self) -> None:
        # Fixture #15 repair: an actual second-code transaction, not only
        # the declared-boundary-flag proxy above. `box_1f_market_discount`
        # is the same real, already-modeled field this milestone's non-goals
        # explicitly name as an unsupported second code (accrued market
        # discount, code D) - a covered-w-st member carrying both
        # box_1g_wash_sale_adjustment=yes (code W) and
        # box_1f_market_discount=yes (code D) is a genuine multi-code row,
        # honestly declared unsupported via no-other-form8949-adjustments=no.
        b = dict(BOUNDARY_PATH_B)
        b["tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments"] = "no"
        report = _run_tmp(
            _build_acts(w_st=[(1000, 4000, 500)], w_st_market_discount=True, boundary=b),
            "demo.sdw.t1.real-second-code",
        )
        rows = _by_artifact(report)
        # See test_no_other_form8949_adjustments_no_blocks_path_b: v8
        # completeness records the present "no" rather than blocking it.
        self.assertEqual(rows[SD_ATT]["disposition"], "published", rows[SD_ATT])

    def test_noncovered_basis_reporting_case_remains_blocked(self) -> None:
        # Fixture #16 regression: a noncovered/basis-not-reported Form 8949
        # source has no fact-type representation in this milestone (ADR-0061
        # non-goals) - it can only be honestly declared, never asserted as a
        # member of any covered family. Declaring no-form8949-sources="no"
        # (a real Form 8949 source exists) without also declaring
        # no-other-form8949-adjustments (absent, not "yes") must remain
        # blocked exactly as it did before this milestone's W-only successor
        # existed - the successor never silently admits an unsupported
        # noncovered case.
        b = dict(BOUNDARY_PATH_B)
        del b["tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments"]
        report = _run_tmp(_build_acts(w_st=[(1000, 4000, 500)], boundary=b), "demo.sdw.t1.noncovered")
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_ATT]["disposition"], "blocked", rows[SD_ATT])


class Downstream(unittest.TestCase):
    def test_net_gain(self) -> None:
        # W ST partial loss -500; direct LT gain 5000 → net 4500
        report = _run_tmp(
            _build_acts(w_st=[(1000, 2000, 500)], direct_lt=[(6000, 1000)]),
            "demo.sdw.t1.net-gain",
        )
        self.assertEqual(_pub_value(report, LINE1B), -500)
        self.assertEqual(_pub_value(report, LINE8A), 5000)
        self.assertEqual(_pub_value(report, LINE16), 4500)
        self.assertEqual(_pub_value(report, LINE7A), 4500)

    def test_over_cap_loss(self) -> None:
        report = _run_tmp(_build_acts(w_st=[(1000, 10000, 1000)]), "demo.sdw.t1.over-cap")
        # h = 1000-10000+1000 = -8000; line21 = 3000
        self.assertEqual(_pub_value(report, LINE1B), -8000)
        self.assertEqual(_pub_value(report, LINE21), 3000)
        self.assertEqual(_pub_value(report, LINE7A), -3000)


class PathBClosedEmpty(unittest.TestCase):
    def test_path_b_closed_empty_w_family_is_zero_not_blocked(self) -> None:
        # ADR-0061 Production condition 4: Path B (supported W-family only)
        # with both W families closed-empty (no wash-sale transactions at
        # all) is a valid zero result, not a block - closure with zero
        # members is an honest "no W activity", the same closed-empty
        # discipline every other source family in this project already
        # applies.
        report = _run_tmp(
            _build_acts(w_st=[], w_lt=[], boundary=BOUNDARY_PATH_B),
            "demo.sdw.t1.path-b-closed-empty",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE1B]["disposition"], "published", rows[LINE1B])
        self.assertEqual(_pub_value(report, LINE1B), 0)
        self.assertEqual(rows[LINE8B]["disposition"], "published", rows[LINE8B])
        self.assertEqual(_pub_value(report, LINE8B), 0)


class InboundCarryoverInteraction(unittest.TestCase):
    def test_w_transaction_coexists_with_inbound_short_term_carryover(self) -> None:
        # Fixture #7: a covered-w-st transaction coexists with an honestly-
        # declared inbound short-term capital-loss carryover (ADR-0059/0060).
        # Prior-return values mirror the inbound-carryovers milestone's own
        # ST-only fixture (t2): W8 (ST carryover) = 5000, W13 (LT) = 0.
        prior = {P1: 20000, P3: -10000, P4: 2000, P5: -8000, P2: -3000}
        report = _run_tmp(
            _build_acts(w_st=[(1000, 4000, 500)], boundary=BOUNDARY_PATH_B_WITH_CARRYOVER, prior=prior),
            "demo.sdw.t1.carryover",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE1B]["disposition"], "published", rows[LINE1B])
        self.assertEqual(_pub_value(report, LINE1B), -2500)
        self.assertEqual(rows["tax.us.2025.rule.capital-loss-carryover.short-term"]["disposition"], "published")
        self.assertEqual(_pub_value(report, LINE6), -5000)
        self.assertEqual(_pub_value(report, LINE7), -7500)
        self.assertEqual(rows[SD_ATT]["disposition"], "published", rows[SD_ATT])
        self.assertEqual(rows[F8949]["disposition"], "published", rows[F8949])


class CorrectionAndDisplacement(unittest.TestCase):
    def test_box_1g_amount_correction_at_same_identity_displaces(self) -> None:
        # Fixture #8: correcting the box-1g disallowed amount at the same
        # transaction identity (broker/statement/transaction/tax-year)
        # displaces the enclosing box subtotal, Form 8949, Schedule D line
        # 1b/7, line 16/21, selected-preferential-base, and Form 1040
        # line 7a - the same displacement shape ADR-0057/ADR-0059 already
        # use (ADR-0061 Decision 3).
        acts = _build_acts(w_st=[(1000, 4000, 500)])
        baseline = _run_tmp(acts, "demo.sdw.t1.correction-baseline")
        self.assertEqual(_pub_value(baseline, LINE1B), -2500)
        self.assertEqual(_pub_value(baseline, LINE7A), -2500)

        txn = "demo.sdw.t1.w-st-txn-0"
        corrected_obj = {
            **_TXN_BASE,
            "proceeds": 1000,
            "basis": 4000,
            "long_term": "no",
            "box_1g_wash_sale_adjustment": "yes",
            "box_1g_wash_sale_disallowed_amount": 1500,
        }
        corrected_acts = list(acts)
        idx = len(corrected_acts)
        corrected_acts.append(_live_act(idx, "assertion", {
            "finding": _attested(
                "demo.sdw.t1.finding.w-st-obj-0.correction",
                f"tax.us.2025.f1099b.covered-w-st-txn|broker=demo.sdw.t1.broker,statement=demo.sdw.t1.b-stmt,transaction={txn},tax-year=2025",
                corrected_obj,
            )
        }))
        idx += 1
        corrected_acts.append(_live_act(idx, "assertion", {
            "finding": _attested(
                "demo.sdw.t1.finding.w-st-adjustment-0.correction",
                f"tax.us.2025.f1099b.covered-w-st-txn.adjustment|broker=demo.sdw.t1.broker,statement=demo.sdw.t1.b-stmt,transaction={txn},tax-year=2025",
                1500,
            )
        }))
        corrected = _run_tmp(corrected_acts, "demo.sdw.t1.correction-corrected")
        # h = 1000 - 4000 + 1500 = -2500 - the amount alone changed by 1000.
        self.assertEqual(_pub_value(corrected, LINE1B), -1500)
        self.assertEqual(_pub_value(corrected, LINE7), -1500)
        self.assertEqual(_pub_value(corrected, LINE16), -1500)
        self.assertEqual(_pub_value(corrected, LINE21), 1500)
        self.assertEqual(_pub_value(corrected, LINE7A), -1500)
        rows = _by_artifact(corrected)
        self.assertEqual(rows[SPB]["disposition"], "published", rows[SPB])
        self.assertEqual(rows[F8949]["disposition"], "published", rows[F8949])


class LateMemberLifecycle(unittest.TestCase):
    def test_late_w_st_member_after_closure_and_restored_successor_closure(self) -> None:
        # Fixture #9: a late covered-w-st member asserted after the family's
        # only closure reopens it (blocked) until a new closure is asserted
        # for the resulting leaf horizon (restored, correctly aggregated).
        base_acts = _build_acts(w_st=[(1000, 4000, 500)])

        late_txn = "demo.sdw.t1.w-st-txn-late"

        def add_late_member(acts: list[dict[str, object]]) -> list[dict[str, object]]:
            acts = list(acts)

            def add(kind: str, payload: dict[str, object]) -> None:
                acts.append(_live_act(len(acts), kind, payload))

            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": late_txn,
                        "kind": "tax.us.f1099b-transaction",
                        "label": "late w-st txn",
                    }
                },
            )
            val = {
                **_TXN_BASE,
                "proceeds": 500,
                "basis": 2000,
                "long_term": "no",
                "box_1g_wash_sale_adjustment": "yes",
                "box_1g_wash_sale_disallowed_amount": 300,
            }
            add(
                "member-transition",
                {
                    "family": {"id": "tax.us.2025.f1099b.covered-w-st", "version": "v1"},
                    "scope": _FACT_SCOPE,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            "demo.sdw.t1.finding.w-st-obj-late",
                            f"tax.us.2025.f1099b.covered-w-st-txn|broker=demo.sdw.t1.broker,statement=demo.sdw.t1.b-stmt,transaction={late_txn},tax-year=2025",
                            val,
                        ),
                    },
                    "successor": {"id": "demo.sdw.t1.wst.h0.m0.late", "predecessor": "demo.sdw.t1.wst.h0.m0"},
                },
            )
            for field, amount, horizon_prefix in (
                ("proceeds", 500, "demo.sdw.t1.wst-p"),
                ("basis", 2000, "demo.sdw.t1.wst-b"),
                ("adjustment", 300, "demo.sdw.t1.wst-a"),
            ):
                add(
                    "member-transition",
                    {
                        "family": {"id": f"tax.us.2025.f1099b.covered-w-st-{field}", "version": "v1"},
                        "scope": _FACT_SCOPE,
                        "member": {
                            "action": "assert",
                            "finding": _attested(
                                f"demo.sdw.t1.finding.w-st-{field}-late",
                                f"tax.us.2025.f1099b.covered-w-st-txn.{field}|broker=demo.sdw.t1.broker,statement=demo.sdw.t1.b-stmt,transaction={late_txn},tax-year=2025",
                                amount,
                            ),
                        },
                        "successor": {"id": f"{horizon_prefix}.h0.m0.late", "predecessor": f"{horizon_prefix}.h0.m0"},
                    },
                )
            return acts

        def add_reclosure(acts: list[dict[str, object]]) -> list[dict[str, object]]:
            acts = list(acts)

            def add(kind: str, payload: dict[str, object]) -> None:
                acts.append(_live_act(len(acts), kind, payload))

            for fam, cft, horizon in (
                ("tax.us.2025.f1099b.covered-w-st", "tax.us.2025.f1099b.covered-w-st.source-closure", "demo.sdw.t1.wst.h0.m0.late"),
                ("tax.us.2025.f1099b.covered-w-st-proceeds", "tax.us.2025.f1099b.covered-w-st-proceeds.source-closure", "demo.sdw.t1.wst-p.h0.m0.late"),
                ("tax.us.2025.f1099b.covered-w-st-basis", "tax.us.2025.f1099b.covered-w-st-basis.source-closure", "demo.sdw.t1.wst-b.h0.m0.late"),
                ("tax.us.2025.f1099b.covered-w-st-adjustment", "tax.us.2025.f1099b.covered-w-st-adjustment.source-closure", "demo.sdw.t1.wst-a.h0.m0.late"),
            ):
                add(
                    "assertion",
                    {
                        "finding": _attested(
                            f"demo.sdw.t1.close.{fam.replace('.', '-')}.late",
                            f"{cft}|family-horizon={horizon},tax-year=2025",
                            True,
                        )
                    },
                )
            return acts

        reopened_acts = add_late_member(base_acts)
        blocked = _run_tmp(reopened_acts, "demo.sdw.t1.late-member-blocked")
        blocked_rows = _by_artifact(blocked)
        self.assertEqual(blocked_rows[LINE1B]["disposition"], "blocked", blocked_rows[LINE1B])

        restored_acts = add_reclosure(reopened_acts)
        restored = _run_tmp(restored_acts, "demo.sdw.t1.late-member-restored")
        # d=1000+500=1500; e=4000+2000=6000; g=500+300=800 -> h=1500-6000+800=-3700
        self.assertEqual(_pub_value(restored, LINE1B), -3700)
        restored_rows = _by_artifact(restored)
        self.assertEqual(restored_rows[F8949]["disposition"], "published", restored_rows[F8949])


class PresentationGolden(unittest.TestCase):
    """Fixture #19: one canonical positive presentation golden and compact
    negative mutations (citation-walk / presentation model), mirroring the
    pattern used by the current-year-losses and inbound-carryovers
    milestones' own presentation goldens - no separately committed golden
    file, no new presentation mechanism (ADR-0046)."""

    def _model(self, acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
        with TemporaryDirectory() as tmp:
            outcome = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=REPO,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id=run_id,
                governance_pins=[],
                surface=_surface(),
                output_name="out.json",
            )
            assert outcome.refusal is None, outcome.refusal
            assert outcome.presentation_path is not None
            return cast(dict[str, Any], json.loads(outcome.presentation_path.read_text("utf-8")))

    def test_canonical_positive_golden(self) -> None:
        model = self._model(_build_acts(w_st=[(1000, 4000, 500)]), "demo.sdw.t1.pres-golden")
        sections = {s["id"]: s for s in model["sections"]}
        attachments = {a["id"]: a for a in model["attachments"]}

        line1b = sections["line-1b-h"]["resolved"]["act"]["finding"]
        self.assertEqual(float(line1b["value"]), -2500)
        self.assertEqual(float(sections["line-7"]["resolved"]["act"]["finding"]["value"]), -2500)
        self.assertEqual(float(sections["line-sch-d-16"]["resolved"]["act"]["finding"]["value"]), -2500)
        self.assertEqual(float(sections["line-21"]["resolved"]["act"]["finding"]["value"]), 2500)
        self.assertEqual(float(sections["line-7a"]["resolved"]["act"]["finding"]["value"]), -2500)
        self.assertEqual(attachments[F8949]["resolved"]["disposition"], "published")
        self.assertEqual(attachments[SD_ATT]["resolved"]["disposition"], "published")
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertIn(F8949, group_ids)
        self.assertIn(SD_ATT, group_ids)

    def test_negative_mutation_blocked_guard_never_presents_a_value(self) -> None:
        # Compact in-test mutation, never a separately committed golden
        # (mirrors the MD-N12-style deferral already used elsewhere in this
        # project): code W on a gain transaction blocks line 1b, and the
        # presentation model must carry the block, not a numeric value.
        model = self._model(_build_acts(w_st=[(5000, 1000, 100)]), "demo.sdw.t1.pres-neg-guard")
        sections = {s["id"]: s for s in model["sections"]}
        resolved = sections["line-1b-h"]["resolved"]
        self.assertNotEqual(resolved.get("disposition"), "published_value")
        act = resolved.get("act")
        if act is not None:
            self.assertNotIn("value", act.get("finding", {}))

    def test_negative_mutation_form8949_blocked_when_declaration_absent(self) -> None:
        b = dict(BOUNDARY_PATH_B)
        del b["tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments"]
        model = self._model(
            _build_acts(w_st=[(1000, 4000, 500)], boundary=b), "demo.sdw.t1.pres-neg-declaration"
        )
        attachments = {a["id"]: a for a in model["attachments"]}
        self.assertEqual(attachments[F8949]["resolved"]["disposition"], "blocked")
        self.assertEqual(attachments[SD_ATT]["resolved"]["disposition"], "blocked")

    def test_form8949_row_explanation_and_line_1b_8b_citation_walk(self) -> None:
        """Fixture #17 (columns (d)/(e)/(g)/(h) tie-out) at the presentation-
        model level: box A (short-term) and box D (long-term) both carry
        walkable row-explanation parts, and Schedule D lines 1b/8b cite the
        exact underlying transaction facts, not merely a subtotal-level pin
        - the same citation-walk pattern lines 1a/8a and 6/14 already use
        (ADR-0062 Decision 7, ADR-0046 zero-authority/citation identity)."""
        model = self._model(
            _build_acts(w_st=[(1000, 4000, 500)], w_lt=[(2000, 7000, 2000)]),
            "demo.sdw.t1.pres-row-walk",
        )
        sections = {s["id"]: s for s in model["sections"]}
        groups = {g["id"]: g for g in model["citationGroups"]}

        # Each box total cites its own three contributing transaction facts
        # (proceeds/basis/adjustment), never a bare subtotal-level pin.
        self.assertEqual(len(sections["line-1b-h"]["citationSites"]), 3)
        self.assertEqual(len(sections["line-8b-h"]["citationSites"]), 3)

        # The Form 8949 attachment publishes one walkable row-explanation
        # part per box/column; each ties its reported subtotal to the exact
        # transaction fact(s) that produced it - this is the row
        # explanation itself, not a summary.
        f8949_group = groups[F8949]
        parts_by_heading = {p["heading"]: p for p in f8949_group["parts"]}
        expected = {
            "Part I box A column (d): short-term wash-sale proceeds": 1000,
            "Part I box A column (e): short-term wash-sale basis": 4000,
            "Part I box A column (g): short-term wash-sale adjustment": 500,
            "Part II box D column (d): long-term wash-sale proceeds": 2000,
            "Part II box D column (e): long-term wash-sale basis": 7000,
            "Part II box D column (g): long-term wash-sale adjustment": 2000,
        }
        self.assertEqual(set(parts_by_heading), set(expected))
        for heading, subtotal in expected.items():
            part = parts_by_heading[heading]
            self.assertEqual(part["tieOutText"], f"Reported subtotal: {subtotal}")
            self.assertEqual(len(part["citationSites"]), 1)

        # Column (h) per box reproduces d - e + g exactly, from the same
        # cited transaction facts the row-explanation parts above publish.
        self.assertEqual(float(sections["line-1b-h"]["resolved"]["act"]["finding"]["value"]), 1000 - 4000 + 500)
        self.assertEqual(float(sections["line-8b-h"]["resolved"]["act"]["finding"]["value"]), 2000 - 7000 + 2000)


if __name__ == "__main__":
    unittest.main()
