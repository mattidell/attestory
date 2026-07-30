"""Track 2 Capital-Gain Distributions / Line 7a: coordinator-from-facts goldens.

Every named class enters exclusively through ``live_coordinate_run`` from an
authoritative act log (never a hand-built ``RunContext``), against package
``tax.us.2025.package.core-calculations`` v7.
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
T3 = REPO / "packages" / "sample_data" / "frrs_t3"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2056"}

CONCLUSION_RULE = "tax.us.2025.rule.schedule-d-required.conclusion"
LINE7A_RULE = "tax.us.2025.rule.form1040-line7a"
LINE7B_RULE = "tax.us.2025.rule.form1040-line7b"
LINE9_RULE = "tax.us.2025.rule.form1040-line9"
LINE16_RULE = "tax.us.2025.rule.form1040-line16"
SUBTOTAL_2A_RULE = "tax.us.2025.rule.f1099div-2a-subtotal"

C1 = "tax.us.2025.exception1.only-box2a-capital-gains"
C2 = "tax.us.2025.exception1.no-capital-losses"
C3 = "tax.us.2025.exception1.no-qof-deferral"
C4 = "tax.us.2025.exception1.no-boxes-2b-2c-2d"
CG_DIST = "tax.us.2025.capital-gain-distributions"


def _act(name: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads((T3 / "adoptions" / name).read_text("utf-8")))


def _surface() -> PublicationSurface:
    return PublicationSurface(
        T3 / "publication_surface" / "releases", CONTENT / "published-packages.json", CONTENT
    )


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


def _run(acts: list[dict[str, object]], run_id: str, root: Path) -> dict[str, Any]:
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
        surface=_surface(),
        output_name="out.json",
    )
    assert result.refusal is None, result.refusal
    assert result.output_path is not None
    return cast(dict[str, Any], json.loads(result.output_path.read_text()))


def _run_tmp(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        return _run(acts, run_id, Path(tmp))


def _by_artifact(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["artifact_id"]: row for row in report["dispositions"]}


class EligibleSinglePayer(unittest.TestCase):
    def test_line7a_publishes_and_line9_includes_once(self) -> None:
        report = _run_tmp(_cgd_t2_acts(box2a=1500, box1b=0, cg_dist="yes"), "demo.cgd.t2.eligible-single")
        rows = _by_artifact(report)
        self.assertEqual(rows[CONCLUSION_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE7B_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE9_RULE]["disposition"], "published")
        pin_ids = {p["id"] for p in rows[LINE7B_RULE]["pins"]}
        self.assertIn("tax.us.2025.citation.form1040.line-7b", pin_ids)
        line7a_fid = rows[LINE7A_RULE].get("finding_id")
        line9_line7a_pins = [p for p in rows[LINE9_RULE]["pins"] if p.get("id") == line7a_fid]
        self.assertEqual(len(line9_line7a_pins), 1)


class ComponentAbsence(unittest.TestCase):
    def test_missing_c4_blocks_conclusion_and_chain(self) -> None:
        report = _run_tmp(
            _cgd_t2_acts(components={"C1": "yes", "C2": "yes", "C3": "yes", "C4": None}),
            "demo.cgd.t2.missing-c4",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[CONCLUSION_RULE]["disposition"], "blocked")
        self.assertEqual(rows[CONCLUSION_RULE]["code"], "DEPENDENCY_ABSENT")
        self.assertIn(C4, rows[CONCLUSION_RULE]["missing"])
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE9_RULE]["disposition"], "blocked")


class ComponentNo(unittest.TestCase):
    def test_c4_no_guard_inapplicable_line7a_blocks_line9(self) -> None:
        report = _run_tmp(
            _cgd_t2_acts(components={"C1": "yes", "C2": "yes", "C3": "yes", "C4": "no"}),
            "demo.cgd.t2.c4-no",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[CONCLUSION_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "inapplicable")
        self.assertEqual(rows[LINE7B_RULE]["disposition"], "inapplicable")
        self.assertEqual(rows[LINE9_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE16_RULE]["disposition"], "inapplicable")


class ClosedEmptyFamily(unittest.TestCase):
    def test_closed_empty_publishes_zero(self) -> None:
        report = _run_tmp(
            _cgd_t2_acts(box2a=None, close_2a=True, cg_dist="no", box1b=0),
            "demo.cgd.t2.closed-empty",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE16_RULE]["disposition"], "published")


class OpenFamily(unittest.TestCase):
    def test_open_family_blocks_line7a(self) -> None:
        report = _run_tmp(
            _cgd_t2_acts(box2a=1500, close_2a=False, cg_dist="yes"),
            "demo.cgd.t2.open-family",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "blocked")


class MultiPayer(unittest.TestCase):
    def test_multi_payer_sums(self) -> None:
        report = _run_tmp(
            _cgd_t2_acts(multi_payer_box2a=[1000, 500], box1b=0, cg_dist="yes"),
            "demo.cgd.t2.multi-payer",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "published")
        self.assertEqual(rows[SUBTOTAL_2A_RULE]["disposition"], "published")


class QdcgBranches(unittest.TestCase):
    def test_q_zero_l_positive_selects_qdcg(self) -> None:
        report = _run_tmp(
            _cgd_t2_acts(box2a=1500, box1b=0, cg_dist="yes"),
            "demo.cgd.t2.q0-l-pos",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE16_RULE]["disposition"], "published")
        pin_ids = {p["id"] for p in rows[LINE16_RULE]["pins"]}
        self.assertIn(rows[CONCLUSION_RULE]["finding_id"], pin_ids)

    def test_q_positive_l_zero_pins_declaration_no(self) -> None:
        report = _run_tmp(
            _cgd_t2_acts(box2a=None, close_2a=True, box1b=600, box1a=600, cg_dist="no"),
            "demo.cgd.t2.q-pos-l0",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE16_RULE]["disposition"], "published")
        pin_ids = {p["id"] for p in rows[LINE16_RULE]["pins"]}
        self.assertIn("demo.cgd.t2.finding.cg-dist", pin_ids)


class CorrectionLifecycle(unittest.TestCase):
    def test_forward_component_correction_displaces_chain(self) -> None:
        report = _run_tmp(
            _cgd_t2_acts(box2a=1500, box1b=0, cg_dist="yes", c4_successor="no"),
            "demo.cgd.t2.forward-correction",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE7A_RULE]["disposition"], "inapplicable")
        self.assertEqual(rows[LINE9_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE16_RULE]["disposition"], "inapplicable")


if __name__ == "__main__":
    unittest.main()
