"""Track 2 Schedule D Covered LTCG: coordinator-from-facts goldens.

Every named class enters exclusively through ``live_coordinate_run`` from an
authoritative act log (never a hand-built ``RunContext``), against package
``tax.us.2025.package.core-calculations`` v11 (ADR-0052/0053/0054).
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
FIXTURES = REPO / "packages" / "sample_data" / "schedule_d_covered_ltcg_8a_t2"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2059"}

CONCLUSION_RULE = "tax.us.2025.rule.schedule-d-required.conclusion"
SELECTED_BASE_RULE = "tax.us.2025.rule.selected-preferential-base"
LINE7A_RULE = "tax.us.2025.rule.form1040-line7a"
LINE9_RULE = "tax.us.2025.rule.form1040-line9"
LINE16_RULE = "tax.us.2025.rule.form1040-line16"
SD_ATTACHMENT = "tax.us.2025.rule.attachment.schedule-d"
SD_LINE8A_GAIN = "tax.us.2025.rule.schedule-d-line8a-gain"
SD_LINE15 = "tax.us.2025.rule.schedule-d-line15"
SD_LINE16 = "tax.us.2025.rule.schedule-d-line16"
PROCEEDS_SUBTOTAL_RULE = "tax.us.2025.rule.f1099b-covered-ltcg-proceeds-subtotal"
BASIS_SUBTOTAL_RULE = "tax.us.2025.rule.f1099b-covered-ltcg-basis-subtotal"

C1 = "tax.us.2025.exception1.only-box2a-capital-gains"
C2 = "tax.us.2025.exception1.no-capital-losses"
C3 = "tax.us.2025.exception1.no-qof-deferral"
C4 = "tax.us.2025.exception1.no-boxes-2b-2c-2d"

BOUNDARY_DECLARATIONS = (
    "tax.us.2025.schedule-d-boundary.no-short-term-transactions",
    "tax.us.2025.schedule-d-boundary.no-current-capital-losses",
    "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers",
    "tax.us.2025.schedule-d-boundary.no-form8949-sources",
    "tax.us.2025.schedule-d-boundary.no-other-schedule-d-sources",
    "tax.us.2025.schedule-d-boundary.no-lines-18-19-sources",
    "tax.us.2025.schedule-d-boundary.no-1099da-or-qof",
)

_ELIGIBLE_TXN_VALUE = {
    "proceeds": 6000,
    "basis": 2000,
    "covered_security": "yes",
    "basis_reported_to_irs": "yes",
    "long_term": "yes",
    "box_1f_market_discount": "no",
    "box_1g_wash_sale_adjustment": "no",
    "ordinary_indicated": "no",
    "qof_indicated": "no",
    "taxpayer_side_adjustment": "no",
    "collectibles_or_special_rate": "no",
    "gain_only": "yes",
}


def _act(name: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads((FIXTURES / "adoptions" / name).read_text("utf-8")))


def _surface(registry: str = "published-packages.v6.json") -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases", CONTENT / registry, CONTENT
    )


def _live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.sdcl.t2.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-08-02T00:00:{index:02d}Z",
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


def _sdcl_t2_acts(
    *,
    box2a: float | None = None,
    close_2a: bool = True,
    components: dict[str, str | None] | None = None,
    eligible_txn: bool = False,
    close_eligible: bool = True,
    boundary: dict[str, str | None] | None = None,
    adoption_file: str = "adopt-core-v11-current.json",
    correction: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    """Build a minimal act log against package v11 (or ``adoption_file``).

    ``eligible_txn`` admits one covered-long-term-gain transaction (and its
    twin scalar companions) on one broker statement anchor. ``boundary``
    overrides the seven Schedule D absence declarations (default: all "yes"
    when an eligible transaction is present, omitted entirely otherwise -
    ADR-0053 Decision 1's boundary declarations are never required by the
    direct-route/closed-empty branch). ``correction`` supersedes one or more
    boundary declarations with a new current value after the initial batch
    (ADR-0055's T0->T1->T2 lifecycle trace), ordinary free supersession at
    the same fact identity, not a new finding kind.
    """
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
        "f1099b-covered-ltcg.bundle.json",
        "schedule-d-boundary.bundle.json",
        "f1099b-covered-ltcg-scalars.bundle.json",
    ):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text())})

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.sdcl.t2.employer", "kind": "tax.us.employer", "label": "Synthetic employer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.sdcl.t2.w2", "kind": "tax.us.w2-slip", "label": "Synthetic W-2"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.sdcl.t2.payer", "kind": "tax.us.dividend-payer", "label": "Synthetic payer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.sdcl.t2.stmt", "kind": "tax.us.1099div-statement", "label": "Synthetic 1099-DIV"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.sdcl.t2.broker", "kind": "tax.us.f1099b-broker", "label": "Synthetic broker"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.sdcl.t2.b-stmt", "kind": "tax.us.f1099b-statement", "label": "Synthetic 1099-B"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.sdcl.t2.b-txn", "kind": "tax.us.f1099b-transaction", "label": "Synthetic sale"}})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = (
        ("tax.us.2025.w2", "v2", "demo.sdcl.t2.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.sdcl.t2.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.sdcl.t2.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.sdcl.t2.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.sdcl.t2.nonform.h0"),
        ("tax.us.2025.f1099int.b10", "v1", "demo.sdcl.t2.int-b10.h0"),
        ("tax.us.2025.f1099oid.b5", "v1", "demo.sdcl.t2.oid-b5.h0"),
        ("tax.us.2025.form1065-k1.box5", "v1", "demo.sdcl.t2.k1-box5.h0"),
        ("tax.us.2025.f1099div.1a", "v1", "demo.sdcl.t2.div1a.h0"),
        ("tax.us.2025.f1099div.1b", "v1", "demo.sdcl.t2.div1b.h0"),
        ("tax.us.2025.f1099div.2a", "v1", "demo.sdcl.t2.div2a.h0"),
        ("tax.us.2025.f1099b.covered-ltcg", "v1", "demo.sdcl.t2.eligible.h0"),
        ("tax.us.2025.f1099b.covered-ltcg-proceeds", "v1", "demo.sdcl.t2.proceeds.h0"),
        ("tax.us.2025.f1099b.covered-ltcg-basis", "v1", "demo.sdcl.t2.basis.h0"),
    )
    for family_id, version, horizon_id in families:
        add("horizon-genesis", {"family": {"id": family_id, "version": version}, "scope": scope, "horizon_id": horizon_id})

    w2_horizon = "demo.sdcl.t2.w2.h0"
    add("member-transition", {
        "family": {"id": "tax.us.2025.w2", "version": "v2"},
        "scope": scope,
        "member": {"action": "assert", "finding": _attested(
            "demo.sdcl.t2.finding.wages",
            "tax.us.2025.w2.box1-wages|employer=demo.sdcl.t2.employer,w2-slip=demo.sdcl.t2.w2,tax-year=2025",
            90000,
        )},
        "successor": {"id": "demo.sdcl.t2.w2.h1", "predecessor": w2_horizon},
    })
    w2_horizon = "demo.sdcl.t2.w2.h1"

    div2a_horizon = "demo.sdcl.t2.div2a.h0"
    if box2a is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099div.2a", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.sdcl.t2.finding.box2a",
                "tax.us.2025.f1099div.box2a-capital-gain-distribution|payer=demo.sdcl.t2.payer,statement=demo.sdcl.t2.stmt,tax-year=2025",
                box2a,
            )},
            "successor": {"id": "demo.sdcl.t2.div2a.h1", "predecessor": div2a_horizon},
        })
        div2a_horizon = "demo.sdcl.t2.div2a.h1"

    eligible_horizon = "demo.sdcl.t2.eligible.h0"
    proceeds_horizon = "demo.sdcl.t2.proceeds.h0"
    basis_horizon = "demo.sdcl.t2.basis.h0"
    if eligible_txn:
        add("assertion", {"finding": _attested(
            "demo.sdcl.t2.finding.anchor",
            "tax.us.2025.f1099b.statement-anchor|broker=demo.sdcl.t2.broker,statement=demo.sdcl.t2.b-stmt,tax-year=2025",
            {"broker_name": "Synthetic Broker"},
        )})
        txn_key = "broker=demo.sdcl.t2.broker,statement=demo.sdcl.t2.b-stmt,transaction=demo.sdcl.t2.b-txn,tax-year=2025"
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099b.covered-ltcg", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.sdcl.t2.finding.eligible-txn",
                f"tax.us.2025.f1099b.covered-ltcg-txn|{txn_key}",
                _ELIGIBLE_TXN_VALUE,
            )},
            "successor": {"id": "demo.sdcl.t2.eligible.h1", "predecessor": eligible_horizon},
        })
        eligible_horizon = "demo.sdcl.t2.eligible.h1"
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099b.covered-ltcg-proceeds", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.sdcl.t2.finding.proceeds",
                f"tax.us.2025.f1099b.covered-ltcg-txn.proceeds|{txn_key}",
                _ELIGIBLE_TXN_VALUE["proceeds"],
            )},
            "successor": {"id": "demo.sdcl.t2.proceeds.h1", "predecessor": proceeds_horizon},
        })
        proceeds_horizon = "demo.sdcl.t2.proceeds.h1"
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099b.covered-ltcg-basis", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.sdcl.t2.finding.basis",
                f"tax.us.2025.f1099b.covered-ltcg-txn.basis|{txn_key}",
                _ELIGIBLE_TXN_VALUE["basis"],
            )},
            "successor": {"id": "demo.sdcl.t2.basis.h1", "predecessor": basis_horizon},
        })
        basis_horizon = "demo.sdcl.t2.basis.h1"

    add("assertion", {"finding": _attested("demo.sdcl.t2.finding.rounding", "rounding.convention|tax-year=2025", "half_up")})
    add("assertion", {"finding": _attested("demo.sdcl.t2.finding.status", "tax.us.2025.filing-status|tax-year=2025", "single")})

    component_facts = {"C1": (C1, "demo.sdcl.t2.finding.c1"), "C2": (C2, "demo.sdcl.t2.finding.c2"),
                        "C3": (C3, "demo.sdcl.t2.finding.c3"), "C4": (C4, "demo.sdcl.t2.finding.c4")}
    for alias, value in components.items():
        if value is None:
            continue
        fact_type, fid = component_facts[alias]
        add("assertion", {"finding": _attested(fid, f"{fact_type}|tax-year=2025", value)})

    if boundary is None and eligible_txn:
        boundary = {name: "yes" for name in BOUNDARY_DECLARATIONS}
    if boundary:
        for name, value in boundary.items():
            if value is None:
                continue
            add("assertion", {"finding": _attested(f"demo.sdcl.t2.finding.{name.split('.')[-1]}", f"{name}|tax-year=2025", value)})

    closures = [
        ("demo.sdcl.t2.closure.w2", "tax.us.2025.w2.source-closure", w2_horizon),
        ("demo.sdcl.t2.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure", "demo.sdcl.t2.int-b1.h0"),
        ("demo.sdcl.t2.closure.int-b3", "tax.us.2025.f1099int.b3.source-closure", "demo.sdcl.t2.int-b3.h0"),
        ("demo.sdcl.t2.closure.oid-b1", "tax.us.2025.f1099oid.b1.source-closure", "demo.sdcl.t2.oid-b1.h0"),
        ("demo.sdcl.t2.closure.nonform", "tax.us.2025.non-form-interest.source-closure", "demo.sdcl.t2.nonform.h0"),
        ("demo.sdcl.t2.closure.int-b10", "tax.us.2025.f1099int.b10.source-closure", "demo.sdcl.t2.int-b10.h0"),
        ("demo.sdcl.t2.closure.oid-b5", "tax.us.2025.f1099oid.b5.source-closure", "demo.sdcl.t2.oid-b5.h0"),
        ("demo.sdcl.t2.closure.k1-box5", "tax.us.2025.form1065-k1.box5.source-closure", "demo.sdcl.t2.k1-box5.h0"),
        ("demo.sdcl.t2.closure.div1a", "tax.us.2025.f1099div.1a.source-closure", "demo.sdcl.t2.div1a.h0"),
        ("demo.sdcl.t2.closure.div1b", "tax.us.2025.f1099div.1b.source-closure", "demo.sdcl.t2.div1b.h0"),
        ("demo.sdcl.t2.closure.eligible", "tax.us.2025.f1099b.covered-ltcg.source-closure", eligible_horizon),
        ("demo.sdcl.t2.closure.proceeds", "tax.us.2025.f1099b.covered-ltcg-proceeds.source-closure", proceeds_horizon),
        ("demo.sdcl.t2.closure.basis", "tax.us.2025.f1099b.covered-ltcg-basis.source-closure", basis_horizon),
    ]
    if close_2a:
        closures.append(("demo.sdcl.t2.closure.div2a", "tax.us.2025.f1099div.2a.source-closure", div2a_horizon))
    if not close_eligible:
        closures = [c for c in closures if c[0] != "demo.sdcl.t2.closure.eligible"]
    for finding_id, fact_type, horizon_id in closures:
        add("assertion", {"finding": _attested(finding_id, f"{fact_type}|family-horizon={horizon_id},tax-year=2025", True)})

    if correction:
        for name, value in correction.items():
            add("assertion", {"finding": _attested(
                f"demo.sdcl.t2.finding.{name.split('.')[-1]}.correction",
                f"{name}|tax-year=2025",
                value,
            )})

    adoption = _act(adoption_file)
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _run(
    acts: list[dict[str, object]], run_id: str, root: Path,
    registry: str = "published-packages.v6.json",
) -> dict[str, Any]:
    result = live_coordinate_run(
        WorkspaceCapability(root / "L"),
        repo_root=REPO,
        authoritative_acts=acts,
        workspace_revision=len(acts),
        run_scope=SCOPE,
        scope_user=USER,
        request={"schema": "run-request.v1"},
        run_id=run_id,
        governance_pins=[],
        surface=_surface(registry),
        output_name="out.json",
    )
    assert result.refusal is None, result.refusal
    assert result.output_path is not None
    return cast(dict[str, Any], json.loads(result.output_path.read_text()))


def _run_tmp(
    acts: list[dict[str, object]], run_id: str,
    registry: str = "published-packages.v6.json",
) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        return _run(acts, run_id, Path(tmp), registry)


def _by_artifact(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["artifact_id"]: row for row in report["dispositions"]}


class DirectRouteClosedEmptyEligibleFamily(unittest.TestCase):
    """No eligible 1099-B transactions: direct route publishes exactly as ADR-0050,
    the seven Schedule D boundary declarations are never required."""

    def test_direct_route_publishes_without_boundary_declarations(self) -> None:
        report = _run_tmp(_sdcl_t2_acts(box2a=1500, eligible_txn=False), "demo.sdcl.t2.direct-route")
        rows = _by_artifact(report)
        self.assertEqual(rows[CONCLUSION_RULE]["disposition"], "published")
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE9_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE16_RULE]["disposition"], "published")
        self.assertEqual(rows[SD_ATTACHMENT]["disposition"], "inapplicable")
        # The selected preferential base's finding pins the direct producer's
        # signature only - box-2a subtotal + conclusion - never a Schedule D symbol.
        base_pin_ids = {p["id"] for p in rows[SELECTED_BASE_RULE]["pins"]}
        self.assertNotIn(rows[SD_LINE16]["finding_id"], base_pin_ids)


class ScheduleDRouteEligibleTransaction(unittest.TestCase):
    """One eligible covered-LTCG transaction, closed-empty box 2a, all seven
    boundary declarations yes: the Schedule D producer is selected."""

    def test_schedule_d_route_publishes_and_line9_includes_once(self) -> None:
        report = _run_tmp(
            _sdcl_t2_acts(box2a=None, close_2a=True, eligible_txn=True),
            "demo.sdcl.t2.schedule-d-route",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[PROCEEDS_SUBTOTAL_RULE]["disposition"], "published")
        self.assertEqual(rows[BASIS_SUBTOTAL_RULE]["disposition"], "published")
        self.assertEqual(rows[SD_LINE8A_GAIN]["disposition"], "published")
        self.assertEqual(rows[SD_LINE15]["disposition"], "published")
        self.assertEqual(rows[SD_LINE16]["disposition"], "published")
        self.assertEqual(rows[SD_ATTACHMENT]["disposition"], "published")
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE9_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE16_RULE]["disposition"], "published")
        # The selected preferential base's finding pins the Schedule D
        # producer's signature only - the untaken direct branch's box-2a
        # subtotal / conclusion / C1-C4 are never named or pinned.
        base_pin_ids = {p["id"] for p in rows[SELECTED_BASE_RULE]["pins"]}
        self.assertIn(rows[SD_LINE16]["finding_id"], base_pin_ids)
        self.assertNotIn(rows[CONCLUSION_RULE].get("finding_id"), base_pin_ids)


class ScheduleDRouteMissingBoundaryDeclaration(unittest.TestCase):
    """An eligible transaction with one boundary declaration missing: the
    selected preferential base blocks naming exactly the missing declaration."""

    def test_missing_declaration_blocks_naming_it(self) -> None:
        boundary: dict[str, str | None] = {name: "yes" for name in BOUNDARY_DECLARATIONS}
        boundary["tax.us.2025.schedule-d-boundary.no-form8949-sources"] = None
        report = _run_tmp(
            _sdcl_t2_acts(box2a=None, close_2a=True, eligible_txn=True, boundary=boundary),
            "demo.sdcl.t2.missing-declaration",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "blocked")
        self.assertIn(
            "tax.us.2025.schedule-d-boundary.no-form8949-sources",
            rows[SELECTED_BASE_RULE]["missing"],
        )
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE9_RULE]["disposition"], "blocked")


class ScheduleDRouteViolatedBoundaryDeclaration(unittest.TestCase):
    """An eligible transaction with one boundary declaration answered "no":
    a known violation of ADR-0052 Decision 2's bounded source class. The
    selected-preferential-base rule re-checks declaration *values* (not just
    presence) and correctly goes inapplicable, blocking every downstream
    numeric publication - no fabricated tax result. Known gap (see handoff):
    the attachment citizen's own required-and-complete/incomplete disposition
    uses ADR-0036's generic completeness check, which is presence-only (built
    for Schedule B's different semantics); it does not yet distinguish a
    declared "no" from a declared "yes" and remains "published" here."""

    def test_violated_declaration_is_inapplicable_not_a_fabricated_publish(self) -> None:
        boundary: dict[str, str | None] = {name: "yes" for name in BOUNDARY_DECLARATIONS}
        boundary["tax.us.2025.schedule-d-boundary.no-current-capital-losses"] = "no"
        report = _run_tmp(
            _sdcl_t2_acts(box2a=None, close_2a=True, eligible_txn=True, boundary=boundary),
            "demo.sdcl.t2.violated-declaration",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "inapplicable")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE9_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE16_RULE]["disposition"], "blocked")


class BothGainsPreservedExactlyOnce(unittest.TestCase):
    """Box 2a present-and-nonzero alongside an eligible transaction: the
    Schedule D route is selected (C1 cannot hold), and box 2a flows through
    Schedule D line 13 exactly once, not lost and not double-counted."""

    def test_box2a_and_eligible_transaction_both_flow_through_line15(self) -> None:
        report = _run_tmp(
            _sdcl_t2_acts(box2a=500, close_2a=True, eligible_txn=True),
            "demo.sdcl.t2.both-gains",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_LINE8A_GAIN]["disposition"], "published")
        self.assertEqual(rows[SD_LINE15]["disposition"], "published")
        # line 15 pins both line 8a's gain and the box-2a subtotal, exactly once each.
        line15_pin_ids = {p["id"] for p in rows[SD_LINE15]["pins"]}
        self.assertIn(rows[SD_LINE8A_GAIN]["finding_id"], line15_pin_ids)
        self.assertIn(rows["tax.us.2025.rule.f1099div-2a-subtotal"]["finding_id"], line15_pin_ids)
        # The Schedule D route is selected despite a nonzero box-2a subtotal:
        # C1 (only box-2a gains) cannot hold once an eligible 1099-B gain exists.
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")
        base_pin_ids = {p["id"] for p in rows[SELECTED_BASE_RULE]["pins"]}
        self.assertIn(rows[SD_LINE16]["finding_id"], base_pin_ids)


class AttachmentCompletenessViolationConverges(unittest.TestCase):
    """ADR-0055 N1: a present, current, disqualifying declaration now makes
    the attachment's own disposition agree with selected-preferential-base,
    against package v12 (attachment-rule.v4)."""

    def test_violated_declaration_blocks_attachment_naming_it(self) -> None:
        boundary: dict[str, str | None] = {name: "yes" for name in BOUNDARY_DECLARATIONS}
        boundary["tax.us.2025.schedule-d-boundary.no-current-capital-losses"] = "no"
        report = _run_tmp(
            _sdcl_t2_acts(
                box2a=None, close_2a=True, eligible_txn=True, boundary=boundary,
                adoption_file="adopt-core-v12-current.json",
            ),
            "demo.sdcl.t2.v12.violated",
            registry="published-packages.v7.json",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_ATTACHMENT]["disposition"], "blocked")
        self.assertEqual(rows[SD_ATTACHMENT]["code"], "COMPLETENESS_VALUE_VIOLATION")
        self.assertIn(
            "tax.us.2025.schedule-d-boundary.no-current-capital-losses=no",
            rows[SD_ATTACHMENT]["missing"],
        )
        # Both authorities now agree: the numeric route is inapplicable too.
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "inapplicable")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "blocked")


class AttachmentAbsenceUnaffected(unittest.TestCase):
    """ADR-0055 N2 (contrast case): an absent declaration is unaffected -
    still DEPENDENCY_ABSENT naming the missing symbol, no value read."""

    def test_missing_declaration_still_dependency_absent(self) -> None:
        boundary: dict[str, str | None] = {name: "yes" for name in BOUNDARY_DECLARATIONS}
        boundary["tax.us.2025.schedule-d-boundary.no-form8949-sources"] = None
        report = _run_tmp(
            _sdcl_t2_acts(
                box2a=None, close_2a=True, eligible_txn=True, boundary=boundary,
                adoption_file="adopt-core-v12-current.json",
            ),
            "demo.sdcl.t2.v12.absent",
            registry="published-packages.v7.json",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_ATTACHMENT]["disposition"], "blocked")
        self.assertEqual(rows[SD_ATTACHMENT]["code"], "DEPENDENCY_ABSENT")
        self.assertIn(
            "tax.us.2025.schedule-d-boundary.no-form8949-sources",
            rows[SD_ATTACHMENT]["missing"],
        )


class AttachmentPositiveUnaffected(unittest.TestCase):
    """ADR-0055 P1: all seven declarations "yes" - unaffected, still
    published (required-and-complete), against package v12."""

    def test_all_yes_still_publishes(self) -> None:
        report = _run_tmp(
            _sdcl_t2_acts(
                box2a=None, close_2a=True, eligible_txn=True,
                adoption_file="adopt-core-v12-current.json",
            ),
            "demo.sdcl.t2.v12.positive",
            registry="published-packages.v7.json",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[SD_ATTACHMENT]["disposition"], "published")
        self.assertEqual(rows[SELECTED_BASE_RULE]["disposition"], "published")


class AttachmentLifecycleCorrection(unittest.TestCase):
    """ADR-0055 T0->T1->T2: the attachment's disposition now changes in
    step with a correction that flips real-world eligibility, instead of
    staying invariant across it."""

    def test_correction_converges_attachment_from_blocked_to_published(self) -> None:
        boundary: dict[str, str | None] = {name: "yes" for name in BOUNDARY_DECLARATIONS}
        boundary["tax.us.2025.schedule-d-boundary.no-current-capital-losses"] = "no"
        report_t0 = _run_tmp(
            _sdcl_t2_acts(
                box2a=None, close_2a=True, eligible_txn=True, boundary=boundary,
                adoption_file="adopt-core-v12-current.json",
            ),
            "demo.sdcl.t2.v12.lifecycle-t0",
            registry="published-packages.v7.json",
        )
        rows_t0 = _by_artifact(report_t0)
        self.assertEqual(rows_t0[SD_ATTACHMENT]["disposition"], "blocked")
        self.assertEqual(rows_t0[SD_ATTACHMENT]["code"], "COMPLETENESS_VALUE_VIOLATION")

        report_t2 = _run_tmp(
            _sdcl_t2_acts(
                box2a=None, close_2a=True, eligible_txn=True, boundary=boundary,
                adoption_file="adopt-core-v12-current.json",
                correction={"tax.us.2025.schedule-d-boundary.no-current-capital-losses": "yes"},
            ),
            "demo.sdcl.t2.v12.lifecycle-t2",
            registry="published-packages.v7.json",
        )
        rows_t2 = _by_artifact(report_t2)
        self.assertEqual(rows_t2[SD_ATTACHMENT]["disposition"], "published")
        self.assertEqual(rows_t2[SELECTED_BASE_RULE]["disposition"], "published")


if __name__ == "__main__":
    unittest.main()
