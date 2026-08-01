"""Production-shaped K1-P/K1-N evidence through ``live_coordinate_run``."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from tests.test_capital_gain_distributions_line7a_t2_coordinator import _cgd_t2_acts


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "k1_interest_breadth"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v4.json",
        CONTENT,
    )


def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.k1.breadth.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-07-31T12:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _attested(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def _k1_acts(
    *,
    k1_values: list[float],
    close_k1: bool = True,
    box1_interest: float | None = None,
    dividends: float = 0,
    complete_schedule_b: bool = True,
) -> list[dict[str, object]]:
    acts = _cgd_t2_acts(
        box1a=dividends,
        box1b=0,
        box2a=None,
        close_2a=True,
        cg_dist="no",
    )
    acts.pop()  # replace historical v7 adoption with the v9 route

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    for name in ("form1065-k1.bundle.json", "scheduleb.bundle.json"):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text("utf-8"))})

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.k1.partnership", "kind": "tax.us.partnership", "label": "Synthetic partnership"}})
    for index in range(max(1, len(k1_values))):
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": f"demo.k1.statement.{index}", "kind": "tax.us.form1065-k1-statement", "label": f"Synthetic Form-1065 K-1 statement {index}"}})
    if box1_interest is not None:
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.k1.bank", "kind": "tax.us.interest-payer", "label": "Synthetic bank"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.k1.1099int", "kind": "tax.us.1099int-statement", "label": "Synthetic Form 1099-INT"}})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    add("horizon-genesis", {"family": {"id": "tax.us.2025.form1065-k1.box5", "version": "v1"}, "scope": scope, "horizon_id": "demo.k1.h0"})
    horizon = "demo.k1.h0"
    for index, value in enumerate(k1_values):
        evidence_id = f"demo.k1.evidence.{index}"
        contribution_id = f"demo.k1.contribution.{index}"
        add("evidence-submitted", {"evidence": {"schema": "evidence.v1", "id": evidence_id, "kind": "demo.statement.form1065-k1", "label": f"Synthetic Form-1065 K-1 box 5 item {index}", "content": {"value": value}}})
        add("contribution", {"contribution": {"schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id, "content": {"mode": "manual-entry", "synthetic": True}}})
        successor = f"demo.k1.h{index + 1}"
        add("member-transition", {
            "family": {"id": "tax.us.2025.form1065-k1.box5", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2",
                "id": f"demo.k1.finding.{index}",
                "fact_id": f"tax.us.2025.form1065-k1.box5-interest|partnership=demo.k1.partnership,k1-statement=demo.k1.statement.{index},tax-year=2025",
                "value": value,
                "basis": "documentary",
                "evidence_ids": [evidence_id],
                "contribution_id": contribution_id,
            }},
            "successor": {"id": successor, "predecessor": horizon},
        })
        horizon = successor

    if box1_interest is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": "demo.k1.finding.1099int",
                "fact_id": "tax.us.2025.f1099int.box1-interest|payer=demo.k1.bank,statement=demo.k1.1099int,tax-year=2025",
                "value": box1_interest, "basis": "attested", "evidence_ids": [],
            }},
            "successor": {"id": "demo.k1.int-b1.h1", "predecessor": "demo.cgd.t2.int-b1.h0"},
        })
        add("assertion", {"finding": _attested("demo.k1.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure|family-horizon=demo.k1.int-b1.h1,tax-year=2025", True)})

    if close_k1:
        add("assertion", {"finding": _attested("demo.k1.closure", f"tax.us.2025.form1065-k1.box5.source-closure|family-horizon={horizon},tax-year=2025", True)})
    if complete_schedule_b:
        add("assertion", {"finding": _attested("demo.k1.scheduleb.foreign-account", "tax.us.2025.scheduleb.foreign-account|tax-year=2025", "no")})
        add("assertion", {"finding": _attested("demo.k1.scheduleb.foreign-trust", "tax.us.2025.scheduleb.foreign-trust|tax-year=2025", "no")})

    adoption = cast(dict[str, object], json.loads((FIXTURES / "adoptions" / "adopt-core-v9-current.json").read_text("utf-8")))
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _run(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    with TemporaryDirectory() as tmp:
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
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
        assert result.output_path is not None and result.presentation_path is not None
        return json.loads(result.output_path.read_text()), json.loads(result.presentation_path.read_text())


def _section(model: dict[str, Any], section_id: str) -> dict[str, Any]:
    return next(section for section in model["sections"] if section["id"] == section_id)


class PositiveLineAndIdentityCases(unittest.TestCase):
    def test_k1_p1_single_member_recomputes_line2b_and_line9(self) -> None:
        """K1-P1: one $80 K-1 reaches cited line 2b and downstream line 9."""
        _, model = _run(_k1_acts(k1_values=[80]), "demo.k1.p1")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 80)
        self.assertEqual(_section(model, "line-9")["resolved"]["value"], 90080)
        sites = _section(model, "line-2b")["citationSites"]
        self.assertIn("demo.k1.finding.0", {site["pinId"] for site in sites})

    def test_k1_p2_mixed_1099int_and_k1_remain_distinct(self) -> None:
        """K1-P2: $1,000 Form 1099-INT plus $80 K-1 publishes $1,080."""
        _, model = _run(_k1_acts(k1_values=[80], box1_interest=1000), "demo.k1.p2")
        line2b = _section(model, "line-2b")
        self.assertEqual(line2b["resolved"]["value"], 1080)
        pin_ids = {site["pinId"] for site in line2b["citationSites"]}
        self.assertIn("demo.k1.finding.0", pin_ids)
        self.assertIn("demo.k1.finding.1099int", pin_ids)

    def test_k1_p3_same_partnership_originals_count_once_each(self) -> None:
        """K1-P3: two logical statements from one partnership stay distinct."""
        _, model = _run(_k1_acts(k1_values=[30, 50]), "demo.k1.p3")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 80)
        sites = _section(model, "line-2b")["citationSites"]
        self.assertTrue({"demo.k1.finding.0", "demo.k1.finding.1"} <= {s["pinId"] for s in sites})

    def test_k1_p4_correction_preserves_fact_identity_and_replaces_value(self) -> None:
        """K1-P4: correction on one logical K-1 changes $80 to $90."""
        acts = _k1_acts(k1_values=[80])
        evidence_id = "demo.k1.evidence.correction"
        contribution_id = "demo.k1.contribution.correction"
        acts.append(_act(len(acts), "evidence-submitted", {"evidence": {"schema": "evidence.v1", "id": evidence_id, "kind": "demo.statement.form1065-k1", "label": "Synthetic corrected Form-1065 K-1", "content": {"value": 90}}}))
        acts.append(_act(len(acts), "contribution", {"contribution": {"schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id, "content": {"mode": "manual-entry", "synthetic": True}}}))
        acts.append(_act(len(acts), "assertion", {"finding": {
            "schema": "finding.v2", "id": "demo.k1.finding.correction",
            "fact_id": "tax.us.2025.form1065-k1.box5-interest|partnership=demo.k1.partnership,k1-statement=demo.k1.statement.0,tax-year=2025",
            "value": 90, "basis": "documentary", "evidence_ids": [evidence_id], "contribution_id": contribution_id,
        }}))
        from packages.kernel.currency import compute_currency
        from packages.kernel.findings import project
        from packages.derivation.loader import DerivationSchemas

        currency = compute_currency(project(tuple(acts), DerivationSchemas().registry))
        self.assertIn("demo.k1.finding.0", currency.displaced_finding_ids)
        self.assertIn("demo.k1.finding.correction", currency.current_finding_ids)
        _, model = _run(acts, "demo.k1.p4")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 90)
        self.assertIn("demo.k1.finding.correction", {s["pinId"] for s in _section(model, "line-2b")["citationSites"]})


class ClosureAndScheduleBCases(unittest.TestCase):
    def test_k1_p5_closed_empty_is_honest_zero(self) -> None:
        """K1-P5: closed-empty K-1 publishes zero without changing siblings."""
        _, model = _run(_k1_acts(k1_values=[]), "demo.k1.p5")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 0)

    def test_k1_p6_exact_threshold_is_not_required(self) -> None:
        """K1-P6: exactly $1,500 preserves strict-greater-than behavior."""
        _, model = _run(_k1_acts(k1_values=[1500]), "demo.k1.p6")
        self.assertEqual(model["citationGroups"], [])

    def test_k1_p7_k1_alone_over_threshold_itemizes(self) -> None:
        """K1-P7: $1,501 K-1 requires Schedule B and exposes the K-1 row."""
        _, model = _run(_k1_acts(k1_values=[1501]), "demo.k1.p7")
        group = next(group for group in model["citationGroups"] if group["id"] == "tax.us.2025.rule.attachment.schedule-b")
        part_i = next(part for part in group["parts"] if part["heading"] == "Part I: Taxable Interest")
        self.assertIn("demo.k1.finding.0", {site["pinId"] for site in part_i["citationSites"]})

    def test_k1_p8_combined_threshold_itemizes_both_families(self) -> None:
        """K1-P8: $1,000 Form 1099-INT plus $600 K-1 ties to $1,600."""
        _, model = _run(_k1_acts(k1_values=[600], box1_interest=1000), "demo.k1.p8")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 1600)
        part_i = model["citationGroups"][0]["parts"][0]
        self.assertTrue({"demo.k1.finding.0", "demo.k1.finding.1099int"} <= {s["pinId"] for s in part_i["citationSites"]})

    def test_k1_p9_dividend_trigger_still_includes_k1_rows(self) -> None:
        """K1-P9: a dividend trigger does not suppress current Part-I rows."""
        _, model = _run(_k1_acts(k1_values=[80], dividends=2000), "demo.k1.p9")
        part_i = model["citationGroups"][0]["parts"][0]
        self.assertIn("demo.k1.finding.0", {site["pinId"] for site in part_i["citationSites"]})

    def test_k1_n1_unclosed_family_blocks_line2b_and_downstream(self) -> None:
        """K1-N1: no current K-1 closure blocks line 2b and line 9."""
        _, model = _run(_k1_acts(k1_values=[80], close_k1=False), "demo.k1.n1")
        self.assertEqual(_section(model, "line-2b")["resolved"]["disposition"], "blocked")
        self.assertEqual(_section(model, "line-9")["resolved"]["disposition"], "blocked")

    def test_k1_n2_late_member_displaces_old_closure_until_reclosed(self) -> None:
        """K1-N2: successor horizon closure is required after a late member."""
        acts = _k1_acts(k1_values=[80])
        scope = {"tax-year": "2025", "subject": "demo.primary"}
        acts.append(_act(len(acts), "entity-introduced", {"entity": {
            "schema": "entity.v1", "id": "demo.k1.statement.late",
            "kind": "tax.us.form1065-k1-statement", "label": "Synthetic late Form-1065 K-1",
        }}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": "tax.us.2025.form1065-k1.box5", "version": "v1"}, "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": "demo.k1.finding.late",
                "fact_id": "tax.us.2025.form1065-k1.box5-interest|partnership=demo.k1.partnership,k1-statement=demo.k1.statement.late,tax-year=2025",
                "value": 20, "basis": "attested", "evidence_ids": [],
            }},
            "successor": {"id": "demo.k1.h2", "predecessor": "demo.k1.h1"},
        }))
        _, blocked = _run(acts, "demo.k1.n2.blocked")
        self.assertEqual(_section(blocked, "line-2b")["resolved"]["disposition"], "blocked")
        acts.append(_act(len(acts), "assertion", {"finding": _attested("demo.k1.closure.h2", "tax.us.2025.form1065-k1.box5.source-closure|family-horizon=demo.k1.h2,tax-year=2025", True)}))
        _, restored = _run(acts, "demo.k1.n2.restored")
        self.assertEqual(_section(restored, "line-2b")["resolved"]["value"], 100)


class PresentationContainment(unittest.TestCase):
    def test_k1_n13_non_numeric_k1_section_is_redacted_without_sibling_loss(self) -> None:
        """K1-N13: existing per-section renderer contains malformed numeric data."""
        from tools.generate_k1_interest_breadth_goldens import MALFORMED_TARGET

        _, model = _run(_k1_acts(k1_values=[80]), "demo.k1.n13")
        malformed = copy.deepcopy(model)
        _section(malformed, "line-2b")["resolved"]["value"] = "rejected-k1-value"
        self.assertIsInstance(_section(malformed, "line-9")["resolved"]["value"], (int, float))
        renderer = (ROOT / "tools" / "presentation_harness" / "examples" / "pages" / "citation-walk.v1.html").read_text("utf-8")
        self.assertIn('throw new SectionError("invalid-numeric-value")', renderer)
        self.assertIn("function renderSafely", renderer)
        self.assertIn("for (const section of FIXTURE.sections || [])", renderer)
        committed = json.loads(MALFORMED_TARGET.read_text("utf-8"))
        self.assertEqual(_section(committed, "line-2b")["resolved"]["value"], "rejected-k1-value")
        self.assertIsInstance(_section(committed, "line-9")["resolved"]["value"], (int, float))

    def test_k1_p1_p2_committed_golden_is_live_deterministic(self) -> None:
        """K1-P1 K1-P2: committed presentation is the coordinator result."""
        from tools.generate_k1_interest_breadth_goldens import TARGET, regenerate

        self.assertEqual(json.loads(TARGET.read_text("utf-8")), regenerate())


if __name__ == "__main__":
    unittest.main()
