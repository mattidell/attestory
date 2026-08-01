"""Production-shaped MD-P/MD-N evidence through ``live_coordinate_run``."""

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
FIXTURES = ROOT / "packages" / "sample_data" / "market_discount_interest"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v5.json",
        CONTENT,
    )


def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.md.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-08-01T12:{index // 60:02d}:{index % 60:02d}Z",
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


def _md_acts(
    *,
    b10_values: list[float] | None = None,
    oid5_values: list[float] | None = None,
    close_b10: bool = True,
    close_oid5: bool = True,
    box1_interest: float | None = None,
    dividends: float = 0,
    complete_schedule_b: bool = True,
) -> list[dict[str, object]]:
    b10_values = [] if b10_values is None else b10_values
    oid5_values = [] if oid5_values is None else oid5_values
    acts = _cgd_t2_acts(box1a=dividends, box1b=0, box2a=None, close_2a=True, cg_dist="no")
    acts.pop()  # replace historical v7 adoption with the v10 route

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    for name in ("f1099int-b10.bundle.json", "f1099oid-b5.bundle.json", "form1065-k1.bundle.json", "scheduleb.bundle.json"):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text("utf-8"))})

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.md.payer", "kind": "tax.us.interest-payer", "label": "Synthetic broker"}})
    for index in range(max(1, len(b10_values))):
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": f"demo.md.b10.stmt.{index}", "kind": "tax.us.1099int-statement", "label": f"Synthetic Form 1099-INT box-10 statement {index}"}})
    for index in range(max(1, len(oid5_values))):
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": f"demo.md.oid5.stmt.{index}", "kind": "tax.us.1099oid-statement", "label": f"Synthetic Form 1099-OID box-5 statement {index}"}})
    if box1_interest is not None:
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.md.bank", "kind": "tax.us.interest-payer", "label": "Synthetic bank"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.md.1099int", "kind": "tax.us.1099int-statement", "label": "Synthetic Form 1099-INT"}})

    add("horizon-genesis", {"family": {"id": "tax.us.2025.f1099int.b10", "version": "v1"}, "scope": SCOPE_KEY, "horizon_id": "demo.md.b10.h0"})
    add("horizon-genesis", {"family": {"id": "tax.us.2025.f1099oid.b5", "version": "v1"}, "scope": SCOPE_KEY, "horizon_id": "demo.md.oid5.h0"})
    add("horizon-genesis", {"family": {"id": "tax.us.2025.form1065-k1.box5", "version": "v1"}, "scope": SCOPE_KEY, "horizon_id": "demo.md.k1.h0"})

    b10_horizon = "demo.md.b10.h0"
    for index, value in enumerate(b10_values):
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099int.b10", "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {"action": "assert", "finding": _attested(
                f"demo.md.finding.b10.{index}",
                f"tax.us.2025.f1099int.box10-market-discount|payer=demo.md.payer,statement=demo.md.b10.stmt.{index},tax-year=2025",
                value,
            )},
            "successor": {"id": f"demo.md.b10.h{index + 1}", "predecessor": b10_horizon},
        })
        b10_horizon = f"demo.md.b10.h{index + 1}"

    oid5_horizon = "demo.md.oid5.h0"
    for index, value in enumerate(oid5_values):
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099oid.b5", "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {"action": "assert", "finding": _attested(
                f"demo.md.finding.oid5.{index}",
                f"tax.us.2025.f1099oid.box5-market-discount|payer=demo.md.payer,statement=demo.md.oid5.stmt.{index},tax-year=2025",
                value,
            )},
            "successor": {"id": f"demo.md.oid5.h{index + 1}", "predecessor": oid5_horizon},
        })
        oid5_horizon = f"demo.md.oid5.h{index + 1}"

    if box1_interest is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": "demo.md.finding.1099int",
                "fact_id": "tax.us.2025.f1099int.box1-interest|payer=demo.md.bank,statement=demo.md.1099int,tax-year=2025",
                "value": box1_interest, "basis": "attested", "evidence_ids": [],
            }},
            "successor": {"id": "demo.md.int-b1.h1", "predecessor": "demo.cgd.t2.int-b1.h0"},
        })
        add("assertion", {"finding": _attested("demo.md.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure|family-horizon=demo.md.int-b1.h1,tax-year=2025", True)})

    if close_b10:
        add("assertion", {"finding": _attested("demo.md.closure.b10", f"tax.us.2025.f1099int.b10.source-closure|family-horizon={b10_horizon},tax-year=2025", True)})
    if close_oid5:
        add("assertion", {"finding": _attested("demo.md.closure.oid5", f"tax.us.2025.f1099oid.b5.source-closure|family-horizon={oid5_horizon},tax-year=2025", True)})
    add("assertion", {"finding": _attested("demo.md.closure.k1", "tax.us.2025.form1065-k1.box5.source-closure|family-horizon=demo.md.k1.h0,tax-year=2025", True)})
    if complete_schedule_b:
        add("assertion", {"finding": _attested("demo.md.scheduleb.foreign-account", "tax.us.2025.scheduleb.foreign-account|tax-year=2025", "no")})
        add("assertion", {"finding": _attested("demo.md.scheduleb.foreign-trust", "tax.us.2025.scheduleb.foreign-trust|tax-year=2025", "no")})

    adoption = cast(dict[str, object], json.loads((FIXTURES / "adoptions" / "adopt-core-v10-current.json").read_text("utf-8")))
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
    def test_md_p1_box10_member_reaches_line2b(self) -> None:
        """MD-P1: one $80 box-10 market-discount item reaches line 2b."""
        _, model = _run(_md_acts(b10_values=[80]), "demo.md.p1")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 80)
        sites = _section(model, "line-2b")["citationSites"]
        self.assertIn("demo.md.finding.b10.0", {site["pinId"] for site in sites})

    def test_md_p2_oid_box5_member_reaches_line2b(self) -> None:
        """MD-P2: one $65 box-5 OID market-discount item reaches line 2b."""
        _, model = _run(_md_acts(oid5_values=[65]), "demo.md.p2")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 65)
        sites = _section(model, "line-2b")["citationSites"]
        self.assertIn("demo.md.finding.oid5.0", {site["pinId"] for site in sites})

    def test_md_p3_both_routes_contribute_once_each(self) -> None:
        """MD-P3: a box-10 item and a box-5 item both count, once each."""
        _, model = _run(_md_acts(b10_values=[30], oid5_values=[50]), "demo.md.p3")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 80)
        pin_ids = {site["pinId"] for site in _section(model, "line-2b")["citationSites"]}
        self.assertIn("demo.md.finding.b10.0", pin_ids)
        self.assertIn("demo.md.finding.oid5.0", pin_ids)

    def test_md_p4_existing_interest_plus_market_discount_sums(self) -> None:
        """MD-P4: $1,000 ordinary box-1 interest plus $80 box-10 market discount."""
        _, model = _run(_md_acts(b10_values=[80], box1_interest=1000), "demo.md.p4")
        line2b = _section(model, "line-2b")
        self.assertEqual(line2b["resolved"]["value"], 1080)
        pin_ids = {site["pinId"] for site in line2b["citationSites"]}
        self.assertIn("demo.md.finding.b10.0", pin_ids)
        self.assertIn("demo.md.finding.1099int", pin_ids)

    def test_md_p5_two_original_statements_stay_distinct(self) -> None:
        """MD-P5: two original box-10 statements from one payer both contribute."""
        _, model = _run(_md_acts(b10_values=[30, 50]), "demo.md.p5")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 80)
        sites = _section(model, "line-2b")["citationSites"]
        self.assertTrue({"demo.md.finding.b10.0", "demo.md.finding.b10.1"} <= {s["pinId"] for s in sites})

    def test_md_p6_correction_preserves_fact_identity_and_replaces_value(self) -> None:
        """MD-P6: a corrected box-10 statement changes $80 to $90 on the same logical id."""
        acts = _md_acts(b10_values=[80])
        acts.append(_act(len(acts), "assertion", {"finding": _attested(
            "demo.md.finding.correction",
            "tax.us.2025.f1099int.box10-market-discount|payer=demo.md.payer,statement=demo.md.b10.stmt.0,tax-year=2025",
            90,
        )}))
        from packages.kernel.currency import compute_currency
        from packages.kernel.findings import project
        from packages.derivation.loader import DerivationSchemas

        currency = compute_currency(project(tuple(acts), DerivationSchemas().registry))
        self.assertIn("demo.md.finding.b10.0", currency.displaced_finding_ids)
        self.assertIn("demo.md.finding.correction", currency.current_finding_ids)
        _, model = _run(acts, "demo.md.p6")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 90)
        self.assertIn("demo.md.finding.correction", {s["pinId"] for s in _section(model, "line-2b")["citationSites"]})


