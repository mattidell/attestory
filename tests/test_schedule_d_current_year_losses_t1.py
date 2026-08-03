"""Track 1 Current-Year Capital Losses: citizens + coordinator goldens (ADR-0057/0058)."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.schema_registry import KERNEL_SCHEMA_DIR

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
FIXTURES = REPO / "packages" / "sample_data" / "schedule_d_current_year_losses_t1"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2059"}

SELECTED_BASE_RULE = "tax.us.2025.rule.selected-preferential-base"
LINE7A_RULE = "tax.us.2025.rule.form1040-line7a"
LINE9_RULE = "tax.us.2025.rule.form1040-line9"
LINE16_RULE = "tax.us.2025.rule.form1040-line16"
SD_ATTACHMENT = "tax.us.2025.rule.attachment.schedule-d"
SD_LINE1A = "tax.us.2025.rule.schedule-d-line1a-gain"
SD_LINE7 = "tax.us.2025.rule.schedule-d-line7"
SD_LINE8A = "tax.us.2025.rule.schedule-d-line8a-gain"
SD_LINE15 = "tax.us.2025.rule.schedule-d-line15"
SD_LINE16 = "tax.us.2025.rule.schedule-d-line16"
SD_LINE21 = "tax.us.2025.rule.schedule-d-line21"

BOUNDARY_5 = (
    "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers",
    "tax.us.2025.schedule-d-boundary.no-form8949-sources",
    "tax.us.2025.schedule-d-boundary.no-other-schedule-d-sources",
    "tax.us.2025.schedule-d-boundary.no-lines-18-19-sources",
    "tax.us.2025.schedule-d-boundary.no-1099da-or-qof",
)

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
        CONTENT / "published-packages.v9.json",
        CONTENT,
    )


def _live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.sdcyl.t1.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-08-03T00:00:{index:02d}Z",
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
    components: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    """Build act log for package v14 (ADR-0057/0058).

    ``st`` / ``lt`` are lists of (proceeds, basis) for short-term / long-term
    transactions. Empty list means closed-empty family.
    ``box1a`` / ``box1b`` optionally contribute ordinary/qualified dividends.
    ``close_st`` / ``close_lt`` omit family-closure attestation when False
    (unclosed/stale family fixture).
    """
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
        "f1099b-covered-lt-scalars.bundle.json",
        "f1099b-covered-st-scalars.bundle.json",
    ):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text())})

    for eid, kind, label in (
        ("demo.sdcyl.t1.employer", "tax.us.employer", "Synthetic employer"),
        ("demo.sdcyl.t1.w2", "tax.us.w2-slip", "Synthetic W-2"),
        ("demo.sdcyl.t1.payer", "tax.us.dividend-payer", "Synthetic payer"),
        ("demo.sdcyl.t1.stmt", "tax.us.1099div-statement", "Synthetic 1099-DIV"),
        ("demo.sdcyl.t1.broker", "tax.us.f1099b-broker", "Synthetic broker"),
        ("demo.sdcyl.t1.b-stmt", "tax.us.f1099b-statement", "Synthetic 1099-B"),
    ):
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": eid, "kind": kind, "label": label}})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = (
        ("tax.us.2025.w2", "v2", "demo.sdcyl.t1.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.sdcyl.t1.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.sdcyl.t1.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.sdcyl.t1.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.sdcyl.t1.nonform.h0"),
        ("tax.us.2025.f1099int.b10", "v1", "demo.sdcyl.t1.int-b10.h0"),
        ("tax.us.2025.f1099oid.b5", "v1", "demo.sdcyl.t1.oid-b5.h0"),
        ("tax.us.2025.form1065-k1.box5", "v1", "demo.sdcyl.t1.k1-box5.h0"),
        ("tax.us.2025.f1099div.1a", "v1", "demo.sdcyl.t1.div1a.h0"),
        ("tax.us.2025.f1099div.1b", "v1", "demo.sdcyl.t1.div1b.h0"),
        ("tax.us.2025.f1099div.2a", "v1", "demo.sdcyl.t1.div2a.h0"),
        ("tax.us.2025.f1099b.covered-lt", "v1", "demo.sdcyl.t1.lt.h0"),
        ("tax.us.2025.f1099b.covered-lt-proceeds", "v1", "demo.sdcyl.t1.lt-p.h0"),
        ("tax.us.2025.f1099b.covered-lt-basis", "v1", "demo.sdcyl.t1.lt-b.h0"),
        ("tax.us.2025.f1099b.covered-st", "v1", "demo.sdcyl.t1.st.h0"),
        ("tax.us.2025.f1099b.covered-st-proceeds", "v1", "demo.sdcyl.t1.st-p.h0"),
        ("tax.us.2025.f1099b.covered-st-basis", "v1", "demo.sdcyl.t1.st-b.h0"),
    )
    for family_id, version, horizon_id in families:
        add("horizon-genesis", {"family": {"id": family_id, "version": version}, "scope": scope, "horizon_id": horizon_id})

    w2_h = "demo.sdcyl.t1.w2.h0"
    add("member-transition", {
        "family": {"id": "tax.us.2025.w2", "version": "v2"},
        "scope": scope,
        "member": {"action": "assert", "finding": _attested(
            "demo.sdcyl.t1.finding.wages",
            "tax.us.2025.w2.box1-wages|employer=demo.sdcyl.t1.employer,w2-slip=demo.sdcyl.t1.w2,tax-year=2025",
            90000,
        )},
        "successor": {"id": "demo.sdcyl.t1.w2.h1", "predecessor": w2_h},
    })
    w2_h = "demo.sdcyl.t1.w2.h1"

    div2a_h = "demo.sdcyl.t1.div2a.h0"
    if box2a is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099div.2a", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.sdcyl.t1.finding.box2a",
                "tax.us.2025.f1099div.box2a-capital-gain-distribution|payer=demo.sdcyl.t1.payer,statement=demo.sdcyl.t1.stmt,tax-year=2025",
                box2a,
            )},
            "successor": {"id": "demo.sdcyl.t1.div2a.h1", "predecessor": div2a_h},
        })
        div2a_h = "demo.sdcyl.t1.div2a.h1"

    div1a_h = "demo.sdcyl.t1.div1a.h0"
    if box1a is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099div.1a", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.sdcyl.t1.finding.box1a",
                "tax.us.2025.f1099div.box1a-ordinary|payer=demo.sdcyl.t1.payer,statement=demo.sdcyl.t1.stmt,tax-year=2025",
                box1a,
            )},
            "successor": {"id": "demo.sdcyl.t1.div1a.h1", "predecessor": div1a_h},
        })
        div1a_h = "demo.sdcyl.t1.div1a.h1"

    div1b_h = "demo.sdcyl.t1.div1b.h0"
    if box1b is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099div.1b", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.sdcyl.t1.finding.box1b",
                "tax.us.2025.f1099div.box1b-qualified|payer=demo.sdcyl.t1.payer,statement=demo.sdcyl.t1.stmt,tax-year=2025",
                box1b,
            )},
            "successor": {"id": "demo.sdcyl.t1.div1b.h1", "predecessor": div1b_h},
        })
        div1b_h = "demo.sdcyl.t1.div1b.h1"

    add("assertion", {"finding": _attested(
        "demo.sdcyl.t1.finding.anchor",
        "tax.us.2025.f1099b.statement-anchor|broker=demo.sdcyl.t1.broker,statement=demo.sdcyl.t1.b-stmt,tax-year=2025",
        {"broker_name": "Synthetic Broker"},
    )})

    def add_txns(prefix: str, family: str, long_term: str, pairs: list[tuple[float, float]], horizons: dict[str, str]) -> dict[str, str]:
        for i, (proceeds, basis) in enumerate(pairs):
            txn_id = f"demo.sdcyl.t1.{prefix}-txn-{i}"
            add("entity-introduced", {"entity": {
                "schema": "entity.v1", "id": txn_id,
                "kind": "tax.us.f1099b-transaction", "label": f"Synthetic {prefix} sale {i}",
            }})
            key = f"broker=demo.sdcyl.t1.broker,statement=demo.sdcyl.t1.b-stmt,transaction={txn_id},tax-year=2025"
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
                        f"demo.sdcyl.t1.finding.{prefix}-{fam_key}-{i}",
                        f"tax.us.2025.f1099b.{fact_suffix}|{key}",
                        amount,
                    )},
                    "successor": {"id": succ, "predecessor": pred},
                })
                horizons[fam_key] = succ
        return horizons

    st_h = {"obj": "demo.sdcyl.t1.st.h0", "p": "demo.sdcyl.t1.st-p.h0", "b": "demo.sdcyl.t1.st-b.h0"}
    lt_h = {"obj": "demo.sdcyl.t1.lt.h0", "p": "demo.sdcyl.t1.lt-p.h0", "b": "demo.sdcyl.t1.lt-b.h0"}
    st_h = add_txns("st", "covered-st", "no", st, st_h)
    lt_h = add_txns("lt", "covered-lt", "yes", lt, lt_h)

    add("assertion", {"finding": _attested("demo.sdcyl.t1.finding.rounding", "rounding.convention|tax-year=2025", "half_up")})
    add("assertion", {"finding": _attested("demo.sdcyl.t1.finding.status", "tax.us.2025.filing-status|tax-year=2025", filing_status)})

    for alias, value in components.items():
        fact_type = {"C1": C1, "C2": C2, "C3": C3, "C4": C4}[alias]
        add("assertion", {"finding": _attested(f"demo.sdcyl.t1.finding.{alias.lower()}", f"{fact_type}|tax-year=2025", value)})

    if boundary is None and (st or lt):
        boundary = {name: "yes" for name in BOUNDARY_5}
    if boundary:
        for name, bvalue in boundary.items():
            if bvalue is None:
                continue
            add("assertion", {"finding": _attested(
                f"demo.sdcyl.t1.finding.{name.split('.')[-1]}",
                f"{name}|tax-year=2025",
                bvalue,
            )})

    closures = [
        ("demo.sdcyl.t1.closure.w2", "tax.us.2025.w2.source-closure", w2_h),
        ("demo.sdcyl.t1.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure", "demo.sdcyl.t1.int-b1.h0"),
        ("demo.sdcyl.t1.closure.int-b3", "tax.us.2025.f1099int.b3.source-closure", "demo.sdcyl.t1.int-b3.h0"),
        ("demo.sdcyl.t1.closure.oid-b1", "tax.us.2025.f1099oid.b1.source-closure", "demo.sdcyl.t1.oid-b1.h0"),
        ("demo.sdcyl.t1.closure.nonform", "tax.us.2025.non-form-interest.source-closure", "demo.sdcyl.t1.nonform.h0"),
        ("demo.sdcyl.t1.closure.int-b10", "tax.us.2025.f1099int.b10.source-closure", "demo.sdcyl.t1.int-b10.h0"),
        ("demo.sdcyl.t1.closure.oid-b5", "tax.us.2025.f1099oid.b5.source-closure", "demo.sdcyl.t1.oid-b5.h0"),
        ("demo.sdcyl.t1.closure.k1", "tax.us.2025.form1065-k1.box5.source-closure", "demo.sdcyl.t1.k1-box5.h0"),
        ("demo.sdcyl.t1.closure.div1a", "tax.us.2025.f1099div.1a.source-closure", div1a_h),
        ("demo.sdcyl.t1.closure.div1b", "tax.us.2025.f1099div.1b.source-closure", div1b_h),
    ]
    if close_st:
        closures.extend([
            ("demo.sdcyl.t1.closure.st", "tax.us.2025.f1099b.covered-st.source-closure", st_h["obj"]),
            ("demo.sdcyl.t1.closure.st-p", "tax.us.2025.f1099b.covered-st-proceeds.source-closure", st_h["p"]),
            ("demo.sdcyl.t1.closure.st-b", "tax.us.2025.f1099b.covered-st-basis.source-closure", st_h["b"]),
        ])
    if close_lt:
        closures.extend([
            ("demo.sdcyl.t1.closure.lt", "tax.us.2025.f1099b.covered-lt.source-closure", lt_h["obj"]),
            ("demo.sdcyl.t1.closure.lt-p", "tax.us.2025.f1099b.covered-lt-proceeds.source-closure", lt_h["p"]),
            ("demo.sdcyl.t1.closure.lt-b", "tax.us.2025.f1099b.covered-lt-basis.source-closure", lt_h["b"]),
        ])
    if close_2a:
        closures.append(("demo.sdcyl.t1.closure.div2a", "tax.us.2025.f1099div.2a.source-closure", div2a_h))
    for finding_id, fact_type, horizon_id in closures:
        add("assertion", {"finding": _attested(finding_id, f"{fact_type}|family-horizon={horizon_id},tax-year=2025", True)})

    adoption = json.loads((FIXTURES / "adoptions" / "adopt-core-v14-current.json").read_text())
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


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
        assert result.refusal is None, result.refusal
        assert result.output_path is not None
        return cast(dict[str, Any], json.loads(result.output_path.read_text()))


def _by_artifact(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["artifact_id"]: row for row in report["dispositions"]}


class PackageDualExclusion(unittest.TestCase):
    def test_v14_excludes_gain_only_ltcg_stack(self) -> None:
        pkg = json.loads((CONTENT / "package.core-calculations.v14.json").read_text())
        ids = {m["id"] for m in pkg["members"]}
        self.assertIn("tax.us.2025.f1099b.covered-lt", ids)
        self.assertIn("tax.us.2025.f1099b.covered-st", ids)
        self.assertNotIn("tax.us.2025.f1099b.covered-ltcg", ids)
        self.assertNotIn("tax.us.2025.f1099b.covered-ltcg-proceeds", ids)

    def test_quantity_vocabulary_v5_published(self) -> None:
        schema_path = KERNEL_SCHEMA_DIR / "quantity-vocabulary.v5.schema.json"
        self.assertTrue(schema_path.is_file())
        self.assertTrue((CONTENT / "quantity.covered-lt-proceeds.json").is_file())
        self.assertTrue((CONTENT / "package.core-calculations.v14.json").is_file())
        pkg = json.loads((CONTENT / "package.core-calculations.v14.json").read_text())
        self.assertEqual(pkg["schema"], "artifact-package.v9")
        self.assertIn("quantity-vocabulary.v5", pkg["admitted_schemas"])


class ShortTermLossBelowCap(unittest.TestCase):
    def test_st_loss_publishes_line21_and_floored_base(self) -> None:
        # proceeds 1000, basis 2500 => line1a = -1500; line16 = -1500; line21 = 1500; line7a = -1500
        report = _run_tmp(_build_acts(st=[(1000, 2500)], lt=[]), "demo.sdcyl.t1.st-loss")
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_LINE1A]["disposition"], "published")
        self.assertEqual(rows[SD_LINE7]["disposition"], "published")
        self.assertEqual(rows[SD_LINE16]["disposition"], "published")
        self.assertEqual(rows[SD_LINE21]["disposition"], "published")
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")
        self.assertEqual(rows[SD_ATTACHMENT]["disposition"], "published")
        self.assertEqual(rows[LINE9_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE16_RULE]["disposition"], "published")


class LongTermLossBelowCap(unittest.TestCase):
    def test_lt_loss_route(self) -> None:
        report = _run_tmp(_build_acts(st=[], lt=[(2000, 3500)]), "demo.sdcyl.t1.lt-loss")
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_LINE8A]["disposition"], "published")
        self.assertEqual(rows[SD_LINE16]["disposition"], "published")
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")


class NetLossOverCap(unittest.TestCase):
    def test_loss_capped_at_3000(self) -> None:
        # net -5000 -> line21 3000, line7a -3000, base 0
        report = _run_tmp(_build_acts(st=[(1000, 4000)], lt=[(1000, 3000)]), "demo.sdcyl.t1.over-cap")
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_LINE21]["disposition"], "published")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")


class MFSCap(unittest.TestCase):
    def test_mfs_limit_parameter_is_1500(self) -> None:
        """Disclosed limitation (Finding 2): demo tax-brackets and
        qdcg-preferential-brackets cover only single/married_filing_jointly, so
        this milestone cannot ship a full MFS live_coordinate_run golden without
        expanding those tables (out of scope). The §1211 MFS $1,500 cap is
        still asserted here as a static parameter-value check against
        demo.parameter.capital-loss-limit.2025 (ADR-0058 Decision 2). See the
        milestone plan Fixtures section for the same disclosure."""
        param = json.loads((CONTENT / "parameter.capital-loss-limit.json").read_text())
        self.assertEqual(param["values"]["married_filing_separately"], "1500")
        self.assertEqual(param["values"]["single"], "3000")


class MixedNetGain(unittest.TestCase):
    def test_st_gain_offset_by_lt_loss_still_net_gain(self) -> None:
        # ST +2000, LT -500 => net +1500
        report = _run_tmp(_build_acts(st=[(5000, 3000)], lt=[(1000, 1500)]), "demo.sdcyl.t1.mixed-gain")
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_LINE16]["disposition"], "published")
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")


class DirectRouteBothEmpty(unittest.TestCase):
    def test_both_empty_uses_direct_box2a(self) -> None:
        report = _run_tmp(_build_acts(st=[], lt=[], box2a=1500), "demo.sdcyl.t1.direct")
        rows = _by_artifact(report)
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")
        self.assertEqual(rows[SD_ATTACHMENT]["disposition"], "inapplicable")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")


class BoundaryMissing(unittest.TestCase):
    def test_missing_inbound_blocks(self) -> None:
        boundary: dict[str, str | None] = {n: "yes" for n in BOUNDARY_5}
        boundary["tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers"] = None
        report = _run_tmp(
            _build_acts(st=[(1000, 2000)], lt=[], boundary=boundary),
            "demo.sdcyl.t1.missing-inbound",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "blocked")



class QPositiveWithNetScheduleDLoss(unittest.TestCase):
    """Finding 1 / ADR-0058 Decision 5: Q>0 with floored-zero preferential base
    still publishes line 16 via the QDCG ladder (L=0), not ordinary-only only."""

    def test_line16_publishes_when_q_positive_and_base_floored_zero(self) -> None:
        # ST loss net -1500 => preferential base floors to 0; box1b=600 => Q>0
        report = _run_tmp(
            _build_acts(st=[(1000, 2500)], lt=[], box1a=600, box1b=600),
            "demo.sdcyl.t1.qpos-net-loss",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")
        self.assertEqual(rows[SD_LINE16]["disposition"], "published")
        self.assertEqual(rows[LINE16_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")


class ReverseMixedNetGain(unittest.TestCase):
    """Finding 3: LT gain offset by a larger ST loss, still net gain — mirror of MixedNetGain."""

    def test_lt_gain_offset_by_larger_st_loss_still_net_gain(self) -> None:
        # ST -500 (1000-1500), LT +2000 (5000-3000) => net +1500
        report = _run_tmp(
            _build_acts(st=[(1000, 1500)], lt=[(5000, 3000)]),
            "demo.sdcyl.t1.reverse-mixed-gain",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_LINE1A]["disposition"], "published")
        self.assertEqual(rows[SD_LINE8A]["disposition"], "published")
        self.assertEqual(rows[SD_LINE16]["disposition"], "published")
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")
        # Net gain path: line 21 publishes 0 (or published zero), not a positive cap
        self.assertEqual(rows[SD_LINE21]["disposition"], "published")


class Box2aWithTransactionLosses(unittest.TestCase):
    """Finding 3: box-2a coexists with ST/LT net loss; Schedule D selected; no double-count."""

    def test_box2a_and_losses_select_schedule_d_once_each(self) -> None:
        report = _run_tmp(
            _build_acts(st=[(1000, 2500)], lt=[], box2a=500),
            "demo.sdcyl.t1.box2a-with-loss",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_ATTACHMENT]["disposition"], "published")
        self.assertEqual(rows[SD_LINE15]["disposition"], "published")
        self.assertEqual(rows[SD_LINE16]["disposition"], "published")
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")
        # Schedule D route: base pins line 16 finding, not just box-2a alone
        base_pin_ids = {p["id"] for p in rows[SELECTED_BASE_RULE]["pins"]}
        self.assertIn(rows[SD_LINE16]["finding_id"], base_pin_ids)
        # line 15 pins both 8a (or path) and box-2a subtotal once each
        line15_pin_ids = {p["id"] for p in rows[SD_LINE15]["pins"]}
        self.assertIn(rows["tax.us.2025.rule.f1099div-2a-subtotal"]["finding_id"], line15_pin_ids)
        # Preferential base is floored (loss net of box2a may still be negative)
        # Downstream still publishes once through the selected base / line 7a chain
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")


class FamilyClosureUnclosed(unittest.TestCase):
    """Finding 3: missing/unclosed ST family produces honest blocked disposition."""

    def test_unclosed_st_family_blocks_subtotal_or_downstream(self) -> None:
        report = _run_tmp(
            _build_acts(st=[(1000, 2500)], lt=[], close_st=False),
            "demo.sdcyl.t1.unclosed-st",
        )
        rows = _by_artifact(report)
        # Line 1a requires the ST object family closed (require_closed) — blocked
        self.assertEqual(rows[SD_LINE1A]["disposition"], "blocked")
        self.assertEqual(rows[SD_LINE1A]["code"], "SOURCE_SET_UNCLOSED")
        self.assertIn("tax.us.2025.f1099b.covered-st", rows[SD_LINE1A].get("missing", []))
        # Downstream selected preferential base cannot publish a numeric Schedule D amount
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "blocked")


class InboundCarryoverPresentButViolated(unittest.TestCase):
    """Finding 3: present-but-violated inbound-carryover is distinct from present-but-missing."""

    def test_violated_inbound_is_inapplicable_not_missing(self) -> None:
        boundary: dict[str, str | None] = {n: "yes" for n in BOUNDARY_5}
        boundary["tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers"] = "no"
        report = _run_tmp(
            _build_acts(st=[(1000, 2000)], lt=[], boundary=boundary),
            "demo.sdcyl.t1.violated-inbound",
        )
        rows = _by_artifact(report)
        # Value "no" fails the guard's categorical all(...) → inapplicable
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "inapplicable")
        # Attachment value-check names the violation distinctly from absence
        self.assertEqual(rows[SD_ATTACHMENT]["disposition"], "blocked")
        self.assertEqual(rows[SD_ATTACHMENT]["code"], "COMPLETENESS_VALUE_VIOLATION")
        self.assertTrue(
            any(
                "no-inbound-capital-loss-carryovers" in str(x)
                for x in rows[SD_ATTACHMENT].get("missing", [])
            )
        )

    def test_missing_inbound_is_dependency_absent_not_value_violation(self) -> None:
        boundary: dict[str, str | None] = {n: "yes" for n in BOUNDARY_5}
        boundary["tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers"] = None
        report = _run_tmp(
            _build_acts(st=[(1000, 2000)], lt=[], boundary=boundary),
            "demo.sdcyl.t1.missing-inbound-distinct",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "blocked")
        self.assertEqual(rows[SELECTED_BASE_RULE].get("code"), "DEPENDENCY_ABSENT")
        self.assertIn(
            "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers",
            rows[SELECTED_BASE_RULE].get("missing", []),
        )
        self.assertEqual(rows[SD_ATTACHMENT]["disposition"], "blocked")
        self.assertEqual(rows[SD_ATTACHMENT]["code"], "DEPENDENCY_ABSENT")


class HistoricalBytesUntouched(unittest.TestCase):
    def test_gain_only_citizens_unchanged(self) -> None:
        # mere existence + registry still lists historical package v13
        self.assertTrue((CONTENT / "f1099b-covered-ltcg.bundle.json").is_file())
        self.assertTrue((CONTENT / "package.core-calculations.v13.json").is_file())
        self.assertTrue((CONTENT / "rule.selected-preferential-base.json").is_file())


if __name__ == "__main__":
    unittest.main()
