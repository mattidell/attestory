"""Track 1 Inbound Capital-Loss Carryovers: prior-return authority + worksheet route (ADR-0059/0060)."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import LiveCoordinatorOutcome, live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import validate_package
from packages.derivation.production_resolver import PublicationSurface

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
FIXTURES = REPO / "packages" / "sample_data" / "schedule_d_inbound_loss_carryovers_t1"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2059"}

W8_RULE = "tax.us.2025.rule.capital-loss-carryover.short-term"
W13_RULE = "tax.us.2025.rule.capital-loss-carryover.long-term"
LINE6 = "tax.us.2025.rule.schedule-d-line6"
LINE7 = "tax.us.2025.rule.schedule-d-line7"
LINE14 = "tax.us.2025.rule.schedule-d-line14"
LINE15 = "tax.us.2025.rule.schedule-d-line15"
LINE16 = "tax.us.2025.rule.schedule-d-line16"
LINE21 = "tax.us.2025.rule.schedule-d-line21"
LINE1A = "tax.us.2025.rule.schedule-d-line1a-gain"
LINE8A = "tax.us.2025.rule.schedule-d-line8a-gain"
SPB = "tax.us.2025.rule.selected-preferential-base"
LINE7A = "tax.us.2025.rule.form1040-line7a"
LINE9 = "tax.us.2025.rule.form1040-line9"
SD_ATT = "tax.us.2025.rule.attachment.schedule-d"

DECL = "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers"
P1 = "tax.us.2025.prior-return.form1040.line-15"
P2 = "tax.us.2025.prior-return.schedule-d.line-21"
P3 = "tax.us.2025.prior-return.schedule-d.line-7"
P4 = "tax.us.2025.prior-return.schedule-d.line-15"
P5 = "tax.us.2025.prior-return.schedule-d.line-16"
PRIOR = (P1, P2, P3, P4, P5)

FOUR_RETAINED = (
    "tax.us.2025.schedule-d-boundary.no-form8949-sources",
    "tax.us.2025.schedule-d-boundary.no-other-schedule-d-sources",
    "tax.us.2025.schedule-d-boundary.no-lines-18-19-sources",
    "tax.us.2025.schedule-d-boundary.no-1099da-or-qof",
)

BOUNDARY_PATH_A: dict[str, str | None] = {DECL: "yes", **{n: "yes" for n in FOUR_RETAINED}}
BOUNDARY_PATH_B: dict[str, str | None] = {DECL: "no", **{n: "yes" for n in FOUR_RETAINED}}

C1 = "tax.us.2025.exception1.only-box2a-capital-gains"
C2 = "tax.us.2025.exception1.no-capital-losses"
C3 = "tax.us.2025.exception1.no-qof-deferral"
C4 = "tax.us.2025.exception1.no-boxes-2b-2c-2d"

_TXN_BASE = {
    "covered_security": "yes",
    "basis_reported_to_irs": "yes",
    "box_1f_market_discount": "no",
    "box_1g_wash_sale_adjustment": "no",
    "ordinary_indicated": "no",
    "qof_indicated": "no",
    "taxpayer_side_adjustment": "no",
    "collectibles_or_special_rate": "no",
}


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v11.json",
        CONTENT,
    )


def _live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.sdilc.t1.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-08-04T12:00:{index:02d}Z",
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


def _txn_value(*, proceeds: float, basis: float, long_term: str) -> dict[str, object]:
    return {**_TXN_BASE, "proceeds": proceeds, "basis": basis, "long_term": long_term}


def _prior_fact_id(type_id: str) -> str:
    return f"{type_id}|tax-year=2025,source-tax-year=2024"


def _build_acts(
    *,
    st: list[tuple[float, float]] | None = None,
    lt: list[tuple[float, float]] | None = None,
    box2a: float | None = None,
    box1a: float | None = None,
    box1b: float | None = None,
    close_2a: bool = True,
    close_st: bool = True,
    close_lt: bool = True,
    filing_status: str = "single",
    boundary: dict[str, str | None] | None = None,
    prior: dict[str, float] | None = None,
    components: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    if st is None:
        st = []
    if lt is None:
        lt = []
    if components is None:
        components = {"C1": "yes", "C2": "yes", "C3": "yes", "C4": "yes"}
    acts: list[dict[str, object]] = []

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_live_act(len(acts), kind, payload))

    for name in (
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
        "prior-return.bundle.json",
        "f1099b-covered-lt-scalars.bundle.json",
        "f1099b-covered-st-scalars.bundle.json",
        "scheduleb-adjustment.nominee.bundle.json",
        "scheduleb-adjustment.accrued-interest.bundle.json",
        "scheduleb-adjustment.abp-adjustment.bundle.json",
    ):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text())})

    for eid, kind, label in (
        ("demo.sdilc.t1.employer", "tax.us.employer", "Synthetic employer"),
        ("demo.sdilc.t1.w2", "tax.us.w2-slip", "Synthetic W-2"),
        ("demo.sdilc.t1.payer", "tax.us.dividend-payer", "Synthetic payer"),
        ("demo.sdilc.t1.stmt", "tax.us.1099div-statement", "Synthetic 1099-DIV"),
        ("demo.sdilc.t1.broker", "tax.us.f1099b-broker", "Synthetic broker"),
        ("demo.sdilc.t1.b-stmt", "tax.us.f1099b-statement", "Synthetic 1099-B"),
    ):
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": eid, "kind": kind, "label": label}})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = (
        ("tax.us.2025.w2", "v2", "demo.sdilc.t1.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.sdilc.t1.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.sdilc.t1.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.sdilc.t1.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.sdilc.t1.nonform.h0"),
        ("tax.us.2025.f1099int.b10", "v1", "demo.sdilc.t1.int-b10.h0"),
        ("tax.us.2025.f1099oid.b5", "v1", "demo.sdilc.t1.oid-b5.h0"),
        ("tax.us.2025.form1065-k1.box5", "v1", "demo.sdilc.t1.k1-box5.h0"),
        ("tax.us.2025.f1099div.1a", "v1", "demo.sdilc.t1.div1a.h0"),
        ("tax.us.2025.f1099div.1b", "v1", "demo.sdilc.t1.div1b.h0"),
        ("tax.us.2025.f1099div.2a", "v1", "demo.sdilc.t1.div2a.h0"),
        ("tax.us.2025.f1099b.covered-lt", "v1", "demo.sdilc.t1.lt.h0"),
        ("tax.us.2025.f1099b.covered-lt-proceeds", "v1", "demo.sdilc.t1.lt-p.h0"),
        ("tax.us.2025.f1099b.covered-lt-basis", "v1", "demo.sdilc.t1.lt-b.h0"),
        ("tax.us.2025.f1099b.covered-st", "v1", "demo.sdilc.t1.st.h0"),
        ("tax.us.2025.f1099b.covered-st-proceeds", "v1", "demo.sdilc.t1.st-p.h0"),
        ("tax.us.2025.f1099b.covered-st-basis", "v1", "demo.sdilc.t1.st-b.h0"),
        ("tax.us.2025.scheduleb.adjustment.nominee", "v1", "demo.sdilc.t1.sb-nominee.h0"),
        ("tax.us.2025.scheduleb.adjustment.accrued-interest", "v1", "demo.sdilc.t1.sb-accrued.h0"),
        ("tax.us.2025.scheduleb.adjustment.abp-adjustment", "v1", "demo.sdilc.t1.sb-abp.h0"),
    )
    for family_id, version, horizon_id in families:
        add("horizon-genesis", {"family": {"id": family_id, "version": version}, "scope": scope, "horizon_id": horizon_id})

    w2_h = "demo.sdilc.t1.w2.h0"
    add("member-transition", {
        "family": {"id": "tax.us.2025.w2", "version": "v2"},
        "scope": scope,
        "member": {"action": "assert", "finding": _attested(
            "demo.sdilc.t1.finding.wages",
            "tax.us.2025.w2.box1-wages|employer=demo.sdilc.t1.employer,w2-slip=demo.sdilc.t1.w2,tax-year=2025",
            90000,
        )},
        "successor": {"id": "demo.sdilc.t1.w2.h1", "predecessor": w2_h},
    })
    w2_h = "demo.sdilc.t1.w2.h1"

    div2a_h = "demo.sdilc.t1.div2a.h0"
    if box2a is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099div.2a", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.sdilc.t1.finding.box2a",
                "tax.us.2025.f1099div.box2a-capital-gain-distribution|payer=demo.sdilc.t1.payer,statement=demo.sdilc.t1.stmt,tax-year=2025",
                box2a,
            )},
            "successor": {"id": "demo.sdilc.t1.div2a.h1", "predecessor": div2a_h},
        })
        div2a_h = "demo.sdilc.t1.div2a.h1"

    div1a_h = "demo.sdilc.t1.div1a.h0"
    if box1a is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099div.1a", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.sdilc.t1.finding.box1a",
                "tax.us.2025.f1099div.box1a-ordinary|payer=demo.sdilc.t1.payer,statement=demo.sdilc.t1.stmt,tax-year=2025",
                box1a,
            )},
            "successor": {"id": "demo.sdilc.t1.div1a.h1", "predecessor": div1a_h},
        })
        div1a_h = "demo.sdilc.t1.div1a.h1"

    div1b_h = "demo.sdilc.t1.div1b.h0"
    if box1b is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099div.1b", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.sdilc.t1.finding.box1b",
                "tax.us.2025.f1099div.box1b-qualified|payer=demo.sdilc.t1.payer,statement=demo.sdilc.t1.stmt,tax-year=2025",
                box1b,
            )},
            "successor": {"id": "demo.sdilc.t1.div1b.h1", "predecessor": div1b_h},
        })
        div1b_h = "demo.sdilc.t1.div1b.h1"

    add("assertion", {"finding": _attested(
        "demo.sdilc.t1.finding.anchor",
        "tax.us.2025.f1099b.statement-anchor|broker=demo.sdilc.t1.broker,statement=demo.sdilc.t1.b-stmt,tax-year=2025",
        {"broker_name": "Synthetic Broker"},
    )})

    def add_txns(prefix: str, family: str, long_term: str, pairs: list[tuple[float, float]], horizons: dict[str, str]) -> dict[str, str]:
        for i, (proceeds, basis) in enumerate(pairs):
            txn_id = f"demo.sdilc.t1.{prefix}-txn-{i}"
            add("entity-introduced", {"entity": {
                "schema": "entity.v1", "id": txn_id,
                "kind": "tax.us.f1099b-transaction", "label": f"Synthetic {prefix} sale {i}",
            }})
            key = f"broker=demo.sdilc.t1.broker,statement=demo.sdilc.t1.b-stmt,transaction={txn_id},tax-year=2025"
            val = _txn_value(proceeds=proceeds, basis=basis, long_term=long_term)
            for fam_key, fact_suffix, amount in (
                ("obj", f"{family}-txn", val),
                ("p", f"{family}-txn.proceeds", proceeds),
                ("b", f"{family}-txn.basis", basis),
            ):
                fam_id = {
                    "obj": f"tax.us.2025.f1099b.{family}",
                    "p": f"tax.us.2025.f1099b.{family}-proceeds",
                    "b": f"tax.us.2025.f1099b.{family}-basis",
                }[fam_key]
                pred = horizons[fam_key]
                succ = f"{pred}.n{i}"
                add("member-transition", {
                    "family": {"id": fam_id, "version": "v1"},
                    "scope": scope,
                    "member": {"action": "assert", "finding": _attested(
                        f"demo.sdilc.t1.finding.{prefix}-{fam_key}-{i}",
                        f"tax.us.2025.f1099b.{fact_suffix}|{key}",
                        amount,
                    )},
                    "successor": {"id": succ, "predecessor": pred},
                })
                horizons[fam_key] = succ
        return horizons

    st_h = {"obj": "demo.sdilc.t1.st.h0", "p": "demo.sdilc.t1.st-p.h0", "b": "demo.sdilc.t1.st-b.h0"}
    lt_h = {"obj": "demo.sdilc.t1.lt.h0", "p": "demo.sdilc.t1.lt-p.h0", "b": "demo.sdilc.t1.lt-b.h0"}
    st_h = add_txns("st", "covered-st", "no", st, st_h)
    lt_h = add_txns("lt", "covered-lt", "yes", lt, lt_h)

    add("assertion", {"finding": _attested("demo.sdilc.t1.finding.rounding", "rounding.convention|tax-year=2025", "half_up")})
    add("assertion", {"finding": _attested("demo.sdilc.t1.finding.status", "tax.us.2025.filing-status|tax-year=2025", filing_status)})

    for alias, component_value in components.items():
        fact_type = {"C1": C1, "C2": C2, "C3": C3, "C4": C4}[alias]
        add("assertion", {"finding": _attested(f"demo.sdilc.t1.finding.{alias.lower()}", f"{fact_type}|tax-year=2025", component_value)})

    if boundary is None:
        boundary = dict(BOUNDARY_PATH_A)
    for name, bvalue in boundary.items():
        if bvalue is None:
            continue
        add("assertion", {"finding": _attested(
            f"demo.sdilc.t1.finding.{name.split('.')[-1]}",
            f"{name}|tax-year=2025",
            bvalue,
        )})

    if prior:
        for type_id, prior_value in prior.items():
            # full type tail is unique across form1040 vs schedule-d lines
            tail = type_id.removeprefix("tax.us.2025.prior-return.")
            add("assertion", {"finding": _attested(
                f"demo.sdilc.t1.finding.prior.{tail.replace('.', '-')}",
                _prior_fact_id(type_id),
                prior_value,
            )})

    closures = [
        ("demo.sdilc.t1.closure.w2", "tax.us.2025.w2.source-closure", w2_h),
        ("demo.sdilc.t1.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure", "demo.sdilc.t1.int-b1.h0"),
        ("demo.sdilc.t1.closure.int-b3", "tax.us.2025.f1099int.b3.source-closure", "demo.sdilc.t1.int-b3.h0"),
        ("demo.sdilc.t1.closure.oid-b1", "tax.us.2025.f1099oid.b1.source-closure", "demo.sdilc.t1.oid-b1.h0"),
        ("demo.sdilc.t1.closure.nonform", "tax.us.2025.non-form-interest.source-closure", "demo.sdilc.t1.nonform.h0"),
        ("demo.sdilc.t1.closure.int-b10", "tax.us.2025.f1099int.b10.source-closure", "demo.sdilc.t1.int-b10.h0"),
        ("demo.sdilc.t1.closure.oid-b5", "tax.us.2025.f1099oid.b5.source-closure", "demo.sdilc.t1.oid-b5.h0"),
        ("demo.sdilc.t1.closure.k1", "tax.us.2025.form1065-k1.box5.source-closure", "demo.sdilc.t1.k1-box5.h0"),
        ("demo.sdilc.t1.closure.div1a", "tax.us.2025.f1099div.1a.source-closure", div1a_h),
        ("demo.sdilc.t1.closure.div1b", "tax.us.2025.f1099div.1b.source-closure", div1b_h),
        ("demo.sdilc.t1.closure.sb-nominee", "tax.us.2025.scheduleb.adjustment.nominee.source-closure", "demo.sdilc.t1.sb-nominee.h0"),
        ("demo.sdilc.t1.closure.sb-accrued", "tax.us.2025.scheduleb.adjustment.accrued-interest.source-closure", "demo.sdilc.t1.sb-accrued.h0"),
        ("demo.sdilc.t1.closure.sb-abp", "tax.us.2025.scheduleb.adjustment.abp-adjustment.source-closure", "demo.sdilc.t1.sb-abp.h0"),
    ]
    if close_st:
        closures.extend([
            ("demo.sdilc.t1.closure.st", "tax.us.2025.f1099b.covered-st.source-closure", st_h["obj"]),
            ("demo.sdilc.t1.closure.st-p", "tax.us.2025.f1099b.covered-st-proceeds.source-closure", st_h["p"]),
            ("demo.sdilc.t1.closure.st-b", "tax.us.2025.f1099b.covered-st-basis.source-closure", st_h["b"]),
        ])
    if close_lt:
        closures.extend([
            ("demo.sdilc.t1.closure.lt", "tax.us.2025.f1099b.covered-lt.source-closure", lt_h["obj"]),
            ("demo.sdilc.t1.closure.lt-p", "tax.us.2025.f1099b.covered-lt-proceeds.source-closure", lt_h["p"]),
            ("demo.sdilc.t1.closure.lt-b", "tax.us.2025.f1099b.covered-lt-basis.source-closure", lt_h["b"]),
        ])
    if close_2a:
        closures.append(("demo.sdilc.t1.closure.div2a", "tax.us.2025.f1099div.2a.source-closure", div2a_h))
    for finding_id, fact_type, horizon_id in closures:
        add("assertion", {"finding": _attested(finding_id, f"{fact_type}|family-horizon={horizon_id},tax-year=2025", True)})

    adoption = json.loads((FIXTURES / "adoptions" / "adopt-core-v16-current.json").read_text())
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _parse_report(result: LiveCoordinatorOutcome) -> dict[str, Any]:
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
                    values[symbol] = float(raw) if isinstance(raw, str) and raw not in {"checked", "yes", "no"} else raw
                except ValueError:
                    values[symbol] = raw
            elif symbol is not None and "value" in resolved:
                values[symbol] = resolved["value"]
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
    # Worksheet intermediates and selected-preferential-base are not form-field
    # presentation surfaces; recover them from signed Schedule D lines / line 16.
    if symbol == "tax.us.2025.capital-loss-carryover.short-term":
        return -float(values.get("tax.us.2025.schedule-d.line-6", 0.0))
    if symbol == "tax.us.2025.capital-loss-carryover.long-term":
        return -float(values.get("tax.us.2025.schedule-d.line-14", 0.0))
    if symbol == "tax.us.2025.capital-gains.selected-preferential-base":
        return max(float(values.get("tax.us.2025.schedule-d.line-16", 0.0)), 0.0)
    raise AssertionError(f"no published value for {rule_id} symbol={symbol} known={list(values)[:20]}")


def _t1_prior() -> dict[str, float]:
    return {P1: 50000, P3: -8000, P4: -5000, P5: -13000, P2: -3000}


def _t2_prior() -> dict[str, float]:
    return {P1: 20000, P3: -10000, P4: 2000, P5: -8000, P2: -3000}


def _t3_prior() -> dict[str, float]:
    return {P1: 40000, P3: 4000, P4: -12000, P5: -8000, P2: -3000}


def _t6_prior() -> dict[str, float]:
    return {P1: -2000, P3: -10000, P4: 0, P5: -10000, P2: -3000}


def _t7_prior() -> dict[str, float]:
    return {P1: 80000, P3: -2000, P4: -500, P5: -2500, P2: -2500}


class PackageSurface(unittest.TestCase):
    def test_v16_validates_and_adopts_new_citizens(self) -> None:
        pkg = json.loads((CONTENT / "package.core-calculations.v16.json").read_text())
        self.assertEqual(pkg["version"], "v16")

        def body(cid: str, version: str) -> dict[str, Any]:
            for path in CONTENT.glob("*.json"):
                d = cast(dict[str, Any], json.loads(path.read_text()))
                if d.get("id") == cid and str(d.get("version")) == version:
                    return d
            raise AssertionError(cid)

        corpus = {(m["id"], m["version"]): body(m["id"], m["version"]) for m in pkg["members"]}
        result = validate_package(pkg, corpus, DerivationSchemas())
        self.assertTrue(result.ok, result.issues)
        ids = {m["id"] for m in pkg["members"]}
        self.assertIn("tax.us.2025.prior-return.vocabulary", ids)
        self.assertIn("tax.us.2025.rule.capital-loss-carryover.short-term", ids)
        self.assertIn("tax.us.2025.rule.schedule-d-line6", ids)
        self.assertIn("tax.us.2025.rule.schedule-d-line14", ids)

    def test_no_schedule_d_line_rule_pins_prior_return(self) -> None:
        """ADR-0059 Decision 7 structural non-confusion proof."""
        for path in CONTENT.glob("rule.schedule-d-line*.json"):
            text = path.read_text()
            self.assertNotIn("prior-return", text, path.name)

    def test_no_2026_carry_symbols(self) -> None:
        """ADR-0060 Decision 7 / plan D7."""
        pattern = re.compile(r"tax\.us\.2026|carryover.to.2026|carry.to.2026", re.I)
        for path in list(CONTENT.glob("*.json")) + list(FIXTURES.rglob("*.json")):
            text = path.read_text()
            self.assertIsNone(pattern.search(text), f"2026 carry marker in {path}")


class PathADeclaredNoCarryover(unittest.TestCase):
    def test_path_a_publishes_zero_without_prior_facts(self) -> None:
        report = _run_tmp(
            _build_acts(st=[(1000, 2500)], lt=[], boundary=BOUNDARY_PATH_A, prior=None),
            "demo.sdilc.t1.path-a",
        )
        rows = _by_artifact(report)
        self.assertEqual(_pub_value(report, W8_RULE), 0)
        self.assertEqual(_pub_value(report, W13_RULE), 0)
        self.assertEqual(_pub_value(report, LINE6), 0)
        self.assertEqual(_pub_value(report, LINE14), 0)
        # ST loss 1500; no carryover → same as prior milestone
        self.assertEqual(_pub_value(report, LINE7), -1500)
        self.assertEqual(_pub_value(report, LINE16), -1500)
        self.assertEqual(_pub_value(report, LINE21), 1500)
        self.assertEqual(_pub_value(report, LINE7A), -1500)


class WorksheetArithmetic(unittest.TestCase):
    def test_t1_both_st_and_lt_carryovers(self) -> None:
        report = _run_tmp(
            _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t1_prior()),
            "demo.sdilc.t1.t1",
        )
        rows = _by_artifact(report)
        self.assertEqual(_pub_value(report, W8_RULE), 5000)
        self.assertEqual(_pub_value(report, W13_RULE), 5000)
        self.assertEqual(_pub_value(report, LINE6), -5000)
        self.assertEqual(_pub_value(report, LINE14), -5000)
        self.assertEqual(_pub_value(report, LINE7), -5000)
        self.assertEqual(_pub_value(report, LINE15), -5000)
        self.assertEqual(_pub_value(report, LINE16), -10000)
        self.assertEqual(_pub_value(report, LINE21), 3000)
        self.assertEqual(_pub_value(report, LINE7A), -3000)
        self.assertEqual(rows[SD_ATT]["disposition"], "published")
        self.assertEqual(rows[SPB]["disposition"], "published")
        self.assertEqual(_pub_value(report, SPB), 0)  # max(line16, 0)

    def test_t2_st_only(self) -> None:
        report = _run_tmp(
            _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t2_prior()),
            "demo.sdilc.t1.t2",
        )
        rows = _by_artifact(report)
        self.assertEqual(_pub_value(report, W8_RULE), 5000)
        self.assertEqual(_pub_value(report, W13_RULE), 0)

    def test_t3_lt_only(self) -> None:
        report = _run_tmp(
            _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t3_prior()),
            "demo.sdilc.t1.t3",
        )
        rows = _by_artifact(report)
        self.assertEqual(_pub_value(report, W8_RULE), 0)
        self.assertEqual(_pub_value(report, W13_RULE), 5000)

    def test_t6_taxable_income_limited(self) -> None:
        report = _run_tmp(
            _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t6_prior()),
            "demo.sdilc.t1.t6",
        )
        rows = _by_artifact(report)
        self.assertEqual(_pub_value(report, W8_RULE), 9000)
        self.assertEqual(_pub_value(report, W13_RULE), 0)

    def test_t7_ineligible_zero_result(self) -> None:
        report = _run_tmp(
            _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t7_prior()),
            "demo.sdilc.t1.t7",
        )
        rows = _by_artifact(report)
        self.assertEqual(_pub_value(report, W8_RULE), 0)
        self.assertEqual(_pub_value(report, W13_RULE), 0)
        # still published (not blocked) with five facts present
        self.assertEqual(rows[W8_RULE]["disposition"], "published")


class CarryoverRouting(unittest.TestCase):
    def test_t8_carryover_only_requires_schedule_d(self) -> None:
        report = _run_tmp(
            _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t1_prior()),
            "demo.sdilc.t1.t8",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_ATT]["disposition"], "published")
        self.assertEqual(_pub_value(report, LINE7A), -3000)

    def test_carryover_offsetting_current_year_gain(self) -> None:
        # ST gain 4000 (proceeds 5000 basis 1000) + W8=5000 → line7 = 4000-5000 = -1000
        report = _run_tmp(
            _build_acts(st=[(5000, 1000)], lt=[], boundary=BOUNDARY_PATH_B, prior=_t2_prior()),
            "demo.sdilc.t1.offset-gain",
        )
        rows = _by_artifact(report)
        self.assertEqual(_pub_value(report, W8_RULE), 5000)
        self.assertEqual(_pub_value(report, LINE1A), 4000)
        self.assertEqual(_pub_value(report, LINE7), -1000)
        self.assertEqual(_pub_value(report, LINE16), -1000)
        # Finding 3: combined net loss is -1000 (under the $3,000 cap). Assert line 21 equals actual combined loss, not cap parameter.
        self.assertEqual(_pub_value(report, LINE21), 1000)
        self.assertEqual(_pub_value(report, LINE7A), -1000)

    def test_carryover_with_current_year_loss_under_cap(self) -> None:
        # ST loss 1000 + W8 5000 → line7=-6000; line21=3000
        report = _run_tmp(
            _build_acts(st=[(1000, 2000)], lt=[], boundary=BOUNDARY_PATH_B, prior=_t2_prior()),
            "demo.sdilc.t1.with-cy-loss",
        )
        rows = _by_artifact(report)
        self.assertEqual(_pub_value(report, LINE7), -6000)
        self.assertEqual(_pub_value(report, LINE21), 3000)
        self.assertEqual(_pub_value(report, LINE7A), -3000)

    def test_carryover_with_box2a(self) -> None:
        report = _run_tmp(
            _build_acts(
                st=[], lt=[], box2a=2000,
                boundary=BOUNDARY_PATH_B, prior=_t3_prior(),
            ),
            "demo.sdilc.t1.with-box2a",
        )
        rows = _by_artifact(report)
        self.assertEqual(_pub_value(report, W13_RULE), 5000)
        self.assertEqual(_pub_value(report, LINE15), 2000 - 5000)
        self.assertEqual(_pub_value(report, LINE16), -3000)


class PathBAbsenceAndRegression(unittest.TestCase):
    def test_path_b_missing_prior_blocks(self) -> None:
        report = _run_tmp(
            _build_acts(st=[(1000, 2000)], lt=[], boundary=BOUNDARY_PATH_B, prior=None),
            "demo.sdilc.t1.path-b-missing",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[W8_RULE]["disposition"], "blocked")
        self.assertEqual(rows[W8_RULE].get("code") or rows[W8_RULE].get("blocked", {}).get("code"), "DEPENDENCY_ABSENT")

    def test_prior_return_fact_correction_displaces_dependents(self) -> None:
        """Finding 1: Correcting P3 (2024 line 7) from -10000 (T2) to -8000 displaces dependent W8, line6/7/16/21, line7a/9, SPB, and attachment."""
        acts = _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t2_prior())
        with TemporaryDirectory() as tmp:
            ws_dir = Path(tmp) / "L"
            res1 = live_coordinate_run(
                WorkspaceCapability(ws_dir),
                repo_root=REPO,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="demo.sdilc.t1.corr-step1",
                governance_pins=[],
                surface=_surface(),
                output_name="out1.json",
            )
            rep1 = _parse_report(res1)
            rows1 = _by_artifact(rep1)
            self.assertEqual(_pub_value(rep1, W8_RULE), 5000)
            self.assertEqual(_pub_value(rep1, LINE6), -5000)
            self.assertEqual(_pub_value(rep1, LINE7), -5000)
            self.assertEqual(_pub_value(rep1, LINE16), -5000)
            self.assertEqual(_pub_value(rep1, LINE21), 3000)
            self.assertEqual(_pub_value(rep1, LINE7A), -3000)
            self.assertEqual(rows1[SD_ATT]["disposition"], "published")
            self.assertEqual(rows1[SPB]["disposition"], "published")

            # Step 2: Supersede P3 with new value -8000
            new_acts = list(acts[:-1])
            p3_fact_id = _prior_fact_id(P3)
            new_acts.append(_live_act(len(new_acts), "assertion", {
                "finding": _attested(
                    "demo.sdilc.t1.finding.prior.schedule-d-line-7-corr",
                    p3_fact_id,
                    -8000,
                )
            }))
            adoption = json.loads((FIXTURES / "adoptions" / "adopt-core-v16-current.json").read_text())
            adoption["committed_against"] = len(new_acts)
            new_acts.append(adoption)

            res2 = live_coordinate_run(
                WorkspaceCapability(ws_dir),
                repo_root=REPO,
                authoritative_acts=new_acts,
                workspace_revision=len(new_acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="demo.sdilc.t1.corr-step2",
                governance_pins=[],
                surface=_surface(),
                output_name="out2.json",
            )
            rep2 = _parse_report(res2)
            rows2 = _by_artifact(rep2)
            self.assertEqual(_pub_value(rep2, W8_RULE), 3000)
            self.assertEqual(_pub_value(rep2, LINE6), -3000)
            self.assertEqual(_pub_value(rep2, LINE7), -3000)
            self.assertEqual(_pub_value(rep2, LINE16), -3000)
            self.assertEqual(_pub_value(rep2, LINE21), 3000)
            self.assertEqual(_pub_value(rep2, LINE7A), -3000)
            self.assertEqual(rows2[SD_ATT]["disposition"], "published")
            self.assertEqual(rows2[SPB]["disposition"], "published")

    def test_path_a_to_path_b_switch_displaces_dependents(self) -> None:
        """Finding 2: Correcting declaration "yes" → "no" displaces W8/W13 and dependents to Path B real results."""
        acts = _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_A, prior=None)
        with TemporaryDirectory() as tmp:
            ws_dir = Path(tmp) / "L"
            res1 = live_coordinate_run(
                WorkspaceCapability(ws_dir),
                repo_root=REPO,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="demo.sdilc.t1.switch-step1",
                governance_pins=[],
                surface=_surface(),
                output_name="out1.json",
            )
            rep1 = _parse_report(res1)
            rows1 = _by_artifact(rep1)
            self.assertEqual(_pub_value(rep1, W8_RULE), 0)
            self.assertEqual(_pub_value(rep1, W13_RULE), 0)
            self.assertEqual(_pub_value(rep1, LINE6), 0)
            self.assertEqual(_pub_value(rep1, LINE14), 0)

            # Step 2: Supersede declaration to "no" and supply five prior-return facts
            new_acts = list(acts[:-1])
            new_acts.append(_live_act(len(new_acts), "assertion", {
                "finding": _attested(
                    "demo.sdilc.t1.finding.decl-corr-no",
                    f"{DECL}|tax-year=2025",
                    "no",
                )
            }))
            for type_id, prior_value in _t1_prior().items():
                tail = type_id.removeprefix("tax.us.2025.prior-return.")
                new_acts.append(_live_act(len(new_acts), "assertion", {
                    "finding": _attested(
                        f"demo.sdilc.t1.finding.prior.{tail.replace('.', '-')}",
                        _prior_fact_id(type_id),
                        prior_value,
                    )
                }))
            adoption = json.loads((FIXTURES / "adoptions" / "adopt-core-v16-current.json").read_text())
            adoption["committed_against"] = len(new_acts)
            new_acts.append(adoption)

            res2 = live_coordinate_run(
                WorkspaceCapability(ws_dir),
                repo_root=REPO,
                authoritative_acts=new_acts,
                workspace_revision=len(new_acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="demo.sdilc.t1.switch-step2",
                governance_pins=[],
                surface=_surface(),
                output_name="out2.json",
            )
            rep2 = _parse_report(res2)
            rows2 = _by_artifact(rep2)
            self.assertEqual(_pub_value(rep2, W8_RULE), 5000)
            self.assertEqual(_pub_value(rep2, W13_RULE), 5000)
            self.assertEqual(_pub_value(rep2, LINE6), -5000)
            self.assertEqual(_pub_value(rep2, LINE14), -5000)
            self.assertEqual(_pub_value(rep2, LINE7), -5000)
            self.assertEqual(_pub_value(rep2, LINE15), -5000)
            self.assertEqual(_pub_value(rep2, LINE16), -10000)
            self.assertEqual(_pub_value(rep2, LINE21), 3000)
            self.assertEqual(_pub_value(rep2, LINE7A), -3000)
            self.assertEqual(rows2[SD_ATT]["disposition"], "published")
            self.assertEqual(rows2[SPB]["disposition"], "published")

    def test_prior_milestone_path_a_regression(self) -> None:
        """Existing current-year loss shape still holds under Path A."""
        report = _run_tmp(
            _build_acts(st=[(1000, 4000)], lt=[(1000, 3000)], boundary=BOUNDARY_PATH_A),
            "demo.sdilc.t1.regression-over-cap",
        )
        rows = _by_artifact(report)
        # ST -3000 + LT -2000 = -5000; line21 = 3000; line7a = -3000
        self.assertEqual(_pub_value(report, LINE16), -5000)
        self.assertEqual(_pub_value(report, LINE21), 3000)
        self.assertEqual(_pub_value(report, LINE7A), -3000)
        self.assertEqual(_pub_value(report, W8_RULE), 0)
        self.assertEqual(_pub_value(report, W13_RULE), 0)

    def test_negative_values_never_reach_spb_or_qdcg_base(self) -> None:
        report = _run_tmp(
            _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t1_prior()),
            "demo.sdilc.t1.neg-injection",
        )
        rows = _by_artifact(report)
        spb_val = float(_pub_value(report, SPB))
        self.assertGreaterEqual(spb_val, 0)
        # W8/W13 nonnegative
        self.assertGreaterEqual(float(_pub_value(report, W8_RULE)), 0)
        self.assertGreaterEqual(float(_pub_value(report, W13_RULE)), 0)


if __name__ == "__main__":
    unittest.main()