class ClosureAndScheduleBCases(unittest.TestCase):
    def test_md_p7_both_families_closed_empty_is_honest_zero(self) -> None:
        """MD-P7: closed-empty market-discount families publish an unchanged zero."""
        _, model = _run(_md_acts(b10_values=[], oid5_values=[]), "demo.md.p7")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 0)

    def test_md_p8_threshold_and_dividend_trigger_still_itemize(self) -> None:
        """MD-P8: a market-discount amount that crosses the $1,500 threshold itemizes."""
        _, model = _run(_md_acts(b10_values=[1501]), "demo.md.p8")
        group = next(group for group in model["citationGroups"] if group["id"] == "tax.us.2025.rule.attachment.schedule-b")
        part_i = next(part for part in group["parts"] if part["heading"] == "Part I: Taxable Interest")
        self.assertIn("demo.md.finding.b10.0", {site["pinId"] for site in part_i["citationSites"]})

    def test_md_p9_dividend_trigger_does_not_suppress_market_discount_rows(self) -> None:
        """MD-P9: a dividend-only trigger still exposes current market-discount rows."""
        _, model = _run(_md_acts(oid5_values=[80], dividends=2000), "demo.md.p9")
        part_i = model["citationGroups"][0]["parts"][0]
        self.assertIn("demo.md.finding.oid5.0", {site["pinId"] for site in part_i["citationSites"]})

    def test_md_n1_unclosed_family_blocks_line2b_and_downstream(self) -> None:
        """MD-N1: no current box-10 closure blocks line 2b and line 9."""
        _, model = _run(_md_acts(b10_values=[80], close_b10=False), "demo.md.n1.b10")
        self.assertEqual(_section(model, "line-2b")["resolved"]["disposition"], "blocked")
        self.assertEqual(_section(model, "line-9")["resolved"]["disposition"], "blocked")

    def test_md_n1_unclosed_oid_family_blocks_line2b(self) -> None:
        """MD-N1: no current box-5 closure blocks line 2b even with box-10 closed."""
        _, model = _run(_md_acts(oid5_values=[80], close_oid5=False), "demo.md.n1.oid5")
        self.assertEqual(_section(model, "line-2b")["resolved"]["disposition"], "blocked")

    def test_md_n2_late_member_displaces_old_closure_until_reclosed(self) -> None:
        """MD-N2: a late box-10 member reopens the family until re-closure."""
        acts = _md_acts(b10_values=[80])
        acts.append(_act(len(acts), "entity-introduced", {"entity": {
            "schema": "entity.v1", "id": "demo.md.b10.stmt.late",
            "kind": "tax.us.1099int-statement", "label": "Synthetic late box-10 statement",
        }}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": "tax.us.2025.f1099int.b10", "version": "v1"}, "scope": SCOPE_KEY,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": "demo.md.finding.late",
                "fact_id": "tax.us.2025.f1099int.box10-market-discount|payer=demo.md.payer,statement=demo.md.b10.stmt.late,tax-year=2025",
                "value": 20, "basis": "attested", "evidence_ids": [],
            }},
            "successor": {"id": "demo.md.b10.h2", "predecessor": "demo.md.b10.h1"},
        }))
        _, blocked = _run(acts, "demo.md.n2.blocked")
        self.assertEqual(_section(blocked, "line-2b")["resolved"]["disposition"], "blocked")
        acts.append(_act(len(acts), "assertion", {"finding": _attested("demo.md.closure.b10.h2", "tax.us.2025.f1099int.b10.source-closure|family-horizon=demo.md.b10.h2,tax-year=2025", True)}))
        _, restored = _run(acts, "demo.md.n2.restored")
        self.assertEqual(_section(restored, "line-2b")["resolved"]["value"], 100)


class PresentationContainment(unittest.TestCase):
    def test_md_n12_non_numeric_market_discount_section_is_redacted_without_sibling_loss(self) -> None:
        """MD-N12: existing per-section renderer contains malformed numeric data."""
        from tools.generate_market_discount_interest_goldens import MALFORMED_TARGET

        _, model = _run(_md_acts(b10_values=[80], oid5_values=[65]), "demo.md.n12")
        malformed = copy.deepcopy(model)
        _section(malformed, "line-2b")["resolved"]["value"] = "rejected-md-value"
        self.assertIsInstance(_section(malformed, "line-9")["resolved"]["value"], (int, float))
        renderer = (ROOT / "tools" / "presentation_harness" / "examples" / "pages" / "citation-walk.v1.html").read_text("utf-8")
        self.assertIn('throw new SectionError("invalid-numeric-value")', renderer)
        committed = json.loads(MALFORMED_TARGET.read_text("utf-8"))
        self.assertEqual(_section(committed, "line-2b")["resolved"]["value"], "rejected-md-value")
        self.assertIsInstance(_section(committed, "line-9")["resolved"]["value"], (int, float))

    def test_md_p10_committed_golden_is_live_deterministic(self) -> None:
        """MD-P10: committed presentation is the coordinator result."""
        from tools.generate_market_discount_interest_goldens import TARGET, regenerate

        self.assertEqual(json.loads(TARGET.read_text("utf-8")), regenerate())


if __name__ == "__main__":
    unittest.main()
